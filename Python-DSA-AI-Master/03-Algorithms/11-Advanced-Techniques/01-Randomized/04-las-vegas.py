"""
Las Vegas Algorithms

Learning Objectives:
1. Define a Las Vegas algorithm and understand its properties.
2. Differentiate Las Vegas algorithms (deterministic correctness, probabilistic time) 
   from Monte Carlo algorithms.
3. Implement practical examples like Randomized QuickSort and the N-Queens problem.

Concept Explanation:
A Las Vegas algorithm is a randomized algorithm that always produces the correct result 
or informs about the failure, but the time taken is a random variable. The worst-case 
runtime may be theoretically infinite, but expected runtime is very fast.
"""

import random
from typing import List, Optional

# Basic Implementation: Finding an element in an array
def randomized_find(arr: List[int], target: int) -> int:
    """A naive Las Vegas algorithm to find an index of a target element."""
    if target not in arr:
        return -1
        
    while True:
        idx = random.randint(0, len(arr) - 1)
        if arr[idx] == target:
            return idx

# Intermediate Implementation: Randomized QuickSort
def las_vegas_quicksort(arr: List[int]) -> List[int]:
    """QuickSort with a random pivot is a Las Vegas algorithm."""
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return las_vegas_quicksort(left) + mid + las_vegas_quicksort(right)

# Advanced Implementation: Las Vegas N-Queens
def is_safe(board: List[int], row: int, col: int) -> bool:
    for r in range(row):
        c = board[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def las_vegas_n_queens(n: int) -> Optional[List[int]]:
    """Places N queens randomly. Returns None if dead end is reached."""
    board = [-1] * n
    for row in range(n):
        valid_cols = [col for col in range(n) if is_safe(board, row, col)]
        
        if not valid_cols:
            return None
            
        board[row] = random.choice(valid_cols)
    return board

def solve_n_queens(n: int) -> List[int]:
    """Repeatedly run the Las Vegas N-Queens until successful."""
    while True:
        solution = las_vegas_n_queens(n)
        if solution is not None:
            return solution

# Performance Analysis
def performance_analysis():
    """
    Time Complexity:
    - QuickSort: Expected O(N log N), Worst-case O(N^2)
    - N-Queens: Expected time depends on N. Restarting avoids deep backtracking.
    """
    pass

# Edge Cases
def edge_cases():
    """
    - Infinite loops if termination is impossible.
    """
    pass

# Interview Challenge
def challenge_bogo_sort(arr: List[int]) -> List[int]:
    """Challenge: BogoSort. Randomly shuffles until sorted."""
    def is_sorted(a):
        return all(a[i] <= a[i+1] for i in range(len(a)-1))
        
    a = arr.copy()
    iterations = 0
    while not is_sorted(a) and iterations < 1000:
        random.shuffle(a)
        iterations += 1
    return a

# Tests
def run_tests():
    arr = [1, 2, 3, 4, 5]
    idx = randomized_find(arr, 3)
    assert arr[idx] == 3
    assert randomized_find(arr, 10) == -1
    
    unsorted = [3, 1, 4, 1, 5, 9, 2]
    assert las_vegas_quicksort(unsorted) == [1, 1, 2, 3, 4, 5, 9]
    
    n_queens_solution = solve_n_queens(8)
    assert len(n_queens_solution) == 8
    
    bogo_res = challenge_bogo_sort([2, 1, 3])
    assert bogo_res == [1, 2, 3]
    
    print("All Las Vegas tests passed!")

if __name__ == "__main__":
    run_tests()
