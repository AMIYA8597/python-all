"""
# ==============================================================================
# LABORATORY: A* SEARCH (HEURISTIC OPTIMIZATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Dijkstra's Algorithm finds the shortest path perfectly, but it is BLIND.
# If you are in New York and want to drive to Los Angeles, Dijkstra will explore 
# roads heading to Boston, Florida, and Canada, expanding in a perfect circle, 
# completely unaware that LA is to the West!
#
# It wastes massive CPU cycles exploring completely irrational directions.
#
# In 1968, researchers at Stanford (building the Shakey the Robot AI) invented 
# the A* (A-Star) algorithm.
#
# A* gives Dijkstra a "Compass". It uses a "Heuristic" (an educated guess).
# Dijkstra prioritizes nodes solely on `g`: The physical distance from the Start.
# A* prioritizes nodes based on `f = g + h`:
# - `g`: Physical distance from the Start.
# - `h`: Estimated (Heuristic) distance to the Target!
#
# If the heuristic tells the Priority Queue that LA is to the West, the PQ will 
# aggressively prioritize western roads, instantly pruning the eastern expansion.
#
# Rule of A*: The heuristic MUST be "Admissible". It must NEVER overestimate the 
# true distance. If it overestimates, A* loses its mathematical guarantee and 
# might return a sub-optimal path.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Heuristic Functions (Manhattan vs Euclidean).
# - Implement A* on a 2D Grid Map (Video Game Pathfinding).
# - Track the `f = g + h` equation in a Min-Heap.
#
# ==============================================================================
"""

import heapq
from typing import List, Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HEURISTICS
# ==============================================================================
def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """
    Used when movement is strictly 4-directional (Up, Down, Left, Right).
    Like driving in Manhattan, you cannot drive diagonally through buildings.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def euclidean_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """
    Used when movement can be diagonal or omni-directional. (Pythagorean Theorem).
    """
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** 0.5


# ==============================================================================
# 4. A-STAR ENGINE (2D GRID PATHFINDING)
# ==============================================================================
def a_star(grid: List[List[int]], start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    Finds the shortest path on a 2D grid.
    Grid constraints: 0 = Free Space, 1 = Wall/Obstacle.
    Returns the exact path array of coordinates.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    # Priority Queue stores: (f_score, g_score, (r, c))
    # We include g_score in the tuple just to break ties predictably.
    pq = []
    
    # Heuristic for the Start node
    start_h = manhattan_distance(start, target)
    heapq.heappush(pq, (0 + start_h, 0, start))
    
    # Dictionaries to track actual g-scores and parent pointers
    g_scores = {start: 0}
    parent_map = {start: None}
    
    # 4-Directional Movement (Up, Down, Left, Right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    nodes_explored = 0 # To prove A*'s efficiency later!
    
    while pq:
        # Pop the node with the lowest `f_score`
        current_f, current_g, current_node = heapq.heappop(pq)
        
        # Stale record check (same as Dijkstra)
        if current_g > g_scores.get(current_node, float('inf')):
            continue
            
        nodes_explored += 1
            
        # We found the target! Reconstruct path!
        if current_node == target:
            path = []
            curr = target
            while curr is not None:
                path.append(curr)
                curr = parent_map[curr]
            return path[::-1], nodes_explored
            
        # Explore neighbors
        r, c = current_node
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Boundary & Wall Checks
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                neighbor = (nr, nc)
                
                # In a 2D unweighted grid, every step costs exactly 1
                tentative_g = current_g + 1
                
                # If we found a strictly FASTER path to this neighbor...
                if tentative_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = tentative_g
                    parent_map[neighbor] = current_node
                    
                    # CALCULATE THE HEURISTIC (The A* Magic)
                    h = manhattan_distance(neighbor, target)
                    f = tentative_g + h
                    
                    heapq.heappush(pq, (f, tentative_g, neighbor))
                    
    return None, nodes_explored # Unreachable


def demonstrate_astar():
    section_header("Algorithm: A* Search (Video Game Pathfinding)")
    
    # 0 = Empty, 1 = Wall
    grid = [
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 1, 0, 0, 0]
    ]
    
    start = (0, 0)
    target = (4, 5)
    
    print("Executing A* Search Engine...")
    path, explored = a_star(grid, start, target)
    
    # Let's draw the grid with the path!
    print("\nVisual Output (S=Start, E=End, #=Wall, *=Path):")
    for r in range(len(grid)):
        row_str = ""
        for c in range(len(grid[0])):
            if (r, c) == start: row_str += "S "
            elif (r, c) == target: row_str += "E "
            elif grid[r][c] == 1: row_str += "# "
            elif path and (r, c) in path: row_str += "* "
            else: row_str += ". "
        print(row_str)
        
    print(f"\nTotal Nodes Explored by A*: {explored}")
    print("If you ran standard Dijkstra, it would have explored practically every '.' on the board!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What happens if the Heuristic is exactly 0 for every node?
   Answer: If $h = 0$, the priority equation $f = g + h$ simply becomes $f = g$. This is the exact mathematical equation for Dijkstra's Algorithm! A* flawlessly degrades into standard Dijkstra when the heuristic is disabled.

2. What does "Admissible" mean, and why does it break the algorithm if violated?
   Answer: "Admissible" means the heuristic must NEVER overestimate the true distance. If the real distance to the target is 10 miles, the heuristic can guess 5 (safe), 9 (safe), or 10 (perfect). But if it guesses 15 (overestimate), the Priority Queue will look at that path and incorrectly categorize it as highly expensive. The PQ will ignore it and finalize a sub-optimal 12-mile path instead! A* strictly relies on the heuristic being optimistic to mathematically guarantee the shortest path.

3. Can A* be used on graphs that are not 2D Grids?
   Answer: YES! The internet routing system BGP uses heuristics. Rubik's Cube solvers use A* with a 3D state-space graph where the heuristic is the "Manhattan Distance of the colored cubes to their correct faces". As long as you can write a mathematical function that estimates the cost to the target without overestimating, A* will obliterate Dijkstra's runtimes.
"""

if __name__ == "__main__":
    demonstrate_astar()
    print("\n[SUCCESS] Laboratory: A* Search Completed.")
