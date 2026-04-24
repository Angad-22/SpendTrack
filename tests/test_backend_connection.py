import pytest
from database.queries import (
    get_user_by_id,
    get_recent_transactions,
    get_summary_stats,
    get_category_breakdown,
)


# ── USER INFO + TRANSACTION HISTORY ──────────────────────────────────────────

def test_get_user_by_id_valid(seeded_db):
    user = get_user_by_id(seeded_db)
    assert user["name"] == "Demo User"
    assert user["email"] == "demo@spendly.com"
    assert user["member_since"] == "January 2026"


def test_get_user_by_id_not_found(seeded_db):
    assert get_user_by_id(9999) is None


def test_get_recent_transactions_returns_newest_first(seeded_db):
    rows = get_recent_transactions(seeded_db)
    assert len(rows) > 0
    for row in rows:
        assert {"date", "description", "category", "amount"} <= row.keys()
    dates = [r["date"] for r in rows]
    assert dates == sorted(dates, reverse=True)


def test_get_recent_transactions_empty(empty_db):
    assert get_recent_transactions(empty_db) == []


def test_get_recent_transactions_amount_format(seeded_db):
    rows = get_recent_transactions(seeded_db)
    assert all(r["amount"].startswith("₹") for r in rows)


# ── SUMMARY STATS ─────────────────────────────────────────────────────────────

def test_get_summary_stats_total_spent(seeded_db):
    stats = get_summary_stats(seeded_db)
    assert stats["total_spent"] == "₹6,600.00"


def test_get_summary_stats_transaction_count(seeded_db):
    stats = get_summary_stats(seeded_db)
    assert stats["transaction_count"] == 8


def test_get_summary_stats_top_category(seeded_db):
    stats = get_summary_stats(seeded_db)
    assert stats["top_category"] == "Bills"


def test_get_summary_stats_no_expenses(empty_db):
    stats = get_summary_stats(empty_db)
    assert stats == {"total_spent": "₹0.00", "transaction_count": 0, "top_category": "—"}


# ── CATEGORY BREAKDOWN ────────────────────────────────────────────────────────

def test_get_category_breakdown_returns_7_categories(seeded_db):
    cats = get_category_breakdown(seeded_db)
    assert len(cats) == 7


def test_get_category_breakdown_sorted_descending(seeded_db):
    cats = get_category_breakdown(seeded_db)
    assert cats[0]["name"] == "Bills"
    assert cats[-1]["name"] == "Transport"


def test_get_category_breakdown_pct_sums_to_100(seeded_db):
    cats = get_category_breakdown(seeded_db)
    assert sum(c["pct"] for c in cats) == 100


def test_get_category_breakdown_amount_format(seeded_db):
    cats = get_category_breakdown(seeded_db)
    assert all(c["amount"].startswith("₹") for c in cats)


def test_get_category_breakdown_empty(empty_db):
    assert get_category_breakdown(empty_db) == []
