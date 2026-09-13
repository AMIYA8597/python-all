"""
LeetCode Medium Problems for Competitive Programming
==================================================

This module covers "Medium" level algorithmic problems commonly found on LeetCode.

Learning Objectives:
1. Apply advanced data structures like Heaps, Tries, and monotonic stacks.
2. Master algorithmic paradigms like Graph Traversal (BFS/DFS), Backtracking, and Dynamic Programming.
3. Understand trade-offs between time and space complexity.

Concept Explanation:
Medium problems typically involve combining multiple concepts or recognizing a non-obvious 
application of a known algorithm. Examples include graph traversals (island problems), 
sliding window techniques for subarrays, and backtracking for combinatorics.

Basic vs Professional Implementation:
A basic backtracking approach might recalculate identical states or use excessive memory by creating 
copies of large collections. A professional implementation uses backtracking with state restoration (in-place)
and memoization to prune the search space effectively.

Use Cases:
- Core problem sets for technical interviews at top tech companies.
- Competitive programming (Div 2 and Div 3 levels).
- Building efficient real-world algorithms for parsing, networking, and optimization.

"""

from typing import List
import collections

def number_of_islands(grid: List[List[str]]) -> int:
    """
    Counts the number of islands (connected components of '1's) in a 2D grid.
    
    Approach:
    Use Depth-First Search (DFS) or Breadth-First Search (BFS) to traverse the grid.
    When a '1' is found, increment the island count and trigger a traversal that marks
    all connected '1's as '0's (visited) to avoid double counting.
    
    Time Complexity: O(M * N) where M is rows and N is cols.
    Space Complexity: O(M * N) for the recursion stack in the worst case (a grid filled with '1's).
    
    Args:
        grid: A 2D list of strings '1' (land) and '0' (water).
        
    Returns:
        Integer count of islands.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r: int, c: int):
        # Base case / bounds check
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited by mutating the grid (can also use a visited set if mutation is not allowed)
        grid[r][c] = '0'
        
        # Traverse neighbors
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
                
    return islands


def length_of_longest_substring(s: str) -> int:
    """
    Finds the length of the longest substring without repeating characters.
    
    Approach:
    Sliding window using two pointers (left and right). We use a hash map to store the 
    most recent index of each character. If we see a character again, we move the left 
    pointer to skip the repeating character.
    
    Time Complexity: O(N) where N is the length of the string.
    Space Complexity: O(min(M, N)) where M is the size of the charset.
    
    Args:
        s: Input string.
        
    Returns:
        Length of the longest valid substring.
    """
    char_index_map = {}
    max_length = 0
    left = 0
    
    for right, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= left:
            # Move the left pointer to the right of the previous occurrence
            left = char_index_map[char] + 1
            
        char_index_map[char] = right
        max_length = max(max_length, right - left + 1)
        
    return max_length


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Finds all unique triplets in the array which gives the sum of zero.
    
    Approach:
    Sort the array. Iterate through the array and use two pointers (left and right) 
    to find pairs that sum to `-num`. We must skip duplicate values to ensure unique triplets.
    
    Time Complexity: O(N^2) where N is the number of elements.
    Space Complexity: O(1) or O(N) depending on the sorting algorithm.
    
    Args:
        nums: List of integers.
        
    Returns:
        List of lists, where each inner list is a valid triplet.
    """
    res = []
    nums.sort()
    
    for i in range(len(nums)):
        # Skip positive integers as their sum can never be zero
        if nums[i] > 0:
            break
        
        # Skip duplicates for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total > 0:
                right -= 1
            elif total < 0:
                left += 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                
                # Skip duplicates for the second element
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                    
    return res

# ==========================================
# Common Mistakes & Performance Considerations
# ==========================================
# 1. Not handling duplicates properly in 3Sum will result in Time Limit Exceeded or incorrect output.
# 2. In grid traversal problems, failing to mark nodes as visited leads to infinite recursion/loops.

# ==========================================
# Interview Challenge
# ==========================================
# How would you modify the Number of Islands solution if the grid is too large to fit in memory
# and you have to read it in chunks? (Hint: Union-Find across boundaries).

if __name__ == "__main__":
    print("Testing Number of Islands...")
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert number_of_islands(grid1) == 1
    
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert number_of_islands(grid2) == 3
    print("Number of Islands passed.")

    print("Testing Longest Substring Without Repeating Characters...")
    assert length_of_longest_substring("abcabcbb") == 3 # "abc"
    assert length_of_longest_substring("bbbbb") == 1    # "b"
    assert length_of_longest_substring("pwwkew") == 3   # "wke"
    print("Longest Substring passed.")

    print("Testing 3Sum...")
    assert three_sum([-1,0,1,2,-1,-4]) == [[-1,-1,2],[-1,0,1]]
    assert three_sum([0,1,1]) == []
    assert three_sum([0,0,0]) == [[0,0,0]]
    print("3Sum passed.")
    
    print("\nAll tests passed successfully.")
