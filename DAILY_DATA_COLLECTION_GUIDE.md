# Daily Data Collection Guide

**Purpose:** Automate fetching real-time stock market data from Yahoo Finance for analysis.

---

## 🎯 Quick Start

### Run Daily Data Collection
```bash
cd /home/user/millionaire-project
python3 scripts/daily_data_fetcher.py
```

That's it! The script will:
1. Fetch data for all 14 tracked stocks
2. Calculate technical indicators (RSI, MACD, SMAs)
3. Save to `analysis/{today}/data/market_data.json`
4. Display summary with RSI conditions

---

## 📅 When to Run

### Recommended Schedule

**Option 1: Daily (After Market Close)**
```bash
# Run after Bursa Malaysia closes (5:00 PM MYT)
# Best time: 6:00 PM MYT or later
python3 scripts/daily_data_fetcher.py
```

**Option 2: Weekly (Friday Evening)**
```bash
# Run every Friday after market close
# Get week's closing data
python3 scripts/daily_data_fetcher.py
```

**Option 3: Manual (On-Demand)**
```bash
# Run anytime you want updated data
python3 scripts/daily_data_fetcher.py
```

---

## 🔧 Advanced Usage

### Fetch Data for Specific Date
```bash
python3 scripts/daily_data_fetcher.py --date 2025-11-22
```

### Check if Script Works
```bash
# Test the script
python3 scripts/daily_data_fetcher.py --date 2025-11-21
```

---

## 📊 What Data is Collected

### For Each Stock:
1. **Current Price** (RM)
2. **52-Week High/Low**
3. **RSI (14-period)** - Momentum indicator
4. **MACD** - Trend indicator
5. **SMA 20/50/200** - Moving averages
6. **Volume** (current and 20-day average)
7. **Distance from 52w high/low** (%)

### Technical Indicators Explained:

**RSI (Relative Strength Index):**
- **< 10:** EXTREME oversold - panic selling
- **< 30:** Oversold - potential buying opportunity
- **30-70:** Normal range
- **> 70:** Overbought - caution
- **> 80:** EXTREME overbought - correction risk

**MACD (Moving Average Convergence Divergence):**
- **Bullish:** MACD above signal line (uptrend)
- **Bearish:** MACD below signal line (downtrend)

**SMA (Simple Moving Averages):**
- **SMA20:** Short-term trend (1 month)
- **SMA50:** Medium-term trend (2.5 months)
- **SMA200:** Long-term trend (10 months)

---

## 📁 Output Files

### Data Storage Structure:
```
analysis/
  └── 2025-11-21/           # Today's date
      ├── data/
      │   └── market_data.json   # Raw market data ✅
      ├── technology/
      │   ├── INARI.md
      │   ├── UNISEM.md
      │   ├── PENTA.md
      │   └── GREATEC.md
      ├── finance/
      │   ├── PBBANK.md
      │   ├── MAYBANK.md
      │   ├── CIMB.md
      │   ├── HLBANK.md
      │   └── MAXIS.md
      ├── utilities/
      │   ├── PGAS.md
      │   ├── VSOLAR.md
      │   ├── GASMSIA.md
      │   ├── TENAGA.md
      │   └── YTLPOWR.md
      └── index.md              # Daily summary
```

---

## 🚀 Automation Options

### Option 1: Manual Daily Execution
```bash
# Run manually every day
python3 scripts/daily_data_fetcher.py
```

**Pros:** Full control, run when needed
**Cons:** Must remember to run daily

---

### Option 2: Cron Job (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 6:00 PM)
0 18 * * * cd /home/user/millionaire-project && python3 scripts/daily_data_fetcher.py >> logs/data_fetch.log 2>&1
```

**Pros:** Fully automated, hands-free
**Cons:** Requires cron setup

---

### Option 3: Windows Task Scheduler
1. Open "Task Scheduler"
2. Create Basic Task
3. Set trigger: Daily at 6:00 PM
4. Action: Start a program
5. Program: `python3`
6. Arguments: `/home/user/millionaire-project/scripts/daily_data_fetcher.py`

---

## 📝 Sample Output

```
======================================================================
📈 DAILY STOCK DATA FETCHER
======================================================================
Date: 2025-11-21
Stocks to fetch: 14
Data source: Yahoo Finance
======================================================================
  Fetching INARI (0166.KL)... ✅ RM 2.39 | RSI 28.9
  Fetching UNISEM (5005.KL)... ✅ RM 3.19 | RSI 32.0
  Fetching PBBANK (PBBANK.KL)... ✅ RM 4.25 | RSI 57.5
  ...
======================================================================
✅ Successfully fetched: 14/14 stocks
======================================================================

💾 Data saved to: analysis/2025-11-21/data/market_data.json

======================================================================
📊 MARKET DATA SUMMARY
======================================================================

