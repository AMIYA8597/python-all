"""
# ==============================================================================
# LABORATORY: DEQUES (DOUBLE-ENDED QUEUES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Standard Python lists are dynamic arrays, making operations at the end O(1) 
# but operations at the front O(N). If you need to add or remove data from BOTH 
# ends of a collection efficiently, you MUST use `collections.deque`. 
# Under the hood in CPython, a deque is implemented as a doubly-linked list of 
# fixed-length memory blocks. It is the absolute optimal choice for Queues and 
# Sliding Window algorithms.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the C-level block architecture of a deque.
# - Prove the O(1) vs O(N) performance difference for left-side operations.
# - Use the `maxlen` parameter to create an automatic Ring Buffer.
# - Solve a classic FAANG interview problem: Sliding Window Maximum.
#
# ==============================================================================
"""

import timeit
from collections import deque
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DEQUE MECHANICS AND RING BUFFERS
# ==============================================================================
def demonstrate_deque_mechanics():
    """
    Deques support O(1) append and pop from BOTH ends.
    They also support a `maxlen` argument. If the deque is full, appending 
    to one side automatically pops from the opposite side, creating a perfect 
    Ring Buffer (useful for keeping the "last 10 log messages").
    """
    section_header("Deque Mechanics and maxlen")
    
    dq = deque(["B", "C"])
    print(f"Initial: {dq}")
    
    # O(1) operations on both ends
    dq.append("D")
    dq.appendleft("A")
    print(f"After appends: {dq}")
    
    popped_right = dq.pop()
    popped_left = dq.popleft()
    print(f"Popped Right: {popped_right}, Popped Left: {popped_left}")
    print(f"Final: {dq}")
    
    print("\n--- Automatic Ring Buffer (maxlen) ---")
    # Creates a deque that can hold a MAXIMUM of 3 items
    history = deque(maxlen=3)
    
    for i in range(1, 6):
        history.append(f"Event-{i}")
        print(f"Added Event-{i}, Buffer state: {history}")
        
    print("Notice how Event-1 and Event-2 were automatically pushed out!")


# ==============================================================================
# 4. PERFORMANCE COMPARISON: DEQUE VS LIST
# ==============================================================================
def demonstrate_performance():
    """
    We prove that insert(0, x) on a list is catastrophic compared to appendleft(x)
    on a deque.
    """
    section_header("Performance: Deque vs List for Left Operations")
    
    N = 50_000
    
    def bad_list_insert():
        lst = []
        for i in range(N):
            # O(N) operation inside an O(N) loop = O(N^2) time
            lst.insert(0, i) 
            
    def good_deque_insert():
        dq = deque()
        for i in range(N):
            # O(1) operation inside an O(N) loop = O(N) time
            dq.appendleft(i)
            
    print(f"Inserting {N:,} elements at index 0...")
    
    t_list = timeit.timeit(bad_list_insert, number=1)
    t_deque = timeit.timeit(good_deque_insert, number=1)
    
    print(f"List insert(0) time:  {t_list:.5f}s")
    print(f"Deque appendleft time:{t_deque:.5f}s")
    print(f"-> Deque is {t_list/t_deque:,.0f}x faster!")


# ==============================================================================
# 5. CLASSIC INTERVIEW PROBLEM: SLIDING WINDOW MAXIMUM
# ==============================================================================
def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    """
    LeetCode #239: Sliding Window Maximum (Hard)
    Time Complexity: O(N)
    Space Complexity: O(K)
    
    Problem: Given an array `nums` and a sliding window of size `k`, return the 
    maximum element in the window as it slides from left to right.
    
    Naive approach: Find max() of every window slice -> O(N * K) time (Too slow!).
    Optimal approach: Use a Monotonic Deque. We store INDICES in the deque. 
    We maintain the deque so that the values it points to are strictly DECREASING.
    The largest value's index is always at deque[0].
    """
    if not nums or k == 0:
        return []
        
    result = []
    dq = deque() # Will store INDICES
    
    for i in range(len(nums)):
        # 1. Remove indices that are no longer in the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()
            
        # 2. Remove indices of smaller elements from the back of the deque.
        # They are useless because they are smaller than the current element `nums[i]`
        # and they arrived earlier, so they will expire earlier anyway.
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
            
        # 3. Add the current element's index
        dq.append(i)
        
        # 4. If our window has reached size k, the max is at the front of the deque
        if i >= k - 1:
            result.append(nums[dq[0]])
            
    return result

def demonstrate_sliding_window():
    section_header("Algorithm: Sliding Window Maximum (Monotonic Deque)")
    
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    
    print(f"Array: {nums}")
    print(f"Window size (K): {k}")
    
    result = maxSlidingWindow(nums, k)
    
    print(f"Max Sliding Window Result: {result}")
    print("Expected: [3, 3, 5, 5, 6, 7]")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `deque` not O(1) for arbitrary index access (e.g., `dq[50]`)?
   Answer: Because under the hood, a deque is a linked list of memory blocks. It is not a single contiguous array. To find the 50th item, it must traverse the pointers from the closest end. Therefore, index access is technically O(N) (bounded by N/2).

2. How do you implement a ring buffer (a queue that automatically discards the oldest items when full) in Python?
   Answer: Instantiate a deque with the `maxlen` parameter: `q = deque(maxlen=100)`. When you append the 101st item, it automatically pops the oldest item in O(1) time.

3. What is a Monotonic Deque?
   Answer: A deque whose elements are strictly increasing or strictly decreasing. It is maintained by popping elements from the back of the deque before inserting a new element that would break the monotonicity. It is heavily used in Sliding Window algorithms to find local maximums/minimums in O(N) time.
"""

if __name__ == "__main__":
    demonstrate_deque_mechanics()
    demonstrate_performance()
    demonstrate_sliding_window()
    print("\n[SUCCESS] Laboratory: Deques Completed.")
