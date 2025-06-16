"""
Universal query processing framework for the unified query language interpreter.

This module provides the core query processing infrastructure that can be
extended by domain-specific implementations while sharing common functionality
for parsing, execution, and result handling.
"""

import re
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from .models import (
    BaseQuery, QueryResult, QueryStatus, UserContext, 
    QueryExecutionContext, AuditEvent, AccessAction
)


class QueryParseError(Exception):
    """Exception raised when query parsing fails."""
    pass


class QueryExecutionError(Exception):
    """Exception raised when query execution fails."""
    pass


class BaseQueryParser(ABC):
    """Abstract base class for query parsers."""
    
    @abstractmethod
    def parse_query(self, query: str) -> BaseQuery:
        """
        Parse a query string into a structured BaseQuery object.
        
        Args:
            query: Raw query string to parse
            
        Returns:
            BaseQuery object with parsed components
            
        Raises:
            QueryParseError: If query parsing fails
        """
        pass
    
    @abstractmethod
    def extract_tables(self, query: str) -> List[str]:
        """Extract table names from query."""
        pass
    
    @abstractmethod
    def extract_fields(self, query: str) -> List[str]:
        """Extract field names from query."""
        pass


class DefaultQueryParser(BaseQueryParser):
    """Default SQL-like query parser implementation."""
    
    def __init__(self):
        self.table_pattern = re.compile(r'\bFROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', re.IGNORECASE)
        self.field_pattern = re.compile(r'SELECT\s+(.*?)\s+FROM', re.IGNORECASE | re.DOTALL)
        self.where_pattern = re.compile(r'\bWHERE\s+(.*?)(?:\s+ORDER\s+BY|\s+GROUP\s+BY|\s+LIMIT|$)', re.IGNORECASE | re.DOTALL)
        self.join_pattern = re.compile(r'\b(LEFT|RIGHT|INNER|OUTER)?\s*JOIN\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+ON\s+(.*?)(?:\s+WHERE|\s+ORDER|\s+GROUP|\s+LIMIT|$)', re.IGNORECASE)
    
    def parse_query(self, query: str) -> BaseQuery:
        """Parse SQL-like query into BaseQuery object."""
        try:
            base_query = BaseQuery(raw_query=query.strip())
            
            # Extract components
            base_query.tables = self.extract_tables(query)
            base_query.fields = self.extract_fields(query)
            base_query.joins = self._extract_joins(query)
            base_query.conditions = self._extract_conditions(query)
            
            # Store parsed representation
            base_query.parsed_query = {
                'tables': base_query.tables,
                'fields': base_query.fields,
                'joins': base_query.joins,
                'conditions': base_query.conditions
            }
            
            return base_query
            
        except Exception as e:
            raise QueryParseError(f"Failed to parse query: {str(e)}")
    
    def extract_tables(self, query: str) -> List[str]:
        """Extract table names from FROM and JOIN clauses."""
        tables = []
        
        # Extract from FROM clause
        from_match = self.table_pattern.search(query)
        if from_match:
            tables.append(from_match.group(1))
        
        # Extract from JOIN clauses
        join_matches = self.join_pattern.findall(query)
        for match in join_matches:
            if len(match) >= 2:
                tables.append(match[1])
        
        return list(set(tables))  # Remove duplicates
    
    def extract_fields(self, query: str) -> List[str]:
        """Extract field names from SELECT clause."""
        match = self.field_pattern.search(query)
        if not match:
            return []
        
        fields_str = match.group(1).strip()
        if fields_str == '*':
            return ['*']
        
        # Split by comma and clean up
        fields = [field.strip() for field in fields_str.split(',')]
        return [field for field in fields if field]
    
    def _extract_joins(self, query: str) -> List[Dict[str, Any]]:
        """Extract JOIN information."""
        joins = []
        matches = self.join_pattern.findall(query)
        
        for match in matches:
            join_type = match[0] if match[0] else 'INNER'
            table = match[1]
            condition = match[2].strip()
            
            joins.append({
                'type': join_type,
                'table': table,
                'condition': condition
            })
        
        return joins
    
    def _extract_conditions(self, query: str) -> List[Dict[str, Any]]:
        """Extract WHERE conditions."""
        match = self.where_pattern.search(query)
        if not match:
            return []
        
        conditions_str = match.group(1).strip()
        
        # Simple condition parsing - can be enhanced
        conditions = []
        for condition in conditions_str.split(' AND '):
            condition = condition.strip()
            if condition:
                conditions.append({
                    'type': 'condition',
                    'expression': condition
                })
        
        return conditions


