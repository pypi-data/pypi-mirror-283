import yfinance as yf
from .get_portfolio_returns import get_portfolio_returns
from .adjusted_sharpe import adjusted_sharpe
from .annual_return import annual_return
from .average_returns import average_return
from .calmar_ratio import calculate_calmar_ratio
from .capm_calculation import calculate_capm, calculate_market_return
from .correlation import correlation_with_index
from .cvar_calculator import calculate_cvar
from .double_sharpe import double_sharpe
from .famafrench import get_fama_french_factors, calculate_fama_french
from .intraweek_variances import calculate_intraweek_variances, analyze_portfolio_volatility
from .market_alpha import alpha
from .market_beta import beta
from .modified_sharpe import modified_sharpe
from .momentum import calculate_momentum
from .rsi import calculate_rsi
from .sharpe_ratio import sharpe_ratio, get_risk_free_rate
from .sortino_ratio import sortino_ratio
from .treynor_ratio import treynor_ratio
from .var_calculator import calculate_var
from .volatility import calculate_portfolio_volatility

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_ui(results, momentum=None, rsi=None):
    def on_closing():
        root.destroy()
        plt.close('all')

    root = tk.Tk()
    root.title("Stock Market Analysis Results")
    root.geometry("1000x800")  # Increased window size

    root.protocol("WM_DELETE_WINDOW", on_closing)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Main results tab
    results_frame = ttk.Frame(notebook)
    notebook.add(results_frame, text="Analysis Results")

    tree = ttk.Treeview(results_frame, columns=('Indicator', 'Value'), show='headings')
    tree.heading('Indicator', text='Indicator')
    tree.heading('Value', text='Value')
    tree.column('Indicator', width=200)
    tree.column('Value', width=400)
    tree.pack(fill=tk.BOTH, expand=True)

    for indicator, value in results.items():
        if indicator not in ['Momentum', 'RSI']:
            if isinstance(value, float):
                formatted_value = f"{value:.4f}"
            else:
                formatted_value = str(value)
            tree.insert('', 'end', values=(indicator, formatted_value))

    # Create separate tabs for Momentum and RSI if they are selected
    if momentum is not None:
        momentum_frame = ttk.Frame(notebook)
        notebook.add(momentum_frame, text="Momentum")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(momentum.index, momentum, label='Momentum', linewidth=1)
        ax.axhline(y=0, color='r', linestyle='--', linewidth=0.8)
        ax.set_title('Momentum', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Momentum', fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.grid(True, linestyle=':', alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=momentum_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    if rsi is not None:
        rsi_frame = ttk.Frame(notebook)
        notebook.add(rsi_frame, text="RSI")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(rsi.index, rsi, label='RSI', linewidth=1)
        ax.axhline(y=70, color='r', linestyle='--', linewidth=0.8)
        ax.axhline(y=30, color='g', linestyle='--', linewidth=0.8)
        ax.set_title('Relative Strength Index (RSI)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('RSI', fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_ylim(0, 100)
        ax.grid(True, linestyle=':', alpha=0.6)

        canvas = FigureCanvasTkAgg(fig, master=rsi_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    root.mainloop()

def seffybacktest(portfolio_returns):
    def get_user_input(prompt, default=None):
        return simpledialog.askstring("Input", prompt, initialvalue=default)

    def select_indicators():
        indicator_window = tk.Toplevel(root)
        indicator_window.title("Select Indicators")
        indicator_window.geometry("300x400")

        listbox = tk.Listbox(indicator_window, selectmode=tk.MULTIPLE)
        for i, indicator in enumerate(indicators):
            listbox.insert(tk.END, f"{i+1}. {indicator}")
        listbox.pack(fill=tk.BOTH, expand=True)

        def on_select():
            selected_indices = listbox.curselection()
            for i in selected_indices:
                selected_indicators.append(indicators[i])
            indicator_window.destroy()

        select_button = tk.Button(indicator_window, text="Select", command=on_select)
        select_button.pack()

        indicator_window.wait_window()

    print("Welcome to EQUATE's Portfolio Analysis Tool: the Seffy Backtest!")
    
    # List of available indicators
    indicators = [
        "Adjusted Sharpe Ratio", "Annual Return", "Average Return", "Calmar Ratio",
        "CAPM", "Correlation with Index", "CVaR", "Double Sharpe Ratio",
        "Fama-French Factors", "Intraweek Variances", "Market Alpha", "Market Beta",
        "Modified Sharpe Ratio", "Momentum", "RSI", "Sharpe Ratio", "Sortino Ratio",
        "Treynor Ratio", "VaR", "Portfolio Volatility"
    ]
    
    # User selects indicators
    selected_indicators = []
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    select_indicators()

    # Check if risk-free rate is needed
    risk_free_rate = None
    if any(indicator in ["Adjusted Sharpe Ratio", "CAPM", "Double Sharpe Ratio", "Fama-French Factors", "Market Alpha", "Modified Sharpe Ratio", "Sharpe Ratio", "Sortino Ratio", "Treynor Ratio"] for indicator in selected_indicators):
        risk_free_rate_str = get_user_input("Enter the annual risk-free rate (Enter for default: 4.25%):", "4.25%")
        try:
            risk_free_rate = float(risk_free_rate_str.replace('%', '')) / 100 if '%' in risk_free_rate_str else float(risk_free_rate_str)
        except ValueError:
            risk_free_rate = 0.0425

    # Check if baseline market index is needed
    ticker = None
    if any(indicator in ["CAPM", "Correlation with Index", "Market Alpha", "Market Beta", "Treynor Ratio"] for indicator in selected_indicators):
        ticker = get_user_input("Enter a market baseline indice ticker (Enter for S&P 500):", "^GSPC")
    
    # Check if momentum or RSI plots are needed
    plot_momentum_rsi = False
    if "Momentum" in selected_indicators or "RSI" in selected_indicators:
        plot_momentum_rsi = messagebox.askyesno("Plot Graphs", "Do you want to plot stock momentum and RSI graphs?")

    # Check if volatility is annualized
    annualize = False
    if "Portfolio Volatility" in selected_indicators:
        annualize = messagebox.askyesno("Annualize Volatility", "Annualize Volatility?")
    
    # Create progress bar window
    progress_window = tk.Toplevel(root)
    progress_window.title("Analysis Progress")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window, text="Calculating...")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, orient=tk.HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=10)

    # Perform analysis for selected indicators
    results = {}
    total_indicators = len(selected_indicators)

    for i, indicator in enumerate(selected_indicators):
        progress_label.config(text=f"Calculating {indicator}...")
        progress_bar['value'] = (i / total_indicators) * 100
        progress_window.update()

        if indicator == "Adjusted Sharpe Ratio":
            results[indicator] = adjusted_sharpe(portfolio_returns, risk_free_rate)
        elif indicator == "Annual Return":
            results[indicator] = annual_return(portfolio_returns)
        elif indicator == "Average Return":
            results[indicator] = average_return(portfolio_returns)
        elif indicator == "Calmar Ratio":
            results[indicator] = calculate_calmar_ratio(portfolio_returns)
        elif indicator == "CAPM":
            results[indicator] = calculate_capm(portfolio_returns, risk_free_rate, ticker)
        elif indicator == "Correlation with Index":
            results[indicator] = correlation_with_index(portfolio_returns, ticker)
        elif indicator == "CVaR":
            results[indicator] = calculate_cvar(portfolio_returns)
        elif indicator == "Double Sharpe Ratio":
            results[indicator] = double_sharpe(portfolio_returns, risk_free_rate)
        elif indicator == "Fama-French Factors":
            start_date = portfolio_returns.index[0]
            end_date = portfolio_returns.index[-1]
            ff_factors = get_fama_french_factors(start_date, end_date)
            results[indicator] = calculate_fama_french(portfolio_returns, risk_free_rate, ticker)
        elif indicator == "Intraweek Variances":
            intraweek_results = analyze_portfolio_volatility(portfolio_returns)
            results["Average Intraweek Variance"] = intraweek_results.get("average_intraweek_variance")
            results["Highest Variance Week"] = intraweek_results.get("highest_variance_week")
            results["Highest Variance"] = intraweek_results.get("highest_variance")
        elif indicator == "Market Alpha":
            results[indicator] = alpha(portfolio_returns, ticker, risk_free_rate)
        elif indicator == "Market Beta":
            results[indicator] = beta(portfolio_returns, ticker)
        elif indicator == "Modified Sharpe Ratio":
            results[indicator] = modified_sharpe(portfolio_returns, risk_free_rate)
        elif indicator == "Momentum":
            results[indicator] = calculate_momentum(portfolio_returns, plot=plot_momentum_rsi)
        elif indicator == "RSI":
            results[indicator] = calculate_rsi(portfolio_returns, plot=plot_momentum_rsi)
        elif indicator == "Sharpe Ratio":
            results[indicator] = sharpe_ratio(portfolio_returns, risk_free_rate)
        elif indicator == "Sortino Ratio":
            results[indicator] = sortino_ratio(portfolio_returns, risk_free_rate)
        elif indicator == "Treynor Ratio":
            portfolio_beta = beta(portfolio_returns, ticker)
            results[indicator] = treynor_ratio(portfolio_returns, portfolio_beta, risk_free_rate)
        elif indicator == "VaR":
            results[indicator] = calculate_var(portfolio_returns)
        elif indicator == "Portfolio Volatility":
            results[indicator] = calculate_portfolio_volatility(portfolio_returns, annualize)

    progress_window.destroy()

    # Display results in a separate UI
    create_ui(results, momentum=results.get("Momentum"), rsi=results.get("RSI"))


