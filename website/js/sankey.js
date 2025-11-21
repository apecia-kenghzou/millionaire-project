// Sankey Diagram for Market Money Flow Visualization

function initSankey() {
    if (!moneyFlowData || !moneyFlowData.sankey_data) {
        console.error('Money flow data not loaded');
        return;
    }

    const container = document.getElementById('sankey-chart');
    const width = container.clientWidth - 40;
    const height = 600;

    // Clear existing SVG
    container.innerHTML = '';

    // Add title and description
    const titleDiv = document.createElement('div');
    titleDiv.style.marginBottom = '20px';
    titleDiv.innerHTML = `
        <h3 style="margin-bottom: 10px;">Market Money Flow Analysis - Nov 21, 2025</h3>
        <p style="color: #6c757d; font-size: 0.95rem;">
            Showing institutional vs retail capital flows, sector allocation, and accumulation/distribution patterns.
            <strong>Net Institutional Flow: +RM ${(moneyFlowData.net_institutional_flow_rm / 1000000).toFixed(1)}M</strong>
        </p>
    `;
    container.appendChild(titleDiv);

    // Create SVG
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('background', '#f8f9fa')
        .style('border-radius', '10px');

    const g = svg.append('g')
        .attr('transform', 'translate(20, 20)');

    // Set up sankey generator
    const sankey = d3.sankey()
        .nodeWidth(20)
        .nodePadding(15)
        .extent([[0, 0], [width - 60, height - 60]]);

    // Prepare data
    const { nodes, links } = moneyFlowData.sankey_data;

    // Create sankey layout
    const sankeyData = sankey({
        nodes: nodes.map(d => Object.assign({}, d)),
        links: links.map(d => Object.assign({}, d))
    });

    // Color scale for different flow types
    const colorScale = d3.scaleOrdinal()
        .domain(['Institutional', 'Retail', 'Technology', 'Finance', 'Utilities',
                 'Buying', 'Selling', 'Accumulation', 'Distribution', 'Neutral'])
        .range(['#667eea', '#f093fb', '#17a2b8', '#007bff', '#6f42c1',
                '#28a745', '#dc3545', '#0ba360', '#e74c3c', '#95a5a6']);

    // Function to get link color
    function getLinkColor(link) {
        const sourceName = link.source.name.toLowerCase();
        const targetName = link.target.name.toLowerCase();

        if (sourceName.includes('institutional')) return '#667eea';
        if (sourceName.includes('retail')) return '#f093fb';
        if (targetName.includes('technology')) return '#17a2b8';
        if (targetName.includes('finance')) return '#007bff';
        if (targetName.includes('utilities')) return '#6f42c1';
        if (targetName.includes('buying')) return '#28a745';
        if (targetName.includes('selling')) return '#dc3545';
        if (targetName.includes('accumulation')) return '#0ba360';
        if (targetName.includes('distribution')) return '#e74c3c';

        return '#95a5a6';
    }

    // Draw links
    const link = g.append('g')
        .selectAll('.link')
        .data(sankeyData.links)
        .enter()
        .append('path')
        .attr('class', 'link')
        .attr('d', d3.sankeyLinkHorizontal())
        .attr('stroke', d => getLinkColor(d))
        .attr('stroke-width', d => Math.max(1, d.width))
        .attr('fill', 'none')
        .attr('opacity', 0.4)
        .on('mouseover', function(event, d) {
            d3.select(this).attr('opacity', 0.7);
            showTooltip(event, d);
        })
        .on('mouseout', function() {
            d3.select(this).attr('opacity', 0.4);
            hideTooltip();
        });

    // Draw nodes
    const node = g.append('g')
        .selectAll('.node')
        .data(sankeyData.nodes)
        .enter()
        .append('g')
        .attr('class', 'node');

    node.append('rect')
        .attr('x', d => d.x0)
        .attr('y', d => d.y0)
        .attr('height', d => d.y1 - d.y0)
        .attr('width', d => d.x1 - d.x0)
        .attr('fill', d => {
            const name = d.name.toLowerCase();
            if (name.includes('institutional')) return '#667eea';
            if (name.includes('retail')) return '#f093fb';
            if (name.includes('technology')) return '#17a2b8';
            if (name.includes('finance')) return '#007bff';
            if (name.includes('utilities')) return '#6f42c1';
            if (name.includes('buying')) return '#28a745';
            if (name.includes('selling')) return '#dc3545';
            if (name.includes('accumulation')) return '#0ba360';
            if (name.includes('distribution')) return '#e74c3c';
            return '#95a5a6';
        })
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .on('mouseover', function(event, d) {
            d3.select(this).attr('opacity', 0.8);
            showNodeTooltip(event, d);
        })
        .on('mouseout', function() {
            d3.select(this).attr('opacity', 1);
            hideTooltip();
        });

    // Add node labels
    node.append('text')
        .attr('x', d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
        .attr('y', d => (d.y1 + d.y0) / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', d => d.x0 < width / 2 ? 'start' : 'end')
        .text(d => d.name)
        .style('font-size', '12px')
        .style('font-weight', '600')
        .style('fill', '#212529');

    // Tooltip
    const tooltip = d3.select('body')
        .append('div')
        .attr('class', 'sankey-tooltip')
        .style('position', 'absolute')
        .style('background', 'white')
        .style('padding', '10px 15px')
        .style('border-radius', '8px')
        .style('box-shadow', '0 4px 15px rgba(0,0,0,0.2)')
        .style('font-size', '13px')
        .style('pointer-events', 'none')
        .style('opacity', 0)
        .style('z-index', 10000);

    function showTooltip(event, d) {
        const value = (d.value / 1000000).toFixed(1);
        tooltip
            .html(`
                <strong>${d.source.name} → ${d.target.name}</strong><br/>
                <span style="color: #667eea;">Flow: RM ${value}M</span><br/>
                ${d.label ? `<em>${d.label}</em>` : ''}
            `)
            .style('left', (event.pageX + 15) + 'px')
            .style('top', (event.pageY - 30) + 'px')
            .style('opacity', 1);
    }

    function showNodeTooltip(event, d) {
        const inflow = d.sourceLinks.reduce((sum, l) => sum + l.value, 0);
        const outflow = d.targetLinks.reduce((sum, l) => sum + l.value, 0);
        const netFlow = outflow - inflow;

        tooltip
            .html(`
                <strong>${d.name}</strong><br/>
                <span style="color: #28a745;">Inflow: RM ${(inflow / 1000000).toFixed(1)}M</span><br/>
                <span style="color: #dc3545;">Outflow: RM ${(outflow / 1000000).toFixed(1)}M</span><br/>
                <span style="font-weight: 600;">Net: RM ${(netFlow / 1000000).toFixed(1)}M</span>
            `)
            .style('left', (event.pageX + 15) + 'px')
            .style('top', (event.pageY - 30) + 'px')
            .style('opacity', 1);
    }

    function hideTooltip() {
        tooltip.style('opacity', 0);
    }

    // Add legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 200}, 20)`);

    const legendData = [
        { label: 'Institutional Flow', color: '#667eea' },
        { label: 'Retail Flow', color: '#f093fb' },
        { label: 'Finance Sector', color: '#007bff' },
        { label: 'Utilities Sector', color: '#6f42c1' },
        { label: 'Technology Sector', color: '#17a2b8' },
        { label: 'Buying Pressure', color: '#28a745' },
        { label: 'Selling Pressure', color: '#dc3545' }
    ];

    legendData.forEach((item, i) => {
        const legendRow = legend.append('g')
            .attr('transform', `translate(0, ${i * 25})`);

        legendRow.append('rect')
            .attr('width', 15)
            .attr('height', 15)
            .attr('fill', item.color);

        legendRow.append('text')
            .attr('x', 20)
            .attr('y', 12)
            .text(item.label)
            .style('font-size', '11px')
            .style('fill', '#212529');
    });

    // Add summary statistics below the chart
    const summaryDiv = document.createElement('div');
    summaryDiv.style.marginTop = '30px';
    summaryDiv.style.display = 'grid';
    summaryDiv.style.gridTemplateColumns = 'repeat(auto-fit, minmax(200px, 1fr))';
    summaryDiv.style.gap = '15px';

    const sectors = moneyFlowData.sector_flows;
    sectors.forEach(sector => {
        const sectorCard = document.createElement('div');
        sectorCard.style.padding = '15px';
        sectorCard.style.background = 'white';
        sectorCard.style.border = '2px solid #e9ecef';
        sectorCard.style.borderRadius = '8px';

        const flowColor = sector.net_flow === 'Inflow' ? '#28a745' :
                          sector.net_flow === 'Outflow' ? '#dc3545' : '#6c757d';

        sectorCard.innerHTML = `
            <h4 style="margin: 0 0 10px 0; color: #212529;">${sector.sector}</h4>
            <div style="font-size: 0.9rem; color: #6c757d;">
                <div><strong>Flow:</strong> <span style="color: ${flowColor}">${sector.net_flow}</span> (${sector.flow_strength})</div>
                <div><strong>Volume:</strong> RM ${(sector.total_volume_rm / 1000000).toFixed(1)}M</div>
                <div><strong>Buying:</strong> ${sector.buying_pressure}% | <strong>Selling:</strong> ${sector.selling_pressure}%</div>
            </div>
        `;

        summaryDiv.appendChild(sectorCard);
    });

    container.appendChild(summaryDiv);

    console.log('Sankey diagram initialized');
}

// Re-initialize on window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        if (moneyFlowData) {
            initSankey();
        }
    }, 250);
});
