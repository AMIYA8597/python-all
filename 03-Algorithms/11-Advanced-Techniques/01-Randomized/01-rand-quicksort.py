"""
# ==============================================================================
# LABORATORY: RANDOMIZED ALGORITHMS (QUICKSORT & QUICKSELECT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned Quicksort in the basic algorithms phase. 
# It picks the first (or last) element as the Pivot, partitions the array into 
# "Smaller than Pivot" and "Larger than Pivot", and recursively sorts the halves.
#
# But Standard Quicksort has a fatal flaw: The $O(N^2)$ Adversary Attack.
# If an attacker feeds a pre-sorted array (like 1, 2, 3, 4, 5) into Standard 
# Quicksort, it will pick '1' as the pivot. The partition fails to divide the 
# array in half; it splits it into size 0 and size N-1! 
# The recursion depth hits N, and the runtime catastrophically degrades to $O(N^2)$.
#
# The Solution: Randomized Quicksort.
# We pick a completely RANDOM element to be the pivot, and swap it to the end 
# before partitioning! 
# Because the pivot is chosen randomly, NO SPECIFIC INPUT ARRAY CAN FORCE THE 
# $O(N^2)$ WORST CASE! The expected runtime mathematically converges to a rigid 
# $O(N \log N)$ regardless of the input data.
#
# Application: Quickselect (Hoare's Selection Algorithm)
# Problem: "Find the 5th largest element in an unsorted array of 1 Billion items."
# - Sorting takes $O(N \log N)$.
# - A Min-Heap takes $O(N \log K)$.
# - Quickselect takes $O(N)$ expected time!
# How? When you partition the array, the Pivot is placed in its ABSOLUTE FINAL 
# SORTED POSITION. If the pivot lands at index 5, you instantly found the 5th 
# element! If it lands at index 8, you THROW AWAY the right half and only recurse 
# on the left half! 
# Because you only search one half, the time complexity is $N + N/2 + N/4... = O(N)$!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the adversarial $O(N^2)$ worst case.
# - Implement Randomized Partitioning.
# - Master $O(N)$ Quickselect for K-th Order Statistics.
#
# ==============================================================================
"""

import random
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RANDOMIZED PARTITIONING ENGINE
# ==============================================================================
def partition(arr: List[int], low: int, high: int) -> int:
    """
    Standard Lomuto Partition scheme.
    Uses the element at `arr[high]` as the pivot.
    Places the pivot in its correct sorted position and returns that index.
    """
    pivot = arr[high]
    
    # `i` is the boundary of the "Smaller than Pivot" zone
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            # Swap it into the Smaller zone!
            arr[i], arr[j] = arr[j], arr[i]
            
    # Finally, swap the Pivot (which is at `high`) to rest directly AFTER the Smaller zone!
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1


def randomized_partition(arr: List[int], low: int, high: int) -> int:
    """
    The Randomized Security wrapper.
    Picks a random pivot, swaps it to `high`, and runs standard partition!
    """
    rand_pivot_idx = random.randint(low, high)
    
    # Hide the random pivot at the end of the array so standard partition can use it!
    arr[rand_pivot_idx], arr[high] = arr[high], arr[rand_pivot_idx]
    
    return partition(arr, low, high)


# ==============================================================================
# 4. RANDOMIZED QUICKSORT & QUICKSELECT
# ==============================================================================
def randomized_quicksort(arr: List[int], low: int, high: int):
    """
    Sorts the array in expected O(N log N) time.
    Immune to adversarial pre-sorted array attacks.
    """
    if low < high:
        # 1. Partition around a random pivot
        pivot_idx = randomized_partition(arr, low, high)
        
        # 2. Recursively sort BOTH halves
        randomized_quicksort(arr, low, pivot_idx - 1)
        randomized_quicksort(arr, pivot_idx + 1, high)


def quickselect(arr: List[int], low: int, high: int, k_index: int) -> int:
    """
    Finds the element that WOULD be at `k_index` if the array were fully sorted.
    Expected Time Complexity: O(N)
    Worst Case Time Complexity: O(N^2) (Mathematically almost impossible with randomness).
    """
    if low == high:
        # Only one element left! It must be our answer.
        return arr[low]
        
    # 1. Partition the array!
    # The pivot is now sitting in its ABSOLUTE CORRECT SORTED POSITION.
    pivot_idx = randomized_partition(arr, low, high)
    
    # 2. Check if we got incredibly lucky!
    if k_index == pivot_idx:
        return arr[pivot_idx]
        
    # 3. If our target is to the LEFT of the pivot, the right side is GARBAGE!
    # We completely discard the right side and only recurse left.
    elif k_index < pivot_idx:
        return quickselect(arr, low, pivot_idx - 1, k_index)
        
    # 4. If our target is to the RIGHT, we discard the left side!
    else:
        return quickselect(arr, pivot_idx + 1, high, k_index)


