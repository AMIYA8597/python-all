"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (MOCK INTERVIEWS - ADVANCED PAIR PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Beyond simple bug fixing, advanced pair programming interviews test your ability 
# to refactor legacy code into extensible, object-oriented, design-pattern-driven 
# architecture while navigating a complex domain logic.
#
# A junior engineer looks at a massive `if/elif/else` block parsing API responses, 
# adds another `elif` to it, and calls it a day. The codebase remains a brittle 
# monolithic script.
#
# A senior engineer identifies the architectural flaw (violation of the Open-Closed 
# Principle). They collaboratively suggest implementing a Strategy Pattern or a 
# Factory Pattern. They build abstract base classes, ensuring that the next time 
# a feature is added, the core logic never needs to be touched again.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Architectural Refactoring.
# - Master SOLID Principle application during live interviews.
# - Master abstracting Domain Logic.
#
# ==============================================================================
"""

import time
import sys
from abc import ABC, abstractmethod

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

def simulate_typing(text: str, delay: float = 0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ==============================================================================
# 3. THE LEGACY CODEBASE (VIOLATING SOLID PRINCIPLES)
# ==============================================================================
# "We need to add a new 'Crypto' payment method to our payment processor. 
# Here is the existing code. Please add the feature and clean it up."

class LegacyPaymentProcessor:
    def process_payment(self, amount: float, method: str):
        # VIOLATION: Open-Closed Principle (OCP).
        # Every time a new payment method is added, we must physically modify 
        # this core function, risking breaking existing integrations!
        if method == "credit_card":
            print(f"Processing ${amount} via Credit Card API.")
            # ... 50 lines of complex CC logic ...
            return True
        elif method == "paypal":
            print(f"Processing ${amount} via PayPal API.")
            # ... 50 lines of complex PayPal logic ...
            return True
        # Adding Crypto here would require another `elif`...
        else:
            raise ValueError("Unknown payment method")


# ==============================================================================
# 4. ADVANCED REFACTORING (THE STRATEGY PATTERN)
# ==============================================================================
def advanced_pair_programming_simulation():
    section_header("Live Simulation: Architectural Refactoring (SOLID)")
    
    simulate_typing("INTERVIEWER: 'Here is the `LegacyPaymentProcessor`. We need to add Crypto.'")
    
    simulate_typing("\n[STAGE 1: IDENTIFYING THE ARCHITECTURAL FLAW]")
    simulate_typing("CANDIDATE: 'I see an `if/elif/else` chain checking the payment method.'")
    simulate_typing("CANDIDATE: 'If I just add an `elif method == 'crypto'`, it violates the Open-Closed Principle. This class should be open for extension but closed for modification.'")
    simulate_typing("CANDIDATE: 'I propose we refactor this using the Strategy Pattern. We can define an Abstract Base Class for Payments, and inject the specific strategy at runtime.'")
    simulate_typing("INTERVIEWER: 'I love that idea. Show me the architecture.'")
    
    # --------------------------------------------------------------------------
    # CANDIDATE ARCHITECTS THE SOLUTION
    # --------------------------------------------------------------------------
    simulate_typing("\n--- IMPLEMENTING STRATEGY PATTERN ---")
    
    # 1. THE CONTRACT (Interface)
    class PaymentStrategy(ABC):
        @abstractmethod
        def pay(self, amount: float) -> bool:
            pass
            
    # 2. THE CONCRETE IMPLEMENTATIONS
    class CreditCardPayment(PaymentStrategy):
        def pay(self, amount: float) -> bool:
            print(f"  [STRATEGY] Processing ${amount} via Credit Card API.")
            return True
            
    class PayPalPayment(PaymentStrategy):
        def pay(self, amount: float) -> bool:
            print(f"  [STRATEGY] Processing ${amount} via PayPal API.")
            return True
            
    # THE NEW FEATURE! (Added without modifying any existing classes)
    class CryptoPayment(PaymentStrategy):
        def pay(self, amount: float) -> bool:
            print(f"  [STRATEGY] Processing ${amount} via Crypto Blockchain.")
            return True
            
    # 3. THE REFACTORED PROCESSOR (Context)
    class ModernPaymentProcessor:
        # Dependency Injection!
        def __init__(self, strategy: PaymentStrategy):
            self.strategy = strategy
            
        def process_payment(self, amount: float):
            # The core logic is now completely agnostic to the payment method!
            return self.strategy.pay(amount)
            
    simulate_typing("\nCANDIDATE: 'The refactoring is complete.'")
    simulate_typing("CANDIDATE: 'Now, if we want to add Apple Pay next week, we just create an `ApplePayPayment` class. The `ModernPaymentProcessor` never needs to be touched again.'")
    
    simulate_typing("\n[STAGE 2: TESTING THE NEW ARCHITECTURE]")
    simulate_typing("INTERVIEWER: 'Run a test to prove the dependency injection works.'")
    
    # Executing the test!
    crypto_strategy = CryptoPayment()
    processor = ModernPaymentProcessor(crypto_strategy)
    processor.process_payment(500.00)
    
    simulate_typing("\nINTERVIEWER: 'Flawless execution. You demonstrated true Staff-level architectural vision.'")


def run_all_labs():
    advanced_pair_programming_simulation()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is the Open-Closed Principle (OCP) critical for enterprise systems, and how did the `if/elif` block violate it?"
   Senior Answer: "The Open-Closed Principle mandates that a software entity should be Open for Extension (adding new features) but Closed for Modification (you shouldn't have to alter existing, tested code). An `if/elif` chain completely violates this. Every time a new feature is added, you must physically open the core function and inject a new `elif` branch. In an enterprise system, modifying core functions forces you to re-run the entire test suite for *all* previous features, risking regression bugs. By using Polymorphism and the Strategy Pattern, we extend the system by writing brand new, isolated classes, leaving the core processor mathematically untouched."

2. Interviewer: "What is Dependency Injection, and why is `ModernPaymentProcessor(crypto_strategy)` a prime example of it?"
   Senior Answer: "Dependency Injection (DI) is a design pattern where an object receives its dependencies from the outside, rather than instantiating them internally. If the `ModernPaymentProcessor` instantiated `CryptoPayment()` directly inside its `__init__` method, it would be tightly coupled to that specific implementation, making it impossible to swap payment methods or inject Mock objects for Unit Testing. By demanding a `PaymentStrategy` interface in the constructor parameters, the processor is completely decoupled. The caller is responsible for injecting the dependency, granting the architecture infinite runtime flexibility."

3. Interviewer: "In Python, why do we use `from abc import ABC, abstractmethod` instead of just raising a `NotImplementedError` in a standard base class?"
   Senior Answer: "Raising `NotImplementedError` is a runtime check. If a developer forgets to implement a method, the code will physically compile and run perfectly until that specific method is called, at which point it crashes in production. By inheriting from `ABC` and decorating methods with `@abstractmethod`, we activate Python's strict interface enforcement. If a developer tries to instantiate a subclass that forgot to implement a required method, Python will instantly throw a fatal `TypeError` at the exact moment of instantiation, catching the architectural flaw instantly during initialization rather than silently failing later."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Mock Interviews (Advanced Pair Programming) Completed.")
