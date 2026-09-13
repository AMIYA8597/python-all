"""
# ==============================================================================
# LABORATORY: CYCLE DETECTION (KAHN'S & UNION-FIND)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You previously learned how to detect cycles using DFS. But DFS requires deep 
# recursion and complex 3-state logic for directed graphs. 
# There are two alternative algorithms that are heavily tested in interviews:
# 
# 1. Kahn's Algorithm: Uses BFS and In-Degrees to perform Topological Sort and 
#    detect cycles simultaneously in directed graphs.
# 2. Union-Find (Disjoint Set): The absolute best algorithm for detecting cycles 
#    in an UNDIRECTED graph, as it operates in near O(1) amortized time per edge.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand In-Degrees and implement Kahn's Algorithm.
# - Understand Disjoint Sets and the "Find" and "Union" operations.
# - Implement Union-Find with Path Compression for cycle detection.
#
# ==============================================================================
"""

from collections import deque, defaultdict
from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KAHN'S ALGORITHM (BFS TOPOLOGICAL SORT)
# ==============================================================================
def kahns_algorithm(num_nodes: int, edges: List[List[int]]) -> List[int]:
    """
    LeetCode #207: Course Schedule (Directed Graph Cycle Detection)
    Time Complexity: O(V + E)
    
    Logic:
    1. Calculate the In-Degree (number of incoming edges) for every node.
    2. Put all nodes with an In-Degree of 0 (no prerequisites) into a queue.
    3. Pop a node, add it to the result, and "remove" its outgoing edges by 
       decrementing the In-Degree of its neighbors.
    4. If a neighbor's In-Degree hits 0, add it to the queue.
    5. If the result array doesn't contain all nodes, A CYCLE EXISTS!
    """
    adj = defaultdict(list)
    in_degree = [0] * num_nodes
    
    # Build graph and in-degrees
    for src, dst in edges:
        adj[src].append(dst)
        in_degree[dst] += 1
        
    # Queue initially contains only nodes with 0 incoming edges
    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        # "Remove" this node's edges to its neighbors
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # If we processed every node, no cycle exists!
    if len(topo_order) == num_nodes:
        return topo_order
    else:
        # A cycle exists, returning empty list
        return []

def demonstrate_kahns():
    section_header("Algorithm: Kahn's BFS Cycle Detection")
    
    num_nodes = 4
    # Valid: 0->1, 0->2, 1->3, 2->3
    valid_edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    
    # Invalid: 0->1, 1->2, 2->0 (Cycle!)
    invalid_edges = [[0, 1], [1, 2], [2, 0]]
    
    print("Testing Valid DAG:")
    res1 = kahns_algorithm(num_nodes, valid_edges)
    print(f"Topological Order: {res1} (Cycle? {len(res1) == 0})")
    
    print("\nTesting Invalid Cyclic Graph:")
    res2 = kahns_algorithm(3, invalid_edges)
    print(f"Topological Order: {res2} (Cycle? {len(res2) == 0})")
    print("Why? Because in a cycle, all nodes have an in-degree of at least 1.")
    print("The queue is completely empty at the start, and the algorithm halts!")


# ==============================================================================
# 4. UNION-FIND (DISJOINT SET) FOR UNDIRECTED GRAPHS
# ==============================================================================
class UnionFind:
    """
    Tracks disjoint sets (components) in a graph.
    Every node points to a "parent". The root of a set points to itself.
    """
    def __init__(self, size: int):
        # Initially, every node is its own absolute parent (root)
        self.parent = [i for i in range(size)]
        # Used to keep the tree flat when merging
        self.rank = [1] * size

    def find(self, x: int) -> int:
        """
        Finds the absolute root of the set containing x.
        Uses PATH COMPRESSION: It updates the parent pointer of every node it 
        touches to point directly to the root, flattening the tree to O(1) time.
        """
        if self.parent[x] != x:
            # Recursively find the root, and point this node directly to it!
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merges the sets containing x and y.
        Returns False if they were ALREADY in the same set (meaning this edge creates a CYCLE!).
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        # If they share the same root, they are already connected.
        # Adding an edge between them creates a Cycle!
        if root_x == root_y:
            return False
            
        # Merge by Rank (attach the smaller tree under the taller tree to keep it flat)
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True

def demonstrate_union_find():
    section_header("Algorithm: Union-Find (Undirected Cycle Detection)")
    
    num_nodes = 4
    uf = UnionFind(num_nodes)
    
    edges = [
        (0, 1), # Union successful
        (1, 2), # Union successful
        (2, 3), # Union successful
        (0, 3)  # CYCLE! 0 and 3 are already connected via 1 and 2!
    ]
    
    print("Processing Edges:")
    for u, v in edges:
        success = uf.union(u, v)
        if success:
            print(f" Edge ({u}, {v}) added. (Union Successful)")
        else:
            print(f" Edge ({u}, {v}) REJECTED! Adding this edge creates a Cycle.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does Kahn's algorithm detect a cycle?
   Answer: It relies on In-Degrees (incoming edges). A node is only added to the queue if its In-Degree drops to 0. In a cycle (e.g., A->B->C->A), every node has at least 1 incoming edge from within the cycle. Therefore, none of them will ever drop to 0, they will never enter the queue, and the final output array will be missing these nodes.

2. What is "Path Compression" in a Union-Find data structure?
   Answer: When calling `find(x)`, the function traverses up the parent pointers until it hits the absolute root. During the return phase of the recursion, it updates the parent pointer of EVERY node it touched to point DIRECTLY to the absolute root. Future `find` calls on those nodes take exactly O(1) time.

3. Why is Union-Find better than DFS for Cycle Detection in undirected graphs?
   Answer: If you are building a graph dynamically (adding edges one by one over time), DFS requires you to run an O(V+E) search every single time an edge is added. Union-Find processes each edge in Amortized O(1) time (`Inverse Ackermann function`), detecting cycles instantly on insertion.
"""

if __name__ == "__main__":
    demonstrate_kahns()
    demonstrate_union_find()
    print("\n[SUCCESS] Laboratory: Cycle Detection (Kahn & UF) Completed.")
