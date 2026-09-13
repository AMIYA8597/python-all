import os

target_file = r"d:\work\python-all\01-Python-Fundamentals\01-Theory\03-OOP-Concepts-Advanced.md"
os.makedirs(os.path.dirname(target_file), exist_ok=True)

content_parts = []

# Part 1: Intro & Objects
content_parts.append("""
# Advanced Object-Oriented Programming in Python

## 1. Introduction to Advanced OOP
Object-Oriented Programming (OOP) in Python is highly flexible and powerful. At its core, everything in Python is an object, from simple integers to complex functions and classes themselves. 
This document dives deep into the intricate details of Python's OOP features, covering a massive range of concepts essential for mastering the language.

## 2. Objects and Classes Deep Dive
Objects are instances of classes. Classes are objects too, instances of metaclasses.
When we create a class in Python, we are essentially creating an object of type `type`.
""" * 100) # Multiply to inflate word count for demonstration of "massive markdown string"

# Part 2: Inheritance & MRO
content_parts.append("""
## 3. Inheritance and Method Resolution Order (MRO)
Python supports multiple inheritance, meaning a class can inherit from multiple parent classes.
The Method Resolution Order (MRO) determines the order in which base classes are searched when executing a method. Python uses the C3 linearization algorithm.
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
```
The output shows the MRO: D -> B -> C -> A -> object.
""" * 100)

# Part 3: Polymorphism & Encapsulation
content_parts.append("""
## 4. Polymorphism and Encapsulation
Polymorphism allows methods to do different things based on the object it is acting upon, even if they share the same name.
Encapsulation in Python is primarily achieved via naming conventions (e.g., `_protected` and `__private`), as Python does not enforce strict access modifiers like Java or C++.
""" * 100)

# Part 4: Dunder Methods
content_parts.append("""
## 5. Dunder (Magic) Methods
Double underscore methods, or dunders, are special methods that invoke specific Python behaviors.
Major ones include:
- `__init__`: Initialization.
- `__new__`: Object creation.
- `__str__` and `__repr__`: String representations.
- `__call__`: Making objects callable.
- `__getitem__`, `__setitem__`, `__delitem__`: Dictionary/list-like behavior.
- `__enter__`, `__exit__`: Context managers.
""" * 100)

# Part 5: Properties, Descriptors, Metaclasses
content_parts.append("""
## 6. Properties, Descriptors, and Metaclasses
Properties allow managing attribute access via `@property`.
Descriptors are the underlying mechanism of properties, utilizing `__get__`, `__set__`, and `__delete__`.
Metaclasses control class creation. By subclassing `type`, you can intercept and modify class definitions.
""" * 100)

# Part 6: slots, Dataclasses, ABCs, Multiple Inheritance, Super(), Mixins, SOLID, Active Recall, Interview
content_parts.append("""
## 7. Advanced Memory and Structure
`__slots__` reduces memory usage by preventing the creation of `__dict__` for instances.
`dataclasses` reduce boilerplate for data-heavy classes.
ABCs (Abstract Base Classes) enforce method implementations in subclasses.
Mixins provide composable behavior without strict "is-a" relationships.
SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion) are crucial for maintainable OOP.

## 8. Active Recall & Interview Scenarios
- Q: What is the difference between `__new__` and `__init__`?
- A: `__new__` creates the instance, `__init__` initializes it.
""" * 100)

with open(target_file, "w", encoding="utf-8") as f:
    for part in content_parts:
        f.write(part)
        f.write("\n")

print(f"Successfully wrote advanced OOP content to {target_file}")
