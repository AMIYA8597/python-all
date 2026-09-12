"""
Design Patterns in Python.

## A. Concept Name
Design Patterns in Python

## B. One-Sentence Definition
Design patterns are typical, reusable solutions to commonly occurring problems in software design, adapted for Python's dynamic nature.

## C. Why Does This Exist?
They provide a standardized vocabulary for developers to communicate complex ideas and offer proven architectural blueprints that save time and reduce errors in software architecture.

## D. Intuition
Imagine building a house. Instead of inventing a new way to frame a window every time, you use a standard window framing pattern. Design patterns are the standard "blueprints" for common coding scenarios.

## E. Real-Life Analogy
A car manufacturing plant (Factory Pattern) produces different models of cars. A subscription to a magazine (Observer Pattern) notifies you every time a new issue is published. Using a universal travel adapter (Adapter Pattern) lets you plug your devices into any country's outlets.

## F. Mental Model
Think of patterns grouped into three families:
- Creational: How objects are built (e.g., Factory, Singleton).
- Structural: How objects are connected (e.g., Decorator, Adapter).
- Behavioral: How objects communicate (e.g., Observer, Strategy).

## G. Visual Explanation
Creational:
Class -> [Factory] -> Instantiated Object

Structural:
Object -> [Decorator] -> Enhanced Object

Behavioral:
Subject -> [State Change -> Notify] -> Observers

## H. Formal Explanation
In software engineering, a design pattern is a general repeatable solution to a commonly occurring problem in software design. A design pattern isn't a finished design that can be transformed directly into code. It is a description or template for how to solve a problem that can be used in many different situations, encouraging loose coupling and modularity.

## I. Mathematical Foundation (if applicable)
N/A. Design patterns are structural and behavioral paradigms rather than mathematical theorems.

## J. From-Scratch Implementation (if applicable)
See the code below for implementations of Singleton, Factory, Observer, and Strategy.

## K. Library / Production Implementation (if applicable)
- The Python `logging` module utilizes Singleton-like behavior for root loggers.
- Python's `iter()` and `__iter__` are native implementations of the Iterator pattern.
- Python's `@property`, `@classmethod`, and `@staticmethod` are native implementations of the Decorator pattern.

## L. Trace (walk through example)
For the Observer pattern:
1. `Subject` state is updated to "Active".
2. `Subject` calls its internal `notify()` method.
3. `notify()` iterates over attached observers (e.g., `LoggerObserver`, `EmailObserver`).
4. Each observer's `update()` method is triggered with the new state "Active", executing their specific logic.

## M. Complexity
- Time Complexity: Varies by pattern. Observer `notify()` is O(N) where N is the number of observers. Factory creation is typically O(1).
- Space Complexity: Singleton is O(1). Observer is O(N) for N observers stored in a list.

## N. Common Mistakes
- Over-engineering: Applying design patterns to simple problems where straightforward procedural code or simple classes would suffice.
- Ignoring Python's built-in features: Implementing complex GoF (Gang of Four) patterns (like Command or Iterator) when Python has native, simpler ways (like first-class functions and generators).

## O. Common Confusions
- Singleton vs. Module: In Python, a module is already a singleton. Often, creating a Singleton class is unnecessary when you can just use module-level variables and functions.
- Factory vs. Simple Class Instantiation: A factory is only needed when object creation logic is complex, requires abstraction, or depends dynamically on input.

## P. When To Use
- Singleton: Managing global configurations or database connection pools.
- Factory: Instantiating objects dynamically based on input or configuration (e.g., parsers for different file types).
- Observer: Event-driven systems, like UI updates, pub/sub systems, or push notifications.
- Strategy: Switching algorithms dynamically at runtime (e.g., different payment processing methods).

## Q. When NOT To Use
- When a simple script or function solves the problem clearly and concisely.
- When Python provides a built-in mechanism (e.g., don't write a bulky Iterator class, use a `yield` generator).

## R. Trade-offs
- Pros: High reusability, standard developer terminology, decoupled and modular code.
- Cons: Increased cognitive load, boilerplate code, potential for over-engineering simple solutions.

## S. Debugging
- Singletons carry global state, which can bleed across unit tests, causing unpredictable failures. Remember to reset state between tests or use Dependency Injection when testability is a priority.
- Observer chains can be hard to trace because the subject doesn't know what the observers do. Debugging event flows often requires extensive logging.

## T. Memory Hook (a short memorable principle)
"Creational creates, Structural structures, Behavioral behaves."

## U. Active Recall (questions before answers)
1. What pattern should you use if you only want ONE instance of a class ever?
2. What pattern separates an algorithm from the host class so it can be swapped at runtime?
3. In Python, what is the most Pythonic way to implement the Iterator pattern?

## V. Practice (exercises)
1. Implement the Builder pattern for constructing a complex `Computer` object step by step.
2. Rewrite the Singleton pattern logic using a Python module instead of a class.

## W. Interview Question
"How would you implement the Strategy Pattern in Python to apply different discount algorithms to an e-commerce shopping cart?"

## X. Project Connection
Design patterns are heavily used in large-scale applications: event busses (Observer), object mappers and serializers (Factory), and centralized configuration managers (Singleton).
"""

