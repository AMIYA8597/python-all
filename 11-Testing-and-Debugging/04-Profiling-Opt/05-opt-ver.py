"""
Optimization and Verification in Python

Learning Objectives:
1. Identify common performance anti-patterns in Python.
2. Apply optimizations (e.g., algorithmic improvements, choosing right data structures).
3. Verify that optimizations do not break functionality.
4. Write testable, optimized code.

Concept Explanation:
Optimization is the process of modifying code to work more efficiently or use fewer resources.
However, "Premature optimization is the root of all evil" (Donald Knuth). Only optimize
after identifying bottlenecks via profiling. Crucially, any optimization must be verified
to ensure the logic remains correct.

Imports:
- timeit: For verifying performance gains.
- unittest: For verifying correctness.
"""

import timeit
import unittest
from typing import List, Set, Any

# ==========================================
# Basic Implementation: Unoptimized Code
# ==========================================

def find_duplicates_unoptimized(items: List[int]) -> List[int]:
    """Finds duplicates using an O(n^2) approach."""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

# ==========================================
# Intermediate Implementation: Optimized Code
# ==========================================

def find_duplicates_optimized(items: List[int]) -> List[int]:
    """Finds duplicates using an O(n) approach with sets."""
    seen: Set[int] = set()
    duplicates: Set[int] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

# ==========================================
# Advanced Implementation: Verification & Benchmarking
# ==========================================

class TestOptimizationVerification(unittest.TestCase):
    """Verifies that the optimized function produces the same results."""
    
    def test_find_duplicates(self) -> None:
        test_cases = [
            ([1, 2, 3, 2, 1, 5, 6, 5], [1, 2, 5]),
            ([1, 2, 3, 4], []),
            ([], []),
            ([1, 1, 1, 1], [1])
        ]
        
        for data, expected in test_cases:
            with self.subTest(data=data):
                # Sort results because sets do not guarantee order
                unopt_res = sorted(find_duplicates_unoptimized(data))
                opt_res = sorted(find_duplicates_optimized(data))
                expected_sorted = sorted(expected)
                
                self.assertEqual(unopt_res, expected_sorted)
                self.assertEqual(opt_res, expected_sorted)

def verify_performance() -> None:
    """Benchmarks unoptimized vs optimized to prove the gain."""
    setup_code = """
from __main__ import find_duplicates_unoptimized, find_duplicates_optimized
import random
data = [random.randint(1, 100) for _ in range(500)]
    """
    
    time_unopt = timeit.timeit("find_duplicates_unoptimized(data)", setup=setup_code, number=100)
    time_opt = timeit.timeit("find_duplicates_optimized(data)", setup=setup_code, number=100)
    
    print(f"Unoptimized time: {time_unopt:.4f}s")
    print(f"Optimized time:   {time_opt:.4f}s")
    if time_opt > 0:
        print(f"Speedup: {time_unopt / time_opt:.2f}x")

# ==========================================
# Edge Cases & Interview Challenge
# ==========================================

"""
Edge Cases:
1. Large Datasets: The unoptimized O(n^2) function will hang or take unacceptably
   long on very large lists, highlighting the need for algorithmic optimization.
2. Memory Overhead: The optimized version uses extra memory (O(n) space for the `seen`
   and `duplicates` sets) to achieve O(n) time. This is a classic time-memory trade-off.

Interview Challenge:
Question: How would you optimize the `find_duplicates` function if memory was extremely
constrained and you couldn't use extra sets/dictionaries, but the input list could be modified?
Hint: Sort the list first (O(n log n) time, O(1) space), then iterate through comparing
adjacent elements.
"""

if __name__ == "__main__":
    print("--- Optimization and Verification ---")
    print("1. Running Correctness Verification:")
    
    # Run unittest suite programmatically
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOptimizationVerification)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n2. Running Performance Verification:")
    verify_performance()
