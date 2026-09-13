"""
# ==============================================================================
# LABORATORY: QUEUES (FIFO)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Queues follow the First-In, First-Out (FIFO) principle (like a line at a store).
# They are the core data structure for Breadth-First Search (BFS), task scheduling, 
# message brokering (RabbitMQ/Kafka concepts), and thread-pool execution.
# Using the wrong data structure for a Queue in Python guarantees performance failure.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why `list.pop(0)` is an O(N) disaster.
# - Implement a highly performant Queue using `collections.deque`.
# - Differentiate between `collections.deque` and `queue.Queue`.
# - Solve a classic FAANG interview problem: Breadth-First Search (BFS).
#
# ==============================================================================
"""

import timeit
from collections import deque
from queue import Queue as ThreadSafeQueue

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DISASTER OF LIST QUEUES
# ==============================================================================
def demonstrate_list_trap():
    """
    A Python `list` is a contiguous array. Removing the 0th element leaves a hole.
    Python must loop through all N-1 remaining elements and copy them one slot 
    to the left. This makes popping an O(N) operation.
    """
    section_header("The list.pop(0) Disaster")
    
    N = 100_000
    
    def bad_queue():
        q = list(range(N))
        while q:
            q.pop(0) # O(N)
            
    def good_queue():
        q = deque(range(N))
        while q:
            q.popleft() # O(1)
            
    print(f"Emptying a queue of {N:,} elements...")
    
    bad_time = timeit.timeit(bad_queue, number=1)
    print(f"Using a List (O(N^2) total):  {bad_time:.4f} seconds")
    
    good_time = timeit.timeit(good_queue, number=1)
    print(f"Using a Deque (O(N) total):   {good_time:.4f} seconds")
    print(f"-> Deque is {bad_time/good_time:,.0f}x faster!")


# ==============================================================================
# 4. IMPLEMENTING A SAFE QUEUE (DEQUE)
# ==============================================================================
class SafeQueue:
    """
    A custom wrapper around deque to prevent accidental O(N) operations 
    (like inserting into the middle).
    """
    def __init__(self):
        # A deque is a doubly-linked list in C.
        self._data = deque()
        
    def enqueue(self, item) -> None:
        """Add to the back of the queue (O(1))."""
        self._data.append(item)
        
    def dequeue(self):
        """Remove from the front of the queue (O(1))."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()
        
    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]
        
    def is_empty(self) -> bool:
        return len(self._data) == 0

def demonstrate_safe_queue():
    section_header("Safe Queue Implementation")
    
    q = SafeQueue()
    q.enqueue("Alice")
    q.enqueue("Bob")
    q.enqueue("Charlie")
    
    print(f"Next in line (peek): {q.peek()}")
    
    print("\nProcessing line:")
    while not q.is_empty():
        print(f" Processing: {q.dequeue()}")


# ==============================================================================
# 5. CLASSIC INTERVIEW PROBLEM: BREADTH-FIRST SEARCH (BFS)
# ==============================================================================
# We use a Queue to explore a graph level by level.

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [], 'E': [], 'F': []
}

def bfs_traversal(start_node: str):
    """
    BFS explores the graph horizontally (level by level) rather than vertically.
    It guarantees finding the shortest path in an unweighted graph.
    """
    visited = set()
    queue = deque([start_node])
    
    while queue:
        # 1. Pop from the front
        node = queue.popleft()
        
        if node not in visited:
            print(f" Visited: {node}")
            # 2. Mark as visited
            visited.add(node)
            
            # 3. Add all unvisited neighbors to the back of the queue
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

def demonstrate_bfs():
    section_header("Breadth-First Search (BFS) using a Queue")
    print("Graph Structure: A -> [B, C], B -> [D, E], C -> [F]")
    print("Expected BFS Order: A (Level 0) -> B, C (Level 1) -> D, E, F (Level 2)")
    
    print("\nBFS Execution:")
    bfs_traversal('A')


# ==============================================================================
# 6. THREAD-SAFE QUEUES (queue.Queue)
# ==============================================================================
def demonstrate_thread_queue():
    """
    collections.deque is fast, but it is NOT designed for inter-thread communication.
    If you have multiple threads (Producer/Consumer), you must use `queue.Queue`.
    It uses internal Locks (Mutexes) to prevent race conditions.
    """
    section_header("Thread-Safe Queues (queue module)")
    
    q = ThreadSafeQueue(maxsize=3)
    
    print("Putting 3 items into the bounded thread-safe queue...")
    q.put(1)
    q.put(2)
    q.put(3)
    
    print(f"Queue full? {q.full()}")
    
    # If we do q.put(4) here, the thread will BLOCK FOREVER until a consumer 
    # takes an item out, preventing Memory Overflows in Prod.
    print("Getting 1 item out...")
    item = q.get()
    print(f"Got: {item}")
    
    print("To use across async tasks, use `asyncio.Queue`.")
    print("To use across separate OS processes, use `multiprocessing.Queue`.")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `collections.deque` $O(1)$ for popping from the left, while a `list` is $O(N)$?
   Answer: A list is a contiguous array, so removing the front element requires shifting all remaining elements to the left. A deque is a block-based doubly-linked list. Removing the front element just updates a pointer.

2. When traversing a graph, how does a Queue change the search pattern compared to a Stack?
   Answer: A Stack (LIFO) produces Depth-First Search (DFS), diving to the bottom of a branch before backtracking. A Queue (FIFO) produces Breadth-First Search (BFS), exploring all nodes at the current depth (level) before moving deeper.

3. If `deque` is so fast, why would you ever use `queue.Queue`?
   Answer: `deque` is for raw algorithmic data manipulation in a single thread. `queue.Queue` is specifically designed for cross-thread communication. It includes internal Locks to prevent race conditions and supports blocking operations (e.g., waiting for an item to arrive).
"""

if __name__ == "__main__":
    demonstrate_list_trap()
    demonstrate_safe_queue()
    demonstrate_bfs()
    demonstrate_thread_queue()
    print("\n[SUCCESS] Laboratory: Queues Completed.")
