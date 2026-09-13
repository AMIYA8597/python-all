"""
# ==============================================================================
# LABORATORY: ADVANCED BIPARTITE MATCHING (HOPCROFT-KARP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Bipartite Matching can be solved using DFS Augmenting Paths 
# in O(V * E) time. For 99% of interviews, that is sufficient. 
# However, if you are working at Uber matching 100,000 drivers to 100,000 riders, 
# O(V * E) is too slow (potentially 100,000 * 1,000,000 operations).
#
# The Hopcroft-Karp algorithm is the absolute state-of-the-art for this problem, 
# reducing the time complexity to exactly O(E * sqrt(V)).
# It achieves this magic by running BFS to find the SHORTEST augmenting paths 
# in bulk, and then using DFS to actually apply those paths simultaneously.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how BFS groups unmatched nodes by shortest distance.
# - Understand the role of the Dummy Node (0).
# - Implement the Hopcroft-Karp algorithm.
#
# ==============================================================================
"""

from collections import deque
from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HOPCROFT-KARP IMPLEMENTATION
# ==============================================================================
class HopcroftKarp:
    """
    We assume vertices are 1-indexed for both Left and Right sets.
    Node 0 is treated as a special "Dummy Node" representing an UNMATCHED state.
    """
    def __init__(self, num_left: int, num_right: int):
        self.U = num_left   # Left set
        self.V = num_right  # Right set
        # Adjacency list: Left node -> List of Right nodes
        self.adj: Dict[int, List[int]] = {u: [] for u in range(1, num_left + 1)}
        
    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)

    def execute(self) -> int:
        # pair_u[u] = The right node matched to left node u
        # pair_v[v] = The left node matched to right node v
        # 0 means unmatched!
        pair_u = [0] * (self.U + 1)
        pair_v = [0] * (self.V + 1)
        dist = [0] * (self.U + 1)
        
        def bfs() -> bool:
            """
            Builds distance layers from unmatched left nodes to unmatched right nodes.
            Returns True if at least one augmenting path was found.
            """
            queue = deque()
            
            # Start BFS from all currently UNMATCHED left nodes
            for u in range(1, self.U + 1):
                if pair_u[u] == 0:
                    dist[u] = 0
                    queue.append(u)
                else:
                    dist[u] = float('inf')
                    
            # Set distance to Dummy Node as Infinity
            dist[0] = float('inf')
            
            while queue:
                u = queue.popleft()
                
                # If distance of u is less than the shortest path to dummy node found so far...
                if dist[u] < dist[0]:
                    for v in self.adj[u]:
                        # pair_v[v] is the left node currently owning v
                        # If pair_v[v] is 0, it's unmatched (Dummy node!)
                        next_u = pair_v[v]
                        
                        # If this left node hasn't been visited yet...
                        if dist[next_u] == float('inf'):
                            # Assign its distance
                            dist[next_u] = dist[u] + 1
                            queue.append(next_u)
                            
            # If dist[0] is no longer Infinity, it means we successfully reached 
            # the Dummy Node (found an unmatched right node!)
            return dist[0] != float('inf')
            
        def dfs(u: int) -> bool:
            """
            Traverses the exact distance layers built by BFS to apply the matches.
            """
            if u != 0:
                for v in self.adj[u]:
                    next_u = pair_v[v]
                    
                    # We ONLY follow edges that move strictly to the next distance layer
                    if dist[next_u] == dist[u] + 1:
                        # Recursively try to match the next node
                        if dfs(next_u):
                            # Success! We can claim this match
                            pair_v[v] = u
                            pair_u[u] = v
                            return True
                            
                # If no match found down this path, mark distance to Infinity so 
                # we don't try it again during this phase
                dist[u] = float('inf')
                return False
            return True # Reached Dummy Node 0, success!

        # Core execution loop
        matching = 0
        
        # While BFS can find AT LEAST ONE augmenting path...
        while bfs():
            # Apply DFS for ALL unmatched left nodes
            for u in range(1, self.U + 1):
                if pair_u[u] == 0:
                    if dfs(u):
                        matching += 1
                        
        return matching

def demonstrate_hopcroft_karp():
    section_header("Algorithm: Hopcroft-Karp O(E * sqrt(V))")
    
    print("Scenario: 4 Applicants (Left), 4 Jobs (Right) - 1 Indexed")
    print(" App 1 -> Job 1, 2")
    print(" App 2 -> Job 1")
    print(" App 3 -> Job 1, 4")
    print(" App 4 -> Job 3")
    
    hk = HopcroftKarp(4, 4)
    hk.add_edge(1, 1)
    hk.add_edge(1, 2)
    hk.add_edge(2, 1)
    hk.add_edge(3, 1)
    hk.add_edge(3, 4)
    hk.add_edge(4, 3)
    
    matches = hk.execute()
    
    print(f"\nMaximum Applicants Hired: {matches}")
    print("Explanation:")
    print(" App 2 takes Job 1 (its only choice).")
    print(" App 1 takes Job 2.")
    print(" App 4 takes Job 3 (its only choice).")
    print(" App 3 takes Job 4.")
    print(" All 4 got hired flawlessly!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Hopcroft-Karp use BFS and DFS together?
   Answer: Simple DFS matching evaluates paths one by one, often taking extremely long, convoluted paths to bump matches around. Hopcroft-Karp uses BFS to map out the SHORTEST possible augmenting paths for ALL unmatched nodes simultaneously, grouping them into "distance layers". The DFS then strictly follows these layers to quickly apply the matches in bulk.

2. What does Node 0 (the Dummy Node) represent?
   Answer: In this implementation, `pair_v[v]` returns the left node matched to right node `v`. If `v` is UNMATCHED, it returns `0`. By setting `dist[0]`, the BFS naturally tracks the shortest distance to any unmatched right node without needing complex flags.

3. Why is the time complexity exactly O(E * sqrt(V))?
   Answer: This is a famous mathematical proof. It is proven that any augmenting path strictly increases the size of the matching. Furthermore, it is proven that after exactly `sqrt(V)` BFS/DFS phases, the remaining unmatched paths (if any) are so long that they are disjoint, and a final DFS resolves them all in O(E) time.
"""

if __name__ == "__main__":
    demonstrate_hopcroft_karp()
    print("\n[SUCCESS] Laboratory: Advanced Bipartite Matching Completed.")
