"""
Factory patterns for the unified in-memory database library.

This module provides common factory functionality that can be shared across both
vectordb and syncdb implementations.
"""

from typing import Dict, Any, Type, Callable, Optional, TypeVar, Generic
from abc import ABC, abstractmethod
from .base import ThreadSafeMixin
from .exceptions import ConfigurationError

T = TypeVar('T')


class ComponentFactory(ThreadSafeMixin, Generic[T]):
    """Generic factory for creating configurable components."""
    
    def __init__(self):
        super().__init__()
        self._creators: Dict[str, Callable[..., T]] = {}
        self._default_configs: Dict[str, Dict[str, Any]] = {}
        self._aliases: Dict[str, str] = {}
    
    def register(self, name: str, creator: Callable[..., T], 
                default_config: Optional[Dict[str, Any]] = None):
        """Register a component creator."""
        with self._lock:
            self._creators[name] = creator
            if default_config:
                self._default_configs[name] = default_config
    
    def register_alias(self, alias: str, name: str):
        """Register an alias for a component name."""
        with self._lock:
            if name not in self._creators:
                raise ConfigurationError(f"Cannot create alias '{alias}' for unknown component '{name}'")
            self._aliases[alias] = name
    
    def create(self, name: str, **kwargs) -> T:
        """Create a component by name."""
        with self._lock:
            # Resolve alias
            actual_name = self._aliases.get(name, name)
            
            if actual_name not in self._creators:
                available = list(self._creators.keys()) + list(self._aliases.keys())
                raise ConfigurationError(f"Unknown component '{name}'. Available: {available}")
            
            # Merge default config with provided kwargs
            config = self._default_configs.get(actual_name, {}).copy()
            config.update(kwargs)
            
            creator = self._creators[actual_name]
            try:
                return creator(**config)
            except Exception as e:
                raise ConfigurationError(f"Failed to create component '{name}': {e}")
    
    def get_available_components(self) -> Dict[str, str]:
        """Get available components and their aliases."""
        with self._lock:
            result = {}
            for name in self._creators.keys():
                result[name] = name
            for alias, name in self._aliases.items():
                result[alias] = name
            return result
    
    def has_component(self, name: str) -> bool:
        """Check if component is available."""
        with self._lock:
            actual_name = self._aliases.get(name, name)
            return actual_name in self._creators
    
    def unregister(self, name: str):
        """Unregister a component."""
        with self._lock:
            if name in self._creators:
                del self._creators[name]
            if name in self._default_configs:
                del self._default_configs[name]
            # Remove aliases pointing to this component
            aliases_to_remove = [alias for alias, target in self._aliases.items() if target == name]
            for alias in aliases_to_remove:
                del self._aliases[alias]


class RegistryMixin:
    """Mixin providing registry pattern for pluggable components."""
    
    def __init__(self):
        self._registry: Dict[str, Any] = {}
        self._registry_lock = __import__('threading').RLock()
    
    def register_component(self, name: str, component: Any):
        """Register a component."""
        with self._registry_lock:
            self._registry[name] = component
    
    def unregister_component(self, name: str):
        """Unregister a component."""
        with self._registry_lock:
            if name in self._registry:
                del self._registry[name]
    
    def get_component(self, name: str) -> Any:
        """Get a registered component."""
        with self._registry_lock:
            if name not in self._registry:
                raise ValueError(f"Component '{name}' not found in registry")
            return self._registry[name]
    
    def has_component(self, name: str) -> bool:
        """Check if component is registered."""
        with self._registry_lock:
            return name in self._registry
    
    def list_components(self) -> list:
        """List all registered component names."""
        with self._registry_lock:
            return list(self._registry.keys())
    
    def clear_registry(self):
        """Clear all registered components."""
        with self._registry_lock:
            self._registry.clear()


class SingletonMeta(type):
    """Metaclass for singleton pattern."""
    
    _instances = {}
    _lock = __import__('threading').Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractFactory(ABC):
    """Abstract factory interface."""
    
    @abstractmethod
    def create_component(self, component_type: str, **kwargs) -> Any:
        """Create a component of the specified type."""
        pass
    
    @abstractmethod
    def get_supported_types(self) -> list:
        """Get list of supported component types."""
        pass


class ConfigurableFactory(AbstractFactory):
    """Factory that creates components based on configuration."""
    
    def __init__(self):
        self._component_types: Dict[str, Type] = {}
        self._component_configs: Dict[str, Dict[str, Any]] = {}
    
    def register_type(self, type_name: str, component_class: Type, 
                     default_config: Optional[Dict[str, Any]] = None):
        """Register a component type."""
        self._component_types[type_name] = component_class
        if default_config:
            self._component_configs[type_name] = default_config
    
    def create_component(self, component_type: str, **kwargs) -> Any:
        """Create a component of the specified type."""
        if component_type not in self._component_types:
            raise ValueError(f"Unknown component type: {component_type}")
        
        component_class = self._component_types[component_type]
        
        # Merge default config with provided kwargs
        config = self._component_configs.get(component_type, {}).copy()
        config.update(kwargs)
        
        return component_class(**config)
    
    def get_supported_types(self) -> list:
        """Get list of supported component types."""
        return list(self._component_types.keys())


