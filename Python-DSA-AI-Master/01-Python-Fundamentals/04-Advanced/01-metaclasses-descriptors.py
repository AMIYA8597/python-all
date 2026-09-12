"""
## A. Concept Name
Metaclasses and Descriptors in Python

## B. One-Sentence Definition
Descriptors are objects that govern attribute access via `__get__`, `__set__`, and `__delete__`, while metaclasses are "classes of classes" that govern how classes themselves are created and behave.

## C. Why Does This Exist?
They exist to provide powerful, flexible hooks into Python's underlying object-oriented mechanics. Descriptors abstract away getter/setter logic into reusable components (like `@property`). Metaclasses allow for automatic modification, registration, or validation of classes at creation time (like `type`).

## D. Intuition
Think of a class as a template for creating objects. A **metaclass** is the template for creating that template. 
Think of an attribute as a variable attached to an object. A **descriptor** intercepts the dot `.` operator so you can run custom code whenever someone reads, writes, or deletes that variable.

## E. Real-Life Analogy
**Descriptor**: Like a bouncer at a club door. When someone tries to enter (access an attribute), the bouncer checks their ID (runs validation logic) before letting them in or turning them away.
**Metaclass**: Like an architect designing a factory. The factory produces cars (classes produce instances), but the architect decides how the factory itself is built (the metaclass creates the class).

## F. Mental Model
- Regular Object Creation: `Instance = Class()`
- Class Creation: `Class = Metaclass()`
- Attribute Access without Descriptor: `obj.attr` -> directly fetches from `obj.__dict__`
- Attribute Access with Descriptor: `obj.attr` -> calls `Descriptor.__get__(self, obj, type)`

## G. Visual Explanation
```text
Metaclass -> creates -> Class -> creates -> Instance
                       |
                       +-- contains Descriptor(s)
                       
Instance.attr_access --> Descriptor.__get__() / Descriptor.__set__()
```

## H. Formal Explanation
A **descriptor** is any object that defines at least one of the methods `__get__()`, `__set__()`, or `__delete__()`. They are invoked by the `__getattribute__()` method during attribute lookup. 
A **metaclass** is a class whose instances are classes. By default, `type` is the metaclass for all classes in Python. Custom metaclasses inherit from `type` and typically override `__new__` or `__init__` to modify the class dictionary before or after the class object is constructed.

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
See the `ValidatedField` and `SingletonMeta` classes in the code below for from-scratch implementations.

## K. Library / Production Implementation (if applicable)
- Descriptors: Python's built-in `@property`, `@classmethod`, `@staticmethod`, and `super()` are all implemented using descriptors. Django ORM fields (e.g., `models.CharField()`) are descriptors.
- Metaclasses: ABCs (Abstract Base Classes) use `ABCMeta`. Django models use a metaclass to parse fields and set up database tables.

## L. Trace (walk through example)
For the `CachedProperty` descriptor below:
1. First access to `comp.heavy_result`: `CachedProperty.__get__` is called.
2. It executes `self.func(instance)`, returning 42.
3. It stores 42 directly into `instance.__dict__['heavy_result']`.
4. Second access: Python finds `'heavy_result'` in the instance dictionary *before* looking at the non-data descriptor on the class. It returns 42 immediately without calling `__get__`.

## M. Complexity
- **Time Complexity:** 
  - Descriptors add a small overhead (function call) to attribute access, typically $O(1)$.
  - Metaclasses run only at import/class definition time, so runtime complexity for instance creation is unaffected (unless `__call__` is overridden, e.g., Singleton).
- **Space Complexity:** $O(1)$ additional space for descriptors per class, plus state stored in instance `__dict__`.

## N. Common Mistakes
1. Storing state on the descriptor instance itself instead of the object's `__dict__`. Since descriptors are class attributes, state stored on them is shared across all instances of the class!
2. Forgetting that descriptors must be instantiated at the class level, not inside `__init__`.

## O. Common Confusions
- **Data vs. Non-Data Descriptors**: A descriptor with `__set__` or `__delete__` is a *data descriptor*. One with only `__get__` is a *non-data descriptor*. Data descriptors take precedence over instance dictionaries, while instance dictionaries take precedence over non-data descriptors.

## P. When To Use
- **Descriptors**: Reusing attribute validation logic across multiple fields (e.g., ORM fields, typed attributes).
- **Metaclasses**: Class registration, automatic API generation, enforcing coding standards across subclasses, Singleton pattern.

## Q. When NOT To Use
- If a simple `@property` suffices, don't write a custom descriptor.
- If class decorators or simple inheritance can solve the problem, don't write a metaclass. "Metaclasses are deeper magic than 99% of users should ever worry about." - Tim Peters

## R. Trade-offs
- **Pros**: Extreme power, DRY (Don't Repeat Yourself) code for attribute access and class construction.
- **Cons**: High cognitive load for readers; can make debugging tracebacks confusing.

## S. Debugging
- Use `hasattr`, `getattr`, and `vars()` to inspect `__dict__` directly when descriptors behave unexpectedly.
- For metaclasses, insert `print()` or `breakpoint()` inside `__new__` to see exactly what dictionary of attributes is being passed to create the class.

## T. Memory Hook (a short memorable principle)
"Descriptors intercept the dot; Metaclasses build the box."

## U. Active Recall (questions before answers)
1. What methods make an object a descriptor?
2. Where must a descriptor be instantiated?
3. What is the default metaclass in Python?

## V. Practice (exercises)
1. Write a `TypeChecked` descriptor that ensures an attribute only accepts values of a specified type.
2. Write a metaclass that automatically converts all method names in a class to lowercase.

## W. Interview Question
Write a descriptor `CachedProperty` that computes a property once and caches the result for subsequent accesses. (Implementation provided below).

## X. Project Connection
Used heavily in Object-Relational Mappers (ORMs) like SQLAlchemy or Django to map Python attributes to database columns.
"""

