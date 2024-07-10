import numpy as np
from sharpe_ratio import get_risk_free_rate

def double_sharpe(portfolio_returns, risk_free_rate=None):
    
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()
    
    # Convert annual risk-free rate to daily rate
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    
    # Calculate excess returns
    excess_returns = portfolio_returns - 2 * daily_risk_free_rate
    
    # Calculate Sharpe ratio
    double_sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
    return double_sharpe
