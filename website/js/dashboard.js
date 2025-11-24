// Dashboard Main Logic and Stock Detail Modal

// Show stock detail modal
function showStockDetail(symbolOrCode) {
    const symbol = resolveSymbol(symbolOrCode);

    if (!symbol) {
        alert(`Stock not found: ${symbolOrCode}`);
        return;
    }

    const stock = getStockBySymbol(symbol);

    if (!stock) {
        alert(`Stock data not found for: ${symbol}`);
        return;
    }

    // Get money flow data if available
    const moneyFlow = moneyFlowData?.institutional_activity?.find(a => a.symbol === symbol);

    // Build modal content
    const modalBody = document.getElementById('modal-body');
    const companyName = stock.company_name || getStockName(symbol);
    const shortSymbol = symbol.replace('.KL', '');

    // Get sector 4-digit code
    const fourDigitCode = shortSymbol.match(/\d+/)?.[0] || shortSymbol;

    modalBody.innerHTML = `
        <div class="stock-detail-header" style="margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h2 style="margin: 0 0 0.5rem 0; font-size: 2rem;">${shortSymbol}</h2>
                    <h3 style="margin: 0; color: #6c757d; font-weight: 500;">${companyName}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #6c757d;">
                        <strong>Sector:</strong> ${stock.sector || 'N/A'} |
                        <strong>Code:</strong> ${fourDigitCode}
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: #212529; margin-bottom: 0.5rem;">
                        ${stock.current_price_rm ? `RM ${stock.current_price_rm.toFixed(2)}` : 'N/A'}
                    </div>
                    ${stock.rank ? `<div style="font-size: 1.1rem; color: #6c757d;">Rank: #${stock.rank}</div>` : ''}
                </div>
            </div>
        </div>

        <!-- Key Metrics -->
        <div class="stock-metrics" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            <div class="metric-card" style="padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">Composite Score</div>
                <div style="font-size: 2rem; font-weight: 700; color: ${stock.composite_score >= 7.5 ? '#28a745' : '#ffc107'};">
                    ${stock.composite_score ? stock.composite_score.toFixed(2) : 'N/A'}/10
                </div>
                <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.5rem;">
                    Fundamental: ${stock.fundamental_score?.toFixed(1) || 'N/A'} | Technical: ${stock.technical_score?.toFixed(1) || 'N/A'}
                </div>
            </div>

            <div class="metric-card" style="padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">RSI (14)</div>
                <div style="font-size: 2rem; font-weight: 700; color: ${stock.technical_indicators?.rsi_14 < 30 ? '#28a745' : stock.technical_indicators?.rsi_14 > 70 ? '#dc3545' : '#212529'};">
                    ${stock.technical_indicators?.rsi_14 ? stock.technical_indicators.rsi_14.toFixed(1) : 'N/A'}
                </div>
                <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.5rem;">
                    ${stock.technical_indicators?.rsi_status || 'N/A'}
                </div>
            </div>

            <div class="metric-card" style="padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">Expected Return</div>
                <div style="font-size: 2rem; font-weight: 700; color: #28a745;">
                    ${stock.expected_return_12m?.base_case || 'N/A'}
                </div>
                <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.5rem;">
                    Conservative: ${stock.expected_return_12m?.conservative || 'N/A'}
                </div>
            </div>

            <div class="metric-card" style="padding: 1.5rem; background: #f8f9fa; border-radius: 10px;">
                <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">Allocation</div>
                <div style="font-size: 2rem; font-weight: 700; color: #007bff;">
                    ${stock.portfolio_allocation_percent ? stock.portfolio_allocation_percent + '%' : 'N/A'}
                </div>
                <div style="font-size: 0.85rem; color: #6c757d; margin-top: 0.5rem;">
                    ${stock.portfolio_allocation_rm ? `RM ${stock.portfolio_allocation_rm.toLocaleString()}` : 'Not allocated'}
                </div>
            </div>
        </div>

        <!-- Action Recommendation -->
        <div class="action-section" style="padding: 1.5rem; background: ${stock.action_recommendation?.includes('BUY') ? '#d4edda' : '#fff3cd'}; border-radius: 10px; margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0;">Recommended Action</h3>
            <div style="font-size: 1.5rem; font-weight: 700; color: ${stock.action_recommendation?.includes('BUY') ? '#155724' : '#856404'}; margin-bottom: 1rem;">
                ${stock.action_recommendation || 'WATCH'}
            </div>
            <div style="color: #212529;">
                <strong>Entry Zone:</strong> ${stock.entry_zone_rm || 'N/A'}<br/>
                <strong>Stop Loss:</strong> RM ${stock.stop_loss_rm || 'N/A'} |
                <strong>Target:</strong> RM ${stock.profit_target_rm || 'N/A'}
            </div>
        </div>

        <!-- Investment Thesis -->
        ${stock.investment_thesis ? `
        <div class="thesis-section" style="padding: 1.5rem; background: #e7f3ff; border-left: 4px solid #007bff; margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0;">Investment Thesis</h3>
            <p style="margin: 0; line-height: 1.6;">${stock.investment_thesis}</p>
        </div>
        ` : ''}

        <!-- Return Drivers -->
        ${stock.return_drivers && stock.return_drivers.length > 0 ? `
        <div class="drivers-section" style="margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0;">Return Drivers</h3>
            <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8;">
                ${stock.return_drivers.map(driver => `<li>${driver}</li>`).join('')}
            </ul>
        </div>
        ` : ''}

        <!-- Key Catalysts -->
        ${stock.key_catalysts && stock.key_catalysts.length > 0 ? `
        <div class="catalysts-section" style="margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0;">Key Catalysts</h3>
            <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8;">
                ${stock.key_catalysts.map(catalyst => `<li>${catalyst}</li>`).join('')}
            </ul>
        </div>
        ` : ''}

        <!-- Money Flow Analysis -->
        ${moneyFlow ? `
        <div class="money-flow-section" style="padding: 1.5rem; background: ${moneyFlow.activity.includes('Accumulation') ? '#d1ecf1' : '#f8d7da'}; border-radius: 10px; margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0;">💰 Money Flow Analysis</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                <div>
                    <div style="font-size: 0.85rem; color: #6c757d;">Activity</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">${moneyFlow.activity}</div>
                </div>
                <div>
                    <div style="font-size: 0.85rem; color: #6c757d;">Volume Ratio</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">${moneyFlow.volume_ratio}x</div>
                </div>
                <div>
                    <div style="font-size: 0.85rem; color: #6c757d;">Indicator</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: ${moneyFlow.money_flow_indicator === 'Bullish' ? '#28a745' : '#dc3545'};">
                        ${moneyFlow.money_flow_indicator}
                    </div>
                </div>
                <div>
                    <div style="font-size: 0.85rem; color: #6c757d;">Est. Flow</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">
                        RM ${(moneyFlow.estimated_institutional_flow_rm / 1000000).toFixed(1)}M
                    </div>
                </div>
            </div>
            <div style="margin-top: 1rem; padding: 1rem; background: white; border-radius: 5px;">
                <strong>Analysis:</strong> ${moneyFlow.rationale}
            </div>
        </div>
        ` : ''}

        <!-- Technical Indicators -->
        ${stock.technical_indicators ? `
        <div class="technical-section" style="margin-bottom: 2rem;">
            <h3 style="margin: 0 0 1rem 0;">Technical Indicators</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 0.85rem; color: #6c757d;">MACD Status</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">${stock.technical_indicators.macd_status || 'N/A'}</div>
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 0.85rem; color: #6c757d;">Trend</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">${stock.technical_indicators.trend || 'N/A'}</div>
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 0.85rem; color: #6c757d;">Volume Ratio</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">${stock.technical_indicators.volume_ratio}x</div>
                </div>
                <div style="padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <div style="font-size: 0.85rem; color: #6c757d;">Volume Status</div>
                    <div style="font-size: 1.1rem; font-weight: 600;">${stock.technical_indicators.volume_status || 'N/A'}</div>
                </div>
            </div>
        </div>
        ` : ''}

        <!-- Risk Level -->
        <div class="risk-section" style="padding: 1.5rem; background: #fff3cd; border-radius: 10px;">
            <h3 style="margin: 0 0 1rem 0;">Risk Assessment</h3>
            <div style="font-size: 1.2rem; font-weight: 600; color: #856404; margin-bottom: 0.5rem;">
                Risk Level: ${stock.risk_level || 'Medium'}
            </div>
            ${stock.critical_note ? `
            <div style="margin-top: 1rem; padding: 1rem; background: white; border-radius: 5px;">
                <strong>Important Note:</strong> ${stock.critical_note}
            </div>
            ` : ''}
        </div>

        <!-- Analysis File Link -->
        <div style="margin-top: 2rem; text-align: center;">
            <a href="/website/viewer.html?file=/analysis/2025-11-21/${stock.sector?.toLowerCase()}/${shortSymbol}.md"
               target="_blank"
               style="display: inline-block; padding: 1rem 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 10px; font-weight: 600; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4); transition: all 0.3s ease;">
                📄 View Beautiful Analysis Report
            </a>
        </div>
    `;

    // Show modal
    document.getElementById('stock-modal').style.display = 'block';

    // Smooth scroll to top of modal
    document.querySelector('.modal-content').scrollTop = 0;
}

// Close modal
function closeModal() {
    document.getElementById('stock-modal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('stock-modal');
    if (event.target === modal) {
        closeModal();
    }
};

// Smooth scrolling for nav links
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // Update active nav link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // ESC to close modal
        if (e.key === 'Escape') {
            closeModal();
        }
    });
});
