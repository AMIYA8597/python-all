"""
# ==============================================================================
# LABORATORY: ADVANCED FLOYD-WARSHALL (PATH RECONSTRUCTION & REACHABILITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Floyd-Warshall finds the absolute shortest distance between 
# every pair of nodes in O(V^3) time. 
# But just knowing the distance is useless if you don't know the actual route! 
# How do you reconstruct the exact sequence of cities to visit? We must maintain 
# a secondary `next_node` matrix.
#
# Additionally, if you strip away the weights and just use Boolean logic (0 or 1), 
# Floyd-Warshall becomes "Warshall's Algorithm", which computes the "Transitive 
# Closure" of a graph. This instantly tells you: "Is there ANY path between A and B?", 
# which is heavily used in networking and compiler analysis.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Track and reconstruct the shortest path using a `next_node` matrix.
# - Detect negative weight cycles by inspecting the diagonal.
# - Compute Transitive Closure (Warshall's Algorithm).
#
# ==============================================================================
"""

from typing import List, Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. FLOYD-WARSHALL WITH PATH RECONSTRUCTION
# ==============================================================================
class FloydWarshallAdvanced:
    def __init__(self, num_vertices: int):
        self.n = num_vertices
        self.dist = [[float('inf')] * self.n for _ in range(self.n)]
        # next_node[i][j] stores the NEXT node to visit when traveling from i to j
        self.next_node = [[-1] * self.n for _ in range(self.n)]
        
        for i in range(self.n):
            self.dist[i][i] = 0
            self.next_node[i][i] = i
            
    def add_edge(self, u: int, v: int, weight: int):
        self.dist[u][v] = weight
        # Initially, the next step from u to v is just v
        self.next_node[u][v] = v
        
    def execute(self):
        """O(V^3) Dynamic Programming computation."""
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    
                    # If going through k is shorter...
                    if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                        # The new next step from i to j is whatever the next step 
                        # was from i to k!
                        self.next_node[i][j] = self.next_node[i][k]

    def has_negative_cycle(self) -> bool:
        """
        If the distance from a node to ITSELF drops below 0, it means there is 
        a negative cycle in the graph.
        """
        for i in range(self.n):
            if self.dist[i][i] < 0:
                return True
        return False

    def reconstruct_path(self, u: int, v: int) -> Optional[List[int]]:
        """Reconstructs the exact path from u to v using the next_node matrix."""
        # If there's no path, or a negative cycle destroyed the pathing
        if self.next_node[u][v] == -1:
            return None
            
        path = [u]
        while u != v:
            u = self.next_node[u][v]
            path.append(u)
        return path

def demonstrate_path_reconstruction():
    section_header("Algorithm: Floyd-Warshall Path Reconstruction")
    
    fw = FloydWarshallAdvanced(4)
    fw.add_edge(0, 1, 3)
    fw.add_edge(0, 2, 8)
    fw.add_edge(1, 2, 4)
    fw.add_edge(1, 3, 2)
    fw.add_edge(2, 3, 1)
    
    fw.execute()
    
    start, end = 0, 3
    print(f"Shortest Distance from {start} to {end}: {fw.dist[start][end]}")
    
    path = fw.reconstruct_path(start, end)
    print(f"Reconstructed Path: {' -> '.join(map(str, path))}")
    print("Explanation: 0 -> 1 (cost 3), 1 -> 3 (cost 2). Total = 5.")


# ==============================================================================
# 4. TRANSITIVE CLOSURE (WARSHALL'S ALGORITHM)
# ==============================================================================
def transitive_closure(num_vertices: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Finds if a path exists between ANY pair of nodes.
    We don't care about weights. We just use 1 (reachable) and 0 (unreachable).
    Time Complexity: O(V^3)
    """
    # 1. Initialize Reachability Matrix
    reach = [[0] * num_vertices for _ in range(num_vertices)]
    
    for i in range(num_vertices):
        reach[i][i] = 1 # A node can always reach itself
        
    for u, v in edges:
        reach[u][v] = 1 # Direct edges are reachable
        
    # 2. Dynamic Programming (Bitwise OR)
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                
                # reach[i][j] is True IF:
                # It was already True (reach[i][j])
                # OR (reach[i][k] AND reach[k][j] are both True)
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
                
    return reach

def demonstrate_transitive_closure():
    section_header("Algorithm: Transitive Closure (Reachability)")
    
    # 0 points to 1 and 2
    # 1 points to 2
    # 2 points to 3
    edges = [(0, 1), (0, 2), (1, 2), (2, 3)]
    num_nodes = 4
    
    print("Graph: 0->1, 0->2, 1->2, 2->3")
    
    reach = transitive_closure(num_nodes, edges)
    
    print("\nReachability Matrix:")
    print("    " + "  ".join(str(i) for i in range(num_nodes)))
    print("  " + "-" * (num_nodes * 3))
    for i in range(num_nodes):
        print(f"{i} | {reach[i]}")
        
    print("\nNotice that Reach[0][3] is 1 (True).")
    print("Even though there is no direct edge from 0 to 3, the algorithm deduced")
    print("that 0 can reach 3 (via 0->2->3 or 0->1->2->3).")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does the `next_node` matrix update during Floyd-Warshall?
   Answer: When we discover that the path `i -> k -> j` is faster than `i -> j`, we update the next step from `i` to `j`. The new next step is simply the next step from `i` to `k`. (Because to get to `j` through `k`, we must first take the optimal path to `k`).

2. How does Floyd-Warshall detect a Negative Cycle?
   Answer: We initialize the distance from any node to itself `dist[i][i]` as 0. If there is a negative cycle, eventually the path `i -> ... -> i` will evaluate to a negative number, and the algorithm will overwrite `dist[i][i]` with that negative value. Checking the diagonal at the end instantly reveals cycles.

3. Can you optimize Warshall's Transitive Closure?
   Answer: Yes! Because it only uses 1s and 0s, you can use Python's built-in bitwise integers (which act as bit arrays). You can bitwise OR entire rows at once: `reach[i] |= reach[k]` (if `reach[i][k]` is true). This reduces the inner loop to a single fast CPU instruction, drastically speeding up the algorithm.
"""

if __name__ == "__main__":
    demonstrate_path_reconstruction()
    demonstrate_transitive_closure()
    print("\n[SUCCESS] Laboratory: Advanced Floyd-Warshall Completed.")
