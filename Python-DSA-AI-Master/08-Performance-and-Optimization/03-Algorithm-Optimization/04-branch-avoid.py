"""
Algorithm Optimization: Branch Avoidance (Branch Prediction)

Learning Objectives:
1. Understand how CPU Branch Prediction works.
2. Recognize how unpredictable `if` statements can stall the CPU pipeline.
3. Learn techniques to replace branching logic with arithmetic or lookups.
4. Analyze the performance difference on sorted vs. unsorted data.

Concept Explanation:
Modern CPUs process instructions in a pipeline. When encountering a branch (e.g., an `if` 
statement), the CPU guesses which way the code will go (Branch Prediction) to keep 
the pipeline full. If it guesses wrong, it must flush the pipeline, incurring a 
significant performance penalty. Replacing branches with math or dictionary lookups 
can sometimes yield more consistent and faster execution, especially on unpredictable data.
"""

import time
import random
from typing import List

# --- Basic Implementation ---
def count_positives_branched(data: List[int]) -> int:
    """Standard branching logic."""
    count = 0
    for x in data:
        if x > 0:  # The branch
            count += 1
    return count

# --- Intermediate Implementation ---
def count_positives_branchless(data: List[int]) -> int:
    """Branchless logic using boolean conversion to integer."""
    count = 0
    for x in data:
        # True evaluates to 1, False to 0. No CPU branching required!
        count += (x > 0)
    return count

# --- Advanced Implementation / Performance Analysis ---
def performance_analysis():
    """Compare performance on sorted vs unsorted data.
    Note: Python's interpreter overhead often masks low-level CPU branch 
    misprediction penalties, but the principle is crucial for compiled extensions (C/Cython)."""
    
    size = 1_000_000
    # Unsorted data (unpredictable branching)
    unsorted_data = [random.choice([-1, 1]) for _ in range(size)]
    
    # Sorted data (highly predictable branching: all -1s, then all 1s)
    sorted_data = sorted(unsorted_data)
    
    print(f"Dataset Size: {size}")
    
    # Branched Unsorted
    start = time.perf_counter()
    count_positives_branched(unsorted_data)
    t_branch_unsort = time.perf_counter() - start
    
    # Branched Sorted
    start = time.perf_counter()
    count_positives_branched(sorted_data)
    t_branch_sort = time.perf_counter() - start
    
    # Branchless Unsorted
    start = time.perf_counter()
    count_positives_branchless(unsorted_data)
    t_bless_unsort = time.perf_counter() - start
    
    print("\nBranched Logic:")
    print(f"  Unsorted (Mispredictions high): {t_branch_unsort:.4f}s")
    print(f"  Sorted   (Mispredictions low):  {t_branch_sort:.4f}s")
    print(f"  Penalty for unsorted:           {(t_branch_unsort/t_branch_sort - 1)*100:.1f}%")
    
    print("\nBranchless Logic:")
    print(f"  Unsorted: {t_bless_unsort:.4f}s")
    
# --- Edge Cases ---
def branchless_dictionary_lookup(code: str) -> str:
    """Using a dictionary to avoid if/elif chains."""
    # Instead of: if code == 'A': return 'Alpha' elif ...
    lookup = {
        'A': 'Alpha',
        'B': 'Beta',
        'C': 'Gamma'
    }
    return lookup.get(code, 'Unknown')

# --- Interview Challenge ---
"""
Challenge: Write a branchless function that returns the maximum of two numbers 
(x and y) using basic arithmetic/bitwise operators (assuming integers).
"""
def branchless_max(x: int, y: int) -> int:
    # If x > y, (x > y) is 1. If x <= y, it is 0.
    # Note: Pure math way in C: x ^ ((x ^ y) & -(x < y))
    # Python integer booleans make it easy:
    return x * (x >= y) + y * (y > x)

# --- Tests ---
def run_tests():
    data = [-5, -1, 0, 1, 5]
    assert count_positives_branched(data) == 2
    assert count_positives_branchless(data) == 2
    assert branchless_max(10, 20) == 20
    assert branchless_max(50, -5) == 50
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Branch Avoidance ---")
    performance_analysis()
    run_tests()
