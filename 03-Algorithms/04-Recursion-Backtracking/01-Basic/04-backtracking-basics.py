"""
# ==============================================================================
# LABORATORY: BACKTRACKING FUNDAMENTALS (CHOOSE, EXPLORE, UNCHOOSE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen Recursion. But what happens if you need to search through a massive 
# tree of possibilities to find a valid solution (like solving a Maze, Sudoku, 
# or finding all Permutations of a password)?
#
# You use "Backtracking".
# Backtracking is just Recursion applied to a State Space Tree. It follows a 
# strict 3-step paradigm:
# 1. CHOOSE: Make a decision and modify the current State (e.g. add a letter).
# 2. EXPLORE: Recursively call the function to continue down that path.
# 3. UNCHOOSE: The recursion returned! Either the path failed, or we found a 
#    solution. We MUST undo the decision we made in step 1 (remove the letter) 
#    so we can test the next possible decision!
#
# If you forget the "Unchoose" step, your State object becomes permanently corrupted.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Choose -> Explore -> Unchoose paradigm.
# - Understand why we must `path.pop()`.
# - Implement generating all Binary Strings of length N.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BACKTRACKING TEMPLATE
# ==============================================================================
def generate_binary_strings(n: int) -> List[str]:
    """
    Generates all possible combinations of '0's and '1's of length N.
    Time Complexity: O(2^N)
    Space Complexity: O(N) Call Stack + O(2^N) to hold the final answers.
    """
    all_results = []
    
    # We use a mutable List to act as our "State". 
    # Strings in Python are Immutable. If we used strings, every `+` operation 
    # would create a brand new copy of the string in RAM, causing heavy O(N^2) 
    # memory overhead.
    current_path = []
    
    def backtrack(depth: int):
        # 1. THE BASE CASE (SUCCESS)
        # If the depth equals N, we have constructed a full string!
        if depth == n:
            # WARNING: You MUST append a COPY of `current_path`.
            # If you just do `all_results.append(current_path)`, you are appending 
            # a memory reference to the exact same list. When the recursion 
            # eventually modifies that list, your saved answer will change too!
            all_results.append("".join(current_path))
            return
            
        # 2. THE BRANCHING CHOICES
        # At this specific depth in the tree, what are our valid choices?
        # We can either place a '0' or a '1'.
        for choice in ['0', '1']:
            
            # --- CHOOSE ---
            # Modify the state with our choice
            current_path.append(choice)
            
            # --- EXPLORE ---
            # Recursively dive deeper into the tree with this new state
            backtrack(depth + 1)
            
            # --- UNCHOOSE (BACKTRACK) ---
            # The recursion returned! We are back at this exact level of the tree.
            # We MUST revert the state so the `for` loop can try the next choice.
            current_path.pop()

    # Kick off the recursion from depth 0
    backtrack(0)
    
    return all_results

def demonstrate_backtracking():
    section_header("Algorithm: Basic Backtracking (Binary Strings)")
    
    n = 3
    print(f"Generating all binary strings of length {n}...")
    
    results = generate_binary_strings(n)
    
    print(f"\nFound {len(results)} solutions:")
    for res in results:
        print(f" -> {res}")
        
    print("\nNotice how the algorithm perfectly exhausts all paths starting with '0'")
    print("before backtracking all the way to the top and trying paths starting with '1'.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must you append `path[:]` or `"".join(path)` instead of just appending `path` to the final results array?
   Answer: Pass-by-Reference trap! A Python list `[]` is a mutable object stored at a specific memory address. When you `append(path)`, you are just appending a pointer to that address. As the backtracking algorithm continues, it `pop()`s and `append()`s elements to that exact same list. When the algorithm finishes, the list will be completely empty! You will print out `[[], [], []]`. You MUST create a deep copy or string copy to freeze the state at that moment in time.

2. Why use a `list` and `append/pop` instead of just passing strings `backtrack(path + "0")`?
   Answer: In Python, strings are Immutable. `path + "0"` takes $O(N)$ time because the CPU must allocate a brand new string in memory and copy all the characters over. `list.append()` takes $O(1)$ time. For deep recursive trees, creating thousands of string copies causes massive performance and memory degradation.

3. What is the difference between standard Recursion and Backtracking?
   Answer: Standard Recursion usually returns a value directly up the chain (e.g. `return n * func(n-1)`). Backtracking uses Recursion purely as a mechanism to explore a "Decision Tree" (Depth-First Search). It modifies a global/shared State variable, dives down a path, and then reverts the State variable when it returns.
"""

if __name__ == "__main__":
    demonstrate_backtracking()
    print("\n[SUCCESS] Laboratory: Backtracking Basics Completed.")
