"""Migrated project profitability analyzer for freelancers using common library."""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Set

import pandas as pd
from pydantic import BaseModel

# Import common library components
from common.core.engines.analysis_engine import AnalysisEngine
from common.core.models.analysis_results import AnalysisResult
from common.core.models.base_transaction import BaseTransaction, TransactionType
from common.core.utils.financial_calculations import FinancialCalculations
from common.core.utils.date_helpers import DateHelpers
from common.core.engines.time_series_analyzer import TimeSeriesAnalyzer

# Import persona-specific models
from personal_finance_tracker.models.common import (
    Client,
    Project,
    TimeEntry,
    Transaction,
    Invoice,
)
from personal_finance_tracker.project.models import (
    ProjectMetricType,
    ProfitabilityMetric,
    ProjectProfitability,
    ClientProfitability,
    TrendPoint,
    TrendAnalysis,
)


class FreelancerProjectProfiler(AnalysisEngine):
    """
    Freelancer-specific project profitability analyzer extending common analysis engine.
    
    Analyzes project profitability based on time tracking, expenses,
    and revenue data to help freelancers make informed business decisions.
    """

    def __init__(self):
        """Initialize the project profiler with common analysis engine capabilities."""
        super().__init__(enable_caching=True, enable_performance_tracking=True)
        
        # Initialize time series analyzer for trend analysis
        self.time_series_analyzer = TimeSeriesAnalyzer()
        
        # Set configuration defaults
        self.set_configuration({
            "performance_threshold_seconds": 3.0,
            "minimum_hours_for_rate_calculation": 0.01,
            "minimum_revenue_for_margin_calculation": 0.01,
            "minimum_expenses_for_roi_calculation": 0.01
        })

    def analyze(self, data: Dict) -> AnalysisResult:
        """
        Perform comprehensive project profitability analysis.
        
        Args:
            data: Dictionary containing analysis parameters
            
        Returns:
            AnalysisResult with profitability analysis
        """
        with self.measure_performance("project_profitability_analysis"):
            analysis_type = data.get("analysis_type", "project")
            
            if analysis_type == "project":
                result = self.analyze_project_profitability(**data)
            elif analysis_type == "client":
                result = self.analyze_client_profitability(**data)
            elif analysis_type == "all_projects":
                result = self.analyze_all_projects(**data)
            elif analysis_type == "trend":
                result = self.generate_trend_analysis(**data)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            return AnalysisResult(
                analysis_type=f"project_{analysis_type}_profitability",
                calculation_date=datetime.now(),
                processing_time_ms=self.get_performance_stats().get("project_profitability_analysis", {}).get("avg_duration_ms", 0),
                confidence_score=1.0,  # Profitability calculations are deterministic
                metadata={
                    "result": result.__dict__ if hasattr(result, '__dict__') else str(result),
                    "analysis_engine": "FreelancerProjectProfiler"
                }
            )

    def analyze_project_profitability(
        self,
        project: Project,
        time_entries: List[TimeEntry],
        transactions: List[Transaction],
        invoices: List[Invoice],
        force_recalculation: bool = False,
        **kwargs
    ) -> ProjectProfitability:
        """
        Analyze the profitability of a single project with caching.

        Args:
            project: Project to analyze
            time_entries: Time entries associated with the project
            transactions: Transactions associated with the project
            invoices: Invoices associated with the project
            force_recalculation: Whether to force recalculation

        Returns:
            ProjectProfitability analysis result
        """
        # Generate cache key
        cache_key = f"project_{project.id}_{hash(str(time_entries + transactions + invoices))}"
        
        # Check cache unless forced recalculation
        if not force_recalculation:
            cached_result = self.get_cached_result(cache_key)
            if cached_result is not None:
                return cached_result

        with self.measure_performance("single_project_analysis"):
            # Filter to entries for this project
            project_time_entries = [e for e in time_entries if e.project_id == project.id]

            # Calculate total hours
            total_hours = sum(
                entry.duration_minutes / 60
                for entry in project_time_entries
                if entry.duration_minutes is not None
            )

            # Calculate total revenue from invoices
            project_invoices = [i for i in invoices if i.project_id == project.id]
            paid_invoices = [i for i in project_invoices if i.status == "paid"]
            total_revenue = sum(invoice.amount for invoice in paid_invoices)

            # Calculate total expenses
            project_expenses = [
                t
                for t in transactions
                if (
                    t.transaction_type == TransactionType.EXPENSE
                    and t.project_id == project.id
                )
            ]
            total_expenses = sum(t.amount for t in project_expenses)

            # Calculate profitability metrics using common library
            total_profit = total_revenue - total_expenses

            # Use configuration for minimum values to avoid division by zero
            min_hours = self.get_config_value("minimum_hours_for_rate_calculation", 0.01)
            min_revenue = self.get_config_value("minimum_revenue_for_margin_calculation", 0.01)
            min_expenses = self.get_config_value("minimum_expenses_for_roi_calculation", 0.01)

            effective_hourly_rate = total_revenue / max(total_hours, min_hours)
            profit_margin = 100 * total_profit / max(total_revenue, min_revenue)
            
            # Use common library ROI calculation
            roi = FinancialCalculations.calculate_roi(total_profit, max(total_expenses, min_expenses))

            # Determine if project is completed
            is_completed = (
                project.end_date is not None and project.end_date <= datetime.now()
            )

            # Create project profitability result
            result = ProjectProfitability(
                project_id=project.id,
                project_name=project.name,
                client_id=project.client_id,
                start_date=project.start_date,
                end_date=project.end_date,
                total_hours=total_hours,
                total_revenue=total_revenue,
                total_expenses=total_expenses,
                total_profit=total_profit,
                effective_hourly_rate=effective_hourly_rate,
                profit_margin=profit_margin,
                roi=roi,
                is_completed=is_completed,
                calculation_date=datetime.now(),
                metrics=[
                    ProfitabilityMetric(
                        project_id=project.id,
                        metric_type=ProjectMetricType.HOURLY_RATE,
                        value=effective_hourly_rate,
                    ),
                    ProfitabilityMetric(
                        project_id=project.id,
                        metric_type=ProjectMetricType.TOTAL_PROFIT,
                        value=total_profit,
                    ),
                    ProfitabilityMetric(
                        project_id=project.id,
                        metric_type=ProjectMetricType.PROFIT_MARGIN,
                        value=profit_margin,
                    ),
                    ProfitabilityMetric(
                        project_id=project.id, metric_type=ProjectMetricType.ROI, value=roi
                    ),
                ],
            )

            # Cache the result
            self.set_cached_result(cache_key, result)

            return result

    def analyze_client_profitability(
        self,
        client: Client,
        projects: List[Project],
        time_entries: List[TimeEntry],
        transactions: List[Transaction],
        invoices: List[Invoice],
        force_recalculation: bool = False,
        **kwargs
    ) -> ClientProfitability:
        """
        Analyze the profitability of all projects for a client.

        Args:
            client: Client to analyze
            projects: All projects for the client
            time_entries: All time entries
            transactions: All transactions
            invoices: All invoices
            force_recalculation: Whether to force recalculation

        Returns:
            ClientProfitability analysis result
        """
        # Generate cache key
        cache_key = f"client_{client.id}_{hash(str(projects + time_entries + transactions + invoices))}"
        
        # Check cache unless forced recalculation
        if not force_recalculation:
            cached_result = self.get_cached_result(cache_key)
            if cached_result is not None:
                return cached_result

        with self.measure_performance("client_analysis"):
            # Filter to client's projects
            client_projects = [p for p in projects if p.client_id == client.id]

            if not client_projects:
                return ClientProfitability(
                    client_id=client.id,
                    client_name=client.name,
                    number_of_projects=0,
                    total_hours=0.0,
                    total_revenue=0.0,
                    total_expenses=0.0,
                    total_profit=0.0,
                    average_hourly_rate=0.0,
                    average_profit_margin=0.0,
                )

            # Analyze each project
            project_analyses = []
            for project in client_projects:
                analysis = self.analyze_project_profitability(
                    project, time_entries, transactions, invoices, force_recalculation
                )
                project_analyses.append(analysis)

            # Calculate client-level metrics
            total_hours = sum(p.total_hours for p in project_analyses)
            total_revenue = sum(p.total_revenue for p in project_analyses)
            total_expenses = sum(p.total_expenses for p in project_analyses)
            total_profit = sum(p.total_profit for p in project_analyses)

            # Calculate averages using configuration minimums
            min_hours = self.get_config_value("minimum_hours_for_rate_calculation", 0.01)
            min_revenue = self.get_config_value("minimum_revenue_for_margin_calculation", 0.01)
            
            avg_hourly_rate = total_revenue / max(total_hours, min_hours)
            avg_profit_margin = 100 * total_profit / max(total_revenue, min_revenue)

            # Calculate average invoice payment time using DateHelpers
            client_invoices = [
                i for i in invoices if i.client_id == client.id and i.status == "paid"
            ]
            payment_days = []

            for invoice in client_invoices:
                if invoice.payment_date and invoice.issue_date:
                    days = DateHelpers.get_business_days_between(invoice.issue_date, invoice.payment_date)
                    payment_days.append(days)

            avg_payment_days = None
            if payment_days:
                avg_payment_days = sum(payment_days) / len(payment_days)

            # Create client profitability result
            result = ClientProfitability(
                client_id=client.id,
                client_name=client.name,
                number_of_projects=len(client_projects),
                total_hours=total_hours,
                total_revenue=total_revenue,
                total_expenses=total_expenses,
                total_profit=total_profit,
                average_hourly_rate=avg_hourly_rate,
                average_profit_margin=avg_profit_margin,
                average_invoice_payment_days=avg_payment_days,
                projects=project_analyses,
            )

            # Cache the result
            self.set_cached_result(cache_key, result)

            return result

    def analyze_all_projects(
        self,
        projects: List[Project],
        time_entries: List[TimeEntry],
        transactions: List[Transaction],
        invoices: List[Invoice],
        force_recalculation: bool = False,
        **kwargs
    ) -> List[ProjectProfitability]:
        """
        Analyze profitability for all projects with performance monitoring.

        Args:
            projects: All projects to analyze
            time_entries: All time entries
            transactions: All transactions
            invoices: All invoices
            force_recalculation: Whether to force recalculation

        Returns:
            List of ProjectProfitability analysis results
        """
        with self.measure_performance("all_projects_analysis"):
            # Analyze each project
            results = []
            for project in projects:
                analysis = self.analyze_project_profitability(
                    project, time_entries, transactions, invoices, force_recalculation
                )
                results.append(analysis)

            # Sort by profitability (highest first)
            results.sort(key=lambda x: x.total_profit, reverse=True)

            # Verify performance requirement using configuration
            perf_stats = self.get_performance_stats()
            elapsed_time = perf_stats.get("all_projects_analysis", {}).get("avg_duration_ms", 0) / 1000.0
            threshold = self.get_config_value("performance_threshold_seconds", 3.0)
            
            if len(projects) > 100 and elapsed_time > threshold:
                print(
                    f"Warning: Project analysis took {elapsed_time:.2f} seconds for {len(projects)} projects"
                )

            return results

    def generate_trend_analysis(
        self,
        metric_type: ProjectMetricType,
        start_date: datetime,
        end_date: datetime,
        period: str = "monthly",
        project_id: Optional[str] = None,
        client_id: Optional[str] = None,
        projects: Optional[List[Project]] = None,
        time_entries: Optional[List[TimeEntry]] = None,
        transactions: Optional[List[Transaction]] = None,
        invoices: Optional[List[Invoice]] = None,
        **kwargs
    ) -> TrendAnalysis:
        """
        Generate trend analysis for project metrics over time using time series analyzer.

        Args:
            metric_type: Type of metric to analyze
            start_date: Start date for analysis
            end_date: End date for analysis
            period: Period for grouping ("weekly", "monthly", "quarterly", "yearly")
            project_id: Optional project ID to filter
            client_id: Optional client ID to filter
            projects: Optional list of projects
            time_entries: Optional list of time entries
            transactions: Optional list of transactions
            invoices: Optional list of invoices

        Returns:
            TrendAnalysis result
        """
        if not projects or not time_entries or not transactions or not invoices:
            return TrendAnalysis(
                metric_type=metric_type,
                project_id=project_id,
                client_id=client_id,
                period=period,
                start_date=start_date,
                end_date=end_date,
                data_points=[],
            )

        with self.measure_performance("trend_analysis"):
            # Filter projects
            filtered_projects = projects
            if project_id:
                filtered_projects = [p for p in projects if p.id == project_id]
            elif client_id:
                filtered_projects = [p for p in projects if p.client_id == client_id]

            if not filtered_projects:
                return TrendAnalysis(
                    metric_type=metric_type,
                    project_id=project_id,
                    client_id=client_id,
                    period=period,
                    start_date=start_date,
                    end_date=end_date,
                    data_points=[],
                )

            # Get project IDs for filtering
            project_ids = {p.id for p in filtered_projects}

            # Use DateHelpers for period boundaries
            periods = DateHelpers.group_by_period(
                [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)],
                period
            )

            # Calculate metric for each period
            data_points = []

            for period_key, period_dates in periods.items():
                if not period_dates:
                    continue
                    
                period_start = min(period_dates)
                period_end = max(period_dates)

                # Filter data for this period
                period_time_entries = [
                    e
                    for e in time_entries
                    if (
                        e.project_id in project_ids
                        and e.start_time >= period_start
                        and e.start_time <= period_end
                    )
                ]

                period_transactions = [
                    t
                    for t in transactions
                    if (
                        t.project_id in project_ids
                        and t.date >= period_start
                        and t.date <= period_end
                    )
                ]

                period_invoices = [
                    i
                    for i in invoices
                    if (
                        i.project_id in project_ids
                        and i.issue_date >= period_start
                        and i.issue_date <= period_end
                        and i.status == "paid"
                    )
                ]

                # Calculate metrics for this period
                total_hours = sum(
                    entry.duration_minutes / 60
                    for entry in period_time_entries
                    if entry.duration_minutes is not None
                )

                total_revenue = sum(invoice.amount for invoice in period_invoices)

                total_expenses = sum(
                    t.amount
                    for t in period_transactions
                    if t.transaction_type == TransactionType.EXPENSE
                )

                total_profit = total_revenue - total_expenses

                # Determine metric value based on type using configuration minimums
                min_hours = self.get_config_value("minimum_hours_for_rate_calculation", 0.01)
                min_revenue = self.get_config_value("minimum_revenue_for_margin_calculation", 0.01)
                min_expenses = self.get_config_value("minimum_expenses_for_roi_calculation", 0.01)
                
                metric_value = 0.0

                if metric_type == ProjectMetricType.HOURLY_RATE:
                    metric_value = total_revenue / max(total_hours, min_hours)
                elif metric_type == ProjectMetricType.TOTAL_PROFIT:
                    metric_value = total_profit
                elif metric_type == ProjectMetricType.PROFIT_MARGIN:
                    metric_value = 100 * total_profit / max(total_revenue, min_revenue)
                elif metric_type == ProjectMetricType.ROI:
                    metric_value = FinancialCalculations.calculate_roi(total_profit, max(total_expenses, min_expenses))

                # Add data point
                data_point = TrendPoint(
                    date=period_start, value=metric_value
                )
                data_points.append(data_point)

            # Sort data points by date
            data_points.sort(key=lambda x: x.date)

            # Create trend analysis
            trend = TrendAnalysis(
                metric_type=metric_type,
                project_id=project_id,
                client_id=client_id,
                period=period,
                start_date=start_date,
                end_date=end_date,
                data_points=data_points,
                description=f"{period.title()} trend of {metric_type.value} from {start_date.date()} to {end_date.date()}",
            )

            return trend

    def record_time_entry(self, time_entry: TimeEntry) -> TimeEntry:
        """
        Record a new time entry for a project and clear cache.

        Args:
            time_entry: Time entry to record

        Returns:
            The recorded time entry
        """
        # Clear cache when new time entry is recorded
        self.clear_cache()
        return time_entry

    def allocate_expense(
        self, transaction: Transaction, project_id: str, amount: Optional[float] = None
    ) -> Transaction:
        """
        Allocate an expense to a project and clear cache.

        Args:
            transaction: Transaction to allocate
            project_id: Project ID to allocate to
            amount: Optional amount to allocate (defaults to full amount)

        Returns:
            The updated transaction
        """
        # Validate transaction is an expense
        if transaction.transaction_type != TransactionType.EXPENSE:
            raise ValueError("Transaction must be an expense")

        # Update transaction project
        transaction.project_id = project_id

        # Clear cache to ensure recalculation
        self.clear_cache()

        return transaction


# Backward compatibility alias
ProjectProfiler = FreelancerProjectProfiler