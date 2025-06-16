import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


def serialize_model(model: BaseModel, format: str = "json") -> str:
    """Serialize a Pydantic model to string format."""
    if format.lower() == "json":
        return model.model_dump_json(indent=2)
    elif format.lower() == "dict":
        return str(model.model_dump())
    else:
        raise ValueError(f"Unsupported serialization format: {format}")


def deserialize_model(data: str, model_class: Type[T], format: str = "json") -> T:
    """Deserialize string data to a Pydantic model."""
    if format.lower() == "json":
        return model_class.model_validate_json(data)
    elif format.lower() == "dict":
        # Convert string representation of dict back to dict
        dict_data = eval(data)  # Note: eval is dangerous, use carefully
        return model_class.model_validate(dict_data)
    else:
        raise ValueError(f"Unsupported deserialization format: {format}")


def save_model_to_file(model: BaseModel, file_path: str, format: str = "json") -> bool:
    """Save a Pydantic model to a file."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == "json":
            with open(path, 'w', encoding='utf-8') as f:
                f.write(model.model_dump_json(indent=2))
        elif format.lower() == "pickle":
            with open(path, 'wb') as f:
                pickle.dump(model.model_dump(), f)
        else:
            raise ValueError(f"Unsupported file format: {format}")
        
        return True
        
    except Exception:
        return False


def load_model_from_file(file_path: str, model_class: Type[T], format: str = "json") -> Optional[T]:
    """Load a Pydantic model from a file."""
    try:
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        if format.lower() == "json":
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return model_class.model_validate(data)
        elif format.lower() == "pickle":
            with open(path, 'rb') as f:
                data = pickle.load(f)
            return model_class.model_validate(data)
        else:
            raise ValueError(f"Unsupported file format: {format}")
            
    except Exception:
        return None


def serialize_datetime(dt: datetime) -> str:
    """Serialize datetime to ISO format string."""
    return dt.isoformat()


def deserialize_datetime(dt_string: str) -> datetime:
    """Deserialize datetime from ISO format string."""
    return datetime.fromisoformat(dt_string)


def create_backup_filename(original_path: str, timestamp: Optional[datetime] = None) -> str:
    """Create a backup filename with timestamp."""
    path = Path(original_path)
    
    if timestamp is None:
        timestamp = datetime.now()
    
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    backup_name = f"{path.stem}_{timestamp_str}.bak"
    
    return str(path.parent / backup_name)


def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """Safely load JSON with fallback to default value."""
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(obj: Any, default: Any = None, indent: int = 2) -> str:
    """Safely dump object to JSON with fallback."""
    try:
        return json.dumps(obj, indent=indent, default=str)
    except (TypeError, ValueError):
        return json.dumps(default, indent=indent) if default is not None else "{}"


def compress_data(data: str) -> bytes:
    """Compress string data using gzip."""
    import gzip
    return gzip.compress(data.encode('utf-8'))


def decompress_data(compressed_data: bytes) -> str:
    """Decompress gzip data to string."""
    import gzip
    return gzip.decompress(compressed_data).decode('utf-8')


def serialize_with_compression(model: BaseModel) -> bytes:
    """Serialize model and compress the result."""
    json_data = model.model_dump_json()
    return compress_data(json_data)


def deserialize_with_decompression(compressed_data: bytes, model_class: Type[T]) -> T:
    """Decompress data and deserialize to model."""
    json_data = decompress_data(compressed_data)
    return model_class.model_validate_json(json_data)


def export_models_to_archive(models: Dict[str, BaseModel], archive_path: str) -> bool:
    """Export multiple models to a ZIP archive."""
    import zipfile
    
    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for name, model in models.items():
                json_data = model.model_dump_json(indent=2)
                zipf.writestr(f"{name}.json", json_data)
        
        return True
        
    except Exception:
        return False


def import_models_from_archive(archive_path: str, model_classes: Dict[str, Type[BaseModel]]) -> Dict[str, BaseModel]:
    """Import multiple models from a ZIP archive."""
    import zipfile
    
    models = {}
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            for name, model_class in model_classes.items():
                try:
                    json_data = zipf.read(f"{name}.json").decode('utf-8')
                    models[name] = model_class.model_validate_json(json_data)
                except (KeyError, json.JSONDecodeError):
                    # Skip missing or invalid files
                    continue
        
        return models
        
    except Exception:
        return {}


def create_model_snapshot(model: BaseModel, snapshot_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a snapshot of a model with metadata."""
    if snapshot_id is None:
        snapshot_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return {
        "snapshot_id": snapshot_id,
        "timestamp": datetime.now().isoformat(),
        "model_class": model.__class__.__name__,
        "data": model.model_dump(),
        "version": "1.0"
    }