class BaseQueryExecutor(ABC):
    """Abstract base class for query executors."""
    
    def __init__(self, parser: Optional[BaseQueryParser] = None):
        self.parser = parser or DefaultQueryParser()
        self.query_history: List[QueryResult] = []
    
    @abstractmethod
    def execute_query(self, query: str, context: UserContext, **kwargs) -> QueryResult:
        """
        Execute a query and return results.
        
        Args:
            query: Query string to execute
            context: User context for the query
            **kwargs: Additional execution parameters
            
        Returns:
            QueryResult with execution results
        """
        pass
    
    def parse_and_execute(self, query: str, context: UserContext, **kwargs) -> QueryResult:
        """Parse and execute a query in one step."""
        try:
            # Parse query
            parsed_query = self.parser.parse_query(query)
            
            # Create execution context
            exec_context = QueryExecutionContext(
                query=parsed_query,
                user_context=context
            )
            
            # Execute query
            result = self._execute_with_context(exec_context, **kwargs)
            
            # Store in history
            self.query_history.append(result)
            
            return result
            
        except Exception as e:
            # Create error result
            error_result = self._create_error_result(
                query, context.user_id, str(e)
            )
            self.query_history.append(error_result)
            return error_result
    
    def get_query_history(self, user_id: Optional[str] = None) -> List[QueryResult]:
        """Get query execution history, optionally filtered by user."""
        if user_id:
            return [result for result in self.query_history if result.user_id == user_id]
        return self.query_history.copy()
    
    def _execute_with_context(self, context: QueryExecutionContext, **kwargs) -> QueryResult:
        """Execute query with full context - to be implemented by subclasses."""
        context.status = QueryStatus.EXECUTING
        start_time = time.time()
        
        try:
            # Add audit event for query start
            context.add_audit_event(
                AccessAction.QUERY,
                f"tables:{','.join(context.query.tables)}",
                "started"
            )
            
            # Call subclass implementation
            result = self.execute_query(context.query.raw_query, context.user_context, **kwargs)
            
            # Update result with execution time
            execution_time = int((time.time() - start_time) * 1000)
            result.execution_time_ms = execution_time
            result.query_id = context.query.query_id
            
            context.status = QueryStatus.COMPLETED
            context.result = result
            
            # Add completion audit event
            context.add_audit_event(
                AccessAction.QUERY,
                f"tables:{','.join(context.query.tables)}",
                "completed",
                execution_time_ms=execution_time,
                row_count=result.row_count
            )
            
            return result
            
        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            error_result = self._create_error_result(
                context.query.raw_query, 
                context.user_context.user_id, 
                str(e),
                execution_time
            )
            error_result.query_id = context.query.query_id
            
            context.status = QueryStatus.FAILED
            context.result = error_result
            context.add_error(str(e))
            
            # Add error audit event
            context.add_audit_event(
                AccessAction.QUERY,
                f"tables:{','.join(context.query.tables)}",
                "failed",
                execution_time_ms=execution_time,
                error=str(e)
            )
            
            return error_result
    
    def _create_error_result(self, query: str, user_id: str, error: str, 
                           execution_time: int = 0) -> QueryResult:
        """Create a standardized error result."""
        return QueryResult(
            query_id="",  # Will be set by caller
            status=QueryStatus.FAILED,
            execution_time_ms=execution_time,
            user_id=user_id,
            error=error,
            metadata={"query": query}
        )
    
    def _create_denied_result(self, query: str, user_id: str, reason: str,
                            execution_time: int = 0) -> QueryResult:
        """Create a standardized access denied result."""
        return QueryResult(
            query_id="",  # Will be set by caller
            status=QueryStatus.DENIED,
            execution_time_ms=execution_time,
            user_id=user_id,
            access_granted=False,
            reason=reason,
            metadata={"query": query}
        )


class QueryValidator:
    """Utility class for query validation."""
    
    def __init__(self):
        self.forbidden_keywords = {
            'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 
            'INSERT', 'UPDATE', 'GRANT', 'REVOKE'
        }
        self.max_query_length = 10000
    
    def validate_query(self, query: str) -> List[str]:
        """
        Validate query for security and safety.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check length
        if len(query) > self.max_query_length:
            errors.append(f"Query too long (max {self.max_query_length} characters)")
        
        # Check for forbidden keywords
        query_upper = query.upper()
        for keyword in self.forbidden_keywords:
            if keyword in query_upper:
                errors.append(f"Forbidden keyword: {keyword}")
        
        # Check for SQL injection patterns
        if self._check_sql_injection(query):
            errors.append("Potential SQL injection detected")
        
        return errors
    
    def _check_sql_injection(self, query: str) -> bool:
        """Basic SQL injection detection."""
        injection_patterns = [
            r"';.*--",  # Comment injection
            r"'\s*OR\s*'.*'='",  # OR injection
            r"'\s*UNION\s*SELECT",  # UNION injection
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        
        return False


class QueryResultBuilder:
    """Helper class for building query results."""
    
    @staticmethod
    def create_success_result(query_id: str, user_id: str, data: List[Dict[str, Any]], 
                            execution_time_ms: int, **kwargs) -> QueryResult:
        """Create a successful query result."""
        columns = list(data[0].keys()) if data else []
        
        return QueryResult(
            query_id=query_id,
            status=QueryStatus.COMPLETED,
            execution_time_ms=execution_time_ms,
            user_id=user_id,
            row_count=len(data),
            column_count=len(columns),
            columns=columns,
            data=data,
            **kwargs
        )
    
    @staticmethod
    def create_empty_result(query_id: str, user_id: str, 
                          execution_time_ms: int, reason: str = "") -> QueryResult:
        """Create an empty result."""
        return QueryResult(
            query_id=query_id,
            status=QueryStatus.COMPLETED,
            execution_time_ms=execution_time_ms,
            user_id=user_id,
            row_count=0,
            column_count=0,
            columns=[],
            data=[],
            reason=reason
        )