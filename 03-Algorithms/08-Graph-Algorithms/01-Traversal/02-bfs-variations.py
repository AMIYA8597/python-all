"""
# ==============================================================================
# LABORATORY: GRAPH ALGORITHMS (BFS VARIATIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Depth-First Search (DFS) uses a Stack (LIFO) to plunge as 
# deep as possible into a graph. 
# 
# Breadth-First Search (BFS) is the exact opposite. It uses a Queue (FIFO).
# It starts at the root and sweeps outwards in perfect concentric circles. 
# It checks everything 1 mile away, then everything 2 miles away, then 3 miles.
#
# Because it naturally expands in perfect geometric ripples, BFS has a massive 
# superpower that DFS does not:
# It guarantees that the FIRST time you hit a node, you have mathematically 
# found the absolute SHORTEST PATH to that node (in an unweighted graph).
#
# How does LinkedIn know you are a "3rd degree connection" with someone?
# It runs a BFS! 
# But a standard BFS takes too long for 1 billion users. To optimize it, they 
# use "Bi-directional BFS". They start a BFS from YOU, and a simultaneous BFS 
# from the TARGET, and let the ripples crash into each other in the middle. 
# This slices the Time Complexity exponentially!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the FIFO Queue structure (`collections.deque`).
# - Implement Shortest Path tracking using a `parent` map.
# - Understand how Bi-Directional BFS shatters the O(b^d) branching limit.
#
# ==============================================================================
"""

from collections import deque
from typing import Dict, List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. STANDARD BREADTH-FIRST SEARCH (O(V + E))
# ==============================================================================
def bfs_shortest_path(graph: Dict[int, List[int]], start_node: int, target_node: int) -> Optional[List[int]]:
    """
    Finds the exact shortest path between two nodes using BFS.
    Time Complexity: O(V + E)
    Space Complexity: O(V) for the Queue, Visited Set, and Parent Map.
    """
    
    # 1. THE QUEUE
    # DO NOT USE a standard Python list `[]` for a Queue!
    # `list.pop(0)` requires shifting every single element in memory, making it O(N).
    # `collections.deque` uses a Doubly-Linked List, making `.popleft()` strictly O(1)!
    queue = deque([start_node])
    
    visited = set()
    visited.add(start_node)
    
    # The `parent` map tracks exactly HOW we discovered a node.
    # If Node 5 discovered Node 6, parent[6] = 5.
    parent_map = {start_node: None}
    
    # 2. THE BFS LOOP (Concentric Rings)
    while queue:
        # Pop the oldest, closest node
        current = queue.popleft()
        
        # Did we find the target?
        if current == target_node:
            # We found it! Reconstruct the exact path by walking backward!
            path = []
            curr = target_node
            while curr is not None:
                path.append(curr)
                curr = parent_map[curr]
            
            # The path was constructed backward (Target -> Start), so reverse it!
            return path[::-1]
            
        # Explore all neighbors
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                
                # IMPORTANT: Mark it visited the millisecond we PUSH it, not pop it!
                # If we wait to mark it until we pop it, another node's ripple 
                # might push a duplicate copy of this neighbor into the queue!
                visited.add(neighbor)
                parent_map[neighbor] = current
                
                # Push the neighbor to the BACK of the line!
                queue.append(neighbor)
                
    return None # Target not found in the connected component


# ==============================================================================
# 4. BI-DIRECTIONAL BFS (EXPONENTIAL OPTIMIZATION)
# ==============================================================================
def bi_directional_bfs(graph: Dict[int, List[int]], start: int, target: int) -> bool:
    """
    Shoots ripples from both the Start and Target simultaneously.
    If the Branching Factor is `b` and distance is `d`, standard BFS takes O(b^d).
    Bi-directional takes O(b^(d/2) + b^(d/2)), which is exponentially faster!
    """
    if start == target:
        return True
        
    q_start = deque([start])
    q_target = deque([target])
    
    visited_start = set([start])
    visited_target = set([target])
    
    # We expand the ripples 1 layer at a time, taking turns!
    while q_start and q_target:
        
        # --- EXPAND START RIPPLE BY 1 LAYER ---
        # We must process the entire exact layer (not just 1 node!)
        for _ in range(len(q_start)):
            curr = q_start.popleft()
            for neighbor in graph.get(curr, []):
                if neighbor in visited_target:
                    # COLLISION! The two ripples hit each other!
                    return True 
                if neighbor not in visited_start:
                    visited_start.add(neighbor)
                    q_start.append(neighbor)
                    
        # --- EXPAND TARGET RIPPLE BY 1 LAYER ---
        for _ in range(len(q_target)):
            curr = q_target.popleft()
            for neighbor in graph.get(curr, []):
                if neighbor in visited_start:
                    # COLLISION! The two ripples hit each other!
                    return True
                if neighbor not in visited_target:
                    visited_target.add(neighbor)
                    q_target.append(neighbor)
                    
    return False


def demonstrate_bfs():
    section_header("Algorithm: Breadth-First Search")
    
    # Adjacency List for an unweighted graph
    graph = {
        1: [2, 3],
        2: [1, 4, 5],
        3: [1, 6, 7],
        4: [2],
        5: [2, 8],
        6: [3],
        7: [3, 9],
        8: [5, 10],
        9: [7],
        10: [8]
    }
    
    start = 1
    target = 10
    
    print(f"Executing Standard BFS Shortest Path ({start} -> {target})...")
    path = bfs_shortest_path(graph, start, target)
    print(f"Optimal Path found: {path}")
    
    print(f"\nExecuting Exponentially Faster Bi-Directional BFS...")
    found = bi_directional_bfs(graph, start, target)
    print(f"Path exists? {found}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does BFS guarantee the shortest path, but DFS does not?
   Answer: Because BFS explores outward in perfect concentric rings (radii of distance 1, then 2, then 3). If it finds the target node on ring 3, it is physically impossible for a shorter path to exist on ring 1 or 2, because those rings were exhaustively searched before ring 3 was even created! DFS, on the other hand, blindly plunges down a random path and might find the target node on a massively winding path of distance 900, completely ignoring the direct edge of distance 1 sitting right next to it.

2. Why must you use `collections.deque` instead of a standard `[]`?
   Answer: In memory, a Python List `[]` is a contiguous block of RAM. If you execute `list.pop(0)`, the operating system has to physically shift the memory addresses of every other element in the list one slot to the left. If the queue has 100,000 elements, popping the front takes $O(N)$ time. A `deque` is a Doubly-Linked List (pointers), so snapping the front node off takes $O(1)$ constant time.

3. Why is Bi-Directional BFS exponentially faster?
   Answer: Imagine a graph where every user has 100 friends (Branching Factor $b=100$). You want to find a connection 4 degrees away ($d=4$). Standard BFS explores $100^4 = 100,000,000$ nodes. Bi-Directional BFS starts from both sides and meets exactly in the middle at $d/2 = 2$. It explores $100^2$ from the left (10,000 nodes) and $100^2$ from the right (10,000 nodes). Total nodes explored: 20,000. It dropped from 100 Million to 20 Thousand!
"""

if __name__ == "__main__":
    demonstrate_bfs()
    print("\n[SUCCESS] Laboratory: BFS Variations Completed.")
