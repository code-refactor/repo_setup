"""
Import/export framework for the unified personal knowledge management library.
"""

import json
import os
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from uuid import UUID

try:
    from jinja2 import Environment, FileSystemLoader, Template
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False

from .models import BaseKnowledgeNode
from .storage import BaseStorage

T = TypeVar('T', bound=BaseKnowledgeNode)


class BaseExporter(ABC):
    """Base class for data exporters."""
    
    def __init__(self, storage: BaseStorage):
        self.storage = storage
    
    @abstractmethod
    def export(self, data: List[T], output_path: Union[str, Path], **kwargs) -> bool:
        """Export data to a file."""
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get the file extension for this exporter."""
        pass
    
    def prepare_data(self, data: List[T]) -> List[Dict[str, Any]]:
        """Prepare data for export by converting to dictionaries."""
        prepared_data = []
        for item in data:
            item_dict = item.model_dump()
            # Convert UUIDs to strings for serialization
            for key, value in item_dict.items():
                if isinstance(value, UUID):
                    item_dict[key] = str(value)
                elif isinstance(value, set):
                    item_dict[key] = list(value)
                elif isinstance(value, datetime):
                    item_dict[key] = value.isoformat()
            prepared_data.append(item_dict)
        return prepared_data


class JSONExporter(BaseExporter):
    """Export data to JSON format."""
    
    def export(self, data: List[T], output_path: Union[str, Path], **kwargs) -> bool:
        """Export data to JSON file."""
        try:
            prepared_data = self.prepare_data(data)
            
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'total_items': len(prepared_data),
                'data_type': data[0].__class__.__name__ if data else 'Unknown',
                'items': prepared_data
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def get_file_extension(self) -> str:
        return '.json'


class MarkdownExporter(BaseExporter):
    """Export data to Markdown format."""
    
    def export(self, data: List[T], output_path: Union[str, Path], **kwargs) -> bool:
        """Export data to Markdown file."""
        try:
            template = kwargs.get('template', self._get_default_template())
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Export Report\n\n")
                f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Items:** {len(data)}\n")
                f.write(f"**Data Type:** {data[0].__class__.__name__ if data else 'Unknown'}\n\n")
                
                for item in data:
                    f.write(self._format_item_markdown(item, template))
                    f.write("\n---\n\n")
            
            return True
        except Exception as e:
            print(f"Error exporting to Markdown: {e}")
            return False
    
    def get_file_extension(self) -> str:
        return '.md'
    
    def _get_default_template(self) -> str:
        """Get default Markdown template."""
        return """## {title}

**ID:** {id}
**Created:** {created_at}
**Updated:** {updated_at}

{content}

**Tags:** {tags}
"""
    
    def _format_item_markdown(self, item: T, template: str) -> str:
        """Format a single item as Markdown."""
        item_dict = item.model_dump()
        
        # Convert complex types to strings
        for key, value in item_dict.items():
            if isinstance(value, UUID):
                item_dict[key] = str(value)
            elif isinstance(value, set):
                item_dict[key] = ', '.join(sorted(value))
            elif isinstance(value, datetime):
                item_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, list):
                item_dict[key] = ', '.join(str(v) for v in value)
        
        # Set defaults for missing fields
        defaults = {
            'title': item_dict.get('title', f"Item {item_dict.get('id', 'Unknown')}"),
            'content': item_dict.get('content', 'No content available'),
            'tags': item_dict.get('tags', 'None')
        }
        
        for key, default_value in defaults.items():
            if key not in item_dict or not item_dict[key]:
                item_dict[key] = default_value
        
        try:
            return template.format(**item_dict)
        except KeyError as e:
            # Fallback to simple format if template fails
            return f"## {item_dict.get('title', 'Item')}\n\n{item_dict.get('content', 'No content')}\n"


class CSVExporter(BaseExporter):
    """Export data to CSV format."""
    
    def export(self, data: List[T], output_path: Union[str, Path], **kwargs) -> bool:
        """Export data to CSV file."""
        try:
            import csv
            
            if not data:
                return False
            
            prepared_data = self.prepare_data(data)
            
            # Get all unique fields from all items
            all_fields = set()
            for item in prepared_data:
                all_fields.update(item.keys())
            
            # Sort fields for consistent output
            fieldnames = sorted(all_fields)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for item in prepared_data:
                    # Convert complex types to strings for CSV
                    csv_item = {}
                    for field in fieldnames:
                        value = item.get(field, '')
                        if isinstance(value, (list, dict)):
                            csv_item[field] = json.dumps(value)
                        else:
                            csv_item[field] = str(value) if value is not None else ''
                    writer.writerow(csv_item)
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def get_file_extension(self) -> str:
        return '.csv'


class TemplateEngine:
    """Template engine for generating formatted output."""
    
    def __init__(self, template_dir: Optional[Union[str, Path]] = None):
        self.template_dir = Path(template_dir) if template_dir else None
        self.jinja_env = None
        
        if HAS_JINJA2 and self.template_dir and self.template_dir.exists():
            self.jinja_env = Environment(loader=FileSystemLoader(str(self.template_dir)))
    
    def render_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Render a template with data."""
        if HAS_JINJA2:
            template = Template(template_content)
            return template.render(**data)
        else:
            # Simple string formatting fallback
            try:
                return template_content.format(**data)
            except KeyError:
                return template_content
    
    def render_file_template(self, template_name: str, data: Dict[str, Any]) -> str:
        """Render a template file with data."""
        if self.jinja_env:
            template = self.jinja_env.get_template(template_name)
            return template.render(**data)
        else:
            # Try to read template file and use simple formatting
            if self.template_dir:
                template_path = self.template_dir / template_name
                if template_path.exists():
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                    return self.render_template(template_content, data)
            return ""
    
    def get_available_templates(self) -> List[str]:
        """Get list of available template files."""
        if not self.template_dir or not self.template_dir.exists():
            return []
        
        templates = []
        for file_path in self.template_dir.glob("*.html"):
            templates.append(file_path.name)
        for file_path in self.template_dir.glob("*.md"):
            templates.append(file_path.name)
        for file_path in self.template_dir.glob("*.txt"):
            templates.append(file_path.name)
        
        return sorted(templates)


