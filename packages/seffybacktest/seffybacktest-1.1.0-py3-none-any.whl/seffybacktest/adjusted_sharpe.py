import pandas as pd
import numpy as np
from scipy import stats
from sharpe_ratio import get_risk_free_rate

def adjusted_sharpe(portfolio_returns, risk_free_rate=None):
    """
    Calculate the Adjusted Sharpe Ratio for Skewness for a given portfolio.

    Parameters:
    portfolio_returns (pd.Series): Daily returns of the portfolio
    risk_free_rate (float): Annual risk-free rate. If None, it will be fetched using get_risk_free_rate()

    Returns:
    float: Adjusted Sharpe Ratio for Skewness
    """
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()

    # Convert annual risk-free rate to daily rate
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1

    # Calculate excess returns
    excess_returns = portfolio_returns - daily_risk_free_rate

    # Calculate annualized Sharpe ratio
    sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

    # Calculate skewness and kurtosis
    skewness = stats.skew(excess_returns)
    kurtosis = stats.kurtosis(excess_returns)

    # Calculate adjusted Sharpe ratio
    adjusted_sharpe = sharpe_ratio * (1 + (skewness / 6) * sharpe_ratio - ((kurtosis - 3) / 24) * sharpe_ratio**2)

    return adjusted_sharpe

