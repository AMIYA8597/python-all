"""
# ==============================================================================
# LABORATORY: PRIORITY QUEUES AND HEAPS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A normal Queue processes items First-In, First-Out. But in an operating system, 
# a high-priority process (like moving the mouse) must execute before a low-priority 
# background task, regardless of when it arrived. 
# A Priority Queue solves this. Under the hood, it is implemented using a Heap, 
# achieving O(log N) insertion and extraction, which is drastically faster than 
# sorting an array (O(N log N)) every time a new item arrives.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Min-Heap and Max-Heap.
# - Use Python's `heapq` module to manage a priority queue.
# - Implement custom object priority using `__lt__` (Less Than).
# - Solve a classic FAANG interview problem: Top K Frequent Elements.
#
# ==============================================================================
"""

import heapq
from typing import List, Any
from collections import Counter

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MIN-HEAP AND MAX-HEAP BASICS
# ==============================================================================
def demonstrate_heap_basics():
    """
    Python's `heapq` module only implements a Min-Heap.
    The smallest element is ALWAYS at index 0.
    """
    section_header("Min-Heap and Max-Heap Fundamentals")
    
    # 1. Min-Heap
    numbers = [5, 1, 9, 3, 7]
    
    print("Original list:", numbers)
    # Transforms the list into a heap IN-PLACE in O(N) time.
    heapq.heapify(numbers)
    print("Min-Heapified list:", numbers)
    print(f"Smallest element (O(1) access): {numbers[0]}")
    
    print("\nExtracting elements in ascending order (O(log N) per extraction):")
    while numbers:
        print(f" Popped: {heapq.heappop(numbers)}")
        
        
    # 2. Max-Heap Workaround
    print("\n--- Max-Heap Workaround ---")
    # To create a Max-Heap in Python, push the NEGATIVE of the values.
    # The largest number becomes the smallest negative number.
    max_numbers = [5, 1, 9, 3, 7]
    max_heap = [-x for x in max_numbers]
    heapq.heapify(max_heap)
    
    print("Extracting elements in descending order (Max-Heap):")
    while max_heap:
        # Multiply by -1 again to restore the original value
        print(f" Popped: {-heapq.heappop(max_heap)}")


# ==============================================================================
# 4. CUSTOM OBJECTS IN A HEAP
# ==============================================================================
class Task:
    """
    If we put custom objects in a heap, `heapq` tries to compare them using `<`.
    We must define the `__lt__` (less than) magic method.
    """
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority # Lower number = higher priority (e.g., Priority 1 is first)
        
    def __lt__(self, other: 'Task') -> bool:
        # The heap will use this to determine ordering
        return self.priority < other.priority
        
    def __repr__(self) -> str:
        return f"Task('{self.name}', P{self.priority})"

def demonstrate_object_heap():
    section_header("Custom Object Priority Queue")
    
    task_queue = []
    
    # Push tasks (O(log N))
    heapq.heappush(task_queue, Task("Send Email", 3))
    heapq.heappush(task_queue, Task("Process Payment", 1))
    heapq.heappush(task_queue, Task("Generate Report", 5))
    heapq.heappush(task_queue, Task("Login User", 2))
    
    print("Tasks in queue (internal heap layout):", task_queue)
    
    print("\nExecuting tasks in priority order:")
    while task_queue:
        task = heapq.heappop(task_queue)
        print(f" Executing: {task.name}")


# ==============================================================================
# 5. CLASSIC INTERVIEW PROBLEM: TOP K FREQUENT ELEMENTS
# ==============================================================================
def topKFrequent(nums: List[int], k: int) -> List[int]:
    """
    LeetCode #347: Top K Frequent Elements
    Time Complexity: O(N log K)
    Space Complexity: O(N + K)
    
    Why use a heap?
    If we sort the frequencies, it takes O(N log N).
    If we use a Min-Heap of size K, it takes O(N log K). If K is small (e.g., top 10 
    out of 1,000,000 items), O(N log K) is massively faster than O(N log N).
    """
    # 1. Count frequencies (O(N))
    count = Counter(nums)
    
    heap = []
    
    # 2. Maintain a Min-Heap of size K (O(N log K))
    for num, freq in count.items():
        # Push a tuple. Python compares tuples element by element.
        # So it will sort by 'freq' first.
        heapq.heappush(heap, (freq, num))
        
        # If the heap grows larger than K, we pop the SMALLEST frequency.
        # This guarantees only the K LARGEST frequencies remain in the heap.
        if len(heap) > k:
            heapq.heappop(heap)
            
    # 3. Extract the elements (The heap contains tuples of (freq, num))
    return [num for freq, num in heap]

def demonstrate_top_k():
    section_header("Algorithm: Top K Frequent Elements")
    
    data = [1, 1, 1, 2, 2, 3, 4, 4, 4, 4, 5]
    K = 2
    
    print(f"Dataset: {data}")
    print(f"Finding the Top {K} most frequent elements...")
    
    result = topKFrequent(data, K)
    print(f"Result: {result}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the time complexity of pushing an element to a heap vs extracting an element?
   Answer: Both `heappush` and `heappop` take O(log N) time because the element must "bubble up" or "bubble down" the binary tree structure to restore the heap property.

2. How do you implement a Max-Heap in Python?
   Answer: Python's `heapq` is strictly a Min-Heap. You simulate a Max-Heap by inserting the negative of the numeric values. When extracting, you multiply by -1 again.

3. Why use a Heap instead of just calling `.sort()`?
   Answer: If you need to repeatedly extract the largest/smallest item while new items are constantly arriving (e.g., a live task queue), calling `.sort()` every time takes O(N log N), which is disastrously slow. A heap maintains its structure and extracts items in O(log N).
"""

if __name__ == "__main__":
    demonstrate_heap_basics()
    demonstrate_object_heap()
    demonstrate_top_k()
    print("\n[SUCCESS] Laboratory: Priority Queues Completed.")
