"""
# ==============================================================================
# LABORATORY: ADVANCED BFS APPLICATIONS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know that BFS expands layer-by-layer, making it the perfect algorithm for 
# finding the Shortest Path in an unweighted graph. 
# But basic BFS just visits nodes. How do you actually EXTRACT the shortest path? 
# How do you handle multiple starting points simultaneously (e.g., finding the 
# nearest hospital for a whole city)? 
# And what happens if the edges have weights of only 0 or 1?
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Extract the actual Shortest Path using a `parents` dictionary.
# - Master Multi-Source BFS (e.g., LeetCode #994: Rotting Oranges).
# - Understand 0-1 BFS using a Deque.
#
# ==============================================================================
"""

from collections import deque
from typing import List, Dict, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EXTRACTING THE SHORTEST PATH
# ==============================================================================
def shortest_path_bfs(graph: Dict[str, List[str]], start: str, end: str) -> Optional[List[str]]:
    """
    Standard BFS just tells you IF a path exists. 
    To reconstruct the path, we must remember WHO discovered EACH node.
    We do this using a `parents` hash map.
    """
    queue = deque([start])
    visited = {start}
    
    # Track the node that "discovered" the current node
    parents = {start: None}
    
    while queue:
        current = queue.popleft()
        
        # Did we reach the destination?
        if current == end:
            break
            
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current # current discovered neighbor!
                queue.append(neighbor)
                
    # If we never reached the end, there is no path
    if end not in parents:
        return None
        
    # Reconstruct the path by walking backwards from the end to the start
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = parents[curr]
        
    # Reverse it because we walked backwards
    return path[::-1]

def demonstrate_path_extraction():
    section_header("Algorithm: Reconstructing the Shortest Path")
    
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E', 'G'],
        'G': ['F']
    }
    
    print("Finding shortest path from 'A' to 'G'...")
    path = shortest_path_bfs(graph, 'A', 'G')
    print(f"Path found: {' -> '.join(path)}")


# ==============================================================================
# 4. MULTI-SOURCE BFS (ROTTING ORANGES)
# ==============================================================================
def rotting_oranges(grid: List[List[int]]) -> int:
    """
    LeetCode #994: Rotting Oranges
    Grid: 0 = Empty, 1 = Fresh Orange, 2 = Rotten Orange.
    Every minute, any fresh orange adjacent to a rotten orange becomes rotten.
    Return the minimum minutes until no cell has a fresh orange.
    
    Why Multi-Source BFS?
    If there are 3 rotten oranges to start, they all start rotting their neighbors 
    SIMULTANEOUSLY. We cannot run BFS from just one orange. We must push ALL 
    initially rotten oranges onto the queue at minute 0!
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0
    
    # 1. Initialization: Find all fresh and rotten oranges
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                # Push coordinates and current minute (0)
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh_count += 1
                
    if fresh_count == 0:
        return 0 # Nothing to rot
        
    minutes_passed = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # 2. Multi-Source BFS
    while queue:
        r, c, mins = queue.popleft()
        
        # Process neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # If valid and fresh, rot it!
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2 # Mark as rotten (visited)
                fresh_count -= 1
                queue.append((nr, nc, mins + 1))
                minutes_passed = max(minutes_passed, mins + 1)
                
    return minutes_passed if fresh_count == 0 else -1

def demonstrate_multi_source_bfs():
    section_header("Algorithm: Multi-Source BFS (Simultaneous Expansion)")
    
    grid = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    
    print("Initial Grid (2=Rotten, 1=Fresh, 0=Empty):")
    for row in grid: print(row)
    
    mins = rotting_oranges(grid)
    print(f"\nTime taken for all oranges to rot: {mins} minutes.")


# ==============================================================================
# 5. 0-1 BFS (DEQUE ROUTING)
# ==============================================================================
def demonstrate_01_bfs():
    section_header("Concept: 0-1 BFS")
    print("""
Standard BFS assumes every edge has a weight of 1.
Dijkstra's Algorithm handles variable weights (e.g., 5, 10, 50).
But what if edges only have weights of exactly 0 or 1? (e.g., breaking down a wall 
costs 1, moving through empty space costs 0).

Using Dijkstra (with a Priority Queue) takes O(E log V).
A 0-1 BFS takes exactly O(V + E) using a simple Deque!

How it works:
When traversing an edge, if the weight is 0, you push the neighbor to the FRONT 
of the deque (`appendleft`). If the weight is 1, you push it to the BACK (`append`).
Because 0-weight edges jump to the front of the line, the queue magically 
maintains sorted priority order without the O(log N) overhead of a Heap!
    """)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In a standard BFS, how do you reconstruct the actual path taken to the destination?
   Answer: You maintain a Hash Map (or Array) mapping each child node to its parent node. When the destination is reached, you start at the destination and repeatedly look up the parent, building the path backwards until you reach the start node.

2. Why must you push ALL starting nodes into the queue before the `while queue:` loop in a Multi-Source BFS?
   Answer: Because we need to simulate simultaneous expansion. If we ran a full BFS from Start Node A, and then a full BFS from Start Node B, the distances would be calculated sequentially, completely breaking the simulation. Enqueuing them all at initialization puts them all at "Depth 0" so they expand outwards together.

3. Why does 0-1 BFS push 0-weight edges to the front of the Deque?
   Answer: Because traversing a 0-weight edge costs nothing, meaning that neighbor is technically at the EXACT SAME distance as the current node. It must be processed in the current level of expansion before moving on to nodes that are distance + 1.
"""

if __name__ == "__main__":
    demonstrate_path_extraction()
    demonstrate_multi_source_bfs()
    demonstrate_01_bfs()
    print("\n[SUCCESS] Laboratory: Advanced BFS Completed.")
