"""
# ==============================================================================
# LABORATORY: ADVANCED CLASSES, OBJECTS, AND MEMORY
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Basic OOP is easy. Professional OOP requires understanding how Python constructs 
# objects (__new__), how it resolves inheritance trees (MRO/C3 Linearization), 
# and how to strictly control state and memory overhead using @property and __slots__.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between object CREATION (__new__) and INITIALIZATION (__init__).
# - Implement the Singleton pattern using __new__.
# - Master Multiple Inheritance and the Method Resolution Order (MRO).
# - Understand Abstract Base Classes (abc) for enforcing interface contracts.
# - Use @property for computed attributes and encapsulation.
# - Optimize memory for millions of objects using __slots__.
#
# ==============================================================================
"""

import sys
from abc import ABC, abstractmethod
from typing import Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. __NEW__ VS __INIT__ (THE SINGLETON PATTERN)
# ==============================================================================

class DatabaseConnection:
    """
    __new__ actually creates the memory for the object.
    __init__ just populates it.
    By overriding __new__, we can hijack the creation process to implement a Singleton 
    (where only ONE instance of this class can ever exist).
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("  [SYSTEM] Creating the physical DatabaseConnection object...")
            # We call the base object's __new__ to actually allocate memory
            cls._instance = super().__new__(cls)
        else:
            print("  [SYSTEM] Returning cached DatabaseConnection object...")
        return cls._instance

    def __init__(self, dsn: str):
        # TRAP: __init__ is called EVERY TIME you do DatabaseConnection().
        # Even if __new__ returns the cached instance, __init__ re-runs!
        print(f"  [INIT] Initializing with DSN: {dsn}")
        self.dsn = dsn

def demonstrate_new_vs_init():
    section_header("__new__ vs __init__ (Singleton)")
    
    db1 = DatabaseConnection("postgres://localhost")
    db2 = DatabaseConnection("mysql://remote")
    
    print(f"\ndb1 ID: {id(db1)} | dsn: {db1.dsn}")
    print(f"db2 ID: {id(db2)} | dsn: {db2.dsn}")
    assert db1 is db2, "They are the exact same memory object."


# ==============================================================================
# 4. MULTIPLE INHERITANCE & MRO (C3 LINEARIZATION)
# ==============================================================================

class A:
    def process(self):
        print("  Processing A")

class B(A):
    def process(self):
        print("  Processing B")
        super().process()

class C(A):
    def process(self):
        print("  Processing C")
        super().process()

# D inherits from both B and C (Diamond problem)
class D(B, C):
    def process(self):
        print("  Processing D")
        super().process()

def demonstrate_mro():
    """
    Python resolves the "Diamond Problem" (which parent's method to call first) 
    using the C3 Linearization algorithm.
    """
    section_header("Method Resolution Order (MRO)")
    
    print("MRO for Class D:")
    for cls in D.mro():
        print(f" - {cls.__name__}")
        
    print("\nExecuting D().process():")
    # Because of super(), the calls chain according to the MRO: D -> B -> C -> A
    obj = D()
    obj.process()


# ==============================================================================
# 5. ABSTRACT BASE CLASSES (ENFORCING CONTRACTS)
# ==============================================================================

class BaseDataExtractor(ABC):
    """
    An ABC (Abstract Base Class) cannot be instantiated.
    It forces any child class to implement the @abstractmethod methods.
    """
    @abstractmethod
    def extract(self) -> str:
        pass
        
    def log(self, msg: str):
        print(f"[LOG] {msg}")

class CsvExtractor(BaseDataExtractor):
    # If we do not implement extract(), Python will throw a TypeError upon instantiation.
    def extract(self) -> str:
        self.log("Extracting CSV...")
        return "csv_data"

def demonstrate_abc():
    section_header("Abstract Base Classes (ABC)")
    
    # ext = BaseDataExtractor() # ERROR: TypeError (Can't instantiate abstract class)
    
    extractor = CsvExtractor()
    print(extractor.extract())


# ==============================================================================
# 6. ENCAPSULATION WITH @PROPERTY
# ==============================================================================

class TemperatureSensor:
    def __init__(self, celsius: float):
        self._celsius = celsius # Protected attribute
        
    @property
    def celsius(self) -> float:
        """Getter: Looks like an attribute, acts like a method."""
        return self._celsius
        
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Setter: Adds validation to the assignment."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is impossible!")
        self._celsius = value
        
    @property
    def fahrenheit(self) -> float:
        """Computed property. No setter provided, making it read-only."""
        return (self._celsius * 9/5) + 32

def demonstrate_properties():
    section_header("@property (Getters, Setters, Validation)")
    
    sensor = TemperatureSensor(25.0)
    
    # We access 'celsius' as if it's a raw variable, but it calls the @property
    print(f"Current temp: {sensor.celsius}°C")
    
    # We assign as if it's a raw variable, but it calls the @celsius.setter
    sensor.celsius = 30.0
    print(f"Updated temp: {sensor.celsius}°C")
    
    # Computed read-only property
    print(f"In Fahrenheit: {sensor.fahrenheit}°F")
    
    # Error handling
    try:
        sensor.celsius = -300.0
    except ValueError as e:
        print(f"Validation caught error: {e}")


# ==============================================================================
# 7. MEMORY OPTIMIZATION: __SLOTS__
# ==============================================================================

class PointNormal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlotted:
    # __slots__ prevents the creation of the __dict__ for this class.
    # It hardcodes the memory layout in C, saving massive amounts of RAM.
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

def demonstrate_slots():
    section_header("__slots__ Memory Optimization")
    
    p_norm = PointNormal(1, 2)
    p_slot = PointSlotted(1, 2)
    
    # Every normal object has a __dict__ holding its attributes
    print(f"Normal object dict: {p_norm.__dict__}")
    
    # Slotted objects DO NOT have a __dict__!
    print(f"Slotted object has __dict__? {hasattr(p_slot, '__dict__')}")
    
    # RAM Comparison
    # Note: sys.getsizeof() is tricky. For normal objects, we must add the size of the dict!
    size_norm = sys.getsizeof(p_norm) + sys.getsizeof(p_norm.__dict__)
    size_slot = sys.getsizeof(p_slot)
    
    print(f"Approx RAM per Normal object: {size_norm} bytes")
    print(f"Approx RAM per Slotted object: {size_slot} bytes")
    
    # TRAP: You cannot add new attributes to a slotted object at runtime.
    try:
        p_slot.z = 10
    except AttributeError as e:
        print(f"__slots__ trap: {e}")


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain `__new__` vs `__init__`.
   Answer: `__new__` is a class method that allocates memory and CREATES the object. It returns the object. `__init__` is an instance method that takes the created object (`self`) and INITIALIZES its variables.

2. What is the Method Resolution Order (MRO)?
   Answer: It is the order Python searches through the parent classes when you call a method or attribute. It uses the C3 Linearization algorithm to ensure parents are searched left-to-right and a parent is never searched before all of its children have been searched.

3. Why use `@property`?
   Answer: It allows you to access a method as if it were a simple attribute. This provides encapsulation and validation (via setters) without forcing the user to type `obj.get_value()` and `obj.set_value()`.

4. How does `__slots__` save memory?
   Answer: Normal Python objects store their attributes in a dictionary (`__dict__`). Dictionaries have significant memory overhead. `__slots__` tells Python to use a fixed-size C-struct instead, drastically reducing RAM usage when creating millions of instances.
"""

if __name__ == "__main__":
    demonstrate_new_vs_init()
    demonstrate_mro()
    demonstrate_abc()
    demonstrate_properties()
    demonstrate_slots()
    print("\n[SUCCESS] Laboratory: Advanced OOP Completed.")
