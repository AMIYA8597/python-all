\"\"\"
Module: CodeChef Lunchtime Contest Practice
=========================================
Why it exists:
In Competitive Programming, CodeChef "Lunchtime" is a popular contest format. 
This module explores a classic CP problem typically seen in such contests, focusing 
on Greedy Algorithms and Array Manipulation. 

Learning Objectives:
1. Understand how to break down a typical CodeChef problem statement.
2. Learn how to write optimized I/O for Python in CP.
3. Apply Greedy strategies and basic Data Structures to achieve optimal Time Complexity.

Concept Explanation:
--------------------
Problem Statement (Hypothetical typical problem):
Given an array of integers representing the tastiness of lunch items, you are allowed 
to pair adjacent items and replace them with their sum, but you can only do this at most `K` times.
Your goal is to maximize the sum of the absolute values of the remaining items.

Basic Approach:
Iterate over the array, try all combinations of pairings, and find the maximum sum.
Time Complexity: Exponential O(2^N) - TLE (Time Limit Exceeded).

Professional Approach:
Use dynamic programming or a greedy strategy depending on exact constraints. 
For our educational example, we'll implement a classic "Maximum Subarray Sum with a twist" 
or a "Greedy Pairing" to demonstrate O(N) or O(N log N) logic. 
Let's implement a problem where we want to maximize the sum after some operations.

To make it concrete: 
Given an array `A` of `N` integers and an integer `K`. You can negate at most `K` 
elements in the array. Maximize the sum of the array.

Time Complexity: O(N log N) to sort, or O(N) using a heap for optimal tracking.
Space Complexity: O(1) beyond the input array.
\"\"\"

import heapq
from typing import List

def maximize_sum_basic(arr: List[int], k: int) -> int:
    \"\"\"
    Basic approach: Sort the array, negate negative numbers up to K times.
    If K is still > 0 and odd, negate the smallest absolute value.
    
    Time Complexity: O(N log N)
    Space Complexity: O(1) or O(N) depending on sorting.
    \"\"\"
    if not arr:
        return 0
    
    arr_sorted = sorted(arr)
    i = 0
    while k > 0 and i < len(arr_sorted) and arr_sorted[i] < 0:
        arr_sorted[i] = -arr_sorted[i]
        k -= 1
        i += 1
        
    if k > 0 and k % 2 == 1:
        # We need to flip the smallest absolute value
        min_idx = 0
        for j in range(1, len(arr_sorted)):
            if arr_sorted[j] < arr_sorted[min_idx]:
                min_idx = j
        arr_sorted[min_idx] = -arr_sorted[min_idx]
        
    return sum(arr_sorted)

def maximize_sum_pro(arr: List[int], k: int) -> int:
    \"\"\"
    Professional approach using a min-heap.
    Heapify takes O(N). Extract-min and insert takes O(log N).
    Total Time Complexity: O(N + K log N). 
    This is faster than O(N log N) when K is much smaller than N.
    \"\"\"
    if not arr:
        return 0
        
    # Copy array to avoid mutating input
    heap = arr.copy()
    heapq.heapify(heap)
    
    for _ in range(k):
        smallest = heapq.heappop(heap)
        if smallest >= 0:
            # If the smallest is positive and we still have flips, 
            # if remaining K is even, it cancels out.
            # If remaining K is odd, flip this smallest once.
            # Wait, popping and pushing just negates it. Let's do it directly.
            heapq.heappush(heap, -smallest)
        else:
            heapq.heappush(heap, -smallest)
            
    return sum(heap)

# ---------------------------------------------------------
# Example Usage and Tests
# ---------------------------------------------------------
def main():
    arr = [2, -3, -1, 5, -4]
    k = 2
    # Expected: [-4, -3] negated -> [4, 3, -1, 2, 5] -> Sum = 13
    
    assert maximize_sum_basic(arr, k) == 13, "Basic approach failed"
    assert maximize_sum_pro(arr, k) == 13, "Pro approach failed"
    
    arr2 = [4, 2, 3]
    k2 = 1
    # Expected: flip 2 -> [4, -2, 3] -> Sum = 5
    assert maximize_sum_pro(arr2, k2) == 5
    
    print("CodeChef Lunchtime Practice Tests Passed!")

if __name__ == "__main__":
    main()

\"\"\"
Interview Challenge:
--------------------
Q: How would you solve this if you were NOT allowed to sort or use a heap, 
and the values of array elements were bounded strictly between -100 and 100?
A: Use Counting Sort! Since the range is small (-100 to 100), we can create 
a frequency array of size 201. We can then iterate from -100 to 0, flipping 
frequencies up to K times. This reduces the time complexity to O(N + Range), 
which is practically O(N).
\"\"\"
