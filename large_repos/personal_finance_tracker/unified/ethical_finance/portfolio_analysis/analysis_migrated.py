"""Migrated portfolio analysis system for ESG-aligned investments using common library."""

from typing import Dict, List, Optional, Any, Tuple
from datetime import date
import time
from dataclasses import dataclass
import pandas as pd
import numpy as np

# Import common library components
from common.core.engines.analysis_engine import AnalysisEngine
from common.core.models.analysis_results import AnalysisResult
from common.core.utils.financial_calculations import FinancialCalculations
from common.core.engines.time_series_analyzer import TimeSeriesAnalyzer

# Import persona-specific models
from ethical_finance.models import Investment, Portfolio, InvestmentHolding
from ethical_finance.ethical_screening.screening_migrated import SociallyResponsibleEthicalScreener, ScreeningResult


@dataclass
class PortfolioCompositionResult:
    """Result of analyzing the composition of a portfolio."""
    
    portfolio_id: str
    analysis_date: date
    sector_breakdown: Dict[str, float]
    industry_breakdown: Dict[str, float]
    esg_theme_exposure: Dict[str, float]
    concentration_metrics: Dict[str, float]
    top_holdings: List[Tuple[str, float]]
    ethical_alignment: Dict[str, Any]
    processing_time_ms: float = 0


@dataclass
class DiversificationAssessment:
    """Assessment of portfolio diversification with ethical constraints."""
    
    portfolio_id: str
    assessment_date: date
    diversification_score: float  # 0-100
    sector_concentration_risk: Dict[str, float]
    industry_concentration_risk: Dict[str, float]
    esg_theme_concentration_risk: Dict[str, float]
    diversification_recommendations: List[Dict[str, Any]]
    ethical_constraints_applied: List[str]
    processing_time_ms: float = 0


@dataclass
class PortfolioOptimizationResult:
    """Result of optimizing a portfolio for both returns and ethical alignment."""
    
    portfolio_id: str
    optimization_date: date
    current_ethical_score: float
    current_risk_metrics: Dict[str, float]
    recommended_changes: List[Dict[str, Any]]
    expected_improvement: Dict[str, float]
    optimization_constraints: Dict[str, Any]
    processing_time_ms: float = 0


