"""
Pattern processing engine for unified pattern matching and validation.

This module provides a generic pattern processing framework that can handle
both compliance patterns (for sensitive data detection) and file patterns
(for database file recognition).
"""

import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Pattern, Optional, Union, Any, Callable, Set
from pydantic import BaseModel, Field

from ..types.enums import Priority, SeverityLevel


class PatternType(str, Enum):
    """Type of pattern for different use cases."""
    COMPLIANCE = "compliance"
    FILE_PATTERN = "file_pattern"
    GENERIC = "generic"


class PatternCategory(str, Enum):
    """Categories for pattern classification."""
    # Compliance categories
    PII = "pii"  # Personally Identifiable Information
    PHI = "phi"  # Protected Health Information
    PCI = "pci"  # Payment Card Industry Data
    FINANCIAL = "financial"
    PROPRIETARY = "proprietary"
    CREDENTIALS = "credentials"
    
    # File pattern categories
    DATA = "data"
    INDEX = "index"
    LOG = "log"
    TEMP = "temp"
    CONFIG = "config"
    BACKUP = "backup"
    
    # Generic
    OTHER = "other"


class PatternMatch(BaseModel):
    """Result of a pattern match operation."""
    pattern_name: str
    matched_text: str
    start_position: int
    end_position: int
    confidence: float = 1.0
    context: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BasePattern(BaseModel, ABC):
    """Base class for all pattern definitions."""
    name: str
    description: str
    pattern: str
    pattern_type: PatternType
    category: PatternCategory
    priority: Priority = Priority.MEDIUM
    enabled: bool = True
    compiled_regex: Optional[Pattern] = Field(None, exclude=True)
    validation_func: Optional[str] = None
    context_rules: List[str] = Field(default_factory=list)
    false_positive_examples: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.compiled_regex = re.compile(self.pattern, re.IGNORECASE)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{self.pattern}': {e}")

    @abstractmethod
    def match(self, content: str, context: Optional[str] = None) -> List[PatternMatch]:
        """Find matches of this pattern in the given content."""
        pass

    def is_valid_match(self, match_text: str, context: Optional[str] = None) -> bool:
        """Validate if a match is a true positive."""
        # Apply context rules if available
        if self.context_rules and context:
            for rule in self.context_rules:
                if not self._check_context_rule(rule, context):
                    return False
        
        # Apply validation function if available
        if self.validation_func:
            validator = PatternValidators.get_validator(self.validation_func)
            if validator and not validator(match_text):
                return False
        
        # Check against false positive examples
        if match_text.lower() in [fp.lower() for fp in self.false_positive_examples]:
            return False
            
        return True

    def _check_context_rule(self, rule: str, context: str) -> bool:
        """Check if a context rule is satisfied."""
        if rule.startswith("must be near words like"):
            words = rule.split("must be near words like")[1].strip()
            required_words = [w.strip() for w in words.split(",")]
            context_lower = context.lower()
            return any(word.strip() in context_lower for word in required_words)
        return True


class CompliancePattern(BasePattern):
    """Pattern for compliance/sensitive data detection."""
    sensitivity: SeverityLevel
    
    def __init__(self, **data):
        data["pattern_type"] = PatternType.COMPLIANCE
        super().__init__(**data)

    def match(self, content: str, context: Optional[str] = None) -> List[PatternMatch]:
        """Find compliance pattern matches in content."""
        matches = []
        if not self.enabled or not self.compiled_regex:
            return matches

        for match in self.compiled_regex.finditer(content):
            match_text = match.group()
            if self.is_valid_match(match_text, context):
                matches.append(PatternMatch(
                    pattern_name=self.name,
                    matched_text=match_text,
                    start_position=match.start(),
                    end_position=match.end(),
                    confidence=self._calculate_confidence(match_text, context),
                    context=context,
                    metadata={
                        "sensitivity": self.sensitivity.value,
                        "category": self.category.value,
                        "priority": self.priority.value
                    }
                ))
        return matches

    def _calculate_confidence(self, match_text: str, context: Optional[str] = None) -> float:
        """Calculate confidence score for a match."""
        confidence = 1.0
        
        # Reduce confidence if no context validation
        if self.context_rules and not context:
            confidence *= 0.8
            
        # Adjust based on pattern complexity
        if len(self.pattern) < 20:  # Simple patterns are less reliable
            confidence *= 0.9
            
        return min(confidence, 1.0)


