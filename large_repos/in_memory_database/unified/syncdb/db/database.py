"""
Core in-memory database engine implementation.
"""
from typing import Dict, List, Any, Optional, Tuple, Callable, Set
import copy
from common.core import (
    BaseComponent, PerformanceTrackingMixin, ThreadSafeDict,
    generate_id, get_timestamp, validate_non_empty
)
from .schema import DatabaseSchema, TableSchema


class Table(BaseComponent, PerformanceTrackingMixin):
    """
    A database table that stores records in memory.
    """
    def __init__(self, schema: TableSchema, **config):
        super().__init__(**config)
        self.schema = schema
        self.records = ThreadSafeDict()  # Use thread-safe dictionary
        self.record_timestamps = ThreadSafeDict()  # Use thread-safe dictionary for record timestamps
        self.change_log: List[Dict[str, Any]] = []
        self.index_counter = 0  # Used for assigning sequential IDs to changes
    
    def _get_primary_key_tuple(self, record: Dict[str, Any]) -> Tuple:
        """Extract primary key values as a tuple for indexing."""
        return tuple(record[pk] for pk in self.schema.primary_keys)
    
    def _validate_record(self, record: Dict[str, Any]) -> None:
        """Validate a record against the schema and raise exception if invalid."""
        errors = self.schema.validate_record(record)
        if errors:
            raise ValueError(f"Invalid record: {', '.join(errors)}")
    
    def insert(self, record: Dict[str, Any], client_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Insert a new record into the table.
        Returns the inserted record.
        """
        start_time = get_timestamp()
        try:
            with self._lock:  # Use thread safety from BaseComponent
                self._validate_record(record)
                pk_tuple = self._get_primary_key_tuple(record)

                if pk_tuple in self.records:
                    raise ValueError(f"Record with primary key {pk_tuple} already exists")

                # Create a copy to avoid modifying the original
                stored_record = copy.deepcopy(record)

                # Apply default values for missing fields
                for column in self.schema.columns:
                    if column.name not in stored_record and column.default is not None:
                        stored_record[column.name] = column.default() if callable(column.default) else column.default

                self.records[pk_tuple] = stored_record
                current_time = get_timestamp()
                self.record_timestamps[pk_tuple] = current_time

                # Record the change in the log
                self._record_change("insert", pk_tuple, None, stored_record, client_id)
                
                self._touch()  # From TimestampedMixin
                return stored_record
        finally:
            # Track performance
            duration = get_timestamp() - start_time
            self.track_operation("insert", duration)
    
    def update(self, record: Dict[str, Any], client_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing record in the table.
        Returns the updated record.
        """
        start_time = get_timestamp()
        try:
            with self._lock:  # Use thread safety from BaseComponent
                self._validate_record(record)
                pk_tuple = self._get_primary_key_tuple(record)
                
                if pk_tuple not in self.records:
                    raise ValueError(f"Record with primary key {pk_tuple} does not exist")
                
                # Get the old record before updating
                old_record = copy.deepcopy(self.records[pk_tuple])
                
                # Create a copy to avoid modifying the original
                stored_record = copy.deepcopy(record)
                self.records[pk_tuple] = stored_record
                current_time = get_timestamp()
                self.record_timestamps[pk_tuple] = current_time
                
                # Record the change in the log
                self._record_change("update", pk_tuple, old_record, stored_record, client_id)
                
                self._touch()  # From TimestampedMixin
                return stored_record
        finally:
            # Track performance
            duration = get_timestamp() - start_time
            self.track_operation("update", duration)
    
    def delete(self, primary_key_values: List[Any], client_id: Optional[str] = None) -> None:
        """Delete a record from the table by its primary key values."""
        pk_tuple = tuple(primary_key_values)
        
        if pk_tuple not in self.records:
            raise ValueError(f"Record with primary key {pk_tuple} does not exist")
        
        # Get the record before deleting
        old_record = copy.deepcopy(self.records[pk_tuple])
        
        # Remove the record
        del self.records[pk_tuple]
        
        # Record the change in the log
        self._record_change("delete", pk_tuple, old_record, None, client_id)
    
    def get(self, primary_key_values: List[Any]) -> Optional[Dict[str, Any]]:
        """Get a record by its primary key values."""
        pk_tuple = tuple(primary_key_values)
        record = self.records.get(pk_tuple)
        return copy.deepcopy(record) if record else None
    
    def query(self, 
              conditions: Optional[Dict[str, Any]] = None, 
              limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Query records that match the given conditions.
        
        Args:
            conditions: Dictionary of column name to value that records must match
            limit: Maximum number of records to return
            
        Returns:
            List of matching records
        """
        result = []
        
        for record in self.records.values():
            if conditions is None or self._matches_conditions(record, conditions):
                result.append(copy.deepcopy(record))
            
            if limit is not None and len(result) >= limit:
                break
                
        return result
    
    def _matches_conditions(self, record: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
        """Check if a record matches all the given conditions."""
        for col_name, expected_value in conditions.items():
            if col_name not in record or record[col_name] != expected_value:
                return False
        return True
    
    def _record_change(self, 
                      operation: str, 
                      pk_tuple: Tuple, 
                      old_record: Optional[Dict[str, Any]], 
                      new_record: Optional[Dict[str, Any]],
                      client_id: Optional[str] = None) -> None:
        """Record a change in the change log."""
        self.index_counter += 1
        change = {
            "id": self.index_counter,
            "operation": operation,
            "primary_key": pk_tuple,
            "timestamp": get_timestamp(),  # Use common timestamp utility
            "old_record": old_record,
            "new_record": new_record,
            "client_id": client_id or "server"
        }
        self.change_log.append(change)
    
    def get_changes_since(self, index: int) -> List[Dict[str, Any]]:
        """Get all changes that occurred after the given index."""
        return [change for change in self.change_log if change["id"] > index]


class Transaction:
    """
    Manages a database transaction.
    """
    def __init__(self, database: 'Database'):
        self.database = database
        self.tables_snapshot: Dict[str, Dict[Tuple, Dict[str, Any]]] = {}
        self.operations: List[Tuple[str, str, Dict[str, Any]]] = []
        self.committed = False
        self.rolled_back = False
    
    def __enter__(self):
        """Begin the transaction by creating snapshots of tables."""
        for table_name, table in self.database.tables.items():
            # Convert ThreadSafeDict to regular dict for deepcopy
            records_dict = dict(table.records.items())
            self.tables_snapshot[table_name] = copy.deepcopy(records_dict)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Rollback the transaction if not committed and an exception occurred."""
        if exc_type is not None and not self.committed and not self.rolled_back:
            self.rollback()
        return False  # Don't suppress exceptions
    
    def insert(self, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record as part of this transaction."""
        if self.committed or self.rolled_back:
            raise ValueError("Transaction already completed")

        result = self.database.insert(table_name, record, client_id="transaction")
        self.operations.append(("insert", table_name, copy.deepcopy(record)))
        return result

    def update(self, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record as part of this transaction."""
        if self.committed or self.rolled_back:
            raise ValueError("Transaction already completed")

        result = self.database.update(table_name, record, client_id="transaction")
        self.operations.append(("update", table_name, copy.deepcopy(record)))
        return result

    def delete(self, table_name: str, primary_key_values: List[Any]) -> None:
        """Delete a record as part of this transaction."""
        if self.committed or self.rolled_back:
            raise ValueError("Transaction already completed")

        self.database.delete(table_name, primary_key_values, client_id="transaction")
        self.operations.append(("delete", table_name, {"primary_key_values": primary_key_values}))
    
    def commit(self) -> None:
        """Commit the transaction."""
        if self.committed or self.rolled_back:
            raise ValueError("Transaction already completed")
        
        self.committed = True
        # All changes have already been applied to the database tables
        # We just need to mark the transaction as committed
    
    def rollback(self) -> None:
        """Roll back the transaction."""
        if self.committed or self.rolled_back:
            raise ValueError("Transaction already completed")

        # Step 1: Remove any newly added records
        for op_type, table_name, data in self.operations:
            if op_type == "insert":
                # For inserts, we need to remove the record
                table = self.database.tables.get(table_name)
                if table:
                    # Extract the primary key to identify the record
                    primary_keys = self.database.schema.tables[table_name].primary_keys
                    pk_values = [data[pk_name] for pk_name in primary_keys if pk_name in data]
                    if pk_values:
                        pk_tuple = tuple(pk_values)
                        # Remove the record that was inserted
                        if pk_tuple in table.records:
                            del table.records[pk_tuple]
                            # Also remove from record_timestamps
                            if pk_tuple in table.record_timestamps:
                                del table.record_timestamps[pk_tuple]

        # Step 2: Restore previous state for updated records
        for table_name, records_snapshot in self.tables_snapshot.items():
            table = self.database.tables[table_name]
            # Restore all records from the snapshot
            for pk_tuple, record in records_snapshot.items():
                table.records[pk_tuple] = copy.deepcopy(record)

        # Step 3: Remove transaction changes from change logs
        for table_name in self.database.tables:
            table = self.database.tables[table_name]
            # Remove changes with this transaction's client ID
            original_length = len(table.change_log)
            table.change_log = [
                change for change in table.change_log
                if change.get("client_id") != "transaction"
            ]
            # If we removed changes, reset the index counter
            if len(table.change_log) < original_length:
                table.index_counter = max([0] + [c.get("id", 0) for c in table.change_log])

        self.rolled_back = True


class Database(BaseComponent, PerformanceTrackingMixin):
    """
    An in-memory database that stores tables and supports transactions.
    """
    def __init__(self, schema: DatabaseSchema, **config):
        super().__init__(**config)
        self.schema = schema
        self.tables = ThreadSafeDict()  # Use thread-safe dictionary

        # Create tables based on the schema
        for table_name, table_schema in schema.tables.items():
            self._create_table(table_schema)

    def _create_table(self, table_schema: TableSchema) -> Table:
        """Create a new table based on the schema."""
        table = Table(table_schema)
        self.tables[table_schema.name] = table
        return table
    
    def _get_table(self, table_name: str) -> Table:
        """Get a table by name or raise an exception if it doesn't exist."""
        table = self.tables.get(table_name)
        if table is None:
            raise ValueError(f"Table {table_name} does not exist")
        return table
    
    def insert(self, 
              table_name: str, 
              record: Dict[str, Any], 
              client_id: Optional[str] = None,
              transaction: Optional[Transaction] = None) -> Dict[str, Any]:
        """
        Insert a record into a table.
        
        Args:
            table_name: The name of the table
            record: The record to insert
            client_id: Optional ID of the client making the change
            transaction: Optional transaction to use
            
        Returns:
            The inserted record
        """
        table = self._get_table(table_name)
        return table.insert(record, client_id)
    
    def update(self, 
              table_name: str, 
              record: Dict[str, Any], 
              client_id: Optional[str] = None,
              transaction: Optional[Transaction] = None) -> Dict[str, Any]:
        """
        Update a record in a table.
        
        Args:
            table_name: The name of the table
            record: The record to update (must include primary key)
            client_id: Optional ID of the client making the change
            transaction: Optional transaction to use
            
        Returns:
            The updated record
        """
        table = self._get_table(table_name)
        return table.update(record, client_id)
    
    def delete(self, 
              table_name: str, 
              primary_key_values: List[Any], 
              client_id: Optional[str] = None,
              transaction: Optional[Transaction] = None) -> None:
        """
        Delete a record from a table.
        
        Args:
            table_name: The name of the table
            primary_key_values: The values for the primary key columns
            client_id: Optional ID of the client making the change
            transaction: Optional transaction to use
        """
        table = self._get_table(table_name)
        table.delete(primary_key_values, client_id)
    
    def get(self, table_name: str, primary_key_values: List[Any]) -> Optional[Dict[str, Any]]:
        """
        Get a record from a table by its primary key.
        
        Args:
            table_name: The name of the table
            primary_key_values: The values for the primary key columns
            
        Returns:
            The record if found, None otherwise
        """
        table = self._get_table(table_name)
        return table.get(primary_key_values)
    
    def query(self, 
             table_name: str, 
             conditions: Optional[Dict[str, Any]] = None, 
             limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Query records from a table.
        
        Args:
            table_name: The name of the table
            conditions: Optional conditions that records must match
            limit: Optional maximum number of records to return
            
        Returns:
            List of matching records
        """
        table = self._get_table(table_name)
        return table.query(conditions, limit)
    
    def begin_transaction(self) -> Transaction:
        """Begin a new transaction."""
        return Transaction(self)
    
    def get_changes_since(self, table_name: str, index: int) -> List[Dict[str, Any]]:
        """
        Get all changes to a table since the given index.
        
        Args:
            table_name: The name of the table
            index: The index to get changes after
            
        Returns:
            List of changes
        """
        table = self._get_table(table_name)
        return table.get_changes_since(index)
    
    def generate_client_id(self) -> str:
        """Generate a unique client ID."""
        return generate_id()  # Use common ID generation