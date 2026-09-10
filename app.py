import os
import re
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "portal.db"
UPLOAD_DIR = ROOT / "database" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def row_to_dict(row):
    return dict(row) if row else None


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    conn.executescript((ROOT / "database" / "schema.sql").read_text(encoding="utf-8"))
    count = conn.execute("SELECT COUNT(*) FROM services").fetchone()[0]
    if count == 0:
        services = [
            ("Income Certificate", "Certificates", "Request an income certificate.", "Active"),
            ("Residence Certificate", "Certificates", "Request proof of residence.", "Active"),
            ("Birth Certificate Support", "Certificates", "Access birth certificate guidance and submission support.", "Active"),
            ("Document Verification", "Appointments", "Book an in-person verification slot.", "Active"),
        ]
        conn.executemany("INSERT INTO services(name, category, description, status) VALUES (?, ?, ?, ?)", services)
    demo_email = "demo@citizen.local"
    if not conn.execute("SELECT 1 FROM users WHERE email = ?", (demo_email,)).fetchone():
        user_id = conn.execute(
            "INSERT INTO users(name, email, password_hash, phone, role, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("Demo Citizen", demo_email, generate_password_hash("Demo@12345"), "0000000000", "citizen", now()),
        ).lastrowid
        service_id = conn.execute("SELECT id FROM services ORDER BY id LIMIT 1").fetchone()[0]
        app_no = "DCS-2026-001"
        conn.execute(
            "INSERT INTO applications(user_id, service_id, application_number, status, submitted_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, service_id, app_no, "Document Verification", now(), now()),
        )
        conn.execute(
            "INSERT INTO notifications(user_id, title, message, is_read, created_at) VALUES (?, ?, ?, 0, ?)",
            (user_id, "Welcome", "Your demo citizen account is ready for testing.", now()),
        )
    conn.commit()
    conn.close()


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required"}), 401
        return fn(*args, **kwargs)
    return wrapper


def valid_email(value):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value or ""))


def json_error(message, code=400):
    return jsonify({"error": message}), code


@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PATCH,OPTIONS"
    return response


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Digital Citizen Service Portal API"})


