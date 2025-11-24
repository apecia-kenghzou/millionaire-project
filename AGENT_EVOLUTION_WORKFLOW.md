# 🔄 AGENT EVOLUTION WORKFLOW

**Purpose:** Continuous improvement system for stock analysis agents
**Goal:** Maximize returns through data-driven agent enhancements
**Status:** Active - Milestone 6

---

## 📋 OVERVIEW

This workflow enables your agents to **self-improve** based on actual trading results. Every prediction is tracked, validated, and used to enhance future analysis.

### Key Principle:
**"What gets measured, gets improved. What gets rewarded, gets repeated."**

---

## 🔄 WEEKLY WORKFLOW

### Monday Morning: Validate Predictions
**Time:** 10 minutes
**Script:** `python3 scripts/validate_predictions.py`

**What It Does:**
1. Fetches latest market prices
2. Updates all active predictions with current returns
3. Calculates agent performance metrics
4. Generates lessons learned

**Expected Output:**
```
✅ PENTA.KL:
   Entry: RM 3.85 → Current: RM 4.15
   Return: +7.79% (7 days)
   Peak: +8.31% | Drawdown: -2.34%
   ✅ On track: 7.8% vs 6.0% expected after 7 days
   💡 Rank mismatch justified: Low rank #11 but performing well

📊 PORTFOLIO SUMMARY
Active Positions: 3
Avg Return (Active): +5.23%

🤖 AGENT PERFORMANCE
FundamentalAnalyzer: avg_score 8.2, avg_return 5.2%
TechnicalAnalyzer: avg_score 5.8, avg_return 5.2%
RankingEngine: avg_rank 8.3, avg_return 5.2%
```

---

### Weekly Tasks (15-30 minutes)

#### 1. Review Agent Performance
```bash
# Check agent accuracy
cat reports/agent_performance.json | jq '.agents'

# Look for patterns:
# - Are high fundamental scores beating low ones?
# - Are high technical scores beating low ones?
# - Is rank #1 beating rank #5 beating rank #10?
```

#### 2. Identify Winners and Losers
```bash
# Best performers
cat predictions_tracking.json | jq '.predictions | sort_by(.actual_performance.current_return_pct) | reverse | .[0:3]'

# Worst performers
cat predictions_tracking.json | jq '.predictions | sort_by(.actual_performance.current_return_pct) | .[0:3]'
```

#### 3. Extract Lessons
**For Winners:** What did agents get right?
- High fundamental score? → Trust fundamentals more
- Low technical but recovery signal? → Weight recovery plays higher
- Oversold RSI? → RSI oversold is powerful signal

**For Losers:** What did agents miss?
- High technical score but failed? → Which indicator was wrong?
- Strong fundamentals but weak price? → Was sector wrong?
- High composite but underperformed? → Ranking formula issue?

---

## 🎯 MONTHLY REVIEW (Once per month)

### When: End of month
### Time: 1-2 hours
### Goal: Major agent improvements

### Step 1: Calculate Agent Accuracy (30 min)

Run comprehensive performance analysis:
```bash
python3 scripts/analyze_agent_accuracy.py
```

**What to Measure:**

**FundamentalAnalyzer:**
- Correlation: Do high scores = high returns?
- Best metric: Which of 6 metrics predicts returns best?
- Worst metric: Which metric adds no value?

**TechnicalAnalyzer:**
- Correlation: Do high scores = high returns?
- Best indicator: RSI? MACD? Trend? Volume?
- Special setups: Do oversold recoveries outperform?

**RankingEngine:**
- Rank effectiveness: Does #1 beat #5 beat #10?
- Formula accuracy: Is 50/50 optimal or should we adjust?
- Context awareness: Do special cases perform better?

### Step 2: Identify Improvements (30 min)

Based on data, decide:
1. **Which weights to adjust?**
   - Fundamental metrics: Increase ROE weight? Decrease dividend?
   - Technical indicators: Increase RSI recovery? Decrease MACD?
   - Ranking formula: Change 50/50 split?

2. **Which features to add?**
   - New indicators that correlate with returns?
   - New scoring bonuses for special setups?
   - New filters to avoid losers?

3. **Which agents need redesign?**
   - Any agent consistently wrong?
   - Any agent adding no value?
   - Any agent that could be enhanced?

### Step 3: Implement Improvements (30-60 min)

**Option A: Quick Fixes** (Parameter tuning)
```python
# Example: Adjust ranking weights
# Before:
composite = fundamental * 0.5 + technical * 0.5

# After (if data shows fundamentals predict better):
composite = fundamental * 0.6 + technical * 0.4
```

**Option B: Feature Additions** (New logic)
```python
# Example: Add oversold recovery bonus
if rsi_previous < 15 and rsi_current > 25:
    technical_score += 2.0  # Boost for extreme recovery
```

**Option C: Agent Redesign** (Major changes)
- Rewrite agent prompt with new framework
- Add new data sources
- Change scoring methodology

### Step 4: Test and Deploy (10 min)

