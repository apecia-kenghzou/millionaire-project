#!/usr/bin/env python3
"""
Auto-Regeneration Script - Milestone 5
Analyze current holdings and make intelligent buy/sell/hold decisions
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class PortfolioDecisionEngine:
    """Make intelligent buy/sell/hold decisions based on current portfolio and market data"""

    def __init__(self):
        self.market_data = self._load_market_data()
        self.portfolio = self._load_portfolio()
        self.decisions = {
            'sell': [],
            'hold': [],
            'buy_more': [],
            'new_buy': []
        }
        self.date = datetime.now().strftime('%Y-%m-%d')

    def _load_market_data(self) -> Dict:
        """Load current market data"""
        data_file = Path('current_market_data.json')
        if not data_file.exists():
            print("❌ Market data not found. Run: python3 scripts/daily_data_fetcher.py")
            sys.exit(1)

        with open(data_file, 'r') as f:
            data = json.load(f)

        timestamp = data.get('fetch_date') or data.get('timestamp') or 'Unknown'
        print(f"✅ Loaded market data from {timestamp}")
        return data

    def _load_portfolio(self) -> Dict:
        """Load current portfolio"""
        portfolio_file = Path('website/data/portfolio.json')
        if not portfolio_file.exists():
            print("❌ Portfolio not found")
            sys.exit(1)

        with open(portfolio_file, 'r') as f:
            portfolio = json.load(f)

        print(f"✅ Loaded portfolio: {len(portfolio['holdings'])} holdings, RM {portfolio['capital']['current_cash_rm']:,.2f} cash")
        return portfolio

    def _get_stock_data(self, symbol: str) -> Dict:
        """Get stock data from market data"""
        # Remove .KL suffix if present for matching
        symbol_clean = symbol.replace('.KL', '')

        for stock in self.market_data['stocks']:
            # Try matching yahoo_symbol (e.g., "PENTA.KL" or "0166.KL")
            if stock.get('yahoo_symbol') == symbol:
                return stock
            # Try matching simple symbol (e.g., "PENTA")
            if stock.get('symbol') == symbol_clean:
                return stock
            # Try matching yahoo_symbol without .KL
            yahoo_sym = stock.get('yahoo_symbol', '').replace('.KL', '')
            if yahoo_sym == symbol_clean:
                return stock

        return None

    def analyze_holding(self, holding: Dict) -> Dict:
        """
        Analyze a current holding and decide: SELL, HOLD, or BUY MORE

        Returns decision dict with recommendation and rationale
        """
        symbol = holding['symbol']
        stock_data = self._get_stock_data(symbol)

        if not stock_data:
            return {
                'symbol': symbol,
                'decision': 'HOLD',
                'reason': 'No current market data available',
                'confidence': 'low'
            }

        # Get key metrics
        purchase_price = holding['purchase_price_rm']
        current_price = stock_data['current_price_rm']
        rsi = stock_data.get('momentum_indicators', {}).get('rsi_14', 50)
        macd_histogram = stock_data.get('momentum_indicators', {}).get('histogram', 0)
        volume_ratio = stock_data.get('volume_analysis', {}).get('volume_ratio', 1.0)

        # Calculate performance
        price_change_pct = ((current_price - purchase_price) / purchase_price) * 100

        # Get stop loss from suggested buys (if available)
        stop_loss = self._get_stop_loss(symbol)

        # Decision logic
        decision = self._make_decision(
            symbol=symbol,
            purchase_price=purchase_price,
            current_price=current_price,
            price_change_pct=price_change_pct,
            rsi=rsi,
            macd_histogram=macd_histogram,
            volume_ratio=volume_ratio,
            stop_loss=stop_loss,
            holding=holding,
            stock_data=stock_data
        )

        return decision

    def _get_stop_loss(self, symbol: str) -> float:
        """Get stop loss price for a symbol"""
        stop_losses = {
            'PBBANK.KL': 4.05,
            'PGAS.KL': 17.00,
            'MAYBANK.KL': 9.50,
            'PENTA.KL': 3.50,
            'GASMSIA.KL': 4.05,
            'CIMB.KL': 7.10,
            'INARI.KL': 2.15
        }
        return stop_losses.get(symbol, 0)

    def _make_decision(self, symbol, purchase_price, current_price, price_change_pct,
                      rsi, macd_histogram, volume_ratio, stop_loss, holding, stock_data) -> Dict:
        """Apply decision logic"""

        # SELL CONDITIONS
        if stop_loss > 0 and current_price < stop_loss:
            return {
                'symbol': symbol,
                'decision': 'SELL',
                'reason': f'STOP LOSS HIT: Price RM {current_price:.2f} < Stop Loss RM {stop_loss:.2f}',
                'urgency': 'IMMEDIATE',
                'confidence': 'high',
                'shares': holding['shares'],
                'expected_proceeds_rm': holding['shares'] * current_price,
                'realized_pl_rm': (current_price - purchase_price) * holding['shares'],
                'realized_pl_pct': price_change_pct
            }

        if rsi > 75:
            return {
                'symbol': symbol,
                'decision': 'SELL',
                'reason': f'EXTREME OVERBOUGHT: RSI {rsi:.1f} > 75. Take profits.',
                'urgency': 'HIGH',
                'confidence': 'high',
                'shares': holding['shares'],
                'expected_proceeds_rm': holding['shares'] * current_price,
                'realized_pl_rm': (current_price - purchase_price) * holding['shares'],
                'realized_pl_pct': price_change_pct,
                'note': 'Sell all or 50% to lock in gains'
            }

        if price_change_pct > 40 and rsi > 65:
            return {
                'symbol': symbol,
                'decision': 'SELL',
                'reason': f'PROFIT TARGET: +{price_change_pct:.1f}% gain. RSI {rsi:.1f} overbought. Take profits.',
                'urgency': 'MEDIUM',
                'confidence': 'medium',
                'shares': holding['shares'] // 2,  # Sell half
                'expected_proceeds_rm': (holding['shares'] // 2) * current_price,
                'realized_pl_rm': (current_price - purchase_price) * (holding['shares'] // 2),
                'realized_pl_pct': price_change_pct,
                'note': 'Sell 50%, let rest run'
            }

        # BUY MORE CONDITIONS
        if rsi < 30 and price_change_pct < -10:
            # Oversold + down from purchase = average down opportunity
            suggested_shares = min(holding['shares'], int(1000 / current_price))  # Buy similar amount
            return {
                'symbol': symbol,
                'decision': 'BUY MORE',
                'reason': f'OVERSOLD AVERAGE DOWN: RSI {rsi:.1f} < 30. Price {price_change_pct:+.1f}% from purchase. Strong fundamentals intact.',
                'urgency': 'HIGH',
                'confidence': 'high',
                'suggested_shares': suggested_shares,
                'suggested_price_rm': current_price,
                'suggested_allocation_rm': suggested_shares * current_price,
                'new_average_cost_rm': ((holding['shares'] * purchase_price) + (suggested_shares * current_price)) / (holding['shares'] + suggested_shares),
                'note': f'Average down from RM {purchase_price:.2f} to lower cost basis'
            }

        if volume_ratio > 1.5 and 30 < rsi < 40 and macd_histogram > 0:
            # High volume accumulation at good price
            suggested_shares = int(500 / current_price)
            return {
                'symbol': symbol,
                'decision': 'BUY MORE',
                'reason': f'INSTITUTIONAL ACCUMULATION: Volume {volume_ratio:.2f}x, RSI {rsi:.1f}, MACD bullish. Add to position.',
                'urgency': 'MEDIUM',
                'confidence': 'medium',
                'suggested_shares': suggested_shares,
                'suggested_price_rm': current_price,
                'suggested_allocation_rm': suggested_shares * current_price,
                'new_average_cost_rm': ((holding['shares'] * purchase_price) + (suggested_shares * current_price)) / (holding['shares'] + suggested_shares),
                'note': 'Increased conviction - institutions buying'
            }

        # HOLD CONDITIONS (default)
        status = "on track"
        if price_change_pct > 15:
            status = "ahead of expectations"
        elif price_change_pct < -5:
            status = "behind expectations"

        target_price = self._get_target_price(symbol, current_price)
        upside = ((target_price - current_price) / current_price) * 100 if target_price else 0

        return {
            'symbol': symbol,
            'decision': 'HOLD',
            'reason': f'ON TRACK: {status}. Paper P/L: {price_change_pct:+.1f}%. RSI {rsi:.1f} healthy.',
            'confidence': 'high',
            'current_pl_pct': price_change_pct,
            'current_pl_rm': (current_price - purchase_price) * holding['shares'],
            'target_price_rm': target_price,
            'upside_remaining_pct': upside,
            'rsi': rsi,
            'status': status,
            'note': f'Continue holding. Monitor stop loss RM {stop_loss:.2f}' if stop_loss else 'Continue holding'
        }

    def _get_target_price(self, symbol: str, current_price: float) -> float:
        """Get target price for a symbol"""
        targets = {
            'PENTA.KL': 5.00,      # 30% target
            'GASMSIA.KL': 4.80,    # 18% target
            'PBBANK.KL': 4.68,     # 15% target
            'PGAS.KL': 19.50,      # 15% target
            'MAYBANK.KL': 10.80,   # 15% target
            'CIMB.KL': 8.20,       # 15% target
            'INARI.KL': 2.85       # 22% target
        }
        return targets.get(symbol, current_price * 1.15)  # Default 15% target

    def analyze_new_opportunities(self) -> List[Dict]:
        """Identify new buy opportunities from non-held stocks"""
        new_opportunities = []

        # Get list of currently held symbols
        held_symbols = {h['symbol'] for h in self.portfolio['holdings']}

        # Analyze each stock we don't hold
        for stock in self.market_data['stocks']:
            symbol = stock['symbol']

            if symbol in held_symbols:
                continue  # Skip stocks we already hold

            # Get key metrics
            rsi = stock.get('momentum_indicators', {}).get('rsi_14', 50)
            volume_ratio = stock.get('volume_analysis', {}).get('volume_ratio', 1.0)
            current_price = stock['current_price_rm']

            # Simple scoring (in real version, use proper fundamental analysis)
            # For now, use basic technical signals

            if rsi < 35 and volume_ratio > 1.3:
                # Oversold + high volume = potential opportunity
                new_opportunities.append({
                    'symbol': symbol,
                    'current_price_rm': current_price,
                    'rsi': rsi,
                    'volume_ratio': volume_ratio,
                    'signal': 'OVERSOLD + HIGH VOLUME',
                    'confidence': 'medium',
                    'suggested_allocation_rm': 3000,  # Default allocation
                    'suggested_shares': int(3000 / current_price),
                    'reason': f'RSI {rsi:.1f} oversold with {volume_ratio:.2f}x volume. Potential accumulation opportunity.'
                })

            elif 40 < rsi < 60 and volume_ratio > 1.5:
                # Neutral RSI + high volume = institutional interest
                new_opportunities.append({
                    'symbol': symbol,
                    'current_price_rm': current_price,
                    'rsi': rsi,
                    'volume_ratio': volume_ratio,
                    'signal': 'INSTITUTIONAL ACCUMULATION',
                    'confidence': 'medium',
                    'suggested_allocation_rm': 2500,
                    'suggested_shares': int(2500 / current_price),
                    'reason': f'RSI {rsi:.1f} neutral with {volume_ratio:.2f}x volume. Institutions buying.'
                })

        return sorted(new_opportunities, key=lambda x: x['confidence'], reverse=True)[:3]  # Top 3

    def generate_decision_report(self) -> str:
        """Generate comprehensive decision report"""

        # Categorize decisions
        for holding in self.portfolio['holdings']:
            decision = self.analyze_holding(holding)
            decision_type = decision['decision']

            if decision_type == 'SELL':
                self.decisions['sell'].append(decision)
            elif decision_type == 'HOLD':
                self.decisions['hold'].append(decision)
            elif decision_type == 'BUY MORE':
                self.decisions['buy_more'].append(decision)

        # Find new opportunities
        self.decisions['new_buy'] = self.analyze_new_opportunities()

        # Generate report markdown
        report = self._build_report_markdown()

        # Save report
        decisions_dir = Path('decisions')
        decisions_dir.mkdir(exist_ok=True)

        report_file = decisions_dir / f"{self.date}_portfolio_decisions.md"
        with open(report_file, 'w') as f:
            f.write(report)

        print(f"\n✅ Decision report saved: {report_file}")

        return report

    def _build_report_markdown(self) -> str:
        """Build the decision report markdown"""

        capital = self.portfolio['capital']
        cash = capital['current_cash_rm']

        timestamp = self.market_data.get('fetch_date') or self.market_data.get('timestamp') or 'Unknown'

        report = f"""# 📊 Portfolio Decision Report - {self.date}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Market Data:** {timestamp}

