"""
Python Basics Interview Questions

This module contains practical, realistic interview questions focused on Python fundamentals.
Topics covered: Strings, basic control flow, type hints, scoping, and mutability.

Each question includes:
- A description of the problem and its real-world relevance.
- A beginner/naive solution.
- An advanced/optimal solution with detailed explanations.
- Edge cases and time/space complexity analysis.
- Pytest-compatible tests.
"""

import sys
from typing import List, Any, Callable

# =============================================================================
# Question 1: String Reversal (Testing slicing vs loops)
# =============================================================================
"""
Context: Often used as a warm-up. Tests if the candidate knows Pythonic idioms 
(like slicing) versus traditional C-style loops.

Task: Write a function to reverse a string.
"""

def reverse_string_naive(s: str) -> str:
    """
    Naive approach: Iterating backwards.
    Time Complexity: O(N) where N is the length of the string.
    Space Complexity: O(N) to build the new string.
    """
    reversed_s = ""
    for i in range(len(s) - 1, -1, -1):
        reversed_s += s[i] # Strings are immutable, so this creates a new string every time! Inefficient in older Pythons.
    return reversed_s

def reverse_string_optimal(s: str) -> str:
    """
    Optimal approach: Python's slice notation.
    Time Complexity: O(N). Implemented in C under the hood, highly optimized.
    Space Complexity: O(N) to return the new string.
    """
    return s[::-1]

def test_reverse_string():
    assert reverse_string_optimal("hello") == "olleh"
    assert reverse_string_optimal("") == ""
    assert reverse_string_optimal("a") == "a"
    assert reverse_string_optimal("racecar") == "racecar"
    print("test_reverse_string passed.")


# =============================================================================
# Question 2: Scope and Default Mutable Arguments (The Classic Python Gotcha)
# =============================================================================
"""
Context: This is arguably the most common Python-specific interview question. 
It tests deep understanding of how Python evaluates default arguments (at function definition time, not call time).

Task: Fix the bug in the provided function `append_to_list_buggy`.
"""

def append_to_list_buggy(val: Any, target_list: List[Any] = []) -> List[Any]: # type: ignore
    """
    BUGGY: The default list is created ONCE when the function is defined.
    Every subsequent call without a target_list shares the same underlying list object.
    """
    target_list.append(val)
    return target_list

def append_to_list_fixed(val: Any, target_list: List[Any] | None = None) -> List[Any]:
    """
    FIXED: Use None as the default value, and create a new list inside the function.
    """
    if target_list is None:
        target_list = []
    target_list.append(val)
    return target_list

def test_append_to_list():
    # Demonstrating the bug
    l1 = append_to_list_buggy(1)
    l2 = append_to_list_buggy(2)
    # l1 and l2 are the SAME list! l1 == [1, 2], not [1].
    
    # Testing the fix
    f1 = append_to_list_fixed(1)
    f2 = append_to_list_fixed(2)
    assert f1 == [1]
    assert f2 == [2]
    
    # Passing an explicit list still works
    f3 = append_to_list_fixed(3, [0])
    assert f3 == [0, 3]
    print("test_append_to_list passed.")


# =============================================================================
# Question 3: Late Binding in Closures
# =============================================================================
"""
Context: Another classic scoping question. Tests understanding of how lambda functions
capture variables from their surrounding scope (by reference/name, not by value at creation time).

Task: What does the buggy function return? Fix it to return [0, 2, 4, 6, 8].
"""

def create_multipliers_buggy() -> List[Callable[[int], int]]:
    """
    Buggy: The lambda captures the variable 'i', not its value.
    By the time the lambdas are called, the loop has finished and 'i' is 4.
    So all functions multiply by 4.
    """
    return [lambda x: i * x for i in range(5)]

def create_multipliers_fixed() -> List[Callable[[int], int]]:
    """
    Fixed: Force early binding by passing 'i' as a default argument to the lambda.
    Default arguments are evaluated at creation time.
    """
    return [lambda x, i=i: i * x for i in range(5)]

def test_create_multipliers():
    # Buggy behavior: all lambdas multiply by 4
    buggy_funcs = create_multipliers_buggy()
    assert [f(2) for f in buggy_funcs] == [8, 8, 8, 8, 8]
    
    # Fixed behavior: lambdas multiply by 0, 1, 2, 3, 4
    fixed_funcs = create_multipliers_fixed()
    assert [f(2) for f in fixed_funcs] == [0, 2, 4, 6, 8]
    print("test_create_multipliers passed.")


if __name__ == "__main__":
    print("Running Python Basics tests...")
    test_reverse_string()
    test_append_to_list()
    test_create_multipliers()
    print("All tests passed successfully.")
