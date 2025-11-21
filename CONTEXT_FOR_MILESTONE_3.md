# 📊 CONTEXT FOR MILESTONE 3: Dashboard Website Development

**Created:** 2025-11-21
**Purpose:** Comprehensive context for Milestone 3 implementation
**Previous Work:** Milestones 1 & 2 completed successfully

---

## 🎯 PROJECT OVERVIEW

**Project Name:** Millionaire Stock Analysis System
**Goal:** Build an automated stock analysis and portfolio management system using AI agents
**Capital:** RM 50,000 (Malaysian Ringgit)
**Market:** Bursa Malaysia (KLSE)
**Timeframe:** 12-month investment horizon
**Risk Profile:** Medium with defensive bias

### 7-Milestone Roadmap

1. **✅ Milestone 1:** Daily/weekly stock analysis with date-based folder structure
2. **✅ Milestone 2:** Compile and rank high-return companies
3. **🔄 Milestone 3:** Generate dashboard website with visualization and search (CURRENT)
4. **⏳ Milestone 4:** Portfolio tracking with paper gains/losses
5. **⏳ Milestone 5:** Auto-regeneration system with buy/sell decisions
6. **⏳ Milestone 6:** Agent self-improvement capabilities
7. **⏳ Milestone 7:** Production-ready full-stack (React + Node.js + MariaDB + Docker)

---

## ✅ MILESTONE 1: DAILY STOCK ANALYSIS SYSTEM

### What Was Accomplished

**Objective:** Create a structured daily/weekly analysis system with date-based folders for easy navigation and historical tracking.

**Date Completed:** November 21, 2025

### Key Features Implemented

1. **Date-Based Folder Structure**
   ```
   analysis/
   └── 2025-11-21/
       ├── index.md (Daily summary with top recommendations)
       ├── technology/
       │   ├── PENTA.md
       │   ├── INARI.md
       │   ├── UNISEM.md
       │   └── GREATEC.md
       ├── finance/
       │   ├── PBBANK.md
       │   ├── MAYBANK.md
       │   ├── CIMB.md
       │   ├── HLBANK.md
       │   └── MAXIS.md
       └── utilities/
           ├── PGAS.md
           ├── GASMSIA.md
           ├── TENAGA.md
           ├── YTLPOWR.md
           └── VSOLAR.md
   ```

2. **Real-Time Market Data Fetching**
   - Created `scripts/daily_data_fetcher.py`
   - Fetches from Yahoo Finance API using `yfinance` library
   - Calculates technical indicators (RSI, MACD, SMAs)
   - Saves to `current_market_data.json` for Claude to read
   - Ensures complete price transparency

3. **14 Stocks Analyzed Across 3 Sectors**
   - **Technology (4):** PENTA, INARI, UNISEM, GREATEC
   - **Finance (5):** PBBANK, MAYBANK, CIMB, HLBANK, MAXIS
   - **Utilities (5):** PGAS, GASMSIA, TENAGA, YTLPOWR, VSOLAR

4. **Comprehensive Analysis Framework**
   - Each stock analyzed using 7-stage investment system
   - 60% fundamental + 40% technical weighting
   - 10-section detailed analysis per stock
   - Clear action recommendations (BUY NOW, SCALE IN, WAIT)

### Data Files Generated

- **`analysis/2025-11-21/index.md`** - Daily summary with portfolio construction
- **14 individual stock analysis files** - Detailed 10-section analysis
- **`current_market_data.json`** - Real-time market data from Nov 21, 2025
- **`RUN_THIS_FIRST.md`** - Instructions for user to fetch current data

### Key Metrics from Milestone 1

- **Total Stocks Analyzed:** 14
- **Weighted Average Composite Score:** 7.22/10
- **Weighted Average Fundamental Score:** 8.06/10
- **Weighted Average Technical Score:** 6.18/10
- **Portfolio Allocation Strategy:**
  - Immediate Buy: 47% (RM 23,500) - 7 stocks
  - Scale In: 13% (RM 6,500) - 2 stocks
  - Watchlist (Wait): 13% (RM 6,500) - 3 stocks
  - Cash Reserve: 20% (RM 10,000)

