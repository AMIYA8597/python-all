"""
Python Lists and Dictionaries Interview Questions

This module covers essential data structures in Python: Lists and Dictionaries (Hash Maps).
Topics covered: List comprehensions, dictionary merging, algorithmic problems using dicts,
and time/space complexity analysis.

Each question includes:
- A description of the problem.
- A beginner/naive solution.
- An advanced/optimal solution with detailed explanations.
- Edge cases and time/space complexity analysis.
- Pytest-compatible tests.
"""

from typing import List, Dict, Any, Tuple

# =============================================================================
# Question 1: Flatten a Nested List
# =============================================================================
"""
Context: Tests ability to work with list comprehensions and basic recursion or 
iteration for varied depth.

Task: Given a list of lists (1 level deep), flatten it into a single list.
"""

def flatten_list_naive(nested_list: List[List[Any]]) -> List[Any]:
    """
    Naive approach: Nested for loops.
    Time Complexity: O(N) where N is total number of elements.
    Space Complexity: O(N) for the new list.
    """
    flat = []
    for sublist in nested_list:
        for item in sublist:
            flat.append(item)
    return flat

def flatten_list_optimal(nested_list: List[List[Any]]) -> List[Any]:
    """
    Optimal approach: List comprehension.
    It's generally faster in Python because it's executed in C.
    Readability: [item for sublist in nested_list for item in sublist]
    """
    return [item for sublist in nested_list for item in sublist]

def test_flatten_list():
    nested = [[1, 2], [3, 4], [5]]
    assert flatten_list_optimal(nested) == [1, 2, 3, 4, 5]
    assert flatten_list_optimal([[], [1], []]) == [1]
    assert flatten_list_optimal([]) == []
    print("test_flatten_list passed.")


# =============================================================================
# Question 2: Merging Dictionaries
# =============================================================================
"""
Context: Tests knowledge of Python version features and dictionary operations.

Task: Merge two dictionaries. If there are overlapping keys, dict2 should overwrite dict1.
"""

def merge_dicts_old(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Python 3.4 and earlier approach: using update()
    Note: update() modifies in place, so we copy first to avoid mutating input.
    """
    merged = dict1.copy()
    merged.update(dict2)
    return merged

def merge_dicts_py35(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Python 3.5+ approach: Dictionary unpacking.
    """
    return {**dict1, **dict2}

def merge_dicts_py39(dict1: Dict[Any, Any], dict2: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Python 3.9+ approach: The merge operator `|`.
    This is the most modern and preferred way if using Python >= 3.9.
    """
    return dict1 | dict2

def test_merge_dicts():
    d1 = {'a': 1, 'b': 2}
    d2 = {'b': 3, 'c': 4}
    expected = {'a': 1, 'b': 3, 'c': 4}
    
    assert merge_dicts_old(d1, d2) == expected
    assert merge_dicts_py35(d1, d2) == expected
    assert merge_dicts_py39(d1, d2) == expected
    print("test_merge_dicts passed.")


# =============================================================================
# Question 3: Find Duplicates (Sets and Lists)
# =============================================================================
"""
Context: Tests understanding of hashable types and time complexity.

Task: Find all duplicate elements in a list. Return them as a list.
"""

def find_duplicates_naive(arr: List[int]) -> List[int]:
    """
    Naive approach: Count occurrences using count().
    Time Complexity: O(N^2) because list.count() takes O(N) and we loop N times.
    Space Complexity: O(N).
    """
    duplicates = []
    for item in arr:
        if arr.count(item) > 1 and item not in duplicates:
            duplicates.append(item)
    return duplicates

def find_duplicates_optimal(arr: List[int]) -> List[int]:
    """
    Optimal approach: Use a set to track seen items and another set for duplicates.
    Time Complexity: O(N) because set lookup is O(1) on average.
    Space Complexity: O(N) to store seen items and duplicates.
    """
    seen = set()
    duplicates = set()
    for item in arr:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

def test_find_duplicates():
    assert sorted(find_duplicates_optimal([1, 2, 3, 2, 1, 4, 5, 4])) == [1, 2, 4]
    assert find_duplicates_optimal([1, 2, 3]) == []
    assert find_duplicates_optimal([]) == []
    print("test_find_duplicates passed.")


# =============================================================================
# Question 4: Two Sum (Dictionary Application)
# =============================================================================
"""
Context: The classic LeetCode #1. Tests if the candidate knows how to use 
dictionaries (hash maps) to reduce time complexity from O(N^2) to O(N).

Task: Given an array of integers and a target sum, return the indices of the 
two numbers that add up to the target. Assume exactly one valid solution exists.
"""

def two_sum_naive(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Naive approach: Check every pair.
    Time Complexity: O(N^2).
    Space Complexity: O(1).
    """
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return -1, -1

def two_sum_optimal(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Optimal approach: One-pass Hash Map.
    As we iterate, store the needed complement (target - current) in a dict.
    Time Complexity: O(N). Dictionary lookup is O(1) average.
    Space Complexity: O(N). Store up to N elements in the dictionary.
    """
    num_to_index: Dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return num_to_index[complement], i
        num_to_index[num] = i
    
    return -1, -1 # Should not be reached based on problem constraints

def test_two_sum():
    assert two_sum_optimal([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum_optimal([3, 2, 4], 6) == (1, 2)
    assert two_sum_optimal([3, 3], 6) == (0, 1)
    print("test_two_sum passed.")


if __name__ == "__main__":
    print("Running Lists and Dictionaries tests...")
    test_flatten_list()
    test_merge_dicts()
    test_find_duplicates()
    test_two_sum()
    print("All tests passed successfully.")
