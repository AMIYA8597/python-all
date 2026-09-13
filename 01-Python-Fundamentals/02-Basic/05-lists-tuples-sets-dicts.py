"""
# ==============================================================================
# LABORATORY 05: DATA STRUCTURES (LISTS, TUPLES, SETS, DICTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Choosing the wrong data structure is the #1 cause of performance issues in Python.
# Using a list for membership testing `if item in lst` is O(N). Doing this in a loop
# causes O(N^2) time complexity. Using a set makes it O(1).
# 
# Furthermore, understanding the C-level implementations (Dynamic Arrays vs 
# Hash Tables) is a fundamental prerequisite for the DSA track and technical interviews.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Lists as C-level dynamic arrays (over-allocation).
# - Master deep slicing mechanics `lst[start:stop:step]`.
# - Understand the Immutability of Tuples and why they are hashable.
# - Understand Sets and Dicts as Hash Tables (and hash collisions).
# - Master List/Dict/Set Comprehensions.
# - Understand Big-O complexities for common operations.
#
# ==============================================================================
"""

import sys
import timeit
from typing import List, Tuple, Set, Dict, Any

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. LISTS: DYNAMIC ARRAYS
# ==============================================================================
def demonstrate_lists():
    """
    Python lists are NOT linked lists. They are contiguous arrays of pointers 
    in C. When they run out of space, they allocate a larger array and copy 
    the pointers over (Over-allocation strategy).
    """
    section_header("Lists: Dynamic Arrays")
    
    lst = []
    print("Watch the memory allocation grow as we append:")
    prev_size = sys.getsizeof(lst)
    print(f"Length: 0, Size: {prev_size} bytes")
    
    for i in range(1, 10):
        lst.append(i)
        curr_size = sys.getsizeof(lst)
        if curr_size != prev_size:
            print(f"Length: {i}, Size: {curr_size} bytes (Reallocation triggered!)")
            prev_size = curr_size
            
    # SLICING MECHANICS
    # syntax: lst[start:stop:step]
    nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("\nSlicing:")
    print(f"Original: {nums}")
    print(f"nums[2:7]    -> {nums[2:7]} (start 2, up to but not including 7)")
    print(f"nums[::2]    -> {nums[::2]} (every second element)")
    print(f"nums[::-1]   -> {nums[::-1]} (idiomatic way to reverse a list)")
    
    # TRAP: Slicing creates a SHALLOW COPY.
    print(f"Does nums[::-1] point to the same object? {nums[::-1] is nums}")


# ==============================================================================
# 4. TUPLES: IMMUTABLE RECORDS
# ==============================================================================
def demonstrate_tuples():
    """
    Tuples are fixed-size, immutable arrays. Because they are immutable, 
    Python can optimize them heavily and they can be used as Dictionary keys 
    (they are Hashable).
    """
    section_header("Tuples: Immutable Records")
    
    tup = (1, 2, 3)
    print(f"Tuple size: {sys.getsizeof(tup)} bytes")
    lst = [1, 2, 3]
    print(f"List size:  {sys.getsizeof(lst)} bytes (Lists are heavier)")
    
    # TRICK: Tuples containing mutable objects
    # The tuple holds the REFERENCE. It cannot point to a new list, 
    # but the list ITSELF can mutate!
    weird_tup = (1, [2, 3])
    print(f"\nBefore mutation: {weird_tup}")
    weird_tup[1].append(4)
    print(f"After mutation:  {weird_tup}")
    # Note: Because weird_tup contains an unhashable type (list), 
    # it can NO LONGER be used as a dictionary key, despite being a tuple!


# ==============================================================================
# 5. SETS & DICTS: HASH TABLES
# ==============================================================================
def demonstrate_hash_tables():
    """
    Sets and Dictionaries are implemented as Hash Tables in CPython.
    Key lookups are O(1) on average.
    """
    section_header("Dictionaries & Sets (Hash Tables)")
    
    # In Python 3.7+, Dictionaries maintain insertion order!
    d = {"apple": 1, "banana": 2, "cherry": 3}
    print("Dictionary iteration maintains insertion order:")
    for k, v in d.items():
        print(f"  {k}: {v}")
        
    # Sets only store unique keys (no values).
    s = {1, 2, 2, 3, 3, 3, 4}
    print(f"\nSet deduplication: {{1, 2, 2, 3, 3, 3, 4}} -> {s}")
    
    # PERFORMANCE COMPARISON: List vs Set Membership (in operator)
    print("\n--- Performance: List vs Set (10,000 items) ---")
    large_list = list(range(10000))
    large_set = set(range(10000))
    
    # We are searching for 9999, which is at the very end.
    list_time = timeit.timeit("9999 in large_list", globals=locals(), number=10000)
    set_time = timeit.timeit("9999 in large_set", globals=locals(), number=10000)
    
    print(f"List lookup time: {list_time:.4f} seconds (O(N))")
    print(f"Set lookup time:  {set_time:.4f} seconds (O(1))")
    print(f"Set is {list_time/set_time:.1f}x faster!")


# ==============================================================================
# 6. COMPREHENSIONS (PYTHONIC DATA GENERATION)
# ==============================================================================
def demonstrate_comprehensions():
    """
    Comprehensions are executed in C and are faster (and cleaner) than using
    append() inside a for loop.
    Syntax: [expression for item in iterable if condition]
    """
    section_header("Comprehensions")
    
    # List comprehension
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"List comprehension (evens): {evens}")
    
    # Dictionary comprehension
    squares_dict = {x: x**2 for x in range(5)}
    print(f"Dict comprehension (squares): {squares_dict}")
    
    # Set comprehension
    # Note the curly braces!
    unique_chars = {char for char in "abracadabra"}
    print(f"Set comprehension (unique chars): {unique_chars}")
    
    # TRAP: Tuple Comprehension does NOT exist!
    # (x for x in range(5)) creates a GENERATOR EXPRESSION, not a tuple.
    gen = (x for x in range(5))
    print(f"\n(x for x in range(5)) creates: {type(gen)}")
    # To actually make a tuple, wrap the generator in tuple():
    print(f"tuple(x for x in range(5)) creates: {tuple(gen)}")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Big-O time complexity of `item in list` vs `item in set`?
   Answer: O(N) for list. O(1) for set (average case).

2. Are Python dictionaries ordered?
   Answer: Since Python 3.7, dictionaries maintain insertion order natively. Before that, they did not.

3. Why do lists occasionally jump in memory size when appending?
   Answer: Lists are dynamic arrays. When the underlying C-array fills up, Python over-allocates a larger array and copies the pointers over to prevent O(N) allocation on EVERY append.

4. Can you use a tuple as a dictionary key?
   Answer: Yes, BUT only if everything inside the tuple is immutable (hashable). If the tuple contains a list, it cannot be hashed and will raise a TypeError.

5. What does `my_list[::-1]` do?
   Answer: It returns a SHALLOW COPY of the list in reverse order.
"""

if __name__ == "__main__":
    demonstrate_lists()
    demonstrate_tuples()
    demonstrate_hash_tables()
    demonstrate_comprehensions()
    print("\n[SUCCESS] Laboratory 05 Completed.")
