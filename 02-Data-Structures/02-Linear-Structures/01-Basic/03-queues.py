#!/usr/bin/env python3
"""
Comprehensive Queue Implementations
==================================

This module provides complete implementations of different types of queues:
1. Simple Queue (FIFO)
2. Circular Queue
3. Priority Queue
4. Deque (Double-ended Queue)

All implementations include detailed explanations, complexity analysis,
and practical examples.

Author: Python DSA Master
Date: 2024
"""

import heapq
from typing import Any, Optional, List, Tuple, Generic, TypeVar
from collections import deque as collections_deque
from dataclasses import dataclass, field

T = TypeVar('T')

# ==============================================================================
# SIMPLE QUEUE (FIFO - First In, First Out)
# ==============================================================================

class SimpleQueue(Generic[T]):
    """
    Simple Queue implementation using Python list.
    
    Time Complexities:
    - Enqueue (add to rear): O(1) amortized
    - Dequeue (remove from front): O(n) - due to list shifting
    - Peek: O(1)
    - Size: O(1)
    
    Space Complexity: O(n) where n is number of elements
    """
    
    def __init__(self):
        self._items: List[T] = []
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        """Add item to the rear of queue."""
        self._items.append(item)
        self._size += 1
    
    def dequeue(self) -> T:
        """Remove and return item from front of queue."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self._items.pop(0)  # O(n) operation
        self._size -= 1
        return item
    
    def peek(self) -> T:
        """Return front item without removing it."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return number of items in queue."""
        return self._size
    
    def __str__(self) -> str:
        return f"Queue({self._items})"
    
    def __repr__(self) -> str:
        return self.__str__()

# ==============================================================================
# EFFICIENT QUEUE USING TWO STACKS
# ==============================================================================

class EfficientQueue(Generic[T]):
    """
    Efficient Queue implementation using two stacks.
    
    This provides O(1) amortized time for both enqueue and dequeue operations.
    
    Time Complexities:
    - Enqueue: O(1)
    - Dequeue: O(1) amortized, O(n) worst case
    - Peek: O(1) amortized
    - Size: O(1)
    """
    
    def __init__(self):
        self._input_stack: List[T] = []    # For enqueue operations
        self._output_stack: List[T] = []   # For dequeue operations
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        """Add item to rear of queue."""
        self._input_stack.append(item)
        self._size += 1
    
    def dequeue(self) -> T:
        """Remove and return item from front of queue."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        # If output stack is empty, move all items from input stack
        if not self._output_stack:
            while self._input_stack:
                self._output_stack.append(self._input_stack.pop())
        
        self._size -= 1
        return self._output_stack.pop()
    
    def peek(self) -> T:
        """Return front item without removing it."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        if not self._output_stack:
            while self._input_stack:
                self._output_stack.append(self._input_stack.pop())
        
        return self._output_stack[-1]
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return number of items in queue."""
        return self._size

# ==============================================================================
# CIRCULAR QUEUE
# ==============================================================================

class CircularQueue(Generic[T]):
    """
    Circular Queue implementation with fixed capacity.
    
    Time Complexities:
    - Enqueue: O(1)
    - Dequeue: O(1)
    - Peek: O(1)
    - All operations are O(1)
    
    Space Complexity: O(capacity)
    """
    
    def __init__(self, capacity: int = 10):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self._capacity = capacity
        self._items: List[Optional[T]] = [None] * capacity
        self._front = 0
        self._rear = -1
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        """Add item to rear of queue."""
        if self.is_full():
            raise OverflowError("Queue is full")
        
        self._rear = (self._rear + 1) % self._capacity
        self._items[self._rear] = item
        self._size += 1
    
    def dequeue(self) -> T:
        """Remove and return item from front of queue."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        
        item = self._items[self._front]
        self._items[self._front] = None  # Clear reference
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item
    
    def peek(self) -> T:
        """Return front item without removing it."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[self._front]
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if queue is full."""
        return self._size == self._capacity
    
    def size(self) -> int:
        """Return number of items in queue."""
        return self._size
    
    def capacity(self) -> int:
        """Return total capacity of queue."""
        return self._capacity
    
    def display(self) -> List[T]:
        """Display all items in queue order."""
        if self.is_empty():
            return []
        
        items = []
        i = self._front
        for _ in range(self._size):
            items.append(self._items[i])
            i = (i + 1) % self._capacity
        return items

# ==============================================================================
# PRIORITY QUEUE
# ==============================================================================

@dataclass
class PriorityItem:
    """Item with priority for priority queue."""
    priority: int
    item: Any
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def __le__(self, other):
        return self.priority <= other.priority
    
    def __gt__(self, other):
        return self.priority > other.priority
    
    def __ge__(self, other):
        return self.priority >= other.priority

