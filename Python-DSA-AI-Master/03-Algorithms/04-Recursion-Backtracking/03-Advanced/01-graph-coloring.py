"""
======================================================================================
Graph Coloring Algorithm (m-Coloring Problem)
======================================================================================

Learning Objectives:
1. Understand the m-Coloring Problem and its mathematical foundation.
2. Master the application of backtracking to solve Constraint Satisfaction Problems (CSPs).
3. Analyze the immense time and space complexities involved.
4. Translate theoretical Graph Coloring to practical applications (e.g., Scheduling, Register Allocation).

--------------------------------------------------------------------------------------
1. Intuition & Real-World Analogy
--------------------------------------------------------------------------------------
Imagine you are organizing a university exam schedule. Each vertex represents a 
course, and an edge between two vertices means there is a student taking both courses. 
You cannot schedule these two courses at the same time (they cannot share the same 
"color"). The number of time slots you have is `m`. Your goal is to assign a time slot 
(color) to each course (vertex) so that no two conflicting courses share the same time slot.

Another classic analogy is the Map Coloring Problem. You want to color a political map
of countries such that no two adjacent countries share the same color. How many 
colors do you need? (Hint: The Four Color Theorem states 4 colors suffice for any planar map!)

--------------------------------------------------------------------------------------
2. Formal Explanation
--------------------------------------------------------------------------------------
The m-Coloring problem is defined as:
Given an undirected graph G = (V, E) and an integer m, can we assign a color c(v) 
from the set {1, 2, ..., m} to each vertex v in V such that for every edge (u, v) in E,
c(u) != c(v)?

This is a classic Constraint Satisfaction Problem (CSP):
- Variables: Vertices V
- Domains: Colors {1, ..., m}
- Constraints: For all edges (u, v) in E, color[u] != color[v]

Since this problem is NP-Complete, there is no known polynomial-time algorithm to 
solve it in the general case. We resort to exhaustive search techniques like 
Backtracking.

--------------------------------------------------------------------------------------
3. Complexity Analysis
--------------------------------------------------------------------------------------
- Time Complexity: O(m^V). In the worst case, we might try all m colors for each of 
  the V vertices. While backtracking prunes invalid paths early, the worst-case upper 
  bound remains exponential.
- Space Complexity: O(V) for the recursive call stack (due to the depth of the 
  recursion tree being V) and O(V) for the color assignment array. Overall Space: O(V).

--------------------------------------------------------------------------------------
4. Debugging & Common Mistakes
--------------------------------------------------------------------------------------
- Common Mistake 1: Forgetting to "unassign" the color (backtrack) when a path 
  fails. If you don't reset `color[v] = 0`, subsequent exploration paths are 
  corrupted by invalid state.
- Common Mistake 2: Incorrect graph representation. Assuming the graph is directed 
  instead of undirected, meaning `graph[u][v]` is 1 but `graph[v][u]` is 0. Both must
  reflect the conflict!
- Debugging Tip: Print the recursion tree state. Log the current vertex being colored 
  and the current assignments `color` array to trace the backtracking path.

--------------------------------------------------------------------------------------
5. Active Recall & Memory Anchors
--------------------------------------------------------------------------------------
Q: Why is it O(m^V) and not O(V^m)?
A: We have V vertices (levels in the recursion tree), and at each vertex, we branch 
   m times (try m colors). The branching factor is m, depth is V. Thus m * m ... (V times) = m^V.

Q: How does Graph Coloring relate to Sudoku?
A: Sudoku is a specific instance of graph coloring! The cells are vertices, colors 
   are digits 1-9, and edges connect cells in the same row, column, or 3x3 box.
"""

from typing import List, Optional
import time

