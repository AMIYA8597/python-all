"""
# ==============================================================================
# LABORATORY: MEDIAN OF MEDIANS (DETERMINISTIC O(N) SELECT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you learned Randomized Quickselect. It finds the K-th 
# smallest element in O(N) EXPECTED time.
# 
# However, if you are incredibly unlucky, your randomizer might pick the absolute 
# worst pivot (the smallest or largest element) every single time. The recursion 
# degrades to $O(N^2)$.
# 
# While this is statistically impossible in practice, Computer Scientists require 
# strict mathematical guarantees. In 1973, Blum, Floyd, Pratt, Rivest, and Tarjan 
# published a paper titled "Time Bounds for Selection".
#
# They invented the "Median of Medians" algorithm. It guarantees a STRICT O(N) 
# Worst-Case runtime, completely eliminating the $O(N^2)$ degradation!
#
# How does it work?
# Instead of picking a random pivot, it CALCULATES a mathematically "good" pivot.
# 1. Break the array into chunks of 5 elements.
# 2. Find the exact median of each 5-element chunk (using insertion sort).
# 3. Create a new array containing all those chunk medians.
# 4. Recursively call the algorithm to find the Median of the Medians!
# 5. Use that final Median of Medians as the Pivot!
#
# Why chunks of 5?
# Mathematics! Using chunks of 5 guarantees that the chosen pivot will be greater 
# than at least 30% of the elements, and less than at least 30% of the elements. 
# This mathematically forces the partition to split the array at WORST 30/70! 
# A 30/70 split geometrically decays fast enough to guarantee an absolute $O(N)$ 
# overall runtime.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 30/70 Partition Guarantee.
# - Implement the Chunk-of-5 reduction.
# - Master the Deterministic O(N) Quickselect architecture.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MEDIAN OF MEDIANS ENGINE (DETERMINISTIC O(N))
# ==============================================================================
def find_median_of_5(arr: List[int]) -> int:
    """
    Sorts a tiny array of maximum 5 elements and returns the median.
    Since N <= 5, this is technically O(1) time.
    """
    arr.sort() # Timsort is heavily optimized for tiny arrays
    return arr[len(arr) // 2]


def median_of_medians(arr: List[int], k: int) -> int:
    """
    Finds the K-th smallest element in STRICT O(N) worst-case time!
    Note: k is 1-indexed here! (e.g. k=1 means the absolute minimum element).
    """
    n = len(arr)
    
    # 1. BASE CASE
    # If the array is small enough, just sort it and return!
    if n <= 5:
        arr_sorted = sorted(arr)
        return arr_sorted[k - 1]
        
    # 2. CHUNK REDUCTION
    # Break the array into chunks of 5 elements each.
    medians = []
    for i in range(0, n, 5):
        chunk = arr[i : i + 5]
        medians.append(find_median_of_5(chunk))
        
    # 3. RECURSIVELY FIND THE MEDIAN OF MEDIANS!
    # We want the exact mathematical median of the `medians` array.
    # The median is the (length // 2 + 1)-th smallest element!
    pivot_value = median_of_medians(medians, len(medians) // 2 + 1)
    
    # 4. PARTITION THE ARRAY (Without moving elements in-place)
    # Since we are focusing on clarity over memory optimization, we will partition 
    # the array into three physical lists: Less, Equal, and Greater.
    less = []
    equal = []
    greater = []
    
    for x in arr:
        if x < pivot_value:
            less.append(x)
        elif x == pivot_value:
            equal.append(x)
        else:
            greater.append(x)
            
    # 5. RECURSIVE SELECTION (The Quickselect Logic)
    
    # If the K-th element falls within the `less` zone...
    if k <= len(less):
        return median_of_medians(less, k)
        
    # If the K-th element falls within the `equal` zone, WE FOUND IT!
    elif k <= len(less) + len(equal):
        return pivot_value
        
    # If the K-th element is in the `greater` zone...
    else:
        # We must adjust K! Since we are throwing away the `less` and `equal` 
        # zones, the 10th smallest element overall might become the 3rd smallest 
        # element inside the `greater` zone!
        new_k = k - len(less) - len(equal)
        return median_of_medians(greater, new_k)


def demonstrate_median_of_medians():
    section_header("Algorithm: Median of Medians (Deterministic Quickselect)")
    
    # An unsorted array
    data = [12, 3, 5, 7, 4, 19, 26, 2, 8, 1, 15, 11]
    print(f"Dataset: {data}")
    print(f"Sorted Dataset (For visual verification): {sorted(data)}")
    
    # Let's find the 4th smallest element
    k = 4
    print(f"\nFinding the {k}th smallest element...")
    ans = median_of_medians(data, k)
    
    print(f"Result: {ans}")
    print(f"Verification: Index 3 of sorted array is {sorted(data)[3]}!")
    
    # Let's find the exact Median of the dataset
    median_k = len(data) // 2 + 1
    print(f"\nFinding the exact Median (K = {median_k})...")
    ans_med = median_of_medians(data, median_k)
    print(f"Result: {ans_med}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the algorithm break the array into chunks of 5? Why not 3 or 7?
   Answer: It's purely mathematical optimization. 
   - If we use chunks of 3, the math proves the worst-case partition is 33/67. This decays too slowly, and the recursive overhead actually causes the time complexity to degrade slightly worse than $O(N)$. 
   - If we use chunks of 5, the worst-case partition is strictly bounded at 30/70. The recurrence relation $T(n) = T(n/5) + T(7n/10) + O(N)$ mathematically evaluates to strict $O(N)$. 
   - We could use chunks of 7, 9, or 11 (which provide even better 25/75 or 20/80 bounds), but sorting a 11-element chunk is significantly slower than sorting a 5-element chunk. 5 is the mathematical "sweet spot" that minimizes sorting overhead while guaranteeing $O(N)$ decay.

2. How do we know the Median of Medians guarantees a 30/70 split?
   Answer: Imagine a 5x5 grid of elements. Sort each column vertically, then sort the columns horizontally by their median. The absolute center element is the Median of Medians. 
   Because of the sorting, the top-left quadrant is mathematically guaranteed to be smaller than the center, and the bottom-right quadrant is guaranteed to be larger! These quadrants contain exactly 30% of the elements. Therefore, the pivot is guaranteed to have at least 30% of elements smaller than it, and at least 30% larger. The worst possible split is throwing away 30% and recursing on 70%.

3. If Median of Medians is $O(N)$ worst-case, why is `randomized_quickselect` used in production?
   Answer: The Constant Factors! The Median of Medians algorithm creates a ton of overhead: slicing arrays into chunks of 5, sorting those chunks, building a new median array, and running a massive secondary recursion just to find the pivot. This massive constant overhead makes it run 5x to 10x slower than Randomized Quickselect in reality. Randomized Quickselect has no overhead; it just picks a random number and partitions. Because the random worst-case $O(N^2)$ is effectively impossible on modern hardware, we trade the strict mathematical guarantee for raw speed.
"""

if __name__ == "__main__":
    demonstrate_median_of_medians()
    print("\n[SUCCESS] Laboratory: Median of Medians Completed.")
