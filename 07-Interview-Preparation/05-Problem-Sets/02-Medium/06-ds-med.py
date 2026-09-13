"""
Medium Data Structures Interview Questions

This module contains a comprehensive set of medium-level data structure interview questions.
It is designed to bridge the gap between basic concepts and advanced algorithmic thinking,
often asked in coding interviews for mid-level software engineering roles.

We cover:
1. Advanced list manipulations (e.g., sliding window, two pointers).
2. Hash maps and hash sets for optimal lookups.
3. Stack and Queue applications.
4. Tree traversal and properties.

Each problem includes:
- A beginner explanation and a deep technical explanation.
- An optimal Python solution with type hints.
- Real-world use cases.
- Time and Space Complexity analysis.
- Unit tests using the `unittest` framework to ensure correctness.

---
Problem 1: LRU Cache (Least Recently Used)
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Problem 2: Daily Temperatures
Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature.

Problem 3: Binary Tree Right Side View
Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.
"""

import collections
import unittest
from typing import List, Optional, Dict

# ============================================================================
# Problem 1: LRU (Least Recently Used) Cache
# ============================================================================
# Beginner Explanation:
# Imagine you have a small desk. You can only fit a few books on it. When you
# bring a new book to read and the desk is full, you remove the book you haven't
# read for the longest time to make space. An LRU Cache works the same way for data in software.
#
# Technical Explanation:
# An LRU cache requires O(1) time complexity for both `get` and `put` operations.
# To achieve this, we use a combination of a Hash Map (for O(1) lookups) and a
# Doubly Linked List (for O(1) insertions and deletions at both ends).
# In Python, `collections.OrderedDict` internally implements this exact structure,
# making it extremely efficient for this problem. However, in an interview, you may
# be asked to implement the Doubly Linked List manually. Here, we use `OrderedDict`.
#
# Real-World Use Cases:
# - Browser history and caching web pages.
# - Database query caching.
# - Operating System page replacement algorithms.
#
# Performance Considerations:
# Time Complexity: O(1) for `get` and `put`.
# Space Complexity: O(C) where C is the capacity of the cache.
# ============================================================================

class LRUCache:
    def __init__(self, capacity: int):
        self.cache: collections.OrderedDict[int, int] = collections.OrderedDict()
        self.capacity: int = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # Move the accessed item to the end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Update value and mark as most recently used
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            self.cache[key] = value
            # If over capacity, remove the first item (least recently used)
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)

# ============================================================================
# Problem 2: Daily Temperatures
# ============================================================================
# Beginner Explanation:
# You have a list of temperatures for the upcoming days. For each day, you want
# to know how many days you have to wait until it gets warmer. If it never gets
# warmer, you wait 0 days.
#
# Technical Explanation:
# A naive solution would be nested loops, taking O(N^2) time.
# The optimal solution uses a "Monotonic Decreasing Stack". We iterate through the
# array, and for each day, we push its index onto the stack. If we encounter a
# day that is warmer than the day represented by the index at the top of the stack,
# we pop the stack and calculate the difference in days.
#
# Real-World Use Cases:
# - Stock market analysis (finding the next day the price is higher).
# - Time series data analysis where you need the next "peak" or "threshold" event.
#
# Performance Considerations:
# Time Complexity: O(N) because each index is pushed and popped at most once.
# Space Complexity: O(N) for the stack in the worst-case (strictly decreasing temps).
# ============================================================================

def dailyTemperatures(temperatures: List[int]) -> List[int]:
    n = len(temperatures)
    answer = [0] * n
    stack: List[int] = [] # Stores indices

    for i, temp in enumerate(temperatures):
        # While stack is not empty and current temp is greater than the temp at top of stack
        while stack and temp > temperatures[stack[-1]]:
            prev_index = stack.pop()
            answer[prev_index] = i - prev_index
        stack.append(i)
    
    return answer

# ============================================================================
# Problem 3: Binary Tree Right Side View
# ============================================================================
# Beginner Explanation:
# Look at a family tree from the right side. You can only see the people on the
# outermost right edge at each level. Some people might be hidden behind others.
# We want to list the people we can see from top to bottom.
#
# Technical Explanation:
# This requires traversing the tree level by level (Breadth-First Search - BFS).
# We can use a queue to keep track of nodes at the current level. For each level,
# the last node processed will be the one visible from the right side.
# Alternatively, Depth-First Search (DFS) can be used by prioritizing the right child.
#
# Real-World Use Cases:
# - Rendering UI elements where only top-most or right-most elements are visible (z-indexing).
# - Analyzing hierarchical directory structures.
#
# Performance Considerations:
# Time Complexity: O(N) where N is the number of nodes (we visit every node).
# Space Complexity: O(D) where D is the diameter of the tree for the BFS queue, or O(H) for DFS call stack.
# ============================================================================

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def rightSideView(root: Optional[TreeNode]) -> List[int]:
    if not root:
        return []
    
    right_view: List[int] = []
    queue = collections.deque([root])
    
    while queue:
        level_length = len(queue)
        for i in range(level_length):
            node = queue.popleft()
            # If it's the last node in the current level, add to view
            if i == level_length - 1:
                right_view.append(node.val)
            
            # Add children for the next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
    return right_view

# ============================================================================
# Unit Tests
# ============================================================================
class TestMediumDS(unittest.TestCase):
    
    def test_lru_cache(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        self.assertEqual(cache.get(1), 1)    # returns 1
        cache.put(3, 3)                      # evicts key 2
        self.assertEqual(cache.get(2), -1)   # returns -1 (not found)
        cache.put(4, 4)                      # evicts key 1
        self.assertEqual(cache.get(1), -1)   # returns -1 (not found)
        self.assertEqual(cache.get(3), 3)    # returns 3
        self.assertEqual(cache.get(4), 4)    # returns 4

    def test_daily_temperatures(self):
        self.assertEqual(dailyTemperatures([73,74,75,71,69,72,76,73]), [1,1,4,2,1,1,0,0])
        self.assertEqual(dailyTemperatures([30,40,50,60]), [1,1,1,0])
        self.assertEqual(dailyTemperatures([30,60,90]), [1,1,0])
        self.assertEqual(dailyTemperatures([90,80,70]), [0,0,0]) # strictly decreasing

    def test_right_side_view(self):
        # Tree:
        #    1
        #  /   \
        # 2     3
        #  \     \
        #   5     4
        root1 = TreeNode(1)
        root1.left = TreeNode(2)
        root1.right = TreeNode(3)
        root1.left.right = TreeNode(5)
        root1.right.right = TreeNode(4)
        self.assertEqual(rightSideView(root1), [1, 3, 4])
        
        # Tree:
        #    1
        #   /
        #  3
        root2 = TreeNode(1, left=TreeNode(3))
        self.assertEqual(rightSideView(root2), [1, 3])
        
        # Empty Tree
        self.assertEqual(rightSideView(None), [])

if __name__ == '__main__':
    unittest.main()
