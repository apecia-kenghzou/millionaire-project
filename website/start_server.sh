#!/bin/bash

# Millionaire Dashboard - Local Server Launcher

echo "======================================================================"
echo "💰 MILLIONAIRE STOCK DASHBOARD"
echo "======================================================================"
echo ""
echo "Starting local web server..."
echo ""
echo "🌐 Dashboard will be available at: http://localhost:8000"
echo ""
echo "Features:"
echo "  ✅ Top 3 High-Return Opportunities (PENTA 🔥, GASMSIA 💰, PBBANK ⭐)"
echo "  ✅ Market Money Flow Visualization (Sankey Diagram)"
echo "  ✅ Stock Search (4-digit code + Company name)"
echo "  ✅ Sortable/Filterable Table (14 stocks)"
echo "  ✅ Detailed Stock Analysis Modal"
echo ""
echo "======================================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "======================================================================"
echo ""

# Change to website directory
cd "$(dirname "$0")"

# Start Python HTTP server
python3 -m http.server 8000
