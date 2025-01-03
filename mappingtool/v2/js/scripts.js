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

function generateMenu() {
    const menu = document.getElementById("menu");
    if (!menu) {
        console.error("Menu element not found!");
        return;
    }
    console.log("Menu element found:", menu);
    screens.forEach(screen => {
        console.log("Adding screen:", screen);
        const link = document.createElement("a");
        link.href = `#${screen.id}`;
        link.textContent = screen.name;
        link.onclick = () => loadScreen(screen.id);
        menu.appendChild(link);
    });
    console.log("Menu generated successfully:", menu.innerHTML);
}


document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded and parsed");
    generateMenu();
});

