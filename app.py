import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for

from database.db import get_db, init_db, seed_db

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

    user = {
        "name": "Priya Sharma",
        "email": "priya@example.com",
        "member_since": "April 2025",
    }

    stats = {
        "total_spent": "₹8,600.00",
        "transaction_count": 8,
        "top_category": "Bills",
    }

    transactions = [
        {"date": "20 Apr 2025", "description": "Groceries",        "category": "Food",          "amount": "₹380.00"},
        {"date": "18 Apr 2025", "description": "Misc",             "category": "Other",         "amount": "₹300.00"},
        {"date": "15 Apr 2025", "description": "New shoes",        "category": "Shopping",      "amount": "₹1,500.00"},
        {"date": "12 Apr 2025", "description": "Movie tickets",    "category": "Entertainment", "amount": "₹650.00"},
        {"date": "10 Apr 2025", "description": "Pharmacy",         "category": "Health",        "amount": "₹800.00"},
        {"date": "07 Apr 2025", "description": "Electricity bill", "category": "Bills",         "amount": "₹2,400.00"},
        {"date": "05 Apr 2025", "description": "Auto rickshaw",    "category": "Transport",     "amount": "₹120.00"},
        {"date": "03 Apr 2025", "description": "Lunch with team",  "category": "Food",          "amount": "₹450.00"},
    ]

    categories = [
        {"name": "Bills",         "amount": "₹2,400.00", "pct": 28},
        {"name": "Shopping",      "amount": "₹1,500.00", "pct": 17},
        {"name": "Food",          "amount": "₹830.00",   "pct": 10},
        {"name": "Health",        "amount": "₹800.00",   "pct":  9},
        {"name": "Entertainment", "amount": "₹650.00",   "pct":  8},
        {"name": "Other",         "amount": "₹300.00",   "pct":  3},
        {"name": "Transport",     "amount": "₹120.00",   "pct":  1},
    ]

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
