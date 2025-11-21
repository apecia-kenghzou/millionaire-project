// Stock Search Functionality

function searchStocks() {
    const query = document.getElementById('stock-search').value.trim();

    if (!query) {
        alert('Please enter a stock code or name to search');
        return;
    }

    const resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = '';

    // Search for matches
    const matches = findStockMatches(query);

    if (matches.length === 0) {
        resultsDiv.innerHTML = `
            <div style="padding: 2rem; text-align: center; color: #6c757d;">
                <h3>No results found for "${query}"</h3>
                <p>Try searching by:</p>
                <ul style="list-style: none; padding: 0; margin-top: 1rem;">
                    <li>• 4-digit code (e.g., 7160, 5209, 1155)</li>
                    <li>• Stock symbol (e.g., PENTA, PBBANK, GASMSIA)</li>
                    <li>• Company name (e.g., Pentamaster, Public Bank)</li>
                </ul>
            </div>
        `;
        return;
    }

    // Display results
    matches.forEach(stock => {
        const card = createSearchResultCard(stock);
        resultsDiv.appendChild(card);
    });
}

function findStockMatches(query) {
    const q = query.toUpperCase().trim();
    const matches = [];
    const stocks = getAllStocks();

    stocks.forEach(stock => {
        const symbol = stock.symbol.replace('.KL', '');
        const companyName = (stock.company_name || getStockName(stock.symbol)).toUpperCase();

        // Check if query matches
        let score = 0;

        // Exact symbol match
        if (symbol === q) score += 100;
        // Symbol contains query
        else if (symbol.includes(q)) score += 50;
        // Company name starts with query
        else if (companyName.startsWith(q)) score += 75;
        // Company name contains query
        else if (companyName.includes(q)) score += 25;

        // Check 4-digit code match
        const fourDigit = symbol.match(/\d+/);
        if (fourDigit && fourDigit[0] === q) score += 100;

        if (score > 0) {
            matches.push({ stock, score });
        }
    });

    // Sort by score (highest first)
    matches.sort((a, b) => b.score - a.score);

    return matches.map(m => m.stock);
}

function createSearchResultCard(stock) {
    const card = document.createElement('div');
    card.className = 'search-result-card';
    card.onclick = () => showStockDetail(stock.symbol.replace('.KL', ''));

    const symbol = stock.symbol.replace('.KL', '');
    const companyName = stock.company_name || getStockName(stock.symbol);
    const price = stock.current_price_rm;
    const rsi = stock.technical_indicators?.rsi_14 || stock.rsi_14;
    const action = stock.action_recommendation || 'WATCH';

    // Determine action color
    let actionColor = '#6c757d';
    if (action.includes('BUY NOW')) actionColor = '#28a745';
    else if (action.includes('SCALE')) actionColor = '#ffc107';
    else if (action.includes('WAIT')) actionColor = '#dc3545';

    // Priority badge
    let priorityBadge = '';
    if (symbol === 'PENTA' && rsi < 35) {
        priorityBadge = '<span style="background: linear-gradient(90deg, #ff6b6b, #ee5a24); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;">🔥 Priority #1</span>';
    } else if (symbol === 'GASMSIA' && rsi < 35) {
        priorityBadge = '<span style="background: linear-gradient(90deg, #ffd93d, #ff9a00); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;">💰 Priority #2</span>';
    } else if (symbol === 'PBBANK') {
        priorityBadge = '<span style="background: linear-gradient(90deg, #4facfe, #00f2fe); color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;">⭐ Priority #3</span>';
    }

    card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.8rem;">
            <div>
                <h3 style="margin: 0 0 0.3rem 0; font-size: 1.3rem; color: #007bff;">${symbol}</h3>
                <p style="margin: 0; color: #6c757d; font-size: 0.9rem;">${companyName}</p>
            </div>
            ${priorityBadge}
        </div>

        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.8rem; margin-bottom: 1rem;">
            <div>
                <span style="font-size: 0.8rem; color: #6c757d;">Price</span>
                <div style="font-size: 1.3rem; font-weight: 700; color: #212529;">
                    ${price ? `RM ${price.toFixed(2)}` : '-'}
                </div>
            </div>
            <div>
                <span style="font-size: 0.8rem; color: #6c757d;">RSI</span>
                <div style="font-size: 1.3rem; font-weight: 700; color: ${rsi < 30 ? '#28a745' : rsi > 70 ? '#dc3545' : '#212529'};">
                    ${rsi ? rsi.toFixed(1) : '-'}
                </div>
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.9rem; font-weight: 600; color: ${actionColor};">
                ${action}
            </span>
            <span style="font-size: 0.85rem; color: #007bff; font-weight: 600;">
                View Details →
            </span>
        </div>
    `;

    return card;
}

// Allow search on Enter key
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('stock-search');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchStocks();
            }
        });
    }
});
