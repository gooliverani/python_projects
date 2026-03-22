# User Registration System

A Python project that implements a simple **user registration system** with input validation, duplicate checking, exception handling, and in-memory data storage.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [1. In-Memory Database](#1-in-memory-database)
  - [2. Validation Functions](#2-validation-functions)
  - [3. Orchestrator — validate_user_data()](#3-orchestrator--validate_user_data)
  - [4. Registration — create_user_account()](#4-registration--create_user_account)
  - [5. Testing — run_tests()](#5-testing--run_tests)
- [Concepts Demonstrated](#concepts-demonstrated)
- [Sample Output](#sample-output)
- [How to Run](#how-to-run)

---

## Overview

This project simulates a user registration workflow. Users provide a **name**, **email**, and **password**. The system validates each field, checks for duplicate emails, and either registers the user or logs the failure with a reason.

It is designed as a learning project to practice core Python concepts in a real-world-like scenario.

---

## Project Structure

```
project_1/
└── user_registration_system.py   # All logic in a single module
```

---

## How It Works

### 1. In-Memory Database

```python
registered_users = []
failed_registrations = []
```

Two module-level **lists** act as a simulated database:

| List                   | Purpose                                                  |
|------------------------|----------------------------------------------------------|
| `registered_users`     | Stores dictionaries of successfully registered users.    |
| `failed_registrations` | Logs each failed attempt with the email and error reason.|

Since these are **mutable global objects**, every function that appends to them shares the same data without needing `global` declarations (only reads and mutations, no reassignment).

---

### 2. Validation Functions

Three small, focused functions each handle **one** validation rule:

#### `validate_name(name) -> bool`

```python
return len(name) >= 3
```

- Checks that the name is **at least 3 characters** long.
- Uses the built-in `len()` function and a simple comparison.

#### `validate_email(email) -> bool`

```python
return "@" in email and "." in email
```

- Checks that the email contains both **`@`** and **`.`** characters.
- Uses the `in` operator — a straightforward membership test on strings.
- This is a simplified check suitable for learning; production code would use regex or a dedicated library.

#### `validate_password(password) -> bool`

```python
if len(password) < 8:
    return False

has_uppercase = any(char.isupper() for char in password)
has_digit     = any(char.isdigit() for char in password)

return has_uppercase and has_digit
```

- **Length check**: rejects passwords shorter than 8 characters immediately (early return).
- **`any()` with generator expressions**: iterates through characters and short-circuits — stops as soon as the first uppercase letter (or digit) is found, making it efficient.
- **`str.isupper()` / `str.isdigit()`**: built-in string methods that classify individual characters.

**Key takeaway**: Each validator returns a simple `bool` — it knows nothing about error messages. This keeps the functions pure and reusable.

---

### 3. Orchestrator — `validate_user_data()`

```python
def validate_user_data(name, email, password) -> bool:
    if not validate_name(name):
        raise ValueError("Name must contain at least 3 characters.")

    if not validate_email(email):
        raise ValueError("Email must contain '@' and '.'.")

    if not validate_password(password):
        raise ValueError("Password must be at least 8 characters long ...")

    return True
```

This function **coordinates** all three validators and adds the error-reporting layer:

1. Calls each validator in sequence.
2. If any validator returns `False`, it **raises a `ValueError`** with a descriptive message.
3. If all pass, returns `True`.

**Why raise exceptions instead of returning error strings?**

- Exceptions separate the **happy path** (everything is valid) from the **error path** (something failed).
- The caller can use `try/except` to handle failures cleanly in one place.
- Each error message is specific, so the user knows exactly what went wrong.

---

### 4. Registration — `create_user_account()`

```python
def create_user_account(name, email, password):
    try:
        validate_user_data(name, email, password)

        if any(user["email"] == email for user in registered_users):
            raise ValueError("An account with this email already exists.")

        user_record = {
            "name": name,
            "email": email,
            "password": password,
            "status": "active",
        }

        registered_users.append(user_record)
        return user_record

    except ValueError as error:
        failed_registrations.append({"email": email, "error": str(error)})
        return None
```

This is the **main entry point** for the registration workflow. Step by step:

| Step | What happens | Python concept |
|------|-------------|----------------|
| **1** | `validate_user_data()` is called — if any field is invalid, a `ValueError` is raised and execution jumps to the `except` block. | Exception propagation |
| **2** | Duplicate email check using `any()` on the `registered_users` list. Iterates through existing records and checks the `"email"` key. | Generator expression + `any()` |
| **3** | A **dictionary** `user_record` is created with four keys: name, email, password, and status. | `dict` literal |
| **4** | The record is **appended** to `registered_users` and returned to the caller. | `list.append()` |
| **Except** | On any `ValueError`, the failure is **logged** into `failed_registrations` with the email and error message, then `None` is returned. | `try/except`, `str()` conversion |

**Key design choices:**

- **`try/except` wraps the entire flow**: both validation errors and duplicate errors are caught in one place.
- **Returns `dict` on success, `None` on failure**: the caller can use a simple truthiness check (`if result:`).
- **Failures are logged, not lost**: every failed attempt is recorded for later inspection.

---

### 5. Testing — `run_tests()`

```python
test_cases = [
    ("Vlada", "vlada@gmail.com", "Password1"),       # Valid
    ("AnotherUser", "vlada@gmail.com", "Password1"),  # Duplicate email
    ("Veljko", "veljko@gmail.com", "Password1"),       # Valid
    ("Edi", "edi@gmail.com", "weakpass"),             # Weak password
]

for index, (name, email, password) in enumerate(test_cases, start=1):
    result = create_user_account(name, email, password)
```

| Test | Expected Outcome | Why |
|------|-----------------|-----|
| 1 — Vlada | **Success** | All fields are valid. |
| 2 — AnotherUser | **Fail** — duplicate email | `vlada@gmail.com` was already registered in Test 1. |
| 3 — Veljko | **Success** | Different email, valid data. |
| 4 — Edi | **Fail** — weak password | `"weakpass"` has no uppercase letter and no digit. |

**Python concepts used here:**

- **List of tuples**: a clean way to define multiple test scenarios as data.
- **`enumerate(iterable, start=1)`**: generates `(index, item)` pairs with human-friendly numbering.
- **Tuple unpacking**: `(name, email, password)` destructures each tuple directly in the `for` loop.

---

## Concepts Demonstrated

| Concept | Where it's used |
|---------|----------------|
| **Functions & parameters** | All `validate_*` functions, `create_user_account()` |
| **Type hints** | `name: str`, `-> bool` annotations on every function |
| **Docstrings** | Every function has a Google-style docstring |
| **Boolean logic** | `and`, `not`, comparison operators |
| **`any()` with generators** | Password validation, duplicate email check |
| **String methods** | `.isupper()`, `.isdigit()` |
| **Exception handling** | `try/except ValueError`, `raise ValueError(...)` |
| **Dictionaries** | User records stored as `dict` objects |
| **Lists** | `registered_users`, `failed_registrations` |
| **`enumerate()`** | Numbered iteration in `run_tests()` |
| **Tuple unpacking** | Destructuring test cases in the `for` loop |
| **f-strings** | `f"\nTest {index}"` |
| **Early return** | `if len(password) < 8: return False` |

---

## Sample Output

```
Test 1
Registration successful: {'name': 'Vlada', 'email': 'vlada@gmail.com', 'password': 'Password1', 'status': 'active'}

Test 2
Registration failed.

Test 3
Registration successful: {'name': 'Veljko', 'email': 'veljko@gmail.com', 'password': 'Password1', 'status': 'active'}

Test 4
Registration failed.

Final Registered Users:
[{'name': 'Vlada', 'email': 'vlada@gmail.com', 'password': 'Password1', 'status': 'active'},
 {'name': 'Veljko', 'email': 'veljko@gmail.com', 'password': 'Password1', 'status': 'active'}]

Failed Registrations:
[{'email': 'vlada@gmail.com', 'error': 'An account with this email already exists.'},
 {'email': 'edi@gmail.com', 'error': 'Password must be at least 8 characters long and contain one uppercase letter and one digit.'}]
```

---

## How to Run

```bash
python user_registration_system.py
```

No external dependencies required — uses only Python built-in features.
