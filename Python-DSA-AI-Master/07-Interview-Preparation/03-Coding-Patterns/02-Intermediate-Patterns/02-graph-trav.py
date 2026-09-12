"""
Graph Traversal Patterns

Learning Objectives:
1. Understand Graph representation (Adjacency List, Adjacency Matrix).
2. Master DFS (Depth-First Search) for Graphs.
3. Master BFS (Breadth-First Search) for Graphs.
4. Learn cycle detection and topological sorting.
5. Analyze time and space complexity of graph algorithms.

Concept Explanation:
Graphs can be traversed using BFS or DFS. Unlike trees, graphs may contain cycles, so keeping track of visited nodes is crucial to avoid infinite loops.
- DFS goes deep into a branch before backtracking. It's often implemented recursively or with a stack.
- BFS explores nodes layer by layer. It's implemented with a queue and is useful for finding the shortest path in unweighted graphs.
"""

from typing import List, Dict, Set
import collections

# Basic Implementation: DFS Traversal
def graph_dfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Time: O(V + E), Space: O(V)"""
    visited = set()
    res = []
    
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        res.append(node)
        for neighbor in graph.get(node, []):
            dfs(neighbor)
            
    dfs(start)
    return res

# Intermediate Implementation: BFS Traversal
def graph_bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Time: O(V + E), Space: O(V)"""
    visited = set([start])
    queue = collections.deque([start])
    res = []
    
    while queue:
        node = queue.popleft()
        res.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return res

# Advanced Implementation: Topological Sort (Kahn's Algorithm)
def topological_sort(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """Time: O(V + E), Space: O(V + E)"""
    adj = collections.defaultdict(list)
    indegree = [0] * num_courses
    
    for dest, src in prerequisites:
        adj[src].append(dest)
        indegree[dest] += 1
        
    queue = collections.deque([i for i in range(num_courses) if indegree[i] == 0])
    res = []
    
    while queue:
        node = queue.popleft()
        res.append(node)
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
                
    return res if len(res) == num_courses else []

# Edge Cases to Handle:
# 1. Disconnected graphs (need to iterate over all vertices).
# 2. Graphs with cycles (ensure visited sets are used).
# 3. Empty graph.

# Interview Challenge: Number of Islands (Implicit Graph DFS/BFS)
def num_islands(grid: List[List[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    islands = 0
    
    def bfs(r, c):
        q = collections.deque([(r, c)])
        visited.add((r, c))
        while q:
            row, col = q.popleft()
            directions = [[1,0],[-1,0],[0,1],[0,-1]]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if (0 <= nr < rows and 0 <= nc < cols and 
                    grid[nr][nc] == '1' and (nr, nc) not in visited):
                    q.append((nr, nc))
                    visited.add((nr, nc))
                    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                bfs(r, c)
                islands += 1
    return islands

def run_tests():
    graph = {
        0: [1, 2],
        1: [2],
        2: [0, 3],
        3: [3]
    }
    
    assert graph_dfs(graph, 2) == [2, 0, 1, 3]
    assert graph_bfs(graph, 2) == [2, 0, 3, 1]
    
    assert topological_sort(4, [[1,0],[2,0],[3,1],[3,2]]) in ([0,1,2,3], [0,2,1,3])
    assert topological_sort(2, [[1,0],[0,1]]) == [] # Cycle
    
    grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    assert num_islands(grid) == 3
    
    print("All Graph Traversal tests passed!")

if __name__ == "__main__":
    run_tests()
