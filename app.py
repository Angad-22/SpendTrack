import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

from database.db import get_db, init_db, seed_db
from database.queries import (
    get_category_breakdown,
    get_recent_transactions,
    get_summary_stats,
    get_user_by_id,
)

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()

# Routes

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html", error="All fields are required", name=name, email=email)

    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters", name=name, email=email)

    from werkzeug.security import generate_password_hash
    password_hash = generate_password_hash(password)

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists", name=name, email=email)
    finally:
        conn.close()

    return redirect(url_for("login", registered=1))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="Invalid email or password")

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    from werkzeug.security import check_password_hash
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password")

    session["user_id"] = user["id"]
    return redirect(url_for("landing", login=1))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # ── USER INFO ─────────────────────────────────────────────────────────────
    user = get_user_by_id(user_id)
    # ── END USER INFO ─────────────────────────────────────────────────────────

    # ── SUMMARY STATS ─────────────────────────────────────────────────────────
    stats = get_summary_stats(user_id)
    # ── END SUMMARY STATS ─────────────────────────────────────────────────────

    # ── TRANSACTION HISTORY ───────────────────────────────────────────────────
    transactions = get_recent_transactions(user_id)
    # ── END TRANSACTION HISTORY ───────────────────────────────────────────────

    # ── CATEGORY BREAKDOWN ────────────────────────────────────────────────────
    categories = get_category_breakdown(user_id)
    # ── END CATEGORY BREAKDOWN ────────────────────────────────────────────────

    return render_template("profile.html", user=user, stats=stats, transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
