"""
## A. Concept Name
Advanced Object-Oriented Programming in Python (Dunders, Properties, Slots, MRO, and Metaclasses)

## B. One-Sentence Definition
Advanced OOP features in Python allow you to deeply integrate custom objects into Python's core syntax, optimize their memory footprint, rigorously control attribute access, and elegantly manage complex inheritance hierarchies.

## C. Why Does This Exist?
When building simple scripts, basic classes are enough. But as systems grow, especially in complex AI/ML frameworks (like PyTorch or TensorFlow):
- You want custom objects to behave like built-in types (e.g., adding two objects with `+`).
- You need to validate data upon assignment without breaking existing APIs.
- You instantiate millions of objects and can't afford Python's default memory overhead.
- You build deeply nested architectures and need predictable method resolution.

## D. Intuition
Think of a standard Python class as a generic, plain box. It works, but it doesn't plug into the rest of the factory (Python's built-in functions). Advanced OOP provides the "adapters" (dunder methods), "access control points" (properties), "blueprints for blueprints" (metaclasses), and "space-savers" (slots) to make your box an enterprise-grade machine.

## E. Real-Life Analogy
Basic OOP is building a car from a generic kit.
Advanced OOP is building a Tesla:
- Properties: The dashboard limits you to safe speeds (validation) while abstracting the engine.
- Dunder methods: Standard charging cables plug perfectly into your custom port.
- `__slots__`: Stripping out unneeded weight for track-level performance.
- MRO: A strict chain of command when the computer, driver, and sensors all give conflicting steering inputs.

## F. Mental Model
- Dunder methods (`__init__`, `__add__`): The Hooks. Python checks for these hooks when performing operations.
- `@property`: The Guard. Looks like an attribute, acts like a method.
- `__slots__`: The Corset. Prevents dynamic bloat, fixing the object's shape in memory.
- MRO (Method Resolution Order): The Ancestry Tree. A strict left-to-right, depth-first algorithm to resolve inheritance conflicts.

## G. Visual Explanation
The typical object memory vs Slotted object:

DEFAULT INSTANCE
+--------------------+
| obj                | ---> [ pointer to dict ] ---> { 'x': 10, 'y': 20, 'dynamic': 'allowed' } (Heavy overhead)
+--------------------+

SLOTTED INSTANCE
+--------------------+
| obj (__slots__)    | ---> [ x: 10 | y: 20 ] (Direct memory array, fixed size, fast, no dict)
+--------------------+

MRO Diamond Problem (D inherits from B and C, which inherit from A)
    A
  /   \
 B     C
  \   /
    D

Python's C3 Linearization determines the MRO: D -> B -> C -> A -> object.

## H. Formal Explanation
Python's data model heavily relies on "magic" methods (surrounded by double underscores). Operations like `x + y` translate to `x.__add__(y)`. `@property` wraps methods in a descriptor object, triggering functions on attribute access. `__slots__` replaces the instance `__dict__` with a statically sized array in C. MRO uses the C3 linearization algorithm to ensure monotonic, predictable method resolution in multiple inheritance.

## I. Mathematical Foundation (if applicable)
Let C be a class that inherits from B1, B2, ..., BN.
L(C) = [C] + merge(L(B1), L(B2), ..., L(BN), [B1, B2, ..., BN])
The merge process takes the head of the first list. If it is not in the tail of any other list, it is added to the MRO and removed from all lists. Otherwise, it moves to the next head.

## J. From-Scratch Implementation (if applicable)
(See Python code below for Vector, App, and Singleton implementations.)

## K. Library / Production Implementation (if applicable)
Python's standard library relies on dunders everywhere. For example, `len()` calls `__len__()`, iteration calls `__iter__()`. `functools.total_ordering` is a great example of a class decorator interacting with dunder methods (`__eq__`, `__lt__`, etc.).

## L. Trace (walk through example)
Let's trace `App().greet()`:
1. `App.greet()` is called. Returns "App -> " + `super().greet()`.
2. In `App`, `super()` resolves to the next in MRO, which is `PluginA`.
3. `PluginA.greet()` is called. Returns "PluginA -> " + `super().greet()`.
4. Crucially, in `PluginA`, `super()` resolves to the next class in `App`'s MRO, which is `PluginB` (NOT `Base`!).
5. `PluginB.greet()` is called. Returns "PluginB -> " + `super().greet()`.
6. In `PluginB`, `super()` resolves to `Base`.
7. `Base.greet()` returns "Base".
8. The final unwound string: "App -> PluginA -> PluginB -> Base".

## M. Complexity
- **Time**: 
  - Attribute access with `@property`: O(1) + minor function call overhead.
  - Instance creation with `__slots__`: Faster (O(1)) than allocating a dict.
- **Space**:
  - Without slots: Base object size + dict overhead (~100-200 bytes per object).
  - With slots: C-level array of pointers (~40-50 bytes per object).

## N. Common Mistakes
- **Mutable default args in class variables**: e.g., `class A: items = []`. Modifying `A().items` affects ALL instances.
- **`super()` misunderstanding**: Thinking `super()` in a parent class calls its *own* parent. No, `super()` delegates to the *next class in the instance's MRO*.
- **Forgetting `NotImplemented`**: Returning `False` instead of `NotImplemented` in `__eq__`. If you return `NotImplemented`, Python gracefully tries the reverse operation `other.__eq__(self)`.
- **Using `__slots__` incorrectly**: Inheriting from a class without `__slots__` negates the memory benefits.

## O. Common Confusions
- **`@classmethod` vs `@staticmethod`**: 
  - `@classmethod` takes `cls` as the first argument. Useful for alternative constructors.
  - `@staticmethod` takes no implicit first argument. Just a normal function grouped inside a class for namespace organization.
- **`__str__` vs `__repr__`**:
  - `__str__`: For end-users (readable).
  - `__repr__`: For developers (unambiguous, ideally executable code to recreate the object). Fallback for `__str__`.
- **`__getattr__` vs `__getattribute__`**:
  - `__getattr__`: Called ONLY when an attribute is NOT found normally.
  - `__getattribute__`: Called for EVERY attribute access. Danger: easy to cause infinite recursion.

## P. When To Use
- **`@property`**: When you need validation on attribute assignment, or when an attribute is dynamically computed (e.g., `circle.area`).
- **`__slots__`**: When you are creating millions of instances of a simple data class (e.g., nodes in a graph, elements in a dataset).
- **Dunders (`__add__`, `__getitem__`)**: When you want your object to behave like native Python numbers, lists, or contexts (using `with`).

## Q. When NOT To Use
- **`__slots__`**: On objects that need dynamic attributes, or classes meant to be subclassed by external users who might need flexibility.
- **Deep Multiple Inheritance**: Diamond inheritance is confusing. Prefer composition over inheritance.
- **Metaclasses**: 99% of the time. If you think you need a metaclass, you probably just need decorators or class decorators.

## R. Trade-offs
- Memory (`__slots__`) vs Flexibility (`__dict__`).
- Elegance (`@property`) vs Transparency (explicit getters/setters like `set_value()` make it obvious that computation/validation is occurring).
- Power (Metaclasses) vs Readability (Metaclasses add significant cognitive load for other developers).

## S. Debugging
- **MRO issues**: Use `print(ClassName.__mro__)` or `print(ClassName.mro())` to explicitly see the resolution order.
- **Slot errors**: `AttributeError: 'Vector' object has no attribute 'z'`. This is a *feature* of slots, blocking dynamic creation. Ensure all needed variables are in `__slots__`.

## T. Memory Hook (a short memorable principle)
- "Properties Protect, Slots Shrink, Dunders Delegate, MRO Maps."

## U. Active Recall (questions before answers)
1. Why does `__slots__` save memory?
   - It eliminates the `__dict__` overhead, storing attributes in a statically sized array.
2. How does C3 linearization resolve the diamond inheritance problem?
   - It computes a monotonic, left-to-right depth-first order while preserving local precedence and preventing duplicate classes.
3. What is the difference between returning `NotImplemented` and `False` in `__eq__`?
   - `NotImplemented` signals Python to try the reflected operation (`other.__eq__(self)`); `False` just definitively says they aren't equal.
4. When should you use `@classmethod` over `@staticmethod`?
   - When you need access to the class itself, primarily to instantiate it (e.g., alternative constructors like `from_json`).

## V. Practice (exercises)
Exercise: Create a `Temperature` class.
- It should initialize with Celsius.
- Use `@property` to allow getting/setting `fahrenheit`.
- When setting `fahrenheit`, mathematically update the internal celsius value.
- Add a dunder method so `temp1 > temp2` works correctly.
(See code section below for solution)

## W. Interview Question
Q: What is a Metaclass, and how would you implement a Singleton using it?
A: A metaclass is a "class of a class". Just as an object is an instance of a class, a class is an instance of a metaclass (by default, `type`). Metaclasses intercept class creation.
To implement a Singleton (ensure only one instance of a class exists), we override the `__call__` method of the metaclass, which dictates what happens when the class is "called" (instantiated).

## X. Project Connection
In PyTorch, `torch.nn.Module` relies heavily on advanced OOP:
- **`__setattr__` and `__getattr__`**: When you do `self.conv = nn.Conv2d(...)` inside a Module, PyTorch intercepts this assignment to automatically register `conv` as a sub-module, ensuring its parameters are tracked by the optimizer.
- **`__call__`**: Calling a model `output = model(input)` executes `__call__`, which triggers pre-forward hooks, calls the `forward()` method, and triggers post-forward hooks.
- **Multiple Inheritance**: Dataset classes in PyTorch often use mixins (multiple inheritance) to add specific sampling or transformation behaviors while retaining the core `IterableDataset` base.
"""

