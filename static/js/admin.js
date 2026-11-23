// =========================================================
// FACULTY DASHBOARD - MODAL & LIVE SEARCH CONTROLLER
// =========================================================

// Open Faculty Review Modal with Project Details & Hidden Project ID
function openReviewModal(projectId, title, student, roll, stack, desc) {
    const modal = document.getElementById('reviewModal');
    if (!modal) return;

    document.getElementById('modalProjectId').value = projectId || '';
    document.getElementById('modalProjectTitle').textContent = title || 'Project Title';
    document.getElementById('modalStudentName').textContent = student || 'Unknown Student';
    document.getElementById('modalStudentRoll').textContent = roll || 'N/A';
    document.getElementById('modalProjectStack').textContent = stack || 'Not Specified';
    document.getElementById('modalProjectDesc').textContent = desc || 'No description provided.';

    modal.classList.add('active');
}

// Close Review Modal
function closeReviewModal() {
    const modal = document.getElementById('reviewModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking on the dark backdrop
window.addEventListener('click', (event) => {
    const modal = document.getElementById('reviewModal');
    if (event.target === modal) {
        closeReviewModal();
    }
});

// Live Instant Search for Pending Submissions
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('facultySearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            const projectCards = document.querySelectorAll('#pendingReviewsSection .project-detail-card');
            
            projectCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});