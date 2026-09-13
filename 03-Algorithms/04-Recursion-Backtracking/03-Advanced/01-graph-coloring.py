"""
# ==============================================================================
# LABORATORY: M-COLORING PROBLEM (ADVANCED BACKTRACKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The "Graph Coloring Problem" is one of the most famous problems in Computer Science.
# Given a map of countries (which can be represented as a Graph), can you color 
# every country using exactly M colors, such that no two bordering countries 
# share the same color?
#
# This isn't just about maps. It solves real-world constraints:
# - Sudoku is technically a 9-coloring graph problem.
# - University Class Scheduling: You have 10 exams. Some students are in multiple 
#   classes (edges between exams). Can you schedule all exams in M time slots 
#   so no student has two exams at the same time?
# - Register Allocation: A Compiler assigning M physical CPU registers to 
#   thousands of local variables.
#
# The M-Coloring problem is NP-Complete. There is no known fast algorithm. 
# We are forced to use Backtracking to brute-force the Decision Tree, while 
# relying on heavy Pruning to survive.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model a constraint problem as a Graph.
# - Master complex State Validation against adjacent nodes.
# - Understand Chromatic Number.
#
# ==============================================================================
"""

from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STATE VALIDATION (ADJACENCY CHECK)
# ==============================================================================
def is_safe_to_color(graph: Dict[int, List[int]], node: int, color_to_try: int, 
                     colors_assigned: List[int]) -> bool:
    """
    Checks if it is mathematically safe to paint `node` with `color_to_try`.
    Time Complexity: O(Degree of Node) -> O(V) Worst case.
    """
    # Look at every neighbor of the current node
    for neighbor in graph[node]:
        
        # If the neighbor is ALREADY painted with the color we want to use...
        if colors_assigned[neighbor] == color_to_try:
            return False
            
    return True


# ==============================================================================
# 4. THE M-COLORING ENGINE
# ==============================================================================
def m_coloring_backtrack(graph: Dict[int, List[int]], m: int, node: int, 
                         colors_assigned: List[int], num_nodes: int) -> bool:
    """
    Attempts to color the graph using `m` colors.
    Returns True the microsecond it finds a valid full assignment (Early Exit).
    Time Complexity: O(M^V) Worst case.
    Space Complexity: O(V) Call Stack + O(V) Color Array.
    """
    # 1. BASE CASE (SUCCESS)
    # If we have successfully assigned a color to every node (0 to V-1)...
    if node == num_nodes:
        return True
        
    # 2. THE CHOICES
    # We are at `node`. We have `m` different paint colors to try (1 through m).
    for color in range(1, m + 1):
        
        # --- PRUNING ---
        # Before we paint it, we must check if any neighbors already have this color.
        if is_safe_to_color(graph, node, color, colors_assigned):
            
            # --- CHOOSE ---
            colors_assigned[node] = color
            
            # --- EXPLORE ---
            # Move to the next node. If the recursive cascade returns True, 
            # instantly propagate the True upwards!
            if m_coloring_backtrack(graph, m, node + 1, colors_assigned, num_nodes) is True:
                return True
                
            # --- UNCHOOSE ---
            # This color led to a dead end deeper in the tree.
            # Erase the color (reset to 0) and try the next paint color.
            colors_assigned[node] = 0
            
    # 3. FATAL DEAD END
    # We tried all `m` colors for this node, and NONE worked.
    # The graph CANNOT be colored with only `m` colors down this branch.
    return False


def solve_graph_coloring(graph: Dict[int, List[int]], m: int, num_nodes: int) -> None:
    # 0 means "Unpainted"
    colors_assigned = [0] * num_nodes
    
    # Start the engine at Node 0
    success = m_coloring_backtrack(graph, m, 0, colors_assigned, num_nodes)
    
    if success:
        print(f" SUCCESS! The graph CAN be colored using {m} colors.")
        print(" Node Assignments:")
        for node in range(num_nodes):
            print(f"  Node {node} -> Color {colors_assigned[node]}")
    else:
        print(f" FAILED! The graph CANNOT be colored with only {m} colors.")


def demonstrate_coloring():
    section_header("Algorithm: M-Coloring Backtracking")
    
    # We define an Adjacency List for a Graph with 4 nodes (0, 1, 2, 3)
    # 
    #   (0)---(1)
    #    |  \  |
    #    |   \ |
    #   (3)---(2)
    #
    # Node 0 is connected to 1, 2, 3 (It is in the center)
    graph = {
        0: [1, 2, 3],
        1: [0, 2],
        2: [0, 1, 3],
        3: [0, 2]
    }
    num_nodes = 4
    
    print("Graph Structure: 0 is connected to everything.")
    
    m = 2
    print(f"\nAttempting to color with M = {m} colors...")
    solve_graph_coloring(graph, m, num_nodes)
    
    m = 3
    print(f"\nAttempting to color with M = {m} colors...")
    solve_graph_coloring(graph, m, num_nodes)


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Chromatic Number of a graph?
   Answer: It is the absolute Minimum number of colors required to color the graph. For a Bipartite Graph, the chromatic number is 2. For a complete graph $K_N$ (where every node connects to every other node), the chromatic number is $N$. Finding the exact Chromatic Number of an arbitrary graph is NP-Hard.

2. Why is the Time Complexity $O(M^V)$?
   Answer: We have $V$ nodes (the depth of the recursion tree). At every node, we have $M$ branches to explore (the different paint colors). Therefore, the worst-case number of nodes explored in the decision tree is $M^V$.

3. How does this algorithm prove if a graph is Bipartite?
   Answer: A Bipartite Graph is mathematically defined as a graph that can be colored using exactly 2 colors. If you run this exact algorithm with $M=2$, and it returns `True`, you have mathematically proven the graph is Bipartite!
"""

if __name__ == "__main__":
    demonstrate_coloring()
    print("\n[SUCCESS] Laboratory: Graph Coloring Completed.")
