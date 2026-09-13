"""
# ==============================================================================
# LABORATORY: WEIGHTED JOB SCHEDULING (WHEN GREEDY FAILS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned two Greedy scheduling algorithms:
# 1. Activity Selection: Every job takes a different amount of time, but every 
#    job has the SAME VALUE (1). Greedy works! (Sort by End Time).
# 2. Job Sequencing with Deadlines: Every job has a DIFFERENT VALUE, but every 
#    job takes the SAME AMOUNT OF TIME (1 day). Greedy works! (Sort by Profit).
#
# But what if BOTH are different?
# What if jobs have DIFFERENT DURATIONS and DIFFERENT PROFITS?
# Example: 
# - Job A: 10 hours, $100.
# - Job B: 1 hour, $90.
# - Job C: 1 hour, $90.
# 
# A pure Greedy algorithm collapses completely. 
# If you sort by Profit, you pick Job A ($100), but it blocks B and C, losing $180!
# If you sort by Density ($/hr), you pick B and C, but what if they overlap?
# 
# This is called "Weighted Interval Scheduling". It is the final boss of the 
# scheduling problems. Greedy FAILS. We MUST use Dynamic Programming combined 
# with Binary Search to solve it in O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why the Greedy Choice Property fails for 2D variance.
# - Combine Sorting (Greedy) with State Transitions (DP).
# - Use Binary Search (`bisect`) inside a DP loop for O(N log N) performance.
#
# ==============================================================================
"""

import bisect
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DP + BINARY SEARCH ENGINE (O(N log N))
# ==============================================================================
class Job:
    def __init__(self, start: int, end: int, profit: int):
        self.start = start
        self.end = end
        self.profit = profit


def weighted_job_scheduling(jobs: List[Job]) -> int:
    """
    Time Complexity: O(N log N) (Sorting is O(N log N), and we do N Binary Searches).
    Space Complexity: O(N) for the DP array.
    """
    if not jobs:
        return 0
        
    n = len(jobs)
    
    # 1. THE GREEDY FOUNDATION (SORT BY END TIME)
    # Just like Activity Selection, the absolute most efficient way to organize 
    # intervals is by their End Time. This allows us to sweep the timeline 
    # left-to-right mathematically.
    jobs.sort(key=lambda x: x.end)
    
    # Extract just the end times into an array so we can run fast Binary Searches on it!
    end_times = [job.end for job in jobs]
    
    # 2. STATE DEFINITION
    # `dp[i]` represents the MAXIMUM profit achievable using a subset of the 
    # first `i` jobs.
    dp = [0] * n
    
    # Base Case: The max profit for the first job is just its own profit.
    dp[0] = jobs[0].profit
    
    # 3. TABULATION LOOP
    for i in range(1, n):
        current_profit = jobs[i].profit
        
        # --- THE BINARY SEARCH TRICK ---
        # If we INCLUDE this current job, we must find the most recent previous 
        # job that does NOT conflict with it!
        # The current job starts at `jobs[i].start`.
        # We need to find the job whose `end` is <= `jobs[i].start`.
        # Because `end_times` is strictly sorted, we can use Binary Search (`bisect_right`)
        # in O(log N) time instead of a slow backwards O(N) loop!
        
        # `bisect_right` returns an insertion index. If we subtract 1, it gives us 
        # the index of the last job that finishes before the current job starts!
        latest_non_conflict_idx = bisect.bisect_right(end_times, jobs[i].start) - 1
        
        if latest_non_conflict_idx >= 0:
            # We found a valid previous job! Add its absolute optimal DP profit.
            current_profit += dp[latest_non_conflict_idx]
            
        # --- STATE TRANSITION EQUATION ---
        # Option A: We EXCLUDE the current job. (The max profit is whatever we had at `i-1`).
        # Option B: We INCLUDE the current job. (The `current_profit` we just calculated).
        # We take the mathematical maximum!
        dp[i] = max(dp[i - 1], current_profit)
        
    # The final answer is the last element in the DP array.
    return dp[n - 1]


def demonstrate_weighted_scheduling():
    section_header("Algorithm: Weighted Job Scheduling (DP + Binary Search)")
    
    # Format: (Start, End, Profit)
    jobs_data = [
        (3, 10, 20),
        (1, 2, 50),
        (6, 19, 100),
        (2, 100, 200)
    ]
    
    jobs = [Job(s, e, p) for s, e, p in jobs_data]
    
    print("Available Jobs:")
    for j in jobs:
        print(f" Start: {j.start:3d} | End: {j.end:3d} | Profit: ${j.profit}")
        
    print("\nExecuting DP + Binary Search...")
    ans = weighted_job_scheduling(jobs)
    
    print(f"\nMaximum Profit Achievable: ${ans} (Expected: $250)")
    print("Explanation:")
    print("If you Greedily sort by Profit, you pick (2, 100, $200). That consumes ")
    print("the entire timeline, blocking everything else. Profit: $200.")
    print("But DP calculates that by picking (1, 2, $50) and (2, 100, $200), ")
    print("they perfectly align (Start 2 >= End 2), yielding $250!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Greedy Choice Property fail for Weighted Interval Scheduling?
   Answer: Because there is a massive variance in both Time and Value simultaneously. A greedy algorithm only evaluates the immediate local state. If a job has a massive payout, Greedy will instantly lock it in. But that job might span 400 days, blocking 400 smaller jobs that collectively sum to a much higher payout. Greedy cannot "look ahead" or "calculate opportunity costs" across a timeline; only Dynamic Programming can.

2. Why do we still sort by End Time if it's a DP problem?
   Answer: Sorting establishes the topological order of the timeline! DP needs a guaranteed chronological sequence to ensure that when calculating state `i`, all previous states `0` to `i-1` have already been fully resolved. If the array wasn't sorted by End Time, `dp[i-1]` might physically occur AFTER `dp[i]`, shattering the logic of the algorithm.

3. Without Binary Search, what is the Time Complexity of this DP algorithm?
   Answer: $O(N^2)$. Inside the `for i in range(1, n)` loop, you would need another `for j in range(i-1, -1, -1)` loop to manually scan backwards until you find a non-conflicting job. Because we sorted the array first, the End Times are perfectly monotonically increasing, allowing us to swap the inner $O(N)$ loop for an $O(\\log N)$ Binary Search, dropping the total time to $O(N \\log N)$.
"""

if __name__ == "__main__":
    demonstrate_weighted_scheduling()
    print("\n[SUCCESS] Laboratory: Weighted Job Scheduling Completed.")
