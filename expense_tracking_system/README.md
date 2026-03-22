# Expense Tracking System

A simple Python expense tracking application that lets you add, store, analyze, and display expenses — built entirely with fundamental Python concepts.

---

## Project Overview

This project fulfills the **Expense Tracking System** requirements:

| Requirement | Status |
|---|---|
| Simulated database (global list) | Done |
| Add expense with validation | Done |
| Calculate total expenses | Done |
| Calculate total by category | Done |
| Show all expenses | Done |
| Testing section with invalid input | Done |

---

## How to Run

```bash
python expense_tracking_system.py
```

**Expected Output:**

```
Error: Amount must be greater than 0.

Total Expenses: 170
Total Food Expenses: 150

All Expenses:
1. Food - Groceries : $50
2. Transport - Taxi : $20
3. Food - Restaurant : $100
```

---

## Detailed Code Explanation

### Part 1: Simulated Database

```python
expenses = []
```

- A **global list** serves as the in-memory database for the entire application.
- Every expense added by `add_expense()` is appended here as a **dictionary**.
- Using a global list keeps things simple — all functions can read from and write to the same shared data store without needing to pass it around as an argument.

---

### Part 2: `add_expense(amount, category, description)`

```python
def add_expense(amount: float, category: str, description: str) -> dict:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")

    expense = {
        "amount": amount,
        "category": category,
        "description": description
    }

    expenses.append(expense)
    return expense
```

**Step-by-step breakdown:**

1. **Validation** — The very first thing the function does is check whether `amount` is positive. If not, it raises a `ValueError` with a descriptive message. This prevents bad data from entering the system.
2. **Dictionary creation** — A dictionary is built with three keys (`amount`, `category`, `description`). Dictionaries are ideal here because they let us access each field by name rather than by position.
3. **Storing** — The dictionary is appended to the global `expenses` list.
4. **Return value** — The created expense is returned so the caller can confirm what was stored or use it further.

**Key concepts demonstrated:**
- **Input validation** with an `if` guard and `raise`
- **Exception handling** via `ValueError`
- **Type hints** (`amount: float`, `-> dict`) for readability
- **Dictionaries** as structured data containers

---

### Part 3: `calculate_total_expenses()`

```python
def calculate_total_expenses() -> float:
    total = 0

    for expense in expenses:
        total += expense["amount"]

    return total
```

**Step-by-step breakdown:**

1. **Initialize accumulator** — `total` starts at `0`.
2. **Loop** — A `for` loop iterates over every dictionary in the `expenses` list.
3. **Accumulate** — Each expense's `"amount"` value is added to `total` using `+=`.
4. **Return** — The final sum is returned.

**Key concepts demonstrated:**
- **Accumulator pattern** — a common technique where you initialize a variable before a loop and update it on every iteration.
- **Dictionary key access** — `expense["amount"]` retrieves the value stored under the `"amount"` key.

---

### Part 4: `calculate_total_by_category(category)`

```python
def calculate_total_by_category(category: str) -> float:
    total = 0

    for expense in expenses:
        if expense["category"].lower() == category.lower():
            total += expense["amount"]

    return total
```

**Step-by-step breakdown:**

1. Same accumulator setup as `calculate_total_expenses()`.
2. **Filtering** — Inside the loop, an `if` condition checks whether the expense's category matches the requested category.
3. **Case-insensitive comparison** — Both sides are converted to lowercase with `.lower()` so that `"Food"`, `"food"`, and `"FOOD"` all match.
4. Only matching expenses contribute to `total`.

**Key concepts demonstrated:**
- **Filtering inside a loop** — combining iteration with a conditional check.
- **String method `.lower()`** — ensures the comparison is not affected by capitalization differences.
- **Parameterized function** — the `category` argument makes this function reusable for any category.

---

### Part 5: `show_expenses()`

```python
def show_expenses() -> None:
    if not expenses:
        print("No expenses recorded.")
        return

    print("\nAll Expenses:")
    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. {expense['category']} - "
            f"{expense['description']} : ${expense['amount']}"
        )
```

**Step-by-step breakdown:**

1. **Guard clause** — If the list is empty (`not expenses` evaluates to `True` for an empty list), a message is printed and the function returns early. This avoids printing a heading with no data below it.
2. **`enumerate()` with `start=1`** — Produces pairs of `(index, expense)` where the index begins at 1 instead of the default 0, making the output human-friendly.
3. **f-string formatting** — An f-string assembles each line, pulling values from the dictionary by key.

**Key concepts demonstrated:**
- **Guard clause / early return** — a clean pattern to handle edge cases at the top of a function.
- **`enumerate()`** — a built-in that pairs each item with its index, removing the need for a manual counter variable.
- **f-strings** — Python's modern string formatting syntax for embedding expressions inside strings.

---

### Part 6: Testing Section

```python
def run_tests() -> None:
    try:
        add_expense(50, "Food", "Groceries")
        add_expense(20, "Transport", "Taxi")
        add_expense(100, "Food", "Restaurant")
        add_expense(0, "Entertainment", "Cinema")  # Invalid — triggers ValueError

    except ValueError as error:
        print("Error:", error)

    print("\nTotal Expenses:", calculate_total_expenses())
    print("Total Food Expenses:", calculate_total_by_category("Food"))

    show_expenses()


if __name__ == "__main__":
    run_tests()
```

**Step-by-step breakdown:**

1. **`try` / `except`** — The four `add_expense()` calls are wrapped in a `try` block. The first three succeed, but the fourth passes `0` as the amount, which triggers the `ValueError` raised inside `add_expense()`. Execution jumps to the `except` block where the error message is printed.
2. **Important behavior** — Because the exception occurs on the fourth call, only three expenses are stored. The invalid one is never appended to the list.
3. **Aggregation calls** — `calculate_total_expenses()` returns `170` (50 + 20 + 100) and `calculate_total_by_category("Food")` returns `150` (50 + 100).
4. **Display** — `show_expenses()` prints all three valid expenses.
5. **`if __name__ == "__main__":`** — This guard ensures `run_tests()` only executes when the script is run directly. If another module imports this file, the tests won't run automatically.

**Key concepts demonstrated:**
- **Exception handling** with `try` / `except` — catching specific exceptions (`ValueError`) gracefully.
- **`as error`** — captures the exception object so its message can be printed.
- **`__name__` guard** — standard Python practice to separate reusable code from script execution.

---

## Python Concepts Used

| Concept | Where Used |
|---|---|
| **Global variables** | `expenses` list shared across all functions |
| **Dictionaries** | Each expense stored as `{"amount", "category", "description"}` |
| **Lists** | `expenses` list holds all expense dictionaries |
| **Functions with parameters** | All four core functions accept arguments and return values |
| **Type hints** | Function signatures use `: float`, `: str`, `-> dict`, etc. |
| **Docstrings** | Every function has a triple-quoted description |
| **Input validation** | `amount <= 0` check with `raise ValueError` |
| **Exception handling** | `try` / `except ValueError` in `run_tests()` |
| **`for` loop** | Iterating over the expenses list |
| **Accumulator pattern** | `total += expense["amount"]` in calculation functions |
| **`enumerate()`** | Numbering expenses in `show_expenses()` |
| **f-strings** | Formatting output strings |
| **`.lower()` comparison** | Case-insensitive category matching |
| **Guard clause** | Early return in `show_expenses()` for empty list |
| **`__name__` guard** | Running tests only when script is executed directly |
