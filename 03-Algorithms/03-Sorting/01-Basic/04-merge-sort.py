"""
# ==============================================================================
# LABORATORY: ITERATIVE (BOTTOM-UP) MERGE SORT
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Merge Sort is a recursive "Divide and Conquer" algorithm.
# It splits the array in half, then in half again, down to arrays of size 1.
# 
# But recursion is dangerous. Every recursive call adds a frame to the OS Call Stack. 
# If you are sorting an array of 100 Million items, the Call Stack might overflow, 
# crashing your program instantly (StackOverflowError).
#
# What if we skip the "Divide" step entirely?
# Since we know the array will eventually be split into sizes of 1 anyway... 
# why not just START at the bottom?
# 
# "Bottom-Up Merge Sort" is fully Iterative. It uses a `while` loop instead of 
# recursion. It merges arrays of size 1 into size 2, then size 2 into size 4, 
# then 4 into 8, until the entire array is sorted!
#
# This completely eliminates the O(log N) Call Stack memory overhead, making it 
# safer and faster for massive system-level applications.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to eliminate Recursion.
# - Master Iterative Bottom-Up merging.
# - Understand power-of-2 step sizes.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ITERATIVE (BOTTOM-UP) MERGE SORT
# ==============================================================================
def merge_bottom_up(arr: List[int]) -> List[int]:
    """
    Sorts an array iteratively (no recursion!).
    Time Complexity: O(N log N)
    Space Complexity: O(N) for the temporary array, but O(1) Call Stack!
    """
    n = len(arr)
    
    # We need a temporary array to hold the merged data.
    # Creating ONE temporary array upfront is much faster than creating hundreds 
    # of small arrays during recursion.
    temp = [0] * n
    
    # Step size starts at 1 (Arrays of size 1).
    # It will double every pass: 1 -> 2 -> 4 -> 8 -> 16...
    width = 1
    
    while width < n:
        # Iterate through the array, merging pairs of blocks of size `width`
        for i in range(0, n, 2 * width):
            
            # Left block starts at i, ends at i + width
            left_start = i
            left_end = min(i + width, n)
            
            # Right block starts at i + width, ends at i + 2*width
            right_start = left_end
            right_end = min(i + 2 * width, n)
            
            # Now, merge these two contiguous blocks!
            l = left_start
            r = right_start
            t = left_start # Pointer for the temp array
            
            # Standard Two-Pointer Merge logic
            while l < left_end and r < right_end:
                if arr[l] <= arr[r]:
                    temp[t] = arr[l]
                    l += 1
                else:
                    temp[t] = arr[r]
                    r += 1
                t += 1
                
            # Copy remaining elements from left block
            while l < left_end:
                temp[t] = arr[l]
                l += 1
                t += 1
                
            # Copy remaining elements from right block
            while r < right_end:
                temp[t] = arr[r]
                r += 1
                t += 1
                
            # Immediately copy the merged data back into the original array
            # so the next `width` iteration has the updated data!
            for k in range(left_start, right_end):
                arr[k] = temp[k]
                
        # Double the block size for the next pass
        print(f" Pass with Width {width}: {arr}")
        width *= 2
        
    return arr

def demonstrate_bottom_up():
    section_header("Algorithm: Bottom-Up Merge Sort")
    
    arr = [38, 27, 43, 3, 9, 82, 10, 1]
    print(f"Initial Array: {arr}\n")
    
    sorted_arr = merge_bottom_up(arr)
    print(f"\nFinal Sorted Array: {sorted_arr}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Bottom-Up Merge Sort preferred in hardware/embedded systems?
   Answer: Hardware systems have very small Call Stacks. Recursion runs the risk of a StackOverflow. Bottom-Up Merge Sort is purely Iterative (uses standard `while` loops), guaranteeing that the Call Stack never grows past O(1).

2. How does the Iterative version handle arrays whose length is NOT a power of 2?
   Answer: The `min()` function in the boundary calculations saves us! If `i + width` exceeds the length of the array, `min(i + width, n)` caps it perfectly at the end of the array. The algorithm will happily merge a block of size 4 with a block of size 1.

3. Can Merge Sort be done entirely In-Place (O(1) auxiliary space)?
   Answer: Mathematically, yes, but it is incredibly complex. Standard Merge Sort takes O(N) space to hold the merged elements. "In-Place Merge Sort" uses advanced algorithmic tricks (like block-swapping and reversing segments) to merge the two halves without a temporary array. However, doing so increases the Constant Factor so much that it is extremely slow in practice, so nobody uses it in production.
"""

if __name__ == "__main__":
    demonstrate_bottom_up()
    print("\n[SUCCESS] Laboratory: Iterative Merge Sort Completed.")
