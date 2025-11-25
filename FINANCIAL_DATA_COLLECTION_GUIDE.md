# Financial Data Collection Guide

**Purpose:** Automate the collection of quarterly and annual financial reports for Malaysian stocks using FREE APIs.

**Created:** 2025-11-25
**Last Updated:** 2025-11-25

---

## 🎯 What This Script Does

The `fetch_financial_data.py` script automatically downloads:

1. **Annual Financial Statements** (last 3-5 years)
   - Income Statement (Revenue, Net Profit, Expenses)
   - Balance Sheet (Assets, Liabilities, Equity, Debt)
   - Cash Flow Statement (Operating, Investing, Financing)

2. **Quarterly Financial Statements** (last 4-8 quarters)
   - Quarterly Income Statement
   - Quarterly Balance Sheet
   - Quarterly Cash Flow
   - Quarterly Earnings History

3. **Calculated Metrics** (auto-computed)
   - Revenue Growth (YoY %)
   - Net Profit Margin (%)
   - ROE - Return on Equity (%)
   - Debt to Equity Ratio
   - Quarterly Momentum (improving/deteriorating)

4. **Company Information**
   - Sector, Industry
   - Market Cap
   - Employee Count
   - Business Description

---

## 📦 Data Source: 100% FREE

**Primary:** Yahoo Finance API via `yfinance` library
- ✅ FREE forever
- ✅ No API keys needed
- ✅ Covers Malaysian stocks (KLSE)
- ✅ Updated regularly (usually within 24-48 hours of company filings)

**Note:** Data comes from Bursa Malaysia filings → Yahoo Finance → Your system

---

## 🚀 Installation

### 1. Install Required Library

```bash
cd /home/user/millionaire-project

# Install yfinance (FREE Yahoo Finance API)
pip3 install yfinance

# Or if using requirements.txt
echo "yfinance>=0.2.0" >> requirements.txt
pip3 install -r requirements.txt
```

### 2. Make Script Executable

```bash
chmod +x scripts/fetch_financial_data.py
```

---

## 📖 How to Use

### Method 1: Fetch Specific Symbols

```bash
# Single stock
python3 scripts/fetch_financial_data.py --symbols PBBANK.KL

# Multiple stocks (comma-separated)
python3 scripts/fetch_financial_data.py --symbols PBBANK.KL,GASMSIA.KL,PENTA.KL

# All stocks in a list
python3 scripts/fetch_financial_data.py --symbols PBBANK.KL,MAYBANK.KL,CIMB.KL,GENM.KL,TENAGA.KL
```

### Method 2: Fetch from Portfolio/Watchlist File

```bash
# From your portfolio
python3 scripts/fetch_financial_data.py --file portfolio.json

# From a watchlist
python3 scripts/fetch_financial_data.py --file watchlists/priority.json

# From any JSON file with symbols
python3 scripts/fetch_financial_data.py --file my_stocks.json
```

### Method 3: Custom Options

```bash
# Custom output directory
python3 scripts/fetch_financial_data.py --symbols PBBANK.KL --output data/my_reports

# Custom delay between requests (be respectful to API)
python3 scripts/fetch_financial_data.py --symbols PBBANK.KL,MAYBANK.KL --delay 3

# Full example
python3 scripts/fetch_financial_data.py \
  --file portfolio.json \
  --output data/financial_reports \
  --delay 2
```

---

## 📂 Output Format

### Directory Structure

```
millionaire-project/
├── data/
│   └── financial_reports/
│       ├── PBBANK_financials.json
│       ├── GASMSIA_financials.json
│       ├── PENTA_financials.json
│       └── _fetch_summary.json
```

### Example Output File: `PBBANK_financials.json`

