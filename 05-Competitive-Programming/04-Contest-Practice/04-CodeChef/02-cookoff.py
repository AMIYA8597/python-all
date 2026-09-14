"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CODECHEF COOK-OFF)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The CodeChef Cook-Off is a 2.5-hour short-format sprint. Speed and pattern 
# recognition are everything. 
#
# A classic Cook-Off problem: "You have a network of N computers and M cables. 
# Over time, cables are slowly cut, permanently breaking connections. You receive 
# queries asking: 'Are computers A and B still connected?'"
#
# If you run a DFS/BFS every time a cable is cut, it takes O(N) per query, 
# resulting in a Time Limit Exceeded (TLE).
#
# Can you use a Disjoint Set Union (DSU)? A standard DSU is incredibly fast 
# at ADDING connections. But mathematically, a DSU CANNOT REMOVE connections 
# without completely rebuilding the tree from scratch (which takes O(N)).
#
# The solution is a famous CP pattern: "Time Reversal". 
# You read all the queries in advance (Offline). You destroy all the cables 
# that are *going* to be cut. Then, you process the timeline strictly BACKWARDS! 
# Instead of cutting cables, you are now mathematically ADDING cables back into 
# the DSU! You answer all queries instantly in O(1) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Disjoint Set Union (DSU) architecture.
# - Master the Offline Time Reversal pattern for Graph Destruction queries.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DISJOINT SET UNION (DSU)
# ==============================================================================
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i: int) -> int:
        """Finds the Root of the set, with Path Compression."""
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """Unites two sets using Union by Size."""
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i == root_j:
            return False # Already connected
            
        # Attach the smaller tree under the larger tree!
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i
            
        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]
        return True

# ==============================================================================
# 4. OFFLINE TIME REVERSAL ALGORITHM
# ==============================================================================
def solve_offline_destruction(n: int, edges: list[tuple[int, int]], queries: list[tuple[str, int, int]]) -> list[bool]:
    """
    Simulates destroying edges and checking connectivity.
    Queries format: 
      ("CUT", edge_index, 0)
      ("CHECK", node_u, node_v)
      
    Time Complexity: O(Q * alpha(N)) -> virtually O(Q)
    """
    dsu = DSU(n)
    
    # 1. Identify exactly which edges are doomed to be cut at ANY point in time.
    cut_edges = set()
    for q_type, u, v in queries:
        if q_type == "CUT":
            cut_edges.add(u) # u holds the edge_index here
            
    # 2. Build the "End of Time" Graph. 
    # Add all edges that survived the entire timeline without ever being cut.
    for i, (u, v) in enumerate(edges):
        if i not in cut_edges:
            dsu.union(u, v)
            
    answers = []
    
    # 3. Time Reversal! Process the queries BACKWARDS.
    for i in range(len(queries) - 1, -1, -1):
        q_type, u, v = queries[i]
        
        if q_type == "CHECK":
            # Are they connected AT THIS MOMENT in the timeline?
            is_connected = dsu.find(u) == dsu.find(v)
            answers.append(is_connected)
            
        elif q_type == "CUT":
            # Going backwards in time, a "CUT" is mathematically a "REPAIR"!
            # We magically restore the edge in the DSU!
            edge_to_restore = edges[u] 
            dsu.union(edge_to_restore[0], edge_to_restore[1])
            
    # The answers were collected backwards, so we must reverse them 
    # to match the true chronological timeline!
    answers.reverse()
    
    return answers

def demonstrate_time_reversal():
    section_header("Offline Time Reversal (DSU Destruction)")
    
    n = 4
    edges = [
        (0, 1), # Edge 0
        (1, 2), # Edge 1
        (2, 3)  # Edge 2
    ]
    
    queries = [
        ("CHECK", 0, 3), # Expected: True (All edges exist)
        ("CUT", 1, 0),   # Cut Edge 1 (disconnects 0,1 from 2,3)
        ("CHECK", 0, 3), # Expected: False
        ("CHECK", 0, 1), # Expected: True (0 and 1 are still connected)
        ("CUT", 0, 0),   # Cut Edge 0 (disconnects 0 from 1)
        ("CHECK", 0, 1)  # Expected: False
    ]
    
    print(f"Nodes: {n}")
    print(f"Initial Edges: {edges}")
    print("\nChronological Events:")
    for q in queries:
        if q[0] == "CHECK":
            print(f"  Are {q[1]} and {q[2]} connected?")
        else:
            print(f"  [!] Edge {q[1]} was completely DESTROYED!")
            
    ans = solve_offline_destruction(n, edges, queries)
    
    print("\nChronological Answers:")
    check_idx = 0
    for q in queries:
        if q[0] == "CHECK":
            print(f"  Query {check_idx}: {ans[check_idx]}")
            check_idx += 1
            
    print("\nThe DSU solved a destructive problem by processing the entire ")
    print("timeline backwards and repairing edges instead of destroying them!")


def run_all_labs():
    demonstrate_time_reversal()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is a standard Disjoint Set Union (DSU) completely incapable of processing "Remove Edge" operations?
   Answer: A DSU uses "Path Compression". When `find(x)` is called, it takes every node along the path to the root and mathematically snaps them directly to the root, completely destroying the original tree hierarchy. Because the original physical structure of the tree is irreversibly flattened to guarantee $O(1)$ speed, if you try to "remove" an edge, the DSU has absolutely no physical memory of what the tree looked like before the edge was added. The nodes are permanently tangled. To safely remove an edge, you would have to completely clear the DSU and rebuild it from scratch, running at $O(N)$.

2. Explain the philosophical concept of "Offline Time Reversal" in graph problems.
   Answer: If a data structure is magnificent at ADDING things (like DSU), but mathematically incapable of REMOVING things, and the problem asks you to REMOVE things over time... you change the flow of time! By reading all queries in advance (Offline), you can look at the absolute end of the universe (the state of the graph after every single cut has occurred). You build this broken graph. Then, you read the timeline from end-to-beginning. A chronological "Cut" becomes a retrograde "Add". You magically transform a destructive problem into a constructive problem, allowing the DSU to operate natively in $O(1)$!

3. In the DSU `union` function, what is "Union by Size" and why is it critical?
   Answer: If you naively attach Tree A to Tree B indiscriminately, you can mathematically create a worst-case scenario where the Tree degenerates into a single long linked list (a straight line). If this happens, `find()` degenerates to $O(N)$ time, crashing the algorithm. "Union by Size" physically counts the number of nodes in both trees. It mathematically guarantees that the smaller tree is ALWAYS attached as a child of the larger tree. This forces the tree to remain incredibly wide and shallow. By combining Union by Size with Path Compression, the depth of the tree will never exceed $\approx 4$, achieving the near-constant Ackermann time bound $O(\alpha(N))$.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CodeChef Cook-Off Completed.")
