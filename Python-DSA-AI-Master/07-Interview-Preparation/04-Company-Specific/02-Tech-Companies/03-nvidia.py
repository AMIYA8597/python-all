"""
NVIDIA Specific Interview Preparation Module.

Learning Objectives:
- Master array manipulations, median finding algorithms, and interval problems.
- Understand caching systems and fundamental data structures.
- Handle multi-dimensional arrays and matrix problems.

Concept Explanation:
NVIDIA often focuses on C++ and systems programming, but in Python rounds, you can expect questions involving intervals, multi-dimensional array operations (graphics/tensor analogues), and caching.
"""
from typing import List, Optional

# Basic Implementation: Merge Intervals
def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Basic level: Merge Intervals.
    """
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        last_merged = merged[-1]
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
            
    return merged

# Intermediate Implementation: LRU Cache
class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    """
    Intermediate level: Least Recently Used Cache.
    Implemented using a Doubly Linked List and a Hash Map.
    """
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {} 
        self.left, self.right = Node(), Node() 
        self.left.next, self.right.prev = self.right, self.left

    def _remove(self, node: Node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev

    def _insert(self, node: Node):
        prev, nxt = self.right.prev, self.right
        prev.next = nxt.prev = node
        node.prev, node.next = prev, nxt

    def get(self, key: int) -> int:
        if key in self.cache:
            self._remove(self.cache[key])
            self._insert(self.cache[key])
            return self.cache[key].val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self._insert(self.cache[key])
        if len(self.cache) > self.cap:
            lru = self.left.next
            self._remove(lru)
            del self.cache[lru.key]

# Advanced Implementation: Median of Two Sorted Arrays
def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    """
    Advanced level: Median of Two Sorted Arrays.
    
    Performance Analysis:
    - Time Complexity: O(log(min(m,n))) using binary search.
    - Space Complexity: O(1).
    """
    A, B = nums1, nums2
    total = len(nums1) + len(nums2)
    half = total // 2
    if len(B) < len(A):
        A, B = B, A
        
    l, r = 0, len(A) - 1
    while True:
        i = (l + r) // 2 
        j = half - i - 2 
        
        Aleft = A[i] if i >= 0 else float("-infinity")
        Aright = A[i + 1] if (i + 1) < len(A) else float("infinity")
        Bleft = B[j] if j >= 0 else float("-infinity")
        Bright = B[j + 1] if (j + 1) < len(B) else float("infinity")
        
        if Aleft <= Bright and Bleft <= Aright:
            if total % 2:
                return min(Aright, Bright)
            return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
        elif Aleft > Bright:
            r = i - 1
        else:
            l = i + 1

def run_tests():
    print("Testing Merge Intervals...")
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    assert merge_intervals(intervals) == [[1,6],[8,10],[15,18]]
    
    print("Testing LRU Cache...")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)
    assert lru.get(2) == -1
    
    print("Testing Median of Two Sorted Arrays...")
    nums1, nums2 = [1,3], [2]
    assert findMedianSortedArrays(nums1, nums2) == 2.0
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
