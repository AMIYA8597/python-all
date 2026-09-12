"""
## A. Concept Name
Depth-First Search (DFS)

## B. Real-World Analogy
Navigating a maze by keeping your hand on the right wall and following the path as deep as it goes until you hit a dead end, then backtracking to the last intersection.

## C. Core Mechanism
Traverses a graph or tree by visiting a node and then recursively visiting its unvisited neighbors before exploring other paths.

## D. Time & Space Complexity
- Time Complexity: O(V + E) where V is vertices and E is edges.
- Space Complexity: O(V) for the visited set and recursion stack (in worst case).

## E. Code Implementation
(See below)

## F. Use Cases
- Topological sorting
- Finding connected components
- Solving puzzles like mazes

## G. Data Structures Used
Recursion (Call Stack) or explicit Stack, and a Set for tracking visited nodes.

## H. Edge Cases
- Disconnected graphs
- Cyclic graphs
- Empty graphs

## I. Common Pitfalls
- Forgetting to mark a node as visited (leads to infinite loops in cyclic graphs).
- Exceeding recursion depth limit for very large graphs.

## J. Debugging Tips
Trace the recursion tree and print nodes as they are added to the visited set.

## K. Interview Relevance
Highly relevant for graph traversal questions, pathfinding, and backtracking.

## L. Advanced Concepts
Iterative deepening DFS (IDDFS).

## M. Alternative Approaches
Breadth-First Search (BFS).

## N. When NOT to use
When finding the shortest path in unweighted graphs (use BFS instead).

## O. Historical Context
First formulated in the 19th century by Charles Pierre Trémaux as a strategy for solving mazes.

## P. Python specifics
In Python, default recursion limit is 1000, which might need to be increased using `sys.setrecursionlimit()` for large graphs.

## Q. Performance Optimization
Use an iterative approach with a stack for extremely deep graphs to avoid recursion limit errors.

## R. Testing
Test with acyclic, cyclic, sparse, dense, and disconnected graphs.

## S. Code Structure
Generally defined as a standalone function or method within a Graph class.

## T. Design Patterns
Often combined with the Visitor pattern.

## U. Related Algorithms
BFS, Dijkstra's algorithm, A* search.

## V. System Design
Useful in web crawlers and dependency resolution.

## W. Scalability
Can be parallelized but is inherently sequential in exploring deep paths.

## X. Project Connection
DFS is foundational in AI for state-space searching, game playing algorithms, and navigating decision trees.
"""

def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    
    if node not in visited:
        visited.add(node)
        for neighbor in graph.get(node, []):
            dfs_recursive(graph, neighbor, visited)
    
    return visited

def dfs_iterative(graph, start_node):
    visited = set()
    stack = [start_node]
    
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # Add neighbors to stack
            # To match recursive behavior, push reversed neighbors
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return visited

if __name__ == "__main__":
    sample_graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    
    print("Recursive DFS:", dfs_recursive(sample_graph, 'A'))
    print("Iterative DFS:", dfs_iterative(sample_graph, 'A'))
