"""
# ==============================================================================
# LABORATORY: FRACTIONAL KNAPSACK (GREEDY DENSITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've seen the 0/1 Knapsack Problem solved with a 2D Dynamic Programming grid.
# In 0/1 Knapsack, you CANNOT break items apart. You either steal the whole TV, 
# or you leave it.
#
# But what if you are stealing Gold Dust, Silver Flakes, and Platinum Sand?
# You CAN break these items apart. If your bag only has 2 lbs of free space, 
# you can scoop exactly 2 lbs of Gold Dust into it!
#
# This is the "Fractional Knapsack" problem.
# Because the physical restriction of "wasted space" is completely eliminated, 
# Dynamic Programming is massive overkill. 
# We can solve this with a pure, lightning-fast Greedy Algorithm in O(N log N) time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the "Value Density" (Value/Weight) greedy heuristic.
# - Implement fractional mathematical capacity calculations.
# - Solidify exactly WHY Greedy works here, but fails for 0/1 Knapsack.
#
# ==============================================================================
"""

from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GREEDY DENSITY ALGORITHM
# ==============================================================================
class Item:
    def __init__(self, name: str, value: float, weight: float):
        self.name = name
        self.value = value
        self.weight = weight
        # 1. THE GREEDY HEURISTIC: VALUE DENSITY
        # This is the "Price per Pound".
        self.density = value / weight


def fractional_knapsack(capacity: float, items: List[Item]) -> float:
    """
    Time Complexity: O(N log N) (Due to sorting).
    Space Complexity: O(1) auxiliary (assuming in-place sort).
    """
    
    # 2. SORT BY DENSITY (DESCENDING)
    # We greedily want to shove the most valuable material per pound into the bag first!
    items.sort(key=lambda x: x.density, reverse=True)
    
    total_profit = 0.0
    current_capacity = capacity
    
    # 3. THE GREEDY LOOP
    for item in items:
        # If the bag is full, we can immediately terminate!
        if current_capacity <= 0:
            break
            
        # Scenario A: The item fits COMPLETELY inside the bag.
        if item.weight <= current_capacity:
            # We take the whole thing!
            total_profit += item.value
            current_capacity -= item.weight
            print(f" -> Took 100% of {item.name}. Remaining Capacity: {current_capacity}")
            
        # Scenario B: The item is too heavy. It only PARTIALLY fits.
        else:
            # This is the defining feature of the Fractional Knapsack.
            # We figure out exactly what fraction of the item we can take.
            fraction_taken = current_capacity / item.weight
            
            # Add that exact fractional value to our profit
            fractional_value = item.value * fraction_taken
            total_profit += fractional_value
            
            print(f" -> Took {fraction_taken*100:.1f}% of {item.name}. Remaining Capacity: 0.0")
            
            # The bag is now guaranteed to be 100.00% full.
            current_capacity = 0
            break
            
    return total_profit


def demonstrate_fractional_knapsack():
    section_header("Algorithm: Fractional Knapsack")
    
    capacity = 50.0
    
    # (Name, Value, Weight)
    items_data = [
        ("Gold Dust", 60.0, 10.0),      # Density: $6/lb
        ("Silver Flakes", 100.0, 20.0), # Density: $5/lb
        ("Platinum Sand", 120.0, 30.0)  # Density: $4/lb
    ]
    
    items = [Item(name, v, w) for name, v, w in items_data]
    
    print(f"Backpack Capacity: {capacity} lbs\n")
    print("Items Available:")
    for item in items:
        print(f" - {item.name}: Weight={item.weight}lbs, Value=${item.value} (Density: ${item.density}/lb)")
        
    print("\nExecuting Greedy Density Algorithm...")
    ans = fractional_knapsack(capacity, items)
    
    print(f"\nTotal Maximum Profit: ${ans:.2f} (Expected: $240.00)")
    
    print("\nCompare this to 0/1 Knapsack!")
    print("If we could NOT break the items (0/1 Knapsack), the optimal choice")
    print("is to skip Gold entirely, and just take Silver(20) + Platinum(30).")
    print("That perfectly fills 50lbs, yielding $220.00.")
    print("But because we CAN break items, the Greedy algorithm gets $240.00!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does the Greedy Density heuristic fail for the 0/1 Knapsack problem?
   Answer: In 0/1 Knapsack, picking a high-density item might leave "wasted space" in the bag that cannot be filled by anything else. For example, a bag holds 50 lbs. Item A is 10 lbs ($60, density 6). Item B is 20 lbs ($100, density 5). Item C is 30 lbs ($120, density 4). Greedy picks A(10) and B(20). Remaining capacity is 20. C(30) doesn't fit! The bag has 20 lbs of empty, wasted space, yielding $160. But skipping A(10) allows B(20)+C(30) to fit perfectly, leaving 0 wasted space and yielding $220.

2. Does Fractional Knapsack always perfectly fill the bag to 100% capacity?
   Answer: Yes, assuming the total physical weight of all available items is greater than or equal to the bag's capacity. The algorithm will never leave wasted space.

3. Is it possible to solve Fractional Knapsack in $O(N)$ time instead of $O(N \\log N)$?
   Answer: Surprisingly, YES! In advanced theory, instead of doing a full $O(N \\log N)$ sort, you can use a "Selection Algorithm" (like Quickselect) to find the median density element in $O(N)$ time. You can aggressively partition the array, mathematically determining which half of the items fit into the bag without ever fully sorting them! But in real interviews, the $O(N \\log N)$ `.sort()` is the expected optimal answer.
"""

if __name__ == "__main__":
    demonstrate_fractional_knapsack()
    print("\n[SUCCESS] Laboratory: Fractional Knapsack Completed.")
