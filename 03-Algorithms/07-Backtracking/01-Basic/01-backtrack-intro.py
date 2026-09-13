"""
# ==============================================================================
# LABORATORY: BACKTRACKING (THE STATE SPACE TREE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen Greedy Algorithms (which pick the absolute best option and NEVER 
# look back) and Dynamic Programming (which exhaustively calculates every option 
# but uses caching to avoid recalculating).
#
# What if you CAN'T use DP because there are no "Overlapping Subproblems"?
# What if the problem physically requires you to output every single valid 
# combination, permutation, or path? (e.g., Output every possible password, 
# or solve a Sudoku board).
#
# Welcome to Backtracking.
# Backtracking is an algorithmic paradigm that systematically searches the 
# "State Space Tree" using Depth-First Search (DFS).
#
# The Core Philosophy is simple: 
# 1. MAKE A CHOICE (e.g., "Place a Queen here", "Pick the letter A").
# 2. RECURSIVELY EXPLORE (Dive deeper into the tree with that choice active).
# 3. UN-MAKE THE CHOICE (Backtrack! Remove the Queen, erase the letter A, 
#    so you can try the next choice).
#
# By physically un-making choices, a single array or grid can be reused 
# billions of times in memory, keeping Space Complexity incredibly low (O(N)), 
# even though the Time Complexity is astronomical (O(2^N) or O(N!)).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the "Choose -> Explore -> Unchoose" paradigm.
# - Visualize the State Space Tree.
# - Implement standard Combinations (nCr).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BACKTRACKING ENGINE (COMBINATIONS nCr)
# ==============================================================================
def combine(n: int, k: int) -> List[List[int]]:
    """
    Finds all possible combinations of `k` numbers out of the range 1 to `n`.
    E.g. If n=4, k=2: [1,2], [1,3], [1,4], [2,3], [2,4], [3,4]
    
    Time Complexity: O(k * (nCr)) - Generating the combinations and copying the array.
    Space Complexity: O(k) for the recursion stack and the `current_path` array!
    """
    
    results = []
    
    # We use a single shared list to track our current path.
    # We will append to it, and pop from it (Backtrack).
    current_path = []
    
    def backtrack(start_num: int):
        # 1. THE BASE CASE (SUCCESS)
        # Did our current path reach the required length `k`?
        if len(current_path) == k:
            # We MUST append a COPY (or slice `[:]`) of the array to results!
            # If we just append `current_path`, we are appending a memory reference.
            # When we pop from it later, the result inside `results` will be destroyed!
            results.append(current_path[:])
            return
            
        # 2. THE EXPLORATION LOOP
        # We loop from the `start_num` up to `n`.
        # (By enforcing `start_num`, we prevent permutations like [2,1] from 
        # appearing if we already generated [1,2]. This is crucial for Combinations!).
        for num in range(start_num, n + 1):
            
            # --- STEP A: MAKE A CHOICE ---
            # Lock the number into our path.
            current_path.append(num)
            
            # --- STEP B: RECURSIVELY EXPLORE ---
            # Dive deeper into the State Space Tree.
            # We pass `num + 1` so the next level ONLY picks numbers larger 
            # than the current one.
            backtrack(num + 1)
            
            # --- STEP C: UN-MAKE THE CHOICE (BACKTRACK) ---
            # We returned from the deep recursion. 
            # We MUST remove the number we just added so the loop can safely 
            # move on to the next number!
            current_path.pop()


    # Start the engine at number 1
    backtrack(1)
    
    return results


def demonstrate_backtracking():
    section_header("Algorithm: Backtracking (Combinations nCr)")
    
    n = 4
    k = 2
    
    print(f"Generating all combinations of {k} numbers out of 1 to {n}...")
    ans = combine(n, k)
    
    print(f"\nTotal Combinations: {len(ans)}")
    print("Combinations:")
    for combo in ans:
        print(f" -> {combo}")
        
    print("\nVisualizing the State Space Tree for n=4, k=2:")
    print("                 []")
    print("       /      /      \\      \\")
    print("     [1]    [2]      [3]    [4]")
    print("    / | \\   / \\       |      (Pruned)")
    print(" [1,2][1,3][1,4] [2,3][2,4] [3,4]")
    print(" (Backtrack occurs after every leaf node is hit!)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we MUST use `current_path[:]` when appending to results?
   Answer: In Python, Lists are passed and stored by Reference. If you do `results.append(current_path)`, the `results` list holds a pointer to the exact physical RAM location of `current_path`. When the backtracking algorithm subsequently executes `current_path.pop()`, it deletes the data at that RAM location! When the algorithm finishes, `results` will just print `[[], [], []]`. By using `[:]` or `.copy()`, we freeze a deep copy of the state at that exact millisecond.

2. What is "Pruning" (Bounding Function)?
   Answer: Look at the Tree diagram. Notice that node `[4]` is marked as "(Pruned)". If we are at `[4]`, the length of the path is 1. We need $k=2$. But there are no numbers left after 4! Therefore, exploring the `[4]` branch is a complete waste of CPU cycles. We can add an `if` statement to mathematically prevent the recursion from entering dead branches, massively speeding up the algorithm. 

3. How does Backtracking differ from pure Depth-First Search (DFS)?
   Answer: They are fundamentally the same mechanism (Recursion using the Call Stack). However, "DFS" usually refers to traversing a physical graph that already exists in memory (like an Adjacency List). "Backtracking" refers to dynamically GENERATING an abstract "State Space Tree" on the fly, and systematically creating/destroying the state (`append` / `pop`) as you traverse it.
"""

if __name__ == "__main__":
    demonstrate_backtracking()
    print("\n[SUCCESS] Laboratory: Backtracking Intro Completed.")
