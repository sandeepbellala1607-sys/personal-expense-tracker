import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-before-deployment"

DB_PATH = Path(__file__).with_name("expenses.db")


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0)
            )
        """)


@app.route("/")
def index():
    with connect_db() as conn:
        expenses = conn.execute("""
            SELECT id, expense_date, category, description, amount
            FROM expenses
            ORDER BY expense_date DESC, id DESC
        """).fetchall()

        total = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        ).fetchone()[0]

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add_expense():
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()
    expense_date = request.form.get("expense_date", "").strip()
    amount_text = request.form.get("amount", "").strip()

    if not category or not description or not expense_date or not amount_text:
        flash("Please fill in all fields.")
        return redirect(url_for("index"))

    try:
        amount = float(amount_text)

        if amount <= 0:
            raise ValueError

        parsed_date = date.fromisoformat(expense_date)

    except ValueError:
        flash("Enter a valid date and an amount greater than zero.")
        return redirect(url_for("index"))

    with connect_db() as conn:
        conn.execute("""
            INSERT INTO expenses
                (expense_date, category, description, amount)
            VALUES (?, ?, ?, ?)
        """, (parsed_date.isoformat(), category, description, amount))

    flash("Expense added successfully!")
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    with connect_db() as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

    if cursor.rowcount:
        flash("Expense deleted successfully.")
    else:
        flash("Expense not found.")

    return redirect(url_for("index"))


create_table()

if __name__ == "__main__":
    app.run(debug=True)

