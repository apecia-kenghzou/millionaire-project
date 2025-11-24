// Portfolio Tracking Visualization

let portfolioData = null;

// Load portfolio data
async function loadPortfolioData() {
    try {
        // Add cache-busting timestamp to force fresh data
        const timestamp = new Date().getTime();
        const response = await fetch(`data/portfolio.json?t=${timestamp}`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        portfolioData = await response.json();
        console.log('Portfolio data loaded:', portfolioData);
        renderPortfolio();
    } catch (error) {
        console.error('Error loading portfolio data:', error);
        showErrorMessage('Failed to load portfolio data. Please refresh the page.');
    }
}

function renderPortfolio() {
    if (!portfolioData) {
        console.error('Portfolio data not loaded');
        return;
    }

    console.log('Rendering portfolio with', portfolioData.holdings.length, 'holdings');
    renderPortfolioSummary();
    renderHoldingsTable();
    renderPerformanceChart();
    renderTransactionHistory();
}

function showErrorMessage(message) {
    const summaryEl = document.getElementById('portfolio-summary');
    if (summaryEl) {
        summaryEl.innerHTML = `
            <div style="padding: 2rem; text-align: center; background: #fee; border-radius: 10px; color: #c33;">
                <h3>❌ Error</h3>
                <p>${message}</p>
            </div>
        `;
    }
}

function renderPortfolioSummary() {
    const capital = portfolioData.capital;
    const perf = portfolioData.performance_summary;

    const summaryHTML = `
        <div class="portfolio-summary-cards">
            <div class="portfolio-card">
                <div class="card-header">
                    <h3>💰 Total Portfolio Value</h3>
                </div>
                <div class="card-value-large">RM ${capital.total_portfolio_value_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</div>
                <div class="card-breakdown">
                    <div class="breakdown-item">
                        <span class="label">Cash:</span>
                        <span class="value">RM ${capital.current_cash_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</span>
                    </div>
                    <div class="breakdown-item">
                        <span class="label">Invested:</span>
                        <span class="value">RM ${capital.total_invested_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</span>
                    </div>
                </div>
            </div>

            <div class="portfolio-card ${capital.total_paper_gain_loss_rm >= 0 ? 'positive' : 'negative'}">
                <div class="card-header">
                    <h3>📊 Paper Gain/Loss</h3>
                </div>
                <div class="card-value-large ${capital.total_paper_gain_loss_rm >= 0 ? 'gain' : 'loss'}">
                    RM ${capital.total_paper_gain_loss_rm >= 0 ? '+' : ''}${capital.total_paper_gain_loss_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}
                </div>
                <div class="card-percentage ${capital.total_paper_gain_loss_percent >= 0 ? 'gain' : 'loss'}">
                    ${capital.total_paper_gain_loss_percent >= 0 ? '+' : ''}${capital.total_paper_gain_loss_percent.toFixed(2)}%
                </div>
            </div>

            <div class="portfolio-card">
                <div class="card-header">
                    <h3>🎯 Performance</h3>
                </div>
                <div class="performance-stats">
                    <div class="stat-item">
                        <span class="stat-label">Days Tracked:</span>
                        <span class="stat-value">${perf.days_tracked}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Win Rate:</span>
                        <span class="stat-value">${perf.win_rate.toFixed(2)}%</span>
                    </div>
                    ${perf.best_performer ? `
                    <div class="stat-item">
                        <span class="stat-label">Best:</span>
                        <span class="stat-value gain">${perf.best_performer.symbol.replace('.KL', '')} (${perf.best_performer.gain_loss_percent >= 0 ? '+' : ''}${perf.best_performer.gain_loss_percent.toFixed(2)}%)</span>
                    </div>
                    ` : ''}
                    ${perf.worst_performer ? `
                    <div class="stat-item">
                        <span class="stat-label">Worst:</span>
                        <span class="stat-value loss">${perf.worst_performer.symbol.replace('.KL', '')} (${perf.worst_performer.gain_loss_percent >= 0 ? '+' : ''}${perf.worst_performer.gain_loss_percent.toFixed(2)}%)</span>
                    </div>
                    ` : ''}
                </div>
            </div>

            <div class="portfolio-card">
                <div class="card-header">
                    <h3>📈 Capital Overview</h3>
                </div>
                <div class="capital-breakdown">
                    <div class="capital-item">
                        <span class="label">Initial:</span>
                        <span class="value">RM ${capital.initial_capital_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</span>
                    </div>
                    <div class="capital-item">
                        <span class="label">Current:</span>
                        <span class="value">RM ${capital.total_portfolio_value_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</span>
                    </div>
                    <div class="capital-item gain-loss">
                        <span class="label">Return:</span>
                        <span class="value ${(capital.total_portfolio_value_rm - capital.initial_capital_rm) >= 0 ? 'gain' : 'loss'}">
                            RM ${((capital.total_portfolio_value_rm - capital.initial_capital_rm) >= 0 ? '+' : '')}${(capital.total_portfolio_value_rm - capital.initial_capital_rm).toLocaleString('en-MY', {minimumFractionDigits: 2})}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    `;

    const container = document.getElementById('portfolio-summary');
    if (container) {
        container.innerHTML = summaryHTML;
    }
}

function renderHoldingsTable() {
    const holdings = portfolioData.holdings || [];

    if (holdings.length === 0) {
        const container = document.getElementById('holdings-table');
        if (container) {
            container.innerHTML = `
                <div class="no-holdings">
                    <h3>No Holdings Yet</h3>
                    <p>Execute Day 1 trades to start tracking your portfolio!</p>
                    <code>python3 scripts/execute_day1_buys.py</code>
                </div>
            `;
        }
        return;
    }

    let tableHTML = `
        <table class="holdings-table">
            <thead>
                <tr>
                    <th>Stock</th>
                    <th>Shares</th>
                    <th>Purchase Price</th>
                    <th>Current Price</th>
                    <th>Purchase Value</th>
                    <th>Current Value</th>
                    <th>P/L (RM)</th>
                    <th>P/L (%)</th>
                    <th>Purchase Date</th>
                </tr>
            </thead>
            <tbody>
    `;

    holdings.forEach(holding => {
        const symbol = holding.symbol.replace('.KL', '');
        const isGain = holding.paper_gain_loss_rm >= 0;

        tableHTML += `
            <tr class="holding-row ${isGain ? 'gain-row' : 'loss-row'}">
                <td class="symbol-cell">
                    <strong>${symbol}</strong>
                </td>
                <td class="number-cell">${holding.shares.toLocaleString()}</td>
                <td class="number-cell">RM ${holding.purchase_price_rm.toFixed(2)}</td>
                <td class="number-cell">RM ${holding.current_price_rm.toFixed(2)}</td>
                <td class="number-cell">RM ${holding.purchase_value_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</td>
                <td class="number-cell">RM ${holding.current_value_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}</td>
                <td class="number-cell ${isGain ? 'gain' : 'loss'}">
                    ${isGain ? '+' : ''}RM ${holding.paper_gain_loss_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}
                </td>
                <td class="number-cell ${isGain ? 'gain' : 'loss'}">
                    ${isGain ? '+' : ''}${holding.paper_gain_loss_percent.toFixed(2)}%
                </td>
                <td class="date-cell">${holding.purchase_date}</td>
            </tr>
        `;
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    const container = document.getElementById('holdings-table');
    if (container) {
        container.innerHTML = tableHTML;
    }
}

function renderPerformanceChart() {
    const dailyPerf = portfolioData.daily_performance || [];

    if (dailyPerf.length === 0) {
        const container = document.getElementById('performance-chart');
        if (container) {
            container.innerHTML = `
                <div class="no-data">
                    <p>No performance data yet. Mark daily performance to see trends!</p>
                    <code>python3 scripts/portfolio_tracker.py mark --prices-file current_market_data.json</code>
                </div>
            `;
        }
        return;
    }

    // Prepare data for chart
    const dates = dailyPerf.map(p => p.date);
    const portfolioValues = dailyPerf.map(p => p.portfolio_summary.total_portfolio_value_rm);
    const returns = dailyPerf.map(p => p.portfolio_summary.total_return_percent);

    const container = document.getElementById('performance-chart');
    if (!container) return;

    // Create canvas for Chart.js
    container.innerHTML = '<canvas id="portfolio-chart-canvas"></canvas>';

    const ctx = document.getElementById('portfolio-chart-canvas').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [
                {
                    label: 'Portfolio Value (RM)',
                    data: portfolioValues,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    yAxisID: 'y',
                    tension: 0.4
                },
                {
                    label: 'Return (%)',
                    data: returns,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    yAxisID: 'y1',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Portfolio Performance Over Time'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Portfolio Value (RM)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Return (%)'
                    },
                    grid: {
                        drawOnChartArea: false
                    }
                }
            }
        }
    });
}

