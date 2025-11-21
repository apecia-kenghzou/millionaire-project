# Share Analysis Expert System - Master Orchestration

## Project Goal
Develop an intelligent share analysis system to help Malaysian investors identify the best shares with high return potential through systematic analysis and risk management.

---

## Quick Reference

| Component | Location |
|-----------|----------|
| Agent Prompts | `@agents/*.md` |
| Master Instruction | This file (SHARE_ANALYSIS_MASTER.md) |
| User Profile Data | `profiles/{user_id}.json` |
| Session Handoffs | `sessions/{session_id}/handoff-{AgentName}.json` |
| Analysis Reports | `sessions/{session_id}/reports/` |

---

## Functional Requirements

### Core Analysis Pipeline
The system performs a structured, iterative analysis to identify and recommend Malaysian shares:

1. **Money Flow Analysis** - Identify which market sectors are attracting capital
2. **Sector Company Identification** - Find top companies in high-inflow sectors
3. **Fundamental Analysis** - Analyze quarterly and annual financial reports
4. **Technical Analysis** - Perform price action and chart pattern analysis
5. **Ranking & Iteration** - Repeat steps 2-4 until top 3 companies identified
6. **Entry/Exit Planning** - Create detailed trading plans with risk management

### User Management
- Create and maintain investor profiles
- Track risk tolerance, investment capital, and time horizon
- Monitor analysis history and recommendations
- Provide ongoing guidance and next steps

### Analysis Outputs
- Sector momentum analysis with inflow percentages
- Company fundamentals scorecard
- Technical analysis with key levels
- Top 3 recommended companies with detailed rationale
- Entry price, exit targets, and stop-loss levels
- Risk-adjusted portfolio allocation

---

## Technical Stack

### Backend Architecture
- **Runtime:** Node.js 18+
- **Framework:** Express 4.18+
- **Data Layer:** MongoDB (company data, reports) or JSON (for MVP)
- **Analysis Libraries:**
  - `ta-lib` or `tulind` - Technical analysis indicators
  - `csv-parse` - Financial report parsing
  - `axios` - Web scraping Malaysian exchange data
  - `dotenv` - Configuration management

### Data Sources
- Bursa Malaysia API / Web scraping
- Company quarterly and annual reports (PDF parsing)
- Price and volume data (OHLC)
- Market sentiment and money flow indicators
- Analyst reports and earnings calendars

### Testing & Validation
- **Framework:** Jest / Vitest
- **Coverage:** 90%+ required
- **Integration Tests:** End-to-end analysis pipeline
- **Data Validation:** Financial data integrity checks

### Documentation
- **Format:** Markdown
- **API Spec:** OpenAPI 3.0.3
- **Analysis Reports:** PDF/JSON exports

---

## Analysis Workflow Architecture

### Orchestration Pattern: Iterative Ranking Pipeline with Quality Gates

**Mode:** Iterative Refinement with Score-Based Ranking
**Max Pipeline Iterations:** 3 (full loops until top 3 found)
**Per-Agent Max Retries:** 3

