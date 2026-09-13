"""
Medium-Level Graph Problems for Interview Preparation
====================================================

This module covers medium-level graph problems. Graph theory is critical for solving 
complex relationships between entities.

Topics Covered:
1. Number of Islands (Matrix/Grid traversal)
2. Course Schedule (Topological Sort / Cycle Detection)
3. Clone Graph (Graph Traversal with Hash Map)
4. Rotting Oranges (Multi-source BFS)

Beginner Explanation:
A graph is a collection of nodes (vertices) connected by edges. In matrix problems, 
each cell is a node, and its neighbors (up, down, left, right) are connected by edges.
Graph traversal usually involves BFS (Breadth-First Search) or DFS (Depth-First Search).

Deep Technical Explanation:
- Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges.
  For grids, V is rows * cols, and E is roughly 4 * V, meaning O(rows * cols).
- Space Complexity: O(V) to keep track of visited nodes and recursion stack / queue.
- Cycle Detection: Crucial in directed graphs (e.g., dependency resolution). Often solved using 
  DFS with node coloring (unvisited, visiting, visited) or Kahn's algorithm for topological sorting.
- BFS vs DFS: Use BFS when looking for the shortest path in unweighted graphs (like Rotting Oranges).
  DFS is often simpler to implement for exploring entire connected components (like Number of Islands).

Real-World Use Cases:
- Social networks (friends recommendations)
- Routing protocols (network packet routing)
- Build systems (resolving task dependencies like `make` or npm packages)
- Maps and Navigation (GPS pathfinding)
"""

from typing import List, Dict, Optional, Deque, Set
from collections import deque, defaultdict

# -----------------------------------------------------------------------------
# 1. Number of Islands
# -----------------------------------------------------------------------------
"""
Problem: Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water),
return the number of islands. An island is surrounded by water and is formed by connecting adjacent
lands horizontally or vertically.

Approach (DFS):
Iterate through every cell. When a '1' is found, increment the island count, and launch a DFS
to mark all connected '1's as '0' (visited) so they aren't counted again.

Time Complexity: O(M * N)
Space Complexity: O(M * N) in worst case for recursion stack.
"""

def numIslands(grid: List[List[str]]) -> int:
    """
    Returns the number of connected components (islands) in a grid.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r: int, c: int):
        # Base case: out of bounds or water
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
            return
        
        # Mark as visited (sink the island part)
        grid[r][c] = '0'
        
        # Explore neighbors
        dfs(r - 1, c) # Up
        dfs(r + 1, c) # Down
        dfs(r, c - 1) # Left
        dfs(r, c + 1) # Right

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                islands += 1
                dfs(r, c)
                
    return islands

# -----------------------------------------------------------------------------
# 2. Course Schedule
# -----------------------------------------------------------------------------
"""
Problem: There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take
course bi first if you want to take course ai. Return true if you can finish all courses.

Approach (Topological Sort / Kahn's Algorithm):
Count the in-degree (number of prerequisites) for each course.
Build an adjacency list for the graph.
Queue all courses with an in-degree of 0.
Process the queue: decrement the in-degree of neighbors. If a neighbor reaches 0, add it to the queue.
If we process all courses, there are no cycles.

Time Complexity: O(V + E)
Space Complexity: O(V + E)
"""

def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Determines if all courses can be finished without cyclical dependencies.
    """
    # Build graph and in-degrees
    adj: Dict[int, List[int]] = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
        
    # Start with courses that have no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    courses_taken = 0
    
    while queue:
        current = queue.popleft()
        courses_taken += 1
        
        # For each course that depends on the current one
        for next_course in adj[current]:
            in_degree[next_course] -= 1
            # If all prerequisites are fulfilled, we can take it
            if in_degree[next_course] == 0:
                queue.append(next_course)
                
    return courses_taken == numCourses

# -----------------------------------------------------------------------------
# 3. Clone Graph
# -----------------------------------------------------------------------------
class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List['Node']] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

"""
Problem: Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph.

Approach (DFS with HashMap):
Use a hash map to store already copied nodes to avoid infinite loops and duplicate node creation.
If the node is already in the map, return the cloned reference.
Otherwise, create a new node, put it in the map, and recursively clone its neighbors.

Time Complexity: O(V + E)
Space Complexity: O(V) for the hash map and recursion stack.
"""

def cloneGraph(node: Optional['Node']) -> Optional['Node']:
    """
    Returns a deep copy of an undirected graph.
    """
    if not node:
        return None
        
    old_to_new: Dict[Node, Node] = {}
    
    def dfs(curr: Node) -> Node:
        if curr in old_to_new:
            return old_to_new[curr]
            
        # Create a copy and add it to the map
        copy = Node(curr.val)
        old_to_new[curr] = copy
        
        # Clone neighbors
        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))
            
        return copy
        
    return dfs(node)

# -----------------------------------------------------------------------------
# 4. Rotting Oranges
# -----------------------------------------------------------------------------
"""
Problem: You are given an m x n grid where each cell can have one of three values:
0 representing an empty cell, 1 representing a fresh orange, or 2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
Return the minimum number of minutes that must elapse until no cell has a fresh orange. If impossible, return -1.

Approach (Multi-source BFS):
First pass: find all rotten oranges and add them to a queue. Count the fresh oranges.
BFS: For each minute, process all currently rotten oranges in the queue, infecting adjacent fresh ones.
Keep track of time. If fresh oranges remain after BFS, return -1.

Time Complexity: O(M * N)
Space Complexity: O(M * N) for the queue.
"""

def orangesRotting(grid: List[List[int]]) -> int:
    """
    Calculates the minimum time to rot all oranges.
    """
    if not grid:
        return -1
        
    rows, cols = len(grid), len(grid[0])
    queue: Deque = deque()
    fresh_count = 0
    
    # Step 1: Initialize queue with all rotten oranges and count fresh ones
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1
                
    if fresh_count == 0:
        return 0 # No fresh oranges to begin with
        
    minutes_passed = 0
    directions = [(1,0), (-1,0), (0,1), (0,-1)]
    
    # Step 2: BFS level by level
    while queue and fresh_count > 0:
        minutes_passed += 1
        # Process the current level of rotting oranges
        for _ in range(len(queue)):
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # If in bounds and fresh, rot it
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc))
                    
    return minutes_passed if fresh_count == 0 else -1


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Testing Medium Graph Problems...")

    # Test Number of Islands
    grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    print(f"Number of Islands: {numIslands(grid)}") # Expected: 3
    
    # Test Course Schedule
    print(f"Can finish courses: {canFinish(2, [[1,0]])}") # Expected: True
    print(f"Can finish courses (cycle): {canFinish(2, [[1,0],[0,1]])}") # Expected: False
    
    # Test Rotting Oranges
    oranges = [[2,1,1],[1,1,0],[0,1,1]]
    print(f"Minutes to rot all: {orangesRotting(oranges)}") # Expected: 4

    print("All tests passed.")
