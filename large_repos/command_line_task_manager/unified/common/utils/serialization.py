"""Serialization utilities for the unified command line task manager."""

import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from uuid import UUID

from ..core.models import BaseEntity


EntityType = TypeVar('EntityType', bound=BaseEntity)


class DateTimeUtils:
    """Utilities for datetime handling and serialization."""
    
    # Standard ISO format
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    
    # Alternative formats for parsing
    PARSE_FORMATS = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d"
    ]
    
    @staticmethod
    def to_iso_string(dt: datetime) -> str:
        """Convert datetime to ISO string."""
        return dt.strftime(DateTimeUtils.ISO_FORMAT)
    
    @staticmethod
    def from_iso_string(iso_string: str) -> datetime:
        """Parse datetime from ISO string."""
        if not isinstance(iso_string, str):
            raise ValueError(f"Expected string, got {type(iso_string)}")
        
        # Try different formats
        for fmt in DateTimeUtils.PARSE_FORMATS:
            try:
                return datetime.strptime(iso_string, fmt)
            except ValueError:
                continue
        
        # If none worked, try fromisoformat (Python 3.7+)
        try:
            # Handle Z timezone indicator
            if iso_string.endswith('Z'):
                iso_string = iso_string[:-1] + '+00:00'
            return datetime.fromisoformat(iso_string)
        except ValueError:
            pass
        
        raise ValueError(f"Unable to parse datetime string: {iso_string}")
    
    @staticmethod
    def now_iso() -> str:
        """Get current datetime as ISO string."""
        return DateTimeUtils.to_iso_string(datetime.now())
    
    @staticmethod
    def is_valid_iso_string(iso_string: str) -> bool:
        """Check if string is a valid ISO datetime."""
        try:
            DateTimeUtils.from_iso_string(iso_string)
            return True
        except (ValueError, TypeError):
            return False


class UUIDUtils:
    """Utilities for UUID handling and serialization."""
    
    @staticmethod
    def to_string(uuid_obj: UUID) -> str:
        """Convert UUID to string."""
        return str(uuid_obj)
    
    @staticmethod
    def from_string(uuid_string: str) -> UUID:
        """Parse UUID from string."""
        if not isinstance(uuid_string, str):
            raise ValueError(f"Expected string, got {type(uuid_string)}")
        
        try:
            return UUID(uuid_string)
        except ValueError as e:
            raise ValueError(f"Invalid UUID string: {uuid_string}") from e
    
    @staticmethod
    def is_valid_uuid_string(uuid_string: str) -> bool:
        """Check if string is a valid UUID."""
        try:
            UUIDUtils.from_string(uuid_string)
            return True
        except (ValueError, TypeError):
            return False


