import numpy as np
from .sharpe_ratio import get_risk_free_rate

def sortino_ratio(portfolio_returns, risk_free_rate=None):
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()

    # Convert annual risk-free rate to daily rate
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    
    # Calculate excess returns
    excess_returns = portfolio_returns - daily_risk_free_rate
    
    # Calculate downside returns
    downside_returns = excess_returns[excess_returns < 0]
    
    # Calculate downside deviation (annualized)
    downside_deviation = np.sqrt(252) * np.sqrt(np.mean(downside_returns**2))
    
    # Calculate Sortino ratio
    sortino = np.sqrt(252) * excess_returns.mean() / downside_deviation
    
    return sortino


