"""
# ==============================================================================
# LABORATORY: DESCRIPTORS AND METACLASSES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You use Descriptors and Metaclasses every day without realizing it. `@property`, 
# `@classmethod`, and `super()` are all implemented using Descriptors. Django ORM, 
# SQLAlchemy, and Pydantic build their models using Metaclasses. Mastering these 
# topics elevates you from a Python user to a framework designer.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Descriptor Protocol (`__get__`, `__set__`, `__delete__`).
# - Implement a custom Data Descriptor (Validation).
# - Understand `type` as the default Metaclass.
# - Write a custom Metaclass to intercept Class creation.
# - Implement the Metaclass Registry Pattern (The secret behind ORMs).
#
# ==============================================================================
"""

import sys
from typing import Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DESCRIPTOR PROTOCOL
# ==============================================================================
# A Descriptor is any object that implements __get__, __set__, or __delete__.
# It allows you to customize what happens when a class attribute is accessed.

class IntegerField:
    """
    A Data Descriptor that ensures an attribute is strictly an integer,
    and enforces a minimum and maximum value.
    This is EXACTLY how Django models and Pydantic fields work under the hood!
    """
    def __init__(self, min_value: int = None, max_value: int = None):
        self.min_value = min_value
        self.max_value = max_value
        # Python 3.6+ __set_name__ automatically gets the variable name
        self.name = None 

    def __set_name__(self, owner, name):
        # E.g., if assigned to 'age' in the User class, self.name = 'age'
        self.name = name

    def __get__(self, instance, owner) -> Any:
        # If accessed via the class (User.age), instance is None.
        if instance is None:
            return self
        # Fetch the value from the instance's dictionary
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value: Any) -> None:
        print(f"  [DESCRIPTOR] Validating {self.name} = {value}")
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer, got {type(value)}")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be <= {self.max_value}")
        
        # Store it in the instance's dictionary
        instance.__dict__[self.name] = value

class User:
    # We assign the Descriptor to the CLASS attribute.
    age = IntegerField(min_value=0, max_value=120)
    score = IntegerField(min_value=0)
    
    def __init__(self, name: str, age: int, score: int):
        self.name = name
        self.age = age      # Triggers IntegerField.__set__
        self.score = score  # Triggers IntegerField.__set__

def demonstrate_descriptors():
    section_header("Descriptors (Custom Validation Fields)")
    
    # Valid instantiation
    u = User("Alice", age=30, score=100)
    print(f"User created: {u.name}, Age: {u.age}")
    
    # Validation failures
    try:
        u.age = 150 # Triggers __set__ which raises ValueError
    except ValueError as e:
        print(f"Caught ValueError: {e}")
        
    try:
        u.score = "high" # Triggers __set__ which raises TypeError
    except TypeError as e:
        print(f"Caught TypeError: {e}")


# ==============================================================================
# 4. METACLASSES: CLASSES ARE OBJECTS TOO
# ==============================================================================
# Objects are instances of Classes.
# Classes are instances of Metaclasses!
# The default metaclass in Python is `type`.

class PluginMeta(type):
    """
    A custom Metaclass that intercepts the creation of any class that uses it.
    It automatically registers the class in a global dictionary.
    """
    registry = {}
    
    # __new__ is called when the CLASS is being defined in memory 
    # (NOT when an instance of the class is created).
    def __new__(mcs, name, bases, namespace):
        print(f"  [METACLASS] Intercepting creation of class: {name}")
        
        # We can modify the class before it is created!
        # Let's forcefully add an attribute to the class.
        namespace['is_plugin'] = True
        
        # Actually create the class object using the default 'type' logic
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Register it
        if name != "BasePlugin":
            mcs.registry[name] = cls
            
        return cls

class BasePlugin(metaclass=PluginMeta):
    pass

# When Python parses these lines, the Metaclass __new__ executes immediately!
class AudioPlugin(BasePlugin):
    pass

class VideoPlugin(BasePlugin):
    pass

def demonstrate_metaclasses():
    section_header("Metaclasses (The Registry Pattern)")
    
    print("\nPlugins automatically registered by the Metaclass:")
    for name, cls in PluginMeta.registry.items():
        print(f" - {name} (is_plugin: {cls.is_plugin})")
        
    # Notice we didn't have to write `registry.add(AudioPlugin)`.
    # It happened automatically at class creation time. This is how 
    # web frameworks auto-discover your Models and Views!


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a Descriptor?
   Answer: Any object that implements the `__get__`, `__set__`, or `__delete__` methods. It allows you to customize attribute lookup, assignment, and deletion.

2. How is `@property` implemented in Python?
   Answer: `@property` is simply a built-in Descriptor! It implements `__get__` and `__set__` to call your defined getter and setter functions.

3. What is a Metaclass?
   Answer: A "class of a class". Just as a class dictates how instances behave, a metaclass dictates how classes behave. The default metaclass is `type`.

4. When would you use a Metaclass in production?
   Answer: Metaclasses are used in framework design (like Django ORM or SQLAlchemy) to intercept class definitions. For example, to read the Data Descriptors defined on the class and automatically generate a corresponding SQL table schema in the database.
"""

if __name__ == "__main__":
    demonstrate_descriptors()
    demonstrate_metaclasses()
    print("\n[SUCCESS] Laboratory: Advanced OOP (Metaclasses) Completed.")
