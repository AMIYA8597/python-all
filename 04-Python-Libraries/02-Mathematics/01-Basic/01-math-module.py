"""
# ==============================================================================
# LABORATORY: THE MATH MODULE (PERFORMANCE & PRECISION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python provides basic arithmetic operators (`+`, `-`, `*`, `/`, `**`). 
# However, when writing algorithms, you often need trigonometry, logarithms, 
# advanced combinatorics, and strict floating-point control.
#
# The built-in `math` module is a thin Python wrapper around the highly 
# optimized C Standard Library math functions. 
#
# Because it relies on the C layer, `math` operations are significantly faster 
# and mathematically safer than trying to compute them natively in Python. 
# For example, `math.isclose()` solves the infamous floating-point precision 
# bug where `0.1 + 0.2 != 0.3`.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand IEEE 754 Floating-Point precision limits.
# - Utilize `math.isclose()` to safely compare floats.
# - Execute Combinatorics (`comb`, `perm`) natively in C.
# - Compare `math.pow()` vs the Python `**` operator.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FLOATING-POINT CATASTROPHES (IEEE 754)
# ==============================================================================
def demonstrate_floating_point():
    section_header("Floating-Point Precision and `isclose`")
    
    # 1. THE PROBLEM
    a = 0.1
    b = 0.2
    c = 0.3
    
    print("The Infamous Floating-Point Error:")
    print(f"0.1 + 0.2 == 0.3 -> {a + b == c}")
    print(f"Actual memory value of 0.1 + 0.2: {a + b:.17f}")
    
    print("\nExplanation: Computers use Base-2 (Binary). The fraction 1/10 cannot ")
    print("be perfectly represented in Binary (it creates a repeating decimal). ")
    print("When the C hardware truncates the repeating decimal to 64 bits, ")
    print("microscopic precision is lost.")
    
    # 2. THE SOLUTION
    print("\nThe Fix: `math.isclose()`")
    # `isclose` mathematically checks if the absolute difference between the two 
    # numbers is within a microscopic tolerance (rel_tol = 1e-09).
    safe_comparison = math.isclose(a + b, c)
    print(f"math.isclose(0.1 + 0.2, 0.3) -> {safe_comparison}")


# ==============================================================================
# 4. ALGORITHMIC COMBINATORICS IN C
# ==============================================================================
def demonstrate_combinatorics():
    section_header("Combinatorics (Permutations & Combinations)")
    
    # If you try to calculate "100 Choose 5" natively in Python using factorials, 
    # it is slow and generates massive numbers in memory. 
    # Python 3.8+ introduced `math.comb` which executes instantly in C!
    
    n = 52 # A deck of cards
    k = 5  # A poker hand
    
    print(f"Total possible 5-card Poker hands (Order doesn't matter):")
    combinations = math.comb(n, k)
    print(f"math.comb(52, 5) = {combinations:,}")
    
    print(f"\nTotal possible 5-card draws (Order DOES matter):")
    permutations = math.perm(n, k)
    print(f"math.perm(52, 5) = {permutations:,}")


# ==============================================================================
# 5. EXPONENTS AND LOGARITHMS
# ==============================================================================
def demonstrate_powers():
    section_header("Exponents and Logarithms")
    
    print("1. Exponentiation:")
    # Python `**` operator vs `math.pow`
    # `**` works on Integers, preserving infinite integer precision!
    # `math.pow` casts everything to a Float (C `double`) before computing!
    print(f"Python 10**3   : {10**3} (Type: {type(10**3)})")
    print(f"math.pow(10, 3): {math.pow(10, 3)} (Type: {type(math.pow(10, 3))})")
    
    print("\n2. Logarithms:")
    # Finding the depth of a Binary Tree with 1,000,000 nodes!
    # Log base 2 of 1,000,000.
    nodes = 1_000_000
    tree_depth = math.log2(nodes)
    print(f"Depth of 1M node Binary Tree: {tree_depth:.2f} levels")
    
    # Base-10 logarithm (e.g. counting the number of digits in a massive integer!)
    massive_number = 999_999_999_999
    digits = math.floor(math.log10(massive_number)) + 1
    print(f"Number of digits in {massive_number}: {digits}")


# ==============================================================================
# 6. MATHEMATICAL CONSTANTS & SPECIAL FUNCTIONS
# ==============================================================================
def demonstrate_constants():
    section_header("Constants & Euclidean Geometry")
    
    print(f"Pi (π) : {math.pi}")
    print(f"Tau (τ): {math.tau} (Exactly 2*Pi, used in advanced math)")
    print(f"Euler's Number (e): {math.e}")
    print(f"Infinity: {math.inf} (Used as initial baseline in Min/Max algorithms)")
    
    print("\nEuclidean Distance (Pythagorean Theorem without overflow):")
    # Calculating hypotenuse. `math.hypot` is safer than `math.sqrt(x**2 + y**2)` 
    # because it prevents mathematical overflow when squaring massive numbers!
    x = 3.0
    y = 4.0
    hypotenuse = math.hypot(x, y)
    print(f"math.hypot({x}, {y}) = {hypotenuse}")


def run_all_labs():
    demonstrate_floating_point()
    demonstrate_combinatorics()
    demonstrate_powers()
    demonstrate_constants()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `0.1 + 0.2 == 0.3` evaluate to False, and how do we fix it?
   Answer: It evaluates to False because of IEEE 754 floating-point limitations. Computers store numbers in Binary (Base-2). The decimal fraction 1/10 produces an infinitely repeating binary sequence (just like 1/3 produces 0.333333... in decimal). The CPU truncates this infinite sequence to fit into 64 bits, meaning 0.1 is actually stored as 0.10000000000000000555. When you add them, the tiny errors compound. The fix is to use `math.isclose(a+b, c)` which mathematically checks if the absolute difference between them is smaller than a microscopic tolerance threshold.

2. When should you use `math.pow(x, y)` instead of `x ** y`?
   Answer: You should use `x ** y` almost all the time if working with Integers. Python integers have infinite precision. If you do `2 ** 100`, Python allocates extra bytes to store the massive exact integer. `math.pow` instantly converts the inputs to C-level `double` floats. Floats lose exact precision after 15 digits. `math.pow(2, 100)` will return a float, which might be an approximation if the number exceeds the 64-bit mantissa! `math.pow` is only useful when you specifically want C-level floating-point arithmetic speed for non-integers.

3. Why is `math.inf` useful in algorithmic programming?
   Answer: In Graph Algorithms (like Dijkstra's) or Dynamic Programming, you often need to initialize an array of "Shortest Distances" or a `global_minimum` tracking variable. If you initialize it to `9999999`, a massive graph might actually contain a path longer than that, breaking your algorithm! Initializing variables to `float('inf')` or `math.inf` provides a mathematically perfect ceiling. ANY finite number will evaluate as `< math.inf`, guaranteeing the tracking variable updates correctly on the first comparison!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: The Math Module Completed.")