@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name, email, password = data.get("name", "").strip(), data.get("email", "").strip().lower(), data.get("password", "")
    if len(name) < 2 or not valid_email(email) or len(password) < 8:
        return json_error("Provide a valid name, email, and password of at least 8 characters.")
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO users(name, email, password_hash, phone, role, created_at) VALUES (?, ?, ?, ?, 'citizen', ?)",
            (name, email, generate_password_hash(password), data.get("phone", "").strip(), now()),
        )
        user_id = cur.lastrowid
        conn.execute("INSERT INTO notifications(user_id, title, message, is_read, created_at) VALUES (?, ?, ?, 0, ?)", (user_id, "Account created", "Your citizen account was created successfully.", now()))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return json_error("An account with this email already exists.", 409)
    conn.close()
    session["user_id"] = user_id
    return jsonify({"message": "Registration successful", "user": {"id": user_id, "name": name, "email": email}}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email, password = data.get("email", "").strip().lower(), data.get("password", "")
    conn = get_db()
    user = conn.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if not user or not check_password_hash(user["password_hash"], password):
        return json_error("Invalid email or password.", 401)
    session["user_id"] = user["id"]
    return jsonify({"message": "Login successful", "user": {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}})


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/api/services")
def services():
    conn = get_db()
    rows = conn.execute("SELECT id, name, category, description, status FROM services WHERE status = 'Active' ORDER BY id").fetchall()
    conn.close()
    return jsonify({"services": [row_to_dict(r) for r in rows]})


@app.route("/api/services/<int:service_id>")
def service(service_id):
    conn = get_db()
    row = conn.execute("SELECT id, name, category, description, status FROM services WHERE id = ?", (service_id,)).fetchone()
    conn.close()
    return (jsonify(row_to_dict(row)) if row else json_error("Service not found", 404))


@app.route("/api/applications", methods=["GET", "POST"])
@require_auth
def applications():
    conn = get_db()
    user_id = session["user_id"]
    if request.method == "GET":
        rows = conn.execute("""SELECT a.id, a.application_number, a.status, a.submitted_at, a.updated_at, s.name AS service_name
                              FROM applications a JOIN services s ON s.id=a.service_id
                              WHERE a.user_id=? ORDER BY a.updated_at DESC""", (user_id,)).fetchall()
        conn.close()
        return jsonify({"applications": [row_to_dict(r) for r in rows]})
    data = request.get_json(silent=True) or {}
    service_id = data.get("service_id")
    if not isinstance(service_id, int):
        return json_error("service_id must be an integer")
    service = conn.execute("SELECT id FROM services WHERE id=? AND status='Active'", (service_id,)).fetchone()
    if not service:
        conn.close(); return json_error("Service not found", 404)
    app_no = f"DCS-{datetime.now().year}-{conn.execute('SELECT COALESCE(MAX(id),0)+1 FROM applications').fetchone()[0]:03d}"
    timestamp = now()
    cur = conn.execute("INSERT INTO applications(user_id, service_id, application_number, status, submitted_at, updated_at) VALUES (?, ?, ?, 'Submitted', ?, ?)", (user_id, service_id, app_no, timestamp, timestamp))
    conn.execute("INSERT INTO notifications(user_id, application_id, title, message, is_read, created_at) VALUES (?, ?, ?, ?, 0, ?)", (user_id, cur.lastrowid, "Application submitted", f"Application {app_no} has been submitted.", timestamp))
    conn.commit(); conn.close()
    return jsonify({"message": "Application submitted", "application_number": app_no}), 201


@app.route("/api/applications/track/<application_number>")
def track(application_number):
    conn = get_db()
    row = conn.execute("""SELECT a.application_number, a.status, a.submitted_at, a.updated_at, s.name AS service_name
                          FROM applications a JOIN services s ON s.id=a.service_id WHERE a.application_number=?""", (application_number.strip(),)).fetchone()
    conn.close()
    if not row: return json_error("Application not found", 404)
    statuses = ["Submitted", "Under Review", "Document Verification", "Approved"]
    current = row["status"]
    current_index = statuses.index(current) if current in statuses else 0
    return jsonify({"application": row_to_dict(row), "timeline": [{"label": s, "completed": i <= current_index, "active": i == current_index} for i, s in enumerate(statuses)]})


@app.route("/api/applications/<int:application_id>")
@require_auth
def application_detail(application_id):
    conn = get_db()
    row = conn.execute("SELECT a.id, a.application_number, a.status, a.submitted_at, a.updated_at, s.name AS service_name FROM applications a JOIN services s ON s.id=a.service_id WHERE a.id=? AND a.user_id=?", (application_id, session["user_id"])).fetchone()
    conn.close()
    return (jsonify(row_to_dict(row)) if row else json_error("Application not found", 404))


@app.route("/api/appointments", methods=["GET", "POST"])
@require_auth
def appointments():
    conn = get_db(); user_id = session["user_id"]
    if request.method == "GET":
        rows = conn.execute("SELECT id, department, appointment_date, appointment_time, status, created_at FROM appointments WHERE user_id=? ORDER BY appointment_date, appointment_time", (user_id,)).fetchall()
        conn.close(); return jsonify({"appointments": [row_to_dict(r) for r in rows]})
    data = request.get_json(silent=True) or {}
    department, date, time = data.get("department", "").strip(), data.get("date", "").strip(), data.get("time", "").strip()
    if not department or not date or not time: conn.close(); return json_error("Department, date and time are required")
    timestamp = now()
    cur = conn.execute("INSERT INTO appointments(user_id, department, appointment_date, appointment_time, status, created_at) VALUES (?, ?, ?, ?, 'Confirmed', ?)", (user_id, department, date, time, timestamp))
    conn.execute("INSERT INTO notifications(user_id, title, message, is_read, created_at) VALUES (?, ?, ?, 0, ?)", (user_id, "Appointment confirmed", f"Your {department} appointment is confirmed for {date} at {time}.", timestamp))
    conn.commit(); conn.close()
    return jsonify({"message": "Appointment confirmed", "appointment_id": cur.lastrowid}), 201


@app.route("/api/documents", methods=["GET", "POST"])
@require_auth
def documents():
    conn = get_db(); user_id = session["user_id"]
    if request.method == "GET":
        rows = conn.execute("SELECT d.id, d.filename, d.document_type, d.status, d.uploaded_at FROM documents d WHERE d.user_id=? ORDER BY d.uploaded_at DESC", (user_id,)).fetchall()
        conn.close(); return jsonify({"documents": [row_to_dict(r) for r in rows]})
    file = request.files.get("file")
    if not file or not file.filename: conn.close(); return json_error("A document file is required")
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS: conn.close(); return json_error("Only PDF, PNG, JPG and JPEG files are allowed")
    safe_name = secure_filename(file.filename)
    stored = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{safe_name}"
    file.save(UPLOAD_DIR / stored)
    timestamp = now()
    cur = conn.execute("INSERT INTO documents(user_id, filename, document_type, storage_path, status, uploaded_at) VALUES (?, ?, ?, ?, 'Uploaded', ?)", (user_id, safe_name, data_type := request.form.get("document_type", "General"), str(Path("database/uploads") / stored), timestamp))
    conn.commit(); conn.close()
    return jsonify({"message": "Document uploaded", "document_id": cur.lastrowid, "status": "Uploaded"}), 201


@app.route("/api/notifications")
@require_auth
def notifications():
    conn = get_db(); rows = conn.execute("SELECT id, title, message, is_read, created_at FROM notifications WHERE user_id=? ORDER BY created_at DESC", (session["user_id"],)).fetchall(); conn.close()
    return jsonify({"notifications": [row_to_dict(r) for r in rows]})


@app.route("/api/notifications/<int:notification_id>/read", methods=["PATCH"])
@require_auth
def mark_read(notification_id):
    conn = get_db(); cur = conn.execute("UPDATE notifications SET is_read=1 WHERE id=? AND user_id=?", (notification_id, session["user_id"])); conn.commit(); conn.close()
    return (jsonify({"message": "Notification marked as read"}) if cur.rowcount else json_error("Notification not found", 404))


@app.route("/api/me")
@require_auth
def me():
    conn = get_db(); row = conn.execute("SELECT id, name, email, phone, role, created_at FROM users WHERE id=?", (session["user_id"],)).fetchone(); conn.close()
    return jsonify({"user": row_to_dict(row)})


@app.errorhandler(413)
def too_large(_):
    return json_error("File is too large. Maximum size is 5 MB.", 413)


@app.route("/api/<path:unknown>", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
def not_found(unknown):
    return json_error(f"API route /api/{unknown} was not found", 404)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
