"""Migrated tax management engine for freelancers using common library."""

import calendar
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Union

import pandas as pd
from pydantic import BaseModel

# Import common library components
from common.core.engines.analysis_engine import AnalysisEngine
from common.core.models.analysis_results import AnalysisResult
from common.core.models.base_transaction import BaseTransaction, TransactionType
from common.core.utils.financial_calculations import FinancialCalculations
from common.core.utils.date_helpers import DateHelpers

# Import persona-specific models
from personal_finance_tracker.models.common import (
    TaxPayment,
    TaxRate,
    TaxDeduction,
)

from personal_finance_tracker.tax.models import (
    FilingStatus,
    TaxJurisdiction,
    QuarterInfo,
    TaxBracket,
    TaxLiability,
    EstimatedPayment,
    TaxYearSummary,
)


class FreelancerTaxManager(AnalysisEngine):
    """
    Freelancer-specific tax management engine extending common analysis engine.
    
    Handles tax calculations, estimated payment scheduling,
    and tax optimization for freelancers.
    """

    def __init__(self, filing_status: FilingStatus = FilingStatus.SINGLE):
        """
        Initialize the tax manager.

        Args:
            filing_status: Tax filing status
        """
        super().__init__(enable_caching=True, enable_performance_tracking=True)
        
        self.filing_status = filing_status
        self._tax_brackets = {}  # Cache for tax brackets
        self._se_tax_rate = 15.3  # Self-employment tax rate (percentage)
        self._se_tax_income_limit = 147000  # For 2022 (Social Security wage base)
        self._standard_deduction = {
            2022: {
                FilingStatus.SINGLE: 12950,
                FilingStatus.MARRIED_JOINT: 25900,
                FilingStatus.MARRIED_SEPARATE: 12950,
                FilingStatus.HEAD_OF_HOUSEHOLD: 19400,
            }
        }
        
        # Load default tax brackets
        self.load_default_brackets()

    def analyze(self, data: Union[List[BaseTransaction], Dict]) -> AnalysisResult:
        """
        Analyze tax obligations for given data.
        
        Args:
            data: Transaction list or tax calculation parameters
            
        Returns:
            AnalysisResult with tax liability information
        """
        with self.measure_performance("tax_analysis"):
            if isinstance(data, list):
                # Transaction-based analysis
                tax_year = datetime.now().year
                liability = self.calculate_tax_liability(transactions=data, tax_year=tax_year)
            elif isinstance(data, dict):
                # Parameter-based analysis
                liability = self.calculate_tax_liability(**data)
            else:
                raise ValueError("Data must be transaction list or parameter dict")
            
            return AnalysisResult(
                analysis_type="tax_liability",
                calculation_date=datetime.now(),
                processing_time_ms=self.get_performance_stats().get("tax_analysis", {}).get("avg_duration_ms", 0),
                confidence_score=1.0,  # Tax calculations are deterministic
                metadata={
                    "liability": liability.__dict__,
                    "filing_status": self.filing_status.value,
                    "analysis_engine": "FreelancerTaxManager"
                }
            )

    def set_tax_brackets(self, brackets: List[TaxBracket]) -> None:
        """
        Set tax brackets for calculations.

        Args:
            brackets: List of tax brackets
        """
        # Index brackets by jurisdiction, year, and filing status
        for bracket in brackets:
            key = (bracket.jurisdiction, bracket.tax_year, bracket.filing_status)
            self._tax_brackets[key] = bracket
        
        # Clear cache when brackets change
        self.clear_cache()

    def get_tax_brackets(
        self,
        jurisdiction: TaxJurisdiction,
        tax_year: int,
        filing_status: Optional[FilingStatus] = None,
    ) -> Optional[TaxBracket]:
        """
        Get tax brackets for a specific jurisdiction and year.

        Args:
            jurisdiction: Tax jurisdiction
            tax_year: Tax year
            filing_status: Filing status (defaults to instance filing status)

        Returns:
            Tax bracket if found, None otherwise
        """
        status = filing_status or self.filing_status
        key = (jurisdiction, tax_year, status)
        return self._tax_brackets.get(key)

    def load_default_brackets(self) -> None:
        """Load default tax brackets for common jurisdictions."""
        # 2022 federal tax brackets (simplified example)
        federal_single = TaxBracket(
            jurisdiction=TaxJurisdiction.FEDERAL,
            filing_status=FilingStatus.SINGLE,
            tax_year=2022,
            income_thresholds=[0, 10275, 41775, 89075, 170050, 215950, 539900],
            rates=[10, 12, 22, 24, 32, 35, 37],
        )

        federal_married_joint = TaxBracket(
            jurisdiction=TaxJurisdiction.FEDERAL,
            filing_status=FilingStatus.MARRIED_JOINT,
            tax_year=2022,
            income_thresholds=[0, 20550, 83550, 178150, 340100, 431900, 647850],
            rates=[10, 12, 22, 24, 32, 35, 37],
        )

        self.set_tax_brackets([federal_single, federal_married_joint])

    def calculate_tax_quarters(self, tax_year: int) -> List[QuarterInfo]:
        """
        Calculate tax quarter information for a specific year.

        Args:
            tax_year: Tax year

        Returns:
            List of tax quarter information
        """
        quarters = []

        # Use DateHelpers for quarter calculations
        q1_start, q1_end = DateHelpers.get_quarter_dates(datetime(tax_year, 1, 15))
        q2_start, q2_end = DateHelpers.get_quarter_dates(datetime(tax_year, 4, 15))
        q3_start, q3_end = DateHelpers.get_quarter_dates(datetime(tax_year, 7, 15))
        q4_start, q4_end = DateHelpers.get_quarter_dates(datetime(tax_year, 10, 15))

        # Tax-specific due dates
        quarters = [
            QuarterInfo(
                year=tax_year,
                quarter=1,
                start_date=datetime(tax_year, 1, 1),
                end_date=datetime(tax_year, 3, 31),
                due_date=datetime(tax_year, 4, 15),
                description=f"Q1 {tax_year} (Jan-Mar)",
            ),
            QuarterInfo(
                year=tax_year,
                quarter=2,
                start_date=datetime(tax_year, 4, 1),
                end_date=datetime(tax_year, 5, 31),
                due_date=datetime(tax_year, 6, 15),
                description=f"Q2 {tax_year} (Apr-May)",
            ),
            QuarterInfo(
                year=tax_year,
                quarter=3,
                start_date=datetime(tax_year, 6, 1),
                end_date=datetime(tax_year, 8, 31),
                due_date=datetime(tax_year, 9, 15),
                description=f"Q3 {tax_year} (Jun-Aug)",
            ),
            QuarterInfo(
                year=tax_year,
                quarter=4,
                start_date=datetime(tax_year, 9, 1),
                end_date=datetime(tax_year, 12, 31),
                due_date=datetime(tax_year + 1, 1, 15),
                description=f"Q4 {tax_year} (Sep-Dec)",
            ),
        ]

        return quarters

    def get_current_quarter(self) -> QuarterInfo:
        """
        Get the current tax quarter information.

        Returns:
            Information about the current tax quarter
        """
        today = datetime.now()
        year = today.year

        quarters = self.calculate_tax_quarters(year)

        # Find the current quarter
        for quarter in quarters:
            if quarter.start_date <= today <= quarter.end_date:
                return quarter

        # If not found (shouldn't happen), return the last quarter of the year
        return quarters[-1]

    def calculate_taxable_income(
        self,
        transactions: List[BaseTransaction],
        tax_year: int,
        deductions: List[TaxDeduction] = None,
    ) -> Tuple[float, float, float]:
        """
        Calculate taxable income for a tax year.

        Args:
            transactions: List of all transactions (BaseTransaction format)
            tax_year: Tax year to calculate for
            deductions: List of tax deductions

        Returns:
            Tuple of (total income, total deductions, taxable income)
        """
        # Filter transactions to the tax year using DateHelpers
        year_start = datetime(tax_year, 1, 1)
        year_end = datetime(tax_year, 12, 31, 23, 59, 59)

        year_transactions = [
            t for t in transactions if year_start <= t.date <= year_end
        ]

        # Calculate total income
        income_transactions = [
            t for t in year_transactions if t.is_income()
        ]
        total_income = float(sum(t.amount for t in income_transactions))

        # Calculate business expenses using metadata for business percentage
        expense_transactions = [
            t for t in year_transactions 
            if t.is_expense() 
            and t.category is not None
            and t.category != "personal"  # Assuming personal expenses are not deductible
        ]

        total_expenses = 0.0
        for t in expense_transactions:
            # Check for business_use_percentage in metadata
            business_pct = t.get_metadata("business_use_percentage", 100.0)
            if business_pct is not None:
                total_expenses += float(t.amount) * (business_pct / 100.0)
            else:
                # Default to 100% business if not specified for business categories
                total_expenses += float(t.amount)

        # Add additional deductions
        additional_deductions = 0.0
        if deductions:
            additional_deductions = sum(d.amount for d in deductions)

        # Get standard deduction
        std_deduction = self._standard_deduction.get(tax_year, {}).get(
            self.filing_status,
            12950,  # Default to 2022 single
        )

        # Calculate total deductions (greater of itemized or standard)
        total_deductions = max(total_expenses + additional_deductions, std_deduction)

        # Calculate taxable income
        taxable_income = max(0, total_income - total_deductions)

        return total_income, total_deductions, taxable_income

    def calculate_federal_tax(
        self,
        taxable_income: float,
        tax_year: int,
        filing_status: Optional[FilingStatus] = None,
    ) -> float:
        """
        Calculate federal income tax using common financial calculations.

        Args:
            taxable_income: Taxable income amount
            tax_year: Tax year
            filing_status: Filing status (defaults to instance filing status)

        Returns:
            Federal tax amount
        """
        # Get tax brackets
        status = filing_status or self.filing_status
        brackets = self.get_tax_brackets(TaxJurisdiction.FEDERAL, tax_year, status)

        if not brackets:
            raise ValueError(f"No federal tax brackets for {tax_year} and {status}")

        # Use common library tax calculation
        bracket_data = [
            (thresh, rate / 100) for thresh, rate in zip(brackets.income_thresholds, brackets.rates)
        ]
        
        return FinancialCalculations.calculate_tax_bracket(taxable_income, bracket_data)

    def calculate_self_employment_tax(self, net_business_income: float) -> float:
        """
        Calculate self-employment tax.

        Args:
            net_business_income: Net business income

        Returns:
            Self-employment tax amount
        """
        # SE tax is calculated on 92.35% of net business income
        taxable_income = net_business_income * 0.9235

        # Social Security portion (12.4%) is subject to wage base limit
        social_security_portion = min(taxable_income, self._se_tax_income_limit) * 0.124

        # Medicare portion (2.9%) applies to all income
        medicare_portion = taxable_income * 0.029

        # Additional Medicare Tax (0.9%) on income above threshold
        # (simplified - would normally depend on filing status)
        additional_medicare = max(0, taxable_income - 200000) * 0.009

        return social_security_portion + medicare_portion + additional_medicare

    def calculate_tax_liability(
        self,
        income: Optional[float] = None,
        transactions: Optional[List[BaseTransaction]] = None,
        tax_year: int = datetime.now().year,
        deductions: List[TaxDeduction] = None,
        include_state: bool = True,
        jurisdiction: TaxJurisdiction = TaxJurisdiction.FEDERAL,
    ) -> TaxLiability:
        """
        Calculate total tax liability with performance tracking.

        Args:
            income: Direct income amount (optional)
            transactions: List of transactions (optional)
            tax_year: Tax year to calculate for
            deductions: List of tax deductions
            include_state: Whether to include state tax calculations
            jurisdiction: Primary tax jurisdiction

        Returns:
            TaxLiability object with detailed tax information
        """
        with self.measure_performance("tax_liability_calculation"):
            # Calculate taxable income
            if income is not None:
                # Direct income provided
                total_income = income
                # Use standard deduction as default
                std_deduction = self._standard_deduction.get(tax_year, {}).get(
                    self.filing_status,
                    12950,  # Default to 2022 single
                )
                total_deductions = std_deduction
                taxable_income = max(0, total_income - total_deductions)
            elif transactions is not None:
                # Calculate from transactions
                total_income, total_deductions, taxable_income = self.calculate_taxable_income(
                    transactions, tax_year, deductions
                )
            else:
                raise ValueError("Either income or transactions must be provided")

            # Calculate federal income tax
            federal_tax = self.calculate_federal_tax(taxable_income, tax_year)

            # Calculate self-employment tax
            # For this example, assume all income is business income
            self_employment_tax = self.calculate_self_employment_tax(
                total_income - total_deductions
            )

            # Calculate state tax (simplified example)
            state_tax = 0.0
            if include_state:
                # Simplified: assume 5% flat state tax
                state_tax = taxable_income * 0.05

            # Calculate total tax
            total_tax = federal_tax + self_employment_tax + state_tax

            # Calculate effective and marginal rates
            effective_rate = 0.0
            if total_income > 0:
                effective_rate = (total_tax / total_income) * 100

            # Get federal brackets to determine marginal rate
            brackets = self.get_tax_brackets(
                TaxJurisdiction.FEDERAL, tax_year, self.filing_status
            )
            marginal_rate = 0.0

            if brackets:
                for i, threshold in enumerate(brackets.income_thresholds):
                    if i < len(brackets.income_thresholds) - 1:
                        if taxable_income < brackets.income_thresholds[i + 1]:
                            marginal_rate = brackets.rates[i]
                            break
                    else:
                        marginal_rate = brackets.rates[i]

            # Create detailed breakdown
            breakdown = {
                "federal_income_tax": federal_tax,
                "self_employment_tax": self_employment_tax,
                "state_tax": state_tax,
                "total_tax": total_tax,
            }

            # Create tax liability object
            liability = TaxLiability(
                jurisdiction=TaxJurisdiction.FEDERAL,  # Primary jurisdiction
                tax_year=tax_year,
                income=total_income,
                deductions=total_deductions,
                taxable_income=taxable_income,
                tax_amount=total_tax,
                effective_rate=effective_rate,
                marginal_rate=marginal_rate,
                filing_status=self.filing_status,
                breakdown=breakdown,
            )

            return liability

    def calculate_quarterly_tax_payment(
        self,
        quarterly_taxable_income: float,
        ytd_taxable_income: float,
        tax_year: int,
        quarter: int,
        prior_payments: float = 0.0,
    ) -> EstimatedPayment:
        """
        Calculate estimated quarterly tax payment.

        Args:
            quarterly_taxable_income: Taxable income for the quarter
            ytd_taxable_income: Year-to-date taxable income
            tax_year: Tax year
            quarter: Quarter number (1-4)
            prior_payments: Sum of prior payments made this year

        Returns:
            EstimatedPayment object with payment details
        """
        # Get quarter information
        quarters = self.calculate_tax_quarters(tax_year)
        quarter_info = next((q for q in quarters if q.quarter == quarter), None)
        
        if not quarter_info:
            raise ValueError(f"Invalid quarter: {quarter}")
            
        # Calculate federal tax on YTD income
        ytd_federal_tax = self.calculate_federal_tax(ytd_taxable_income, tax_year)
        
        # Calculate self-employment tax on YTD income (simplified)
        ytd_se_tax = ytd_taxable_income * 0.15  # Approximate SE tax rate
        
        # Total YTD liability
        ytd_liability = ytd_federal_tax + ytd_se_tax
        
        # Calculate payment based on quarter
        if quarter == 1:
            # First quarter - pay 25% of projected annual tax
            payment_amount = ytd_liability * 0.25
        else:
            # For later quarters, adjust for prior payments
            remaining_liability = ytd_liability - prior_payments
            remaining_quarters = 5 - quarter  # Quarters remaining including current
            
            if remaining_quarters <= 0:
                # Last quarter or past end of year
                payment_amount = remaining_liability
            else:
                payment_amount = remaining_liability / remaining_quarters
                
        # Calculate safe harbor amount (simplified)
        safe_harbor = ytd_liability * 0.225  # 90% of annual tax / 4
        
        # Create estimated payment object with federal tax component for test compatibility
        payment = EstimatedPayment(
            tax_year=tax_year,
            quarter=quarter,
            jurisdiction=TaxJurisdiction.FEDERAL,
            due_date=quarter_info.due_date,
            payment_amount=max(0, payment_amount),
            minimum_required=max(0, min(payment_amount, safe_harbor)),
            safe_harbor_amount=safe_harbor,
            year_to_date_liability=ytd_liability,
            previous_payments=prior_payments,
            federal_tax=ytd_federal_tax * (quarter/4),
            self_employment_tax=ytd_se_tax * (quarter/4),
            notes=f"Estimated Q{quarter} tax payment for {tax_year}",
        )
        
        return payment

    def get_tax_summary(
        self,
        transactions: List[BaseTransaction],
        payments: List[TaxPayment],
        tax_year: int,
        deductions: List[TaxDeduction] = None,
    ) -> TaxYearSummary:
        """
        Generate a summary of tax obligations for a year.

        Args:
            transactions: List of all transactions (BaseTransaction format)
            payments: List of tax payments
            tax_year: Tax year
            deductions: List of tax deductions

        Returns:
            TaxYearSummary object with detailed tax information
        """
        # Calculate liability
        liability = self.calculate_tax_liability(transactions=transactions, tax_year=tax_year, deductions=deductions)

        # Filter to business transactions for the year using DateHelpers
        year_start = datetime(tax_year, 1, 1)
        year_end = datetime(tax_year, 12, 31, 23, 59, 59)

        year_transactions = [
            t for t in transactions if year_start <= t.date <= year_end
        ]

        # Calculate income and expenses
        income_transactions = [
            t for t in year_transactions if t.is_income()
        ]
        total_income = float(sum(t.amount for t in income_transactions))

        expense_transactions = [
            t for t in year_transactions
            if t.is_expense() 
            and t.category is not None
            and t.category != "personal"
        ]
        
        total_expenses = 0.0
        for t in expense_transactions:
            business_pct = t.get_metadata("business_use_percentage", 100.0)
            if business_pct is not None:
                total_expenses += float(t.amount) * (business_pct / 100.0)
            else:
                total_expenses += float(t.amount)

        # Get total payments
        year_payments = [p for p in payments if p.tax_year == tax_year]
        total_paid = sum(p.amount for p in year_payments)

        # Create summary
        summary = TaxYearSummary(
            tax_year=tax_year,
            total_income=total_income,
            total_expenses=total_expenses,
            total_deductions=liability.deductions,
            taxable_income=liability.taxable_income,
            total_tax=liability.tax_amount,
            effective_tax_rate=liability.effective_rate,
            federal_tax=liability.breakdown["federal_income_tax"],
            state_tax=liability.breakdown.get("state_tax", 0.0),
            self_employment_tax=liability.breakdown["self_employment_tax"],
            total_paid=total_paid,
            balance_due=max(0, liability.tax_amount - total_paid),
            deductions=deductions or [],
            payments=year_payments,
        )

        return summary

    def optimize_deductions(
        self,
        transactions: List[BaseTransaction],
        potential_deductions: List[TaxDeduction],
        tax_year: int,
        target_liability: Optional[float] = None,
    ) -> List[TaxDeduction]:
        """
        Optimize tax deductions to minimize tax liability.

        Args:
            transactions: List of all transactions
            potential_deductions: List of potential deductions to consider
            tax_year: Tax year
            target_liability: Optional target tax liability

        Returns:
            List of optimized deductions
        """
        # Start with base liability without extra deductions
        base_liability = self.calculate_tax_liability(transactions=transactions, tax_year=tax_year)

        # If no target, simply use all deductions
        if target_liability is None:
            return potential_deductions

        # Sort deductions by amount (largest first)
        sorted_deductions = sorted(
            potential_deductions, key=lambda d: d.amount, reverse=True
        )

        # Start with no deductions
        selected_deductions = []
        current_liability = base_liability.tax_amount

        # Add deductions until target is reached
        for deduction in sorted_deductions:
            # Calculate liability with this deduction
            test_deductions = selected_deductions + [deduction]
            test_liability = self.calculate_tax_liability(
                transactions=transactions, tax_year=tax_year, deductions=test_deductions
            )

            # If this reduces liability closer to target, add it
            if abs(test_liability.tax_amount - target_liability) < abs(
                current_liability - target_liability
            ):
                selected_deductions.append(deduction)
                current_liability = test_liability.tax_amount

            # If we've reached or gone below target, stop
            if current_liability <= target_liability:
                break

        return selected_deductions


# Backward compatibility alias
TaxManager = FreelancerTaxManager