// Dynamic Menu Data
const screens = [
    { name: "Dashboard", id: "dashboard" },
    { name: "Rig Monitoring", id: "rig-monitoring" },
    { name: "Routing", id: "routing" },
    { name: "Street Mapping", id: "street-mapping" },
    { name: "Issue Management", id: "issue-management" },
    { name: "Progress Overview", id: "progress-overview" },
    { name: "Data Sync", id: "data-sync" },
    { name: "Settings", id: "settings" },
    { name: "User Management", id: "user-management" },
    { name: "Validation", id: "validation" },
    { name: "Reports", id: "reports" }
];

// Function to Generate Menu
function generateMenu() {
    const menu = document.getElementById("menu");
    screens.forEach(screen => {
        const link = document.createElement("a");
        link.href = `#${screen.id}`;
        link.textContent = screen.name;
        link.onclick = () => loadScreen(screen.id);
        menu.appendChild(link);
    });
}

// Function to Load Screen Content
function loadScreen(screenId) {
    const content = document.getElementById("content");
    content.innerHTML = `<h1>${screenId.replace("-", " ")}</h1><p>Content for ${screenId} goes here.</p>`;
}

// Initialize Menu
generateMenu();
