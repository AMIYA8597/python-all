"""
Module: Exception Handling

Learning Objectives:
1. Master the `try...except...else...finally` block structure.
2. Learn how to catch specific exceptions and handle multiple exceptions.
3. Understand how to raise custom exceptions.
4. Best practices for clean and robust error handling.

Interview Questions Covered:
- When would you use `else` and `finally` in exception handling?
- How do you create and raise a custom exception?
- Why is catching `Exception` generally frowned upon, and what should you do instead?
"""

from typing import Union

# ---------------------------------------------------------
# Concept 1: Custom Exceptions
# ---------------------------------------------------------
class InsufficientFundsError(Exception):
    """Raised when an account has insufficient funds for a transaction."""
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        self.message = f"Cannot withdraw {amount}. Current balance is {balance}."
        super().__init__(self.message)

# ---------------------------------------------------------
# Concept 2: try-except-else-finally
# ---------------------------------------------------------
class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance
        
    def withdraw(self, amount: float) -> Union[float, None]:
        print(f"\nAttempting to withdraw {amount} from account with {self.balance}...")
        try:
            if amount < 0:
                raise ValueError("Withdrawal amount cannot be negative.")
            if amount > self.balance:
                raise InsufficientFundsError(self.balance, amount)
            
            # Simulate withdrawal
            self.balance -= amount
            
        except ValueError as ve:
            print(f"ValueError caught: {ve}")
        except InsufficientFundsError as ife:
            print(f"InsufficientFundsError caught: {ife}")
        except Exception as e:
            # Catch-all for unexpected errors (usually discouraged unless logging)
            print(f"Unexpected error: {e}")
        else:
            # Executes ONLY if NO exception was raised
            print("Withdrawal successful!")
            return amount
        finally:
            # Executes ALWAYS, regardless of exceptions
            print(f"Transaction finished. Final balance: {self.balance}")
            
        return None

# ---------------------------------------------------------
# Tests and Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    account = BankAccount(100.0)
    
    # Successful withdrawal
    account.withdraw(40.0)
    
    # Raises InsufficientFundsError
    account.withdraw(80.0)
    
    # Raises ValueError
    account.withdraw(-10.0)
