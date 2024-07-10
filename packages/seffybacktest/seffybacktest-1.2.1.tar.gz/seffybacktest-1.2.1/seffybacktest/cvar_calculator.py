from var_calculator import calculate_var

def calculate_cvar(portfolio_returns, confidence_level=0.95):
    """
    Calculate Conditional Value at Risk (CVaR) using the historical method.
    
    Parameters:
    portfolio_returns (pandas.Series): Daily returns of the portfolio
    confidence_level (float): Confidence level for CVaR calculation (default: 0.95)
    
    Returns:
    float: Conditional Value at Risk
    """
    # Calculate VaR
    var = calculate_var(portfolio_returns, confidence_level)
    
    # Calculate CVaR
    cvar = -portfolio_returns[portfolio_returns <= -var].mean()
    
    return cvar

    