import time
from typing import Any, Type, Dict, Tuple

# --- Basic Implementation: Property as a Built-in Descriptor ---
class Person:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        """Property is a built-in descriptor."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value


# --- Intermediate Implementation: Custom Descriptor ---
class ValidatedField:
    """A descriptor that validates attribute values."""
    def __init__(self, min_length: int = 0, max_length: int = 100) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.name: str = ""

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be a string")
        if not (self.min_length <= len(value) <= self.max_length):
            raise ValueError(f"{self.name} length must be between {self.min_length} and {self.max_length}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance: Any) -> None:
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class User:
    username = ValidatedField(min_length=3, max_length=15)
    
    def __init__(self, username: str) -> None:
        self.username = username


# --- Advanced Implementation: Custom Metaclass ---
class SingletonMeta(type):
    """A metaclass for implementing the Singleton design pattern."""
    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args: Tuple, **kwargs: Dict[str, Any]) -> Any:
        if cls not in cls._instances:
            # Call __new__ and __init__ of the class to create an instance
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """A singleton database connection."""
    def __init__(self) -> None:
        self.connected_at = time.time()


# --- Interview Challenge Solution Implementation ---
class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        # Overwrite the descriptor with the computed value in the instance dictionary
        instance.__dict__[self.name] = value
        return value

class ExpensiveComputation:
    @CachedProperty
    def heavy_result(self) -> int:
        print("Computing heavy_result...")
        time.sleep(0.1)  # Simulate expensive work
        return 42


# --- Tests ---
def run_tests() -> None:
    print("Testing Descriptors and Metaclasses...")

    # Test Property Descriptor
    p = Person("Alice")
    assert p.name == "Alice"
    try:
        p.name = 123  # type: ignore
        assert False, "Should raise TypeError"
    except TypeError:
        pass

    # Test Custom Descriptor
    u = User("Bob")
    assert u.username == "Bob"
    try:
        User("A")
        assert False, "Should raise ValueError due to length"
    except ValueError:
        pass

    # Test Singleton Metaclass
    db1 = DatabaseConnection()
    time.sleep(0.01)
    db2 = DatabaseConnection()
    assert db1 is db2
    assert db1.connected_at == db2.connected_at

    # Test CachedProperty
    comp = ExpensiveComputation()
    start = time.time()
    res1 = comp.heavy_result  # Computes
    duration1 = time.time() - start
    
    start = time.time()
    res2 = comp.heavy_result  # Uses cache
    duration2 = time.time() - start
    
    assert res1 == res2 == 42
    assert duration1 > 0.05
    assert duration2 < 0.01

    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
