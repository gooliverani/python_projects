"""
Mini Banking System

A simple banking system that allows:
- Account creation
- Deposits
- Withdrawals
- Transaction tracking
- Account summary display
"""


# -------------------------------------------------
# Simulated Database
# -------------------------------------------------

# Global list acting as an in-memory database to store all bank accounts.
# Each element is a dictionary representing one account.
accounts = []


# -------------------------------------------------
# Helper Function: Find Account
# -------------------------------------------------

def find_account(name: str):
    """
    Find an account by name.

    Args:
        name (str): Account holder name.

    Returns:
        dict: Account dictionary if found.
        None: If account does not exist.
    """
    # Loop through all accounts and perform a case-insensitive name match
    for account in accounts:
        if account["name"].lower() == name.lower():
            return account
    # Return None if no matching account is found
    return None


# -------------------------------------------------
# Create Account
# -------------------------------------------------

def create_account(name: str, initial_balance: float):
    """
    Create a new bank account.

    Args:
        name (str): Account holder name.
        initial_balance (float): Starting balance.

    Returns:
        dict: Created account dictionary.

    Raises:
        ValueError: If balance is negative or account exists.
    """
    # Validate that starting balance is not negative
    if initial_balance < 0:
        raise ValueError("Initial balance cannot be negative.")

    # Prevent duplicate accounts by checking if the name already exists
    if find_account(name):
        raise ValueError("Account with this name already exists.")

    # Build the account dictionary with name, balance, and an empty transaction log
    account = {
        "name": name,
        "balance": initial_balance,
        "transactions": []
    }

    # Store the new account in the global accounts list (simulated database)
    accounts.append(account)
    return account


# -------------------------------------------------
# Deposit
# -------------------------------------------------

def deposit(name: str, amount: float):
    """
    Deposit money into an account.

    Args:
        name (str): Account holder name.
        amount (float): Amount to deposit.

    Returns:
        float: Updated balance.

    Raises:
        ValueError: If amount is invalid or account not found.
    """
    # Reject zero or negative deposit amounts
    if amount <= 0:
        raise ValueError("Deposit amount must be greater than 0.")

    # Look up the account; raise an error if it doesn't exist
    account = find_account(name)

    if not account:
        raise ValueError("Account not found.")

    # Increase the account balance by the deposit amount
    account["balance"] += amount

    # Record the deposit in the transaction history
    account["transactions"].append({
        "type": "Deposit",
        "amount": amount
    })

    return account["balance"]


# -------------------------------------------------
# Withdraw
# -------------------------------------------------

def withdraw(name: str, amount: float):
    """
    Withdraw money from an account.

    Args:
        name (str): Account holder name.
        amount (float): Amount to withdraw.

    Returns:
        float: Updated balance.

    Raises:
        ValueError: If insufficient funds or invalid amount.
    """
    # Reject zero or negative withdrawal amounts
    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than 0.")

    # Look up the account; raise an error if it doesn't exist
    account = find_account(name)

    if not account:
        raise ValueError("Account not found.")

    # Ensure the account has enough funds to cover the withdrawal
    if amount > account["balance"]:
        raise ValueError("Insufficient funds.")

    # Decrease the account balance by the withdrawal amount
    account["balance"] -= amount

    # Record the withdrawal in the transaction history
    account["transactions"].append({
        "type": "Withdrawal",
        "amount": amount
    })

    return account["balance"]


# -------------------------------------------------
# Show Account Summary
# -------------------------------------------------

def show_account(name: str):
    """
    Display account summary including transactions.

    Args:
        name (str): Account holder name.
    """
    # Look up the account by name
    account = find_account(name)

    if not account:
        print("Account not found.")
        return

    # Display account holder name and current balance
    print(f"\nAccount Summary for {account['name']}")
    print(f"Current Balance: ${account['balance']}")

    # Loop through and display each recorded transaction
    print("Transactions:")
    if not account["transactions"]:
        print("No transactions yet.")
    else:
        for transaction in account["transactions"]:
            print(f"- {transaction['type']} : ${transaction['amount']}")


# -------------------------------------------------
# Testing Section
# -------------------------------------------------

def run_tests():
    # Wrap operations in try/except to gracefully handle validation errors
    try:
        create_account("Vlada", 1000)   # Create account with $1000 starting balance
        deposit("Vlada", 200)            # Deposit $200  -> balance becomes $1200
        withdraw("Vlada", 150)           # Withdraw $150 -> balance becomes $1050
        withdraw("Vlada", 2000)          # Overdraft test -> should raise ValueError

    except ValueError as error:
        print("Error:", error)

    # Display final account summary with all recorded transactions
    show_account("Vlada")


# Entry point: run the test suite when the script is executed
run_tests()