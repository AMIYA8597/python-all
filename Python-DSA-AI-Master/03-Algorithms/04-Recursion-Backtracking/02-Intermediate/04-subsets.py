"""
Subsets and Power Set (Backtracking)

This module explains the Subsets problem and demonstrates how to solve it using 
the backtracking paradigm.

Learning Objectives:
1. Understand the concept of a Power Set and subsets.
2. Master the backtracking template for combinations and subsets.
3. Learn how to optimize recursive calls and manage state (path).
4. Analyze the time and space complexity of generating all subsets.

Concept Explanation:
Given an integer array nums of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets.

A subset of an array is a selection of elements (possibly none) of the array.
For an array of size N, there are exactly 2^N possible subsets.

Beginner Explanation:
Imagine you have a bag with an apple, a banana, and a cherry. What are all the possible
combinations of fruits you can take out of the bag?
- You could take nothing: []
- You could take one fruit: [apple], [banana], [cherry]
- You could take two fruits: [apple, banana], [apple, cherry], [banana, cherry]
- You could take all three: [apple, banana, cherry]
Backtracking systematically explores these choices: for each item, we either "include" it
or "exclude" it from our current selection.

Professional Implementation:
In professional scenarios, generating subsets can be done via recursion (backtracking) or 
iteratively (using bit manipulation or cascading). We implement both below, with type hints
and robust edge-case handling.
"""

from typing import List

def subsets_recursive(nums: List[int]) -> List[List[int]]:
    """
    Generate all subsets using classic backtracking (Depth-First Search).
    
    Time Complexity: O(N * 2^N) - We generate 2^N subsets, and for each, 
                     copying the path into the result takes O(N) worst case.
    Space Complexity: O(N) for the recursion stack (excluding output space).
    """
    if not nums:
        return [[]]
        
    result: List[List[int]] = []
    
    def backtrack(index: int, current_path: List[int]) -> None:
        # Every path we encounter is a valid subset, so we add it immediately.
        # We append a COPY of current_path because lists are mutable in Python.
        result.append(list(current_path))
        
        # Iterate over the remaining elements to branch out
        for i in range(index, len(nums)):
            # "Include" nums[i]
            current_path.append(nums[i])
            # Move on to the next element
            backtrack(i + 1, current_path)
            # "Exclude" nums[i] (backtrack)
            current_path.pop()
            
    backtrack(0, [])
    return result

def subsets_iterative(nums: List[int]) -> List[List[int]]:
    """
    Generate all subsets using cascading (iterative approach).
    
    Time Complexity: O(N * 2^N)
    Space Complexity: O(1) auxiliary space (excluding output).
    """
    result: List[List[int]] = [[]]
    
    for num in nums:
        # For each number, add it to all existing subsets to create new subsets
        # We must iterate over a snapshot of the current result to avoid infinite loops
        new_subsets = []
        for curr in result:
            new_subsets.append(curr + [num])
        result.extend(new_subsets)
        
    return result

# ==========================================
# Interview Challenge & Common Mistakes
# ==========================================
# Challenge: What if `nums` contains duplicates? (e.g., Subsets II problem)
# Solution: Sort `nums` first, and in the backtrack loop, skip duplicates by checking:
# if i > index and nums[i] == nums[i-1]: continue
#
# Common Mistake: Forgetting to append a COPY of the path (i.e., doing result.append(path))
# In Python, this will result in an array full of empty lists, because all references point
# to the same list which gets popped back to empty.

def test_subsets():
    nums = [1, 2, 3]
    expected_length = 8  # 2^3
    
    res_recursive = subsets_recursive(nums)
    res_iterative = subsets_iterative(nums)
    
    assert len(res_recursive) == expected_length, "Recursive subsets length failed"
    assert len(res_iterative) == expected_length, "Iterative subsets length failed"
    
    # Check if a specific subset exists
    assert [1, 2] in res_recursive
    assert [] in res_recursive
    assert [1, 2, 3] in res_recursive
    
    print("All subset tests passed successfully!")

if __name__ == "__main__":
    test_subsets()
