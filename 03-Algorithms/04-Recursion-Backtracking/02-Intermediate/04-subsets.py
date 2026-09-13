"""
# ==============================================================================
# LABORATORY: SUBSETS (POWER SET) & BITMASKING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A "Subset" (or Power Set) is a mathematical concept. Given a set of elements 
# `[1, 2, 3]`, find ALL possible combinations of any length.
# This includes the empty set `[]` and the full set `[1, 2, 3]`.
#
# How many subsets are there? Exactly 2^N.
# Why? Because for every single element, you make a binary decision: 
# "Do I INCLUDE it in this subset, or EXCLUDE it?"
# 3 elements * 2 decisions each = 2 * 2 * 2 = 8 subsets.
#
# Because there are exactly 2^N combinations, we can generate them using two 
# completely different algorithms:
# 1. Backtracking (The "Pick or Don't Pick" Decision Tree).
# 2. Bitmasking (Using raw binary numbers `000` to `111` to instantly map 
#    hardware bits directly to array indices!).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Implement Subsets via Backtracking (Include/Exclude branches).
# - Master Bitmasking subset generation.
# - Concept: Deduplication for Subsets II.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BACKTRACKING (PICK OR DON'T PICK)
# ==============================================================================
def subsets_backtracking(nums: List[int]) -> List[List[int]]:
    """
    Time Complexity: O(N * 2^N)
    Space Complexity: O(N) Call Stack + O(N * 2^N) for output array.
    """
    results = []
    current_subset = []
    
    def backtrack(index: int):
        # 1. BASE CASE
        # If we have made an Include/Exclude decision for EVERY element...
        if index == len(nums):
            results.append(list(current_subset))
            return
            
        # 2. BRANCH 1: "INCLUDE" the element
        # --- CHOOSE ---
        current_subset.append(nums[index])
        # --- EXPLORE ---
        backtrack(index + 1)
        # --- UNCHOOSE ---
        current_subset.pop()
        
        # 3. BRANCH 2: "EXCLUDE" the element
        # We don't add anything. We just move to the next index!
        backtrack(index + 1)

    backtrack(0)
    return results

def demonstrate_backtracking():
    section_header("Algorithm: Subsets via Backtracking")
    
    nums = [1, 2, 3]
    print(f"Generating all subsets for {nums} using Backtracking:\n")
    
    results = subsets_backtracking(nums)
    for res in results:
        print(f" -> {res}")
        
    print(f"\nTotal Subsets: {len(results)} (Formula: 2^N = 2^3 = 8)")


# ==============================================================================
# 4. BITMASKING (THE HARDWARE HACK)
# ==============================================================================
def subsets_bitmasking(nums: List[int]) -> List[List[int]]:
    """
    Generates subsets using raw CPU Binary mathematics.
    Time Complexity: O(N * 2^N)
    Space Complexity: O(1) Auxiliary (Not counting output array).
    """
    n = len(nums)
    results = []
    
    # 1. The total number of subsets is exactly 2^N.
    # In Python, `1 << n` shifts a binary 1 to the left N times, which is exactly 2^N!
    total_subsets = 1 << n
    
    # 2. Loop from 0 to 7 (for an array of size 3).
    # Binary representation:
    # 0 = 000 (Exclude all)
    # 1 = 001 (Include index 0)
    # 2 = 010 (Include index 1)
    # 3 = 011 (Include index 0 and 1)
    # ...
    # 7 = 111 (Include all)
    for mask in range(total_subsets):
        current_subset = []
        
        # 3. For this specific mask, check every bit (0 to N-1).
        for i in range(n):
            # If the i-th bit in `mask` is a 1...
            if (mask & (1 << i)) != 0:
                # Include the element!
                current_subset.append(nums[i])
                
        results.append(current_subset)
        
    return results

def demonstrate_bitmasking():
    section_header("Algorithm: Subsets via Bitmasking")
    
    nums = ["A", "B", "C"]
    print(f"Generating all subsets for {nums} using Bitmasking:\n")
    
    results = subsets_bitmasking(nums)
    for mask, res in enumerate(results):
        # Format the mask to show 3 binary digits (e.g. 000, 001)
        binary_str = format(mask, '03b')
        print(f" Mask: {binary_str}  ->  {res}")
        

# ==============================================================================
# 5. SUBSETS II (HANDLING DUPLICATES)
# ==============================================================================
def subsets_with_duplicates(nums: List[int]) -> List[List[int]]:
    """
    If the array is [1, 2, 2], we shouldn't output [1, 2] twice!
    """
    # CRITICAL: Must sort first so duplicates are adjacent!
    nums.sort()
    
    results = []
    current_subset = []
    
    def backtrack(index: int):
        # Unlike the previous backtracking, we append to results AT EVERY STEP.
        # Every node in the decision tree is a valid subset!
        results.append(list(current_subset))
        
        # Loop from the current index to the end
        for i in range(index, len(nums)):
            
            # --- DEDUPLICATION PRUNING ---
            # If this is a duplicate element, AND it's not the first element in 
            # this specific recursive loop (`i > index`), skip it!
            if i > index and nums[i] == nums[i - 1]:
                continue
                
            current_subset.append(nums[i])
            backtrack(i + 1)
            current_subset.pop()

    backtrack(0)
    return results


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the Time Complexity $O(N \\times 2^N)$ instead of just $O(2^N)$?
   Answer: There are mathematically $2^N$ subsets. However, to construct each subset, we must copy the temporary `current_subset` list into the final `results` array using `list(current_subset)`. An array copy is an $O(N)$ operation. We execute an $O(N)$ copy exactly $2^N$ times.

2. Which is better for generating Subsets: Backtracking or Bitmasking?
   Answer: For raw performance, Bitmasking is faster because bitwise operations `(1 << i)` are executed directly on the CPU hardware in 1 clock cycle, completely avoiding the overhead of OS Call Stacks and recursive function jumps. However, Backtracking is far more flexible. If you want to stop early, or apply complex "Pruning" rules, Backtracking is required.

3. Why do we append to `results` at the very beginning of the `backtrack()` function for Subsets II?
   Answer: Because for combinations/subsets, every single node in the recursion tree represents a valid partial subset! (Unlike Permutations, where we only append when we reach the very bottom of the tree `depth == N`).
"""

if __name__ == "__main__":
    demonstrate_backtracking()
    demonstrate_bitmasking()
    print("\n[SUCCESS] Laboratory: Subsets & Combinations Completed.")
