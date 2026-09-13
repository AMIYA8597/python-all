"""
# ==============================================================================
# LABORATORY 07: OOP BASICS (CLASSES, INSTANCES, AND STATE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Everything in Python is an object, but understanding how to create your own 
# classes allows you to encapsulate state and behavior. This is fundamental for
# building maintainable systems, APIs, and Machine Learning pipelines (e.g., 
# writing custom PyTorch nn.Module classes).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between a Class (Blueprint) and an Instance.
# - Understand the `self` parameter.
# - Master the `__init__` constructor and instance attributes.
# - Differentiate between Class Attributes and Instance Attributes.
# - Understand encapsulation (name mangling with `__`).
# - Master basic Inheritance and method overriding.
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. CLASS VS INSTANCE, __INIT__, AND SELF
# ==============================================================================

class Robot:
    """
    A simple class representing a Robot.
    """
    # 1. The __init__ method initializes the state of a NEW instance.
    # It is called automatically after the object is created in memory.
    # 2. 'self' is the reference to the specific instance being created/modified.
    # It is NOT a keyword, just a strong convention.
    def __init__(self, name: str, battery: int = 100):
        self.name = name       # Instance attribute
        self.battery = battery # Instance attribute
        
    def introduce(self) -> None:
        """Instance method. Needs 'self' to access instance data."""
        print(f"Beep! I am {self.name}. Battery: {self.battery}%")
        
    def work(self) -> None:
        if self.battery >= 10:
            print(f"{self.name} is working...")
            self.battery -= 10
        else:
            print(f"{self.name} is out of battery! Please recharge.")

def demonstrate_basics():
    section_header("Classes, Instances, and `self`")
    
    # Instantiation (creates two distinct objects in memory)
    r1 = Robot("R2-D2")
    r2 = Robot("C-3PO", battery=50)
    
    print(f"r1 ID: {id(r1)} | r2 ID: {id(r2)}")
    assert r1 is not r2, "They are distinct instances in memory."
    
    # Method invocation
    # Under the hood, r1.introduce() becomes Robot.introduce(r1)
    r1.introduce()
    r2.introduce()
    
    # Modifying state
    r1.work()
    r1.introduce()


# ==============================================================================
# 4. CLASS ATTRIBUTES VS INSTANCE ATTRIBUTES
# ==============================================================================

class Fleet:
    # CLASS ATTRIBUTE: Shared among all instances of the class.
    # Lives on the Class object, not the instance object.
    total_robots_created = 0
    
    def __init__(self, name: str):
        self.name = name # INSTANCE ATTRIBUTE
        
        # We access the class attribute via the Class name to increment it globally
        Fleet.total_robots_created += 1

def demonstrate_attributes():
    section_header("Class vs Instance Attributes")
    
    print(f"Initial Fleet size: {Fleet.total_robots_created}")
    
    bot_a = Fleet("Alpha")
    bot_b = Fleet("Beta")
    
    print(f"Fleet size after 2 creations: {Fleet.total_robots_created}")
    
    # TRAP: Reading via the instance works (falls back to class dict)
    print(f"bot_a reads total_robots_created: {bot_a.total_robots_created}")
    
    # TRAP: WRITING via the instance creates a SHADOW instance attribute!
    bot_a.total_robots_created = 999 
    print("\n--- After bot_a.total_robots_created = 999 ---")
    print(f"bot_a total (Shadowed): {bot_a.total_robots_created}")
    print(f"bot_b total (Unchanged): {bot_b.total_robots_created}")
    print(f"Fleet class total (Unchanged): {Fleet.total_robots_created}")


# ==============================================================================
# 5. ENCAPSULATION AND NAME MANGLING
# ==============================================================================

class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        # A single underscore indicates "protected" (Convention only. Python won't stop you)
        self._internal_id = "ID-1234"
        
        # A double underscore triggers "name mangling" (Pseudo-private)
        self.__balance = balance
        
    def get_balance(self) -> float:
        return self.__balance
        
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount

def demonstrate_encapsulation():
    section_header("Encapsulation & Name Mangling")
    
    acc = BankAccount("Alice", 1000.0)
    print(f"Owner (Public): {acc.owner}")
    print(f"ID (Protected): {acc._internal_id}")
    
    # print(acc.__balance) # ERROR! AttributeError
    print("Direct access to __balance blocked. Using getter:")
    print(f"Balance: {acc.get_balance()}")
    
    # TRAP: It is NOT truly private. Python just renames it to _ClassName__attribute
    mangled_name = "_BankAccount__balance"
    print(f"\nAccessing mangled name directly (BAD PRACTICE): {getattr(acc, mangled_name)}")


# ==============================================================================
# 6. INHERITANCE AND SUPER()
# ==============================================================================

# Base Class
class Animal:
    def __init__(self, name: str):
        self.name = name
        
    def speak(self) -> str:
        return "..."

# Derived Class
class Dog(Animal):
    def __init__(self, name: str, breed: str):
        # super() dynamically finds the parent class and calls its method
        super().__init__(name)
        self.breed = breed
        
    # Overriding the parent method
    def speak(self) -> str:
        return "Woof!"

def demonstrate_inheritance():
    section_header("Basic Inheritance & super()")
    
    a = Animal("Generic")
    d = Dog("Rex", "German Shepherd")
    
    print(f"Animal says: {a.speak()}")
    print(f"Dog ({d.breed}) says: {d.speak()}")
    
    # Type checking
    print(f"\nIs 'd' a Dog? {isinstance(d, Dog)}")
    print(f"Is 'd' an Animal? {isinstance(d, Animal)} (Yes, polymorphism!)")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between a class and an instance?
   Answer: A class is a blueprint defining structure and behavior. An instance is a concrete object in memory created from that blueprint.

2. What does `__init__` do? Is it a constructor?
   Answer: It is an INITIALIZER, not a constructor. The object is already created in memory (by `__new__`) before `__init__` is called to set the initial state.

3. Why is `self` explicitly required in method definitions?
   Answer: Python does not automatically resolve variables to instance properties. You must explicitly tell Python to look in the instance namespace via `self.attribute`. When calling `obj.method()`, Python passes `obj` as the first argument automatically.

4. Are double underscores (`__attr`) truly private in Python?
   Answer: No. Python uses "name mangling" to change the attribute name to `_ClassName__attr` to prevent accidental overriding in subclasses, but it can still be accessed directly if you know the mangled name.

5. What happens if you do `instance.class_attribute = 10`?
   Answer: You create a local SHADOW instance attribute that hides the class attribute for that specific instance. The class attribute remains unchanged for all other instances.
"""

if __name__ == "__main__":
    demonstrate_basics()
    demonstrate_attributes()
    demonstrate_encapsulation()
    demonstrate_inheritance()
    print("\n[SUCCESS] Laboratory 07 Completed.")
