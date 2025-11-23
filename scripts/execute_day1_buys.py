#!/usr/bin/env python3
"""
Execute Day 1 Recommended Buys
Automatically execute the Priority #1, #2, #3 trades from Milestone 2
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.portfolio_tracker import PortfolioTracker

def execute_day1_trades():
    """Execute Day 1 priority trades"""

    print("=" * 80)
    print("💰 EXECUTING DAY 1 RECOMMENDED BUYS")
    print("=" * 80)
    print("\nBased on Milestone 2 analysis (Nov 21, 2025):")
    print("  🔥 Priority #1: PENTA (Recovery Play)")
    print("  💰 Priority #2: GASMSIA (Oversold Entry)")
    print("  ⭐ Priority #3: PBBANK (#1 Ranked)")
    print("\n" + "=" * 80)

    tracker = PortfolioTracker()

    # Get user confirmation
    response = input("\nExecute Day 1 trades? This will buy 3 stocks for RM 13,500 total. (y/n): ")

    if response.lower() != 'y':
        print("❌ Trades cancelled")
        return

    print("\n📈 Executing trades...\n")

    # Priority #1: PENTA (7160.KL)
    print("🔥 Trade 1/3: PENTA")
    tracker.buy_stock(
        symbol="PENTA.KL",
        shares=1038,
        price=3.85,
        date="2025-11-21"
    )

    print()

    # Priority #2: GASMSIA (5209.KL)
    print("💰 Trade 2/3: GASMSIA")
    tracker.buy_stock(
        symbol="GASMSIA.KL",
        shares=699,
        price=4.29,
        date="2025-11-21"
    )

    print()

    # Priority #3: PBBANK
    print("⭐ Trade 3/3: PBBANK")
    tracker.buy_stock(
        symbol="PBBANK.KL",
        shares=1511,
        price=4.30,
        date="2025-11-21"
    )

    print("\n" + "=" * 80)
    print("✅ DAY 1 TRADES COMPLETE!")
    print("=" * 80)

    # Show portfolio
    tracker.show_portfolio()

    print("\n📊 Next Steps:")
    print("  1. Run daily_data_fetcher.py to get current prices")
    print("  2. Run: python3 scripts/portfolio_tracker.py mark --prices-file current_market_data.json")
    print("  3. View portfolio in dashboard: cd website && ./start_server.sh")
    print()


if __name__ == "__main__":
    execute_day1_trades()
