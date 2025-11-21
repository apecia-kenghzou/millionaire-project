# Resources Directory

**Purpose:** Documentation, methodology, data sources, and evidence for all analysis stages

---

## Directory Structure

```
resources/
├── README.md (this file)
├── DATA_SOURCES_AND_LIMITATIONS.md ⭐
├── methodology/
│   ├── TECHNICAL_ANALYSIS_METHODOLOGY.md ⭐
│   ├── RANKING_METHODOLOGY.md
│   └── RISK_MANAGEMENT_METHODOLOGY.md
└── data_sources/
    ├── yahoo_finance_ticker_mapping.json
    └── bursa_malaysia_references.md
```

---

## Key Documents

### ⭐ DATA_SOURCES_AND_LIMITATIONS.md
**Must Read First!**

This document provides **100% transparency** on what data is:
- ✅ **REAL** (Yahoo Finance technical data - verified)
- ⚠️ **ESTIMATED** (Sector analysis, fundamentals - not directly fetched)

Read this to understand:
- What you can trust for real trading
- What needs verification from official sources
- How to get real data for production use
- Limitations of the current system

### ⭐ TECHNICAL_ANALYSIS_METHODOLOGY.md
**Technical Analysis Deep Dive**

Explains in detail:
- How RSI, MACD, SMA are calculated
- Technical score formula (Trend 30%, Momentum 40%, Volume 15%, S/R 15%)
- Action recommendation logic (BUY NOW vs WAIT vs SCALE IN)
- Real examples with step-by-step calculations
- Python code snippets for each indicator

---

## What Each Analysis Stage Uses

### Stage 1: MoneyFlowAnalyzer
- **Data:** ⚠️ ESTIMATED (not real Bursa Malaysia data)
- **Purpose:** Sector rotation framework
- **Limitation:** Use as conceptual guide, verify with real investment bank reports
- **Real Source:** Bloomberg, Maybank Research, CIMB Research

### Stage 2: CompanyFinder
- **Data:** ⚠️ PARTIALLY ESTIMATED
- **Purpose:** Company screening
- **Limitation:** Market cap and volume figures estimated
- **Real Source:** Bursa Malaysia website, KLSE Screener

### Stage 3: FundamentalAnalyzer
- **Data:** ⚠️ ESTIMATED (no real financial statements fetched)
- **Purpose:** Fundamental quality scoring
- **Limitation:** Revenue, profit, ROE figures based on general knowledge
- **Real Source:** Company annual reports, quarterly results on Bursa Malaysia

### Stage 4: TechnicalAnalyzer ⭐
- **Data:** ✅ **REAL** (Yahoo Finance)
- **Purpose:** Price action and momentum analysis
- **Verification:** User confirmed accurate vs KLSE app
- **Source:** `scripts/fetch_technical_data.py`
- **Status:** Production-ready for technical analysis

### Stage 5: RankingEngine
- **Data:** ✅ REAL (technical) + ⚠️ ESTIMATED (fundamental)
- **Formula:** Composite = (Fundamental × 60%) + (Technical × 40%)
- **Limitation:** 60% of score based on estimated fundamentals

### Stage 6: EntryExitPlanner
- **Data:** ✅ REAL (entry prices, stop losses based on real current prices)
- **Purpose:** Trading plan with specific price levels
- **Status:** Entry prices are real and actionable

### Stage 7: ReportGenerator
- **Data:** Mixed (real technical + estimated fundamental)
- **Purpose:** Final consolidated report
- **Limitation:** Verify fundamental claims before trading

---

## How to Use This for Real Trading

### ✅ Can Use Directly (REAL Data)
1. **Current stock prices** - from Yahoo Finance
2. **Technical indicators** - RSI, MACD, SMA calculations
3. **Entry price zones** - based on real current prices
4. **Stop loss levels** - calculated from real support levels
5. **Technical trends** - uptrend/downtrend/sideways classifications

### ⚠️ Must Verify Separately (ESTIMATED Data)
1. **Company financials** - Check annual reports on Bursa Malaysia
2. **Revenue and profit** - Verify from quarterly results
3. **Market capitalization** - Check Bursa Malaysia live data
4. **Sector money flow** - Read investment bank research reports
5. **Analyst consensus** - Check Bloomberg/Reuters if available

---

## Improvement Roadmap

### Phase 1: ✅ DONE
- [x] Real technical data from Yahoo Finance
- [x] Price verification vs KLSE app
- [x] RSI, MACD, SMA calculations
- [x] Transparent documentation

