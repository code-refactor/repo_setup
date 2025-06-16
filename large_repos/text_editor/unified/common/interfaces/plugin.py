from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

from ..core.models import Change, Position
from .editor import EditorInterface


class Command:
    """Represents a command that can be executed."""
    
    def __init__(self, name: str, description: str, handler: Callable, 
                 shortcut: Optional[str] = None, category: str = "General"):
        self.name = name
        self.description = description
        self.handler = handler
        self.shortcut = shortcut
        self.category = category
        self.enabled = True
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the command."""
        if not self.enabled:
            raise RuntimeError(f"Command '{self.name}' is disabled")
        return self.handler(*args, **kwargs)


class MenuAction:
    """Represents a menu action."""
    
    def __init__(self, label: str, command: Command, separator_before: bool = False):
        self.label = label
        self.command = command
        self.separator_before = separator_before


class ToolbarAction:
    """Represents a toolbar action."""
    
    def __init__(self, label: str, command: Command, icon: Optional[str] = None, 
                 tooltip: Optional[str] = None):
        self.label = label
        self.command = command
        self.icon = icon
        self.tooltip = tooltip or command.description


class PluginInterface(ABC):
    """Abstract interface for editor plugins."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the plugin name."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Get the plugin version."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get the plugin description."""
        pass
    
    @abstractmethod
    def get_author(self) -> str:
        """Get the plugin author."""
        pass
    
    @abstractmethod
    def initialize(self, editor: EditorInterface) -> None:
        """Initialize the plugin with the editor instance."""
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the plugin and clean up resources."""
        pass
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if the plugin is enabled."""
        pass
    
    @abstractmethod
    def enable(self) -> None:
        """Enable the plugin."""
        pass
    
    @abstractmethod
    def disable(self) -> None:
        """Disable the plugin."""
        pass
    
    def get_commands(self) -> List[Command]:
        """Get list of commands provided by the plugin."""
        return []
    
    def get_menu_actions(self) -> Dict[str, List[MenuAction]]:
        """Get menu actions organized by menu name."""
        return {}
    
    def get_toolbar_actions(self) -> List[ToolbarAction]:
        """Get toolbar actions provided by the plugin."""
        return []
    
    def get_settings_schema(self) -> Dict[str, Any]:
        """Get the schema for plugin settings."""
        return {}
    
    def get_settings(self) -> Dict[str, Any]:
        """Get current plugin settings."""
        return {}
    
    def set_settings(self, settings: Dict[str, Any]) -> None:
        """Set plugin settings."""
        pass
    
    def on_text_changed(self, change: Change) -> None:
        """Handle text change events."""
        pass
    
    def on_cursor_moved(self, old_pos: Position, new_pos: Position) -> None:
        """Handle cursor movement events."""
        pass
    
    def on_selection_changed(self, old_selection, new_selection) -> None:
        """Handle selection change events."""
        pass
    
    def on_file_opened(self, file_path: str) -> None:
        """Handle file open events."""
        pass
    
    def on_file_saved(self, file_path: str) -> None:
        """Handle file save events."""
        pass
    
    def on_file_closed(self, file_path: str) -> None:
        """Handle file close events."""
        pass


class PersonaExtension(PluginInterface):
    """Base class for persona-specific extensions."""
    
    @abstractmethod
    def get_persona_name(self) -> str:
        """Get the name of the persona this extension supports."""
        pass
    
    @abstractmethod
    def get_features(self) -> List[str]:
        """Get list of features provided by this persona."""
        pass
    
    @abstractmethod
    def configure_ui(self, ui_manager) -> None:
        """Configure persona-specific UI elements."""
        pass
    
    @abstractmethod
    def get_analytics(self) -> Dict[str, Any]:
        """Get persona-specific analytics data."""
        pass
    
    def get_persona_settings(self) -> Dict[str, Any]:
        """Get persona-specific settings."""
        return {}
    
    def set_persona_settings(self, settings: Dict[str, Any]) -> None:
        """Set persona-specific settings."""
        pass
    
    def on_persona_activated(self) -> None:
        """Handle persona activation."""
        pass
    
    def on_persona_deactivated(self) -> None:
        """Handle persona deactivation."""
        pass


class ThemePlugin(PluginInterface):
    """Interface for theme plugins."""
    
    @abstractmethod
    def get_theme_name(self) -> str:
        """Get the theme name."""
        pass
    
    @abstractmethod
    def get_color_scheme(self) -> Dict[str, str]:
        """Get the color scheme definition."""
        pass
    
    @abstractmethod
    def get_font_settings(self) -> Dict[str, Any]:
        """Get font settings."""
        pass
    
    @abstractmethod
    def apply_theme(self, ui_manager) -> None:
        """Apply the theme to the UI."""
        pass


