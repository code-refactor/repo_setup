import re
from typing import Optional, Tuple, List
from pathlib import Path

from ..core.models import Position


def validate_position(position: Position, max_line: int, max_column: int) -> Tuple[bool, Optional[str]]:
    """Validate a position against buffer bounds."""
    if position.line < 0:
        return False, "Line number cannot be negative"
    
    if position.column < 0:
        return False, "Column number cannot be negative"
    
    if position.line > max_line:
        return False, f"Line number {position.line} exceeds maximum {max_line}"
    
    if position.column > max_column:
        return False, f"Column number {position.column} exceeds maximum {max_column}"
    
    return True, None


def validate_text(text: str, max_length: Optional[int] = None, 
                 allowed_chars: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """Validate text content."""
    if max_length is not None and len(text) > max_length:
        return False, f"Text length {len(text)} exceeds maximum {max_length}"
    
    if allowed_chars is not None:
        invalid_chars = set(text) - set(allowed_chars)
        if invalid_chars:
            return False, f"Text contains invalid characters: {invalid_chars}"
    
    return True, None


def validate_file_path(path: str) -> Tuple[bool, Optional[str]]:
    """Validate a file path."""
    if not path:
        return False, "Path cannot be empty"
    
    try:
        file_path = Path(path)
        
        # Check for invalid characters in path
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
        if any(char in str(file_path) for char in invalid_chars):
            return False, f"Path contains invalid characters: {invalid_chars}"
        
        # Check if path is too long
        if len(str(file_path)) > 260:  # Windows MAX_PATH limitation
            return False, "Path is too long (exceeds 260 characters)"
        
        # Check if parent directory exists when creating new files
        if not file_path.exists() and file_path.parent.exists():
            # Check if we can write to the parent directory
            if not file_path.parent.is_dir():
                return False, "Parent path is not a directory"
        
        return True, None
        
    except Exception as e:
        return False, f"Invalid path: {str(e)}"


def validate_regex_pattern(pattern: str) -> Tuple[bool, Optional[str]]:
    """Validate a regular expression pattern."""
    if not pattern:
        return False, "Pattern cannot be empty"
    
    try:
        re.compile(pattern)
        return True, None
    except re.error as e:
        return False, f"Invalid regex pattern: {str(e)}"


def validate_encoding(encoding: str) -> Tuple[bool, Optional[str]]:
    """Validate a text encoding."""
    if not encoding:
        return False, "Encoding cannot be empty"
    
    try:
        # Test if the encoding is supported
        "test".encode(encoding)
        return True, None
    except (LookupError, ValueError) as e:
        return False, f"Unsupported encoding: {str(e)}"


def validate_line_ending(line_ending: str) -> Tuple[bool, Optional[str]]:
    """Validate line ending format."""
    valid_endings = ['\n', '\r\n', '\r']
    
    if line_ending not in valid_endings:
        return False, f"Invalid line ending. Must be one of: {valid_endings}"
    
    return True, None


def validate_search_options(pattern: str, regex: bool = False, 
                          case_sensitive: bool = False) -> Tuple[bool, Optional[str]]:
    """Validate search options and pattern."""
    if not pattern:
        return False, "Search pattern cannot be empty"
    
    if regex:
        return validate_regex_pattern(pattern)
    
    return True, None


def validate_word_count_target(target: int) -> Tuple[bool, Optional[str]]:
    """Validate a word count target."""
    if target < 0:
        return False, "Word count target cannot be negative"
    
    if target > 1000000:  # Arbitrary large limit
        return False, "Word count target is too large (maximum: 1,000,000)"
    
    return True, None


def validate_time_duration(seconds: float) -> Tuple[bool, Optional[str]]:
    """Validate a time duration in seconds."""
    if seconds < 0:
        return False, "Duration cannot be negative"
    
    if seconds > 86400 * 365:  # One year in seconds
        return False, "Duration is too long (maximum: 1 year)"
    
    return True, None


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing invalid characters."""
    # Remove or replace invalid characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
    sanitized = filename
    
    for char in invalid_chars:
        sanitized = sanitized.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    
    # Ensure filename is not empty
    if not sanitized:
        sanitized = "untitled"
    
    # Truncate if too long
    if len(sanitized) > 255:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        max_name_length = 255 - len(ext) - 1 if ext else 255
        sanitized = name[:max_name_length] + ('.' + ext if ext else '')
    
    return sanitized


def validate_json_content(content: str) -> Tuple[bool, Optional[str]]:
    """Validate JSON content."""
    if not content.strip():
        return False, "JSON content cannot be empty"
    
    try:
        import json
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """Validate a URL."""
    if not url:
        return False, "URL cannot be empty"
    
    # Basic URL pattern validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        return False, "Invalid URL format"
    
    return True, None


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate an email address."""
    if not email:
        return False, "Email cannot be empty"
    
    # Basic email pattern validation
    email_pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )
    
    if not email_pattern.match(email):
        return False, "Invalid email format"
    
    return True, None


