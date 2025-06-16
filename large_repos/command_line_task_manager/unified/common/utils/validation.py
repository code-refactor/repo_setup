"""Validation utilities for the unified command line task manager."""

import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set, Union
from uuid import UUID

from ..core.exceptions import ValidationError, ValidationErrorCollection


class ValidationRule:
    """Represents a single validation rule."""
    
    def __init__(self, validator: Callable[[Any], bool], error_message: str):
        self.validator = validator
        self.error_message = error_message
    
    def validate(self, value: Any) -> bool:
        """Validate a value using this rule."""
        try:
            return self.validator(value)
        except Exception:
            return False


class FieldValidator:
    """Validator for individual fields with multiple rules."""
    
    def __init__(self, field_name: str):
        self.field_name = field_name
        self.rules: List[ValidationRule] = []
        self.required = False
    
    def add_rule(self, validator: Callable[[Any], bool], error_message: str) -> 'FieldValidator':
        """Add a validation rule."""
        self.rules.append(ValidationRule(validator, error_message))
        return self
    
    def make_required(self) -> 'FieldValidator':
        """Mark this field as required."""
        self.required = True
        return self
    
    def validate(self, value: Any) -> List[str]:
        """Validate a value and return list of error messages."""
        errors = []
        
        # Check if required
        if self.required and (value is None or (isinstance(value, str) and not value.strip())):
            errors.append(f"Field '{self.field_name}' is required")
            return errors
        
        # If value is None and not required, skip other validations
        if value is None:
            return errors
        
        # Apply all rules
        for rule in self.rules:
            if not rule.validate(value):
                errors.append(rule.error_message)
        
        return errors


