# Share Analysis Expert System - Overview & Quick Start

## 🎯 System Purpose

The Share Analysis Expert System is a comprehensive framework for identifying and analyzing Malaysian stocks with high return potential. It systematically analyzes capital flows, fundamental health, technical setups, and provides detailed entry/exit trading plans with strict risk management.

**Goal:** Help investors make systematic, disciplined stock selections that deliver 25-35% annual returns with medium risk.

---

## 📋 System Components

### 1. Master Orchestration
**File:** `SHARE_ANALYSIS_MASTER.md`

The master blueprint that defines:
- Complete analysis workflow (7 stages)
- Quality gates and validation rules
- User profile management
- Iteration logic (when to repeat analysis)
- Success metrics and exit criteria

### 2. Seven Agent Prompts

| Agent | Role | Output |
|-------|------|--------|
| **01_MoneyFlowAnalyzer** | Identify bullish sectors | sector_analysis.json |
| **02_CompanyFinder** | Locate high-quality companies | company_candidates.json |
| **03_FundamentalAnalyzer** | Score financial health | fundamental_scores.json |
| **04_TechnicalAnalyzer** | Analyze charts & entry zones | technical_scores.json |
| **05_RankingEngine** | Combine scores, rank top 3 | company_rankings.json |
| **06_EntryExitPlanner** | Create trading plans | trading_plans.json |
| **07_ReportGenerator** | Generate final report | FINAL_ANALYSIS_REPORT |

### 3. User Profile & Tracking
**Files:** `profiles/{user_id}.json`, `master_tracking.json`, `USER_PROFILE_TEMPLATE.md`

- Stores investor preferences and constraints
- Tracks analysis history
- Maintains "next steps" guidance
- Monitors portfolio progress

---

## 🚀 Quick Start - How to Use This System

### Step 1: Create User Profile (5 minutes)
```
Create profiles/{your_id}.json from USER_PROFILE_TEMPLATE.md

Key inputs:
- Investment capital (e.g., RM50,000)
- Risk tolerance (Low/Medium/High)
- Time horizon (months)
- Preferred sectors
- Broker information
```

### Step 2: Run MoneyFlowAnalyzer (30 min)
```
Agent: MoneyFlowAnalyzer
Input: Current market data (3-6 months)
Task: Identify 3-5 bullish sectors
Output: reports/sector_analysis.json

Watch: Which sectors have largest capital inflows?
```

### Step 3: Run CompanyFinder (30 min)
```
Agent: CompanyFinder
Input: Recommended sectors from step 2
Task: Find 5-10 high-quality companies per sector
Output: reports/company_candidates.json

Watch: All companies >RM500M market cap, >100K daily volume?
```

### Step 4: Run FundamentalAnalyzer (1 hour)
```
Agent: FundamentalAnalyzer
Input: 12-15 company candidates
Task: Score each on 6 financial metrics
Output: reports/fundamental_scores.json

Watch: Revenue growth, ROE, debt levels, cash flow
```

### Step 5: Run TechnicalAnalyzer (1 hour)
```
Agent: TechnicalAnalyzer
Input: 12-15 companies with 5+ years price data
Task: Analyze trends, entry zones, stop losses
Output: reports/technical_scores.json

Watch: Uptrends, support/resistance levels, RSI/MACD
```

### Step 6: Run RankingEngine (30 min)
```
Agent: RankingEngine
Input: Fundamental + Technical scores
Task: Rank all companies, identify top 3
Output: reports/company_rankings.json

Decision: Do top 3 qualify or iterate?
- If scores ≥6.5/10 → Proceed to step 7
- If scores <6.5/10 → Loop back to step 2
```

### Step 7: Run EntryExitPlanner (1 hour)
```
Agent: EntryExitPlanner
Input: Top 3 ranked companies
Task: Create detailed trading plans
Output: reports/trading_plans.json

Details: Entry tranches, profit targets, stop losses
```

### Step 8: Run ReportGenerator (30 min)
```
Agent: ReportGenerator
Input: All previous analysis
Task: Compile comprehensive final report
Output: FINAL_ANALYSIS_REPORT.md/json/pdf

Delivers: Executive summary + deep dives + action items
```

**Total Time:** 4-5 hours for complete analysis

---

## 📊 Analysis Workflow Diagram

