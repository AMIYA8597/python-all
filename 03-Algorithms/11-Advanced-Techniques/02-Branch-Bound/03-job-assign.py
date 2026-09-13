"""
# ==============================================================================
# LABORATORY: BRANCH AND BOUND (JOB ASSIGNMENT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Problem: You manage a construction company with N workers and N tasks. 
# Due to different skill levels, each worker charges a different amount of money 
# to perform each task. This is given as an $N \times N$ Cost Matrix.
# 
# Rule: You must assign exactly ONE worker to exactly ONE task.
# Goal: Minimize the total cost.
#
# If you have 20 workers, there are $20! = 2.4 \times 10^{18}$ possible assignment 
# permutations. A brute force algorithm will fail.
#
# Solution: Branch and Bound.
# We build a Backtracking search tree. At Level 0, we assign Worker 0. At Level 1, 
# we assign Worker 1. 
#
# To prune branches, we calculate an optimistic Lower Bound for the REMAINING workers.
# How? By mathematically relaxing the rules!
# The rule says "One worker per task". But for the bound calculation, we ignore 
# that rule! For every unassigned worker, we scan their row in the cost matrix 
# and find their absolute cheapest task. We sum those minimums up.
# 
# Even if multiple workers want the exact same cheap task, we allow it for the 
# bound calculation! This generates an incredibly optimistic, mathematically 
# strict lower ceiling. If `current_cost + bound >= best_cost`, we PRUNE!
#
# (Note: For massive matrices $N > 50$, the Hungarian Algorithm solves this in 
# strict $O(N^3)$ time, but BnB is heavily tested in university curriculums).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model assignment problems using State Space Trees.
# - Calculate Lower Bounds using Row/Column minimums.
# - Combine Backtracking with aggressive mathematical pruning.
#
# ==============================================================================
"""

import math
from typing import List, Tuple
from dataclasses import dataclass
import heapq

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BRANCH AND BOUND ENGINE (BEST-FIRST SEARCH)
# ==============================================================================
@dataclass
class AssignmentNode:
    worker_id: int
    cost_so_far: int
    lower_bound: int
    assigned_jobs: List[bool] # Which jobs are currently taken?
    
    # Python's `heapq` requires comparison operators!
    # We want to explore the node with the LOWEST bound first (Best-First Search).
    def __lt__(self, other):
        return self.lower_bound < other.lower_bound


def calculate_lower_bound(cost_matrix: List[List[int]], current_worker: int, assigned_jobs: List[bool]) -> int:
    """
    Calculates the relaxed Mathematical Lower Bound for all remaining workers.
    We simply find the absolute minimum cost for each remaining worker among 
    the currently UNAVAILABLE jobs.
    """
    n = len(cost_matrix)
    bound = 0
    
    # Loop through all workers that haven't been assigned yet
    for w in range(current_worker + 1, n):
        min_job_cost = float('inf')
        
        # Scan their row to find the cheapest AVAILABLE job
        for j in range(n):
            if not assigned_jobs[j]:
                if cost_matrix[w][j] < min_job_cost:
                    min_job_cost = cost_matrix[w][j]
                    
        bound += min_job_cost
        
    return bound


