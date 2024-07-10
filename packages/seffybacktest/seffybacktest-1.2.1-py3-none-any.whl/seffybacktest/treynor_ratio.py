import numpy as np
from sharpe_ratio import get_risk_free_rate

def treynor_ratio(portfolio_returns, beta, risk_free_rate=None):
    
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()

    # Convert annual risk-free rate to daily rate
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    
    # Calculate excess returns
    excess_returns = portfolio_returns - daily_risk_free_rate
    
    # Calculate treynor ratio
    treynor = np.sqrt(252) * excess_returns.mean() / beta
    
    return treynor

