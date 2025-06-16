import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Dict, List, Optional, Callable, Pattern
from enum import Enum

from ..models.analysis_results import CategoryResult


class RuleType(Enum):
    DESCRIPTION_CONTAINS = "description_contains"
    DESCRIPTION_REGEX = "description_regex"
    AMOUNT_RANGE = "amount_range"
    AMOUNT_EQUALS = "amount_equals"
    TAG_CONTAINS = "tag_contains"
    CUSTOM_FUNCTION = "custom_function"
    CATEGORY_EQUALS = "category_equals"


@dataclass
class CategorizationRule:
    """Rule for categorizing items."""
    
    rule_id: str
    category: str
    rule_type: RuleType
    confidence: Decimal
    priority: int = 100  # Lower number = higher priority
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Rule-specific parameters
    text_pattern: Optional[str] = None
    regex_pattern: Optional[Pattern] = None
    amount_min: Optional[Decimal] = None
    amount_max: Optional[Decimal] = None
    amount_value: Optional[Decimal] = None
    required_tags: List[str] = field(default_factory=list)
    custom_function: Optional[Callable[[Any], bool]] = None
    category_value: Optional[str] = None
    
    def __post_init__(self):
        """Initialize rule-specific patterns and values."""
        if not isinstance(self.confidence, Decimal):
            self.confidence = Decimal(str(self.confidence))
        
        # Compile regex pattern if provided
        if self.rule_type == RuleType.DESCRIPTION_REGEX and self.text_pattern:
            try:
                self.regex_pattern = re.compile(self.text_pattern, re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{self.text_pattern}': {e}")
        
        # Convert amount values to Decimal
        if self.amount_min is not None and not isinstance(self.amount_min, Decimal):
            self.amount_min = Decimal(str(self.amount_min))
        if self.amount_max is not None and not isinstance(self.amount_max, Decimal):
            self.amount_max = Decimal(str(self.amount_max))
        if self.amount_value is not None and not isinstance(self.amount_value, Decimal):
            self.amount_value = Decimal(str(self.amount_value))
    
    def matches(self, item: Any) -> bool:
        """Check if item matches this rule."""
        try:
            if self.rule_type == RuleType.DESCRIPTION_CONTAINS:
                return self._check_description_contains(item)
            elif self.rule_type == RuleType.DESCRIPTION_REGEX:
                return self._check_description_regex(item)
            elif self.rule_type == RuleType.AMOUNT_RANGE:
                return self._check_amount_range(item)
            elif self.rule_type == RuleType.AMOUNT_EQUALS:
                return self._check_amount_equals(item)
            elif self.rule_type == RuleType.TAG_CONTAINS:
                return self._check_tag_contains(item)
            elif self.rule_type == RuleType.CUSTOM_FUNCTION:
                return self._check_custom_function(item)
            elif self.rule_type == RuleType.CATEGORY_EQUALS:
                return self._check_category_equals(item)
            else:
                return False
        except Exception:
            return False
    
    def _check_description_contains(self, item: Any) -> bool:
        """Check if description contains text pattern."""
        if not self.text_pattern:
            return False
        
        description = getattr(item, 'description', '') or ''
        return self.text_pattern.lower() in description.lower()
    
    def _check_description_regex(self, item: Any) -> bool:
        """Check if description matches regex pattern."""
        if not self.regex_pattern:
            return False
        
        description = getattr(item, 'description', '') or ''
        return bool(self.regex_pattern.search(description))
    
    def _check_amount_range(self, item: Any) -> bool:
        """Check if amount is within range."""
        amount = getattr(item, 'amount', None)
        if amount is None:
            return False
        
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        if self.amount_min is not None and amount < self.amount_min:
            return False
        if self.amount_max is not None and amount > self.amount_max:
            return False
        
        return True
    
    def _check_amount_equals(self, item: Any) -> bool:
        """Check if amount equals specific value."""
        if self.amount_value is None:
            return False
        
        amount = getattr(item, 'amount', None)
        if amount is None:
            return False
        
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        return amount == self.amount_value
    
    def _check_tag_contains(self, item: Any) -> bool:
        """Check if item has required tags."""
        tags = getattr(item, 'tags', []) or []
        
        if not self.required_tags:
            return len(tags) > 0
        
        return any(tag in tags for tag in self.required_tags)
    
    def _check_custom_function(self, item: Any) -> bool:
        """Check using custom function."""
        if not self.custom_function:
            return False
        
        return self.custom_function(item)
    
    def _check_category_equals(self, item: Any) -> bool:
        """Check if item category equals specific value."""
        if not self.category_value:
            return False
        
        category = getattr(item, 'category', None)
        return category == self.category_value


class CategorizationEngine:
    """Unified rule-based categorization framework."""
    
    def __init__(self):
        self.rules: List[CategorizationRule] = []
        self.cache: Dict[str, CategoryResult] = {}
        self.default_category = "uncategorized"
        self.min_confidence_threshold = Decimal('0.5')
    
    def add_rule(self, rule: CategorizationRule) -> None:
        """Add a categorization rule."""
        self.rules.append(rule)
        # Sort rules by priority (lower number = higher priority)
        self.rules.sort(key=lambda r: (r.priority, -float(r.confidence)))
        self.clear_cache()
    
    def remove_rule(self, rule_id: str) -> bool:
        """Remove a categorization rule by ID."""
        original_count = len(self.rules)
        self.rules = [rule for rule in self.rules if rule.rule_id != rule_id]
        
        if len(self.rules) != original_count:
            self.clear_cache()
            return True
        return False
    
    def get_rule(self, rule_id: str) -> Optional[CategorizationRule]:
        """Get a rule by ID."""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def categorize_item(self, item: Any) -> CategoryResult:
        """Categorize a single item."""
        # Generate cache key
        cache_key = self._generate_cache_key(item)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Find matching rules
        matching_rules = []
        for rule in self.rules:
            if rule.matches(item):
                matching_rules.append(rule)
        
        # Determine best category
        if not matching_rules:
            result = CategoryResult(
                category=self.default_category,
                confidence_score=Decimal('0.1'),
                matched_rules=[],
                alternative_categories=[]
            )
        else:
            # Use highest priority rule
            best_rule = matching_rules[0]
            
            # Create alternatives from other matching rules
            alternatives = []
            for rule in matching_rules[1:5]:  # Up to 4 alternatives
                alternatives.append({
                    'category': rule.category,
                    'confidence': rule.confidence,
                    'reason': f"Matched rule: {rule.description or rule.rule_id}"
                })
            
            result = CategoryResult(
                category=best_rule.category,
                confidence_score=best_rule.confidence,
                matched_rules=[rule.rule_id for rule in matching_rules],
                alternative_categories=alternatives
            )
        
        # Cache result
        self.cache[cache_key] = result
        return result
    
    def batch_categorize(self, items: List[Any]) -> Dict[str, CategoryResult]:
        """Categorize multiple items efficiently."""
        results = {}
        
        for item in items:
            item_id = self._get_item_id(item)
            results[item_id] = self.categorize_item(item)
        
        return results
    
    def get_confidence_score(self, item: Any, category: str) -> Decimal:
        """Get confidence score for item being in specific category."""
        result = self.categorize_item(item)
        
        if result.category == category:
            return result.confidence_score
        
        # Check alternatives
        for alt in result.alternative_categories:
            if alt['category'] == category:
                return alt['confidence']
        
        return Decimal('0')
    
    def get_categories(self) -> List[str]:
        """Get all categories from rules."""
        categories = set(rule.category for rule in self.rules)
        categories.add(self.default_category)
        return sorted(list(categories))
    
    def get_rules_for_category(self, category: str) -> List[CategorizationRule]:
        """Get all rules for a specific category."""
        return [rule for rule in self.rules if rule.category == category]
    
    def validate_rules(self) -> Dict[str, List[str]]:
        """Validate all rules and return any issues."""
        issues = {
            'errors': [],
            'warnings': []
        }
        
        rule_ids = set()
        for rule in self.rules:
            # Check for duplicate rule IDs
            if rule.rule_id in rule_ids:
                issues['errors'].append(f"Duplicate rule ID: {rule.rule_id}")
            rule_ids.add(rule.rule_id)
            
            # Check rule validity
            if rule.confidence < 0 or rule.confidence > 1:
                issues['warnings'].append(f"Rule {rule.rule_id} confidence out of range: {rule.confidence}")
            
            # Check rule-specific parameters
            if rule.rule_type == RuleType.DESCRIPTION_CONTAINS and not rule.text_pattern:
                issues['errors'].append(f"Rule {rule.rule_id} missing text_pattern for DESCRIPTION_CONTAINS")
            
            if rule.rule_type == RuleType.AMOUNT_RANGE:
                if rule.amount_min is None and rule.amount_max is None:
                    issues['errors'].append(f"Rule {rule.rule_id} missing amount range for AMOUNT_RANGE")
        
        return issues
    
    def clear_cache(self) -> None:
        """Clear categorization cache."""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'cache_size': len(self.cache),
            'total_rules': len(self.rules),
            'categories': len(self.get_categories())
        }
    
    def set_default_category(self, category: str) -> None:
        """Set default category for uncategorized items."""
        self.default_category = category
        self.clear_cache()
    
    def set_confidence_threshold(self, threshold: Decimal) -> None:
        """Set minimum confidence threshold."""
        if not isinstance(threshold, Decimal):
            threshold = Decimal(str(threshold))
        self.min_confidence_threshold = threshold
        self.clear_cache()
    
    def _generate_cache_key(self, item: Any) -> str:
        """Generate cache key for item."""
        # Create simple hash-based key
        item_str = str(item) if not hasattr(item, '__dict__') else str(vars(item))
        rules_hash = hash(tuple((r.rule_id, r.priority, str(r.confidence)) for r in self.rules))
        return f"{hash(item_str)}_{rules_hash}"
    
    def _get_item_id(self, item: Any) -> str:
        """Get unique identifier for item."""
        if hasattr(item, 'id'):
            return str(item.id)
        elif hasattr(item, '__dict__'):
            return str(hash(tuple(sorted(vars(item).items()))))
        else:
            return str(hash(str(item)))