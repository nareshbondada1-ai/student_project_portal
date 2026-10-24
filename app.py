import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from db import query_one, query_all, execute_commit

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key_98765")

# Upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
ALLOWED_EXTENSIONS = {"pdf", "zip", "doc", "docx"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    if "user_id" in session:
        if session.get("role") == "STUDENT":
            return redirect(url_for("student_dashboard"))
        elif session.get("role") == "ADMIN":
            return redirect(url_for("admin_dashboard"))
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    role = request.form.get("role", "STUDENT").strip().upper()
    full_name = request.form.get("full_name", "").strip()
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone_no = request.form.get("phone_no", "").strip()
    raw_password = request.form.get("password", "")
    course = request.form.get("course", "").strip()
    dob = request.form.get("dob")
    gender = request.form.get("gender")
    roll_no = request.form.get("roll_no", "").strip() if role == "STUDENT" else None
    terms_accepted = request.form.get("terms_accepted", "Y")

    existing = query_one(
        "SELECT user_id FROM USERS WHERE username = %s OR email = %s",
        (username, email)
    )
    if existing:
        flash("Username or Email is already registered!", "danger")
        return redirect(url_for("home"))

    hashed_pw = generate_password_hash(raw_password)

    sql = """
        INSERT INTO USERS (
            USERNAME, EMAIL, PASSWORD, FULL_NAME, PHONE_NO,
            ROLE, ROLL_NO, COURSE, DOB, GENDER, TERMS_ACCEPTED
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    execute_commit(sql, (
        username, email, hashed_pw, full_name, phone_no,
        role, roll_no, course, dob, gender, terms_accepted
    ))

    # Auto-login newly registered user
    new_user = query_one("SELECT user_id, username, full_name, role FROM USERS WHERE username = %s", (username,))
    if new_user:
        session["user_id"] = new_user["user_id"]
        session["username"] = new_user["username"]
        session["full_name"] = new_user["full_name"]
        session["role"] = new_user["role"]
        
        if new_user["role"] == "STUDENT":
            return redirect(url_for("student_dashboard"))
        else:
            return redirect(url_for("admin_dashboard"))

    flash("Registration successful! Please login.", "success")
    return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    identifier = request.form.get("identifier", "").strip()
    password = request.form.get("password", "")
    requested_role = request.form.get("role", "STUDENT").strip().upper()

    user = query_one(
        "SELECT * FROM USERS WHERE (LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s)) AND role = %s",
        (identifier, identifier, requested_role)
    )

    if not user or not check_password_hash(user["password"], password):
        flash("Invalid username/email or password!", "danger")
        return redirect(url_for("home"))

    session["user_id"] = user["user_id"]
    session["username"] = user["username"]
    session["full_name"] = user["full_name"]
    session["role"] = user["role"]

    if user["role"] == "STUDENT":
        return redirect(url_for("student_dashboard"))
    else:
        return redirect(url_for("admin_dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/student/dashboard")
def student_dashboard():
    if "user_id" not in session or session.get("role") != "STUDENT":
        flash("Please log in as a student.", "warning")
        return redirect(url_for("home"))

    student_id = session["user_id"]
    student = query_one("SELECT * FROM USERS WHERE user_id = %s", (student_id,))

    projects_sql = """
        SELECT p.*, r.rating, r.feedback, r.reviewed_at, u.full_name AS reviewer_name
        FROM PROJECTS p
        LEFT JOIN PROJECT_REVIEWS r ON p.project_id = r.project_id
        LEFT JOIN USERS u ON r.admin_id = u.user_id
        WHERE p.student_id = %s
        ORDER BY p.submitted_at DESC
    """
    projects = query_all(projects_sql, (student_id,))

    total = len(projects)
    approved = sum(1 for p in projects if p["status"] == "APPROVED")
    pending = sum(1 for p in projects if p["status"] == "PENDING")
    
    ratings = [float(p["rating"]) for p in projects if p.get("rating") is not None]
    avg_rating = round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    return render_template(
        "student_dashboard.html",
        student=student,
        projects=projects,
        total=total,
        approved=approved,
        pending=pending,
        avg_rating=avg_rating
    )


@app.route("/student/upload-project", methods=["POST"])
def upload_project():
    if "user_id" not in session or session.get("role") != "STUDENT":
        return redirect(url_for("home"))

    student_id = session["user_id"]
    title = request.form.get("title", "").strip()
    tech_stack = request.form.get("tech_stack", "").strip()
    project_link = request.form.get("project_link", "").strip()
    description = request.form.get("description", "").strip()

    doc_file = request.files.get("document")
    doc_filename = None
    if doc_file and allowed_file(doc_file.filename):
        safe_name = secure_filename(f"std_{student_id}_{doc_file.filename}")
        doc_file.save(os.path.join(app.config["UPLOAD_FOLDER"], safe_name))
        doc_filename = safe_name

    sql = """
        INSERT INTO PROJECTS (
            STUDENT_ID, TITLE, DESCRIPTION, TECH_STACK, PROJECT_LINK, DOCUMENT_PATH, STATUS
        ) VALUES (%s, %s, %s, %s, %s, %s, 'PENDING')
    """
    execute_commit(sql, (student_id, title, description, tech_stack, project_link, doc_filename))

    flash("Project submitted successfully for faculty review!", "success")
    return redirect(url_for("student_dashboard"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Please log in as faculty.", "warning")
        return redirect(url_for("home"))

    admin_id = session["user_id"]
    admin = query_one("SELECT * FROM USERS WHERE user_id = %s", (admin_id,))

    pending_sql = """
        SELECT p.*, u.full_name AS student_name, u.roll_no, u.course
        FROM PROJECTS p
        JOIN USERS u ON p.student_id = u.user_id
        WHERE p.status = 'PENDING'
        ORDER BY p.submitted_at ASC
    """
    pending_projects = query_all(pending_sql)

    evaluated_sql = """
        SELECT p.*, u.full_name AS student_name, u.roll_no,
               r.rating, r.feedback, r.reviewed_at
        FROM PROJECTS p
        JOIN USERS u ON p.student_id = u.user_id
        JOIN PROJECT_REVIEWS r ON p.project_id = r.project_id
        WHERE r.admin_id = %s
        ORDER BY r.reviewed_at DESC
    """
    evaluated_projects = query_all(evaluated_sql, (admin_id,))

    total_submissions = len(pending_projects) + len(evaluated_projects)
    approved_count = sum(1 for p in evaluated_projects if p["status"] == "APPROVED")

    ratings = [float(p["rating"]) for p in evaluated_projects if p.get("rating") is not None]
    avg_awarded = round(sum(ratings) / len(ratings), 1) if ratings else 0.0

    return render_template(
        "admin_dashboard.html",
        admin=admin,
        pending_projects=pending_projects,
        evaluated_projects=evaluated_projects,
        total_submissions=total_submissions,
        approved_count=approved_count,
        avg_awarded=avg_awarded
    )


@app.route("/admin/evaluate", methods=["POST"])
def evaluate_project():
    if "user_id" not in session or session.get("role") != "ADMIN":
        return redirect(url_for("home"))

    admin_id = session["user_id"]
    project_id = request.form.get("project_id")
    status = request.form.get("status", "APPROVED").strip().upper()
    rating = float(request.form.get("rating", 4.0))
    feedback = request.form.get("feedback", "").strip()

    execute_commit(
        "UPDATE PROJECTS SET STATUS = %s WHERE PROJECT_ID = %s",
        (status, project_id)
    )

    review_sql = """
        INSERT INTO PROJECT_REVIEWS (PROJECT_ID, ADMIN_ID, RATING, FEEDBACK, REVIEWED_AT)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (PROJECT_ID) DO UPDATE SET
            RATING = EXCLUDED.RATING,
            FEEDBACK = EXCLUDED.FEEDBACK,
            ADMIN_ID = EXCLUDED.ADMIN_ID,
            REVIEWED_AT = CURRENT_TIMESTAMP
    """
    execute_commit(review_sql, (project_id, admin_id, rating, feedback))

    flash("Project evaluation and rating saved successfully!", "success")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)