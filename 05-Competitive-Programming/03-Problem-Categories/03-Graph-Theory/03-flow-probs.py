"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (NETWORK MAX FLOW)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are designing a water pipeline system. There is a Source (a massive 
# reservoir) and a Sink (a city). Between them is a complex web of pipes.
# 
# Each pipe has a physical capacity (e.g., this pipe can only handle 10 
# gallons per minute). If you try to push 50 gallons through the web, what is 
# the maximum amount of water that will actually reach the city without 
# bursting any pipes?
#
# This is the "Maximum Flow" problem. It is arguably the most mathematically 
# beautiful topic in advanced competitive programming. It solves bipartite 
# matching, airline scheduling, and physical routing.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the concept of the Residual Graph (Backwards Edges).
# - Understand the Ford-Fulkerson method.
# - Implement Edmonds-Karp (Ford-Fulkerson using BFS).
#
# ==============================================================================
"""

from collections import defaultdict, deque

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EDMONDS-KARP ALGORITHM (O(V E^2))
# ==============================================================================
class MaxFlow:
    """
    Implements the Edmonds-Karp algorithm for Maximum Flow.
    Time Complexity: O(V * E^2)
    Space Complexity: O(V + E)
    """
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        # The physical network of pipes
        self.adj = defaultdict(list)
        # 2D Matrix storing the remaining CAPACITY of every pipe
        self.capacity = [[0] * num_nodes for _ in range(num_nodes)]
        
    def add_edge(self, u: int, v: int, cap: int) -> None:
        """
        Adds a directed pipe from u to v with capacity `cap`.
        CRITICAL: We must also initialize the mathematical "Backwards Edge" 
        from v to u with 0 capacity. This allows the algorithm to "undo" bad decisions!
        """
        self.adj[u].append(v)
        self.adj[v].append(u) # Backwards edge for Residual Graph
        self.capacity[u][v] += cap

    def _bfs(self, source: int, sink: int, parent: list[int]) -> int:
        """
        Uses Breadth-First Search (BFS) to find ANY path from Source to Sink 
        that still has remaining capacity > 0.
        Returns the bottleneck (the smallest pipe) on that specific path.
        """
        # Reset parent tracking for this BFS run
        for i in range(self.n):
            parent[i] = -1
            
        parent[source] = -2 # Special marker for the root
        
        # Queue stores (current_node, current_bottleneck_flow)
        queue = deque([(source, float('inf'))])
        
        while queue:
            u, flow = queue.popleft()
            
            for v in self.adj[u]:
                # If we haven't visited V, AND the pipe still has physical room left:
                if parent[v] == -1 and self.capacity[u][v] > 0:
                    parent[v] = u
                    
                    # The bottleneck is the smallest pipe encountered so far
                    new_flow = min(flow, self.capacity[u][v])
                    
                    if v == sink:
                        return new_flow
                        
                    queue.append((v, new_flow))
                    
        # No path found. The network is completely maxed out!
        return 0

    def calculate_max_flow(self, source: int, sink: int) -> int:
        """
        The Ford-Fulkerson engine.
        Repeatedly finds a path, pushes water, and updates the Residual Graph.
        """
        total_flow = 0
        parent = [-1] * self.n
        
        while True:
            # 1. Find an Augmenting Path using BFS (Edmonds-Karp rule)
            bottleneck_flow = self._bfs(source, sink, parent)
            
            # 2. If no path exists, the mathematical Max Flow is officially achieved!
            if bottleneck_flow == 0:
                break
                
            total_flow += bottleneck_flow
            
            # 3. Traverse the path backwards from Sink to Source, updating the capacities!
            current = sink
            while current != source:
                prev = parent[current]
                
                # Subtract capacity from the Forward Edge (We used up this space!)
                self.capacity[prev][current] -= bottleneck_flow
                
                # ADD capacity to the Backwards Edge (The Residual Graph Magic!)
                # This mathematically allows future BFS runs to "push water backwards" 
                # to undo this decision if a better global route is found later!
                self.capacity[current][prev] += bottleneck_flow
                
                current = prev
                
        return total_flow

def demonstrate_edmonds_karp():
    section_header("Max Flow (Edmonds-Karp)")
    
    # Let's build a network with 6 nodes.
    # 0 = Source, 5 = Sink
    mf = MaxFlow(6)
    
    # Adding pipes: add_edge(u, v, capacity)
    mf.add_edge(0, 1, 16)
    mf.add_edge(0, 2, 13)
    mf.add_edge(1, 2, 10)
    mf.add_edge(1, 3, 12)
    mf.add_edge(2, 1, 4)
    mf.add_edge(2, 4, 14)
    mf.add_edge(3, 2, 9)
    mf.add_edge(3, 5, 20)
    mf.add_edge(4, 3, 7)
    mf.add_edge(4, 5, 4)
    
    print("Simulating Water Flow from Source (0) to Sink (5)...")
    result = mf.calculate_max_flow(0, 5)
    print(f"Absolute Maximum Flow mathematically possible: {result} gallons")
    print("(Expected Answer: 23)")


def run_all_labs():
    demonstrate_edmonds_karp()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In the Ford-Fulkerson method, what is the mathematical purpose of the "Backwards Edge" in the Residual Graph (`capacity[current][prev] += flow`)?
   Answer: The Backwards Edge is the most brilliant concept in Max Flow. Suppose you use BFS, and it greedily finds a path sending 10 gallons of water down the middle pipe. Later, the algorithm realizes that sending water down the middle pipe blocked a massive 50-gallon side route! Because the algorithm is greedy, how can it correct this mistake? The Backwards Edge! When the algorithm pushed 10 gallons forward, it mathematically added 10 gallons of capacity to the *backwards* edge. In the next BFS run, the algorithm can explicitly route 10 gallons *backwards* through the pipe. Mathematically, "pushing 10 gallons backward" exactly cancels out the "10 gallons forward" from the previous run, effectively "undoing" the bad decision and allowing the water to dynamically reroute to achieve the absolute global maximum flow.

2. Ford-Fulkerson relies on finding ANY augmenting path. Why does the Edmonds-Karp implementation specifically force the use of Breadth-First Search (BFS) to find the path, instead of DFS?
   Answer: If you use DFS to find a path, you might accidentally find a deeply winding, mathematically terrible path that only pushes 1 gallon of water. If the graph capacities are extremely large (e.g., $10^9$), DFS might run a billion times, pushing 1 gallon back and forth in a pathological infinite loop, resulting in a disastrous $O(E \times \text{MaxFlow})$ time limit exceeded (TLE). Edmonds-Karp forces the use of BFS. BFS mathematically guarantees that it always finds the path with the *fewest number of edges*. Jack Edmonds and Richard Karp mathematically proved in 1972 that if you strictly choose the shortest unweighted path, the algorithm will terminate in exactly $O(V \times E^2)$ time, making it fiercely immune to pathological edge weights and infinite loops.

3. Name a real-world software engineering problem that can be modeled using Maximum Flow.
   Answer: Bipartite Matching (e.g., Uber or Tinder). Suppose you have 50 Uber Drivers and 50 Riders. Each driver is only willing to pick up a subset of riders based on distance. You want to maximize the total number of rides matched. You model this by creating a "Super Source" node that connects to all 50 Drivers with a capacity of 1. You connect the 50 Riders to a "Super Sink" node with a capacity of 1. You add edges between Drivers and Riders with capacity 1. Running Maximum Flow from the Super Source to the Super Sink will mathematically route the 1s through the graph, yielding the absolute maximum possible number of matched rides!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Network Max Flow Completed.")