function renderTransactionHistory() {
    const transactions = portfolioData.transaction_history || [];

    if (transactions.length === 0) {
        const container = document.getElementById('transaction-history');
        if (container) {
            container.innerHTML = '<p class="no-data">No transactions yet</p>';
        }
        return;
    }

    // Show last 20 transactions
    const recentTransactions = transactions.slice(-20).reverse();

    let historyHTML = '<div class="transactions-list">';

    recentTransactions.forEach(txn => {
        const isBuy = txn.type === 'BUY';
        const symbol = txn.symbol.replace('.KL', '');

        historyHTML += `
            <div class="transaction-item ${isBuy ? 'buy' : 'sell'}">
                <div class="txn-icon">${isBuy ? '📈' : '📉'}</div>
                <div class="txn-details">
                    <div class="txn-header">
                        <strong>${txn.type} ${symbol}</strong>
                        <span class="txn-date">${txn.date}</span>
                    </div>
                    <div class="txn-info">
                        ${txn.shares.toLocaleString()} shares @ RM ${txn.price_rm.toFixed(2)} = RM ${txn.total_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})}
                    </div>
                    ${!isBuy && txn.realized_gain_loss_rm !== undefined ? `
                    <div class="txn-pnl ${txn.realized_gain_loss_rm >= 0 ? 'gain' : 'loss'}">
                        Realized P/L: ${txn.realized_gain_loss_rm >= 0 ? '+' : ''}RM ${txn.realized_gain_loss_rm.toLocaleString('en-MY', {minimumFractionDigits: 2})} (${txn.realized_gain_loss_percent >= 0 ? '+' : ''}${txn.realized_gain_loss_percent.toFixed(2)}%)
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    });

    historyHTML += '</div>';

    const container = document.getElementById('transaction-history');
    if (container) {
        container.innerHTML = historyHTML;
    }
}

// Initialize portfolio visualization
document.addEventListener('DOMContentLoaded', () => {
    loadPortfolioData();
});
