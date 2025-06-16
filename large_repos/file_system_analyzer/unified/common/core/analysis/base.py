"""
Base analysis classes and interfaces.

This module provides the foundational classes for all analysis operations
used by both the Security Auditor and Database Administrator implementations.
"""

import time
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, Type
from uuid import uuid4

from ..types.models import AnalysisResult, RecommendationModel, ConfigurationModel
from ..types.enums import AnalysisStatus, Priority
from .caching import CacheManager

logger = logging.getLogger(__name__)


class BaseAnalyzer(ABC):
    """Base class for all analysis operations."""
    
    def __init__(self, config: Optional[ConfigurationModel] = None):
        """
        Initialize analyzer with configuration.
        
        Args:
            config: Configuration options for the analyzer
        """
        self.config = config or ConfigurationModel()
        self.cache_manager = CacheManager() if self.config.enable_caching else None
        self.analysis_id = str(uuid4())
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None
        
    @abstractmethod
    def analyze(self, input_data: Any) -> AnalysisResult:
        """
        Execute analysis operation.
        
        Args:
            input_data: Data to analyze
            
        Returns:
            Analysis result
        """
        pass
    
    @abstractmethod
    def generate_recommendations(self, analysis_result: AnalysisResult) -> List[RecommendationModel]:
        """
        Generate actionable recommendations based on analysis results.
        
        Args:
            analysis_result: Result from analysis operation
            
        Returns:
            List of recommendations
        """
        pass
    
    def start_analysis(self) -> None:
        """Mark the start of analysis."""
        self._start_time = datetime.now()
        logger.info(f"Starting analysis {self.analysis_id}")
    
    def end_analysis(self) -> None:
        """Mark the end of analysis."""
        self._end_time = datetime.now()
        logger.info(f"Completed analysis {self.analysis_id}")
    
    def create_result(self, 
                     status: AnalysisStatus, 
                     metadata: Optional[Dict[str, Any]] = None,
                     error_message: Optional[str] = None) -> AnalysisResult:
        """
        Create an analysis result object.
        
        Args:
            status: Analysis status
            metadata: Additional metadata
            error_message: Error message if analysis failed
            
        Returns:
            Analysis result object
        """
        duration = None
        if self._start_time and self._end_time:
            duration = (self._end_time - self._start_time).total_seconds()
        
        return AnalysisResult(
            analysis_id=self.analysis_id,
            status=status,
            start_time=self._start_time or datetime.now(),
            end_time=self._end_time,
            duration=duration,
            metadata=metadata or {},
            error_message=error_message
        )
    
    def get_cached_result(self, cache_key: str) -> Optional[Any]:
        """
        Get cached result if caching is enabled.
        
        Args:
            cache_key: Cache key to lookup
            
        Returns:
            Cached result or None
        """
        if self.cache_manager:
            return self.cache_manager.get(cache_key)
        return None
    
    def cache_result(self, cache_key: str, result: Any, ttl: Optional[int] = None) -> None:
        """
        Cache result if caching is enabled.
        
        Args:
            cache_key: Cache key to store under
            result: Result to cache
            ttl: Time to live in seconds (uses config default if not provided)
        """
        if self.cache_manager:
            ttl = ttl or self.config.cache_ttl_seconds
            self.cache_manager.set(cache_key, result, ttl)
    
    def run_analysis(self, input_data: Any) -> AnalysisResult:
        """
        Run complete analysis with error handling and timing.
        
        Args:
            input_data: Data to analyze
            
        Returns:
            Analysis result
        """
        try:
            self.start_analysis()
            result = self.analyze(input_data)
            self.end_analysis()
            
            # Update result with timing information
            if self._start_time and self._end_time:
                result.duration = (self._end_time - self._start_time).total_seconds()
                result.end_time = self._end_time
            
            return result
            
        except Exception as e:
            self.end_analysis()
            logger.error(f"Analysis {self.analysis_id} failed: {e}")
            
            return self.create_result(
                status=AnalysisStatus.FAILED,
                error_message=str(e),
                metadata={"exception_type": type(e).__name__}
            )


