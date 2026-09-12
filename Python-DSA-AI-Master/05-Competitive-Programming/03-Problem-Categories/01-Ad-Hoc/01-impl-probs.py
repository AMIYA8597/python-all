"""
## A. Concept Name
Implementation Problems (Ad-Hoc)

## B. One-Sentence Definition
Implementation problems are algorithmic challenges where the logic or rules are explicitly given, and the difficulty lies in translating those rules into clean, bug-free, and efficient code without relying on a pre-packaged algorithmic trick.

## C. Why Does This Exist?
In the real world, software engineering is often about taking complex business requirements (rules, constraints, logic) and accurately translating them into code, testing your ability to read specifications, handle edge cases, and organize code cleanly.

## D. Intuition
Imagine following a very detailed, multi-step recipe to bake a cake. You don't need a degree in chemistry, but you must follow instructions perfectly, measure exactly, and not skip any steps, or the cake will fail.

## E. Real-Life Analogy
Translating a legal contract or tax code into software. The rules are laid out in plain English, but correctly handling all the nested conditions, exemptions, and clauses in code is an exercise in meticulous implementation.

## F. Mental Model
Think of it as building a custom state machine or a pipeline of data transformations where your primary tool is careful control flow, clear mappings (dictionaries), and modular helper functions rather than a specific algorithm like Dijkstra's or Dynamic Programming.

## G. Visual Explanation
```
Problem Statement Rules -> State / Mappings -> Careful Iteration -> Expected Output
(e.g., Roman Numeral) -> (I=1, V=5...) -> (Check IV vs VI) -> (Integer)
```

## H. Formal Explanation
An "Ad-Hoc" problem doesn't fit neatly into standard algorithmic categories. "Implementation problems" are a subset where the algorithm is either provided or trivial to deduce. The challenge is in the translation of the problem description into a programming language. Mastery involves using language-specific idioms (like Python's slice, dicts, iterables) to minimize friction and avoid deeply nested control structures.

## I. Mathematical Foundation (if applicable)
N/A - Usually relies on basic arithmetic, logic, and discrete math rather than deep mathematical theorems.

## J. From-Scratch Implementation (if applicable)
N/A - Varies entirely by problem. See examples below (Next Permutation, Roman to Integer).

## K. Library / Production Implementation (if applicable)
Often corresponds to writing parsers, formatters, validators, or migrating legacy business logic line-by-line.

## L. Trace (walk through example)
Given `roman_to_int("MCMXCIV")`
1. Iterate right to left.
2. V (5) -> total = 5. prev = 5
3. I (1) < 5 -> total -= 1 (4). prev = 1
4. C (100) > 1 -> total += 100 (104). prev = 100
5. X (10) < 100 -> total -= 10 (94). prev = 10
6. M (1000) > 10 -> total += 1000 (1094). prev = 1000
7. C (100) < 1000 -> total -= 100 (994). prev = 100
8. M (1000) > 100 -> total += 1000 (1994). prev = 1000. Returns 1994.

## M. Complexity
- Time Complexity: Typically O(N), where N is the length of the input.
- Space Complexity: O(1) or O(N), depending on whether in-place modification or extra mappings are used.

## N. Common Mistakes
1. Hardcoding too many edge cases instead of finding the general rule.
2. Creating new arrays when an in-place modification (using two pointers) would save memory.
3. Modifying an array while iterating over it, causing skipped elements.
4. Using string concatenation (`+`) in a loop instead of `"".join()` (which is O(N)).
5. Deeply nested `if/else` instead of using dictionary mappings or guard clauses.

## O. Common Confusions
"Isn't every problem an implementation problem?" Yes, but in the context of competitive programming and interviews, it implies the *only* difficulty is the implementation, whereas in a DP problem, finding the recurrence relation is the main difficulty.

## P. When To Use
- Processing structured data according to complex business rules.
- Writing game logic, simulations, or string parsers.

## Q. When NOT To Use
- When the problem clearly requires a known algorithm (like Shortest Path, Knapsack, MST). Trying to "ad-hoc" a DP problem usually leads to exponential time.

## R. Trade-offs
- Code elegance vs. speed of writing: In interviews, it's sometimes faster to write slightly messy code that works, but clean code is much less bug-prone. Use helper functions!

## S. Debugging
- Step through your code manually with the provided example test cases.
- Off-by-one errors are extremely common. Double-check loop boundaries and array indices.
- Validate input constraints. Unexpected data structures can lead to infinite loops.

## T. Memory Hook (a short memorable principle)
"Map the rules, isolate the logic, keep it flat."

## U. Active Recall (questions before answers)
1. What defines an implementation problem?
2. How can dictionaries help in implementation problems?
3. Why is iterating backwards sometimes useful (e.g., in Roman to Integer)?

## V. Practice (exercises)
Try writing the "Integer to English Words" function. Organize your code cleanly so you don't have deeply nested logic for millions, thousands, etc.

## W. Interview Question
"Implement a function that converts an integer into an English words string. For example, 123 -> 'One Hundred Twenty Three'."

## X. Project Connection
Used heavily in data pipelines, rule engines, ETL processes, and whenever translating precise business logic into software (like tax calculators or invoice generators).
"""

from typing import List

def next_permutation(nums: List[int]) -> None:
    """
    Modifies nums in-place to the next lexicographical permutation.
    
    Time Complexity: O(N) where N is the length of nums.
    Space Complexity: O(1) as it is modified in-place.
    
    Algorithm:
    1. Find the largest index i such that nums[i] < nums[i+1]. If no such i exists,
       the array is sorted in descending order. Just reverse it.
    2. If such i exists, find the largest index j > i such that nums[j] > nums[i].
    3. Swap nums[i] and nums[j].
    4. Reverse the sub-array from i+1 to the end.
    """
    if not nums:
        return

    n = len(nums)
    i = n - 2

    # Step 1: Find the first decreasing element from the end
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find the element just larger than nums[i] to swap with
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Step 3: Swap them
        nums[i], nums[j] = nums[j], nums[i]

    # Step 4: Reverse the remaining suffix
    left = i + 1
    right = n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1


def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string to an integer.
    
    Time Complexity: O(N) where N is the length of the string.
    Space Complexity: O(1).
    """
    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    # Iterate from right to left to easily handle subtractions (e.g., IV)
    for char in reversed(s):
        curr_value = roman_map[char]
        if curr_value < prev_value:
            total -= curr_value
        else:
            total += curr_value
        prev_value = curr_value
        
    return total


if __name__ == "__main__":
    # Test Next Permutation
    nums_test = [1, 2, 3]
    next_permutation(nums_test)
    assert nums_test == [1, 3, 2], f"Expected [1, 3, 2], got {nums_test}"
    
    nums_test2 = [3, 2, 1]
    next_permutation(nums_test2)
    assert nums_test2 == [1, 2, 3], f"Expected [1, 2, 3], got {nums_test2}"
    
    nums_test3 = [1, 1, 5]
    next_permutation(nums_test3)
    assert nums_test3 == [1, 5, 1], f"Expected [1, 5, 1], got {nums_test3}"

    # Test Roman to Integer
    assert roman_to_int("III") == 3
    assert roman_to_int("LVIII") == 58
    assert roman_to_int("MCMXCIV") == 1994
    
    print("All implementation problems tests passed successfully!")
