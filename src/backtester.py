import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# -----------------------------
# CONFIGURATION
# -----------------------------
TICKER = "SPY"
START_DATE = "2000-01-01"
TRANSACTION_COST = 0.002
RISK_FREE_ANNUAL = 0.04
DAILY_RF = RISK_FREE_ANNUAL / 252

# -----------------------------
# DATA LOADING & INDICATORS
# -----------------------------
def download_data(ticker, start):
    data = yf.download(ticker, start=start)
    data["returns"] = data["Close"].pct_change()
    return data

def add_sma(data, fast=50, slow=200):
    data["fast_sma"] = data["Close"].rolling(fast).mean()
    data["slow_sma"] = data["Close"].rolling(slow).mean()
    return data

# -----------------------------
# STRATEGIES
# -----------------------------
def generate_signals(data):
    data["signal_sma"] = (data["fast_sma"] > data["slow_sma"]).astype(int)
    data["signal_price"] = (data["Close"] > data["Close"].rolling(200).mean()).astype(int)
    return data

def compute_strategy_returns(data, signal, name, risk_free=True):
    df = data.copy()
    #calculate total number of trade with changes in signal using diff() then change negative numbers to abs
    df[f"{name}_trade"] = signal.diff().abs().fillna(0)
    df[f"{name}_strategy"] = signal.shift(1) * df["returns"]
    
    df[f"{name}_strategy_after_cost"] = (
        df[f"{name}_strategy"]
        - TRANSACTION_COST * df[f"{name}_trade"]
        + ((1 - signal.shift(1)) * DAILY_RF if risk_free else 0)
    )
    return df[f"{name}_strategy_after_cost"]

# -----------------------------
# PERFORMANCE METRICS
# -----------------------------
def cagr(equity):
    equity = equity.dropna()
    years = (equity.index[-1] - equity.index[0]).days / 365.25
    return (equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1

def total_return(equity):
    return (equity.iloc[-1] - 1) * 100


def max_drawdown(equity):
    return (equity / equity.cummax() - 1).min()

def calmar_ratio(equity):
    mdd = abs(max_drawdown(equity))
    return cagr(equity) / mdd if mdd else np.nan

def sharpe_ratio(returns, risk_free=RISK_FREE_ANNUAL):
    excess = returns - risk_free / 252
    return np.sqrt(252) * excess.mean() / excess.std()

def sortino_ratio(returns, risk_free=RISK_FREE_ANNUAL):
    excess = returns - risk_free / 252
    downside = excess[excess < 0]
    if downside.empty: return np.nan
    downside_std = np.sqrt((downside**2).mean())
    return (excess.mean() * 252) / downside_std

# -----------------------------
# MAIN ANALYSIS PIPELINE
# -----------------------------
data = download_data(TICKER, START_DATE)
data = add_sma(data)
data = generate_signals(data)

data["ret_sma"] = compute_strategy_returns(data, data["signal_sma"], "sma", risk_free=True)
data["ret_price"] = compute_strategy_returns(data, data["signal_price"], "price", risk_free=True)

equity = pd.DataFrame({
    "SMA Strategy": (1 + data["ret_sma"]).cumprod(),
    "Price/SMA Strategy": (1 + data["ret_price"]).cumprod(),
    "Benchmark": (1 + data["returns"]).cumprod()
})

# -----------------------------
# REPORTING
# -----------------------------
def report(name, equity_curve, returns):
    print(f"\n📈 {name} Results:")
    print(f"CAGR: {cagr(equity_curve):.2%}")
    print(f'Total Return: {total_return(equity_curve):.2f}%')
    print(f"Max Drawdown: {max_drawdown(equity_curve):.2%}")
    print(f"Calmar Ratio: {calmar_ratio(equity_curve):.2f}")
    print(f"Sharpe Ratio: {sharpe_ratio(returns):.2f}")
    print(f"Sortino Ratio: {sortino_ratio(returns):.2f}")

report("SMA Strategy", equity["SMA Strategy"], data["ret_sma"])
report("Price/SMA Strategy", equity["Price/SMA Strategy"], data["ret_price"])
report("Benchmark", equity["Benchmark"], data["returns"])

# -----------------------------
# PLOTTING
# -----------------------------

drawdowns = equity / equity.cummax() - 1

#height ratios ---> top plot (equity curve) is twice as tall as bottom (drawdown)
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
equity.plot(ax=axes[0], title=f"Equity Curves for {TICKER}")
axes[0].set_ylabel("Portfolio Value")

drawdowns.plot(ax=axes[1], title="Drawdowns")
#convert numeric values like -0.15 into -15%.
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
axes[1].set_ylabel("Drawdown (%)")

#prevent overlapping labels
plt.tight_layout() 
plt.show()
