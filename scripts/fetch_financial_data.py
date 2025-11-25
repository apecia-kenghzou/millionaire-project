#!/usr/bin/env python3
"""
Automated Financial Data Fetcher for Malaysian Stocks
Uses FREE APIs to download quarterly and annual financial data

Data Sources:
1. yfinance - Free Yahoo Finance API (financial statements, quarterly data)
2. Direct scraping from Bursa Malaysia announcements (backup)

Usage:
    python3 scripts/fetch_financial_data.py --symbols PBBANK.KL,GASMSIA.KL,PENTA.KL
    python3 scripts/fetch_financial_data.py --file watchlists/priority.json

Output: data/financial_reports/{symbol}_financials.json
"""

import yfinance as yf
import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import time

class FinancialDataFetcher:
    """Fetches quarterly and annual financial data for Malaysian stocks"""

    def __init__(self, output_dir="data/financial_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_stock_financials(self, symbol):
        """
        Fetch comprehensive financial data for a stock

        Args:
            symbol: Stock symbol (e.g., PBBANK.KL, GASMSIA.KL)

        Returns:
            dict: Financial data including quarterly and annual reports
        """
        print(f"\n{'='*60}")
        print(f"Fetching financial data for: {symbol}")
        print(f"{'='*60}")

        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)

            # Get basic info
            info = ticker.info

            # Get financial statements
            print(f"  ✓ Downloading income statements...")
            income_stmt_annual = ticker.financials  # Annual income statement
            income_stmt_quarterly = ticker.quarterly_financials  # Quarterly

            print(f"  ✓ Downloading balance sheets...")
            balance_sheet_annual = ticker.balance_sheet  # Annual balance sheet
            balance_sheet_quarterly = ticker.quarterly_balance_sheet  # Quarterly

            print(f"  ✓ Downloading cash flow statements...")
            cashflow_annual = ticker.cashflow  # Annual cash flow
            cashflow_quarterly = ticker.quarterly_cashflow  # Quarterly

            # Get earnings data (quarterly earnings history)
            print(f"  ✓ Downloading earnings history...")
            earnings = ticker.earnings
            quarterly_earnings = ticker.quarterly_earnings

            # Compile data
            financial_data = {
                "symbol": symbol,
                "company_name": info.get('longName', symbol),
                "sector": info.get('sector', 'Unknown'),
                "industry": info.get('industry', 'Unknown'),
                "currency": info.get('currency', 'MYR'),
                "market_cap": info.get('marketCap', 0),
                "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_source": "Yahoo Finance API (yfinance)",

                # Annual Data
                "annual_income_statement": self._convert_df_to_dict(income_stmt_annual),
                "annual_balance_sheet": self._convert_df_to_dict(balance_sheet_annual),
                "annual_cashflow": self._convert_df_to_dict(cashflow_annual),
                "annual_earnings": self._convert_df_to_dict(earnings),

                # Quarterly Data
                "quarterly_income_statement": self._convert_df_to_dict(income_stmt_quarterly),
                "quarterly_balance_sheet": self._convert_df_to_dict(balance_sheet_quarterly),
                "quarterly_cashflow": self._convert_df_to_dict(cashflow_quarterly),
                "quarterly_earnings": self._convert_df_to_dict(quarterly_earnings),

                # Company Info (for reference)
                "company_info": {
                    "full_time_employees": info.get('fullTimeEmployees', 0),
                    "website": info.get('website', ''),
                    "description": info.get('longBusinessSummary', ''),
                    "exchange": info.get('exchange', 'KLSE'),
                    "quote_type": info.get('quoteType', 'EQUITY')
                },

                # Calculated Metrics (for quick access)
                "calculated_metrics": self._calculate_metrics(
                    income_stmt_annual,
                    balance_sheet_annual,
                    cashflow_annual,
                    quarterly_earnings
                )
            }

            # Save to file
            output_file = self.output_dir / f"{symbol.replace('.KL', '')}_financials.json"
            with open(output_file, 'w') as f:
                json.dump(financial_data, f, indent=2, default=str)

            print(f"  ✓ Saved to: {output_file}")
            print(f"  ✓ Annual statements: {len(income_stmt_annual.columns) if not income_stmt_annual.empty else 0} periods")
            print(f"  ✓ Quarterly statements: {len(income_stmt_quarterly.columns) if not income_stmt_quarterly.empty else 0} periods")

            return financial_data

        except Exception as e:
            print(f"  ✗ Error fetching {symbol}: {str(e)}")
            return None

    def _convert_df_to_dict(self, df):
        """Convert pandas DataFrame to JSON-serializable dict"""
        if df is None or df.empty:
            return {}

        # Convert DataFrame to dict with dates as strings
        result = {}
        for col in df.columns:
            date_str = col.strftime("%Y-%m-%d") if hasattr(col, 'strftime') else str(col)
            result[date_str] = {}
            for idx in df.index:
                value = df.loc[idx, col]
                # Handle NaN and infinity
                if hasattr(value, 'item'):  # numpy types
                    value = value.item()
                if value is None or (isinstance(value, float) and (value != value or value == float('inf') or value == float('-inf'))):
                    value = None
                result[date_str][str(idx)] = value

        return result

    def _calculate_metrics(self, income_stmt, balance_sheet, cashflow, quarterly_earnings):
        """Calculate common financial metrics"""
        metrics = {
            "calculated_date": datetime.now().strftime("%Y-%m-%d"),
            "metrics": {}
        }

        try:
            if not income_stmt.empty and not balance_sheet.empty:
                # Get most recent period
                latest_date = income_stmt.columns[0]

                # Revenue and Profitability
                revenue = income_stmt.loc['Total Revenue', latest_date] if 'Total Revenue' in income_stmt.index else 0
                net_income = income_stmt.loc['Net Income', latest_date] if 'Net Income' in income_stmt.index else 0

                # Balance Sheet items
                total_equity = balance_sheet.loc['Stockholders Equity', latest_date] if 'Stockholders Equity' in balance_sheet.index else 0
                total_debt = balance_sheet.loc['Total Debt', latest_date] if 'Total Debt' in balance_sheet.index else 0

                # Calculate metrics
                metrics["metrics"] = {
                    "latest_revenue": float(revenue) if revenue else 0,
                    "latest_net_income": float(net_income) if net_income else 0,
                    "net_profit_margin_pct": (float(net_income) / float(revenue) * 100) if revenue else 0,
                    "roe_pct": (float(net_income) / float(total_equity) * 100) if total_equity else 0,
                    "debt_to_equity": (float(total_debt) / float(total_equity)) if total_equity else 0,
                }

                # Revenue growth (if we have 2+ periods)
                if len(income_stmt.columns) >= 2:
                    prev_revenue = income_stmt.loc['Total Revenue', income_stmt.columns[1]] if 'Total Revenue' in income_stmt.index else 0
                    if prev_revenue:
                        growth = ((revenue - prev_revenue) / prev_revenue) * 100
                        metrics["metrics"]["yoy_revenue_growth_pct"] = float(growth)

                # Quarterly momentum (last 4 quarters)
                if not quarterly_earnings.empty and len(quarterly_earnings) >= 4:
                    last_4_earnings = quarterly_earnings.tail(4)['Earnings'].tolist() if 'Earnings' in quarterly_earnings.columns else []
                    if len(last_4_earnings) >= 2:
                        recent_trend = "improving" if last_4_earnings[-1] > last_4_earnings[-2] else "deteriorating"
                        metrics["metrics"]["quarterly_momentum"] = recent_trend
                        metrics["metrics"]["last_4_quarters_avg_earnings"] = sum(last_4_earnings) / len(last_4_earnings)

        except Exception as e:
            metrics["error"] = str(e)

        return metrics

    def fetch_multiple_stocks(self, symbols, delay=2):
        """
        Fetch financial data for multiple stocks

        Args:
            symbols: List of stock symbols
            delay: Delay between requests (seconds) to be respectful to API

        Returns:
            dict: Results for all symbols
        """
        results = {
            "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_symbols": len(symbols),
            "successful": 0,
            "failed": 0,
            "data": {}
        }

        for i, symbol in enumerate(symbols, 1):
            print(f"\n[{i}/{len(symbols)}] Processing {symbol}...")

            data = self.fetch_stock_financials(symbol)

            if data:
                results["data"][symbol] = "Success"
                results["successful"] += 1
            else:
                results["data"][symbol] = "Failed"
                results["failed"] += 1

            # Respectful delay between requests
            if i < len(symbols):
                print(f"  → Waiting {delay}s before next request...")
                time.sleep(delay)

        # Save summary
        summary_file = self.output_dir / "_fetch_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*60}")
        print(f"FETCH SUMMARY")
        print(f"{'='*60}")
        print(f"Total symbols: {results['total_symbols']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Summary saved to: {summary_file}")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Fetch financial data for Malaysian stocks using free APIs"
    )
    parser.add_argument(
        '--symbols',
        type=str,
        help='Comma-separated list of stock symbols (e.g., PBBANK.KL,GASMSIA.KL)'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='JSON file containing symbols (portfolio.json or watchlist)'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=2,
        help='Delay between requests in seconds (default: 2)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/financial_reports',
        help='Output directory for financial data (default: data/financial_reports)'
    )

    args = parser.parse_args()

    # Get symbols
    symbols = []

    if args.symbols:
        symbols = [s.strip() for s in args.symbols.split(',')]

    elif args.file:
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)

            # Extract symbols from different file formats
            if 'holdings' in data:  # portfolio.json
                symbols = [h['symbol'] for h in data['holdings']]
            elif 'companies' in data:  # watchlist format
                symbols = [c['symbol'] for c in data['companies']]
            elif isinstance(data, list):  # Simple list
                symbols = data

        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            sys.exit(1)

    else:
        print("Error: Must provide either --symbols or --file")
        parser.print_help()
        sys.exit(1)

    # Ensure .KL suffix
    symbols = [s if '.KL' in s else f"{s}.KL" for s in symbols]

    print(f"\n{'='*60}")
    print(f"FINANCIAL DATA FETCHER")
    print(f"{'='*60}")
    print(f"Symbols to fetch: {len(symbols)}")
    print(f"Symbols: {', '.join(symbols)}")
    print(f"Output directory: {args.output}")
    print(f"Delay between requests: {args.delay}s")

    # Fetch data
    fetcher = FinancialDataFetcher(output_dir=args.output)
    results = fetcher.fetch_multiple_stocks(symbols, delay=args.delay)

    print(f"\n✅ Done! Check {args.output}/ for results")


if __name__ == "__main__":
    main()
