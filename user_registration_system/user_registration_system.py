"""
User Registration System

A simple user registration module that demonstrates:
- Validation functions
- Exception handling
- Duplicate checking
- Basic in-memory storage
"""


# -------------------------------------------------------------------
# Simulated Database
# -------------------------------------------------------------------

# KEY POINT: Using lists as simple in-memory storage instead of a real database.
# 'registered_users' holds successful registrations (list of dicts).
# 'failed_registrations' logs every failed attempt with the reason.
registered_users = []
failed_registrations = []


# -------------------------------------------------------------------
# Validation Functions
# -------------------------------------------------------------------

# KEY POINT: Each validation rule is isolated in its own function.
# This follows the Single Responsibility Principle — each function
# does exactly one thing, making the code easy to test and maintain.

def validate_name(name: str) -> bool:
    """
    Validate that the name contains at least 3 characters.

    Args:
        name (str): The user's name.

    Returns:
        bool: True if valid, otherwise False.
    """
    return len(name) >= 3


def validate_email(email: str) -> bool:
    """
    Validate that the email contains both '@' and '.'.

    Args:
        email (str): The user's email address.

    Returns:
        bool: True if valid, otherwise False.
    """
    # KEY POINT: Basic email check using 'in' operator.
    # This is a simplified check — production systems would use regex or a library.
    return "@" in email and "." in email


def validate_password(password: str) -> bool:
    """
    Validate the password strength.

    Rules:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one digit

    Args:
        password (str): The user's password.

    Returns:
        bool: True if valid, otherwise False.
    """
    if len(password) < 8:
        return False

    # KEY POINT: Using any() with a generator expression for efficient character checks.
    # any() short-circuits — it stops as soon as it finds the first matching character.
    has_uppercase = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)

    return has_uppercase and has_digit


# -------------------------------------------------------------------
# Orchestrator Validation Function
# -------------------------------------------------------------------

# KEY POINT: This function acts as a central orchestrator — it calls all individual
# validators and raises a ValueError with a specific message on failure.
# This pattern keeps the registration function clean and focused.

def validate_user_data(name: str, email: str, password: str) -> bool:
    """
    Validate all user inputs.

    Args:
        name (str): The user's name.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        bool: True if all validations pass.

    Raises:
        ValueError: If any validation rule fails.
    """
    if not validate_name(name):
        raise ValueError("Name must contain at least 3 characters.")

    if not validate_email(email):
        raise ValueError("Email must contain '@' and '.'.")

    if not validate_password(password):
        raise ValueError(
            "Password must be at least 8 characters long and "
            "contain one uppercase letter and one digit."
        )

    return True


# -------------------------------------------------------------------
# Registration Function
# -------------------------------------------------------------------

# KEY POINT: This is the main entry point for registering a user.
# It uses try/except to handle validation errors and duplicate emails gracefully,
# logging failures instead of crashing the program.

def create_user_account(name: str, email: str, password: str):
    """
    Create a new user account after validation.

    Args:
        name (str): The user's name.
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        dict: User dictionary if registration succeeds.
        None: If registration fails.

    Raises:
        ValueError: Internally raised during validation or duplicate checks.
    """
    try:
        # Step 1: Validate all fields (raises ValueError on failure)
        validate_user_data(name, email, password)

        # Step 2: Check for duplicate email using any() on the registered_users list
        if any(user["email"] == email for user in registered_users):
            raise ValueError("An account with this email already exists.")

        # Step 3: Build a user record as a dictionary
        user_record = {
            "name": name,
            "email": email,
            "password": password,
            "status": "active",
        }

        # Step 4: Save to in-memory "database" and return the record
        registered_users.append(user_record)
        return user_record

    except ValueError as error:
        # KEY POINT: Failed registrations are logged, not silently discarded.
        # The error message from validation or duplicate check is preserved.
        failed_registrations.append(
            {"email": email, "error": str(error)}
        )
        return None


# -------------------------------------------------------------------
# Testing Section
# -------------------------------------------------------------------

# KEY POINT: Test cases are defined as a list of tuples — a clean pattern for
# running multiple scenarios through the same logic without code duplication.

def run_tests():
    """
    Execute sample registration scenarios.

    Returns:
        None
    """
    test_cases = [
        ("Vlada", "vlada@gmail.com", "Password1"),       # Valid — should succeed
        ("AnotherUser", "vlada@gmail.com", "Password1"),  # Duplicate email — should fail
        ("Veljko", "veljko@gmail.com", "Password1"),       # Valid — should succeed
        ("Edi", "edi@gmail.com", "weakpass"),             # Weak password — should fail
    ]

    # KEY POINT: enumerate() with start=1 gives a human-friendly test number.
    # Tuple unpacking (name, email, password) makes each iteration readable.
    for index, (name, email, password) in enumerate(test_cases, start=1):
        print(f"\nTest {index}")
        result = create_user_account(name, email, password)

        if result:
            print("Registration successful:", result)
        else:
            print("Registration failed.")

    # Print summary of both lists to verify the system's behavior
    print("\nFinal Registered Users:")
    print(registered_users)

    print("\nFailed Registrations:")
    print(failed_registrations)



run_tests()