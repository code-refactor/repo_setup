"""Migrated expense categorization system using common library."""

import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Union
from uuid import uuid4
from decimal import Decimal

# Import common library components
from common.core.engines.categorization_engine import CategorizationEngine, CategorizationRule, RuleType
from common.core.models.analysis_results import CategoryResult, AnalysisResult
from common.core.engines.analysis_engine import AnalysisEngine
from common.core.models.base_transaction import BaseTransaction


class FreelancerExpenseCategorizer(CategorizationEngine):
    """
    Freelancer-specific expense categorizer extending common categorization engine.
    
    Handles business vs personal expense separation, mixed-use items,
    and freelancer-specific categorization rules.
    """
    
    def __init__(self):
        """Initialize the freelancer expense categorizer."""
        super().__init__()
        self.mixed_use_items = []
        self.audit_trail = []
        self.default_business_categories = [
            "business_supplies", "software", "marketing", "office_rent",
            "utilities", "travel", "equipment", "professional_development",
            "professional_services", "health_insurance", "phone", "internet"
        ]
        
        # Set freelancer-specific default category
        self.set_default_category("personal")
        
        # Initialize with default rules
        self._add_default_rules()
    
    def add_business_rule(self, 
                         category: str,
                         business_percentage: float,
                         description_patterns: List[str],
                         amount_min: Optional[float] = None,
                         amount_max: Optional[float] = None,
                         priority: int = 100) -> str:
        """
        Add a business expense categorization rule.
        
        Args:
            category: The expense category to assign
            business_percentage: Percentage of business use (0-100)
            description_patterns: Text patterns to match in description
            amount_min: Minimum amount to match (optional)
            amount_max: Maximum amount to match (optional)
            priority: Rule priority (lower = higher priority)
            
        Returns:
            Rule ID for the created rule
        """
        if business_percentage < 0 or business_percentage > 100:
            raise ValueError("Business percentage must be between 0 and 100")
        
        rule_id = str(uuid4())
        
        # Create regex rule for description matching with multiple patterns
        rule = CategorizationRule(
            rule_id=rule_id,
            category=category,
            rule_type=RuleType.DESCRIPTION_REGEX,
            confidence=Decimal('0.85'),
            priority=priority,
            text_pattern='(' + '|'.join(description_patterns) + ')',
            metadata={
                'business_use_percentage': business_percentage,
                'rule_type': 'business_expense',
                'is_mixed_use': business_percentage < 100
            }
        )
        
        # Add amount constraints if specified
        if amount_min is not None:
            rule.amount_min = Decimal(str(amount_min))
        if amount_max is not None:
            rule.amount_max = Decimal(str(amount_max))
            rule.rule_type = RuleType.AMOUNT_RANGE
        
        self.add_rule(rule)
        return rule_id
    
    def categorize_expense(self, transaction: BaseTransaction) -> CategoryResult:
        """
        Categorize an expense transaction with business use calculation.
        
        Args:
            transaction: The transaction to categorize
            
        Returns:
            CategoryResult with business use metadata
        """
        # Use parent categorization
        result = self.categorize_item(transaction)
        
        # Add business use percentage to result metadata
        matched_rule = None
        if result.matched_rules:
            rule_id = result.matched_rules[0]
            matched_rule = self.get_rule(rule_id)
        
        if matched_rule and 'business_use_percentage' in matched_rule.metadata:
            business_percentage = matched_rule.metadata['business_use_percentage']
            result.metadata['business_use_percentage'] = business_percentage
            result.metadata['business_amount'] = float(transaction.amount) * (business_percentage / 100)
            result.metadata['personal_amount'] = float(transaction.amount) * ((100 - business_percentage) / 100)
            
            # Track mixed-use items
            if business_percentage > 0 and business_percentage < 100:
                self._add_mixed_use_item(transaction, business_percentage, result.category)
        else:
            # Default to personal expense
            result.metadata['business_use_percentage'] = 0.0
            result.metadata['business_amount'] = 0.0
            result.metadata['personal_amount'] = float(transaction.amount)
        
        # Record audit trail
        self._record_audit_entry(transaction, result)
        
        return result
    
    def batch_categorize_expenses(self, transactions: List[BaseTransaction]) -> Dict[str, CategoryResult]:
        """
        Categorize multiple expense transactions efficiently.
        
        Args:
            transactions: List of transactions to categorize
            
        Returns:
            Dictionary mapping transaction IDs to categorization results
        """
        results = {}
        
        for transaction in transactions:
            if transaction.is_expense():
                result = self.categorize_expense(transaction)
                results[transaction.id] = result
        
        return results
    
    def get_business_expense_summary(self, transactions: List[BaseTransaction], 
                                   start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> Dict[str, float]:
        """
        Generate summary of business expenses by category.
        
        Args:
            transactions: List of transactions to analyze
            start_date: Start date filter (optional)
            end_date: End date filter (optional)
            
        Returns:
            Dictionary with business expense totals by category
        """
        # Filter transactions by date if specified
        filtered_transactions = transactions
        if start_date or end_date:
            filtered_transactions = []
            for t in transactions:
                if start_date and t.date < start_date:
                    continue
                if end_date and t.date > end_date:
                    continue
                filtered_transactions.append(t)
        
        # Categorize and summarize
        results = self.batch_categorize_expenses(filtered_transactions)
        summary = {}
        
        for transaction_id, result in results.items():
            category = result.category
            business_amount = result.metadata.get('business_amount', 0.0)
            
            if category not in summary:
                summary[category] = 0.0
            summary[category] += business_amount
        
        return summary
    
    def get_mixed_use_items(self) -> List[Dict]:
        """Get list of items with mixed business/personal use."""
        return self.mixed_use_items.copy()
    
    def get_audit_trail(self) -> List[Dict]:
        """Get categorization audit trail."""
        return self.audit_trail.copy()
    
    def export_rules_for_tax_prep(self) -> List[Dict]:
        """Export categorization rules in format suitable for tax preparation."""
        exported_rules = []
        
        for rule in self.rules:
            if rule.metadata.get('rule_type') == 'business_expense':
                exported_rules.append({
                    'rule_id': rule.rule_id,
                    'category': rule.category,
                    'business_use_percentage': rule.metadata.get('business_use_percentage', 0),
                    'description_pattern': rule.text_pattern,
                    'confidence': float(rule.confidence),
                    'priority': rule.priority
                })
        
        return exported_rules
    
    def _add_default_rules(self):
        """Add default categorization rules for common freelancer expenses."""
        
        # Software and subscriptions - typically 100% business
        self.add_business_rule(
            category="software",
            business_percentage=100.0,
            description_patterns=["adobe", "github", "slack", "zoom", "office 365", "microsoft", "google workspace"],
            priority=10
        )
        
        # Marketing expenses - 100% business
        self.add_business_rule(
            category="marketing",
            business_percentage=100.0,
            description_patterns=["facebook ads", "google ads", "linkedin", "twitter", "marketing"],
            priority=10
        )
        
        # Office supplies - typically 100% business
        self.add_business_rule(
            category="business_supplies",
            business_percentage=100.0,
            description_patterns=["staples", "office depot", "amazon business", "printer", "paper", "pens"],
            priority=20
        )
        
        # Internet and phone - often mixed use
        self.add_business_rule(
            category="internet",
            business_percentage=75.0,  # Default 75% business use
            description_patterns=["comcast", "verizon", "at&t", "internet", "wifi"],
            priority=30
        )
        
        self.add_business_rule(
            category="phone",
            business_percentage=60.0,  # Default 60% business use
            description_patterns=["verizon wireless", "t-mobile", "att wireless", "phone bill"],
            priority=30
        )
        
        # Travel expenses - typically 100% business when work-related
        self.add_business_rule(
            category="travel",
            business_percentage=100.0,
            description_patterns=["uber", "lyft", "taxi", "airline", "hotel", "airbnb", "expedia"],
            priority=25
        )
        
        # Professional development - 100% business
        self.add_business_rule(
            category="professional_development",
            business_percentage=100.0,
            description_patterns=["udemy", "coursera", "skillshare", "conference", "training", "certification"],
            priority=15
        )
        
        # Equipment - typically 100% business
        self.add_business_rule(
            category="equipment",
            business_percentage=100.0,
            description_patterns=["laptop", "computer", "monitor", "keyboard", "mouse", "desk", "chair"],
            priority=20
        )
    
    def _add_mixed_use_item(self, transaction: BaseTransaction, business_percentage: float, category: str):
        """Record a mixed-use item for audit purposes."""
        item = {
            'transaction_id': transaction.id,
            'date': transaction.date.isoformat(),
            'amount': float(transaction.amount),
            'description': transaction.description,
            'category': category,
            'business_percentage': business_percentage,
            'business_amount': float(transaction.amount) * (business_percentage / 100),
            'personal_amount': float(transaction.amount) * ((100 - business_percentage) / 100)
        }
        self.mixed_use_items.append(item)
    
    def _record_audit_entry(self, transaction: BaseTransaction, result: CategoryResult):
        """Record categorization in audit trail."""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'transaction_id': transaction.id,
            'transaction_date': transaction.date.isoformat(),
            'amount': float(transaction.amount),
            'description': transaction.description,
            'assigned_category': result.category,
            'confidence_score': float(result.confidence_score),
            'business_use_percentage': result.metadata.get('business_use_percentage', 0.0),
            'matched_rules': result.matched_rules
        }
        self.audit_trail.append(audit_entry)


