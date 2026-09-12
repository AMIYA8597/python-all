"""
## A. Concept Name
Lock-Free Structures

## B. Learning Objectives
1. Understand the concept of Non-blocking algorithms.
2. Learn about Compare-And-Swap (CAS) operations.
3. Comprehend the limitations of pure Python regarding true lock-free structures.

## C. Concept Explanation
Lock-free data structures allow concurrent access without using mutual exclusion (locks/mutexes).
They typically rely on atomic operations like Compare-And-Swap (CAS) provided by the hardware.
In standard CPython, the Global Interpreter Lock (GIL) serializes thread execution, meaning true
lock-free multi-threading at the CPU level isn't fully achievable purely in Python without C extensions.
However, we can simulate the concept using abstractions.

## D. Performance Analysis
- Avoids deadlocks and priority inversion.
- Can suffer from high contention leading to repeated retries.

## E. Implementation Details
The implementation provides a simulated CAS and a lock-free stack using this CAS to demonstrate the concept of retry-loops common in lock-free algorithms.

## F. Real-World Applications
- High-concurrency low-latency systems.
- Operating system kernels and drivers.
- Real-time trading engines.

## X. Project Connection
These structures can be integrated into high-throughput asynchronous pipelines where minimizing lock contention is crucial for overall performance.
"""

import threading
import time
from typing import Any

class SimulatedCAS:
    """Simulates a Compare-And-Swap atomic operation."""
    def __init__(self, value: Any):
        self.value = value
        self.lock = threading.Lock() # Required to simulate atomicity in Python

    def compare_and_swap(self, expected: Any, new: Any) -> bool:
        with self.lock:
            if self.value == expected:
                self.value = new
                return True
            return False

class LockFreeStackSimulated:
    """
    Advanced Implementation: Simulated Lock-Free Stack using CAS.
    Demonstrates the retry-loop concept common in lock-free algorithms.
    """
    class Node:
        def __init__(self, data: Any):
            self.data = data
            self.next = None

    def __init__(self):
        self.head = SimulatedCAS(None)

    def push(self, data: Any) -> None:
        new_node = self.Node(data)
        while True:
            current_head = self.head.value
            new_node.next = current_head
            if self.head.compare_and_swap(current_head, new_node):
                break
            # simulated backoff could go here

    def pop(self) -> Any:
        while True:
            current_head = self.head.value
            if current_head is None:
                return None
            next_node = current_head.next
            if self.head.compare_and_swap(current_head, next_node):
                return current_head.data

def interview_challenge_read_write_lock():
    """
    Interview Challenge: Implement a read-write lock mechanism.
    Allows multiple readers or one writer, ensuring no read/write or write/write overlaps.
    (Conceptual simulation using basic locks).
    """
    class RWLock:
        def __init__(self):
            self.readers = 0
            self.read_lock = threading.Lock()
            self.write_lock = threading.Lock()

        def acquire_read(self):
            with self.read_lock:
                self.readers += 1
                if self.readers == 1:
                    self.write_lock.acquire()

        def release_read(self):
            with self.read_lock:
                self.readers -= 1
                if self.readers == 0:
                    self.write_lock.release()

        def acquire_write(self):
            self.write_lock.acquire()

        def release_write(self):
            self.write_lock.release()

    return RWLock()

def run_tests() -> None:
    print("Testing SimulatedCAS...")
    cas = SimulatedCAS(10)
    assert cas.compare_and_swap(10, 20) == True
    assert cas.value == 20
    assert cas.compare_and_swap(10, 30) == False

    print("Testing LockFreeStackSimulated...")
    lfs = LockFreeStackSimulated()
    def worker_push():
        for i in range(5): lfs.push(i)
    
    t1 = threading.Thread(target=worker_push)
    t2 = threading.Thread(target=worker_push)
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    count = 0
    while lfs.pop() is not None:
        count += 1
    assert count == 10

    print("Testing Interview Challenge...")
    rw = interview_challenge_read_write_lock()
    rw.acquire_read()
    rw.acquire_read() # multiple readers allowed
    rw.release_read()
    rw.release_read()
    rw.acquire_write()
    rw.release_write()

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
