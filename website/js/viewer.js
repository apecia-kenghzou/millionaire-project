/**
 * MARKDOWN VIEWER - Beautiful Stock Analysis Display
 * Fetches and renders markdown files with syntax highlighting
 */

// Configure marked.js for better rendering
if (typeof marked !== 'undefined') {
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: true,
        mangle: false,
        sanitize: false,
        smartLists: true,
        smartypants: true,
        xhtml: false
    });
}

// Get file path from URL parameters
function getFilePathFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('file');
}

// Format file path for display
function formatFilePath(filePath) {
    if (!filePath) return 'Unknown';

    // Remove leading slash and make it more readable
    const cleanPath = filePath.replace(/^\//, '');

    // Extract meaningful parts
    const parts = cleanPath.split('/');
    const date = parts[1] || '';
    const sector = parts[2] || '';
    const file = parts[3] || '';

    return `${date} / ${sector} / ${file}`;
}

// Extract stock symbol from file path
function extractStockSymbol(filePath) {
    if (!filePath) return 'Stock';
    const match = filePath.match(/\/([^\/]+)\.md$/);
    return match ? match[1] : 'Stock';
}

// Fetch and display markdown content
async function loadMarkdownFile(filePath) {
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const contentEl = document.getElementById('markdown-content');
    const filePathEl = document.getElementById('file-path');
    const lastUpdatedEl = document.getElementById('last-updated');

    try {
        // Show loading state
        loadingEl.style.display = 'flex';
        errorEl.style.display = 'none';
        contentEl.style.display = 'none';

        // Update header with file info
        filePathEl.textContent = formatFilePath(filePath);
        const stockSymbol = extractStockSymbol(filePath);
        document.title = `${stockSymbol} Analysis | Millionaire Dashboard`;

        // Fetch the markdown file
        const response = await fetch(filePath);

        if (!response.ok) {
            throw new Error(`Failed to load file: ${response.status} ${response.statusText}`);
        }

        const markdownText = await response.text();

        // Convert markdown to HTML
        const htmlContent = marked.parse(markdownText);

        // Inject the HTML into the content area
        contentEl.innerHTML = htmlContent;

        // Apply syntax highlighting to code blocks
        if (typeof hljs !== 'undefined') {
            contentEl.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }

        // Enhance tables with hover effects
        enhanceTables();

        // Add smooth scroll to internal links
        addSmoothScrolling();

        // Update last modified date
        const lastModified = response.headers.get('last-modified');
        if (lastModified) {
            const date = new Date(lastModified);
            lastUpdatedEl.textContent = date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } else {
            lastUpdatedEl.textContent = 'Recently';
        }

        // Hide loading, show content
        loadingEl.style.display = 'none';
        contentEl.style.display = 'block';

        // Smooth fade-in animation
        contentEl.style.opacity = '0';
        setTimeout(() => {
            contentEl.style.transition = 'opacity 0.5s ease';
            contentEl.style.opacity = '1';
        }, 50);

    } catch (error) {
        console.error('Error loading markdown:', error);

        // Show error state
        loadingEl.style.display = 'none';
        errorEl.style.display = 'block';

        const errorMessageEl = document.getElementById('error-message');
        errorMessageEl.textContent = `Could not load analysis file: ${error.message}`;

        // Update title
        document.title = 'Error | Millionaire Dashboard';
    }
}

// Enhance tables with additional features
function enhanceTables() {
    const tables = document.querySelectorAll('.markdown-body table');

    tables.forEach(table => {
        // Wrap table in responsive container
        if (!table.parentElement.classList.contains('table-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-wrapper';
            wrapper.style.overflowX = 'auto';
            wrapper.style.marginBottom = '1.5rem';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }

        // Add zebra striping if not already styled
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            if (index % 2 === 0) {
                row.style.backgroundColor = '#ffffff';
            } else {
                row.style.backgroundColor = '#f8f9fa';
            }
        });
    });
}

// Add smooth scrolling for internal anchor links
function addSmoothScrolling() {
    const links = document.querySelectorAll('.markdown-body a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Highlight important keywords in the content
function highlightKeywords() {
    const contentEl = document.getElementById('markdown-content');
    const keywords = {
        'BUY': '#27ae60',
        'SELL': '#e74c3c',
        'HOLD': '#f39c12',
        'STRONG BUY': '#27ae60',
        'ACCUMULATE': '#2ecc71',
        'BULLISH': '#27ae60',
        'BEARISH': '#e74c3c',
        'OVERSOLD': '#3498db',
        'OVERBOUGHT': '#e67e22'
    };

    // This is a simple implementation - could be enhanced
    Object.keys(keywords).forEach(keyword => {
        const color = keywords[keyword];
        const regex = new RegExp(`\\b${keyword}\\b`, 'gi');

        // Apply to text nodes only (to avoid breaking HTML)
        const walker = document.createTreeWalker(
            contentEl,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const nodesToReplace = [];
        while (walker.nextNode()) {
            if (walker.currentNode.nodeValue.match(regex)) {
                nodesToReplace.push(walker.currentNode);
            }
        }

        nodesToReplace.forEach(node => {
            const span = document.createElement('span');
            span.innerHTML = node.nodeValue.replace(
                regex,
                `<strong style="color: ${color}; background: ${color}15; padding: 2px 6px; border-radius: 3px;">$&</strong>`
            );
            node.parentNode.replaceChild(span, node);
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const filePath = getFilePathFromURL();

    if (!filePath) {
        // No file specified, show error
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
        document.getElementById('error-message').textContent =
            'No file specified. Please provide a file path in the URL parameters.';
        return;
    }

    // Load the markdown file
    loadMarkdownFile(filePath);
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Escape key: go back to dashboard
    if (e.key === 'Escape') {
        window.location.href = '/website/index.html';
    }

    // Ctrl/Cmd + P: print
    if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        // Let default print handler work
    }
});

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getFilePathFromURL,
        formatFilePath,
        extractStockSymbol,
        loadMarkdownFile
    };
}
