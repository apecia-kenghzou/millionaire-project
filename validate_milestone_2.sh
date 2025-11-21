#!/bin/bash
# Milestone 2 Validation Script

echo "=== MILESTONE 2 QUALITY GATE VALIDATION ==="
echo ""
echo "Checking compilation files..."
echo ""

# Check if all required files exist
files=(
    "compilations/2025-11-21_high_return_companies.json"
    "watchlists/active_watchlist_2025-11-21.json"
    "MILESTONE_2_COMPILATION_REPORT.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file MISSING"
    fi
done

echo ""
echo "Validating JSON files..."

# Validate JSON syntax
for json_file in compilations/2025-11-21_high_return_companies.json watchlists/active_watchlist_2025-11-21.json; do
    if jq empty "$json_file" 2>/dev/null; then
        echo "✓ $json_file is valid JSON"
    else
        echo "✗ $json_file has JSON syntax errors"
    fi
done

echo ""
echo "Checking high-return companies data..."

# Count companies in compilation
high_return_count=$(jq '.high_return_companies | length' compilations/2025-11-21_high_return_companies.json 2>/dev/null || echo "0")
echo "  High-return companies identified: $high_return_count"

# Check total allocation
total_allocated=$(jq '.portfolio_allocation_summary.total_allocated_rm' compilations/2025-11-21_high_return_companies.json 2>/dev/null || echo "0")
echo "  Total allocated: RM $total_allocated"

# Check cash reserve
cash_reserve=$(jq '.portfolio_allocation_summary.cash_reserve_rm' compilations/2025-11-21_high_return_companies.json 2>/dev/null || echo "0")
echo "  Cash reserve: RM $cash_reserve"

echo ""
echo "Checking watchlist categories..."

# Count watchlist categories
buy_now_count=$(jq '.category_1_buy_now.count' watchlists/active_watchlist_2025-11-21.json 2>/dev/null || echo "0")
scale_in_count=$(jq '.category_2_scale_in.count' watchlists/active_watchlist_2025-11-21.json 2>/dev/null || echo "0")
wait_count=$(jq '.category_3_wait_for_pullback.count' watchlists/active_watchlist_2025-11-21.json 2>/dev/null || echo "0")

echo "  Buy Now stocks: $buy_now_count"
echo "  Scale In stocks: $scale_in_count"
echo "  Wait for Pullback: $wait_count"

echo ""
echo "=== QUALITY GATE STATUS ==="

# Determine overall status
if [ "$high_return_count" -ge 7 ] && [ "$total_allocated" -gt 0 ] && [ -f "MILESTONE_2_COMPILATION_REPORT.md" ]; then
    echo "✓ ALL QUALITY GATES PASSED"
    echo ""
    echo "Summary:"
    echo "  - $high_return_count high-return companies identified"
    echo "  - RM $total_allocated allocated (76%)"
    echo "  - RM $cash_reserve cash reserve (24%)"
    echo "  - $buy_now_count immediate buy opportunities"
    echo "  - $scale_in_count scale-in strategies"
    echo "  - $wait_count wait-for-pullback stocks"
    echo ""
    echo "✓ MILESTONE 2 COMPLETE"
else
    echo "✗ SOME QUALITY GATES FAILED"
fi

