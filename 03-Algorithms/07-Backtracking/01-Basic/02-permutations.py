"""
# ==============================================================================
# LABORATORY: PERMUTATIONS (WITH AND WITHOUT DUPLICATES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Generating Permutations is the classic O(N!) Backtracking problem.
# If you have an array `[1, 2, 3]`, you must output all 6 possible orderings.
#
# In the previous lab (Combinations), order didn't matter. [1, 2] was identical 
# to [2, 1]. So we used a `start_index` to force the loop to only pick numbers 
# to the right.
# In Permutations, order DOES matter. [1, 2] is a different state than [2, 1].
# This means our inner `for` loop must scan the ENTIRE array every time, but we 
# must use a `visited` boolean array to prevent picking the exact same element 
# twice in the same path.
#
# The FAANG difficulty spike: What if the input has duplicates? e.g., `[1, 1, 2]`.
# A naive permutation algorithm will output `[1, 1, 2]` twice (once for the first 1, 
# once for the second 1).
# We must implement "Same-Level Pruning" to instantly terminate duplicate branches 
# in the State Space Tree without fully exploring them!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Combinatorial index constraints and 
#   Permutational `visited` arrays.
# - Master Same-Level Pruning for duplicate elements.
# - Understand why O(N!) time complexity is the physical limit.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ADVANCED PERMUTATIONS ENGINE (HANDLING DUPLICATES)
# ==============================================================================
def permute_unique(nums: List[int]) -> List[List[int]]:
    """
    Generates all UNIQUE permutations of an array that may contain duplicates.
    
    Time Complexity: O(N * N!) (N! permutations, and each takes O(N) to copy).
    Space Complexity: O(N) for the recursion stack and boolean array.
    """
    results = []
    current_path = []
    
    # 1. THE PRUNING REQUIREMENT
    # To easily skip duplicates, we MUST sort the array first.
    # This guarantees that identical numbers sit right next to each other.
    nums.sort()
    
    # We use a boolean array to track which physical elements are currently 
    # being used in the active recursive path.
    visited = [False] * len(nums)
    
    def backtrack():
        # 1. BASE CASE (SUCCESS)
        # If the path is exactly the length of the input array, we've used 
        # every element exactly once!
        if len(current_path) == len(nums):
            results.append(current_path[:])
            return
            
        # 2. THE EXPLORATION LOOP
        # For permutations, we always loop from 0 to N. We don't use a `start_index`.
        for i in range(len(nums)):
            
            # --- PATH VALIDATION ---
            # If we are already using this exact physical element in the current 
            # path, we obviously can't pick it again.
            if visited[i]:
                continue
                
            # --- SAME-LEVEL DUPLICATE PRUNING ---
            # This is the FAANG trick!
            # If the current number is IDENTICAL to the previous number...
            # AND the previous number is NOT VISITED (`visited[i-1] == False`)...
            # What does this mean physically in the tree?
            # It means we are on the exact same horizontal level of the tree, 
            # and we just finished fully exploring the branch for the previous 
            # identical number! There is ZERO mathematical reason to explore the 
            # exact same branch again. PRUNE IT!
            if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                continue
                
            # --- STEP A: MAKE A CHOICE ---
            visited[i] = True
            current_path.append(nums[i])
            
            # --- STEP B: EXPLORE ---
            backtrack()
            
            # --- STEP C: BACKTRACK ---
            current_path.pop()
            visited[i] = False


    backtrack()
    return results


def demonstrate_permutations():
    section_header("Algorithm: Permutations II (Handling Duplicates)")
    
    nums = [1, 1, 2]
    
    print(f"Input Array (Contains Duplicates): {nums}")
    print("\nExecuting Backtracking with Same-Level Pruning...")
    ans = permute_unique(nums)
    
    print(f"\nTotal Unique Permutations: {len(ans)}")
    for p in ans:
        print(f" -> {p}")
        
    print("\nIf we used Naive Permutations, we would have generated 6 results:")
    print("[1(A), 1(B), 2], [1(B), 1(A), 2], etc.")
    print("Because we sorted and checked `not visited[i-1]`, we instantly pruned ")
    print("the redundant branches, saving massive CPU cycles!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `not visited[i-1]` mean we are on the same level of the tree?
   Answer: This is a beautiful piece of logic. If `visited[i-1]` was `True`, it would mean the previous identical number is currently IN OUR PATH (e.g., we are building `[1, 1]`). This is totally valid! But if `visited[i-1]` is `False`, it means we just finished using it, we popped it, we backtracked back up to this level, and now the `for` loop is moving to index `i`. Because it's the exact same number, doing it again would generate the exact same permutation subtree! 

2. Could we just use a Python `set()` to store the results and avoid duplicates?
   Answer: Yes, you could. But that is considered a "Naive" or "Brute Force" solution in an interview. If the array is `[1, 1, 1, 1, 1, 1, 1, 2]`, there are 8 elements (8! = 40,320 naive permutations), but only 8 unique permutations! If you use a Set, your algorithm will blindly execute 40,320 recursive calls, taking huge amounts of time, just for the Set to throw 40,312 of them away. Pruning prevents the recursive calls from even happening.

3. Is $O(N!)$ always bad?
   Answer: Yes, factorials grow faster than exponentials. $10!$ is 3.6 million. $15!$ is 1.3 trillion. $20!$ is 2.4 quintillion. You can NEVER run a permutation algorithm on an array larger than 12 or 13 elements, no matter how fast your computer is. It is the absolute physical limit of computation.
"""

if __name__ == "__main__":
    demonstrate_permutations()
    print("\n[SUCCESS] Laboratory: Permutations Completed.")