def restore_from_snapshot(snapshot: Dict[str, Any], model_class: Type[T]) -> Optional[T]:
    """Restore a model from a snapshot."""
    try:
        # Validate snapshot format
        required_fields = ["snapshot_id", "timestamp", "model_class", "data"]
        if not all(field in snapshot for field in required_fields):
            return None
        
        # Check model class matches
        if snapshot["model_class"] != model_class.__name__:
            return None
        
        # Restore model
        return model_class.model_validate(snapshot["data"])
        
    except Exception:
        return None


def migrate_model_data(old_data: Dict[str, Any], migration_rules: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate model data using migration rules."""
    new_data = old_data.copy()
    
    for rule_type, rules in migration_rules.items():
        if rule_type == "rename_fields":
            for old_name, new_name in rules.items():
                if old_name in new_data:
                    new_data[new_name] = new_data.pop(old_name)
        
        elif rule_type == "remove_fields":
            for field_name in rules:
                new_data.pop(field_name, None)
        
        elif rule_type == "add_fields":
            for field_name, default_value in rules.items():
                if field_name not in new_data:
                    new_data[field_name] = default_value
        
        elif rule_type == "transform_fields":
            for field_name, transform_func in rules.items():
                if field_name in new_data:
                    try:
                        new_data[field_name] = transform_func(new_data[field_name])
                    except Exception:
                        # Keep original value if transformation fails
                        pass
    
    return new_data


def validate_serialized_data(data: str, expected_fields: list) -> bool:
    """Validate that serialized data contains expected fields."""
    try:
        parsed_data = json.loads(data)
        return all(field in parsed_data for field in expected_fields)
    except (json.JSONDecodeError, TypeError):
        return False


def clean_serialized_data(data: Dict[str, Any], remove_none: bool = True, 
                         remove_empty: bool = False) -> Dict[str, Any]:
    """Clean serialized data by removing unwanted values."""
    cleaned_data = {}
    
    for key, value in data.items():
        # Skip None values if requested
        if remove_none and value is None:
            continue
        
        # Skip empty collections if requested
        if remove_empty and (
            (isinstance(value, (list, dict, str)) and len(value) == 0)
        ):
            continue
        
        # Recursively clean nested dictionaries
        if isinstance(value, dict):
            cleaned_value = clean_serialized_data(value, remove_none, remove_empty)
            if cleaned_value or not remove_empty:
                cleaned_data[key] = cleaned_value
        else:
            cleaned_data[key] = value
    
    return cleaned_data


def get_model_schema_hash(model_class: Type[BaseModel]) -> str:
    """Get a hash of the model schema for version tracking."""
    import hashlib
    
    schema = model_class.model_json_schema()
    schema_str = json.dumps(schema, sort_keys=True)
    
    return hashlib.md5(schema_str.encode()).hexdigest()


def verify_model_compatibility(data: Dict[str, Any], model_class: Type[BaseModel]) -> bool:
    """Verify that data is compatible with model class."""
    try:
        model_class.model_validate(data)
        return True
    except Exception:
        return False