---

## 💼 PORTFOLIO SUMMARY

- **Total Portfolio Value:** RM {capital['total_portfolio_value_rm']:,.2f}
- **Cash Available:** RM {cash:,.2f}
- **Total Invested:** RM {capital['total_invested_rm']:,.2f}
- **Paper Gain/Loss:** RM {capital['total_paper_gain_loss_rm']:+,.2f} ({capital['total_paper_gain_loss_percent']:+.2f}%)
- **Holdings:** {len(self.portfolio['holdings'])} stocks

---

## 📋 DECISION SUMMARY

- 📉 **SELL:** {len(self.decisions['sell'])} stocks
- ✅ **HOLD:** {len(self.decisions['hold'])} stocks
- 📈 **BUY MORE:** {len(self.decisions['buy_more'])} stocks
- 🆕 **NEW BUY:** {len(self.decisions['new_buy'])} opportunities

---
"""

        # SELL DECISIONS
        if self.decisions['sell']:
            report += "\n## 📉 SELL DECISIONS\n\n"
            for dec in self.decisions['sell']:
                report += f"""### {dec['symbol'].replace('.KL', '')}
- **Shares:** {dec['shares']:,}
- **Urgency:** {dec['urgency']}
- **Reason:** {dec['reason']}
- **Expected Proceeds:** RM {dec['expected_proceeds_rm']:,.2f}
- **Realized P/L:** RM {dec['realized_pl_rm']:+,.2f} ({dec['realized_pl_pct']:+.2f}%)
{f"- **Note:** {dec.get('note', '')}" if dec.get('note') else ''}

