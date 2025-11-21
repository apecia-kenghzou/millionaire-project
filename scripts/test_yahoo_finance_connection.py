#!/usr/bin/env python3
"""
Test Yahoo Finance Connection and Data Quality
===============================================

This script tests the connection to Yahoo Finance and validates
that all 14 Malaysian stock tickers are working correctly.

Quick test to ensure data pipeline is operational.

Usage:
    python3 scripts/test_yahoo_finance_connection.py

Expected Output:
    - All 14 stocks should show ✓ SUCCESS
    - Prices should match your KLSE app or broker platform
    - Takes ~30-60 seconds to run

Author: Share Analysis Expert System
Date: 2025-11-19
"""

import yfinance as yf
from datetime import datetime
import sys

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Test stock mapping
TEST_STOCKS = {
    'INARI': '0166.KL',
    'PBBANK': 'PBBANK.KL',
    'MAYBANK': '1155.KL',
    'UNISEM': '5005.KL',
    'PENTA': '7160.KL',
    'GREATEC': 'GREATEC.KL',
    'CIMB': '1023.KL',
    'HLBANK': '5819.KL',
    'TENAGA': '5347.KL',
    'PGAS': '6033.KL',
    'YTLPOWR': 'YTLPOWR.KL',
    'GASMSIA': '5209.KL',
    'VSOLAR': '0215.KL',
    'MAXIS': '6012.KL'
}

def test_ticker(name, symbol):
    """Test a single ticker and return status"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period='5d')  # Just last 5 days for quick test

        if df.empty:
            return False, "No data returned", None

        latest_price = df['Close'].iloc[-1]
        latest_date = df.index[-1].date()
        num_days = len(df)

        return True, f"RM{latest_price:.2f}", {
            'price': latest_price,
            'date': str(latest_date),
            'days': num_days
        }

    except Exception as e:
        return False, str(e)[:50], None

def print_header():
    """Print test header"""
    print()
    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}{BLUE}Yahoo Finance Connection Test{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Testing: {len(TEST_STOCKS)} Malaysian stocks")
    print(f"Purpose: Verify data pipeline operational")
    print('=' * 80)
    print()

def print_results(results):
    """Print test results in table format"""
    print()
    print(f"{BOLD}Results:{RESET}")
    print('-' * 80)
    print(f"{'Stock':<12} {'Yahoo Symbol':<15} {'Status':<10} {'Latest Price':<15}")
    print('-' * 80)

    success_count = 0

    for name, (status, message, data) in results.items():
        symbol = TEST_STOCKS[name]

        if status:
            status_text = f"{GREEN}✓ SUCCESS{RESET}"
            price_text = message
            success_count += 1
        else:
            status_text = f"{RED}✗ FAILED{RESET}"
            price_text = f"{RED}{message}{RESET}"

        print(f"{name:<12} {symbol:<15} {status_text:<20} {price_text:<15}")

    print('-' * 80)
    print()

    # Summary
    total = len(results)
    success_rate = (success_count / total) * 100

    if success_rate == 100:
        status_color = GREEN
        status_message = "ALL SYSTEMS OPERATIONAL"
    elif success_rate >= 80:
        status_color = YELLOW
        status_message = "MOSTLY OPERATIONAL"
    else:
        status_color = RED
        status_message = "SYSTEM ISSUES DETECTED"

    print(f"{BOLD}Summary:{RESET}")
    print(f"Success: {success_count}/{total} ({success_rate:.1f}%)")
    print(f"Status: {status_color}{BOLD}{status_message}{RESET}")
    print()

    # Price check reminder
    if success_count > 0:
        print(f"{YELLOW}⚠️  IMPORTANT:{RESET}")
        print("Compare these prices with your KLSE app or broker platform.")
        print("Prices should match within RM0.01-0.02 (minor timing differences OK).")
        print()

def main():
    """Main test execution"""
    print_header()

    print(f"{BLUE}Testing connections...{RESET}")
    print("(This will take 30-60 seconds)")
    print()

    results = {}

    for i, (name, symbol) in enumerate(TEST_STOCKS.items(), 1):
        print(f"[{i:2d}/14] Testing {name:<12} ({symbol:<15})... ", end='', flush=True)

        status, message, data = test_ticker(name, symbol)

        results[name] = (status, message, data)

        if status:
            print(f"{GREEN}✓ {message}{RESET}")
        else:
            print(f"{RED}✗ {message}{RESET}")

    print_results(results)

    # Exit code
    success_count = sum(1 for s, _, _ in results.values() if s)
    if success_count == len(TEST_STOCKS):
        print(f"{GREEN}{BOLD}✓ All tests passed! System ready for analysis.{RESET}")
        print()
        return 0
    elif success_count >= len(TEST_STOCKS) * 0.8:
        print(f"{YELLOW}{BOLD}⚠️  Some tests failed, but system mostly operational.{RESET}")
        print()
        return 1
    else:
        print(f"{RED}{BOLD}✗ Multiple failures detected. Check internet connection.{RESET}")
        print()
        return 2

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        print(f"{YELLOW}Test interrupted by user{RESET}")
        sys.exit(130)
    except Exception as e:
        print()
        print(f"{RED}{BOLD}Unexpected error: {e}{RESET}")
        sys.exit(1)
