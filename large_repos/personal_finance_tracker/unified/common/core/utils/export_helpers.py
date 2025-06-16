import csv
import json
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union
from io import StringIO
from dataclasses import asdict, is_dataclass


class ExportHelpers:
    """Data export utilities for generating reports and files."""
    
    @staticmethod
    def to_json(data: Any, indent: int = 2, sort_keys: bool = True) -> str:
        """Convert data to JSON string with proper serialization."""
        return json.dumps(
            data, 
            indent=indent, 
            sort_keys=sort_keys, 
            default=ExportHelpers._json_serializer,
            ensure_ascii=False
        )
    
    @staticmethod
    def to_csv(data: List[Dict[str, Any]], include_headers: bool = True) -> str:
        """Convert list of dictionaries to CSV string."""
        if not data:
            return ""
        
        output = StringIO()
        
        # Get all unique keys from all dictionaries
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        
        fieldnames = sorted(list(all_keys))
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        if include_headers:
            writer.writeheader()
        
        for row in data:
            # Convert values to strings, handling special types
            serialized_row = {}
            for key in fieldnames:
                value = row.get(key, '')
                serialized_row[key] = ExportHelpers._csv_serialize_value(value)
            
            writer.writerow(serialized_row)
        
        return output.getvalue()
    
    @staticmethod
    def to_tsv(data: List[Dict[str, Any]], include_headers: bool = True) -> str:
        """Convert list of dictionaries to TSV (Tab-Separated Values) string."""
        if not data:
            return ""
        
        lines = []
        
        # Get all unique keys from all dictionaries
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        
        fieldnames = sorted(list(all_keys))
        
        if include_headers:
            lines.append('\t'.join(fieldnames))
        
        for row in data:
            values = []
            for key in fieldnames:
                value = row.get(key, '')
                serialized_value = ExportHelpers._csv_serialize_value(value)
                # Escape tabs in values
                serialized_value = str(serialized_value).replace('\t', '    ')
                values.append(serialized_value)
            lines.append('\t'.join(values))
        
        return '\n'.join(lines)
    
    @staticmethod
    def to_html_table(data: List[Dict[str, Any]], 
                     table_class: str = "financial-table",
                     include_headers: bool = True) -> str:
        """Convert list of dictionaries to HTML table."""
        if not data:
            return f'<table class="{table_class}"></table>'
        
        # Get all unique keys from all dictionaries
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        
        fieldnames = sorted(list(all_keys))
        
        html_parts = [f'<table class="{table_class}">']
        
        if include_headers:
            html_parts.append('  <thead>')
            html_parts.append('    <tr>')
            for field in fieldnames:
                escaped_field = ExportHelpers._html_escape(field)
                html_parts.append(f'      <th>{escaped_field}</th>')
            html_parts.append('    </tr>')
            html_parts.append('  </thead>')
        
        html_parts.append('  <tbody>')
        for row in data:
            html_parts.append('    <tr>')
            for field in fieldnames:
                value = row.get(field, '')
                escaped_value = ExportHelpers._html_escape(str(ExportHelpers._csv_serialize_value(value)))
                html_parts.append(f'      <td>{escaped_value}</td>')
            html_parts.append('    </tr>')
        html_parts.append('  </tbody>')
        html_parts.append('</table>')
        
        return '\n'.join(html_parts)
    
    @staticmethod
    def flatten_nested_dict(nested_dict: Dict[str, Any], 
                           separator: str = ".", 
                           prefix: str = "") -> Dict[str, Any]:
        """Flatten nested dictionary structure."""
        flattened = {}
        
        for key, value in nested_dict.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            
            if isinstance(value, dict):
                flattened.update(ExportHelpers.flatten_nested_dict(value, separator, new_key))
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # Handle list of dictionaries
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        list_prefix = f"{new_key}[{i}]"
                        flattened.update(ExportHelpers.flatten_nested_dict(item, separator, list_prefix))
                    else:
                        flattened[f"{new_key}[{i}]"] = item
            else:
                flattened[new_key] = value
        
        return flattened
    
    @staticmethod
    def create_summary_export(data: Dict[str, Any], 
                             title: str = "Financial Summary", 
                             format_type: str = "json") -> str:
        """Create a standardized summary export."""
        export_data = {
            'title': title,
            'generated_at': datetime.now().isoformat(),
            'summary': data.get('summary', {}),
            'details': data.get('details', {}),
            'metadata': data.get('metadata', {})
        }
        
        if format_type.lower() == 'json':
            return ExportHelpers.to_json(export_data)
        elif format_type.lower() == 'csv':
            # Flatten the data for CSV export
            flattened = ExportHelpers.flatten_nested_dict(export_data)
            return ExportHelpers.to_csv([flattened])
        else:
            return str(export_data)
    
    @staticmethod
    def export_transaction_list(transactions: List[Any], 
                               format_type: str = "csv") -> str:
        """Export list of transaction objects."""
        transaction_dicts = []
        
        for transaction in transactions:
            if is_dataclass(transaction):
                transaction_dict = asdict(transaction)
            elif hasattr(transaction, '__dict__'):
                transaction_dict = vars(transaction)
            else:
                transaction_dict = {'transaction': str(transaction)}
            
            # Ensure all values are serializable
            transaction_dict = ExportHelpers._make_serializable(transaction_dict)
            transaction_dicts.append(transaction_dict)
        
        if format_type.lower() == 'csv':
            return ExportHelpers.to_csv(transaction_dicts)
        elif format_type.lower() == 'tsv':
            return ExportHelpers.to_tsv(transaction_dicts)
        elif format_type.lower() == 'json':
            return ExportHelpers.to_json(transaction_dicts)
        elif format_type.lower() == 'html':
            return ExportHelpers.to_html_table(transaction_dicts)
        else:
            return str(transaction_dicts)
    
    @staticmethod
    def create_report_header(title: str, period: str = "", 
                           generated_by: str = "Financial Analysis System") -> Dict[str, str]:
        """Create standardized report header."""
        return {
            'title': title,
            'period': period,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'generated_by': generated_by
        }
    
    @staticmethod
    def format_currency_for_export(amount: Union[Decimal, float], 
                                  currency_symbol: str = "$",
                                  precision: int = 2) -> str:
        """Format currency amount for export."""
        if isinstance(amount, Decimal):
            formatted_amount = f"{amount:.{precision}f}"
        else:
            formatted_amount = f"{float(amount):.{precision}f}"
        
        return f"{currency_symbol}{formatted_amount}"
    
    @staticmethod
    def format_percentage_for_export(value: Union[Decimal, float], 
                                   precision: int = 2) -> str:
        """Format percentage for export."""
        if isinstance(value, Decimal):
            formatted_value = f"{value:.{precision}f}"
        else:
            formatted_value = f"{float(value):.{precision}f}"
        
        return f"{formatted_value}%"
    
    @staticmethod
    def _json_serializer(obj: Any) -> Any:
        """Custom JSON serializer for special types."""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'isoformat'):  # date objects
            return obj.isoformat()
        elif is_dataclass(obj):
            return asdict(obj)
        elif hasattr(obj, '__dict__'):
            return vars(obj)
        else:
            return str(obj)
    
    @staticmethod
    def _csv_serialize_value(value: Any) -> str:
        """Serialize value for CSV output."""
        if value is None:
            return ""
        elif isinstance(value, (list, dict)):
            return json.dumps(value, default=ExportHelpers._json_serializer)
        elif isinstance(value, Decimal):
            return str(value)
        elif isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif hasattr(value, 'isoformat'):  # date objects
            return value.isoformat()
        else:
            return str(value)
    
    @staticmethod
    def _html_escape(text: str) -> str:
        """Escape HTML special characters."""
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
    
    @staticmethod
    def _make_serializable(obj: Any) -> Any:
        """Recursively make object serializable."""
        if isinstance(obj, dict):
            return {k: ExportHelpers._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [ExportHelpers._make_serializable(item) for item in obj]
        elif isinstance(obj, (Decimal, datetime)) or hasattr(obj, 'isoformat'):
            return ExportHelpers._json_serializer(obj)
        elif is_dataclass(obj):
            return ExportHelpers._make_serializable(asdict(obj))
        elif hasattr(obj, '__dict__'):
            return ExportHelpers._make_serializable(vars(obj))
        else:
            return obj