class GraphColoring:
    """
    A class to represent a graph and solve the m-coloring problem using Backtracking.
    We represent the graph using an adjacency matrix for O(1) edge lookups, which 
    is fast for dense graphs.
    """
    def __init__(self, vertices: int):
        self.V = vertices
        # Adjacency matrix representation. graph[u][v] == 1 means an edge exists.
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]
        
        # Memory anchor: What if we used an Adjacency List?
        # Is_safe would take O(degree(v)) instead of O(V). 
        # For sparse graphs, an Adjacency List is far more efficient!

    def is_safe(self, v: int, color_assignment: List[int], c: int) -> bool:
        """
        Check if it's valid to assign color 'c' to vertex 'v'.
        We scan all other vertices. If they are adjacent to 'v' AND already 
        have color 'c', it's a conflict!
        
        Args:
            v (int): The current vertex index.
            color_assignment (List[int]): Array storing current color assignments.
            c (int): The color we are trying to assign.
            
        Returns:
            bool: True if safe, False otherwise.
        """
        for i in range(self.V):
            # Constraint check: If adjacent AND has the same color
            if self.graph[v][i] == 1 and color_assignment[i] == c:
                return False
        return True

    def _graph_coloring_util(self, m: int, color_assignment: List[int], v: int) -> bool:
        """
        The core recursive backtracking function.
        
        Args:
            m (int): Total number of colors available.
            color_assignment (List[int]): Current state of assignments.
            v (int): The current vertex we are trying to color.
            
        Returns:
            bool: True if coloring is possible from this state, False otherwise.
        """
        # Base Case: If all vertices are colored, we found a valid assignment!
        if v == self.V:
            return True

        # Recursive Step: Try assigning each color from 1 to m to vertex v.
        for c in range(1, m + 1):
            if self.is_safe(v, color_assignment, c):
                # 1. Choose: Assign the color
                color_assignment[v] = c
                
                # 2. Explore: Move to the next vertex
                # If this path leads to a full valid coloring, return True immediately
                if self._graph_coloring_util(m, color_assignment, v + 1):
                    return True
                
                # 3. Un-choose (Backtrack): The color 'c' didn't lead to a solution.
                # Reset the color and try the next color in the loop.
                # THIS IS THE MOST CRITICAL STEP IN BACKTRACKING!
                color_assignment[v] = 0
                
        # If no color from 1 to m works for vertex v, return False to trigger 
        # backtracking in the previous stack frame.
        return False

    def solve_m_coloring(self, m: int) -> Optional[List[int]]:
        """
        Public API to solve the graph coloring problem.
        Initializes the assignment array and triggers the recursive utility.
        
        Args:
            m (int): Max number of colors to use.
            
        Returns:
            List[int] if a solution exists, else None.
        """
        # color_assignment initialized to 0 (meaning uncolored).
        # Colors will be 1-indexed (1 to m).
        color_assignment = [0] * self.V
        
        # Start coloring from vertex 0
        if not self._graph_coloring_util(m, color_assignment, 0):
            print(f"Solution does not exist for {m} colors.")
            return None
            
        return color_assignment


# =====================================================================
# Professional Testing and Edge Cases
# =====================================================================

def run_tests():
    print("--- Graph Coloring Backtracking Tests ---")
    
    # Test Case 1: Simple planar graph (Square with one diagonal)
    # V0 - V1
    # |  \ |
    # V3 - V2
    g1 = GraphColoring(4)
    g1.graph = [
        [0, 1, 1, 1], # Vertex 0 is connected to 1, 2, 3
        [1, 0, 1, 0], # Vertex 1 is connected to 0, 2
        [1, 1, 0, 1], # Vertex 2 is connected to 0, 1, 3
        [1, 0, 1, 0], # Vertex 3 is connected to 0, 2
    ]
    
    print("\nTest 1: Square with one diagonal (Requires 3 colors)")
    m = 3
    result1 = g1.solve_m_coloring(m)
    assert result1 is not None, "Test 1 Failed"
    print(f"Colors assigned: {result1}")
    
    # Test Case 2: Complete Graph K4
    # In a complete graph, every vertex is connected to every other vertex.
    # Therefore, a complete graph with V vertices requires exactly V colors!
    g2 = GraphColoring(4)
    g2.graph = [
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0]
    ]
    print("\nTest 2: Complete Graph K4 (Requires exactly 4 colors)")
    
    # Let's try coloring K4 with 3 colors (Should fail)
    print("Trying with 3 colors...")
    result2_fail = g2.solve_m_coloring(3)
    assert result2_fail is None, "Test 2 Failed (Expected None)"
    
    # Let's try coloring K4 with 4 colors (Should succeed)
    print("Trying with 4 colors...")
    result2_success = g2.solve_m_coloring(4)
    assert result2_success is not None, "Test 2 Failed"
    print(f"Colors assigned: {result2_success}")
    
    # Test Case 3: Bipartite Graph
    # Can always be colored using 2 colors.
    # V0 -- V1, V2 -- V3
    g3 = GraphColoring(4)
    g3.graph = [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ]
    print("\nTest 3: Disconnected Bipartite components (Requires 2 colors)")
    result3 = g3.solve_m_coloring(2)
    assert result3 is not None, "Test 3 Failed"
    print(f"Colors assigned: {result3}")

    print("\nAll Graph Coloring tests passed successfully!")

if __name__ == "__main__":
    run_tests()
