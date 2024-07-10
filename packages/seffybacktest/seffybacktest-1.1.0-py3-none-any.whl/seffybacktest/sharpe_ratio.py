import numpy as np

def sharpe_ratio(portfolio_returns, risk_free_rate=None):
    
    if risk_free_rate is None:
        risk_free_rate = get_risk_free_rate()
    
    # Convert annual risk-free rate to daily rate
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    
    # Calculate excess returns
    excess_returns = portfolio_returns - daily_risk_free_rate
    
    # Calculate Sharpe ratio
    sharpe = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
    return sharpe

def get_risk_free_rate():
    default_rate = 0.0425  # 4.25%
    user_input = input(f"Enter the annual risk-free rate (Enter for default: {default_rate:.2%}): ")
    
    if user_input.strip() == "":
        return default_rate
    else:
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Using default rate.")
            return default_rate

