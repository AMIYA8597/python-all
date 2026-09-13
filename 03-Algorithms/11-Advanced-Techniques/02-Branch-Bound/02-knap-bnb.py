"""
# ==============================================================================
# LABORATORY: BRANCH AND BOUND (0/1 KNAPSACK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that the 0/1 Knapsack problem is solved using Dynamic Programming 
# in $O(N \times W)$ time.
# 
# But what if a problem gives you $N=100$ items, and a Knapsack Capacity of 
# $W=1,000,000,000$ (One Billion)? 
# 
# DP will allocate a 2D array of size $100 \times 1,000,000,000$. That requires 
# 400 Gigabytes of RAM. Your computer instantly crashes. DP is a "Pseudo-Polynomial" 
# algorithm; it is completely destroyed by massive weights!
#
# Solution: Branch and Bound using Fractional Relaxation!
# We view this as a Backtracking tree (Include Item / Exclude Item).
# To prune terrible branches, we need a Mathematical Upper Bound: "Assuming a 
# miracle, what is the MAXIMUM possible profit I can make if I continue down this path?"
#
# How do we calculate the best-case miracle? We RELAX the rules!
# The 0/1 Knapsack forbids taking fractions of items. But the Fractional Knapsack 
# allows it, and can be solved instantly in $O(N)$ time using a Greedy approach 
# (taking items with the best Value/Weight ratio)!
# 
# At every node in our search tree, we calculate the Greedy Fractional Knapsack 
# on the REMAINING items. This gives an absolute mathematical ceiling. 
# If `current_profit + fractional_bound <= best_profit_so_far`, we PRUNE! 
# We just mathematically proved that even if we were allowed to break the rules 
# and take fractions, we STILL couldn't beat the current record!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Pseudo-Polynomial RAM limits.
# - Sort items by Density (Value / Weight).
# - Calculate Optimistic Bounds using Fractional Relaxation.
#
# ==============================================================================
"""

from typing import List, Tuple
from dataclasses import dataclass
from collections import deque

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BRANCH AND BOUND ENGINE (FRACTIONAL RELAXATION)
# ==============================================================================
@dataclass
class Item:
    weight: int
    value: int
    density: float # Value / Weight

@dataclass
class Node:
    level: int       # Index of the item we are currently considering
    profit: int      # Current accumulated profit
    weight: int      # Current accumulated weight
    bound: float     # The mathematical upper bound of this branch!


def get_optimistic_bound(u: Node, n: int, capacity: int, items: List[Item]) -> float:
    """
    Calculates the Fractional Knapsack mathematical ceiling from this node onward.
    Assumes `items` is already sorted by density (Highest to Lowest).
    """
    # If this specific node already exceeded the knapsack capacity, it's invalid!
    if u.weight >= capacity:
        return 0.0
        
    profit_bound = float(u.profit)
    current_weight = u.weight
    
    # We greedily pack the REMAINING items (from level + 1 onwards)
    j = u.level + 1
    while j < n and current_weight + items[j].weight <= capacity:
        current_weight += items[j].weight
        profit_bound += items[j].value
        j += 1
        
    # If the knapsack is STILL not full, and there is an item left, we RELAX 
    # the 0/1 integer constraint and pack a FRACTION of it to fill the exact remainder!
    if j < n:
        remaining_capacity = capacity - current_weight
        # We add the fractional value
        profit_bound += remaining_capacity * items[j].density
        
    return profit_bound


