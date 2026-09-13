"""
# ==============================================================================
# LABORATORY: JOB SEQUENCING WITH DEADLINES (GREEDY + DISJOINT SET)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Another classic Greedy Problem: "Job Sequencing with Deadlines".
# You are a freelancer. You have N jobs you could accept.
# Each job takes exactly 1 day to complete.
# Each job has a Deadline (e.g., must be finished by Day 3) and a Profit ($$).
# How do you maximize your total profit?
#
# The Greedy Heuristic is obvious: SORT BY PROFIT DESCENDING!
# We absolutely want to do the highest-paying jobs. 
# But WHEN do we schedule them?
# If a high-paying job has a deadline of Day 5, should we do it on Day 1?
# NO! If we do it on Day 1, we might block a different job that had a strict 
# deadline of Day 1. 
# The optimal Greedy Choice is: "Schedule the job on the LATEST POSSIBLE DAY 
# before its deadline."
#
# A naive implementation uses an array of days and scans backwards. Time: O(N^2).
# A Master-level implementation uses the "Disjoint Set" (Union-Find) data 
# structure to instantly jump to the nearest empty day! Time: O(N log N).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Sort by Profit vs sorting by Deadline.
# - Understand the "Latest Possible Day" greedy choice.
# - Implement Disjoint Set path compression to optimize the schedule search.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE GREEDY ALGORITHM (O(N^2))
# ==============================================================================
def job_sequencing_naive(jobs: List[Tuple[str, int, int]]) -> Tuple[int, List[str]]:
    """
    Input: List of (JobName, Deadline, Profit)
    Time Complexity: O(N^2)
    Space Complexity: O(MaxDeadline)
    """
    # 1. Sort by Profit (Descending)
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    # Find the maximum deadline to size our schedule array
    max_deadline = max(job[1] for job in jobs)
    
    # The schedule array. 0-indexed, but days are 1-indexed.
    # We create it slightly larger for 1-indexing convenience.
    schedule = [None] * (max_deadline + 1)
    
    total_profit = 0
    jobs_done = []
    
    for job in jobs:
        name, deadline, profit = job
        
        # 2. THE GREEDY CHOICE: START FROM THE DEADLINE AND SCAN BACKWARDS
        # Find the latest available free day for this job.
        for day in range(deadline, 0, -1):
            if schedule[day] is None:
                # We found a free day! Lock it in.
                schedule[day] = name
                total_profit += profit
                jobs_done.append(name)
                break
                
    return total_profit, jobs_done


# ==============================================================================
# 4. DISJOINT SET (UNION-FIND) OPTIMIZATION (O(N log N))
# ==============================================================================
class DisjointSet:
    def __init__(self, max_day: int):
        # The parent of `day` is the greatest available free day less than or 
        # equal to `day`.
        # Initially, every day is its own parent (meaning the day itself is free!)
        self.parent = [i for i in range(max_day + 1)]
        
    def find(self, day: int) -> int:
        """
        Finds the nearest available free day.
        Uses Path Compression to flatten the tree for O(1) amortized time!
        """
        # If a day is its own parent, it means this day is free.
        if self.parent[day] == day:
            return day
            
        # Path Compression: Point directly to the root free day.
        self.parent[day] = self.find(self.parent[day])
        return self.parent[day]
        
    def union(self, u: int, v: int):
        """
        Marks a day as occupied by pointing it to the next available free day.
        """
        self.parent[u] = v


def job_sequencing_dsu(jobs: List[Tuple[str, int, int]]) -> int:
    """
    Input: List of (JobName, Deadline, Profit)
    Time Complexity: O(N log N) (The sort dominates. The DSU operations are amortized O(1)).
    """
    # 1. Sort by Profit (Descending)
    jobs.sort(key=lambda x: x[2], reverse=True)
    
    max_deadline = max(job[1] for job in jobs)
    
    dsu = DisjointSet(max_deadline)
    total_profit = 0
    
    for job in jobs:
        name, deadline, profit = job
        
        # 2. INSTANTLY find the nearest available day <= deadline
        available_day = dsu.find(deadline)
        
        # If the available day is > 0, we can schedule it!
        if available_day > 0:
            total_profit += profit
            
            # 3. UNION: Mark this day as occupied!
            # The next available day for anything requesting `available_day` 
            # is now whatever is available BEFORE it (available_day - 1).
            dsu.union(available_day, dsu.find(available_day - 1))
            
    return total_profit


def demonstrate_job_sequence():
    section_header("Algorithm: Job Sequencing with Deadlines")
    
    # Format: (JobName, Deadline, Profit)
    jobs = [
        ("Job_A", 2, 100),
        ("Job_B", 1, 19),
        ("Job_C", 2, 27),
        ("Job_D", 1, 25),
        ("Job_E", 3, 15)
    ]
    
    print("Available Jobs:")
    for j in jobs:
        print(f" {j[0]}: Deadline Day {j[1]} | Profit ${j[2]}")
        
    print("\nExecuting Naive Greedy Algorithm (O(N^2))...")
    profit_naive, scheduled = job_sequencing_naive(jobs.copy())
    print(f"Total Profit: ${profit_naive}")
    print(f"Jobs Scheduled: {scheduled}")
    
    print("\nExecuting DSU-Optimized Greedy Algorithm (O(N log N))...")
    profit_dsu = job_sequencing_dsu(jobs.copy())
    print(f"Total Profit: ${profit_dsu}")
    
    print("\nExplanation of the Greedy Strategy:")
    print("1. Sort by Profit: A($100), C($27), D($25), B($19), E($15).")
    print("2. Job A (Deadline 2): Schedule on Day 2. (Leaves Day 1 open).")
    print("3. Job C (Deadline 2): Day 2 is full! Scan backwards. Schedule on Day 1.")
    print("4. Job D (Deadline 1): Day 1 is full. Discard.")
    print("5. Job B (Deadline 1): Day 1 is full. Discard.")
    print("6. Job E (Deadline 3): Schedule on Day 3.")
    print("Total = $100 + $27 + $15 = $142.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we schedule the job as LATE as possible?
   Answer: Opportunity Cost! If a job can be done on Day 1, 2, or 3, doing it on Day 1 permanently consumes a high-value slot that another stricter job (with a deadline of Day 1) might have needed. By pushing jobs to the very edge of their deadline, we preserve maximum flexibility for the earlier slots in the timeline.

2. How does the Disjoint Set (Union-Find) flatten the array scan?
   Answer: In the naive array, if Days 5, 4, 3, and 2 are full, and we try to schedule a job with a Deadline of 5, the `for` loop has to individually check 5, 4, 3, 2 before finally finding Day 1. That's an $O(N)$ linear scan. The DSU links the nodes together. By executing `dsu.union(5, dsu.find(4))` and doing Path Compression, the moment we ask `dsu.find(5)`, the data structure instantly returns `1` in $O(1)$ amortized time!

3. If each job took a DIFFERENT amount of time (e.g. Job A takes 3 days, Job B takes 1 day), does Greedy still work?
   Answer: NO! If jobs have different durations, the Greedy algorithm completely collapses (similar to how 0/1 Knapsack collapses compared to Fractional Knapsack). This variation is called "Weighted Job Scheduling", and it REQUIRES a Dynamic Programming solution (specifically, $O(N \\log N)$ DP with Binary Search to find the last non-overlapping job).
"""

if __name__ == "__main__":
    demonstrate_job_sequence()
    print("\n[SUCCESS] Laboratory: Job Sequencing Completed.")