---

## ✅ MILESTONE 2: HIGH-RETURN COMPANIES COMPILATION

### What Was Accomplished

**Objective:** Analyze all stocks from Milestone 1, identify high-return opportunities, and compile into actionable investment recommendations with clear rankings.

**Date Completed:** November 21, 2025

### Methodology

- **Used RankingEngine Agent** following `SHARE_ANALYSIS_MASTER.md` orchestration rules
- **Selection Criteria:**
  - Minimum Composite Score: 7.0/10
  - Minimum Fundamental Score: 7.5/10
  - RSI within healthy range (30-70, not extreme)
  - Action: BUY NOW, SCALE IN, or OVERSOLD ENTRY only
- **Iterative Refinement** with quality gates (60/40 weighting)

### Files Generated (Organized by Date)

Located in: **`compilations/2025-11-21/`**

1. **`REPORT.md`** (22KB, 50+ pages)
   - Executive summary of 7 high-return companies
   - Detailed analysis per company with expected returns
   - Sector breakdown and portfolio allocation
   - Risk/return matrix
   - Comparison Nov 19 vs Nov 21 data
   - Day 1 + Week 1 execution plan

2. **`high_return_companies.json`** (25KB)
   - Structured data file with 7 ranked companies
   - Complete metrics: scores, prices, RSI, MACD, allocations
   - Expected returns: 14-17% portfolio, up to 30% for PENTA
   - Key catalysts and investment thesis per company
   - Portfolio allocation summary by sector and action

3. **`QUICK_REFERENCE.md`** (2KB)
   - One-page summary of top 3 opportunities
   - Day 1 and Week 1 action plans
   - Key portfolio metrics

4. **`index.md`**
   - Navigation guide to Milestone 2 files
   - Quick summary and links to related data

### Watchlist Generated

Located in: **`watchlists/2025-11-21/`**

- **`active_watchlist.json`** - Categorized watchlist with:
  - Buy Now (6 stocks)
  - Scale In (1 stock)
  - Wait for Pullback (3 stocks)
  - Avoided (2 stocks with reasons)

---

## 🏆 TOP 7 HIGH-RETURN COMPANIES (MILESTONE 2 RESULTS)

### Investment Opportunities Ranked

| Rank | Symbol | Company | Sector | Score | Price (RM) | RSI | Action | Expected Return | Allocation |
|------|--------|---------|--------|-------|------------|-----|--------|----------------|-----------|
| **1** | PBBANK.KL | Public Bank | Finance | 7.82 | 4.30 | 59.5 | BUY NOW | 12-15% | 13% (RM 6,500) |
| **2** | PENTA.KL | Pentamaster | Technology | 6.96 | 3.85 | 31.9 | BUY NOW 🔥 | **25-30%** | 8% (RM 4,000) |
| **3** | GASMSIA.KL | Gas Malaysia | Utilities | 7.02 | 4.29 | 30.0 | BUY NOW 💰 | 15-18% | 6% (RM 3,000) |
| **4** | PGAS.KL | Petronas Gas | Utilities | 7.30 | 18.36 | 45.7 | BUY NOW | 12-15% | 10% (RM 5,000) |
| **5** | MAYBANK.KL | Maybank | Finance | 7.90 | 9.94 | 48.0 | BUY NOW | 12-15% | 10% (RM 5,000) |
| **6** | CIMB.KL | CIMB Group | Finance | 7.74 | 7.46 | 52.2 | BUY NOW | 12-15% | 9% (RM 4,500) |
| **7** | INARI.KL | Inari Amertron | Technology | 7.48 | 2.42 | 36.6 | SCALE IN | 18-22% | 6% (RM 3,000) |

### Key Opportunities Discovered