def get_kth_smallest(arr: List[int], k: int) -> int:
    """
    Wrapper for Quickselect.
    k is 1-indexed (e.g., 1st smallest = minimum).
    """
    if k < 1 or k > len(arr):
        raise ValueError("Invalid K")
        
    # Convert 1-indexed K to 0-indexed K_index
    k_index = k - 1
    
    # We must pass a COPY of the array if we don't want to mutate the original, 
    # because Quickselect physically moves elements around!
    return quickselect(arr.copy(), 0, len(arr) - 1, k_index)


def get_kth_largest(arr: List[int], k: int) -> int:
    """
    The K-th largest is mathematically the (N - K + 1)-th smallest!
    """
    n = len(arr)
    return get_kth_smallest(arr, n - k + 1)


def demonstrate_randomized_algorithms():
    section_header("Algorithm: Randomized Quicksort")
    
    # A pre-sorted array! (This would trigger O(N^2) on Standard Quicksort)
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Let's shuffle it to prove it sorts correctly, though it handles sorted fine!
    test_arr = [10, 3, 5, 1, 9, 2, 8, 4, 7, 6]
    print(f"Unsorted Array: {test_arr}")
    
    randomized_quicksort(test_arr, 0, len(test_arr) - 1)
    print(f"Sorted Array  : {test_arr}")
    
    section_header("Algorithm: Quickselect O(N)")
    
    data = [3, 2, 1, 5, 6, 4]
    print(f"Dataset: {data}")
    
    k = 2
    # The 2nd largest should be 5.
    print(f"\nFinding the {k}nd LARGEST element...")
    ans_large = get_kth_largest(data, k)
    print(f"Result: {ans_large} (Expected: 5)")
    
    # The 3rd smallest should be 3.
    k2 = 3
    print(f"\nFinding the {k2}rd SMALLEST element...")
    ans_small = get_kth_smallest(data, k2)
    print(f"Result: {ans_small} (Expected: 3)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Quickselect achieve $O(N)$ time while Quicksort is $O(N \log N)$?
   Answer: Quicksort is a branching algorithm. It splits the array in half, and MUST physically traverse down the Left branch AND the Right branch. This creates a tree of $\log N$ height, evaluating $N$ elements at each level: $O(N \log N)$. 
   Quickselect does NOT branch! It splits the array in half, and instantly throws half the data in the garbage. It only traverses down ONE branch! 
   The work done is: $N + N/2 + N/4 + N/8 \dots$
   This is a geometric series that mathematically converges to $2N$. Therefore, the absolute time complexity is exactly $O(N)$!

2. How does `random.randint` prevent the $O(N^2)$ Adversary Attack?
   Answer: In standard Quicksort (picking the last element as pivot), a malicious hacker can intentionally craft an array formatted like `[10, 9, 8, 7, 6]` and send it to your server. Your server will pick 6, partition poorly, and take $O(N^2)$ time, causing a Denial of Service (DoS) timeout. 
   If your server picks a RANDOM pivot, the malicious hacker cannot mathematically predict which number your server will pick. They cannot pre-craft an array to trigger the worst-case scenario. The probability of your randomizer accidentally picking the absolute worst pivot at EVERY single recursive level is roughly $(1/N)^N$, which is astronomically close to $0$.

3. What is the Median of Medians?
   Answer: While Randomized Quickselect has an Expected time of $O(N)$, its absolute Worst-Case time is technically still $O(N^2)$ if you are incredibly unlucky. In 1973, five famous computer scientists (including Rivest and Tarjan) invented the "Median of Medians" algorithm. It deterministically calculates a "good" pivot by breaking the array into chunks of 5, finding their medians, and recursively finding the median of those medians. This guarantees a strict, deterministic $O(N)$ worst-case time! However, because the constant factors (chunking arrays) are very slow, Randomized Quickselect is preferred in real-world production.
"""

if __name__ == "__main__":
    demonstrate_randomized_algorithms()
    print("\n[SUCCESS] Laboratory: Randomized Algorithms Completed.")
