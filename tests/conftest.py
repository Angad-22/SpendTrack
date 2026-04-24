import pytest
from werkzeug.security import generate_password_hash
from database.db import get_db, init_db


@pytest.fixture
def seeded_db(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test.db")
    monkeypatch.setattr("database.db.DB_PATH", db_file)
    init_db()
    conn = get_db()
    conn.execute(
        "INSERT INTO users (id, name, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
        (1, "Demo User", "demo@spendly.com", generate_password_hash("demo123"), "2026-01-15 10:00:00"),
    )
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        [
            (1, 2400.0, "Bills",         "2026-01-07", "Electricity bill"),
            (1, 1500.0, "Shopping",      "2026-01-15", "New shoes"),
            (1,  800.0, "Health",        "2026-01-10", "Pharmacy"),
            (1,  650.0, "Entertainment", "2026-01-12", "Movie tickets"),
            (1,  450.0, "Food",          "2026-01-03", "Lunch with team"),
            (1,  380.0, "Food",          "2026-01-20", "Groceries"),
            (1,  300.0, "Other",         "2026-01-18", "Misc"),
            (1,  120.0, "Transport",     "2026-01-05", "Auto rickshaw"),
        ],
    )
    conn.commit()
    conn.close()
    return 1  # user_id


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test_empty.db")
    monkeypatch.setattr("database.db.DB_PATH", db_file)
    init_db()
    conn = get_db()
    conn.execute(
        "INSERT INTO users (id, name, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
        (2, "Empty User", "empty@example.com", generate_password_hash("pass"), "2026-02-10 08:00:00"),
    )
    conn.commit()
    conn.close()
    return 2  # user_id
