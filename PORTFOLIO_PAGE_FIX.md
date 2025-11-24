# 🔧 Portfolio Page Fix

## Problem
After running `python3 scripts/execute_day1_buys.py` or any buy/sell commands, the portfolio page showed no changes even though the scripts ran without errors.

## Root Cause
**Two different portfolio.json files:**

1. `/portfolio.json` ← Scripts were writing here
2. `/website/data/portfolio.json` ← Website was reading from here

The scripts and website were using different files, so they were out of sync!

## Solution
Updated all scripts to use `website/data/portfolio.json` as the single source of truth:

### Files Modified:
- `scripts/portfolio_tracker.py` → Changed default path from `portfolio.json` to `website/data/portfolio.json`
- `scripts/regenerate_analysis.py` → Changed portfolio loading path to `website/data/portfolio.json`

### Result:
✅ Scripts and website now use the SAME file
✅ Portfolio page updates immediately after buying/selling stocks
✅ No more sync issues

## How to Test

### 1. Buy stocks:
```bash
python3 scripts/execute_day1_buys.py
```

### 2. Check the portfolio:
```bash
# View in CLI
python3 scripts/portfolio_tracker.py show

# View in browser
# Go to http://localhost:8000/website/portfolio.html
```

### 3. You should see:
- Holdings table with your stocks
- Updated capital (cash reduced)
- Transaction history
- Portfolio summary

## Before vs After

### Before (Broken):
```
execute_day1_buys.py runs → Updates /portfolio.json
Website reads → /website/data/portfolio.json (empty)
Result: ❌ Nothing shows on website
```

### After (Fixed):
```
execute_day1_buys.py runs → Updates /website/data/portfolio.json
Website reads → /website/data/portfolio.json (same file!)
Result: ✅ Portfolio page shows all your holdings!
```

## Note
The old `/portfolio.json` in the project root is now unused. All portfolio operations use `/website/data/portfolio.json`.
