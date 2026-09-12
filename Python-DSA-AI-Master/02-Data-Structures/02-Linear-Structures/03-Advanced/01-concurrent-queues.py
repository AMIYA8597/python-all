"""
## A. Concept Name
Concurrent Queues

## B. Real-World Analogy
Think of a busy coffee shop where multiple cashiers (producers) are taking orders and placing them on a single counter, while multiple baristas (consumers) are picking up those orders to make the drinks. A concurrent queue ensures that no two baristas pick up the same order and that cashiers don't overwrite each other's tickets.

## C. Visual Representation
Producer 1 \
            \
             -> [ Enqueue -> Lock -> Queue -> Lock -> Dequeue ] -> Consumer 1
            /
Producer 2 /

## D. Core Components
1. **Queue Structure**: The underlying data container (like a list or linked list).
2. **Lock/Mutex**: Ensures only one thread modifies the queue at a time.
3. **Condition Variables (optional)**: Used for blocking operations (e.g., waiting for the queue to have items).

## E. Time & Space Complexity
- **Time**: O(1) for enqueue/dequeue (excluding thread contention overhead).
- **Space**: O(N) where N is the maximum number of items in the queue.

## F. Step-by-Step Walkthrough
1. A thread attempts to enqueue an item.
2. It acquires the lock.
3. It adds the item to the underlying structure.
4. It releases the lock.
5. Another thread acquires the lock to dequeue and safely removes an item.

## G. Edge Cases & Constraints
- Empty queue when dequeuing.
- Full queue when enqueuing (if bounded).
- High contention causing thread starvation.

## H. Common Pitfalls
- Forgetting to lock around both checking for emptiness and the actual dequeue operation (race conditions).
- Deadlocks if multiple locks are used improperly.

## I. Interview Patterns
- Producer-Consumer problem.
- Rate limiting.
- Thread pool task queues.

## J. Code Implementation Options
- Basic standard list with `threading.Lock`.
- Python's built-in `queue.Queue`.
- `collections.deque` with locks.

## K. Basic Implementation (Code level mapping)
`LockedQueue` demonstrates how to manually manage a standard Python list using `threading.Lock`.

## L. Intermediate/Advanced (Code level mapping)
`ThreadingQueueWrapper` uses the thread-safe `queue.Queue` from Python's standard library.

## M. Real-World Use Cases
- Web server request handling.
- Background task processing (e.g., Celery).
- Log message aggregation.

## N. Quick Reference
- `q = queue.Queue()`: Thread-safe FIFO queue.
- `q.put(item)`: Enqueue (blocks if full).
- `q.get()`: Dequeue (blocks if empty).

## O. Practice Exercises
- Implement a priority concurrent queue.
- Add timeouts to the custom `LockedQueue`.

## P. Assessment Questions
1. Why is a standard list not thread-safe for pop(0)?
2. What is the purpose of a poison pill in a producer-consumer setup?

## Q. Debugging Tips
- Use `logging` instead of `print` to avoid garbled output in multi-threaded debugging.
- Beware of silent deadlocks.

## R. System Design Context
Concurrent queues are the building blocks for message brokers like RabbitMQ or Kafka in distributed systems.

## S. Anti-Patterns
- Polling (busy-waiting) an empty queue instead of using blocking mechanisms or condition variables.

## T. Language Specifics (Python)
- Python's Global Interpreter Lock (GIL) means threads won't execute Python bytecode in parallel, but thread synchronization is still required for non-atomic operations.

## U. Performance Tuning
- Use lock-free queues for ultra-high performance (mostly in C/C++, harder in pure Python).
- Batch enqueues/dequeues to reduce lock acquisition overhead.

## V. Related Concepts
- Semaphores.
- Thread Pools.
- Asyncio (event loop-based concurrency).

## W. AI / ML Applications
- Data loading pipelines where multiple threads fetch/preprocess images and put them in a queue for the GPU to consume.

## X. Project Connection
Applying thread-safe queues allows building robust, multi-threaded pipelines, critical for modern scalable architectures and parallel data processing.
"""

import threading
import queue
import time
from typing import Any

class LockedQueue:
    """Basic Implementation: Thread-safe queue using a standard list and a lock."""
    def __init__(self) -> None:
        self.items: list = []
        self.lock = threading.Lock()

    def enqueue(self, item: Any) -> None:
        with self.lock:
            self.items.append(item)

    def dequeue(self) -> Any:
        with self.lock:
            if not self.items:
                return None
            return self.items.pop(0)

class ThreadingQueueWrapper:
    """Intermediate/Advanced Implementation: Using Python's queue.Queue."""
    def __init__(self, maxsize: int = 0) -> None:
        self.q: queue.Queue = queue.Queue(maxsize=maxsize)

    def put(self, item: Any) -> None:
        self.q.put(item)

    def get(self) -> Any:
        return self.q.get()

    def task_done(self) -> None:
        self.q.task_done()

    def join(self) -> None:
        self.q.join()

def interview_challenge_producer_consumer() -> int:
    """
    Interview Challenge: Producer-Consumer Problem
    Implement a simple producer-consumer model using queue.Queue to demonstrate thread-safety.
    Returns the total number of processed items.
    """
    q = queue.Queue()
    processed_count = 0
    lock = threading.Lock()

    def producer():
        for i in range(5):
            q.put(i)
            time.sleep(0.01)

    def consumer():
        nonlocal processed_count
        while True:
            item = q.get()
            if item is None:
                break
            with lock:
                processed_count += 1
            q.task_done()

    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    
    t1.start()
    t2.start()
    
    t1.join()
    q.put(None) # poison pill
    t2.join()
    
    return processed_count

def run_tests() -> None:
    print("Testing LockedQueue...")
    lq = LockedQueue()
    def worker1(q): q.enqueue(1)
    def worker2(q): q.enqueue(2)
    t1 = threading.Thread(target=worker1, args=(lq,))
    t2 = threading.Thread(target=worker2, args=(lq,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    assert len(lq.items) == 2

    print("Testing Interview Challenge...")
    assert interview_challenge_producer_consumer() == 5
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
