"""
## A. Concept Name
Advanced Searching Algorithms: A* (A-Star) Pathfinding and Heuristic Search

## B. One-Sentence Definition
A* is an informed search algorithm that uses a heuristic function to guide its graph traversal, efficiently finding the shortest path between a start and goal node.

## C. How It Works (Intuition)
Unlike uninformed algorithms (like BFS or Dijkstra's) that explore in all directions equally, A* uses a "heuristic" (a smart guess) to estimate the distance to the goal. It prioritizes paths that look promising, combining the known cost from the start with the estimated cost to the end.

## D. Visual/Mental Model
Imagine you are navigating a maze. BFS checks every single path step-by-step. Dijkstra checks the shortest known paths. A* is like having a compass that points toward the goal; you still follow the paths, but you always prefer the paths that lead in the general direction of your compass heading.

## E. Step-by-Step Execution
1. Create a priority queue (open list) and push the start node.
2. Maintain a set of visited nodes (closed list).
3. While the open list is not empty, pop the node with the lowest total cost `f(n) = g(n) + h(n)`.
4. If this node is the goal, reconstruct and return the path.
5. Otherwise, add the node to the closed list.
6. For each neighbor of the current node, if it is unwalkable or already in the closed list, ignore it.
7. Calculate the neighbor's `g`, `h`, and `f` scores.
8. Push the neighbor to the open list if it's new or better than a previous path to it.

## F. Time & Space Complexity
- Time Complexity: O(b^d), where b is the branching factor and d is the depth of the shortest path. With a good heuristic, it is much faster in practice.
- Space Complexity: O(b^d) as it stores generated nodes in memory (both open and closed lists).

## G. Python Implementation
See the `a_star_search` function and `Node` class defined below.

## H. Core Code Explanation
- `g(n)`: Exact cost from start to node n.
- `h(n)`: Estimated cost from n to goal (using Manhattan distance for 4-way grids).
- `f(n)`: Total estimated cost (`g + h`).
- `heapq`: Python's min-heap used as a priority queue to always process the node with the lowest `f` score first.

## I. Debugging / Common Pitfalls
- Inadmissible Heuristic: Overestimating the distance to the goal causes A* to act like a greedy best-first search, which may not find the shortest path.
- Equality and Hashing: Ensure your Node classes implement `__eq__` and `__lt__` properly if used in a heap.
- Stale Heap Elements: Pushing updated nodes to `heapq` without removing old ones can waste memory and time.

## J. Alternative Approaches
- Dijkstra's Algorithm: Guaranteed to find the shortest path but explores uniformly (equivalent to A* where h(n) = 0).
- Greedy Best-First Search: Fast but not guaranteed to find the shortest path (equivalent to A* where g(n) = 0).
- BFS: Only works on unweighted graphs.

## K. When to Use (Pros & Cons)
- Pros: Complete and optimal (if the heuristic is admissible). Much faster than Dijkstra's on average.
- Cons: High memory usage because it stores all generated nodes.

## L. Real-World Applications
- GPS Navigation Systems
- Video Game AI (NPC pathfinding)
- Robot path planning and obstacle avoidance

## M. System Design Context
In a large-scale system like Uber or Google Maps, A* might be too slow for continent-wide routing. Systems often pre-compute hierarchies (Contraction Hierarchies) or use advanced A* variants like ALT (A*, Landmarks, Triangle inequality) for macro-routing, while standard A* is used for micro-routing.

## N. Interview Tips & Tricks
- Always clarify if movement is 4-way (use Manhattan) or 8-way/any-angle (use Euclidean or Chebyshev).
- Be prepared to discuss admissibility: A heuristic is admissible if it never overestimates the true cost.

## O. Frequently Asked Questions
Q: Can A* handle negative weights?
A: No, just like Dijkstra's, A* cannot handle graphs with negative edge weights.

## P. Code Kata / Practice Exercises
1. Modify the heuristic to support 8-way diagonal movement.
2. Implement bidirectional A* search.
3. Use a different data structure to manage open nodes more efficiently.

## Q. Related Patterns
- Graph Traversal Patterns
- Priority Queue / Heap Pattern
- State Space Search

## R. Anti-Patterns
- Using an overly complex heuristic that takes more time to compute than it saves in search iterations.
- Not using a `closed_set`, which leads to infinite loops in cyclic graphs.

## S. History / Origin
A* was created in 1968 by Peter Hart, Nils Nilsson, and Bertram Raphael at the Stanford Research Institute (SRI) while working on the Shakey the Robot project.

## T. Memory Management / Internals
In Python, storing thousands of `Node` objects can create significant GC overhead. In production, use flat arrays and 1D indexing for grids to optimize memory and cache locality.

## U. Advanced Variants
- IDA* (Iterative Deepening A*): Uses much less memory (DFS-based).
- D* Lite: An incremental heuristic search used when the graph changes dynamically (e.g., discovering new obstacles).
- Jump Point Search (JPS): An optimization for A* on uniform cost grids.

## V. Standard Library Counterparts
Python's standard library doesn't include A*, but `heapq` is essential for implementing it. Libraries like `networkx` offer built-in `astar_path` functions.

## W. Language-Specific Quirks
Python's `heapq` does not support updating priorities. To implement priority updates, you either push duplicates and ignore stale entries upon popping (as done here), or maintain a separate dictionary mapping nodes to their current list entries and mark stale entries as 'removed'.

## X. Project Connection
Used heavily in map routing modules and autonomous agent simulations within larger AI applications.
"""

