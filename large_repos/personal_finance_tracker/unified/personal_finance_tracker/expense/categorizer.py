"""Expense categorization system for freelancers."""

import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Union
from uuid import UUID

import pandas as pd
from pydantic import BaseModel

from personal_finance_tracker.models.common import (
    ExpenseCategory,
    Transaction,
    TransactionType,
)

from personal_finance_tracker.expense.models import (
    CategorizationRule,
    MixedUseItem,
    CategorizationResult,
    ExpenseSummary,
    AuditRecord,
)


class ExpenseCategorizer:
    """
    Expense categorization system for freelancers.

    This class helps separate business and personal expenses, calculate
    business use percentages, and maintain audit-ready records.
    """

    def __init__(self):
        """Initialize the expense categorizer."""
        self.rules = []
        self.mixed_use_items = []
        self.audit_trail = []
        self._categorization_cache = {}

    def add_categorization_rule(self, rule: CategorizationRule) -> CategorizationRule:
        """
        Add a new categorization rule.

        Args:
            rule: The rule to add

        Returns:
            The added rule
        """
        # Check for duplicate rule ID
        if any(r.id == rule.id for r in self.rules):
            raise ValueError(f"Rule with ID {rule.id} already exists")

        # Add the rule
        self.rules.append(rule)

        # Sort rules by priority (highest first)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

        # Clear cache since rules have changed
        self._categorization_cache = {}

        return rule

    def update_categorization_rule(
        self, rule: CategorizationRule
    ) -> CategorizationRule:
        """
        Update an existing categorization rule.

        Args:
            rule: The rule to update

        Returns:
            The updated rule
        """
        # Find the rule to update
        for i, existing_rule in enumerate(self.rules):
            if existing_rule.id == rule.id:
                # Update the rule
                rule.updated_at = datetime.now()
                self.rules[i] = rule

                # Sort rules by priority (highest first)
                self.rules.sort(key=lambda r: r.priority, reverse=True)

                # Clear cache since rules have changed
                self._categorization_cache = {}

                return rule

        raise ValueError(f"Rule with ID {rule.id} not found")

    def remove_categorization_rule(self, rule_id: UUID) -> bool:
        """
        Remove a categorization rule.

        Args:
            rule_id: ID of the rule to remove

        Returns:
            True if the rule was removed, False otherwise
        """
        # Find the rule to remove
        for i, rule in enumerate(self.rules):
            if rule.id == rule_id:
                # Remove the rule
                del self.rules[i]

                # Clear cache since rules have changed
                self._categorization_cache = {}

                return True

        return False

    def add_mixed_use_item(self, item: MixedUseItem) -> MixedUseItem:
        """
        Add a new mixed-use item.

        Args:
            item: The mixed-use item to add

        Returns:
            The added item
        """
        # Check for duplicate item ID
        if any(i.id == item.id for i in self.mixed_use_items):
            raise ValueError(f"Mixed-use item with ID {item.id} already exists")

        # Add the item
        self.mixed_use_items.append(item)

        # Clear cache
        self._categorization_cache = {}

        return item

    def categorize_transaction(
        self, transaction: Transaction, recategorize: bool = False
    ) -> CategorizationResult:
        """
        Categorize a transaction using the defined rules.

        Args:
            transaction: The transaction to categorize
            recategorize: Whether to recategorize even if already categorized

        Returns:
            CategorizationResult with the categorization details
        """
        # Start performance timer
        start_time = time.time()

        # Skip non-expense transactions
        if transaction.transaction_type != TransactionType.EXPENSE:
            return CategorizationResult(
                transaction_id=transaction.id,
                original_transaction=transaction,
                confidence_score=0.0,
            )

        # Check cache unless forced to recategorize
        cache_key = str(transaction.id)
        if not recategorize and cache_key in self._categorization_cache:
            return self._categorization_cache[cache_key]

        # Skip if already categorized and not forced to recategorize
        if not recategorize and transaction.category is not None:
            return CategorizationResult(
                transaction_id=transaction.id,
                original_transaction=transaction,
                assigned_category=transaction.category,
                business_use_percentage=transaction.business_use_percentage,
                confidence_score=1.0,  # Already categorized, so high confidence
                notes="Transaction was already categorized",
            )

        # Check if this matches a known mixed-use item
        mixed_use_match = None
        for item in self.mixed_use_items:
            if item.name.lower() in transaction.description.lower():
                mixed_use_match = item
                break

        # Apply categorization rules
        matched_rule = None
        for rule in self.rules:
            if rule.matches(transaction):
                matched_rule = rule
                break

        # Determine category and business use percentage
        if mixed_use_match:
            category = mixed_use_match.category
            business_percentage = mixed_use_match.business_use_percentage
            is_mixed_use = True
            confidence = 0.9
            notes = f"Matched mixed-use item: {mixed_use_match.name}"
        elif matched_rule:
            category = matched_rule.category
            business_percentage = matched_rule.business_use_percentage
            is_mixed_use = business_percentage < 100 and business_percentage > 0
            confidence = 0.8
            notes = f"Matched rule: {matched_rule.name}"
        else:
            # Default to personal if no rules match
            category = ExpenseCategory.PERSONAL
            business_percentage = 0.0
            is_mixed_use = False
            confidence = 0.5
            notes = "No matching rules, defaulted to personal expense"

        # Create result
        result = CategorizationResult(
            transaction_id=transaction.id,
            original_transaction=transaction,
            matched_rule=matched_rule,
            assigned_category=category,
            business_use_percentage=business_percentage,
            confidence_score=confidence,
            is_mixed_use=is_mixed_use,
            notes=notes,
        )

        # Record audit trail
        audit_record = AuditRecord(
            transaction_id=transaction.id,
            action="categorize",
            previous_state={
                "category": transaction.category,
                "business_use_percentage": transaction.business_use_percentage,
            },
            new_state={
                "category": category,
                "business_use_percentage": business_percentage,
            },
        )
        self.audit_trail.append(audit_record)

        # Update cache
        self._categorization_cache[cache_key] = result

        # Performance metrics
        elapsed_time = time.time() - start_time

        return result

    def categorize_transactions(
        self, transactions: List[Transaction], recategorize: bool = False
    ) -> List[CategorizationResult]:
        """
        Categorize multiple transactions using the defined rules.

        Args:
            transactions: List of transactions to categorize
            recategorize: Whether to recategorize even if already categorized

        Returns:
            List of CategorizationResult objects
        """
        # Start performance timer
        start_time = time.time()

        # Categorize each transaction
        results = []
        for transaction in transactions:
            result = self.categorize_transaction(transaction, recategorize)
            results.append(result)

        # Performance metrics
        elapsed_time = time.time() - start_time

        return results

    def apply_categorization(
        self, transaction: Transaction, result: CategorizationResult
    ) -> Transaction:
        """
        Apply a categorization result to a transaction.

        Args:
            transaction: The transaction to update
            result: The categorization result to apply

        Returns:
            The updated transaction
        """
        # Record previous state for audit
        previous_state = {
            "category": transaction.category,
            "business_use_percentage": transaction.business_use_percentage,
        }

        # Apply categorization
        transaction.category = result.assigned_category
        transaction.business_use_percentage = result.business_use_percentage

        # Record audit trail
        audit_record = AuditRecord(
            transaction_id=transaction.id,
            action="apply_categorization",
            previous_state=previous_state,
            new_state={
                "category": transaction.category,
                "business_use_percentage": transaction.business_use_percentage,
            },
        )
        self.audit_trail.append(audit_record)

        return transaction

    def generate_expense_summary(
        self, transactions: List[Transaction], start_date: datetime, end_date: datetime
    ) -> ExpenseSummary:
        """
        Generate a summary of expenses by category.

        Args:
            transactions: List of transactions
            start_date: Start date for the summary period
            end_date: End date for the summary period

        Returns:
            ExpenseSummary object with expense totals by category
        """
        # Filter to expenses in the date range
        expenses = [
            t
            for t in transactions
            if (
                t.transaction_type == TransactionType.EXPENSE
                and start_date <= t.date <= end_date
            )
        ]

        # Categorize any uncategorized expenses
        for expense in expenses:
            if expense.category is None:
                result = self.categorize_transaction(expense)
                self.apply_categorization(expense, result)

        # Calculate totals
        total_expenses = sum(t.amount for t in expenses)
        business_expenses = sum(
            t.amount * (t.business_use_percentage / 100)
            for t in expenses
            if t.category != ExpenseCategory.PERSONAL
            and t.business_use_percentage is not None
        )
        personal_expenses = total_expenses - business_expenses

        # Calculate expenses by category
        by_category = {}
        for expense in expenses:
            category = expense.category or ExpenseCategory.OTHER
            amount = expense.amount

            # For business expenses, apply the business use percentage
            if (
                category != ExpenseCategory.PERSONAL
                and expense.business_use_percentage is not None
            ):
                amount_business = amount * (expense.business_use_percentage / 100)

                # Add to business category
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += amount_business

                # Add personal portion to personal category
                amount_personal = amount - amount_business
                if amount_personal > 0:
                    if ExpenseCategory.PERSONAL not in by_category:
                        by_category[ExpenseCategory.PERSONAL] = 0
                    by_category[ExpenseCategory.PERSONAL] += amount_personal
            else:
                # Personal expense
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += amount

        # Create summary
        summary = ExpenseSummary(
            period_start=start_date,
            period_end=end_date,
            total_expenses=total_expenses,
            business_expenses=business_expenses,
            personal_expenses=personal_expenses,
            by_category=by_category,
        )

        return summary

    def get_audit_trail(
        self, transaction_id: Optional[UUID] = None, limit: int = 100
    ) -> List[AuditRecord]:
        """
        Get the audit trail for transactions.

        Args:
            transaction_id: Optional transaction ID to filter by
            limit: Maximum number of records to return

        Returns:
            List of audit records
        """
        if transaction_id:
            # Filter to specific transaction
            filtered_trail = [
                record
                for record in self.audit_trail
                if record.transaction_id == transaction_id
            ]
        else:
            filtered_trail = self.audit_trail

        # Sort by timestamp (newest first) and limit
        sorted_trail = sorted(filtered_trail, key=lambda r: r.timestamp, reverse=True)

        return sorted_trail[:limit]

    def attach_receipt(
        self, transaction: Transaction, receipt_path: str
    ) -> Transaction:
        """
        Attach a receipt to a transaction.

        Args:
            transaction: The transaction to update
            receipt_path: Path to the receipt file

        Returns:
            The updated transaction
        """
        # Record previous state for audit
        previous_state = {"receipt_path": transaction.receipt_path}

        # Update receipt path
        transaction.receipt_path = receipt_path

        # Record audit trail
        audit_record = AuditRecord(
            transaction_id=transaction.id,
            action="attach_receipt",
            previous_state=previous_state,
            new_state={"receipt_path": receipt_path},
        )
        self.audit_trail.append(audit_record)

        return transaction

    def correct_categorization(
        self,
        transaction: Transaction,
        new_category: ExpenseCategory,
        new_business_percentage: float,
    ) -> Transaction:
        """
        Correct the categorization of a transaction.

        Args:
            transaction: The transaction to update
            new_category: The correct category
            new_business_percentage: The correct business use percentage

        Returns:
            The updated transaction
        """
        # Record previous state for audit
        previous_state = {
            "category": transaction.category,
            "business_use_percentage": transaction.business_use_percentage,
        }

        # Update transaction
        transaction.category = new_category
        transaction.business_use_percentage = new_business_percentage

        # Record audit trail
        audit_record = AuditRecord(
            transaction_id=transaction.id,
            action="correct_categorization",
            previous_state=previous_state,
            new_state={
                "category": new_category,
                "business_use_percentage": new_business_percentage,
            },
            notes="Manual correction of categorization",
        )
        self.audit_trail.append(audit_record)

        # Clear cache for this transaction
        cache_key = str(transaction.id)
        if cache_key in self._categorization_cache:
            del self._categorization_cache[cache_key]

        return transaction
