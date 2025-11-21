#!/usr/bin/env python3
"""
Daily Stock Data Fetcher
========================

Fetches real-time market data from Yahoo Finance for all tracked stocks.
Saves data to JSON files for analysis pipeline.

Usage:
    python3 scripts/daily_data_fetcher.py [--date YYYY-MM-DD]

Author: Share Analysis Expert System
Date: 2025-11-21
"""

import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import sys

# Configuration
STOCKS = {
    # Technology Sector
    "INARI": "0166.KL",
    "UNISEM": "5005.KL",
    "PENTA": "7160.KL",
    "GREATEC": "GREATEC.KL",

    # Finance Sector
    "PBBANK": "PBBANK.KL",
    "MAYBANK": "1155.KL",
    "CIMB": "1023.KL",
    "HLBANK": "5819.KL",
    "MAXIS": "6012.KL",

    # Utilities Sector
    "PGAS": "6033.KL",
    "VSOLAR": "0215.KL",
    "GASMSIA": "5209.KL",
    "TENAGA": "5347.KL",
    "YTLPOWR": "YTLPOWR.KL"
}

SECTOR_MAPPING = {
    "INARI": "Technology",
    "UNISEM": "Technology",
    "PENTA": "Technology",
    "GREATEC": "Technology",
    "PBBANK": "Finance",
    "MAYBANK": "Finance",
    "CIMB": "Finance",
    "HLBANK": "Finance",
    "MAXIS": "Finance",
    "PGAS": "Utilities",
    "VSOLAR": "Utilities",
    "GASMSIA": "Utilities",
    "TENAGA": "Utilities",
    "YTLPOWR": "Utilities"
}