class FreelancerExpenseAnalyzer(AnalysisEngine):
    """
    High-level expense analysis engine for freelancers.
    
    Provides comprehensive expense analysis including categorization,
    business use calculations, and tax-ready summaries.
    """
    
    def __init__(self):
        """Initialize the expense analyzer."""
        super().__init__(enable_caching=True, enable_performance_tracking=True)
        self.categorizer = FreelancerExpenseCategorizer()
    
    def analyze(self, transactions: List[BaseTransaction]) -> AnalysisResult:
        """
        Analyze expense transactions for freelancer tax purposes.
        
        Args:
            transactions: List of transactions to analyze
            
        Returns:
            AnalysisResult with expense categorization and business use analysis
        """
        with self.measure_performance("expense_analysis"):
            start_time = time.time()
            
            # Filter to expense transactions only
            expense_transactions = [t for t in transactions if t.is_expense()]
            
            # Categorize all expenses
            categorization_results = self.categorizer.batch_categorize_expenses(expense_transactions)
            
            # Calculate summary statistics
            total_expenses = sum(float(t.amount) for t in expense_transactions)
            total_business_expenses = sum(
                result.metadata.get('business_amount', 0.0) 
                for result in categorization_results.values()
            )
            total_personal_expenses = total_expenses - total_business_expenses
            
            # Calculate business use percentage
            business_use_percentage = (total_business_expenses / total_expenses * 100) if total_expenses > 0 else 0
            
            # Generate category breakdown
            category_breakdown = {}
            for result in categorization_results.values():
                category = result.category
                business_amount = result.metadata.get('business_amount', 0.0)
                
                if category not in category_breakdown:
                    category_breakdown[category] = {
                        'total_amount': 0.0,
                        'business_amount': 0.0,
                        'transaction_count': 0
                    }
                
                category_breakdown[category]['business_amount'] += business_amount
                category_breakdown[category]['transaction_count'] += 1
            
            # Create analysis result
            processing_time = (time.time() - start_time) * 1000
            
            result = AnalysisResult(
                analysis_type="freelancer_expense_analysis",
                calculation_date=datetime.now(),
                processing_time_ms=processing_time,
                confidence_score=Decimal('0.9'),
                metadata={
                    'total_transactions': len(expense_transactions),
                    'total_expenses': total_expenses,
                    'total_business_expenses': total_business_expenses,
                    'total_personal_expenses': total_personal_expenses,
                    'business_use_percentage': business_use_percentage,
                    'category_breakdown': category_breakdown,
                    'mixed_use_items_count': len(self.categorizer.get_mixed_use_items()),
                    'categorization_results': {
                        tid: {
                            'category': result.category,
                            'confidence': float(result.confidence_score),
                            'business_amount': result.metadata.get('business_amount', 0.0)
                        } for tid, result in categorization_results.items()
                    }
                }
            )
            
            return result
    
    def get_tax_deduction_summary(self, transactions: List[BaseTransaction], 
                                 tax_year: int) -> Dict[str, float]:
        """
        Generate tax deduction summary for a specific year.
        
        Args:
            transactions: List of transactions
            tax_year: Tax year to analyze
            
        Returns:
            Dictionary with deductible amounts by category
        """
        # Filter transactions by tax year
        year_transactions = [
            t for t in transactions 
            if t.date.year == tax_year and t.is_expense()
        ]
        
        # Get business expense summary
        return self.categorizer.get_business_expense_summary(year_transactions)
    
    def add_categorization_rule(self, category: str, business_percentage: float, 
                               patterns: List[str], **kwargs) -> str:
        """Add a new categorization rule."""
        return self.categorizer.add_business_rule(
            category=category,
            business_percentage=business_percentage,
            description_patterns=patterns,
            **kwargs
        )
    
    def get_categorizer(self) -> FreelancerExpenseCategorizer:
        """Get the underlying categorizer for advanced operations."""
        return self.categorizer