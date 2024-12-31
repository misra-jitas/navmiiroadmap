// Navigation handler for sidebar links
function navigateTo(page) {
    // Ensure navigation links are correct
    window.location.href = `./pages/${page}.html`;
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

    // Example: Add event listeners for actions
    const sidebarLinks = document.querySelectorAll('.sidebar ul li a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(link.getAttribute('href').replace('.html', ''));
        });
    });
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', initApp);
