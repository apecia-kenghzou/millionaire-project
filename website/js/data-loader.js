// Data Loader - Load all JSON data files
let highReturnData = null;
let marketData = null;
let moneyFlowData = null;
let watchlistData = null;

// Stock code to symbol mapping
const STOCK_MAPPING = {
    // By 4-digit code
    '7160': 'PENTA.KL',
    '0166': 'INARI.KL',
    '5005': 'UNISEM.KL',
    '1155': 'MAYBANK.KL',
    '1023': 'CIMB.KL',
    '5819': 'HLBANK.KL',
    '6012': 'MAXIS.KL',
    '6033': 'PGAS.KL',
    '5209': 'GASMSIA.KL',
    '5347': 'TENAGA.KL',
    '0215': 'VSOLAR.KL',

    // By symbol
    'PBBANK': 'PBBANK.KL',
    'MAYBANK': 'MAYBANK.KL',
    'CIMB': 'CIMB.KL',
    'HLBANK': 'HLBANK.KL',
    'MAXIS': 'MAXIS.KL',
    'PENTA': 'PENTA.KL',
    'INARI': 'INARI.KL',
    'UNISEM': 'UNISEM.KL',
    'GREATEC': 'GREATEC.KL',
    'PGAS': 'PGAS.KL',
    'GASMSIA': 'GASMSIA.KL',
    'TENAGA': 'TENAGA.KL',
    'YTLPOWR': 'YTLPOWR.KL',
    'VSOLAR': 'VSOLAR.KL'
};

// Company name mapping
const COMPANY_NAMES = {
    'PBBANK.KL': 'Public Bank Berhad',
    'MAYBANK.KL': 'Malayan Banking Berhad',
    'CIMB.KL': 'CIMB Group Holdings',
    'HLBANK.KL': 'Hong Leong Bank',
    'MAXIS.KL': 'Maxis Berhad',
    'PENTA.KL': 'Pentamaster Corporation',
    'INARI.KL': 'Inari Amertron Berhad',
    'UNISEM.KL': 'Unisem (M) Berhad',
    'GREATEC.KL': 'Greatech Technology',
    'PGAS.KL': 'Petronas Gas Berhad',
    'GASMSIA.KL': 'Gas Malaysia Berhad',
    'TENAGA.KL': 'Tenaga Nasional Berhad',
    'YTLPOWR.KL': 'YTL Power International',
    'VSOLAR.KL': 'Vortex Solar Berhad'
};

// Load all data files
async function loadAllData() {
    try {
        const [highReturnRes, marketRes, moneyFlowRes, watchlistRes] = await Promise.all([
            fetch('data/high_return_companies.json'),
            fetch('data/current_market_data.json'),
            fetch('data/market_money_flow.json'),
            fetch('data/active_watchlist.json')
        ]);

        highReturnData = await highReturnRes.json();
        marketData = await marketRes.json();
        moneyFlowData = await moneyFlowRes.json();
        watchlistData = await watchlistRes.json();

        console.log('All data loaded successfully');

        // Initialize the dashboard
        initDashboard();
    } catch (error) {
        console.error('Error loading data:', error);
        alert('Error loading data files. Please ensure all JSON files are in the data/ folder.');
    }
}

// Initialize dashboard after data is loaded
function initDashboard() {
    // Populate stocks table
    populateStocksTable();

    // Initialize Sankey diagram
    if (typeof initSankey === 'function') {
        initSankey();
    }

    console.log('Dashboard initialized');
}

// Get stock by symbol
function getStockBySymbol(symbol) {
    // Check in high return companies
    const highReturnStock = highReturnData?.high_return_companies?.find(s => s.symbol === symbol);
    if (highReturnStock) return highReturnStock;

    // Check in market data
    const marketStock = marketData?.stocks?.find(s => s.symbol === symbol);
    if (marketStock) return marketStock;

    return null;
}

// Get all stocks combined
function getAllStocks() {
    const stocks = [];
    const symbols = new Set();

    // Add high return companies first
    if (highReturnData?.high_return_companies) {
        highReturnData.high_return_companies.forEach(stock => {
            stocks.push({
                ...stock,
                isHighReturn: true
            });
            symbols.add(stock.symbol);
        });
    }

    // Add remaining stocks from market data
    if (marketData?.stocks) {
        marketData.stocks.forEach(stock => {
            if (!symbols.has(stock.symbol)) {
                stocks.push({
                    ...stock,
                    isHighReturn: false,
                    action_recommendation: determineAction(stock)
                });
            }
        });
    }

    return stocks;
}

// Determine action for non-high-return stocks
function determineAction(stock) {
    const rsi = stock.rsi_14;

    if (rsi < 25) return 'WAIT';
    if (rsi > 70) return 'WAIT';
    if (rsi >= 30 && rsi <= 40) return 'SCALE IN';
    if (rsi > 40 && rsi < 70) return 'WAIT';

    return 'WATCH';
}

// Get stock name from symbol
function getStockName(symbol) {
    return COMPANY_NAMES[symbol] || symbol;
}

// Resolve symbol from code or name
function resolveSymbol(query) {
    const q = query.toUpperCase().trim();

    // Check direct mapping
    if (STOCK_MAPPING[q]) {
        return STOCK_MAPPING[q];
    }

    // Check if already a valid symbol
    if (COMPANY_NAMES[q]) {
        return q;
    }

    // Check partial matches in company names
    for (const [symbol, name] of Object.entries(COMPANY_NAMES)) {
        if (name.toUpperCase().includes(q) || symbol.toUpperCase().includes(q)) {
            return symbol;
        }
    }

    return null;
}

// Load data on page load
document.addEventListener('DOMContentLoaded', loadAllData);
