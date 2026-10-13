from datetime import date

expenses = []


def add_expense():
    print("\n--- Add Expense ---")

    category = input("Enter category (Food/Travel/Shopping/Bills): ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount in rupees: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    expense = {
        "date": date.today().isoformat(),
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(expense)

    print("Expense added successfully!")


def view_expenses():
    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded yet.")
        return

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. Date: {expense['date']} | "
            f"Category: {expense['category']} | "
            f"Description: {expense['description']} | "
            f"Amount: ₹{expense['amount']:.2f}"
        )


def show_total():
    total = sum(expense["amount"] for expense in expenses)

    print(f"\nTotal Expenses: ₹{total:.2f}")


def search_by_category():
    category = input("\nEnter category to search: ").strip().lower()

    matching_expenses = [
        expense for expense in expenses
        if expense["category"].strip().lower() == category
    ]

    if not matching_expenses:
        print("No expenses found for this category.")
        return

    print(f"\nExpenses in {category.title()}:")

    for expense in matching_expenses:
        print(
            f"{expense['date']} - {expense['description']} - "
            f"₹{expense['amount']:.2f}"
        )


def main():
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total Expenses")
        print("4. Search by Category")
        print("5. Exit")

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
            print("Thank you for using the Expense Tracker!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()