class EntitySerializer:
    """Serializer for entity objects with support for complex types."""
    
    def __init__(self, indent: Optional[int] = None, sort_keys: bool = True):
        self.indent = indent
        self.sort_keys = sort_keys
    
    def serialize(self, obj: Any) -> str:
        """Serialize an object to JSON string."""
        return json.dumps(obj, default=self._json_encoder, 
                         indent=self.indent, sort_keys=self.sort_keys)
    
    def deserialize(self, json_string: str) -> Any:
        """Deserialize JSON string to object."""
        try:
            return json.loads(json_string, object_hook=self._json_decoder)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")
    
    def serialize_entity(self, entity: BaseEntity) -> str:
        """Serialize a BaseEntity to JSON string."""
        return self.serialize(self._entity_to_dict(entity))
    
    def deserialize_entity(self, json_string: str, entity_class: Type[EntityType]) -> EntityType:
        """Deserialize JSON string to entity object."""
        data = self.deserialize(json_string)
        return self._dict_to_entity(data, entity_class)
    
    def serialize_entities(self, entities: List[BaseEntity]) -> str:
        """Serialize a list of entities to JSON string."""
        entity_dicts = [self._entity_to_dict(entity) for entity in entities]
        return self.serialize(entity_dicts)
    
    def deserialize_entities(self, json_string: str, entity_class: Type[EntityType]) -> List[EntityType]:
        """Deserialize JSON string to list of entities."""
        data_list = self.deserialize(json_string)
        if not isinstance(data_list, list):
            raise ValueError("Expected JSON array for entity list")
        
        return [self._dict_to_entity(data, entity_class) for data in data_list]
    
    def _entity_to_dict(self, entity: BaseEntity) -> Dict[str, Any]:
        """Convert entity to dictionary with proper type handling."""
        return entity.model_dump()
    
    def _dict_to_entity(self, data: Dict[str, Any], entity_class: Type[EntityType]) -> EntityType:
        """Convert dictionary to entity with proper type handling."""
        # Convert string UUIDs and datetimes
        processed_data = self._process_entity_dict(data)
        return entity_class(**processed_data)
    
    def _process_entity_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process dictionary to convert string representations to proper types."""
        processed = {}
        
        for key, value in data.items():
            if value is None:
                processed[key] = value
            elif key == 'id' or key.endswith('_id') or key.endswith('_ids'):
                # Handle UUID fields
                if isinstance(value, str):
                    if key.endswith('_ids') or isinstance(value, list):
                        # Handle UUID lists/sets
                        if isinstance(value, str):
                            processed[key] = {UUIDUtils.from_string(value)}  # Single UUID as set
                        else:
                            processed[key] = {UUIDUtils.from_string(v) for v in value if v}
                    else:
                        processed[key] = UUIDUtils.from_string(value)
                elif isinstance(value, list):
                    processed[key] = {UUIDUtils.from_string(v) for v in value if v}
                else:
                    processed[key] = value
            elif key.endswith('_at') or key.endswith('_date'):
                # Handle datetime fields
                if isinstance(value, str):
                    processed[key] = DateTimeUtils.from_iso_string(value)
                else:
                    processed[key] = value
            elif isinstance(value, dict):
                # Recursively process nested dictionaries
                processed[key] = self._process_entity_dict(value)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # Process list of dictionaries
                processed[key] = [self._process_entity_dict(item) for item in value]
            else:
                processed[key] = value
        
        return processed
    
    def _json_encoder(self, obj: Any) -> Any:
        """Custom JSON encoder for complex types."""
        if isinstance(obj, datetime):
            return DateTimeUtils.to_iso_string(obj)
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return UUIDUtils.to_string(obj)
        elif isinstance(obj, set):
            return list(obj)
        elif hasattr(obj, 'model_dump'):
            # Pydantic model
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):
            # General object with attributes
            return obj.__dict__
        else:
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    def _json_decoder(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        """Custom JSON decoder for complex types."""
        # This is a simple decoder that doesn't automatically convert types
        # Type conversion happens in _process_entity_dict when we know the context
        return obj


class DataExporter:
    """Export entities to various formats."""
    
    def __init__(self, serializer: Optional[EntitySerializer] = None):
        self.serializer = serializer or EntitySerializer(indent=2)
    
    def export_to_json(self, entities: List[BaseEntity], 
                      include_metadata: bool = True) -> str:
        """Export entities to JSON format."""
        export_data = {
            "entities": [self.serializer._entity_to_dict(entity) for entity in entities]
        }
        
        if include_metadata:
            export_data["metadata"] = {
                "export_timestamp": DateTimeUtils.now_iso(),
                "entity_count": len(entities),
                "entity_types": list(set(type(entity).__name__ for entity in entities))
            }
        
        return self.serializer.serialize(export_data)
    
    def export_to_csv(self, entities: List[BaseEntity], 
                     include_fields: Optional[List[str]] = None) -> str:
        """Export entities to CSV format."""
        if not entities:
            return ""
        
        import csv
        import io
        
        output = io.StringIO()
        
        # Determine fields to include
        if include_fields is None:
            # Use all fields from the first entity
            sample_entity = entities[0]
            entity_dict = self.serializer._entity_to_dict(sample_entity)
            include_fields = list(entity_dict.keys())
        
        writer = csv.DictWriter(output, fieldnames=include_fields)
        writer.writeheader()
        
        for entity in entities:
            entity_dict = self.serializer._entity_to_dict(entity)
            # Flatten complex fields for CSV
            flattened_dict = self._flatten_for_csv(entity_dict, include_fields)
            writer.writerow(flattened_dict)
        
        return output.getvalue()
    
    def _flatten_for_csv(self, data: Dict[str, Any], include_fields: List[str]) -> Dict[str, str]:
        """Flatten complex data types for CSV export."""
        flattened = {}
        
        for field in include_fields:
            value = data.get(field)
            
            if value is None:
                flattened[field] = ""
            elif isinstance(value, (list, set)):
                # Join lists/sets with semicolons
                flattened[field] = "; ".join(str(v) for v in value)
            elif isinstance(value, dict):
                # Convert dict to JSON string
                flattened[field] = json.dumps(value)
            elif isinstance(value, (datetime, date)):
                # Format dates as ISO strings
                flattened[field] = DateTimeUtils.to_iso_string(value) if isinstance(value, datetime) else value.isoformat()
            elif isinstance(value, UUID):
                flattened[field] = str(value)
            else:
                flattened[field] = str(value)
        
        return flattened


class DataImporter:
    """Import entities from various formats."""
    
    def __init__(self, serializer: Optional[EntitySerializer] = None):
        self.serializer = serializer or EntitySerializer()
    
    def import_from_json(self, json_data: str, entity_class: Type[EntityType]) -> List[EntityType]:
        """Import entities from JSON format."""
        try:
            data = self.serializer.deserialize(json_data)
            
            # Handle both direct entity arrays and wrapped format
            if isinstance(data, dict) and "entities" in data:
                entities_data = data["entities"]
            elif isinstance(data, list):
                entities_data = data
            else:
                raise ValueError("JSON must contain either an array of entities or an object with 'entities' field")
            
            return [self.serializer._dict_to_entity(entity_data, entity_class) for entity_data in entities_data]
            
        except Exception as e:
            raise ValueError(f"Failed to import from JSON: {str(e)}")
    
    def import_from_csv(self, csv_data: str, entity_class: Type[EntityType],
                       field_mapping: Optional[Dict[str, str]] = None) -> List[EntityType]:
        """Import entities from CSV format."""
        import csv
        import io
        
        try:
            csv_file = io.StringIO(csv_data)
            reader = csv.DictReader(csv_file)
            
            entities = []
            for row in reader:
                # Apply field mapping if provided
                if field_mapping:
                    mapped_row = {}
                    for csv_field, entity_field in field_mapping.items():
                        if csv_field in row:
                            mapped_row[entity_field] = row[csv_field]
                    row_data = mapped_row
                else:
                    row_data = dict(row)
                
                # Process the row data
                processed_data = self._process_csv_row(row_data)
                entity = self.serializer._dict_to_entity(processed_data, entity_class)
                entities.append(entity)
            
            return entities
            
        except Exception as e:
            raise ValueError(f"Failed to import from CSV: {str(e)}")
    
    def _process_csv_row(self, row_data: Dict[str, str]) -> Dict[str, Any]:
        """Process CSV row data to convert string values to appropriate types."""
        processed = {}
        
        for field, value in row_data.items():
            if not value or value.strip() == "":
                processed[field] = None
                continue
            
            # Try to convert based on field name patterns
            if field == 'id' or field.endswith('_id'):
                # UUID field
                try:
                    processed[field] = UUIDUtils.from_string(value.strip())
                except ValueError:
                    processed[field] = value.strip()
            elif field.endswith('_ids'):
                # UUID list/set field
                try:
                    uuid_strings = [s.strip() for s in value.split(';') if s.strip()]
                    processed[field] = {UUIDUtils.from_string(s) for s in uuid_strings}
                except ValueError:
                    processed[field] = set(value.split(';'))
            elif field.endswith('_at') or field.endswith('_date'):
                # DateTime field
                try:
                    processed[field] = DateTimeUtils.from_iso_string(value.strip())
                except ValueError:
                    processed[field] = value.strip()
            elif field in ['tags', 'notes'] or field.endswith('_list'):
                # List/set field
                processed[field] = [s.strip() for s in value.split(';') if s.strip()]
            elif value.strip().lower() in ['true', 'false']:
                # Boolean field
                processed[field] = value.strip().lower() == 'true'
            elif value.strip().replace('.', '').replace('-', '').isdigit():
                # Numeric field
                try:
                    if '.' in value:
                        processed[field] = float(value)
                    else:
                        processed[field] = int(value)
                except ValueError:
                    processed[field] = value.strip()
            else:
                # String field
                processed[field] = value.strip()
        
        return processed