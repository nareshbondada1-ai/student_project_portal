// Main Frontend JavaScript for Minor Project

document.addEventListener("DOMContentLoaded", () => {
    console.log("[Minor Project] Frontend initialized successfully.");

    // Auto-dismiss flash alerts after 4 seconds
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // Real-time filter for project items
    const searchInput = document.getElementById("searchFilter");
    const itemsContainer = document.getElementById("itemsContainer");

    if (searchInput && itemsContainer) {
        searchInput.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase().trim();
            const itemCards = itemsContainer.querySelectorAll(".item-card");

            itemCards.forEach((card) => {
                const title = card.getAttribute("data-title") || "";
                const desc = card.querySelector(".item-desc")?.textContent.toLowerCase() || "";

                if (title.includes(query) || desc.includes(query)) {
                    card.style.display = "flex";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }

    // Client-side validation on item form
    const itemForm = document.getElementById("itemForm");
    if (itemForm) {
        itemForm.addEventListener("submit", (e) => {
            const titleInput = document.getElementById("title");
            if (!titleInput.value.trim()) {
                e.preventDefault();
                alert("Please provide an item title.");
                titleInput.focus();
            }
        });
    }
});