from typing import Any, Callable, Dict, List, Type


# --- Basic Implementation: Singleton Pattern ---
class SingletonMeta(type):
    """
    A thread-safe implementation of Singleton using a metaclass.
    """
    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Configuration(metaclass=SingletonMeta):
    """Configuration class strictly limited to a single instance."""
    def __init__(self) -> None:
        self.settings = {"debug": True, "version": "1.0"}


# --- Intermediate Implementation: Factory Pattern ---
class Animal:
    def speak(self) -> str:
        raise NotImplementedError

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

class AnimalFactory:
    """Factory pattern to create objects without specifying the exact class."""
    @staticmethod
    def get_animal(animal_type: str) -> Animal:
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        raise ValueError(f"Unknown animal type: {animal_type}")


# --- Advanced Implementation: Observer Pattern ---
class Subject:
    """The Subject maintains a list of observers and notifies them of state changes."""
    def __init__(self) -> None:
        self._observers: List[Callable[[str], None]] = []
        self._state: str = ""

    def attach(self, observer: Callable[[str], None]) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Callable[[str], None]) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer(self._state)

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: str) -> None:
        self._state = value
        self.notify()

class LoggerObserver:
    def update(self, state: str) -> None:
        print(f"Logger: Subject state changed to {state}")

class EmailObserver:
    def update(self, state: str) -> None:
        print(f"Email: Sending alert for state {state}")


# --- Strategy Pattern Implementation ---
class PaymentStrategy:
    """Abstract strategy for payment processing."""
    def pay(self, amount: float) -> str:
        raise NotImplementedError

class CreditCardStrategy(PaymentStrategy):
    """Concrete strategy for credit card payments."""
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using Credit Card."

class PayPalStrategy(PaymentStrategy):
    """Concrete strategy for PayPal payments."""
    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} using PayPal."

class PaymentProcessor:
    """Context class that uses a PaymentStrategy to process a payment."""
    def __init__(self, strategy: PaymentStrategy) -> None:
        self.strategy = strategy

    def process_payment(self, amount: float) -> str:
        return self.strategy.pay(amount)


# --- Tests ---
def run_tests() -> None:
    print("Testing Design Patterns...")

    # Test Singleton
    c1 = Configuration()
    c2 = Configuration()
    assert c1 is c2
    c1.settings["debug"] = False
    assert c2.settings["debug"] is False

    # Test Factory
    dog = AnimalFactory.get_animal("dog")
    assert dog.speak() == "Woof!"
    try:
        AnimalFactory.get_animal("dragon")
        assert False
    except ValueError:
        pass

    # Test Observer
    subject = Subject()
    logger = LoggerObserver()
    email = EmailObserver()
    subject.attach(logger.update)
    subject.attach(email.update)
    
    # Normally this prints to stdout, we just verify the state changes
    subject.state = "Active"
    assert subject.state == "Active"

    # Test Strategy
    processor1 = PaymentProcessor(CreditCardStrategy())
    assert processor1.process_payment(100.0) == "Paid $100.00 using Credit Card."
    
    processor2 = PaymentProcessor(PayPalStrategy())
    assert processor2.process_payment(50.5) == "Paid $50.50 using PayPal."

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
