"""
# ==============================================================================
# LABORATORY: BRANCH AND BOUND (GENERAL FRAMEWORKS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Branch and Bound (BnB) is not a single algorithm like Dijkstra's or Quicksort. 
# It is an algorithmic ARCHITECTURE (like Divide and Conquer).
#
# In the previous three labs, you solved TSP, 0/1 Knapsack, and Job Assignment. 
# If you look closely at the code, they used completely different traversal methods!
# - TSP used Depth-First Search (Recursion).
# - Knapsack used Breadth-First Search (Queue).
# - Job Assignment used Best-First Search (Priority Queue / Min-Heap).
#
# How do you choose which traversal method to use for your specific problem?
#
# 1. DFS Branch & Bound (Recursion)
#    - PRO: Extremely memory efficient. The call stack only stores $O(N)$ nodes.
#    - CON: You might dive deep down a terrible branch first, failing to update 
#      the `global_best` bound, meaning you miss out on early pruning. 
#      (Requires a Greedy initialization to work well).
#
# 2. BFS Branch & Bound (Queue)
#    - PRO: Explores the tree level by level. Good for shallow trees.
#    - CON: A branching factor of 10 means level 5 has 100,000 nodes physically 
#      sitting in the RAM queue. Can cause Out-Of-Memory crashes.
#
# 3. Best-First Branch & Bound (Priority Queue / A* Search)
#    - PRO: The most intelligent. Always jumps to the node with the absolute 
#      best Mathematical Bound. The very first time it hits a leaf node, it is 
#      guaranteed to be the global minimum.
#    - CON: Maintaining the Min-Heap adds $O(\log Q)$ overhead, and the queue 
#      can still grow exponentially large.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Formalize the mathematical requirements for a valid Lower Bound function.
# - Understand the architecture differences between DFS, BFS, and Best-First.
# - Implement a generic abstract class for Branch and Bound.
#
# ==============================================================================
"""

import heapq
from abc import ABC, abstractmethod
from typing import Any, List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BRANCH AND BOUND ARCHITECTURE (BEST-FIRST ABSTRACTION)
# ==============================================================================
class BnBNode(ABC):
    """
    Abstract Node class for a generic Best-First Branch and Bound search.
    """
    def __init__(self, cost_so_far: float, bound: float, level: int):
        self.cost = cost_so_far
        self.bound = bound
        self.level = level

    # The magic of Best-First Search: The heap sorts by BOUND!
    def __lt__(self, other: 'BnBNode') -> bool:
        return self.bound < other.bound

    @abstractmethod
    def generate_children(self) -> List['BnBNode']:
        """
        Creates all valid branches (children) from this node.
        Must calculate the cost and optimistic bound for each child!
        """
        pass
        
    @abstractmethod
    def is_leaf(self) -> bool:
        """
        Returns True if this node represents a fully completed solution.
        """
        pass


class BranchAndBoundSolver:
    def __init__(self, root: BnBNode, minimize: bool = True):
        self.root = root
        self.minimize = minimize
        
        # Performance Tracking
        self.nodes_explored = 0
        self.branches_pruned = 0
        
    def solve(self) -> Optional[BnBNode]:
        """
        Executes the Best-First Search algorithm using a Priority Queue.
        """
        pq = []
        # Python's heapq is a MIN-HEAP. 
        # If we want to MAXIMIZE (like in Knapsack), we must negate the bounds!
        heapq.heappush(pq, self.root)
        
        # Track the best solution found so far (in case a non-optimal branch 
        # hits a leaf node first, though rare in strict Best-First).
        best_leaf = None
        best_cost = float('inf') if self.minimize else float('-inf')
        
        while pq:
            curr_node = heapq.heappop(pq)
            self.nodes_explored += 1
            
            # 1. PRUNING CHECK (Is this node already worse than our best leaf?)
            if self.minimize:
                if curr_node.bound >= best_cost:
                    self.branches_pruned += 1
                    continue
            else:
                if curr_node.bound <= best_cost:
                    self.branches_pruned += 1
                    continue
                    
            # 2. IS IT A COMPLETED SOLUTION?
            if curr_node.is_leaf():
                # Update global best!
                if self.minimize:
                    if curr_node.cost < best_cost:
                        best_cost = curr_node.cost
                        best_leaf = curr_node
                else:
                    if curr_node.cost > best_cost:
                        best_cost = curr_node.cost
                        best_leaf = curr_node
                
                # In a strict mathematical Best-First search, the FIRST leaf node 
                # popped from the priority queue is the absolute global optimum!
                # We can instantly terminate.
                print(f"[Termination] Best-First Search reached the mathematical bottom!")
                return best_leaf
                
            # 3. BRANCHING!
            children = curr_node.generate_children()
            
            for child in children:
                # Secondary Pruning Check (Don't even put it in the queue if it's bad)
                if self.minimize and child.bound >= best_cost:
                    self.branches_pruned += 1
                    continue
                if not self.minimize and child.bound <= best_cost:
                    self.branches_pruned += 1
                    continue
                    
                heapq.heappush(pq, child)
                
        return best_leaf


