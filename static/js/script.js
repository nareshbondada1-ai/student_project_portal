// Toggle between Main Tabs (Login vs Register)
function switchMainTab(tab) {
    const loginSection = document.getElementById("loginSection");
    const registerSection = document.getElementById("registerSection");
    const tabLoginBtn = document.getElementById("tabLoginBtn");
    const tabRegisterBtn = document.getElementById("tabRegisterBtn");

    if (tab === "login") {
        loginSection.classList.add("active");
        registerSection.classList.remove("active");
        tabLoginBtn.classList.add("active");
        tabRegisterBtn.classList.remove("active");
    } else {
        loginSection.classList.remove("active");
        registerSection.classList.add("active");
        tabLoginBtn.classList.remove("active");
        tabRegisterBtn.classList.add("active");
    }
}

// Toggle between Student & Admin Login
function switchLoginRole(role) {
    const studentBtn = document.getElementById("studentLoginTab");
    const adminBtn = document.getElementById("adminLoginTab");
    const loginRoleInput = document.getElementById("loginRole");
    const loginSubmitBtn = document.getElementById("loginSubmitBtn");

    loginRoleInput.value = role;

    if (role === "STUDENT") {
        studentBtn.classList.add("active");
        adminBtn.classList.remove("active");
        loginSubmitBtn.textContent = "Login as Student";
    } else {
        adminBtn.classList.add("active");
        studentBtn.classList.remove("active");
        loginSubmitBtn.textContent = "Login as Admin / Professor";
    }
}

// Automatically show/hide Roll No based on Register Role
function toggleStudentFields(role) {
    const rollNoGroup = document.getElementById("rollNoGroup");
    const regRollNo = document.getElementById("regRollNo");
    const courseLabel = document.getElementById("courseLabel");

    if (role === "ADMIN") {
        rollNoGroup.style.display = "none";
        regRollNo.removeAttribute("required");
        courseLabel.innerHTML = 'Department <span class="required">*</span>';
    } else {
        rollNoGroup.style.display = "block";
        regRollNo.setAttribute("required", "required");
        courseLabel.innerHTML = 'Course <span class="required">*</span>';
    }
}