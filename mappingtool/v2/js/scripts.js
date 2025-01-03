// Screen Data
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

// Generate Menu
function generateMenu() {
    const menu = document.getElementById("menu");
    if (!menu) {
        console.error("Menu element not found!");
        return;
    }

    screens.forEach(screen => {
        const link = document.createElement("a");
        link.href = `/mappingtool/v2/pages/${screen.id}.html`;
        link.textContent = screen.name;
        menu.appendChild(link);
    });

    console.log("Menu generated successfully:", menu.innerHTML);
}

// Initialize Menu on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded. Initializing menu...");
    generateMenu();
});
