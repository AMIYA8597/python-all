"""
Metaclasses and Descriptors in Python

Learning Objectives:
1. Understand the concept of metaclasses and how they control class creation.
2. Master the descriptor protocol (__get__, __set__, __delete__).
3. Implement practical use cases for metaclasses (e.g., Singleton, validation).
4. Implement practical use cases for descriptors (e.g., typed attributes, lazy properties).

Concept Explanation:
- A class in Python is an object, and its type is a metaclass (by default, `type`).
- Metaclasses allow you to intercept class creation, modify class dictionaries, and enforce constraints on subclasses.
- A descriptor is an object attribute with "binding behavior", meaning its attribute access has been overridden by methods in the descriptor protocol.

Interview Focus:
- Explain what a metaclass is and give a practical use case.
- Implement a custom descriptor for attribute validation.
- Explain the difference between __getattr__, __getattribute__, and descriptors.
"""
import time
from typing import Any, Type, Dict, Callable

# ==========================================
# 1. Metaclasses
# ==========================================

class SingletonMeta(type):
    """
    A metaclass that creates a Singleton base class when called.
    """
    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if cls not in cls._instances:
            # Create the instance and store it
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    """Example of a Singleton using a metaclass."""
    def __init__(self):
        print("Initializing Database Connection")
        self.connected = True


# ==========================================
# 2. Descriptors
# ==========================================

class Typed:
    """
    A descriptor that enforces type checking on an attribute.
    """
    def __init__(self, name: str, expected_type: Type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Expected {self.expected_type}, got {type(value)}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance: Any) -> None:
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class Person:
    name = Typed("name", str)
    age = Typed("age", int)

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class LazyProperty:
    """
    A descriptor for a property that is only computed once and then cached.
    """
    def __init__(self, function: Callable):
        self.function = function
        self.name = function.__name__

    def __get__(self, instance: Any, owner: Type) -> Any:
        if instance is None:
            return self
        # Compute the value
        value = self.function(instance)
        # Cache the value in the instance dictionary
        # Subsequent accesses will read directly from __dict__ because
        # this is a non-data descriptor (no __set__).
        setattr(instance, self.name, value)
        return value

class DataAnalyzer:
    def __init__(self, data: list):
        self.data = data

    @LazyProperty
    def expensive_computation(self) -> int:
        print("Computing expensive result...")
        time.sleep(1) # Simulate expensive work
        return sum(self.data) * 2

# ==========================================
# Interview Challenge: API Model Validation
# ==========================================
# Use a metaclass and descriptors to build a simple declarative model validation system.

class Validator:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None: return self
        return instance.__dict__.get(self.name)

class StringField(Validator):
    def __init__(self, min_length=0, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if len(value) < self.min_length:
            raise ValueError(f"{self.name} must be >= {self.min_length} chars")
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"{self.name} must be <= {self.max_length} chars")
        instance.__dict__[self.name] = value

class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        fields = {k: v for k, v in namespace.items() if isinstance(v, Validator)}
        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for name, field in self._fields.items():
            if name in kwargs:
                setattr(self, name, kwargs[name])

class User(Model):
    username = StringField(min_length=3, max_length=20)
    email = StringField(min_length=5)

def test_metaclasses_and_descriptors():
    # Test Singleton
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    assert db1 is db2, "Singleton failed"
    
    # Test Typed Descriptor
    p = Person("Alice", 30)
    assert p.name == "Alice"
    try:
        p.age = "thirty"
        assert False, "TypeError expected"
    except TypeError:
        pass
    
    # Test Lazy Property
    analyzer = DataAnalyzer([1, 2, 3])
    # First access computes
    start = time.time()
    res1 = analyzer.expensive_computation
    time1 = time.time() - start
    
    # Second access caches
    start = time.time()
    res2 = analyzer.expensive_computation
    time2 = time.time() - start
    
    assert res1 == 12
    assert res1 == res2
    assert time1 > 0.5
    assert time2 < 0.1
    
    # Test API Model Validation
    user = User(username="admin", email="admin@example.com")
    assert user.username == "admin"
    try:
        User(username="ab")
        assert False, "ValueError expected for short username"
    except ValueError:
        pass

    print("All metaclass and descriptor tests passed!")

if __name__ == "__main__":
    test_metaclasses_and_descriptors()
