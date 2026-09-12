\"\"\"
Iterative Deepening Depth-First Search (IDDFS)
==============================================

1. Introduction & Why it Exists:
--------------------------------
IDDFS is a state space/graph search strategy in which a depth-limited version of 
Depth-First Search (DFS) is run repeatedly with increasing depth limits until the 
goal is found.
It combines the best of Breadth-First Search (BFS) and DFS:
- It is optimally complete (finds the shortest path on unweighted graphs, like BFS).
- It uses strictly linear memory space O(d), where d is the depth (like DFS), avoiding 
  the exponential memory requirement of BFS.

2. Learning Objectives:
-----------------------
- Understand Depth-Limited Search (DLS).
- Implement IDDFS iteratively by incrementing depth.
- Analyze the asymptotic time complexity (why the repeated searches don't ruin performance).
- Handle cycle detection carefully to maintain space complexity.

3. Concept Explanation:
-----------------------
IDDFS calls DLS with depth 0, then 1, then 2...
Although it re-explores upper levels, the number of nodes at level `d` grows 
exponentially (e.g., branching factor `b^d`). The vast majority of time is spent in 
the deepest level. Thus, the asymptotic time complexity is still O(b^d), matching BFS.
\"\"\"

from typing import Dict, List, Any, Optional

class Graph:
    def __init__(self):
        self.adj: Dict[str, List[str]] = {}
        
    def add_edge(self, u: str, v: str):
        if u not in self.adj:
            self.adj[u] = []
        self.adj[u].append(v)
        
def dls(graph: Graph, node: str, target: str, limit: int, path: List[str]) -> bool:
    \"\"\"
    Depth-Limited Search.
    \"\"\"
    path.append(node)
    
    if node == target:
        return True
        
    if limit <= 0:
        path.pop()
        return False
        
    for neighbor in graph.adj.get(node, []):
        # Note: In a true graph we need to avoid cycles. Since IDDFS targets tree-like 
        # spaces or limits depth strictly, visited sets are sometimes omitted, or maintained 
        # strictly per-path to avoid infinite loops without breaking the O(d) space guarantee.
        if neighbor not in path:
            if dls(graph, neighbor, target, limit - 1, path):
                return True
                
    path.pop()
    return False

def iddfs(graph: Graph, start: str, target: str, max_depth: int) -> Optional[List[str]]:
    \"\"\"
    Iterative Deepening DFS.
    \"\"\"
    for limit in range(max_depth + 1):
        path: List[str] = []
        if dls(graph, start, target, limit, path):
            return path
    return None

if __name__ == \"__main__\":
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    g.add_edge('B', 'D')
    g.add_edge('B', 'E')
    g.add_edge('C', 'F')
    g.add_edge('E', 'G')
    
    target = 'G'
    max_d = 4
    
    print(f\"Searching for {target} using IDDFS...\")
    result = iddfs(g, 'A', target, max_d)
    
    assert result == ['A', 'B', 'E', 'G'], \"Incorrect path found!\"
    print(f\"Path found: {' -> '.join(result)}\")
    print(\"All assertions passed!\")
