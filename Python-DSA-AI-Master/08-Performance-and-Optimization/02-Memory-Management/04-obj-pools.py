"""
Memory Management: Object Pools

Learning Objectives:
1. Understand the Object Pool design pattern.
2. Learn how object pooling avoids repeated allocation/deallocation overhead.
3. Implement a thread-safe object pool.
4. Analyze when to use (and when NOT to use) object pools in Python.

Concept Explanation:
Creating and destroying complex objects frequently can cause memory fragmentation
and trigger the garbage collector. An Object Pool maintains a set of initialized
objects kept ready to use. When an object is needed, it's borrowed from the pool;
when done, it's returned to the pool instead of being destroyed.
"""

import time
from typing import List, Any
import queue

# --- Basic Implementation ---
class ExpensiveObject:
    """An object that takes time to initialize."""
    def __init__(self, obj_id: int):
        self.obj_id = obj_id
        # Simulate expensive initialization
        time.sleep(0.01)
        self.reset()
        
    def reset(self):
        """Reset object state for reuse."""
        self.data = []

class SimpleObjectPool:
    """A basic non-thread-safe object pool."""
    def __init__(self, size: int):
        self._pool: List[ExpensiveObject] = [ExpensiveObject(i) for i in range(size)]
        
    def acquire(self) -> ExpensiveObject:
        if not self._pool:
            raise RuntimeError("Pool is empty!")
        return self._pool.pop()
        
    def release(self, obj: ExpensiveObject) -> None:
        obj.reset()
        self._pool.append(obj)

# --- Intermediate Implementation ---
class ThreadSafeObjectPool:
    """A thread-safe object pool using queue."""
    def __init__(self, size: int):
        self._pool: queue.Queue = queue.Queue(maxsize=size)
        for i in range(size):
            self._pool.put(ExpensiveObject(i))
            
    def acquire(self, timeout: float = 1.0) -> ExpensiveObject:
        return self._pool.get(timeout=timeout)
        
    def release(self, obj: ExpensiveObject) -> None:
        obj.reset()
        self._pool.put(obj)

# --- Advanced Implementation / Performance Analysis ---
def without_pool(iterations: int) -> float:
    start = time.perf_counter()
    for i in range(iterations):
        obj = ExpensiveObject(i)
        obj.data.append("test")
        # Object dies here, GC will eventually clean it
    return time.perf_counter() - start

def with_pool(iterations: int, pool_size: int = 10) -> float:
    pool = SimpleObjectPool(pool_size)
    start = time.perf_counter()
    for _ in range(iterations):
        obj = pool.acquire()
        obj.data.append("test")
        pool.release(obj)
    return time.perf_counter() - start

# --- Edge Cases ---
def demonstrate_edge_cases():
    """Demonstrate pool exhaustion."""
    pool = SimpleObjectPool(2)
    o1 = pool.acquire()
    o2 = pool.acquire()
    try:
        o3 = pool.acquire() # Pool is empty
    except RuntimeError as e:
        print(f"Expected Exception: {e}")

# --- Interview Challenge ---
"""
Challenge: Create a Context Manager for pool acquisition so users don't 
forget to release the object even if an exception occurs.
"""
class PoolResource:
    def __init__(self, pool: ThreadSafeObjectPool):
        self.pool = pool
        self.obj = None
        
    def __enter__(self) -> ExpensiveObject:
        self.obj = self.pool.acquire()
        return self.obj
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.obj:
            self.pool.release(self.obj)

# --- Tests ---
def run_tests():
    pool = ThreadSafeObjectPool(2)
    with PoolResource(pool) as obj:
        assert isinstance(obj, ExpensiveObject)
        obj.data.append("x")
    
    # Assert it was released and reset
    obj2 = pool.acquire()
    assert len(obj2.data) == 0
    pool.release(obj2)
    print("All tests passed.")

if __name__ == '__main__':
    print("--- Performance Analysis: Object Pools ---")
    ITER = 50
    t_nopool = without_pool(ITER)
    t_pool = with_pool(ITER)
    
    print(f"Time Without Pool (allocating {ITER} times): {t_nopool:.4f}s")
    print(f"Time With Pool (reusing objects):            {t_pool:.4f}s")
    
    demonstrate_edge_cases()
    run_tests()
