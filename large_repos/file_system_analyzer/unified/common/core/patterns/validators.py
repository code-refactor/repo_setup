"""
Pattern validation utilities for ensuring pattern correctness and effectiveness.

This module provides tools to validate patterns before they are used,
test their effectiveness, and ensure they meet quality standards.
"""

import re
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass
from enum import Enum

from .engine import BasePattern, PatternMatch


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in a pattern."""
    severity: ValidationSeverity
    code: str
    message: str
    suggestion: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None


class PatternValidator:
    """Validator for pattern definitions and their regex expressions."""
    
    def __init__(self):
        self.validation_rules = self._initialize_rules()
    
    def validate_pattern(self, pattern: BasePattern) -> List[ValidationIssue]:
        """Validate a pattern definition."""
        issues = []
        
        # Validate basic properties
        issues.extend(self._validate_basic_properties(pattern))
        
        # Validate regex syntax
        issues.extend(self._validate_regex_syntax(pattern))
        
        # Validate regex effectiveness
        issues.extend(self._validate_regex_effectiveness(pattern))
        
        # Validate pattern-specific rules
        issues.extend(self._validate_pattern_specific(pattern))
        
        return issues
    
    def validate_patterns(self, patterns: List[BasePattern]) -> Dict[str, List[ValidationIssue]]:
        """Validate multiple patterns."""
        results = {}
        for pattern in patterns:
            results[pattern.name] = self.validate_pattern(pattern)
        return results
    
    def _validate_basic_properties(self, pattern: BasePattern) -> List[ValidationIssue]:
        """Validate basic pattern properties."""
        issues = []
        
        # Check required fields
        if not pattern.name:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                code="MISSING_NAME",
                message="Pattern name is required"
            ))
        
        if not pattern.description:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="MISSING_DESCRIPTION",
                message="Pattern description is recommended",
                suggestion="Add a clear description of what this pattern matches"
            ))
        
        if not pattern.pattern:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                code="MISSING_PATTERN",
                message="Pattern regex is required"
            ))
        
        # Check name format
        if pattern.name and not re.match(r'^[A-Za-z0-9\s\-_]+$', pattern.name):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="INVALID_NAME_FORMAT",
                message="Pattern name contains special characters",
                suggestion="Use only letters, numbers, spaces, hyphens, and underscores"
            ))
        
        return issues
    
    def _validate_regex_syntax(self, pattern: BasePattern) -> List[ValidationIssue]:
        """Validate regex syntax."""
        issues = []
        
        if not pattern.pattern:
            return issues
        
        try:
            re.compile(pattern.pattern, re.IGNORECASE)
        except re.error as e:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                code="INVALID_REGEX",
                message=f"Invalid regex syntax: {e}",
                suggestion="Check regex syntax and escape special characters"
            ))
            return issues  # Don't continue if regex is invalid
        
        # Check for common regex issues
        issues.extend(self._check_regex_issues(pattern.pattern))
        
        return issues
    
    def _validate_regex_effectiveness(self, pattern: BasePattern) -> List[ValidationIssue]:
        """Validate regex effectiveness and performance."""
        issues = []
        
        if not pattern.pattern or not pattern.compiled_regex:
            return issues
        
        # Check for overly broad patterns
        if self._is_overly_broad(pattern.pattern):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="OVERLY_BROAD",
                message="Pattern may match too broadly",
                suggestion="Consider adding more specific constraints"
            ))
        
        # Check for potential performance issues
        performance_issues = self._check_performance_issues(pattern.pattern)
        issues.extend(performance_issues)
        
        # Check for false positive risks
        fp_issues = self._check_false_positive_risks(pattern)
        issues.extend(fp_issues)
        
        return issues
    
    def _validate_pattern_specific(self, pattern: BasePattern) -> List[ValidationIssue]:
        """Validate pattern-specific rules based on pattern type."""
        issues = []
        
        # Import here to avoid circular imports
        from .engine import CompliancePattern, FilePattern
        
        if isinstance(pattern, CompliancePattern):
            issues.extend(self._validate_compliance_pattern(pattern))
        elif isinstance(pattern, FilePattern):
            issues.extend(self._validate_file_pattern(pattern))
        
        return issues
    
    def _validate_compliance_pattern(self, pattern) -> List[ValidationIssue]:
        """Validate compliance-specific pattern rules."""
        issues = []
        
        # Check if sensitive patterns have validation functions
        if pattern.sensitivity.value in ["high", "critical"] and not pattern.validation_func:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="MISSING_VALIDATION",
                message="High/critical sensitivity patterns should have validation functions",
                suggestion="Add a validation function to reduce false positives"
            ))
        
        # Check if context rules are present for ambiguous patterns
        ambiguous_categories = ["credentials", "financial"]
        if pattern.category.value in ambiguous_categories and not pattern.context_rules:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="MISSING_CONTEXT_RULES",
                message="Ambiguous patterns should have context rules",
                suggestion="Add context rules to improve accuracy"
            ))
        
        return issues
    
    def _validate_file_pattern(self, pattern) -> List[ValidationIssue]:
        """Validate file pattern specific rules."""
        issues = []
        
        # Check if file patterns have anchors
        if not pattern.pattern.endswith('$') and not pattern.pattern.startswith('^'):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                code="MISSING_ANCHORS",
                message="File patterns often benefit from anchors",
                suggestion="Consider adding ^ or $ anchors for exact matching"
            ))
        
        return issues
    
    def _check_regex_issues(self, pattern: str) -> List[ValidationIssue]:
        """Check for common regex issues."""
        issues = []
        
        # Check for catastrophic backtracking risks
        backtrack_patterns = [
            r'\(\.\*\)\+',
            r'\(\.\*\)\*',
            r'\(\w+\)\+\1',
            r'\([^)]*\+[^)]*\)\*',
        ]
        
        for bt_pattern in backtrack_patterns:
            if re.search(bt_pattern, pattern):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    code="CATASTROPHIC_BACKTRACKING_RISK",
                    message="Pattern may cause catastrophic backtracking",
                    suggestion="Revise pattern to avoid nested quantifiers"
                ))
        
        # Check for inefficient patterns
        if '..*' in pattern:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="INEFFICIENT_QUANTIFIER",
                message="Consecutive .* quantifiers can be combined",
                suggestion="Combine .* patterns for better performance"
            ))
        
        # Check for unescaped special characters in likely literal contexts
        literal_specials = ['.', '+', '*', '?', '^', '$', '(', ')', '[', ']', '{', '}', '|', '\\']
        for char in literal_specials:
            if char in pattern and f'\\{char}' not in pattern:
                # Only warn for common cases where escaping is likely needed
                if char in ['.', '+', '*', '?'] and pattern.count(char) == 1:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.INFO,
                        code="UNESCAPED_SPECIAL_CHAR",
                        message=f"Special character '{char}' may need escaping",
                        suggestion=f"Use \\{char} if you want to match the literal character"
                    ))
        
        return issues
    
    def _is_overly_broad(self, pattern: str) -> bool:
        """Check if a pattern is overly broad."""
        broad_indicators = [
            r'^\.\*',  # Starts with .*
            r'\.\*$',  # Ends with .*
            r'^\.\+',  # Starts with .+
            r'\.\+$',  # Ends with .+
            r'^\w+$',  # Just word characters
            r'^\d+$',  # Just digits
        ]
        
        return any(re.search(indicator, pattern) for indicator in broad_indicators)
    
    def _check_performance_issues(self, pattern: str) -> List[ValidationIssue]:
        """Check for potential performance issues."""
        issues = []
        
        # Complex patterns
        if len(pattern) > 200:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="VERY_LONG_PATTERN",
                message="Very long patterns may impact performance",
                suggestion="Consider breaking into multiple simpler patterns"
            ))
        
        # Many alternations
        if pattern.count('|') > 10:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="MANY_ALTERNATIONS",
                message="Many alternations may impact performance",
                suggestion="Consider using character classes or separate patterns"
            ))
        
        # Deep nesting
        nesting_depth = 0
        max_depth = 0
        for char in pattern:
            if char == '(':
                nesting_depth += 1
                max_depth = max(max_depth, nesting_depth)
            elif char == ')':
                nesting_depth -= 1
        
        if max_depth > 5:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="DEEP_NESTING",
                message="Deeply nested patterns may impact performance",
                suggestion="Consider flattening the pattern structure"
            ))
        
        return issues
    
    def _check_false_positive_risks(self, pattern: BasePattern) -> List[ValidationIssue]:
        """Check for false positive risks."""
        issues = []
        
        # Patterns without validation that match common formats
        risky_patterns = {
            r'\d{9}': "9-digit numbers (could match many things)",
            r'\d{16}': "16-digit numbers (could match non-card numbers)",
            r'\w+@\w+\.\w+': "Simple email patterns (could match non-emails)",
        }
        
        for risky_pattern, description in risky_patterns.items():
            if re.search(risky_pattern, pattern.pattern) and not pattern.validation_func:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    code="FALSE_POSITIVE_RISK",
                    message=f"Pattern matches {description}",
                    suggestion="Consider adding validation or making pattern more specific"
                ))
        
        return issues
    
    def _initialize_rules(self) -> Dict[str, Any]:
        """Initialize validation rules."""
        return {
            "max_pattern_length": 500,
            "max_alternations": 15,
            "max_nesting_depth": 8,
            "required_fields": ["name", "pattern"],
            "recommended_fields": ["description", "category"]
        }


class PatternTester:
    """Test patterns against sample data."""
    
    def __init__(self):
        self.test_cases: Dict[str, List[Tuple[str, bool]]] = {}
    
    def add_test_case(self, pattern_name: str, text: str, should_match: bool):
        """Add a test case for a pattern."""
        if pattern_name not in self.test_cases:
            self.test_cases[pattern_name] = []
        self.test_cases[pattern_name].append((text, should_match))
    
    def test_pattern(self, pattern: BasePattern) -> Dict[str, Any]:
        """Test a pattern against its test cases."""
        if pattern.name not in self.test_cases:
            return {"error": "No test cases found for pattern"}
        
        results = {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "details": []
        }
        
        for text, should_match in self.test_cases[pattern.name]:
            matches = pattern.match(text)
            has_matches = len(matches) > 0
            
            test_result = {
                "text": text,
                "expected": should_match,
                "actual": has_matches,
                "passed": has_matches == should_match,
                "matches": [m.matched_text for m in matches]
            }
            
            results["details"].append(test_result)
            results["total"] += 1
            
            if test_result["passed"]:
                results["passed"] += 1
            else:
                results["failed"] += 1
        
        results["pass_rate"] = results["passed"] / results["total"] if results["total"] > 0 else 0
        return results
    
    def load_default_test_cases(self):
        """Load default test cases for common patterns."""
        # SSN test cases
        self.add_test_case("Social Security Number", "123-45-6789", True)
        self.add_test_case("Social Security Number", "000-45-6789", False)  # Invalid
        self.add_test_case("Social Security Number", "123-00-6789", False)  # Invalid
        self.add_test_case("Social Security Number", "123456789", False)    # No format
        
        # Credit card test cases
        self.add_test_case("Credit Card Number", "4111111111111111", True)  # Valid Visa
        self.add_test_case("Credit Card Number", "4111111111111112", False) # Invalid checksum
        self.add_test_case("Credit Card Number", "1234567890123456", False) # Not valid card format
        
        # Email test cases
        self.add_test_case("Email Address", "user@example.com", True)
        self.add_test_case("Email Address", "user.name+tag@example.co.uk", True)
        self.add_test_case("Email Address", "invalid.email", False)
        self.add_test_case("Email Address", "@example.com", False)
        
        # Phone number test cases
        self.add_test_case("US Phone Number", "(555) 123-4567", True)
        self.add_test_case("US Phone Number", "555-123-4567", True)
        self.add_test_case("US Phone Number", "5551234567", True)
        self.add_test_case("US Phone Number", "123-456", False)  # Too short


def validate_pattern_collection(patterns: List[BasePattern]) -> Dict[str, Any]:
    """Validate a collection of patterns and return summary report."""
    validator = PatternValidator()
    tester = PatternTester()
    tester.load_default_test_cases()
    
    # Validate all patterns
    validation_results = validator.validate_patterns(patterns)
    
    # Test patterns that have test cases
    test_results = {}
    for pattern in patterns:
        if pattern.name in tester.test_cases:
            test_results[pattern.name] = tester.test_pattern(pattern)
    
    # Generate summary
    total_issues = sum(len(issues) for issues in validation_results.values())
    critical_issues = sum(
        1 for issues in validation_results.values() 
        for issue in issues 
        if issue.severity == ValidationSeverity.CRITICAL
    )
    error_issues = sum(
        1 for issues in validation_results.values() 
        for issue in issues 
        if issue.severity == ValidationSeverity.ERROR
    )
    
    summary = {
        "total_patterns": len(patterns),
        "total_issues": total_issues,
        "critical_issues": critical_issues,
        "error_issues": error_issues,
        "patterns_with_issues": len([name for name, issues in validation_results.items() if issues]),
        "patterns_tested": len(test_results),
        "validation_results": validation_results,
        "test_results": test_results
    }
    
    return summary