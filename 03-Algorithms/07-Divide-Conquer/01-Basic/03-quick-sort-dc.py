"""
# ==============================================================================
# LABORATORY: QUICK SORT & RANDOMIZED DIVIDE AND CONQUER
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You saw that Merge Sort physically chops arrays in half, forcing a perfect 
# O(N log N) runtime. But creating those arrays requires O(N) extra RAM memory.
#
# Quick Sort is the ultimate "In-Place" Divide & Conquer algorithm. It requires 
# strictly O(1) extra space!
# 
# The magic is in the "Partition" function. Instead of blindly chopping the 
# array in half, it picks a "Pivot" number. It sweeps the array and throws every 
# number smaller than the pivot to the left, and every number larger to the right.
#
# The Divide & Conquer phases are inverted compared to Merge Sort:
# 1. DIVIDE: Pick a Pivot. Partition the array in O(N) time. (Heavy lifting here).
# 2. CONQUER: Recursively call Quick Sort on the left and right partitions.
# 3. COMBINE: Do absolutely nothing! (O(1) time). The array is already sorted in-place.
#
# But there is a deadly trap. If you always pick the LAST element as the pivot, 
# and the array is ALREADY SORTED, you will partition 1 element to the right, 
# and N-1 elements to the left. 
# T(n) = T(n-1) + O(n). This collapses to O(N^2) time!
#
# To fix this, we use a "Randomized Pivot". By picking a random number as the 
# pivot, we mathematically guarantee that the array will split roughly in half, 
# restoring the O(N log N) expected runtime!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the inverted D&C structure (Heavy Divide, Empty Combine).
# - Implement Lomuto Partitioning.
# - Implement Randomized Pivoting to prevent O(N^2) attacks.
#
# ==============================================================================
"""

import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RANDOMIZED QUICK SORT ENGINE
# ==============================================================================
def quick_sort(nums: List[int], low: int, high: int):
    """
    In-Place Divide & Conquer Sorting.
    Expected Time Complexity: O(N log N).
    Space Complexity: O(log N) due to recursion stack (Auxiliary space is O(1)).
    """
    # 1. BASE CASE
    if low >= high:
        return
        
    # --- RANDOMIZED PIVOT ---
    # Pick a random index between low and high.
    # Swap it with the `high` index so it sits at the end (allowing us to use 
    # the standard Lomuto partition algorithm without rewriting it!)
    pivot_idx = random.randint(low, high)
    nums[pivot_idx], nums[high] = nums[high], nums[pivot_idx]
    
    # 2. DIVIDE (THE PARTITION STEP)
    # This does the heavy O(N) work of shifting elements around the pivot.
    split_index = partition(nums, low, high)
    
    # 3. CONQUER (RECURSIVE CALLS)
    # The `split_index` is in its ABSOLUTE PERFECT FINAL POSITION. 
    # We do NOT include it in the recursive calls!
    quick_sort(nums, low, split_index - 1)
    quick_sort(nums, split_index + 1, high)
    
    # 4. COMBINE
    # Nothing to do! The array was mutated in place.


def partition(nums: List[int], low: int, high: int) -> int:
    """
    Lomuto Partition Scheme.
    Sweeps the array, throwing smaller elements to the left.
    Returns the final resting index of the Pivot.
    """
    pivot_value = nums[high]
    
    # `i` tracks the boundary of the "Smaller than Pivot" zone.
    i = low - 1
    
    for j in range(low, high):
        # If the current element is smaller than or equal to the pivot...
        if nums[j] <= pivot_value:
            # Expand the "Smaller" zone by 1!
            i += 1
            # Swap the small element into the zone!
            nums[i], nums[j] = nums[j], nums[i]
            
    # The `i` pointer is at the very end of the "Smaller" zone.
    # Therefore, `i + 1` is the start of the "Larger" zone.
    # We swap the Pivot (which is sitting at `high`) directly into `i + 1`!
    nums[i + 1], nums[high] = nums[high], nums[i + 1]
    
    return i + 1


def demonstrate_quick_sort():
    section_header("Algorithm: Randomized Quick Sort (D&C)")
    
    # Seed for reproducible random pivots in the demonstration
    random.seed(42)
    
    nums = [10, 80, 30, 90, 40, 50, 70]
    
    print(f"Unsorted Input Array: {nums}")
    print("\nExecuting In-Place Divide & Conquer (Quick Sort)...")
    
    quick_sort(nums, 0, len(nums) - 1)
    
    print(f"\nSorted Output: {nums}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the Combine step in Quick Sort $O(1)$, but in Merge Sort it is $O(N)$?
   Answer: Because Merge Sort's Divide step was a "blind" chop. It just cut the array in half without looking at the numbers. Therefore, it had to do all the logical sorting work during the Combine step (merging). Quick Sort is the exact opposite. Its Divide step (Partition) does all the logical sorting work by physically moving elements around the pivot. Because everything is already in place, the Combine step is empty.

2. What is an "Algorithm Attack", and how does the Randomized Pivot prevent it?
   Answer: In competitive programming or production environments, a malicious user can intentionally send a pre-sorted array (or reverse sorted array) to your Quick Sort API. If you use the `high` index as a pivot, their array forces $T(n) = T(n-1) + O(n)$, causing an $O(N^2)$ algorithmic DoS (Denial of Service) attack, freezing the server! By picking a random pivot mathematically unknown to the attacker, you guarantee the mathematical probability of an $O(N^2)$ execution is virtually zero.

3. Why is Quick Sort practically faster than Merge Sort if they are both $O(N \\log N)$?
   Answer: "Cache Locality". Quick Sort swaps elements sequentially in a tight loop within the same physical array. Modern CPUs can pre-fetch this memory into the ultra-fast L1 Cache. Merge Sort constantly allocates and deallocates new temporary arrays during the merge step, causing "Cache Misses" which forces the CPU to wait for slower RAM. Even though the mathematical big-O is the same, the constant factors in physics make Quick Sort faster.
"""

if __name__ == "__main__":
    demonstrate_quick_sort()
    print("\n[SUCCESS] Laboratory: Quick Sort D&C Completed.")
