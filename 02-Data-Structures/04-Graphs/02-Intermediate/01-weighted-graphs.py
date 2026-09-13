"""
# ==============================================================================
# LABORATORY: WEIGHTED GRAPHS & BELLMAN-FORD
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already learned that Dijkstra's algorithm solves the shortest path problem 
# in O(E log V) time. However, Dijkstra has a fatal flaw: it assumes that adding 
# edges to a path always INCREASES the total distance. 
# 
# What if a graph has NEGATIVE weights? (e.g., a financial transaction network 
# where certain trades yield a profit, effectively reducing the cost). 
# Dijkstra will return the wrong answer.
# Even worse, what if there is a NEGATIVE CYCLE? (A loop that reduces the distance 
# by -5 every time you go around it). The shortest path is mathematically -Infinity!
#
# The Bellman-Ford algorithm solves this. It handles negative weights and can 
# explicitly detect Negative Cycles.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Dijkstra fails on negative weights.
# - Implement Bellman-Ford in O(V * E) time.
# - Detect Negative Cycles using the N-th relaxation step.
#
# ==============================================================================
"""

from typing import List, Tuple, Dict, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BELLMAN-FORD ALGORITHM
# ==============================================================================
class Graph:
    def __init__(self, vertices: int):
        self.V = vertices
        # Bellman-Ford doesn't actually need an Adjacency List. 
        # It just needs a flat list of all edges!
        self.edges: List[Tuple[int, int, int]] = []
        
    def add_edge(self, u: int, v: int, w: int):
        self.edges.append((u, v, w))

def bellman_ford(graph: Graph, start: int) -> Optional[Dict[int, int]]:
    """
    Finds the shortest path from start to all other nodes.
    Time Complexity: O(V * E)
    Space Complexity: O(V)
    
    Returns: A dictionary of shortest distances, or None if a Negative Cycle exists.
    """
    # 1. Initialize distances to Infinity
    distances = {i: float('inf') for i in range(graph.V)}
    distances[start] = 0
    
    # 2. Relax all edges (V - 1) times.
    # Why V - 1? The longest possible path in a graph without cycles is exactly 
    # V - 1 edges long. Therefore, relaxing all edges V - 1 times guarantees 
    # that the shortest paths have propagated through the entire graph.
    for i in range(graph.V - 1):
        # We loop through EVERY SINGLE EDGE in the entire graph
        for u, v, weight in graph.edges:
            # If the node `u` has been reached, and going through `u` to get to `v` 
            # is cheaper than `v`'s current known distance...
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                # Relax the edge! (Update the distance)
                distances[v] = distances[u] + weight
                
    # 3. Detect Negative Cycles
    # If we relax the edges one more time (the V-th time), and a distance STILL 
    # gets smaller, it is mathematically impossible unless a Negative Cycle exists!
    for u, v, weight in graph.edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            print("CRITICAL ERROR: Graph contains a Negative Weight Cycle!")
            return None # The concept of a shortest path is meaningless here
            
    return distances


# ==============================================================================
# 4. EXECUTION & DEMONSTRATION
# ==============================================================================
def demonstrate_bellman_ford():
    section_header("Algorithm: Bellman-Ford (Handling Negative Weights)")
    
    # Graph with a negative weight (but NO negative cycle)
    # 0 --(5)--> 1
    # 0 --(4)--> 2
    # 1 --(-3)-> 2  <-- Negative edge!
    
    # If we use Dijkstra from 0 to 2:
    # 1. Dijkstra sees 0->2 costs 4, and 0->1 costs 5. 
    # 2. It pops 2 (cost 4) and permanently locks it in.
    # 3. Later it pops 1, sees it can go to 2 for a total of 5 - 3 = 2. 
    # 4. Dijkstra ignores it because 2 is already locked in! 
    # Dijkstra outputs 4. The true answer is 2.
    
    g = Graph(3)
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 4)
    g.add_edge(1, 2, -3)
    
    print("Running Bellman-Ford on graph with negative weight...")
    distances = bellman_ford(g, 0)
    
    print("Shortest Distances from Node 0:")
    for node, dist in distances.items():
        print(f"  To Node {node}: {dist}")
        
    print("\nNotice that the distance to Node 2 is correctly identified as 2 (via Node 1).")

def demonstrate_negative_cycle():
    section_header("Algorithm: Detecting Negative Cycles")
    
    # Graph with a Negative Cycle
    # 0 --(1)--> 1
    # 1 --(1)--> 2
    # 2 --(-5)-> 1  <-- Loops back to 1 with a huge negative weight!
    
    g = Graph(3)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 1, -5) # The cycle is 1 -> 2 -> 1, which costs 1 - 5 = -4.
    
    print("Running Bellman-Ford on graph with a Negative Cycle...")
    distances = bellman_ford(g, 0)
    
    if distances is None:
        print("Algorithm safely aborted. A shortest path cannot exist because you could just run the cycle infinitely to reach -Infinity distance.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between Dijkstra and Bellman-Ford?
   Answer: Dijkstra is a Greedy algorithm. It uses a Min-Heap to lock in the shortest path of the closest node, assuming distances only grow. Bellman-Ford is a Dynamic Programming algorithm. It blindly "relaxes" (attempts to improve) EVERY single edge in the graph `V-1` times, guaranteeing that it finds the shortest path even if weights fluctuate negatively.

2. Why does Bellman-Ford iterate exactly V - 1 times?
   Answer: In a graph with V vertices, the absolute longest possible path that doesn't contain a cycle has exactly V - 1 edges. By relaxing every edge V - 1 times, we guarantee that the distance information has propagated through the maximum possible chain length.

3. Why is Dijkstra preferred over Bellman-Ford in almost all real-world applications (like Google Maps)?
   Answer: Bellman-Ford takes O(V * E) time. Dijkstra takes O(E log V) time. For a road network with 1 million intersections and 3 million roads, Dijkstra takes ~60 Million operations (milliseconds). Bellman-Ford would take 3 Trillion operations (hours). Negative roads do not exist in the real world, so Dijkstra is perfectly safe and exponentially faster.
"""

if __name__ == "__main__":
    demonstrate_bellman_ford()
    demonstrate_negative_cycle()
    print("\n[SUCCESS] Laboratory: Bellman-Ford Completed.")
