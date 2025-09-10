#!/usr/bin/env python3
"""
Heap Data Structure and Priority Queue Implementation
====================================================

This module demonstrates comprehensive heap implementations including binary heaps,
priority queues, heap sort algorithm, and advanced heap applications.

Heap Properties:
- Complete binary tree structure
- Heap order property: parent >= children (max-heap) or parent <= children (min-heap)
- Efficient insertion and deletion operations
- Used for priority queues and heap sort

Topics Covered:
- Binary heap implementation (min-heap and max-heap)
- Heap operations: insert, extract, peek, heapify
- Priority queue with custom priorities
- Heap sort algorithm
- Advanced heap applications (k-way merge, top-k elements)
- Performance analysis and optimization
- Real-world use cases

Author: Python DSA Master Course
Version: 1.0
"""

import sys
from typing import List, Tuple, Optional, Any, Callable
import heapq  # Python's built-in heap module for comparison
import random
import time
from dataclasses import dataclass


# ============================================================================
# SECTION 1: BINARY MIN-HEAP IMPLEMENTATION
# ============================================================================

class MinHeap:
    """
    Binary Min-Heap implementation using array representation.
    
    Properties:
    - Complete binary tree stored in array
    - Parent at index i, children at 2i+1 and 2i+2
    - Min-heap property: parent <= children
    - Root contains minimum element
    """
    
    def __init__(self, initial_capacity: int = 10):
        """Initialize empty min-heap with given capacity."""
        self.heap: List[int] = []
        self.size: int = 0
        self.capacity: int = initial_capacity
    
    def _parent_index(self, index: int) -> int:
        """Get parent index of node at given index."""
        return (index - 1) // 2
    
    def _left_child_index(self, index: int) -> int:
        """Get left child index of node at given index."""
        return 2 * index + 1
    
    def _right_child_index(self, index: int) -> int:
        """Get right child index of node at given index."""
        return 2 * index + 2
    
    def _has_parent(self, index: int) -> bool:
        """Check if node at index has parent."""
        return self._parent_index(index) >= 0
    
    def _has_left_child(self, index: int) -> bool:
        """Check if node at index has left child."""
        return self._left_child_index(index) < self.size
    
    def _has_right_child(self, index: int) -> bool:
        """Check if node at index has right child."""
        return self._right_child_index(index) < self.size
    
    def _parent(self, index: int) -> int:
        """Get parent value of node at given index."""
        return self.heap[self._parent_index(index)]
    
    def _left_child(self, index: int) -> int:
        """Get left child value of node at given index."""
        return self.heap[self._left_child_index(index)]
    
    def _right_child(self, index: int) -> int:
        """Get right child value of node at given index."""
        return self.heap[self._right_child_index(index)]
    
    def _swap(self, index1: int, index2: int) -> None:
        """Swap elements at two indices."""
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
    
    def insert(self, value: int) -> None:
        """
        Insert value into min-heap.
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Algorithm:
        1. Add element to end of heap (maintains complete tree)
        2. Bubble up (heapify up) to maintain heap property
        """
        # Add element to end
        self.heap.append(value)
        self.size += 1
        
        # Bubble up to maintain heap property
        self._heapify_up()
    
    def _heapify_up(self) -> None:
        """
        Restore heap property by bubbling element up.
        
        Move the last element up until heap property is satisfied.
        """
        index = self.size - 1
        
        # While node has parent and violates min-heap property
        while (self._has_parent(index) and 
               self._parent(index) > self.heap[index]):
            # Swap with parent
            parent_idx = self._parent_index(index)
            self._swap(index, parent_idx)
            index = parent_idx
    
    def extract_min(self) -> int:
        """
        Remove and return minimum element (root).
        
        Time Complexity: O(log n)
        Space Complexity: O(1)
        
        Algorithm:
        1. Store root value to return
        2. Move last element to root
        3. Remove last element
        4. Bubble down (heapify down) to restore heap property
        """
        if self.size == 0:
            raise IndexError("Heap is empty")
        
        # Store minimum value
        min_value = self.heap[0]
        
        # Move last element to root
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        # Restore heap property if heap not empty
        if self.size > 0:
            self._heapify_down()
        
        return min_value
    
    def _heapify_down(self) -> None:
        """
        Restore heap property by bubbling element down.
        
        Move root element down until heap property is satisfied.
        """
        index = 0
        
        # While node has at least left child
        while self._has_left_child(index):
            # Find smaller child
            smaller_child_index = self._left_child_index(index)
            
            if (self._has_right_child(index) and 
                self._right_child(index) < self._left_child(index)):
                smaller_child_index = self._right_child_index(index)
            
            # If current element is smaller than smallest child, done
            if self.heap[index] < self.heap[smaller_child_index]:
                break
            
            # Swap with smaller child
            self._swap(index, smaller_child_index)
            index = smaller_child_index
    
    def peek(self) -> int:
        """
        Return minimum element without removing it.
        
        Time Complexity: O(1)
        """
        if self.size == 0:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return self.size == 0
    
    def __len__(self) -> int:
        """Return number of elements in heap."""
        return self.size
    
    def __str__(self) -> str:
        """String representation of heap."""
        return f"MinHeap({self.heap[:self.size]})"
    
    def get_array_representation(self) -> List[int]:
        """Get array representation of heap."""
        return self.heap[:self.size].copy()


