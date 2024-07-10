import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sharpe_ratio import get_risk_free_rate

def alpha(portfolio_returns, ticker = None , risk_free_rate=None):
    """
    Calculate the alpha of a portfolio.

    Parameters:
    portfolio_returns (pd.Series): Daily returns of the portfolio
    benchmark_ticker (str): Ticker symbol for the benchmark index (default is S&P 500)
    risk_free_rate (float): Annualized risk-free rate (if None, it will be fetched)

    Returns:
    float: Annualized alpha of the portfolio
    """
    # Ask user for benchmark ticker
    if ticker is None:
        index_ticker = input("Enter a ticker for correlation analysis (Enter for S&P 500): ").strip()
    else:
        index_ticker = ticker

    
    # Ensure the index is datetime
    portfolio_returns.index = pd.to_datetime(portfolio_returns.index)

    # Get benchmark returns
    start_date = portfolio_returns.index[0]
    end_date = portfolio_returns.index[-1]
    benchmark_data = yf.download(index_ticker, start=start_date, end=end_date)
    benchmark_returns = benchmark_data['Adj Close'].pct_change().dropna()

    # Align dates
    aligned_data = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
    aligned_data.columns = ['Portfolio', 'Benchmark']

    # Calculate excess returns
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()  # Assuming you have this function
    daily_rf = (1 + risk_free_rate) ** (1/252) - 1

    excess_portfolio_returns = aligned_data['Portfolio'] - daily_rf
    excess_benchmark_returns = aligned_data['Benchmark'] - daily_rf

    # Perform regression
    X = excess_benchmark_returns.values.reshape(-1, 1)
    y = excess_portfolio_returns.values
    model = LinearRegression().fit(X, y)

    # Calculate alpha
    alpha = model.intercept_

    # Annualize alpha
    alpha_annualized = (1 + alpha) ** 252 - 1

    return alpha_annualized