```
┌──────────────────────────────────────────────────────────┐
│  [User Profile Setup] (collect investment criteria)      │
└────────────────────┬─────────────────────────────────────┘
                     ↓
      ┌─────────────────────────────────┐
      │  Iteration Counter = 0          │
      │  Ranked Companies Count = 0     │
      └─────────────┬───────────────────┘
                    ↓
    ┌────────────────────────────────────────────┐
    │  [MoneyFlowAnalyzer] - Sector Analysis    │
    │  Identify high-inflow market sectors       │
    └────────────┬───────────────────────────────┘
                 ↓
      Quality Gate 1: Are sectors identified?
            ├─ NO → Retry (max 3x) / Human input
            └─ YES ↓
    ┌────────────────────────────────────────────┐
    │  [CompanyFinder] - Top Company Screening   │
    │  Find 5-10 companies per identified sector │
    └────────────┬───────────────────────────────┘
                 ↓
      Quality Gate 2: Companies found ≥5?
            ├─ NO → Retry / Expand search
            └─ YES ↓
    ┌────────────────────────────────────────────┐
    │  [FundamentalAnalyzer] - Financial Analysis│
    │  Score: Revenue growth, Profitability,     │
    │         ROE, Debt ratio, Dividend yield    │
    └────────────┬───────────────────────────────┘
                 ↓
      Quality Gate 3: Scores calculated?
            ├─ NO → Retry
            └─ YES ↓
    ┌────────────────────────────────────────────┐
    │  [TechnicalAnalyzer] - Chart Analysis      │
    │  Score: Trend, Support/Resistance,         │
    │         RSI, MACD, Moving averages         │
    └────────────┬───────────────────────────────┘
                 ↓
      Quality Gate 4: Technical scores done?
            ├─ NO → Retry
            └─ YES ↓
    ┌────────────────────────────────────────────┐
    │  [RankingEngine] - Combined Scoring        │
    │  Merge fundamental + technical scores      │
    │  Rank companies by composite score         │
    └────────────┬───────────────────────────────┘
                 ↓
      Quality Gate 5: Top companies ranked?
            ├─ YES - Check count:
            │  ├─ Count ≥ 3 → Go to EntryExitPlanner
            │  └─ Count < 3 → Iteration++
            │                 Loop back to CompanyFinder
            │                 (iteration < 3)
            └─ NO → Retry RankingEngine
    
    ┌────────────────────────────────────────────┐
    │  [EntryExitPlanner] - Trading Strategy     │
    │  Calculate: Entry prices, exit targets,    │
    │  stop-loss, position sizing (risk-adjusted)│
    └────────────┬───────────────────────────────┘
                 ↓
      Quality Gate 6: Plans generated?
            ├─ NO → Retry
            └─ YES ↓
    ┌────────────────────────────────────────────┐
    │  [ReportGenerator] - Final Report          │
    │  Create PDF/JSON report with all findings  │
    └────────────┬───────────────────────────────┘
                 ↓
         ┌──────────────────────┐
         │  [COMPLETE]          │
         │  Report Ready        │
         └──────────────────────┘
```

### Iteration Logic

#### Global Iteration Counter
- Tracks full analysis loops
- Increments when CompanyFinder is re-run (need more companies)
- **Max:** 3 full iterations
- **On Exceed:** Use best available companies or escalate

#### Per-Agent Retry Counter
- Tracks retries of single agent without looping
- Resets when moving to next agent
- **Max:** 3 retries per agent

#### Early Termination Condition
- If ≥3 qualified companies ranked → Proceed to EntryExitPlanner
- No need to wait for iterations if quality threshold met

---

## Agent Orchestration Flow

### Stage 1: User Profile Initialization
**Agent:** ProfileManager

**Inputs from User:**
- Name and investment experience level
- Risk tolerance (Low/Medium/High)
- Investment capital amount (RM)
- Investment time horizon (months/years)
- Preferred sectors (optional)
- Exclusion criteria (if any)

**Outputs:**
- `profiles/{user_id}.json` - User profile document
- Initial preferences stored
- `handoff-ProfileManager.json`

**Success Criteria:**
- [ ] All required fields captured
- [ ] Risk profile clearly defined
- [ ] Capital and timeframe confirmed
- [ ] Profile saved successfully

---

### Stage 2: Money Flow Analysis
**Agent:** MoneyFlowAnalyzer
**Prompt File:** `@agents/01_MoneyFlowAnalyzer.md`

**Inputs:**
- `profiles/{user_id}.json`
- Bursa Malaysia market data (last 3-6 months)
- Sector performance metrics
- Foreign and local fund inflows by sector

**Outputs:**
- `reports/sector_analysis.json`
  ```json
  {
    "sectors": [
      {
        "name": "Technology",
        "inflow_strength": 8.5,
        "trend": "bullish",
        "momentum": "increasing",
        "inflow_percentage": 22.5,
        "rationale": "AI boom, semiconductor demand...",
        "top_companies_count": 0
      }
    ],
    "recommended_sectors": ["Technology", "Finance"],
    "excluded_sectors": ["Energy"],
    "analysis_date": "2025-01-15"
  }
  ```
- `handoff-MoneyFlowAnalyzer.json`

**Success Criteria:**
- [ ] 3-5 sectors identified with inflow analysis
- [ ] Inflow percentages and trends calculated
- [ ] Clear rationale for sector selection
- [ ] Data sources documented
- [ ] Date and timeframe specified

**Validation Command:**
```bash
cat reports/sector_analysis.json | jq '.recommended_sectors | length'
# Should return ≥3
```

---

### Stage 3: Company Finding
**Agent:** CompanyFinder
**Prompt File:** `@agents/02_CompanyFinder.md`

**Inputs:**
- `reports/sector_analysis.json` (recommended sectors)
- `profiles/{user_id}.json` (user preferences)
- Bursa Malaysia company listings
- Market cap and liquidity filters

