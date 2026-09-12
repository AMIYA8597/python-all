"""
Job Sequencing Problem with Deadlines

Learning Objectives:
1. Model jobs with deadlines and profits.
2. Implement greedy selection to maximize profit under time constraints.
3. Understand disjoint set applications for faster job scheduling (advanced).

Concept Explanation:
Given a set of jobs where every job has a deadline and profit if the job is finished before the deadline.
It is also given that every job takes the same time (1 unit) to complete.
The goal is to maximize the total profit if only one job can be scheduled at a time.
The greedy strategy is to sort the jobs in decreasing order of profit, and then for each job, 
find the latest available time slot before its deadline.

Performance Analysis:
- Time Complexity: O(N^2) for basic, O(N log N) with Disjoint Set Union (DSU) for advanced.
- Space Complexity: O(N) to store time slots.

Edge Cases:
- Max deadline is very large.
- All deadlines are 1.
- No jobs provided.

Interview Challenge:
"Given jobs with deadlines and profits, maximize your profit."
"""

from typing import List, Tuple
import unittest

def job_scheduling_basic(profits: List[int], deadlines: List[int]) -> int:
    """Basic O(N^2) implementation returning max profit."""
    if not profits or not deadlines:
        return 0
        
    n = len(profits)
    jobs = [(profits[i], deadlines[i]) for i in range(n)]
    jobs.sort(key=lambda x: x[0], reverse=True)
    
    max_deadline = max(deadlines)
    slots = [-1] * max_deadline
    total_profit = 0
    
    for profit, deadline in jobs:
        for j in range(min(max_deadline - 1, deadline - 1), -1, -1):
            if slots[j] == -1:
                slots[j] = 1
                total_profit += profit
                break
                
    return total_profit

class Job:
    def __init__(self, id: str, deadline: int, profit: int):
        self.id = id
        self.deadline = deadline
        self.profit = profit

def job_scheduling_intermediate(jobs: List[Job]) -> Tuple[int, List[str]]:
    """Intermediate implementation returning total profit and scheduled job IDs."""
    jobs.sort(key=lambda x: x.profit, reverse=True)
    
    if not jobs:
        return 0, []
        
    max_deadline = max(job.deadline for job in jobs)
    slots = [None] * max_deadline
    total_profit = 0
    
    for job in jobs:
        for j in range(min(max_deadline - 1, job.deadline - 1), -1, -1):
            if slots[j] is None:
                slots[j] = job.id
                total_profit += job.profit
                break
                
    return total_profit, [s for s in slots if s is not None]

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))
        
    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
        
    def union(self, i: int, j: int):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j

def job_scheduling_advanced(jobs: List[Job]) -> Tuple[int, List[str]]:
    """Advanced implementation using Disjoint Set Union (DSU) for O(N log N) time."""
    jobs.sort(key=lambda x: x.profit, reverse=True)
    
    if not jobs:
        return 0, []
        
    max_deadline = max(job.deadline for job in jobs)
    dsu = DSU(max_deadline)
    total_profit = 0
    scheduled_jobs = []
    
    for job in jobs:
        available_slot = dsu.find(job.deadline)
        if available_slot > 0:
            dsu.union(available_slot, available_slot - 1)
            total_profit += job.profit
            scheduled_jobs.append(job.id)
            
    return total_profit, scheduled_jobs

class TestJobScheduling(unittest.TestCase):
    def test_basic(self):
        profits = [20, 15, 10, 5, 1]
        deadlines = [2, 2, 1, 3, 3]
        self.assertEqual(job_scheduling_basic(profits, deadlines), 40) # 20 + 15 + 5
        
    def test_intermediate(self):
        jobs = [Job('a', 2, 100), Job('b', 1, 19), Job('c', 2, 27), Job('d', 1, 25), Job('e', 3, 15)]
        profit, ids = job_scheduling_intermediate(jobs)
        self.assertEqual(profit, 142) # a, c, e
        
    def test_advanced(self):
        jobs = [Job('a', 2, 100), Job('b', 1, 19), Job('c', 2, 27), Job('d', 1, 25), Job('e', 3, 15)]
        profit, ids = job_scheduling_advanced(jobs)
        self.assertEqual(profit, 142)

if __name__ == "__main__":
    unittest.main()
