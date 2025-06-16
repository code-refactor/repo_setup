"""
Configuration management utilities for the unified query language interpreter.

This module provides configuration loading, validation, and management
functionality that can be used across all persona implementations.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""
    pass


class ConfigLoader:
    """Load and parse configuration from various sources."""
    
    def __init__(self):
        self.config_cache: Dict[str, Dict[str, Any]] = {}
    
    def load_from_file(self, file_path: Union[str, Path], 
                      cache: bool = True) -> Dict[str, Any]:
        """Load configuration from a file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise ConfigError(f"Configuration file not found: {file_path}")
        
        # Check cache first
        cache_key = str(file_path.absolute())
        if cache and cache_key in self.config_cache:
            return self.config_cache[cache_key]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    config = json.load(f)
                elif file_path.suffix.lower() in ['.yml', '.yaml']:
                    if not YAML_AVAILABLE:
                        raise ConfigError("PyYAML not available for YAML configuration files")
                    config = yaml.safe_load(f)
                else:
                    # Try to detect format from content
                    content = f.read()
                    f.seek(0)
                    
                    if content.strip().startswith('{'):
                        config = json.load(f)
                    elif YAML_AVAILABLE:
                        config = yaml.safe_load(f)
                    else:
                        raise ConfigError(f"Unsupported configuration file format: {file_path}")
            
            # Cache the result
            if cache:
                self.config_cache[cache_key] = config
            
            return config
            
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise ConfigError(f"Failed to parse configuration file {file_path}: {e}")
        except Exception as e:
            raise ConfigError(f"Error loading configuration file {file_path}: {e}")
    
    def load_from_env(self, prefix: str = "") -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}
        
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            
            # Remove prefix if present
            config_key = key[len(prefix):] if prefix else key
            config_key = config_key.lower()
            
            # Try to parse value as JSON first, then as string
            try:
                config[config_key] = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                config[config_key] = value
        
        return config
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Load configuration from a dictionary."""
        return config_dict.copy()
    
    def merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple configuration dictionaries."""
        merged = {}
        
        for config in configs:
            merged = self._deep_merge(merged, config)
        
        return merged
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result


class ConfigValidator:
    """Validate configuration against schemas and rules."""
    
    def __init__(self):
        self.validation_rules: Dict[str, List[callable]] = {}
    
    def add_validation_rule(self, key: str, validator: callable):
        """Add a validation rule for a configuration key."""
        if key not in self.validation_rules:
            self.validation_rules[key] = []
        self.validation_rules[key].append(validator)
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Run custom validation rules
        for key, validators in self.validation_rules.items():
            if key in config:
                for validator in validators:
                    try:
                        if not validator(config[key]):
                            errors.append(f"Validation failed for key '{key}'")
                    except Exception as e:
                        errors.append(f"Validation error for key '{key}': {e}")
        
        return errors
    
    def validate_required_keys(self, config: Dict[str, Any], 
                             required_keys: List[str]) -> List[str]:
        """Validate that required keys are present."""
        errors = []
        
        for key in required_keys:
            if key not in config:
                errors.append(f"Required configuration key missing: '{key}'")
            elif config[key] is None:
                errors.append(f"Required configuration key is None: '{key}'")
        
        return errors
    
    def validate_types(self, config: Dict[str, Any], 
                      type_specs: Dict[str, type]) -> List[str]:
        """Validate configuration value types."""
        errors = []
        
        for key, expected_type in type_specs.items():
            if key in config:
                if not isinstance(config[key], expected_type):
                    actual_type = type(config[key]).__name__
                    expected_type_name = expected_type.__name__
                    errors.append(
                        f"Configuration key '{key}' has type {actual_type}, "
                        f"expected {expected_type_name}"
                    )
        
        return errors


