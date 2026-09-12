"""
## A. Concept Name
Topological Sort

## B. One-Sentence Definition
Topological sorting of a Directed Acyclic Graph (DAG) is a linear ordering of its vertices such that for every directed edge u -> v, u comes before v in the ordering.

## C. Why Does This Exist?
To resolve dependencies and find a valid sequence of tasks where some tasks must be performed before others (e.g., build systems, course scheduling).

## D. Intuition
If you have a list of tasks with prerequisites, you need to find an order to complete them such that no prerequisite is violated. Topological sort gives you that valid sequence.

## E. Real-Life Analogy
Getting dressed. You must put on your socks before your shoes, and your underwear before your pants. Some things are independent (shirt vs pants), but dependent items must follow a strict order.

## F. Mental Model
Imagine a flowing river with checkpoints. The water only flows in one direction (directed). A topological sort simply lists all the checkpoints in an order where you never have to go "upstream" to reach the next checkpoint in the list.

## G. Visual Explanation
Vertices: {A, B, C, D}
Edges (dependencies): A->C, B->C, C->D
Valid Topological Orders: 
1. A, B, C, D
2. B, A, C, D
(Both A and B must come before C, and C before D)

## H. Formal Explanation
A topological sort of a graph G = (V, E) is a linear ordering of V such that for every edge (u, v) in E, u appears before v in the ordering. It is ONLY possible if G is a Directed Acyclic Graph (DAG).

## I. Mathematical Foundation
- A directed graph has a topological ordering if and only if it is acyclic.
- Every DAG has at least one topological ordering.
- If the graph has a cycle (e.g., A -> B -> A), no topological ordering is possible.

## J. From-Scratch Implementation
(See code below for Kahn's Algorithm (BFS) and DFS-based implementations)

## K. Library / Production Implementation
Python's `graphlib.TopologicalSorter` (introduced in Python 3.9) is the standard library for topological sorting.

## L. Trace (walk through example)
Graph: 0->1, 0->2, 1->3, 2->3
Kahn's Algorithm:
1. Calculate in-degrees: [0=0, 1=1, 2=1, 3=2]
2. Queue nodes with 0 in-degree: [0]
3. Pop 0. Add to result. Order=[0]. Neighbors of 0 are 1, 2. Decrement their in-degrees. In-degrees: [0=0, 1=0, 2=0, 3=2]. Queue: [1, 2].
4. Pop 1. Add to result. Order=[0, 1]. Neighbors of 1 is 3. Decrement in-degree. In-degrees: [3=1]. Queue: [2].
5. Pop 2. Add to result. Order=[0, 1, 2]. Neighbors of 2 is 3. Decrement in-degree. In-degrees: [3=0]. Queue: [3].
6. Pop 3. Add to result. Order=[0, 1, 2, 3]. Queue: []. Done.

## M. Complexity
Time Complexity: O(V + E) where V is vertices and E is edges (both Kahn's and DFS visit each node and edge exactly once).
Space Complexity: O(V) to store in-degrees, queue (Kahn's) or visited sets, stack (DFS).

## N. Common Mistakes
- Trying to topologically sort a graph with cycles.
- Trying to topologically sort an undirected graph.
- Forgetting to check if the final sorted list length equals the number of vertices (to detect cycles in Kahn's algorithm).

## O. Common Confusions
- "Is Topological Sort unique?" No, unless there's a Hamiltonian path (a directed path that visits all vertices). Most DAGs have multiple valid topological orders.
- "BFS vs DFS for Topo Sort?" Kahn's uses BFS (in-degrees), while the other uses DFS (post-order traversal, then reversed). Both are O(V + E).

## P. When To Use
- Resolving dependencies (makefiles, package managers like npm/pip).
- Course scheduling with prerequisites.
- Task scheduling in pipelines or distributed systems.

## Q. When NOT To Use
- When the graph has undirected edges.
- When the graph has cycles (circular dependencies).
- When you just need to find the shortest path.

## R. Trade-offs
- Kahn's Algorithm is iteratively straightforward and naturally detects cycles (if processed count != V).
- DFS-based is naturally elegant for recursive implementations but requires an extra `rec_stack` set to explicitly detect cycles.

## S. Debugging
- Print the in-degree of all vertices; ensure at least one vertex has an in-degree of 0 to start.
- Check cycle detection logic. If the graph is stuck or raises an error, trace the cycles.

## T. Memory Hook
"Start with nothing pointing at you." (For Kahn's algorithm - start with in-degree 0).
"DFS and flip." (For DFS - do a normal DFS and reverse the resulting stack).

## U. Active Recall
1. What happens if you run Kahn's algorithm on a graph with a cycle?
2. Why do we reverse the stack in DFS topological sort?
3. Can an undirected tree be topologically sorted?

## V. Practice
- Course Schedule II (LeetCode 210)
- Alien Dictionary (LeetCode 269)
- Build a Package Manager

## W. Interview Question
"Alien Dictionary: Given a sorted dictionary of an alien language, find the order of characters using Topological Sort."
"Determine if a cycle exists in a set of dependent tasks."

## X. Project Connection
In an AI or MLOps project, DAGs and topological sorting are extensively used in workflow orchestrators like Apache Airflow or Kubeflow to schedule and run dependent tasks (e.g., Data Extraction -> Data Cleaning -> Model Training -> Evaluation).
"""

