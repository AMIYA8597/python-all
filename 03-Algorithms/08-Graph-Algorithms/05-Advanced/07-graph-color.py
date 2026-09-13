"""
# ==============================================================================
# LABORATORY: GRAPH COLORING (BACKTRACKING & GREEDY HEURISTICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a University timetable. There are 100 final exams. 
# You cannot schedule two exams in the same time slot if a student is enrolled 
# in both classes!
#
# How many time slots do you need?
# This is mathematically identical to the "Graph Coloring Problem".
# - Vertices = Exams.
# - Edges = A student takes both exams (conflict).
# - Colors = Time Slots.
#
# The goal is to color every vertex such that NO TWO ADJACENT VERTICES share the 
# same color, using the absolute minimum number of colors. The minimum number 
# is called the "Chromatic Number".
#
# Bipartite graphs have a chromatic number of 2.
# The famous "Four Color Theorem" proved that any physical 2D map (like a map 
# of the US states) has a chromatic number of at most 4.
#
# Finding the exact Chromatic Number for a general graph is NP-Complete!
# A brute-force backtracking algorithm takes O(M^V) time, where M is the number 
# of colors and V is the vertices.
#
# Because it's NP-Complete, production systems (like Sudoku solvers and compilers 
# doing Register Allocation) use Backtracking for small graphs, and Greedy 
# Heuristics (like the Welsh-Powell algorithm) for massive graphs.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Chromatic Number constraint.
# - Implement M-Coloring Exact Backtracking (NP-Complete).
# - Implement Welsh-Powell Greedy Heuristic (Polynomial Time Approximation).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EXACT M-COLORING ENGINE (BACKTRACKING, O(M^V))
# ==============================================================================
class ExactGraphColoring:
    def __init__(self, vertices: int, graph: List[List[int]]):
        self.V = vertices
        self.graph = graph
        self.colors = [-1] * vertices
        
    def _is_safe(self, node: int, color_to_try: int) -> bool:
        """
        Checks if assigning this color violates the golden rule:
        No adjacent node can have the same color.
        """
        for neighbor in range(self.V):
            # If an edge exists AND the neighbor already has this exact color...
            if self.graph[node][neighbor] == 1 and self.colors[neighbor] == color_to_try:
                return False
        return True
        
    def _backtrack(self, m: int, current_node: int) -> bool:
        """
        Recursive Backtracking DFS.
        Tries to color the graph using at most `m` colors.
        """
        # BASE CASE: If we reached the end, we successfully colored everything!
        if current_node == self.V:
            return True
            
        # Try all possible colors (0 to m-1)
        for c in range(m):
            if self._is_safe(current_node, c):
                # Assign the color!
                self.colors[current_node] = c
                
                # Recurse to the next node!
                if self._backtrack(m, current_node + 1):
                    return True
                    
                # BACKTRACK: If that color choice led to a dead-end down the road, 
                # erase it and try the next color!
                self.colors[current_node] = -1
                
        # If we tried ALL colors and nothing worked, this `m` is too small!
        return False
        
    def solve(self, m: int) -> bool:
        """Returns True if the graph can be colored with `m` colors."""
        if self._backtrack(m, 0):
            return True
        return False


# ==============================================================================
# 4. WELSH-POWELL GREEDY ENGINE (O(V^2))
# ==============================================================================
def welsh_powell_greedy(vertices: int, graph: List[List[int]]) -> List[int]:
    """
    Polynomial-time heuristic. It doesn't guarantee the absolute minimum 
    Chromatic Number, but it gets extremely close, blazingly fast.
    """
    # 1. CALCULATE DEGREES
    # Count how many edges each node has
    degrees = []
    for i in range(vertices):
        deg = sum(graph[i])
        degrees.append((deg, i))
        
    # 2. SORT BY DEGREE (DESCENDING)
    # The Welsh-Powell trick: Always color the most heavily connected nodes FIRST.
    # They are the hardest to color. If you leave them for last, you will be 
    # forced to invent new colors.
    degrees.sort(reverse=True, key=lambda x: x[0])
    
    colors = [-1] * vertices
    current_color = 0
    
    # 3. GREEDY ASSIGNMENT
    for _, node in degrees:
        if colors[node] != -1:
            continue # Already colored in a previous sweep
            
        # Assign the current color to this node
        colors[node] = current_color
        
        # Now, look at ALL OTHER uncolored nodes in the sorted list.
        # Can we greedily slap this exact same color on them too?
        for _, other_node in degrees:
            if colors[other_node] == -1:
                # Is it safe? (Does it share an edge with ANY node that ALREADY 
                # has `current_color`?)
                safe = True
                for neighbor in range(vertices):
                    if graph[other_node][neighbor] == 1 and colors[neighbor] == current_color:
                        safe = False
                        break
                        
                if safe:
                    colors[other_node] = current_color
                    
        # We exhausted all safe nodes for this color. Move to the next color!
        current_color += 1
        
    return colors


def demonstrate_coloring():
    section_header("Algorithm: Graph Coloring")
    
    vertices = 4
    # Adjacency Matrix
    # 0 is connected to 1, 2, 3
    # 1 is connected to 0, 2
    # 2 is connected to 0, 1, 3
    # 3 is connected to 0, 2
    # This is a dense graph with triangles!
    graph = [
        [0, 1, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0],
    ]
    
    print("Graph Adjacency Matrix:")
    for row in graph: print(row)
        
    print("\n--- EXACT BACKTRACKING (NP-Complete) ---")
    exact = ExactGraphColoring(vertices, graph)
    
    # Let's test different M limits!
    for m in range(2, 5):
        # Reset colors for the test
        exact.colors = [-1] * vertices
        if exact.solve(m):
            print(f"Graph CAN be colored with {m} colors! Assignment: {exact.colors}")
            break
        else:
            print(f"Graph CANNOT be colored with {m} colors.")
            
    print("\n--- WELSH-POWELL GREEDY HEURISTIC ---")
    greedy_colors = welsh_powell_greedy(vertices, graph)
    max_color_used = max(greedy_colors) + 1
    print(f"Greedy Heuristic used {max_color_used} colors! Assignment: {greedy_colors}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the Backtracking algorithm $O(M^V)$?
   Answer: We have $V$ vertices. For every single vertex, the recursive loop attempts to assign one of $M$ possible colors. It branches out $M$ times at every level of the tree. The tree has a depth of $V$. Therefore, the total number of leaves in the execution tree is bounded by $M^V$. If $M=3$ and $V=20$, it's $3^{20} = 3.4$ Billion operations.

2. Why does the Welsh-Powell greedy algorithm sort by degree descending?
   Answer: Imagine a "Hub" node connected to 50 other nodes. If you color the 50 outer nodes first using a random greedy approach, they might accidentally use 5 different colors. When you finally reach the Hub node in the center, you realize it is touching 5 colors! You are forced to use a 6th color. By sorting descending, you color the Hub FIRST. It gets Color 0. Then the 50 outer nodes can easily be greedy-colored using just 1 or 2 other colors, keeping the global total minimized!

3. Where is Graph Coloring used in the real world?
   Answer: 
   - Compiler Optimization (Register Allocation): Variables are Vertices. If two variables are alive at the exact same time in the code, there is an Edge between them (they conflict). The Colors are physical CPU Registers. Compilers use Graph Coloring to assign variables to the limited CPU registers!
   - Sudoku: Every cell is a vertex. Every cell in the same row, column, or 3x3 grid shares an Edge. You must color the graph using exactly $M=9$ colors (numbers)!
"""

if __name__ == "__main__":
    demonstrate_coloring()
    print("\n[SUCCESS] Laboratory: Graph Coloring Completed.")
