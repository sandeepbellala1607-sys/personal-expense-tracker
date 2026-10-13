import sqlite3
from datetime import date

DB_NAME = "expenses.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


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


def add_expense():
    print("\n--- Add Expense ---")

    category = input("Category: ").strip()
    description = input("Description: ").strip()

    if not category or not description:
        print("Category and description are required.")
        return

    try:
        amount = float(input("Amount in rupees: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    with connect_db() as conn:
        conn.execute(
            """
            INSERT INTO expenses
                (expense_date, category, description, amount)
            VALUES (?, ?, ?, ?)
            """,
            (date.today().isoformat(), category, description, amount)
        )

    print("Expense saved successfully!")


def view_expenses():
    with connect_db() as conn:
        rows = conn.execute("""
            SELECT id, expense_date, category, description, amount
            FROM expenses
            ORDER BY expense_date DESC, id DESC
        """).fetchall()

    if not rows:
        print("No expenses recorded.")
        return

    print("\n--- All Expenses ---")

    for row in rows:
        expense_id, expense_date, category, description, amount = row

        print(
            f"ID: {expense_id} | {expense_date} | {category} | "
            f"{description} | ₹{amount:.2f}"
        )


def show_total():
    with connect_db() as conn:
        result = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses"
        ).fetchone()

    print(f"\nTotal Expenses: ₹{result[0]:.2f}")


def search_by_category():
    category = input("Enter category: ").strip()

    with connect_db() as conn:
        rows = conn.execute(
            """
            SELECT expense_date, description, amount
            FROM expenses
            WHERE LOWER(category) = LOWER(?)
            ORDER BY expense_date DESC
            """,
            (category,)
        ).fetchall()

    if not rows:
        print("No matching expenses found.")
        return

    for expense_date, description, amount in rows:
        print(f"{expense_date} | {description} | ₹{amount:.2f}")


def delete_expense():
    view_expenses()

    try:
        expense_id = int(input("\nEnter the ID to delete: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    with connect_db() as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,)
        )

    if cursor.rowcount:
        print("Expense deleted successfully.")
    else:
        print("Expense ID not found.")


def main():
    create_table()

    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total")
        print("4. Search by Category")
        print("5. Delete Expense")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total()
        elif choice == "4":
            search_by_category()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()