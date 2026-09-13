"""
# ==============================================================================
# LABORATORY: RADIX SORT (O(d * N) DIGIT-BY-DIGIT SORT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous laboratory, we saw that Counting Sort achieves O(N) time, 
# breaking the mathematical O(N log N) barrier. However, it had a fatal flaw:
# if the array contained the number 1 Billion, it would crash your computer 
# trying to allocate an array of 1 Billion empty slots.
#
# "Radix Sort" solves this problem beautifully. 
# Instead of treating 1 Billion as a single massive number, it treats it as 
# a sequence of 10 digits (1, 0, 0, 0, 0, 0, 0, 0, 0, 0).
# 
# It runs Counting Sort on the 1s place. Then the 10s place. Then the 100s place.
# Because a single digit can only be 0 through 9, Counting Sort only ever needs 
# an array of size 10!
#
# By repeating Counting Sort $d$ times (where $d$ is the number of digits of the 
# largest number), Radix Sort completely sidesteps the massive memory blowup, 
# achieving O(d * N) time while using strictly O(N) memory!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Least Significant Digit (LSD) sorting.
# - Understand why the subroutine MUST be a Stable Sort.
# - Implement a Base-10 Radix Sort.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RADIX SORT IMPLEMENTATION (LSD)
# ==============================================================================
def counting_sort_for_radix(arr: List[int], exp: int) -> None:
    """
    A modified Stable Counting Sort that only looks at ONE specific digit.
    `exp` represents the current digit's place (1, 10, 100, 1000...)
    """
    n = len(arr)
    output = [0] * n
    
    # Base 10 means digits are 0-9. We only ever need an array of size 10!
    counts = [0] * 10
    
    # 1. Tally the frequencies of the SPECIFIC DIGIT
    for i in range(n):
        # Math trick to extract the digit:
        # If number is 256, and exp is 10: 
        # (256 // 10) % 10 -> 25 % 10 -> 5 (The tens place digit)
        index = (arr[i] // exp) % 10
        counts[index] += 1
        
    # 2. Build the Prefix Sum array
    for i in range(1, 10):
        counts[i] += counts[i - 1]
        
    # 3. Build the output array backwards to guarantee STABILITY
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        placement = counts[index] - 1
        
        output[placement] = arr[i]
        counts[index] -= 1
        
    # Copy the sorted output back into the original array
    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr: List[int]) -> List[int]:
    """
    Time Complexity: O(d * (N + b)) where d=digits, b=base (10).
    Space Complexity: O(N + b)
    """
    if not arr: return []
    
    # Find the maximum number to know how many digits we have
    max_num = max(arr)
    
    # Start at the 1s place (exp = 1)
    exp = 1
    
    # Keep running Counting Sort as long as the maximum number has digits left
    while max_num // exp > 0:
        print(f"Sorting by {exp}s place...")
        counting_sort_for_radix(arr, exp)
        print(f" -> {arr}")
        
        # Move to the next digit (10s place, 100s place, etc.)
        exp *= 10
        
    return arr

def demonstrate_radix():
    section_header("Algorithm: Radix Sort (LSD)")
    
    # Notice we have varying lengths: 3 digits, 2 digits, 1 digit
    arr = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Initial Unsorted: {arr}\n")
    
    radix_sort(arr)
    print(f"\nFinal Sorted:     {arr}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why MUST the internal Counting Sort be "Stable"?
   Answer: If we sort the 10s place, we are grouping all the numbers in the 20s together (21, 24, 28). But wait! We ALREADY sorted the 1s place in the previous loop! If the sort is Unstable, it will scramble the 1s place while sorting the 10s place. A Stable sort guarantees that ties in the 10s place are broken by their relative order (which is perfectly sorted by the 1s place).

2. If Radix Sort is $O(d \\times N)$, and $d$ is just a constant (like 10 digits), doesn't that make it $O(N)$? Why isn't it the default sorting algorithm?
   Answer: Yes, mathematically it is linear! But remember, Big-O drops constants. In the real world, constants matter. The overhead of isolating digits `(num // exp) % 10`, allocating temporary arrays, and doing multiple full passes over memory creates a massive Constant Factor. For standard datasets (under 1 million integers), the highly optimized CPU cache performance of Quick Sort $O(N \\log N)$ is actually faster in clock time than Radix Sort.

3. What is MSD vs LSD Radix Sort?
   Answer: 
   - LSD (Least Significant Digit): Starts at the 1s place and works left. Easiest to implement.
   - MSD (Most Significant Digit): Starts at the highest place (e.g., millions place). Groups the numbers into buckets, and recursively sorts each bucket. It is used to sort Strings alphabetically!
"""

if __name__ == "__main__":
    demonstrate_radix()
    print("\n[SUCCESS] Laboratory: Radix Sort Completed.")
