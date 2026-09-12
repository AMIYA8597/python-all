"""
=============================================================================
MAXIMUM BIPARTITE MATCHING - FROM BEGINNER TO PROFESSIONAL
=============================================================================

### 1. Intuition & Real-World Analogy
Imagine you are organizing a job fair. You have a set of `Applicants` (Left side) 
and a set of `Jobs` (Right side). 
Each applicant has a list of jobs they are qualified for, and each job has one opening.
A "matching" is an assignment of applicants to jobs such that:
1. No applicant is assigned to more than one job.
2. No job is assigned to more than one applicant.

The goal? Assign as many applicants to jobs as possible. This is the 
Maximum Bipartite Matching (MBM) problem. 

### 2. Formal Explanation
A graph G = (V, E) is bipartite if its vertices can be partitioned into two 
disjoint sets, L and R, such that every edge in E connects a vertex in L to a vertex in R.
- **Matching (M)**: A subset of edges where no two edges share a common vertex.
- **Maximum Matching**: A matching of maximum possible size.
- **Augmenting Path**: A path that alternates between edges not in M and edges in M,
  starting and ending at an unmatched vertex.
According to **Berge's Lemma**, a matching M is maximum if and only if there 
is no augmenting path. 

### 3. Implementation - Hopcroft-Karp vs DFS Approach
While the DFS-based approach (Ford-Fulkerson simplified for unit networks) is O(V * E),
the **Hopcroft-Karp** algorithm provides a much faster O(E * sqrt(V)) time complexity
by finding multiple shortest augmenting paths simultaneously using BFS and DFS.
For educational purposes, we provide the clean DFS-based approach often asked in interviews, 
followed by a discussion of its real-world implementation.

"""

from typing import List, Dict, Optional, Set

class BipartiteMatcher:
    """
    A class to perform Maximum Bipartite Matching.
    
    Sets:
      U (Left Side) - Indexed 0 to left_size - 1
      V (Right Side) - Indexed 0 to right_size - 1
    """
    def __init__(self, left_size: int, right_size: int):
        self.left_size = left_size
        self.right_size = right_size
        
        # Adjacency list for U to V
        # adj[u] contains a list of v's that u is connected to.
        self.adj: List[List[int]] = [[] for _ in range(left_size)]

    def add_edge(self, u: int, v: int) -> None:
        """
        Adds a directed edge from U (left) to V (right).
        
        Args:
            u: Index of the vertex in the left set (0-indexed).
            v: Index of the vertex in the right set (0-indexed).
        """
        if 0 <= u < self.left_size and 0 <= v < self.right_size:
            self.adj[u].append(v)
        else:
            raise ValueError(f"Edge ({u}, {v}) is out of bounds.")

    def _dfs_augment(self, u: int, match_r: List[int], seen: List[bool]) -> bool:
        """
        A DFS based function that returns True if a matching for vertex u is possible.
        
        Args:
            u: The current vertex in the left set to find a match for.
            match_r: An array where match_r[v] is the vertex in the left set assigned to right vertex v.
            seen: A boolean array to keep track of visited right vertices in the current DFS.
            
        Returns:
            True if an augmenting path is found, otherwise False.
        """
        # Try every job (vertex v in Right Set) that applicant u is interested in
        for v in self.adj[u]:
            # If job v is not visited in this DFS traversal
            if not seen[v]:
                seen[v] = True # Mark job v as visited
                
                # If job v is not assigned to any applicant OR 
                # previously assigned applicant for job v (match_r[v]) has an alternate job available
                if match_r[v] == -1 or self._dfs_augment(match_r[v], match_r, seen):
                    # We can assign job v to applicant u
                    match_r[v] = u
                    return True
        return False

    def max_matching(self) -> int:
        """
        Calculates the maximum number of matches possible.
        
        Returns:
            The size of the maximum matching.
        """
        # match_r keeps track of which applicant (U) is assigned to which job (V)
        # Initially, all jobs are available (-1)
        match_r = [-1] * self.right_size
        
        result = 0 # Count of matches
        
        # Iterate over all applicants in the left set
        for i in range(self.left_size):
            # For each applicant, clear the 'seen' array (reset visited jobs)
            seen = [False] * self.right_size
            
            # Find if applicant 'i' can get a job
            if self._dfs_augment(i, match_r, seen):
                result += 1
                
        return result

    def get_matches(self) -> Dict[int, int]:
        """
        Retrieves the exact assignments after computing the maximum matching.
        Call this ONLY after calling max_matching() to ensure it's calculated, 
        or call it internally. (For simplicity, we'll recompute here).
        
        Returns:
            A dictionary mapping Left vertex (applicant) -> Right vertex (job).
        """
        match_r = [-1] * self.right_size
        for i in range(self.left_size):
            seen = [False] * self.right_size
            self._dfs_augment(i, match_r, seen)
            
        # Reconstruct mapping from U to V
        matches = {}
        for v in range(self.right_size):
            u = match_r[v]
            if u != -1:
                matches[u] = v
        return matches

