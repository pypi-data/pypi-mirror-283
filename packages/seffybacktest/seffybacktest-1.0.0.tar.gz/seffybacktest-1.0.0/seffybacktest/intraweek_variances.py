import numpy as np
import pandas as pd
import datetime as dt

def calculate_intraweek_variances(portfolio_returns):
    """
    Calculate intraweek variances of portfolio returns.
    
    Parameters:
    portfolio_returns (pd.Series): Daily portfolio returns with a DatetimeIndex
    
    Returns:
    pd.Series: Weekly variances of portfolio returns
    """
    # Ensure the index is DatetimeIndex
    if not isinstance(portfolio_returns.index, pd.DatetimeIndex):
        raise ValueError("portfolio_returns must have a DatetimeIndex")

    # Group returns by week
    weekly_groups = portfolio_returns.groupby(pd.Grouper(freq='W'))

    # Calculate variance for each week
    intraweek_variances = weekly_groups.apply(lambda x: np.var(x, ddof=1) if len(x) > 1 else np.nan)

    return intraweek_variances

def analyze_portfolio_volatility(portfolio_returns, interactive=False, 
                                 return_avg_variance=True, 
                                 return_highest_week=True, 
                                 return_highest_variance=True):
    """
    Analyze portfolio volatility using intraweek variances.
    
    Parameters:
    portfolio_returns (pd.Series): Daily portfolio returns with a DatetimeIndex
    interactive (bool): If True, prompts user for input on what to return
    return_avg_variance (bool): Whether to return average intraweek variance
    return_highest_week (bool): Whether to return the week with highest variance
    return_highest_variance (bool): Whether to return the highest variance value
    
    Returns:
    dict: Analysis results based on user preferences or function parameters
    """
    if interactive:
        return_avg_variance = input("Return average intraweek variance? (Y/N): ").upper() == 'Y'
        return_highest_week = input("Return week with highest variance? (Y/N): ").upper() == 'Y'
        return_highest_variance = input("Return highest variance value? (Y/N): ").upper() == 'Y'

    # Calculate intraweek variances
    intraweek_vars = calculate_intraweek_variances(portfolio_returns)

    results = {}

    if return_avg_variance:
        results["average_intraweek_variance"] = np.mean(intraweek_vars)

    if return_highest_week:
        highest_week = intraweek_vars.idxmax()
        results["highest_variance_week"] = highest_week.date()

    if return_highest_variance:
        results["highest_variance"] = intraweek_vars.max()

    return results