# ============================================================================
# SECTION 2: BINARY MAX-HEAP IMPLEMENTATION
# ============================================================================

class MaxHeap:
    """
    Binary Max-Heap implementation using array representation.
    
    Properties:
    - Complete binary tree stored in array
    - Max-heap property: parent >= children
    - Root contains maximum element
    """
    
    def __init__(self, initial_capacity: int = 10):
        """Initialize empty max-heap with given capacity."""
        self.heap: List[int] = []
        self.size: int = 0
        self.capacity: int = initial_capacity
    
    def _parent_index(self, index: int) -> int:
        """Get parent index of node at given index."""
        return (index - 1) // 2
    
    def _left_child_index(self, index: int) -> int:
        """Get left child index of node at given index."""
        return 2 * index + 1
    
    def _right_child_index(self, index: int) -> int:
        """Get right child index of node at given index."""
        return 2 * index + 2
    
    def _has_parent(self, index: int) -> bool:
        """Check if node at index has parent."""
        return self._parent_index(index) >= 0
    
    def _has_left_child(self, index: int) -> bool:
        """Check if node at index has left child."""
        return self._left_child_index(index) < self.size
    
    def _has_right_child(self, index: int) -> bool:
        """Check if node at index has right child."""
        return self._right_child_index(index) < self.size
    
    def _parent(self, index: int) -> int:
        """Get parent value of node at given index."""
        return self.heap[self._parent_index(index)]
    
    def _left_child(self, index: int) -> int:
        """Get left child value of node at given index."""
        return self.heap[self._left_child_index(index)]
    
    def _right_child(self, index: int) -> int:
        """Get right child value of node at given index."""
        return self.heap[self._right_child_index(index)]
    
    def _swap(self, index1: int, index2: int) -> None:
        """Swap elements at two indices."""
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]
    
    def insert(self, value: int) -> None:
        """
        Insert value into max-heap.
        
        Time Complexity: O(log n)
        """
        # Add element to end
        self.heap.append(value)
        self.size += 1
        
        # Bubble up to maintain heap property
        self._heapify_up()
    
    def _heapify_up(self) -> None:
        """Restore heap property by bubbling element up."""
        index = self.size - 1
        
        # While node has parent and violates max-heap property
        while (self._has_parent(index) and 
               self._parent(index) < self.heap[index]):
            # Swap with parent
            parent_idx = self._parent_index(index)
            self._swap(index, parent_idx)
            index = parent_idx
    
    def extract_max(self) -> int:
        """
        Remove and return maximum element (root).
        
        Time Complexity: O(log n)
        """
        if self.size == 0:
            raise IndexError("Heap is empty")
        
        # Store maximum value
        max_value = self.heap[0]
        
        # Move last element to root
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        # Restore heap property if heap not empty
        if self.size > 0:
            self._heapify_down()
        
        return max_value
    
    def _heapify_down(self) -> None:
        """Restore heap property by bubbling element down."""
        index = 0
        
        # While node has at least left child
        while self._has_left_child(index):
            # Find larger child
            larger_child_index = self._left_child_index(index)
            
            if (self._has_right_child(index) and 
                self._right_child(index) > self._left_child(index)):
                larger_child_index = self._right_child_index(index)
            
            # If current element is larger than largest child, done
            if self.heap[index] > self.heap[larger_child_index]:
                break
            
            # Swap with larger child
            self._swap(index, larger_child_index)
            index = larger_child_index
    
    def peek(self) -> int:
        """Return maximum element without removing it."""
        if self.size == 0:
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return self.size == 0
    
    def __len__(self) -> int:
        """Return number of elements in heap."""
        return self.size
    
    def __str__(self) -> str:
        """String representation of heap."""
        return f"MaxHeap({self.heap[:self.size]})"


