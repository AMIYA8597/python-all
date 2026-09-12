"""
Bidirectional Search Algorithm (Graph Traversal)

===============================================================================
1. INTRODUCTION & LEARNING OBJECTIVES
===============================================================================
What is Bidirectional Search?
Bidirectional search is a graph search algorithm that finds the shortest path 
from an initial vertex to a goal vertex in a directed or undirected graph. 
It runs two simultaneous searches: one forward from the initial state and 
the other backward from the goal, stopping when the two meet.

Learning Objectives:
- Understand the rationale and performance benefits of bidirectional search.
- Implement bidirectional search on unweighted graphs to find the shortest path.
- Analyze the time and space complexity and contrast it with standard BFS.
- Learn to reconstruct the path correctly once the two searches meet.

===============================================================================
2. CONCEPT EXPLANATION & INDUSTRY USE CASES
===============================================================================
Standard Breadth-First Search (BFS) expands nodes layer by layer from the start.
If the branching factor is `b` and distance from start to goal is `d`, standard 
BFS explores O(b^d) nodes. 

Bidirectional search effectively halves the exponent. Both the forward and 
backward searches expand up to distance `d/2`. The total nodes explored 
become O(b^(d/2) + b^(d/2)), which is significantly smaller than O(b^d).

Industry Use Cases:
1. Routing Applications: Finding the shortest route between two cities on a map.
2. Social Networks: Finding the shortest connection (degrees of separation) 
   between two users (e.g., LinkedIn connections).
3. Puzzle Solving: AI algorithms for solving Rubik's cube or 15-puzzle.

===============================================================================
3. IMPLEMENTATION & ADVANCED CONCEPTS
===============================================================================
Below is a robust, type-hinted implementation of Bidirectional Search using
adjacency lists.
"""

from collections import deque
from typing import Dict, List, Optional, Set, Tuple, Any

class Graph:
    """
    Represents an undirected graph using an adjacency list.
    """
    def __init__(self) -> None:
        self.adj_list: Dict[str, List[str]] = {}

    def add_edge(self, u: str, v: str) -> None:
        """Adds an undirected edge between u and v."""
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)  # Undirected

    def get_neighbors(self, vertex: str) -> List[str]:
        return self.adj_list.get(vertex, [])


def bidirectional_search(graph: Graph, start: str, goal: str) -> Optional[List[str]]:
    """
    Finds the shortest path between start and goal using bidirectional search.

    Args:
        graph: The undirected graph.
        start: The starting vertex.
        goal: The target vertex.

    Returns:
        A list of vertices representing the shortest path, or None if no path exists.
    """
    if start not in graph.adj_list or goal not in graph.adj_list:
        return None

    if start == goal:
        return [start]

    # Queues for BFS
    queue_fwd = deque([start])
    queue_bwd = deque([goal])

    # Visited dictionaries storing the parent of each node to reconstruct the path
    # visited[node] = parent_node
    visited_fwd: Dict[str, Optional[str]] = {start: None}
    visited_bwd: Dict[str, Optional[str]] = {goal: None}

    def expand_level(queue: deque, visited_this: Dict[str, Optional[str]], 
                     visited_other: Dict[str, Optional[str]]) -> Optional[str]:
        """
        Expands one level (all nodes currently in the queue) of the BFS.
        Returns the intersecting node if found, else None.
        """
        # Explore only nodes in the current layer
        level_size = len(queue)
        for _ in range(level_size):
            curr = queue.popleft()

            for neighbor in graph.get_neighbors(curr):
                if neighbor not in visited_this:
                    visited_this[neighbor] = curr
                    queue.append(neighbor)
                    
                    # Check for intersection
                    if neighbor in visited_other:
                        return neighbor
        return None

    while queue_fwd and queue_bwd:
        # Expand forward search
        intersect_node = expand_level(queue_fwd, visited_fwd, visited_bwd)
        if intersect_node:
            return construct_path(visited_fwd, visited_bwd, intersect_node)

        # Expand backward search
        intersect_node = expand_level(queue_bwd, visited_bwd, visited_fwd)
        if intersect_node:
            return construct_path(visited_fwd, visited_bwd, intersect_node)

    return None


def construct_path(visited_fwd: Dict[str, Optional[str]], 
                   visited_bwd: Dict[str, Optional[str]], 
                   intersect_node: str) -> List[str]:
    """
    Reconstructs the full path from start to goal given the intersection node
    and the parent pointers from both searches.
    """
    # Reconstruct path from start to intersect_node
    path = []
    curr: Optional[str] = intersect_node
    while curr is not None:
        path.append(curr)
        curr = visited_fwd[curr]
    path.reverse()  # path is now [start, ..., intersect_node]

    # Reconstruct path from intersect_node to goal
    curr = visited_bwd[intersect_node]
    while curr is not None:
        path.append(curr)
        curr = visited_bwd[curr]
        
    return path

===============================================================================
4. COMPLEXITY ANALYSIS
===============================================================================
- Time Complexity: O(b^(d/2)), where `b` is the branching factor and `d` is the 
  distance from start to goal. Both BFS queues expand out to at most `d/2` levels.
- Space Complexity: O(b^(d/2)) to store the queues and visited sets (parent pointers).

Comparison with standard BFS:
Standard BFS time & space complexity: O(b^d).
Bidirectional search provides a dramatic improvement when b and d are large.

===============================================================================
5. COMMON MISTAKES & INTERVIEW QUESTIONS
===============================================================================
Mistake: Alternating node-by-node instead of level-by-level. 
To guarantee the shortest path, we must expand level-by-level. Otherwise, 
the first intersection might not lie on the absolute shortest path.

Interview Challenge: 
"Given a dictionary of words, find the shortest transformation sequence from a 
start word to an end word, changing only one letter at a time (Word Ladder). 
Optimize this using Bidirectional BFS."
(This is a classic problem where bidirectional search excels over standard BFS).

===============================================================================
6. TESTS & ASSERTIONS
===============================================================================
if __name__ == "__main__":
    g = Graph()
    
    # Simple linear graph: A-B-C-D-E
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]
    for u, v in edges:
        g.add_edge(u, v)
        
    path1 = bidirectional_search(g, 'A', 'E')
    print(f"Path A -> E: {path1}")
    assert path1 == ['A', 'B', 'C', 'D', 'E']

    # More complex graph
    g2 = Graph()
    edges2 = [
        ('S', 'A'), ('S', 'B'),
        ('A', 'C'), ('B', 'C'),
        ('B', 'D'), ('C', 'E'),
        ('D', 'F'), ('E', 'F'),
        ('F', 'G')
    ]
    for u, v in edges2:
        g2.add_edge(u, v)

    path2 = bidirectional_search(g2, 'S', 'G')
    print(f"Path S -> G: {path2}")
    
    # Path length should be 5 (e.g., S -> B -> D -> F -> G or S -> B -> C -> E -> F -> G)
    # Actually S-B-D-F-G is 5 nodes (distance 4)
    assert len(path2) == 5
    print("All bidirectional search tests passed!")
