"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - INHERITANCE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have a complex backend. I want to guarantee that every single 
# Database Connector class strictly implements a `connect()` and `query()` method. 
# If a junior developer creates a class without those methods, I want the code 
# to mathematically crash BEFORE it even runs."
#
# If you say "Just raise NotImplementedError in the parent class", you fail. 
# That only crashes at *Runtime* (when a user clicks a button on the live website).
# 
# You must use `abc.ABC` (Abstract Base Classes) to enforce structural contracts 
# that crash at *Instantiation Time* (when the server boots up).
#
# Interviewer: "What is Duck Typing?"
# A junior developer says: "If it walks like a duck, it's a duck."
# A senior developer explains that Python completely ignores Inheritance graphs 
# when calling methods, relying entirely on the physical presence of the 
# requested mathematical `__dunder__` method at Runtime.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Abstract Base Classes (`abc.ABC`).
# - Master Duck Typing (Dynamic Polymorphism).
# - Understand Mixins (Horizontal composition).
#
# ==============================================================================
"""

import abc

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ABSTRACT BASE CLASSES (ABC)
# ==============================================================================
class DatabaseConnector(abc.ABC):
    """
    An Abstract Base Class. You physically cannot instantiate this class.
    It serves purely as a strict structural blueprint for children.
    """
    
    @abc.abstractmethod
    def connect(self):
        """Children MUST implement this, or they will crash at instantiation!"""
        pass
        
    @abc.abstractmethod
    def query(self, sql: str):
        pass

class BadPostgresConnector(DatabaseConnector):
    """A junior developer forgot to implement `query()`!"""
    def connect(self):
        print("Connected to Postgres")
        
class GoodPostgresConnector(DatabaseConnector):
    def connect(self):
        print("Connected to Postgres")
        
    def query(self, sql: str):
        print(f"Executing: {sql}")

def demonstrate_abc():
    section_header("Abstract Base Classes (Enforcing Contracts)")
    
    print("Attempting to instantiate GoodPostgresConnector...")
    db = GoodPostgresConnector()
    db.connect()
    
    print("\nAttempting to instantiate BadPostgresConnector...")
    try:
        bad_db = BadPostgresConnector()
    except TypeError as e:
        print(f"  [CRASH PREVENTED] TypeError: {e}")
        print("  -> The ABC blocked the instantiation BEFORE it could cause a bug in production!")


# ==============================================================================
# 4. DUCK TYPING (DYNAMIC POLYMORPHISM)
# ==============================================================================
class Duck:
    def make_sound(self):
        print("Quack!")

class Robot:
    def make_sound(self):
        print("Bzzzt! Beep!")

def execute_sound(entity):
    """
    Notice there are ZERO Type Hints enforcing that `entity` is a Duck or an Animal.
    Python completely ignores inheritance graphs. It only cares about one thing:
    Does the physical `make_sound` function exist in RAM on this object?
    """
    entity.make_sound()

def demonstrate_duck_typing():
    section_header("Duck Typing (Dynamic Polymorphism)")
    
    d = Duck()
    r = Robot()
    
    print("Executing sound on a biological Duck:")
    execute_sound(d)
    
    print("Executing sound on a mechanical Robot:")
    execute_sound(r)
    
    print("\nThe function succeeded for both, even though they share ZERO inheritance.")
    print("This is the absolute core philosophy of Python Polymorphism.")


# ==============================================================================
# 5. MIXINS (HORIZONTAL COMPOSITION)
# ==============================================================================
class JSONExportMixin:
    """
    A Mixin is a class that contains methods for use by other classes without 
    having to be the parent class of those other classes. It is "horizontal" 
    functionality injection.
    """
    def export_to_json(self):
        import json
        # Relies on the child class having a __dict__!
        return json.dumps(self.__dict__)

class User(JSONExportMixin):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

def demonstrate_mixins():
    section_header("Mixins (Horizontal Injection)")
    
    u = User("Alice", "Admin")
    
    print("The User class has no `export_to_json` method of its own.")
    print("It inherited it horizontally from the Mixin!")
    
    json_data = u.export_to_json()
    print(f"\nResult: {json_data}")


def run_all_labs():
    demonstrate_abc()
    demonstrate_duck_typing()
    demonstrate_mixins()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is `abc.ABC` mathematically superior to simply raising `NotImplementedError` in a parent class?"
   Senior Answer: "If a parent class method simply raises `NotImplementedError`, the junior developer's child class will successfully instantiate and boot up the server. The bug will lay completely dormant in memory for 3 months until a live customer clicks a button that triggers the missing method, causing a catastrophic production crash at Runtime. `abc.ABC` fundamentally hooks into Python's `__new__` allocator. If the child class is missing an `@abstractmethod`, `abc.ABC` violently crashes the program at the exact millisecond you attempt to instantiate the class (Instantiation Time). It shifts the error detection massively to the left (Fail-Fast architecture)."

2. Interviewer: "Explain the philosophy of Duck Typing and how it relates to Python's Magic `__dunder__` methods."
   Senior Answer: "In Java (Static Typing), if you want to pass an object into `calculate_area(Shape s)`, the object MUST strictly inherit from the `Shape` interface, or the code will not compile. Python rejects this rigid hierarchy. Python uses Duck Typing: 'If it walks like a duck, it is a duck.' If you write `len(my_object)`, Python does not check if `my_object` inherits from a `Lengthable` interface. It simply looks at the object in RAM and asks: 'Do you physically possess the `__len__` dunder method?' If yes, it executes it. This allows massive flexibility, enabling objects of entirely different lineages to perfectly mimic each other's behavior simply by implementing the correct magic methods."

3. Interviewer: "What is a Mixin, and why do we use it instead of deep Inheritance trees?"
   Senior Answer: "Deep inheritance trees (e.g., `Animal` -> `Mammal` -> `Dog`) become incredibly brittle and mathematically impossible to maintain when you need to share functionality across completely unrelated branches (e.g., a `Bird` and an `Airplane` both need a `fly()` method, but they share no common parent except `object`). A Mixin is a lightweight, standalone class that contains exactly one specific slice of functionality (like `JSONExportMixin` or `FlyableMixin`). You inject it horizontally using Multiple Inheritance: `class Airplane(Vehicle, FlyableMixin)`. This heavily favors 'Composition over Inheritance', keeping the class hierarchy shallow and modular."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Inheritance & OOP) Completed.")
