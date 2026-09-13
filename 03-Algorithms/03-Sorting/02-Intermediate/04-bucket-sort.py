"""
# ==============================================================================
# LABORATORY: BUCKET SORT (DISTRIBUTION SORT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned Counting Sort (for small integers) and Radix Sort (for large integers).
# But what if you have an array of Floating Point numbers? 
# [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
#
# You cannot use Counting Sort because you cannot have an array index of `0.17`!
#
# If the floating point numbers are "Uniformly Distributed" (spread out evenly), 
# you can use "Bucket Sort". 
# 
# We create N empty "Buckets" (arrays). We mathematically map each floating point 
# number into a specific bucket. Since the numbers are evenly distributed, each 
# bucket will only receive 1 or 2 numbers! We quickly run Insertion Sort on each 
# tiny bucket, and then concatenate them all together.
#
# Because sorting 1 or 2 items takes O(1) time, sorting N buckets takes exactly 
# O(N) time! We have achieved Linear Time sorting for Floating Points!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Uniform Distribution.
# - Master the mathematical mapping to a bucket index `int(n * value)`.
# - Implement Bucket Sort using Insertion Sort as the subroutine.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BUCKET SORT IMPLEMENTATION
# ==============================================================================
def insertion_sort_for_bucket(arr: List[float]) -> None:
    """
    Standard Insertion Sort. 
    It is extremely fast for tiny arrays (size < 10).
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def bucket_sort(arr: List[float]) -> List[float]:
    """
    Sorts an array of floating point numbers in the range [0.0, 1.0).
    Time Complexity: O(N) Average. O(N^2) Worst case.
    Space Complexity: O(N) for the buckets.
    """
    if not arr: return []
    
    n = len(arr)
    
    # 1. Create N empty buckets
    # Note: We create a list of lists. Do NOT do `[[]] * n` as it creates references 
    # to the exact same list in memory!
    buckets: List[List[float]] = [[] for _ in range(n)]
    
    # 2. Scatter the numbers into the buckets (O(N) Time)
    for value in arr:
        # THE MAPPING FUNCTION
        # If value is 0.78, and we have 10 buckets... 0.78 * 10 = 7.8
        # int(7.8) is 7. It belongs in Bucket 7!
        # If value is 0.17, 0.17 * 10 = 1.7. It belongs in Bucket 1!
        
        # Edge case: If the value is exactly 1.0 (the max possible bound), 
        # it would map to index 10, causing an OutOfBounds error. Cap it at N-1.
        index = int(n * value)
        if index == n:
            index -= 1
            
        buckets[index].append(value)
        
    print("\nScatter Phase:")
    for i in range(n):
        if buckets[i]:
            print(f" Bucket {i}: {buckets[i]}")
            
    # 3. Sort each individual bucket using Insertion Sort (Average O(N) total)
    for i in range(n):
        insertion_sort_for_bucket(buckets[i])
        
    # 4. Gather the sorted buckets back into a single array (O(N) Time)
    sorted_arr = []
    for i in range(n):
        sorted_arr.extend(buckets[i])
        
    return sorted_arr

def demonstrate_bucket_sort():
    section_header("Algorithm: Bucket Sort")
    
    arr = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print(f"Initial Unsorted: {arr}")
    
    sorted_arr = bucket_sort(arr)
    print(f"\nFinal Sorted:     {sorted_arr}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fatal worst-case flaw of Bucket Sort?
   Answer: If the data is NOT uniformly distributed (e.g., [0.91, 0.92, 0.93, 0.94, 0.95]), every single element will map mathematically into the exact same bucket (Bucket 9). Bucket Sort then runs Insertion Sort on a single bucket containing all $N$ elements. Insertion Sort takes $O(N^2)$ time. The entire algorithm degrades catastrophically.

2. Why do we use Insertion Sort to sort the individual buckets? Why not Quick Sort?
   Answer: Because we expect the numbers to be uniformly distributed, each bucket should mathematically contain around 1 to 3 elements. Quick Sort has a massive constant factor overhead (recursion calls, pivot calculations) that makes it very slow for tiny arrays. Insertion Sort has virtually zero overhead and is the fastest algorithm in existence for arrays of size $N < 10$.

3. Can Bucket Sort handle numbers larger than 1.0?
   Answer: Yes. You must normalize the numbers first. Find the absolute Minimum and Maximum in the array. The formula to map any number into the [0.0, 1.0) range is: `normalized = (value - min) / (max - min)`. Then you just use the standard Bucket Sort mapping function!
"""

if __name__ == "__main__":
    demonstrate_bucket_sort()
    print("\n[SUCCESS] Laboratory: Bucket Sort Completed.")