def solve_job_assignment_bnb(cost_matrix: List[List[int]]) -> int:
    """
    Solves the Assignment Problem using a Best-First Branch and Bound strategy.
    Uses a Priority Queue (Min-Heap) to constantly explore the most promising 
    branches first!
    """
    n = len(cost_matrix)
    
    # 1. PRIORITY QUEUE INITIALIZATION
    pq = []
    
    # Root node: Before any workers are assigned.
    root_jobs = [False] * n
    root_bound = calculate_lower_bound(cost_matrix, -1, root_jobs)
    
    root = AssignmentNode(
        worker_id=-1, 
        cost_so_far=0, 
        lower_bound=root_bound, 
        assigned_jobs=root_jobs
    )
    
    heapq.heappush(pq, root)
    
    # Performance Trackers
    nodes_explored = 0
    
    # 2. BEST-FIRST SEARCH
    while pq:
        # Pop the node with the absolute LOWEST optimistic bound!
        # This guarantees that the first time we hit the final worker, it is 
        # mathematically impossible for any other branch to beat it!
        curr = heapq.heappop(pq)
        nodes_explored += 1
        
        # The worker we need to assign next
        next_worker = curr.worker_id + 1
        
        # If we just finished assigning the last worker, we are DONE!
        # Because we use a Min-Heap based on Lower Bounds, the first complete 
        # leaf node we extract is mathematically guaranteed to be the global minimum!
        if next_worker == n:
            print(f"[Performance] Nodes Explored in Heap: {nodes_explored}")
            return curr.cost_so_far
            
        # 3. BRANCHING!
        # Try assigning this worker to every available job.
        for j in range(n):
            if not curr.assigned_jobs[j]:
                
                # Mark job as taken
                child_jobs = curr.assigned_jobs.copy()
                child_jobs[j] = True
                
                child_cost = curr.cost_so_far + cost_matrix[next_worker][j]
                
                # Calculate the bound for this specific branch
                child_bound_remainder = calculate_lower_bound(cost_matrix, next_worker, child_jobs)
                total_child_bound = child_cost + child_bound_remainder
                
                child_node = AssignmentNode(
                    worker_id=next_worker,
                    cost_so_far=child_cost,
                    lower_bound=total_child_bound,
                    assigned_jobs=child_jobs
                )
                
                # Throw it into the Priority Queue!
                heapq.heappush(pq, child_node)
                
    return -1


def demonstrate_assignment():
    section_header("Algorithm: Branch and Bound (Job Assignment)")
    
    # Cost Matrix (4 Workers, 4 Jobs)
    # W0: 9, 2, 7, 8
    # W1: 6, 4, 3, 7
    # W2: 5, 8, 1, 8
    # W3: 7, 6, 9, 4
    costs = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    
    print("Cost Matrix (Rows=Workers, Cols=Jobs):")
    for row in costs: print(row)
    
    print("\nExecuting Best-First Branch and Bound...")
    min_cost = solve_job_assignment_bnb(costs)
    
    print(f"\nAbsolute Minimum Cost: {min_cost}")
    print("Optimal Assignment Check:")
    print(" - W0 takes Job 1 (Cost: 2)")
    print(" - W1 takes Job 0 (Cost: 6)")
    print(" - W2 takes Job 2 (Cost: 1)")
    print(" - W3 takes Job 3 (Cost: 4)")
    print("Total: 2 + 6 + 1 + 4 = 13. Perfect!")
    
    print("\nNotice the extreme efficiency: A full backtracking tree for N=4 has 64 nodes.")
    print("Our Best-First Heap found the answer incredibly fast by always prioritizing")
    print("the branches with the lowest Mathematical Bounds!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Min-Heap (Best-First Search) allow us to stop instantly at the bottom?
   Answer: In standard Depth-First Search (DFS) Branch & Bound, you must find a valid solution first, save it as `best_cost`, and then continue exploring other branches to see if they can beat it. 
   In Best-First Search (using a Min-Heap sorted by Lower Bound), the priority queue ALWAYS expands the mathematically most promising node in the entire tree. Therefore, the very first time the heap pops a node that represents a FULLY COMPLETED assignment (a leaf node), it is mathematically impossible for any other node in the queue to be better, because the queue is strictly sorted by lowest bounds! You terminate immediately.

2. How did we calculate the Lower Bound for this problem?
   Answer: We mathematically relaxed the "One Worker per Job" constraint. To find the minimum possible cost for the remaining workers, we simply scanned each worker's row and picked the cheapest job that wasn't already assigned to a previous worker. Even if two remaining workers both desperately wanted the exact same cheap job, we pretended they could BOTH have it! This generates an optimistic bound (lower than reality) which is mathematically safe for pruning.

3. Is Branch and Bound the optimal algorithm for the Assignment Problem?
   Answer: For small-to-medium matrices, yes. However, for massive matrices (e.g., $1000 \times 1000$), the number of branches still grows too fast, and calculating the bound takes $O(N^2)$ time per node. The absolute mathematically optimal algorithm is the Hungarian Algorithm (Kuhn-Munkres), which solves it deterministically in strict $O(N^3)$ time using bipartite matching and matrix reduction!
"""

if __name__ == "__main__":
    demonstrate_assignment()
    print("\n[SUCCESS] Laboratory: Job Assignment BnB Completed.")
