// Stocks Table - Sortable and Filterable

let allStocksData = [];
let currentSort = { column: 0, ascending: false }; // Default sort by rank descending

function populateStocksTable() {
    allStocksData = getAllStocks();

    // Sort by rank by default
    allStocksData.sort((a, b) => {
        const rankA = a.rank || 999;
        const rankB = b.rank || 999;
        return rankA - rankB;
    });

    renderTable(allStocksData);
}

function renderTable(stocks) {
    const tbody = document.getElementById('stocks-tbody');
    tbody.innerHTML = '';

    stocks.forEach((stock, index) => {
        const row = tbody.insertRow();
        row.onclick = () => showStockDetail(stock.symbol.replace('.KL', ''));

        // Rank
        const rankCell = row.insertCell();
        rankCell.textContent = stock.rank || '-';
        rankCell.style.textAlign = 'center';
        rankCell.style.fontWeight = stock.rank <= 3 ? '700' : '500';

        // Symbol
        const symbolCell = row.insertCell();
        symbolCell.textContent = stock.symbol.replace('.KL', '');
        symbolCell.style.fontWeight = '600';
        symbolCell.style.color = '#007bff';

        // Company
        const companyCell = row.insertCell();
        companyCell.textContent = stock.company_name || getStockName(stock.symbol);

        // Sector
        const sectorCell = row.insertCell();
        sectorCell.textContent = stock.sector || '-';
        const sectorColor = stock.sector === 'Technology' ? '#17a2b8' :
                            stock.sector === 'Finance' ? '#007bff' :
                            stock.sector === 'Utilities' ? '#6f42c1' : '#6c757d';
        sectorCell.style.color = sectorColor;
        sectorCell.style.fontWeight = '500';

        // Composite Score
        const scoreCell = row.insertCell();
        scoreCell.textContent = stock.composite_score ? stock.composite_score.toFixed(2) : '-';
        scoreCell.style.textAlign = 'center';
        scoreCell.style.fontWeight = '600';
        if (stock.composite_score >= 7.5) {
            scoreCell.style.color = '#28a745';
        } else if (stock.composite_score >= 7.0) {
            scoreCell.style.color = '#ffc107';
        }

        // Price
        const priceCell = row.insertCell();
        priceCell.textContent = stock.current_price_rm ?
            `RM ${stock.current_price_rm.toFixed(2)}` : '-';
        priceCell.style.textAlign = 'right';
        priceCell.style.fontWeight = '600';

        // RSI
        const rsiCell = row.insertCell();
        const rsi = stock.technical_indicators?.rsi_14 || stock.rsi_14;
        rsiCell.textContent = rsi ? rsi.toFixed(1) : '-';
        rsiCell.style.textAlign = 'center';
        rsiCell.style.fontWeight = '600';

        // Color RSI based on level
        if (rsi) {
            if (rsi < 30) {
                rsiCell.style.color = '#28a745'; // Green - oversold
                rsiCell.style.background = '#d4edda';
            } else if (rsi > 70) {
                rsiCell.style.color = '#dc3545'; // Red - overbought
                rsiCell.style.background = '#f8d7da';
            } else {
                rsiCell.style.color = '#212529';
            }
        }

        // Action
        const actionCell = row.insertCell();
        const action = stock.action_recommendation || 'WATCH';
        const actionBadge = document.createElement('span');
        actionBadge.className = 'action-badge';
        actionBadge.textContent = action;

        if (action.includes('BUY NOW')) {
            actionBadge.classList.add('action-buy');
        } else if (action.includes('SCALE')) {
            actionBadge.classList.add('action-scale');
        } else {
            actionBadge.classList.add('action-wait');
        }

        actionCell.appendChild(actionBadge);
        actionCell.style.textAlign = 'center';

        // Expected Return
        const returnCell = row.insertCell();
        const expectedReturn = stock.expected_return_12m;
        if (expectedReturn && expectedReturn.base_case) {
            returnCell.textContent = expectedReturn.base_case;
        } else {
            returnCell.textContent = '-';
        }
        returnCell.style.textAlign = 'center';
        returnCell.style.fontWeight = '600';
        returnCell.style.color = '#28a745';

        // Allocation
        const allocationCell = row.insertCell();
        if (stock.portfolio_allocation_percent) {
            allocationCell.textContent = `${stock.portfolio_allocation_percent}% (RM ${stock.portfolio_allocation_rm?.toLocaleString()})`;
        } else {
            allocationCell.textContent = '-';
        }
        allocationCell.style.textAlign = 'right';
        allocationCell.style.fontSize = '0.9rem';
    });
}

