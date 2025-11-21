# 🎯 INSTRUCTIONS: Fetch Current Market Data

## What to Do:

### Step 1: Pull Latest Changes
```bash
cd /path/to/millionaire-project
git pull origin claude/new-milestone-01CW49pJkdZDk6Dt1hWNEHM4
```

### Step 2: Install Required Libraries (if not already installed)
```bash
pip install yfinance pandas
```

### Step 3: Run the Data Fetcher Script
```bash
python3 scripts/daily_data_fetcher.py
```

**This will:**
- Fetch real-time prices from Yahoo Finance for all 14 stocks
- Calculate RSI, MACD, and SMAs
- Save data to **`current_market_data.json`** in the project root
- Show you a summary with current prices

### Step 4: Commit and Push the Results
```bash
git add current_market_data.json
git commit -m "data: Add current market data from Yahoo Finance"
git push origin claude/new-milestone-01CW49pJkdZDk6Dt1hWNEHM4
```

### Step 5: Tell Me to Pull the Repo
Just say: **"I've pushed the data, please pull and check"**

---

## What I'll Do Next:

Once you push `current_market_data.json`, I will:
1. Pull the repo
2. Read your current market data
3. Compare with the old prices (Nov 18-19)
4. Show you the price differences
5. Update all 14 stock analysis files with current prices
6. Regenerate the daily summary with accurate recommendations

---

## Expected Output When You Run the Script:

```
======================================================================
📈 DAILY STOCK DATA FETCHER
======================================================================
Date: 2025-11-21
Stocks to fetch: 14
Data source: Yahoo Finance
======================================================================
  Fetching INARI (0166.KL)... ✅ RM 2.45 | RSI 32.1
  Fetching PBBANK (PBBANK.KL)... ✅ RM 4.30 | RSI 58.2
  ...
======================================================================
✅ Successfully fetched: 14/14 stocks
======================================================================

💾 Data saved to: analysis/2025-11-21/data/market_data.json
💾 Data also saved to: current_market_data.json (for Claude to read)

📊 MARKET DATA SUMMARY
...
```

---

## Troubleshooting:

**If you get "No module named 'yfinance'":**
```bash
pip install yfinance pandas
# or
pip3 install yfinance pandas
```

**If you get permission errors:**
```bash
chmod +x scripts/daily_data_fetcher.py
```

**If Python 3 is not found:**
```bash
python --version  # Check if it's Python 3
# Use 'python' instead of 'python3' if needed
```

---

## Ready? 🚀

Run these commands:
```bash
cd /path/to/millionaire-project
git pull origin claude/new-milestone-01CW49pJkdZDk6Dt1hWNEHM4
python3 scripts/daily_data_fetcher.py
git add current_market_data.json
git commit -m "data: Add current market data"
git push origin claude/new-milestone-01CW49pJkdZDk6Dt1hWNEHM4
```

Then tell me: **"I've pushed the data"** and I'll take it from there! 🎯