class FilePattern(BasePattern):
    """Pattern for file recognition and classification."""
    engine: Optional[str] = None  # Database engine for DB file patterns
    
    def __init__(self, **data):
        data["pattern_type"] = PatternType.FILE_PATTERN
        super().__init__(**data)

    def match(self, content: str, context: Optional[str] = None) -> List[PatternMatch]:
        """Find file pattern matches."""
        matches = []
        if not self.enabled or not self.compiled_regex:
            return matches

        # For file patterns, we typically match against filenames or paths
        if self.compiled_regex.search(content):
            matches.append(PatternMatch(
                pattern_name=self.name,
                matched_text=content,
                start_position=0,
                end_position=len(content),
                confidence=1.0,
                context=context,
                metadata={
                    "category": self.category.value,
                    "engine": self.engine,
                    "priority": self.priority.value
                }
            ))
        return matches


class PatternEngine:
    """Main pattern processing engine."""
    
    def __init__(self):
        self.patterns: Dict[str, BasePattern] = {}
        self.patterns_by_type: Dict[PatternType, List[BasePattern]] = {
            PatternType.COMPLIANCE: [],
            PatternType.FILE_PATTERN: [],
            PatternType.GENERIC: []
        }
        self.patterns_by_category: Dict[PatternCategory, List[BasePattern]] = {}

    def register_pattern(self, pattern: BasePattern) -> None:
        """Register a new pattern with the engine."""
        self.patterns[pattern.name] = pattern
        self.patterns_by_type[pattern.pattern_type].append(pattern)
        
        if pattern.category not in self.patterns_by_category:
            self.patterns_by_category[pattern.category] = []
        self.patterns_by_category[pattern.category].append(pattern)

    def register_patterns(self, patterns: List[BasePattern]) -> None:
        """Register multiple patterns."""
        for pattern in patterns:
            self.register_pattern(pattern)

    def unregister_pattern(self, pattern_name: str) -> bool:
        """Remove a pattern from the engine."""
        if pattern_name not in self.patterns:
            return False
            
        pattern = self.patterns[pattern_name]
        del self.patterns[pattern_name]
        self.patterns_by_type[pattern.pattern_type].remove(pattern)
        self.patterns_by_category[pattern.category].remove(pattern)
        return True

    def get_pattern(self, pattern_name: str) -> Optional[BasePattern]:
        """Get a pattern by name."""
        return self.patterns.get(pattern_name)

    def get_patterns_by_type(self, pattern_type: PatternType) -> List[BasePattern]:
        """Get all patterns of a specific type."""
        return self.patterns_by_type.get(pattern_type, [])

    def get_patterns_by_category(self, category: PatternCategory) -> List[BasePattern]:
        """Get all patterns in a specific category."""
        return self.patterns_by_category.get(category, [])

    def enable_pattern(self, pattern_name: str) -> bool:
        """Enable a pattern."""
        if pattern_name in self.patterns:
            self.patterns[pattern_name].enabled = True
            return True
        return False

    def disable_pattern(self, pattern_name: str) -> bool:
        """Disable a pattern."""
        if pattern_name in self.patterns:
            self.patterns[pattern_name].enabled = False
            return True
        return False

    def scan_content(
        self, 
        content: str, 
        pattern_type: Optional[PatternType] = None,
        category: Optional[PatternCategory] = None,
        context: Optional[str] = None
    ) -> List[PatternMatch]:
        """Scan content with specified patterns."""
        matches = []
        
        # Determine which patterns to use
        patterns_to_use = []
        if pattern_type:
            patterns_to_use.extend(self.get_patterns_by_type(pattern_type))
        elif category:
            patterns_to_use.extend(self.get_patterns_by_category(category))
        else:
            patterns_to_use = list(self.patterns.values())
        
        # Filter enabled patterns only
        patterns_to_use = [p for p in patterns_to_use if p.enabled]
        
        # Apply patterns
        for pattern in patterns_to_use:
            try:
                pattern_matches = pattern.match(content, context)
                matches.extend(pattern_matches)
            except Exception as e:
                # Log error but continue with other patterns
                print(f"Error applying pattern {pattern.name}: {e}")
                continue
        
        # Sort matches by position and confidence
        matches.sort(key=lambda m: (m.start_position, -m.confidence))
        return matches

    def scan_file_path(self, file_path: str, engine: Optional[str] = None) -> List[PatternMatch]:
        """Scan a file path against file patterns."""
        matches = []
        file_patterns = self.get_patterns_by_type(PatternType.FILE_PATTERN)
        
        for pattern in file_patterns:
            if not pattern.enabled:
                continue
                
            # If engine is specified, only use patterns for that engine
            if engine and hasattr(pattern, 'engine') and pattern.engine and pattern.engine != engine:
                continue
                
            try:
                pattern_matches = pattern.match(file_path)
                matches.extend(pattern_matches)
            except Exception as e:
                print(f"Error applying file pattern {pattern.name}: {e}")
                continue
        
        return matches

    def get_statistics(self) -> Dict[str, Any]:
        """Get engine statistics."""
        total_patterns = len(self.patterns)
        enabled_patterns = sum(1 for p in self.patterns.values() if p.enabled)
        
        stats = {
            "total_patterns": total_patterns,
            "enabled_patterns": enabled_patterns,
            "disabled_patterns": total_patterns - enabled_patterns,
            "by_type": {
                pt.value: len(patterns) for pt, patterns in self.patterns_by_type.items()
            },
            "by_category": {
                cat.value: len(patterns) for cat, patterns in self.patterns_by_category.items()
            }
        }
        return stats


