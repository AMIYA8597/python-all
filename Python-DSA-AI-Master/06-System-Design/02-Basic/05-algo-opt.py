"""
Algorithm Optimization in Python

# Learning Objectives
1. Understand the importance of choosing the right data structures.
2. Apply memoization and caching to reduce redundant computations.
3. Optimize loops and conditionals for better execution time.
4. Grasp the time-space tradeoff in algorithm design.

# Concept Explanation
Algorithm optimization is the process of modifying an algorithm to make it execute faster 
or use less memory. In System Design, inefficient algorithms at the component level can 
bottleneck the entire system. Key techniques include:
- Using Hash Maps (Dictionaries) for O(1) lookups instead of O(N) list searches.
- Caching/Memoization (e.g., functools.lru_cache) to avoid repeating expensive function calls.
- Loop unrolling, avoiding computations inside loops, and using list comprehensions.
- Utilizing built-in functions which are highly optimized in C (like sum(), max()).

# Industry Use Cases
- High-frequency trading systems where microseconds matter.
- Large-scale data processing pipelines (ETL).
- Web backend services minimizing latency for API responses.
"""

import time
from typing import List, Dict, Set, Any
from functools import lru_cache

# ==========================================
# 1. Basic vs Optimized Lookups
# ==========================================
def find_duplicates_basic(arr: List[int]) -> List[int]:
    """Basic O(N^2) time complexity approach."""
    duplicates = []
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j] and arr[i] not in duplicates:
                duplicates.append(arr[i])
    return duplicates

def find_duplicates_optimized(arr: List[int]) -> List[int]:
    """Optimized O(N) time and O(N) space complexity approach using sets."""
    seen: Set[int] = set()
    duplicates: Set[int] = set()
    for num in arr:
        if num in seen:
            duplicates.add(num)
        seen.add(num)
    return list(duplicates)

# ==========================================
# 2. Caching / Memoization
# ==========================================
def fibonacci_basic(n: int) -> int:
    """Exponential time complexity O(2^N)."""
    if n <= 1:
        return n
    return fibonacci_basic(n-1) + fibonacci_basic(n-2)

@lru_cache(maxsize=None)
def fibonacci_optimized(n: int) -> int:
    """Linear time complexity O(N) using memoization."""
    if n <= 1:
        return n
    return fibonacci_optimized(n-1) + fibonacci_optimized(n-2)

# ==========================================
# 3. Professional Implementation: Rate Limiter Optimization
# ==========================================
class BasicRateLimiter:
    """A naive rate limiter using lists. Slow removal of old timestamps."""
    def __init__(self, time_window_sec: int, max_requests: int):
        self.time_window = time_window_sec
        self.max_requests = max_requests
        self.requests: Dict[str, List[float]] = {}
        
    def is_allowed(self, client_id: str) -> bool:
        current_time = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = []
            
        # Clean up old requests (O(N) operation)
        self.requests[client_id] = [t for t in self.requests[client_id] if current_time - t <= self.time_window]
        
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(current_time)
            return True
        return False

from collections import deque

class OptimizedRateLimiter:
    """An optimized rate limiter using Deque for O(1) removals from the left."""
    def __init__(self, time_window_sec: int, max_requests: int):
        self.time_window = time_window_sec
        self.max_requests = max_requests
        self.requests: Dict[str, deque[float]] = {}
        
    def is_allowed(self, client_id: str) -> bool:
        current_time = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = deque()
            
        q = self.requests[client_id]
        # Clean up old requests efficiently (Amortized O(1))
        while q and current_time - q[0] > self.time_window:
            q.popleft()
            
        if len(q) < self.max_requests:
            q.append(current_time)
            return True
        return False

# ==========================================
# 4. Complexity Analysis
# ==========================================
"""
Basic Rate Limiter:
- Time: O(N) where N is the number of requests in the window, due to list comprehension rebuilding.
- Space: O(N)

Optimized Rate Limiter:
- Time: O(1) amortized. Deque operations (append/popleft) are O(1).
- Space: O(N) for storing timestamps.

# Interview Challenge
Q: How would you optimize the Rate Limiter if memory was highly constrained (e.g., Millions of users)?
A: Instead of storing individual timestamps (Sliding Window Log), we could use the Token Bucket or 
   Fixed Window Counter algorithms. Fixed window only requires storing an integer counter and a 
   window timestamp, reducing space from O(N) per user to O(1) per user.
"""

if __name__ == "__main__":
    print("Running Algorithm Optimization Tests...")
    
    # Test Duplicates
    data = [1, 2, 3, 2, 4, 5, 1, 6]
    assert sorted(find_duplicates_basic(data)) == [1, 2]
    assert sorted(find_duplicates_optimized(data)) == [1, 2]
    
    # Test Fibonacci
    assert fibonacci_optimized(10) == 55
    
    # Test Rate Limiter
    rl = OptimizedRateLimiter(time_window_sec=1, max_requests=2)
    assert rl.is_allowed("user1") is True
    assert rl.is_allowed("user1") is True
    assert rl.is_allowed("user1") is False # 3rd request blocked
    
    print("All optimization tests passed!")
