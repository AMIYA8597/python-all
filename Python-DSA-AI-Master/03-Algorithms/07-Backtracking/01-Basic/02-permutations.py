"""
## A. Concept Name
Permutations (Backtracking)

## B. Concept Explanation
A permutation of a set is an arrangement of its members into a sequence or linear order. 
For a given list of distinct integers, backtracking can be used to generate all possible permutations by building the sequence one element at a time and swapping elements.

## C. Use Cases
1. Generating all possible arrangements of items.
2. Brute-force searching for problems like the Traveling Salesperson Problem (TSP).
3. Solving puzzles like Sudoku or Cryptarithmetic.

## D. Code Implementation
Below is a foundational implementation of generating permutations using backtracking.

## X. Project Connection
Permutations are often required in optimization projects where all possible combinations of variables or routes need to be evaluated to find the best outcome, such as in logistics and route planning systems.
"""

def permute(nums):
    """
    Generate all permutations of a given list of distinct integers.
    
    Args:
        nums: List[int] - A list of distinct integers.
        
    Returns:
        List[List[int]] - A list containing all possible permutations.
    """
    def backtrack(first = 0):
        # if all integers are used up
        if first == n:  
            output.append(nums[:])
        for i in range(first, n):
            # place i-th integer first 
            # in the current permutation
            nums[first], nums[i] = nums[i], nums[first]
            # use next integers to complete the permutations
            backtrack(first + 1)
            # backtrack
            nums[first], nums[i] = nums[i], nums[first]
    
    n = len(nums)
    output = []
    backtrack()
    return output

if __name__ == "__main__":
    nums = [1, 2, 3]
    print(f"Permutations of {nums}:")
    for p in permute(nums):
        print(p)
