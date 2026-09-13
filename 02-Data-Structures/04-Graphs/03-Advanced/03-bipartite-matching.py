"""
# ==============================================================================
# LABORATORY: MAXIMUM BIPARTITE MATCHING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Imagine you have 5 Uber Drivers and 5 Riders. Each driver is only willing to 
# pick up specific riders based on distance. How do you assign drivers to riders 
# such that the MAXIMUM number of rides occur? 
# 
# This is the "Maximum Bipartite Matching" problem. A Bipartite graph has two 
# distinct sets of nodes (Drivers and Riders), and all edges strictly connect 
# a node from Set A to a node from Set B.
# 
# This can be elegantly solved by transforming it into a Max Flow problem, or 
# by using the specialized Hopcroft-Karp algorithm for maximum efficiency.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to model Bipartite Matching as a Max Flow Network.
# - Understand the concept of the "Super-Source" and "Super-Sink".
# - Implement Hopcroft-Karp (or standard DFS augmenting paths) for Matching.
#
# ==============================================================================
"""

from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MAX FLOW REDUCTION (CONCEPT)
# ==============================================================================
def explain_max_flow_reduction():
    section_header("Concept: Solving Matching via Max Flow")
    print("""
We can solve this problem using the Edmonds-Karp algorithm you just learned!
How?
1. Create a "Super-Source" node. Connect it to every Driver with a pipe of Capacity 1.
2. Create a "Super-Sink" node. Connect every Rider to it with a pipe of Capacity 1.
3. Keep the edges between Drivers and Riders, giving them a Capacity of 1.

Because every node is bottlenecked by a Capacity of 1, running a standard 
Max Flow algorithm will find the maximum number of unique Driver-Rider pairs!
    """)


# ==============================================================================
# 4. DFS AUGMENTING PATHS (STANDARD BIPARTITE MATCHING)
# ==============================================================================
class BipartiteGraph:
    def __init__(self, num_left: int, num_right: int):
        self.left_size = num_left
        self.right_size = num_right
        # adj[u] contains a list of nodes in the right set that left node `u` can connect to
        self.adj: Dict[int, List[int]] = {i: [] for i in range(num_left)}
        
    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)

def bipartite_match_dfs(graph: BipartiteGraph) -> int:
    """
    Finds the maximum bipartite matching using DFS Augmenting Paths.
    Time Complexity: O(V * E)
    
    This is simpler than Hopcroft-Karp and perfectly sufficient for most interviews.
    """
    # match[v] stores the LEFT node assigned to RIGHT node `v`
    # -1 means the right node is currently unmatched
    match = [-1] * graph.right_size
    
    def dfs(u: int, visited: set) -> bool:
        """
        Attempts to find a match for LEFT node `u`.
        Returns True if successful.
        """
        for v in graph.adj[u]:
            # If we haven't already tried to match this right node in the current pass...
            if v not in visited:
                visited.add(v)
                
                # If right node `v` is UNMATCHED, we claim it!
                # OR, if `v` IS matched, but its current owner (match[v]) can be 
                # bumped to a DIFFERENT right node (recursive DFS), we steal `v`!
                if match[v] == -1 or dfs(match[v], visited):
                    match[v] = u
                    return True
        return False

    matches_found = 0
    # Try to find a match for every node in the left set
    for i in range(graph.left_size):
        visited = set()
        if dfs(i, visited):
            matches_found += 1
            
    return matches_found

def demonstrate_bipartite_matching():
    section_header("Algorithm: Bipartite Matching (DFS)")
    
    print("Scenario: 4 Applicants (Left 0-3), 4 Jobs (Right 0-3)")
    print(" Applicant 0 can do Job 1 or 2.")
    print(" Applicant 1 can do Job 0.")
    print(" Applicant 2 can do Job 0 or 3.")
    print(" Applicant 3 can do Job 2.")
    
    bg = BipartiteGraph(4, 4)
    bg.add_edge(0, 1)
    bg.add_edge(0, 2)
    bg.add_edge(1, 0)
    bg.add_edge(2, 0)
    bg.add_edge(2, 3)
    bg.add_edge(3, 2)
    
    max_matches = bipartite_match_dfs(bg)
    
    print(f"\nMaximum Applicants Hired: {max_matches}")
    print("Explanation: App 1 -> Job 0. App 2 -> Job 3. App 3 -> Job 2. App 0 -> Job 1.")
    print("All 4 got hired! The DFS algorithm 'bumped' assignments recursively to make it work.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the recursive call `dfs(match[v], visited)` actually do?
   Answer: This is the "Augmenting Path" logic. It says: "I want Job V, but Applicant X already has it. Hey Applicant X, can you recursively check if there are ANY OTHER jobs you are willing to take?" If Applicant X finds another job, they take it, freeing up Job V for me!

2. Why do we need the `visited` set in the DFS?
   Answer: Without `visited`, we would enter infinite loops. I bump Applicant X from Job V, so Applicant X tries to find a new job. X's other choice is Job W, but Job W is taken by Applicant Y. So Y gets bumped. Y's other choice happens to be Job V! Y tries to bump me, and the cycle continues forever. `visited` ensures a job is only investigated once per DFS pass.

3. What is Hopcroft-Karp and when is it used?
   Answer: The DFS approach takes O(V * E). Hopcroft-Karp uses a BFS pass to find MULTIPLE augmenting paths simultaneously, then uses DFS to apply them all at once. This drastically reduces the time complexity to O(E * sqrt(V)). It is strictly used in advanced competitive programming when the graph has 100,000+ nodes.
"""

if __name__ == "__main__":
    explain_max_flow_reduction()
    demonstrate_bipartite_matching()
    print("\n[SUCCESS] Laboratory: Bipartite Matching Completed.")
