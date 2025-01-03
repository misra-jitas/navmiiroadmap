// Screen Data
const screens = [
     {
        name: "DCA Drive Collection Area",
        id: "grid-management",
        description: "Manage grid cells, resize, assign, and visualize grid metadata."
    },
    {
        name: "Drive-Time Estimator UI",
        id: "drive-time-estimator",
        description: "Calculate drive times with overlays for weather, traffic, and construction."
    },
    {
        name: "Progress Tracker UI",
        id: "progress-tracker",
        description: "Track progress, annotate missed roads, and view real-time updates."
    },
    {
        name: "Data Export UI",
        id: "data-export",
        description: "Filter, export data in various formats, and preview export summaries."
    },
    {
        name: "User Parameters UI",
        id: "user-parameters",
        description: "Manage custom parameters and save configurations for projects."
    },
    {
        name: "Communication Hub UI",
        id: "communication-hub",
        description: "View live updates and provide feedback from the central hub."
    },
    {
        name: "Planner Dashboard",
        id: "planner-dashboard",
        description: "Overview of grids, progress, drive-time estimates, and tools for planning."
    },
    {
        name: "Operator View",
        id: "operator-view",
        description: "Assigned cells, route visualization, and communication interface."
    },
    {
        name: "Project Manager Dashboard",
        id: "project-manager-dashboard",
        description: "High-level project progress and efficiency metrics overview."
    },
    {
        name: "Accounting Dashboard",
        id: "accounting-dashboard",
        description: "Granular financial data and export tools for cost analysis."
    },
    {
        name: "Client View",
        id: "client-view",
        description: "Simplified progress overview with cost-effectiveness visualization."
    }
];

// Generate Sidebar Menu
function generateMenu() {
    const menu = document.getElementById("menu");
    if (!menu) {
        console.error("Menu element not found!");
        return;
    }

    screens.forEach(screen => {
        const container = document.createElement("div");
        container.className = "menu-item";

        const link = document.createElement("a");
        link.href = `/mappingtool/v2/pages/${screen.id}.html`;
        link.textContent = screen.name;

        const description = document.createElement("p");
        description.textContent = screen.description;

        container.appendChild(link);
        container.appendChild(description);
        menu.appendChild(container);
    });

    console.log("Menu generated successfully:", menu.innerHTML);
}

// Initialize Menu on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded. Initializing menu...");
    generateMenu();
});
