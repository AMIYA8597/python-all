# Problem Solving Patterns for Coding Interviews

## 1. Introduction

Memorizing solutions to hundreds of coding problems is an inefficient and brittle strategy for interview preparation. Instead, top candidates focus on recognizing **patterns**. Many complex algorithms and data structure problems can be mapped to a relatively small set of foundational patterns. Once you recognize the pattern, the structure of the solution becomes clear.

This document details the most critical problem-solving patterns you must master for technical interviews, complete with deep explanations and Python implementations.

---

## 2. Sliding Window

### 2.1 Concept
The Sliding Window pattern is used to perform operations on a specific window size of a given array or linked list. It's particularly useful when you need to find subarrays or substrings that satisfy certain conditions (e.g., max sum, longest substring with distinct characters). 

Instead of recomputing the operations for overlapping elements in consecutive windows, we "slide" the window by moving its boundaries, adding the new element and removing the old one.

### 2.2 Use Cases
- Finding maximum/minimum subarrays of a given size.
- Finding the longest substring with K distinct characters.
- String anagrams.

### 2.3 Python Example: Maximum Sum Subarray of Size K

```python
def max_sub_array_of_size_k(k, arr):
    """
    Finds the maximum sum of any contiguous subarray of size k.
    
    Time Complexity: O(N) where N is the number of elements in the array.
    Space Complexity: O(1)
    """
    max_sum = 0
    window_sum = 0
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]  # Add the next element
        
        # When we hit the window size, evaluate and slide
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]  # Remove the element going out
            window_start += 1                # Slide the window ahead
            
    return max_sum

# Example Usage
print(max_sub_array_of_size_k(3, [2, 1, 5, 1, 3, 2]))  # Output: 9 (subarray [5, 1, 3])
```

---

## 3. Two Pointers

### 3.1 Concept
In problems where we deal with sorted arrays (or linked lists) and need to find a set of elements that fulfill certain constraints, the Two Pointers approach becomes quite useful. The set of elements could be a pair, a triplet or even a subarray. We use two pointers iterating through the data structure in tandem until one or both of the pointers hit a certain condition.

### 3.2 Use Cases
- Finding pairs with a target sum in a sorted array.
- Removing duplicates in-place.
- Comparing strings containing backspaces.
- Reversing an array.

### 3.3 Python Example: Pair with Target Sum

```python
def pair_with_targetsum(arr, target_sum):
    """
    Finds a pair in a sorted array that adds up to a target sum.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    left = 0
    right = len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target_sum:
            return [left, right] # Found the pair
        elif target_sum > current_sum:
            left += 1  # Need a larger sum, move left pointer right
        else:
            right -= 1 # Need a smaller sum, move right pointer left
            
    return [-1, -1] # Pair not found

# Example Usage
print(pair_with_targetsum([1, 2, 3, 4, 6], 6)) # Output: [1, 3] (indices of 2 and 4)
```

---

## 4. Fast & Slow Pointers (Tortoise & Hare)

### 4.1 Concept
The Fast and Slow pointer approach, also known as the Hare & Tortoise algorithm, is a pointer algorithm that uses two pointers moving through an iterable (like an array or linked list) at different speeds. This approach is primarily used to detect cycles in a cyclic data structure.

### 4.2 Use Cases
- Detecting a cycle in a Linked List.
- Finding the middle node of a Linked List.
- Determining if a number is a "Happy Number".

