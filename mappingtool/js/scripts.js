// Navigation handler for sidebar links
function navigateTo(page) {
    // Ensure correct navigation
    window.location.href = `../pages/${page}.html`;
}

// Dynamically update the menu items
function generateMenu() {
    const menuItems = [
        { name: 'Dashboard', link: 'dashboard.html' },
        { name: 'Drive-Time Estimator', link: 'drive_time_estimator.html' }
        { name: 'Rig Management', link: 'rig_management.html' },
        { name: 'Route Allocation', link: 'route_allocation.html' },
        { name: 'Grid Management', link: 'grid_management.html' },
        { name: 'Analytics', link: 'analytics.html' },
        { name: 'Settings', link: 'settings.html' },
        
    ];

    const menu = document.querySelector('.sidebar ul');
    menu.innerHTML = ''; // Clear existing menu items

    menuItems.forEach(item => {
        const newMenuItem = document.createElement('li');
        newMenuItem.innerHTML = `<a href="${item.link}">${item.name}</a>`;
        menu.appendChild(newMenuItem);
    });

    // Add event listeners to all links
    const sidebarLinks = menu.querySelectorAll('a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('href').replace('.html', '');
            navigateTo(page);
        });
    });
}

// Initialize grid tools
function initGridTools() {
    const mapContainer = document.getElementById('map-container');
    const gridOverlay = document.getElementById('grid-overlay');

    if (mapContainer && gridOverlay) {
        document.getElementById('tool-slide').addEventListener('click', () => {
            alert('Slide Selection Tool Activated');
        });

        document.getElementById('tool-square').addEventListener('click', () => {
            alert('Square Selection Tool Activated');
        });

        document.getElementById('tool-polygon').addEventListener('click', () => {
            alert('Polygon Selection Tool Activated');
        });
    }
}

// Initialize the app
function initApp() {
    console.log('App initialized');
    generateMenu();
    initGridTools();
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', initApp);
