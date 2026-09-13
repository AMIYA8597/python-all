"""
# ==============================================================================
# LABORATORY: CIRCULAR QUEUES (RING BUFFERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Standard arrays waste space when used as queues. If you enqueue and dequeue 
# repeatedly, the front of the array becomes empty and useless unless you shift 
# all elements (O(N)). Circular Queues (Ring Buffers) solve this by wrapping the 
# tail pointer back to the front using the modulo operator (%). 
# They are heavily used in OS network packet buffers, audio streaming, and 
# high-frequency logging systems where memory is fixed and pre-allocated.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Modulo Operator (%) for wrapping indices.
# - Design an Array-based Circular Queue in O(1) time.
# - Solve a classic FAANG interview problem (LeetCode #622).
#
# ==============================================================================
"""

from typing import Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CIRCULAR QUEUE IMPLEMENTATION
# ==============================================================================
class MyCircularQueue:
    """
    LeetCode #622: Design Circular Queue
    A fixed-size array-based queue.
    """
    def __init__(self, k: int):
        self.capacity = k
        # We pre-allocate a fixed-size array
        self.queue = [None] * k 
        
        self.head = 0
        self.tail = -1
        self.size = 0

    def enQueue(self, value: int) -> bool:
        """Adds an item to the rear of the queue. Returns True if successful."""
        if self.isFull():
            return False
            
        # The magic of the Ring Buffer: Modulo wrapping
        self.tail = (self.tail + 1) % self.capacity
        self.queue[self.tail] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        """Deletes an item from the front of the queue. Returns True if successful."""
        if self.isEmpty():
            return False
            
        # Clear the old data (optional, but good for garbage collection)
        self.queue[self.head] = None 
        
        # Advance the head pointer with modulo wrapping
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        
        # Reset pointers if empty (keeps things clean)
        if self.isEmpty():
            self.head = 0
            self.tail = -1
            
        return True

    def Front(self) -> int:
        """Gets the front item."""
        if self.isEmpty():
            return -1
        return self.queue[self.head]

    def Rear(self) -> int:
        """Gets the last item."""
        if self.isEmpty():
            return -1
        return self.queue[self.tail]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
        
    def display(self) -> None:
        """Visualizer for the internal fixed array."""
        print(f"  Internal Array: {self.queue} | Head: {self.head} | Tail: {self.tail} | Size: {self.size}")


def demonstrate_circular_queue():
    section_header("Circular Queue Execution")
    
    cq = MyCircularQueue(3) # Capacity is 3
    
    print("Enqueuing 1, 2, 3:")
    print(f"enQueue(1): {cq.enQueue(1)}")
    print(f"enQueue(2): {cq.enQueue(2)}")
    print(f"enQueue(3): {cq.enQueue(3)}")
    cq.display()
    
    print("\nAttempting to enqueue 4 when full:")
    print(f"enQueue(4): {cq.enQueue(4)} (Queue is full!)")
    
    print("\nDequeuing one item (frees up the front of the array):")
    print(f"deQueue(): {cq.deQueue()}")
    cq.display()
    
    print("\nEnqueuing 4 (This wraps around to index 0!):")
    print(f"enQueue(4): {cq.enQueue(4)}")
    cq.display()
    
    print("\nChecking Front and Rear:")
    print(f"Front: {cq.Front()}")
    print(f"Rear: {cq.Rear()}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why use a Circular Queue (Ring Buffer) instead of a standard list Queue?
   Answer: In a standard list, if you pop from the front, it takes O(N) to shift elements. If you fake it by moving a pointer forward without shifting, the front of the list becomes "dead space", wasting RAM. A Circular Queue wraps the tail pointer back to the beginning of the dead space, achieving O(1) operations with perfectly fixed memory usage.

2. How do you advance a pointer `p` in an array of size `K` so that it wraps around to 0 when it hits `K`?
   Answer: `p = (p + 1) % K`. The modulo operator returns the remainder of division. For example, if K=5 and p=4, `(4 + 1) % 5 = 0`.

3. Where are Circular Queues used in production?
   Answer: Audio/Video streaming buffers, Network packet routers, CPU scheduling queues, and anywhere memory fragmentation cannot be tolerated (e.g., embedded systems).
"""

if __name__ == "__main__":
    demonstrate_circular_queue()
    print("\n[SUCCESS] Laboratory: Circular Queues Completed.")
