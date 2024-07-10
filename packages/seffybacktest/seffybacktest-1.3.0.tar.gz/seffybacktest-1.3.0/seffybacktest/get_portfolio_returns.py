import yfinance as yf

def get_portfolio_returns(tickers, weights, start_date, end_date):
    """
    Get portfolio returns for given tickers and weights.
    
    Parameters:
    tickers (list): List of stock tickers
    weights (list): List of weights for each stock
    start_date (str): Start date for historical data
    end_date (str): End date for historical data
    
    Returns:
    pandas.Series: Daily returns of the portfolio
    """
    # Download historical data
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    # Calculate daily returns
    returns = data.pct_change().dropna()

    # Calculate portfolio returns
    if len(tickers) == 1:
        portfolio_returns = returns
    else:
        portfolio_returns = (returns * weights).sum(axis=1)

    portfolio_returns.index = portfolio_returns.index.tz_localize(None)


    return portfolio_returns