**Action:**
```bash
python3 scripts/portfolio_tracker.py sell --symbol {dec['symbol']} --shares {dec['shares']} --price {dec.get('expected_proceeds_rm', 0) / dec['shares']:.2f}
```

---

"""

        # HOLD DECISIONS
        if self.decisions['hold']:
            report += "\n## ✅ HOLD DECISIONS\n\n"
            for dec in self.decisions['hold']:
                report += f"""### {dec['symbol'].replace('.KL', '')}
- **Status:** {dec['status']}
- **Paper P/L:** RM {dec['current_pl_rm']:+,.2f} ({dec['current_pl_pct']:+.2f}%)
- **RSI:** {dec['rsi']:.1f}
- **Target Price:** RM {dec.get('target_price_rm', 0):.2f}
- **Upside Remaining:** {dec.get('upside_remaining_pct', 0):+.1f}%
- **Reason:** {dec['reason']}
{f"- **Note:** {dec.get('note', '')}" if dec.get('note') else ''}

**Action:** Continue holding

---

"""

        # BUY MORE DECISIONS
        if self.decisions['buy_more']:
            report += "\n## 📈 BUY MORE (Current Holdings)\n\n"
            for dec in self.decisions['buy_more']:
                report += f"""### {dec['symbol'].replace('.KL', '')}
