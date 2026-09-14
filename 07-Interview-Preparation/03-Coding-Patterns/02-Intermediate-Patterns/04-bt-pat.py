"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - BACKTRACKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Given an array [1, 2, 3], return all possible permutations."
#
# A junior engineer tries to write three nested `for` loops. But what if the 
# input array has 10 elements? You cannot dynamically write 10 nested loops.
# You MUST use Recursion to mathematically traverse a "Decision Tree".
#
# Backtracking is an algorithmic technique for solving problems recursively by 
# trying to build a solution incrementally, one piece at a time, and removing 
# those solutions that fail to satisfy the constraints of the problem at any point 
# in time ("backtracking" to the previous state).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Backtracking State Machine (`Choose -> Explore -> Un-Choose`).
# - Master the 'Subsets' algorithmic pattern.
# - Master the 'Permutations' algorithmic pattern.
# - Understand why `result.append(path[:])` is mathematically required.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BACKTRACKING: SUBSETS (THE POWER SET)
# ==============================================================================
def subsets(nums: List[int]) -> List[List[int]]:
    """
    Time: O(N * 2^N) | Space: O(N) for recursion stack.
    Generates all possible subsets of an array.
    Decision Tree: At every number, we make a binary choice: "Include it, or Skip it."
    """
    result = []
    
    def backtrack(index: int, current_path: List[int]):
        # The 'Base Case': We have made a decision for every single element.
        if index >= len(nums):
            print(f"    [LEAF] Path constructed: {current_path}")
            # CRITICAL: We MUST append a DEEP COPY of the current path!
            # If we just do `result.append(current_path)`, we append a Pointer.
            # When the path mathematically un-chooses and empties itself, the 
            # final result matrix will just be full of empty arrays!
            result.append(current_path[:])
            return
            
        print(f"  Node {index}: Current path {current_path}. Making decision for {nums[index]}")
            
        # DECISION 1: Include the current number! (CHOOSE)
        current_path.append(nums[index])
        # Explore down that branch! (EXPLORE)
        backtrack(index + 1, current_path)
        
        # DECISION 2: Skip the current number! (UN-CHOOSE / BACKTRACK)
        # We physically delete the number from our memory array!
        removed = current_path.pop()
        print(f"  Node {index}: Backtracking! Removed {removed}. Path is now {current_path}.")
        # Explore down the alternative branch! (EXPLORE)
        backtrack(index + 1, current_path)
        
    print("  Initializing Decision Tree (Include vs Skip)...")
    backtrack(0, [])
    return result

def demonstrate_subsets():
    section_header("Backtracking: Subsets (Include vs Skip)")
    
    nums = [1, 2, 3]
    print(f"Array: {nums}\n")
    
    result = subsets(nums)
    print(f"\nResult: Total {len(result)} Subsets generated:")
    print(result)


# ==============================================================================
# 4. BACKTRACKING: PERMUTATIONS (FACTORIAL SCALING)
# ==============================================================================
def permutations(nums: List[int]) -> List[List[int]]:
    """
    Time: O(N * N!) | Space: O(N)
    Generates all possible orderings of an array.
    """
    result = []
    
    def backtrack(current_path: List[int]):
        # Base Case: The path contains exactly N elements!
        if len(current_path) == len(nums):
            result.append(current_path[:])
            return
            
        # We must loop through ALL available elements for this specific position.
        for num in nums:
            # We can't reuse a number we already placed in the permutation!
            if num in current_path:
                continue
                
            # 1. CHOOSE
            current_path.append(num)
            
            # 2. EXPLORE
            backtrack(current_path)
            
            # 3. UN-CHOOSE (BACKTRACK)
            current_path.pop()
            
    backtrack([])
    return result

def demonstrate_permutations():
    section_header("Backtracking: Permutations (N!)")
    
    nums = ['A', 'B', 'C']
    print(f"Array: {nums}\n")
    
    result = permutations(nums)
    print(f"\nResult: Total {len(result)} Permutations generated:")
    for p in result: print(f"  {p}")


def run_all_labs():
    demonstrate_subsets()
    demonstrate_permutations()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why MUST you append `path[:]` to the results array instead of just `path`?"
   Senior Answer: "In Python, a List is passed and stored by Reference (a physical memory Pointer). The `path` variable is a single, mutable array in RAM that is constantly being modified, appended to, and popped from by the algorithmic State Machine as it traverses the tree. If you write `result.append(path)`, you are simply appending 8 identical pointers to the exact same physical array. When the algorithmic tree finishes, it physically empties the array to backtrack to the absolute root. Therefore, your final output will print out `[[], [], []]`. By writing `path[:]` (or `list(path)`), you force the CPU to allocate a brand new, isolated block of RAM, permanently freezing a 'snapshot' of the data at that exact microsecond."

2. Interviewer: "What is the algorithmic difference between 'Subsets' and 'Permutations'?"
   Senior Answer: "Subsets scales at $O(2^N)$. It is a strict Binary Decision Tree. At every index, you make exactly two choices: 'Include it, or Skip it'. The relative order of elements is preserved, but the size of the result varies. Permutations scales at $O(N!)$ (Factorial). It requires you to place *every* element, but in every possible mathematical order. Therefore, you do not pass an `index` variable down the tree. Instead, at every node, you iterate through the *entire* array, check if the element has already been used (`if num in path`), and branch outward. The first position has $N$ choices, the second has $N-1$ choices, creating an explosion of factorial combinations."

3. Interviewer: "When writing the Permutations algorithm, `if num in path` takes $O(N)$ time. Can we optimize this?"
   Senior Answer: "Yes. Using `if num in path` is perfectly fine for small arrays, but as $N$ grows, scanning the array at every single node of the $N!$ tree is algorithmically devastating. We can optimize it by maintaining an external boolean array (e.g., `visited = [False] * N`), or a Bitmask, or a Hash Set. Before exploring, we mark `visited[i] = True`. After backtracking, we un-choose it by marking `visited[i] = False`. This reduces the $O(N)$ lookup to a perfect $O(1)$ Hash or Array access, drastically accelerating the backtracking engine."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Backtracking) Completed.")
