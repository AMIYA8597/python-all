"""
# ==============================================================================
# LABORATORY: GRAPH TRAVERSALS (DFS & BFS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know how to represent a Graph. Now you must traverse it.
# Unlike Trees, Graphs can have CYCLES (Node A points to Node B, which points 
# back to Node A). If you do a simple recursive traversal on a cyclic graph, 
# you will enter an infinite loop and crash with a `RecursionError`.
# To solve this, all Graph Traversals REQUIRE a `visited` Set to track which nodes 
# have already been explored.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Graph DFS (Depth-First Search) using Recursion + Visited Set.
# - Master Graph BFS (Breadth-First Search) using a Queue + Visited Set.
# - Understand when to use BFS (Shortest Path) vs DFS (Connectivity).
# - Count Connected Components in an undirected graph.
#
# ==============================================================================
"""

from collections import defaultdict, deque
from typing import List, Set

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GRAPH TRAVERSAL SETUP
# ==============================================================================
class Graph:
    def __init__(self):
        self.adj = defaultdict(list)
        
    def add_edge(self, u: str, v: str):
        # Undirected graph for these examples
        self.adj[u].append(v)
        self.adj[v].append(u)

def build_sample_graph() -> Graph:
    """
    Builds the following graph:
      A --- B --- C
      |     |
      D --- E
      
      F --- G (Disconnected Component)
    """
    g = Graph()
    edges = [
        ("A", "B"), ("A", "D"), 
        ("B", "C"), ("B", "E"), 
        ("D", "E"), 
        ("F", "G")
    ]
    for u, v in edges:
        g.add_edge(u, v)
    return g


# ==============================================================================
# 4. DEPTH-FIRST SEARCH (DFS)
# ==============================================================================
def graph_dfs(graph: Graph, start_node: str):
    """
    DFS explores as FAR as possible along each branch before backtracking.
    Time Complexity: O(V + E)
    Space Complexity: O(V) for the Call Stack and Visited Set.
    """
    visited = set()
    traversal_path = []
    
    def dfs_recursive(node: str):
        # If we've seen it, stop. (Prevents infinite loops on cycles)
        if node in visited:
            return
            
        # 1. Mark as visited and process
        visited.add(node)
        traversal_path.append(node)
        
        # 2. Explore all neighbors
        for neighbor in graph.adj[node]:
            dfs_recursive(neighbor)
            
    # Start the recursion
    dfs_recursive(start_node)
    return traversal_path

def demonstrate_dfs():
    section_header("Algorithm: Depth-First Search (DFS)")
    g = build_sample_graph()
    
    print("Starting DFS from Node 'A':")
    path = graph_dfs(g, "A")
    print(f"Path: {' -> '.join(path)}")
    print("Notice how it dove deep into D and E before ever touching C!")


# ==============================================================================
# 5. BREADTH-FIRST SEARCH (BFS)
# ==============================================================================
def graph_bfs(graph: Graph, start_node: str):
    """
    BFS explores the graph in "concentric circles" (level by level).
    It is guaranteed to find the SHORTEST PATH in an unweighted graph!
    Time Complexity: O(V + E)
    Space Complexity: O(V) for the Queue and Visited Set.
    """
    visited = set([start_node])
    queue = deque([start_node])
    traversal_path = []
    
    while queue:
        # Pop from the front of the queue
        node = queue.popleft()
        traversal_path.append(node)
        
        # Explore all neighbors
        for neighbor in graph.adj[node]:
            # ONLY add to queue if we haven't visited it
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return traversal_path

def demonstrate_bfs():
    section_header("Algorithm: Breadth-First Search (BFS)")
    g = build_sample_graph()
    
    print("Starting BFS from Node 'A':")
    path = graph_bfs(g, "A")
    print(f"Path: {' -> '.join(path)}")
    print("Notice how it visited B and D (Distance 1) BEFORE touching E and C (Distance 2)!")


# ==============================================================================
# 6. APPLICATION: CONNECTED COMPONENTS
# ==============================================================================
def count_components(graph: Graph) -> int:
    """
    If a graph is disconnected (like islands), a single DFS or BFS will NOT 
    reach every node. We must iterate over all nodes and launch a DFS/BFS 
    whenever we find an unvisited node.
    """
    visited = set()
    components = 0
    
    def dfs(node: str):
        visited.add(node)
        for neighbor in graph.adj[node]:
            if neighbor not in visited:
                dfs(neighbor)
                
    # Loop over EVERY known node in the graph
    for node in graph.adj.keys():
        if node not in visited:
            # We found a new island!
            components += 1
            # Run DFS to map out the entire island and mark it as visited
            dfs(node)
            
    return components

def demonstrate_components():
    section_header("Application: Connected Components")
    g = build_sample_graph()
    
    num_components = count_components(g)
    print(f"The graph contains {num_components} connected components.")
    print("(Expected 2: [A, B, C, D, E] is one component, [F, G] is the other).")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Graph traversal require a `visited` set when a Tree traversal does not?
   Answer: A standard Tree has no cycles. A node cannot point back to its parent or ancestor. A Graph can have cycles. Without a `visited` set to short-circuit the traversal, a cycle (e.g., A -> B -> A -> B) will cause an infinite loop.

2. If you want to find the Shortest Path out of a maze, should you use DFS or BFS?
   Answer: You MUST use BFS. BFS expands level-by-level, meaning the very first time it encounters the exit, it is mathematically guaranteed to be the shortest path. DFS explores deep into dead-ends first, and while it might find the exit, it will likely be a very long, winding path.

3. When building the BFS queue, should you mark the node as `visited` WHEN you pop it, or WHEN you push it?
   Answer: You MUST mark it as `visited` WHEN YOU PUSH IT to the queue. If you wait until you pop it, multiple neighbors might see that the node is "unvisited" and push duplicate copies of the same node onto the queue, exploding your memory to O(V^2)!
"""

if __name__ == "__main__":
    demonstrate_dfs()
    demonstrate_bfs()
    demonstrate_components()
    print("\n[SUCCESS] Laboratory: Graph Traversals Completed.")