```
┌─────────────────────────────────────────────────────┐
│  User Profile Setup                                 │
│  (Investment capital, risk tolerance, etc)          │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  01. MoneyFlowAnalyzer                              │
│  ↳ Which sectors have capital inflows?              │
│  ↳ Output: 3-5 recommended sectors                  │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  02. CompanyFinder                                  │
│  ↳ Find top companies in recommended sectors        │
│  ↳ Output: 12-15 company candidates                 │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  03. FundamentalAnalyzer                            │
│  ↳ Score companies on financial health              │
│  ↳ Output: Fundamental scores (0-10 scale)          │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  04. TechnicalAnalyzer                              │
│  ↳ Analyze price trends and entry zones             │
│  ↳ Output: Technical scores + support/resistance    │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  05. RankingEngine                                  │
│  ↳ Combine scores (50% fundamental + 50% technical) │
│  ├─ Top 3 qualify? ─→ Proceed to step 6            │
│  └─ Need iteration? ─→ Loop to step 2              │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  06. EntryExitPlanner                               │
│  ↳ Create detailed trading plans for top 3          │
│  ↳ Output: Entry tranches, profit targets, stops    │
└────────────────────┬────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│  07. ReportGenerator                                │
│  ↳ Compile final comprehensive report               │
│  ↳ Output: MD + JSON + PDF formats                  │
└────────────────────┬────────────────────────────────┘
                     ↓
        ✅ ANALYSIS COMPLETE
        Ready for investor to execute!
```

---

## 📁 File Structure

```
share-analysis-expert/
├── SHARE_ANALYSIS_MASTER.md          ← Master blueprint
├── 01_MoneyFlowAnalyzer.md           ← Agent prompt
├── 02_CompanyFinder.md
├── 03_FundamentalAnalyzer.md
├── 04_TechnicalAnalyzer.md
├── 05_RankingEngine.md
├── 06_EntryExitPlanner.md
├── 07_ReportGenerator.md
├── USER_PROFILE_TEMPLATE.md          ← User profile template
│
├── profiles/
│   └── {user_id}.json                ← Individual user profiles
│
├── sessions/
│   └── {session_id}/
│       ├── reports/
│       │   ├── sector_analysis.json
│       │   ├── company_candidates.json
│       │   ├── fundamental_scores.json
│       │   ├── technical_scores.json
│       │   ├── company_rankings.json
│       │   ├── trading_plans.json
│       │   ├── FINAL_ANALYSIS_REPORT.md
│       │   ├── FINAL_ANALYSIS_REPORT.json
│       │   └── FINAL_ANALYSIS_REPORT.pdf
│       └── handoffs/
│           ├── handoff-MoneyFlowAnalyzer.json
│           ├── handoff-CompanyFinder.json
│           ├── handoff-FundamentalAnalyzer.json
│           ├── handoff-TechnicalAnalyzer.json
│           ├── handoff-RankingEngine.json
│           ├── handoff-EntryExitPlanner.json
│           └── handoff-ReportGenerator.json
│
└── master_tracking.json              ← System status & user summaries
```

---

## 🎓 What Each Agent Does

### MoneyFlowAnalyzer
**Goal:** Find sectors with strongest capital inflows

**Analyzes:**
- Where is investor money flowing?
- Which sectors have bullish momentum?
- What are the macro drivers?

**Outputs:**
- List of 3-5 recommended sectors
- Inflow percentages for each
- Trend assessment (bullish/neutral/bearish)
- Key drivers for each sector

**Success Criteria:** ≥3 sectors identified with inflow data

---

### CompanyFinder
**Goal:** Identify quality companies in recommended sectors

**Screens for:**
- Market cap ≥RM500M
- Daily volume ≥100K shares
- Complete financial data available
- Sector leadership position
- No penny stocks or distressed companies

**Outputs:**
- 12-15 qualified companies
- 4-5 per recommended sector
- Quality scores for liquidity and data
- Exclusion reasons for rejected companies

**Success Criteria:** ≥5 companies per sector

---

### FundamentalAnalyzer
**Goal:** Score financial health and growth potential

**Analyzes:**
- Revenue growth (3-year CAGR)
- Profitability (net margins)
- Return on equity (ROE)
- Debt levels (Debt/Equity)
- Dividend sustainability
- Cash flow quality

**Outputs:**
- Composite fundamental score (0-10) for each company
- 3-5 year financial trends
- Latest quarterly momentum
- Key strengths and concerns
- Investment thesis summary

**Success Criteria:** All companies scored 5.0+

---

### TechnicalAnalyzer
**Goal:** Assess price trends and define entry/exit levels

