"""
# ==============================================================================
# LABORATORY 01: VARIABLES, DATA TYPES, AND THE OBJECT MODEL
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python abstracts memory management and typing, which makes development fast. 
# However, this abstraction causes catastrophic bugs when scaling to Data Science 
# and AI if the engineer does not understand the underlying object model.
#
# Understanding that variables are "labels" (references) rather than "containers"
# is the single most important conceptual leap in mastering Python.
#
# 2. PREREQUISITES
# ----------------
# - Basic CLI usage.
# - Ability to run a python script: `python 01-variables-and-datatypes.py`
#
# 3. LEARNING OBJECTIVES
# ----------------------
# - Master the 'names vs objects' memory model.
# - Distinguish between mutability and immutability at the C-struct level.
# - Understand the Pass-by-Object-Reference parameter passing mechanism.
# - Master type hints for production engineering.
# - Diagnose and prevent the 'Mutable Default Argument' anti-pattern.
#
# ==============================================================================
"""

import sys
import copy
from typing import List, Dict, Tuple, Set, Optional, Any, Union

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 4. THE MENTAL MODEL: STICKY NOTES, NOT BOXES
# ==============================================================================

def demonstrate_references():
    """
    In C, a variable is a box holding a value.
    In Python, a variable is a sticky note holding a memory address.
    """
    section_header("The Sticky Note Mental Model")
    
    # 1. We create a list object in memory: [1, 2, 3]
    # 2. We put a sticky note named 'a' on it.
    a = [1, 2, 3]
    
    # 1. We take a NEW sticky note named 'b'.
    # 2. We put it on the EXACT SAME object that 'a' is on.
    # WE DO NOT COPY THE LIST.
    b = a
    
    print(f"Initial state -> a: {a}, b: {b}")
    print(f"Address of a: {id(a)}")
    print(f"Address of b: {id(b)}")
    
    assert id(a) == id(b), "a and b point to the identical memory address."
    
    # Because they point to the same object, mutating the object through 'b'
    # changes what 'a' sees.
    b.append(4)
    print(f"After b.append(4) -> a: {a}, b: {b}")
    
    # Reassigning 'a' moves the sticky note to a NEW object.
    # It does NOT affect 'b'.
    a = [9, 9]
    print(f"After a = [9, 9] -> a: {a}, b: {b}")
    assert id(a) != id(b), "a now points to a new object. b remains on the old one."


# ==============================================================================
# 5. IDENTITY VS EQUALITY (is vs ==)
# ==============================================================================

def demonstrate_identity_vs_equality():
    """
    '==' checks if values are equal.
    'is' checks if memory addresses are equal.
    """
    section_header("Identity (is) vs Equality (==)")
    
    list1 = [10, 20]
    list2 = [10, 20]
    
    print(f"list1: {list1} (ID: {id(list1)})")
    print(f"list2: {list2} (ID: {id(list2)})")
    
    print(f"list1 == list2 : {list1 == list2}  (Values are identical)")
    print(f"list1 is list2 : {list1 is list2} (They are distinct objects in memory)")
    
    # --- CPython Implementation Detail: Small Integer Interning ---
    # To save memory, CPython pre-creates integers from -5 to 256.
    # Any variable assigned these numbers will point to the SAME cached object.
    
    x = 100
    y = 100
    print(f"\nx = {x} (ID: {id(x)}), y = {y} (ID: {id(y)})")
    print(f"x is y : {x is y} (True because 100 is cached!)")
    
    x_large = 1000
    y_large = 1000
    # Note: In a script, the compiler might optimize this to True, 
    # but in a REPL, it evaluates to False!
    print(f"x_large = {x_large}, y_large = {y_large}")
    print(f"x_large is y_large : {x_large is y_large}")


# ==============================================================================
# 6. MUTABILITY VS IMMUTABILITY
# ==============================================================================

def demonstrate_immutability():
    """
    Immutable objects cannot be changed in place. 
    Operations on them create NEW objects.
    """
    section_header("Immutability")
    
    # Strings are immutable
    s = "hello"
    old_id = id(s)
    
    # s[0] = "H" # TypeError!
    
    s = s.capitalize() # Returns a NEW string object
    new_id = id(s)
    
    print(f"old string ID: {old_id}")
    print(f"new string ID: {new_id}")
    assert old_id != new_id, "The string object was not changed, a new one was created."
    
    # Tuples are immutable arrays
    t = (1, 2, [3, 4])
    # t[0] = 99 # TypeError!
    
    # TRICK QUESTION / EDGE CASE:
    # What happens if a tuple contains a mutable object (like a list)?
    print(f"\nTuple containing a list: {t}")
    t[2].append(5) 
    print(f"Tuple after modifying internal list: {t}")
    # Why did this work? The tuple holds a REFERENCE to the list. 
    # The reference did not change, so the tuple's immutability wasn't violated. 
    # But the underlying list mutated!


