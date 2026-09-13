"""
# ==============================================================================
# LABORATORY: DESIGN PATTERNS (THE PYTHONIC WAY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Design patterns are standardized solutions to common software architecture 
# problems (from the "Gang of Four"). However, Java-style design patterns are 
# often overkill in Python because Python has first-class functions and dynamic 
# typing. This lab demonstrates how to implement the Factory, Strategy, and 
# Observer patterns the "Pythonic" way.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Factory Pattern using `@classmethod`.
# - Understand the Strategy Pattern using First-Class Functions.
# - Understand the Observer Pattern (Pub/Sub).
#
# ==============================================================================
"""

from typing import Callable, List, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE FACTORY PATTERN (VIA CLASSMETHODS)
# ==============================================================================

class Document:
    def __init__(self, content: str, doc_type: str):
        self.content = content
        self.doc_type = doc_type
        
    @classmethod
    def from_csv(cls, csv_string: str):
        """
        A Factory Method. It creates and returns an instance of the class
        using alternative parsing logic. This is highly Pythonic.
        """
        # Parse the CSV (simplified)
        rows = csv_string.strip().split('\n')
        content = f"CSV with {len(rows)} rows"
        return cls(content=content, doc_type="CSV")
        
    @classmethod
    def from_json(cls, json_string: str):
        """Another Factory Method."""
        content = f"Parsed JSON: {json_string}"
        return cls(content=content, doc_type="JSON")
        
    def __str__(self):
        return f"[Document: {self.doc_type}] {self.content}"

def demonstrate_factory():
    section_header("Factory Pattern (@classmethod)")
    
    # We use the factory methods to construct the object in different ways!
    doc1 = Document.from_csv("id,name\n1,Alice\n2,Bob")
    doc2 = Document.from_json('{"key": "value"}')
    
    print(doc1)
    print(doc2)


# ==============================================================================
# 4. THE STRATEGY PATTERN (VIA FIRST-CLASS FUNCTIONS)
# ==============================================================================
# In Java, the Strategy Pattern requires an interface (DiscountStrategy) and 
# multiple classes (TenPercentDiscount, FlatDiscount). 
# In Python, we just pass a function!

def ten_percent_discount(order_total: float) -> float:
    return order_total * 0.90

def flat_discount(order_total: float) -> float:
    return order_total - 10.0 if order_total > 10.0 else 0.0

class Order:
    def __init__(self, total: float, discount_strategy: Callable[[float], float]):
        self.total = total
        self.discount_strategy = discount_strategy # The Strategy!
        
    def get_final_price(self) -> float:
        # We simply call the injected strategy function
        return self.discount_strategy(self.total)

def demonstrate_strategy():
    section_header("Strategy Pattern (Functions as objects)")
    
    order1 = Order(100.0, ten_percent_discount)
    order2 = Order(100.0, flat_discount)
    
    print(f"10% Discount Strategy:  ${order1.get_final_price():.2f}")
    print(f"Flat Discount Strategy: ${order2.get_final_price():.2f}")


# ==============================================================================
# 5. THE OBSERVER PATTERN (PUB / SUB)
# ==============================================================================

class Subject:
    def __init__(self):
        self._observers: List[Callable[[Any], None]] = []
        self._state = None
        
    def attach(self, observer: Callable[[Any], None]):
        self._observers.append(observer)
        
    def set_state(self, state: Any):
        print(f"  [Subject] State changing to: {state}")
        self._state = state
        self._notify()
        
    def _notify(self):
        for observer in self._observers:
            # Call the observer function and pass the new state
            observer(self._state)

def email_alert_observer(state: Any):
    print(f"  [Observer 1] Sending Email Alert for state: {state}")
    
def database_logger_observer(state: Any):
    print(f"  [Observer 2] Logging state to Database: {state}")

def demonstrate_observer():
    section_header("Observer Pattern (Pub/Sub)")
    
    system = Subject()
    
    # Attach the observers (subscribers)
    system.attach(email_alert_observer)
    system.attach(database_logger_observer)
    
    # When the state changes, the subject automatically notifies all observers
    print("Triggering state change 1:")
    system.set_state("CRITICAL_ERROR")
    
    print("\nTriggering state change 2:")
    system.set_state("RESOLVED")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `@classmethod` used for the Factory Pattern in Python?
   Answer: It provides alternative constructors. Because it receives the class `cls` as its first argument, it can instantiate and return the object without hardcoding the class name, allowing it to work perfectly even if subclassed.

2. Why is the Strategy Pattern simpler in Python than in Java?
   Answer: In Java, functions cannot exist on their own, so you must create an Interface and multiple Classes to hold the different algorithms. In Python, functions are first-class objects, so you can simply pass the algorithm (function) directly into the object.

3. What is the Observer Pattern?
   Answer: It is a publish-subscribe architecture where a Subject maintains a list of Observers (functions or objects). When the Subject's state changes, it loops through the list and notifies all Observers automatically, decoupling the source of the event from the systems that react to it.
"""

if __name__ == "__main__":
    demonstrate_factory()
    demonstrate_strategy()
    demonstrate_observer()
    print("\n[SUCCESS] Laboratory: Design Patterns Completed.")
