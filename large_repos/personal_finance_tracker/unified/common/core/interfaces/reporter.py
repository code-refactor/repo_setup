from abc import ABC, abstractmethod
from typing import Any, Dict, List, Protocol, runtime_checkable

from ..models.analysis_results import SummaryReport


@runtime_checkable
class Reporter(Protocol):
    """Standard interface for all reporters."""
    
    def generate_report(self, data: Any) -> SummaryReport:
        """Generate a report from data."""
        ...
    
    def export_report(self, report: SummaryReport, format_type: str) -> str:
        """Export report in specified format."""
        ...


class ReportGenerator(ABC):
    """Abstract base class for report generators."""
    
    @abstractmethod
    def generate_report(self, data: Any, report_type: str = "summary") -> SummaryReport:
        """Generate a report from analysis data."""
        pass
    
    @abstractmethod
    def export_report(self, report: SummaryReport, format_type: str = "json") -> str:
        """Export report in specified format (json, csv, html, etc.)."""
        pass
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats."""
        return ["json", "csv", "html", "txt"]
    
    def validate_format(self, format_type: str) -> bool:
        """Validate export format."""
        return format_type.lower() in self.get_supported_formats()
    
    def create_report_metadata(self, report_type: str, data_source: str = "") -> Dict[str, Any]:
        """Create standard report metadata."""
        from datetime import datetime
        
        return {
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'data_source': data_source,
            'generator': self.__class__.__name__
        }