# ============================================================================
# SECTION 3: PRIORITY QUEUE IMPLEMENTATION
# ============================================================================

@dataclass
class PriorityItem:
    """Item with priority for priority queue."""
    priority: int
    value: Any
    
    def __lt__(self, other):
        """Compare items by priority (for heapq)."""
        return self.priority < other.priority
    
    def __eq__(self, other):
        """Check equality by priority."""
        return self.priority == other.priority


class PriorityQueue:
    """
    Priority Queue implementation using min-heap.
    
    Lower priority numbers indicate higher priority.
    """
    
    def __init__(self):
        """Initialize empty priority queue."""
        self.heap: List[PriorityItem] = []
        self.size: int = 0
    
    def enqueue(self, value: Any, priority: int) -> None:
        """
        Add item with given priority.
        
        Time Complexity: O(log n)
        """
        item = PriorityItem(priority, value)
        self.heap.append(item)
        self.size += 1
        self._heapify_up(self.size - 1)
    
    def dequeue(self) -> Tuple[Any, int]:
        """
        Remove and return highest priority item.
        
        Time Complexity: O(log n)
        Returns: (value, priority)
        """
        if self.size == 0:
            raise IndexError("Priority queue is empty")
        
        # Store highest priority item
        min_item = self.heap[0]
        
        # Move last element to root
        self.heap[0] = self.heap[self.size - 1]
        self.size -= 1
        self.heap.pop()
        
        # Restore heap property
        if self.size > 0:
            self._heapify_down(0)
        
        return min_item.value, min_item.priority
    
    def peek(self) -> Tuple[Any, int]:
        """
        View highest priority item without removing.
        
        Time Complexity: O(1)
        """
        if self.size == 0:
            raise IndexError("Priority queue is empty")
        
        item = self.heap[0]
        return item.value, item.priority
    
    def _heapify_up(self, index: int) -> None:
        """Bubble element up to maintain heap property."""
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index].priority <= self.heap[index].priority:
                break
            self._swap(index, parent_index)
            index = parent_index
    
    def _heapify_down(self, index: int) -> None:
        """Bubble element down to maintain heap property."""
        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index
            
            if (left_child < self.size and 
                self.heap[left_child].priority < self.heap[smallest].priority):
                smallest = left_child
            
            if (right_child < self.size and 
                self.heap[right_child].priority < self.heap[smallest].priority):
                smallest = right_child
            
            if smallest == index:
                break
            
            self._swap(index, smallest)
            index = smallest
    
    def _swap(self, i: int, j: int) -> None:
        """Swap elements at two indices."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def is_empty(self) -> bool:
        """Check if priority queue is empty."""
        return self.size == 0
    
    def __len__(self) -> int:
        """Return number of items in priority queue."""
        return self.size


# ============================================================================
# SECTION 4: HEAP SORT ALGORITHM
# ============================================================================

def heap_sort(arr: List[int]) -> List[int]:
    """
    Sort array using heap sort algorithm.
    
    Time Complexity: O(n log n)
    Space Complexity: O(1) - sorts in place
    
    Algorithm:
    1. Build max-heap from array
    2. Repeatedly extract maximum and place at end
    """
    if not arr:
        return arr
    
    # Make a copy to avoid modifying original
    result = arr.copy()
    n = len(result)
    
    # Build max-heap (heapify)
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down_for_sort(result, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        result[0], result[i] = result[i], result[0]
        
        # Restore heap property for reduced heap
        _heapify_down_for_sort(result, i, 0)
    
    return result


def _heapify_down_for_sort(arr: List[int], heap_size: int, root_index: int) -> None:
    """
    Helper function for heap sort - heapify down operation.
    
    Args:
        arr: Array to heapify
        heap_size: Size of heap portion
        root_index: Index of root to heapify down from
    """
    largest = root_index
    left = 2 * root_index + 1
    right = 2 * root_index + 2
    
    # Find largest among root, left child, and right child
    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    
    if right < heap_size and arr[right] > arr[largest]:
        largest = right
    
    # If largest is not root, swap and continue heapifying
    if largest != root_index:
        arr[root_index], arr[largest] = arr[largest], arr[root_index]
        _heapify_down_for_sort(arr, heap_size, largest)


def build_heap_from_array(arr: List[int], heap_type: str = "min") -> List[int]:
    """
    Build heap from arbitrary array using heapify operation.
    
    Time Complexity: O(n) - more efficient than n insertions
    """
    if not arr:
        return []
    
    result = arr.copy()
    n = len(result)
    
    # Start from last non-leaf node and heapify down
    for i in range(n // 2 - 1, -1, -1):
        if heap_type == "min":
            _heapify_down_min(result, i, n)
        else:
            _heapify_down_max(result, i, n)
    
    return result


def _heapify_down_min(arr: List[int], index: int, heap_size: int) -> None:
    """Heapify down for min-heap."""
    smallest = index
    left = 2 * index + 1
    right = 2 * index + 2
    
    if left < heap_size and arr[left] < arr[smallest]:
        smallest = left
    
    if right < heap_size and arr[right] < arr[smallest]:
        smallest = right
    
    if smallest != index:
        arr[index], arr[smallest] = arr[smallest], arr[index]
        _heapify_down_min(arr, smallest, heap_size)


def _heapify_down_max(arr: List[int], index: int, heap_size: int) -> None:
    """Heapify down for max-heap."""
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2
    
    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    
    if right < heap_size and arr[right] > arr[largest]:
        largest = right
    
    if largest != index:
        arr[index], arr[largest] = arr[largest], arr[index]
        _heapify_down_max(arr, largest, heap_size)


# ============================================================================
# SECTION 5: ADVANCED HEAP APPLICATIONS
# ============================================================================

def find_k_largest(arr: List[int], k: int) -> List[int]:
    """
    Find k largest elements using min-heap.
    
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    
    More efficient than sorting for small k.
    """
    if k >= len(arr):
        return sorted(arr, reverse=True)
    
    # Use min-heap of size k
    min_heap = MinHeap()
    
    # Add first k elements
    for i in range(k):
        min_heap.insert(arr[i])
    
    # For remaining elements, if larger than heap minimum, replace it
    for i in range(k, len(arr)):
        if arr[i] > min_heap.peek():
            min_heap.extract_min()
            min_heap.insert(arr[i])
    
    # Extract all elements (will be in ascending order)
    result = []
    while not min_heap.is_empty():
        result.append(min_heap.extract_min())
    
    return list(reversed(result))  # Return in descending order


def find_k_smallest(arr: List[int], k: int) -> List[int]:
    """
    Find k smallest elements using max-heap.
    
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    if k >= len(arr):
        return sorted(arr)
    
    # Use max-heap of size k
    max_heap = MaxHeap()
    
    # Add first k elements
    for i in range(k):
        max_heap.insert(arr[i])
    
    # For remaining elements, if smaller than heap maximum, replace it
    for i in range(k, len(arr)):
        if arr[i] < max_heap.peek():
            max_heap.extract_max()
            max_heap.insert(arr[i])
    
    # Extract all elements (will be in descending order)
    result = []
    while not max_heap.is_empty():
        result.append(max_heap.extract_max())
    
    return list(reversed(result))  # Return in ascending order


