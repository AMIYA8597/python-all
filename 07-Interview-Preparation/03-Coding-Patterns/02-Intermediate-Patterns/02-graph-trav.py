"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (CODING PATTERNS - GRAPH TRAVERSAL)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "Given a 2D matrix of 1s (land) and 0s (water), count the number 
# of islands. An island is surrounded by water and formed by connecting adjacent 
# lands horizontally or vertically."
#
# A junior engineer attempts to use deeply nested `for` loops, gets confused by 
# the boundaries of the matrix, revisits the same land multiple times, and creates 
# an infinite loop. They fail.
#
# A senior engineer immediately recognizes this as a Graph problem! 
# The Matrix IS the Graph. Every cell is a Node, and its 4 adjacent neighbors are 
# its Edges. To prevent infinite loops (because Graphs, unlike Trees, can have 
# cycles!), the senior engineer deploys a strictly enforced `visited` Hash Set 
# or physically mutates the matrix to mathematically mark nodes as dead.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Graph Traversal on a 2D Matrix (BFS and DFS).
# - Master the mathematical boundary checks (`0 <= r < ROWS`).
# - Master cycle prevention using State Mutation (The 'Visited' Set).
#
# ==============================================================================
"""

import collections
from typing import List, Set, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DEPTH-FIRST SEARCH ON A MATRIX (NUMBER OF ISLANDS)
# ==============================================================================
def num_islands_dfs(grid: List[List[str]]) -> int:
    """
    Time: O(R * C) | Space: O(R * C) for the recursive call stack.
    We iterate through the matrix. The moment we find a '1' (Land), we increment 
    our Island count, and then deploy a DFS virus that spreads in 4 directions, 
    physically mutating the Land into '0' (Water) so we never visit it again!
    """
    if not grid: return 0
    
    ROWS, COLS = len(grid), len(grid[0])
    islands = 0
    
    def dfs_sink_island(r: int, c: int):
        # BASE CASE / BOUNDARY CHECKS!
        # If we step out of bounds, OR we step in Water ('0'), we stop spreading.
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or grid[r][c] == '0':
            return
            
        # STATE MUTATION (CYCLE PREVENTION):
        # We physically sink the land! It becomes water. 
        # This completely eliminates the need for an external 'Visited' Hash Set!
        grid[r][c] = '0'
        
        # Spread the virus in all 4 physical directions (Up, Down, Left, Right)
        dfs_sink_island(r + 1, c)
        dfs_sink_island(r - 1, c)
        dfs_sink_island(r, c + 1)
        dfs_sink_island(r, c - 1)

    print("  Scanning the Grid...")
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == '1':
                print(f"    -> [NEW ISLAND FOUND] Launching DFS Virus at ({r}, {c})")
                islands += 1
                dfs_sink_island(r, c)
                
    return islands

def demonstrate_islands_dfs():
    section_header("Number of Islands (DFS State Mutation)")
    
    grid = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    
    # We must deep copy it because DFS will physically destroy it!
    import copy
    grid_copy = copy.deepcopy(grid)
    
    print("Original Matrix:")
    for row in grid_copy: print(f"  {row}")
    print()
    
    result = num_islands_dfs(grid_copy)
    print(f"\nResult: Total Islands = {result}")


# ==============================================================================
# 4. BREADTH-FIRST SEARCH ON A MATRIX (SHORTEST PATH)
# ==============================================================================
def oranges_rotting_bfs(grid: List[List[int]]) -> int:
    """
    Time: O(R * C) | Space: O(R * C)
    Every minute, any fresh orange ('1') that is 4-directionally adjacent to a 
    rotten orange ('2') becomes rotten. Return the minimum minutes.
    
    Why BFS? Because DFS dives deep down one path blindly. BFS spreads out evenly 
    layer by layer. Finding the 'Shortest Path' or 'Minimum Minutes' mathematically 
    requires a Multi-Source BFS!
    """
    if not grid: return -1
    
    ROWS, COLS = len(grid), len(grid[0])
    queue = collections.deque()
    fresh_count = 0
    
    # 1. MULTI-SOURCE INITIALIZATION
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 2:
                # Add ALL rotten oranges to the queue at Time=0
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1
                
    if fresh_count == 0: return 0 # No fresh oranges to begin with!
    
    minutes_passed = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    print(f"  Initial State: {fresh_count} fresh oranges. {len(queue)} rotten oranges in Queue.")
    
    # 2. BFS SPREADING
    while queue and fresh_count > 0:
        minutes_passed += 1
        print(f"  [Minute {minutes_passed}] Spreading rot...")
        
        # We must only process the oranges currently in the queue for this specific minute!
        for _ in range(len(queue)):
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # If neighbor is in bounds AND is a fresh orange...
                if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
                    # Physically rot it! (State Mutation prevents infinite loops)
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc)) # Add to queue for the NEXT minute
                    
    # If there are still fresh oranges, they are mathematically isolated on an island!
    return minutes_passed if fresh_count == 0 else -1

def demonstrate_rotting_oranges():
    section_header("Rotting Oranges (Multi-Source BFS)")
    
    # 2: Rotten, 1: Fresh, 0: Empty
    grid = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    
    print("Original Grid:")
    for row in grid: print(f"  {row}")
    print()
    
    result = oranges_rotting_bfs(grid)
    print(f"\nResult: Total Minutes = {result}")


def run_all_labs():
    demonstrate_islands_dfs()
    demonstrate_rotting_oranges()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In a Graph traversal, why is it absolutely catastrophic to forget the `visited` Set (or State Mutation), whereas in a Tree traversal it's generally fine?"
   Senior Answer: "A Tree is a highly structured Directed Acyclic Graph (DAG). Parent nodes point to children, but children NEVER point back to parents. You physically cannot enter an infinite loop in a standard Tree. A generic Graph, however, can contain Cycles (e.g., A points to B, B points to C, C points to A). If you do not mathematically track which nodes you have already processed (either via an external Hash Set or by mutating the matrix cell from '1' to '0'), the algorithm will violently bounce between A, B, and C forever, instantly crashing the server with a `RecursionError` or a massive CPU spike."

2. Interviewer: "When finding the 'Shortest Path' in a maze, why MUST we use BFS instead of DFS?"
   Senior Answer: "DFS explores a graph by diving as deeply down a single path as mathematically possible before backtracking. If it finds the target, the path it took is simply the *first* path it found, not necessarily the shortest. It could have taken a massive, spiraling 100-step detour. BFS, however, explores the graph identically to ripples in a pond. It perfectly explores all paths of length 1, then all paths of length 2, and so on. Therefore, the absolute mathematical second that BFS touches the target, we have mathematical certainty that it is the Shortest Path, because all shorter permutations were definitively exhausted in the previous ripples."

3. Interviewer: "What is 'Multi-Source BFS', and why did we use it in the Rotting Oranges problem?"
   Senior Answer: "A standard BFS originates from exactly ONE starting node. However, in the Rotting Oranges problem, the matrix might start with 5 completely independent rotten oranges scattered across the grid. If we run 5 separate BFS algorithms sequentially, the algorithm degrades to $O(N^2)$ and overlapping ripples cause horrific calculation collisions. Multi-Source BFS solves this by pre-loading ALL 5 rotten oranges into the Queue *before* the `while` loop even begins. This forces the single BFS instance to spread from all 5 locations simultaneously at Time=0, simulating perfect parallel expansion in a flawless $O(N)$ sweep."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Graph Traversal) Completed.")
