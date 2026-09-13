"""
# ==============================================================================
# LABORATORY: PERMUTATIONS & IN-PLACE SWAPPING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A "Permutation" is all the possible ways to arrange a set of items where 
# ORDER MATTERS. (e.g. "ABC" is different from "CBA").
# 
# The number of permutations of N items is exactly N! (N Factorial). 
# For just 10 items, there are 3.6 Million permutations. For 13 items, there 
# are 6.2 Billion! Permutation algorithms are astronomically slow (O(N!)) and 
# should only be used on very small datasets (usually N <= 10).
#
# How do we generate them? We could use Backtracking with a `visited` Set to 
# track which numbers we have already used. But creating sets and creating copies 
# of arrays for every single recursive call wastes massive amounts of RAM.
#
# Instead, we can generate all Permutations strictly IN-PLACE. 
# We use a single array and physically swap elements. 
# We lock `arr[0]`, permute the rest. Then swap `arr[0]` with `arr[1]`, lock it, 
# and permute the rest!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master In-Place Swapping for Backtracking.
# - Understand the N! Time Complexity boundary.
# - Concept: Deduplication (How to handle arrays with duplicate elements).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PERMUTATIONS (IN-PLACE SWAPPING)
# ==============================================================================
def permute(arr: List[int]) -> List[List[int]]:
    """
    Generates all permutations of a unique array.
    Time Complexity: O(N * N!)
    Space Complexity: O(N) Call Stack (Output array not counted).
    """
    results = []
    
    def backtrack(start: int):
        # 1. BASE CASE (SUCCESS)
        # If `start` has reached the end of the array, the entire array is 
        # locked in a specific permutation!
        if start == len(arr):
            # Must append a COPY `arr[:]`, otherwise we append a memory pointer!
            results.append(arr[:])
            return
            
        # 2. CHOICES
        # We want to place every available element into the `start` position.
        # We do this by swapping `arr[start]` with `arr[i]`.
        for i in range(start, len(arr)):
            
            # --- CHOOSE ---
            arr[start], arr[i] = arr[i], arr[start]
            
            # --- EXPLORE ---
            # We have locked the `start` index. 
            # Recursively permute everything from `start + 1` to the end!
            backtrack(start + 1)
            
            # --- UNCHOOSE ---
            # We must revert the physical swap to restore the array 
            # so the next loop iteration is completely clean.
            arr[start], arr[i] = arr[i], arr[start]

    backtrack(0)
    return results

def demonstrate_permutations():
    section_header("Algorithm: Basic Permutations")
    
    arr = [1, 2, 3]
    print(f"Generating permutations for array: {arr}\n")
    
    results = permute(arr)
    for p in results:
        print(f" -> {p}")
        
    print(f"\nTotal Permutations: {len(results)} (Formula: 3! = 6)")


# ==============================================================================
# 4. PERMUTATIONS II (HANDLING DUPLICATES)
# ==============================================================================
def permute_unique(arr: List[int]) -> List[List[int]]:
    """
    Generates all UNIQUE permutations of an array that contains duplicates.
    Example: [1, 1, 2] should not generate [1, 1, 2] twice.
    """
    # CRITICAL: We MUST sort the array first so identical elements are adjacent!
    arr.sort()
    
    results = []
    current_path = []
    visited = [False] * len(arr)
    
    def backtrack():
        if len(current_path) == len(arr):
            results.append(list(current_path))
            return
            
        for i in range(len(arr)):
            # If we already used this exact element in the current path, skip it.
            if visited[i]:
                continue
                
            # THE DEDUPLICATION PRUNING CHECK
            # If the current element is identical to the previous element...
            # AND the previous element was NOT visited in this specific depth branch...
            # It means we ALREADY generated a full recursion tree for this exact number!
            # Skip it to prevent duplicate answers.
            if i > 0 and arr[i] == arr[i - 1] and not visited[i - 1]:
                continue
                
            # --- CHOOSE ---
            visited[i] = True
            current_path.append(arr[i])
            
            # --- EXPLORE ---
            backtrack()
            
            # --- UNCHOOSE ---
            visited[i] = False
            current_path.pop()

    backtrack()
    return results

def demonstrate_permutations_unique():
    section_header("Algorithm: Unique Permutations (Deduplication)")
    
    arr = [1, 1, 2]
    print(f"Generating UNIQUE permutations for array with duplicates: {arr}\n")
    
    results = permute_unique(arr)
    for p in results:
        print(f" -> {p}")
        
    print(f"\nNotice how it only printed 3 answers, perfectly skipping the identical duplicates!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the Time Complexity $O(N \\times N!)$ and not just $O(N!)$?
   Answer: There are mathematically $N!$ permutations generated. However, when the Base Case is hit `if start == len(arr):`, we execute `results.append(arr[:])`. Creating a physical copy of an array takes $O(N)$ time. Therefore, we do an $O(N)$ operation exactly $N!$ times.

2. Why did we use In-Place Swapping for Unique Elements, but a `visited` array for Duplicate Elements?
   Answer: In-Place Swapping physically scrambles the array. If the array had duplicates, scrambling it would separate identical elements, completely breaking the `arr[i] == arr[i-1]` deduplication check! To safely deduplicate, the array MUST remain perfectly sorted at all times. A `visited` array allows us to pick elements out of order while preserving the physical sorted structure of the source array.

3. What is the difference between Permutations and Combinations?
   Answer: Permutations: Order MATTERS (Lock code `123` is different from `321`). Combinations: Order does NOT matter (A fruit salad with `Apple, Banana` is identical to `Banana, Apple`). Combination algorithms use a `start_index` to forcefully push the recursion forward, preventing it from ever looking backwards, which naturally eliminates reverse-ordered duplicates.
"""

if __name__ == "__main__":
    demonstrate_permutations()
    demonstrate_permutations_unique()
    print("\n[SUCCESS] Laboratory: Permutations Completed.")