class ValidationUtils:
    """Collection of common validation utilities."""
    
    # Email validation regex
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # URL validation regex
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format."""
        if not isinstance(email, str):
            return False
        return bool(ValidationUtils.EMAIL_PATTERN.match(email))
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format."""
        if not isinstance(url, str):
            return False
        return bool(ValidationUtils.URL_PATTERN.match(url))
    
    @staticmethod
    def is_valid_uuid(uuid_str: str) -> bool:
        """Validate UUID format."""
        if not isinstance(uuid_str, str):
            return False
        try:
            UUID(uuid_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_non_empty_string(value: Any) -> bool:
        """Check if value is a non-empty string."""
        return isinstance(value, str) and len(value.strip()) > 0
    
    @staticmethod
    def is_positive_number(value: Any) -> bool:
        """Check if value is a positive number."""
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_non_negative_number(value: Any) -> bool:
        """Check if value is a non-negative number."""
        try:
            return float(value) >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_in_range(min_val: Union[int, float], max_val: Union[int, float]) -> Callable[[Any], bool]:
        """Create a validator for numeric range."""
        def validator(value: Any) -> bool:
            try:
                num_value = float(value)
                return min_val <= num_value <= max_val
            except (ValueError, TypeError):
                return False
        return validator
    
    @staticmethod
    def is_min_length(min_length: int) -> Callable[[Any], bool]:
        """Create a validator for minimum string length."""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return len(value.strip()) >= min_length
        return validator
    
    @staticmethod
    def is_max_length(max_length: int) -> Callable[[Any], bool]:
        """Create a validator for maximum string length."""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return len(value) <= max_length
        return validator
    
    @staticmethod
    def is_in_set(valid_values: Set[Any]) -> Callable[[Any], bool]:
        """Create a validator for membership in a set."""
        def validator(value: Any) -> bool:
            return value in valid_values
        return validator
    
    @staticmethod
    def matches_pattern(pattern: str) -> Callable[[Any], bool]:
        """Create a validator for regex pattern matching."""
        compiled_pattern = re.compile(pattern)
        
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return bool(compiled_pattern.match(value))
        return validator
    
    @staticmethod
    def is_valid_date_string(date_format: str = "%Y-%m-%d") -> Callable[[Any], bool]:
        """Create a validator for date string format."""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            try:
                datetime.strptime(value, date_format)
                return True
            except ValueError:
                return False
        return validator
    
    @staticmethod
    def is_future_date(value: Any) -> bool:
        """Check if value is a future date."""
        if isinstance(value, str):
            try:
                date_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                return False
        elif isinstance(value, datetime):
            date_value = value
        else:
            return False
        
        return date_value > datetime.now()
    
    @staticmethod
    def is_valid_file_size(max_size_mb: float) -> Callable[[Any], bool]:
        """Create a validator for file size in MB."""
        max_size_bytes = max_size_mb * 1024 * 1024
        
        def validator(value: Any) -> bool:
            try:
                size_bytes = int(value)
                return 0 <= size_bytes <= max_size_bytes
            except (ValueError, TypeError):
                return False
        return validator
    
    @staticmethod
    def has_required_keys(required_keys: Set[str]) -> Callable[[Any], bool]:
        """Create a validator for dictionary with required keys."""
        def validator(value: Any) -> bool:
            if not isinstance(value, dict):
                return False
            return required_keys.issubset(set(value.keys()))
        return validator
    
    @staticmethod
    def is_valid_json_string(value: Any) -> bool:
        """Check if value is a valid JSON string."""
        if not isinstance(value, str):
            return False
        try:
            import json
            json.loads(value)
            return True
        except (ValueError, json.JSONDecodeError):
            return False


class EntityValidator:
    """Comprehensive validator for entity objects."""
    
    def __init__(self, entity_type: str):
        self.entity_type = entity_type
        self.field_validators: Dict[str, FieldValidator] = {}
        self.custom_validators: List[Callable[[Dict[str, Any]], List[str]]] = []
    
    def add_field(self, field_name: str) -> FieldValidator:
        """Add a field validator."""
        if field_name not in self.field_validators:
            self.field_validators[field_name] = FieldValidator(field_name)
        return self.field_validators[field_name]
    
    def add_custom_validator(self, validator: Callable[[Dict[str, Any]], List[str]]) -> None:
        """Add a custom validator function."""
        self.custom_validators.append(validator)
    
    def validate(self, data: Dict[str, Any]) -> ValidationErrorCollection:
        """Validate entity data and return collection of errors."""
        errors = ValidationErrorCollection()
        
        # Validate individual fields
        for field_name, validator in self.field_validators.items():
            field_value = data.get(field_name)
            field_errors = validator.validate(field_value)
            
            for error_message in field_errors:
                errors.add_error(field_name, error_message, field_value)
        
        # Run custom validators
        for custom_validator in self.custom_validators:
            try:
                custom_errors = custom_validator(data)
                for error_message in custom_errors:
                    errors.add_error("custom", error_message)
            except Exception as e:
                errors.add_error("custom", f"Custom validation failed: {str(e)}")
        
        return errors
    
    def validate_and_raise(self, data: Dict[str, Any]) -> None:
        """Validate and raise ValidationError if there are any errors."""
        errors = self.validate(data)
        errors.raise_if_errors()


# Common field validators factory functions
def create_string_validator(field_name: str, required: bool = False, 
                          min_length: Optional[int] = None,
                          max_length: Optional[int] = None,
                          pattern: Optional[str] = None) -> FieldValidator:
    """Create a string field validator with common rules."""
    validator = FieldValidator(field_name)
    
    if required:
        validator.make_required()
    
    validator.add_rule(
        lambda x: isinstance(x, str) if x is not None else True,
        f"Field '{field_name}' must be a string"
    )
    
    if min_length is not None:
        validator.add_rule(
            ValidationUtils.is_min_length(min_length),
            f"Field '{field_name}' must be at least {min_length} characters long"
        )
    
    if max_length is not None:
        validator.add_rule(
            ValidationUtils.is_max_length(max_length),
            f"Field '{field_name}' must be no more than {max_length} characters long"
        )
    
    if pattern is not None:
        validator.add_rule(
            ValidationUtils.matches_pattern(pattern),
            f"Field '{field_name}' does not match required pattern"
        )
    
    return validator


def create_enum_validator(field_name: str, enum_class: type, required: bool = False) -> FieldValidator:
    """Create an enum field validator."""
    validator = FieldValidator(field_name)
    
    if required:
        validator.make_required()
    
    if hasattr(enum_class, 'values'):
        valid_values = enum_class.values()
        validator.add_rule(
            ValidationUtils.is_in_set(valid_values),
            f"Field '{field_name}' must be one of: {', '.join(valid_values)}"
        )
    
    return validator


def create_numeric_validator(field_name: str, required: bool = False,
                           min_value: Optional[Union[int, float]] = None,
                           max_value: Optional[Union[int, float]] = None,
                           positive_only: bool = False) -> FieldValidator:
    """Create a numeric field validator."""
    validator = FieldValidator(field_name)
    
    if required:
        validator.make_required()
    
    validator.add_rule(
        lambda x: isinstance(x, (int, float)) if x is not None else True,
        f"Field '{field_name}' must be a number"
    )
    
    if positive_only:
        validator.add_rule(
            ValidationUtils.is_positive_number,
            f"Field '{field_name}' must be a positive number"
        )
    
    if min_value is not None and max_value is not None:
        validator.add_rule(
            ValidationUtils.is_in_range(min_value, max_value),
            f"Field '{field_name}' must be between {min_value} and {max_value}"
        )
    
    return validator