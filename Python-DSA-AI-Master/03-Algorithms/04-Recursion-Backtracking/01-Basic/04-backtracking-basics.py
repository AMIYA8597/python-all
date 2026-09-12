"""
Module: Backtracking Basics

Learning Objectives:
1. Understand the paradigm of backtracking.
2. Differentiate backtracking from plain recursion (making and unmaking choices).
3. Visualize the state-space tree and pruning.
4. Implement classic backtracking templates.

Concept Explanation:
Backtracking is an algorithmic technique for solving problems recursively by trying to build a solution incrementally.
If we realize that a partial solution cannot possibly be extended to a valid solution, we abandon it ("backtrack") and try another path.

Imports:
"""
from typing import List

def generate_binary_strings(n: int) -> List[str]:
    """Basic implementation: Generate all binary strings of length n."""
    result = []
    
    def backtrack(current_string: str):
        if len(current_string) == n:
            result.append(current_string)
            return
            
        # Try appending '0'
        backtrack(current_string + '0')
        # Try appending '1'
        backtrack(current_string + '1')
        
    backtrack("")
    return result

def subsets(nums: List[int]) -> List[List[int]]:
    """Intermediate implementation: Generate all subsets of a set (Combinations)."""
    result = []
    
    def backtrack(start: int, current_subset: List[int]):
        # Add the current subset to result (deep copy)
        result.append(list(current_subset))
        
        for i in range(start, len(nums)):
            # Make a choice
            current_subset.append(nums[i])
            # Recurse
            backtrack(i + 1, current_subset)
            # Undo the choice (Backtrack)
            current_subset.pop()
            
    backtrack(0, [])
    return result

def permutations(nums: List[int]) -> List[List[int]]:
    """Advanced implementation: Generate all permutations of a list."""
    result = []
    
    def backtrack(current_perm: List[int], used: List[bool]):
        if len(current_perm) == len(nums):
            result.append(list(current_perm))
            return
            
        for i in range(len(nums)):
            if used[i]:
                continue
                
            # Make choice
            used[i] = True
            current_perm.append(nums[i])
            
            # Recurse
            backtrack(current_perm, used)
            
            # Undo choice
            current_perm.pop()
            used[i] = False
            
    backtrack([], [False] * len(nums))
    return result

def performance_analysis():
    """Analyze time complexities."""
    print("Performance Analysis (State Space Size):")
    print("Binary Strings (n=3):", len(generate_binary_strings(3)), "Expected: 2^n")
    print("Subsets (n=3):", len(subsets([1, 2, 3])), "Expected: 2^n")
    print("Permutations (n=3):", len(permutations([1, 2, 3])), "Expected: n!")

def edge_cases():
    """Handle edge cases like empty inputs."""
    print("\nEdge Cases:")
    print(f"Empty list subsets: {subsets([])}")
    print(f"Empty list permutations: {permutations([])}")

def interview_challenge():
    """
    Challenge: N-Queens Problem formulation (basic).
    """
    print("\nInterview Challenge: N-Queens conceptually uses backtracking to place queens and prunes invalid paths.")

def run_tests():
    """Unit tests."""
    assert len(generate_binary_strings(3)) == 8
    assert len(subsets([1, 2])) == 4
    assert len(permutations([1, 2, 3])) == 6
    print("\nAll tests passed successfully.")

if __name__ == "__main__":
    print("--- Backtracking Basics ---\n")
    print(f"Subsets of [1, 2]: {subsets([1, 2])}")
    print("")
    performance_analysis()
    edge_cases()
    interview_challenge()
    run_tests()