"""
### 4. Complexity Analysis

- **Time Complexity:** O(V_L * E) where V_L is the number of vertices in the left set, 
  and E is the total number of edges. 
  In the worst case, for each vertex in L, we might explore the entire edge set in the DFS.
- **Space Complexity:** O(V_L + V_R + E) for the adjacency list representation. 
  The `seen` and `match_r` arrays take O(V_R) space. 
  The DFS recursion stack takes up to O(V_L) space. Thus, overall O(V + E) space.

### 5. Debugging & Common Mistakes
- **Shared `seen` array across loop iterations**: A common mistake is initializing the 
  `seen` array outside the main loop in `max_matching`. It MUST be reinitialized for 
  every vertex `i` in `self.left_size`. If you don't reset it, the DFS will incorrectly 
  think vertices are permanently exhausted.
- **Off-by-one indices**: Bipartite matching often maps left vertices to right vertices. 
  Ensure your U and V sets are strictly 0-indexed up to their respective sizes.
- **Applying to non-bipartite graphs**: This algorithm only works if the graph can be split 
  into two independent sets. For general graphs, you must use Edmonds' Blossom algorithm.

### 6. Active Recall & Memory Anchors
- **Memory Anchor**: "Applicant looking for a Job". If the job is taken, ask the current 
  job-holder to find *another* job. If they can, you take this job! This chain reaction 
  is exactly what the DFS does (finding an Augmenting Path).
- **Q**: What does Berge's Lemma state?
  **A**: A matching is maximum iff there are no augmenting paths. 
- **Q**: Why reset `seen` inside the loop for each left vertex?
  **A**: Because an augmenting path search for vertex `i` might need to visit a right-vertex 
  that was previously explored unsuccessfully for a different starting vertex `k`.

### 7. Professional Application
In actual production systems (e.g., Uber matching riders to drivers, or Kubernetes assigning 
pods to nodes), we often use weighted bipartite matching (the Hungarian Algorithm/Kuhn-Munkres) 
or network flow (Min-Cost Max-Flow) to optimize for distance/cost, not just the maximum 
number of assignments.
"""

def test_bipartite_matching():
    # Example: 4 Applicants (0, 1, 2, 3) and 4 Jobs (0, 1, 2, 3)
    # 0 is interested in 1, 2
    # 1 is interested in 0, 1
    # 2 is interested in 2
    # 3 is interested in 2, 3
    matcher = BipartiteMatcher(4, 4)
    matcher.add_edge(0, 1)
    matcher.add_edge(0, 2)
    matcher.add_edge(1, 0)
    matcher.add_edge(1, 1)
    matcher.add_edge(2, 2)
    matcher.add_edge(3, 2)
    matcher.add_edge(3, 3)

    max_matches = matcher.max_matching()
    print(f"Maximum number of applicants assigned: {max_matches}")
    
    matches = matcher.get_matches()
    print("Assignments (Applicant -> Job):")
    for applicant, job in sorted(matches.items()):
        print(f"  Applicant {applicant} -> Job {job}")

if __name__ == "__main__":
    test_bipartite_matching()
