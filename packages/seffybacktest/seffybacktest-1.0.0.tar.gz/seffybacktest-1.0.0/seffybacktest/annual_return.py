def annual_return(portfolio_returns):
    """
    Calculate the annualized return of a portfolio.

    Parameters:
    portfolio_returns (pd.Series): Daily returns of the portfolio
    
    """
    cumulative_returns = (1 + portfolio_returns).cumprod()
    total_return = cumulative_returns.iloc[-1] - 1
    annualized_return = (1 + total_return) ** (12 / (len(portfolio_returns) / 252)) - 1

    return annualized_return


