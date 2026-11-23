// Switch between dashboard sections
function showSection(sectionId, clickedBtn = null) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(sec => sec.classList.remove('active'));

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Update active state in sidebar navigation
    const navItems = document.querySelectorAll('.sidebar-menu .nav-item');
    navItems.forEach(item => item.classList.remove('active'));

    if (clickedBtn) {
        clickedBtn.classList.add('active');
    } else {
        const matchingBtn = document.querySelector(`.sidebar-menu .nav-item[onclick*="${sectionId}"]`);
        if (matchingBtn) matchingBtn.classList.add('active');
    }

    // Update Topbar Title dynamically
    const titles = {
        'overviewSection': 'Dashboard Overview',
        'myProjectsSection': 'My Submitted Projects',
        'uploadSection': 'Upload & Submit Project',
        'pendingReviewsSection': 'Review Student Submissions',
        'evaluatedSection': 'Evaluated Project History',
        'profileSection': 'Profile Details'
    };

    const heading = document.getElementById('pageHeading');
    if (heading && titles[sectionId]) {
        heading.textContent = titles[sectionId];
    }
}

// Auto-dismiss alert popups after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });
});