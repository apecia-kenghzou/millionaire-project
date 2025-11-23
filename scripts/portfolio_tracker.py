#!/usr/bin/env python3
"""
Portfolio Tracker - Milestone 4
Track stock holdings, calculate paper gains/losses, and mark daily performance
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

class PortfolioTracker:
    """Manage portfolio tracking with paper gains/losses"""

    def __init__(self, portfolio_file: str = "portfolio.json"):
        self.portfolio_file = Path(portfolio_file)
        self.portfolio = self._load_portfolio()

    def _load_portfolio(self) -> Dict:
        """Load portfolio from JSON file"""
        if self.portfolio_file.exists():
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        else:
            print(f"❌ Portfolio file not found: {self.portfolio_file}")
            sys.exit(1)

    def _save_portfolio(self):
        """Save portfolio to JSON file"""
        self.portfolio['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f, indent=2)
        print(f"💾 Portfolio saved to {self.portfolio_file}")

    def buy_stock(self, symbol: str, shares: int, price: float, date: str = None):
        """
        Buy stock and add to holdings

        Args:
            symbol: Stock symbol (e.g., PENTA.KL)
            shares: Number of shares to buy
            price: Purchase price per share
            date: Purchase date (default: today)
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        total_cost = shares * price

        # Check if enough cash
        current_cash = self.portfolio['capital']['current_cash_rm']
        if total_cost > current_cash:
            print(f"❌ Insufficient cash! Need RM {total_cost:.2f}, have RM {current_cash:.2f}")
            return False

        # Create holding entry
        holding = {
            "symbol": symbol,
            "shares": shares,
            "purchase_price_rm": price,
            "purchase_date": date,
            "purchase_value_rm": total_cost,
            "current_price_rm": price,  # Will be updated by mark_daily_performance
            "current_value_rm": total_cost,
            "paper_gain_loss_rm": 0.00,
            "paper_gain_loss_percent": 0.00
        }

        # Check if we already hold this stock
        existing_holding = next((h for h in self.portfolio['holdings'] if h['symbol'] == symbol), None)

        if existing_holding:
            # Average down/up
            total_shares = existing_holding['shares'] + shares
            total_cost_all = existing_holding['purchase_value_rm'] + total_cost
            avg_price = total_cost_all / total_shares

            existing_holding['shares'] = total_shares
            existing_holding['purchase_price_rm'] = round(avg_price, 4)
            existing_holding['purchase_value_rm'] = round(total_cost_all, 2)
            existing_holding['current_value_rm'] = round(total_shares * existing_holding['current_price_rm'], 2)

            print(f"📈 Added to existing position: {symbol}")
            print(f"   Total Shares: {total_shares}")
            print(f"   Average Price: RM {avg_price:.4f}")
        else:
            # New holding
            self.portfolio['holdings'].append(holding)
            print(f"✅ Bought new position: {symbol}")
            print(f"   Shares: {shares}")
            print(f"   Price: RM {price:.2f}")

        # Update capital
        self.portfolio['capital']['current_cash_rm'] = round(current_cash - total_cost, 2)
        self.portfolio['capital']['total_invested_rm'] = round(
            self.portfolio['capital']['total_invested_rm'] + total_cost, 2
        )

        # Add to transaction history
        transaction = {
            "type": "BUY",
            "symbol": symbol,
            "shares": shares,
            "price_rm": price,
            "total_rm": total_cost,
            "date": date,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.portfolio['transaction_history'].append(transaction)

        # Update suggested_buys status
        for suggestion in self.portfolio.get('suggested_buys', []):
            if suggestion['symbol'] == symbol:
                suggestion['status'] = 'executed'
                suggestion['executed_date'] = date
                suggestion['executed_price'] = price
                suggestion['executed_shares'] = shares

        self._save_portfolio()
        print(f"💰 Remaining Cash: RM {self.portfolio['capital']['current_cash_rm']:.2f}")

        return True

    def sell_stock(self, symbol: str, shares: int, price: float, date: str = None):
        """
        Sell stock and remove/reduce from holdings

        Args:
            symbol: Stock symbol (e.g., PENTA.KL)
            shares: Number of shares to sell
            price: Selling price per share
            date: Sale date (default: today)
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        # Find holding
        holding = next((h for h in self.portfolio['holdings'] if h['symbol'] == symbol), None)

        if not holding:
            print(f"❌ No holding found for {symbol}")
            return False

        if shares > holding['shares']:
            print(f"❌ Cannot sell {shares} shares. Only have {holding['shares']} shares of {symbol}")
            return False

        # Calculate proceeds
        total_proceeds = shares * price
        cost_basis = shares * holding['purchase_price_rm']
        realized_gain_loss = total_proceeds - cost_basis

        # Update or remove holding
        if shares == holding['shares']:
            # Sell entire position
            self.portfolio['holdings'].remove(holding)
            print(f"🔻 Sold entire position: {symbol}")
        else:
            # Partial sell
            holding['shares'] -= shares
            holding['purchase_value_rm'] = round(holding['shares'] * holding['purchase_price_rm'], 2)
            holding['current_value_rm'] = round(holding['shares'] * holding['current_price_rm'], 2)
            print(f"📉 Sold partial position: {symbol}")
            print(f"   Remaining Shares: {holding['shares']}")

        # Update capital
        self.portfolio['capital']['current_cash_rm'] = round(
            self.portfolio['capital']['current_cash_rm'] + total_proceeds, 2
        )
        self.portfolio['capital']['total_invested_rm'] = round(
            self.portfolio['capital']['total_invested_rm'] - cost_basis, 2
        )

        # Add to transaction history
        transaction = {
            "type": "SELL",
            "symbol": symbol,
            "shares": shares,
            "price_rm": price,
            "total_rm": total_proceeds,
            "cost_basis_rm": cost_basis,
            "realized_gain_loss_rm": round(realized_gain_loss, 2),
            "realized_gain_loss_percent": round((realized_gain_loss / cost_basis) * 100, 2),
            "date": date,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.portfolio['transaction_history'].append(transaction)

        self._save_portfolio()

        print(f"💵 Sale Proceeds: RM {total_proceeds:.2f}")
        print(f"💰 Realized Gain/Loss: RM {realized_gain_loss:.2f} ({transaction['realized_gain_loss_percent']:.2f}%)")
        print(f"💰 Total Cash: RM {self.portfolio['capital']['current_cash_rm']:.2f}")

        return True

    def mark_daily_performance(self, current_prices: Dict[str, float], date: str = None):
        """
        Mark daily performance with current prices

        Args:
            current_prices: Dict mapping symbol to current price
            date: Performance date (default: today)
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        print(f"\n📊 Marking Performance for {date}")
        print("=" * 60)

        total_current_value = 0.0
        total_paper_gain_loss = 0.0

        performance_data = {
            "date": date,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "holdings": []
        }

        # Update each holding with current price
        for holding in self.portfolio['holdings']:
            symbol = holding['symbol']

            if symbol not in current_prices:
                print(f"⚠️  No price data for {symbol}, skipping...")
                continue

            current_price = current_prices[symbol]
            shares = holding['shares']
            purchase_price = holding['purchase_price_rm']

            current_value = shares * current_price
            purchase_value = holding['purchase_value_rm']
            paper_gain_loss = current_value - purchase_value
            paper_gain_loss_pct = (paper_gain_loss / purchase_value) * 100 if purchase_value > 0 else 0

            # Update holding
            holding['current_price_rm'] = round(current_price, 2)
            holding['current_value_rm'] = round(current_value, 2)
            holding['paper_gain_loss_rm'] = round(paper_gain_loss, 2)
            holding['paper_gain_loss_percent'] = round(paper_gain_loss_pct, 2)

            total_current_value += current_value
            total_paper_gain_loss += paper_gain_loss

            # Add to performance record
            performance_data['holdings'].append({
                "symbol": symbol,
                "shares": shares,
                "purchase_price_rm": purchase_price,
                "current_price_rm": current_price,
                "current_value_rm": round(current_value, 2),
                "paper_gain_loss_rm": round(paper_gain_loss, 2),
                "paper_gain_loss_percent": round(paper_gain_loss_pct, 2)
            })

            # Print holding performance
            gain_loss_color = "🟢" if paper_gain_loss >= 0 else "🔴"
            print(f"{gain_loss_color} {symbol}: {shares} shares @ RM {current_price:.2f}")
            print(f"   Purchase: RM {purchase_value:.2f} | Current: RM {current_value:.2f}")
            print(f"   P/L: RM {paper_gain_loss:+.2f} ({paper_gain_loss_pct:+.2f}%)")

        # Calculate portfolio totals
        cash = self.portfolio['capital']['current_cash_rm']
        total_portfolio_value = total_current_value + cash
        total_return = total_portfolio_value - self.portfolio['capital']['initial_capital_rm']
        total_return_pct = (total_return / self.portfolio['capital']['initial_capital_rm']) * 100

        # Update capital
        self.portfolio['capital']['total_portfolio_value_rm'] = round(total_portfolio_value, 2)
        self.portfolio['capital']['total_paper_gain_loss_rm'] = round(total_paper_gain_loss, 2)
        self.portfolio['capital']['total_paper_gain_loss_percent'] = round(
            (total_paper_gain_loss / self.portfolio['capital']['total_invested_rm']) * 100
            if self.portfolio['capital']['total_invested_rm'] > 0 else 0, 2
        )

        # Update performance data
        performance_data['portfolio_summary'] = {
            "cash_rm": round(cash, 2),
            "invested_value_rm": round(total_current_value, 2),
            "total_portfolio_value_rm": round(total_portfolio_value, 2),
            "total_paper_gain_loss_rm": round(total_paper_gain_loss, 2),
            "total_return_rm": round(total_return, 2),
            "total_return_percent": round(total_return_pct, 2)
        }

        # Add to daily performance history
        self.portfolio['daily_performance'].append(performance_data)

        # Update performance summary
        self._update_performance_summary()

        self._save_portfolio()

        # Print summary
        print("\n" + "=" * 60)
        print("📈 PORTFOLIO SUMMARY")
        print("=" * 60)
        print(f"💵 Cash: RM {cash:.2f}")
        print(f"📊 Invested Value: RM {total_current_value:.2f}")
        print(f"💰 Total Portfolio Value: RM {total_portfolio_value:.2f}")
        print(f"📊 Paper Gain/Loss: RM {total_paper_gain_loss:+.2f} ({self.portfolio['capital']['total_paper_gain_loss_percent']:+.2f}%)")
        print(f"🎯 Total Return: RM {total_return:+.2f} ({total_return_pct:+.2f}%)")
        print("=" * 60)

        return True

    def _update_performance_summary(self):
        """Update performance summary with best/worst performers"""
        holdings = self.portfolio['holdings']

        if not holdings:
            return

        # Find best and worst performers
        best = max(holdings, key=lambda h: h.get('paper_gain_loss_percent', 0))
        worst = min(holdings, key=lambda h: h.get('paper_gain_loss_percent', 0))

        self.portfolio['performance_summary']['best_performer'] = {
            "symbol": best['symbol'],
            "gain_loss_percent": best.get('paper_gain_loss_percent', 0),
            "gain_loss_rm": best.get('paper_gain_loss_rm', 0)
        }

        self.portfolio['performance_summary']['worst_performer'] = {
            "symbol": worst['symbol'],
            "gain_loss_percent": worst.get('paper_gain_loss_percent', 0),
            "gain_loss_rm": worst.get('paper_gain_loss_rm', 0)
        }

        self.portfolio['performance_summary']['days_tracked'] = len(self.portfolio['daily_performance'])

        # Calculate win rate
        winning_holdings = sum(1 for h in holdings if h.get('paper_gain_loss_rm', 0) > 0)
        total_holdings = len(holdings)
        self.portfolio['performance_summary']['win_rate'] = round(
            (winning_holdings / total_holdings) * 100 if total_holdings > 0 else 0, 2
        )

        # Update total return
        self.portfolio['performance_summary']['total_return_rm'] = self.portfolio['capital']['total_paper_gain_loss_rm']
        self.portfolio['performance_summary']['total_return_percent'] = self.portfolio['capital']['total_paper_gain_loss_percent']

    def show_portfolio(self):
        """Display current portfolio status"""
        print("\n" + "=" * 80)
        print("💼 PORTFOLIO STATUS")
        print("=" * 80)

        capital = self.portfolio['capital']
        print(f"\n💰 CAPITAL:")
        print(f"   Initial Capital: RM {capital['initial_capital_rm']:,.2f}")
        print(f"   Current Cash: RM {capital['current_cash_rm']:,.2f}")
        print(f"   Total Invested: RM {capital['total_invested_rm']:,.2f}")
        print(f"   Total Portfolio Value: RM {capital['total_portfolio_value_rm']:,.2f}")
        print(f"   Paper Gain/Loss: RM {capital['total_paper_gain_loss_rm']:+,.2f} ({capital['total_paper_gain_loss_percent']:+.2f}%)")

        print(f"\n📊 HOLDINGS ({len(self.portfolio['holdings'])} stocks):")

        if not self.portfolio['holdings']:
            print("   No holdings yet")
        else:
            for holding in self.portfolio['holdings']:
                symbol = holding['symbol'].replace('.KL', '')
                shares = holding['shares']
                purchase_price = holding['purchase_price_rm']
                current_price = holding.get('current_price_rm', purchase_price)
                current_value = holding.get('current_value_rm', 0)
                paper_gl = holding.get('paper_gain_loss_rm', 0)
                paper_gl_pct = holding.get('paper_gain_loss_percent', 0)

                gl_symbol = "🟢" if paper_gl >= 0 else "🔴"

                print(f"\n   {gl_symbol} {symbol}")
                print(f"      Shares: {shares:,}")
                print(f"      Purchase Price: RM {purchase_price:.2f}")
                print(f"      Current Price: RM {current_price:.2f}")
                print(f"      Current Value: RM {current_value:,.2f}")
                print(f"      P/L: RM {paper_gl:+,.2f} ({paper_gl_pct:+.2f}%)")

        print(f"\n🎯 PERFORMANCE SUMMARY:")
        perf = self.portfolio['performance_summary']
        print(f"   Total Return: RM {perf['total_return_rm']:+,.2f} ({perf['total_return_percent']:+.2f}%)")
        print(f"   Days Tracked: {perf['days_tracked']}")
        print(f"   Win Rate: {perf['win_rate']:.2f}%")

        if perf.get('best_performer'):
            best = perf['best_performer']
            print(f"   Best Performer: {best['symbol']} ({best['gain_loss_percent']:+.2f}%)")

        if perf.get('worst_performer'):
            worst = perf['worst_performer']
            print(f"   Worst Performer: {worst['symbol']} ({worst['gain_loss_percent']:+.2f}%)")

        print("\n" + "=" * 80)

    def show_transactions(self, limit: int = 10):
        """Show recent transactions"""
        transactions = self.portfolio['transaction_history']

        print(f"\n📝 TRANSACTION HISTORY (last {limit}):")
        print("=" * 80)

        if not transactions:
            print("No transactions yet")
        else:
            for txn in transactions[-limit:]:
                txn_type = txn['type']
                symbol = txn['symbol'].replace('.KL', '')
                shares = txn['shares']
                price = txn['price_rm']
                total = txn['total_rm']
                date = txn['date']

                type_symbol = "📈" if txn_type == "BUY" else "📉"

                print(f"{type_symbol} {txn_type} {symbol} | {shares} shares @ RM {price:.2f} = RM {total:.2f} | {date}")

                if txn_type == "SELL":
                    gl = txn.get('realized_gain_loss_rm', 0)
                    gl_pct = txn.get('realized_gain_loss_percent', 0)
                    print(f"   Realized P/L: RM {gl:+.2f} ({gl_pct:+.2f}%)")

        print("=" * 80)


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Portfolio Tracker CLI")
    parser.add_argument('action', choices=['show', 'buy', 'sell', 'mark', 'transactions'],
                        help="Action to perform")
    parser.add_argument('--symbol', help="Stock symbol (e.g., PENTA.KL)")
    parser.add_argument('--shares', type=int, help="Number of shares")
    parser.add_argument('--price', type=float, help="Price per share")
    parser.add_argument('--date', help="Transaction date (YYYY-MM-DD)")
    parser.add_argument('--prices-file', help="JSON file with current prices")

    args = parser.parse_args()

    tracker = PortfolioTracker()

    if args.action == 'show':
        tracker.show_portfolio()

    elif args.action == 'buy':
        if not all([args.symbol, args.shares, args.price]):
            print("❌ --symbol, --shares, and --price required for buy")
            sys.exit(1)
        tracker.buy_stock(args.symbol, args.shares, args.price, args.date)
        tracker.show_portfolio()

    elif args.action == 'sell':
        if not all([args.symbol, args.shares, args.price]):
            print("❌ --symbol, --shares, and --price required for sell")
            sys.exit(1)
        tracker.sell_stock(args.symbol, args.shares, args.price, args.date)
        tracker.show_portfolio()

    elif args.action == 'mark':
        if args.prices_file:
            with open(args.prices_file, 'r') as f:
                data = json.load(f)
                # Extract prices from current_market_data.json format
                prices = {}
                for stock in data.get('stocks', []):
                    prices[stock['symbol']] = stock['current_price']
                tracker.mark_daily_performance(prices, args.date)
        else:
            print("❌ --prices-file required for mark action")
            sys.exit(1)

    elif args.action == 'transactions':
        tracker.show_transactions()


if __name__ == "__main__":
    main()
