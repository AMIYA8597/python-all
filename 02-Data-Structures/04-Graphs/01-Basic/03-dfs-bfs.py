"""
# ==============================================================================
# LABORATORY: ADVANCED DFS APPLICATIONS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know how to write a basic DFS to traverse a graph. 
# But DFS is also the foundation for solving complex topological and structural 
# graph problems. 
# For example, if you are building a package manager (npm, pip), how do you know 
# if a user has created a circular dependency (A requires B, B requires A)? You 
# use DFS Cycle Detection. 
# If you are matching students to dormitories where certain students hate each other, 
# how do you divide them into two safe groups? You use DFS Bipartite Coloring.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Cycle Detection in Undirected Graphs (tracking the parent).
# - Master Cycle Detection in Directed Graphs (using 3 states: Unvisited, Visiting, Visited).
# - Solve Bipartite Graph coloring (LeetCode #785).
#
# ==============================================================================
"""

from collections import defaultdict
from typing import Dict, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CYCLE DETECTION (UNDIRECTED GRAPH)
# ==============================================================================
def has_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    """
    In an undirected graph, A connects to B, which implies B connects to A.
    If DFS visits A, then visits B, it will naturally look back at A.
    THIS IS NOT A CYCLE! To find a real cycle, we must ignore the node we 
    just came from (the parent).
    """
    visited = set()
    
    def dfs(node: int, parent: int) -> bool:
        visited.add(node)
        
        for neighbor in graph[node]:
            # If we haven't seen it, explore it.
            if neighbor not in visited:
                if dfs(neighbor, node): # neighbor's parent is the current node
                    return True
            # If we HAVE seen it, and it's NOT our direct parent... it's a cycle!
            elif neighbor != parent:
                return True
                
        return False

    # A graph might be disconnected, so we must check all nodes
    for node in graph:
        if node not in visited:
            if dfs(node, -1):
                return True
    return False

def demonstrate_undirected_cycle():
    section_header("Algorithm: Undirected Cycle Detection")
    
    # Linear: 1 - 2 - 3
    no_cycle_graph = {1: [2], 2: [1, 3], 3: [2]}
    # Triangle: 1 - 2 - 3 - 1
    cycle_graph = {1: [2, 3], 2: [1, 3], 3: [1, 2]}
    
    print(f"Graph 1 (Line) Has Cycle: {has_cycle_undirected(no_cycle_graph)}")
    print(f"Graph 2 (Triangle) Has Cycle: {has_cycle_undirected(cycle_graph)}")


# ==============================================================================
# 4. CYCLE DETECTION (DIRECTED GRAPH)
# ==============================================================================
def has_cycle_directed(graph: Dict[int, List[int]], num_courses: int) -> bool:
    """
    LeetCode #207: Course Schedule (Prerequisite cycles)
    In a Directed Graph, the parent trick doesn't work.
    Instead, we must use 3 States:
    0 = Unvisited
    1 = Visiting (Currently in the recursive call stack)
    2 = Visited (Fully explored and safe)
    
    A cycle ONLY exists if we encounter a node that is currently in the 
    'Visiting' state (State 1).
    """
    # 0 = Unvisited, 1 = Visiting, 2 = Visited
    states = {i: 0 for i in range(num_courses)}
    
    def dfs(node: int) -> bool:
        if states[node] == 1:
            return True # Cycle detected! (Back edge)
        if states[node] == 2:
            return False # Already verified safe (Cross edge)
            
        # Mark as Visiting
        states[node] = 1
        
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
                
        # Mark as fully Visited (Safe)
        states[node] = 2
        return False

    for i in range(num_courses):
        if states[i] == 0:
            if dfs(i):
                return True
    return False

def demonstrate_directed_cycle():
    section_header("Algorithm: Directed Cycle Detection (Course Schedule)")
    
    # Valid: 0 -> 1 -> 2
    valid_courses = {0: [1], 1: [2]}
    # Invalid: 0 -> 1 -> 2 -> 0
    invalid_courses = {0: [1], 1: [2], 2: [0]}
    
    print(f"Valid Curriculum Has Cycle: {has_cycle_directed(valid_courses, 3)}")
    print(f"Invalid Curriculum Has Cycle: {has_cycle_directed(invalid_courses, 3)}")


# ==============================================================================
# 5. BIPARTITE GRAPH (GRAPH COLORING)
# ==============================================================================
def is_bipartite(graph: List[List[int]]) -> bool:
    """
    LeetCode #785: Is Graph Bipartite?
    A Bipartite graph can be colored with 2 colors such that NO two adjacent 
    nodes have the same color.
    
    Strategy: Run DFS. Color the current node Red. Try to color all its neighbors 
    Blue. If a neighbor is already Red, the graph is NOT bipartite.
    """
    # 0 = Uncolored, 1 = Red, -1 = Blue
    colors = {}
    
    def dfs(node: int, color: int) -> bool:
        colors[node] = color
        
        for neighbor in graph[node]:
            if neighbor not in colors:
                # Color the neighbor with the OPPOSITE color
                if not dfs(neighbor, -color):
                    return False
            # If the neighbor is already colored with the SAME color, it fails!
            elif colors[neighbor] == color:
                return False
                
        return True

    # Graph might be disconnected
    for i in range(len(graph)):
        if i not in colors:
            # Start coloring this component with Color 1
            if not dfs(i, 1):
                return False
    return True

def demonstrate_bipartite():
    section_header("Algorithm: Is Bipartite? (Graph Coloring)")
    
    # Bipartite (Even cycle): 0-1, 1-2, 2-3, 3-0
    # Colors: 0:Red, 1:Blue, 2:Red, 3:Blue (Valid!)
    bipartite_graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
    
    # Not Bipartite (Odd cycle: Triangle): 0-1, 1-2, 2-0
    # Colors: 0:Red, 1:Blue, 2:Red... wait, 2 connects to 0! Both are Red!
    triangle_graph = [[1, 2], [0, 2], [0, 1]]
    
    print(f"Graph 1 (Square) is Bipartite: {is_bipartite(bipartite_graph)}")
    print(f"Graph 2 (Triangle) is Bipartite: {is_bipartite(triangle_graph)}")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Cycle Detection in an Undirected graph require passing the `parent` node?
   Answer: Because an undirected edge A-B is represented as A->B and B->A in the adjacency list. When DFS moves from A to B, the loop in B will immediately look at A as a neighbor. If we don't explicitly ignore the parent, the algorithm will falsely report a cycle every single time.

2. In a Directed graph, why do we need 3 states (Unvisited, Visiting, Visited) instead of a simple boolean `visited` set?
   Answer: In a directed graph, if A->C and B->C, DFS might visit C via A, mark it as visited, and finish. Later, DFS explores B, sees C, and says "Ah! C is in the visited set, Cycle!". This is wrong; it's just a cross-edge, not a cycle. We only detect a cycle if we hit a node that is CURRENTLY in the call stack ("Visiting" state).

3. What is the defining characteristic of a graph that is NOT Bipartite?
   Answer: The graph contains an ODD length cycle (like a triangle). An even length cycle (like a square) can alternate Red-Blue-Red-Blue perfectly. An odd cycle (Red-Blue-Red...) forces the last node to connect back to the first node, resulting in two Reds touching.
"""

if __name__ == "__main__":
    demonstrate_undirected_cycle()
    demonstrate_directed_cycle()
    demonstrate_bipartite()
    print("\n[SUCCESS] Laboratory: Advanced DFS Applications Completed.")
