"""
# ==============================================================================
# LABORATORY: HAMILTONIAN PATHS & CYCLES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A "Hamiltonian Path" is a path through a Graph that visits EVERY SINGLE VERTEX 
# exactly once.
# A "Hamiltonian Cycle" is a Hamiltonian Path that has a final edge connecting 
# the last vertex back to the starting vertex, forming a closed loop.
#
# This is NOT the same as an Eulerian Path (which visits every EDGE exactly once).
# Eulerian Paths are easy (O(V+E) time using Hierholzer's Algorithm).
#
# Finding a Hamiltonian Path is mathematically NP-Complete. It is one of the 
# hardest problems in Computer Science. The Traveling Salesperson Problem (TSP) 
# is literally just a Hamiltonian Cycle on a Weighted Graph!
#
# Because there is no known fast algorithm, we must use Backtracking to 
# brute-force explore the graph while aggressively pruning dead ends.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Hamiltonian vs Eulerian.
# - Master Graph Traversal Backtracking.
# - Validate Graph Connectivity constraints.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BACKTRACKING ENGINE (HAMILTONIAN CYCLE)
# ==============================================================================
def is_safe_to_visit(graph: List[List[int]], node_to_visit: int, 
                     path: List[int], pos: int) -> bool:
    """
    Validates two constraints:
    1. Does an edge actually exist between the previous node and the new node?
    2. Have we already visited this new node?
    """
    # 1. Edge check (Matrix contains a 0 if no edge exists)
    previous_node = path[pos - 1]
    if graph[previous_node][node_to_visit] == 0:
        return False
        
    # 2. Visited check (Has this node already been added to the path?)
    # Using `in` on a list is O(V), but V is so small it doesn't matter.
    # In production, use a boolean `visited` array for O(1) checks.
    if node_to_visit in path:
        return False
        
    return True


def solve_hamiltonian_cycle(graph: List[List[int]]) -> None:
    """
    Time Complexity: O(N!) Worst Case.
    Space Complexity: O(N) Call Stack.
    """
    num_vertices = len(graph)
    
    # The path array stores the sequence of vertices we visit.
    # Initialize it with -1 (Empty).
    path = [-1] * num_vertices
    
    # Without loss of generality, we can ALWAYS start a Cycle from Vertex 0.
    # If a valid loop exists, it doesn't matter where we start on the loop!
    path[0] = 0
    
    def backtrack(pos: int) -> bool:
        # 1. BASE CASE (SUCCESS)
        # We successfully placed a vertex into every slot (0 to V-1)!
        if pos == num_vertices:
            # But wait! For a CYCLE, the very last vertex must connect back to 0!
            last_node = path[pos - 1]
            if graph[last_node][0] == 1:
                # CYCLE VERIFIED!
                return True
            else:
                # We found a Hamiltonian Path, but NOT a Cycle!
                return False
                
        # 2. CHOICES
        # We are at position `pos` in our path. Try adding any vertex 1 to V-1.
        for v in range(1, num_vertices):
            
            # --- PRUNING ---
            if is_safe_to_visit(graph, v, path, pos):
                
                # --- CHOOSE ---
                path[pos] = v
                
                # --- EXPLORE ---
                if backtrack(pos + 1) is True:
                    return True
                    
                # --- UNCHOOSE ---
                path[pos] = -1
                
        # 3. DEAD END
        return False

    # Execute
    if backtrack(1) is True:
        print(" SUCCESS! Found a Hamiltonian Cycle:")
        
        # Format the path for printing
        # We append the starting vertex to the end to visualize the closed loop
        cycle_str = " -> ".join(str(node) for node in path)
        cycle_str += f" -> {path[0]}"
        print(f" {cycle_str}")
    else:
        print(" FAILED! No Hamiltonian Cycle exists in this graph.")


def demonstrate_hamiltonian():
    section_header("Algorithm: Hamiltonian Cycle")
    
    # Graph 1: A Square with a diagonal cross
    # (0)--(1)
    #  | \ / |
    #  | / \ |
    # (3)--(2)
    # This DOES have a cycle: 0 -> 1 -> 2 -> 3 -> 0
    graph1 = [
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 1, 1, 0]
    ]
    print("Graph 1 (Complete Graph K4):")
    solve_hamiltonian_cycle(graph1)
    
    # Graph 2: A Star/Hub topology
    #   (1)
    #    |
    #   (0)--(2)
    #    |
    #   (3)
    # This DOES NOT have a Hamiltonian Cycle. You must visit 0 multiple times.
    graph2 = [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ]
    print("\nGraph 2 (Star Graph):")
    solve_hamiltonian_cycle(graph2)


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Hamiltonian Cycle NP-Complete, but Eulerian Cycle is O(V+E)?
   Answer: An Eulerian Cycle asks you to visit every EDGE. Leonhard Euler proved a mathematical theorem in 1736: "A graph has an Eulerian cycle if and only if every vertex has an EVEN degree." You don't need to search the graph at all! You just count the degrees of the vertices in $O(V)$ time. There is no such mathematical shortcut for Hamiltonian Cycles (visiting every VERTEX). You are mathematically forced to brute-force the paths.

2. Why can we hardcode `path[0] = 0`? Don't we need to try starting at Node 1?
   Answer: If a graph contains a closed loop (A -> B -> C -> D -> A), that loop is identical regardless of where you start tracing it. (B -> C -> D -> A -> B) is the exact same cycle physically. By forcefully locking Node 0 as the starting point, we divide the Backtracking Search Space by $V$, massively speeding up the algorithm without losing any validity!

3. What happens if the problem asks for a Hamiltonian PATH, not a Cycle?
   Answer: Two changes: First, the Base Case check `graph[last_node][0] == 1` is completely deleted; hitting `pos == V` is an instant success. Second, you CANNOT hardcode `path[0] = 0`. A Path has a specific Start and End. It might be (1 -> 2 -> 3), but (0 -> ...) might lead to a dead end. You must wrap the backtracking engine in a `for` loop that tries starting at every possible node.
"""

if __name__ == "__main__":
    demonstrate_hamiltonian()
    print("\n[SUCCESS] Laboratory: Hamiltonian Paths Completed.")
