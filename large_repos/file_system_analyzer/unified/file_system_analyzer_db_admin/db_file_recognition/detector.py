"""Database file detection and categorization."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Iterator, Union
from datetime import datetime
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
from collections import Counter

from ..utils.types import DatabaseEngine, FileCategory, DatabaseFile, ScanStatus, AnalysisResult
from common.core.filesystem import FileSystemScanner, get_file_metadata
from common.core.patterns import PatternEngine, PatternType, PatternLibrary, FilePattern, PatternCategory


logger = logging.getLogger(__name__)


class DatabaseFileAnalysisResult(AnalysisResult):
    """Results from database file analysis."""

    total_files_scanned: int
    total_size_bytes: int
    files_by_engine: Dict[DatabaseEngine, int]
    size_by_engine: Dict[DatabaseEngine, int]
    files_by_category: Dict[FileCategory, int]
    size_by_category: Dict[FileCategory, int]
    detected_files: List[DatabaseFile]


class DatabaseFileDetector:
    """
    Detects and categorizes database files across multiple database engines.
    
    This class identifies files associated with various database engines
    (MySQL, PostgreSQL, MongoDB, Oracle, SQL Server) and categorizes them
    by their function (data, index, log, etc.).
    """

    def __init__(
        self,
        ignore_extensions: Optional[Set[str]] = None,
        content_sampling_size: int = 8192,
        max_workers: int = 10,
    ):
        """
        Initialize the database file detector.

        Args:
            ignore_extensions: Set of file extensions to ignore
            content_sampling_size: Number of bytes to read for content-based detection
            max_workers: Maximum number of worker threads for parallel processing
        """
        self.ignore_extensions = ignore_extensions or {
            '.exe', '.dll', '.so', '.pyc', '.pyo', '.class', '.jar',
            '.zip', '.tar', '.gz', '.7z', '.rar', '.bz2',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
            '.mp3', '.mp4', '.avi', '.mov', '.pdf', '.doc', '.docx',
            '.xls', '.xlsx', '.ppt', '.pptx',
        }
        self.content_sampling_size = content_sampling_size
        self.max_workers = max_workers
        
        # Initialize pattern engine with database file patterns
        self.pattern_engine = PatternEngine()
        self.file_scanner = FileSystemScanner()
        db_patterns = PatternLibrary.get_database_file_patterns()
        self.pattern_engine.register_patterns(db_patterns)

    def detect_engine_from_path(self, file_path: Path) -> Optional[DatabaseEngine]:
        """
        Detect database engine based on file path pattern.

        Args:
            file_path: Path to the file

        Returns:
            Detected database engine, or None if not detected
        """
        path_str = str(file_path)
        
        # Use pattern engine to detect file patterns
        matches = self.pattern_engine.scan_file_path(path_str)
        
        if matches:
            # Get the first match with engine metadata
            for match in matches:
                engine_name = match.metadata.get("engine")
                if engine_name:
                    try:
                        return DatabaseEngine(engine_name.lower())
                    except ValueError:
                        continue
                        
        return None

    def detect_category_from_path(
        self, file_path: Path, engine: Optional[DatabaseEngine] = None
    ) -> FileCategory:
        """
        Detect file category based on file path pattern.

        Args:
            file_path: Path to the file
            engine: Database engine to limit the search (optional)

        Returns:
            Detected file category, or FileCategory.UNKNOWN if not detected
        """
        path_str = str(file_path)

        # Special case for PostgreSQL WAL files for test compatibility
        if "pg_wal" in path_str or "pg_xlog" in path_str:
            return FileCategory.LOG

        # Special case for MongoDB index files
        if "index-" in path_str and engine == DatabaseEngine.MONGODB:
            return FileCategory.INDEX

        # Use pattern engine to detect file patterns
        engine_filter = engine.value.lower() if engine and engine != DatabaseEngine.UNKNOWN else None
        matches = self.pattern_engine.scan_file_path(path_str, engine=engine_filter)
        
        if matches:
            # Get the first match and extract category
            for match in matches:
                category_name = match.metadata.get("category")
                if category_name:
                    try:
                        # Map PatternCategory to FileCategory
                        if category_name == "data":
                            return FileCategory.DATA
                        elif category_name == "index":
                            return FileCategory.INDEX
                        elif category_name == "log":
                            return FileCategory.LOG
                        elif category_name == "temp":
                            return FileCategory.TEMP
                        elif category_name == "config":
                            return FileCategory.CONFIG
                        elif category_name == "backup":
                            return FileCategory.BACKUP
                    except ValueError:
                        continue

        return FileCategory.UNKNOWN

    def sample_file_content(self, file_path: Path) -> Optional[bytes]:
        """
        Read a sample of file content for content-based detection.

        Args:
            file_path: Path to the file

        Returns:
            Sample of file content, or None if file can't be read
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read(self.content_sampling_size)
        except (PermissionError, OSError, IOError) as e:
            logger.debug(f"Cannot read content from {file_path}: {e}")
            return None

    def detect_engine_from_content(self, content: bytes) -> Optional[DatabaseEngine]:
        """
        Detect database engine based on file content.

        Args:
            content: File content sample

        Returns:
            Detected database engine, or None if not detected
        """
        # MySQL signature detection
        if b"MySQL" in content or b"InnoDB" in content:
            return DatabaseEngine.MYSQL
            
        # PostgreSQL signature detection
        if b"PostgreSQL" in content or b"PGDMP" in content:
            return DatabaseEngine.POSTGRESQL
            
        # MongoDB signature detection
        if b"MongoDB" in content or b"WiredTiger" in content:
            return DatabaseEngine.MONGODB
            
        # Oracle signature detection
        if b"Oracle" in content or b"ORACLE" in content:
            return DatabaseEngine.ORACLE
            
        # SQL Server signature detection
        if b"Microsoft SQL Server" in content or b"MSSQL" in content:
            return DatabaseEngine.MSSQL
            
        return None

    def analyze_file(self, file_path: Path) -> Optional[DatabaseFile]:
        """
        Analyze a single file to determine if it's a database file.

        Args:
            file_path: Path to the file

        Returns:
            DatabaseFile object if it's a database file, None otherwise
        """
        try:
            # Skip files with ignored extensions
            if file_path.suffix.lower() in self.ignore_extensions:
                return None
                
            # Get file stats using common library
            stats = get_file_metadata(str(file_path))
            
            # Skip directories and non-existent files  
            if not file_path.is_file():
                return None
                
            # Try to detect database engine from path
            engine = self.detect_engine_from_path(file_path)
            
            # If we couldn't detect from path and file is not too large, sample content
            if (not engine or engine == DatabaseEngine.UNKNOWN) and stats.get("file_size", 0) < 10_000_000:
                content = self.sample_file_content(file_path)
                if content:
                    content_engine = self.detect_engine_from_content(content)
                    if content_engine:
                        engine = content_engine
            
            # If still no engine detected, skip this file
            if not engine:
                return None
                
            # Detect file category
            category = self.detect_category_from_path(file_path, engine)
            
            # Create database file object
            return DatabaseFile(
                path=str(file_path),
                engine=engine,
                category=category,
                size_bytes=stats.get("file_size", 0),
                last_modified=stats.get("last_modified", datetime.now()),
                creation_time=stats.get("creation_time"),
                last_accessed=stats.get("last_accessed"),
                is_compressed=file_path.suffix.lower() in {'.gz', '.zip', '.bz2', '.xz', '.7z', '.rar'},
            )
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return None

    def scan_directory(
        self,
        root_path: Union[str, Path],
        recursive: bool = True,
        follow_symlinks: bool = False,
        max_depth: Optional[int] = None,
        max_files: Optional[int] = None,
    ) -> DatabaseFileAnalysisResult:
        """
        Scan a directory for database files.

        Args:
            root_path: Starting directory for search
            recursive: Whether to search recursively
            follow_symlinks: Whether to follow symbolic links
            max_depth: Maximum directory depth to search
            max_files: Maximum number of files to process

        Returns:
            Analysis result containing detected database files and statistics
        """
        start_time = datetime.now()
        root = Path(root_path)
        
        if not root.exists() or not root.is_dir():
            return DatabaseFileAnalysisResult(
                analysis_duration_seconds=0,
                scan_status=ScanStatus.FAILED,
                error_message=f"Root path {root_path} does not exist or is not a directory",
                total_files_scanned=0,
                total_size_bytes=0,
                files_by_engine={},
                size_by_engine={},
                files_by_category={},
                size_by_category={},
                detected_files=[],
            )
        
        try:
            # Find all files using common filesystem scanner
            scan_options = {
                "recursive": recursive,
                "follow_symlinks": follow_symlinks,
                "max_depth": max_depth,
                "max_files": max_files
            }
            
            all_files = list(self.file_scanner.find_files(
                root_path=str(root),
                **scan_options
            ))
            
            total_files = len(all_files)
            logger.info(f"Found {total_files} files to analyze in {root_path}")
            
            # Process files in parallel
            detected_files = []
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_file = {executor.submit(self.analyze_file, Path(f)): f for f in all_files}
                for future in as_completed(future_to_file):
                    result = future.result()
                    if result:
                        detected_files.append(result)
            
            # Compute statistics
            total_size = sum(f.size_bytes for f in detected_files)
            
            files_by_engine = Counter()
            size_by_engine = Counter()
            files_by_category = Counter()
            size_by_category = Counter()
            
            for file in detected_files:
                files_by_engine[file.engine] += 1
                size_by_engine[file.engine] += file.size_bytes
                files_by_category[file.category] += 1
                size_by_category[file.category] += file.size_bytes
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            return DatabaseFileAnalysisResult(
                analysis_duration_seconds=duration,
                scan_status=ScanStatus.COMPLETED,
                total_files_scanned=total_files,
                total_size_bytes=total_size,
                files_by_engine=dict(files_by_engine),
                size_by_engine=dict(size_by_engine),
                files_by_category=dict(files_by_category),
                size_by_category=dict(size_by_category),
                detected_files=detected_files,
            )
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.error(f"Error scanning directory {root_path}: {e}")
            return DatabaseFileAnalysisResult(
                analysis_duration_seconds=duration,
                scan_status=ScanStatus.FAILED,
                error_message=str(e),
                total_files_scanned=0,
                total_size_bytes=0,
                files_by_engine={},
                size_by_engine={},
                files_by_category={},
                size_by_category={},
                detected_files=[],
            )