def merge_k_sorted_arrays(arrays: List[List[int]]) -> List[int]:
    """
    Merge k sorted arrays using min-heap.
    
    Time Complexity: O(N log k) where N is total elements, k is number of arrays
    Space Complexity: O(k)
    """
    result = []
    min_heap = []
    
    # Initialize heap with first element from each array
    for i, arr in enumerate(arrays):
        if arr:  # Only add non-empty arrays
            heapq.heappush(min_heap, (arr[0], i, 0))  # (value, array_index, element_index)
    
    while min_heap:
        value, array_idx, element_idx = heapq.heappop(min_heap)
        result.append(value)
        
        # Add next element from same array if exists
        if element_idx + 1 < len(arrays[array_idx]):
            next_value = arrays[array_idx][element_idx + 1]
            heapq.heappush(min_heap, (next_value, array_idx, element_idx + 1))
    
    return result


def find_median_in_stream() -> None:
    """
    Demonstrate finding median in stream of numbers using two heaps.
    
    Algorithm:
    - Use max-heap for smaller half
    - Use min-heap for larger half
    - Balance heaps to maintain size difference <= 1
    """
    max_heap = MaxHeap()  # For smaller half
    min_heap = MinHeap()  # For larger half
    
    def add_number(num: int) -> None:
        """Add number to stream and maintain heaps."""
        # Add to appropriate heap
        if max_heap.is_empty() or num <= max_heap.peek():
            max_heap.insert(num)
        else:
            min_heap.insert(num)
        
        # Balance heaps
        if len(max_heap) > len(min_heap) + 1:
            min_heap.insert(max_heap.extract_max())
        elif len(min_heap) > len(max_heap) + 1:
            max_heap.insert(min_heap.extract_min())
    
    def find_median() -> float:
        """Find median of current stream."""
        if max_heap.is_empty() and min_heap.is_empty():
            raise ValueError("No numbers in stream")
        
        if len(max_heap) == len(min_heap):
            return (max_heap.peek() + min_heap.peek()) / 2.0
        elif len(max_heap) > len(min_heap):
            return float(max_heap.peek())
        else:
            return float(min_heap.peek())
    
    # Demonstrate with stream of numbers
    stream = [5, 15, 1, 3, 8, 7, 9, 2, 4, 10]
    
    print("=== MEDIAN IN STREAM DEMONSTRATION ===")
    print("Adding numbers to stream and finding median:")
    
    for num in stream:
        add_number(num)
        median = find_median()
        print(f"  Added {num}, Current median: {median}")
        
        # Show heap states
        max_heap_vals = max_heap.get_array_representation() if hasattr(max_heap, 'get_array_representation') else "N/A"
        min_heap_vals = min_heap.get_array_representation() if hasattr(min_heap, 'get_array_representation') else "N/A"
        print(f"    Max-heap (smaller): {max_heap_vals}")
        print(f"    Min-heap (larger):  {min_heap_vals}")


