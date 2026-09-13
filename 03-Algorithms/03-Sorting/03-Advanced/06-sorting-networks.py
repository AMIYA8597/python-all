"""
# ==============================================================================
# LABORATORY: SORTING NETWORKS (BITONIC SORT & HARDWARE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Every sorting algorithm we have covered so far (Quick Sort, Merge Sort) uses 
# software control-flow: `if arr[i] > arr[j]`. 
# Depending on the data, the CPU will execute a completely different sequence 
# of instructions (Branch Prediction).
#
# But what if you are designing a silicon microchip (ASIC or FPGA) and you need 
# to sort data directly using copper wires and logic gates, without a CPU?
# What if you are programming a GPU with 4,000 cores that requires all cores to 
# execute the exact same instruction simultaneously (SIMD)?
#
# You need a "Sorting Network".
# A Sorting Network is a predetermined sequence of "Comparators". A comparator 
# takes two wires, compares the values, and always puts the smaller value on the 
# top wire and the larger value on the bottom wire.
#
# The most famous sorting network is **Bitonic Sort**. 
# It is completely **Data-Oblivious**. The sequence of comparisons is exactly the 
# same whether the array is already sorted or completely reversed.
# 
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Data-Oblivious Algorithms.
# - Understand Bitonic Sequences.
# - Implement a software simulation of a Bitonic Sorting Network.
# - Understand why O(log^2 N) parallel time is so powerful.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BITONIC SORT IMPLEMENTATION
# ==============================================================================
def comp_and_swap(arr: List[int], i: int, j: int, direction: int) -> None:
    """
    Simulates a hardware Comparator.
    `direction` = 1 for Ascending (smaller on top).
    `direction` = 0 for Descending (larger on top).
    """
    if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr: List[int], low: int, count: int, direction: int) -> None:
    """
    Recursively merges a Bitonic sequence (one that goes up, then down) into a 
    fully sorted sequence.
    """
    if count > 1:
        k = count // 2
        
        # Compare and swap elements at a distance of `k`
        for i in range(low, low + k):
            comp_and_swap(arr, i, i + k, direction)
            
        # Recursively merge the two halves
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)

def bitonic_sort_recursive(arr: List[int], low: int, count: int, direction: int) -> None:
    """
    Builds a Bitonic sequence by recursively sorting the first half in Ascending 
    order, and the second half in Descending order.
    """
    if count > 1:
        k = count // 2
        
        # Sort left half in ASCENDING order (1)
        bitonic_sort_recursive(arr, low, k, 1)
        
        # Sort right half in DESCENDING order (0)
        bitonic_sort_recursive(arr, low + k, k, 0)
        
        # The entire array is now a Bitonic Sequence (Goes UP then DOWN).
        # We can now merge it into a single sorted direction!
        bitonic_merge(arr, low, count, direction)

def bitonic_sort(arr: List[int]) -> List[int]:
    """
    Bitonic Sort only works mathematically if the array size is a Power of 2!
    Time Complexity: O(N log^2 N) sequential. O(log^2 N) parallel!
    """
    n = len(arr)
    # Check if N is a power of 2
    if (n & (n - 1)) != 0 or n == 0:
        raise ValueError("Bitonic Sort requires an array size that is a Power of 2!")
        
    bitonic_sort_recursive(arr, 0, n, 1) # 1 means sort Ascending
    return arr

def demonstrate_bitonic_sort():
    section_header("Algorithm: Bitonic Sort (Sorting Networks)")
    
    # Must be a power of 2 (size 8)
    arr = [3, 7, 4, 8, 6, 2, 1, 5]
    print(f"Initial Unsorted Array: {arr}\n")
    
    print("Executing Bitonic Sort...")
    # In a real hardware ASIC, all the comparators in a single stage execute 
    # simultaneously in a single clock cycle!
    bitonic_sort(arr)
    
    print(f"Final Sorted Array: {arr}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Bitonic Sort heavily used in GPUs?
   Answer: GPUs execute code using SIMD (Single Instruction, Multiple Data). This means thousands of cores must execute the EXACT same line of code at the exact same time. If a sorting algorithm uses `if/else` statements that branch differently for different numbers, the GPU cores fall out of sync (Warp Divergence) and performance collapses. Bitonic Sort is "Data-Oblivious"—it performs the exact same swaps regardless of the data, keeping all GPU cores perfectly synchronized.

2. Why is Data-Obliviousness important in Cryptography?
   Answer: "Timing Attacks" (a Side-Channel Attack). If you sort sensitive cryptographic keys using Quick Sort, an attacker can mathematically measure exactly how many milliseconds the CPU took to sort it. Because Quick Sort is faster on certain arrays and slower on others, the attacker can use the timing data to reverse-engineer the cryptographic keys! A Data-Oblivious algorithm takes the exact same number of milliseconds to run no matter what the input is, rendering Timing Attacks impossible.

3. What is the Parallel Time Complexity of Bitonic Sort?
   Answer: If you have enough hardware comparators (or GPU cores) to execute an entire stage simultaneously, the Time Complexity drops to the depth of the network, which is mathematically proven to be $O(\\log^2 N)$. For an array of 1 Million elements, while Merge Sort requires ~20 Million operations, a parallel Bitonic Network finishes in exactly 400 clock cycles!
"""

if __name__ == "__main__":
    demonstrate_bitonic_sort()
    print("\n[SUCCESS] Laboratory: Sorting Networks Completed.")
