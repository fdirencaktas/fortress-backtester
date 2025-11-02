# Fortress Backtester 🏰
A lightweight Python backtesting engine built from scratch — designed to test rule-based trading strategies using **Pandas**, **NumPy**, and **Matplotlib**.

---

## 📘 Project Overview

This project demonstrates how to build a **fully functional backtesting pipeline** without relying on external backtesting frameworks.

It supports:
- Data download from Yahoo Finance
- Custom strategy logic (MA crossover, price above MA)
- Transaction cost modeling
- Risk-free return integration
- Key performance metrics (CAGR, Sharpe, Sortino, Calmar, Max Drawdown)
- Equity curve and drawdown visualization

---

## ⚙️ Features

| Feature | Description |
|----------|--------------|
| **Custom Signals** | Moving average crossover and price/MA cross |
| **Performance Metrics** | CAGR, Sharpe, Sortino, Calmar, Drawdown |
| **Visualization** | Equity curve and drawdown plots |
| **Transaction Costs** | Optional cost per trade |
| **Risk-Free Adjustment** | Daily risk-free rate added to idle capital |

---

## 📊 Example Output

![Equity Curves](<img width="800" height="400" alt="example" src="https://github.com/user-attachments/assets/d1622801-1891-4664-b7d4-6ff7ed55a34d" />
)

---

## 🧩 How It Works

1. **Load Data**  
   Downloads OHLCV data using `yfinance`.

2. **Generate Signals**  
   Two sample strategies:
   - SMA Crossover (50/200)
   - Price vs. 200-day SMA

3. **Simulate Trades**  
   Position tracking and returns with transaction costs.

4. **Evaluate Performance**  
   Computes CAGR, Sharpe, Sortino, Calmar, and Drawdown.

5. **Visualize Results**  
   Plots equity curves and drawdown using Matplotlib.

---

## 🚀 How to Run

```bash
git clone https://github.com/fdirencaktas/fortress-backtester.git
cd fortress-backtester
pip install -r requirements.txt
python src/backtester.py