### 4.3 Python Example: Linked List Cycle Detection

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def has_cycle(head):
    """
    Detects if a linked list contains a cycle.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        fast = fast.next.next # Moves 2 steps
        slow = slow.next      # Moves 1 step
        
        if slow == fast:      # They meet, cycle exists
            return True
            
    return False

# Example Setup
head = Node(1)
head.next = Node(2)
head.next.next = Node(3)
head.next.next.next = head.next # Creates a cycle back to Node 2

print(has_cycle(head)) # Output: True
```

---

## 5. Merge Intervals

### 5.1 Concept
The Merge Intervals pattern deals with problems involving overlapping intervals. In mostly all interval problems, we either need to find overlapping intervals or merge intervals if they overlap. The standard approach is to sort the intervals based on their start times and then process them sequentially.

### 5.2 Use Cases
- Merging overlapping schedules/meetings.
- Inserting a new interval into a list of sorted intervals.
- Determining if any two intervals overlap.

### 5.3 Python Example: Merge Overlapping Intervals

```python
def merge_intervals(intervals):
    """
    Merges all overlapping intervals.
    
    Time Complexity: O(N log N) due to sorting.
    Space Complexity: O(N) to store the result list.
    """
    if not intervals:
        return []

    # Sort intervals based on the start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for i in range(1, len(intervals)):
        current_interval = intervals[i]
        last_added_interval = merged[-1]
        
        # Check if the current interval overlaps with the last added interval
        if current_interval[0] <= last_added_interval[1]:
            # Merge by updating the end time of the last added interval
            last_added_interval[1] = max(last_added_interval[1], current_interval[1])
        else:
            # No overlap, add the current interval
            merged.append(current_interval)
            
    return merged

# Example Usage
print(merge_intervals([[1,4], [2,5], [7,9]])) # Output: [[1, 5], [7, 9]]
```

---

## 6. Breadth First Search (BFS) for Trees/Graphs

### 6.1 Concept
BFS is a traversal strategy for trees or graphs where we explore all the nodes at the present depth level before moving on to the nodes at the next depth level. It is typically implemented using a Queue data structure to keep track of the nodes to visit next.

### 6.2 Use Cases
- Level order traversal of a tree.
- Finding the shortest path in an unweighted graph.
- Connecting level-order siblings.

### 6.3 Python Example: Tree Level Order Traversal

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order_traversal(root):
    """
    Returns the level order traversal of a binary tree.
    
    Time Complexity: O(N) where N is the total number of nodes.
    Space Complexity: O(N) for the queue.
    """
    result = []
    if root is None:
        return result

    queue = deque()
    queue.append(root)

    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            current_node = queue.popleft()
            current_level.append(current_node.val)
            
            # Add children to the queue
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
                
        result.append(current_level)
        
    return result

# Example Usage
root = TreeNode(12)
root.left = TreeNode(7)
root.right = TreeNode(1)
root.left.left = TreeNode(9)
root.right.left = TreeNode(10)
root.right.right = TreeNode(5)

print(level_order_traversal(root)) # Output: [[12], [7, 1], [9, 10, 5]]
```

---

## 7. Depth First Search (DFS) for Trees/Graphs

### 7.1 Concept
DFS is a traversal strategy where we go as deep as possible down one path before backtracking. It is typically implemented using Recursion (which implicitly uses the call stack) or iteratively using an explicit Stack data structure.

### 7.2 Use Cases
- Path finding problems (e.g., does a path exist from root to leaf with a given sum).
- Topological sorting.
- Finding connected components in a graph.

### 7.3 Python Example: Path Sum

```python
def has_path_sum(root, target_sum):
    """
    Determines if a tree has a root-to-leaf path that adds up to target_sum.
    
    Time Complexity: O(N)
    Space Complexity: O(H) where H is the height of the tree (call stack overhead).
    """
    if root is None:
        return False

    # If the current node is a leaf and its value is equal to target_sum, we've found a path
    if root.val == target_sum and root.left is None and root.right is None:
        return True

    # Recursively call to traverse the left and right sub-tree
    # Subtract current node's value from the target sum
    return has_path_sum(root.left, target_sum - root.val) or \
           has_path_sum(root.right, target_sum - root.val)
```

---

## 8. Top 'K' Elements (Heaps)

### 8.1 Concept
Any problem that asks us to find the top/smallest/frequent 'K' elements among a given set falls under this pattern. The most efficient data structure to track the 'K' elements is a Heap. 
- Use a Min-Heap to find the Top K *largest* elements.
- Use a Max-Heap to find the Top K *smallest* elements.

### 8.2 Use Cases
- Top K numbers in an array.
- Kth smallest number.
- Top K frequent words.

### 8.3 Python Example: Find Top K Largest Numbers

```python
import heapq

def find_k_largest_numbers(nums, k):
    """
    Finds the K largest numbers in an array using a Min-Heap.
    
    Time Complexity: O(N log K) 
    Space Complexity: O(K) for the heap.
    """
    min_heap = []
    
    # Put first 'K' numbers in the min heap
    for i in range(k):
        heapq.heappush(min_heap, nums[i])
        
    # Go through the remaining numbers of the array, if the number from the array 
    # is bigger than the top(smallest) number of the min-heap, remove top number 
    # and add the number from array
    for i in range(k, len(nums)):
        if nums[i] > min_heap[0]:
            heapq.heappop(min_heap)
            heapq.heappush(min_heap, nums[i])
            
    # The heap now contains the top k largest numbers
    return list(min_heap)

print(find_k_largest_numbers([3, 1, 5, 12, 2, 11], 3)) # Output: [5, 12, 11] (order may vary)
```

## 9. Conclusion
Mastering these patterns (and others like Backtracking, Dynamic Programming, and Topological Sort) provides a robust mental framework for deconstructing new, unseen problems during interviews. Always look for the underlying structure of the problem before writing code.
