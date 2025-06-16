"""
Configuration management for the unified in-memory database library.

This module provides common configuration functionality that can be shared
across both vectordb and syncdb implementations.
"""

import json
import os
from typing import Any, Dict, List, Optional, Union, Callable, Type
from .base import SerializableMixin, TimestampedMixin, ThreadSafeMixin
from .exceptions import ConfigurationError, ValidationError


class ConfigValidator:
    """Validate configuration dictionaries."""
    
    def __init__(self):
        self._validators: Dict[str, Callable[[Any], bool]] = {}
        self._type_validators: Dict[str, Type] = {}
        self._range_validators: Dict[str, tuple] = {}
        self._choices_validators: Dict[str, List[Any]] = {}
        self._required_keys: set = set()
        self._default_values: Dict[str, Any] = {}
    
    def add_validator(self, key: str, validator: Callable[[Any], bool], 
                     error_message: str = None):
        """Add custom validator for a key."""
        self._validators[key] = validator
        if error_message:
            self._validators[f"{key}_error"] = error_message
    
    def add_type_validator(self, key: str, expected_type: Type):
        """Add type validator for a key."""
        self._type_validators[key] = expected_type
    
    def add_range_validator(self, key: str, min_val: Union[int, float], 
                           max_val: Union[int, float]):
        """Add range validator for a key."""
        self._range_validators[key] = (min_val, max_val)
    
    def add_choices_validator(self, key: str, choices: List[Any]):
        """Add choices validator for a key."""
        self._choices_validators[key] = choices
    
    def set_required(self, key: str, required: bool = True):
        """Set whether a key is required."""
        if required:
            self._required_keys.add(key)
        else:
            self._required_keys.discard(key)
    
    def set_default(self, key: str, default_value: Any):
        """Set default value for a key."""
        self._default_values[key] = default_value
    
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration dictionary."""
        # Start with defaults
        validated_config = self._default_values.copy()
        validated_config.update(config)
        
        # Check required keys
        for key in self._required_keys:
            if key not in validated_config:
                raise ConfigurationError(f"Required configuration key '{key}' is missing")
        
        # Validate each key
        for key, value in validated_config.items():
            self._validate_key(key, value)
        
        return validated_config
    
    def _validate_key(self, key: str, value: Any):
        """Validate a single key-value pair."""
        # Type validation
        if key in self._type_validators:
            expected_type = self._type_validators[key]
            if not isinstance(value, expected_type):
                raise ConfigurationError(
                    f"Configuration key '{key}' must be of type {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
        
        # Range validation
        if key in self._range_validators:
            min_val, max_val = self._range_validators[key]
            if not (min_val <= value <= max_val):
                raise ConfigurationError(
                    f"Configuration key '{key}' must be between {min_val} and {max_val}, "
                    f"got {value}"
                )
        
        # Choices validation
        if key in self._choices_validators:
            choices = self._choices_validators[key]
            if value not in choices:
                raise ConfigurationError(
                    f"Configuration key '{key}' must be one of {choices}, got {value}"
                )
        
        # Custom validation
        if key in self._validators:
            validator = self._validators[key]
            if not validator(value):
                error_msg = self._validators.get(f"{key}_error", 
                                               f"Invalid value for configuration key '{key}': {value}")
                raise ConfigurationError(error_msg)


class ProfileManager(SerializableMixin, TimestampedMixin, ThreadSafeMixin):
    """Manage different operational profiles."""
    
    def __init__(self):
        super().__init__()
        self._profiles: Dict[str, Dict[str, Any]] = {}
        self._current_profile: Optional[str] = None
        self._profile_validators: Dict[str, ConfigValidator] = {}
    
    def create_profile(self, name: str, config: Dict[str, Any], 
                      validator: Optional[ConfigValidator] = None):
        """Create a new profile."""
        with self._lock:
            if validator:
                config = validator.validate(config)
                self._profile_validators[name] = validator
            
            self._profiles[name] = config
            self._touch()
    
    def update_profile(self, name: str, config: Dict[str, Any]):
        """Update an existing profile."""
        with self._lock:
            if name not in self._profiles:
                raise ConfigurationError(f"Profile '{name}' does not exist")
            
            # Validate if validator exists
            if name in self._profile_validators:
                validator = self._profile_validators[name]
                merged_config = self._profiles[name].copy()
                merged_config.update(config)
                config = validator.validate(merged_config)
            
            self._profiles[name].update(config)
            self._touch()
    
    def delete_profile(self, name: str):
        """Delete a profile."""
        with self._lock:
            if name not in self._profiles:
                raise ConfigurationError(f"Profile '{name}' does not exist")
            
            if self._current_profile == name:
                self._current_profile = None
            
            del self._profiles[name]
            if name in self._profile_validators:
                del self._profile_validators[name]
            
            self._touch()
    
    def set_current_profile(self, name: str):
        """Set the current active profile."""
        with self._lock:
            if name not in self._profiles:
                raise ConfigurationError(f"Profile '{name}' does not exist")
            
            self._current_profile = name
            self._touch()
    
    def get_current_profile(self) -> Optional[str]:
        """Get the current active profile name."""
        with self._lock:
            return self._current_profile
    
    def get_profile(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Get profile configuration."""
        with self._lock:
            if name is None:
                name = self._current_profile
            
            if name is None:
                raise ConfigurationError("No current profile set")
            
            if name not in self._profiles:
                raise ConfigurationError(f"Profile '{name}' does not exist")
            
            return self._profiles[name].copy()
    
    def get_profile_names(self) -> List[str]:
        """Get list of available profile names."""
        with self._lock:
            return list(self._profiles.keys())
    
    def has_profile(self, name: str) -> bool:
        """Check if profile exists."""
        with self._lock:
            return name in self._profiles
    
    def get_profile_value(self, key: str, profile_name: Optional[str] = None, 
                         default: Any = None) -> Any:
        """Get a specific value from a profile."""
        profile = self.get_profile(profile_name)
        return profile.get(key, default)


