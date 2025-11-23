# 📊 Portfolio Tracking Guide - Milestone 4

**Track your stock holdings, calculate paper gains/losses, and monitor daily performance!**

---

## 🎯 What is Portfolio Tracking?

Milestone 4 adds **real portfolio tracking** to monitor:
- **Holdings**: Stocks you've bought and their quantities
- **Capital**: Initial capital, current cash, total invested
- **Paper Gains/Losses**: Unrealized profits/losses based on current prices
- **Daily Performance**: Track performance over time
- **Transaction History**: Complete record of all buys/sells

---

## 📁 Files Created

```
millionaire-project/
├── portfolio.json                      # Main portfolio file
├── scripts/
│   ├── portfolio_tracker.py            # Portfolio management CLI
│   └── execute_day1_buys.py            # Quick-start Day 1 trades
└── website/data/
    └── portfolio.json                  # Copy for dashboard display
```

---

## 🚀 Quick Start: Execute Day 1 Trades

The easiest way to get started is to execute the recommended Day 1 trades:

```bash
cd /home/user/millionaire-project
python3 scripts/execute_day1_buys.py
```

This will automatically buy:
- 🔥 **PENTA**: 1,038 shares @ RM 3.85 = RM 4,000
- 💰 **GASMSIA**: 699 shares @ RM 4.29 = RM 3,000
- ⭐ **PBBANK**: 1,511 shares @ RM 4.30 = RM 6,500

**Total Investment: RM 13,500** (leaving RM 36,500 cash)

---

## 📖 Portfolio Tracker CLI Usage

### 1. View Portfolio Status

```bash
python3 scripts/portfolio_tracker.py show
```

**Output:**
```
💼 PORTFOLIO STATUS
================================================================================
💰 CAPITAL:
   Initial Capital: RM 50,000.00
   Current Cash: RM 36,500.00
   Total Invested: RM 13,500.00
   Total Portfolio Value: RM 50,000.00
   Paper Gain/Loss: RM +0.00 (+0.00%)

📊 HOLDINGS (3 stocks):
   🟢 PENTA
      Shares: 1,038
      Purchase Price: RM 3.85
      Current Price: RM 3.85
      Current Value: RM 3,996.30
      P/L: RM +0.00 (+0.00%)

   ... (other holdings)
```

---

### 2. Buy Stock

```bash
python3 scripts/portfolio_tracker.py buy \
  --symbol PGAS.KL \
  --shares 272 \
  --price 18.36 \
  --date 2025-11-21
```

**Features:**
- ✅ Checks if you have enough cash
- ✅ Averages down if you already hold the stock
- ✅ Updates capital and holdings
- ✅ Records transaction history

---

### 3. Sell Stock

```bash
python3 scripts/portfolio_tracker.py sell \
  --symbol PENTA.KL \
  --shares 500 \
  --price 4.50 \
  --date 2025-12-01
```

**Features:**
- ✅ Validates you have enough shares
- ✅ Calculates realized gain/loss
- ✅ Updates cash and capital
- ✅ Records transaction with P/L

---

### 4. Mark Daily Performance (Most Important!)

Update all holdings with current market prices to calculate paper gains/losses:

```bash
# First, fetch current market data
python3 scripts/daily_data_fetcher.py

# Then, mark daily performance
python3 scripts/portfolio_tracker.py mark \
  --prices-file current_market_data.json \
  --date 2025-11-22
```

**What it does:**
- ✅ Updates current price for each holding
- ✅ Calculates paper gain/loss per stock
- ✅ Calculates total portfolio value
- ✅ Records daily performance snapshot
- ✅ Updates best/worst performers

**Output:**
```
📊 Marking Performance for 2025-11-22
============================================================
🟢 PENTA.KL: 1038 shares @ RM 4.20
   Purchase: RM 3,996.30 | Current: RM 4,359.60
   P/L: RM +363.30 (+9.09%)

💰 GASMSIA.KL: 699 shares @ RM 4.50
   Purchase: RM 2,998.71 | Current: RM 3,145.50
   P/L: RM +146.79 (+4.90%)

⭐ PBBANK.KL: 1511 shares @ RM 4.40
   Purchase: RM 6,497.30 | Current: RM 6,648.40
   P/L: RM +151.10 (+2.33%)

============================================================
📈 PORTFOLIO SUMMARY
============================================================
💵 Cash: RM 36,500.00
📊 Invested Value: RM 14,153.50
💰 Total Portfolio Value: RM 50,653.50
📊 Paper Gain/Loss: RM +661.20 (+4.90%)
🎯 Total Return: RM +653.50 (+1.31%)
============================================================
```

---