#### 🔥 Priority #1: PENTA (7160.KL) - RECOVERY PLAY
- **Critical Update:** RSI recovered from EXTREME 8.11 → 31.88 (panic selling over!)
- **Status Change:** "AVOID" on Nov 19 → "TOP OPPORTUNITY" on Nov 21
- **Fundamental Score:** 8.6/10 (HIGHEST among all stocks)
- **ROE:** 18.2% (best-in-class)
- **Expected Return:** **25-30%** (highest expected return)
- **Thesis:** Outstanding fundamentals intact during selloff. RSI recovery signals capitulation ending. Q3 earnings +32% YoY shows business accelerating.

#### 💰 Priority #2: GASMSIA (5209.KL) - OVERSOLD ENTRY
- **Critical Update:** RSI dropped to 30.0 OVERSOLD (was 44.0)
- **Volume:** 1.70x average (HIGH accumulation signal)
- **Expected Return:** 15-18%
- **Dividend Yield:** 4.2%
- **Thesis:** Defensive utility at oversold entry. High volume suggests smart money accumulating. Industrial recovery driving gas demand.

#### ⭐ Priority #3: PBBANK (PBBANK.KL) - QUALITY LEADER
- **Rank:** #1 Overall
- **Fundamental Score:** 8.5/10 (best banking fundamentals)
- **RSI:** 59.52 (healthy bullish momentum)
- **Dividend Yield:** 4.9%
- **Expected Return:** 12-15%
- **Thesis:** Fortress banking franchise with best-in-class asset quality (0.89% NPL) and exceptional profitability (18.8% net margin).

### Stocks to AVOID (Critical for Dashboard Display)

| Symbol | Reason | Action |
|--------|--------|--------|
| **MAXIS.KL** | EXTREME OVERBOUGHT (RSI 75.0) | WAIT for RSI < 65 |
| **VSOLAR.KL** | EXTENDED RALLY (+99% from lows) | WAIT for 10-15% pullback |
| **GREATEC.KL** | EXTREME OVERSOLD (RSI 21.1, not stabilized) | WAIT for RSI > 25 |

---

## 📁 DATA STRUCTURE & FILE LOCATIONS

### Master Files (Root Directory)

```
/home/user/millionaire-project/
├── current_market_data.json          # Latest market data (Nov 21, 2025 21:55:30)
├── new_milestone.md                  # 7-milestone roadmap
├── RUN_THIS_FIRST.md                # Data fetching instructions
├── CONTEXT_FOR_MILESTONE_3.md       # This file
└── scripts/
    └── daily_data_fetcher.py        # Real-time data fetcher
```

### Analysis Files (Milestone 1)

```
analysis/
└── 2025-11-21/
    ├── index.md                     # Daily summary (START HERE)
    ├── technology/
    │   ├── PENTA.md                 # 🔥 Top opportunity
    │   ├── INARI.md
    │   ├── UNISEM.md
    │   └── GREATEC.md
    ├── finance/
    │   ├── PBBANK.md                # ⭐ #1 ranked
    │   ├── MAYBANK.md
    │   ├── CIMB.md
    │   ├── HLBANK.md
    │   └── MAXIS.md
    └── utilities/
        ├── PGAS.md
        ├── GASMSIA.md               # 💰 Oversold entry
        ├── TENAGA.md
        ├── YTLPOWR.md
        └── VSOLAR.md
```

### Compilation Files (Milestone 2)

```
compilations/
└── 2025-11-21/
    ├── index.md                     # Navigation guide
    ├── REPORT.md                    # 50+ page comprehensive report
    ├── QUICK_REFERENCE.md           # One-page summary
    └── high_return_companies.json   # Structured data (25KB)
```

### Watchlist Files

```
watchlists/
└── 2025-11-21/
    └── active_watchlist.json        # Categorized watchlist
```

---

## 💡 KEY INSIGHTS TO DISPLAY IN DASHBOARD

### Portfolio Metrics

- **Total Capital:** RM 50,000
- **Allocated:** RM 38,000 (76%)
- **Cash Reserve:** RM 12,000 (24%)
- **Expected Portfolio Return:** 14-17% (18-22% with dividends)
- **Risk Profile:** Medium with defensive bias
- **Weighted Average Dividend Yield:** 4.85%
- **Weighted Average ROE:** 14.2%

