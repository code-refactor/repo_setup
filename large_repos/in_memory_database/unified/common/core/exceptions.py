"""
Exception classes for the unified in-memory database library.

This module provides common exception types that can be shared across both
vectordb and syncdb implementations.
"""


class UnifiedDatabaseError(Exception):
    """Base exception for all database operations."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message
    
    def to_dict(self):
        """Convert exception to dictionary representation."""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details
        }


class ValidationError(UnifiedDatabaseError):
    """Exception raised for validation-related errors."""
    
    def __init__(self, message: str, field_name: str = None, field_value=None):
        super().__init__(message, error_code="VALIDATION_ERROR")
        self.field_name = field_name
        self.field_value = field_value
        if field_name:
            self.details['field_name'] = field_name
        if field_value is not None:
            self.details['field_value'] = field_value


class ConfigurationError(UnifiedDatabaseError):
    """Exception raised for configuration-related errors."""
    
    def __init__(self, message: str, config_key: str = None, config_value=None):
        super().__init__(message, error_code="CONFIG_ERROR")
        self.config_key = config_key
        self.config_value = config_value
        if config_key:
            self.details['config_key'] = config_key
        if config_value is not None:
            self.details['config_value'] = config_value


class SerializationError(UnifiedDatabaseError):
    """Exception raised for serialization-related errors."""
    
    def __init__(self, message: str, serialization_type: str = None):
        super().__init__(message, error_code="SERIALIZATION_ERROR")
        self.serialization_type = serialization_type
        if serialization_type:
            self.details['serialization_type'] = serialization_type


class VectorError(UnifiedDatabaseError):
    """Exception raised for vector operation errors."""
    
    def __init__(self, message: str, operation: str = None, dimensions: tuple = None):
        super().__init__(message, error_code="VECTOR_ERROR")
        self.operation = operation
        self.dimensions = dimensions
        if operation:
            self.details['operation'] = operation
        if dimensions:
            self.details['dimensions'] = dimensions


class IndexError(UnifiedDatabaseError):
    """Exception raised for indexing-related errors."""
    
    def __init__(self, message: str, index_type: str = None, index_name: str = None):
        super().__init__(message, error_code="INDEX_ERROR")
        self.index_type = index_type
        self.index_name = index_name
        if index_type:
            self.details['index_type'] = index_type
        if index_name:
            self.details['index_name'] = index_name


class SynchronizationError(UnifiedDatabaseError):
    """Exception raised for synchronization-related errors."""
    
    def __init__(self, message: str, sync_operation: str = None, client_id: str = None):
        super().__init__(message, error_code="SYNC_ERROR")
        self.sync_operation = sync_operation
        self.client_id = client_id
        if sync_operation:
            self.details['sync_operation'] = sync_operation
        if client_id:
            self.details['client_id'] = client_id


class ConflictError(UnifiedDatabaseError):
    """Exception raised for conflict resolution errors."""
    
    def __init__(self, message: str, conflict_type: str = None, 
                 table_name: str = None, record_id: str = None):
        super().__init__(message, error_code="CONFLICT_ERROR")
        self.conflict_type = conflict_type
        self.table_name = table_name
        self.record_id = record_id
        if conflict_type:
            self.details['conflict_type'] = conflict_type
        if table_name:
            self.details['table_name'] = table_name
        if record_id:
            self.details['record_id'] = record_id


class SchemaError(UnifiedDatabaseError):
    """Exception raised for schema-related errors."""
    
    def __init__(self, message: str, schema_version: int = None, 
                 table_name: str = None, column_name: str = None):
        super().__init__(message, error_code="SCHEMA_ERROR")
        self.schema_version = schema_version
        self.table_name = table_name
        self.column_name = column_name
        if schema_version is not None:
            self.details['schema_version'] = schema_version
        if table_name:
            self.details['table_name'] = table_name
        if column_name:
            self.details['column_name'] = column_name


class CompressionError(UnifiedDatabaseError):
    """Exception raised for compression-related errors."""
    
    def __init__(self, message: str, compression_type: str = None, 
                 compression_level: str = None):
        super().__init__(message, error_code="COMPRESSION_ERROR")
        self.compression_type = compression_type
        self.compression_level = compression_level
        if compression_type:
            self.details['compression_type'] = compression_type
        if compression_level:
            self.details['compression_level'] = compression_level


class PowerManagementError(UnifiedDatabaseError):
    """Exception raised for power management errors."""
    
    def __init__(self, message: str, power_mode: str = None, battery_level: float = None):
        super().__init__(message, error_code="POWER_ERROR")
        self.power_mode = power_mode
        self.battery_level = battery_level
        if power_mode:
            self.details['power_mode'] = power_mode
        if battery_level is not None:
            self.details['battery_level'] = battery_level


class FeatureStoreError(UnifiedDatabaseError):
    """Exception raised for feature store operations."""
    
    def __init__(self, message: str, entity_id: str = None, 
                 feature_name: str = None, version: int = None):
        super().__init__(message, error_code="FEATURE_STORE_ERROR")
        self.entity_id = entity_id
        self.feature_name = feature_name
        self.version = version
        if entity_id:
            self.details['entity_id'] = entity_id
        if feature_name:
            self.details['feature_name'] = feature_name
        if version is not None:
            self.details['version'] = version


class BatchProcessingError(UnifiedDatabaseError):
    """Exception raised for batch processing errors."""
    
    def __init__(self, message: str, batch_size: int = None, 
                 processed_count: int = None, failed_count: int = None):
        super().__init__(message, error_code="BATCH_ERROR")
        self.batch_size = batch_size
        self.processed_count = processed_count
        self.failed_count = failed_count
        if batch_size is not None:
            self.details['batch_size'] = batch_size
        if processed_count is not None:
            self.details['processed_count'] = processed_count
        if failed_count is not None:
            self.details['failed_count'] = failed_count


class TransactionError(UnifiedDatabaseError):
    """Exception raised for transaction-related errors."""
    
    def __init__(self, message: str, transaction_id: str = None, 
                 operation: str = None):
        super().__init__(message, error_code="TRANSACTION_ERROR")
        self.transaction_id = transaction_id
        self.operation = operation
        if transaction_id:
            self.details['transaction_id'] = transaction_id
        if operation:
            self.details['operation'] = operation


class NetworkError(UnifiedDatabaseError):
    """Exception raised for network-related errors."""
    
    def __init__(self, message: str, network_operation: str = None, 
                 latency: float = None, packet_loss: float = None):
        super().__init__(message, error_code="NETWORK_ERROR")
        self.network_operation = network_operation
        self.latency = latency
        self.packet_loss = packet_loss
        if network_operation:
            self.details['network_operation'] = network_operation
        if latency is not None:
            self.details['latency'] = latency
        if packet_loss is not None:
            self.details['packet_loss'] = packet_loss


class PerformanceError(UnifiedDatabaseError):
    """Exception raised for performance-related errors."""
    
    def __init__(self, message: str, operation: str = None, 
                 duration: float = None, threshold: float = None):
        super().__init__(message, error_code="PERFORMANCE_ERROR")
        self.operation = operation
        self.duration = duration
        self.threshold = threshold
        if operation:
            self.details['operation'] = operation
        if duration is not None:
            self.details['duration'] = duration
        if threshold is not None:
            self.details['threshold'] = threshold


# Exception handling utilities
def handle_exception(func):
    """Decorator to wrap functions with unified exception handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnifiedDatabaseError:
            # Re-raise our own exceptions
            raise
        except ValueError as e:
            raise ValidationError(str(e))
        except TypeError as e:
            raise ValidationError(str(e))
        except KeyError as e:
            raise ConfigurationError(f"Missing required key: {e}")
        except Exception as e:
            raise UnifiedDatabaseError(f"Unexpected error: {e}")
    return wrapper


def create_error_response(error: UnifiedDatabaseError) -> dict:
    """Create standardized error response dictionary."""
    return {
        'success': False,
        'error': error.to_dict(),
        'timestamp': __import__('time').time()
    }