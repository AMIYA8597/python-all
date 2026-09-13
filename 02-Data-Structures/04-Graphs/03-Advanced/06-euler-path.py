"""
# ==============================================================================
# LABORATORY: EULERIAN PATHS & CIRCUITS (HIERHOLZER'S ALGORITHM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In 1736, the mathematician Leonhard Euler was asked if it was possible to take 
# a walk through the city of Königsberg, crossing every one of its 7 bridges 
# EXACTLY ONCE. 
# This puzzle invented the entire field of Graph Theory!
#
# - An "Eulerian Path" is a trail in a graph that visits EVERY EDGE exactly once.
# - An "Eulerian Circuit" is an Eulerian Path that starts and ends on the SAME vertex.
# (Do not confuse this with a Hamiltonian Path, which visits every VERTEX exactly once 
# and is NP-Complete).
#
# This algorithm is used in DNA sequencing (de Bruijn graphs), snow plow routing 
# (clearing every street exactly once), and LeetCode #332 (Reconstruct Itinerary).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Degree conditions required for an Eulerian Path to exist.
# - Implement Hierholzer's Algorithm in O(V + E) time.
# - Solve "Reconstruct Itinerary" using Post-Order DFS.
#
# ==============================================================================
"""

from collections import defaultdict
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATHEMATICAL CONDITIONS FOR EULERIAN PATHS
# ==============================================================================
def explain_eulerian_conditions():
    section_header("Concept: The Mathematics of Bridges")
    print("""
Before running any algorithm, you can instantly know if an Eulerian Path exists 
just by counting the Degrees (number of edges) of each node!

For an UNDIRECTED Graph:
- Eulerian Circuit: ALL vertices must have an EVEN degree. (Because every time you 
  enter a node, you must have an edge to exit it).
- Eulerian Path: Exactly ZERO or TWO vertices can have an ODD degree. (If two, 
  they MUST be the Start and End nodes).

For a DIRECTED Graph:
- Eulerian Circuit: Every vertex must have In-Degree == Out-Degree.
- Eulerian Path: 
  - Exactly ONE vertex has (Out-Degree - In-Degree == 1) -> START NODE
  - Exactly ONE vertex has (In-Degree - Out-Degree == 1) -> END NODE
  - All other vertices have In-Degree == Out-Degree.
    """)


# ==============================================================================
# 4. HIERHOLZER'S ALGORITHM (POST-ORDER DFS)
# ==============================================================================
def find_itinerary(tickets: List[List[str]]) -> List[str]:
    """
    LeetCode #332: Reconstruct Itinerary
    Given a list of flight tickets [from, to], reconstruct the itinerary in order.
    Must start at "JFK". If there are multiple valid itineraries, return the one 
    that is smallest in lexical (alphabetical) order.
    
    This is literally Hierholzer's Algorithm for finding an Eulerian Path!
    """
    # 1. Build Adjacency List. 
    # We sort the destinations in REVERSE alphabetical order so we can pop from 
    # the end of the list in O(1) time.
    adj = defaultdict(list)
    
    # Sort tickets alphabetically by destination first
    tickets.sort(key=lambda x: x[1], reverse=True)
    
    for src, dst in tickets:
        adj[src].append(dst)
        
    # The reconstructed path
    itinerary = []
    
    def dfs(node: str):
        # As long as there are outgoing edges from this node...
        while adj[node]:
            # Pop the lexicographically smallest edge
            next_node = adj[node].pop()
            dfs(next_node)
            
        # We only append a node to the itinerary AFTER exploring ALL of its outgoing 
        # edges! This is a Post-Order traversal.
        # Why? If we get stuck in a "dead end" early on, it gets added to the 
        # itinerary LAST. When we reverse the final result, the dead end becomes 
        # the true destination!
        itinerary.append(node)

    # 2. Run Hierholzer's starting from JFK
    dfs("JFK")
    
    # 3. Reverse the post-order result to get the actual path
    return itinerary[::-1]

def demonstrate_hierholzer():
    section_header("Algorithm: Hierholzer's Algorithm (Eulerian Path)")
    
    # Let's look at a tricky case!
    # JFK -> KUL (Dead end!)
    # JFK -> NRT -> JFK
    #
    # If we greedily go JFK -> KUL, we get stuck immediately and fail to use 
    # the other tickets. Hierholzer's solves this brilliantly.
    
    tickets = [
        ["JFK", "KUL"],
        ["JFK", "NRT"],
        ["NRT", "JFK"]
    ]
    
    print("Tickets:")
    for t in tickets: print(f"  {t[0]} -> {t[1]}")
    
    print("\nHow Hierholzer's works:")
    print("1. DFS starts at JFK. It has two choices: KUL or NRT.")
    print("2. Alphabetically, it picks KUL first.")
    print("3. At KUL, there are no edges! DFS finishes for KUL. KUL is appended to the result.")
    print("4. DFS backtracks to JFK. It takes the NRT edge.")
    print("5. At NRT, it takes the edge back to JFK.")
    print("6. At JFK, there are no edges left. JFK is appended.")
    print("7. Finally, it reverses the appended result.")
    
    itinerary = find_itinerary(tickets)
    
    print(f"\nFinal Itinerary: {' -> '.join(itinerary)}")
    print("(Expected: JFK -> NRT -> JFK -> KUL)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between an Eulerian Path and a Hamiltonian Path?
   Answer: Eulerian Path = Visit every EDGE exactly once (Polynomial time, easy). Hamiltonian Path = Visit every NODE exactly once (NP-Complete, mathematically impossible to solve quickly for large graphs).

2. Why must Hierholzer's algorithm use a Post-Order traversal (appending after the loop)?
   Answer: A graph might have a main cycle, and several "dead end" branches. If we append nodes Pre-Order, and we accidentally wander into a dead-end branch first, the itinerary terminates prematurely. Post-Order guarantees that if we hit a dead end, it gets appended first. Because we reverse the list at the end, the dead end correctly becomes the FINAL destination of the journey.

3. Why do we `pop()` the edges from the adjacency list?
   Answer: An Eulerian Path must visit every edge EXACTLY ONCE. By popping the edge, we permanently remove it from the graph, guaranteeing we never traverse it again, preventing infinite loops in cycles.
"""

if __name__ == "__main__":
    explain_eulerian_conditions()
    demonstrate_hierholzer()
    print("\n[SUCCESS] Laboratory: Eulerian Paths Completed.")