import sys
import timeit
from typing import Any

# ==========================================
# J. From-Scratch Implementation
# ==========================================

class Vector:
    """
    Demonstrates Dunders (Magic Methods) and Slots for memory efficiency.
    """
    # Slots prevent the creation of __dict__ and __weakref__, saving ~60% memory per instance.
    __slots__ = ('_x', '_y')

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y

    # --- PROPERTIES ---
    @property
    def x(self) -> float:
        """Getter for x."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Setter with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Coordinate must be numeric")
        self._x = float(value)

    @property
    def y(self) -> float:
        """Getter for y."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Setter with validation."""
        if not isinstance(value, (int, float)):
            raise TypeError("Coordinate must be numeric")
        self._y = float(value)

    # --- DUNDER METHODS (Data Model Hooks) ---
    def __repr__(self) -> str:
        """Official string representation (fallback for __str__)."""
        return f"Vector(x={self._x}, y={self._y})"

    def __eq__(self, other: Any) -> bool:
        """Defines behavior for == operator."""
        if not isinstance(other, Vector):
            return NotImplemented
        return self._x == other.x and self._y == other.y

    def __add__(self, other: 'Vector') -> 'Vector':
        """Defines behavior for + operator."""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self._x + other.x, self._y + other.y)

    # --- CLASS & STATIC METHODS ---
    @classmethod
    def from_tuple(cls, coords: tuple[float, float]) -> 'Vector':
        """Alternative constructor using @classmethod."""
        return cls(coords[0], coords[1])

    @staticmethod
    def origin() -> 'Vector':
        """Utility method that doesn't need class or instance state."""
        return Vector(0.0, 0.0)