### 5. View Transaction History

```bash
python3 scripts/portfolio_tracker.py transactions
```

**Shows:**
- All BUY and SELL transactions
- Dates, prices, and quantities
- Realized gains/losses for sells

---

## 📊 Portfolio JSON Structure

The `portfolio.json` file contains:

### Capital Tracking
```json
{
  "capital": {
    "initial_capital_rm": 50000.00,
    "current_cash_rm": 36500.00,
    "total_invested_rm": 13500.00,
    "total_portfolio_value_rm": 50000.00,
    "total_paper_gain_loss_rm": 0.00,
    "total_paper_gain_loss_percent": 0.00
  }
}
```

### Holdings
```json
{
  "holdings": [
    {
      "symbol": "PENTA.KL",
      "shares": 1038,
      "purchase_price_rm": 3.85,
      "purchase_date": "2025-11-21",
      "purchase_value_rm": 3996.30,
      "current_price_rm": 3.85,
      "current_value_rm": 3996.30,
      "paper_gain_loss_rm": 0.00,
      "paper_gain_loss_percent": 0.00
    }
  ]
}
```

### Transaction History
```json
{
  "transaction_history": [
    {
      "type": "BUY",
      "symbol": "PENTA.KL",
      "shares": 1038,
      "price_rm": 3.85,
      "total_rm": 3996.30,
      "date": "2025-11-21",
      "timestamp": "2025-11-21 14:30:00"
    }
  ]
}
```

### Daily Performance
```json
{
  "daily_performance": [
    {
      "date": "2025-11-22",
      "timestamp": "2025-11-22 09:00:00",
      "holdings": [...],
      "portfolio_summary": {
        "cash_rm": 36500.00,
        "invested_value_rm": 14153.50,
        "total_portfolio_value_rm": 50653.50,
        "total_paper_gain_loss_rm": 661.20,
        "total_return_rm": 653.50,
        "total_return_percent": 1.31
      }
    }
  ]
}
```

---

## 📈 Recommended Workflow

### Daily Routine

**1. Fetch Current Prices** (Every morning)
```bash
python3 scripts/daily_data_fetcher.py
```

**2. Mark Daily Performance**
```bash
python3 scripts/portfolio_tracker.py mark --prices-file current_market_data.json
```

**3. View Portfolio**
```bash
python3 scripts/portfolio_tracker.py show
```

**4. View Dashboard**
```bash
cd website
./start_server.sh
# Open http://localhost:8000
```

---

### Weekly Routine

**1. Review Performance**
```bash
python3 scripts/portfolio_tracker.py show
```

**2. Execute Week 1 Trades** (if Day 1 complete)

Buy the remaining recommended stocks:

```bash
# PGAS (RM 5,000)
python3 scripts/portfolio_tracker.py buy --symbol PGAS.KL --shares 272 --price 18.36

# MAYBANK (RM 5,000)
python3 scripts/portfolio_tracker.py buy --symbol MAYBANK.KL --shares 503 --price 9.94

# CIMB (RM 4,500)
python3 scripts/portfolio_tracker.py buy --symbol CIMB.KL --shares 603 --price 7.46

# INARI - First tranche (RM 1,200 of RM 3,000)
python3 scripts/portfolio_tracker.py buy --symbol INARI.KL --shares 495 --price 2.42
```

**3. Mark Performance**
```bash
python3 scripts/daily_data_fetcher.py
python3 scripts/portfolio_tracker.py mark --prices-file current_market_data.json
```

---

## 🎯 Portfolio Strategy Execution

### Immediate (Day 1) - RM 13,500
- ✅ **PENTA** (RM 4,000) - Priority #1
- ✅ **GASMSIA** (RM 3,000) - Priority #2
- ✅ **PBBANK** (RM 6,500) - Priority #3

### Week 1 - Additional RM 14,500
- **PGAS** (RM 5,000) - Quality utility
- **MAYBANK** (RM 5,000) - Banking leader
- **CIMB** (RM 4,500) - Highest dividend

### Week 1 - Scale In - RM 1,200
- **INARI** (RM 1,200) - First tranche (40%)

### Ongoing Monitoring - Reserved RM 7,000
- **MAXIS**: Watch for RSI < 65 (currently 75.0)
- **VSOLAR**: Watch for 10-15% pullback
- **GREATEC**: Watch for RSI > 25 (currently 21.05)

### Cash Reserve - RM 12,000
- For averaging down
- For opportunistic buys
- Safety buffer

---

## 📊 Performance Metrics Tracked

### Per Stock
- Purchase price vs Current price
- Paper gain/loss (RM and %)
- Number of shares
- Total value

