"""
# ==============================================================================
# LABORATORY: PUSH-RELABEL (LOCALIZED MAX FLOW)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Ford-Fulkerson, Edmonds-Karp, and Dinic's algorithm all share a fundamental 
# paradigm: "Find a complete path from Start to Target, then push water."
#
# In 1986, Andrew Goldberg and Robert Tarjan completely shattered this paradigm 
# with the Push-Relabel algorithm.
#
# They abandoned the concept of "paths" entirely. Instead, they simulate physics!
# 1. Every node in the graph is a Bucket.
# 2. Every node has a physical "Height" (like a water tower).
# 3. Water flows strictly DOWNHILL.
# 4. We artificially lift the Source node (the water treatment plant) high into 
#    the sky, and pour infinite water into it.
# 5. The Source instantly dumps its water into all adjacent buckets. Those buckets 
#    overflow (Excess Flow).
# 6. If a bucket overflows, it looks for a downhill neighbor and PUSHES the water.
# 7. What if it's trapped in a valley? It RELABELS itself (magically lifts itself 
#    up into the air) until it is physically taller than its neighbor, then pushes!
#
# Any water that reaches the Sink stays there. Any trapped water that cannot reach 
# the Sink will eventually elevate itself so high that it flows BACKWARDS into 
# the Source!
#
# The result? A blazing fast O(V^3) algorithm (or O(V^2 \sqrt{E}) with optimizations) 
# that is strictly localized! A node only ever communicates with its immediate 
# neighbors. This makes it insanely easy to parallelize across GPU cores!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Height (Relabel) and Excess Flow properties.
# - Implement the local PUSH operation.
# - Implement the local RELABEL operation.
#
# ==============================================================================
"""

import math
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PUSH-RELABEL ENGINE (O(V^3))
# ==============================================================================
class PushRelabel:
    def __init__(self, vertices: int, graph: List[List[int]]):
        self.V = vertices
        # The Residual Graph (Adjacency Matrix)
        self.C = [[graph[i][j] for j in range(vertices)] for i in range(vertices)]
        # The actual flow currently sitting inside each pipe
        self.F = [[0] * vertices for _ in range(vertices)]
        # The physical Height of the node (Water Tower)
        self.height = [0] * vertices
        # How much water is overflowing the bucket?
        self.excess = [0] * vertices
        
    def push(self, u: int, v: int) -> bool:
        """
        Attempts to push excess water from `u` downhill to `v`.
        Returns True if successful.
        """
        # We can only push water if `u` is strictly taller than `v`!
        if self.height[u] <= self.height[v]:
            return False
            
        # The pipe must have physical capacity remaining!
        # Capacity = (Maximum Pipe Capacity) - (Current Flow inside it)
        sendable_capacity = self.C[u][v] - self.F[u][v]
        
        if sendable_capacity > 0:
            # We push as much water as possible! 
            # The bottleneck is either the pipe size, or the amount of excess water we have.
            flow_to_push = min(self.excess[u], sendable_capacity)
            
            # Move the water!
            self.excess[u] -= flow_to_push
            self.excess[v] += flow_to_push
            
            # Update the physical flow in the forward pipe
            self.F[u][v] += flow_to_push
            # Create the phantom backward flow!
            self.F[v][u] -= flow_to_push
            
            return True
        return False
        
    def relabel(self, u: int):
        """
        Node `u` has excess water, but all neighbors are taller or equal to it!
        We artificially elevate Node `u` to force the water downhill.
        """
        min_height = math.inf
        
        # Look at all neighbors
        for v in range(self.V):
            # If the pipe to this neighbor has capacity...
            if self.C[u][v] - self.F[u][v] > 0:
                # Find the shortest neighbor!
                if self.height[v] < min_height:
                    min_height = self.height[v]
                    
        # Elevate this node so it is exactly 1 foot taller than its shortest neighbor!
        if min_height != math.inf:
            self.height[u] = min_height + 1
            
            
    def max_flow(self, source: int, sink: int) -> int:
        """
        Executes the localized Push-Relabel algorithm.
        Time Complexity: O(V^3)
        """
        # 1. PREFLOW INITIALIZATION
        # Elevate the Source to height V. This ensures it is taller than every 
        # node in the graph forever (the max physical path length is V-1).
        self.height[source] = self.V
        
        # Max out all pipes leaving the source!
        for v in range(self.V):
            if self.C[source][v] > 0:
                flow = self.C[source][v]
                # Push the water!
                self.F[source][v] += flow
                self.F[v][source] -= flow
                self.excess[v] += flow
                # Source has negative excess (infinite water source)
                self.excess[source] -= flow 
                
        # 2. THE LOCAL PUMPING LOOP
        # Find ANY node (excluding Source and Sink) that is overflowing with water!
        while True:
            overflowing_node = -1
            for i in range(self.V):
                if i != source and i != sink and self.excess[i] > 0:
                    overflowing_node = i
                    break
                    
            if overflowing_node == -1:
                break # NO MORE OVERFLOW! Algorithm is finished!
                
            u = overflowing_node
            
            # 3. PUSH OR RELABEL
            # Try to push water downhill to ANY neighbor
            pushed_successfully = False
            for v in range(self.V):
                if self.push(u, v):
                    pushed_successfully = True
                    break
                    
            # If it's trapped in a valley, ELEVATE IT!
            if not pushed_successfully:
                self.relabel(u)
                
        # Whatever water made it to the Sink is our absolute Maximum Flow!
        return self.excess[sink]


