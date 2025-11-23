# 🔄 AUTO-REGENERATION PROMPT - Milestone 5

**Purpose:** Regenerate all stock analysis with fresh market data and make intelligent buy/sell/hold decisions based on current portfolio holdings.

**When to run:** Daily or weekly to keep analysis current and optimize portfolio.

**What this does:**
1. ✅ Fetch fresh market data from Yahoo Finance
2. ✅ Re-analyze all 14 stocks with current prices
3. ✅ Review current portfolio holdings
4. ✅ Make HOLD/SELL/BUY MORE decisions for each holding
5. ✅ Identify new stocks to buy
6. ✅ Generate updated recommendations
7. ✅ Update dashboard with new data

---

## 📋 INSTRUCTIONS FOR CLAUDE

**Follow these steps in order to regenerate the complete analysis:**

---

### STEP 1: Fetch Fresh Market Data

**Action:** Run the data fetcher to get current prices, RSI, MACD, and volume data.

```bash
python3 scripts/daily_data_fetcher.py
```

**Verify:**
- ✅ `current_market_data.json` updated with today's timestamp
- ✅ All 14 stocks have current data
- ✅ Prices are from latest market close

**Read the file:**
```bash
# Read current_market_data.json to understand current market state
```

---

### STEP 2: Read Current Portfolio Holdings

**Action:** Load the current portfolio to understand what we own.

```bash
python3 scripts/portfolio_tracker.py show
```

**Read the file:**
```bash
# Read portfolio.json to see:
# - Current holdings (symbol, shares, purchase price)
# - Cash available
# - Current paper gains/losses
# - Transaction history
```

**Key questions to answer:**
- What stocks do we currently hold?
- What was our purchase price for each?
- What are our current paper gains/losses?
- How much cash do we have available?
- What is our current portfolio allocation?

---

### STEP 3: Analyze Each Current Holding

**For EACH stock we currently hold, perform this analysis:**

#### Analysis Framework

1. **Current Technical Status**
   - Current Price vs Purchase Price
   - RSI (oversold <30, neutral 30-70, overbought >70)
   - MACD (bullish/bearish)
   - Volume ratio (institutional activity)
   - Trend (above/below SMAs)

2. **Fundamental Re-evaluation**
   - Has anything changed fundamentally?
   - Earnings growth still strong?
   - Balance sheet still solid?
   - Business model intact?

3. **Money Flow Analysis**
   - Institutional buying or selling?
   - Volume patterns
   - Accumulation vs distribution

4. **Decision Logic**

   **SELL if:**
   - ✅ Stock hit stop loss (price below stop loss level)
   - ✅ RSI > 75 (extreme overbought, take profits)
   - ✅ Fundamental deterioration (earnings miss, debt spike, etc.)
   - ✅ Distribution pattern (institutions selling)
   - ✅ Better opportunities elsewhere (rebalance)

   **HOLD if:**
   - ✅ Stock performing as expected
   - ✅ RSI in healthy range (30-70)
   - ✅ Fundamentals intact
   - ✅ Still within entry/exit strategy
   - ✅ Meeting return expectations

   **BUY MORE (Average Down/Up) if:**
   - ✅ RSI < 30 (oversold, good entry for more)
   - ✅ Price dropped but fundamentals strong (average down)
   - ✅ Increased conviction (new positive catalyst)
   - ✅ Have available cash
   - ✅ Position size still reasonable (<20% of portfolio)

#### Example Analysis Template

**Stock: PENTA.KL**

**Current Status:**
- Purchase: 1,038 shares @ RM 3.85
- Current Price: RM 4.20 (example)
- Paper P/L: +9.09%
- RSI: 45 (neutral)
- MACD: Bullish
- Volume: 0.8x (normal)

**Fundamental Check:**
- ✅ Q4 earnings +28% YoY (accelerating)
- ✅ ROE still 18.2% (excellent)
- ✅ Balance sheet strong
- ✅ New solar contracts announced

**Money Flow:**
- Institutional buying: Moderate
- Volume pattern: Accumulation

**Decision: HOLD**
- ✅ Meeting expectations (+9% vs 25-30% target)
- ✅ Fundamentals intact
- ✅ RSI healthy
- ✅ Still early in 12-month thesis
- Target: RM 5.00 (+30%)

**Action:** Continue holding, monitor for RM 5.00 exit

---

**Repeat this analysis for ALL current holdings:**
- PENTA.KL
- GASMSIA.KL
- PBBANK.KL
- PGAS.KL (if bought)
- MAYBANK.KL (if bought)
- CIMB.KL (if bought)
- INARI.KL (if bought)

---

### STEP 4: Analyze Non-Held Stocks for New Opportunities

**For stocks we DON'T currently hold, evaluate if we should BUY:**

#### Stocks to Evaluate

**Technology:**
- UNISEM.KL
- GREATEC.KL
- (Others if not held)

**Finance:**
- HLBANK.KL
- MAXIS.KL
- (Others if not held)

**Utilities:**
- TENAGA.KL
- YTLPOWR.KL
- VSOLAR.KL
- (Others if not held)