```json
{
  "symbol": "PBBANK.KL",
  "company_name": "Public Bank Berhad",
  "sector": "Financial Services",
  "industry": "Banks - Regional",
  "currency": "MYR",
  "market_cap": 85000000000,
  "fetch_date": "2025-11-25 10:30:00",
  "data_source": "Yahoo Finance API (yfinance)",

  "annual_income_statement": {
    "2024-12-31": {
      "Total Revenue": 25500000000,
      "Net Income": 7200000000,
      "Operating Income": 9100000000,
      ...
    },
    "2023-12-31": {...},
    "2022-12-31": {...}
  },

  "annual_balance_sheet": {
    "2024-12-31": {
      "Total Assets": 520000000000,
      "Stockholders Equity": 45000000000,
      "Total Debt": 12000000000,
      ...
    }
  },

  "annual_cashflow": {
    "2024-12-31": {
      "Operating Cash Flow": 8500000000,
      "Free Cash Flow": 7200000000,
      ...
    }
  },

  "quarterly_income_statement": {
    "2024-12-31": {...},
    "2024-09-30": {...},
    "2024-06-30": {...},
    "2024-03-31": {...}
  },

  "calculated_metrics": {
    "metrics": {
      "latest_revenue": 25500000000,
      "latest_net_income": 7200000000,
      "net_profit_margin_pct": 28.24,
      "roe_pct": 16.0,
      "debt_to_equity": 0.27,
      "yoy_revenue_growth_pct": 5.2,
      "quarterly_momentum": "improving"
    }
  },

  "company_info": {
    "full_time_employees": 19000,
    "website": "http://www.pbebank.com",
    "description": "Public Bank Berhad provides banking...",
    "exchange": "KLSE"
  }
}
```

---

## ⏰ When to Run This Script

### Weekly (Recommended)
Run every **Monday morning** to catch weekend filings:

```bash
# Add to crontab (runs every Monday at 9am)
0 9 * * 1 cd /home/user/millionaire-project && python3 scripts/fetch_financial_data.py --file portfolio.json
```

### After Earnings Announcements
Malaysian companies typically announce quarterly results:
- **Q1:** End of April / Early May
- **Q2:** End of July / Early August
- **Q3:** End of October / Early November
- **Q4:** End of January / Early February

Run the script **2-3 days after** expected earnings dates to get latest data.

### Before Running Analysis
Always run **BEFORE** starting your weekly/monthly stock analysis:

```bash
# 1. Update financial data
python3 scripts/fetch_financial_data.py --file portfolio.json

# 2. Then run your analysis
# (Your analysis agents will use the fresh data)
```

### Manual Trigger
Run anytime you want fresh data for specific stocks:

```bash
python3 scripts/fetch_financial_data.py --symbols PENTA.KL
```

---

## 🔄 Integration with FundamentalAnalyzer

The FundamentalAnalyzer agent now reads from these auto-fetched files!

**Updated workflow:**

```
STEP 1: Fetch latest financial data
$ python3 scripts/fetch_financial_data.py --file portfolio.json

STEP 2: Run FundamentalAnalyzer
→ Agent reads: data/financial_reports/{symbol}_financials.json
→ Agent calculates: Revenue growth, ROE, margins, debt, etc.
→ Agent outputs: reports/fundamental_scores.json

STEP 3: Continue with TechnicalAnalyzer, RankingEngine, etc.
```

**No more manual downloads!** The agent automatically uses the JSON files.

---

## 📊 What Metrics Are Available

From the fetched data, FundamentalAnalyzer can calculate:

### Revenue Metrics
- 3-year Revenue CAGR
- YoY Revenue Growth (%)
- Quarterly Revenue Trends

### Profitability Metrics
- Net Profit Margin (%)
- Operating Margin (%)
- Gross Margin (%)
- ROE - Return on Equity (%)
- ROA - Return on Assets (%)

### Financial Health Metrics
- Debt to Equity Ratio
- Current Ratio
- Quick Ratio
- Interest Coverage

### Cash Flow Metrics
- Operating Cash Flow
- Free Cash Flow
- Cash Flow Margin (%)
- OCF vs Net Income Quality Check

### Quarterly Momentum
- Latest quarter vs previous quarter
- Latest quarter vs same quarter last year
- EPS growth trends
- Margin expansion/compression

---

## 🛠️ Troubleshooting

### Issue: "Module 'yfinance' not found"
**Solution:**
```bash
pip3 install yfinance
```

### Issue: "No data found for symbol XXXX.KL"
**Possible causes:**
1. Symbol not listed on Bursa Malaysia
2. Symbol format wrong (must include `.KL` suffix)
3. Company recently delisted
4. Temporary Yahoo Finance outage

**Solution:**
```bash
# Verify symbol on Bursa Malaysia website first
# Try fetching again after 5 minutes
# Check if symbol needs different suffix (.KLS, etc.)
```

### Issue: "Rate limit exceeded"
**Solution:**
```bash
# Increase delay between requests
python3 scripts/fetch_financial_data.py --symbols XXX.KL,YYY.KL --delay 5
```