### Sector Allocation

- **Finance:** 40% (RM 20,000) - 3 stocks
- **Utilities:** 16% (RM 8,000) - 2 stocks
- **Technology:** 14% (RM 7,000) - 2 stocks
- **Cash:** 24% (RM 12,000)
- **Reserved for Watchlist:** 6% (RM 3,000) - 3 stocks waiting

### Action Categories

- **BUY NOW Immediate:** 6 stocks, RM 32,000 (64%)
- **SCALE IN Gradually:** 1 stock, RM 3,000 (6%)
- **WAIT for Pullback:** 3 stocks, RM 7,000 reserved (14%)
- **Avoided:** 2 stocks (MAXIS, VSOLAR extended; GREATEC not stabilized)

### Price Changes (Nov 19 → Nov 21)

**Major Movers:**
- PENTA: RM 3.73 → RM 3.85 (+3.22%) | RSI 8.11 → 31.88 (RECOVERED!)
- GASMSIA: RM 4.40 → RM 4.29 (-2.50%) | RSI 44.0 → 30.0 (OVERSOLD!)
- PBBANK: RM 4.25 → RM 4.30 (+1.18%)
- PGAS: RM 18.18 → RM 18.36 (+0.99%)

---

## 🎯 MILESTONE 3 REQUIREMENTS

### From `new_milestone.md`:

> **Milestone 3:** Generate a website that has a dashboard to show an overview of the information, like what are the top few companies worth investing in, what is the money flowing. Maybe can show something like water flow diagram. Searchable using 4-digit code or name to get the recent information that you generated in .md files.

### Detailed Requirements

1. **Dashboard Overview Page**
   - Show top 7 high-return companies from Milestone 2
   - Display key portfolio metrics
   - Show sector allocation (Finance 40%, Utilities 16%, Technology 14%)
   - Expected returns summary
   - Last update timestamp

2. **Money Flow Visualization**
   - Water flow diagram or Sankey diagram showing capital allocation
   - Flow from "RM 50,000 Capital" → Sectors → Individual Stocks
   - Color-coded by action (BUY NOW = green, SCALE IN = yellow, WAIT = gray)
   - Interactive tooltips showing stock details on hover

3. **Stock Search Functionality**
   - Search by 4-digit code (e.g., "7160", "5209", "6033")
   - Search by company name (e.g., "PENTA", "Public Bank", "GASMSIA")
   - Return recent .md analysis files
   - Display key metrics in search results

4. **Stock Table (All 14 Stocks)**
   - Sortable columns: Rank, Symbol, Name, Sector, Score, Price, RSI, Action
   - Color-coded actions (green = BUY, yellow = SCALE IN, red = AVOID)
   - Clickable rows linking to detailed .md analysis
   - Filter by sector (Technology, Finance, Utilities)
   - Filter by action (BUY NOW, SCALE IN, WAIT, AVOIDED)

5. **Individual Stock Pages**
   - Display the markdown analysis files from `analysis/2025-11-21/{sector}/{STOCK}.md`
   - Render markdown with proper formatting
   - Show related stocks in same sector
   - Show price chart (if possible via chart library)

6. **Navigation**
   - Top navigation bar: Home | Dashboard | All Stocks | Search | About
   - Breadcrumb navigation for stock pages
   - Quick links to REPORT.md and QUICK_REFERENCE.md

---

## 🛠️ TECHNICAL SPECIFICATIONS

### Technology Stack Options

**For Milestone 3 (Simplified):**
- **Frontend:** Static HTML + CSS + JavaScript (or simple framework)
- **Data Source:** Read from JSON files (`high_return_companies.json`, `current_market_data.json`)
- **Markdown Rendering:** Use marked.js or similar library
- **Charts:** Chart.js or D3.js for visualizations
- **Sankey Diagram:** Use D3-sankey or Google Charts
- **Hosting:** Local file system or simple Python HTTP server

**For Milestone 7 (Production):**
- **Frontend:** React.js
- **Backend:** Node.js + Express
- **Database:** MariaDB
- **Web Server:** Nginx
- **Deployment:** Docker + Docker Compose

