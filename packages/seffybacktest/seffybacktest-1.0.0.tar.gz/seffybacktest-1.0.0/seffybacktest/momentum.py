import matplotlib.pyplot as plt


def calculate_momentum(returns, window=14, plot=False):
    """
    Calculate the momentum for a given returns series.
    
    Parameters:
    returns (pd.Series): A pandas Series of portfolio returns.
    window (int): The number of periods to use for momentum calculation. Default is 14.
    plot (bool): Whether to plot the momentum. Default is False.
    
    Returns:
    pd.Series: A pandas Series with the calculated momentum values.
    """
    # Calculate cumulative returns
    cum_returns = (1 + returns).cumprod()
    
    # Calculate momentum
    momentum = cum_returns.pct_change(periods=window)

    # # Prompt user option to print the momentum plot
    # if plot:
    #     plt.figure(figsize=(12, 6))
    #     plt.plot(momentum.index, momentum, label='Momentum')
    #     plt.axhline(y=0, color='r', linestyle='--')
    #     plt.title(f'{window}-day Momentum')
    #     plt.xlabel('Date')
    #     plt.ylabel('Momentum')
    #     plt.legend()
    #     plt.show()

    return momentum

