"""
# ==============================================================================
# LABORATORY: SEARCH ALGORITHMS (LINEAR & BINARY SEARCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Searching is the most fundamental operation in computer science.
# "Linear Search" simply checks every item one by one. It takes O(N) time.
# If you have 1 Billion items, it takes 1 Billion operations.
#
# "Binary Search" exploits the fact that an array is SORTED. 
# By checking the middle element and instantly discarding half of the remaining 
# array, the search space shrinks exponentially. 
# For 1 Billion items, Binary Search takes exactly 30 operations (O(log2 N)).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the limits of Linear Search.
# - Understand the integer overflow bug in `(left + right) // 2`.
# - Implement Iterative and Recursive Binary Search.
# - Master upper and lower bounds (`bisect_left`, `bisect_right`).
#
# ==============================================================================
"""

import bisect
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LINEAR SEARCH (THE BASELINE)
# ==============================================================================
def linear_search(arr: List[int], target: int) -> int:
    """
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1


# ==============================================================================
# 4. BINARY SEARCH (ITERATIVE AND RECURSIVE)
# ==============================================================================
def binary_search_iterative(arr: List[int], target: int) -> int:
    """
    Time Complexity: O(log N)
    Space Complexity: O(1)
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        # THE OVERFLOW BUG:
        # You might be tempted to write: mid = (left + right) // 2
        # In Python, this is fine because integers have arbitrary precision.
        # But in C/Java/C++, if left and right are huge numbers (e.g., 2 Billion),
        # adding them together yields 4 Billion, which EXCEEDS the 32-bit integer 
        # limit (2.14B). The program crashes with an Integer Overflow error!
        #
        # THE FIX:
        # Subtract left from right, divide by 2, and add it back to left.
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1 # Target is in the right half
        else:
            right = mid - 1 # Target is in the left half
            
    return -1


def binary_search_recursive(arr: List[int], target: int, left: int, right: int) -> int:
    """
    Time Complexity: O(log N)
    Space Complexity: O(log N) due to the call stack! Iterative is better.
    """
    if left > right:
        return -1
        
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def demonstrate_binary_search():
    section_header("Algorithm: Iterative Binary Search")
    
    arr = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    print(f"Sorted Array: {arr}")
    
    target = 14
    print(f"Searching for {target}...")
    
    idx = binary_search_iterative(arr, target)
    print(f"Found at index: {idx}")


# ==============================================================================
# 5. UPPER AND LOWER BOUNDS (BISECT)
# ==============================================================================
def demonstrate_bisect():
    section_header("Algorithm: Bisect Left vs Bisect Right")
    
    print("What if the array has DUPLICATES? Which index does Binary Search return?")
    
    # Indices: 0  1  2  3  4  5  6
    arr =    [ 1, 3, 5, 5, 5, 7, 9 ]
    print(f"Array: {arr}")
    print("Target: 5 (Appears at indices 2, 3, and 4)")
    
    # A standard binary search might return 3 (the middle). 
    # But often, we want the FIRST occurrence, or the LAST occurrence.
    
    # bisect_left (Lower Bound)
    # Returns the index of the FIRST element that is >= Target
    idx_left = bisect.bisect_left(arr, 5)
    print(f"\nbisect_left(5)  -> Index {idx_left} (The very first '5')")
    
    # bisect_right (Upper Bound)
    # Returns the index of the FIRST element that is STRICTLY GREATER than Target
    idx_right = bisect.bisect_right(arr, 5)
    print(f"bisect_right(5) -> Index {idx_right} (The '7' immediately after the last '5')")
    
    # Mathematical Trick: Counting occurrences
    # How many times does 5 appear?
    count = idx_right - idx_left
    print(f"Occurrences: {idx_right} - {idx_left} = {count}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `left + (right - left) // 2` prevent integer overflow?
   Answer: In statically typed languages (Java/C++), a 32-bit signed integer has a maximum value of 2.14 billion. If `left` is 1.5 billion and `right` is 2.0 billion, `left + right` equals 3.5 billion, which crashes the program (Overflow). By doing `(right - left)`, you get `0.5 billion`. Divided by 2 is `0.25 billion`. Added back to `left` is `1.75 billion`. The math never exceeds 2.14 billion at any step.

2. Why is Iterative Binary Search preferred over Recursive?
   Answer: Iterative takes strictly O(1) memory. Recursive takes O(log N) memory because every recursive function call is added to the OS Call Stack. For massive datasets, you want to avoid unnecessary memory overhead.

3. How would you implement `bisect_left` manually?
   Answer: Inside the `while left <= right:` loop, when `arr[mid] == target`, instead of `return mid`, you keep searching to the left by doing `right = mid - 1`. You record `ans = mid`. When the loop finishes, `ans` holds the absolute first occurrence!
"""

if __name__ == "__main__":
    demonstrate_binary_search()
    demonstrate_bisect()
    print("\n[SUCCESS] Laboratory: Linear and Binary Search Completed.")
