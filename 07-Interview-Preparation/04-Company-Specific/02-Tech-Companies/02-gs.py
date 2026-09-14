"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (GOLDMAN SACHS PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Goldman Sachs interviews are extremely focused on Mathematics, dynamic array 
# boundary processing, and High-Frequency edge-case logic. Problems like 
# "Trapping Rain Water" or "Stock Buy/Sell" are practically guaranteed. 
#
# A junior engineer solves Trapping Rain Water using brute force: for every 
# index, scan the entire left array for the max wall, then the entire right 
# array. This takes O(N^2) and fails.
# 
# A senior engineer understands Mathematical Bottlenecks. The water level is 
# physically restricted by the shortest of the two maximum walls surrounding it. 
# By maintaining two pointers and dynamically tracking `left_max` and `right_max` 
# simultaneously, the entire calculation completes in a flawlessly optimized 
# O(N) Time and O(1) Space pass!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Trapping Rain Water Two-Pointer algorithm.
# - Master mathematical array boundaries and Bottleneck logic.
# - Understand the Stock Buy/Sell state machine.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRAPPING RAIN WATER (THE TWO-POINTER MASTERCLASS)
# ==============================================================================
def trap_water(height: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Given n non-negative integers representing an elevation map where the width 
    of each bar is 1, compute how much water it can trap after raining.
    """
    if not height: return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total_water = 0
    
    print("  Calculating trapped water...")
    
    while left < right:
        # THE MATHEMATICAL BOTTLENECK:
        # Water is strictly bottlenecked by the SHORTER of the two boundaries!
        # If left_max is strictly smaller than right_max, it doesn't matter how 
        # tall the right_max gets. The water will spill over the left wall!
        # Therefore, we can confidently calculate the water for the left pointer!
        if left_max < right_max:
            left += 1
            # Update the physical boundary
            left_max = max(left_max, height[left])
            # The water trapped is the difference between the boundary and the current height!
            water_trapped = left_max - height[left]
            total_water += water_trapped
            
            if water_trapped > 0:
                print(f"    -> Block [{left}] trapped {water_trapped} units of water.")
                
        # If right_max is shorter (or equal), we process from the right side!
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water_trapped = right_max - height[right]
            total_water += water_trapped
            
            if water_trapped > 0:
                print(f"    -> Block [{right}] trapped {water_trapped} units of water.")
                
    return total_water

def demonstrate_trap_water():
    section_header("Goldman Sachs: Trapping Rain Water (O(1) Space)")
    
    # Notice the "valleys" in the array!
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    print(f"Elevation Map: {height}\n")
    
    ans = trap_water(height)
    print(f"\nResult: Total Water Trapped = {ans} units.")


# ==============================================================================
# 4. BEST TIME TO BUY AND SELL STOCK (STATE MACHINE)
# ==============================================================================
def max_profit(prices: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Find the maximum profit you can achieve from ONE transaction.
    (Buy on one day, sell on a future day).
    """
    if not prices: return 0
    
    min_price_seen = prices[0]
    max_profit_seen = 0
    
    print(f"  Historical Prices: {prices}")
    
    for current_price in prices:
        # 1. Could we buy lower?
        if current_price < min_price_seen:
            min_price_seen = current_price
            print(f"    -> [NEW LOW] Buying stock at ${min_price_seen}")
            
        # 2. What if we sold today?
        current_profit = current_price - min_price_seen
        
        # 3. Is this the best trade we've ever made?
        if current_profit > max_profit_seen:
            max_profit_seen = current_profit
            print(f"    -> [NEW RECORD] Selling at ${current_price} yields ${max_profit_seen} profit!")
            
    return max_profit_seen

def demonstrate_stock_market():
    section_header("Goldman Sachs: Best Time to Buy and Sell Stock")
    
    prices = [7, 1, 5, 3, 6, 4]
    
    ans = max_profit(prices)
    print(f"\nResult: Absolute Maximum Profit = ${ans}")


def run_all_labs():
    demonstrate_trap_water()
    demonstrate_stock_market()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Trapping Rain Water problem, why don't we need to know the absolute maximum height of the entire array before calculating the water at index `i`?"
   Senior Answer: "Because of the mathematical properties of a bottleneck. If we are traversing from the left, and we have established a `left_max` of $5$, and we currently know our `right_max` is $10$, it physically does not matter if there is a massive wall of height $50,000$ hiding somewhere in the middle of the array! The water at the current left index is permanently constrained by the `left_max` of $5$. It will spill over the left side regardless of what lies to the right. This allows us to calculate the trapped water dynamically, strictly using the shorter of the two known global boundaries, crushing the complexity to a single $O(N)$ pass."

2. Interviewer: "In the Stock Market problem, why can't we just find the absolute Minimum price, then find the absolute Maximum price, and subtract them?"
   Senior Answer: "Because you cannot travel back in time. If the prices are `[100, 10, 5, 2]`, the absolute Max is $100$ and the absolute Min is $2$. If you subtract them, you get a profit of $98$. However, the $100$ occurred on Day 1, and the $2$ occurred on Day 4. To achieve that profit, you would have to buy on Day 4 and sell on Day 1, violating the strict chronological constraints of time. The algorithm MUST be a chronological State Machine that strictly updates the `min_price_seen` first, and only evaluates `current_price - min_price_seen` on the days *following* the purchase."

3. Interviewer: "How would you solve Trapping Rain Water if instead of a 1D array of bars, you were given a 2D matrix of elevations (Trapping Rain Water II)?"
   Senior Answer: "A 2D array cannot be solved with simple Two Pointers because water can spill out in 4 directions instead of 2. I would model the 2D matrix as a topological Graph and deploy a Min-Heap (Priority Queue). I would push the entire outer perimeter of the matrix into the Heap. The Heap acts as an intelligent BFS perimeter, systematically peeling inwards by always processing the absolute lowest boundary wall first. As it steps inward, any cell lower than the boundary traps water, and the boundary is updated to the maximum of itself and the new cell. This solves the 2D variant flawlessly in $O(R \\times C \\log(R \\times C))$ time."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Tech Companies Prep (Goldman Sachs) Completed.")
