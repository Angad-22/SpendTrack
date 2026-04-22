import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

DB_PATH = "expense_tracker.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    today = datetime.now()
    month_prefix = today.strftime("%Y-%m")

    expenses = [
        (user_id, 450.0, "Food", f"{month_prefix}-03", "Lunch with team"),
        (user_id, 120.0, "Transport", f"{month_prefix}-05", "Auto rickshaw"),
        (user_id, 2400.0, "Bills", f"{month_prefix}-07", "Electricity bill"),
        (user_id, 800.0, "Health", f"{month_prefix}-10", "Pharmacy"),
        (user_id, 650.0, "Entertainment", f"{month_prefix}-12", "Movie tickets"),
        (user_id, 1500.0, "Shopping", f"{month_prefix}-15", "New shoes"),
        (user_id, 300.0, "Other", f"{month_prefix}-18", "Misc"),
        (user_id, 380.0, "Food", f"{month_prefix}-20", "Groceries"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()