from typing import Dict, List, Set, Any
from collections import deque

class TopologicalSort:
    def __init__(self, vertices: int):
        self.vertices = vertices
        self.graph: Dict[int, List[int]] = {i: [] for i in range(vertices)}
        
    def add_edge(self, u: int, v: int) -> None:
        self.graph[u].append(v)

    # --- BASIC / INTERMEDIATE: Kahn's Algorithm (BFS) ---
    def kahn_topological_sort(self) -> List[int]:
        """Uses in-degree array and queue. Good for cycle detection."""
        in_degree = [0] * self.vertices
        for u in self.graph:
            for v in self.graph[u]:
                in_degree[v] += 1
                
        queue = deque([i for i in range(self.vertices) if in_degree[i] == 0])
        topo_order = []
        
        while queue:
            u = queue.popleft()
            topo_order.append(u)
            
            for v in self.graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        # If count of sorted elements != vertices, there is a cycle
        if len(topo_order) != self.vertices:
            raise ValueError("Graph contains a cycle! Topological sort not possible.")
            
        return topo_order

    # --- ADVANCED: DFS Based Topological Sort ---
    def dfs_topological_sort(self) -> List[int]:
        visited = set()
        stack = []
        rec_stack = set() # For cycle detection
        
        def dfs(node: int) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if not dfs(neighbor):
                        return False
                elif neighbor in rec_stack:
                    return False # Cycle detected
                    
            rec_stack.remove(node)
            stack.append(node) # Push after visiting all descendants
            return True

        for i in range(self.vertices):
            if i not in visited:
                if not dfs(i):
                    raise ValueError("Graph contains a cycle! Topological sort not possible.")
                    
        return stack[::-1] # Reverse stack


def test_kahns():
    g = TopologicalSort(6)
    g.add_edge(5, 2)
    g.add_edge(5, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    
    order = g.kahn_topological_sort()
    assert len(order) == 6
    # 5 and 4 should come before 0, 2, etc. Valid order check:
    idx_map = {val: i for i, val in enumerate(order)}
    assert idx_map[5] < idx_map[2]
    assert idx_map[2] < idx_map[3]
    assert idx_map[3] < idx_map[1]
    print("Kahn's algorithm tests passed.")

def test_dfs_topo():
    g = TopologicalSort(6)
    g.add_edge(5, 2)
    g.add_edge(5, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    
    order = g.dfs_topological_sort()
    assert len(order) == 6
    idx_map = {val: i for i, val in enumerate(order)}
    assert idx_map[5] < idx_map[2]
    assert idx_map[2] < idx_map[3]
    assert idx_map[3] < idx_map[1]
    print("DFS topological sort tests passed.")

def test_cycle_detection():
    g = TopologicalSort(3)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    
    try:
        g.kahn_topological_sort()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
        
    try:
        g.dfs_topological_sort()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("Cycle detection tests passed.")

if __name__ == "__main__":
    print("Running Topological Sort tests...")
    test_kahns()
    test_dfs_topo()
    test_cycle_detection()
    print("All tests passed!")
