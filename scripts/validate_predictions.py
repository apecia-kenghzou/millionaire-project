#!/usr/bin/env python3
"""
Prediction Validation Script - Milestone 6
Tracks agent predictions against actual performance to enable continuous improvement
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def load_predictions():
    """Load predictions tracking file"""
    predictions_file = Path('predictions_tracking.json')
    if not predictions_file.exists():
        print("❌ predictions_tracking.json not found")
        sys.exit(1)

    with open(predictions_file, 'r') as f:
        return json.load(f)

def load_market_data():
    """Load current market data"""
    market_file = Path('current_market_data.json')
    if not market_file.exists():
        print("❌ current_market_data.json not found")
        print("💡 Run: python3 scripts/daily_data_fetcher.py")
        sys.exit(1)

    with open(market_file, 'r') as f:
        return json.load(f)

def get_current_price(symbol, market_data):
    """Get current price for a symbol"""
    # Remove .KL suffix for matching
    symbol_clean = symbol.replace('.KL', '')

    for stock in market_data.get('stocks', []):
        if stock['symbol'] == symbol_clean:
            return stock['current_price_rm']

    print(f"⚠️  No price data for {symbol}")
    return None

def calculate_performance(prediction, current_price):
    """Calculate performance metrics"""
    entry_price = prediction['entry_price_rm']
    days_held = (datetime.now() - datetime.strptime(prediction['entry_date'], '%Y-%m-%d')).days

    # Current return
    current_return_rm = (current_price - entry_price) * 100  # Assuming 100 shares for calculation
    current_return_pct = ((current_price - entry_price) / entry_price) * 100

    # Update peak/trough
    peak_price = max(prediction['actual_performance']['peak_price_rm'], current_price)
    trough_price = min(prediction['actual_performance']['trough_price_rm'], current_price)

    peak_return = ((peak_price - entry_price) / entry_price) * 100
    max_drawdown = ((trough_price - entry_price) / entry_price) * 100

    return {
        'current_price_rm': current_price,
        'current_return_pct': round(current_return_pct, 2),
        'current_return_rm': round(current_return_rm, 2),
        'peak_price_rm': peak_price,
        'peak_return_pct': round(peak_return, 2),
        'trough_price_rm': trough_price,
        'max_drawdown_pct': round(max_drawdown, 2),
        'days_held': days_held
    }

def update_milestone_returns(prediction, performance):
    """Update 1-week, 1-month, etc. returns"""
    days_held = performance['days_held']
    actual_perf = prediction['actual_performance']

    # 1 week (7 days)
    if days_held >= 7 and actual_perf['1_week_return'] is None:
        actual_perf['1_week_return'] = performance['current_return_pct']

    # 1 month (30 days)
    if days_held >= 30 and actual_perf['1_month_return'] is None:
        actual_perf['1_month_return'] = performance['current_return_pct']

    # 3 months (90 days)
    if days_held >= 90 and actual_perf['3_month_return'] is None:
        actual_perf['3_month_return'] = performance['current_return_pct']

    # 6 months (180 days)
    if days_held >= 180 and actual_perf['6_month_return'] is None:
        actual_perf['6_month_return'] = performance['current_return_pct']

    # 12 months (365 days)
    if days_held >= 365 and actual_perf['12_month_return'] is None:
        actual_perf['12_month_return'] = performance['current_return_pct']
        actual_perf['final_return'] = performance['current_return_pct']

def generate_lessons(prediction, performance):
    """Generate lessons learned from prediction"""
    lessons = []

    return_pct = performance['current_return_pct']
    predicted_range = prediction['predicted_return_range']
    agent_scores = prediction['agent_scores']

    # Check if prediction on track
    predicted_min = float(predicted_range.split('-')[0].replace('%', ''))
    predicted_max = float(predicted_range.split('-')[1].replace('%', ''))
    timeframe_months = prediction['predicted_timeframe_months']
    days_held = performance['days_held']
    progress = days_held / (timeframe_months * 30)

    expected_return_now = predicted_min * progress
    on_track = return_pct >= expected_return_now * 0.8  # 80% of expected

    if on_track:
        lessons.append(f"✅ On track: {return_pct:.1f}% vs {expected_return_now:.1f}% expected after {days_held} days")
    else:
        lessons.append(f"⚠️  Behind: {return_pct:.1f}% vs {expected_return_now:.1f}% expected after {days_held} days")

    # Check if ranking mismatch was correct
    if agent_scores.get('rank_vs_priority_mismatch'):
        if return_pct > 5:
            lessons.append(f"💡 Rank mismatch justified: Low rank #{agent_scores['original_rank']} but Priority #{agent_scores['priority_assigned']} performing well")
        elif return_pct < -5:
            lessons.append(f"❌ Rank mismatch error: Should have followed rank #{agent_scores['original_rank']} instead of Priority #{agent_scores['priority_assigned']}")

    return lessons

def calculate_agent_performance(predictions):
    """Calculate performance metrics for each agent"""
    # Filter active and completed predictions
    active = [p for p in predictions if p['status'] == 'holding']
    completed = [p for p in predictions if p['status'] == 'closed']

    performance = {
        'validation_date': datetime.now().strftime('%Y-%m-%d'),
        'total_predictions': len(predictions),
        'active_positions': len(active),
        'completed_positions': len(completed),
        'agents': {}
    }

    # Fundamental Analyzer performance
    if predictions:
        fundamental_scores = [p['agent_scores']['fundamental_score'] for p in predictions]
        returns = [p['actual_performance']['current_return_pct'] for p in predictions]

        # Simple correlation (would use scipy in production)
        avg_return = sum(returns) / len(returns)

        performance['agents']['FundamentalAnalyzer'] = {
            'avg_score': round(sum(fundamental_scores) / len(fundamental_scores), 2),
            'avg_return': round(avg_return, 2),
            'accuracy': 'pending' if len(completed) < 5 else 'calculatable',
            'note': f'Need {5 - len(completed)} more completed trades to calculate accuracy'
        }

        # Technical Analyzer performance
        technical_scores = [p['agent_scores']['technical_score'] for p in predictions]
        performance['agents']['TechnicalAnalyzer'] = {
            'avg_score': round(sum(technical_scores) / len(technical_scores), 2),
            'avg_return': round(avg_return, 2),
            'accuracy': 'pending' if len(completed) < 5 else 'calculatable',
            'note': f'Need {5 - len(completed)} more completed trades to calculate accuracy'
        }

        # Ranking Engine performance
        ranks = [p['agent_scores']['original_rank'] for p in predictions]
        performance['agents']['RankingEngine'] = {
            'avg_rank': round(sum(ranks) / len(ranks), 2),
            'avg_return': round(avg_return, 2),
            'rank_effectiveness': 'pending' if len(completed) < 5 else 'calculatable',
            'note': f'Need {5 - len(completed)} more completed trades to validate rankings'
        }

    return performance

def main():
    """Main validation execution"""
    print("=" * 80)
    print("📊 PREDICTION VALIDATION - Agent Performance Tracking")
    print("=" * 80)
    print()

    # Load data
    tracking = load_predictions()
    market_data = load_market_data()

    print(f"📁 Loaded {len(tracking['predictions'])} predictions")
    print(f"📈 Market data from: {market_data.get('fetch_date', 'Unknown')}")
    print()

    # Update each prediction
    updated_count = 0
    for prediction in tracking['predictions']:
        if prediction['status'] != 'holding':
            continue  # Skip closed positions

        symbol = prediction['stock']
        current_price = get_current_price(symbol, market_data)

        if current_price is None:
            print(f"⏭️  Skipping {symbol} - no price data")
            continue

        # Calculate performance
        performance = calculate_performance(prediction, current_price)

        # Update prediction
        prediction['current_price_rm'] = current_price
        prediction['days_held'] = performance['days_held']
        prediction['actual_performance'].update(performance)
        prediction['last_updated'] = datetime.now().strftime('%Y-%m-%d')

        # Update milestone returns
        update_milestone_returns(prediction, performance)

        # Generate lessons
        prediction['lessons'] = generate_lessons(prediction, performance)

        # Print update
        print(f"✅ {symbol}:")
        print(f"   Entry: RM {prediction['entry_price_rm']:.2f} → Current: RM {current_price:.2f}")
        print(f"   Return: {performance['current_return_pct']:+.2f}% ({performance['days_held']} days)")
        print(f"   Peak: {performance['peak_return_pct']:+.2f}% | Drawdown: {performance['max_drawdown_pct']:+.2f}%")

        if prediction['lessons']:
            for lesson in prediction['lessons']:
                print(f"   {lesson}")

        updated_count += 1
        print()

    # Update portfolio summary
    active = [p for p in tracking['predictions'] if p['status'] == 'holding']
    closed = [p for p in tracking['predictions'] if p['status'] == 'closed']

    tracking['portfolio_summary'] = {
        'total_predictions': len(tracking['predictions']),
        'active_positions': len(active),
        'closed_positions': len(closed),
        'avg_return_active': round(sum(p['actual_performance']['current_return_pct'] for p in active) / len(active), 2) if active else 0,
        'avg_return_closed': round(sum(p['actual_performance']['final_return'] for p in closed) / len(closed), 2) if closed else None,
        'win_rate': round(len([p for p in closed if p['actual_performance']['final_return'] > 0]) / len(closed) * 100, 2) if closed else None,
        'last_validation': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Save updated tracking
    with open('predictions_tracking.json', 'w') as f:
        json.dump(tracking, f, indent=2)

    print(f"💾 Updated {updated_count} predictions")
    print()

    # Calculate agent performance
    agent_perf = calculate_agent_performance(tracking['predictions'])

    # Save agent performance report
    with open('reports/agent_performance.json', 'w') as f:
        json.dump(agent_perf, f, indent=2)

    print("=" * 80)
    print("📊 PORTFOLIO SUMMARY")
    print("=" * 80)
    print(f"Active Positions: {tracking['portfolio_summary']['active_positions']}")
    print(f"Closed Positions: {tracking['portfolio_summary']['closed_positions']}")
    print(f"Avg Return (Active): {tracking['portfolio_summary']['avg_return_active']:+.2f}%")
    if tracking['portfolio_summary']['win_rate']:
        print(f"Win Rate: {tracking['portfolio_summary']['win_rate']:.2f}%")
    print()

    print("=" * 80)
    print("🤖 AGENT PERFORMANCE")
    print("=" * 80)
    for agent_name, metrics in agent_perf['agents'].items():
        print(f"\n{agent_name}:")
        for key, value in metrics.items():
            if key != 'note':
                print(f"  {key}: {value}")
        if 'note' in metrics:
            print(f"  💡 {metrics['note']}")
    print()

    print("✅ Validation complete!")
    print("📄 Reports saved:")
    print("   - predictions_tracking.json (updated)")
    print("   - reports/agent_performance.json (created)")
    print()

if __name__ == "__main__":
    main()
