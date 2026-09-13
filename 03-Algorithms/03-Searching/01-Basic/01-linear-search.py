"""
# ==============================================================================
# LABORATORY: LINEAR SEARCH IN DEPTH
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Linear Search is the most intuitive algorithm in computer science. It simply 
# starts at the beginning of an array and checks every single element until it 
# finds the target (or reaches the end).
#
# While Binary Search is exponentially faster (O(log N)), Binary Search CANNOT 
# be used unless the data is perfectly sorted. If data is arriving in real-time, 
# or sorting the data would destroy its original meaning (like time-series data), 
# you are mathematically forced to use Linear Search (O(N)).
#
# Furthermore, in Python, understanding how Linear Search works under the hood 
# is crucial for writing "Pythonic" code. A manual `for` loop in Python is slow. 
# Using the `in` operator offloads the Linear Search to highly optimized C code, 
# making it orders of magnitude faster.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Best, Average, and Worst-Case complexities.
# - Understand Ordered vs Unordered Linear Search.
# - Master Pythonic linear searches (`in`, `list.index()`, and generators).
#
# ==============================================================================
"""

import timeit
from typing import List, Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STANDARD LINEAR SEARCH
# ==============================================================================
def manual_linear_search(arr: List[Any], target: Any) -> int:
    """
    Standard Linear Search.
    Time Complexity:
    - Best Case: O(1) (Target is the very first element)
    - Worst Case: O(N) (Target is the very last element, or doesn't exist)
    - Average Case: O(N/2) -> O(N) (Target is usually in the middle)
    
    Space Complexity: O(1)
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


# ==============================================================================
# 4. ORDERED LINEAR SEARCH (EARLY EXIT)
# ==============================================================================
def ordered_linear_search(arr: List[int], target: int) -> int:
    """
    What if the array is SORTED, but we don't want to write a full Binary Search?
    We can optimize Linear Search with an Early Exit.
    If the array is [10, 20, 30, 40] and we are looking for 25.
    Once we hit 30, we know 25 can NEVER appear later in the array! We can stop.
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
        elif arr[i] > target:
            # We have passed the point where the target could exist.
            print(f" [Early Exit] Passed {target} at index {i}. Stopping search.")
            break
    return -1


def demonstrate_ordered():
    section_header("Algorithm: Ordered Linear Search")
    
    arr = [10, 20, 30, 40, 50, 60]
    target = 25
    
    print(f"Array: {arr}")
    print(f"Searching for: {target}")
    
    idx = ordered_linear_search(arr, target)
    print(f"Result Index: {idx} (Expected: -1)")


# ==============================================================================
# 5. PYTHONIC LINEAR SEARCH (C-OPTIMIZATIONS)
# ==============================================================================
def demonstrate_pythonic_search():
    section_header("Python Concept: C-Optimized Searching")
    
    print("""
Never write a manual `for` loop for Linear Search in production Python.
Python is an interpreted language. A Python `for` loop has massive overhead.

Instead, use the `in` operator or `list.index()`. 
These immediately drop down into the Python Virtual Machine and execute the 
Linear Search loop in raw, highly optimized C code.
    """)
    
    arr = list(range(1, 10000))
    target = 9999
    
    # 1. Checking Existence (Returns True/False)
    exists = target in arr
    print(f"Existence (`{target} in arr`): {exists}")
    
    # 2. Finding Index (Raises ValueError if not found)
    try:
        idx = arr.index(target)
        print(f"Index (`arr.index({target})`): {idx}")
    except ValueError:
        print("Not found")
        
    # 3. Searching for Complex Objects using Generators
    # What if you have a list of Dictionaries and want to find a specific one?
    # `arr.index()` doesn't work well here. Use the `next()` generator!
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"}
    ]
    
    target_id = 2
    # `next` stops at the very first match. The generator `(...)` ensures it 
    # evaluates lazily, achieving perfect O(1) memory and early-exit!
    user = next((u for u in users if u["id"] == target_id), None)
    
    print(f"\nComplex Object Search Result: {user}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why would you ever use Linear Search if Binary Search is $O(\\log N)$?
   Answer: Binary search requires a sorted array. Sorting an array takes $O(N \\log N)$ time. If you only need to search the array ONCE, doing a single $O(N)$ Linear Search is mathematically faster than paying the $O(N \\log N)$ penalty to sort it first. You only sort if you plan to search the same array many times.

2. What is the Time Complexity of Python's `target in list`?
   Answer: It is exactly $O(N)$, because it is just a Linear Search implemented in C. (Note: If it were a `set` or `dict`, it would be $O(1)$ due to Hashing).

3. Why is `next((x for x in data if condition), None)` better than `[x for x in data if condition][0]`?
   Answer: The list comprehension `[...]` forces Python to evaluate the ENTIRE array (O(N) time and O(N) memory) before taking the first element. The generator `(...)` evaluates lazily. The moment `next()` finds a match, it stops the loop instantly (Early Exit), using $O(1)$ memory and potentially $O(1)$ time if the match is early.
"""

if __name__ == "__main__":
    demonstrate_ordered()
    demonstrate_pythonic_search()
    print("\n[SUCCESS] Laboratory: Linear Search Completed.")