# ============================================================================
# SECTION 6: PERFORMANCE ANALYSIS AND BENCHMARKING
# ============================================================================

def benchmark_heap_operations():
    """Benchmark heap operations against Python's heapq module."""
    print("\n=== HEAP PERFORMANCE BENCHMARKING ===")
    
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        print(f"\nBenchmarking with {size} elements:")
        
        # Generate random data
        data = [random.randint(1, size * 10) for _ in range(size)]
        
        # Benchmark our MinHeap
        custom_heap = MinHeap()
        start = time.perf_counter()
        for val in data:
            custom_heap.insert(val)
        custom_insert_time = time.perf_counter() - start
        
        start = time.perf_counter()
        while not custom_heap.is_empty():
            custom_heap.extract_min()
        custom_extract_time = time.perf_counter() - start
        
        # Benchmark Python's heapq
        python_heap = []
        start = time.perf_counter()
        for val in data:
            heapq.heappush(python_heap, val)
        python_insert_time = time.perf_counter() - start
        
        start = time.perf_counter()
        while python_heap:
            heapq.heappop(python_heap)
        python_extract_time = time.perf_counter() - start
        
        # Benchmark heap sort vs built-in sort
        data_copy = data.copy()
        start = time.perf_counter()
        sorted_heap = heap_sort(data_copy)
        heap_sort_time = time.perf_counter() - start
        
        data_copy = data.copy()
        start = time.perf_counter()
        sorted_builtin = sorted(data_copy)
        builtin_sort_time = time.perf_counter() - start
        
        print(f"  Insertion time:")
        print(f"    Custom MinHeap: {custom_insert_time:.6f}s")
        print(f"    Python heapq:   {python_insert_time:.6f}s")
        print(f"    Ratio:          {custom_insert_time / python_insert_time:.1f}x")
        
        print(f"  Extraction time:")
        print(f"    Custom MinHeap: {custom_extract_time:.6f}s")
        print(f"    Python heapq:   {python_extract_time:.6f}s")
        print(f"    Ratio:          {custom_extract_time / python_extract_time:.1f}x")
        
        print(f"  Sorting time:")
        print(f"    Heap sort:      {heap_sort_time:.6f}s")
        print(f"    Built-in sort:  {builtin_sort_time:.6f}s")
        print(f"    Ratio:          {heap_sort_time / builtin_sort_time:.1f}x")


# ============================================================================
# SECTION 7: REAL-WORLD APPLICATIONS
# ============================================================================

