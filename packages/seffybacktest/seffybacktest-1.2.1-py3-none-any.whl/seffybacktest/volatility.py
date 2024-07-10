import numpy as np

def calculate_portfolio_volatility(portfolio_returns, annualize=False):
    """
    Calculate the volatility of portfolio returns.
    
    Parameters:
    portfolio_returns (pandas.Series): Daily returns of the portfolio
    
    Returns:
    float: Portfolio volatility
    """
    # Calculate daily volatility
    daily_volatility = np.std(portfolio_returns)

    if annualize:
        return daily_volatility * np.sqrt(252)
    else:
        return daily_volatility

    # user_input = input(f"Annualize Volatility? (y/n): ")

    # if user_input.strip() == "y":
    #     return daily_volatility * np.sqrt(252)
    # elif user_input.strip() == "n":
    #     return daily_volatility
    # else:
    #     return daily_volatility

