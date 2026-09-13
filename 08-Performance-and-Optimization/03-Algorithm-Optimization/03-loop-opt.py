"""
Algorithm Optimization: Loop Optimizations

Learning Objectives:
1. Identify performance bottlenecks in Python loops.
2. Understand the overhead of attribute lookups and method calls inside loops.
3. Learn loop unrolling and hoisting loop invariants.
4. Apply list comprehensions and generators for faster iteration.

Concept Explanation:
Loops in pure Python are relatively slow because every iteration involves dynamic 
type checking and bytecode interpretation. Optimizing loops involves minimizing 
the work done *inside* the loop. Techniques include moving constant calculations 
outside the loop (hoisting), localizing variable lookups, and preferring 
C-optimized built-ins (like list comprehensions) over explicit `for` loops.
"""

import timeit
import math
from typing import List

# --- Basic Implementation ---
def naive_loop(data: List[int]) -> List[int]:
    """A naive loop with redundant calculations inside."""
    result = []
    for x in data:
        # math.sqrt and math.pi are looked up every iteration!
        val = math.sqrt(x) * math.pi
        result.append(val)
    return result

# --- Intermediate Implementation ---
def hoisted_loop(data: List[int]) -> List[int]:
    """Optimized loop: invariants hoisted and locals cached."""
    result = []
    append = result.append # Local cache of method (faster lookup)
    sqrt = math.sqrt       # Local cache of function
    pi = math.pi           # Local cache of constant
    
    for x in data:
        append(sqrt(x) * pi)
    return result

# --- Advanced Implementation / Performance Analysis ---
def comprehension_loop(data: List[int]) -> List[int]:
    """List comprehension: implemented in C, avoids Python frame setup overhead."""
    sqrt = math.sqrt
    pi = math.pi
    return [sqrt(x) * pi for x in data]

def map_loop(data: List[int]) -> List[float]:
    """Map function: sometimes faster if no lambda is required."""
    # Harder to do exactly the same math without a lambda, so let's simplify 
    # to show map performance.
    return list(map(math.sqrt, data))

def compare_performance():
    setup = """
from __main__ import naive_loop, hoisted_loop, comprehension_loop
data = list(range(10000))
    """
    
    t_naive = timeit.timeit("naive_loop(data)", setup=setup, number=1000)
    t_hoist = timeit.timeit("hoisted_loop(data)", setup=setup, number=1000)
    t_comp = timeit.timeit("comprehension_loop(data)", setup=setup, number=1000)
    
    print(f"Naive Loop:         {t_naive:.4f}s")
    print(f"Hoisted/Local Loop: {t_hoist:.4f}s (Speedup: {t_naive/t_hoist:.2f}x)")
    print(f"List Comprehension: {t_comp:.4f}s (Speedup: {t_naive/t_comp:.2f}x)")

# --- Edge Cases ---
def generator_expression_edge_case():
    """List comprehensions create the whole list in memory. 
    If memory is constrained, use generator expressions instead."""
    data = range(1_000_000)
    # List (Fast, high memory)
    # l = [x*2 for x in data] 
    
    # Generator (Slower iteration, minimal memory)
    g = (x*2 for x in data)
    return g

# --- Interview Challenge ---
"""
Challenge: Optimize this nested loop that finds string matches.
"""
def slow_nested(list_a: List[str], list_b: List[str]) -> List[str]:
    matches = []
    for a in list_a:
        for b in list_b:
            if a == b:
                matches.append(a)
    return matches

def fast_set_intersection(list_a: List[str], list_b: List[str]) -> List[str]:
    # O(N*M) loop becomes O(N+M) set intersection!
    return list(set(list_a).intersection(list_b))

# --- Tests ---
def run_tests():
    d = [1, 4, 9]
    res_naive = naive_loop(d)
    res_comp = comprehension_loop(d)
    assert len(res_naive) == len(res_comp)
    for r1, r2 in zip(res_naive, res_comp):
        assert math.isclose(r1, r2)
    
    assert fast_set_intersection(['a', 'b'], ['b', 'c']) == ['b']
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Loop Optimization ---")
    compare_performance()
    run_tests()