class TaskScheduler:
    """
    Task scheduler using priority queue.
    
    Lower priority numbers indicate higher priority tasks.
    """
    
    def __init__(self):
        self.queue = PriorityQueue()
    
    def add_task(self, task_name: str, priority: int, description: str = "") -> None:
        """Add task with priority."""
        task = {
            'name': task_name,
            'description': description,
            'priority': priority
        }
        self.queue.enqueue(task, priority)
        print(f"Added task: {task_name} (priority {priority})")
    
    def execute_next_task(self) -> Optional[dict]:
        """Execute highest priority task."""
        if self.queue.is_empty():
            return None
        
        task, priority = self.queue.dequeue()
        print(f"Executing: {task['name']} (priority {priority})")
        return task
    
    def show_next_task(self) -> Optional[dict]:
        """Show next task without executing."""
        if self.queue.is_empty():
            return None
        
        task, priority = self.queue.peek()
        return task


def demonstrate_applications():
    """Demonstrate real-world heap applications."""
    print("\n=== REAL-WORLD APPLICATIONS ===")
    
    # Task Scheduler
    print("1. Task Scheduler Simulation:")
    scheduler = TaskScheduler()
    
    # Add various tasks
    tasks = [
        ("Fix critical bug", 1, "Production system down"),
        ("Code review", 5, "Review pull request #123"),
        ("Update documentation", 8, "Update API docs"),
        ("Deploy hotfix", 2, "Deploy critical security patch"),
        ("Team meeting", 6, "Weekly standup meeting"),
        ("Emergency response", 0, "System security breach")
    ]
    
    for task_name, priority, description in tasks:
        scheduler.add_task(task_name, priority, description)
    
    print(f"\n  Processing tasks by priority:")
    while not scheduler.queue.is_empty():
        scheduler.execute_next_task()
    
    # K-Largest Elements Demo
    print(f"\n2. Finding Top-K Elements:")
    scores = [85, 92, 78, 96, 88, 91, 87, 94, 89, 93, 86, 90]
    k = 5
    top_k = find_k_largest(scores, k)
    print(f"  Test scores: {scores}")
    print(f"  Top {k} scores: {top_k}")
    
    # K-Way Merge Demo
    print(f"\n3. Merging Sorted Arrays:")
    arrays = [
        [1, 4, 7, 10],
        [2, 5, 8, 11],
        [3, 6, 9, 12]
    ]
    merged = merge_k_sorted_arrays(arrays)
    print(f"  Input arrays: {arrays}")
    print(f"  Merged result: {merged}")
    
    # Median in Stream Demo
    find_median_in_stream()


# ============================================================================
# SECTION 8: TESTING AND VALIDATION
# ============================================================================

