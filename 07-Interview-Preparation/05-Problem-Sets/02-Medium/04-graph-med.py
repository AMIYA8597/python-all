"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - GRAPH MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Graph problems are fundamentally pathfinding algorithms. You must know when to 
# deploy Depth-First Search (DFS) versus Breadth-First Search (BFS).
#
# A junior engineer tries to solve a Shortest-Path problem using DFS. They get 
# trapped exploring a 10,000-node dead-end branch before realizing the answer 
# was only 2 steps away in another branch, violently exceeding the time limit.
#
# A senior engineer understands Graph Physics. They use DFS (Stack) for aggressive 
# component annihilation (Islands, Cycle Detection). They explicitly deploy BFS 
# (Queue) for radial proximity scaling (Rotting Oranges, Shortest Path), because 
# BFS guarantees the shortest mathematical distance in an unweighted graph.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master DFS Grid Annihilation (Number of Islands).
# - Master Topological Sort and Cycle Detection (Course Schedule).
# - Master Radial BFS (Rotting Oranges).
#
# ==============================================================================
"""

import collections
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NUMBER OF ISLANDS (DFS GRID ANNIHILATION)
# ==============================================================================
def num_islands(grid: List[List[str]]) -> int:
    """
    Time: O(R * C) | Space: O(R * C) for Call Stack worst case
    Given an m x n 2D binary grid which represents a map of '1's (land) and 
    '0's (water), return the number of islands.
    """
    if not grid: return 0
    
    rows = len(grid)
    cols = len(grid[0])
    islands_count = 0
    
    def sink_island(r: int, c: int) -> None:
        # BASE CASES: Boundary violations or Water ('0')
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return
            
        # ANNIHILATE THE LAND!
        # By instantly converting the '1' to a '0', we mathematically guarantee 
        # that we will never process this specific coordinate again, completely 
        # bypassing the need for a separate `visited` Hash Set!
        grid[r][c] = "0"
        
        # Recursively sink all adjacent connected landmasses!
        sink_island(r + 1, c) # Down
        sink_island(r - 1, c) # Up
        sink_island(r, c + 1) # Right
        sink_island(r, c - 1) # Left

    print("  Scanning oceanic grid for landmasses...")
    for r in range(rows):
        for c in range(cols):
            # We found the coast of a brand new Island!
            if grid[r][c] == "1":
                islands_count += 1
                print(f"    -> [ISLAND FOUND] Coordinate ({r},{c}). Deploying Annihilation Engine...")
                # The DFS engine will violently spread out and sink the ENTIRE 
                # island, leaving nothing but water behind!
                sink_island(r, c)
                
    return islands_count

def demonstrate_islands():
    section_header("Medium: Number of Islands (DFS Annihilation)")
    
    grid = [
      ["1","1","0","0","0"],
      ["1","1","0","0","0"],
      ["0","0","1","0","0"],
      ["0","0","0","1","1"]
    ]
    
    ans = num_islands(grid)
    print(f"\nResult: Found {ans} Islands. (Expected: 3)")


# ==============================================================================
# 4. COURSE SCHEDULE (CYCLE DETECTION / TOPOLOGICAL SORT)
# ==============================================================================
def can_finish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Time: O(V + E) | Space: O(V + E)
    There are a total of numCourses. Prerequisites are given as [a, b], which 
    means you must take b before a. Can you finish all courses?
    
    This is mathematically identical to asking: "Does this Directed Graph contain a Cycle?"
    """
    # 1. Build the Adjacency List (The Graph Architecture)
    graph = collections.defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        
    # State Map for Cycle Detection!
    # 0 = Unvisited, 1 = Currently Visiting (In the active Call Stack), 2 = Fully Cleared
    state = [0] * numCourses
    
    def has_cycle(course_id: int) -> bool:
        # If the state is 1, we are currently inside this node's dependency chain!
        # If we hit it again, we have mathematically looped back on ourselves!
        if state[course_id] == 1:
            print(f"      -> [CYCLE DETECTED] Dependency loop at Course {course_id}!")
            return True
            
        # If the state is 2, we already verified this branch in the past. It's safe!
        if state[course_id] == 2:
            return False
            
        # Mark as ACTIVE in the current traversal path!
        state[course_id] = 1
        
        # Traverse all downstream dependencies
        for neighbor in graph[course_id]:
            if has_cycle(neighbor):
                return True
                
        # We successfully explored the entire branch without hitting a cycle!
        # Mark as FULLY CLEARED. We never need to check this node again!
        state[course_id] = 2
        return False

    print("  Mapping dependency graph and executing Cycle Detection...")
    for i in range(numCourses):
        if state[i] == 0:
            if has_cycle(i):
                return False # A cycle exists, graduation is mathematically impossible.
                
    return True