class ChainFactory:
    """Factory for creating chains of components."""
    
    def __init__(self, factory: ComponentFactory):
        self._factory = factory
    
    def create_chain(self, chain_config: list) -> list:
        """Create a chain of components from configuration."""
        chain = []
        
        for step_config in chain_config:
            if isinstance(step_config, str):
                # Simple component name
                component = self._factory.create(step_config)
            elif isinstance(step_config, dict):
                # Component with configuration
                component_name = step_config.pop('type')
                component = self._factory.create(component_name, **step_config)
            else:
                raise ValueError(f"Invalid chain step configuration: {step_config}")
            
            chain.append(component)
        
        return chain


class PluginManager:
    """Manager for dynamically loadable plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, Any] = {}
        self._plugin_metadata: Dict[str, Dict[str, Any]] = {}
    
    def register_plugin(self, name: str, plugin: Any, metadata: Optional[Dict[str, Any]] = None):
        """Register a plugin."""
        self._plugins[name] = plugin
        if metadata:
            self._plugin_metadata[name] = metadata
    
    def unregister_plugin(self, name: str):
        """Unregister a plugin."""
        if name in self._plugins:
            del self._plugins[name]
        if name in self._plugin_metadata:
            del self._plugin_metadata[name]
    
    def get_plugin(self, name: str) -> Any:
        """Get a plugin by name."""
        if name not in self._plugins:
            raise ValueError(f"Plugin '{name}' not found")
        return self._plugins[name]
    
    def list_plugins(self) -> Dict[str, Dict[str, Any]]:
        """List all plugins with their metadata."""
        return {
            name: {
                'plugin': plugin,
                'metadata': self._plugin_metadata.get(name, {})
            }
            for name, plugin in self._plugins.items()
        }
    
    def load_plugin_from_module(self, module_name: str, plugin_name: str, 
                               class_name: str, **kwargs):
        """Load a plugin from a module."""
        try:
            module = __import__(module_name, fromlist=[class_name])
            plugin_class = getattr(module, class_name)
            plugin = plugin_class(**kwargs)
            
            metadata = {
                'module': module_name,
                'class': class_name,
                'loaded_at': __import__('time').time()
            }
            
            self.register_plugin(plugin_name, plugin, metadata)
            return plugin
            
        except Exception as e:
            raise RuntimeError(f"Failed to load plugin '{plugin_name}' from module '{module_name}': {e}")


class DependencyInjector:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register_instance(self, service_name: str, instance: Any):
        """Register a service instance."""
        self._services[service_name] = instance
    
    def register_factory(self, service_name: str, factory: Callable[[], Any]):
        """Register a factory function for a service."""
        self._factories[service_name] = factory
    
    def register_singleton(self, service_name: str, factory: Callable[[], Any]):
        """Register a singleton service."""
        self._factories[service_name] = factory
        # Mark as singleton by adding to singletons dict with None value
        if service_name not in self._singletons:
            self._singletons[service_name] = None
    
    def get_service(self, service_name: str) -> Any:
        """Get a service instance."""
        # Check for direct instance
        if service_name in self._services:
            return self._services[service_name]
        
        # Check for singleton
        if service_name in self._singletons:
            if self._singletons[service_name] is None:
                # Create singleton instance
                factory = self._factories[service_name]
                self._singletons[service_name] = factory()
            return self._singletons[service_name]
        
        # Check for factory
        if service_name in self._factories:
            factory = self._factories[service_name]
            return factory()
        
        raise ValueError(f"Service '{service_name}' not found")
    
    def has_service(self, service_name: str) -> bool:
        """Check if service is registered."""
        return (service_name in self._services or 
                service_name in self._factories or 
                service_name in self._singletons)
    
    def list_services(self) -> list:
        """List all registered service names."""
        return list(set(
            list(self._services.keys()) + 
            list(self._factories.keys()) + 
            list(self._singletons.keys())
        ))


# Decorator for registering components
def register_component(registry: RegistryMixin, name: str):
    """Decorator to register a component in a registry."""
    def decorator(cls):
        registry.register_component(name, cls)
        return cls
    return decorator


# Decorator for creating singleton classes
def singleton(cls):
    """Decorator to make a class a singleton."""
    class SingletonClass(cls, metaclass=SingletonMeta):
        pass
    SingletonClass.__name__ = cls.__name__
    SingletonClass.__qualname__ = cls.__qualname__
    return SingletonClass