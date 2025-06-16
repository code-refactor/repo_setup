"""
Change tracking system for efficient synchronization.
"""
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
import copy
from common.core import (
    BaseComponent, PerformanceTrackingMixin, SerializableMixin,
    get_timestamp, safe_json_serialize, safe_json_deserialize
)


@dataclass
class ChangeRecord(SerializableMixin):
    """Represents a single change to a record."""
    id: int  # Sequential ID for ordering changes
    table_name: str
    primary_key: Tuple  # Primary key values as a tuple
    operation: str  # "insert", "update", or "delete"
    timestamp: float  # Unix timestamp
    client_id: str  # ID of the client that made the change
    old_data: Optional[Dict[str, Any]]  # Previous state (None for inserts)
    new_data: Optional[Dict[str, Any]]  # New state (None for deletes)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization."""
        return {
            "id": self.id,
            "table_name": self.table_name,
            "primary_key": self.primary_key,
            "operation": self.operation,
            "timestamp": self.timestamp,
            "client_id": self.client_id,
            "old_data": self.old_data,
            "new_data": self.new_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChangeRecord':
        """Create a ChangeRecord from a dictionary."""
        return cls(
            id=data["id"],
            table_name=data["table_name"],
            primary_key=tuple(data["primary_key"]),
            operation=data["operation"],
            timestamp=data["timestamp"],
            client_id=data["client_id"],
            old_data=data["old_data"],
            new_data=data["new_data"]
        )


class ChangeTracker(BaseComponent, PerformanceTrackingMixin):
    """
    Tracks changes to database records for efficient synchronization.
    """
    def __init__(self, max_history_size: int = 10000, **config):
        super().__init__(**config)
        self.changes: Dict[str, List[ChangeRecord]] = {}  # Table name -> changes
        self.max_history_size = max_history_size
        self.counters: Dict[str, int] = {}  # Table name -> next change ID
    
    def record_change(self, 
                     table_name: str, 
                     primary_key: Tuple,
                     operation: str, 
                     old_data: Optional[Dict[str, Any]], 
                     new_data: Optional[Dict[str, Any]],
                     client_id: str) -> ChangeRecord:
        """
        Record a change to a database record.
        
        Args:
            table_name: Name of the table
            primary_key: Primary key values as a tuple
            operation: "insert", "update", or "delete"
            old_data: Previous state (None for inserts)
            new_data: New state (None for deletes)
            client_id: ID of the client that made the change
            
        Returns:
            The created ChangeRecord
        """
        # Initialize table changes if not already done
        if table_name not in self.changes:
            self.changes[table_name] = []
            self.counters[table_name] = 0
        
        # Get the next change ID for this table
        change_id = self.counters[table_name]
        self.counters[table_name] += 1
        
        # Create the change record
        change = ChangeRecord(
            id=change_id,
            table_name=table_name,
            primary_key=primary_key,
            operation=operation,
            timestamp=get_timestamp(),  # Use common timestamp utility
            client_id=client_id,
            old_data=copy.deepcopy(old_data) if old_data else None,
            new_data=copy.deepcopy(new_data) if new_data else None
        )
        
        # Add to the change log
        self.changes[table_name].append(change)
        
        # Prune history if necessary
        self._prune_history(table_name)
        
        self._touch()  # From TimestampedMixin
        return change
    
    def _prune_history(self, table_name: str) -> None:
        """
        Prune change history for a table if it exceeds max_history_size.
        """
        table_changes = self.changes.get(table_name, [])
        if len(table_changes) > self.max_history_size:
            # Keep only the most recent changes
            self.changes[table_name] = table_changes[-self.max_history_size:]
    
    def get_changes_since(self, 
                         table_name: str, 
                         since_id: int, 
                         exclude_client_id: Optional[str] = None) -> List[ChangeRecord]:
        """
        Get all changes to a table since a given change ID.
        
        Args:
            table_name: Name of the table
            since_id: Get changes with ID greater than this
            exclude_client_id: Optionally exclude changes made by this client
            
        Returns:
            List of changes since the given ID
        """
        table_changes = self.changes.get(table_name, [])
        
        # Filter changes by ID and optionally by client ID
        filtered_changes = [
            change for change in table_changes
            if change.id > since_id and (exclude_client_id is None or change.client_id != exclude_client_id)
        ]
        
        return filtered_changes
    
    def get_latest_change_id(self, table_name: str) -> int:
        """
        Get the ID of the latest change for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Latest change ID, or -1 if no changes exist
        """
        if table_name not in self.changes or not self.changes[table_name]:
            return -1
        
        return self.changes[table_name][-1].id
    
    def serialize_changes(self, changes: List[ChangeRecord]) -> str:
        """
        Serialize changes to JSON.
        
        Args:
            changes: List of changes to serialize
            
        Returns:
            JSON string representation
        """
        change_dicts = [change.to_dict() for change in changes]
        return safe_json_serialize(change_dicts)  # Use common serialization
    
    def deserialize_changes(self, json_str: str) -> List[ChangeRecord]:
        """
        Deserialize changes from JSON.
        
        Args:
            json_str: JSON string representation
            
        Returns:
            List of ChangeRecord objects
        """
        change_dicts = safe_json_deserialize(json_str)  # Use common deserialization
        return [ChangeRecord.from_dict(change_dict) for change_dict in change_dicts]


class VersionVector(SerializableMixin):
    """
    Tracks the version of data across multiple clients using a vector clock.
    Used for detecting conflicts during synchronization.
    """
    def __init__(self, client_id: str, initial_value: int = 0):
        self.vector: Dict[str, int] = {client_id: initial_value}
        self.client_id = client_id
    
    def increment(self) -> None:
        """Increment the version for the current client."""
        self.vector[self.client_id] = self.vector.get(self.client_id, 0) + 1
    
    def update(self, other: 'VersionVector') -> None:
        """Merge with another version vector, taking the max value for each client."""
        for client_id, version in other.vector.items():
            self.vector[client_id] = max(self.vector.get(client_id, 0), version)
    
    def dominates(self, other: 'VersionVector') -> bool:
        """
        Check if this version vector dominates another.
        
        Returns True if this vector is strictly greater than or equal to the other
        in all dimensions, and strictly greater in at least one dimension.
        """
        strictly_greater = False
        
        # Check all client IDs in the other vector
        for client_id, other_version in other.vector.items():
            this_version = self.vector.get(client_id, 0)
            
            if this_version < other_version:
                return False
            
            if this_version > other_version:
                strictly_greater = True
        
        # Check if we have any client IDs not in the other vector
        for client_id, this_version in self.vector.items():
            if client_id not in other.vector and this_version > 0:
                strictly_greater = True
        
        return strictly_greater
    
    def concurrent_with(self, other: 'VersionVector') -> bool:
        """
        Check if this version vector is concurrent with another.
        
        Returns True if neither vector dominates the other, indicating
        that they represent concurrent modifications.
        """
        return not self.dominates(other) and not other.dominates(self)
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to a dictionary for serialization."""
        return dict(self.vector)
    
    @classmethod
    def from_dict(cls, data: Dict[str, int], client_id: str) -> 'VersionVector':
        """Create a VersionVector from a dictionary."""
        vector = cls(client_id, 0)
        vector.vector = dict(data)
        return vector