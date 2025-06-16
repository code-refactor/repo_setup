from decimal import Decimal, ROUND_HALF_UP
from typing import List, Tuple, Optional, Dict
from datetime import datetime, timedelta
import calendar


class FinancialCalculations:
    """Core financial math operations used across all persona implementations."""
    
    @staticmethod
    def calculate_compound_growth(principal: Decimal, rate: Decimal, periods: int, 
                                 compounding_frequency: int = 1) -> Decimal:
        """
        Calculate compound growth with configurable compounding frequency.
        
        Args:
            principal: Initial principal amount
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%)
            periods: Number of years
            compounding_frequency: Times per year compounding occurs (1=annual, 12=monthly)
        """
        if periods == 0:
            return principal
        
        adjusted_rate = rate / compounding_frequency
        total_periods = periods * compounding_frequency
        
        growth_factor = (Decimal('1') + adjusted_rate) ** total_periods
        return (principal * growth_factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_present_value(future_value: Decimal, rate: Decimal, periods: int) -> Decimal:
        """Calculate present value of future cash flow."""
        if periods == 0:
            return future_value
        
        discount_factor = (Decimal('1') + rate) ** periods
        return (future_value / discount_factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_net_present_value(cash_flows: List[Tuple[int, Decimal]], 
                                   discount_rate: Decimal) -> Decimal:
        """
        Calculate NPV of a series of cash flows.
        
        Args:
            cash_flows: List of (period, amount) tuples
            discount_rate: Discount rate as decimal
        """
        npv = Decimal('0')
        
        for period, amount in cash_flows:
            if period == 0:
                npv += amount
            else:
                pv = FinancialCalculations.calculate_present_value(amount, discount_rate, period)
                npv += pv
        
        return npv.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_internal_rate_of_return(cash_flows: List[Tuple[int, Decimal]], 
                                        initial_guess: Decimal = Decimal('0.1')) -> Optional[Decimal]:
        """
        Calculate IRR using Newton-Raphson method.
        
        Args:
            cash_flows: List of (period, amount) tuples
            initial_guess: Initial guess for IRR (default 10%)
        """
        if not cash_flows:
            return None
        
        rate = initial_guess
        tolerance = Decimal('0.000001')
        max_iterations = 100
        
        for _ in range(max_iterations):
            npv = Decimal('0')
            npv_derivative = Decimal('0')
            
            for period, amount in cash_flows:
                if period == 0:
                    npv += amount
                else:
                    discount_factor = (Decimal('1') + rate) ** period
                    npv += amount / discount_factor
                    npv_derivative -= (amount * period) / (discount_factor * (Decimal('1') + rate))
            
            if abs(npv) < tolerance:
                return rate.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            
            if npv_derivative == 0:
                break
            
            rate = rate - (npv / npv_derivative)
        
        return None  # Failed to converge
    
    @staticmethod
    def calculate_roi(gain: Decimal, cost: Decimal) -> Decimal:
        """Calculate return on investment as percentage."""
        if cost == 0:
            return Decimal('0')
        
        roi = ((gain - cost) / cost) * Decimal('100')
        return roi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_annualized_return(start_value: Decimal, end_value: Decimal, 
                                   years: Decimal) -> Decimal:
        """Calculate annualized return rate."""
        if start_value <= 0 or years <= 0:
            return Decimal('0')
        
        if end_value <= 0:
            return Decimal('-100')  # Total loss
        
        growth_factor = end_value / start_value
        annualized = (growth_factor ** (Decimal('1') / years)) - Decimal('1')
        return (annualized * Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[Decimal], risk_free_rate: Decimal = Decimal('0.02')) -> Decimal:
        """
        Calculate Sharpe ratio for risk-adjusted returns.
        
        Args:
            returns: List of periodic returns (as decimals)
            risk_free_rate: Risk-free rate (annual, as decimal)
        """
        if not returns or len(returns) < 2:
            return Decimal('0')
        
        float_returns = [float(r) for r in returns]
        
        # Calculate mean excess return
        mean_return = Decimal(str(sum(float_returns) / len(float_returns)))
        excess_return = mean_return - risk_free_rate
        
        # Calculate standard deviation
        variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
        std_dev = variance.sqrt()
        
        if std_dev == 0:
            return Decimal('0')
        
        sharpe = excess_return / std_dev
        return sharpe.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_tax_bracket(income: Decimal, brackets: List[Tuple[Decimal, Decimal]]) -> Dict[str, Decimal]:
        """
        Calculate tax owed based on progressive tax brackets.
        
        Args:
            income: Taxable income
            brackets: List of (threshold, rate) tuples sorted by threshold
        """
        if income <= 0:
            return {'tax_owed': Decimal('0'), 'effective_rate': Decimal('0'), 'marginal_rate': Decimal('0')}
        
        tax_owed = Decimal('0')
        previous_threshold = Decimal('0')
        marginal_rate = Decimal('0')
        
        for threshold, rate in brackets:
            if income <= threshold:
                # Tax on remaining income at this bracket
                taxable_in_bracket = income - previous_threshold
                tax_owed += taxable_in_bracket * rate
                marginal_rate = rate
                break
            else:
                # Tax on full bracket
                taxable_in_bracket = threshold - previous_threshold
                tax_owed += taxable_in_bracket * rate
                previous_threshold = threshold
                marginal_rate = rate
        else:
            # Income exceeds highest bracket
            if brackets:
                remaining_income = income - previous_threshold
                highest_rate = brackets[-1][1]
                tax_owed += remaining_income * highest_rate
                marginal_rate = highest_rate
        
        effective_rate = (tax_owed / income) * Decimal('100') if income > 0 else Decimal('0')
        
        return {
            'tax_owed': tax_owed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'effective_rate': effective_rate.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'marginal_rate': (marginal_rate * Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        }
    
    @staticmethod
    def calculate_loan_payment(principal: Decimal, annual_rate: Decimal, 
                              years: int, payments_per_year: int = 12) -> Decimal:
        """Calculate loan payment amount."""
        if annual_rate == 0:
            return principal / (years * payments_per_year)
        
        monthly_rate = annual_rate / payments_per_year
        total_payments = years * payments_per_year
        
        payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / \
                  ((1 + monthly_rate) ** total_payments - 1)
        
        return payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_amortization_schedule(principal: Decimal, annual_rate: Decimal, 
                                      years: int, payments_per_year: int = 12) -> List[Dict]:
        """Generate loan amortization schedule."""
        payment = FinancialCalculations.calculate_loan_payment(principal, annual_rate, years, payments_per_year)
        
        schedule = []
        remaining_balance = principal
        monthly_rate = annual_rate / payments_per_year
        
        for payment_num in range(1, years * payments_per_year + 1):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = payment - interest_payment
            remaining_balance -= principal_payment
            
            # Ensure balance doesn't go negative due to rounding
            if remaining_balance < Decimal('0.01'):
                principal_payment += remaining_balance
                remaining_balance = Decimal('0')
            
            schedule.append({
                'payment_number': payment_num,
                'payment_amount': payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'principal_payment': principal_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'interest_payment': interest_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'remaining_balance': remaining_balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            })
            
            if remaining_balance == 0:
                break
        
        return schedule
    
    @staticmethod
    def normalize_currency(amount: Decimal, precision: int = 2) -> Decimal:
        """Normalize currency amount to specified precision."""
        quantize_str = '0.' + '0' * precision
        return amount.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def convert_currency(amount: Decimal, from_currency: str, to_currency: str, 
                        exchange_rates: Dict[str, Decimal]) -> Optional[Decimal]:
        """
        Convert currency using provided exchange rates.
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code  
            exchange_rates: Dict of currency_pair -> rate
        """
        if from_currency == to_currency:
            return amount
        
        # Direct conversion
        direct_key = f"{from_currency}_{to_currency}"
        if direct_key in exchange_rates:
            return (amount * exchange_rates[direct_key]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Inverse conversion
        inverse_key = f"{to_currency}_{from_currency}"
        if inverse_key in exchange_rates:
            rate = exchange_rates[inverse_key]
            if rate != 0:
                return (amount / rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return None  # No conversion rate available
    
    @staticmethod
    def calculate_expense_ratio(expenses: Decimal, total_assets: Decimal) -> Decimal:
        """Calculate expense ratio as percentage."""
        if total_assets == 0:
            return Decimal('0')
        
        ratio = (expenses / total_assets) * Decimal('100')
        return ratio.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_debt_to_income_ratio(total_debt_payments: Decimal, 
                                      gross_income: Decimal) -> Decimal:
        """Calculate debt-to-income ratio as percentage."""
        if gross_income == 0:
            return Decimal('0')
        
        ratio = (total_debt_payments / gross_income) * Decimal('100')
        return ratio.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_weighted_average(values_and_weights: List[Tuple[float, float]]) -> float:
        """
        Calculate weighted average from list of (value, weight) tuples.
        
        Args:
            values_and_weights: List of (value, weight) tuples
            
        Returns:
            Weighted average as float
        """
        if not values_and_weights:
            return 0.0
        
        total_weighted_value = 0.0
        total_weight = 0.0
        
        for value, weight in values_and_weights:
            total_weighted_value += value * weight
            total_weight += weight
        
        return total_weighted_value / total_weight if total_weight > 0 else 0.0
    
    @staticmethod
    def calculate_hhi(weights: List[float]) -> float:
        """
        Calculate Herfindahl-Hirschman Index for concentration measurement.
        
        Args:
            weights: List of market share weights (should sum to 1.0)
            
        Returns:
            HHI value (0-1, where 1 is maximum concentration)
        """
        if not weights:
            return 0.0
        
        return sum(weight ** 2 for weight in weights)
    
    @staticmethod
    def calculate_sharpe_ratio(portfolio_return: float, risk_free_rate: float, volatility: float) -> float:
        """
        Calculate Sharpe ratio for risk-adjusted returns.
        
        Args:
            portfolio_return: Portfolio return rate
            risk_free_rate: Risk-free rate
            volatility: Portfolio volatility (standard deviation)
            
        Returns:
            Sharpe ratio
        """
        if volatility == 0:
            return 0.0
        
        return (portfolio_return - risk_free_rate) / volatility