"""
Module: Inheritance and Polymorphism

Learning Objectives:
1. Understand Object-Oriented Programming (OOP) concepts in Python.
2. Implement single and multiple inheritance.
3. Understand Method Resolution Order (MRO) and the `super()` function.
4. Implement polymorphism and abstract base classes.

Interview Questions Covered:
- How does multiple inheritance work in Python?
- Explain Method Resolution Order (MRO).
- How do you create an abstract base class (ABC)?
"""

from abc import ABC, abstractmethod
from typing import List

# ---------------------------------------------------------
# Concept 1: Abstract Base Classes & Polymorphism
# ---------------------------------------------------------
class Shape(ABC):
    """An abstract base class representing a generic shape."""
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return the name of the shape."""
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        
    def area(self) -> float:
        return self.width * self.height
        
    def name(self) -> str:
        return "Rectangle"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
        
    def area(self) -> float:
        import math
        return math.pi * (self.radius ** 2)
        
    def name(self) -> str:
        return "Circle"

def print_shape_areas(shapes: List[Shape]) -> None:
    """Demonstrates polymorphism by calling the same methods on different objects."""
    for shape in shapes:
        print(f"{shape.name()} Area: {shape.area():.2f}")

# ---------------------------------------------------------
# Concept 2: Multiple Inheritance and MRO
# ---------------------------------------------------------
class A:
    def process(self) -> str:
        return "A process"

class B(A):
    def process(self) -> str:
        return f"B process -> {super().process()}"

class C(A):
    def process(self) -> str:
        return f"C process -> {super().process()}"

class D(B, C):
    """
    Demonstrates the Diamond Problem and MRO.
    MRO for D: D -> B -> C -> A -> object
    """
    def process(self) -> str:
        return f"D process -> {super().process()}"

# ---------------------------------------------------------
# Tests and Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- Polymorphism Example ---")
    shapes = [Rectangle(4, 5), Circle(3)]
    print_shape_areas(shapes)
    
    print("\n--- Multiple Inheritance and MRO ---")
    d_instance = D()
    print("D process output:", d_instance.process())
    print("MRO of D:", [cls.__name__ for cls in D.__mro__])