1. Update agent file (`.claude/agents/AgentName.md`)
2. Test with historical data if possible
3. Document changes in AGENT_CHANGELOG.md
4. Deploy in next analysis cycle

---

## 📊 QUARTERLY DEEP DIVE (Once per 3 months)

### When: End of quarter
### Time: 3-4 hours
### Goal: Strategic agent enhancements

### Full System Audit

**1. Overall Performance**
- What's our win rate? (Target: 70%+)
- What's our avg return? (Target: 15%+ annually)
- What's our max drawdown? (Target: <15%)

**2. Agent Effectiveness**
- Which agents add the most value?
- Which agents could be retired?
- What new agents should we create?

**3. Competitive Analysis**
- How do we compare to market?
- How do we compare to professionals?
- What edge do we have (or need)?

### Strategic Decisions

**Agent Retirement:**
If an agent adds no value for 3+ months:
- Consider removing it
- Or combining it with another agent
- Or completely redesigning it

**Agent Creation:**
If we repeatedly miss opportunities:
- Create new agent to catch them
- Examples:
  - "SentimentAnalyzer" for news/social sentiment
  - "SeasonalityAnalyzer" for cyclical patterns
  - "DividendHunter" for income investing
  - "MomentumScanner" for breakout trades

**Framework Updates:**
If market conditions change:
- Bull market → Weight technical more
- Bear market → Weight fundamentals more
- High volatility → Tighten stops
- Low volatility → Widen targets

---

## 🛠️ AGENT IMPROVEMENT PROCESS

### When to Improve an Agent

**Triggers:**
1. **Low Accuracy:** <60% correlation with returns for 2+ months
2. **Consistent Errors:** Same type of mistake repeatedly
3. **Market Changes:** Agent logic outdated by new conditions
4. **New Insights:** Data shows better approach exists

### How to Improve an Agent

#### Step 1: Diagnose the Problem
```bash
# Review agent's predictions
cat predictions_tracking.json | jq '.predictions[] | select(.agent_scores.fundamental_score > 8)' | jq '.actual_performance.current_return_pct'

# Expected: High scores → High returns
# If not: Agent has a problem
```

#### Step 2: Analyze Root Cause
**Common Issues:**
- **Wrong weights:** Metric A matters more than thought
- **Missing signals:** Agent ignores important indicators
- **Outdated logic:** Market evolved, agent didn't
- **Bad data:** Input data quality issues

#### Step 3: Design Solution
**Types of Fixes:**
- **Weight adjustment:** Change metric importance
- **Logic enhancement:** Add new rules/bonuses
- **Data improvement:** Better or more data sources
- **Complete redesign:** Start fresh with new approach

#### Step 4: Implement & Test
```bash
# 1. Update agent prompt file
vim .claude/agents/TechnicalAnalyzer.md

# 2. Document change
echo "2025-11-24: Increased RSI weight from 30% to 40%" >> AGENT_CHANGELOG.md

# 3. Test with recent data
# (Manually review last 5 predictions - would improvement help?)

# 4. Deploy
# Agent will use new logic in next analysis cycle
```

#### Step 5: Monitor Results
- Track improved agent's performance
- Compare to pre-improvement baseline
- Expect 2-4 weeks to see impact
- Roll back if worse after 1 month

---

## 📈 SUCCESS METRICS

### Agent Performance Targets

**FundamentalAnalyzer:**
- ✅ Accuracy: >75% (high scores beat low scores)
- ✅ Correlation R²: >0.70 (scores predict returns)
- ✅ Return gap: High scores +10% vs low scores

**TechnicalAnalyzer:**
- ✅ Accuracy: >70%
- ✅ Correlation R²: >0.65
- ✅ Oversold recovery rate: >80% (when flagged)

**RankingEngine:**
- ✅ Rank effectiveness: #1 beats #5 beats #10
- ✅ Top 3 avg return: >18% annually
- ✅ Ranking R²: >0.75

**Overall System:**
- ✅ Win rate: >70%
- ✅ Avg return: >15% annually
- ✅ Max drawdown: <15%
- ✅ Sharpe ratio: >1.5

### How to Check Metrics
```bash
# Weekly quick check
python3 scripts/validate_predictions.py

# Monthly detailed report
python3 scripts/analyze_agent_accuracy.py

# Quarterly full audit
python3 scripts/quarterly_performance_report.py
```

---

## 🎯 PRACTICAL EXAMPLES

### Example 1: TechnicalAnalyzer Improvement

**Problem Found (Week 4):**
```
TechnicalAnalyzer scores:
- PENTA: 4.5/10 → Actual return: +15.2% ✅ (Underscored!)
- STOCK2: 8.2/10 → Actual return: +3.1% ❌ (Overscored!)
- STOCK3: 7.8/10 → Actual return: -2.4% ❌ (Overscored!)

Pattern: Low technical scores on oversold recoveries are WRONG
Pattern: High technical scores without volume confirm are WRONG
```

**Root Cause:**
- RSI oversold recovery (8→32) only worth 30% of score
- But historically this signal has 85% win rate!
- Should be worth more