**Outputs:**
- `reports/company_candidates.json`
  ```json
  {
    "candidates": [
      {
        "symbol": "TECH.KL",
        "name": "Tech Company Ltd",
        "sector": "Technology",
        "market_cap_rm": 5000000000,
        "average_volume": 2500000,
        "pe_ratio": 18.5,
        "selection_reason": "Top market cap, strong volume...",
        "data_quality_score": 9.2
      }
    ],
    "total_candidates": 12,
    "sectors_covered": ["Technology", "Finance"],
    "analysis_date": "2025-01-15"
  }
  ```
- `handoff-CompanyFinder.json`

**Success Criteria:**
- [ ] ≥5 companies per sector identified
- [ ] Each has market cap >RM500M
- [ ] Average daily volume >100K shares
- [ ] Complete pricing and fundamentals data available
- [ ] Data freshness: within 1 week

**Validation Command:**
```bash
cat reports/company_candidates.json | jq '.candidates | length'
# Should return ≥5
```

---

### Stage 4: Fundamental Analysis
**Agent:** FundamentalAnalyzer
**Prompt File:** `@agents/03_FundamentalAnalyzer.md`

**Inputs:**
- `reports/company_candidates.json` (companies to analyze)
- Financial reports (quarterly and annual)
- Balance sheets, income statements, cash flow
- Historical financial data (3-5 years)

**Outputs:**
- `reports/fundamental_scores.json`
  ```json
  {
    "analysis": [
      {
        "symbol": "TECH.KL",
        "company_name": "Tech Company Ltd",
        "scores": {
          "revenue_growth_3yr": 8.2,
          "profitability": 8.5,
          "roe": 7.8,
          "debt_health": 9.1,
          "dividend_yield": 6.5,
          "cash_flow": 8.3
        },
        "composite_fundamental_score": 8.3,
        "key_strengths": ["Growing revenue", "Strong ROE", "Low debt"],
        "key_concerns": ["Declining margins"],
        "latest_quarterly": {
          "date": "Q4 2024",
          "revenue_yoy_growth": 12.5,
          "net_profit_margin": 8.2,
          "eps": 0.35
        }
      }
    ],
    "analysis_period": "3-5 years historical",
    "analysis_date": "2025-01-15"
  }
  ```
- `handoff-FundamentalAnalyzer.json`

**Success Criteria:**
- [ ] All candidate companies scored
- [ ] Composite scores 0-10 scale
- [ ] Latest 4 quarters analyzed
- [ ] 3-5 year trends calculated
- [ ] Key strengths/concerns identified
- [ ] Data sources (report dates) documented

**Scoring Matrix:**
| Metric | Weight | Scale |
|--------|--------|-------|
| Revenue Growth (3yr CAGR) | 20% | 0-10 |
| Profitability (Net Margin Avg) | 20% | 0-10 |
| Return on Equity (ROE) | 20% | 0-10 |
| Debt Health (Debt/Equity) | 15% | 0-10 |
| Dividend Yield | 10% | 0-10 |
| Cash Flow Quality | 15% | 0-10 |

---

### Stage 5: Technical Analysis
**Agent:** TechnicalAnalyzer
**Prompt File:** `@agents/04_TechnicalAnalyzer.md`

**Inputs:**
- `reports/company_candidates.json` (companies)
- OHLCV data (5 years minimum for each company)
- Key technical indicators (RSI, MACD, Moving Averages)

**Outputs:**
- `reports/technical_scores.json`
  ```json
  {
    "analysis": [
      {
        "symbol": "TECH.KL",
        "current_price": 5.42,
        "analysis_date": "2025-01-15",
        "trend_analysis": {
          "primary_trend": "uptrend",
          "trend_strength": 7.5,
          "support_level": 5.10,
          "resistance_level": 5.80,
          "description": "Price in uptrend with support at 5.10"
        },
        "momentum_indicators": {
          "rsi_14": 62.5,
          "rsi_interpretation": "Strong but not overbought",
          "macd_status": "Bullish crossover",
          "macd_score": 8.2
        },
        "moving_averages": {
          "sma_50": 5.15,
          "sma_200": 4.95,
          "position_vs_ma": "Above both (bullish)",
          "ma_score": 8.0
        },
        "composite_technical_score": 7.9,
        "entry_zone": "4.95-5.15",
        "stop_loss_suggestion": 4.85,
        "target_1": 5.80,
        "target_2": 6.20,
        "chart_pattern": "Higher highs and higher lows",
        "volume_trend": "Increasing on rallies (healthy)"
      }
    ],
    "analysis_date": "2025-01-15"
  }
  ```