### Phase 2: 🔄 IN PROGRESS (This Documentation)
- [x] Clear labeling of real vs estimated data
- [x] Methodology documentation
- [x] Python scripts for transparency
- [ ] Bursa Malaysia data references

### Phase 3: 📋 TODO (Future Enhancements)
- [ ] Fetch real financial statements (PDF parsing)
- [ ] Integrate Financial Modeling Prep API
- [ ] Add Bursa Malaysia market statistics
- [ ] Real-time sector rotation data
- [ ] Automated quarterly earnings updates

---

## Scripts Reference

All analysis scripts are in `/scripts/` directory:

```
scripts/
├── fetch_technical_data.py ⭐ (REAL data fetcher)
├── test_yahoo_finance_tickers.py (Ticker validation)
└── (future: fetch_financials.py, fetch_market_stats.py)
```

### Key Script: fetch_technical_data.py

**What it does:**
1. Connects to Yahoo Finance API
2. Fetches 1 year of daily OHLCV data for 14 Malaysian stocks
3. Calculates RSI, MACD, SMA20/50/200
4. Saves to JSON for technical analysis

**Usage:**
```bash
cd /Users/apecia/Documents/project/millionaire
python3 scripts/fetch_technical_data.py
```

**Output:**
```
sessions/session_001/temp_technical_data_complete.json
```

---

## Data Sources for Manual Verification

### Official Malaysian Market Data

**Bursa Malaysia (Primary Exchange):**
- Website: https://www.bursamalaysia.com
- Market prices: https://www.bursamalaysia.com/market_information/equities_prices
- Company announcements: https://www.bursamalaysia.com/listing/listing_resources/announcements
- Trading statistics: https://www.bursamalaysia.com/statistics

**Securities Commission Malaysia:**
- Website: https://www.sc.com.my
- Statistics: https://www.sc.com.my/resources/statistics
- Unit trust data: https://www.sc.com.my/regulation/unit-trust-funds

**Bank Negara Malaysia (Central Bank):**
- Website: https://www.bnm.gov.my
- Economic reports: https://www.bnm.gov.my/publications
- Financial stability: https://www.bnm.gov.my/financial-stability

### Investment Research

**Investment Banks (Subscription Required):**
- Maybank Investment Bank Research
- CIMB Research
- Public Investment Bank Research
- RHB Investment Bank Research
- Hong Leong Investment Bank Research

**Financial Data Providers:**
- Bloomberg Terminal ($24,000/year)
- Refinitiv Eikon ($22,000/year)
- S&P Capital IQ ($12,000/year)
- FactSet ($12,000/year)

### Free Alternatives

**Yahoo Finance (Currently Used):**
- Website: https://finance.yahoo.com
- API: yfinance Python library (FREE)
- Coverage: Prices, technical indicators ✅
- Limitation: Limited fundamental data

**Trading View:**
- Website: https://www.tradingview.com
- Free charts with technical indicators
- Real-time Malaysian stock data
- Community scripts and ideas

**Investing.com:**
- Website: https://www.investing.com
- Real-time prices (free)
- Basic fundamentals (free)
- Economic calendar (free)

---

## Quality Assurance

### Data Verification Checklist

Before trading based on this analysis:

- [ ] Verify current stock prices on Bursa Malaysia or KLSE app
- [ ] Check company latest quarterly results (Bursa announcements)
- [ ] Review annual reports for financial metrics
- [ ] Confirm market cap on official exchange website
- [ ] Read latest analyst reports if available
- [ ] Check dividend history on company IR website
- [ ] Verify sector trends with investment bank research
- [ ] Consult with licensed financial advisor
- [ ] Understand your own risk tolerance
- [ ] Have emergency fund and capital you can afford to lose

---

## Contact & Disclaimer

**System Purpose:**
Educational demonstration of stock analysis framework combining technical (REAL) and fundamental (ESTIMATED) analysis.

**Not Financial Advice:**
This system is NOT a substitute for:
- Professional financial advisory services
- Licensed investment advisors
- Your own due diligence and research
- Official company disclosures and filings

**User Responsibility:**
- All investment decisions are your own responsibility
- Past performance does not guarantee future results
- Markets can be unpredictable and volatile
- Only invest capital you can afford to lose
- Diversification does not guarantee profit or protect against loss

**For Questions:**
- Review documentation in this folder
- Check scripts for calculation methods
- Verify all data with official sources
- Consult licensed financial professionals

---

**Last Updated:** 2025-11-19
**Version:** 1.0
**Status:** Documentation complete, system operational with transparency
