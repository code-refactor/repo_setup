"""
Pattern compilation utilities for optimizing pattern matching performance.

This module provides utilities to compile, optimize, and manage pattern
collections for efficient pattern matching operations.
"""

import re
from typing import Dict, List, Pattern, Optional, Union, Any, Set
from collections import defaultdict

from .engine import BasePattern, PatternType, PatternCategory, CompliancePattern, FilePattern
from ..types.enums import Priority, SeverityLevel


class PatternCompiler:
    """Compiler for optimizing pattern matching performance."""
    
    def __init__(self):
        self.compiled_groups: Dict[str, Pattern] = {}
        self.pattern_mappings: Dict[str, List[str]] = {}
    
    def compile_pattern_group(
        self, 
        patterns: List[BasePattern], 
        group_name: str,
        optimize: bool = True
    ) -> Pattern:
        """
        Compile multiple patterns into a single optimized regex.
        
        Args:
            patterns: List of patterns to compile together
            group_name: Name for the compiled group
            optimize: Whether to apply optimization techniques
            
        Returns:
            Compiled regex pattern
        """
        if not patterns:
            raise ValueError("Cannot compile empty pattern list")
        
        # Extract regex patterns
        regex_patterns = []
        pattern_names = []
        
        for pattern in patterns:
            if pattern.enabled:
                # Wrap each pattern in a named group
                group_pattern = f"(?P<{self._sanitize_name(pattern.name)}>{pattern.pattern})"
                regex_patterns.append(group_pattern)
                pattern_names.append(pattern.name)
        
        if not regex_patterns:
            raise ValueError("No enabled patterns to compile")
        
        # Combine patterns with alternation
        combined_pattern = "|".join(regex_patterns)
        
        if optimize:
            combined_pattern = self._optimize_pattern(combined_pattern)
        
        # Compile the final pattern
        try:
            compiled = re.compile(combined_pattern, re.IGNORECASE | re.MULTILINE)
            self.compiled_groups[group_name] = compiled
            self.pattern_mappings[group_name] = pattern_names
            return compiled
        except re.error as e:
            raise ValueError(f"Failed to compile pattern group '{group_name}': {e}")
    
    def compile_by_category(
        self, 
        patterns: List[BasePattern], 
        optimize: bool = True
    ) -> Dict[PatternCategory, Pattern]:
        """Compile patterns grouped by category."""
        category_patterns = defaultdict(list)
        
        # Group patterns by category
        for pattern in patterns:
            category_patterns[pattern.category].append(pattern)
        
        compiled_groups = {}
        for category, cat_patterns in category_patterns.items():
            group_name = f"category_{category.value}"
            try:
                compiled_groups[category] = self.compile_pattern_group(
                    cat_patterns, group_name, optimize
                )
            except ValueError as e:
                print(f"Warning: Failed to compile category {category}: {e}")
                continue
        
        return compiled_groups
    
    def compile_by_type(
        self, 
        patterns: List[BasePattern], 
        optimize: bool = True
    ) -> Dict[PatternType, Pattern]:
        """Compile patterns grouped by type."""
        type_patterns = defaultdict(list)
        
        # Group patterns by type
        for pattern in patterns:
            type_patterns[pattern.pattern_type].append(pattern)
        
        compiled_groups = {}
        for pattern_type, type_pats in type_patterns.items():
            group_name = f"type_{pattern_type.value}"
            try:
                compiled_groups[pattern_type] = self.compile_pattern_group(
                    type_pats, group_name, optimize
                )
            except ValueError as e:
                print(f"Warning: Failed to compile type {pattern_type}: {e}")
                continue
        
        return compiled_groups
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize pattern name for use in regex group names."""
        # Replace non-alphanumeric characters with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        # Ensure it starts with a letter or underscore
        if sanitized and sanitized[0].isdigit():
            sanitized = f"pattern_{sanitized}"
        return sanitized or "unnamed"
    
    def _optimize_pattern(self, pattern: str) -> str:
        """Apply optimization techniques to the pattern."""
        # Basic optimizations
        optimized = pattern
        
        # Remove redundant grouping
        optimized = re.sub(r'\(\?:', '(?:', optimized)
        
        # Optimize character classes (basic)
        optimized = re.sub(r'\[0-9\]', r'\d', optimized)
        optimized = re.sub(r'\[a-zA-Z\]', r'[a-zA-Z]', optimized)  # Keep as is
        
        return optimized
    
    def get_compiled_group(self, group_name: str) -> Optional[Pattern]:
        """Get a compiled pattern group by name."""
        return self.compiled_groups.get(group_name)
    
    def get_group_patterns(self, group_name: str) -> List[str]:
        """Get the pattern names in a compiled group."""
        return self.pattern_mappings.get(group_name, [])
    
    def clear_compiled_groups(self) -> None:
        """Clear all compiled groups."""
        self.compiled_groups.clear()
        self.pattern_mappings.clear()


class PatternOptimizer:
    """Utilities for optimizing pattern performance."""
    
    @staticmethod
    def analyze_pattern_complexity(pattern: str) -> Dict[str, Any]:
        """Analyze the complexity of a regex pattern."""
        complexity_metrics = {
            "length": len(pattern),
            "groups": pattern.count("("),
            "alternations": pattern.count("|"),
            "quantifiers": len(re.findall(r'[*+?{]', pattern)),
            "character_classes": pattern.count("["),
            "anchors": len(re.findall(r'[\^$]', pattern)),
            "lookarounds": len(re.findall(r'\(\?\w*[=!]', pattern)),
            "estimated_complexity": "low"
        }
        
        # Estimate overall complexity
        score = (
            complexity_metrics["alternations"] * 3 +
            complexity_metrics["quantifiers"] * 2 +
            complexity_metrics["lookarounds"] * 5 +
            complexity_metrics["groups"] +
            complexity_metrics["length"] / 20
        )
        
        if score > 50:
            complexity_metrics["estimated_complexity"] = "high"
        elif score > 20:
            complexity_metrics["estimated_complexity"] = "medium"
        
        return complexity_metrics
    
    @staticmethod
    def suggest_optimizations(pattern: str) -> List[str]:
        """Suggest optimizations for a regex pattern."""
        suggestions = []
        
        # Check for common inefficiencies
        if ".*.*" in pattern:
            suggestions.append("Consider combining consecutive .* quantifiers")
        
        if pattern.count("(") > 10:
            suggestions.append("Consider reducing the number of capture groups")
        
        if "|" in pattern and pattern.count("|") > 5:
            suggestions.append("Consider splitting complex alternations into separate patterns")
        
        if re.search(r'\[0-9\]', pattern):
            suggestions.append("Replace [0-9] with \\d for better performance")
        
        if re.search(r'\[\w\]', pattern):
            suggestions.append("Consider using character class shortcuts")
        
        # Check for catastrophic backtracking risks
        if re.search(r'\(\.\*\)\+', pattern) or re.search(r'\(\.\*\)\*', pattern):
            suggestions.append("WARNING: Pattern may cause catastrophic backtracking")
        
        return suggestions
    
    @staticmethod
    def benchmark_pattern(pattern: str, test_strings: List[str], iterations: int = 1000) -> Dict[str, float]:
        """Benchmark a pattern against test strings."""
        import time
        
        try:
            compiled = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            return {"error": str(e)}
        
        # Measure compilation time
        start_time = time.time()
        for _ in range(iterations):
            re.compile(pattern, re.IGNORECASE)
        compile_time = (time.time() - start_time) / iterations
        
        # Measure matching time
        total_match_time = 0
        matches_found = 0
        
        for test_string in test_strings:
            start_time = time.time()
            for _ in range(iterations):
                matches = compiled.findall(test_string)
                matches_found += len(matches)
            total_match_time += time.time() - start_time
        
        avg_match_time = total_match_time / (len(test_strings) * iterations) if test_strings else 0
        
        return {
            "compile_time_ms": compile_time * 1000,
            "match_time_ms": avg_match_time * 1000,
            "matches_found": matches_found,
            "total_test_strings": len(test_strings)
        }


class PatternLibrary:
    """Pre-built pattern libraries for common use cases."""
    
    @staticmethod
    def get_compliance_patterns() -> List[CompliancePattern]:
        """Get a collection of common compliance patterns."""
        patterns = []
        
        # Social Security Numbers
        patterns.append(CompliancePattern(
            name="Social Security Number",
            description="US Social Security Number",
            pattern=r"\b(?!000|666|9\d{2})([0-8]\d{2}|7([0-6]\d))-(?!00)(\d{2})-(?!0000)(\d{4})\b",
            category=PatternCategory.PII,
            sensitivity=SeverityLevel.HIGH,
            validation_func="validate_ssn"
        ))
        
        # Credit Card Numbers
        patterns.append(CompliancePattern(
            name="Credit Card Number",
            description="Credit card number (major brands)",
            pattern=r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\b",
            category=PatternCategory.PCI,
            sensitivity=SeverityLevel.HIGH,
            validation_func="validate_credit_card"
        ))
        
        # Email Addresses
        patterns.append(CompliancePattern(
            name="Email Address",
            description="Email address",
            pattern=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            category=PatternCategory.PII,
            sensitivity=SeverityLevel.MEDIUM
        ))
        
        # Phone Numbers
        patterns.append(CompliancePattern(
            name="US Phone Number",
            description="US phone number (various formats)",
            pattern=r"\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b",
            category=PatternCategory.PII,
            sensitivity=SeverityLevel.MEDIUM
        ))
        
        # API Keys
        patterns.append(CompliancePattern(
            name="API Key",
            description="Common API key formats",
            pattern=r"\b[A-Za-z0-9_\-]{32,45}\b",
            category=PatternCategory.CREDENTIALS,
            sensitivity=SeverityLevel.HIGH,
            context_rules=["must be near words like key, api, token, secret"]
        ))
        
        return patterns
    
    @staticmethod
    def get_database_file_patterns() -> List[FilePattern]:
        """Get database file recognition patterns."""
        patterns = []
        
        # MySQL patterns
        mysql_patterns = [
            ("MySQL Data File", r".*\.ibd$", PatternCategory.DATA),
            ("MySQL Index File", r".*\.MYI$", PatternCategory.INDEX),
            ("MySQL Binary Log", r".*bin\.([0-9]+)$", PatternCategory.LOG),
            ("MySQL Config", r".*\.cnf$", PatternCategory.CONFIG),
            ("MySQL Backup", r".*\.sql$", PatternCategory.BACKUP),
        ]
        
        for name, pattern, category in mysql_patterns:
            patterns.append(FilePattern(
                name=name,
                description=f"MySQL {category.value} file pattern",
                pattern=pattern,
                category=category,
                engine="mysql",
                metadata={"engine": "mysql"}
            ))
        
        # PostgreSQL patterns
        postgresql_patterns = [
            ("PostgreSQL Data File", r"[0-9]+$", PatternCategory.DATA),
            ("PostgreSQL Log", r"postgresql-.*\.log$", PatternCategory.LOG),
            ("PostgreSQL Config", r"postgresql\.conf$", PatternCategory.CONFIG),
            ("PostgreSQL Backup", r".*\.dump$", PatternCategory.BACKUP),
        ]
        
        for name, pattern, category in postgresql_patterns:
            patterns.append(FilePattern(
                name=name,
                description=f"PostgreSQL {category.value} file pattern",
                pattern=pattern,
                category=category,
                engine="postgresql",
                metadata={"engine": "postgresql"}
            ))
        
        # MongoDB patterns
        mongodb_patterns = [
            ("MongoDB Data File", r".*\.wt$", PatternCategory.DATA),
            ("MongoDB Log", r"mongod\.log.*", PatternCategory.LOG),
            ("MongoDB Config", r"mongod\.conf$", PatternCategory.CONFIG),
            ("MongoDB Backup", r".*\.archive$", PatternCategory.BACKUP),
        ]
        
        for name, pattern, category in mongodb_patterns:
            patterns.append(FilePattern(
                name=name,
                description=f"MongoDB {category.value} file pattern",
                pattern=pattern,
                category=category,
                engine="mongodb",
                metadata={"engine": "mongodb"}
            ))
        
        return patterns