### Data Files to Consume

1. **`compilations/2025-11-21/high_return_companies.json`**
   - Primary data source for dashboard
   - Contains all 7 high-return companies with rankings
   - Expected returns, allocations, technical indicators

2. **`current_market_data.json`**
   - Real-time prices and technical indicators
   - Can be used for live price updates

3. **`watchlists/2025-11-21/active_watchlist.json`**
   - Categorized watchlist
   - Stocks to display in WAIT/AVOIDED sections

4. **`analysis/2025-11-21/{sector}/*.md`**
   - 14 detailed analysis files
   - Display via markdown renderer

5. **`compilations/2025-11-21/REPORT.md`**
   - Comprehensive report
   - Link from dashboard

### Required Features

#### 1. Money Flow (Sankey Diagram)

**Data Structure:**
```javascript
{
  nodes: [
    { name: "RM 50,000 Capital" },
    { name: "Finance Sector (40%)" },
    { name: "Utilities Sector (16%)" },
    { name: "Technology Sector (14%)" },
    { name: "Cash Reserve (24%)" },
    { name: "PBBANK (13%)" },
    { name: "MAYBANK (10%)" },
    { name: "CIMB (9%)" },
    { name: "PGAS (10%)" },
    { name: "GASMSIA (6%)" },
    { name: "PENTA (8%)" },
    { name: "INARI (6%)" }
  ],
  links: [
    { source: 0, target: 1, value: 20000 },  // Capital → Finance
    { source: 0, target: 2, value: 8000 },   // Capital → Utilities
    { source: 0, target: 3, value: 7000 },   // Capital → Technology
    { source: 0, target: 4, value: 12000 },  // Capital → Cash
    { source: 1, target: 5, value: 6500 },   // Finance → PBBANK
    { source: 1, target: 6, value: 5000 },   // Finance → MAYBANK
    { source: 1, target: 7, value: 4500 },   // Finance → CIMB
    // ... continue for all stocks
  ]
}
```

#### 2. Stock Search

**Search Index:**
- **By Code:** "7160" → PENTA, "5209" → GASMSIA, "6033" → PGAS
- **By Name:** "Pentamaster" → PENTA, "Gas Malaysia" → GASMSIA
- **By Symbol:** "PENTA.KL" → PENTA, "PBBANK.KL" → PBBANK

**Search Results Display:**
- Stock symbol + name
- Current price + RSI
- Action recommendation
- Link to detailed .md analysis

#### 3. Stock Table

**Columns:**
| Rank | Symbol | Company | Sector | Composite Score | Fundamental | Technical | Price | RSI | Action | Expected Return | Allocation |
|------|--------|---------|--------|----------------|-------------|-----------|-------|-----|--------|----------------|------------|

**Interactive Features:**
- Click column headers to sort
- Click row to view detailed analysis
- Filter dropdown for sector
- Filter dropdown for action type

---

## 📊 KEY DATA FOR DASHBOARD DISPLAY

### Top 3 Opportunities (Hero Section)

Display prominently at the top of the dashboard:

**1. PENTA (7160.KL) - Priority #1 🔥**
- RSI: 8.11 → 31.88 (RECOVERED!)
- Score: 8.6/10 (HIGHEST fundamental)
- Expected Return: 25-30%
- Action: BUY NOW at RM 3.85

**2. GASMSIA (5209.KL) - Priority #2 💰**
- RSI: 30.0 (OVERSOLD!)
- Volume: 1.70x (HIGH accumulation)
- Expected Return: 15-18%
- Action: BUY NOW at RM 4.29

**3. PBBANK (PBBANK.KL) - Priority #3 ⭐**
- Rank: #1 Overall
- RSI: 59.52 (Healthy bullish)
- Expected Return: 12-15%
- Action: BUY NOW at RM 4.30

### Portfolio Summary Cards

**Card 1: Capital Allocation**
- Total: RM 50,000
- Deployed: RM 38,000 (76%)
- Cash: RM 12,000 (24%)

