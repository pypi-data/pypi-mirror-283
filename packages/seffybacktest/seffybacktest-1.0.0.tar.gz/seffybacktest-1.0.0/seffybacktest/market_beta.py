import yfinance as yf


def beta(portfolio_returns, ticker=None):
    # Extract start and end dates from the portfolio returns DataFrame
    start_date = portfolio_returns.index[0]
    end_date = portfolio_returns.index[-1]
    
    # Calculate ticker returns for the same period, using user input if necessary
    if ticker is None:
        ticker = input("Enter the benchmark ticker symbol (Enter for default: ^GSPC): ").strip()
        if ticker == "":
            ticker = "^GSPC"
    sp500_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    sp500_returns = sp500_data['Close'].pct_change().dropna()

    # Align portfolio and S&P 500 returns based on common dates
    common_dates = portfolio_returns.index.intersection(sp500_returns.index)
    portfolio_returns = portfolio_returns.loc[common_dates]
    sp500_returns = sp500_returns.loc[common_dates]
    if sp500_returns.index.tz is not None:
        sp500_returns.index = sp500_returns.index.tz_localize(None)

    # Calculate beta
    covariance = portfolio_returns.cov(sp500_returns)
    variance = sp500_returns.var()
    beta = covariance / variance
    
    return beta


