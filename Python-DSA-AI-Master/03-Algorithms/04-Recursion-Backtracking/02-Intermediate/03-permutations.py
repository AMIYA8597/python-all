"""
Permutations (Recursion & Backtracking)

Learning Objectives:
1. Master the concept of generating all permutations of a collection.
2. Understand the recursion tree for permutations and how backtracking prunes or explores state space.
3. Learn how to handle duplicates in permutations to avoid redundant work.
4. Grasp the time and space complexity implications of combinatorial problems.

Concept Explanation:
A permutation is an arrangement of all elements of a collection into a specific order. 
For a set of N distinct elements, there are N! (N factorial) possible permutations.
Backtracking is naturally suited for generating permutations: we incrementally build 
a sequence, taking one unused element at a time, recursively exploring the rest, and 
then "backtracking" (undoing our choice) to try the next possible element.

Beginner Explanation:
Imagine you have 3 differently colored blocks: Red, Green, Blue. You want to find all ways 
to line them up. 
- You put Red first. Now you only have Green and Blue left. 
  - You put Green second. Blue must be third. (Red, Green, Blue)
  - You put Blue second. Green must be third. (Red, Blue, Green)
- You put Green first. Now you only have Red and Blue left...
This process of picking one, seeing what's left, and trying all combinations, then going 
back to try a different first block is exactly how backtracking works!

Advanced/Internal Details:
There are two common ways to implement permutations:
1. Using a `visited` boolean array (or set) to keep track of elements currently in the path.
2. In-place swapping: We swap elements in the array to fix a prefix, recurse, and then 
   swap back (backtrack). This is incredibly space-efficient (avoids path arrays).

Handling Duplicates:
If the input array contains duplicates (e.g., [1, 1, 2]), standard permutation will generate 
duplicates. To avoid this, we can sort the array first. When iterating, if `arr[i] == arr[i-1]` 
and `arr[i-1]` was NOT used in the current recursive level, we skip it. This ensures we only 
branch once for each identical element at a given depth.

Performance & Complexity:
- Time Complexity: O(N * N!) where N is the length of the array. N! to generate all combinations, 
  and O(N) time to copy each permutation into the result list.
- Space Complexity: O(N) for the recursion stack and auxiliary space (not counting the output array).

Interview Challenge:
"Given an array of unique integers, return all possible permutations. Can you do it in O(1) 
auxiliary space?"
Answer: Yes, by using the backtracking swap method, we don't need a `visited` array or a separate `path` 
array, achieving O(1) extra space beyond the call stack and output list.
"""

from typing import List

def permute_basic(nums: List[int]) -> List[List[int]]:
    """
    Basic Permutation generation using a 'path' array and a 'visited' boolean array.
    Works for distinct integers.
    
    Args:
        nums: List of distinct integers.
        
    Returns:
        List of all permutations.
    """
    result = []
    visited = [False] * len(nums)
    
    def backtrack(path: List[int]):
        # Base case: if path length equals nums length, we found a permutation
        if len(path) == len(nums):
            result.append(path[:])  # Append a deep copy of path
            return
            
        for i in range(len(nums)):
            if not visited[i]:
                # Choose
                visited[i] = True
                path.append(nums[i])
                
                # Explore
                backtrack(path)
                
                # Un-choose (Backtrack)
                path.pop()
                visited[i] = False
                
    backtrack([])
    return result


def permute_optimized_swap(nums: List[int]) -> List[List[int]]:
    """
    Professional implementation using in-place swapping.
    Saves space by eliminating the 'visited' array and 'path' list.
    Works for distinct integers.
    
    Args:
        nums: List of distinct integers.
        
    Returns:
        List of all permutations.
    """
    result = []
    
    def backtrack(start: int):
        if start == len(nums):
            result.append(nums[:])
            return
            
        for i in range(start, len(nums)):
            # Swap to place element at index i into the 'start' position
            nums[start], nums[i] = nums[i], nums[start]
            
            # Recurse for the rest of the array
            backtrack(start + 1)
            
            # Backtrack: undo the swap
            nums[start], nums[i] = nums[i], nums[start]
            
    backtrack(0)
    return result


def permute_unique(nums: List[int]) -> List[List[int]]:
    """
    Advanced implementation: Generates unique permutations for arrays that might contain duplicates.
    Sorts the array first and skips duplicate branches.
    
    Args:
        nums: List of integers (may contain duplicates).
        
    Returns:
        List of unique permutations.
    """
    result = []
    nums.sort()  # Essential for duplicate skipping logic
    visited = [False] * len(nums)
    
    def backtrack(path: List[int]):
        if len(path) == len(nums):
            result.append(path[:])
            return
            
        for i in range(len(nums)):
            if visited[i]:
                continue
                
            # Skip duplicates: 
            # If the current element is the same as the previous one, AND the previous one 
            # was NOT visited (meaning it was just backtracked from in the same loop level), 
            # we skip it to prevent creating the same permutation branch.
            if i > 0 and nums[i] == nums[i-1] and not visited[i-1]:
                continue
                
            visited[i] = True
            path.append(nums[i])
            
            backtrack(path)
            
            path.pop()
            visited[i] = False
            
    backtrack([])
    return result


# ==========================================
# Tests and Assertions
# ==========================================
if __name__ == "__main__":
    print("Testing Permutation Algorithms...")
    
    # Test Basic Permutation
    nums1 = [1, 2, 3]
    res1 = permute_basic(nums1)
    assert len(res1) == 6, "Failed length check for 3 elements"
    assert [1, 2, 3] in res1 and [3, 2, 1] in res1, "Missing expected permutations"
    
    # Test Optimized Swap Permutation
    res2 = permute_optimized_swap(nums1)
    assert len(res2) == 6, "Swap method failed length check"
    
    # Test Unique Permutations (with duplicates)
    nums_dup = [1, 1, 2]
    res_dup = permute_unique(nums_dup)
    assert len(res_dup) == 3, f"Expected 3 unique permutations, got {len(res_dup)}"
    expected_unique = [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    for p in expected_unique:
        assert p in res_dup, f"Missing unique permutation: {p}"
        
    print("All tests passed successfully!")
