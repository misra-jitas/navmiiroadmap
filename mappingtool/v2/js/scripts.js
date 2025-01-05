// Screen Data
const screens = [
    {
        subtitle: "Core Module Screens",
        screens: [
            {
                name: "DCA Management Platform",
                id: "grid-management",
                description: "Load DCA. Create, estimate and commit Missions in DCA"
            },
            /*
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
            }
            */
        ]
    },
    {
        subtitle: "Role-Specific Screens",
        screens: [
            /*
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
            */
        ]
    }
];

function generateMenu() {
    const menu = document.getElementById("menu");
    if (!menu) {
        console.error("Menu element not found!");
        return;
    }

    screens.forEach(group => {
        // Always add the subtitle
        const subtitle = document.createElement("h3");
        subtitle.textContent = group.subtitle;
        subtitle.className = "menu-subtitle";
        menu.appendChild(subtitle);

        // Only process the first item in each group
        if (group.screens && group.screens.length > 0) {
            const screen = group.screens[0]; // Only the first item
            const container = document.createElement("div");
            container.className = "menu-item";

            const link = document.createElement("a");
            link.href = `/mappingtool/v2/pages/${screen.id}.html`;
            link.target = "_blank"; // Opens the link in a new tab
            link.textContent = screen.name;

            const description = document.createElement("p");
            description.textContent = screen.description;

            container.appendChild(link);
            container.appendChild(description);
            menu.appendChild(container);
        }
    });

    console.log("Menu generated successfully:", menu.innerHTML);
}

// Initialize Menu on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM fully loaded. Initializing menu...");
    generateMenu();
});