- `handoff-TechnicalAnalyzer.json`

**Success Criteria:**
- [ ] All candidates analyzed
- [ ] Composite technical scores 0-10
- [ ] Support/resistance levels identified
- [ ] Trend direction clearly stated
- [ ] Momentum indicators calculated
- [ ] 5+ year data analyzed
- [ ] Entry zones defined
- [ ] Chart patterns described

**Scoring Matrix:**
| Component | Weight | Scale |
|-----------|--------|-------|
| Trend Strength | 35% | 0-10 |
| Momentum (RSI/MACD) | 30% | 0-10 |
| Moving Averages Position | 20% | 0-10 |
| Volume Confirmation | 15% | 0-10 |

---

### Stage 6: Ranking & Iteration
**Agent:** RankingEngine
**Prompt File:** `@agents/05_RankingEngine.md`

**Inputs:**
- `reports/fundamental_scores.json`
- `reports/technical_scores.json`
- `profiles/{user_id}.json` (user risk tolerance)

**Outputs:**
- `reports/company_rankings.json`
  ```json
  {
    "iteration": 1,
    "total_candidates_analyzed": 12,
    "ranked_companies": [
      {
        "rank": 1,
        "symbol": "TECH.KL",
        "company_name": "Tech Company Ltd",
        "fundamental_score": 8.3,
        "technical_score": 7.9,
        "composite_score": 8.1,
        "suitability_for_user": "High (matches medium-risk profile)",
        "rank_reasons": [
          "Highest combined score (8.1/10)",
          "Strong revenue growth with good profitability",
          "Uptrend with confirmed technical support",
          "Adequate liquidity for position sizing"
        ]
      },
      {
        "rank": 2,
        "symbol": "FIN.KL",
        "company_name": "Finance Corp Ltd",
        ...
      },
      {
        "rank": 3,
        "symbol": "IND.KL",
        "company_name": "Industrial Ltd",
        ...
      }
    ],
    "top_3_found": true,
    "analysis_date": "2025-01-15",
    "next_step": "Proceed to EntryExitPlanner"
  }
  ```
- `handoff-RankingEngine.json`

**Success Criteria:**
- [ ] All companies scored and ranked
- [ ] Composite scores = (Fundamental 50% + Technical 50%)
- [ ] Top 3 companies clearly identified
- [ ] Rank rationale documented
- [ ] User risk profile considered
- [ ] Decision on iteration (proceed vs. refine)

**Iteration Decision Logic:**
```
IF (ranked_companies.count ≥ 3) AND 
   (rank_1.score ≥ 7.0) AND
   (rank_3.score ≥ 6.5)
THEN:
  next_step = "Proceed to EntryExitPlanner"
ELSE IF (iteration < 3):
  next_step = "Loop back to CompanyFinder (expand search)"
  iteration++
ELSE:
  next_step = "Use best available candidates"
```

---

### Stage 7: Entry & Exit Planning
**Agent:** EntryExitPlanner
**Prompt File:** `@agents/06_EntryExitPlanner.md`

**Inputs:**
- `reports/company_rankings.json` (top 3 companies)
- `reports/technical_scores.json` (entry zones, support/resistance)
- `profiles/{user_id}.json` (capital, risk tolerance)
- Current market prices

