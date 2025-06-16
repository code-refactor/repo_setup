"""
Unified policy engine for rule evaluation and enforcement.

This module provides a flexible policy evaluation framework that can be
extended by domain-specific implementations to handle business rules,
access control, and compliance requirements.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Union

from .models import PolicyDecision, UserContext, BaseQuery, QueryResult


class PolicyAction(str, Enum):
    """Types of policy enforcement actions."""
    ALLOW = "allow"
    DENY = "deny"
    MODIFY = "modify"
    LOG = "log"
    REVIEW = "review"


class RuleType(str, Enum):
    """Types of policy rules."""
    ACCESS_CONTROL = "access_control"
    DATA_CLASSIFICATION = "data_classification"
    TEMPORAL = "temporal"
    CONTENT_FILTER = "content_filter"
    USAGE_LIMIT = "usage_limit"
    COMPLIANCE = "compliance"


@dataclass
class PolicyRule:
    """Definition of a policy rule."""
    rule_id: str
    name: str
    rule_type: RuleType
    priority: int = 100  # Lower number = higher priority
    enabled: bool = True
    
    # Rule conditions
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Actions to take when rule matches
    action: PolicyAction = PolicyAction.ALLOW
    modifications: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    description: str = ""
    tags: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: Optional[datetime] = None
    
    # Rule-specific configuration
    config: Dict[str, Any] = field(default_factory=dict)


class RuleEvaluator(ABC):
    """Abstract base class for rule evaluators."""
    
    @abstractmethod
    def evaluate_rule(self, rule: PolicyRule, context: Dict[str, Any]) -> bool:
        """
        Evaluate if a rule matches the given context.
        
        Args:
            rule: Policy rule to evaluate
            context: Evaluation context
            
        Returns:
            True if rule matches, False otherwise
        """
        pass


class DefaultRuleEvaluator(RuleEvaluator):
    """Default rule evaluator implementation."""
    
    def evaluate_rule(self, rule: PolicyRule, context: Dict[str, Any]) -> bool:
        """Evaluate rule conditions against context."""
        if not rule.enabled:
            return False
        
        # All conditions must match (AND logic)
        for condition in rule.conditions:
            if not self._evaluate_condition(condition, context):
                return False
        
        return True
    
    def _evaluate_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate a single condition."""
        condition_type = condition.get('type', '')
        
        if condition_type == 'user_role':
            return self._evaluate_user_role(condition, context)
        elif condition_type == 'time_range':
            return self._evaluate_time_range(condition, context)
        elif condition_type == 'resource_pattern':
            return self._evaluate_resource_pattern(condition, context)
        elif condition_type == 'field_pattern':
            return self._evaluate_field_pattern(condition, context)
        elif condition_type == 'usage_limit':
            return self._evaluate_usage_limit(condition, context)
        elif condition_type == 'data_classification':
            return self._evaluate_data_classification(condition, context)
        else:
            # Generic condition evaluation
            return self._evaluate_generic_condition(condition, context)
    
    def _evaluate_user_role(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate user role condition."""
        required_roles = set(condition.get('roles', []))
        user_context = context.get('user_context')
        
        if not user_context or not hasattr(user_context, 'role'):
            return False
        
        if not required_roles:
            return True
        
        # Check if user has any of the required roles
        user_role = user_context.role
        return user_role in required_roles
    
    def _evaluate_time_range(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate time-based condition."""
        start_time = condition.get('start_time')
        end_time = condition.get('end_time')
        days_of_week = condition.get('days_of_week', [])
        
        now = datetime.now()
        current_time = now.time()
        current_day = now.weekday()  # 0 = Monday
        
        # Check time range
        if start_time and end_time:
            start = time.fromisoformat(start_time) if isinstance(start_time, str) else start_time
            end = time.fromisoformat(end_time) if isinstance(end_time, str) else end_time
            
            if not (start <= current_time <= end):
                return False
        
        # Check days of week
        if days_of_week and current_day not in days_of_week:
            return False
        
        return True
    
    def _evaluate_resource_pattern(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate resource pattern matching."""
        patterns = condition.get('patterns', [])
        query = context.get('query')
        
        if not query or not patterns:
            return False
        
        # Check table patterns
        if hasattr(query, 'tables'):
            tables = query.tables
            for pattern in patterns:
                for table in tables:
                    if re.search(pattern, table, re.IGNORECASE):
                        return True
        
        return False
    
    def _evaluate_field_pattern(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate field pattern matching."""
        patterns = condition.get('patterns', [])
        query = context.get('query')
        
        if not query or not patterns:
            return False
        
        # Check field patterns
        if hasattr(query, 'fields'):
            fields = query.fields
            for pattern in patterns:
                for field in fields:
                    if re.search(pattern, field, re.IGNORECASE):
                        return True
        
        return False
    
    def _evaluate_usage_limit(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate usage limit condition."""
        limit = condition.get('limit', 0)
        period = condition.get('period', 'daily')  # daily, hourly, weekly
        
        # This would need to be implemented with actual usage tracking
        # For now, return True (no limit exceeded)
        return True
    
    def _evaluate_data_classification(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate data classification condition."""
        required_levels = set(condition.get('classification_levels', []))
        
        # This would need integration with data classification system
        # For now, return True
        return True
    
    def _evaluate_generic_condition(self, condition: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Evaluate generic condition using field and operator."""
        field = condition.get('field')
        operator = condition.get('operator', 'equals')
        value = condition.get('value')
        
        if not field:
            return False
        
        # Navigate to field in context
        context_value = self._get_nested_value(context, field)
        
        if context_value is None:
            return False
        
        # Apply operator
        if operator == 'equals':
            return context_value == value
        elif operator == 'not_equals':
            return context_value != value
        elif operator == 'contains':
            return value in str(context_value)
        elif operator == 'matches':
            return re.search(str(value), str(context_value), re.IGNORECASE) is not None
        elif operator == 'greater_than':
            return float(context_value) > float(value)
        elif operator == 'less_than':
            return float(context_value) < float(value)
        elif operator == 'in':
            return context_value in value if isinstance(value, (list, set)) else False
        
        return False
    
    def _get_nested_value(self, obj: Dict[str, Any], field_path: str) -> Any:
        """Get nested value from object using dot notation."""
        parts = field_path.split('.')
        current = obj
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None
        
        return current


class PolicyEngine:
    """Main policy engine for rule evaluation and enforcement."""
    
    def __init__(self, evaluator: Optional[RuleEvaluator] = None):
        self.evaluator = evaluator or DefaultRuleEvaluator()
        self.rules: Dict[str, PolicyRule] = {}
        self.rule_cache: Dict[str, List[PolicyRule]] = {}
    
    def add_rule(self, rule: PolicyRule):
        """Add a policy rule to the engine."""
        self.rules[rule.rule_id] = rule
        self._clear_cache()
    
    def remove_rule(self, rule_id: str):
        """Remove a policy rule from the engine."""
        if rule_id in self.rules:
            del self.rules[rule_id]
            self._clear_cache()
    
    def get_rule(self, rule_id: str) -> Optional[PolicyRule]:
        """Get a specific rule by ID."""
        return self.rules.get(rule_id)
    
    def list_rules(self, rule_type: Optional[RuleType] = None, 
                   enabled_only: bool = True) -> List[PolicyRule]:
        """List rules, optionally filtered by type and enabled status."""
        rules = []
        
        for rule in self.rules.values():
            if enabled_only and not rule.enabled:
                continue
            if rule_type and rule.rule_type != rule_type:
                continue
            rules.append(rule)
        
        # Sort by priority (lower number = higher priority)
        rules.sort(key=lambda r: r.priority)
        return rules
    
    def evaluate_query(self, query: BaseQuery, user_context: UserContext,
                      **additional_context) -> PolicyDecision:
        """
        Evaluate a query against all applicable policies.
        
        Args:
            query: Query to evaluate
            user_context: User context for the query
            **additional_context: Additional context for evaluation
            
        Returns:
            PolicyDecision with enforcement actions
        """
        context = {
            'query': query,
            'user_context': user_context,
            **additional_context
        }
        
        decision = PolicyDecision(
            user_context=user_context,
            query_context=query,
            resource=f"tables:{','.join(query.tables)}"
        )
        
        # Get applicable rules
        applicable_rules = self._get_applicable_rules(context)
        
        # Evaluate each rule
        for rule in applicable_rules:
            if self.evaluator.evaluate_rule(rule, context):
                decision.matched_rules.append(rule.rule_id)
                decision.applied_policies.append(rule.name)
                
                # Apply rule action
                self._apply_rule_action(rule, decision, context)
        
        # Set final decision
        if not decision.matched_rules:
            decision.allowed = True
            decision.action = PolicyAction.ALLOW
            decision.reason = "No restricting policies matched"
        
        return decision
    
    def _get_applicable_rules(self, context: Dict[str, Any]) -> List[PolicyRule]:
        """Get rules applicable to the current context."""
        # For now, return all enabled rules sorted by priority
        return self.list_rules(enabled_only=True)
    
    def _apply_rule_action(self, rule: PolicyRule, decision: PolicyDecision,
                          context: Dict[str, Any]):
        """Apply a rule's action to the policy decision."""
        if rule.action == PolicyAction.DENY:
            decision.allowed = False
            decision.action = PolicyAction.DENY
            decision.reason = rule.description or f"Denied by rule: {rule.name}"
            decision.confidence = 1.0
        
        elif rule.action == PolicyAction.MODIFY:
            decision.allowed = True
            decision.action = PolicyAction.MODIFY
            decision.modifications.update(rule.modifications)
            decision.reason = f"Modified by rule: {rule.name}"
        
        elif rule.action == PolicyAction.LOG:
            decision.logging_required = True
            if not decision.action:  # Don't override DENY or MODIFY
                decision.action = PolicyAction.LOG
        
        elif rule.action == PolicyAction.REVIEW:
            decision.allowed = False
            decision.action = PolicyAction.REVIEW
            decision.reason = f"Requires review due to rule: {rule.name}"
    
    def _clear_cache(self):
        """Clear rule cache."""
        self.rule_cache.clear()


class ContextManager:
    """Manage evaluation context for policy decisions."""
    
    def __init__(self):
        self.context_enhancers: List[Callable[[Dict[str, Any]], Dict[str, Any]]] = []
    
    def add_context_enhancer(self, enhancer: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """Add a context enhancer function."""
        self.context_enhancers.append(enhancer)
    
    def enhance_context(self, base_context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance context with additional information."""
        enhanced_context = base_context.copy()
        
        for enhancer in self.context_enhancers:
            try:
                enhanced_context = enhancer(enhanced_context)
            except Exception:
                # Skip failed enhancers
                continue
        
        return enhanced_context
    
    def create_query_context(self, query: BaseQuery, user_context: UserContext,
                           **kwargs) -> Dict[str, Any]:
        """Create a comprehensive query evaluation context."""
        base_context = {
            'query': query,
            'user_context': user_context,
            'timestamp': datetime.now(),
            'tables': query.tables,
            'fields': query.fields,
            'user_id': user_context.user_id,
            'user_role': user_context.role,
            'user_permissions': user_context.permissions,
            **kwargs
        }
        
        return self.enhance_context(base_context)


class ActionDispatcher:
    """Dispatch policy enforcement actions."""
    
    def __init__(self):
        self.action_handlers: Dict[PolicyAction, Callable[[PolicyDecision, Dict[str, Any]], Any]] = {}
    
    def register_handler(self, action: PolicyAction, 
                        handler: Callable[[PolicyDecision, Dict[str, Any]], Any]):
        """Register an action handler."""
        self.action_handlers[action] = handler
    
    def dispatch(self, decision: PolicyDecision, context: Dict[str, Any]) -> Any:
        """Dispatch a policy decision for enforcement."""
        if decision.action in self.action_handlers:
            return self.action_handlers[decision.action](decision, context)
        
        # Default handling
        if decision.action == PolicyAction.DENY:
            raise PermissionError(decision.reason)
        elif decision.action == PolicyAction.REVIEW:
            raise PermissionError(f"Manual review required: {decision.reason}")
        
        return None  # Allow by default