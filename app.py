"""
GenBridge – backend (Python + Flask)
Pages are rendered from templates/, data comes from genbridge.db (SQLite).
"""
import os
import re
import sqlite3
from flask import Flask, jsonify, request, render_template, redirect, url_for, abort

app = Flask(__name__)
# Full path to the database, so it works on the computer AND on the hosting server
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genbridge.db")

# Google Analytics 4 Measurement ID – paste yours here on Friday (looks like "G-ABC123XYZ")
GA_ID = "G-86DMMSYZN9"


def get_db():
    """Open the database. row_factory lets us use column names: row["title"]."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.context_processor
def add_ga_id():
    """Makes GA_ID available in every template (used in base.html)."""
    return {"ga_id": GA_ID}


def find_job(text):
    """Search a job by part of its title (case-insensitive)."""
    conn = get_db()
    row = conn.execute(
        "SELECT title, trend, rank, related FROM jobs WHERE LOWER(title) LIKE LOWER(?)",
        (f"%{text}%",),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ======================= PAGES (front-end) =======================

@app.route("/")
def home():
    conn = get_db()
    mentor_count = conn.execute("SELECT COUNT(*) FROM mentors").fetchone()[0]
    conn.close()
    return render_template("index.html", mentor_count=mentor_count)


@app.route("/trends")
def trends():
    return render_template("trends.html")


@app.route("/check")
def check():
    job = request.args.get("job", "").strip()
    result = find_job(job) if job else None
    return render_template("check.html", job=job, result=result)


@app.route("/mentors")
def mentors():
    conn = get_db()
    rows = conn.execute("SELECT * FROM mentors ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("mentors.html", mentors=rows)


@app.route("/join", methods=["GET", "POST"])
def join():
    errors, form = [], {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ["name", "email", "field", "years", "topics"]}
        # --- server-side validation ---
        if not form["name"]:
            errors.append("Please enter your name.")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", form["email"]):
            errors.append("Please enter a valid e-mail.")
        if not form["field"]:
            errors.append("Please enter your field of experience.")
        if not form["years"].isdigit() or not (1 <= int(form["years"]) <= 70):
            errors.append("Years of experience must be a number from 1 to 70.")
        if not errors:
            conn = get_db()
            conn.execute(
                "INSERT INTO mentors (name, email, field, years, topics) VALUES (?, ?, ?, ?, ?)",
                (form["name"], form["email"], form["field"], int(form["years"]), form["topics"]),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("thanks", kind="mentor"))
    return render_template("join.html", errors=errors, form=form)


@app.route("/request/<int:mentor_id>", methods=["GET", "POST"])
def request_session(mentor_id):
    conn = get_db()
    mentor = conn.execute("SELECT * FROM mentors WHERE id = ?", (mentor_id,)).fetchone()
    conn.close()
    if mentor is None:
        abort(404)
    errors, form = [], {}
    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in ["name", "email", "message"]}
        if not form["name"]:
            errors.append("Please enter your name.")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", form["email"]):
            errors.append("Please enter a valid e-mail.")
        if not errors:
            conn = get_db()
            conn.execute(
                "INSERT INTO requests (mentor_id, name, email, message) VALUES (?, ?, ?, ?)",
                (mentor_id, form["name"], form["email"], form["message"]),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("thanks", kind="request"))
    return render_template("request.html", mentor=mentor, errors=errors, form=form)


@app.route("/thanks/<kind>")
def thanks(kind):
    if kind not in ("mentor", "request"):
        abort(404)
    return render_template("thanks.html", kind=kind)


# ======================= API (JSON for JavaScript) =======================

@app.route("/api/jobs")
def api_jobs():
    conn = get_db()
    rows = conn.execute("SELECT title, trend, rank FROM jobs ORDER BY trend, rank").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/check")
def api_check():
    job = request.args.get("job", "").strip()
    if not job:
        return jsonify({"error": "Please type a job title"}), 400
    result = find_job(job)
    if result is None:
        return jsonify({"job": job, "trend": "unknown"})
    return jsonify(result)


@app.route("/api/stats")
def api_stats():
    """Small summary of our own data – useful for the report."""
    conn = get_db()
    stats = {
        "mentors": conn.execute("SELECT COUNT(*) FROM mentors").fetchone()[0],
        "requests": conn.execute("SELECT COUNT(*) FROM requests").fetchone()[0],
        "jobs_in_database": conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0],
    }
    conn.close()
    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True)