def validate_color_hex(color: str) -> Tuple[bool, Optional[str]]:
    """Validate a hexadecimal color code."""
    if not color:
        return False, "Color code cannot be empty"
    
    # Remove leading # if present
    if color.startswith('#'):
        color = color[1:]
    
    # Check if it's a valid hex color (3 or 6 digits)
    if len(color) not in [3, 6]:
        return False, "Color code must be 3 or 6 hexadecimal digits"
    
    try:
        int(color, 16)
        return True, None
    except ValueError:
        return False, "Color code contains invalid hexadecimal digits"


def validate_percentage(value: float) -> Tuple[bool, Optional[str]]:
    """Validate a percentage value (0-100)."""
    if value < 0:
        return False, "Percentage cannot be negative"
    
    if value > 100:
        return False, "Percentage cannot exceed 100"
    
    return True, None


def validate_priority(priority: int) -> Tuple[bool, Optional[str]]:
    """Validate a priority value (typically 1-10)."""
    if priority < 1:
        return False, "Priority must be at least 1"
    
    if priority > 10:
        return False, "Priority cannot exceed 10"
    
    return True, None


def validate_batch_size(batch_size: int, max_size: int = 1000) -> Tuple[bool, Optional[str]]:
    """Validate a batch size for processing operations."""
    if batch_size <= 0:
        return False, "Batch size must be positive"
    
    if batch_size > max_size:
        return False, f"Batch size cannot exceed {max_size}"
    
    return True, None


def validate_timeout(timeout: float) -> Tuple[bool, Optional[str]]:
    """Validate a timeout value in seconds."""
    if timeout <= 0:
        return False, "Timeout must be positive"
    
    if timeout > 3600:  # 1 hour
        return False, "Timeout cannot exceed 1 hour"
    
    return True, None


def clean_text_input(text: str, preserve_newlines: bool = True) -> str:
    """Clean and normalize text input."""
    if not preserve_newlines:
        # Replace all whitespace with single spaces
        text = re.sub(r'\s+', ' ', text)
    else:
        # Normalize whitespace but preserve line breaks
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Clean each line individually
            cleaned_line = re.sub(r'[ \t]+', ' ', line.strip())
            cleaned_lines.append(cleaned_line)
        
        text = '\n'.join(cleaned_lines)
    
    # Remove control characters except newlines and tabs
    if preserve_newlines:
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    else:
        text = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', text)
    
    return text


def validate_and_clean_input(text: str, max_length: Optional[int] = None,
                           preserve_newlines: bool = True) -> Tuple[str, bool, Optional[str]]:
    """Validate and clean text input in one operation."""
    # First clean the text
    cleaned_text = clean_text_input(text, preserve_newlines)
    
    # Then validate
    is_valid, error_message = validate_text(cleaned_text, max_length)
    
    return cleaned_text, is_valid, error_message