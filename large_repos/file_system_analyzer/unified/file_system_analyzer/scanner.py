"""
Compliance Data Discovery Scanner.

This module provides the main scanner functionality that integrates all the components
of the Compliance Data Discovery Analyzer.
"""

import os
import time
import json
from datetime import datetime, timezone
from typing import Dict, List, Set, Optional, Any, Union, Tuple, Iterator

from pydantic import BaseModel, Field

from file_system_analyzer.detection.scanner import (
    SensitiveDataScanner, 
    ScanOptions, 
    ScanResult,
    ScanSummary
)
from file_system_analyzer.detection.patterns import (
    PatternDefinitions,
    ComplianceCategory,
    SensitivityLevel
)
from file_system_analyzer.audit.logger import (
    AuditLogger,
    AuditEventType
)
from file_system_analyzer.reporting.reports import (
    ReportGenerator,
    ComplianceReport
)
from file_system_analyzer.reporting.frameworks import FrameworkRegistry
from file_system_analyzer.differential.analyzer import (
    DifferentialAnalyzer,
    ScanBaseline,
    DifferentialScanResult
)
from file_system_analyzer.custody.evidence import (
    EvidencePackager,
    EvidencePackage,
    EvidenceType
)
from file_system_analyzer.utils.crypto import CryptoProvider


class ComplianceScanOptions(BaseModel):
    """Options for a compliance scan."""
    scan_options: ScanOptions = Field(default_factory=ScanOptions)
    output_dir: Optional[str] = None
    user_id: str = "system"
    baseline_id: Optional[str] = None
    create_baseline: bool = False
    baseline_name: Optional[str] = None
    generate_reports: bool = True
    report_frameworks: List[str] = Field(default_factory=list)
    create_evidence_package: bool = False
    evidence_package_name: Optional[str] = None
    audit_log_file: Optional[str] = None


