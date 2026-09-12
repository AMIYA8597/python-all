"""
## A. Concept Name
Cycle Detection in Graphs

## B. Motivation / Real-World Context
Detecting cycles is crucial in many real-world scenarios such as deadlock detection in operating systems, finding circular dependencies in package managers or build systems, and avoiding infinite loops in network routing.

## C. Core Mechanics
- **Undirected Graph**: A cycle exists if during traversal we visit a node that is already visited and is not the immediate parent of the current node.
- **Directed Graph**: A cycle exists if we encounter a node that is currently in the recursion stack (a back edge).
- **Union-Find**: A disjoint-set data structure can track connected components in an undirected graph. If two vertices of an edge are already in the same set, adding the edge creates a cycle.

## D. Complexity Analysis
- DFS/BFS approaches: Time O(V + E), Space O(V).
- Union-Find: Time O(E * α(V)), Space O(V).

## E. Implementation Details
The implementations below cover DFS for undirected graphs, DFS for directed graphs (using recursion stack), and Union-Find for undirected graphs.

## F. Edge Cases
- Disconnected graphs: Handled by iterating over all vertices and starting a traversal from each unvisited vertex.
- Self-loops: Should be detected as a cycle immediately.
- Empty graphs: Handled gracefully.

## G. Common Pitfalls
- Forgetting to maintain a separate recursion stack for directed graphs (visited set alone is not enough).
- In undirected graphs, treating the immediate parent as a cycle.

## H. Variations / Extensions
- Finding the actual cycle path.
- Cycle detection in property graphs or labeled graphs.

## I. Interview Challenge
Given a directed graph representing prerequisites for courses, determine if it is possible to finish all courses (detect cycle).

## X. Project Connection
Cycle detection is often used in dependency resolution projects (like task schedulers) and compilation tools to ensure DAG (Directed Acyclic Graph) properties are maintained.
"""

from typing import Dict, List, Set, Any

class CycleDetectionUndirected:
    """Basic: Cycle detection in Undirected Graph using DFS."""
    def __init__(self, vertices: int):
        self.graph: Dict[int, List[int]] = {i: [] for i in range(vertices)}
        self.vertices = vertices
        
    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)
        self.graph[v].append(u)

    def is_cyclic(self) -> bool:
        visited = set()
        
        def dfs(node: int, parent: int) -> bool:
            visited.add(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True # Visited and not parent -> Cycle!
            return False

        for i in range(self.vertices):
            if i not in visited:
                if dfs(i, -1):
                    return True
        return False

class CycleDetectionDirected:
    """Intermediate: Cycle detection in Directed Graph using DFS and recursion stack."""
    def __init__(self, vertices: int):
        self.graph: Dict[int, List[int]] = {i: [] for i in range(vertices)}
        self.vertices = vertices
        
    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)

    def is_cyclic(self) -> bool:
        visited = set()
        rec_stack = set()
        
        def dfs(node: int) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True # Back edge -> Cycle!
                    
            rec_stack.remove(node)
            return False

        for i in range(self.vertices):
            if i not in visited:
                if dfs(i):
                    return True
        return False

class UnionFindAdvanced:
    """Advanced: Cycle detection in Undirected Graph using Union-Find."""
    def __init__(self, vertices: int):
        self.parent = list(range(vertices))
        self.rank = [0] * vertices
        
    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i]) # Path compression
        return self.parent[i]
        
    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i == root_j:
            return True # Cycle detected
            
        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1
        return False

def test_undirected_cycle():
    g = CycleDetectionUndirected(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert not g.is_cyclic()
    g.add_edge(2, 0)
    assert g.is_cyclic()
    print("Undirected cycle tests passed.")

def test_directed_cycle():
    g = CycleDetectionDirected(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    assert not g.is_cyclic()
    g.add_edge(2, 0)
    assert g.is_cyclic()
    print("Directed cycle tests passed.")

def test_union_find():
    uf = UnionFindAdvanced(4)
    assert not uf.union(0, 1)
    assert not uf.union(1, 2)
    assert uf.union(0, 2) # Forms cycle 0-1-2-0
    print("Union Find tests passed.")

if __name__ == "__main__":
    print("Running Cycle Detection tests...")
    test_undirected_cycle()
    test_directed_cycle()
    test_union_find()
    print("All tests passed!")