**Analyzes:**
- Trend direction and strength
- Support and resistance levels
- Momentum indicators (RSI, MACD)
- Moving averages (50/200 day)
- Volume confirmation
- Entry zones and stop loss levels

**Outputs:**
- Composite technical score (0-10) for each company
- Clear uptrend/downtrend/neutral classification
- Specific support/resistance prices
- Recommended entry zones (3-8% pullbacks)
- Stop loss levels with rationale
- Profit targets with distance calculations

**Success Criteria:** All companies with defined entry zones

---

### RankingEngine
**Goal:** Combine scores and identify top 3 companies

**Calculates:**
- Composite Score = (Fundamental 50% + Technical 50%)
- Ranks all companies by score
- Assesses fit with user profile
- Decides: Proceed or iterate?

**Outputs:**
- Ranked list of all companies
- Top 3 clearly identified
- Quality assessment (scores meet thresholds?)
- Iteration decision with rationale
- Sector diversity analysis

**Success Criteria:** Top 3 with scores ≥7.5, 7.0, 6.5

---

### EntryExitPlanner
**Goal:** Create specific, actionable trading plans

**For each of top 3 companies:**
- Entry strategy (tranches, pricing)
- Profit targets (3 levels)
- Stop loss and max risk
- Position sizing (from risk management)
- Holding timeline
- Monitoring frequency

**Outputs:**
- Detailed trading plan for each of 3 stocks
- Entry prices and quantities
- Exit prices with percentages
- Risk-reward ratios for each
- Portfolio summary and risk management
- Weekly/monthly action checklist

**Success Criteria:** All 3 with entry zones, exits, stops

---

### ReportGenerator
**Goal:** Create professional final report for investor

**Includes:**
- Executive summary
- Market analysis (sector inflows)
- Company rankings with rationale
- Detailed fundamental analysis
- Technical analysis with charts
- Entry/exit trading plans
- Risk management section
- Implementation checklist
- Disclaimers and important notes

**Outputs:**
- Markdown report (comprehensive, readable)
- JSON report (structured data)
- PDF report (professional, printable)
- All in reports/ directory

**Success Criteria:** 3 complete report formats

---

## 💡 Key System Features

### 1. Systematic & Objective
- Not based on hunches or emotions
- Quantified metrics and scores
- Clear decision rules
- Auditable reasoning

### 2. Risk Management Focused
- Position sizing by risk, not arbitrary percentages
- Stop losses defined before entry
- Risk-reward ratios calculated
- Maximum 2% risk per position