class FileAnalyzer(BaseAnalyzer):
    """Base class for file-based analysis operations."""
    
    def should_skip_file(self, file_path: str) -> bool:
        """
        Check if a file should be skipped based on configuration.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file should be skipped
        """
        from pathlib import Path
        
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return True
        
        # Check hidden files
        if self.config.skip_hidden and path.name.startswith('.'):
            return True
        
        # Check file size
        try:
            if path.is_file() and path.stat().st_size > self.config.max_file_size:
                return True
        except (PermissionError, OSError):
            return True
        
        # Check extensions
        if self.config.exclude_extensions and path.suffix.lower() in self.config.exclude_extensions:
            return True
        
        if self.config.include_extensions and path.suffix.lower() not in self.config.include_extensions:
            return True
        
        # Check patterns
        file_path_str = str(path)
        for pattern in self.config.exclude_patterns:
            if pattern in file_path_str:
                return True
        
        if self.config.include_patterns:
            match_found = False
            for pattern in self.config.include_patterns:
                if pattern in file_path_str:
                    match_found = True
                    break
            if not match_found:
                return True
        
        return False


class BatchAnalyzer(BaseAnalyzer):
    """Base class for batch analysis operations."""
    
    def __init__(self, config: Optional[ConfigurationModel] = None):
        """Initialize batch analyzer."""
        super().__init__(config)
        self.batch_results: List[AnalysisResult] = []
    
    def analyze_batch(self, items: List[Any]) -> List[AnalysisResult]:
        """
        Analyze a batch of items.
        
        Args:
            items: List of items to analyze
            
        Returns:
            List of analysis results
        """
        results = []
        
        for item in items:
            try:
                result = self.analyze(item)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze item {item}: {e}")
                error_result = self.create_result(
                    status=AnalysisStatus.FAILED,
                    error_message=str(e),
                    metadata={"item": str(item)}
                )
                results.append(error_result)
        
        self.batch_results = results
        return results
    
    def get_batch_summary(self) -> Dict[str, Any]:
        """
        Get summary of batch analysis results.
        
        Returns:
            Summary statistics
        """
        if not self.batch_results:
            return {}
        
        total = len(self.batch_results)
        successful = sum(1 for r in self.batch_results if r.is_successful)
        failed = sum(1 for r in self.batch_results if r.status == AnalysisStatus.FAILED)
        
        return {
            "total_items": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "total_duration": sum(r.duration or 0 for r in self.batch_results),
            "average_duration": sum(r.duration or 0 for r in self.batch_results) / total if total > 0 else 0
        }


class AnalyzerRegistry:
    """Registry for managing analyzer implementations."""
    
    _analyzers: Dict[str, Type[BaseAnalyzer]] = {}
    
    @classmethod
    def register(cls, name: str, analyzer_class: Type[BaseAnalyzer]) -> None:
        """
        Register an analyzer implementation.
        
        Args:
            name: Name of the analyzer
            analyzer_class: Analyzer class to register
        """
        cls._analyzers[name] = analyzer_class
    
    @classmethod
    def get_analyzer(cls, name: str) -> Optional[Type[BaseAnalyzer]]:
        """
        Get analyzer class by name.
        
        Args:
            name: Name of the analyzer
            
        Returns:
            Analyzer class or None if not found
        """
        return cls._analyzers.get(name)
    
    @classmethod
    def list_analyzers(cls) -> List[str]:
        """
        Get list of registered analyzer names.
        
        Returns:
            List of analyzer names
        """
        return list(cls._analyzers.keys())
    
    @classmethod
    def create_analyzer(cls, name: str, config: Optional[ConfigurationModel] = None) -> Optional[BaseAnalyzer]:
        """
        Create an analyzer instance by name.
        
        Args:
            name: Name of the analyzer
            config: Configuration for the analyzer
            
        Returns:
            Analyzer instance or None if not found
        """
        analyzer_class = cls.get_analyzer(name)
        if analyzer_class:
            return analyzer_class(config)
        return None