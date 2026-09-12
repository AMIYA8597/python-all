"""
## A. Concept Name
Eulerian Path and Circuit

## B. Problem Statement
Find a path in a graph that visits every edge exactly once (Eulerian Path) or a path that visits every edge exactly once and ends where it started (Eulerian Circuit).

## C. Real-World Applications
DNA sequencing (De Bruijn graphs), garbage collection routes, mail delivery (Chinese Postman Problem), circuit board printing, and continuous path drawing.

## D. Core Mechanism
Hierholzer's Algorithm uses a post-order DFS stack to traverse edges. As long as the degree conditions are met, any valid traversal where we visit edges and backtrack using a stack will form an Eulerian path/circuit when reversed.

## E. Time & Space Complexity
Time Complexity: O(V + E) using Hierholzer's algorithm (stack-based post-order DFS).
Space Complexity: O(V + E) for the adjacency list and path storage.

## F. Step-by-Step Explanation
1. Verify the graph meets the degree conditions for an Eulerian path or circuit.
2. If an Eulerian path exists, start at a vertex with out-degree - in-degree = 1 (or any vertex if it's a circuit).
3. Follow unvisited edges to adjacent vertices, pushing current vertices to a stack.
4. When a vertex has no unvisited edges, pop it from the stack and add it to the path.
5. Reverse the path at the end.

## G. Implementation Variations
Fleury's Algorithm (avoids crossing bridges unless necessary, O(E^2) time complexity) vs. Hierholzer's Algorithm (O(V + E)). Undirected vs. Directed graph implementations.

## H. Common Pitfalls & Anti-Patterns
Not checking if the graph is connected (a graph with degree conditions met but multiple disconnected components is not Eulerian). Modifying the original graph during traversal instead of using a cloned/temporary graph.

## I. Interview & System Design Questions
Q: What's the difference between Eulerian paths and Hamiltonian paths?
A: Eulerian paths visit every EDGE exactly once (O(V+E) to find). Hamiltonian paths visit every VERTEX exactly once (NP-Hard to find).

## J. Alternative Approaches
Fleury's Algorithm.

## K. Memory & Performance Implications
Hierholzer's Algorithm requires O(V + E) memory for the adjacency list and path array. Safe for large sparse graphs but recursion limit might be exceeded if using recursive DFS; iterative stack-based DFS is preferred.

## L. Edge Cases & Constraints
Graph with isolated vertices (0 edges). Graph consisting of disjoint cycles (Eulerian circuit condition passes on degrees, but graph must be connected).

## M. Distributed/Scalable System Considerations
For extremely large graphs, decomposing the graph into smaller Eulerian subgraphs or using distributed graph processing frameworks like Pregel.

## N. Monitoring & Telemetry
Monitor stack size and memory usage in deep graph traversals.

## O. Clean Code & Design Principles
Separate graph construction, degree verification, and path finding logic. Use deque for efficient edge removal.

## P. Testing Strategies
Test with simple circuits, simple paths, disconnected graphs, single vertices, and graphs lacking Eulerian properties.

## Q. Debugging Tactics
Print vertex degrees and the stack state at each iteration. Verify degree constraints before traversal.

## R. Code Review Checklist
Check that in-degree and out-degree are calculated correctly. Ensure the start node is selected appropriately. Confirm that the path is reversed before returning.

## S. Algorithmic Trade-offs
Hierholzer's is O(V + E) and generally preferred over Fleury's O(E^2), but Fleury's logic can be more intuitive for human problem-solving.

## T. Security & Failure Modes
Out-of-memory errors on massive graphs. Infinite loops if edges are not properly removed from the temp graph.

## U. Asynchronous/Concurrency Patterns
Finding Eulerian paths is inherently sequential, but verifying degrees can be parallelized.

## V. Future Extensions
Extending to solve the Chinese Postman Problem (finding the shortest postman tour in a non-Eulerian graph).

## W. Maintenance & Refactoring
Keep the pathfinding logic decoupled from the underlying graph representation.

## X. Project Connection
Used in genomics pipelines for DNA fragment assembly via De Bruijn graphs.
"""

from typing import List, Dict
from collections import defaultdict

class EulerianGraph:
    def __init__(self, is_directed: bool = False):
        self.graph = defaultdict(list)
        self.is_directed = is_directed
        self.in_degree = defaultdict(int)
        self.out_degree = defaultdict(int)
        
    def add_edge(self, u: int, v: int):
        self.graph[u].append(v)
        self.out_degree[u] += 1
        self.in_degree[v] += 1
        if not self.is_directed:
            self.graph[v].append(u)
            self.out_degree[v] += 1
            self.in_degree[u] += 1
            
    def has_eulerian_path_directed(self) -> bool:
        start_nodes = 0
        end_nodes = 0
        for node in set(self.in_degree.keys()).union(set(self.out_degree.keys())):
            out_d = self.out_degree[node]
            in_d = self.in_degree[node]
            if out_d - in_d > 1 or in_d - out_d > 1:
                return False
            if out_d - in_d == 1:
                start_nodes += 1
            elif in_d - out_d == 1:
                end_nodes += 1
        return (start_nodes == 0 and end_nodes == 0) or (start_nodes == 1 and end_nodes == 1)

    # Hierholzer's Algorithm
    def find_eulerian_path_directed(self) -> List[int]:
        if not self.has_eulerian_path_directed():
            return []
            
        # Find start node
        start_node = list(self.graph.keys())[0] if self.graph else 0
        for node in set(self.in_degree.keys()).union(set(self.out_degree.keys())):
            if self.out_degree[node] - self.in_degree[node] == 1:
                start_node = node
                break
                
        stack = [start_node]
        path = []
        
        # Clone graph to safely remove edges
        from collections import deque
        temp_graph = {u: deque(v) for u, v in self.graph.items()}
        
        while stack:
            u = stack[-1]
            if temp_graph.get(u) and len(temp_graph[u]) > 0:
                v = temp_graph[u].popleft()
                stack.append(v)
            else:
                path.append(stack.pop())
                
        return path[::-1]

# Edge Cases:
# 1. Graph with isolated vertices (0 edges).
# 2. Graph consisting of disjoint cycles (Eulerian circuit condition passes on degrees, but graph must be connected).

# Interview Challenge:
# Q: "What's the difference between Eulerian paths and Hamiltonian paths?"
# A: "Eulerian paths visit every EDGE exactly once (O(E) to find). Hamiltonian paths visit every VERTEX exactly once (NP-Hard to find)."

def test_eulerian():
    g = EulerianGraph(is_directed=True)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    g.add_edge(1, 4)
    
    assert g.has_eulerian_path_directed() == True
    path = g.find_eulerian_path_directed()
    # Path should cover all 4 edges, so 5 nodes long.
    assert len(path) == 5
    
    print("All tests passed for Eulerian Paths.")

if __name__ == "__main__":
    test_eulerian()