#### Analysis Framework for New Buys

1. **Current Technical Status**
   - RSI (look for <35 oversold or 40-60 healthy)
   - MACD (prefer bullish)
   - Volume (high volume = institutional interest)
   - Trend (prefer price above 200 SMA)

2. **Fundamental Score**
   - Must be >= 7.5/10
   - Strong ROE (>12%)
   - Solid balance sheet
   - Growth trajectory

3. **Money Flow**
   - Institutional accumulation?
   - Volume spikes on up days?

4. **Comparative Analysis**
   - Better than current holdings?
   - Better risk/reward?
   - Diversification benefit?

5. **Decision Logic**

   **BUY if:**
   - ✅ Composite score >= 7.5
   - ✅ RSI in buyable zone (<40 or 40-60)
   - ✅ Fundamentals strong
   - ✅ Institutional accumulation
   - ✅ Have available cash
   - ✅ Diversification benefit
   - ✅ Better opportunity than rebalancing existing

   **WAIT/SKIP if:**
   - ❌ RSI > 70 (overbought)
   - ❌ Fundamentals weak (<7.5 score)
   - ❌ Distribution pattern
   - ❌ Insufficient cash
   - ❌ Current holdings better

---

### STEP 5: Portfolio Rebalancing Analysis

**Review overall portfolio allocation:**

1. **Current Allocation Check**
   - Finance sector: Should be ~40%
   - Utilities sector: Should be ~16%
   - Technology sector: Should be ~14%
   - Cash reserve: Should be ~20-25%

2. **Rebalancing Decisions**

   **SELL from over-allocated sector if:**
   - Sector > target by >10%
   - Individual stock > 15% of portfolio
   - Better opportunities elsewhere

   **BUY in under-allocated sector if:**
   - Sector < target by >10%
   - Good opportunities available
   - Have available cash

3. **Risk Management**
   - No single stock > 20% of portfolio
   - Maintain cash buffer
   - Stop losses respected

---

### STEP 6: Generate Updated Recommendations

**Create a new decision report:**

#### Format: `decisions/YYYY-MM-DD_portfolio_decisions.md`

**Include:**

1. **Executive Summary**
   - Current portfolio value
   - Total paper P/L
   - Number of holdings
   - Cash available
   - Overall assessment

2. **SELL Decisions** (if any)
   ```markdown
   ## 📉 SELL DECISIONS

   ### SYMBOL.KL
   - **Shares:** X
   - **Purchase Price:** RM X.XX
   - **Current Price:** RM X.XX
   - **P/L:** +X.X% (RM +XXX)
   - **Reason:** [Stop loss hit / Extreme overbought / Better opportunities]
   - **Action:** SELL all/partial shares
   - **Expected Proceeds:** RM X,XXX
   ```

3. **HOLD Decisions**
   ```markdown
   ## ✅ HOLD DECISIONS

   ### SYMBOL.KL
   - **Shares:** X
   - **Paper P/L:** +X.X%
   - **Status:** [On track / Ahead / Behind expectations]
   - **Target:** RM X.XX (XX% upside remaining)
   - **Action:** Continue holding
   - **Monitor:** [Stop loss / Target price / Catalyst]
   ```

4. **BUY MORE Decisions** (averaging)
   ```markdown
   ## 📈 BUY MORE (Current Holdings)

   ### SYMBOL.KL
   - **Current Holding:** X shares @ RM X.XX
   - **Current Price:** RM X.XX (X% from purchase)
   - **Reason:** [Oversold / Increased conviction / Average down]
   - **Suggested Buy:** X shares @ RM X.XX = RM X,XXX
   - **New Average Cost:** RM X.XX
   - **Updated Allocation:** X% of portfolio
   ```

5. **NEW BUY Decisions**
   ```markdown
   ## 🆕 NEW BUY OPPORTUNITIES

   ### SYMBOL.KL
   - **Company:** Company Name
   - **Sector:** Technology/Finance/Utilities
   - **Current Price:** RM X.XX
   - **RSI:** XX (oversold/neutral)
   - **Composite Score:** X.X/10
   - **Reason:** [Why now is a good entry]
   - **Expected Return:** XX-XX%
   - **Suggested Allocation:** RM X,XXX (X shares)
   - **Stop Loss:** RM X.XX
   - **Target:** RM X.XX
   ```

6. **Cash Management**
   ```markdown
   ## 💰 CASH MANAGEMENT

   - **Current Cash:** RM XX,XXX
   - **After Sells:** RM XX,XXX
   - **After Buys:** RM XX,XXX
   - **Final Cash Reserve:** RM XX,XXX (XX%)
   ```

7. **Action Plan**
   ```markdown
   ## 📋 EXECUTION PLAN

   **Immediate Actions (Today):**
   1. SELL SYMBOL @ RM X.XX (XXX shares)
   2. BUY SYMBOL @ RM X.XX (XXX shares)
   3. BUY MORE SYMBOL @ RM X.XX (XXX shares)

   **Monitor Closely:**
   - SYMBOL: Approaching stop loss RM X.XX
   - SYMBOL: Approaching target RM X.XX
   - SYMBOL: Wait for RSI < 65 to enter

   **Next Review:** [Daily/Weekly/As needed]
   ```

