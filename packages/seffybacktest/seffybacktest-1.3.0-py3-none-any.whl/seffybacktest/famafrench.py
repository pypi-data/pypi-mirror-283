import pandas as pd
from sklearn.linear_model import LinearRegression
from .market_beta import beta
from .sharpe_ratio import get_risk_free_rate
from .capm_calculation import calculate_capm  # Assuming this is the function you provided earlier

def get_fama_french_factors(start_date, end_date):
    """
    Fetch Fama-French factors from Kenneth French's data library.
    
    Parameters:
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    pandas.DataFrame: Fama-French factors (Mkt-RF, SMB, HML)
    """
    url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
    
    ff_factors = pd.read_csv(url, skiprows=3, index_col=0)
    ff_factors = ff_factors[ff_factors.index.astype(str).str.isnumeric()]
    
    ff_factors.columns = ['Mkt-RF', 'SMB', 'HML', 'RF']
    ff_factors.index = pd.to_datetime(ff_factors.index, format='%Y%m%d')
    ff_factors.index.name = 'Date'
    
    ff_factors = ff_factors.loc[start_date:end_date]
    
    for col in ff_factors.columns:
        ff_factors[col] = ff_factors[col] / 100
    
    return ff_factors

def calculate_fama_french(portfolio_returns, risk_free_rate=None, ticker=None):
    """
    Calculate expected return using the Fama-French 3-factor model.
    
    Parameters:
    portfolio_returns (pandas.Series): Daily returns of the portfolio
    risk_free_rate (float): Risk-free rate (annual), optional
    
    Returns:
    float: Expected return according to Fama-French 3-factor model
    dict: Factor loadings (betas) for each factor
    """
    start_date = portfolio_returns.index[0]
    end_date = portfolio_returns.index[-1]

    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()
    
    # Calculate CAPM expected return
    capm_return = calculate_capm(portfolio_returns, risk_free_rate, ticker)
    
    # Fetch Fama-French factors
    ff_factors = get_fama_french_factors(start_date, end_date)
    
    # Align dates of portfolio returns and factors
    aligned_data = pd.concat([portfolio_returns, ff_factors[['SMB', 'HML']]], axis=1).dropna()
    
    # Prepare data for regression
    X = aligned_data[['SMB', 'HML']]
    y = portfolio_returns
    
    # Perform regression
    model = LinearRegression().fit(X, y)
    
    # Calculate expected return
    smb_mean = X['SMB'].mean()
    hml_mean = X['HML'].mean()
    smb_sensitivity = model.coef_[0]
    hml_sensitivity = model.coef_[1]
    
    ff_additional_return = smb_sensitivity * smb_mean + hml_sensitivity * hml_mean
    
    expected_return = capm_return + ff_additional_return
    
    # Prepare factor loadings
    factor_loadings = {
        'Mkt-RF': beta(portfolio_returns, ticker),  # Market beta from CAPM
        'SMB': smb_sensitivity,
        'HML': hml_sensitivity
    }
    
    return expected_return
    # return expected_return, factor_loadings

