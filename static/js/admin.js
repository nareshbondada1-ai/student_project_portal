function openReviewModal(projectId, title, student, roll, stack, desc) {
    document.getElementById('modalProjectId').value = projectId;
    // ... rest of your code
    // Open Review Modal with Project Details
// Open Review Modal with Project Details & Project ID
function openReviewModal(projectId, title, student, roll, stack, desc) {
    document.getElementById('modalProjectId').value = projectId;
    document.getElementById('modalProjectTitle').textContent = title;
    document.getElementById('modalStudentName').textContent = student;
    document.getElementById('modalStudentRoll').textContent = roll;
    document.getElementById('modalProjectStack').textContent = stack;
    document.getElementById('modalProjectDesc').textContent = desc;

    document.getElementById('reviewModal').classList.add('active');
}

// Close Review Modal
function closeReviewModal() {
    document.getElementById('reviewModal').classList.remove('active');
}

// Handle Form Submission (Mock simulation for frontend testing)
function handleEvaluationSubmit(event) {
    event.preventDefault();
    const rating = document.getElementById('ratingInput').value;
    const feedback = document.getElementById('feedbackInput').value;
    const status = document.querySelector('input[name="status"]:checked').value;

    alert(`Evaluation Saved Successfully!\n\nStatus: ${status}\nRating: ${rating}/5.0\nFeedback: ${feedback}`);

    closeReviewModal();
    // In real app, this will submit to Python Flask
}