import heapq
import math
from typing import List, Tuple, Dict, Set, Optional

# =============================================================================
# 1. A* SEARCH IMPLEMENTATION
# =============================================================================

class Node:
    """A node class for A* Pathfinding."""
    def __init__(self, position: Tuple[int, int], parent: Optional['Node'] = None):
        self.position = position
        self.parent = parent
        
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def heuristic_manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star_search(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Professional Implementation of A* Search for a 2D grid.
    
    Args:
        maze: 2D list where 0 is walkable and 1 is a wall.
        start: Tuple of (row, col) starting position.
        end: Tuple of (row, col) ending position.
        
    Returns:
        List of tuples representing the path from start to end, or None if no path.
    """
    start_node = Node(start)
    end_node = Node(end)

    # Initialize open and closed lists
    open_list = []
    closed_set: Set[Tuple[int, int]] = set()

    # Add start node to heap
    heapq.heappush(open_list, start_node)

    # Allowed movements (4-way: Up, Down, Left, Right)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    rows = len(maze)
    cols = len(maze[0])

    while open_list:
        # Get current node with lowest f()
        current_node = heapq.heappop(open_list)
        closed_set.add(current_node.position)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        for direction in directions:
            node_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

            # Make sure within range
            if not (0 <= node_position[0] < rows and 0 <= node_position[1] < cols):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Check if already evaluated
            if node_position in closed_set:
                continue

            # Create new node
            new_node = Node(node_position, current_node)

            # Calculate costs
            new_node.g = current_node.g + 1
            new_node.h = heuristic_manhattan(new_node.position, end_node.position)
            new_node.f = new_node.g + new_node.h

            # Check if node is already in open list with a lower g value
            # Note: For strict correctness, we should check and update existing nodes in open_list,
            # but for simplicity/performance in python heaps, we often just push duplicates and 
            # let the closed_set handle skipping them later.
            heapq.heappush(open_list, new_node)

    return None # No path found

# =============================================================================
# INTERVIEW CHALLENGE
# =============================================================================
# Question: Why do we use Manhattan distance for 4-way movement, but Euclidean 
# distance for any-angle movement? What happens if the heuristic overestimates 
# the actual distance?
#
# Answer:
# 1. We use Manhattan because it perfectly models the exact cost of moving strictly 
#    N, S, E, W. Euclidean models a straight line which isn't possible on a 4-way grid.
# 2. If a heuristic overestimates the distance (is "inadmissible"), A* loses its 
#    guarantee of finding the absolute shortest path. It becomes greedy and may find 
#    a suboptimal path faster. If it underestimates (is "admissible"), it guarantees 
#    the shortest path.

if __name__ == "__main__":
    print("Running Advanced Search Tests...")
    
    # A* Test
    test_maze = [
        [0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0]
    ]
    
    start_pt = (0, 0)
    end_pt = (4, 4)
    
    expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
    
    path = a_star_search(test_maze, start_pt, end_pt)
    assert path == expected_path, f"Path found: {path}"
    
    print("A* Search tests passed successfully!")