---

### STEP 7: Execute Decisions (Optional - User Approval)

**Generate execution commands:**

```bash
# SELL orders
python3 scripts/portfolio_tracker.py sell --symbol SYMBOL.KL --shares XXX --price X.XX

# BUY MORE orders (averaging)
python3 scripts/portfolio_tracker.py buy --symbol SYMBOL.KL --shares XXX --price X.XX

# NEW BUY orders
python3 scripts/portfolio_tracker.py buy --symbol SYMBOL.KL --shares XXX --price X.XX

# Mark performance after execution
python3 scripts/portfolio_tracker.py mark --prices-file current_market_data.json
```

**Note:** Present these commands to the user for approval before executing!

---

### STEP 8: Update Dashboard

**Update website with new data:**

1. **Copy updated files:**
```bash
cp current_market_data.json website/data/
cp portfolio.json website/data/
cp decisions/YYYY-MM-DD_portfolio_decisions.md website/data/latest_decisions.md
```

2. **Add to dashboard:**
   - Latest decisions summary card
   - Buy/Sell/Hold count
   - Performance vs last regeneration
   - Action items pending

---

## 📊 DECISION CRITERIA REFERENCE

### When to SELL

| Condition | Action |
|-----------|--------|
| Price < Stop Loss | SELL IMMEDIATELY |
| RSI > 75 | SELL (take profits) |
| Paper gain > 30% | Consider SELL 50% |
| Fundamental deterioration | SELL |
| Distribution pattern | SELL |

### When to HOLD

| Condition | Action |
|-----------|--------|
| RSI 30-70 | HOLD |
| On track to target | HOLD |
| Fundamentals intact | HOLD |
| Within 12-month thesis | HOLD |

### When to BUY MORE

| Condition | Action |
|-----------|--------|
| RSI < 30 + Strong fundamentals | BUY MORE |
| Price -15% from purchase + Thesis intact | BUY MORE (average down) |
| New positive catalyst | BUY MORE |
| Position < 15% of portfolio | BUY MORE (room to add) |

### When to BUY NEW

| Condition | Action |
|-----------|--------|
| Score >= 7.5 + RSI < 40 | BUY |
| Institutional accumulation + Good fundamentals | BUY |
| Better risk/reward than holdings | REBALANCE & BUY |
| Diversification benefit | BUY |

---

## 🎯 SUCCESS METRICS

After regeneration, track:

✅ **Decision Quality**
- % of holdings that met/exceeded expectations
- Accuracy of buy/sell decisions (review 1 month later)
- Portfolio return vs KLSE index

✅ **Portfolio Health**
- Diversification (no stock > 20%)
- Sector allocation (within targets)
- Cash reserve (20-25%)
- Win rate (% stocks in profit)

✅ **Risk Management**
- All stop losses respected
- No impulsive decisions
- Data-driven rationale for all decisions

---

## 🔄 REGENERATION FREQUENCY

**Daily:** If actively trading or volatile market
**Weekly:** For standard portfolio management (RECOMMENDED)
**Monthly:** For long-term holding strategy

---

## 📝 OUTPUT FILES

After each regeneration, create:

1. **`decisions/YYYY-MM-DD_portfolio_decisions.md`** - Main decision report
2. **`decisions/YYYY-MM-DD_execution_commands.sh`** - CLI commands to execute
3. **`analysis/YYYY-MM-DD/updated_analysis.json`** - Updated stock scores
4. **Updated `portfolio.json`** - If decisions executed

---

## 🚀 QUICK REGENERATION COMMAND

**User runs:**
```bash
# User command (for future automation)
python3 scripts/regenerate_analysis.py --execute-decisions
```

**Or manually trigger by:**
```
User: "Regenerate the analysis and make buy/sell decisions"
Claude: [Follows this prompt file step-by-step]
```

---

## ⚠️ IMPORTANT REMINDERS

1. **Always fetch fresh data first** - Don't use stale prices
2. **Read current portfolio** - Know what we own before deciding
3. **Be disciplined** - Follow the decision criteria, not emotions
4. **Respect stop losses** - Sell immediately if triggered
5. **Maintain cash buffer** - Never go 100% invested
6. **Document rationale** - Explain WHY for each decision
7. **User approval** - Present decisions for approval before executing

---

## 🎉 COMPLETION CHECKLIST

After completing regeneration:

- [ ] Fresh market data fetched
- [ ] All 14 stocks analyzed
- [ ] Current holdings reviewed
- [ ] HOLD/SELL/BUY decisions made
- [ ] New opportunities identified
- [ ] Decision report generated
- [ ] Execution commands prepared
- [ ] Dashboard updated
- [ ] User notified of recommendations

---

**Generated:** Milestone 5 - Auto-Regeneration System
**Purpose:** Keep analysis fresh and optimize portfolio performance
**Usage:** Run weekly or when market conditions change significantly

**LET'S OPTIMIZE THE PORTFOLIO!** 🔄📈💰
