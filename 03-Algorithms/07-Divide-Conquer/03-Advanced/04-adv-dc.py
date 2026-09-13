"""
# ==============================================================================
# LABORATORY: MEDIAN OF MEDIANS (DETERMINISTIC O(N) SELECTION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you want to find the K-th smallest number in an array, sorting the array 
# takes O(N log N) time.
#
# Can we do it in O(N) time?
# Yes! "Quickselect" uses the exact same partitioning logic as Quick Sort, but 
# instead of recursively sorting BOTH halves, it only recurses into the half 
# where the K-th element lives!
# This drops the time from O(N log N) to O(N) on average.
#
# BUT, just like Quick Sort, if the randomly chosen Pivot is terrible (e.g. the 
# absolute largest element every time), Quickselect collapses into O(N^2) time.
#
# In 1973, five of the greatest computer scientists (Blum, Floyd, Pratt, Rivest, 
# and Tarjan) invented the "Median of Medians" algorithm to guarantee a perfect 
# O(N) worst-case time!
#
# 1. DIVIDE the array into chunks of 5 elements.
# 2. Sort each tiny chunk and find its median (O(1) time).
# 3. Recursively call the algorithm to find the True Median of those Medians.
# 4. Use that True Median as the Pivot for the partition!
#
# Mathematics guarantees this pivot will discard at least 30% of the array 
# every single time, absolutely shattering the O(N^2) worst-case!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the limits of Randomized Quickselect.
# - Implement the chunks-of-5 deterministic pivot strategy.
# - Understand how overlapping recurrences bound to O(N).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MEDIAN OF MEDIANS ENGINE (O(N))
# ==============================================================================
def median_of_medians(nums: List[int], k: int) -> int:
    """
    Finds the K-th smallest element in O(N) guaranteed worst-case time.
    Note: `k` is 1-indexed for human readability.
    """
    
    # 1. BASE CASE (Array is small enough to just sort)
    if len(nums) <= 5:
        return sorted(nums)[k - 1]
        
    # 2. DIVIDE (Chunks of 5)
    # Why exactly 5? It is the mathematical sweet spot. 
    # If we used 3, the recurrence T(N/3) + T(2N/3) + O(N) diverges to O(N log N).
    # If we used 7, it works, but the constant factor overhead is slower than 5.
    sublists = [nums[i:i + 5] for i in range(0, len(nums), 5)]
    
    medians = []
    for sublist in sublists:
        sublist.sort()
        medians.append(sublist[len(sublist) // 2])
        
    # 3. CONQUER (Recursive call to find the Median of Medians!)
    # We find the mathematical midpoint of the medians array.
    pivot = median_of_medians(medians, len(medians) // 2 + 1)
    
    # 4. PARTITION (Use the Guaranteed Good Pivot)
    # We don't need a random index. We use the actual value `pivot` to split 
    # the original array into 3 buckets!
    lows = [el for el in nums if el < pivot]
    highs = [el for el in nums if el > pivot]
    pivots = [el for el in nums if el == pivot] # Handles duplicates!
    
    # 5. RECURSIVE SELECTION
    # Which bucket does the K-th element live in?
    if k <= len(lows):
        # It lives in the left bucket!
        return median_of_medians(lows, k)
    elif k > len(lows) + len(pivots):
        # It lives in the right bucket!
        # We must adjust K to strip away the left and middle elements.
        return median_of_medians(highs, k - len(lows) - len(pivots))
    else:
        # It IS the pivot! We found it!
        return pivot


def demonstrate_median_of_medians():
    section_header("Algorithm: Median of Medians (Deterministic O(N))")
    
    # An unsorted array of 15 elements
    nums = [12, 3, 5, 7, 4, 19, 26, 21, 39, 14, 1, 8, 17, 10, 2]
    
    print(f"Unsorted Input Array: {nums}")
    print(f"Sorted Verification : {sorted(nums)}")
    
    # Let's find the 7th smallest element (Expected: 8)
    k = 7
    print(f"\nExecuting O(N) Divide & Conquer for K={k}...")
    ans = median_of_medians(nums, k)
    
    print(f"The {k}th smallest element is: {ans}")
    
    # Let's find the 14th smallest element (Expected: 26)
    k2 = 14
    ans2 = median_of_medians(nums, k2)
    print(f"The {k2}th smallest element is: {ans2}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Recurrence Relation for Median of Medians?
   Answer: 
   Step 1: Divide into chunks of 5 and sort them takes $O(N)$.
   Step 2: Recursively find the median of the $N/5$ medians takes $T(N/5)$.
   Step 3: Partitioning takes $O(N)$.
   Step 4: Because the pivot is mathematically guaranteed to be greater than at least 30% of the array and less than at least 30% of the array, the worst-case recursive call for the bucket takes $T(7N/10)$.
   Total: $T(N) = T(N/5) + T(7N/10) + O(N)$.
   Since $(N/5) + (7N/10) = 9N/10$, the fractions sum to less than 1. By recursion tree induction, this perfectly collapses into $O(N)$!

2. If this is mathematically superior, why does Python's standard library not use it?
   Answer: Constant Factors! The Median of Medians algorithm has a massive amount of overhead: allocating small arrays of 5, sorting them, copying the medians into a new array, recursively calling itself, and generating 3 new lists for partitioning. A Randomized Quickselect algorithm achieves $O(N)$ with practically zero memory overhead and blistering fast $O(1)$ hardware swaps. The theoretical $O(N^2)$ worst-case of random pivoting is so astronomically rare in reality that engineers happily accept the risk in exchange for the 10x faster constant speed.

3. When would you actually use this in a FAANG interview?
   Answer: You likely will never be asked to write the full Median of Medians algorithm on a whiteboard. However, you are HIGHLY likely to be asked: "How can you guarantee Quickselect doesn't hit $O(N^2)$?" Verbally explaining the chunks-of-5 algorithm and the $T(N/5) + T(7N/10)$ math will instantly flag you as a senior-level candidate who understands theoretical bounds.
"""

if __name__ == "__main__":
    demonstrate_median_of_medians()
    print("\n[SUCCESS] Laboratory: Advanced Divide & Conquer Completed.")
