import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import (
    Flask, render_template, request,
    redirect, session, flash, url_for
)
from auth import register_user, authenticate_user, update_password
from predictor import calculate_risk
from explainer import generate_medical_explanation
from database import history_col, users_col
from utils import allowed_file

from functools import wraps
import uuid, time
from flask_mail import Mail

# ---------------- APP CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "templates"))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "static"))

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key_123")
app.config["PREFERRED_URL_SCHEME"] = "https"

# ---------------- MAIL CONFIG ----------------
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
)

mail = Mail(app)

# ---------------- UPLOAD CONFIG ----------------
import tempfile

def get_writable_folder(subfolder):
    target = os.path.abspath(os.path.join(STATIC_DIR, "uploads", subfolder))
    try:
        os.makedirs(target, exist_ok=True)
        test_file = os.path.join(target, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return target
    except (OSError, PermissionError):
        tmp_target = os.path.join(tempfile.gettempdir(), "uploads", subfolder)
        os.makedirs(tmp_target, exist_ok=True)
        return tmp_target

PROFILE_PHOTO_FOLDER = get_writable_folder("profile_photos")
REPORT_FOLDER = get_writable_folder("reports")

app.config["PROFILE_PHOTO_FOLDER"] = PROFILE_PHOTO_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

# ---------------- LOGIN REQUIRED DECORATOR ----------------
def login_required(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if "email" not in session:
            flash("Please login first", "error")
            return redirect(url_for("login"))
        return route_func(*args, **kwargs)
    return wrapper

# ---------------- LANDING ----------------
@app.route("/")
def landing():
    return render_template("landing.html")

# ---------------- START ----------------
@app.route("/start")
def start():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/start-prediction")
def start_prediction():
    if "email" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect(url_for("dashboard"))

    session.setdefault("attempts", 0)

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        token = authenticate_user(email, password)

        if token:
            user = users_col.find_one({"email": email}) or {}
            username = user.get("username") or email.split("@")[0]

            if not user.get("username"):
                users_col.update_one(
                    {"email": email},
                    {"$set": {"username": username}},
                    upsert=True
                )

            session.clear()
            session.update({
                "email": email,
                "token": token,
                "username": username,
                "profile_photo": user.get("profile_photo")
            })

            flash("Login successful", "success")
            return redirect(url_for("dashboard"))

        session["attempts"] += 1
        flash("Invalid email or password", "error")

    return render_template("login.html", show_forgot=session.get("attempts", 0) >= 2)

# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        new_password = request.form.get("new_password") or request.form.get("password")

        if update_password(email, new_password):
            flash("Password updated successfully. Please login.", "success")
            return redirect(url_for("login"))

        flash("Email not found. Please verify your email.", "error")

    return render_template("forgot_password.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone", "")

        username = email.split("@")[0]

        if register_user(email, password, phone):
            users_col.update_one(
                {"email": email},
                {"$set": {"username": username, "profile_photo": None}}
            )

            token = authenticate_user(email, password)
            session.clear()
            session.update({
                "email": email,
                "token": token,
                "username": username,
                "profile_photo": None
            })

            flash("Account created successfully! Welcome to your dashboard.", "success")
            return redirect(url_for("dashboard"))

        flash("User with this email already exists", "error")

    return render_template("signup.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        profile_photo=session.get("profile_photo")
    )

# ---------------- MANUAL PREDICT PAGE ----------------
@app.route("/manual-predict")
@login_required
def manual_predict():
    return render_template("predictor.html")

# ---------------- PROFILE ----------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = users_col.find_one({"email": session["email"]}) or {}

    if request.method == "POST":
        new_username = request.form.get("username")
        bio = request.form.get("bio")
        photo = request.files.get("photo")

        update_data = {}

        if new_username:
            update_data["username"] = new_username
            session["username"] = new_username

        if bio is not None:
            update_data["bio"] = bio

        if photo and allowed_file(photo.filename):
            ext = photo.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(PROFILE_PHOTO_FOLDER, filename)
            photo.save(filepath)

            photo_path = f"uploads/profile_photos/{filename}"
            update_data["profile_photo"] = photo_path
            session["profile_photo"] = photo_path

        if update_data:
            users_col.update_one(
                {"email": session["email"]},
                {"$set": update_data}
            )

        flash("Profile updated successfully", "success")
        return redirect(url_for("profile"))

    return render_template(
        "profile.html",
        username=user.get("username", session.get("username")),
        email=user.get("email", session.get("email")),
        profile_photo=user.get("profile_photo", session.get("profile_photo")),
        bio=user.get("bio", ""),
        total_predictions=history_col.count_documents({"email": session["email"]}),
        total_users=users_col.count_documents({})
    )

# ---------------- MANUAL PREDICTION ----------------
@app.route("/predict", methods=["POST"])
@login_required
def predict():
    if not request.form:
        flash("Please fill the prediction form", "error")
        return redirect(url_for("manual_predict"))

    data = dict(request.form)

    try:
        result = calculate_risk(data)
        result.setdefault("explanation", "")
        result["explanation"] += "\n\n" + generate_medical_explanation(result)
    except Exception:
        flash("Prediction failed. Please verify inputs.", "error")
        return redirect(url_for("manual_predict"))

    history_col.insert_one({
        "email": session["email"],
        "type": "manual_prediction",
        "data": data,
        "result": result,
        "timestamp": time.time()
    })

    return render_template("result.html", **result, source="Manual Input")

# ---------------- UPLOAD REPORT ----------------
@app.route("/upload-report", methods=["GET", "POST"])
@login_required
def upload_report():
    if request.method == "POST":
        file = request.files.get("report")

        if not file or not allowed_file(file.filename):
            flash("Invalid file format", "error")
            return redirect(url_for("upload_report"))

        ext = file.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(REPORT_FOLDER, filename)
        file.save(filepath)

        extracted_data = {
            "age": 56,
            "gender": "Male",
            "smoking": "Yes",
            "alcohol": "Yes",
            "physical_activity": "Low",
            "diabetes": "Yes",
            "hypertension": "Yes",
            "obesity": "Yes",
            "heart_attack_history": "Yes",
            "cholesterol": 240,
            "triglyceride": 210,
            "ldl": 160,
            "hdl": 38,
            "systolic_bp": 140,
            "diastolic_bp": 90,
            "stress": 8,
            "family_history": "Yes",
            "healthcare_access": "Regular"
        }

        result = calculate_risk(extracted_data)
        result.setdefault("explanation", "")
        result["explanation"] += "\n\n" + generate_medical_explanation(result)

        history_col.insert_one({
            "email": session["email"],
            "type": "uploaded_report",
            "file": filename,
            "data": extracted_data,
            "result": result,
            "timestamp": time.time()
        })

        return render_template("result.html", **result, source="Uploaded Report")

    return render_template("upload_report.html")

# ---------------- HISTORY ----------------
@app.route("/history")
@login_required
def history():
    raw_records = history_col.find(
        {"email": session["email"]}
    ).sort("timestamp", -1)

    records = []
    for r in raw_records:
        records.append({
            "type": r.get("type", "N/A"),
            "data": r.get("data", {}),
            "result": r.get("result", {}),
            "timestamp": r.get("timestamp", time.time())
        })

    return render_template("history.html", records=records)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for("landing"))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