# ==============================================================================
# 7. PASS-BY-OBJECT-REFERENCE
# ==============================================================================

def mutate_list(lst: List[int]) -> None:
    # Mutates the object referenced by lst
    lst.append(99)

def reassign_list(lst: List[int]) -> None:
    # Moves the local label 'lst' to a new object. Does not affect caller.
    lst = [4, 5, 6]

def demonstrate_parameter_passing():
    """
    Python is NOT pass-by-value. Python is NOT pass-by-reference (like C++ &).
    Python is Pass-By-Object-Reference.
    """
    section_header("Pass-By-Object-Reference")
    
    my_list = [1, 2]
    print(f"Before function: {my_list}")
    
    mutate_list(my_list)
    print(f"After mutate_list: {my_list}  <- Changed!")
    
    reassign_list(my_list)
    print(f"After reassign_list: {my_list} <- UNCHANGED!")


# ==============================================================================
# 8. THE MUTABLE DEFAULT ARGUMENT ANTI-PATTERN
# ==============================================================================

# DANGEROUS CODE
def append_to_cache(item: str, cache: List[str] = []) -> List[str]:
    """
    Default arguments are evaluated exactly ONCE: when the function is defined 
    (during the parsing/compilation phase). 
    The 'cache' name points to a single list object persisting across calls.
    """
    cache.append(item)
    return cache

# PROFESSIONAL CODE
def append_to_cache_safe(item: str, cache: Optional[List[str]] = None) -> List[str]:
    """
    By using None, we evaluate and create a new list dynamically INSIDE the 
    function execution scope every time it is called.
    """
    if cache is None:
        cache = []
    cache.append(item)
    return cache

def demonstrate_mutable_defaults():
    section_header("The Mutable Default Argument Trap")
    
    print("Using DANGEROUS function:")
    print(f"Call 1: {append_to_cache('User_A')}")
    print(f"Call 2: {append_to_cache('User_B')}") # Wait, User_A is here too!
    
    print("\nUsing SAFE function:")
    print(f"Call 1: {append_to_cache_safe('User_A')}")
    print(f"Call 2: {append_to_cache_safe('User_B')}")


# ==============================================================================
# 9. ADVANCED DATA TYPES: MEMORY OVERHEAD
# ==============================================================================

def demonstrate_memory_overhead():
    section_header("Memory Overhead in Python")
    
    # In C, an integer is 4 bytes. In Python...
    num = 42
    print(f"Size of an integer: {sys.getsizeof(num)} bytes") 
    # Usually 28 bytes! Why?
    # Python ints are C-structs containing:
    # 1. Reference count (8 bytes)
    # 2. Type pointer (8 bytes)
    # 3. Size of digit array (8 bytes)
    # 4. The actual digits (4 bytes)
    
    empty_list = []
    print(f"Size of empty list: {sys.getsizeof(empty_list)} bytes")
    # Usually 56 bytes.
    # Plus 8 bytes for every pointer added.


# ==============================================================================
# 10. TYPE HINTING FOR PRODUCTION
# ==============================================================================

# Type hinting does not affect runtime speed. It is used by static analyzers 
# (mypy) to catch bugs before execution.

def fetch_user_data(user_id: int) -> Dict[str, Union[str, int]]:
    return {"id": user_id, "name": "Alice", "role": "Admin"}

def process_data(data: Any) -> None:
    # 'Any' explicitly tells type checkers to ignore this variable
    pass

# ==============================================================================
# 11. INTERVIEW PREPARATION & ACTIVE RECALL
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the difference between pass-by-reference (C++) and pass-by-object-reference (Python).
   Answer: In C++, pass-by-reference passes the actual memory container, so reassigning it changes the caller's variable. In Python, you pass the memory ADDRESS of the object. Mutating the object affects the caller. Reassigning the variable merely points the local function label to a new object, leaving the caller untouched.

2. Why is [] as a default argument dangerous?
   Answer: Default arguments are evaluated once at function definition time. The empty list becomes a permanent object in memory attached to the function. Every time the function is called without that argument, it uses the exact same list object. 

3. What happens when you do `a = [1, 2]; b = a; a = [3, 4]`?
   Answer: 'b' will be [1, 2] and 'a' will be [3, 4]. Assignment NEVER copies data. The `a = [3, 4]` creates a brand new list and moves the 'a' sticky note to it. 'b' was never moved.
"""

if __name__ == "__main__":
    demonstrate_references()
    demonstrate_identity_vs_equality()
    demonstrate_immutability()
    demonstrate_parameter_passing()
    demonstrate_mutable_defaults()
    demonstrate_memory_overhead()
    print("\n[SUCCESS] Laboratory 01 Completed. Concepts Verified.")