Technology Sector (4 stocks):
  INARI      RM   2.39 | RSI  28.9 🟠 | Bearish
  UNISEM     RM   3.19 | RSI  32.0 🟢 | Bearish
  PENTA      RM   3.73 | RSI   8.1 🔴 | Bearish
  GREATEC    RM   1.82 | RSI   8.8 🔴 | Bearish

Finance Sector (5 stocks):
  PBBANK     RM   4.25 | RSI  57.5 🟢 | Bullish
  MAYBANK    RM   9.94 | RSI  58.6 🟢 | Bearish
  CIMB       RM   7.53 | RSI  62.2 🟢 | Bearish
  HLBANK     RM  21.00 | RSI  55.3 🟢 | Bearish
  MAXIS      RM   4.18 | RSI  84.3 🟣 | Bullish

Utilities Sector (5 stocks):
  PGAS       RM  18.18 | RSI  34.9 🟠 | Bearish
  VSOLAR     RM   3.07 | RSI  55.8 🟢 | Bearish
  GASMSIA    RM   4.40 | RSI  44.0 🟢 | Bearish
  TENAGA     RM  13.18 | RSI  41.9 🟢 | Bearish
  YTLPOWR    RM   3.72 | RSI  28.3 🟠 | Bearish

======================================================================
Average RSI: 44.3
Extreme Oversold (RSI < 10): 2 stocks
Oversold (RSI < 30): 3 stocks
Overbought (RSI > 70): 1 stocks
Extreme Overbought (RSI > 80): 1 stocks
======================================================================

✅ Data collection complete!
📁 Output file: analysis/2025-11-21/data/market_data.json

💡 Next step: Run analysis agents to generate stock reports
```

---

## 🔍 Interpreting the Summary

### RSI Emojis:
- 🔴 **< 10** - EXTREME oversold (DO NOT BUY YET - wait for stabilization)
- 🟠 **< 30** - Oversold (potential buying opportunity)
- 🟢 **30-70** - Normal (healthy trading range)
- 🔵 **> 70** - Overbought (caution)
- 🟣 **> 80** - EXTREME overbought (DO NOT BUY - wait for pullback)

### Action Guidelines:

**When you see:**
- **Multiple 🟠 (oversold):** Good buying opportunities in quality stocks
- **Multiple 🔴 (extreme oversold):** Wait for stabilization before buying
- **Multiple 🟣 (extreme overbought):** Market extended, wait for pullback
- **Mostly 🟢 (neutral):** Normal market conditions

---

## ⚙️ Prerequisites

### Required Python Libraries:
```bash
pip install yfinance pandas
```

### Check if Installed:
```bash
python3 -c "import yfinance; print('✅ yfinance installed')"
python3 -c "import pandas; print('✅ pandas installed')"
```

---

## 🐛 Troubleshooting

### Problem: "No module named 'yfinance'"
```bash
# Solution: Install yfinance
pip install yfinance pandas
```

### Problem: "No data fetched"
```bash
# Check internet connection
ping yahoo.com

# Try manual test
python3 scripts/test_yahoo_finance_connection.py
```

### Problem: "Permission denied"
```bash
# Make script executable
chmod +x scripts/daily_data_fetcher.py
```

---

## 📈 Next Steps After Data Collection

1. **Review the summary** - Look for extreme RSI conditions
2. **Check individual stock files** - Read `analysis/{date}/index.md`
3. **Update your watchlist** - Note stocks with extreme conditions
4. **Execute trades** - Follow recommendations from analysis files
5. **Update portfolio tracker** - Log your positions

---

## 🎯 Pro Tips

1. **Run after market close** - Get end-of-day prices (most accurate)
2. **Check RSI extremes** - RSI < 10 or > 80 are rare opportunities
3. **Compare with previous days** - Track RSI trends over time
4. **Don't chase extreme overbought** - Wait for pullbacks (RSI > 80)
5. **Be patient with extreme oversold** - Wait for RSI recovery (RSI < 10)

---

## 📊 Data Quality

**Source:** Yahoo Finance (same as KLSE app, Bloomberg, TradingView)

**Reliability:** HIGH ✅
- Real-time market data
- Same source as professional platforms
- Verified against KLSE app (2025-11-19)

**Update Frequency:**
- **Daily:** End-of-day prices (5:00 PM MYT close)
- **Intraday:** 15-minute delay (Yahoo Finance limitation)

---

## 🚀 Integration with Analysis Pipeline

### Workflow:
1. **Fetch Data** → `python3 scripts/daily_data_fetcher.py`
2. **Run Agents** → Claude agents generate analysis (automated)
3. **Review Reports** → Read `analysis/{date}/index.md`
4. **Execute Trades** → Follow recommendations
5. **Track Performance** → Update portfolio JSON (Milestone 4)

---

## 📞 Support

**Issues?**
- Check Python version: `python3 --version` (need 3.7+)
- Check internet: `ping yahoo.com`
- Verify libraries: Run test script
- Review error messages in output

---

**Happy Data Collecting! Let's get that real-time market data! 📈💰**

---

*Last Updated: 2025-11-21*
*Part of: Millionaire Project - Milestone 1*
