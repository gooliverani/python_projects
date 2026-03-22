# Mini Banking System

A simple command-line banking system built with pure Python. It supports account creation, deposits, withdrawals, transaction tracking, and account summaries — all without external libraries.

---

## Project Overview

This project demonstrates core Python concepts:

- **Functions** with input validation and return values
- **Dictionaries** to represent structured data (accounts, transactions)
- **Lists** as an in-memory data store
- **Loops** for searching and iterating
- **Exception handling** with `try/except` and `ValueError`

---

## Data Structure

### Accounts List (Simulated Database)

A global list named `accounts` stores all bank accounts. Each account is a **dictionary** with the following structure:

```python
{
    "name": "Vlada",           # Account holder name (str)
    "balance": 1000,           # Current balance (float)
    "transactions": [          # List of transaction records
        {"type": "Deposit",    "amount": 200},
        {"type": "Withdrawal", "amount": 150}
    ]
}
```

- **`name`** — Unique identifier for the account holder.
- **`balance`** — The current available balance, updated after every deposit or withdrawal.
- **`transactions`** — A list of dictionaries, each recording the `type` (`"Deposit"` or `"Withdrawal"`) and `amount` of a single operation.

---

## Code Walkthrough

### 1. `find_account(name)`

**Purpose:** Look up an account by name from the `accounts` list.

**How it works:**
- Iterates through every account in the global `accounts` list.
- Performs a **case-insensitive comparison** (`lower()`) so that `"vlada"` matches `"Vlada"`.
- Returns the matching account dictionary, or `None` if not found.

**Why it matters:** This is a reusable helper used by every other function to locate accounts before performing operations.

```python
def find_account(name: str):
    for account in accounts:
        if account["name"].lower() == name.lower():
            return account
    return None
```

---

### 2. `create_account(name, initial_balance)`

**Purpose:** Create a new bank account and add it to the database.

**How it works:**
1. **Validates** that `initial_balance` is not negative — raises `ValueError` if it is.
2. **Checks for duplicates** by calling `find_account(name)` — raises `ValueError` if the name already exists.
3. **Builds** a new account dictionary with `name`, `balance`, and an empty `transactions` list.
4. **Appends** the new account to the global `accounts` list.
5. **Returns** the created account dictionary.

**Key validation logic:**
- Negative balance → `ValueError("Initial balance cannot be negative.")`
- Duplicate name → `ValueError("Account with this name already exists.")`

```python
def create_account(name: str, initial_balance: float):
    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative.")
    if find_account(name):
        raise ValueError("Account with this name already exists.")
    account = {
        "name": name,
        "balance": initial_balance,
        "transactions": []
    }
    accounts.append(account)
    return account
```

---

### 3. `deposit(name, amount)`

**Purpose:** Add money to an existing account.

**How it works:**
1. **Validates** that `amount` is greater than 0 — raises `ValueError` otherwise.
2. **Finds** the account using `find_account(name)` — raises `ValueError` if not found.
3. **Increases** `account["balance"]` by the deposit amount.
4. **Records** the transaction by appending `{"type": "Deposit", "amount": amount}` to the transactions list.
5. **Returns** the updated balance.

**Example flow:**
```
Balance before: $1000
deposit("Vlada", 200)
Balance after:  $1200
Transaction log: [{"type": "Deposit", "amount": 200}]
```

```python
def deposit(name: str, amount: float):
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")
    account = find_account(name)
    if not account:
        raise ValueError("Account not found.")
    account["balance"] += amount
    account["transactions"].append({"type": "Deposit", "amount": amount})
    return account["balance"]
```

---

### 4. `withdraw(name, amount)`

**Purpose:** Remove money from an existing account, with overdraft protection.

**How it works:**
1. **Validates** that `amount` is greater than 0 — raises `ValueError` otherwise.
2. **Finds** the account using `find_account(name)` — raises `ValueError` if not found.
3. **Checks for sufficient funds** — if `amount > balance`, raises `ValueError("Insufficient funds.")`.
4. **Decreases** `account["balance"]` by the withdrawal amount.
5. **Records** the transaction by appending `{"type": "Withdrawal", "amount": amount}` to the transactions list.
6. **Returns** the updated balance.

**Overdraft protection:** The function will **never** allow a withdrawal that exceeds the current balance. This prevents the account from going into a negative state.

```python
def withdraw(name: str, amount: float):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than 0.")
    account = find_account(name)
    if not account:
        raise ValueError("Account not found.")
    if amount > account["balance"]:
        raise ValueError("Insufficient funds.")
    account["balance"] -= amount
    account["transactions"].append({"type": "Withdrawal", "amount": amount})
    return account["balance"]
```

---

### 5. `show_account(name)`

**Purpose:** Display a formatted summary of an account and its transaction history.

**How it works:**
1. **Finds** the account using `find_account(name)`.
2. If not found, prints `"Account not found."` and returns early.
3. **Prints** the account holder's name and current balance.
4. **Loops** through the `transactions` list and prints each one.
5. If the transactions list is empty, prints `"No transactions yet."`.

**Sample output:**
```
Account Summary for Vlada
Current Balance: $1050
Transactions:
- Deposit : $200
- Withdrawal : $150
```

```python
def show_account(name: str):
    account = find_account(name)
    if not account:
        print("Account not found.")
        return
    print(f"\nAccount Summary for {account['name']}")
    print(f"Current Balance: ${account['balance']}")
    print("Transactions:")
    if not account["transactions"]:
        print("No transactions yet.")
    else:
        for transaction in account["transactions"]:
            print(f"- {transaction['type']} : ${transaction['amount']}")
```

---

### 6. `run_tests()` — Testing Section

**Purpose:** Verify that all functions work correctly, including error handling.

**What it tests:**
| Step | Operation | Expected Result |
|------|-----------|-----------------|
| 1 | `create_account("Vlada", 1000)` | Account created with $1000 balance |
| 2 | `deposit("Vlada", 200)` | Balance increases to $1200 |
| 3 | `withdraw("Vlada", 150)` | Balance decreases to $1050 |
| 4 | `withdraw("Vlada", 2000)` | **Raises** `ValueError` — insufficient funds |
| 5 | `show_account("Vlada")` | Prints account summary with transactions |

**Error handling:** The `try/except` block catches the `ValueError` from the overdraft attempt and prints the error message, allowing the program to continue to the `show_account()` call.

```python
def run_tests():
    try:
        create_account("Vlada", 1000)
        deposit("Vlada", 200)
        withdraw("Vlada", 150)
        withdraw("Vlada", 2000)      # Overdraft test
    except ValueError as error:
        print("Error:", error)
    show_account("Vlada")

run_tests()
```

---

## How to Run

```bash
python mini_banking_system.py
```

**Expected output:**
```
Error: Insufficient funds.

Account Summary for Vlada
Current Balance: $1050
Transactions:
- Deposit : $200
- Withdrawal : $150
```

---

## Python Concepts Used

| Concept | Where It's Used |
|---------|----------------|
| **Global list** | `accounts` list as a simulated database |
| **Dictionaries** | Account structure (`name`, `balance`, `transactions`) and transaction records (`type`, `amount`) |
| **Functions** | `find_account()`, `create_account()`, `deposit()`, `withdraw()`, `show_account()`, `run_tests()` |
| **Loops (`for`)** | Searching accounts in `find_account()`, printing transactions in `show_account()` |
| **String methods** | `.lower()` for case-insensitive name matching |
| **Exception handling** | `raise ValueError` for validation, `try/except` in testing |
| **Type hints** | Function parameter annotations (`: str`, `: float`) |
| **f-strings** | Formatted output in `show_account()` |