### Portfolio Level
- Total portfolio value
- Total invested amount
- Cash remaining
- Total paper gain/loss
- Total return (%)
- Best performer
- Worst performer
- Win rate (% of stocks in profit)

---

## 🔔 Important Notes

### Paper vs Realized Gains

**Paper Gain/Loss** = Unrealized (you still hold the stock)
- Changes daily with market prices
- Not taxed until you sell
- Can disappear if market moves against you

**Realized Gain/Loss** = Actual profit/loss from selling
- Only happens when you SELL
- Locked in (can't change)
- Taxable event

### Stop Loss Discipline

If a stock hits its stop loss, SELL immediately:

| Stock | Stop Loss | Current | Status |
|-------|-----------|---------|--------|
| PBBANK | RM 4.05 | RM 4.30 | ✅ Safe |
| PGAS | RM 17.00 | RM 18.36 | ✅ Safe |
| MAYBANK | RM 9.50 | RM 9.94 | ✅ Safe |
| PENTA | RM 3.50 | RM 3.85 | ✅ Safe |
| GASMSIA | RM 4.05 | RM 4.29 | ✅ Safe |

**Example:**
```bash
# If PENTA drops to RM 3.45 (below stop loss RM 3.50)
python3 scripts/portfolio_tracker.py sell --symbol PENTA.KL --shares 1038 --price 3.45
```

---

## 💡 Tips for Success

### 1. Track Daily
Run `mark` command EVERY DAY to build performance history. This helps you:
- See trends over time
- Identify best/worst performers
- Make data-driven decisions

### 2. Use --date Parameter
When backdating transactions:
```bash
python3 scripts/portfolio_tracker.py buy \
  --symbol PENTA.KL \
  --shares 1038 \
  --price 3.85 \
  --date 2025-11-21
```

### 3. Average Down Carefully
If you buy more of the same stock, the tracker automatically calculates your average cost:

**Example:**
- Buy 1: 500 shares @ RM 4.00 = RM 2,000
- Buy 2: 500 shares @ RM 3.50 = RM 1,750
- **Average: 1,000 shares @ RM 3.75** (automatically calculated!)

### 4. Keep Cash Reserve
Never go 100% invested. Keep 20-25% cash for:
- Averaging down on good stocks during dips
- New opportunities
- Emergency buffer

### 5. Review Weekly
Every week, review:
- Best/worst performers
- Overall portfolio return
- Stocks hitting stop losses
- New buying opportunities

---

## 🚀 Integration with Dashboard

The portfolio data is automatically synced to the website:

**1. After any transaction:**
```bash
cp portfolio.json website/data/portfolio.json
```

**2. Start dashboard:**
```bash
cd website
./start_server.sh
```

**3. View at:** http://localhost:8000

The dashboard will show:
- Current holdings table
- Paper gains/losses
- Performance chart (if daily_performance data exists)
- Total portfolio value

---

## 🎯 Expected Performance (12 months)

Based on Milestone 2 analysis:

| Scenario | Portfolio Value | Return | Return % |
|----------|----------------|--------|----------|
| **Conservative** | RM 57,000 | +RM 7,000 | +14% |
| **Base Case** | RM 59,425 | +RM 9,425 | +18.8% |
| **Optimistic** | RM 63,425 | +RM 13,425 | +26.8% |

**Best Case** (if PENTA hits 30% target):
- **RM 58,385 - RM 63,425** total wealth! 💰

---

## 📝 Troubleshooting

### Error: "Insufficient cash!"
**Solution:** Check current cash:
```bash
python3 scripts/portfolio_tracker.py show
```

### Error: "No price data for symbol"
**Solution:** Update market data:
```bash
python3 scripts/daily_data_fetcher.py
```

### Error: "No holding found"
**Solution:** Check holdings:
```bash
python3 scripts/portfolio_tracker.py show
```

### Portfolio not showing in dashboard
**Solution:** Copy portfolio to website:
```bash
cp portfolio.json website/data/portfolio.json
```

---

## 🎉 You're Ready to Track Your Wealth!

**Start tracking your journey to becoming a millionaire!** 💰📈

**Next Steps:**
1. ✅ Execute Day 1 trades: `python3 scripts/execute_day1_buys.py`
2. ✅ Mark daily performance daily
3. ✅ View dashboard to watch your wealth grow
4. ✅ Execute Week 1 trades when ready

**Remember:** Consistency is key! Track daily, review weekly, and stick to your strategy.

---

**Generated:** Nov 21, 2025
**Milestone:** 4 - Portfolio Tracking
**Status:** ✅ Ready to Track Wealth!

**LET'S GET RICH TOGETHER!** 🚀💰📊