class LanguageSupport(PluginInterface):
    """Interface for language support plugins."""
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        pass
    
    @abstractmethod
    def get_file_extensions(self) -> List[str]:
        """Get file extensions for supported languages."""
        pass
    
    @abstractmethod
    def get_syntax_highlighter(self, language: str):
        """Get syntax highlighter for a specific language."""
        pass
    
    @abstractmethod
    def get_auto_complete_suggestions(self, context: str, position: Position) -> List[str]:
        """Get auto-completion suggestions."""
        pass
    
    @abstractmethod
    def format_code(self, code: str, language: str) -> str:
        """Format code according to language conventions."""
        pass
    
    @abstractmethod
    def validate_syntax(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Validate syntax and return errors/warnings."""
        pass


class ExportPlugin(PluginInterface):
    """Interface for export/import plugins."""
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export/import formats."""
        pass
    
    @abstractmethod
    def export_document(self, content: str, format: str, 
                       options: Optional[Dict[str, Any]] = None) -> bytes:
        """Export document to specified format."""
        pass
    
    @abstractmethod
    def import_document(self, data: bytes, format: str,
                       options: Optional[Dict[str, Any]] = None) -> str:
        """Import document from specified format."""
        pass
    
    @abstractmethod
    def get_export_options(self, format: str) -> Dict[str, Any]:
        """Get available export options for a format."""
        pass


class AnalyticsPlugin(PluginInterface):
    """Interface for analytics plugins."""
    
    @abstractmethod
    def track_event(self, event_name: str, properties: Dict[str, Any]) -> None:
        """Track an analytics event."""
        pass
    
    @abstractmethod
    def track_user_action(self, action: str, context: Dict[str, Any]) -> None:
        """Track a user action."""
        pass
    
    @abstractmethod
    def get_usage_statistics(self) -> Dict[str, Any]:
        """Get usage statistics."""
        pass
    
    @abstractmethod
    def generate_report(self, report_type: str, date_range: tuple) -> Dict[str, Any]:
        """Generate an analytics report."""
        pass
    
    @abstractmethod
    def export_data(self, format: str = "json") -> str:
        """Export analytics data."""
        pass


class CloudSyncPlugin(PluginInterface):
    """Interface for cloud synchronization plugins."""
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Authenticate with cloud service."""
        pass
    
    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if authenticated with cloud service."""
        pass
    
    @abstractmethod
    def sync_document(self, document_path: str) -> bool:
        """Sync a document to cloud storage."""
        pass
    
    @abstractmethod
    def download_document(self, cloud_path: str, local_path: str) -> bool:
        """Download a document from cloud storage."""
        pass
    
    @abstractmethod
    def list_cloud_documents(self) -> List[Dict[str, Any]]:
        """List documents in cloud storage."""
        pass
    
    @abstractmethod
    def resolve_conflicts(self, conflicts: List[Dict[str, Any]]) -> bool:
        """Resolve synchronization conflicts."""
        pass


class PluginManager:
    """Manages plugin loading, activation, and lifecycle."""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.enabled_plugins: set = set()
        self.plugin_dependencies: Dict[str, List[str]] = {}
    
    def register_plugin(self, plugin: PluginInterface) -> bool:
        """Register a plugin."""
        plugin_name = plugin.get_name()
        if plugin_name in self.plugins:
            return False
        
        self.plugins[plugin_name] = plugin
        return True
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin."""
        if plugin_name not in self.plugins:
            return False
        
        if plugin_name in self.enabled_plugins:
            self.disable_plugin(plugin_name)
        
        del self.plugins[plugin_name]
        return True
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a plugin."""
        if plugin_name not in self.plugins:
            return False
        
        plugin = self.plugins[plugin_name]
        
        # Check dependencies
        dependencies = self.plugin_dependencies.get(plugin_name, [])
        for dep in dependencies:
            if dep not in self.enabled_plugins:
                if not self.enable_plugin(dep):
                    return False
        
        plugin.enable()
        self.enabled_plugins.add(plugin_name)
        return True
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin."""
        if plugin_name not in self.plugins or plugin_name not in self.enabled_plugins:
            return False
        
        plugin = self.plugins[plugin_name]
        plugin.disable()
        self.enabled_plugins.discard(plugin_name)
        return True
    
    def get_enabled_plugins(self) -> List[PluginInterface]:
        """Get list of enabled plugins."""
        return [self.plugins[name] for name in self.enabled_plugins]
    
    def get_plugins_by_type(self, plugin_type: type) -> List[PluginInterface]:
        """Get plugins of a specific type."""
        return [plugin for plugin in self.plugins.values() 
                if isinstance(plugin, plugin_type)]
    
    def add_dependency(self, plugin_name: str, dependency: str) -> None:
        """Add a plugin dependency."""
        if plugin_name not in self.plugin_dependencies:
            self.plugin_dependencies[plugin_name] = []
        self.plugin_dependencies[plugin_name].append(dependency)
    
    def shutdown_all_plugins(self) -> None:
        """Shutdown all plugins."""
        for plugin in self.enabled_plugins.copy():
            self.disable_plugin(plugin)
        
        for plugin in self.plugins.values():
            plugin.shutdown()