"""
# ==============================================================================
# LABORATORY 03: CONTROL STRUCTURES AND ITERATION PROTOCOLS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Control structures dictate the flow of the program. Beyond basic if/else loops,
# understanding Python's truthiness rules, the underlying C-level iterator 
# protocol (__iter__ / __next__), and structural pattern matching are essential 
# for writing idiomatic, performant code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Truthiness and the __bool__ dunder method.
# - Understand how a `for` loop actually works under the hood.
# - Avoid common traps with loops (like modifying a list while iterating).
# - Master the infamous `else` clause in loops.
# - Utilize Python 3.10+ Structural Pattern Matching.
#
# ==============================================================================
"""

import sys
from typing import List, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. TRUTHINESS (THE __BOOL__ PROTOCOL)
# ==============================================================================
def demonstrate_truthiness():
    """
    Python evaluates objects in boolean contexts (if/while) based on their 
    __bool__ or __len__ methods.
    """
    section_header("Truthiness")
    
    # Falsy values:
    falsy_values = [0, 0.0, "", [], {}, set(), tuple(), None, False]
    print("Falsy values evaluate to False:")
    for val in falsy_values:
        if not val:
            print(f"  {repr(val)} is Falsy")
            
    # Professional Pattern: Checking for empty collections
    # BAD: if len(my_list) == 0:
    # GOOD: if not my_list:
    my_list: List[int] = []
    if not my_list:
        print("\nIdiomatic check: 'if not my_list' caught the empty list!")


# ==============================================================================
# 4. ADVANCED LOOPING: THE ITERATOR PROTOCOL
# ==============================================================================
def demonstrate_iterators():
    """
    A `for` loop in Python is syntactic sugar for a `while` loop that catches
    a StopIteration exception.
    """
    section_header("The Iterator Protocol Under the Hood")
    
    numbers = [1, 2, 3]
    
    print("Traditional 'for' loop:")
    for num in numbers:
        print(num, end=" ")
    print("\n")
    
    print("What the 'for' loop actually does (desugared):")
    # 1. Get the iterator object by calling __iter__()
    iterator = iter(numbers) 
    
    # 2. Loop infinitely calling __next__()
    while True:
        try:
            item = next(iterator)
            print(item, end=" ")
        except StopIteration:
            # 3. Break when the iterator is exhausted
            break
    print("\n")


# ==============================================================================
# 5. THE INFAMOUS `ELSE` IN LOOPS
# ==============================================================================
def demonstrate_loop_else():
    """
    In Python, `for...else` and `while...else` exist.
    The `else` block executes ONLY IF the loop completes NATURALLY 
    (i.e., it was NOT terminated by a `break` statement).
    """
    section_header("The `else` Clause in Loops")
    
    target = 5
    numbers = [1, 2, 3]
    
    # Use Case: Searching for an item
    for num in numbers:
        if num == target:
            print("Target found! Breaking loop.")
            break
    else:
        # Executes because the break was never hit.
        print("Target NOT found! (Executed the else block)")
        
    target = 2
    for num in numbers:
        if num == target:
            print(f"Target {target} found! Breaking loop.")
            break
    else:
        print("Target NOT found! (This will NOT print)")


# ==============================================================================
# 6. STRUCTURAL PATTERN MATCHING (PYTHON 3.10+)
# ==============================================================================
def process_command(command: str):
    """
    A modern switch-case equivalent, but far more powerful because it 
    matches structures and unpacks them.
    """
    # Splitting command into a list of words
    parts = command.split()
    
    match parts:
        case ["quit" | "exit"]:
            print("Matched: Exiting program.")
        case ["load", filename]:
            print(f"Matched: Loading file '{filename}'")
        case ["save", filename, "--force"]:
            print(f"Matched: Force saving file '{filename}'")
        case ["drop", *items]:
            print(f"Matched: Dropping multiple items: {items}")
        case _:
            print(f"Matched: Unknown command: {command}")

def demonstrate_pattern_matching():
    section_header("Structural Pattern Matching (match/case)")
    
    process_command("load data.csv")
    process_command("save data.csv --force")
    process_command("drop sword shield potion")
    process_command("quit")
    process_command("fly")


# ==============================================================================
# 7. COMMON TRAPS: MODIFIYING A LIST WHILE ITERATING
# ==============================================================================
def demonstrate_iteration_trap():
    section_header("Trap: Modifying a Collection While Iterating")
    
    # TRAP: Removing items from a list while iterating over it causes skipped items!
    nums = [1, 2, 3, 4, 5]
    print(f"Original: {nums}")
    
    for n in nums:
        if n % 2 != 0: # Try to remove odd numbers
            nums.remove(n)
            
    print(f"Result (BUGGED): {nums}  <- Wait, why is '3' still there?")
    # Reason: The internal pointer moves forward, but removing an item shifts 
    # the rest of the items backward. The pointer skips the item that shifted into 
    # the current slot.
    
    # FIX: Iterate over a COPY of the list (nums[:])
    nums = [1, 2, 3, 4, 5]
    for n in nums[:]:
        if n % 2 != 0:
            nums.remove(n)
            
    print(f"Result (FIXED using slice copy): {nums}")
    
    # BETTER FIX: List comprehension (creates a new list)
    nums = [1, 2, 3, 4, 5]
    nums = [n for n in nums if n % 2 == 0]
    print(f"Result (BEST using comprehension): {nums}")


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the `else` block on a `for` loop do?
   Answer: It executes only if the loop completes normally without encountering a `break`.

2. How does a `for` loop actually work?
   Answer: It calls `iter()` on the iterable to get an iterator, then repeatedly calls `next()` until a `StopIteration` exception is raised.

3. Why shouldn't you do `if len(my_list) == 0:`?
   Answer: It is unidiomatic and slightly slower. Use `if not my_list:` which relies on the list's `__bool__` method.

4. What is the bug when modifying a list while iterating?
   Answer: The iterator's internal index increments, but the list elements shift down, causing the next item to be skipped. Fix it by iterating over a copy `for item in lst[:]`.
"""

if __name__ == "__main__":
    demonstrate_truthiness()
    demonstrate_iterators()
    demonstrate_loop_else()
    demonstrate_pattern_matching()
    demonstrate_iteration_trap()
    print("\n[SUCCESS] Laboratory 03 Completed.")