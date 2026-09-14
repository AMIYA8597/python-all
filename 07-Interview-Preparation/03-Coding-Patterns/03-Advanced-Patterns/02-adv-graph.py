"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - ADVANCED GRAPHS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "You are building a package manager like `pip` or `npm`. A user 
# wants to install Package A, which requires Package B, which requires Package C. 
# Write an algorithm to find the exact mathematical installation order."
#
# A junior engineer tries to use nested loops and recursion, gets trapped in a 
# cyclic dependency (A requires B, B requires A), and crashes the server.
#
# A senior engineer recognizes this as a 'Directed Acyclic Graph' (DAG) problem. 
# They instantly deploy Kahn's Algorithm (Topological Sort). By calculating the 
# 'In-Degree' of every node, Kahn's algorithm flawlessly sequences the graph in 
# O(V + E) time, and mathematically proves whether a cyclic paradox exists.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Kahn's Algorithm (Topological Sort / Dependency Resolution).
# - Master Disjoint Set (Union-Find) for Graph Connectivity.
# - Understand the difference between Dijkstra and Topological Sort.
#
# ==============================================================================
"""

import collections
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KAHN'S ALGORITHM (TOPOLOGICAL SORT)
# ==============================================================================
def find_installation_order(num_packages: int, dependencies: List[List[int]]) -> List[int]:
    """
    Time: O(V + E) | Space: O(V + E)
    V = Vertices (Packages), E = Edges (Dependencies)
    dependencies[i] = [a, b] means 'To install a, you must first install b' (b -> a)
    """
    # 1. Initialize the Graph (Adjacency List) and In-Degree array
    # In-Degree means: "How many prerequisites does this package have?"
    adj = {i: [] for i in range(num_packages)}
    in_degree = {i: 0 for i in range(num_packages)}
    
    # 2. Build the Graph
    for dest, src in dependencies:
        adj[src].append(dest)
        in_degree[dest] += 1
        
    print(f"  Graph Adjacency List : {adj}")
    print(f"  Initial In-Degrees   : {in_degree}")
        
    # 3. Find the Absolute Base Cases (Nodes with In-Degree == 0)
    # These are packages with ZERO prerequisites. We can install them immediately!
    queue = collections.deque([n for n in range(num_packages) if in_degree[n] == 0])
    
    install_order = []
    
    # 4. BFS Traversal
    while queue:
        # Install the package!
        current = queue.popleft()
        install_order.append(current)
        print(f"    -> [INSTALLED] Package {current}")
        
        # Now that it's installed, we mathematically 'unlock' all packages that depended on it.
        for neighbor in adj[current]:
            # We decrement the prerequisite count of the neighbor!
            in_degree[neighbor] -= 1
            print(f"       (Package {neighbor} In-Degree reduced to {in_degree[neighbor]})")
            
            # If the neighbor now has 0 prerequisites, it is ready to install!
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 5. CYCLE DETECTION!
    # If the length of our install list doesn't match the total packages, 
    # a circular dependency (paradox) trapped the remaining packages!
    if len(install_order) != num_packages:
        print("  [FATAL ERROR] Cyclic Dependency Detected! Installation Impossible.")
        return []
        
    return install_order

def demonstrate_kahns():
    section_header("Topological Sort (Kahn's Algorithm)")
    
    num = 4
    # 0 depends on 1, 0 depends on 2, 1 depends on 3, 2 depends on 3
    # Directed Graph: 3 -> 1 -> 0
    #                 3 -> 2 -> 0
    deps = [[0, 1], [0, 2], [1, 3], [2, 3]]
    
    print(f"Total Packages: {num}")
    print(f"Dependencies (Dest, Src): {deps}\n")
    
    result = find_installation_order(num, deps)
    print(f"\nResult: Successful Installation Order = {result}")


# ==============================================================================
# 4. DISJOINT SET (UNION-FIND / KRUSKAL'S FOUNDATION)
# ==============================================================================
class UnionFind:
    """
    Time: Amortized O(α(N)) ~ O(1) per operation | Space: O(N)
    Mathematically tracks which nodes belong to which isolated 'Islands' or 'Sets'.
    """
    def __init__(self, n: int):
        # Initially, every node is its own absolute 'Boss' (Parent)
        self.parent = [i for i in range(n)]
        # Used to mathematically balance the tree during a Union
        self.rank = [1] * n
        
    def find(self, n1: int) -> int:
        """
        Recursively climbs the tree to find the absolute Boss of the Set.
        Path Compression: It mathematically rewires the graph so that all nodes 
        point directly to the Boss, crushing a deep O(N) tree into a flat O(1) star!
        """
        # We found the Boss! (The node points to itself)
        if n1 == self.parent[n1]:
            return n1
            
        # PATH COMPRESSION
        self.parent[n1] = self.find(self.parent[n1])
        return self.parent[n1]
        
    def union(self, n1: int, n2: int) -> bool:
        """
        Merges two Sets together.
        Returns False if they were ALREADY in the same Set (Cycle Detected!).
        """
        p1, p2 = self.find(n1), self.find(n2)
        
        # They already have the same Boss! They are in the same Set!
        if p1 == p2:
            return False
            
        # Merge the smaller Set into the larger Set (Union by Rank)
        if self.rank[p1] > self.rank[p2]:
            self.parent[p2] = p1
        elif self.rank[p1] < self.rank[p2]:
            self.parent[p1] = p2
        else:
            self.parent[p1] = p2
            self.rank[p2] += 1
            
        return True

def demonstrate_union_find():
    section_header("Union-Find (Cycle Detection in Undirected Graph)")
    
    print("Graph: We have 3 nodes. Connecting (0,1), then (1,2).")
    uf = UnionFind(3)
    
    print("  Union(0, 1):", uf.union(0, 1))
    print("  Union(1, 2):", uf.union(1, 2))
    
    print("\n  Now we try to connect (0,2).")
    print("  Since 0 is connected to 1, and 1 is connected to 2, 0 and 2 are ALREADY in the same Set!")
    print("  Connecting them would create a Cycle!")
    
    print("  Union(0, 2):", uf.union(0, 2), "(Cycle Detected!)")


def run_all_labs():
    demonstrate_kahns()
    demonstrate_union_find()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does Topological Sort only work on a DAG (Directed Acyclic Graph)?"
   Senior Answer: "Topological Sort relies fundamentally on finding a 'Base Case' node—a node with an In-Degree of exactly 0 (no prerequisites). It installs this node, removes its outgoing edges, and cascades through the graph. If the Graph contains a Cycle (e.g., A requires B, and B requires A), both nodes have an In-Degree of 1. Because there are no nodes with an In-Degree of 0, the Queue is instantly empty, the `while` loop never executes, and the algorithm mathematically deadlocks, proving that cyclic dependency resolution is a logical paradox."

2. Interviewer: "What is the physical difference between 'Path Compression' and 'Union by Rank' in the Union-Find algorithm?"
   Senior Answer: "Union by Rank prevents the tree from becoming a massive, unbalanced Linked List during insertion by mathematically guaranteeing that the shorter tree is always glued under the taller tree, bounding depth to $O(\\log N)$. Path Compression is a read-time optimization that fires during the `find()` operation. When it recursively climbs the tree to find the 'Boss' node, it rewires the `parent` pointer of every single node along the path to point *directly* to the Boss. It violently flattens the tree. Combined, these two heuristics crush the algorithmic time complexity of Union-Find down to the Inverse Ackermann function $\\alpha(N)$, which is practically a pure $O(1)$ constant time for any theoretically computable dataset."

3. Interviewer: "If I want to find the Shortest Path in a weighted graph (e.g., Google Maps), can I use Topological Sort?"
   Senior Answer: "No. Topological Sort is purely for scheduling tasks and resolving dependencies in a DAG. It has absolutely no concept of 'Edge Weights' (distance). To find the shortest path in a weighted graph, you MUST use Dijkstra's Algorithm, which uses a Min-Heap (Priority Queue) to relentlessly pursue the mathematically shortest available edge, or the Bellman-Ford algorithm if the graph contains negative edge weights."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Advanced Graphs) Completed.")
