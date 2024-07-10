import numpy as np
from sharpe_ratio import get_risk_free_rate

def modified_sharpe(portfolio_returns, risk_free_rate=None):
    """
    Calculate the Israelsen Modified Sharpe Ratio for a given portfolio.

    Parameters:
    portfolio_returns (pd.Series): Daily returns of the portfolio
    risk_free_rate (float): Annual risk-free rate. If None, it will be fetched using get_risk_free_rate()

    Returns:
    float: Israelsen Modified Sharpe Ratio
    """
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()

    # Convert annual risk-free rate to daily rate
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1

    # Calculate excess returns
    excess_returns = portfolio_returns - daily_risk_free_rate

    # Calculate annualized excess return
    annualized_excess_return = excess_returns.mean() * 252

    # Calculate annualized standard deviation
    annualized_std = portfolio_returns.std() * np.sqrt(252)

    # Calculate Israelsen Modified Sharpe Ratio
    if annualized_excess_return >= 0:
        modified_sharpe = annualized_excess_return / annualized_std
    else:
        modified_sharpe = annualized_excess_return * annualized_std

    return modified_sharpe

