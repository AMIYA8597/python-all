"""
Module: Permutations and Combinations

Learning Objectives:
1. Understand the mathematical definitions of permutations and combinations.
2. Learn how to compute them efficiently using factorials and DP.
3. Understand how to generate all permutations and combinations of a sequence.

Concept Explanation:
- Permutations (nPr): The number of ways to arrange r objects from n distinct objects. Order matters.
  Formula: nPr = n! / (n-r)!
- Combinations (nCr): The number of ways to choose r objects from n distinct objects. Order does not matter.
  Formula: nCr = n! / (r! * (n-r)!)

Performance Analysis:
- Math-based approach: O(n) for factorials.
- DP-based approach: O(n*r) time and space.
- Generation: O(n * n!) for permutations, O(r * nCr) for combinations.

Edge Cases:
- r > n: Should return 0.
- r < 0 or n < 0: Invalid input, usually raise exception or return 0.
- r = 0 or r = n: nCr = 1.
"""

import math
from typing import List, Generator

# --- Basic Implementation ---
def permutations_math(n: int, r: int) -> int:
    """Computes nPr using math module."""
    if r > n or n < 0 or r < 0: return 0
    return math.perm(n, r)

def combinations_math(n: int, r: int) -> int:
    """Computes nCr using math module."""
    if r > n or n < 0 or r < 0: return 0
    return math.comb(n, r)

# --- Intermediate Implementation ---
def ncr_dp(n: int, r: int) -> int:
    """Computes nCr using Dynamic Programming (Pascal's Triangle)."""
    if r > n or n < 0 or r < 0: return 0
    dp = [0] * (r + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, r), 0, -1):
            dp[j] = dp[j] + dp[j - 1]
    return dp[r]

# --- Advanced Implementation ---
def generate_permutations(elements: List[int]) -> Generator[List[int], None, None]:
    """Generates all permutations using backtracking."""
    n = len(elements)
    def backtrack(start: int):
        if start == n:
            yield elements[:]
        for i in range(start, n):
            elements[start], elements[i] = elements[i], elements[start]
            yield from backtrack(start + 1)
            elements[start], elements[i] = elements[i], elements[start]
    
    yield from backtrack(0)

# --- Interview Challenge ---
# Problem: Next Permutation
# Find the next lexicographically greater permutation of numbers.
def next_permutation(nums: List[int]) -> None:
    """Modifies nums in-place to the next permutation."""
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while j >= 0 and nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    # Reverse the suffix
    nums[i + 1:] = reversed(nums[i + 1:])

# --- Tests ---
def run_tests():
    assert permutations_math(5, 3) == 60
    assert combinations_math(5, 3) == 10
    assert ncr_dp(5, 3) == 10
    
    perms = list(generate_permutations([1, 2, 3]))
    assert len(perms) == 6
    assert [1, 2, 3] in perms
    
    nums = [1, 2, 3]
    next_permutation(nums)
    assert nums == [1, 3, 2]
    print("All tests passed for 01-perm-comb.py!")

if __name__ == "__main__":
    run_tests()
