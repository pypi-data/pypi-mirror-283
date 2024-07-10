import matplotlib.pyplot as plt

def calculate_rsi(returns, window=14, plot=False):
    """
    Calculate the Relative Strength Index (RSI) for a given returns series.
    
    Parameters:
    returns (pd.Series): A pandas Series of portfolio returns.
    window (int): The number of periods to use for RSI calculation. Default is 14.
    
    Returns:
    pd.Series: A pandas Series with the calculated RSI values.
    """
    # Calculate gains and losses
    gain = returns.where(returns > 0, 0)
    loss = -returns.where(returns < 0, 0)

    # Calculate average gain and loss
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    # Calculate relative strength
    rs = avg_gain / avg_loss

    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))

    # # Prompt user option to print the RSI plot
    # if plot:
    #     plt.figure(figsize=(12, 6))
    #     plt.plot(rsi.index, rsi, label='RSI')
    #     plt.axhline(y=70, color='r', linestyle='--')
    #     plt.axhline(y=30, color='g', linestyle='--')
    #     plt.title('Relative Strength Index (RSI)')
    #     plt.xlabel('Date')
    #     plt.ylabel('RSI')
    #     plt.legend()
    #     plt.show()
    


    return rsi