def calculate_rsi(prices, period=14):
    """Calculate RSI (Relative Strength Index)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "macd": round(macd_line.iloc[-1], 4),
        "signal": round(signal_line.iloc[-1], 4),
        "histogram": round(histogram.iloc[-1], 4)
    }


def calculate_sma(prices, period):
    """Calculate Simple Moving Average"""
    return prices.rolling(window=period).mean().iloc[-1]


def fetch_stock_data(symbol, yahoo_symbol, period="1y"):
    """Fetch comprehensive stock data from Yahoo Finance"""
    try:
        print(f"  Fetching {symbol} ({yahoo_symbol})...", end=" ")

        stock = yf.Ticker(yahoo_symbol)
        hist = stock.history(period=period)

        if hist.empty:
            print("❌ No data")
            return None

        current_price = hist['Close'].iloc[-1]

        # Calculate technical indicators
        rsi_14 = calculate_rsi(hist['Close'], 14)
        macd_data = calculate_macd(hist['Close'])
        sma_20 = calculate_sma(hist['Close'], 20)
        sma_50 = calculate_sma(hist['Close'], 50)
        sma_200 = calculate_sma(hist['Close'], 200)

        # Price data
        high_52w = hist['High'].max()
        low_52w = hist['Low'].min()
        avg_volume_20d = hist['Volume'].tail(20).mean()
        current_volume = hist['Volume'].iloc[-1]

        data = {
            "symbol": symbol,
            "yahoo_symbol": yahoo_symbol,
            "sector": SECTOR_MAPPING.get(symbol, "Unknown"),
            "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_price_rm": round(current_price, 2),
            "price_data": {
                "current_price_rm": round(current_price, 2),
                "sma_20": round(sma_20, 3),
                "sma_50": round(sma_50, 3),
                "sma_200": round(sma_200, 3),
                "high_52w": round(high_52w, 2),
                "low_52w": round(low_52w, 2),
                "distance_from_52w_high_percent": round(((current_price - high_52w) / high_52w) * 100, 1),
                "distance_from_52w_low_percent": round(((current_price - low_52w) / low_52w) * 100, 1)
            },
            "momentum_indicators": {
                "rsi_14": round(rsi_14, 2),
                "rsi_interpretation": get_rsi_interpretation(rsi_14),
                "macd": macd_data["macd"],
                "signal_line": macd_data["signal"],
                "histogram": macd_data["histogram"],
                "macd_status": "Bullish" if macd_data["macd"] > macd_data["signal"] else "Bearish"
            },
            "volume_analysis": {
                "current_volume": int(current_volume),
                "avg_volume_20d": int(avg_volume_20d),
                "volume_ratio": round(current_volume / avg_volume_20d, 2)
            },
            "trend_analysis": {
                "price_vs_sma20": "Above" if current_price > sma_20 else "Below",
                "price_vs_sma50": "Above" if current_price > sma_50 else "Below",
                "price_vs_sma200": "Above" if current_price > sma_200 else "Below"
            }
        }

        print(f"✅ RM {current_price:.2f} | RSI {rsi_14:.1f}")
        return data

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def get_rsi_interpretation(rsi):
    """Get RSI interpretation"""
    if rsi < 10:
        return "EXTREME oversold - capitulation level"
    elif rsi < 30:
        return "Oversold - potential buying opportunity"
    elif rsi < 40:
        return "Neutral to slightly bearish"
    elif rsi < 60:
        return "Neutral - balanced momentum"
    elif rsi < 70:
        return "Neutral to slightly bullish"
    elif rsi < 80:
        return "Overbought - caution warranted"
    else:
        return "EXTREME overbought - correction risk HIGH"


def save_data(data_list, date_str):
    """Save fetched data to JSON file"""
    # Create directory structure
    output_dir = Path(f"analysis/{date_str}/data")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save complete data
    output_file = output_dir / "market_data.json"

    output = {
        "fetch_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_stocks": len(data_list),
        "data_source": "Yahoo Finance (yfinance library)",
        "stocks": data_list
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n💾 Data saved to: {output_file}")

    # Also save to a fixed location that Claude can easily read
    fixed_output_file = Path("current_market_data.json")
    with open(fixed_output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"💾 Data also saved to: {fixed_output_file} (for Claude to read)")

    return output_file


def generate_summary(data_list):
    """Generate summary statistics"""
    print("\n" + "="*70)
    print("📊 MARKET DATA SUMMARY")
    print("="*70)

    by_sector = {}
    for stock in data_list:
        sector = stock["sector"]
        if sector not in by_sector:
            by_sector[sector] = []
        by_sector[sector].append(stock)

    for sector, stocks in by_sector.items():
        print(f"\n{sector} Sector ({len(stocks)} stocks):")
        for stock in stocks:
            price = stock["current_price_rm"]
            rsi = stock["momentum_indicators"]["rsi_14"]
            macd_status = stock["momentum_indicators"]["macd_status"]

            # Color code RSI
            if rsi < 10:
                rsi_emoji = "🔴"
            elif rsi < 30:
                rsi_emoji = "🟠"
            elif rsi > 80:
                rsi_emoji = "🟣"
            elif rsi > 70:
                rsi_emoji = "🔵"
            else:
                rsi_emoji = "🟢"

            print(f"  {stock['symbol']:10} RM {price:6.2f} | RSI {rsi:5.1f} {rsi_emoji} | {macd_status}")

    # Statistics
    all_rsi = [s["momentum_indicators"]["rsi_14"] for s in data_list]
    avg_rsi = sum(all_rsi) / len(all_rsi)

    print(f"\n{'='*70}")
    print(f"Average RSI: {avg_rsi:.1f}")
    print(f"Extreme Oversold (RSI < 10): {len([r for r in all_rsi if r < 10])} stocks")
    print(f"Oversold (RSI < 30): {len([r for r in all_rsi if r < 30])} stocks")
    print(f"Overbought (RSI > 70): {len([r for r in all_rsi if r > 70])} stocks")
    print(f"Extreme Overbought (RSI > 80): {len([r for r in all_rsi if r > 80])} stocks")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch daily stock market data")
    parser.add_argument("--date", help="Date for analysis (YYYY-MM-DD), default: today",
                       default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()

    print("=" * 70)
    print("📈 DAILY STOCK DATA FETCHER")
    print("=" * 70)
    print(f"Date: {args.date}")
    print(f"Stocks to fetch: {len(STOCKS)}")
    print(f"Data source: Yahoo Finance")
    print("=" * 70)

    # Fetch data for all stocks
    data_list = []
    success_count = 0

    for symbol, yahoo_symbol in STOCKS.items():
        data = fetch_stock_data(symbol, yahoo_symbol)
        if data:
            data_list.append(data)
            success_count += 1

    print(f"\n{'='*70}")
    print(f"✅ Successfully fetched: {success_count}/{len(STOCKS)} stocks")
    print(f"{'='*70}")

    if data_list:
        # Save data
        output_file = save_data(data_list, args.date)

        # Generate summary
        generate_summary(data_list)

        print(f"✅ Data collection complete!")
        print(f"📁 Output file: {output_file}")
        print(f"\n💡 Next step: Run analysis agents to generate stock reports")

        return 0
    else:
        print("❌ No data fetched. Please check your internet connection.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