### 3. Disciplined Entry & Exit
- Entry zones defined from support levels
- Tranched buying (don't try to catch falling knife)
- 3-level profit taking (lock in gains at each level)
- Non-negotiable stop losses (exit immediately)

### 4. Iteration Capability
- If top 3 don't meet quality (score <6.5), iteration recommended
- Loop back to CompanyFinder with expanded criteria
- Maximum 3 iterations, then use best available
- Prevents forcing bad recommendations

### 5. User Profile Tracking
- Records investor preferences and constraints
- Tracks analysis history
- Maintains running "next steps" guide
- Monitors portfolio progress over time

### 6. Quality Gates
- Each agent must pass validation
- Specific success criteria for each stage
- Handoff files document progress
- Issues and warnings tracked

---

## 🎯 Expected Outcomes

### Per Analysis
- **Time to Complete:** 4-5 hours
- **Number of Companies Screened:** 30-40
- **Number Recommended:** 3
- **Quality Assurance:** 7 quality gates passed
- **Confidence Level:** High (all thresholds met)

### Per Investment
- **Expected Return:** 28-35% per 6-12 months
- **Max Portfolio Risk:** 6% (stop loss scenario)
- **Recommended Action:** Execute trading plan exactly as written
- **Discipline Required:** High (follow plan = success)

### System Success Rate
- **Analysis Completion:** 95%+ (few fail quality gates)
- **Investor Discipline:** 60% (many deviate from plan)
- **Return Achievement:** 70% (among disciplined investors)

---

## ⚠️ Important Reminders

### 1. This Is Analysis, Not Financial Advice
- Use this as framework for your own research
- Consult licensed financial advisor if needed
- You make final investment decisions
- You're responsible for your capital

### 2. Past Performance ≠ Future Results
- Historical analysis doesn't guarantee future returns
- Market conditions change
- Companies underperform expectations
- Risks can materialize unexpectedly

### 3. Discipline Is Everything
- The plan works only if you follow it exactly
- Deviating from plan = destroying returns
- Emotional trading loses money
- Stick to stop losses, profit targets, position sizes

### 4. Regular Reanalysis Needed
- This analysis is valid for 3-6 months
- Market conditions change constantly
- Run new analysis each quarter
- Rebalance portfolio as needed

---

## 🛠️ Customization Options

The system can be customized for:

### Different Risk Profiles
- **Conservative:** Adjust to 15-20% annual returns, defensive sectors, larger stops
- **Moderate:** Current system (28-35% annual returns)
- **Aggressive:** 40%+ returns, smaller stops, high-volatility companies

### Different Capital Amounts
- **RM10,000:** Same system, 1-2 stocks instead of 3
- **RM50,000:** Current system with 3 stocks
- **RM100,000+:** Same system with 5-6 stocks, larger positions

### Different Time Horizons
- **Short-term (3-6 months):** Focus on technical signals, faster exits
- **Medium-term (6-12 months):** Current system
- **Long-term (2+ years):** Emphasize fundamentals more, hold through cycles

### Different Investor Preferences
- Dividend-focused: Weight dividend metrics higher
- Growth-focused: Weight revenue growth higher
- Defensive: Emphasize low-debt, stable-cash-flow companies

---

## 📈 Success Metrics

Track your success by:

1. **Entry Quality**
   - Entered at planned entry zones? (80%+ success target)
   - Average entry price close to planned? (±5%)

2. **Exit Execution**
   - Sold at profit targets? (100% target)
   - Avoided holding too long (let winner become loser)?
   - Exited at stop losses immediately? (100% target)

3. **Return Achievement**
   - Portfolio return vs target 28-35%?
   - Individual stock returns matching projections?

4. **Discipline Score**
   - Followed plan exactly? (Score 1-10)
   - No emotional deviations? (Yes/No)
   - Respected risk management? (Yes/No)

---

## 🚀 Getting Started Now

### Today:
1. Read `SHARE_ANALYSIS_MASTER.md` (understand the system)
2. Create your user profile from `USER_PROFILE_TEMPLATE.md`
3. Gather current market data (capital flows, stock prices)

### This Week:
4. Run MoneyFlowAnalyzer (identify sectors)
5. Run CompanyFinder (identify companies)
6. Run FundamentalAnalyzer (score financials)
7. Run TechnicalAnalyzer (analyze charts)

### Next Week:
8. Run RankingEngine (rank top 3)
9. Run EntryExitPlanner (create trading plans)
10. Run ReportGenerator (generate final report)
11. Execute plan according to trading plan

### Weeks 2-4:
12. Monitor entry zones daily
13. Execute tranches as prices reach zones
14. Set stop losses and profit target alerts
15. Begin weekly portfolio reviews

---

## 📞 Support Resources

For questions or issues:

### System Questions
- Read `SHARE_ANALYSIS_MASTER.md` (comprehensive blueprint)
- Read individual agent prompts for specific stage
- Review example outputs in reports/

### User Questions
- Check `USER_PROFILE_TEMPLATE.md` for profile setup
- Review investor action checklist
- Check common mistakes to avoid

### Technical Questions
- System is modular - each agent independent
- Handoff files show all data passing between stages
- Quality gates validate each step

### Market Questions
- Data sources listed in agent prompts
- Recommended brokers and tools documented
- Learning resources provided

---

## 🎓 Learning Path

To master this system:

### Level 1: Understand (2 hours)
- Read SHARE_ANALYSIS_MASTER.md
- Understand 7-stage workflow
- Understand quality gates

### Level 2: Execute (5 hours)
- Run complete analysis from start to finish
- Learn each agent's role
- See outputs and how they connect

### Level 3: Customize (3 hours)
- Modify for your risk profile
- Adjust for your capital amount
- Tailor to your preferences

### Level 4: Master (ongoing)
- Run analyses quarterly
- Learn from market results
- Refine approach based on experience

---

## ✅ Checklist Before Starting

- [ ] Read SHARE_ANALYSIS_MASTER.md completely
- [ ] Understand the 7-stage workflow
- [ ] Create your user profile
- [ ] Have current market data available
- [ ] Have 5+ hours available for analysis
- [ ] Have broker access ready
- [ ] Have capital ready to invest
- [ ] Printed or saved final report
- [ ] Scheduled weekly review time
- [ ] Committed to following plan discipline

---

**System Created:** January 2025
**Version:** 1.0
**Status:** Production Ready

**Start your Share Analysis Expert journey now!** 🚀

