"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (SHORTEST PATH ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building Google Maps. You need to find the fastest route from New York 
# to Los Angeles. 
#
# A simple Breadth-First Search (BFS) mathematically guarantees the shortest 
# path *only if all roads take exactly 1 hour to drive*. But the real world is 
# Weighted. A highway takes 5 hours; a dirt road takes 12 hours. BFS fails 
# catastrophically on Weighted Graphs.
#
# You must use Dijkstra's Algorithm. Invented in 1956, it uses a Priority Queue 
# (Min-Heap) to intelligently explore the fastest known roads first, finding 
# the mathematical shortest path in O(E log V) time.
#
# But what if there is a wormhole (a road with a negative time cost)? Dijkstra 
# gets trapped in an infinite loop! You must switch to the Bellman-Ford algorithm, 
# which detects Negative Weight Cycles using dynamic programming.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Dijkstra's Algorithm using Python's `heapq`.
# - Understand the relaxation math of Bellman-Ford.
#
# ==============================================================================
"""

import heapq
from collections import defaultdict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIJKSTRA'S ALGORITHM (O(E log V))
# ==============================================================================
def dijkstra(n: int, edges: list[list[int]], start: int) -> list[float]:
    """
    Finds the shortest path from `start` to all other nodes in a Weighted Graph.
    Time Complexity: O((V + E) log V), Space Complexity: O(V + E)
    """
    # 1. Build Adjacency List
    # Maps u -> list of (weight, v)
    adj = defaultdict(list)
    for u, v, weight in edges:
        adj[u].append((weight, v))
        adj[v].append((weight, u)) # Assume Undirected Graph
        
    # 2. Distance Array
    # Initially, we know it takes 0 distance to reach the start node, 
    # and INFINITY distance to reach every other node!
    distances = {i: float('inf') for i in range(n)}
    distances[start] = 0
    
    # 3. Priority Queue (Min-Heap)
    # Stores tuples of (current_distance_from_start, node)
    pq = [(0, start)]
    
    while pq:
        # Pop the node with the absolute SHORTEST known distance from the start
        current_dist, u = heapq.heappop(pq)
        
        # STALE NODE OPTIMIZATION
        # Because we can't easily update tuples inside a Python heap, we just 
        # push duplicate nodes. If we pop a node with a distance WORSE than 
        # what we already found, we just ignore it!
        if current_dist > distances[u]:
            continue
            
        # Explore all roads branching out from `u`
        for edge_weight, v in adj[u]:
            # The mathematical Relaxation equation
            new_dist = current_dist + edge_weight
            
            # If we found a FASTER path to `v`, update it and push to the queue!
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
                
    return [distances[i] for i in range(n)]

def demonstrate_dijkstra():
    section_header("Dijkstra's Algorithm (Fastest Route)")
    
    # Nodes: 0 to 4
    # Edges: [u, v, weight]
    edges = [
        [0, 1, 4],
        [0, 2, 1],
        [2, 1, 2],
        [1, 3, 1],
        [2, 3, 5],
        [3, 4, 3]
    ]
    
    print("Executing Dijkstra's from Node 0...")
    shortest_paths = dijkstra(5, edges, 0)
    
    for i, dist in enumerate(shortest_paths):
        print(f"Shortest path from 0 to {i}: {dist}")
        
    print("\nNotice how to reach Node 1, it didn't take the direct road (cost 4).")
    print("It took the detour through Node 2 (cost 1 + 2 = 3)! The Min-Heap is magic.")


# ==============================================================================
# 4. BELLMAN-FORD ALGORITHM (NEGATIVE CYCLES)
# ==============================================================================
def bellman_ford(n: int, edges: list[list[int]], start: int):
    """
    Finds the shortest path and detects Negative Weight Cycles.
    Time Complexity: O(V * E), Space Complexity: O(V)
    """
    distances = [float('inf')] * n
    distances[start] = 0
    
    # 1. Relaxation Phase
    # The absolute longest a shortest-path can be without repeating a node 
    # is exactly (V - 1) edges. Therefore, we run the relaxation loop (V - 1) times!
    for _ in range(n - 1):
        for u, v, weight in edges:
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                
    # 2. Cycle Detection Phase
    # If we run the loop a Vth time, and a distance STILL gets mathematically shorter,
    # it means there is a Negative Cycle (an infinite loop dropping the score)!
    for u, v, weight in edges:
        if distances[u] + weight < distances[v]:
            return "NEGATIVE WEIGHT CYCLE DETECTED!"
            
    return distances

def demonstrate_bellman_ford():
    section_header("Bellman-Ford (Negative Cycle Detection)")
    
    # Edges with a negative cycle: 1 -> 2 -> 3 -> 1 (Costs -6)
    # The graph will infinitely loop around this triangle!
    edges = [
        [0, 1, 5],
        [1, 2, 2],
        [2, 3, -6], # Massive Negative Road!
        [3, 1, 2]
    ]
    
    print("Executing Bellman-Ford on a graph with a negative cycle...")
    result = bellman_ford(4, edges, 0)
    print(f"Result: {result}")


def run_all_labs():
    demonstrate_dijkstra()
    demonstrate_bellman_ford()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Dijkstra's Algorithm use a Priority Queue (Min-Heap) instead of a standard Queue like BFS?
   Answer: In BFS, edges have no weight, so the first time a node is discovered, it is mathematically guaranteed to be the absolute shortest path. In a Weighted Graph, a direct edge might cost 50, while a detour taking 10 edges might cost a total of 10. If we use a standard FIFO Queue, we would eagerly lock in the cost of 50. A Priority Queue sorts all discovered paths by their total cumulative cost. The algorithm strictly explores the mathematically "cheapest" known path first. Because edge weights are non-negative, once a node is popped from the Min-Heap, it is impossible for a later path to be cheaper, mathematically guaranteeing the shortest path!

2. Explain the "Stale Node" optimization in Python's implementation of Dijkstra's Algorithm (`if current_dist > distances[u]: continue`).
   Answer: In C++ or Java, `std::set` allows you to find an existing node in the Priority Queue and dynamically update its distance to a smaller value in $O(\log N)$ time. Python's `heapq` module does not support dynamically updating elements. To simulate an update, we simply push a *second* copy of the node into the heap with the newly discovered smaller distance. The smaller distance will naturally bubble to the top and be popped first. Eventually, the older, worse distance will be popped. The `continue` statement identifies this stale, outdated copy and instantly discards it, preventing redundant $O(E)$ edge explorations.

3. Why does Dijkstra's Algorithm catastrophically fail if a Graph contains Negative Edge Weights?
   Answer: Dijkstra is a "Greedy" algorithm. Its mathematical proof of correctness relies on the assumption that adding edges to a path can only *increase* the total distance. Once a node is popped from the Min-Heap, Dijkstra permanently finalizes its shortest path and never looks back. If a graph has a negative edge (e.g., $-10$), a path that looks extremely expensive right now might suddenly become the cheapest path later. Dijkstra will completely blind itself to this possibility and finalize the wrong answer. Bellman-Ford fixes this by abandoning the Greedy strategy and blindly relaxing *all* edges exactly $V-1$ times (Dynamic Programming).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Shortest Path Algorithms Completed.")