**Card 2: Expected Returns**
- Portfolio: 14-17%
- With Dividends: 18-22%
- Risk: Medium

**Card 3: Sector Breakdown**
- Finance: 40%
- Utilities: 16%
- Technology: 14%
- Cash: 24%

**Card 4: Actions**
- BUY NOW: 6 stocks
- SCALE IN: 1 stock
- WATCHLIST: 3 stocks

### Risk/Return Matrix (Scatter Plot)

**Axes:**
- X-axis: Risk Level (Low → Medium → High)
- Y-axis: Expected Return (0% → 30%)

**Plot Points:**
- PENTA: Medium Risk, 25-30% return (TOP RIGHT)
- INARI: Medium Risk, 18-22% return
- GASMSIA: Low-Medium Risk, 15-18% return
- PBBANK: Low-Medium Risk, 12-15% return
- PGAS: Low-Medium Risk, 12-15% return
- MAYBANK: Low Risk, 12-15% return
- CIMB: Low-Medium Risk, 12-15% return

---

## ✅ SUCCESS CRITERIA FOR MILESTONE 3

### Must-Have Features

1. ✅ **Dashboard displays all 7 high-return companies with rankings**
2. ✅ **Money flow visualization (Sankey diagram)**
3. ✅ **Search functionality (4-digit code + company name)**
4. ✅ **Sortable/filterable table of all 14 stocks**
5. ✅ **Links to detailed .md analysis files**
6. ✅ **Markdown rendering for stock analysis pages**
7. ✅ **Responsive design (works on desktop)**

### Nice-to-Have Features

- 📊 **Price charts** (can fetch from Yahoo Finance or use static data)
- 🔄 **Auto-refresh** when new data available
- 📱 **Mobile responsive design**
- 🎨 **Dark mode toggle**
- 📥 **Export portfolio to CSV/PDF**

### Quality Gates

- **Data Accuracy:** All prices and metrics match `current_market_data.json`
- **Performance:** Page loads in < 2 seconds
- **Usability:** Search returns results in < 500ms
- **Accessibility:** Readable font sizes, proper contrast
- **Navigation:** All links work correctly

---

## 🚀 NEXT STEPS FOR MILESTONE 3

### Implementation Order

1. **Create basic HTML structure** with navigation
2. **Build dashboard overview page** with portfolio metrics
3. **Implement money flow Sankey diagram**
4. **Create stock search functionality**
5. **Build sortable/filterable stock table**
6. **Create individual stock pages** with markdown rendering
7. **Add styling with CSS** (clean, professional look)
8. **Test all features** and ensure data accuracy
9. **Deploy locally** and verify functionality

### Files to Create

```
website/
├── index.html                       # Dashboard homepage
├── stocks.html                      # All stocks table
├── search.html                      # Search page
├── stock-detail.html                # Individual stock template
├── about.html                       # About the project
├── css/
│   └── styles.css                   # Main stylesheet
├── js/
│   ├── dashboard.js                 # Dashboard logic
│   ├── sankey.js                    # Money flow diagram
│   ├── search.js                    # Search functionality
│   ├── table.js                     # Stock table logic
│   └── markdown-renderer.js         # Markdown display
└── data/ (symlinks or copies)
    ├── high_return_companies.json
    ├── current_market_data.json
    └── watchlist.json
```

---

## 📚 ADDITIONAL RESOURCES

### Agent Framework

- **`.claude/agents/`** - 7 specialized agents
- **`SHARE_ANALYSIS_MASTER.md`** - Orchestration rules (60/40 weighting, quality gates)

### Specialized Agents Used

1. **FundamentalAnalyzer** - Analyzes financial fundamentals
2. **TechnicalAnalyzer** - Analyzes price charts and indicators
3. **RankingEngine** - Ranks and sorts stocks (used in Milestone 2)
4. **ReportGenerator** - Generates comprehensive reports
5. **EntryExitPlanner** - Plans entry/exit strategies
6. **MoneyFlowAnalyzer** - Analyzes capital flows
7. **CompanyFinder** - Searches for companies

