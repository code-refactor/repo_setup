import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from pydantic import BaseModel

from .models import FileInfo
from .buffer import TextBuffer


class FileManager(BaseModel):
    """Manages file operations for the text editor."""
    
    current_file: FileInfo = FileInfo()
    auto_backup: bool = True
    backup_directory: str = ".backups"
    
    def load_file(self, path: str, buffer: TextBuffer) -> bool:
        """Load a file into the buffer."""
        try:
            file_path = Path(path)
            if not file_path.exists():
                return False
            
            # Try UTF-8 first, then fallback to latin-1
            content, encoding = self._read_file_with_encoding(file_path)
            
            # Update buffer
            buffer.set_content(content)
            buffer.modified = False
            
            # Update file info
            stat = file_path.stat()
            self.current_file = FileInfo(
                path=str(file_path.absolute()),
                encoding=encoding,
                modified=False,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                size=stat.st_size
            )
            
            return True
            
        except Exception:
            return False
    
    def save_file(self, buffer: TextBuffer, path: Optional[str] = None) -> bool:
        """Save the buffer content to a file."""
        target_path = path or self.current_file.path
        if not target_path:
            return False
        
        try:
            file_path = Path(target_path)
            
            # Create backup if enabled
            if self.auto_backup and file_path.exists():
                self._create_backup(file_path)
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            content = buffer.get_content()
            with open(file_path, 'w', encoding=self.current_file.encoding) as f:
                f.write(content)
            
            # Update file info
            stat = file_path.stat()
            self.current_file.path = str(file_path.absolute())
            self.current_file.modified = False
            self.current_file.last_modified = datetime.fromtimestamp(stat.st_mtime)
            self.current_file.size = stat.st_size
            
            # Mark buffer as not modified
            buffer.modified = False
            
            return True
            
        except Exception:
            return False
    
    def save_as_file(self, buffer: TextBuffer, path: str) -> bool:
        """Save the buffer content to a new file."""
        old_path = self.current_file.path
        success = self.save_file(buffer, path)
        
        if success:
            # Update current file path
            self.current_file.path = path
        else:
            # Restore old path on failure
            self.current_file.path = old_path
        
        return success
    
    def new_file(self, buffer: TextBuffer) -> None:
        """Create a new file (clear buffer and file info)."""
        buffer.clear()
        buffer.modified = False
        
        self.current_file = FileInfo()
    
    def is_file_modified_externally(self) -> bool:
        """Check if the current file has been modified externally."""
        if not self.current_file.path:
            return False
        
        try:
            file_path = Path(self.current_file.path)
            if not file_path.exists():
                return True  # File was deleted
            
            stat = file_path.stat()
            current_mtime = datetime.fromtimestamp(stat.st_mtime)
            
            return (self.current_file.last_modified is not None and 
                   current_mtime > self.current_file.last_modified)
            
        except Exception:
            return False
    
    def reload_file(self, buffer: TextBuffer) -> bool:
        """Reload the current file from disk."""
        if not self.current_file.path:
            return False
        
        return self.load_file(self.current_file.path, buffer)
    
    def get_file_info(self) -> FileInfo:
        """Get information about the current file."""
        return self.current_file.model_copy()
    
    def has_file(self) -> bool:
        """Check if there's a current file."""
        return self.current_file.path is not None
    
    def get_file_name(self) -> str:
        """Get the name of the current file."""
        if not self.current_file.path:
            return "Untitled"
        return Path(self.current_file.path).name
    
    def get_file_directory(self) -> str:
        """Get the directory of the current file."""
        if not self.current_file.path:
            return ""
        return str(Path(self.current_file.path).parent)
    
    def _read_file_with_encoding(self, file_path: Path) -> Tuple[str, str]:
        """Read file with encoding detection."""
        encodings = ['utf-8', 'latin-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                return content, encoding
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, use utf-8 with error handling
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return content, 'utf-8'
    
    def _create_backup(self, file_path: Path) -> None:
        """Create a backup of the file."""
        try:
            backup_dir = Path(self.backup_directory)
            backup_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.name}.{timestamp}.bak"
            backup_path = backup_dir / backup_name
            
            # Copy file content
            content, _ = self._read_file_with_encoding(file_path)
            with open(backup_path, 'w', encoding=self.current_file.encoding) as f:
                f.write(content)
                
        except Exception:
            # Backup failed, but don't prevent saving
            pass
    
    def list_backups(self) -> list:
        """List available backup files for the current file."""
        if not self.current_file.path:
            return []
        
        try:
            backup_dir = Path(self.backup_directory)
            if not backup_dir.exists():
                return []
            
            file_name = Path(self.current_file.path).name
            pattern = f"{file_name}.*.bak"
            
            backups = []
            for backup_file in backup_dir.glob(pattern):
                stat = backup_file.stat()
                backups.append({
                    'path': str(backup_file),
                    'name': backup_file.name,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'size': stat.st_size
                })
            
            # Sort by modification time (newest first)
            backups.sort(key=lambda x: x['modified'], reverse=True)
            return backups
            
        except Exception:
            return []
    
    def restore_from_backup(self, backup_path: str, buffer: TextBuffer) -> bool:
        """Restore file content from a backup."""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                return False
            
            content, encoding = self._read_file_with_encoding(backup_file)
            buffer.set_content(content)
            buffer.modified = True  # Mark as modified since we're restoring from backup
            
            return True
            
        except Exception:
            return False