# --- MULTIPLE INHERITANCE AND MRO ---
class Base:
    def greet(self):
        return "Base"

class PluginA(Base):
    def greet(self):
        return f"PluginA -> {super().greet()}"

class PluginB(Base):
    def greet(self):
        return f"PluginB -> {super().greet()}"

class App(PluginA, PluginB):
    """
    Inherits from PluginA and PluginB.
    MRO will be App -> PluginA -> PluginB -> Base -> object
    """
    def greet(self):
        return f"App -> {super().greet()}"


# ==========================================
# V. Practice Solution
# ==========================================
class Temperature:
    def __init__(self, c: float):
        self._c = c
        
    @property
    def fahrenheit(self) -> float:
        return (self._c * 9/5) + 32
        
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self._c = (value - 32) * 5/9
        
    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self._c > other._c


# ==========================================
# W. Interview Question Solution
# ==========================================
class SingletonMeta(type):
    """
    A metaclass for the Singleton pattern.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        # cls is the class being instantiated, e.g., Database
        if cls not in cls._instances:
            # Create the instance and store it
            cls._instances[cls] = super().__call__(*args, **kwargs)
        # Return the stored instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        pass


# ==========================================
# Run Examples
# ==========================================
if __name__ == "__main__":
    print("--- Testing Vector ---")
    v1 = Vector(1, 2)
    v2 = Vector.from_tuple((3, 4))
    v3 = v1 + v2
    print(f"v1 + v2 = {v3}")
    print(f"Is v3 == Vector(4, 6)? {v3 == Vector(4, 6)}")
    
    # Try invalid property assignment
    try:
        v1.x = "string" # type: ignore
    except TypeError as e:
        print(f"Validation worked: {e}")

    print("\n--- Testing MRO ---")
    app = App()
    print(app.greet())
    print("MRO:", [c.__name__ for c in App.mro()])
    
    print("\n--- Testing Singleton ---")
    db1 = Database()
    db2 = Database()
    print(f"db1 is db2: {db1 is db2}")

    print("\n--- Testing Temperature (Practice) ---")
    t1 = Temperature(0)
    print(f"0C in Fahrenheit is {t1.fahrenheit}F")
    t1.fahrenheit = 212
    print(f"212F in Celsius is {t1._c}C")
    t2 = Temperature(110)
    print(f"Is t2 (110C) > t1 (100C)? {t2 > t1}")

    print("\n--- Memory Benchmarks (Slots vs Dict) ---")
    class NoSlotVector:
        def __init__(self, x, y):
            self.x, self.y = x, y

    v_slot = Vector(1, 2)
    v_dict = NoSlotVector(1, 2)
    
    # sys.getsizeof doesn't deep-measure dicts, but we can measure the dict itself
    dict_size = sys.getsizeof(v_dict.__dict__)
    slot_size = sys.getsizeof(v_slot)
    print(f"NoSlotVector dict size: {dict_size} bytes (plus object overhead)")
    print(f"Vector (slotted) size: {slot_size} bytes (TOTAL)")
    
    t_slot = timeit.timeit("Vector(1, 2)", globals=globals(), number=100000)
    t_dict = timeit.timeit("NoSlotVector(1, 2)", globals=globals(), number=100000)
    print(f"Instantiation speed (100k): Slotted {t_slot:.4f}s vs Dict {t_dict:.4f}s")
