#!/usr/bin/env python3
"""
Fetch Technical Data from Yahoo Finance
========================================

This script fetches real market data for Malaysian stocks from Yahoo Finance.
Used in Stage 4 (TechnicalAnalyzer) of the Share Analysis Expert System.

Author: Share Analysis Expert System
Date: 2025-11-19
Data Source: Yahoo Finance via yfinance library
Verified Against: KLSE app (user confirmed accuracy)

Requirements:
- yfinance==0.2.66
- pandas==2.3.3
- numpy==2.3.5

Usage:
    python3 scripts/fetch_technical_data.py

Output:
    sessions/session_001/temp_technical_data_complete.json
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import json
import sys
from pathlib import Path

# Malaysian stock ticker mapping
# Yahoo Finance uses 4-digit Bursa Malaysia codes with .KL suffix
STOCK_MAPPING = {
    'INARI.KL': '0166.KL',      # Inari Amertron Berhad
    'PBBANK.KL': 'PBBANK.KL',   # Public Bank Berhad (uses name)
    'MAYBANK.KL': '1155.KL',    # Malayan Banking Berhad
    'UNISEM.KL': '5005.KL',     # Unisem (M) Berhad
    'PENTA.KL': '7160.KL',      # Pentamaster Corporation Berhad
    'GREATEC.KL': 'GREATEC.KL', # Greatech Technology Berhad (uses name)
    'CIMB.KL': '1023.KL',       # CIMB Group Holdings Berhad
    'HLBANK.KL': '5819.KL',     # Hong Leong Bank Berhad
    'TENAGA.KL': '5347.KL',     # Tenaga Nasional Berhad
    'PGAS.KL': '6033.KL',       # Petronas Gas Berhad
    'YTLPOWR.KL': 'YTLPOWR.KL', # YTL Power (uses name)
    'GASMSIA.KL': '5209.KL',    # Gas Malaysia Berhad
    'VSOLAR.KL': '0215.KL',     # Vortex Solar Berhad
    'MAXIS.KL': '6012.KL'       # Maxis Berhad
}

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index (RSI)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def fetch_stock_data(standard_name, yahoo_symbol):
    """Fetch and calculate technical indicators for a stock"""
    try:
        print(f'Fetching {standard_name} ({yahoo_symbol})...')
        ticker = yf.Ticker(yahoo_symbol)

        # Get 1 year of daily data
        df = ticker.history(period='1y')

        if df.empty or len(df) < 50:
            print(f'  ✗ Insufficient data for {standard_name}')
            return None

        # Calculate Moving Averages
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['SMA200'] = df['Close'].rolling(window=200).mean()

        # Calculate RSI
        df['RSI'] = calculate_rsi(df['Close'])

        # Calculate MACD
        df['MACD'], df['Signal'], df['Histogram'] = calculate_macd(df['Close'])

        # Calculate Volume Average
        df['VolAvg20'] = df['Volume'].rolling(window=20).mean()

        # Get latest values
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) >= 2 else latest

        # Determine MACD status
        macd_current = latest['MACD']
        signal_current = latest['Signal']
        macd_prev = prev['MACD']
        signal_prev = prev['Signal']

        if pd.notna(macd_current) and pd.notna(signal_current):
            if macd_current > signal_current:
                macd_status = 'Bullish crossover' if macd_prev <= signal_prev else 'Bullish'
            else:
                macd_status = 'Bearish crossover' if macd_prev >= signal_prev else 'Bearish'
        else:
            macd_status = 'Neutral'

        # Determine trend
        close = latest['Close']
        sma20 = latest['SMA20']
        sma50 = latest['SMA50']
        sma200 = latest['SMA200']

        if pd.notna(sma20) and pd.notna(sma50) and pd.notna(sma200):
            if close > sma20 > sma50 > sma200:
                trend = 'Strong uptrend'
            elif close > sma20 and close > sma50:
                trend = 'Uptrend'
            elif close < sma20 < sma50 < sma200:
                trend = 'Strong downtrend'
            elif close < sma20 and close < sma50:
                trend = 'Downtrend'
            else:
                trend = 'Sideways/Mixed'
        else:
            trend = 'Insufficient data'

        # Compile results
        result = {
            'yahoo_symbol': yahoo_symbol,
            'date': str(latest.name.date()),
            'current_price_rm': round(float(latest['Close']), 3),
            'sma20': round(float(latest['SMA20']), 3) if pd.notna(latest['SMA20']) else None,
            'sma50': round(float(latest['SMA50']), 3) if pd.notna(latest['SMA50']) else None,
            'sma200': round(float(latest['SMA200']), 3) if pd.notna(latest['SMA200']) else None,
            'rsi_14': round(float(latest['RSI']), 2) if pd.notna(latest['RSI']) else None,
            'macd': round(float(latest['MACD']), 4) if pd.notna(latest['MACD']) else None,
            'signal_line': round(float(latest['Signal']), 4) if pd.notna(latest['Signal']) else None,
            'histogram': round(float(latest['Histogram']), 4) if pd.notna(latest['Histogram']) else None,
            'macd_status': macd_status,
            'trend': trend,
            'volume': int(latest['Volume']),
            'vol_avg_20d': int(latest['VolAvg20']) if pd.notna(latest['VolAvg20']) else None,
            'high_52w': round(float(df['Close'].max()), 3),
            'low_52w': round(float(df['Close'].min()), 3),
            'data_points': len(df)
        }

        print(f'  ✓ {standard_name}: RM{result["current_price_rm"]} | RSI: {result["rsi_14"]} | {trend}')
        return result

    except Exception as e:
        print(f'  ✗ {standard_name}: Error - {str(e)}')
        return None

def main():
    """Main execution function"""
    print('=' * 80)
    print('Fetching Real Market Data from Yahoo Finance')
    print('=' * 80)
    print(f'Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Stocks: {len(STOCK_MAPPING)}')
    print(f'Data Period: 1 year (252 trading days)')
    print('=' * 80)
    print()

    results = {}

    for standard_name, yahoo_symbol in STOCK_MAPPING.items():
        result = fetch_stock_data(standard_name, yahoo_symbol)
        results[standard_name] = result

    # Save results
    output_path = Path('sessions/session_001/temp_technical_data_complete.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    successful = len([r for r in results.values() if r is not None])

    print()
    print('=' * 80)
    print(f'✓ Successfully fetched {successful}/{len(STOCK_MAPPING)} stocks')
    print(f'✓ Data saved to: {output_path}')
    print('=' * 80)

    # Print summary statistics
    if successful > 0:
        print()
        print('Summary Statistics:')
        print('-' * 80)
        prices = [r['current_price_rm'] for r in results.values() if r]
        rsis = [r['rsi_14'] for r in results.values() if r and r['rsi_14']]

        print(f'Price Range: RM{min(prices):.2f} - RM{max(prices):.2f}')
        print(f'Average RSI: {sum(rsis)/len(rsis):.2f}')
        print(f'Extreme Oversold (RSI < 30): {len([r for r in rsis if r < 30])} stocks')
        print(f'Extreme Overbought (RSI > 70): {len([r for r in rsis if r > 70])} stocks')
        print('-' * 80)

    return 0 if successful == len(STOCK_MAPPING) else 1

if __name__ == '__main__':
    sys.exit(main())