class ConfigManager:
    """High-level configuration management."""
    
    def __init__(self, config_paths: Optional[List[Union[str, Path]]] = None):
        self.loader = ConfigLoader()
        self.validator = ConfigValidator()
        self.config: Dict[str, Any] = {}
        self.config_paths = config_paths or []
        
        # Setup default validation rules
        self._setup_default_validations()
    
    def load_configuration(self, env_prefix: str = "UNIFIED_QUERY_") -> Dict[str, Any]:
        """Load configuration from multiple sources."""
        configs = []
        
        # Load from files
        for path in self.config_paths:
            try:
                config = self.loader.load_from_file(path)
                configs.append(config)
            except ConfigError:
                # Skip missing or invalid config files
                continue
        
        # Load from environment
        env_config = self.loader.load_from_env(env_prefix)
        if env_config:
            configs.append(env_config)
        
        # Merge all configurations
        if configs:
            self.config = self.loader.merge_configs(*configs)
        
        # Validate configuration
        errors = self.validate_configuration()
        if errors:
            raise ConfigError(f"Configuration validation failed: {'; '.join(errors)}")
        
        return self.config
    
    def validate_configuration(self) -> List[str]:
        """Validate the current configuration."""
        errors = []
        
        # Validate required keys
        required_keys = ['logging', 'audit']
        errors.extend(self.validator.validate_required_keys(self.config, required_keys))
        
        # Validate types
        type_specs = {
            'max_query_length': int,
            'query_timeout_seconds': int,
            'max_results': int,
            'enable_audit_logging': bool,
            'debug_mode': bool
        }
        errors.extend(self.validator.validate_types(self.config, type_specs))
        
        # Custom validation
        errors.extend(self.validator.validate_config(self.config))
        
        return errors
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with dot notation support."""
        return self._get_nested_value(self.config, key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value with dot notation support."""
        self._set_nested_value(self.config, key, value)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get an entire configuration section."""
        return self.get(section, {})
    
    def has_key(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return self._get_nested_value(self.config, key, None) is not None
    
    def _get_nested_value(self, obj: Dict[str, Any], key: str, default: Any) -> Any:
        """Get nested value using dot notation."""
        keys = key.split('.')
        current = obj
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def _set_nested_value(self, obj: Dict[str, Any], key: str, value: Any):
        """Set nested value using dot notation."""
        keys = key.split('.')
        current = obj
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def _setup_default_validations(self):
        """Setup default validation rules."""
        # Positive integer validation
        def positive_int(value):
            return isinstance(value, int) and value > 0
        
        # Non-negative integer validation
        def non_negative_int(value):
            return isinstance(value, int) and value >= 0
        
        # String validation
        def non_empty_string(value):
            return isinstance(value, str) and len(value.strip()) > 0
        
        # Add validation rules
        self.validator.add_validation_rule('max_query_length', positive_int)
        self.validator.add_validation_rule('query_timeout_seconds', positive_int)
        self.validator.add_validation_rule('max_results', positive_int)
        self.validator.add_validation_rule('audit.max_events', positive_int)


class DefaultConfig:
    """Provide default configuration values."""
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration dictionary."""
        return {
            'debug_mode': False,
            'max_query_length': 10000,
            'query_timeout_seconds': 300,
            'max_results': 1000,
            'enable_audit_logging': True,
            
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file_path': None,
                'max_file_size': 10485760,  # 10MB
                'backup_count': 5
            },
            
            'audit': {
                'max_events': 10000,
                'enable_integrity_check': True,
                'hmac_key': None,  # Will be generated if not provided
                'retention_days': 90
            },
            
            'security': {
                'allowed_functions': [],
                'forbidden_keywords': ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE'],
                'max_execution_time': 300,
                'enable_sql_injection_check': True
            },
            
            'performance': {
                'cache_size': 100,
                'cache_ttl_seconds': 3600,
                'enable_query_optimization': True,
                'max_concurrent_queries': 10
            },
            
            'data_sources': {
                'default_connection_timeout': 30,
                'max_connections': 50,
                'connection_retry_attempts': 3
            }
        }


class ConfigFileGenerator:
    """Generate configuration files from templates."""
    
    @staticmethod
    def generate_json_config(output_path: Union[str, Path], 
                           config: Optional[Dict[str, Any]] = None):
        """Generate a JSON configuration file."""
        if config is None:
            config = DefaultConfig.get_default_config()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, sort_keys=True)
    
    @staticmethod
    def generate_yaml_config(output_path: Union[str, Path], 
                           config: Optional[Dict[str, Any]] = None):
        """Generate a YAML configuration file."""
        if not YAML_AVAILABLE:
            raise ConfigError("PyYAML not available for YAML configuration generation")
        
        if config is None:
            config = DefaultConfig.get_default_config()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=True, indent=2)
    
    @staticmethod
    def generate_env_template(output_path: Union[str, Path], 
                            config: Optional[Dict[str, Any]] = None,
                            prefix: str = "UNIFIED_QUERY_"):
        """Generate an environment variables template file."""
        if config is None:
            config = DefaultConfig.get_default_config()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# Environment configuration template for Unified Query Language Interpreter\n")
            f.write(f"# Prefix: {prefix}\n\n")
            
            ConfigFileGenerator._write_env_section(f, config, prefix)
    
    @staticmethod
    def _write_env_section(f, config: Dict[str, Any], prefix: str, parent_key: str = ""):
        """Write configuration section to environment file."""
        for key, value in config.items():
            env_key = f"{prefix}{parent_key}{key}".upper()
            
            if isinstance(value, dict):
                f.write(f"\n# {key.title()} configuration\n")
                ConfigFileGenerator._write_env_section(f, value, prefix, f"{parent_key}{key}_")
            else:
                f.write(f"{env_key}={json.dumps(value) if not isinstance(value, (str, int, float, bool)) else value}\n")