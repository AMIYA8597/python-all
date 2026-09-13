"""
# ==============================================================================
# LABORATORY: EULERIAN PATHS & CIRCUITS (HIERHOLZER'S ALGORITHM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In 1736, the city of Königsberg had 7 bridges. The citizens wondered: 
# "Is it possible to take a walk through the city and cross every single bridge 
# exactly ONCE?"
#
# Leonhard Euler proved it was mathematically impossible. In doing so, he 
# invented the entire field of Graph Theory.
#
# - Eulerian Circuit: Cross every edge exactly once, and finish exactly where 
#   you started. 
#   Mathematical Law: EVERY single node in the graph MUST have an EVEN degree 
#   (number of connected edges). If you enter a node, you must have a way to leave!
#
# - Eulerian Path: Cross every edge exactly once, but finish at a different node.
#   Mathematical Law: Exactly TWO nodes must have an ODD degree (the Start and 
#   the End). Every other node must be EVEN.
#
# 137 years later, in 1873, Carl Hierholzer invented the algorithm to actually 
# construct the path!
#
# Hierholzer's Algorithm is a destructive DFS:
# 1. Start at a valid node.
# 2. Walk across an edge. 
# 3. DESTROY THE EDGE (so you can never cross it again).
# 4. Keep walking randomly. If you get completely stuck (a node has 0 edges left), 
#    push that node to a Stack, and backtrack.
# 5. When the DFS finishes, the Stack magically contains the exact Eulerian Path 
#    in perfect reverse order!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Verify Eulerian properties (In-degree vs Out-degree).
# - Implement Hierholzer's O(V + E) destructive DFS.
# - Reconstruct the Eulerian sequence.
#
# ==============================================================================
"""

from typing import Dict, List, Optional
from collections import defaultdict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HIERHOLZER'S ALGORITHM (O(V + E))
# ==============================================================================
class EulerianPath:
    def __init__(self, vertices: int, directed_edges: List[List[int]]):
        self.V = vertices
        
        # We use a Dictionary of Lists for O(1) edge destruction (pop from end)
        self.graph = defaultdict(list)
        self.in_degree = [0] * vertices
        self.out_degree = [0] * vertices
        
        for u, v in directed_edges:
            self.graph[u].append(v)
            self.out_degree[u] += 1
            self.in_degree[v] += 1
            
        self.path_stack = []
        
    def _verify_eulerian(self) -> Optional[int]:
        """
        Verifies the mathematical laws of Euler for Directed Graphs.
        Returns the required Starting Node, or None if impossible.
        """
        start_nodes = 0
        end_nodes = 0
        start_node_id = -1
        
        for i in range(self.V):
            # If in == out, it's a perfectly balanced EVEN node. (Safe)
            if self.in_degree[i] == self.out_degree[i]:
                continue
                
            # If out == in + 1, this MUST be the Starting Node!
            elif self.out_degree[i] - self.in_degree[i] == 1:
                start_nodes += 1
                start_node_id = i
                
            # If in == out + 1, this MUST be the Ending Node!
            elif self.in_degree[i] - self.out_degree[i] == 1:
                end_nodes += 1
                
            # Any other imbalance mathematically destroys the Eulerian property!
            else:
                return None
                
        # Case A: Eulerian Circuit (All nodes perfectly balanced)
        if start_nodes == 0 and end_nodes == 0:
            # We can start anywhere that has edges!
            for i in range(self.V):
                if self.out_degree[i] > 0:
                    return i
            return 0
            
        # Case B: Eulerian Path (Exactly 1 Start, Exactly 1 End)
        elif start_nodes == 1 and end_nodes == 1:
            return start_node_id
            
        # Case C: Impossible
        return None
        
    def _dfs_destructive(self, u: int):
        """
        Walks randomly, burning bridges. Pushes to stack when trapped.
        """
        # While I have edges left to explore...
        while self.graph[u]:
            # Destroy the edge! (O(1) pop from the end of the list)
            next_node = self.graph[u].pop()
            self._dfs_destructive(next_node)
            
        # I have 0 edges left! I am completely trapped.
        # Push my body to the stack!
        self.path_stack.append(u)
        
    def find_path(self) -> Optional[List[int]]:
        """
        Orchestrates Hierholzer's Algorithm.
        """
        start_node = self._verify_eulerian()
        if start_node is None:
            return None # Impossible
            
        self._dfs_destructive(start_node)
        
        # We must reverse the stack to get the correct chronological forward path
        forward_path = self.path_stack[::-1]
        
        # Final edge case: What if the graph is disconnected? 
        # The DFS wouldn't have reached the other islands!
        # The total length of an Eulerian path must be EXACTLY (Edges + 1).
        total_edges = sum(self.out_degree)
        if len(forward_path) != total_edges + 1:
            return None
            
        return forward_path


def demonstrate_hierholzer():
    section_header("Algorithm: Eulerian Path (Hierholzer)")
    
    vertices = 4
    # Directed Graph
    # 0 -> 1 -> 2 -> 0 (A cycle)
    # 2 -> 3 (An exit!)
    # Let's check the degrees:
    # 0: In=1, Out=1 (Balanced)
    # 1: In=1, Out=1 (Balanced)
    # 2: In=1, Out=2 (Out is +1. This MUST be the Start!)
    # 3: In=1, Out=0 (In is +1. This MUST be the End!)
    edges = [
        [0, 1],
        [1, 2],
        [2, 0],
        [2, 3]
    ]
    
    print("Graph Edges (Directed):")
    for u, v in edges: print(f" {u} -> {v}")
        
    print("\nExecuting Hierholzer's Algorithm...")
    euler = EulerianPath(vertices, edges)
    path = euler.find_path()
    
    if path:
        print(f"\nValid Eulerian Path Found!")
        print(f"Sequence: {' -> '.join(map(str, path))}")
    else:
        print("\nEulerian Path is Mathematically Impossible for this graph.")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does pushing a "trapped" node to the stack guarantee the correct path?
   Answer: Imagine a graph shaped like a Figure-8. You start at the center intersection, trace the left circle, and return to the center. You are NOT trapped yet, because the right circle still has edges! You trace the right circle and return to the center. Now you are trapped! The center gets pushed to the stack. Then the recursion unwinds backward, pushing the nodes of the right circle, then pushing the nodes of the left circle. When you reverse the stack, you get the exact chronological forward order you walked it! 

2. How do Eulerian Paths differ from Hamiltonian Paths?
   Answer: 
   - Eulerian Path: Must visit every EDGE exactly once. (Solved in $O(V+E)$ by Euler and Hierholzer).
   - Hamiltonian Path: Must visit every VERTEX exactly once. (This is NP-Complete! It is the Traveling Salesperson Problem. There is no known fast algorithm, it requires $O(2^V)$ Dynamic Programming or $O(V!)$ Brute Force).

3. Can Hierholzer's Algorithm be used on Undirected Graphs?
   Answer: YES. The only changes required are:
   1. The Eulerian math check changes: For a circuit, EVERY node must have an EVEN degree. For a path, EXACTLY 2 nodes must have an ODD degree.
   2. When destroying the edge $U \\to V$, you MUST also mathematically hunt down and destroy the reverse edge $V \\to U$ in V's adjacency list, otherwise you will cross the same bridge backward!
"""

if __name__ == "__main__":
    demonstrate_hierholzer()
    print("\n[SUCCESS] Laboratory: Eulerian Paths Completed.")
