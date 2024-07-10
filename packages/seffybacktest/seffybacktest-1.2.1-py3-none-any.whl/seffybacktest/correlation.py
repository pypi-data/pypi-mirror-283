import yfinance as yf

def correlation_with_index(portfolio_returns, ticker=None):
    """
    Calculate the correlation between portfolio returns and an index.
    
    Parameters:
    portfolio_returns (pandas.Series): Daily returns of the portfolio
    
    Returns:
    float: Correlation coefficient
    string: Ticker symbol of the index
    """
    # Prompt user for index choice
    if ticker is None:
        index_ticker = input("Enter a ticker for correlation analysis (Enter for S&P 500): ").strip()
    else:
        index_ticker = ticker
        
    # Download index data
    index_data = yf.download(index_ticker, start=portfolio_returns.index[0], end=portfolio_returns.index[-1])
    
    # Calculate index returns
    index_returns = index_data['Adj Close'].pct_change().dropna()
    
    # Align portfolio and index returns based on common dates
    common_dates = portfolio_returns.index.intersection(index_returns.index)
    portfolio_returns = portfolio_returns.loc[common_dates]
    index_returns = index_returns.loc[common_dates]
    index_returns.index = index_returns.index.tz_localize(None)
    
    # Calculate correlation
    correlation = portfolio_returns.corr(index_returns)
    
    return correlation