**Outputs:**
- `reports/trading_plans.json`
  ```json
  {
    "plans": [
      {
        "rank": 1,
        "symbol": "TECH.KL",
        "company_name": "Tech Company Ltd",
        "capital_allocation": {
          "user_total_capital_rm": 50000,
          "risk_tolerance": "Medium",
          "allocation_percentage": 40,
          "position_size_rm": 20000
        },
        "entry_plan": {
          "current_price": 5.42,
          "entry_zone": {
            "price_from": 4.95,
            "price_to": 5.15,
            "strategy": "Buy in tranches as price moves into zone"
          },
          "buy_tranche_1": {
            "price": 5.15,
            "quantity": 1800,
            "amount": 9270,
            "percentage": 50
          },
          "buy_tranche_2": {
            "price": 5.05,
            "quantity": 1900,
            "amount": 9595,
            "percentage": 50
          },
          "avg_entry_price": 5.10,
          "total_shares": 3700,
          "total_investment": 18865
        },
        "exit_plan": {
          "target_1": {
            "price": 5.80,
            "shares_to_sell": 1200,
            "amount": 6960,
            "percentage": 32,
            "rationale": "First profit target, lock in gains"
          },
          "target_2": {
            "price": 6.20,
            "shares_to_sell": 1500,
            "amount": 9300,
            "percentage": 41,
            "rationale": "Second profit target"
          },
          "target_3": {
            "price": 7.00,
            "shares_to_sell": 1000,
            "amount": 7000,
            "percentage": 27,
            "rationale": "Trailing stop for remaining position"
          }
        },
        "risk_management": {
          "stop_loss_price": 4.85,
          "max_loss_per_trade_rm": 1851,
          "risk_reward_ratio": "1:3.2",
          "position_heat": "Medium - Monitor weekly",
          "review_frequency": "Weekly or on significant price moves"
        },
        "timeline": {
          "entry_timeframe": "2-4 weeks",
          "holding_period": "6-12 months",
          "exit_conditions": [
            "Price reaches target 1: Take 32% profit",
            "Price reaches target 2: Take additional 41% profit",
            "Price hits stop loss: Exit all remaining",
            "Technical breakdown: Re-evaluate"
          ]
        }
      }
    ],
    "portfolio_summary": {
      "total_capital_allocated": 50000,
      "expected_gain_optimistic": 16250,
      "expected_return_percentage": 32.5,
      "expected_holding_period_months": 9,
      "portfolio_heat_level": "Medium",
      "diversification": "3 different sectors"
    },
    "risk_warnings": [
      "Market corrections can impact all holdings",
      "Individual company risks - monitor quarterly results",
      "Liquidity risk for smaller positions - check volume before buying"
    ],
    "analysis_date": "2025-01-15"
  }
  ```
- `handoff-EntryExitPlanner.json`

**Success Criteria:**
- [ ] Entry zones clearly defined
- [ ] Buy tranches calculated
- [ ] 3 profit targets with exit percentages
- [ ] Stop-loss calculated with max risk defined
- [ ] Risk-reward ratios documented
- [ ] Position sizes match risk tolerance
- [ ] Review frequency specified
- [ ] Total allocation ≤ user capital

**Position Sizing Formula:**
```
For each position:
  Risk per Trade (RM) = User Capital × Risk % × Allocation %
  Position Size (Shares) = (Entry Price - Stop Loss) / Risk per Trade
  
Example:
  Capital = RM50,000
  Risk Tolerance = 2% per trade = RM1,000
  Allocation to stock = 40% = RM20,000
  Entry = 5.10, Stop = 4.85, Difference = 0.25
  Position = RM1,000 / 0.25 = 4,000 shares
```

---

### Stage 8: Report Generation
**Agent:** ReportGenerator
**Prompt File:** `@agents/07_ReportGenerator.md`

**Inputs:**
- All previous analysis reports
- `profiles/{user_id}.json`
- `trading_plans.json`

**Outputs:**
- `reports/FINAL_ANALYSIS_REPORT.md` (Markdown)
  ```markdown
  # Share Analysis Report
  ## User: [Name]
  ## Date: 2025-01-15
  
  ### Executive Summary
  - Recommended 3 companies across [sectors]
  - Expected return: 28-35%
  - Time horizon: 6-12 months
  - Risk level: Medium
  
  ### Market Analysis
  [Money flow, sector trends]
  
  ### Company Rankings
  [Top 3 with scores]
  
  ### Detailed Analysis
  [Fundamentals, Technical, Entry/Exit for each]
  
  ### Portfolio Strategy
  [Overall allocation, risk management]
  
  ### Next Steps
  [Action items for investor]
  ```
- `reports/FINAL_ANALYSIS_REPORT.json` (Structured JSON)
- `reports/FINAL_ANALYSIS_REPORT.pdf` (PDF export)
- `handoff-ReportGenerator.json`

**Success Criteria:**
- [ ] All analysis components included
- [ ] Clear and actionable recommendations
- [ ] Risk warnings documented
- [ ] Entry/exit plans explicit
- [ ] Multiple format exports (MD, JSON, PDF)
- [ ] Report validated and proofread
- [ ] User-friendly presentation

---

## Quality Gates & Validation

### Quality Gate 1: MoneyFlowAnalyzer
**Validation:** Sectors identified with inflow analysis
```bash
# Pass if:
jq '.recommended_sectors | length' reports/sector_analysis.json
# Returns ≥3
```

### Quality Gate 2: CompanyFinder
**Validation:** Sufficient candidates found
```bash
# Pass if:
jq '.candidates | length' reports/company_candidates.json
# Returns ≥5 per sector
```