class PatternValidators:
    """Registry of validation functions for patterns."""
    
    _validators: Dict[str, Callable[[str], bool]] = {}
    
    @classmethod
    def register_validator(cls, name: str, func: Callable[[str], bool]) -> None:
        """Register a validation function."""
        cls._validators[name] = func
    
    @classmethod
    def get_validator(cls, name: str) -> Optional[Callable[[str], bool]]:
        """Get a validation function by name."""
        return cls._validators.get(name)
    
    @classmethod
    def list_validators(cls) -> List[str]:
        """List all registered validator names."""
        return list(cls._validators.keys())


# Register common validators
def validate_ssn(ssn: str) -> bool:
    """Validate a Social Security Number."""
    ssn = re.sub(r'[\s-]', '', ssn)
    if not re.match(r'^\d{9}$', ssn):
        return False
    if ssn[0:3] == '000' or ssn[3:5] == '00' or ssn[5:9] == '0000':
        return False
    if ssn[0:3] == '666' or int(ssn[0:3]) >= 900:
        return False
    return True


def validate_credit_card(cc: str) -> bool:
    """Validate a credit card number using the Luhn algorithm."""
    cc = re.sub(r'\D', '', cc)
    if not cc.isdigit() or not (13 <= len(cc) <= 19):
        return False
    
    # Luhn algorithm
    digits = [int(d) for d in cc]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(divmod(d * 2, 10))
    return checksum % 10 == 0


# Register built-in validators
PatternValidators.register_validator("validate_ssn", validate_ssn)
PatternValidators.register_validator("validate_credit_card", validate_credit_card)