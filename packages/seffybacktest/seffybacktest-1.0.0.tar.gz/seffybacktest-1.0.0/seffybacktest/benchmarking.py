import pandas as pd
import yfinance as yf
from market_beta import beta
from market_alpha import alpha

# Define the available indices with more detailed information
indices = {
    "1": {"Ticker": "^GSPC", "Full Name": "S&P 500", "Usage": "large-cap U.S. equities"},
    "2": {"Ticker": "^DJI", "Full Name": "Dow Jones Industrial Average", "Usage": "blue-chip U.S. companies"},
    "3": {"Ticker": "^IXIC", "Full Name": "NASDAQ Composite", "Usage": "U.S. technology and growth stocks"},
    "4": {"Ticker": "^FTSE", "Full Name": "FTSE 100", "Usage": "largest UK companies"},
    "5": {"Ticker": "^GSPTSE", "Full Name": "S&P/TSX Composite Index", "Usage": "broad Canadian market"},
    # "6": {"Ticker": "^TX60", "Full Name": "S&P/TSX 60 Index", "Usage": "large-cap Canadian market"},
    # "7": {"Ticker": "^TXSC", "Full Name": "S&P/TSX SmallCap Index", "Usage": "small-cap Canadian companies"}
}

def get_benchmark_returns(tickers, start_date, end_date):
    """
    Fetch benchmark returns from Yahoo Finance for multiple indices.
    """
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    benchmark_returns = data.pct_change(fill_method=None).dropna()
    return benchmark_returns

def benchmark_portfolio(portfolio_returns, selected_indices):
    """
    Benchmark the portfolio returns against the selected benchmark returns.
    """
    start_date = (portfolio_returns.index.min() - pd.Timedelta(days=5)).strftime('%Y-%m-%d')
    end_date = portfolio_returns.index.max().strftime('%Y-%m-%d')
    
    tickers = [index['Ticker'] for index in selected_indices]
    benchmark_returns = get_benchmark_returns(tickers, start_date, end_date)
    
    combined_returns = pd.concat([portfolio_returns, benchmark_returns], axis=1)
    combined_returns.columns = ['Portfolio'] + [index['Full Name'] for index in selected_indices]
    
    combined_returns = combined_returns.dropna()
    
    return combined_returns

def run_benchmark_analysis(portfolio_returns, risk_free_rate):
    """
    Run the benchmarking analysis based on user input.
    
    Parameters:
    portfolio_returns (pd.Series): Daily returns of the portfolio
    
    Returns:
    pd.DataFrame: DataFrame with portfolio and benchmark returns
    dict: Additional analysis results
    """
    # Display the menu
    print("Available benchmark indices:")
    for key, value in indices.items():
        print(f"{key}: {value['Ticker']}: {value['Full Name']}: {value['Usage']}")

    # Get user choices
    choices = input("Enter the numbers of your choices (comma-separated, e.g., 1,3,5): ").split(',')
    selected_indices = [indices[choice.strip()] for choice in choices if choice.strip() in indices]

    if not selected_indices:
        print("No valid choices. Exiting.")
        return None, None

    # Benchmark the portfolio
    results = benchmark_portfolio(portfolio_returns, selected_indices)
    
    # Calculate additional metrics
    correlations = results.corr()['Portfolio'].sort_values(ascending=False)
    annualized_returns = (1 + results.mean()) ** 252 - 1
    
        # calculate beta for every ticker chosen
    betas = []
    for index in selected_indices:
        betas.append(beta(portfolio_returns, index['Ticker']))
    betas = pd.Series(betas, index=[index['Full Name'] for index in selected_indices])
    betas = betas.sort_values(ascending=False)

    alphas = []
    for index in selected_indices:
        alphas.append(alpha(portfolio_returns, index['Ticker'], risk_free_rate))
    alphas = pd.Series(alphas, index=[index['Full Name'] for index in selected_indices])
    alphas = alphas.sort_values(ascending=False)


    analysis_results = {
        "alphas": alphas,
        "betas": betas,
        "correlations": correlations,
        "annualized_returns": annualized_returns
    }

    
    # Display the results
    print("\nBenchmarking results:")
    print(results.head())
    print("\nShape of results:", results.shape)
    print("\nAlphas:")
    print(alphas)
    print("\nBetas:")
    print(betas)
    print("\nCorrelations with Portfolio:")
    print(correlations)
    print("\nAnnualized Returns:")
    print(annualized_returns)
    
    # Optional: save results to CSV
    save_option = input("Do you want to save the results to a CSV file? (y/n): ").lower()
    if save_option == 'y':
        filename = input("Enter the filename (e.g., benchmark_results.csv): ")
        results.to_csv(filename)
        print(f"Results saved to {filename}")

    return results, analysis_results


 

    
