"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (REFACTORING & SOLID PRINCIPLES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer is asked to add a new "PayPal" payment method to an 
# e-commerce system. The system was written procedurally. To add PayPal, the 
# developer must mathematically modify 15 different `if/elif` blocks scattered 
# across 5 different files. They accidentally forget to update the `refund` file. 
# The code deploys, and users cannot get refunds via PayPal. The architecture 
# is mathematically rigid and fragile.
#
# A senior software architect applies the SOLID principles (specifically the 
# Open/Closed Principle). They refactor the system into an Object-Oriented, 
# polymorphic architecture. When the CEO asks for a "Bitcoin" payment method, 
# the architect writes ONE new class (`BitcoinProcessor`), inherits from the 
# `PaymentStrategy` interface, and injects it into the system. They touch exactly 
# zero existing files. The architecture is mathematically Open for Extension, but 
# Closed for Modification.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Code Refactoring (eliminating procedural spaghetti).
# - Execute the Open/Closed Principle (OCP) via Polymorphism.
# - Architect Dependency Injection and the Strategy Pattern.
#
# ==============================================================================
"""

import abc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PROCEDURAL DISASTER (BEFORE REFACTORING)
# ==============================================================================
class SpaghettiOrderProcessor:
    """
    ANTI-PATTERN WARNING.
    This violates the Open/Closed Principle! Every time a new payment method 
    is invented, we must physically open this file and modify the logic.
    """
    def process_order(self, order_amount: float, payment_type: str):
        print(f"  [BAD ARCHITECTURE] Processing ${order_amount}")
        
        if payment_type == "credit_card":
            print("    -> Validating Credit Card digits...")
            print("    -> Charging Stripe API...")
        elif payment_type == "paypal":
            print("    -> Redirecting to PayPal OAuth...")
            print("    -> Charging PayPal API...")
        elif payment_type == "crypto": # A developer just added this!
            print("    -> Validating Wallet Hash...")
            print("    -> Executing Smart Contract...")
        else:
            raise ValueError("Unknown Payment Type")


# ==============================================================================
# 4. THE SOLID REFACTOR (AFTER REFACTORING)
# ==============================================================================
# We mathematically extract the variations into isolated objects!

class PaymentStrategy(abc.ABC):
    """
    The mathematical interface. Every payment processor MUST follow this contract.
    """
    @abc.abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CreditCardProcessor(PaymentStrategy):
    """Isolated, modular logic just for Credit Cards."""
    def pay(self, amount: float) -> bool:
        print(f"    -> [CREDIT CARD] Charging ${amount:.2f} via Stripe API.")
        return True


class PayPalProcessor(PaymentStrategy):
    """Isolated, modular logic just for PayPal."""
    def pay(self, amount: float) -> bool:
        print(f"    -> [PAYPAL] Charging ${amount:.2f} via OAuth Token.")
        return True


class CryptoProcessor(PaymentStrategy):
    """Isolated, modular logic just for Crypto."""
    def pay(self, amount: float) -> bool:
        print(f"    -> [CRYPTO] Executing Smart Contract for ${amount:.2f}.")
        return True


# THE NEW, FLAWLESS PROCESSOR
class SolidOrderProcessor:
    """
    This class is mathematically CLOSED for modification.
    If ApplePay is invented tomorrow, you NEVER touch this class!
    """
    def process_order(self, order_amount: float, payment_method: PaymentStrategy):
        print(f"  [SOLID ARCHITECTURE] Processing ${order_amount:.2f}")
        
        # We rely on Polymorphism! We don't care WHAT the payment method is.
        # We just command it to execute the mathematical contract `pay()`!
        success = payment_method.pay(order_amount)
        
        if success:
            print("  [SUCCESS] Order completed.")
        else:
            print("  [FAILURE] Order rejected.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_refactoring():
    section_header("Code Quality: Refactoring & SOLID Principles")
    
    print("\n  [SCENARIO A: THE SPAGHETTI CODE]")
    bad_processor = SpaghettiOrderProcessor()
    bad_processor.process_order(100.0, "paypal")
    
    
    print("\n  [SCENARIO B: THE SOLID POLYMORPHISM]")
    # We instantiate the exact strategy we want
    payment_strategy = CryptoProcessor()
    
    # We mathematically inject it into the Processor!
    solid_processor = SolidOrderProcessor()
    solid_processor.process_order(100.0, payment_strategy)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  Notice that `SolidOrderProcessor` has no `if/else` statements. ")
    print("  It is completely decoupled from the payment APIs, meaning it ")
    print("  can be Unit Tested in total isolation.")


def run_all_labs():
    demonstrate_refactoring()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What does the 'O' in SOLID stand for, and how did we mathematically achieve it in the `SolidOrderProcessor`?"
   Senior Answer: "The Open/Closed Principle (OCP). It states that a software entity should be Open for Extension, but Closed for Modification. In the Spaghetti code, to add 'ApplePay', the developer had to physically open the existing class, add a new `elif` branch, and risk breaking the Credit Card logic. The class was not closed for modification. In the refactored code, we achieved OCP via Polymorphism (The Strategy Pattern). To add 'ApplePay', we write a brand new `ApplePayProcessor` file. We physically do not touch the `SolidOrderProcessor` file. We extend the system's capabilities (Open for Extension) without mutating existing, tested source code (Closed for Modification)."

2. Interviewer: "Why did we use the `abc.ABC` (Abstract Base Class) module to define `PaymentStrategy`? Why couldn't we just write a normal parent class?"
   Senior Answer: "Mathematical Contract Enforcement. If we just write a normal parent class with a `def pay(): pass` method, a junior developer could create an `ApplePayProcessor`, misspell the method as `def process_payment():`, and the Python interpreter would happily allow the code to execute until it crashes at runtime inside the Order Processor. By inheriting from `abc.ABC` and using the `@abc.abstractmethod` decorator, we mathematically force the CPython interpreter to execute strict Interface validation at the exact moment of instantiation. If the junior developer misspells the `pay()` method, the script will violently crash the millisecond they type `apple = ApplePayProcessor()`, mathematically preventing the broken object from ever entering the processing pipeline."

3. Interviewer: "What is 'Dependency Injection' (DI), and how did we use it in the refactored design?"
   Senior Answer: "Inversion of Control. In a flawed design, the `SolidOrderProcessor` would instantiate the `CryptoProcessor` directly inside its own method (`crypto = CryptoProcessor()`). This tightly couples the two classes together, making it mathematically impossible to Unit Test the Order Processor without also executing the Crypto logic. Dependency Injection states that a class should not construct its own dependencies. Instead, the dependency (the instantiated `CryptoProcessor` object) is mathematically passed (injected) into the function arguments by the orchestrator (`process_order(100.0, payment_strategy)`). This allows us to inject a synthetic `MockPaymentProcessor` during Unit Testing, achieving absolute architectural isolation."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Code Quality (Refactoring) Completed.")