class SociallyResponsiblePortfolioAnalysisSystem(AnalysisEngine):
    """
    Socially responsible investor portfolio analysis system extending common analysis engine.
    
    Analyzes investment portfolios with ESG considerations using common frameworks.
    """
    
    def __init__(self, ethical_screener: Optional[SociallyResponsibleEthicalScreener] = None):
        """Initialize with optional ethical screener and common analysis engine.
        
        Args:
            ethical_screener: Optional EthicalScreener for ethical alignment analysis
        """
        super().__init__(enable_caching=True, enable_performance_tracking=True)
        
        self.ethical_screener = ethical_screener
        
        # Initialize time series analyzer for performance analysis
        self.time_series_analyzer = TimeSeriesAnalyzer()
        
        # Set configuration defaults
        self.set_configuration({
            "performance_threshold_seconds": 5.0,  # 5 second requirement for 200+ holdings
            "max_sector_concentration": 0.25,
            "max_industry_concentration": 0.15,
            "max_esg_theme_concentration": 0.5,
            "min_diversification_score": 70.0
        })

    def analyze(self, data: Dict) -> AnalysisResult:
        """
        Perform comprehensive portfolio analysis.
        
        Args:
            data: Dictionary containing analysis parameters
            
        Returns:
            AnalysisResult with portfolio analysis
        """
        with self.measure_performance("portfolio_analysis"):
            analysis_type = data.get("analysis_type", "composition")
            
            if analysis_type == "composition":
                result = self.analyze_portfolio_composition(**data)
            elif analysis_type == "diversification":
                result = self.assess_diversification(**data)
            elif analysis_type == "optimization":
                result = self.optimize_portfolio(**data)
            elif analysis_type == "esg_theme_concentration":
                result = self.analyze_esg_theme_concentration(**data)
            elif analysis_type == "risk_adjusted_esg":
                result = self.calculate_risk_adjusted_esg_performance(**data)
            else:
                raise ValueError(f"Unknown analysis type: {analysis_type}")
            
            return AnalysisResult(
                analysis_type=f"portfolio_{analysis_type}_analysis",
                calculation_date=time.time(),
                processing_time_ms=self.get_performance_stats().get("portfolio_analysis", {}).get("avg_duration_ms", 0),
                confidence_score=0.9,  # High confidence in portfolio analysis
                metadata={
                    "result": result.__dict__ if hasattr(result, '__dict__') else str(result),
                    "analysis_engine": "SociallyResponsiblePortfolioAnalysisSystem"
                }
            )
    
    def analyze_portfolio_composition(
        self, 
        portfolio: Portfolio, 
        investments: Dict[str, Investment],
        screening_results: Optional[Dict[str, ScreeningResult]] = None,
        **kwargs
    ) -> PortfolioCompositionResult:
        """Analyze the composition of a portfolio with performance tracking.
        
        Args:
            portfolio: The portfolio to analyze
            investments: Dict mapping investment IDs to Investment objects
            screening_results: Optional dict of screening results for ethical analysis
            
        Returns:
            PortfolioCompositionResult containing the analysis
        """
        with self.measure_performance("portfolio_composition_analysis"):
            # Calculate total portfolio value
            total_value = portfolio.total_value
            
            # Calculate sector breakdown
            sector_breakdown = {}
            for holding in portfolio.holdings:
                investment_id = holding.investment_id
                if investment_id in investments:
                    investment = investments[investment_id]
                    sector = investment.sector
                    
                    # Calculate sector weight
                    weight = holding.current_value / total_value
                    
                    if sector in sector_breakdown:
                        sector_breakdown[sector] += weight
                    else:
                        sector_breakdown[sector] = weight
            
            # Calculate industry breakdown
            industry_breakdown = {}
            for holding in portfolio.holdings:
                investment_id = holding.investment_id
                if investment_id in investments:
                    investment = investments[investment_id]
                    industry = investment.industry
                    
                    # Calculate industry weight
                    weight = holding.current_value / total_value
                    
                    if industry in industry_breakdown:
                        industry_breakdown[industry] += weight
                    else:
                        industry_breakdown[industry] = weight
            
            # Calculate ESG theme exposure
            esg_theme_exposure = {}
            
            # Initialize with common ESG themes
            esg_themes = {
                "renewable_energy": 0.0,
                "climate_action": 0.0,
                "social_justice": 0.0,
                "diversity_equity_inclusion": 0.0,
                "sustainable_agriculture": 0.0,
                "circular_economy": 0.0,
                "community_development": 0.0,
                "good_governance": 0.0
            }
            
            for holding in portfolio.holdings:
                investment_id = holding.investment_id
                if investment_id in investments:
                    investment = investments[investment_id]
                    weight = holding.current_value / total_value
                    
                    # Map positive practices to themes
                    for practice in investment.positive_practices:
                        theme = self._map_practice_to_theme(practice)
                        if theme in esg_themes:
                            # Add weight to theme exposure
                            score_factor = investment.esg_ratings.overall / 100
                            esg_themes[theme] += weight * score_factor
            
            # Normalize theme exposure to a 0-1 scale
            for theme, exposure in esg_themes.items():
                # Cap at 1.0 for each theme
                esg_theme_exposure[theme] = min(1.0, exposure)
            
            # Identify top holdings
            top_holdings = []
            for holding in portfolio.holdings:
                weight = holding.current_value / total_value
                top_holdings.append((holding.investment_id, weight))
            
            # Sort by weight descending
            top_holdings.sort(key=lambda x: x[1], reverse=True)
            
            # Calculate concentration metrics using financial calculations
            concentration_metrics = {}
            
            # Herfindahl-Hirschman Index (HHI) for holdings
            holding_weights = [weight for _, weight in top_holdings]
            hhi = FinancialCalculations.calculate_hhi(holding_weights)
            concentration_metrics["holdings_hhi"] = hhi
            
            # Sector concentration
            sector_weights = list(sector_breakdown.values())
            sector_hhi = FinancialCalculations.calculate_hhi(sector_weights)
            concentration_metrics["sector_hhi"] = sector_hhi
            
            # Industry concentration
            industry_weights = list(industry_breakdown.values())
            industry_hhi = FinancialCalculations.calculate_hhi(industry_weights)
            concentration_metrics["industry_hhi"] = industry_hhi
            
            # Top 5 concentration
            top5_concentration = sum(weight for _, weight in top_holdings[:5])
            concentration_metrics["top5_concentration"] = top5_concentration
            
            # Analyze ethical alignment if screening results provided
            ethical_alignment = {}
            if screening_results:
                # Calculate percentage of portfolio passing ethical screening
                holdings_passing = 0
                value_passing = 0.0
                
                for holding in portfolio.holdings:
                    investment_id = holding.investment_id
                    if investment_id in screening_results and screening_results[investment_id].passed:
                        holdings_passing += 1
                        value_passing += holding.current_value
                
                ethical_alignment["holdings_passing_percentage"] = holdings_passing / len(portfolio.holdings) if portfolio.holdings else 0
                ethical_alignment["value_passing_percentage"] = value_passing / total_value if total_value > 0 else 0
                
                # Calculate average ESG scores weighted by holding value using common calculations
                weights_and_scores = []
                for holding in portfolio.holdings:
                    investment_id = holding.investment_id
                    if investment_id in investments and investment_id in screening_results:
                        investment = investments[investment_id]
                        weight = holding.current_value / total_value
                        
                        weights_and_scores.append((investment.esg_ratings.environmental, weight))
                
                if weights_and_scores:
                    weighted_env_score = FinancialCalculations.calculate_weighted_average(weights_and_scores)
                    
                    # Calculate other weighted scores
                    weights_and_scores = [(investments[h.investment_id].esg_ratings.social, h.current_value / total_value) 
                                        for h in portfolio.holdings if h.investment_id in investments]
                    weighted_social_score = FinancialCalculations.calculate_weighted_average(weights_and_scores) if weights_and_scores else 0
                    
                    weights_and_scores = [(investments[h.investment_id].esg_ratings.governance, h.current_value / total_value) 
                                        for h in portfolio.holdings if h.investment_id in investments]
                    weighted_gov_score = FinancialCalculations.calculate_weighted_average(weights_and_scores) if weights_and_scores else 0
                    
                    weights_and_scores = [(investments[h.investment_id].esg_ratings.overall, h.current_value / total_value) 
                                        for h in portfolio.holdings if h.investment_id in investments]
                    weighted_overall_score = FinancialCalculations.calculate_weighted_average(weights_and_scores) if weights_and_scores else 0
                    
                    ethical_alignment["weighted_environmental_score"] = weighted_env_score
                    ethical_alignment["weighted_social_score"] = weighted_social_score
                    ethical_alignment["weighted_governance_score"] = weighted_gov_score
                    ethical_alignment["weighted_overall_score"] = weighted_overall_score
            
            # Get processing time from performance tracker
            processing_time = self.get_performance_stats().get("portfolio_composition_analysis", {}).get("avg_duration_ms", 0)
            
            return PortfolioCompositionResult(
                portfolio_id=portfolio.portfolio_id,
                analysis_date=date.today(),
                sector_breakdown=sector_breakdown,
                industry_breakdown=industry_breakdown,
                esg_theme_exposure=esg_theme_exposure,
                concentration_metrics=concentration_metrics,
                top_holdings=top_holdings[:10],  # Top 10 holdings
                ethical_alignment=ethical_alignment,
                processing_time_ms=max(1.0, processing_time)  # Ensure non-zero processing time
            )
    
    def assess_diversification(
        self, 
        portfolio: Portfolio, 
        investments: Dict[str, Investment],
        ethical_constraints: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> DiversificationAssessment:
        """Assess portfolio diversification considering ethical constraints.
        
        Args:
            portfolio: The portfolio to assess
            investments: Dict mapping investment IDs to Investment objects
            ethical_constraints: Optional dict of ethical constraints to consider
            
        Returns:
            DiversificationAssessment containing the diversification analysis
        """
        with self.measure_performance("diversification_assessment"):
            # Analyze portfolio composition first
            composition = self.analyze_portfolio_composition(portfolio, investments)
            
            # Record which constraints were applied
            applied_constraints = []
            if ethical_constraints:
                for constraint, value in ethical_constraints.items():
                    if value:  # If constraint is active
                        applied_constraints.append(constraint)
            
            # Calculate diversification score (base)
            diversification_metrics = {}
            
            # Use configuration for thresholds
            min_div_score = self.get_config_value("min_diversification_score", 70.0)
            
            # Sector diversification: lower HHI is better
            sector_hhi = composition.concentration_metrics["sector_hhi"]
            # Scale: 1.0 (perfect concentration) to 0.0 (perfect diversification)
            # Convert to a 0-100 score where higher is better
            sector_div_score = max(0, min(100, 100 * (1 - sector_hhi)))
            diversification_metrics["sector_diversification"] = sector_div_score
            
            # Industry diversification
            industry_hhi = composition.concentration_metrics["industry_hhi"]
            industry_div_score = max(0, min(100, 100 * (1 - industry_hhi)))
            diversification_metrics["industry_diversification"] = industry_div_score
            
            # Holdings concentration
            holdings_hhi = composition.concentration_metrics["holdings_hhi"]
            holdings_div_score = max(0, min(100, 100 * (1 - holdings_hhi)))
            diversification_metrics["holdings_diversification"] = holdings_div_score
            
            # Top 5 concentration (lower is better for diversification)
            top5_concentration = composition.concentration_metrics["top5_concentration"]
            top5_div_score = max(0, min(100, 100 * (1 - top5_concentration)))
            diversification_metrics["top5_diversification"] = top5_div_score
            
            # Overall diversification score using weighted average calculation
            weights_and_scores = [
                (sector_div_score, 0.3),
                (industry_div_score, 0.3),
                (holdings_div_score, 0.2),
                (top5_div_score, 0.2)
            ]
            
            overall_score = FinancialCalculations.calculate_weighted_average(weights_and_scores)
            
            # Identify concentration risks using configuration
            max_sector_conc = self.get_config_value("max_sector_concentration", 0.25)
            max_industry_conc = self.get_config_value("max_industry_concentration", 0.15)
            max_esg_theme_conc = self.get_config_value("max_esg_theme_concentration", 0.5)
            
            sector_concentration_risk = {}
            industry_concentration_risk = {}
            esg_theme_concentration_risk = {}
            
            # Sector concentration risk
            for sector, weight in composition.sector_breakdown.items():
                if weight > max_sector_conc:
                    sector_concentration_risk[sector] = weight
            
            # Industry concentration risk
            for industry, weight in composition.industry_breakdown.items():
                if weight > max_industry_conc:
                    industry_concentration_risk[industry] = weight
            
            # ESG theme concentration risk
            for theme, exposure in composition.esg_theme_exposure.items():
                if exposure > max_esg_theme_conc:
                    esg_theme_concentration_risk[theme] = exposure
            
            # Generate diversification recommendations
            recommendations = []
            
            # Sector diversification recommendations
            if sector_concentration_risk:
                recommendations.append({
                    "type": "reduce_sector_concentration",
                    "description": "Reduce concentration in these sectors",
                    "sectors": list(sector_concentration_risk.keys()),
                    "priority": "high" if max(sector_concentration_risk.values()) > 0.4 else "medium"
                })
            
            # Industry diversification recommendations
            if industry_concentration_risk:
                recommendations.append({
                    "type": "reduce_industry_concentration",
                    "description": "Reduce concentration in these industries",
                    "industries": list(industry_concentration_risk.keys()),
                    "priority": "high" if max(industry_concentration_risk.values()) > 0.25 else "medium"
                })
            
            # Holdings diversification recommendations
            if holdings_div_score < min_div_score:
                recommendations.append({
                    "type": "spread_across_more_holdings",
                    "description": "Distribute investment across more holdings",
                    "priority": "medium"
                })
            
            # Apply ethical constraints to recommendations
            if ethical_constraints:
                # Remove recommendations that conflict with ethical constraints
                filtered_recommendations = []
                for rec in recommendations:
                    if rec["type"] == "reduce_sector_concentration":
                        conflicting = False
                        for sector in rec["sectors"]:
                            if self._sector_conflicts_with_constraints(sector, ethical_constraints):
                                conflicting = True
                                break
                        if not conflicting:
                            filtered_recommendations.append(rec)
                    else:
                        filtered_recommendations.append(rec)
                
                recommendations = filtered_recommendations
            
            # Get processing time from performance tracker
            processing_time = self.get_performance_stats().get("diversification_assessment", {}).get("avg_duration_ms", 0)
            
            return DiversificationAssessment(
                portfolio_id=portfolio.portfolio_id,
                assessment_date=date.today(),
                diversification_score=overall_score,
                sector_concentration_risk=sector_concentration_risk,
                industry_concentration_risk=industry_concentration_risk,
                esg_theme_concentration_risk=esg_theme_concentration_risk,
                diversification_recommendations=recommendations,
                ethical_constraints_applied=applied_constraints,
                processing_time_ms=max(1.0, processing_time)
            )
    
    def optimize_portfolio(
        self,
        portfolio: Portfolio,
        investments: Dict[str, Investment],
        candidate_investments: Dict[str, Investment],
        optimization_goals: Dict[str, float],
        constraints: Dict[str, Any],
        **kwargs
    ) -> PortfolioOptimizationResult:
        """Optimize a portfolio for both returns and ethical alignment.
        
        Args:
            portfolio: The portfolio to optimize
            investments: Dict mapping current investment IDs to Investment objects
            candidate_investments: Dict of potential new investments to consider
            optimization_goals: Dict with weights for different optimization goals
            constraints: Dict of constraints to apply during optimization
            
        Returns:
            PortfolioOptimizationResult with recommended changes
        """
        with self.measure_performance("portfolio_optimization"):
            # Extract optimization weights
            financial_weight = optimization_goals.get("financial_return", 0.5)
            ethical_weight = optimization_goals.get("ethical_alignment", 0.5)
            
            # Current portfolio metrics
            # 1. Analyze current composition
            composition = self.analyze_portfolio_composition(portfolio, investments)
            
            # 2. Calculate current ethical score
            current_ethical_score = 0.0
            if "weighted_overall_score" in composition.ethical_alignment:
                current_ethical_score = composition.ethical_alignment["weighted_overall_score"]
            
            # 3. Extract current risk metrics
            current_risk_metrics = {
                "sector_concentration": composition.concentration_metrics["sector_hhi"],
                "industry_concentration": composition.concentration_metrics["industry_hhi"],
                "holdings_concentration": composition.concentration_metrics["holdings_hhi"]
            }
            
            # Identify holdings to potentially reduce
            holdings_to_reduce = []
            
            # 1. Identify highly concentrated sectors/industries
            concentrated_sectors = {
                sector: weight for sector, weight in composition.sector_breakdown.items()
                if weight > constraints.get("max_sector_weight", 0.3)
            }
            
            concentrated_industries = {
                industry: weight for industry, weight in composition.industry_breakdown.items()
                if weight > constraints.get("max_industry_weight", 0.2)
            }
            
            # 2. Find holdings in concentrated areas
            for holding in portfolio.holdings:
                investment_id = holding.investment_id
                if investment_id in investments:
                    investment = investments[investment_id]
                    
                    # Check if in concentrated sector or industry
                    in_concentrated_sector = investment.sector in concentrated_sectors
                    in_concentrated_industry = investment.industry in concentrated_industries
                    
                    # Check ethical score
                    ethical_score = investment.esg_ratings.overall
                    below_ethical_threshold = ethical_score < constraints.get("min_esg_score", 60)
                    
                    # Calculate financial metrics
                    return_pct = holding.return_percentage
                    
                    # Decision on whether to reduce
                    reduction_reason = None
                    if below_ethical_threshold:
                        reduction_reason = "below_ethical_threshold"
                    elif in_concentrated_sector and return_pct < constraints.get("min_return_for_concentration", 10):
                        reduction_reason = "concentrated_sector_low_return"
                    elif in_concentrated_industry and return_pct < constraints.get("min_return_for_concentration", 10):
                        reduction_reason = "concentrated_industry_low_return"
                    
                    if reduction_reason:
                        holdings_to_reduce.append({
                            "investment_id": investment_id,
                            "name": investment.name,
                            "current_weight": holding.current_value / portfolio.total_value,
                            "reduction_reason": reduction_reason,
                            "esg_score": ethical_score,
                            "return_percentage": return_pct
                        })
            
            # Sort holdings to reduce by priority
            holdings_to_reduce.sort(key=lambda x: (
                0 if x["reduction_reason"] == "below_ethical_threshold" else 1,
                -x["current_weight"]  # Higher weight = higher priority
            ))
            
            # Identify potential new investments
            potential_additions = []
            
            for inv_id, investment in candidate_investments.items():
                # Skip if already in portfolio
                if any(h.investment_id == inv_id for h in portfolio.holdings):
                    continue
                
                # Check ethical criteria
                if investment.esg_ratings.overall < constraints.get("min_esg_score", 60):
                    continue
                    
                # Check for excluded sectors/industries
                if (investment.sector in constraints.get("excluded_sectors", []) or
                    investment.industry in constraints.get("excluded_industries", [])):
                    continue
                    
                # Calculate diversification benefit
                diversification_benefit = self._calculate_diversification_benefit(
                    investment, composition.sector_breakdown, composition.industry_breakdown
                )
                
                # Calculate a combined score based on optimization goals
                ethical_score = investment.esg_ratings.overall / 100.0  # Normalize to 0-1
                
                # Simple proxy for expected return (in reality would use more sophisticated models)
                # This is just for demonstration purposes
                expected_return = 0.08  # Assume 8% baseline
                if investment.sector in ["Technology", "Healthcare"]:
                    expected_return += 0.02
                if "renewable_energy" in investment.positive_practices:
                    expected_return += 0.01
                    
                # Combined score using weighted average
                score_components = [
                    (expected_return, financial_weight),
                    (ethical_score, ethical_weight),
                    (diversification_benefit, 0.2)  # Always include some diversification benefit
                ]
                
                combined_score = FinancialCalculations.calculate_weighted_average(score_components)
                
                potential_additions.append({
                    "investment_id": inv_id,
                    "name": investment.name,
                    "sector": investment.sector,
                    "industry": investment.industry,
                    "esg_score": investment.esg_ratings.overall,
                    "expected_return": expected_return * 100,  # Convert to percentage
                    "diversification_benefit": diversification_benefit,
                    "combined_score": combined_score
                })
            
            # Sort potential additions by combined score
            potential_additions.sort(key=lambda x: x["combined_score"], reverse=True)
            
            # Generate recommended changes
            recommended_changes = []
            
            # Recommend reductions
            for holding in holdings_to_reduce[:3]:  # Limit to top 3 recommendations
                recommended_changes.append({
                    "action": "reduce",
                    "investment_id": holding["investment_id"],
                    "name": holding["name"],
                    "current_weight": holding["current_weight"],
                    "target_weight": max(0, holding["current_weight"] - 0.05),  # Reduce by 5%
                    "reason": holding["reduction_reason"]
                })
            
            # Recommend additions
            for addition in potential_additions[:3]:  # Limit to top 3 recommendations
                recommended_changes.append({
                    "action": "add",
                    "investment_id": addition["investment_id"],
                    "name": addition["name"],
                    "current_weight": 0.0,
                    "target_weight": 0.05,  # Start with 5% allocation
                    "reason": f"high_score_{addition['sector']}",
                    "esg_score": addition["esg_score"],
                    "expected_return": addition["expected_return"]
                })
            
            # Calculate expected improvement
            expected_improvement = {}
            
            # Simplistic estimate of ethical score improvement
            if recommended_changes:
                # Calculate average ESG score of additions
                additions = [change for change in recommended_changes if change["action"] == "add"]
                reductions = [change for change in recommended_changes if change["action"] == "reduce"]
                
                if additions:
                    avg_addition_esg = sum(add["esg_score"] for add in additions) / len(additions)
                    expected_ethical_improvement = (avg_addition_esg - current_ethical_score) * 0.05
                    expected_improvement["ethical_score"] = expected_ethical_improvement
                
                # Estimate diversification improvement
                if composition.concentration_metrics["sector_hhi"] > 0.15:
                    expected_improvement["diversification"] = 5.0  # Percentage points
                else:
                    expected_improvement["diversification"] = 2.0
            
            # Get processing time from performance tracker
            processing_time = self.get_performance_stats().get("portfolio_optimization", {}).get("avg_duration_ms", 0)
            
            return PortfolioOptimizationResult(
                portfolio_id=portfolio.portfolio_id,
                optimization_date=date.today(),
                current_ethical_score=current_ethical_score,
                current_risk_metrics=current_risk_metrics,
                recommended_changes=recommended_changes,
                expected_improvement=expected_improvement,
                optimization_constraints=constraints,
                processing_time_ms=max(1.0, processing_time)
            )
    
    def _map_practice_to_theme(self, practice: str) -> str:
        """Map a company's positive practice to an ESG theme.
        
        Args:
            practice: The positive practice string
            
        Returns:
            The corresponding ESG theme
        """
        # Mapping of practices to themes
        practice_theme_map = {
            "renewable_energy": "renewable_energy",
            "clean_energy": "renewable_energy",
            "solar_power": "renewable_energy",
            "wind_power": "renewable_energy",
            "carbon_reduction": "climate_action",
            "emissions_reduction": "climate_action",
            "climate_initiative": "climate_action",
            "sustainable_development": "climate_action",
            "diversity_initiative": "diversity_equity_inclusion",
            "gender_equality": "diversity_equity_inclusion",
            "inclusive_workplace": "diversity_equity_inclusion",
            "equal_opportunity": "diversity_equity_inclusion",
            "sustainable_agriculture": "sustainable_agriculture",
            "organic_farming": "sustainable_agriculture",
            "sustainable_forestry": "sustainable_agriculture",
            "recycling_program": "circular_economy",
            "waste_reduction": "circular_economy",
            "packaging_reduction": "circular_economy",
            "community_investment": "community_development",
            "affordable_housing": "community_development",
            "education_support": "community_development",
            "ethical_sourcing": "social_justice",
            "fair_trade": "social_justice",
            "labor_rights": "social_justice",
            "human_rights": "social_justice",
            "board_diversity": "good_governance",
            "executive_accountability": "good_governance",
            "transparency_initiative": "good_governance"
        }
        
        # Convert practice to lowercase and remove spaces
        practice_key = practice.lower().replace(" ", "_")
        
        # Return mapped theme or default
        return practice_theme_map.get(practice_key, "other")
    
    def _sector_conflicts_with_constraints(self, sector: str, constraints: Dict[str, Any]) -> bool:
        """Check if reducing a sector would conflict with ethical constraints.
        
        Args:
            sector: The sector to check
            constraints: Dict of ethical constraints
            
        Returns:
            True if there is a conflict, False otherwise
        """
        # If sector is in required sectors, it conflicts with reduction
        if "required_sectors" in constraints:
            if sector in constraints["required_sectors"]:
                return True
        
        # Map sectors to ESG themes for checking required themes
        sector_theme_map = {
            "Renewable Energy": "renewable_energy",
            "Clean Technology": "renewable_energy",
            "Sustainable Agriculture": "sustainable_agriculture",
            "Healthcare": "social_impact",
            "Education": "social_impact",
            "Green Building": "climate_action"
        }
        
        # If sector maps to a required theme, it conflicts
        if "required_themes" in constraints and sector in sector_theme_map:
            theme = sector_theme_map[sector]
            if theme in constraints["required_themes"]:
                return True
        
        return False
    
    def _calculate_diversification_benefit(
        self, 
        investment: Investment,
        current_sector_breakdown: Dict[str, float],
        current_industry_breakdown: Dict[str, float]
    ) -> float:
        """Calculate the diversification benefit of adding an investment.
        
        Args:
            investment: The investment to evaluate
            current_sector_breakdown: Current sector weights
            current_industry_breakdown: Current industry weights
            
        Returns:
            Diversification benefit score (0-1)
        """
        benefit = 0.0
        
        # Check if sector is underrepresented
        sector = investment.sector
        if sector not in current_sector_breakdown:
            benefit += 0.5  # New sector adds significant diversification
        elif current_sector_breakdown[sector] < 0.1:
            benefit += 0.3  # Underrepresented sector
        
        # Check if industry is underrepresented
        industry = investment.industry
        if industry not in current_industry_breakdown:
            benefit += 0.5  # New industry adds significant diversification
        elif current_industry_breakdown[industry] < 0.05:
            benefit += 0.3  # Underrepresented industry
        
        # Cap at 1.0
        return min(1.0, benefit)

    def analyze_esg_theme_concentration(
        self,
        portfolio: Portfolio, 
        investments: Dict[str, Investment],
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze ESG theme concentration in a portfolio using common analysis framework.
        
        Args:
            portfolio: The portfolio to analyze
            investments: Dict mapping investment IDs to Investment objects
            
        Returns:
            Dictionary with theme concentration analysis
        """
        with self.measure_performance("esg_theme_concentration_analysis"):
            # Define ESG themes and their related positive practices
            esg_theme_practices = {
                "climate_action": [
                    "carbon_reduction", "emissions_reduction", "renewable_energy",
                    "climate_initiative", "sustainable_development", "clean_energy"
                ],
                "renewable_energy": [
                    "renewable_energy", "clean_energy", "solar_power", "wind_power",
                    "energy_efficiency"
                ],
                "social_justice": [
                    "ethical_sourcing", "fair_trade", "labor_rights", "human_rights",
                    "affordable_housing", "living_wage"
                ],
                "diversity_equity_inclusion": [
                    "diversity_initiative", "gender_equality", "inclusive_workplace",
                    "equal_opportunity", "board_diversity"
                ],
                "sustainable_agriculture": [
                    "sustainable_agriculture", "organic_farming", "sustainable_forestry",
                    "regenerative_farming"
                ],
                "circular_economy": [
                    "recycling_program", "waste_reduction", "packaging_reduction",
                    "product_lifecycle_management", "circular_design"
                ],
                "water_conservation": [
                    "water_efficiency", "clean_water", "water_treatment",
                    "ocean_conservation"
                ],
                "good_governance": [
                    "board_diversity", "executive_accountability", "transparency_initiative",
                    "ethical_business", "anti_corruption"
                ]
            }
            
            # Calculate total portfolio value
            total_portfolio_value = portfolio.total_value
            
            # Initialize theme weights
            theme_weights = {theme: 0.0 for theme in esg_theme_practices}
            theme_holdings = {theme: [] for theme in esg_theme_practices}
            
            # Analyze each holding
            for holding in portfolio.holdings:
                investment_id = holding.investment_id
                if investment_id not in investments:
                    continue
                    
                investment = investments[investment_id]
                holding_weight = holding.current_value / total_portfolio_value
                
                # Check positive practices for theme alignment
                for practice in investment.positive_practices:
                    for theme, practices in esg_theme_practices.items():
                        if any(p.lower() in practice.lower() for p in practices):
                            # Weight by ESG score - higher scores get more theme weight
                            esg_factor = investment.esg_ratings.overall / 100
                            theme_weights[theme] += holding_weight * esg_factor
                            
                            if investment_id not in theme_holdings[theme]:
                                theme_holdings[theme].append(investment_id)
                
                # Check sector-based theme alignment
                sector_theme_map = {
                    "Energy": ["renewable_energy", "climate_action"],
                    "Technology": ["circular_economy"],
                    "Utilities": ["renewable_energy", "water_conservation"],
                    "Consumer Staples": ["sustainable_agriculture"],
                    "Financial Services": ["good_governance"]
                }
                
                if investment.sector in sector_theme_map:
                    for theme in sector_theme_map[investment.sector]:
                        # Add sector-based weight, but at lower intensity than direct practices
                        sector_factor = 0.5 * (investment.esg_ratings.overall / 100)
                        theme_weights[theme] += holding_weight * sector_factor
                        
                        if investment_id not in theme_holdings[theme]:
                            theme_holdings[theme].append(investment_id)
            
            # Calculate diversity metrics using common financial calculations
            non_zero_themes = sum(1 for weight in theme_weights.values() if weight > 0.05)
            
            # Calculate concentration index using HHI
            theme_weight_values = list(theme_weights.values())
            hhi = FinancialCalculations.calculate_hhi(theme_weight_values)
            
            # Normalize theme weights to ensure they sum to 1.0
            total_theme_weight = sum(theme_weights.values())
            if total_theme_weight > 0:
                for theme in theme_weights:
                    theme_weights[theme] /= total_theme_weight
            
            # Build result structure
            themes_data = {}
            for theme, weight in theme_weights.items():
                if weight > 0:
                    themes_data[theme] = {
                        "weight": weight,
                        "holdings": theme_holdings[theme],
                        "holdings_count": len(theme_holdings[theme])
                    }
            
            # Sort themes by weight for easy analysis
            sorted_themes = {
                theme: themes_data[theme]
                for theme in sorted(themes_data, key=lambda t: themes_data[t]["weight"], reverse=True)
            }
            
            result = {
                "themes": sorted_themes,
                "diversity": {
                    "theme_count": non_zero_themes,
                    "concentration_index": hhi,
                    "balanced_exposure": hhi < 0.25,
                    "dominant_theme": max(theme_weights.items(), key=lambda x: x[1])[0] if theme_weights else None
                }
            }
            
            return result

    def calculate_risk_adjusted_esg_performance(
        self,
        portfolio: Portfolio,
        investments: Dict[str, Investment],
        volatility_data: Dict[str, float],
        return_data: Dict[str, float],
        **kwargs
    ) -> Dict[str, Any]:
        """Calculate risk-adjusted ESG performance metrics using common financial calculations.
        
        Args:
            portfolio: The portfolio to analyze
            investments: Dict mapping investment IDs to Investment objects
            volatility_data: Dict mapping investment IDs to volatility values
            return_data: Dict mapping investment IDs to return values
            
        Returns:
            Dictionary with risk-adjusted ESG metrics
        """
        with self.measure_performance("risk_adjusted_esg_performance"):
            total_portfolio_value = portfolio.total_value
            
            # Initialize portfolio-level metrics
            portfolio_esg_score = 0.0
            portfolio_risk = 0.0
            portfolio_return = 0.0
            by_investment = {}
            
            # Collect weights and scores for common calculations
            esg_weights = []
            risk_weights = []
            return_weights = []
            
            # Process each holding
            for holding in portfolio.holdings:
                investment_id = holding.investment_id
                if investment_id not in investments:
                    continue
                    
                investment = investments[investment_id]
                weight = holding.current_value / total_portfolio_value
                
                # Get ESG score
                esg_score = investment.esg_ratings.overall
                
                # Get risk (volatility) and return data
                risk = volatility_data.get(investment_id, 0.15)  # Default if missing
                investment_return = return_data.get(investment_id, 0.08)  # Default if missing
                
                # Calculate risk-adjusted ESG score
                # Formula: ESG score divided by risk, normalized
                # Higher risk should reduce the effective ESG score
                risk_adjusted_esg = esg_score / (1 + risk)
                
                # Calculate risk-return ratio using common calculations
                risk_return_ratio = FinancialCalculations.calculate_roi(investment_return - 0.02, risk) if risk > 0 else 0
                
                # Collect for weighted averages
                esg_weights.append((esg_score, weight))
                risk_weights.append((risk, weight))
                return_weights.append((investment_return, weight))
                
                # Store investment-level metrics
                by_investment[investment_id] = {
                    "name": investment.name,
                    "weight": weight,
                    "esg_score": esg_score,
                    "risk": risk,
                    "return": investment_return,
                    "risk_adjusted_esg_score": risk_adjusted_esg,
                    "risk_return_ratio": risk_return_ratio
                }
            
            # Calculate portfolio-level metrics using common calculations
            portfolio_esg_score = FinancialCalculations.calculate_weighted_average(esg_weights) if esg_weights else 0
            portfolio_risk = FinancialCalculations.calculate_weighted_average(risk_weights) if risk_weights else 0
            portfolio_return = FinancialCalculations.calculate_weighted_average(return_weights) if return_weights else 0
            
            # Calculate portfolio-level risk-adjusted metrics
            portfolio_risk_adjusted_esg = portfolio_esg_score / (1 + portfolio_risk)
            
            # Calculate Sharpe ratio using common calculations
            risk_free_rate = 0.02
            portfolio_sharpe = FinancialCalculations.calculate_sharpe_ratio(portfolio_return, risk_free_rate, portfolio_risk)
            
            # Calculate risk-return-ESG ratio (custom metric combining all three factors)
            # Higher is better: (return * ESG score) / risk
            risk_return_esg_ratio = (portfolio_return * portfolio_esg_score / 100) / portfolio_risk if portfolio_risk > 0 else 0
            
            # Compile result
            result = {
                "overall": {
                    "esg_score": portfolio_esg_score,
                    "risk": portfolio_risk,
                    "return": portfolio_return,
                    "risk_adjusted_esg_score": portfolio_risk_adjusted_esg,
                    "sharpe_ratio": portfolio_sharpe,
                    "risk_return_esg_ratio": risk_return_esg_ratio
                },
                "by_investment": by_investment
            }
            
            return result


# Backward compatibility alias
PortfolioAnalysisSystem = SociallyResponsiblePortfolioAnalysisSystem