def knapsack_branch_and_bound(capacity: int, weights: List[int], values: List[int]) -> int:
    """
    Solves the 0/1 Knapsack problem using Branch and Bound (BFS Queue approach).
    Immune to massive capacities that would crash Dynamic Programming.
    """
    n = len(weights)
    
    # 1. PRE-COMPUTATION
    # We MUST sort the items by Value/Weight density (Highest First).
    # This guarantees our Greedy Fractional Bound calculation is mathematically accurate!
    items = []
    for i in range(n):
        items.append(Item(weights[i], values[i], values[i] / weights[i]))
        
    items.sort(key=lambda x: x.density, reverse=True)
    
    # 2. QUEUE INITIALIZATION (Breadth-First Search)
    queue = deque()
    
    # Dummy root node starts at level -1 (before considering item 0)
    v = Node(level=-1, profit=0, weight=0, bound=0.0)
    queue.append(v)
    
    max_profit = 0
    
    # Performance trackers
    nodes_explored = 0
    branches_pruned = 0
    
    # 3. BFS SEARCH
    while queue:
        nodes_explored += 1
        u = queue.popleft()
        
        # If we reached the final item, there's nothing left to branch!
        if u.level == n - 1:
            continue
            
        # Optimization: We already calculated the Bound when we generated this node.
        # If a better global `max_profit` was discovered while this node was waiting 
        # in the queue, we can prune it instantly!
        if u.bound <= max_profit:
            branches_pruned += 1
            continue
            
        # ==========================================
        # BRANCH 1: INCLUDE the next item
        # ==========================================
        next_level = u.level + 1
        next_item = items[next_level]
        
        include_node = Node(
            level=next_level,
            profit=u.profit + next_item.value,
            weight=u.weight + next_item.weight,
            bound=0.0
        )
        
        # If valid, update global max!
        if include_node.weight <= capacity and include_node.profit > max_profit:
            max_profit = include_node.profit
            
        # Calculate the mathematical bound for the INCLUDE branch!
        include_node.bound = get_optimistic_bound(include_node, n, capacity, items)
        
        # PRUNING CHECK
        if include_node.bound > max_profit:
            queue.append(include_node)
        else:
            branches_pruned += 1
            
        # ==========================================
        # BRANCH 2: EXCLUDE the next item
        # ==========================================
        exclude_node = Node(
            level=next_level,
            profit=u.profit,     # No extra profit
            weight=u.weight,     # No extra weight
            bound=0.0
        )
        
        # Calculate the mathematical bound for the EXCLUDE branch!
        exclude_node.bound = get_optimistic_bound(exclude_node, n, capacity, items)
        
        # PRUNING CHECK
        if exclude_node.bound > max_profit:
            queue.append(exclude_node)
        else:
            branches_pruned += 1
            
    print(f"[Performance] Explored: {nodes_explored}, Pruned: {branches_pruned}")
    return max_profit


def demonstrate_knapsack_bnb():
    section_header("Algorithm: Branch and Bound (0/1 Knapsack)")
    
    # 4 Items
    weights = [2, 4, 6, 9]
    values = [10, 10, 12, 18]
    capacity = 15
    
    print(f"Knapsack Capacity: {capacity}")
    print("Items (Weight, Value):")
    for w, v in zip(weights, values):
        print(f" - W: {w:2d} | V: {v:2d} | Density: {v/w:.2f}")
        
    print("\nExecuting Branch and Bound...")
    profit = knapsack_branch_and_bound(capacity, weights, values)
    
    print(f"\nAbsolute Maximum Profit: {profit}")
    print("Expected: 38 (Items: [2, 10], [4, 10], [9, 18]. Total W: 15, Total V: 38)")
    
    section_header("The Danger of Dynamic Programming")
    print("If you were given W = 1,000,000,000, Dynamic Programming would crash ")
    print("your computer trying to allocate a massive 2D array.")
    print("Branch and Bound solves it effortlessly because it operates strictly on ")
    print("the physical count of N items, regardless of how massive the Weight is!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does DP fail when Knapsack Capacity $W$ is massive?
   Answer: Dynamic Programming relies on an array `dp[item_index][current_weight]`. It physically indexes the array using the integer value of the weight! If $W$ is 1 Billion, the array MUST be 1 Billion elements wide. This is called a "Pseudo-Polynomial" time complexity because the runtime scales linearly with the magnitude of the NUMBER, not the magnitude of the INPUT SIZE. It triggers Out-Of-Memory exceptions instantly.

2. What is "Fractional Relaxation"?
   Answer: To prune branches in a search tree, you need to calculate an upper bound. A strict 0/1 calculation is too slow. We mathematically "relax" the integer constraints of the problem, pretending we are allowed to take fractions of items (e.g., half a TV). The Greedy Fractional algorithm mathematically generates the absolute MAXIMUM possible ceiling of profit. Because it's impossible for the strict integer 0/1 problem to ever beat the relaxed fractional problem, we can safely use the fractional profit as our pruning bound!

3. Why MUST we sort the items by Value/Weight density first?
   Answer: If we don't sort by density, the Greedy Fractional calculation `get_optimistic_bound()` will be mathematically incorrect! The Fractional Knapsack algorithm is ONLY mathematically optimal if it consumes the most dense (most profitable per pound) items first. If the bound calculation is wrong (underestimating the true potential), the algorithm might accidentally prune the branch containing the correct answer, completely destroying the reliability of the Branch and Bound search.
"""

if __name__ == "__main__":
    demonstrate_knapsack_bnb()
    print("\n[SUCCESS] Laboratory: Knapsack Branch & Bound Completed.")