**Solution Implemented:**
```markdown
# In TechnicalAnalyzer.md, added:

## Special Case: Oversold Recovery Scoring
If RSI recovered from extreme oversold (<15) to neutral (>25):
- Override normal technical scoring
- Assign recovery score: 8.5/10
- Rationale: Historically 85% win rate, avg return 22%
```

**Result (After 1 month):**
```
TechnicalAnalyzer improved scores:
- Oversold recoveries: 82% accuracy (was 55%)
- Normal signals: 68% accuracy (was 65%)
- Overall: 73% accuracy (was 61%) ✅ +12% improvement!
```

---

### Example 2: RankingEngine Enhancement

**Problem Found (Month 2):**
```
Rankings vs Reality:
- Rank #1 (Composite 8.5): +8.2% return ❌ (Should be higher!)
- Rank #8 (Composite 7.1): +18.5% return ✅ (Underranked!)
- Rank #11 (Composite 6.5): +22.3% return ✅ (Severely underranked!)

Pattern: Recovery plays rank too low but perform too well
```

**Root Cause:**
- Fixed 50/50 weighting doesn't account for special setups
- Oversold recovery + strong fundamentals = hidden gem
- But gets low rank due to weak technicals

**Solution Implemented:**
```markdown
# In RankingEngine.md, added:

## Context-Aware Composite Scoring
Base: Fundamental 50% + Technical 50%

Bonuses (max +2.5 points):
+1.5: Extreme oversold recovery (RSI <15 → >25)
+1.0: High volume accumulation at oversold (Vol >2x + RSI <35)
+1.2: Quality washout (Fund >8.0 + Tech <5.0 + recovery signal)
```

**Result (After 1 month):**
```
RankingEngine improved rankings:
- Rank #1 avg return: 24.3% (was 18.2%) ✅
- Rank #1-3 hit rate: 87% (was 71%) ✅
- Rank correlation R²: 0.82 (was 0.64) ✅ +28% improvement!
```

---

## 🚀 GETTING STARTED TODAY

### Immediate Actions

1. **Set up tracking** (Done! ✅)
   ```bash
   # Already created:
   # - predictions_tracking.json
   # - scripts/validate_predictions.py
   ```

2. **Run first validation**
   ```bash
   python3 scripts/validate_predictions.py
   # Review: predictions_tracking.json
   # Review: reports/agent_performance.json
   ```

3. **Schedule weekly validation**
   ```bash
   # Add to calendar: Every Monday 9am
   # Task: Run validate_predictions.py
   # Time: 5 minutes
   ```

4. **Schedule monthly review**
   ```bash
   # Add to calendar: Last Friday of month
   # Task: Full agent performance review
   # Time: 1 hour
   ```

---

## 📚 FILES IN THIS SYSTEM

### Tracking & Validation
- `predictions_tracking.json` - All predictions & actual results
- `scripts/validate_predictions.py` - Weekly validation script
- `reports/agent_performance.json` - Agent metrics & accuracy

### Documentation
- `AGENT_IMPROVEMENT_GUIDE.md` - This master guide
- `AGENT_EVOLUTION_WORKFLOW.md` - Weekly/monthly process
- `AGENT_CHANGELOG.md` - All agent changes over time

### Agent Files (to be updated)
- `.claude/agents/FundamentalAnalyzer.md`
- `.claude/agents/TechnicalAnalyzer.md`
- `.claude/agents/RankingEngine.md`
- (+ 4 other agents)

---

## 💡 PRO TIPS

### Tips for Success

1. **Be Data-Driven:** Trust the numbers, not your gut
2. **Be Patient:** Need 5-10 trades minimum to spot patterns
3. **Be Iterative:** Small improvements compound over time
4. **Be Humble:** If agent wrong, fix it - don't make excuses
5. **Be Consistent:** Weekly validation builds edge

### Common Pitfalls to Avoid

❌ **Making changes without data** → Random walk, no progress
❌ **Changing too much at once** → Can't isolate what worked
❌ **Ignoring small wins** → 2% improvement = 26% over year compounded
❌ **Overfitting to recent trades** → Need 10+ trades for patterns
❌ **Stopping the process** → Continuous improvement is the edge

---

## 🎯 NEXT STEPS

### This Week:
1. ✅ Run `validate_predictions.py` (Done!)
2. ⏳ Add remaining portfolio holdings to tracking
3. ⏳ Review agent performance report
4. ⏳ Identify first improvement opportunity

### This Month:
1. Collect 5+ completed trades
2. Run first accuracy analysis
3. Implement 1-2 quick improvements
4. Measure impact

### This Quarter:
1. Achieve 70%+ win rate
2. Achieve 15%+ avg return
3. Build full agent feedback loop
4. Create 1 new agent if needed

---

**Remember:** The goal isn't perfect agents. The goal is agents that get 1% better every week. After 52 weeks, that's 52% better!

**LET'S BUILD AGENTS THAT EVOLVE AND MAKE US MILLIONAIRES!** 🚀💰📈
