"""
# ==============================================================================
# LABORATORY: ITERATIVE DEEPENING DFS (THE AI SEARCH ALGORITHM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# What if you want to find the shortest path to a target in a MASSIVE graph?
# 
# Problem 1: Depth First Search (DFS).
# DFS uses minimal memory (O(d) for the stack). But it plunges blindly. If the 
# graph is infinitely deep (like the state space of a Chess game), DFS will get 
# trapped exploring a useless branch forever and never find the target.
#
# Problem 2: Breadth First Search (BFS).
# BFS guarantees the shortest path because it searches layer by layer! But there 
# is a fatal flaw: The Queue. On the final layer `d`, the Queue must physically 
# store every single node in that layer in RAM. If the branching factor is 35 
# (Chess), layer 10 has 35^10 nodes. That's 2 Trillion Trillion nodes. The RAM 
# of your computer will explode instantly.
#
# The Solution: Iterative Deepening DFS (IDDFS).
# It is the ultimate hybrid algorithm. 
# We run a DFS, but we artificially FORCE it to stop at Depth 1. 
# If it fails, we restart from scratch and run a DFS with a limit of Depth 2.
# Then Depth 3... Depth 4...
#
# This gives us the Layer-by-Layer shortest path guarantee of BFS, but using 
# the microscopic O(d) memory footprint of DFS!
#
# Wait, isn't restarting from the root every single time incredibly inefficient?
# The mathematical irony is NO! The time complexity remains identically O(b^d).
# 
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the limits of BFS memory bounds.
# - Implement Depth-Limited DFS (DLS).
# - Implement the IDDFS outer loop.
# - Understand the mathematical proof of why the repeated work doesn't matter.
#
# ==============================================================================
"""

from typing import Dict, List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DEPTH-LIMITED SEARCH (DLS)
# ==============================================================================
def depth_limited_search(graph: Dict[int, List[int]], current: int, target: int, limit: int, path: List[int]) -> bool:
    """
    A standard DFS, but with a strict mathematical termination depth!
    """
    # 1. We found the target!
    if current == target:
        return True
        
    # 2. We hit the physical limit! Do not explore any deeper. Backtrack!
    if limit <= 0:
        return False
        
    # 3. Standard DFS Exploration
    for neighbor in graph.get(current, []):
        path.append(neighbor)
        
        # Recurse, but DECREMENT the limit!
        if depth_limited_search(graph, neighbor, target, limit - 1, path):
            return True
            
        # Backtrack the path if this branch failed
        path.pop()
        
    return False


# ==============================================================================
# 4. ITERATIVE DEEPENING DFS (IDDFS)
# ==============================================================================
def iddfs(graph: Dict[int, List[int]], start: int, target: int, max_depth: int) -> Optional[List[int]]:
    """
    Time Complexity: O(b^d) where b is branching factor, d is depth of target.
    Space Complexity: O(d) for the exact depth of the recursion stack!
    """
    
    # 1. THE ITERATIVE DEEPENING LOOP
    for limit in range(max_depth + 1):
        
        print(f"-> Launching DLS Engine with Depth Limit: {limit}...")
        
        # Re-initialize the path for this completely fresh run
        path = [start]
        
        # Fire the Depth-Limited Search!
        if depth_limited_search(graph, start, target, limit, path):
            print(f"Target found at depth {limit}!")
            return path
            
    print("Maximum allowed depth reached. Target not found.")
    return None


def demonstrate_iddfs():
    section_header("Algorithm: Iterative Deepening DFS (IDDFS)")
    
    # Let's create a Tree with a massive branching factor
    # Level 0: 0
    # Level 1: 1, 2, 3
    # Level 2: (1->4,5,6), (2->7,8,9), (3->10,11,12)
    # Level 3: (12->13)
    graph = {
        0: [1, 2, 3],
        1: [4, 5, 6],
        2: [7, 8, 9],
        3: [10, 11, 12],
        12: [13]
    }
    
    start = 0
    target = 13
    
    print("Executing IDDFS to find Target 13...\n")
    path = iddfs(graph, start, target, max_depth=5)
    
    print(f"\nFinal Shortest Path: {path}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why doesn't the repeated work at the top levels destroy the Time Complexity?
   Answer: Exponential Growth! In a tree with branching factor $b=10$, Level 1 has 10 nodes. Level 2 has 100. Level 3 has 1,000. Level 4 has 10,000. 
   When IDDFS runs Level 4, it re-calculates all previous levels. So the total work is: 10,000 (Level 4) + 1,000 (Level 3 repeated) + 100 (Level 2 repeated) + 10 (Level 1 repeated). Total: 11,110. 
   Notice how the nodes in the absolute bottom layer (10,000) account for $90\\%$ of the entire mathematical computation! The repeated work at the top is completely irrelevant in Big-O limits. $O(b^d)$ dominates the equation.

2. Does IDDFS guarantee the Shortest Path?
   Answer: YES. Just like BFS, IDDFS evaluates the graph perfectly layer by layer. If a target exists at Depth 2 and another copy exists at Depth 900, the loop `for limit in range(...)` will hit Depth 2 first, successfully find it, and permanently terminate the algorithm long before it ever discovers the Depth 900 version!

3. Where is IDDFS actually used in the real world?
   Answer: AI game engines! (Chess, Checkers, Go). These engines use "Alpha-Beta Pruning" (which is inherently a DFS algorithm). But because game trees are practically infinite, they cannot run standard DFS. They run IDDFS. They set a 2-second time limit on the clock. The engine runs Depth 1, then Depth 2, then Depth 3... until the 2-second clock expires! Whatever the deepest completed depth was, it uses that answer. This architecture is physically impossible with standard BFS due to Queue memory exploding.
"""

if __name__ == "__main__":
    demonstrate_iddfs()
    print("\n[SUCCESS] Laboratory: Iterative Deepening DFS Completed.")
