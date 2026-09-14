"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - OOP INTERNALS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have Class D which inherits from Class B and Class C. Both B 
# and C inherit from A. If I call a method on D, what is the exact mathematical 
# order in which Python searches the classes for that method?"
#
# This is the infamous "Diamond Problem" of Multiple Inheritance.
# If you don't understand the C3 Linearization algorithm (MRO), you will write 
# code that silently calls the wrong parent class, causing catastrophic bugs.
#
# Furthermore, they will ask you the difference between `__init__` and `__new__`.
# `__init__` does NOT create objects. It only initializes them. `__new__` is the 
# true physical allocator. If you are building a Singleton or intercepting 
# memory allocation, you must master `__new__`.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Method Resolution Order (MRO) and the Diamond Problem.
# - Understand the architecture of `super()`.
# - Master `__new__` vs `__init__` (Creating a Singleton).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MULTIPLE INHERITANCE (THE DIAMOND PROBLEM)
# ==============================================================================
class A:
    def execute(self):
        print("Executing A")

class B(A):
    def execute(self):
        print("Executing B")

class C(A):
    def execute(self):
        print("Executing C")

class D(B, C):
    """
    Class D inherits from both B and C. (Diamond Shape!)
    Who wins? Does D check B first, or C first?
    """
    pass

def demonstrate_mro():
    section_header("Method Resolution Order (MRO)")
    
    print("We have a Diamond Inheritance pattern: A <- (B, C) <- D")
    print("If we call `D().execute()`, which class executes?")
    
    obj_d = D()
    print("\nResult:")
    obj_d.execute()
    
    print("\nWhy B? Because of the C3 Linearization Algorithm (MRO).")
    print("Python mathematically flattens the graph into a strict 1D array.")
    print("Let's look at the exact mathematical sequence:")
    
    # .mro() reveals the internal C3 algorithm's array!
    mro_list = [cls.__name__ for cls in D.mro()]
    print(f"\nInternal MRO Array: {mro_list}")
    print("Python searches exactly in this order: D -> B -> C -> A -> object")


# ==============================================================================
# 4. __new__ VS __init__ (THE SINGLETON PATTERN)
# ==============================================================================
class DatabaseConnection:
    """
    A Singleton. We mathematically enforce that only ONE physical instance 
    of this class can EVER exist in RAM, no matter how many times you call it.
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """
        __new__ is the TRUE constructor. It physically allocates RAM.
        It runs BEFORE __init__.
        """
        if cls._instance is None:
            print("  -> [__new__] No instance exists! Physically allocating RAM...")
            # We call the core Python 'object' allocator to physically create it
            cls._instance = super().__new__(cls)
        else:
            print("  -> [__new__] Instance already exists! Intercepting allocation...")
            
        return cls._instance

    def __init__(self, connection_string: str):
        """
        __init__ is just an initializer. It receives the RAM block from __new__.
        NOTE: In a true Singleton, you must be careful because __init__ will 
        still run every time __new__ returns the instance!
        """
        print(f"  -> [__init__] Initializing with {connection_string}")
        self.connection_string = connection_string

def demonstrate_new_vs_init():
    section_header("__new__ vs __init__ (Singleton)")
    
    print("User 1 requests a Database Connection:")
    db1 = DatabaseConnection("AWS-RDS-1")
    
    print("\nUser 2 requests a Database Connection (Expects a brand new object):")
    db2 = DatabaseConnection("AWS-RDS-2")
    
    print("\nLet's check the physical memory addresses:")
    print(f"db1 address: {id(db1)}")
    print(f"db2 address: {id(db2)}")
    print(f"db1 is db2 : {db1 is db2} (They are the exact same physical object!)")


def run_all_labs():
    demonstrate_mro()
    demonstrate_new_vs_init()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Explain the C3 Linearization Algorithm (MRO) used in Python's Multiple Inheritance."
   Senior Answer: "When a class inherits from multiple parents, Python uses the C3 Linearization algorithm to flatten the inheritance graph into a strict 1-Dimensional list. The algorithm guarantees two mathematical rules: 1) Children always precede their parents. 2) The order of parents defined in the class signature (e.g., `class D(B, C)`) is strictly respected (B is searched before C). If the inheritance graph is completely twisted and violates these two rules (e.g., forming a cyclical paradox), the C3 algorithm mathematically fails at compile time and Python throws a `TypeError: Cannot create a consistent method resolution order`. You can view the final 1D list using `Class.mro()`."

2. Interviewer: "What is the physical difference between `__new__` and `__init__`?"
   Senior Answer: "`__new__` is a Class Method responsible for the physical allocation of RAM. It returns the raw, empty memory block (the object). `__init__` is an Instance Method. It does NOT allocate memory; it simply receives the memory block returned by `__new__` and populates it with attributes (like `self.name = 'Alice'`). You almost never touch `__new__` unless you are actively intercepting memory allocation, such as building a Singleton pattern (where you block `__new__` from allocating a second time) or subclassing immutable C-types like Tuple or String (where `__init__` is too late to modify the data, because the memory is already locked)."

3. Interviewer: "What does `super()` actually do under the hood?"
   Senior Answer: "`super()` is not just a hardcoded pointer to 'the parent class'. It is a dynamic proxy that relies entirely on the MRO list. If you have `A <- (B, C) <- D`, and you call `super().execute()` inside class `B`, it does NOT call `A`! It looks at the MRO list (`D, B, C, A`), sees that it is currently inside `B`, and mathematically shifts exactly one slot to the right, landing on `C`! So `B`'s `super()` calls `C`! This allows the Diamond pattern to traverse horizontally across sibling classes before finally moving up to the ultimate parent. This cooperative multiple inheritance is a unique and powerful feature of Python."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (OOP Internals) Completed.")