def demonstrate_architecture():
    section_header("Algorithm: Branch and Bound (Architecture)")
    
    print("This file contains the Abstract Base Class framework for Best-First Search.")
    print("To use it in production:")
    print("1. Subclass `BnBNode`.")
    print("2. Implement `is_leaf()` (e.g., `return self.level == N`).")
    print("3. Implement `generate_children()`.")
    print("   -> Loop through available choices.")
    print("   -> CRITICAL: Calculate an optimistic bound for each choice!")
    print("   -> Return a list of child nodes.")
    print("4. Pass the Root node to `BranchAndBoundSolver` and call `solve()`.")
    
    print("\nWarning on Bound Calculations:")
    print("- Minimization Problem (TSP, Assignment):")
    print("  The bound MUST be purely optimistic (a LOWER bound). It can never ")
    print("  overestimate the cost. If it overestimates, it might accidentally ")
    print("  prune the true optimal answer.")
    print("- Maximization Problem (Knapsack):")
    print("  The bound MUST be purely optimistic (an UPPER bound). It can never ")
    print("  underestimate the profit. (Fractional knapsack perfectly provides this).")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Best-First Search instantly terminate on the first leaf node?
   Answer: The priority queue is strictly sorted by the Mathematical Bound. In a minimization problem, the node at the top of the heap is the one with the absolute LOWEST possible mathematical bound across the entire tree. When a leaf node is popped, its bound is EXACTLY equal to its actual physical cost (because there are no remaining choices to estimate!). If its physical cost was popped before the optimistic mathematical bounds of any other branch, it is mathematically impossible for those other branches to ever achieve a physical cost lower than the leaf node! 

2. If Best-First Search is so good, why did we use DFS for TSP?
   Answer: RAM limitations. In TSP with $N=30$, the branching factor at the root is 30. Then 29, then 28. If we use Best-First Search, the priority queue will rapidly fill up with millions of nodes, consuming Gigabytes of memory, and potentially crashing the system. DFS (Recursion) only explores one branch at a time, meaning the Call Stack only ever holds 30 nodes! If memory is a constraint, DFS Branch & Bound (with a good Greedy initialization) is significantly safer than BFS/Best-First.

3. What happens if your Mathematical Bound is completely inaccurate?
   Answer: 
   - If it is PESSIMISTIC (e.g., estimating the TSP cost will be 500 when the true cost is 300), the pruning logic `bound >= best_cost` might trigger incorrectly and delete the branch containing the true optimal answer! Your algorithm will output the WRONG answer.
   - If it is overly OPTIMISTIC (e.g., estimating the TSP cost will be 0 for every branch), the pruning logic will NEVER trigger! Your algorithm will degrade into a brute-force $O(N!)$ search. 
   Designing a bound that is "Optimistic but tight" is the absolute hardest part of Branch and Bound engineering.
"""

if __name__ == "__main__":
    demonstrate_architecture()
    print("\n[SUCCESS] Laboratory: Branch and Bound Architecture Completed.")