- **Urgency:** {dec['urgency']}
- **Reason:** {dec['reason']}
- **Suggested Buy:** {dec['suggested_shares']:,} shares @ RM {dec['suggested_price_rm']:.2f} = RM {dec['suggested_allocation_rm']:,.2f}
- **New Average Cost:** RM {dec['new_average_cost_rm']:.2f}
{f"- **Note:** {dec.get('note', '')}" if dec.get('note') else ''}

**Action:**
```bash
python3 scripts/portfolio_tracker.py buy --symbol {dec['symbol']} --shares {dec['suggested_shares']} --price {dec['suggested_price_rm']:.2f}
```

---

"""

        # NEW BUY OPPORTUNITIES
        if self.decisions['new_buy']:
            report += "\n## 🆕 NEW BUY OPPORTUNITIES\n\n"
            for opp in self.decisions['new_buy']:
                report += f"""### {opp['symbol'].replace('.KL', '')}
- **Current Price:** RM {opp['current_price_rm']:.2f}
- **RSI:** {opp['rsi']:.1f}
- **Volume Ratio:** {opp['volume_ratio']:.2f}x
- **Signal:** {opp['signal']}
- **Confidence:** {opp['confidence']}
- **Reason:** {opp['reason']}
- **Suggested Allocation:** RM {opp['suggested_allocation_rm']:,.2f} ({opp['suggested_shares']:,} shares)

**Action:**
```bash
python3 scripts/portfolio_tracker.py buy --symbol {opp['symbol']} --shares {opp['suggested_shares']} --price {opp['current_price_rm']:.2f}
```

---

"""

        # Cash Management
        total_sell_proceeds = sum(dec['expected_proceeds_rm'] for dec in self.decisions['sell'])
        total_buy_cost = sum(dec['suggested_allocation_rm'] for dec in self.decisions['buy_more'])
        total_new_buy_cost = sum(opp['suggested_allocation_rm'] for opp in self.decisions['new_buy'])

        final_cash = cash + total_sell_proceeds - total_buy_cost - total_new_buy_cost

        report += f"""## 💰 CASH MANAGEMENT

