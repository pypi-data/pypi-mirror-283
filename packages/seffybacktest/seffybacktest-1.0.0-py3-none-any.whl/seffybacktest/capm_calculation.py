import yfinance as yf
from market_beta import beta
from sharpe_ratio import get_risk_free_rate

def calculate_market_return(portfolio_returns):
    """
    Calculate market return using S&P 500 index.
    
    Parameters:
    portfolio_returns (pandas.Series): Daily returns of the portfolio
    
    Returns:
    float: Annualized market return
    """
    # Extract start and end dates from the portfolio returns DataFrame
    start_date = portfolio_returns.index[0]
    end_date = portfolio_returns.index[-1]

    market_data = yf.download("^GSPC", start=start_date, end=end_date)['Adj Close']
    market_return = market_data.pct_change().dropna()
    annualized_return = (1 + market_return.mean()) ** 252 - 1
    return annualized_return

def calculate_capm(portfolio_returns,risk_free_rate=None, ticker=None):
    """
    Calculate expected return using CAPM.
    
    Parameters:
    beta (float): Beta of the portfolio
    risk_free_rate (float): Risk-free rate (annual)
    market_return (float): Expected market return (annual)
    
    Returns:
    float: Expected return according to CAPM
    """
    market_return = calculate_market_return(portfolio_returns)
    calculated_beta = beta(portfolio_returns, ticker)

    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()

    expected_return = risk_free_rate + calculated_beta * (market_return - risk_free_rate)
    return expected_return

