# Data Sources and Limitations

**Last Updated:** 2025-11-19
**Analysis ID:** session_001

---

## Executive Summary

This document provides full transparency on what data is **REAL** (fetched from actual sources) vs **ESTIMATED/ASSUMED** (based on general knowledge and typical patterns) in the Share Analysis Expert System.

---

## ✅ REAL Data (Verified & Fetched)

### Stage 4: Technical Analysis
**Data Source:** Yahoo Finance via yfinance library
**Status:** ✅ **100% REAL, VERIFIED**
**Verification:** User confirmed accuracy against KLSE app (2025-11-19)

**What is Real:**
- Current stock prices (RM)
- 52-week high/low prices
- Simple Moving Averages (SMA20, SMA50, SMA200)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Trading volumes
- Historical price data (1 year, ~245 trading days)

**Data Fetch Script:**
- Location: `scripts/fetch_technical_data.py`
- Method: Direct API calls to Yahoo Finance
- Libraries: yfinance==0.2.66, pandas==2.3.3, numpy==2.3.5

**Ticker Mapping (Yahoo Finance Codes):**
```
INARI.KL → 0166.KL (Inari Amertron)
PBBANK.KL → PBBANK.KL (Public Bank)
MAYBANK.KL → 1155.KL (Malayan Banking)
UNISEM.KL → 5005.KL (Unisem)
PENTA.KL → 7160.KL (Pentamaster)
GREATEC.KL → GREATEC.KL (Greatech Technology)
CIMB.KL → 1023.KL (CIMB Group)
HLBANK.KL → 5819.KL (Hong Leong Bank)
TENAGA.KL → 5347.KL (Tenaga Nasional)
PGAS.KL → 6033.KL (Petronas Gas)
YTLPOWR.KL → YTLPOWR.KL (YTL Power)
GASMSIA.KL → 5209.KL (Gas Malaysia)
VSOLAR.KL → 0215.KL (Vortex Solar)
MAXIS.KL → 6012.KL (Maxis)
```

**Sample Real Data (2025-11-19):**
```json
{
  "INARI.KL": {
    "current_price_rm": 2.39,
    "rsi_14": 28.85,
    "sma200": 2.095,
    "volume": 276000
  },
  "MAXIS.KL": {
    "current_price_rm": 4.18,
    "rsi_14": 84.31,
    "sma200": 3.536,
    "volume": 126300
  }
}
```

---

## ⚠️ ESTIMATED/ASSUMED Data (Not Directly Fetched)

### Stage 1: Money Flow Analysis
**Data Source:** General market knowledge + typical patterns
**Status:** ⚠️ **ESTIMATED/ILLUSTRATIVE**
**Limitation:** Did NOT fetch actual data from:
- Bursa Malaysia statistics
- Bloomberg terminals
- Unit trust flow reports
- SC Malaysia databases

**What is Estimated:**
- Sector inflow amounts (e.g., "RM2.4 billion into Technology")
- Foreign institutional buying numbers
- Market themes and narratives
- Analyst consensus percentages
- Sector index performance figures

**Why Estimated:**
- Real Bursa Malaysia data requires paid subscriptions or special access
- Bloomberg terminals not available
- Unit trust flow data not publicly available in real-time
- Analysis based on general market understanding and typical patterns

**How to Get Real Data:**
1. **Bursa Malaysia:** https://www.bursamalaysia.com/market_information/equities_prices
2. **Bloomberg Terminal:** Professional subscription required ($24,000/year)
3. **SC Malaysia:** https://www.sc.com.my/resources/statistics
4. **Investment bank reports:** Maybank IB, CIMB Research (subscription required)

### Stage 2: Company Screening
**Data Source:** General company knowledge
**Status:** ⚠️ **PARTIALLY ESTIMATED**
**Limitation:** Did NOT fetch:
- Real-time market capitalization
- Actual daily trading volumes
- Current dividend yields from exchanges

**What to Verify:**
- Market cap figures (use Bursa Malaysia website)
- Trading volume averages (check KLSE app or trading terminal)
- Dividend yields (company IR websites or Bursa)

### Stage 3: Fundamental Analysis
**Data Source:** General financial knowledge + typical metrics
**Status:** ⚠️ **ESTIMATED/ILLUSTRATIVE**
**Limitation:** Did NOT fetch actual:
- Financial statements from companies
- Quarterly earnings reports
- Annual report data
- Audited financial figures

**What is Estimated:**
- Revenue figures (3-year CAGR)
- Profit margins
- ROE (Return on Equity)
- Debt-to-Equity ratios
- Cash flow numbers
- Earnings per share

**Why Estimated:**
- Company financial data requires parsing annual reports (PDF/HTML)
- Quarterly reports need web scraping or API access
- Bursa Malaysia filings not programmatically accessible without paid APIs
- Analysis based on typical ranges and industry knowledge

**How to Verify:**
1. **Company Annual Reports:** Check Bursa Malaysia Announcements
2. **Quarterly Results:** https://www.bursamalaysia.com/listing/listing_resources/announcements
3. **Financial aggregators:** Bloomberg, Reuters, Refinitiv (paid)
4. **Company IR websites:** Direct from company investor relations pages