### Quality Gate 3: FundamentalAnalyzer
**Validation:** All companies scored
```bash
# Pass if:
jq '.analysis | length' reports/fundamental_scores.json
# Returns = candidates count
# AND all composite_fundamental_score ≥ 5.0
```

### Quality Gate 4: TechnicalAnalyzer
**Validation:** Technical analysis complete
```bash
# Pass if:
jq '.analysis | length' reports/technical_scores.json
# Returns = candidates count
# AND all have entry_zone, stop_loss_suggestion
```

### Quality Gate 5: RankingEngine
**Validation:** Top 3 ranked with valid scores
```bash
# Pass if:
jq '.top_3_found' reports/company_rankings.json
# Returns true
# AND rank_1.composite_score ≥ 7.0
```

### Quality Gate 6: EntryExitPlanner
**Validation:** Trading plans complete with risk management
```bash
# Pass if:
jq '.plans | length' reports/trading_plans.json
# Returns 3
# AND all have entry_plan, exit_plan, risk_management
```

---

## User Profile Management

### User Profile Schema
**File:** `profiles/{user_id}.json`

```json
{
  "user_id": "user_12345",
  "name": "John Investor",
  "email": "john@example.com",
  "created_date": "2025-01-15T10:00:00Z",
  "investment_profile": {
    "risk_tolerance": "Medium",
    "experience_level": "Intermediate",
    "investment_capital_rm": 50000,
    "time_horizon_months": 12,
    "preferred_sectors": ["Technology", "Finance"],
    "excluded_sectors": ["Energy", "Gambling"],
    "minimum_market_cap_rm": 500000000,
    "minimum_daily_volume": 100000
  },
  "portfolio_targets": {
    "expected_annual_return_percentage": 25,
    "max_risk_per_trade_percentage": 2,
    "diversification_target_sectors": 3,
    "max_single_position_percentage": 40
  },
  "analysis_history": [
    {
      "session_id": "session_001",
      "created_date": "2025-01-15T10:30:00Z",
      "status": "completed",
      "top_3_recommendations": ["TECH.KL", "FIN.KL", "IND.KL"],
      "report_path": "sessions/session_001/reports/"
    }
  ],
  "preferences": {
    "report_format": "pdf",
    "notification_email": true,
    "language": "en"
  }
}
```

### User Actions & Next Steps

The system maintains a running "Next Steps" guide for each user:

**After Initial Analysis (Session Complete):**
```json
{
  "user_id": "user_12345",
  "current_status": "awaiting_market_opportunity",
  "next_steps": [
    {
      "step": 1,
      "action": "Monitor entry zones",
      "details": "Watch for prices to enter defined zones",
      "target_companies": ["TECH.KL", "FIN.KL", "IND.KL"],
      "timeframe": "2-4 weeks",
      "status": "active"
    },
    {
      "step": 2,
      "action": "Execute entry tranches",
      "details": "Buy in 2 tranches as price enters zone",
      "execution_criteria": "Price at 5.15 (tranche 1), 5.05 (tranche 2)",
      "status": "pending"
    },
    {
      "step": 3,
      "action": "Set price alerts",
      "details": "Set alerts for support, targets, and stop loss",
      "alert_prices": {
        "TECH.KL": [4.85, 5.80, 6.20, 7.00]
      },
      "status": "pending"
    },
    {
      "step": 4,
      "action": "Monitor portfolio weekly",
      "details": "Review positions every week, check for signals",
      "frequency": "Weekly",
      "status": "pending"
    }
  ],
  "last_updated": "2025-01-15T12:00:00Z"
}
```

---

## Analysis Session Structure

### Session Directory
```
sessions/
└── session_001/
    ├── session_metadata.json
    ├── user_snapshot.json
    ├── reports/
    │   ├── sector_analysis.json
    │   ├── company_candidates.json
    │   ├── fundamental_scores.json
    │   ├── technical_scores.json
    │   ├── company_rankings.json
    │   ├── trading_plans.json
    │   ├── FINAL_ANALYSIS_REPORT.md
    │   ├── FINAL_ANALYSIS_REPORT.json
    │   └── FINAL_ANALYSIS_REPORT.pdf
    └── handoffs/
        ├── handoff-ProfileManager.json
        ├── handoff-MoneyFlowAnalyzer.json
        ├── handoff-CompanyFinder.json
        ├── handoff-FundamentalAnalyzer.json
        ├── handoff-TechnicalAnalyzer.json
        ├── handoff-RankingEngine.json
        ├── handoff-EntryExitPlanner.json
        └── handoff-ReportGenerator.json
```