class SettingsManager(SerializableMixin, TimestampedMixin, ThreadSafeMixin):
    """Manage application settings with validation."""
    
    def __init__(self, config_file: Optional[str] = None):
        super().__init__()
        self._config_file = config_file
        self._settings: Dict[str, Any] = {}
        self._validator = ConfigValidator()
        self._observers: List[Callable[[str, Any, Any], None]] = []
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def set_validator(self, validator: ConfigValidator):
        """Set the configuration validator."""
        with self._lock:
            self._validator = validator
            # Re-validate current settings
            if self._settings:
                self._settings = self._validator.validate(self._settings)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        with self._lock:
            old_value = self._settings.get(key)
            
            # Validate the new setting
            temp_settings = self._settings.copy()
            temp_settings[key] = value
            validated_settings = self._validator.validate(temp_settings)
            
            self._settings[key] = validated_settings[key]
            self._touch()
            
            # Notify observers
            for observer in self._observers:
                observer(key, old_value, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        with self._lock:
            return self._settings.get(key, default)
    
    def update(self, settings: Dict[str, Any]):
        """Update multiple settings."""
        with self._lock:
            old_settings = self._settings.copy()
            
            # Validate the updated settings
            temp_settings = self._settings.copy()
            temp_settings.update(settings)
            validated_settings = self._validator.validate(temp_settings)
            
            self._settings.update(validated_settings)
            self._touch()
            
            # Notify observers for changed values
            for key, new_value in settings.items():
                old_value = old_settings.get(key)
                if old_value != new_value:
                    for observer in self._observers:
                        observer(key, old_value, new_value)
    
    def delete(self, key: str):
        """Delete a setting."""
        with self._lock:
            if key in self._settings:
                old_value = self._settings[key]
                del self._settings[key]
                self._touch()
                
                # Notify observers
                for observer in self._observers:
                    observer(key, old_value, None)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings."""
        with self._lock:
            return self._settings.copy()
    
    def clear(self):
        """Clear all settings."""
        with self._lock:
            old_settings = self._settings.copy()
            self._settings.clear()
            self._touch()
            
            # Notify observers
            for key, old_value in old_settings.items():
                for observer in self._observers:
                    observer(key, old_value, None)
    
    def add_observer(self, observer: Callable[[str, Any, Any], None]):
        """Add an observer for setting changes."""
        with self._lock:
            self._observers.append(observer)
    
    def remove_observer(self, observer: Callable[[str, Any, Any], None]):
        """Remove an observer."""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
    
    def load_from_file(self, filename: str):
        """Load settings from JSON file."""
        try:
            with open(filename, 'r') as f:
                settings = json.load(f)
            self.update(settings)
        except Exception as e:
            raise ConfigurationError(f"Failed to load settings from file {filename}: {e}")
    
    def save_to_file(self, filename: Optional[str] = None):
        """Save settings to JSON file."""
        filename = filename or self._config_file
        if not filename:
            raise ConfigurationError("No filename specified for saving settings")
        
        try:
            with open(filename, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            raise ConfigurationError(f"Failed to save settings to file {filename}: {e}")
    
    def load_from_env(self, prefix: str = ""):
        """Load settings from environment variables."""
        env_settings = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                setting_key = key[len(prefix):].lower()
                # Try to parse as JSON, fall back to string
                try:
                    env_settings[setting_key] = json.loads(value)
                except json.JSONDecodeError:
                    env_settings[setting_key] = value
        
        if env_settings:
            self.update(env_settings)


def create_database_config_validator() -> ConfigValidator:
    """Create a configuration validator for database settings."""
    validator = ConfigValidator()
    
    # Basic database settings
    validator.add_type_validator('max_connections', int)
    validator.add_range_validator('max_connections', 1, 10000)
    validator.set_default('max_connections', 100)
    
    validator.add_type_validator('timeout', (int, float))
    validator.add_range_validator('timeout', 0.1, 300.0)
    validator.set_default('timeout', 30.0)
    
    validator.add_type_validator('buffer_size', int)
    validator.add_range_validator('buffer_size', 1024, 1024*1024*100)  # 1KB to 100MB
    validator.set_default('buffer_size', 1024*1024)  # 1MB
    
    # Logging settings
    validator.add_choices_validator('log_level', ['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    validator.set_default('log_level', 'INFO')
    
    validator.add_type_validator('enable_metrics', bool)
    validator.set_default('enable_metrics', True)
    
    return validator


def create_vector_config_validator() -> ConfigValidator:
    """Create a configuration validator for vector database settings."""
    validator = create_database_config_validator()
    
    # Vector-specific settings
    validator.add_type_validator('dimension', int)
    validator.add_range_validator('dimension', 1, 10000)
    validator.set_required('dimension')
    
    validator.add_choices_validator('distance_metric', 
                                  ['euclidean', 'cosine', 'manhattan', 'chebyshev'])
    validator.set_default('distance_metric', 'euclidean')
    
    validator.add_type_validator('index_type', str)
    validator.add_choices_validator('index_type', ['exact', 'approximate'])
    validator.set_default('index_type', 'exact')
    
    # LSH settings for approximate index
    validator.add_type_validator('num_hash_tables', int)
    validator.add_range_validator('num_hash_tables', 1, 100)
    validator.set_default('num_hash_tables', 10)
    
    validator.add_type_validator('hash_length', int)
    validator.add_range_validator('hash_length', 1, 64)
    validator.set_default('hash_length', 10)
    
    return validator


def create_sync_config_validator() -> ConfigValidator:
    """Create a configuration validator for sync database settings."""
    validator = create_database_config_validator()
    
    # Sync-specific settings
    validator.add_type_validator('sync_interval', (int, float))
    validator.add_range_validator('sync_interval', 1.0, 3600.0)  # 1 second to 1 hour
    validator.set_default('sync_interval', 60.0)
    
    validator.add_choices_validator('conflict_resolution', 
                                  ['last_write_wins', 'server_wins', 'client_wins', 'merge_fields'])
    validator.set_default('conflict_resolution', 'last_write_wins')
    
    validator.add_type_validator('enable_compression', bool)
    validator.set_default('enable_compression', True)
    
    validator.add_choices_validator('compression_level', ['NONE', 'LOW', 'MEDIUM', 'HIGH'])
    validator.set_default('compression_level', 'MEDIUM')
    
    # Power management settings
    validator.add_type_validator('enable_power_management', bool)
    validator.set_default('enable_power_management', True)
    
    validator.add_type_validator('low_power_threshold', (int, float))
    validator.add_range_validator('low_power_threshold', 0.0, 1.0)
    validator.set_default('low_power_threshold', 0.2)
    
    return validator