### Issue: "Empty or incomplete data"
**Causes:**
- Company hasn't filed recent reports
- Data not yet available on Yahoo Finance
- Company is newly listed (<1 year)

**Solution:**
- Wait 24-48 hours after company announces results
- Check Bursa Malaysia website for manual download
- Some fields may be legitimately empty (e.g., no dividends)

---

## 🚨 Important Notes

### Data Freshness
- **Yahoo Finance updates:** Usually within 24-48 hours of company filings
- **Bursa Malaysia filings:** Official source, always most current
- **Your fetched data:** As fresh as Yahoo Finance has available

**Best practice:** Fetch data **2-3 days after** known earnings dates for accuracy.

### Data Quality
- ✅ **Revenue, Profit, Equity, Debt:** Very reliable
- ✅ **Cash Flow:** Reliable for most companies
- ⚠️ **Quarterly data:** May have slight delays
- ⚠️ **Very small companies:** May have incomplete data

### Respectful API Usage
- Default delay: **2 seconds** between requests
- This is respectful to Yahoo Finance's servers
- **Don't reduce delay below 1 second**
- If fetching 50+ stocks, use `--delay 3` or higher

### Legal & Ethical
- ✅ **Yahoo Finance API:** Free for personal use
- ✅ **Data is public:** Companies file these reports publicly
- ✅ **No scraping Bursa Malaysia paywall content**
- ✅ **For personal investment decisions only**

---

## 📈 Example Workflow

### Complete Monthly Analysis Workflow

```bash
# STEP 1: Update financial data (takes ~2 min for 10 stocks)
python3 scripts/fetch_financial_data.py --file portfolio.json

# STEP 2: Check what was fetched
cat data/financial_reports/_fetch_summary.json

# STEP 3: View a specific stock's data
cat data/financial_reports/PBBANK_financials.json | jq '.calculated_metrics'

# STEP 4: Run your stock analysis
# → FundamentalAnalyzer reads the JSON files
# → Calculates scores
# → Generates reports/fundamental_scores.json

# STEP 5: Continue with rest of analysis pipeline
# → TechnicalAnalyzer
# → RankingEngine
# → EntryExitPlanner
# → ReportGenerator
```

---

## 🎓 Understanding the Data

### Income Statement
- **Total Revenue:** All money coming in
- **Net Income:** Profit after all expenses and taxes
- **Operating Income:** Profit from core business operations

### Balance Sheet
- **Total Assets:** Everything the company owns
- **Stockholders Equity:** Net worth (Assets - Liabilities)
- **Total Debt:** All borrowed money

### Cash Flow Statement
- **Operating Cash Flow:** Cash generated from business operations
- **Free Cash Flow:** Cash available after capital expenditures
- **Investing/Financing Activities:** Where cash is being used

### Why These Matter
- **Revenue Growth:** Is the business growing?
- **Net Profit Margin:** How efficient is the business?
- **ROE:** How well does management use shareholder money?
- **Debt/Equity:** Is the company over-leveraged?
- **Operating Cash Flow:** Is profit real or just accounting?

---

## 🔮 Future Enhancements

Possible additions (if needed):
1. ✅ **Done:** Basic financial data fetching
2. ⏳ **Future:** Bursa Malaysia direct scraping (if Yahoo Finance data incomplete)
3. ⏳ **Future:** Dividend history tracking
4. ⏳ **Future:** Analyst estimates and guidance
5. ⏳ **Future:** Insider trading data
6. ⏳ **Future:** News sentiment analysis

---

## 📞 Support

**Issues with the script?**
1. Check Troubleshooting section above
2. Verify yfinance is installed: `pip3 show yfinance`
3. Test with a known-good symbol: `PBBANK.KL`
4. Check Yahoo Finance website manually for that stock

**Data quality concerns?**
- Cross-reference with Bursa Malaysia official filings
- Financial data may have slight variations between sources
- Always verify critical numbers before trading

---

## 📝 Summary

**What:** Automated quarterly & annual report fetcher
**How:** FREE Yahoo Finance API (yfinance library)
**When:** Weekly (Monday mornings) or before analysis runs
**Output:** JSON files in `data/financial_reports/`
**Integration:** FundamentalAnalyzer reads these files automatically

**Command to remember:**
```bash
python3 scripts/fetch_financial_data.py --file portfolio.json
```

**That's it!** No more manual report downloads. 100% free. 100% automated. 🚀

---

**Last Updated:** 2025-11-25
**Version:** 1.0
**Status:** ✅ Ready for production use