### Session Metadata
```json
{
  "session_id": "session_001",
  "user_id": "user_12345",
  "created_date": "2025-01-15T10:00:00Z",
  "status": "completed",
  "analysis_timestamp": "2025-01-15T12:45:00Z",
  "analysis_duration_minutes": 165,
  "iterations": 1,
  "total_candidates_analyzed": 12,
  "top_3_companies": ["TECH.KL", "FIN.KL", "IND.KL"],
  "total_capital_recommended": 50000,
  "expected_return_percentage": 30.5,
  "agents_executed": [
    "MoneyFlowAnalyzer",
    "CompanyFinder",
    "FundamentalAnalyzer",
    "TechnicalAnalyzer",
    "RankingEngine",
    "EntryExitPlanner",
    "ReportGenerator"
  ]
}
```

---

## Iteration Scenarios

### Scenario 1: Successful First Iteration
```
MoneyFlowAnalyzer → Finds 4 sectors
CompanyFinder → Finds 15 candidates (3-5 per sector)
FundamentalAnalyzer → Scores all 15
TechnicalAnalyzer → Analyzes all 15
RankingEngine → Top 3 scored 8.5, 8.1, 7.8 → PASS
EntryExitPlanner → Creates trading plans → SUCCESS
```

### Scenario 2: Insufficient Candidates (Iteration 2)
```
MoneyFlowAnalyzer → Finds 3 sectors
CompanyFinder → Finds only 8 candidates → Below 5 per sector
RankingEngine → Top 3 scored 7.2, 6.8, 6.5 → MARGINAL

Action: Iteration++
CompanyFinder (attempt 2) → Expands criteria, finds 12 more
FundamentalAnalyzer → Re-scores all 20
TechnicalAnalyzer → Re-analyzes all 20
RankingEngine → Top 3 scored 8.4, 8.0, 7.6 → PASS
EntryExitPlanner → SUCCESS
```

### Scenario 3: Max Iterations Reached
```
Iteration 1: Finds 3 companies, scores 6.8, 6.2, 5.9 → Below threshold
Iteration 2: Finds 4 companies, scores 7.5, 7.1, 6.6 → Still marginal
Iteration 3: Finds 5 companies, scores 7.8, 7.4, 7.0 → PASS

If Iteration 3 still < 3 companies or scores < 6.5:
→ Use best available candidates
→ Add note: "Analysis used 3 iterations, recommend with caution"
```

---

## Error Handling & Failure Recovery

### Data Availability Issues
| Issue | Recovery |
|-------|----------|
| Missing financial report | Retry with Q-1 or annual report |
| Incomplete price data | Use available data with notation |
| Sector has <5 companies | Expand search or adjust criteria |
| No technical data (new IPO) | Use fundamental analysis only |

### Quality Issues
| Issue | Action |
|-------|--------|
| Low quality score (<6.0) | Exclude from top 3, find replacement |
| Insufficient data | Mark as "pending" and retry later |
| Conflicting indicators | Document both viewpoints |
| System error in agent | Retry agent (max 3x) |

---

## Handoff Format

All agents must create `handoff-{AgentName}.json`:

```json
{
  "agent_name": "MoneyFlowAnalyzer",
  "session_id": "session_001",
  "status": "success",
  "completion_timestamp": "2025-01-15T10:15:00Z",
  "execution_duration_seconds": 180,
  "iteration": 1,
  "retry_count": 0,
  "artifacts_created": [
    "reports/sector_analysis.json"
  ],
  "validation_passed": true,
  "context_for_next_agent": {
    "recommended_sectors": ["Technology", "Finance", "Utilities"],
    "sector_inflow_summary": {
      "Technology": "+22.5% (strongly bullish)",
      "Finance": "+8.2% (neutral to bullish)",
      "Utilities": "-3.1% (slightly bearish)"
    },
    "data_freshness": "Updated 2025-01-15"
  },
  "issues_found": [],
  "warnings": [],
  "validation_command": "jq '.recommended_sectors | length' reports/sector_analysis.json",
  "validation_result": "3 sectors identified"
}
```

---

## Success Metrics & KPIs

### Analysis Quality Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Top 3 avg composite score | ≥7.5/10 | RankingEngine report |
| Fundamental scores coverage | 100% | All candidates scored |
| Technical data completeness | ≥90% | Data availability check |
| Entry zones validation | 100% | All 3 have defined zones |
| Risk management defined | 100% | All 3 have stop loss |