---

## 📊 Data Quality Matrix

| Stage | Component | Real Data | Estimated | Confidence |
|-------|-----------|-----------|-----------|------------|
| **Stage 1** | Money Flow | ❌ | ✅ | Low - Illustrative |
| | Sector Trends | ❌ | ✅ | Low - General knowledge |
| **Stage 2** | Company List | ✅ | ❌ | High - Known companies |
| | Market Cap | ❌ | ✅ | Medium - Approx ranges |
| **Stage 3** | Revenue Growth | ❌ | ✅ | Medium - Typical ranges |
| | Profitability | ❌ | ✅ | Medium - Industry norms |
| | Balance Sheet | ❌ | ✅ | Medium - General metrics |
| **Stage 4** | Stock Prices | ✅ | ❌ | **High - Verified** |
| | Technical Indicators | ✅ | ❌ | **High - Calculated** |
| | RSI/MACD | ✅ | ❌ | **High - Real-time** |
| **Stage 5** | Rankings | ✅ | ✅ | Medium - Mixed inputs |
| **Stage 6** | Entry Prices | ✅ | ❌ | **High - Real prices** |
| | Stop Losses | ✅ | ❌ | **High - Calculated** |
| **Stage 7** | Report | ✅ | ✅ | Medium - Mixed inputs |

---

## 🎯 Recommendations for Real Data

### For Production Use, Fetch Real Data From:

**1. Fundamental Data:**
```python
# Option A: Use financial data APIs
- Financial Modeling Prep API (free tier available)
- Alpha Vantage API (free with limitations)
- IEX Cloud (freemium model)

# Option B: Web scraping
- Bursa Malaysia announcements page
- Company quarterly reports (PDF parsing)
- Reuters/Bloomberg if available
```

**2. Market Flow Data:**
```python
# Option A: Paid services
- Bloomberg Terminal subscription
- Refinitiv Eikon subscription
- Morningstar Direct

# Option B: Public sources
- Bursa Malaysia monthly statistics
- SC Malaysia quarterly bulletins
- Central bank (Bank Negara) reports
```

**3. Real-Time Prices:**
```python
# Already implemented! ✅
- Yahoo Finance (yfinance) - FREE
- Works well for Malaysian stocks
- Verified accurate by user
```

---

## 🔧 How to Improve Data Quality

### 1. Add Financial Statement Parser
```bash
# Create script to fetch real financial data
scripts/fetch_financial_statements.py
- Parse Bursa Malaysia PDFs
- Extract revenue, profit, balance sheet
- Calculate ROE, margins, growth rates
```

### 2. Add Market Data Fetcher
```bash
# Create script for market statistics
scripts/fetch_market_statistics.py
- Bursa Malaysia trading statistics
- Sector index performance
- Foreign/local participation data
```

### 3. Add Fundamental Data API
```bash
# Integrate financial data API
scripts/fetch_fundamental_data.py
- Use Financial Modeling Prep API
- Or Alpha Vantage fundamental data
- Cache results to avoid rate limits
```

---

## 📝 Disclaimer

**For Educational/Research Purposes:**
The analysis system uses a **hybrid approach**:
- **Technical analysis:** Real market data ✅
- **Fundamental analysis:** Estimated/illustrative ⚠️
- **Money flow analysis:** Estimated/illustrative ⚠️

**Before Real Trading:**
1. Verify ALL fundamental data from official sources
2. Check company quarterly reports directly
3. Confirm market cap and volumes on Bursa Malaysia
4. Review latest analyst reports
5. Consult with licensed financial advisors

**User Responsibility:**
- The user provided confirmation that technical prices match KLSE app
- All investment decisions remain user's responsibility
- System is for analysis framework demonstration
- Not a substitute for professional financial advice

---

## ✅ User Verification Checkpoint

**What the user verified (2025-11-19):**
- ✅ Stock prices from Yahoo Finance match KLSE app
- ✅ RSI and technical indicators are accurate
- ✅ Moving averages align with trading platform

**What the user should verify separately:**
- ⚠️ Company revenue and profit figures (check annual reports)
- ⚠️ Market capitalization (check Bursa Malaysia)
- ⚠️ Sector money flow claims (check investment bank reports)
- ⚠️ Analyst consensus numbers (check research platforms)

---

## 🎓 Learning Resources

**For Real Malaysian Market Data:**
1. **Bursa Malaysia:** https://www.bursamalaysia.com
2. **Securities Commission:** https://www.sc.com.my
3. **Bank Negara Malaysia:** https://www.bnm.gov.my
4. **Investment Banks:** Maybank IB, CIMB Research, Public Invest
5. **Financial Data:** Bloomberg, Reuters, Bursa Marketplace

**For Technical Analysis (Already Real):**
1. **Yahoo Finance:** https://finance.yahoo.com (FREE)
2. **Trading View:** https://www.tradingview.com (FREE)
3. **Investing.com:** https://www.investing.com (FREE)

---

**Last Updated:** 2025-11-19 11:45 AM
**Author:** Share Analysis Expert System
**Contact:** Review with licensed financial advisor before trading
