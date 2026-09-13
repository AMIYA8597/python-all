"""
# ==============================================================================
# LABORATORY: GREEDY APPROXIMATION ALGORITHMS (NP-HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen that some problems are mathematically impossible to solve perfectly 
# on large datasets because they are "NP-Hard" (like the Traveling Salesperson 
# or Vertex Cover).
#
# If a company asks you to route 5,000 delivery trucks, the mathematically perfect 
# answer using Bitmask DP takes O(N^2 * 2^N). 2^5000 is larger than the number of 
# atoms in the observable universe. Your algorithm will crash instantly.
#
# In the real world, we give up on perfection. We use "Approximation Algorithms".
# We write a blazing fast Greedy Algorithm that is mathematically PROVEN to return 
# an answer that is "No worse than X times the optimal answer".
#
# Example: The "Vertex Cover" Problem.
# You must place Security Guards at intersections (vertices) such that every single 
# street (edge) is being watched by at least one guard. Find the MINIMUM guards.
# Finding the perfect minimum is NP-Hard.
#
# But there is a brilliant Greedy Approximation: 
# 1. Pick ANY street (edge).
# 2. Put a guard on BOTH ends of the street.
# 3. Mark all connected streets as "watched".
# 4. Repeat until all streets are watched.
#
# This runs in O(V + E) time. And we can mathematically PROVE it will never use 
# more than EXACTLY TWICE the number of guards of the perfect optimal solution. 
# It is a "2-Approximation Algorithm".
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Approximation Ratios (2-Approx).
# - Implement the Greedy Vertex Cover.
# - Differentiate between Heuristics (no guarantees) and Approximations (proven bounds).
#
# ==============================================================================
"""

from typing import List, Tuple, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GREEDY VERTEX COVER (2-APPROXIMATION)
# ==============================================================================
def vertex_cover_approx(vertices: int, edges: List[Tuple[int, int]]) -> Set[int]:
    """
    Finds an approximate Minimum Vertex Cover.
    Time Complexity: O(E) to loop through all edges.
    Space Complexity: O(V) to store the guards.
    """
    
    # Track which streets (edges) are currently watched.
    # To make this O(1) lookup, we will just destroy the edges from a Set as 
    # we watch them.
    unwatched_edges = set(edges)
    
    # The set of intersections where we place guards.
    guards = set()
    
    # 1. THE GREEDY LOOP
    # While there is at least one street that is NOT being watched...
    while unwatched_edges:
        
        # --- THE GREEDY CHOICE ---
        # Pop ANY random, arbitrary edge. It literally doesn't matter which one!
        # (Sets pop randomly in Python).
        u, v = unwatched_edges.pop()
        
        # Place a guard at BOTH ends of this street!
        guards.add(u)
        guards.add(v)
        
        # --- CASCADE EFFECT ---
        # Because we put guards at `u` and `v`, ANY other street connected to 
        # `u` or `v` is now considered "watched"!
        # We must remove all of them from the unwatched pool.
        
        # (We use a list comprehension to filter out the watched edges. In a true 
        # graph using Adjacency Lists, this is done by iterating neighbors in O(V+E)).
        edges_to_remove = []
        for edge in unwatched_edges:
            # If the street touches our guard at `u` OR `v`...
            if edge[0] == u or edge[0] == v or edge[1] == u or edge[1] == v:
                edges_to_remove.append(edge)
                
        for edge in edges_to_remove:
            unwatched_edges.remove(edge)
            
    return guards


def demonstrate_approximation():
    section_header("Algorithm: Greedy Vertex Cover (2-Approximation)")
    
    # Graph structure:
    # 0 --- 1
    # |     |
    # 2 --- 3
    # |
    # 4 --- 5
    
    vertices = 6
    edges = [
        (0, 1), (0, 2),
        (1, 3), (2, 3),
        (2, 4), (4, 5)
    ]
    
    print("City Map (Intersections & Streets):")
    for e in edges:
        print(f" Street connecting Intersection {e[0]} and {e[1]}")
        
    print("\nExecuting O(E) Greedy Approximation Algorithm...")
    guards = vertex_cover_approx(vertices, edges.copy())
    
    print(f"\nGuards placed at Intersections: {guards}")
    print(f"Total Guards used: {len(guards)}")
    
    print("\nAnalysis:")
    print("The Mathematically Perfect Minimum (NP-Hard) requires EXACTLY 3 guards.")
    print("(e.g., placing them at 0, 3, and 4 watches all streets).")
    print(f"Our blazing-fast Greedy Algorithm placed {len(guards)} guards.")
    print("It is guaranteed by Mathematical Proof to NEVER exceed 2 * Optimal (which is 6).")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the mathematical proof that this is a "2-Approximation"?
   Answer: Look at the algorithm. Every time we loop, we pick an edge (u, v) and add BOTH vertices to the guard pool. By definition, the TRUE mathematically perfect algorithm MUST pick at least one of those two vertices to cover that specific edge! So for every edge we process, the optimal solution adds at least 1 guard, and we add exactly 2 guards. Therefore, our total guard count can never physically exceed 2 times the optimal count!

2. Why not just pick a vertex with the highest degree (most connected streets)?
   Answer: That is a very famous heuristic! It feels smarter to put a guard at the busiest intersection. However, mathematically, the "Highest Degree" heuristic is a TRAP. It can be mathematically proven that on certain bipartite graphs, the Highest Degree heuristic will yield a vertex cover that is $O(\\log V)$ times worse than optimal! The seemingly "dumber" algorithm of picking a random edge and guarding both ends provides a much strictly tighter bound (2-Approximation).

3. What is the difference between a "Heuristic" and an "Approximation"?
   Answer: A Heuristic (like Simulated Annealing, Genetic Algorithms, or picking the highest degree) is a "rule of thumb". It usually works well in practice, but there is NO mathematical guarantee; it could theoretically return an answer 100,000 times worse than optimal. An Approximation Algorithm comes with a rigorous mathematical proof (e.g. "This will never be worse than 1.5x the optimal answer, under any circumstances").
"""

if __name__ == "__main__":
    demonstrate_approximation()
    print("\n[SUCCESS] Laboratory: Approximation Algorithms Completed.")
