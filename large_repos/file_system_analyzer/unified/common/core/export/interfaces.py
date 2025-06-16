"""
Data export interfaces for analysis results.

This module provides unified export functionality for all file system analyzer
implementations, supporting JSON, CSV, and HTML report generation.
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ExportInterface:
    """
    Interface for exporting analysis results in various formats.
    
    This class provides methods for exporting analysis results to
    different formats such as JSON, CSV, and HTML reports.
    """

    def __init__(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        timezone: Optional[str] = None,
    ):
        """
        Initialize the export interface.

        Args:
            output_dir: Directory for output files (defaults to current directory)
            timezone: Timezone for timestamps in exports
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.timezone = timezone
        
        # Create output directory if it doesn't exist
        if not self.output_dir.exists():
            os.makedirs(self.output_dir)
            
    def _ensure_serializable(self, data: Any) -> Any:
        """Ensure data is JSON serializable."""
        if isinstance(data, BaseModel):
            return json.loads(data.json())
        elif isinstance(data, datetime):
            return data.isoformat()
        elif isinstance(data, dict):
            return {k: self._ensure_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._ensure_serializable(item) for item in data]
        elif hasattr(data, "__dict__"):
            return self._ensure_serializable(data.__dict__)
        return data

    def export_json(
        self, 
        data: Any, 
        filename: str,
        pretty_print: bool = True,
    ) -> str:
        """
        Export data to a JSON file.

        Args:
            data: Data to export (can be dict, BaseModel, or other serializable object)
            filename: Output filename (will be placed in output_dir)
            pretty_print: Whether to format JSON for readability

        Returns:
            Path to the exported file
        """
        output_path = self.output_dir / filename
        
        # Ensure data is serializable
        serializable_data = self._ensure_serializable(data)
        
        try:
            with open(output_path, 'w') as f:
                if pretty_print:
                    json.dump(serializable_data, f, indent=2, default=str)
                else:
                    json.dump(serializable_data, f, default=str)
            
            logger.info(f"Exported JSON to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error exporting JSON to {output_path}: {e}")
            raise

    def export_csv(
        self, 
        data: List[Dict[str, Any]], 
        filename: str,
        headers: Optional[List[str]] = None,
    ) -> str:
        """
        Export data to a CSV file.

        Args:
            data: List of dictionaries to export as rows
            filename: Output filename (will be placed in output_dir)
            headers: Optional list of column headers (if None, use keys from first row)

        Returns:
            Path to the exported file
        """
        output_path = self.output_dir / filename
        
        if not data:
            logger.warning(f"No data to export to CSV {output_path}")
            return str(output_path)
            
        # Determine headers if not provided
        if headers is None:
            headers = list(data[0].keys())
            
        try:
            with open(output_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                
                for row in data:
                    # Convert any non-string values to strings
                    csv_row = {}
                    for key, value in row.items():
                        if key in headers:
                            if isinstance(value, (dict, list)):
                                csv_row[key] = json.dumps(value)
                            elif isinstance(value, datetime):
                                csv_row[key] = value.isoformat()
                            else:
                                csv_row[key] = str(value)
                    
                    writer.writerow(csv_row)
            
            logger.info(f"Exported CSV to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error exporting CSV to {output_path}: {e}")
            raise

    def export_html_report(
        self, 
        data: Any, 
        filename: str,
        template: Optional[str] = None,
        title: str = "File System Analysis Report",
    ) -> str:
        """
        Export data to an HTML report.

        Args:
            data: Data to include in the report
            filename: Output filename (will be placed in output_dir)
            template: Optional HTML template file path
            title: Report title

        Returns:
            Path to the exported file
        """
        output_path = self.output_dir / filename
        
        # Convert data to serializable form
        report_data = self._ensure_serializable(data)
        
        # Default HTML template
        default_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #3498db; margin-top: 30px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .summary {{ background-color: #eef7fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .recommendation {{ background-color: #f0fff0; padding: 10px; margin-bottom: 10px; border-left: 4px solid #2ecc71; }}
                .warning {{ background-color: #fff0f0; padding: 10px; margin-bottom: 10px; border-left: 4px solid #e74c3c; }}
                .critical {{ background-color: #ffe6e6; padding: 10px; margin-bottom: 10px; border-left: 4px solid #c0392b; }}
                .chart {{ width: 100%; height: 300px; margin-bottom: 20px; }}
                pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                .finding {{ margin-bottom: 15px; padding: 10px; border-radius: 5px; }}
                .finding-high {{ background-color: #fff3cd; border-left: 4px solid #ffc107; }}
                .finding-medium {{ background-color: #d4edda; border-left: 4px solid #28a745; }}
                .finding-low {{ background-color: #d1ecf1; border-left: 4px solid #17a2b8; }}
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <h1>{title}</h1>
            <div class="summary">
                <h2>Summary</h2>
                <pre>{summary}</pre>
            </div>
            <div id="content">
                <h2>Detailed Results</h2>
                <pre>{content}</pre>
            </div>
            <div id="recommendations">
                <h2>Recommendations</h2>
                {recommendations}
            </div>
            <footer>
                <p>Report generated on {timestamp}</p>
            </footer>
        </body>
        </html>
        """
        
        try:
            # Extract recommendations if available
            recommendations = []
            if isinstance(report_data, dict):
                if 'recommendations' in report_data:
                    recommendations = report_data['recommendations']
                elif 'findings' in report_data:
                    # Handle compliance findings
                    recommendations = report_data['findings']
            
            # Create a summary of the data
            summary = self._create_summary(report_data)
            
            # Format recommendations
            recommendations_html = ""
            for i, rec in enumerate(recommendations):
                if isinstance(rec, dict):
                    priority = rec.get('priority', rec.get('severity', '')).lower()
                    css_class = self._get_css_class_for_priority(priority)
                    
                    recommendations_html += f"<div class='{css_class}'>"
                    recommendations_html += f"<h3>{i+1}. {rec.get('title', rec.get('description', 'Finding'))}</h3>"
                    
                    if 'description' in rec and rec['description'] != rec.get('title', ''):
                        recommendations_html += f"<p>{rec.get('description', '')}</p>"
                    
                    recommendations_html += f"<p><strong>Priority/Severity:</strong> {priority}</p>"
                    
                    # Add space savings if available (DB admin)
                    if 'estimated_space_savings_bytes' in rec:
                        savings = self._format_bytes(rec['estimated_space_savings_bytes'])
                        recommendations_html += f"<p><strong>Estimated Space Savings:</strong> {savings}</p>"
                    
                    # Add compliance info if available (security auditor)
                    if 'compliance_framework' in rec:
                        recommendations_html += f"<p><strong>Framework:</strong> {rec['compliance_framework']}</p>"
                    
                    if 'file_path' in rec:
                        recommendations_html += f"<p><strong>File:</strong> {rec['file_path']}</p>"
                    
                    recommendations_html += "</div>"
            
            # Use provided template or default
            template_content = default_template
            if template and os.path.exists(template):
                with open(template, 'r') as f:
                    template_content = f.read()
            
            # Format the HTML content
            formatted_content = template_content.format(
                title=title,
                summary=json.dumps(summary, indent=2),
                content=json.dumps(report_data, indent=2),
                recommendations=recommendations_html,
                timestamp=datetime.now().isoformat()
            )
            
            # Write to file
            with open(output_path, 'w') as f:
                f.write(formatted_content)
                
            logger.info(f"Exported HTML report to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating HTML report {output_path}: {e}")
            raise

    def _get_css_class_for_priority(self, priority: str) -> str:
        """Get CSS class based on priority/severity level."""
        priority_lower = priority.lower()
        if priority_lower in ['critical', 'high']:
            return 'warning'
        elif priority_lower == 'medium':
            return 'finding finding-medium'
        elif priority_lower == 'low':
            return 'finding finding-low'
        else:
            return 'recommendation'

    def _create_summary(self, data: Any) -> Dict[str, Any]:
        """Create a summary of the analysis data."""
        summary = {}
        
        if isinstance(data, dict):
            # Extract key metrics for summary
            if 'scan_status' in data:
                summary['status'] = data['scan_status']
                
            if 'analysis_duration_seconds' in data:
                summary['analysis_duration'] = f"{data['analysis_duration_seconds']:.2f} seconds"
            elif 'duration' in data:
                summary['analysis_duration'] = f"{data['duration']:.2f} seconds"
                
            # Extract database-specific metrics
            if 'total_files_scanned' in data:
                summary['total_files'] = data['total_files_scanned']
            elif 'total_files' in data:
                summary['total_files'] = data['total_files']
                
            if 'total_size_bytes' in data:
                summary['total_size'] = self._format_bytes(data['total_size_bytes'])
                
            if 'total_backup_size_bytes' in data:
                summary['total_backup_size'] = self._format_bytes(data['total_backup_size_bytes'])
                
            if 'total_log_size_bytes' in data:
                summary['total_log_size'] = self._format_bytes(data['total_log_size_bytes'])
                
            if 'overall_compression_ratio' in data:
                summary['compression_ratio'] = f"{data['overall_compression_ratio']:.2f}x"
                
            if 'growth_rate_bytes_per_day' in data:
                summary['daily_growth'] = self._format_bytes(data['growth_rate_bytes_per_day']) + "/day"
            
            # Extract security-specific metrics
            if 'files_with_sensitive_data' in data:
                summary['files_with_sensitive_data'] = data['files_with_sensitive_data']
                
            if 'total_matches' in data:
                summary['total_matches'] = data['total_matches']
                
            # Count recommendations/findings by priority
            recommendations_key = 'recommendations' if 'recommendations' in data else 'findings'
            if recommendations_key in data and isinstance(data[recommendations_key], list):
                by_priority = {}
                for rec in data[recommendations_key]:
                    if isinstance(rec, dict):
                        priority = rec.get('priority', rec.get('severity', 'unknown'))
                        by_priority[priority] = by_priority.get(priority, 0) + 1
                if by_priority:
                    summary['findings_by_priority'] = by_priority
        
        return summary

    def _format_bytes(self, size_bytes: Union[int, float]) -> str:
        """Format bytes to human-readable size."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


class NotificationInterface:
    """
    Interface for sending notifications about analysis results.
    
    This class provides a standardized interface for sending notifications
    about critical findings and recommendations to various channels.
    """

    def __init__(
        self,
        notification_threshold: str = "high",
        max_notifications_per_run: int = 10,
    ):
        """
        Initialize the notification interface.

        Args:
            notification_threshold: Minimum priority for notifications ("critical", "high", "medium", "low")
            max_notifications_per_run: Maximum number of notifications to send per analysis run
        """
        self.notification_threshold = notification_threshold
        self.max_notifications_per_run = max_notifications_per_run
        self.priority_levels = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
            "informational": 4
        }
        self.threshold_level = self.priority_levels.get(notification_threshold.lower(), 2)

    def should_notify(self, priority: str) -> bool:
        """Determine if an item meets the notification threshold."""
        if not priority:
            return False
            
        priority_level = self.priority_levels.get(priority.lower(), 4)
        return priority_level <= self.threshold_level

    def filter_notifications(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter recommendations/findings to those that meet notification criteria.

        Args:
            items: List of recommendation/finding dictionaries

        Returns:
            Filtered list of items for notification
        """
        if not items:
            return []
            
        # Filter by priority threshold
        filtered = []
        for item in items:
            priority = item.get('priority', item.get('severity', ''))
            if self.should_notify(priority):
                filtered.append(item)
        
        # Sort by priority (most important first)
        sorted_items = sorted(
            filtered,
            key=lambda r: self.priority_levels.get(
                r.get('priority', r.get('severity', '')).lower(), 4
            )
        )
        
        # Limit to max notifications
        return sorted_items[:self.max_notifications_per_run]

    def send_email_notification(
        self,
        items: List[Dict[str, Any]],
        recipient: str,
        subject: Optional[str] = None,
        smtp_config: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Send email notification about critical findings.

        Args:
            items: List of recommendation/finding dictionaries
            recipient: Email recipient
            subject: Email subject
            smtp_config: SMTP server configuration

        Returns:
            Success status
        """
        logger.info(f"Email notification would be sent to {recipient} (mock implementation)")
        
        # Filter items
        filtered_items = self.filter_notifications(items)
        if not filtered_items:
            logger.info("No items meet notification threshold")
            return True
            
        # In a real implementation, this would send an actual email
        # For testing purposes, just log the notification
        logger.info(f"Would send {len(filtered_items)} items to {recipient}")
        for i, item in enumerate(filtered_items):
            priority = item.get('priority', item.get('severity', 'unknown'))
            title = item.get('title', item.get('description', 'Unnamed'))
            logger.info(f"  {i+1}. [{priority}] {title}")
            
        return True

    def send_webhook_notification(
        self,
        items: List[Dict[str, Any]],
        webhook_url: str,
        custom_payload: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Send webhook notification about critical findings.

        Args:
            items: List of recommendation/finding dictionaries
            webhook_url: Webhook URL
            custom_payload: Custom payload fields to include

        Returns:
            Success status
        """
        logger.info(f"Webhook notification would be sent to {webhook_url} (mock implementation)")
        
        # Filter items
        filtered_items = self.filter_notifications(items)
        if not filtered_items:
            logger.info("No items meet notification threshold")
            return True
            
        # In a real implementation, this would send an actual webhook request
        # For testing purposes, just log the notification
        logger.info(f"Would send {len(filtered_items)} items to webhook")
        
        # Construct payload (for logging purposes only)
        payload = {
            "timestamp": datetime.now().isoformat(),
            "items": filtered_items,
        }
        
        if custom_payload:
            payload.update(custom_payload)
            
        logger.debug(f"Webhook payload: {json.dumps(payload)}")
        
        return True