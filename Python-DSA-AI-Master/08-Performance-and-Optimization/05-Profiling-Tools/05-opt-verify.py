"""
Profiling Tools: Optimization Verification

Learning Objectives:
1. Understand the scientific method of optimization.
2. Establish a baseline metric before making changes.
3. Verify that optimized code produces the EXACT same output as original code.
4. Measure the speedup and document the tradeoff.

Concept Explanation:
"Premature optimization is the root of all evil." (Donald Knuth).
When you do optimize, you must follow a strict process:
1. Ensure you have tests that prove correctness.
2. Profile to establish a baseline time/memory.
3. Implement the optimization.
4. VERIFY correctness (the new fast code must yield the identical answer).
5. Compare new metrics to baseline to ensure it was worth the complexity.
"""

import timeit
import hashlib
from typing import List, Tuple

# --- Step 1: The Original (Slow) Implementation ---
def find_duplicates_slow(data: List[int]) -> List[int]:
    """Find duplicates using O(N^2) list iteration."""
    duplicates = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    # Sort for deterministic output
    return sorted(duplicates)

# --- Step 2: The Optimized (Fast) Implementation ---
def find_duplicates_fast(data: List[int]) -> List[int]:
    """Find duplicates using O(N) sets."""
    seen = set()
    duplicates = set()
    for x in data:
        if x in seen:
            duplicates.add(x)
        else:
            seen.add(x)
    # Sort for deterministic output
    return sorted(list(duplicates))

# --- Step 3: Verification Framework ---
def verify_optimization(data: List[int]) -> None:
    """Verify both correctness and performance."""
    print(f"Data Size: {len(data)} items")
    
    # 1. Correctness Verification
    res_slow = find_duplicates_slow(data)
    res_fast = find_duplicates_fast(data)
    
    if res_slow != res_fast:
        print("❌ FAILED: Optimized code produces different results!")
        return
    print("✅ CORRECTNESS: Output matches exactly.")
    
    # 2. Performance Verification
    # Using timeit for micro-benchmarking
    setup = "from __main__ import find_duplicates_slow, find_duplicates_fast, data"
    
    # Adjust number of runs based on size to avoid waiting forever
    runs = 10 if len(data) > 1000 else 100
    
    t_slow = timeit.timeit("find_duplicates_slow(data)", setup=setup, number=runs)
    t_fast = timeit.timeit("find_duplicates_fast(data)", setup=setup, number=runs)
    
    print(f"⏱️  BASELINE (Slow):   {t_slow:.4f}s for {runs} runs")
    print(f"⏱️  OPTIMIZED (Fast):  {t_fast:.4f}s for {runs} runs")
    
    speedup = t_slow / t_fast
    print(f"🚀 SPEEDUP:           {speedup:.1f}x faster")
    
    if speedup < 1.1:
        print("⚠️ WARNING: Optimization did not significantly improve performance.")
        print("   Consider reverting if the new code is harder to read.")

# --- Edge Cases ---
def floating_point_verification_edge_case():
    """
    When optimizing math, floating point arithmetic can differ slightly 
    depending on the order of operations (e.g., SIMD vectorization vs scalar).
    You cannot use `==` for floats. You must use `math.isclose()`.
    """
    import math
    a = 0.1 + 0.2
    b = 0.3
    assert a != b # Exact equality fails!
    assert math.isclose(a, b) # Must verify this way

# --- Interview Challenge ---
"""
Challenge: How do you verify that a massive object (like a 1GB DataFrame) 
is identical between two implementations without holding both in memory?

Answer: Calculate a cryptographic hash (like MD5 or SHA256) of the byte 
stream as it's processed, and compare the hashes.
"""
def verify_via_hash(str1: str, str2: str) -> bool:
    h1 = hashlib.md5(str1.encode()).hexdigest()
    h2 = hashlib.md5(str2.encode()).hexdigest()
    return h1 == h2

# --- Execution ---
if __name__ == '__main__':
    print("--- Performance Analysis: Optimization Verification ---\n")
    import random
    
    # Generate data with some duplicates
    test_data = [random.randint(1, 1000) for _ in range(2000)]
    
    verify_optimization(test_data)
    floating_point_verification_edge_case()
    assert verify_via_hash("hello world", "hello world")