class PriorityQueue:
    """
    Priority Queue implementation using heap.
    
    Lower priority numbers = higher priority (min-heap behavior)
    
    Time Complexities:
    - Insert: O(log n)
    - Extract min: O(log n)
    - Peek: O(1)
    - Size: O(1)
    """
    
    def __init__(self):
        self._heap: List[PriorityItem] = []
        self._size = 0
    
    def insert(self, item: Any, priority: int) -> None:
        """Insert item with given priority."""
        priority_item = PriorityItem(priority, item)
        heapq.heappush(self._heap, priority_item)
        self._size += 1
    
    def extract_min(self) -> Tuple[Any, int]:
        """Remove and return item with highest priority (lowest number)."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority_item = heapq.heappop(self._heap)
        self._size -= 1
        return priority_item.item, priority_item.priority
    
    def peek_min(self) -> Tuple[Any, int]:
        """Return item with highest priority without removing it."""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        
        priority_item = self._heap[0]
        return priority_item.item, priority_item.priority
    
    def is_empty(self) -> bool:
        """Check if priority queue is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return number of items in priority queue."""
        return self._size
    
    def change_priority(self, item: Any, new_priority: int) -> bool:
        """Change priority of an existing item."""
        # Find and remove old item
        for i, priority_item in enumerate(self._heap):
            if priority_item.item == item:
                # Remove item
                self._heap[i] = self._heap[-1]
                self._heap.pop()
                self._size -= 1
                heapq.heapify(self._heap)
                
                # Insert with new priority
                self.insert(item, new_priority)
                return True
        return False

# ==============================================================================
# DEQUE (DOUBLE-ENDED QUEUE)
# ==============================================================================

class Node(Generic[T]):
    """Node for doubly linked list implementation."""
    def __init__(self, data: T):
        self.data = data
        self.next: Optional['Node[T]'] = None
        self.prev: Optional['Node[T]'] = None

class Deque(Generic[T]):
    """
    Double-ended queue implementation using doubly linked list.
    
    Time Complexities:
    - Add front/rear: O(1)
    - Remove front/rear: O(1)
    - Peek front/rear: O(1)
    - Size: O(1)
    """
    
    def __init__(self):
        self._head: Optional[Node[T]] = None
        self._tail: Optional[Node[T]] = None
        self._size = 0
    
    def add_front(self, item: T) -> None:
        """Add item to front of deque."""
        new_node = Node(item)
        
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        
        self._size += 1
    
    def add_rear(self, item: T) -> None:
        """Add item to rear of deque."""
        new_node = Node(item)
        
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            new_node.prev = self._tail
            self._tail = new_node
        
        self._size += 1
    
    def remove_front(self) -> T:
        """Remove and return item from front of deque."""
        if self.is_empty():
            raise IndexError("Deque is empty")
        
        item = self._head.data
        
        if self._size == 1:
            self._head = self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None
        
        self._size -= 1
        return item
    
    def remove_rear(self) -> T:
        """Remove and return item from rear of deque."""
        if self.is_empty():
            raise IndexError("Deque is empty")
        
        item = self._tail.data
        
        if self._size == 1:
            self._head = self._tail = None
        else:
            self._tail = self._tail.prev
            self._tail.next = None
        
        self._size -= 1
        return item
    
    def peek_front(self) -> T:
        """Return front item without removing it."""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._head.data
    
    def peek_rear(self) -> T:
        """Return rear item without removing it."""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._tail.data
    
    def is_empty(self) -> bool:
        """Check if deque is empty."""
        return self._size == 0
    
    def size(self) -> int:
        """Return number of items in deque."""
        return self._size
    
    def to_list(self) -> List[T]:
        """Convert deque to list from front to rear."""
        items = []
        current = self._head
        while current:
            items.append(current.data)
            current = current.next
        return items

# ==============================================================================
# PRACTICAL APPLICATIONS AND EXAMPLES
# ==============================================================================

def demonstrate_queue_applications():
    """Demonstrate practical applications of different queue types."""
    
    print("Queue Applications Demonstration")
    print("=" * 40)
    
    # 1. Simple Queue - Task Processing
    print("\n1. Simple Queue - Task Processing System:")
    task_queue = SimpleQueue()
    
    tasks = ["Process payment", "Send email", "Generate report", "Update database"]
    for task in tasks:
        task_queue.enqueue(task)
        print(f"   Added task: {task}")
    
    print(f"   Queue size: {task_queue.size()}")
    print(f"   Next task: {task_queue.peek()}")
    
    # Process tasks
    while not task_queue.is_empty():
        task = task_queue.dequeue()
        print(f"   Processing: {task}")
    
    # 2. Circular Queue - Buffer System
    print("\n2. Circular Queue - Circular Buffer:")
    buffer = CircularQueue(capacity=5)
    
    # Fill buffer
    for i in range(5):
        buffer.enqueue(f"Data_{i}")
    
    print(f"   Buffer contents: {buffer.display()}")
    print(f"   Buffer is full: {buffer.is_full()}")
    
    # Replace old data with new data
    try:
        buffer.enqueue("New_Data")  # This will raise exception
    except OverflowError as e:
        print(f"   {e}")
    
    # Remove some data and add new
    old_data = buffer.dequeue()
    buffer.enqueue("New_Data")
    print(f"   Removed: {old_data}")
    print(f"   New buffer: {buffer.display()}")
    
    # 3. Priority Queue - Hospital Emergency System
    print("\n3. Priority Queue - Hospital Emergency System:")
    emergency_queue = PriorityQueue()
    
    # Add patients with priority (1=Critical, 2=Urgent, 3=Normal)
    patients = [
        ("John Doe", 3),      # Normal
        ("Jane Smith", 1),    # Critical
        ("Bob Johnson", 2),   # Urgent
        ("Alice Brown", 1),   # Critical
        ("Charlie Davis", 3)  # Normal
    ]
    
    for patient, priority in patients:
        emergency_queue.insert(patient, priority)
        priority_name = {1: "Critical", 2: "Urgent", 3: "Normal"}[priority]
        print(f"   Added patient: {patient} ({priority_name})")
    
    print(f"\n   Processing patients by priority:")
    while not emergency_queue.is_empty():
        patient, priority = emergency_queue.extract_min()
        priority_name = {1: "Critical", 2: "Urgent", 3: "Normal"}[priority]
        print(f"   Treating: {patient} ({priority_name})")
    
    # 4. Deque - Undo/Redo System
    print("\n4. Deque - Undo/Redo Operations:")
    operation_history = Deque()
    
    operations = ["Create file", "Add text", "Format text", "Save file"]
    for op in operations:
        operation_history.add_rear(op)
        print(f"   Performed: {op}")
    
    print(f"   History: {operation_history.to_list()}")
    
    # Undo operations
    print("\n   Undoing operations:")
    for _ in range(2):
        if not operation_history.is_empty():
            undone = operation_history.remove_rear()
            print(f"   Undid: {undone}")
    
    print(f"   Remaining history: {operation_history.to_list()}")

def benchmark_queue_implementations():
    """Benchmark different queue implementations."""
    import time
    
    print("\nQueue Performance Benchmark")
    print("=" * 40)
    
    # Test data
    test_size = 10000
    
    # Test SimpleQueue
    start_time = time.time()
    sq = SimpleQueue()
    for i in range(test_size):
        sq.enqueue(i)
    
    for _ in range(test_size):
        sq.dequeue()
    
    simple_time = time.time() - start_time
    
    # Test EfficientQueue
    start_time = time.time()
    eq = EfficientQueue()
    for i in range(test_size):
        eq.enqueue(i)
    
    for _ in range(test_size):
        eq.dequeue()
    
    efficient_time = time.time() - start_time
    
    # Test Python's collections.deque
    start_time = time.time()
    dq = collections_deque()
    for i in range(test_size):
        dq.append(i)
    
    for _ in range(test_size):
        dq.popleft()
    
    deque_time = time.time() - start_time
    
    print(f"Performance Results ({test_size} operations):")
    print(f"  SimpleQueue:     {simple_time:.6f} seconds")
    print(f"  EfficientQueue:  {efficient_time:.6f} seconds")
    print(f"  collections.deque: {deque_time:.6f} seconds")
    
    print(f"\nSpeedup over SimpleQueue:")
    print(f"  EfficientQueue:  {simple_time/efficient_time:.2f}x faster")
    print(f"  collections.deque: {simple_time/deque_time:.2f}x faster")

def main():
    """Main demonstration function."""
    print("Comprehensive Queue Implementations")
    print("=" * 50)
    
    # Run demonstrations
    demonstrate_queue_applications()
    benchmark_queue_implementations()
    
    print("\n" + "=" * 50)
    print("Key Takeaways:")
    print("- Choose queue type based on use case:")
    print("  * Simple Queue: Basic FIFO operations")
    print("  * Circular Queue: Fixed-size buffers")
    print("  * Priority Queue: Importance-based processing")
    print("  * Deque: Front and rear operations")
    print("- Consider performance implications")
    print("- Use Python's collections.deque for production code")
    print("- Understand time complexities for different operations")

if __name__ == "__main__":
    main()