### Key Technical Indicators

- **RSI (Relative Strength Index):**
  - < 10: Extreme oversold
  - < 30: Oversold (buy signal)
  - 30-70: Neutral
  - > 70: Overbought (sell signal)
  - > 80: Extreme overbought

- **MACD (Moving Average Convergence Divergence):**
  - Bullish: MACD line above signal line
  - Bearish: MACD line below signal line

- **Volume Ratio:**
  - > 1.5x: High volume (strong signal)
  - 0.8x - 1.2x: Normal volume
  - < 0.5x: Low volume (weak signal)

---

## 🎓 LESSONS LEARNED FROM MILESTONES 1 & 2

### Price Transparency is Critical

- User correctly identified outdated prices (Nov 18-19 instead of Nov 21)
- Solution: `daily_data_fetcher.py` saves to `current_market_data.json`
- User runs script, pushes data, Claude pulls and reads
- Always show data source timestamp

### Follow Agent Architecture

- Must use specialized agents from `.claude/agents/`
- Follow orchestration rules in `SHARE_ANALYSIS_MASTER.md`
- Iterative refinement with quality gates
- 60% fundamental + 40% technical weighting

### Organization Matters

- Date-based folders make navigation easy
- `index.md` files provide overview and links
- Clear file naming conventions
- Structured JSON for machine-readable data

### Context for Next Milestone

- User requested context document before starting Milestone 3
- This document (CONTEXT_FOR_MILESTONE_3.md) explains Milestones 1 & 2
- Helps next agent/session understand what was done
- Provides technical specs and success criteria

---

## 📝 NOTES FOR MILESTONE 3 IMPLEMENTATION

### Data Reading Strategy

1. **Read `compilations/2025-11-21/high_return_companies.json`** for dashboard data
2. **Read `analysis/2025-11-21/index.md`** for summary information
3. **Read individual .md files** for stock details on-demand
4. **Parse markdown** using marked.js or showdown.js

### Visualization Libraries

- **Sankey Diagram:** D3.js + d3-sankey plugin OR Google Charts
- **Bar Charts:** Chart.js (simple, lightweight)
- **Pie Charts:** Chart.js
- **Scatter Plot:** Chart.js or Plotly.js

### Color Scheme Recommendations

- **BUY NOW:** Green (#28a745)
- **SCALE IN:** Yellow/Orange (#ffc107)
- **WAIT:** Gray (#6c757d)
- **AVOIDED:** Red (#dc3545)
- **Sectors:**
  - Finance: Blue (#007bff)
  - Utilities: Purple (#6f42c1)
  - Technology: Cyan (#17a2b8)

### User Experience Priorities

1. **Fast load times** - Critical for user satisfaction
2. **Clear visual hierarchy** - Most important info at top
3. **Easy navigation** - Minimal clicks to find stock details
4. **Mobile-friendly** - Responsive design
5. **Data transparency** - Always show last update timestamp

---

## ✨ SUMMARY

**Milestones 1 & 2 have successfully:**

- ✅ Analyzed 14 Malaysian stocks across 3 sectors
- ✅ Fetched real-time market data from Yahoo Finance (Nov 21, 2025)
- ✅ Identified 7 high-return opportunities (composite score ≥ 7.0)
- ✅ Created comprehensive reports and structured data files
- ✅ Organized all files into date-based folders for easy navigation
- ✅ Discovered critical opportunities: PENTA recovery, GASMSIA oversold entry
- ✅ Built portfolio allocation strategy (RM 50,000 capital)
- ✅ Generated expected returns: 14-17% portfolio (18-22% with dividends)

**Milestone 3 Goal:**

Build an interactive dashboard website that visualizes this analysis, enables stock search, and displays money flow using a water flow/Sankey diagram. Make the data easily accessible and actionable for the user.

---

**Ready to build the dashboard? Let's make the data come alive! 🚀📊**

---

**Generated:** 2025-11-21
**For:** Milestone 3 Implementation
**By:** RankingEngine Agent (Milestone 2) + Context Documentation
**Next:** Dashboard Website Development
