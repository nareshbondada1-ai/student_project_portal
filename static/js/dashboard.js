// Function to switch between Dashboard tabs
function showSection(sectionId, clickedBtn = null) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(sec => sec.classList.remove('active'));

    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Update Sidebar active state
    if (clickedBtn) {
        const navItems = document.querySelectorAll('.sidebar-menu .nav-item');
        navItems.forEach(item => item.classList.remove('active'));
        clickedBtn.classList.add('active');
    }

    // Update Topbar Title
    const titles = {
        'overviewSection': 'Dashboard Overview',
        'myProjectsSection': 'My Submitted Projects',
        'uploadSection': 'Upload & Submit Project',
        'notificationsSection': 'Notifications & Activity',
        'profileSection': 'Student Profile'
    };
    const heading = document.getElementById('pageHeading');
    if (heading && titles[sectionId]) {
        heading.textContent = titles[sectionId];
    }
}

// Function to Mark Notifications as read
function markAllNotificationsAsRead() {
    const unreadItems = document.querySelectorAll('.notif-item.unread');
    unreadItems.forEach(item => {
        item.classList.remove('unread');
    });

    // Clear notification badge
    const badge = document.getElementById('notifBadge');
    if (badge) {
        badge.style.display = 'none';
    }

    const dot = document.querySelector('.dot-indicator');
    if (dot) {
        dot.style.display = 'none';
    }
}