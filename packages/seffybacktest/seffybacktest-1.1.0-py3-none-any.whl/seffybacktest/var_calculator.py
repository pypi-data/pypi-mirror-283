def calculate_var(portfolio_returns, confidence_level=0.95):
    """
    Calculate Value at Risk (VaR) using the historical method.
    
    Parameters:
    portfolio_returns (pandas.Series): Daily returns of the portfolio
    confidence_level (float): Confidence level for VaR calculation (default: 0.95)
    
    Returns:
    float: Value at Risk
    """
    # Sort returns from worst to best
    sorted_returns = portfolio_returns.sort_values()
    
    # Find the index at the given confidence level
    index = int((1 - confidence_level) * len(sorted_returns))
    
    # Return the VaR
    return -sorted_returns.iloc[index]
