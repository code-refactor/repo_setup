"""Common exception classes for the unified command line task manager."""

from typing import Any, Dict, List, Optional


class BaseTaskManagerError(Exception):
    """Base exception for all task manager errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class EntityNotFoundError(BaseTaskManagerError):
    """Raised when an entity is not found."""
    
    def __init__(self, entity_type: str, entity_id: str, details: Optional[Dict[str, Any]] = None):
        message = f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(message, details)
        self.entity_type = entity_type
        self.entity_id = entity_id


class ValidationError(BaseTaskManagerError):
    """Raised when validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None, 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.field = field
        self.value = value
        
        if field:
            self.message = f"Validation error for field '{field}': {message}"


class DuplicateEntityError(BaseTaskManagerError):
    """Raised when attempting to create a duplicate entity."""
    
    def __init__(self, entity_type: str, identifier: str, details: Optional[Dict[str, Any]] = None):
        message = f"Duplicate {entity_type} with identifier '{identifier}'"
        super().__init__(message, details)
        self.entity_type = entity_type
        self.identifier = identifier


class StorageError(BaseTaskManagerError):
    """Raised when storage operations fail."""
    
    def __init__(self, operation: str, message: str, details: Optional[Dict[str, Any]] = None):
        full_message = f"Storage {operation} failed: {message}"
        super().__init__(full_message, details)
        self.operation = operation


class ServiceError(BaseTaskManagerError):
    """Raised when service operations fail."""
    
    def __init__(self, service_name: str, operation: str, message: str, 
                 details: Optional[Dict[str, Any]] = None):
        full_message = f"Service '{service_name}' {operation} failed: {message}"
        super().__init__(full_message, details)
        self.service_name = service_name
        self.operation = operation


class AssociationError(BaseTaskManagerError):
    """Raised when entity association operations fail."""
    
    def __init__(self, source_type: str, target_type: str, operation: str, 
                 message: str, details: Optional[Dict[str, Any]] = None):
        full_message = f"Association {operation} between {source_type} and {target_type} failed: {message}"
        super().__init__(full_message, details)
        self.source_type = source_type
        self.target_type = target_type
        self.operation = operation


class ConfigurationError(BaseTaskManagerError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, config_key: str, message: str, details: Optional[Dict[str, Any]] = None):
        full_message = f"Configuration error for '{config_key}': {message}"
        super().__init__(full_message, details)
        self.config_key = config_key


class SecurityError(BaseTaskManagerError):
    """Raised when security-related operations fail."""
    
    def __init__(self, operation: str, message: str, details: Optional[Dict[str, Any]] = None):
        full_message = f"Security {operation} failed: {message}"
        super().__init__(full_message, details)
        self.operation = operation


class AuthorizationError(SecurityError):
    """Raised when authorization fails."""
    
    def __init__(self, user: str, operation: str, resource: str, 
                 details: Optional[Dict[str, Any]] = None):
        message = f"User '{user}' not authorized for {operation} on {resource}"
        super().__init__("authorization", message, details)
        self.user = user
        self.resource = resource


class EncryptionError(SecurityError):
    """Raised when encryption/decryption operations fail."""
    
    def __init__(self, operation: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(f"encryption/{operation}", message, details)


class IntegrityError(SecurityError):
    """Raised when data integrity checks fail."""
    
    def __init__(self, resource: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__("integrity", f"Integrity check failed for {resource}: {message}", details)
        self.resource = resource


# Validation error aggregation
class ValidationErrorCollection:
    """Collection of validation errors for batch validation."""
    
    def __init__(self):
        self.errors: List[ValidationError] = []
    
    def add_error(self, field: str, message: str, value: Any = None, 
                  details: Optional[Dict[str, Any]] = None) -> None:
        """Add a validation error to the collection."""
        error = ValidationError(message, field, value, details)
        self.errors.append(error)
    
    def has_errors(self) -> bool:
        """Check if there are any validation errors."""
        return len(self.errors) > 0
    
    def get_summary(self) -> str:
        """Get a summary of all validation errors."""
        if not self.errors:
            return "No validation errors"
        
        error_messages = [error.message for error in self.errors]
        return f"Validation failed with {len(self.errors)} error(s): " + "; ".join(error_messages)
    
    def raise_if_errors(self) -> None:
        """Raise a ValidationError if there are any errors in the collection."""
        if self.has_errors():
            raise ValidationError(self.get_summary(), details={"errors": self.errors})