def demonstrate_push_relabel():
    section_header("Algorithm: Push-Relabel (Max Flow)")
    
    vertices = 6
    # Same exact graph as Ford-Fulkerson, Edmonds-Karp, and Dinic's!
    graph = [
        [0, 16, 13, 0,  0,  0 ], 
        [0, 0,  10, 12, 0,  0 ], 
        [0, 4,  0,  0,  14, 0 ], 
        [0, 0,  9,  0,  0,  20], 
        [0, 0,  0,  7,  0,  4 ], 
        [0, 0,  0,  0,  0,  0 ]  
    ]
    
    source = 0
    sink = 5
    
    print("Graph Capacities Matrix:")
    for row in graph: print(row)
        
    print(f"\nExecuting Push-Relabel Algorithm (S={source} -> T={sink})...")
    pr = PushRelabel(vertices, graph)
    max_flow = pr.max_flow(source, sink)
    
    print(f"\nAbsolute Maximum Water Flow: {max_flow} gallons/sec")
    print("(Expected: 23)")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we artificially set the Source height to exactly $V$?
   Answer: In any graph, the longest possible path without cycles is $V-1$ steps. If the Source is at height $V$, it is mathematically guaranteed to be higher than every other node in the entire network for the entire lifespan of the algorithm. This prevents water from flowing back into the Source *until* the water gets completely trapped and nodes are forced to relabel themselves above height $V$ to send the rejected water back!

2. What makes Push-Relabel better for Parallel GPU processing?
   Answer: Dinic's Algorithm uses BFS and DFS. DFS is strictly sequential: it plunges down a path, waiting for the recursive calls to return. You cannot parallelize a Stack easily. Push-Relabel relies ONLY on the immediate local neighbor states (`excess` and `height`). You can assign 1 Node to 1 GPU core. Every core independently checks its own excess and pushes to its neighbors simultaneously. There is no global path calculation!

3. Is the basic $O(V^3)$ implementation the fastest version?
   Answer: No! The basic `while True` loop blindly scans the array from index $0$ to $V$ to find an overflowing node. By using a "Highest-Label Preflow-Push" optimization (storing overflowing nodes in a Priority Queue sorted by height), we always push water from the tallest node first. This mathematically slashes the time complexity from $O(V^3)$ to $O(V^2 \\sqrt{E})$, which makes it fiercely competitive with Dinic's Algorithm.
"""

if __name__ == "__main__":
    demonstrate_push_relabel()
    print("\n[SUCCESS] Laboratory: Push-Relabel Algorithm Completed.")
