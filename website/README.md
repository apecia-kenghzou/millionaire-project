# 💰 Millionaire Stock Dashboard

**Milestone 3: Dashboard Website**

An interactive dashboard visualizing Malaysian stock market analysis with money flow tracking, search functionality, and detailed stock insights.

---

## 🚀 Quick Start

### Run Locally

```bash
cd /home/user/millionaire-project/website
python3 -m http.server 8000
```

Then open your browser to: **http://localhost:8000**

---

## 📊 Features

### 1. **Top 3 Opportunities** (Hero Section)
- 🔥 **PENTA (7160.KL)** - Priority #1: Recovery play (RSI 8.11→31.88)
- 💰 **GASMSIA (5209.KL)** - Priority #2: Oversold entry (RSI 30.0, 1.70x volume)
- ⭐ **PBBANK (PBBANK.KL)** - Priority #3: #1 Ranked (Best fundamentals)

### 2. **Portfolio Overview**
- Total Capital: RM 50,000
- Expected Returns: 14-17% (18-22% with dividends)
- Sector Breakdown: Finance (40%), Utilities (16%), Technology (14%)
- Action Items: 6 BUY NOW, 1 SCALE IN, 3 WATCHLIST

### 3. **Market Money Flow Visualization** (Sankey Diagram)
- Institutional vs Retail capital flows
- Sector allocation and buying/selling pressure
- Individual stock accumulation/distribution patterns
- Interactive tooltips with detailed flow data

### 4. **Stock Search** (4-digit code + Company name)
- Search by code: `7160`, `5209`, `1155`, etc.
- Search by symbol: `PENTA`, `GASMSIA`, `PBBANK`, etc.
- Search by company name: `Pentamaster`, `Gas Malaysia`, `Public Bank`, etc.

### 5. **All Stocks Table** (14 stocks)
- Sortable by any column (Rank, Score, Price, RSI, etc.)
- Filter by Sector (Technology, Finance, Utilities)
- Filter by Action (BUY NOW, SCALE IN, WAIT)
- Click any row to view detailed analysis

### 6. **Stock Detail Modal**
- Comprehensive metrics (Score, RSI, Expected Return, Allocation)
- Action recommendation with entry/exit zones
- Investment thesis and return drivers
- Money flow analysis (Institutional activity)
- Technical indicators
- Risk assessment
- Link to complete analysis report

---

## 📁 File Structure

```
website/
├── index.html                   # Main dashboard page
├── css/
│   └── styles.css               # Complete styling
├── js/
│   ├── data-loader.js           # Load JSON data files
│   ├── sankey.js                # Money flow Sankey diagram
│   ├── table.js                 # Sortable/filterable stock table
│   ├── search.js                # Stock search functionality
│   └── dashboard.js             # Modal and main dashboard logic
├── data/
│   ├── high_return_companies.json    # 7 high-return companies (Milestone 2)
│   ├── current_market_data.json      # Real-time market data (Nov 21, 2025)
│   ├── market_money_flow.json        # Money flow analysis
│   └── active_watchlist.json         # Categorized watchlist
└── README.md                    # This file
```

---

## 🎯 Key Insights Displayed

### Top Opportunities
1. **PENTA**: 25-30% expected return (recovery play)
2. **GASMSIA**: 15-18% expected return (oversold entry)
3. **PBBANK**: 12-15% expected return (#1 ranked)

### Market Money Flow
- **Net Institutional Flow**: +RM 188.7M (Inflows: RM 199.5M, Outflows: RM 10.8M)
- **Finance Sector**: 72% buying pressure (Strong inflow)
- **Utilities Sector**: 65% buying pressure (Moderate inflow)
- **Technology Sector**: 35% buying pressure (Weak outflow)

### Institutional Activity
- **PBBANK**: RM 43M daily inflow (1.82x volume, RSI 59.52)
- **MAYBANK**: RM 97.3M daily inflow (largest flow!)
- **GASMSIA**: RM 5.9M daily inflow (RSI 30.0 oversold + 1.70x volume)
- **PENTA**: RM 1.8M daily inflow (post-capitulation recovery)
- **MAXIS**: -RM 10.8M daily outflow (distribution zone, RSI 75.0)

---

## 🔍 Search Examples

Try these searches:

- **By 4-digit code**: `7160` (PENTA), `5209` (GASMSIA), `1155` (MAYBANK)
- **By symbol**: `PBBANK`, `PGAS`, `INARI`, `CIMB`
- **By company name**: `Pentamaster`, `Public Bank`, `Gas Malaysia`, `Petronas`

---

## 📊 Sorting and Filtering

### Sort Table
Click any column header to sort:
- Rank (lowest to highest)
- Score (highest to lowest)
- Price (lowest to highest)
- RSI (lowest to highest = most oversold first)
- Expected Return (highest to lowest)

### Filter Table
- **By Sector**: Technology, Finance, Utilities
- **By Action**: BUY NOW, SCALE IN, WAIT

---

## 🛠️ Technologies Used

- **HTML5** - Structure
- **CSS3** - Styling with gradients and animations
- **JavaScript (ES6+)** - Interactive functionality
- **D3.js** - Sankey diagram visualization
- **Chart.js** - (Available for future enhancements)
- **Marked.js** - Markdown rendering (for future stock pages)

---

## 🚀 Future Enhancements (Milestone 4-7)

- **Milestone 4**: Portfolio tracking with paper gains/losses
- **Milestone 5**: Auto-regeneration system with buy/sell decisions
- **Milestone 6**: Agent self-improvement capabilities
- **Milestone 7**: Full-stack production (React + Node.js + MariaDB + Docker)

---

## 📝 Data Sources

- **Market Data**: Yahoo Finance (Real-time, Nov 21, 2025 21:55:30)
- **Analysis**: 7-stage investment analysis system (60% fundamental + 40% technical)
- **Money Flow**: MoneyFlowAnalyzer agent (institutional vs retail activity)
- **Rankings**: RankingEngine agent (composite score ≥ 7.0)

---

## ⚠️ Disclaimer

This is educational analysis, not financial advice. Always consult a licensed financial advisor before making investment decisions.

---

## 🎉 Let's Get Rich Together!

**Generated**: Nov 21, 2025
**Capital**: RM 50,000
**Expected Return**: 14-17% (18-22% w/ dividends)
**Status**: ✅ Ready to Build Wealth!

---

**Milestone 3: Complete** ✅

Next: Milestone 4 - Portfolio Tracking System 🚀