function sortTable(columnIndex) {
    // Toggle sort direction if same column
    if (currentSort.column === columnIndex) {
        currentSort.ascending = !currentSort.ascending;
    } else {
        currentSort.column = columnIndex;
        currentSort.ascending = false;
    }

    const direction = currentSort.ascending ? 1 : -1;

    allStocksData.sort((a, b) => {
        let valA, valB;

        switch (columnIndex) {
            case 0: // Rank
                valA = a.rank || 999;
                valB = b.rank || 999;
                break;
            case 1: // Symbol
                valA = a.symbol;
                valB = b.symbol;
                break;
            case 2: // Company
                valA = a.company_name || getStockName(a.symbol);
                valB = b.company_name || getStockName(b.symbol);
                break;
            case 3: // Sector
                valA = a.sector || '';
                valB = b.sector || '';
                break;
            case 4: // Score
                valA = a.composite_score || 0;
                valB = b.composite_score || 0;
                break;
            case 5: // Price
                valA = a.current_price_rm || 0;
                valB = b.current_price_rm || 0;
                break;
            case 6: // RSI
                valA = a.technical_indicators?.rsi_14 || a.rsi_14 || 0;
                valB = b.technical_indicators?.rsi_14 || b.rsi_14 || 0;
                break;
            case 7: // Action
                valA = a.action_recommendation || 'WATCH';
                valB = b.action_recommendation || 'WATCH';
                break;
            case 8: // Expected Return
                valA = parseFloat((a.expected_return_12m?.base_case || '0%').replace('%', ''));
                valB = parseFloat((b.expected_return_12m?.base_case || '0%').replace('%', ''));
                break;
            case 9: // Allocation
                valA = a.portfolio_allocation_percent || 0;
                valB = b.portfolio_allocation_percent || 0;
                break;
            default:
                return 0;
        }

        if (typeof valA === 'string') {
            return direction * valA.localeCompare(valB);
        }
        return direction * (valA - valB);
    });

    renderTable(allStocksData);

    // Update table header to show sort direction
    const headers = document.querySelectorAll('#stocks-table th');
    headers.forEach((header, index) => {
        header.style.position = 'relative';
        const arrow = header.querySelector('.sort-arrow');
        if (arrow) arrow.remove();

        if (index === columnIndex) {
            const sortArrow = document.createElement('span');
            sortArrow.className = 'sort-arrow';
            sortArrow.textContent = currentSort.ascending ? ' ▲' : ' ▼';
            header.appendChild(sortArrow);
        }
    });
}

function filterTable() {
    const sectorFilter = document.getElementById('sector-filter').value;
    const actionFilter = document.getElementById('action-filter').value;

    let filteredStocks = [...allStocksData];

    // Filter by sector
    if (sectorFilter !== 'all') {
        filteredStocks = filteredStocks.filter(stock => stock.sector === sectorFilter);
    }

    // Filter by action
    if (actionFilter !== 'all') {
        filteredStocks = filteredStocks.filter(stock => {
            const action = stock.action_recommendation || 'WATCH';
            if (actionFilter === 'BUY NOW') {
                return action.includes('BUY NOW');
            } else if (actionFilter === 'SCALE IN') {
                return action.includes('SCALE');
            } else if (actionFilter === 'WAIT') {
                return action.includes('WAIT') && !action.includes('BUY');
            }
            return true;
        });
    }

    renderTable(filteredStocks);
}
