"""Common data models for the ethical finance package."""

from typing import Dict, List, Optional, Any, Union
from datetime import date, datetime
from dataclasses import dataclass, field


@dataclass
class ESGRating:
    """Environmental, Social, and Governance ratings for an investment."""
    
    environmental: int
    social: int
    governance: int
    overall: int
    
    def __post_init__(self):
        """Validate that the overall score is consistent with component scores."""
        # Check if overall is within a reasonable range of the average
        component_avg = (self.environmental + self.social + self.governance) / 3
        if abs(self.overall - component_avg) > 15:  # Allow some variation in methodology
            raise ValueError(f"Overall score {self.overall} is too different from component average {component_avg:.1f}")


@dataclass
class Investment:
    """Model representing an investment opportunity with ESG attributes."""
    
    id: str
    name: str
    sector: str
    industry: str
    market_cap: float
    price: float
    esg_ratings: Union[ESGRating, Dict[str, Any]]
    carbon_footprint: float
    renewable_energy_use: float
    diversity_score: float
    board_independence: float
    controversies: List[str] = field(default_factory=list)
    positive_practices: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Convert dictionary esg_ratings to ESGRating object if necessary."""
        if isinstance(self.esg_ratings, dict):
            self.esg_ratings = ESGRating(
                environmental=self.esg_ratings["environmental"],
                social=self.esg_ratings["social"],
                governance=self.esg_ratings["governance"],
                overall=self.esg_ratings["overall"]
            )
    
    @property
    def has_major_controversies(self) -> bool:
        """Check if the investment has major controversies."""
        major_issues = ["human_rights", "fraud", "corruption", "environmental_disaster"]
        return any(issue in self.controversies for issue in major_issues)


@dataclass
class InvestmentHolding:
    """A specific holding of an investment in a portfolio."""
    
    investment_id: str
    shares: float
    purchase_price: float
    purchase_date: date
    current_price: float
    current_value: float
    
    def __post_init__(self):
        """Validate that current_value = shares * current_price."""
        expected_value = self.shares * self.current_price
        if abs(self.current_value - expected_value) > 0.01:  # Allow for small rounding errors
            raise ValueError(f"Current value {self.current_value} does not match shares * price {expected_value}")
    
    @property
    def return_percentage(self) -> float:
        """Calculate the percentage return on this holding."""
        return (self.current_price / self.purchase_price - 1) * 100


@dataclass
class Portfolio:
    """A collection of investment holdings."""
    
    portfolio_id: str
    name: str
    holdings: List[Union[InvestmentHolding, Dict[str, Any]]]
    total_value: float
    cash_balance: float
    creation_date: date
    last_updated: date
    
    def __post_init__(self):
        """Validate that total_value equals the sum of all holdings' values and convert dict holdings to InvestmentHolding objects."""
        # Convert dictionary holdings to InvestmentHolding objects
        for i, holding in enumerate(self.holdings):
            if isinstance(holding, dict):
                # Convert any string dates to date objects
                if isinstance(holding.get("purchase_date"), str):
                    holding["purchase_date"] = date.fromisoformat(holding["purchase_date"])
                
                self.holdings[i] = InvestmentHolding(**holding)
        
        # Now validate total value
        holdings_sum = sum(holding.current_value for holding in self.holdings)
        if abs(self.total_value - holdings_sum) > 0.01:  # Allow for small rounding errors
            raise ValueError(f"Total value {self.total_value} does not match holdings sum {holdings_sum}")
    
    @property
    def total_assets(self) -> float:
        """Calculate total assets including cash."""
        return self.total_value + self.cash_balance


@dataclass
class ShareholderResolution:
    """Model representing a shareholder resolution with voting results."""
    
    company_id: str
    resolution_id: str
    year: int
    title: str
    category: str
    subcategory: str
    proposed_by: str
    status: str
    votes_for: Optional[float] = None
    votes_against: Optional[float] = None
    abstentions: Optional[float] = None
    company_recommendation: Optional[str] = None
    outcome: Optional[str] = None
    
    def __post_init__(self):
        """Validate that vote percentages sum to approximately 1."""
        if all(val is not None for val in [self.votes_for, self.votes_against, self.abstentions]):
            vote_sum = self.votes_for + self.votes_against + self.abstentions
            if abs(vote_sum - 1.0) > 0.01:  # Allow for small rounding errors
                raise ValueError(f"Vote percentages sum to {vote_sum}, expected 1.0")


@dataclass
class Transaction:
    """Model representing a personal financial transaction."""
    
    id: str
    date: date
    amount: float
    vendor: str
    category: str
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class EthicalCriteria:
    """Customizable ethical screening criteria for investments."""
    
    criteria_id: str
    name: str
    environmental: Dict[str, Any]
    social: Dict[str, Any]
    governance: Dict[str, Any]
    min_overall_score: float
    exclusions: List[str] = field(default_factory=list)
    inclusions: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate that criteria weights are included and sum approximately to 1."""
        # Check that each criteria includes a weight
        for field_name in ['environmental', 'social', 'governance']:
            field_value = getattr(self, field_name)
            if 'weight' not in field_value:
                raise ValueError(f"{field_name} criteria must include a weight")
            
            # Ensure weight is between 0 and 1
            if field_value['weight'] < 0 or field_value['weight'] > 1:
                raise ValueError(f"{field_name} weight must be between 0 and 1")
        
        # Check that weights sum to approximately 1
        weights_sum = (
            self.environmental.get('weight', 0) + 
            self.social.get('weight', 0) + 
            self.governance.get('weight', 0)
        )
        if abs(weights_sum - 1.0) > 0.01:  # Allow for small rounding errors
            raise ValueError(f"Criteria weights sum to {weights_sum}, expected 1.0")


@dataclass
class ImpactMetric:
    """Model for defining and tracking impact metrics."""
    
    metric_id: str
    name: str
    category: str
    unit: str
    description: str
    higher_is_better: bool
    data_source: str


@dataclass
class ImpactData:
    """Impact data for a specific investment in a specific year."""
    
    investment_id: str
    year: int
    metrics: Dict[str, float]
    # Additional fields allowed for future extensibility