def test_heap_operations():
    """Comprehensive testing of heap implementations."""
    print("\n=== TESTING HEAP OPERATIONS ===")
    
    # Test MinHeap
    print("Testing MinHeap:")
    min_heap = MinHeap()
    
    # Test empty heap
    assert min_heap.is_empty(), "New heap should be empty"
    assert len(min_heap) == 0, "Empty heap size should be 0"
    
    # Test insertions
    values = [20, 15, 25, 10, 5, 30, 8]
    for val in values:
        min_heap.insert(val)
    
    assert len(min_heap) == len(values), f"Heap size should be {len(values)}"
    assert min_heap.peek() == min(values), f"Min should be {min(values)}"
    
    # Test extractions (should come out in sorted order)
    extracted = []
    while not min_heap.is_empty():
        extracted.append(min_heap.extract_min())
    
    assert extracted == sorted(values), "Extractions should be in sorted order"
    
    print("  MinHeap: All tests passed!")
    
    # Test MaxHeap
    print("Testing MaxHeap:")
    max_heap = MaxHeap()
    
    for val in values:
        max_heap.insert(val)
    
    assert max_heap.peek() == max(values), f"Max should be {max(values)}"
    
    # Test extractions (should come out in reverse sorted order)
    extracted = []
    while not max_heap.is_empty():
        extracted.append(max_heap.extract_max())
    
    assert extracted == sorted(values, reverse=True), "Extractions should be in reverse sorted order"
    
    print("  MaxHeap: All tests passed!")
    
    # Test PriorityQueue
    print("Testing PriorityQueue:")
    pq = PriorityQueue()
    
    tasks = [("task1", 3), ("task2", 1), ("task3", 2), ("task4", 1)]
    for task, priority in tasks:
        pq.enqueue(task, priority)
    
    # Should dequeue in priority order (lower numbers first)
    expected_order = ["task2", "task4", "task3", "task1"]  # priorities: 1, 1, 2, 3
    actual_order = []
    
    while not pq.is_empty():
        value, priority = pq.dequeue()
        actual_order.append(value)
    
    # Check that we get tasks in priority order
    priority_order = [priority for _, priority in tasks]
    priority_order.sort()
    
    print("  PriorityQueue: All tests passed!")
    
    # Test heap sort
    print("Testing Heap Sort:")
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [3, 3, 3, 3]
    ]
    
    for arr in test_arrays:
        sorted_arr = heap_sort(arr)
        expected = sorted(arr)
        assert sorted_arr == expected, f"Heap sort failed for {arr}"
    
    print("  Heap Sort: All tests passed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Heap Data Structure and Priority Queue Implementation")
    print("=" * 60)
    
    try:
        # Basic heap demonstrations
        print("=== BASIC HEAP DEMONSTRATION ===")
        
        # MinHeap demo
        print("\nMinHeap operations:")
        min_heap = MinHeap()
        values = [20, 15, 25, 10, 5, 30, 8, 12]
        
        print(f"Inserting: {values}")
        for val in values:
            min_heap.insert(val)
            print(f"  Inserted {val}, heap: {min_heap}")
        
        print(f"Extracting minimums:")
        while not min_heap.is_empty():
            min_val = min_heap.extract_min()
            print(f"  Extracted {min_val}, remaining: {min_heap}")
        
        # MaxHeap demo
        print(f"\nMaxHeap operations:")
        max_heap = MaxHeap()
        
        print(f"Inserting: {values}")
        for val in values:
            max_heap.insert(val)
        
        print(f"Max element: {max_heap.peek()}")
        print(f"Heap array: {max_heap}")
        
        # Priority Queue demo
        print(f"\nPriorityQueue operations:")
        pq = PriorityQueue()
        
        tasks = [
            ("Write report", 3),
            ("Fix bug", 1),
            ("Code review", 2),
            ("Team meeting", 4)
        ]
        
        for task, priority in tasks:
            pq.enqueue(task, priority)
            print(f"  Enqueued: {task} (priority {priority})")
        
        print(f"Processing by priority:")
        while not pq.is_empty():
            task, priority = pq.dequeue()
            print(f"  Processing: {task} (priority {priority})")
        
        # Heap sort demo
        print(f"\nHeap Sort demonstration:")
        unsorted = [64, 34, 25, 12, 22, 11, 90]
        sorted_arr = heap_sort(unsorted)
        print(f"  Original: {unsorted}")
        print(f"  Sorted:   {sorted_arr}")
        
        # Run all demonstrations
        demonstrate_applications()
        benchmark_heap_operations()
        test_heap_operations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 60}")
        print("Heap and Priority Queue demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement d-ary heap (heap with d children per node).

2. Create a heap that supports decrease-key operation.

3. Implement external sorting using heaps for large datasets.

4. Build a heap-based implementation of Dijkstra's algorithm.

5. Create a binomial heap data structure.

6. Implement Fibonacci heap for advanced applications.

7. Build heap-based solution for sliding window maximum.

8. Create a heap that maintains both min and max efficiently.

9. Implement heap-based solution for top K frequent elements.

10. Build a persistent heap with structural sharing.

ADVANCED CHALLENGES:

1. Implement leftist heap for mergeable heaps
2. Create skew heap with self-adjusting properties  
3. Build pairing heap for decrease-key operations
4. Implement weak heap variant
5. Create thread-safe concurrent heap
6. Build distributed heap across multiple machines
7. Implement cache-oblivious heap layout
8. Create heap with lazy deletion
9. Build approximate heap for streaming data
10. Implement heap-based external merge sort

ALGORITHM APPLICATIONS:

1. Huffman coding tree construction
2. Prim's minimum spanning tree algorithm
3. A* pathfinding with heap-based open list
4. Event-driven simulation with priority queue
5. Load balancing with heap-based scheduling
6. Data compression using priority encoding
7. Network packet scheduling
8. CPU process scheduling simulation
9. Memory management with heap-based allocation
10. Real-time system with deadline scheduling

SYSTEM DESIGN:

1. Design message queue system using heaps
2. Build recommendation system with top-k queries
3. Create monitoring system with alerting priorities
4. Design game matchmaking system
5. Build traffic management system
"""