class DocumentGenerator:
    """Generate documents from data using templates."""
    
    def __init__(self, storage: BaseStorage, template_dir: Optional[Union[str, Path]] = None):
        self.storage = storage
        self.template_engine = TemplateEngine(template_dir)
        self.exporters = {
            'json': JSONExporter(storage),
            'markdown': MarkdownExporter(storage),
            'csv': CSVExporter(storage)
        }
    
    def generate_report(self, model_type: Type[T], output_path: Union[str, Path],
                       template: Optional[str] = None, format_type: str = 'markdown',
                       filters: Optional[Dict[str, Any]] = None) -> bool:
        """Generate a report for a specific model type."""
        try:
            # Get data
            if filters:
                data = self.storage.query(model_type, **filters)
            else:
                data = self.storage.get_all(model_type)
            
            if not data:
                print(f"No data found for {model_type.__name__}")
                return False
            
            # Get exporter
            exporter = self.exporters.get(format_type)
            if not exporter:
                print(f"Unknown format type: {format_type}")
                return False
            
            # Generate report
            kwargs = {}
            if template:
                kwargs['template'] = template
            
            return exporter.export(data, output_path, **kwargs)
        
        except Exception as e:
            print(f"Error generating report: {e}")
            return False
    
    def generate_custom_document(self, data: List[T], template_name: str,
                                output_path: Union[str, Path], 
                                additional_context: Optional[Dict[str, Any]] = None) -> bool:
        """Generate a custom document using a template."""
        try:
            # Prepare data
            prepared_data = []
            for item in data:
                item_dict = item.model_dump()
                # Convert complex types
                for key, value in item_dict.items():
                    if isinstance(value, UUID):
                        item_dict[key] = str(value)
                    elif isinstance(value, set):
                        item_dict[key] = list(value)
                    elif isinstance(value, datetime):
                        item_dict[key] = value.isoformat()
                prepared_data.append(item_dict)
            
            # Prepare context
            context = {
                'items': prepared_data,
                'total_items': len(prepared_data),
                'generated_at': datetime.now().isoformat(),
                'data_type': data[0].__class__.__name__ if data else 'Unknown'
            }
            
            if additional_context:
                context.update(additional_context)
            
            # Render template
            content = self.template_engine.render_file_template(template_name, context)
            
            if not content:
                print(f"Failed to render template: {template_name}")
                return False
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        
        except Exception as e:
            print(f"Error generating custom document: {e}")
            return False
    
    def export_multiple_formats(self, model_type: Type[T], base_path: Union[str, Path],
                               formats: List[str] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, bool]:
        """Export data in multiple formats."""
        if formats is None:
            formats = ['json', 'markdown', 'csv']
        
        results = {}
        base_path = Path(base_path)
        
        for format_type in formats:
            if format_type in self.exporters:
                exporter = self.exporters[format_type]
                output_path = base_path.with_suffix(exporter.get_file_extension())
                success = self.generate_report(model_type, output_path, format_type=format_type, filters=filters)
                results[format_type] = success
            else:
                results[format_type] = False
        
        return results


class MetadataExtractor:
    """Extract metadata from various file types."""
    
    def __init__(self):
        self.extractors = {
            '.json': self._extract_json_metadata,
            '.md': self._extract_markdown_metadata,
            '.txt': self._extract_text_metadata
        }
    
    def extract_metadata(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """Extract metadata from a file."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {}
        
        metadata = {
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size,
            'created_at': datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
            'modified_at': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            'file_extension': file_path.suffix.lower()
        }
        
        # Extract format-specific metadata
        extractor = self.extractors.get(file_path.suffix.lower())
        if extractor:
            try:
                format_metadata = extractor(file_path)
                metadata.update(format_metadata)
            except Exception as e:
                metadata['extraction_error'] = str(e)
        
        return metadata
    
    def _extract_json_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        metadata = {
            'content_type': 'json',
            'structure_type': type(data).__name__
        }
        
        if isinstance(data, dict):
            metadata['top_level_keys'] = list(data.keys())
            if 'items' in data and isinstance(data['items'], list):
                metadata['item_count'] = len(data['items'])
        elif isinstance(data, list):
            metadata['item_count'] = len(data)
        
        return metadata
    
    def _extract_markdown_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from Markdown file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        metadata = {
            'content_type': 'markdown',
            'line_count': len(lines),
            'character_count': len(content),
            'word_count': len(content.split())
        }
        
        # Count headers
        header_counts = {}
        for line in lines:
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                header_counts[f'h{level}'] = header_counts.get(f'h{level}', 0) + 1
        
        if header_counts:
            metadata['header_counts'] = header_counts
        
        return metadata
    
    def _extract_text_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        return {
            'content_type': 'text',
            'line_count': len(lines),
            'character_count': len(content),
            'word_count': len(content.split()),
            'empty_lines': sum(1 for line in lines if not line.strip())
        }