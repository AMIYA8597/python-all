"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED GRAPH THEORY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A graph is a network. Some networks have vulnerabilities.
# If you are designing the server infrastructure for AWS, you need to know: 
# "If Server X crashes, does it split the entire network into two disconnected 
# halves?"
#
# Server X is mathematically known as an "Articulation Point" (or a Cut Vertex).
# A cable that splits the network if cut is known as a "Bridge".
#
# You cannot simply simulate removing every single server and running BFS 
# $V$ times. That takes $O(V \times (V+E))$ time. You must use Tarjan's 
# Algorithm, which discovers every single vulnerability in the entire network 
# in exactly $O(V + E)$ time using a single, mathematically beautiful Depth 
# First Search (DFS) involving Discovery Times and Low-Link values.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Topological Sort (Kahn's Algorithm) for Course Dependencies.
# - Understand Tarjan's Algorithm for finding Bridges and Articulation Points.
#
# ==============================================================================
"""

from collections import defaultdict, deque

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TOPOLOGICAL SORT (KAHN'S ALGORITHM)
# ==============================================================================
def kahns_algorithm(n: int, dependencies: list[list[int]]) -> list[int]:
    """
    Given a Directed Acyclic Graph (DAG), returns a valid linear ordering.
    Often framed as: "You must take Course U before Course V."
    Time Complexity: O(V + E)
    """
    adj = defaultdict(list)
    in_degree = [0] * n
    
    # 1. Build Graph & Count In-Degrees
    for u, v in dependencies:
        adj[u].append(v)
        # v requires u to finish first. Therefore, v's prerequisite count increases!
        in_degree[v] += 1
        
    # 2. Find nodes with ZERO prerequisites to start the queue
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    
    topo_order = []
    
    while queue:
        # A node with 0 prerequisites can be safely processed right now!
        u = queue.popleft()
        topo_order.append(u)
        
        for v in adj[u]:
            # u is finished! Decrement the prerequisite count for all its children.
            in_degree[v] -= 1
            
            # If child v now has ZERO remaining prerequisites, enqueue it!
            if in_degree[v] == 0:
                queue.append(v)
                
    # 3. Cycle Detection
    if len(topo_order) != n:
        print("Cycle Detected! A valid Topological Sort is mathematically impossible.")
        return []
        
    return topo_order

def demonstrate_kahns():
    section_header("Topological Sort (Kahn's Algorithm)")
    
    # Courses 0 to 5.
    # [u, v] means "u is a prerequisite for v"
    dependencies = [
        [5, 2], [5, 0], [4, 0], [4, 1], [2, 3], [3, 1]
    ]
    
    print("Course Dependencies:")
    print("5 must precede 2 and 0")
    print("4 must precede 0 and 1")
    print("2 must precede 3")
    print("3 must precede 1\n")
    
    order = kahns_algorithm(6, dependencies)
    print(f"Valid Course Schedule: {order}")


# ==============================================================================
# 4. TARJAN'S ALGORITHM (FINDING BRIDGES)
# ==============================================================================
class TarjanBridges:
    """
    Finds all Bridges (Critical Connections) in an Undirected Graph.
    Time Complexity: O(V + E) using Discovery Time & Low-Link values.
    """
    def __init__(self, n: int, edges: list[list[int]]):
        self.adj = defaultdict(list)
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
            
        self.timer = 0
        # The exact moment (tick) a node was first discovered by the DFS.
        self.discovery = [-1] * n
        # The lowest discovery time reachable from this node (including back-edges!).
        self.low = [-1] * n
        self.bridges = []
        
    def _dfs(self, node: int, parent: int) -> None:
        # 1. Initialize discovery and low times
        self.discovery[node] = self.low[node] = self.timer
        self.timer += 1
        
        # 2. Explore neighbors
        for neighbor in self.adj[node]:
            # Do not bounce immediately back to the node that just called us!
            if neighbor == parent:
                continue
                
            # If the neighbor is UNVISITED, dive into it!
            if self.discovery[neighbor] == -1:
                self._dfs(neighbor, node)
                
                # Backtracking: After returning from the child, update our Low-Link!
                # If the child found a back-edge to an ancient ancestor, we inherit it!
                self.low[node] = min(self.low[node], self.low[neighbor])
                
                # BRIDGE DETECTION MATHEMATICS!
                # If the child's absolute lowest reachable ancestor is strictly GREATER
                # than our discovery time, it means the child has NO back-edges to 
                # anything above us. The only way to reach the child is through this 
                # exact edge! Cutting this edge isolates the child! IT IS A BRIDGE!
                if self.low[neighbor] > self.discovery[node]:
                    self.bridges.append([node, neighbor])
                    
            # If the neighbor WAS visited (and it's not the parent), it's a Back-Edge!
            else:
                self.low[node] = min(self.low[node], self.discovery[neighbor])
                
    def find_bridges(self) -> list[list[int]]:
        # Handle disconnected components!
        for i in range(len(self.discovery)):
            if self.discovery[i] == -1:
                self._dfs(i, -1)
        return self.bridges

def demonstrate_tarjan():
    section_header("Tarjan's Algorithm (Bridge Detection)")
    
    # 4 nodes form a circle (0-1-2-0). 
    # Node 1 connects to Node 3.
    # The edge (1, 3) is a Bridge. If cut, 3 is isolated!
    edges = [
        [0, 1], [1, 2], [2, 0], [1, 3]
    ]
    
    print("Graph Structure:")
    print("0 - 1 - 3")
    print("| /")
    print("2")
    
    tb = TarjanBridges(4, edges)
    bridges = tb.find_bridges()
    
    print(f"\nCritical Bridges Found: {bridges}")
    print("Cutting (1, 3) splits the network!")


def run_all_labs():
    demonstrate_kahns()
    demonstrate_tarjan()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Kahn's Algorithm for Topological Sort, how does the algorithm naturally detect if the graph contains a Cycle (e.g., A requires B, and B requires A)?
   Answer: In a cycle, A has an In-Degree of 1 (waiting on B), and B has an In-Degree of 1 (waiting on A). Kahn's Algorithm relies entirely on the queue, and it only enqueues nodes when their In-Degree drops to exactly 0. Because A and B are locked in a cyclic dependency, neither of their prerequisites will ever finish, meaning their In-Degrees will never drop to 0, and they will *never* enter the queue. The queue will eventually dry up and the algorithm will exit. By checking `if len(topo_order) != total_nodes`, we instantly detect that nodes were left behind and mathematically prove a cycle exists.

2. In Tarjan's Algorithm, what is the conceptual difference between the `discovery` array and the `low` array?
   Answer: The `discovery` array is a static timestamp. It records the exact clock tick that the DFS first touched a node. It never changes. The `low` array is a dynamic mathematical tracker. It represents "The absolute earliest (lowest) timestamp that this node can reach by following any path, including exactly one back-edge." Initially, `low` equals `discovery`. But if a node explores a child, and that child finds a secret back-alley tunnel (back-edge) to an ancient ancestor, the child's `low` value drops. The parent node then inherits this dropped value as the DFS backtracks. 

3. Explain the mathematical condition `if low[neighbor] > discovery[node]:` used to detect a Bridge.
   Answer: Suppose Node $X$ was discovered at Time 5. $X$ steps forward to explore Node $Y$. Node $Y$ and all of its descendants explore the graph searching for a back-edge. After exhausting the entire branch, $Y$ reports its absolute lowest reachable timestamp is 7. Because $7 > 5$, this mathematically proves that $Y$ completely failed to find any back-edge leading to $X$ or anyone older than $X$. Therefore, the *only* physical connection between the ancient graph and $Y$'s subtree is the exact cable connecting $X$ to $Y$. If that cable is cut, $Y$'s subtree is permanently severed. It is a Bridge.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Graph Theory Completed.")
