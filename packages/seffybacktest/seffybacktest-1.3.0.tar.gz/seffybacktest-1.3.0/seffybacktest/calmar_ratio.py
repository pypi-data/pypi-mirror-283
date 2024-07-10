
def calculate_calmar_ratio(portfolio_returns, window=36):
    """
    Calculate the Calmar Ratio for a given portfolio.

    Parameters:
    portfolio_returns (pd.Series): Daily returns of the portfolio
    window (int): The number of months to consider for the calculation. Default is 36 (3 years).

    Returns:
    float: Calmar Ratio
    """
    # Convert daily returns to cumulative returns
    cumulative_returns = (1 + portfolio_returns).cumprod()

    # Calculate the running maximum
    running_max = cumulative_returns.cummax()

    # Calculate the drawdown
    drawdown = (cumulative_returns - running_max) / running_max

    # Calculate the maximum drawdown
    max_drawdown = drawdown.min()

    # Calculate the annualized return
    total_return = cumulative_returns.iloc[-1] - 1
    annualized_return = (1 + total_return) ** (252 / len(portfolio_returns)) - 1

    # Calculate Calmar Ratio
    calmar_ratio = annualized_return / abs(max_drawdown)

    return calmar_ratio

