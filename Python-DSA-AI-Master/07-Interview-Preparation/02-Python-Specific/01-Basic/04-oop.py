"""
Object-Oriented Programming (OOP) in Python: Interview Preparation

This module covers important OOP concepts:
- Classes and Objects, `__init__`, `self`
- Inheritance and Polymorphism
- Method Resolution Order (MRO) and `super()`
- Dunder (Magic) Methods (e.g., `__str__`, `__repr__`, `__eq__`)
- Properties (`@property`) for encapsulation
- Class Methods (`@classmethod`) and Static Methods (`@staticmethod`)

Beginner Explanation:
OOP is a way of organizing code using "objects", which bundle data (attributes) and behavior (methods).
A Class is a blueprint, and an Object is a real thing built from that blueprint. 
Inheritance lets a new class borrow features from an existing class.

Technical Explanation:
Python's object model is highly dynamic. Everything is an object, and classes are instances of `type`.
MRO (Method Resolution Order) is resolved using the C3 linearization algorithm, ensuring consistent 
lookup paths in multiple inheritance. 
Dunder methods provide hooks to override standard operators and built-in functions (like `len()`, `str()`).
"""
from typing import Any, List

class Employee:
    """
    Base class representing a generic employee.
    """
    # Class attribute: shared by all instances
    raise_amount: float = 1.05

    def __init__(self, first: str, last: str, pay: int):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self) -> str:
        """
        Using @property allows accessing this method like an attribute (e.g., emp.email)
        This is encapsulation in Python.
        """
        return f"{self.first.lower()}.{self.last.lower()}@company.com"

    @property
    def fullname(self) -> str:
        return f"{self.first} {self.last}"

    @fullname.setter
    def fullname(self, name: str) -> None:
        """
        Setter for the property.
        """
        first, last = name.split(' ')
        self.first = first
        self.last = last

    def apply_raise(self) -> None:
        """
        Applies the class-level raise amount to the instance pay.
        """
        self.pay = int(self.pay * self.raise_amount)

    @classmethod
    def set_raise_amt(cls, amount: float) -> None:
        """
        Class method operates on the class, not the instance.
        """
        cls.raise_amount = amount

    @staticmethod
    def is_workday(day_name: str) -> bool:
        """
        Static method doesn't take cls or self. It behaves like a regular function 
        but is included in the class namespace because it's logically related.
        """
        return day_name.lower() not in ["saturday", "sunday"]

    def __repr__(self) -> str:
        """
        Unambiguous string representation of the object, useful for debugging.
        """
        return f"Employee('{self.first}', '{self.last}', {self.pay})"

    def __str__(self) -> str:
        """
        Readable string representation of the object, for end users.
        """
        return f"{self.fullname} - {self.email}"


class Developer(Employee):
    """
    Subclass demonstrating Inheritance.
    """
    # Developers get a better raise
    raise_amount = 1.10

    def __init__(self, first: str, last: str, pay: int, prog_lang: str):
        # super() delegates to the parent class's method
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang


class Manager(Employee):
    """
    Another subclass demonstrating managing a list of employees.
    """
    def __init__(self, first: str, last: str, pay: int, employees: List[Employee] = None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp: Employee) -> None:
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp: Employee) -> None:
        if emp in self.employees:
            self.employees.remove(emp)


def demonstrate_mro():
    """
    Demonstrates Multiple Inheritance and Method Resolution Order (MRO).
    """
    class A:
        def do_something(self):
            return "A"

    class B(A):
        def do_something(self):
            return "B"

    class C(A):
        def do_something(self):
            return "C"

    class D(B, C):
        pass

    d = D()
    # D inherits from B and C. The MRO dictates it looks in D, then B, then C, then A.
    assert d.do_something() == "B"
    # mro() method shows the exact resolution order
    assert D.mro() == [D, B, C, A, object]


if __name__ == "__main__":
    emp_1 = Employee("Corey", "Schafer", 50000)
    dev_1 = Developer("Test", "User", 60000, "Python")
    
    assert emp_1.email == "corey.schafer@company.com"
    assert dev_1.email == "test.user@company.com"
    
    emp_1.fullname = "John Doe"
    assert emp_1.first == "John"
    assert emp_1.last == "Doe"
    
    emp_1.apply_raise()
    assert emp_1.pay == 52500
    
    assert Employee.is_workday("Monday") is True
    assert Employee.is_workday("Saturday") is False
    
    demonstrate_mro()
    print("All OOP examples passed.")