- **Current Cash:** RM {cash:,.2f}
- **From Sells:** +RM {total_sell_proceeds:,.2f}
- **Buy More:** -RM {total_buy_cost:,.2f}
- **New Buys:** -RM {total_new_buy_cost:,.2f}
- **Final Cash:** RM {final_cash:,.2f} ({(final_cash / capital['initial_capital_rm']) * 100:.1f}% of initial capital)

---

## 📋 EXECUTION PLAN

**Immediate Actions (High Urgency):**
"""

        # High urgency actions
        high_urgency = [d for d in self.decisions['sell'] if d.get('urgency') == 'IMMEDIATE' or d.get('urgency') == 'HIGH']
        high_urgency += [d for d in self.decisions['buy_more'] if d.get('urgency') == 'HIGH']

        if high_urgency:
            for i, dec in enumerate(high_urgency, 1):
                action = 'SELL' if dec['decision'] == 'SELL' else 'BUY MORE'
                symbol = dec['symbol'].replace('.KL', '')
                report += f"{i}. {action} {symbol} - {dec['reason']}\n"
        else:
            report += "None\n"

        report += f"""
**Monitor Closely:**
"""

        # Monitoring list
        monitors = []
        for dec in self.decisions['hold']:
            symbol = dec['symbol'].replace('.KL', '')
            if dec['current_pl_pct'] < -5:
                monitors.append(f"- {symbol}: Approaching stop loss territory ({dec['current_pl_pct']:+.1f}%)")
            elif dec['current_pl_pct'] > 20:
                monitors.append(f"- {symbol}: Approaching profit target ({dec['current_pl_pct']:+.1f}%)")

        if monitors:
            report += "\n".join(monitors) + "\n"
        else:
            report += "All holdings performing as expected\n"

        report += f"""
**Next Review:** {self._next_review_date()}

---

**Generated by:** Auto-Regeneration System (Milestone 5)
**Follow:** @AUTO_REGENERATE.md for full process
"""

        return report

    def _next_review_date(self) -> str:
        """Determine next review date"""
        if len(self.decisions['sell']) > 0 or len([d for d in self.decisions['buy_more'] if d.get('urgency') == 'HIGH']) > 0:
            return "Daily (urgent actions pending)"
        else:
            return "Weekly (standard review)"

    def print_summary(self):
        """Print decision summary to console"""
        print("\n" + "=" * 80)
        print("📊 PORTFOLIO DECISION SUMMARY")
        print("=" * 80)

        print(f"\n📉 SELL: {len(self.decisions['sell'])} stocks")
        for dec in self.decisions['sell']:
            print(f"   • {dec['symbol'].replace('.KL', '')}: {dec['reason']}")

        print(f"\n✅ HOLD: {len(self.decisions['hold'])} stocks")
        for dec in self.decisions['hold']:
            print(f"   • {dec['symbol'].replace('.KL', '')}: {dec['status']} ({dec['current_pl_pct']:+.1f}%)")

        print(f"\n📈 BUY MORE: {len(self.decisions['buy_more'])} stocks")
        for dec in self.decisions['buy_more']:
            print(f"   • {dec['symbol'].replace('.KL', '')}: {dec['reason']}")

        print(f"\n🆕 NEW BUY: {len(self.decisions['new_buy'])} opportunities")
        for opp in self.decisions['new_buy']:
            print(f"   • {opp['symbol'].replace('.KL', '')}: {opp['signal']}")

        print("\n" + "=" * 80)


def main():
    """Main execution"""
    print("🔄 AUTO-REGENERATION SYSTEM - Milestone 5")
    print("=" * 80)

    # Create decision engine
    engine = PortfolioDecisionEngine()

    # Generate decisions
    print("\n🔍 Analyzing portfolio and market conditions...")
    report = engine.generate_decision_report()

    # Print summary
    engine.print_summary()

    print(f"\n📄 Full decision report saved to: decisions/{engine.date}_portfolio_decisions.md")
    print("\n✅ Regeneration complete!")
    print("\n💡 Next steps:")
    print("   1. Review the decision report")
    print("   2. Execute recommended actions (after approval)")
    print("   3. Update dashboard with new data")


if __name__ == "__main__":
    main()
