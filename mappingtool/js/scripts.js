// Navigation handler for sidebar links
function navigateTo(page) {
    // Correct navigation to include the /pages directory once
    window.location.href = `../pages/${page}.html`;
}

// Static menu generation removed; fallback to hardcoded menu in HTML

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
    initGridTools();
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', initApp);
