from datetime import datetime
from database.db import get_db


def get_user_by_id(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return None
    member_since = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")
    return {"name": row["name"], "email": row["email"], "member_since": member_since}


def get_recent_transactions(user_id, limit=10):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT date, description, category, amount FROM expenses"
            " WHERE user_id = ? ORDER BY date DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
    finally:
        conn.close()
    result = []
    for row in rows:
        formatted_date = datetime.strptime(row["date"], "%Y-%m-%d").strftime("%d %b %Y")
        result.append({
            "date": formatted_date,
            "description": row["description"],
            "category": row["category"],
            "amount": f"₹{row['amount']:,.2f}",
        })
    return result


def get_summary_stats(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT SUM(amount), COUNT(*) FROM expenses WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        total = row[0] or 0.0
        count = row[1] or 0
        top = conn.execute(
            "SELECT category, SUM(amount) as cat_total FROM expenses WHERE user_id = ?"
            " GROUP BY category ORDER BY cat_total DESC LIMIT 1",
            (user_id,),
        ).fetchone()
    finally:
        conn.close()
    return {
        "total_spent": f"₹{total:,.2f}",
        "transaction_count": count,
        "top_category": top["category"] if top else "—",
    }


def get_category_breakdown(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT category, SUM(amount) as cat_total FROM expenses"
            " WHERE user_id = ? GROUP BY category ORDER BY cat_total DESC",
            (user_id,),
        ).fetchall()
    finally:
        conn.close()
    if not rows:
        return []
    grand_total = sum(row["cat_total"] for row in rows)
    categories = [
        {"name": row["category"], "amount": f"₹{row['cat_total']:,.2f}", "pct": round(row["cat_total"] / grand_total * 100)}
        for row in rows
    ]
    remainder = 100 - sum(c["pct"] for c in categories)
    categories[0]["pct"] += remainder
    return categories
