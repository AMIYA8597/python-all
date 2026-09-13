"""
# ==============================================================================
# LABORATORY: COUNTING SORT (O(N) NON-COMPARISON SORT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've been told that O(N log N) is the absolute mathematical speed limit for 
# sorting algorithms. This is proven by the "Decision Tree Lower Bound" theorem.
# 
# But there is a loophole. That theorem only applies to "Comparison-Based" sorts 
# (algorithms that use `if a < b`). 
# 
# What if we don't compare the numbers at all?
# What if we just use the number ITSELF as an index in an array?
#
# If you have an array `[3, 1, 3, 2]`. We can create a new "Counts" array of 
# size 4. We scan the input:
# - See a 3? Increment `counts[3]`.
# - See a 1? Increment `counts[1]`.
# 
# Then we just read the Counts array left to right, and print out the numbers!
# We just sorted the array in strictly O(N) time! 
# We shattered the O(N log N) mathematical barrier!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Non-Comparison Sorting.
# - Understand the O(N + K) Time and Space complexity limit.
# - Implement Stable Counting Sort using the Prefix Sum array trick.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE COUNTING SORT (UNSTABLE)
# ==============================================================================
def naive_counting_sort(arr: List[int]) -> List[int]:
    """
    Sorts an array in O(N + K) time, where K is the Maximum value in the array.
    This version is incredibly simple, but it is UNSTABLE, which makes it 
    useless as a subroutine for Radix Sort.
    """
    if not arr: return []
    
    # K is the maximum value.
    k = max(arr)
    
    # 1. Create the Count Array of size K + 1
    # Initialize all counts to 0. (Takes O(K) space)
    counts = [0] * (k + 1)
    
    # 2. Tally the frequencies (Takes O(N) time)
    for num in arr:
        counts[num] += 1
        
    # 3. Reconstruct the sorted array (Takes O(N + K) time)
    sorted_arr = []
    for i in range(len(counts)):
        # For every tally, append that number to the final array
        while counts[i] > 0:
            sorted_arr.append(i)
            counts[i] -= 1
            
    return sorted_arr

def demonstrate_naive():
    section_header("Algorithm: Naive Counting Sort")
    
    arr = [4, 2, 2, 8, 3, 3, 1]
    print(f"Initial Unsorted: {arr}")
    print("Maximum value is 8, so we create a count array of size 9.")
    
    sorted_arr = naive_counting_sort(arr)
    print(f"Final Sorted:     {sorted_arr}")


# ==============================================================================
# 4. STABLE COUNTING SORT (PREFIX SUM)
# ==============================================================================
def stable_counting_sort(arr: List[int]) -> List[int]:
    """
    Sorts an array in O(N + K) time, but remains strictly STABLE.
    This is required for Radix Sort to function correctly.
    """
    if not arr: return []
    k = max(arr)
    counts = [0] * (k + 1)
    
    # 1. Tally the frequencies
    for num in arr:
        counts[num] += 1
        
    # 2. Transform the Counts array into a PREFIX SUM array.
    # What does this do? It tells us the EXACT mathematical ending index 
    # where a number belongs in the final array!
    # If counts[3] is 5, it means the number 3 should be placed at index 4 (5-1).
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
        
    # 3. Build the output array BACKWARDS.
    # By iterating the original array backwards, and using the Prefix Sum array 
    # to find the exact placement index, we guarantee Stability!
    output = [0] * len(arr)
    
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        
        # Look up where this number belongs
        placement_index = counts[num] - 1
        
        # Place it
        output[placement_index] = num
        
        # Decrement the count, so the next identical duplicate is placed 
        # one index to the left! (Preserving stability).
        counts[num] -= 1
        
    return output

def demonstrate_stable():
    section_header("Algorithm: Stable Counting Sort")
    
    arr = [1, 4, 1, 2, 7, 5, 2]
    print(f"Initial Unsorted: {arr}")
    
    sorted_arr = stable_counting_sort(arr)
    print(f"Final Sorted:     {sorted_arr}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. If Counting Sort is $O(N)$, why don't we use it for everything instead of Quick Sort?
   Answer: Look at the Time/Space complexity: $O(N + K)$. $K$ is the maximum value in the array. If you have an array of just two numbers: `[1, 999999999]`, $N$ is 2, but $K$ is 1 Billion! Counting Sort will crash your computer trying to allocate an array of 1 Billion empty zeroes in RAM just to sort two numbers. It is ONLY useful when the numbers are tightly bounded (e.g., sorting ages between 0-120).

2. How does the Prefix Sum make it stable?
   Answer: If we have an array `[3_red, 3_blue]`. When iterating backwards, we hit `3_blue` first. We look at the Prefix Sum to find the absolute LAST valid index for a 3. We place `3_blue` there, and decrement the counter. Next we hit `3_red`. We place it one index to the LEFT of `3_blue`. Because `3_red` is placed to the left of `3_blue` in the final array, their original relative order is perfectly maintained!

3. Can Counting Sort handle negative numbers?
   Answer: The standard version cannot, because array indices in most languages cannot be negative (in Python, a negative index wraps to the back of the list, destroying the logic). You can fix this by finding the Minimum value in the array, and then offsetting everything: `counts[num - minimum]`.
"""

if __name__ == "__main__":
    demonstrate_naive()
    demonstrate_stable()
    print("\n[SUCCESS] Laboratory: Counting Sort Completed.")
