// Navigation handler for sidebar links
function navigateTo(page) {
    // Correct navigation to include the /pages directory once
    window.location.href = `../pages/${page}.html`;
}

// Example: Functionality for future interactivity
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}

// Placeholder: Dynamically update metrics (if needed)
function updateMetrics(metrics) {
    // Example implementation
    document.querySelector('.card h4').textContent = metrics.title;
    document.querySelector('.card p').textContent = metrics.value;
}

// Initialize event listeners or any startup logic
function initApp() {
    console.log('App initialized');

    // Add navigation links for all menu items dynamically
    const menuItems = [
        { name: 'Dashboard', link: 'dashboard.html' },
        { name: 'Rig Management', link: 'rig_management.html' },
        { name: 'Route Allocation', link: 'route_allocation.html' },
        { name: 'Grid Management', link: 'grid_management.html' },
        { name: 'Analytics', link: 'analytics.html' },
        { name: 'Settings', link: 'settings.html' }
    ];

    const menu = document.querySelector('.sidebar ul');
    menu.innerHTML = ''; // Clear existing menu items

    menuItems.forEach(item => {
        const newMenuItem = document.createElement('li');
        newMenuItem.innerHTML = `<a href="${item.link}">${item.name}</a>`;
        menu.appendChild(newMenuItem);
    });

    // Add navigation event listeners
    const sidebarLinks = menu.querySelectorAll('a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('href').replace('.html', '').replace('../pages/', '');
            navigateTo(page);
        });
    });

    // Initialize slicing buttons for grid management
    const mapContainer = document.getElementById('map-container');
    const gridOverlay = document.getElementById('grid-overlay');

    if (mapContainer && gridOverlay) {
        document.getElementById('slice-horizontal').addEventListener('click', () => {
            const currentRows = gridOverlay.style.gridTemplateRows.split(' ').length || 1;
            gridOverlay.style.gridTemplateRows = `repeat(${currentRows + 1}, 1fr)`;
        });

        document.getElementById('slice-vertical').addEventListener('click', () => {
            const currentCols = gridOverlay.style.gridTemplateColumns.split(' ').length || 1;
            gridOverlay.style.gridTemplateColumns = `repeat(${currentCols + 1}, 1fr)`;
        });

        document.getElementById('clear-grid').addEventListener('click', () => {
            gridOverlay.style.gridTemplateRows = 'repeat(1, 1fr)';
            gridOverlay.style.gridTemplateColumns = 'repeat(1, 1fr)';
        });
    }
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', initApp);
