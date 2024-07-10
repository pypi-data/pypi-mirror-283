import numpy as np

def average_return(portfolio_returns):
    """
    Calculate the average return of a portfolio.
    
    Parameters:
    portfolio_returns (array-like): Array of portfolio returns
    
    Returns:
    float: Average return of the portfolio
    """
    # Convert input to numpy array if it's not already
    returns = np.array(portfolio_returns)
  

    # Calculate the average return
    avg_return = np.mean(returns)
    
    return avg_return

