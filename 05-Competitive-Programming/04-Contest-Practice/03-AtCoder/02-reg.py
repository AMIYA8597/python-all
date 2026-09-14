"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ATCODER REGULAR CONTEST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# AtCoder Regular Contests (ARC) are notorious for mathematically subverting 
# your expectations. 
# 
# A standard 0/1 Knapsack problem gives you 100 items. The maximum weight of 
# the backpack (W) is 100,000. 
# You write the standard DP: `dp[W]`. Time Complexity: O(N * W). 
# 100 * 100,000 = 10 Million operations. It passes flawlessly.
#
# Then AtCoder hands you "Knapsack 2" (Educational DP Contest E).
# N is still 100. But the maximum weight of the backpack (W) is now $10^9$!
# 
# If you create an array of size $10^9$, your code will instantly crash with a 
# Memory Limit Exceeded (MLE). If you run $100 \times 10^9$ operations, you 
# get a Time Limit Exceeded (TLE).
#
# You CANNOT iterate over the weights. You must perform an "Inverted State" DP.
# Instead of `dp[Weight] = Max_Value`, you flip the entire mathematical universe!
# You track `dp[Value] = Min_Weight`. Since the maximum value in AtCoder is 
# kept deliberately small ($10^5$), you loop over the VALUES, completely 
# dodging the $10^9$ weight limit!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Inverted State Dynamic Programming.
# - Solve AtCoder DP Contest E (Knapsack 2).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. ATCODER DP CONTEST E: KNAPSACK 2 (INVERTED STATE)
# ==============================================================================
def knapsack_inverted_state(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Solves 0/1 Knapsack when Capacity (W) is massive (e.g., 10^9), 
    but the maximum possible Value (V) is small (e.g., 10^5).
    
    Standard DP: dp[weight] = max(value)
    Inverted DP: dp[value]  = min(weight)
    
    Time Complexity: O(N * Max_Total_Value)
    Space Complexity: O(Max_Total_Value)
    """
    n = len(weights)
    
    # Calculate the absolute maximum value we could physically achieve if we 
    # took every single item in the entire list!
    max_total_value = sum(values)
    
    # dp[v] will store the MINIMUM physical weight required to exactly achieve value `v`.
    # Because we are searching for a minimum, initialize with Infinity!
    dp = [float('inf')] * (max_total_value + 1)
    
    # Base Case: It takes 0 weight to achieve 0 value.
    dp[0] = 0
    
    # Iterate through every item...
    for i in range(n):
        w = weights[i]
        v = values[i]
        
        # We MUST iterate backwards through the values!
        # (Exact same logic as standard 0/1 Knapsack to avoid reusing the same item).
        for current_val in range(max_total_value, v - 1, -1):
            
            # The Inverted State Transition Equation:
            # We either DO NOT take the item (keep the current minimum weight),
            # OR we DO take the item (the weight of this item + the minimum weight 
            # required to achieve the leftover value!).
            dp[current_val] = min(
                dp[current_val], 
                w + dp[current_val - v]
            )
            
    # The DP array is fully populated!
    # Now, we simply scan the array from the HIGHEST value downwards.
    # The very first value we find whose required weight is <= our Backpack Capacity 
    # is mathematically guaranteed to be our optimal answer!
    for v in range(max_total_value, -1, -1):
        if dp[v] <= capacity:
            return v
            
    return 0

def demonstrate_knapsack_inverted():
    section_header("AtCoder DP Contest (Knapsack 2)")
    
    # Notice the weights are massive! (Billion scale)
    weights = [100000000, 500000000, 400000000]
    values = [30, 50, 40] # But the values are small!
    capacity = 500000000
    
    print(f"Item Weights: {weights}")
    print(f"Item Values : {values}")
    print(f"Backpack Cap: {capacity}")
    
    print("\nIf you used standard DP, `dp = [0] * 500000000` would allocate ")
    print("4 GB of RAM and crash instantly.")
    
    ans = knapsack_inverted_state(weights, values, capacity)
    
    print(f"\nMaximum Value Achieved: {ans}")
    print("Why? Item 0 (Weight 100M, Val 30) + Item 2 (Weight 400M, Val 40)")
    print("Total Weight = 500M. Total Value = 70.")
    print("The DP Array size was only 121 (Sum of Values)! RAM usage was virtually zero!")


def run_all_labs():
    demonstrate_knapsack_inverted()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the philosophical shift between Standard DP and Inverted DP for the Knapsack problem.
   Answer: In Standard DP, the Independent Variable (the array index) is the Weight, and the Dependent Variable (the array value) is the Value. You ask: "For exactly 50kg, what is the maximum dollars I can cram inside?" In Inverted DP, you swap the variables. The Independent Variable is the Dollars, and the Dependent Variable is the Weight. You ask: "If I strictly want exactly 100 dollars, what is the absolute lightest possible combination of items I need to carry?" By swapping the question, you mathematically dodge whichever variable constraint is dangerously large ($10^9$) and loop over the variable that is safely small ($10^5$).

2. Why is the Inverted DP array initialized with `float('inf')`, whereas the Standard DP array is initialized with `0`?
   Answer: It directly mirrors the Dependent Variable! In Standard DP, the value inside the array is `Dollars`. You are trying to maximize your profit. Therefore, the default state is having 0 dollars. If you initialize with `0`, the `max()` function will gladly accept higher numbers. In Inverted DP, the value inside the array is `Physical Weight`. You are trying to carry as little weight as mathematically possible. If you initialized the array with `0`, the `min()` function would see `0` weight and say, "Wow, 0 kg! That's the best!" and never update. By initializing with mathematical Infinity, the first valid weight evaluated (e.g., 50kg) will overwrite the infinity, correctly tracking the lightest load.

3. In the final phase of the Inverted Knapsack algorithm, why do we scan the array backwards `for v in range(max_total_value, -1, -1):` instead of just returning `dp[capacity]`?
   Answer: Because the array index is NO LONGER the capacity! The array index is the Value (`v`). The value stored inside `dp[v]` is the physical weight required to achieve that value. We do not care what the absolute maximum value is in a vacuum; we only care about the absolute maximum value we can *afford to carry*. By scanning from the absolute maximum possible value ($10^5$) downwards towards 0, we are testing the most lucrative outcomes first. The exact second we find a value whose required weight (`dp[v]`) is $\le$ our physical `capacity`, we have mathematically found the most profitable valid load! We return `v` and halt.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AtCoder Regular (Inverted DP) Completed.")