### Iteration Efficiency
| Metric | Target | Measurement |
|--------|--------|-------------|
| Iterations to completion | ≤2 | Session metadata |
| Iteration 1 success rate | ≥70% | Historical success count |
| Avg analysis time | ≤3 hours | Duration in session metadata |
| Agent retry rate | <10% | Total retries / agents run |

### Recommendation Accuracy (Post-Use)
| Metric | Target | Measurement |
|--------|--------|-------------|
| Avg return vs prediction | ±15% | User feedback |
| Stop loss triggered | <10% | Portfolio performance |
| Entry zone accuracy | ±5% | Actual vs predicted |
| Holding period accuracy | ±3 months | User execution timeline |

---

## Agent Execution Checklist

### Before Each Agent Runs
- [ ] Read this master instruction
- [ ] Read agent's specific prompt file
- [ ] Review previous agent's handoff
- [ ] Validate input data exists and is fresh
- [ ] Review user profile for constraints

### During Execution
- [ ] Follow agent prompt exactly
- [ ] Document all decisions and rationale
- [ ] Validate output quality gates
- [ ] Create detailed handoff file
- [ ] Note any issues or limitations

### After Completion
- [ ] Create handoff-{AgentName}.json
- [ ] Verify all artifacts exist
- [ ] Run validation command
- [ ] Document context for next agent
- [ ] Report status and issues

---

## Production Checklist

Before deploying analysis to user:

### Data Quality
- [ ] All financial data sources documented
- [ ] Analysis period clearly stated (e.g., "as of 2025-01-15")
- [ ] Data freshness ≤1 week for prices, ≤3 months for financials
- [ ] No data gaps in required fields

### Analysis Quality
- [ ] All 7 agent stages completed
- [ ] All quality gates passed
- [ ] Top 3 companies scored ≥6.5/10
- [ ] Entry/exit plans with explicit levels
- [ ] Risk management defined

### User Communication
- [ ] Risk warnings included
- [ ] Assumptions documented
- [ ] Limitations noted (e.g., "not financial advice")
- [ ] Next steps clear and actionable
- [ ] Contact info for questions

### Documentation
- [ ] Report is well-formatted and readable
- [ ] Technical analysis explained
- [ ] Fundamentals clearly presented
- [ ] Recommendations are specific (not vague)
- [ ] Charts/visuals included (if available)

---

## Next Steps for Users

After receiving analysis report, users should:

**Week 1: Preparation**
- [ ] Read full report thoroughly
- [ ] Understand entry zones and reasons
- [ ] Set up price alerts in brokerage
- [ ] Verify broker access and liquidity
- [ ] Calculate exact share quantities for each tranche

**Week 2-4: Entry Phase**
- [ ] Monitor prices for entry zone
- [ ] Execute tranches per plan
- [ ] Record entry prices and dates
- [ ] Set stop-loss orders in broker
- [ ] Document positions in spreadsheet

**Ongoing: Monitoring**
- [ ] Review portfolio weekly
- [ ] Monitor for technical breakdowns
- [ ] Check quarterly earnings dates
- [ ] Adjust stop losses if needed
- [ ] Exit per plan (don't let winners run indefinitely)

**When to Reassess**
- [ ] Stock breaks below support (check for exit)
- [ ] Company misses earnings (re-evaluate)
- [ ] Major market correction (review allocation)
- [ ] Position reaches profit target (execute exit)

---

## Support & Escalation

### Agent Failure (Retry Logic)
1. **First Failure** → Retry agent with same parameters (max 3x)
2. **Persistent Failure** → Review error logs and adjust input data
3. **Data Issue** → Go back to previous agent, request data refresh
4. **Unknown Error** → Document fully and escalate to human

### Analysis Quality Issues
- **Low scores (all <6.0)** → Expand search, add more sectors
- **Conflicts between metrics** → Increase weighting to quantitative data
- **Insufficient candidates** → Adjust market cap or volume filters
- **User dissatisfaction** → Run new analysis with different criteria

---

## Version & Maintenance

**Version:** 1.0
**Created:** 2025-01-15
**Last Updated:** 2025-01-15
**Status:** Ready for Production

### Future Enhancements
- Machine learning predictions for target prices
- Sentiment analysis from news/social media
- Options strategies for risk management
- Portfolio rebalancing recommendations
- Tax-loss harvesting suggestions
- Comparison to user's existing portfolio
