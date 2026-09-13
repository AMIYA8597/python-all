"""
System Design: Custom Allocators and Object Pooling in Python
=============================================================

Learning Objectives:
1. Understand the Object Pool design pattern.
2. Learn how to bypass Python's dynamic allocation for high-performance paths.
3. Understand how creating and destroying objects affects performance.
4. Implement a thread-safe Custom Allocator / Object Pool.

Concept Explanation:
--------------------
In performance-critical applications, the constant creation and destruction of objects (like creating thousands of bullet objects in a game every second, or connection objects in a web server) can lead to massive CPU overhead. Python handles allocation dynamically, which asks the OS for memory, and later cleans it up via GC.
A Custom Allocator or Object Pool pre-allocates a set of objects. When a new object is needed, it fetches an unused one from the pool. When the object is "destroyed," it is simply returned to the pool, marked as free, avoiding actual memory deallocation and garbage collection overhead.

Industry Use Cases:
-------------------
- Database Connection Pooling (e.g., SQLAlchemy Pool).
- Game Development (Bullet pools, particle systems).
- High-concurrency network servers (reusing socket handler objects).

Basic Implementation:
---------------------
"""
from typing import List, Optional, Type, TypeVar
import threading
import time

T = TypeVar('T')

class Resource:
    """A generic resource that is expensive to create."""
    def __init__(self):
        # Simulate expensive initialization
        self.state = "CLEAN"
        self.id = id(self)

    def reset(self):
        """Reset the resource to a clean state before reusing."""
        self.state = "CLEAN"

class BasicObjectPool:
    """A simple non-thread-safe object pool."""
    def __init__(self, size: int):
        self._pool: List[Resource] = [Resource() for _ in range(size)]

    def acquire(self) -> Optional[Resource]:
        if not self._pool:
            return None # Or raise an exception, or expand pool
        return self._pool.pop()

    def release(self, resource: Resource):
        resource.reset()
        self._pool.append(resource)


# Professional Implementation
# ---------------------------
# Thread-safe Object Pool with dynamic scaling capabilities.

class Connection:
    """Simulated database connection."""
    def __init__(self, conn_id: int):
        self.conn_id = conn_id
        self.is_active = False

    def reset(self):
        self.is_active = False
        
    def __str__(self):
        return f"Conn({self.conn_id})"

class ThreadSafeAllocator:
    def __init__(self, min_size: int, max_size: int, factory_func):
        self.min_size = min_size
        self.max_size = max_size
        self.factory = factory_func
        
        self.pool: List[Any] = []
        self.lock = threading.Lock()
        
        # Pre-allocate minimum size
        for i in range(min_size):
            self.pool.append(self.factory(i))
            
        self.created_count = min_size

    def acquire(self, timeout: float = 2.0) -> Any:
        start_time = time.time()
        while True:
            with self.lock:
                if self.pool:
                    return self.pool.pop()
                elif self.created_count < self.max_size:
                    # Dynamically expand
                    new_obj = self.factory(self.created_count)
                    self.created_count += 1
                    return new_obj
            
            # Wait for someone to release if pool is empty and max capacity reached
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for resource from pool.")
            time.sleep(0.01)

    def release(self, obj: Any):
        with self.lock:
            obj.reset()
            self.pool.append(obj)

# Complexity Analysis:
# Time Complexity: O(1) to acquire or release an object (list pop/append).
# Space Complexity: O(M) where M is the max_size of the pool, preventing memory spikes.

# Common Mistakes:
# 1. Forgetting to reset object state upon releasing back to the pool. This leads to data leaks between different contexts.
# 2. Memory Leaks: If a user acquires an object but forgets to release it (e.g., due to an exception), the pool depletes. Always use context managers (`with` statement) to handle acquisition and release safely.
# 3. Thread contention: Using a single lock for an extremely high-throughput pool might cause bottlenecks.

# Interview Challenge:
# Q: How can you ensure that an object acquired from the pool is always returned, even if an exception occurs?
# A: Implement a Context Manager. Use the `__enter__` method to acquire the object and `__exit__` to release it. 

if __name__ == "__main__":
    print("Running Custom Allocator Tests...")
    
    # Test Basic Pool
    pool = BasicObjectPool(2)
    obj1 = pool.acquire()
    obj2 = pool.acquire()
    assert pool.acquire() is None, "Pool should be empty."
    pool.release(obj1)
    assert pool.acquire() is not None, "Pool should have 1 object now."

    # Test ThreadSafe Pool
    safe_pool = ThreadSafeAllocator(min_size=2, max_size=3, factory_func=Connection)
    c1 = safe_pool.acquire()
    c2 = safe_pool.acquire()
    c3 = safe_pool.acquire()  # Expanding to max_size
    
    try:
        c4 = safe_pool.acquire(timeout=0.1)  # Should timeout
        assert False, "Should have timed out"
    except TimeoutError:
        pass
        
    safe_pool.release(c2)
    c4 = safe_pool.acquire()
    assert c4 is c2, "Should reuse the released connection"
    
    print("All custom allocator tests passed successfully.")