def demonstrate_course_schedule():
    section_header("Medium: Course Schedule (Cycle Detection)")
    
    # You must take 0 to take 1. And you must take 1 to take 0! An impossible paradox!
    prereqs = [[1, 0], [0, 1]]
    print(f"Dependencies: {prereqs}")
    
    ans = can_finish(2, prereqs)
    print(f"\nResult: Can finish? {ans} (Expected: False)")


# ==============================================================================
# 5. ROTTING ORANGES (RADIAL BFS SPREAD)
# ==============================================================================
def oranges_rotting(grid: List[List[int]]) -> int:
    """
    Time: O(R * C) | Space: O(R * C)
    0 = Empty, 1 = Fresh Orange, 2 = Rotten Orange.
    Every minute, any fresh orange that is 4-directionally adjacent to a rotten 
    orange becomes rotten. Return the minimum number of minutes until no cell 
    has a fresh orange.
    """
    rows = len(grid)
    cols = len(grid[0])
    
    queue = collections.deque()
    fresh_count = 0
    
    # 1. INITIALIZATION: Build the Battlefield!
    # Find ALL initially rotten oranges (they are the starting nodes for the BFS!)
    # and count the exact number of fresh oranges.
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1
                
    # If there are no fresh oranges, the job is already done (Time = 0).
    if fresh_count == 0:
        return 0
        
    minutes_passed = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    print(f"  Initial State: {len(queue)} Rotten Nodes, {fresh_count} Fresh Targets.")
    
    # 2. RADIAL BFS SPREAD
    while queue and fresh_count > 0:
        minutes_passed += 1
        level_size = len(queue)
        
        # We MUST process level by level to simulate time passing!
        for _ in range(level_size):
            r, c = queue.popleft()
            
            # Spread the infection in all 4 directions!
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # If it's a valid coordinate AND it contains a Fresh Orange...
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    # INFECT IT!
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc)) # The newly infected orange becomes a spreader for the next minute!
                    
    # If the queue is empty, but there are still fresh oranges left, they must 
    # be mathematically isolated behind empty cells (0) and are impossible to reach!
    if fresh_count > 0:
        print(f"    -> [ISOLATION] {fresh_count} oranges survived. Infection failed.")
        return -1
        
    return minutes_passed

def demonstrate_rotting_oranges():
    section_header("Medium: Rotting Oranges (Radial BFS)")
    
    grid = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    ans = oranges_rotting(grid)
    print(f"\nResult: {ans} minutes. (Expected: 4)")


def run_all_labs():
    demonstrate_islands()
    demonstrate_course_schedule()
    demonstrate_rotting_oranges()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 'Number of Islands', why is modifying the input grid (`grid[r][c] = '0'`) a potentially dangerous practice in production code, even though it achieves $O(1)$ Space?"
   Senior Answer: "Modifying the input grid permanently destroys the original state of the data structure provided by the caller. If another component of the application needed to access that map later, it would receive a completely corrupted, annihilated matrix of zeroes. In a real production environment, you should never aggressively mutate input parameters unless explicitly authorized. Instead, you would allocate a separate `visited` Hash Set or boolean matrix ($O(R \\times C)$ Space) to track the state safely, preserving the integrity of the original data."

2. Interviewer: "In 'Course Schedule', why do we need 3 states (`0`, `1`, `2`) for cycle detection? Why can't we just use a standard boolean `visited` Hash Set?"
   Senior Answer: "A standard boolean `visited` set only tells us if we have *ever* seen a node before across the entire graph. In a Directed Graph, you can legitimately arrive at the same node from two completely different, valid paths without it being a cycle! (e.g., A -> C and B -> C). To detect a cycle, we must definitively prove that we have looped back on our *CURRENT active traversal path*. The `1` state (Currently Visiting) perfectly represents the nodes actively trapped in the current Call Stack. If we hit a `1`, it is a guaranteed paradox loop. The `2` state (Fully Cleared) allows us to safely bypass branches we have already mathematically proven are cycle-free."

3. Interviewer: "Why is BFS (Queue) structurally mandatory for 'Rotting Oranges'? What would happen if you used DFS (Stack)?"
   Senior Answer: "The problem asks for the *minimum* time required for the infection to spread. This is a Radial Proximity problem. BFS uses a Queue, which mathematically processes all nodes at Distance $D$ before ever touching a node at Distance $D+1$. This perfectly simulates the chronological passing of time, expanding the infection outward uniformly like a shockwave. If you used DFS (Stack), the algorithm would aggressively dive down a single narrow path, instantly infecting a node 10,000 miles away before it even checks the orange sitting right next to the origin! DFS completely obliterates the concept of Minimum Distance and Chronological Time, returning catastrophically incorrect results."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Graph Medium) Completed.")
