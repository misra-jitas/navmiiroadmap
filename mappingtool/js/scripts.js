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

    // Add navigation links for new menu items
    const sidebarLinks = document.querySelectorAll('.sidebar ul li a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('href').replace('.html', '').replace('../pages/', '');
            navigateTo(page);
        });
    });

    // Add new menu items dynamically
    const menu = document.querySelector('.sidebar ul');
    const newMenuItem = document.createElement('li');
    newMenuItem.innerHTML = '<a href="grid_management.html">Grid Management</a>';
    menu.appendChild(newMenuItem);
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', initApp);