class ComplianceScanner:
    """Main scanner for compliance data discovery."""
    
    def __init__(
        self, 
        options: Optional[ComplianceScanOptions] = None,
        crypto_provider: Optional[CryptoProvider] = None
    ):
        """Initialize scanner with options."""
        self.options = options or ComplianceScanOptions()
        self.crypto_provider = crypto_provider or CryptoProvider.generate()
        
        # Create components
        self.scanner = SensitiveDataScanner(self.options.scan_options)
        self.audit_logger = AuditLogger(
            log_file=self.options.audit_log_file,
            crypto_provider=self.crypto_provider,
            user_id=self.options.user_id
        )
        self.diff_analyzer = DifferentialAnalyzer()
        self.evidence_packager = EvidencePackager(crypto_provider=self.crypto_provider)
        
        # Initialize state
        self.scan_results = []
        self.scan_summary = None
        self.baseline = None
        self.diff_result = None
        self.reports = {}
        self.evidence_package = None
    
    def scan_directory(self, directory_path: str) -> ScanSummary:
        """Scan a directory for sensitive data."""
        start_time = datetime.now(timezone.utc)
        start_timestamp = time.time()
        
        # Log scan start
        self.audit_logger.log_event(
            event_type=AuditEventType.SCAN_START,
            details={
                "directory": directory_path,
                "recursive": self.options.scan_options.recursive,
                "max_file_size": self.options.scan_options.max_file_size,
                "categories": [c.value for c in self.options.scan_options.categories],
                "min_sensitivity": self.options.scan_options.min_sensitivity
            },
            user_id=self.options.user_id
        )
        
        try:
            # Perform the scan
            self.scan_results = list(self.scanner.scan_directory(directory_path))
            
            # Create scan summary
            self.scan_summary = self.scanner.summarize_scan(self.scan_results)
            
            # Create baseline if requested
            if self.options.create_baseline:
                baseline_name = self.options.baseline_name or f"Baseline_{start_time.strftime('%Y%m%d_%H%M%S')}"
                self.baseline = self.diff_analyzer.create_baseline(
                    scan_results=self.scan_results,
                    name=baseline_name,
                    baseline_id=self.options.baseline_id,
                    crypto_provider=self.crypto_provider
                )
                
                # Save baseline if output directory is specified
                if self.options.output_dir:
                    os.makedirs(self.options.output_dir, exist_ok=True)
                    baseline_path = os.path.join(self.options.output_dir, f"{baseline_name}.json")
                    self.diff_analyzer.save_baseline(self.baseline, baseline_path)
                    
                    # Log baseline creation
                    self.audit_logger.log_event(
                        event_type=AuditEventType.BASELINE_CREATION,
                        details={
                            "baseline_id": self.baseline.baseline_id,
                            "baseline_name": baseline_name,
                            "file_path": baseline_path,
                            "file_count": len(self.baseline.files)
                        },
                        user_id=self.options.user_id
                    )
            
            # Compare to baseline if specified
            elif self.options.baseline_id:
                # Load baseline
                baseline_path = os.path.join(
                    self.options.output_dir or ".", 
                    f"{self.options.baseline_id}.json"
                )
                
                if not os.path.exists(baseline_path):
                    raise FileNotFoundError(f"Baseline not found: {baseline_path}")
                    
                baseline = self.diff_analyzer.load_baseline(baseline_path)
                
                # Verify baseline integrity
                if baseline.verification_info and not baseline.verify(self.crypto_provider):
                    raise ValueError("Baseline integrity verification failed")
                    
                # Compare current scan to baseline
                self.diff_result = self.diff_analyzer.compare_to_baseline(
                    baseline=baseline,
                    current_results=self.scan_results
                )
                
                # Log baseline comparison
                self.audit_logger.log_event(
                    event_type=AuditEventType.BASELINE_COMPARISON,
                    details={
                        "baseline_id": baseline.baseline_id,
                        "new_files": len(self.diff_result.new_files),
                        "modified_files": len(self.diff_result.modified_files),
                        "removed_files": len(self.diff_result.removed_files),
                        "new_matches": self.diff_result.total_new_matches,
                        "removed_matches": self.diff_result.total_removed_matches
                    },
                    user_id=self.options.user_id
                )
            
            # Generate compliance reports if requested
            if self.options.generate_reports:
                frameworks = self.options.report_frameworks
                if not frameworks:
                    # Use all frameworks if none specified
                    frameworks = list(FrameworkRegistry.get_all_frameworks().keys())
                
                for framework_id in frameworks:
                    try:
                        report_generator = ReportGenerator(framework_id)
                        report = report_generator.generate_report(
                            scan_results=self.scan_results,
                            scan_summary=self.scan_summary
                        )
                        
                        # Sign the report
                        report.sign(self.crypto_provider)
                        
                        self.reports[framework_id] = report
                        
                        # Save report if output directory is specified
                        if self.options.output_dir:
                            os.makedirs(self.options.output_dir, exist_ok=True)
                            report_path = os.path.join(
                                self.options.output_dir, 
                                f"compliance_report_{framework_id}_{start_time.strftime('%Y%m%d_%H%M%S')}.json"
                            )
                            report.save(report_path, verify=True, crypto_provider=self.crypto_provider)
                            
                            # Log report generation
                            self.audit_logger.log_event(
                                event_type=AuditEventType.REPORT_GENERATION,
                                details={
                                    "framework_id": framework_id,
                                    "framework_name": report.framework_name,
                                    "file_path": report_path,
                                    "finding_count": report.total_findings
                                },
                                user_id=self.options.user_id
                            )
                    except Exception as e:
                        # Log error but continue with other frameworks
                        self.audit_logger.log_event(
                            event_type=AuditEventType.SYSTEM_ERROR,
                            details={
                                "error": f"Failed to generate report for framework {framework_id}: {str(e)}",
                                "framework_id": framework_id
                            },
                            user_id=self.options.user_id
                        )
            
            # Create evidence package if requested
            if self.options.create_evidence_package and self.options.output_dir:
                package_name = self.options.evidence_package_name or f"Evidence_{start_time.strftime('%Y%m%d_%H%M%S')}"
                self.evidence_package = self.evidence_packager.create_package(
                    name=package_name,
                    description=f"Evidence package for scan of {directory_path}",
                    metadata={
                        "scan_directory": directory_path,
                        "scan_time": start_time.isoformat(),
                        "user_id": self.options.user_id
                    }
                )
                
                # Create temporary directory for evidence files
                evidence_dir = os.path.join(self.options.output_dir, "evidence_files")
                os.makedirs(evidence_dir, exist_ok=True)
                
                # Add reports to evidence package
                for framework_id, report in self.reports.items():
                    report_path = os.path.join(
                        evidence_dir, 
                        f"compliance_report_{framework_id}.json"
                    )
                    with open(report_path, 'w') as f:
                        f.write(report.to_json())
                    
                    self.evidence_packager.add_file_to_package(
                        package=self.evidence_package,
                        file_path=report_path,
                        evidence_type=EvidenceType.COMPLIANCE_REPORT,
                        description=f"Compliance report for {report.framework_name}",
                        metadata={
                            "framework_id": framework_id,
                            "framework_name": report.framework_name,
                            "finding_count": report.total_findings
                        }
                    )
                
                # Add baseline to evidence package if created
                if self.baseline:
                    baseline_path = os.path.join(evidence_dir, "baseline.json")
                    self.diff_analyzer.save_baseline(self.baseline, baseline_path)
                    
                    self.evidence_packager.add_file_to_package(
                        package=self.evidence_package,
                        file_path=baseline_path,
                        evidence_type=EvidenceType.SCAN_BASELINE,
                        description="Scan baseline",
                        metadata={
                            "baseline_id": self.baseline.baseline_id,
                            "baseline_name": self.baseline.name,
                            "file_count": len(self.baseline.files)
                        }
                    )
                
                # Add audit log to evidence package
                if self.options.audit_log_file and os.path.exists(self.options.audit_log_file):
                    self.evidence_packager.add_file_to_package(
                        package=self.evidence_package,
                        file_path=self.options.audit_log_file,
                        evidence_type=EvidenceType.AUDIT_LOG,
                        description="Audit log",
                        metadata={
                            "entry_count": len(self.audit_logger.audit_log.entries)
                        }
                    )
                
                # Add scan summary to evidence package
                summary_path = os.path.join(evidence_dir, "scan_summary.json")
                with open(summary_path, 'w') as f:
                    f.write(json.dumps(self.scan_summary.dict(), default=str))
                    
                self.evidence_packager.add_file_to_package(
                    package=self.evidence_package,
                    file_path=summary_path,
                    evidence_type=EvidenceType.METADATA,
                    description="Scan summary",
                    metadata={
                        "total_files": self.scan_summary.total_files,
                        "files_with_sensitive_data": self.scan_summary.files_with_sensitive_data,
                        "total_matches": self.scan_summary.total_matches
                    }
                )
                
                # Export the evidence package
                package_path = self.evidence_packager.export_package(
                    package=self.evidence_package,
                    output_dir=self.options.output_dir,
                    files_dir=evidence_dir,
                    user_id=self.options.user_id
                )
                
                # Log evidence package creation
                self.audit_logger.log_event(
                    event_type=AuditEventType.REPORT_EXPORT,
                    details={
                        "package_id": self.evidence_package.package_id,
                        "package_name": package_name,
                        "file_path": package_path,
                        "item_count": len(self.evidence_package.items)
                    },
                    user_id=self.options.user_id
                )
            
            # Log scan completion
            end_time = datetime.now(timezone.utc)
            duration = time.time() - start_timestamp
            
            self.audit_logger.log_event(
                event_type=AuditEventType.SCAN_COMPLETE,
                details={
                    "directory": directory_path,
                    "duration": duration,
                    "total_files": self.scan_summary.total_files,
                    "files_with_sensitive_data": self.scan_summary.files_with_sensitive_data,
                    "total_matches": self.scan_summary.total_matches
                },
                user_id=self.options.user_id
            )
            
            return self.scan_summary
            
        except Exception as e:
            # Log scan error
            self.audit_logger.log_event(
                event_type=AuditEventType.SCAN_ERROR,
                details={
                    "directory": directory_path,
                    "error": str(e)
                },
                user_id=self.options.user_id
            )
            
            # Re-raise the exception
            raise