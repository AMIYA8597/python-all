"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING GREEDY (THE GAS STATION TRICK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In Competitive Programming (Codeforces) and FAANG interviews, there is a class 
# of Greedy problems that seem to require O(N^2) time, but can be mathematically 
# collapsed into O(N) time by exploiting a single, brilliant "Greedy Invariant".
#
# Classic Problem: The Circular Gas Station.
# You are driving on a circular highway with N gas stations.
# You have an array `gas` representing how much gas you get at station i.
# You have an array `cost` representing the gas needed to drive from i to i+1.
# Can you complete the entire circle? If so, what is the starting station?
#
# Naive approach: Try starting at Station 0, simulate the circle. If you fail 
# at Station 4, try starting at Station 1... then Station 2... (Time: O(N^2)).
#
# The Greedy Invariant Trick:
# If you started at Station 0 and successfully drove to Station 4, but your tank 
# went negative trying to reach Station 5... 
# IT IS MATHEMATICALLY IMPOSSIBLE TO REACH STATION 5 BY STARTING AT 1, 2, 3, or 4!
# Why? Because starting at 0 gave you a "head start" (a positive tank) when you 
# passed through 1, 2, and 3. If even WITH a head start you couldn't reach 5, 
# starting at 1 with an empty tank will absolutely fail.
#
# Therefore, you instantly SKIP to Station 5 as your new starting point!
# This single realization drops the algorithm from O(N^2) to a single O(N) pass.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Identify Greedy Invariants in O(N^2) simulation loops.
# - Understand the "Telescoping Failure" principle.
# - Implement the O(N) Gas Station algorithm.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GREEDY SKIP ALGORITHM (O(N))
# ==============================================================================
def can_complete_circuit(gas: List[int], cost: List[int]) -> int:
    """
    Time Complexity: O(N) (Exactly one pass).
    Space Complexity: O(1).
    """
    
    # 1. THE GLOBAL CHECK
    # If the total gas available across the entire circle is LESS than the total 
    # cost to drive the entire circle, it is mathematically impossible to complete 
    # the journey, regardless of where you start!
    if sum(gas) < sum(cost):
        return -1
        
    # If total_gas >= total_cost, a valid starting station is mathematically 
    # GUARANTEED to exist (proven by the Circular Graph theorem).
    
    current_tank = 0
    start_station = 0
    
    # 2. THE GREEDY LOOP
    for i in range(len(gas)):
        # Calculate the net change in our tank for this segment
        net_gas = gas[i] - cost[i]
        
        current_tank += net_gas
        
        # --- THE GREEDY INVARIANT TRIGGER ---
        # If our tank goes negative, we failed to reach the next station.
        if current_tank < 0:
            print(f" -> Started at {start_station}, failed at {i}. Tank went negative!")
            print(f"    (Skipping all stations between {start_station} and {i}...)")
            
            # The brilliant leap: If we started at `start_station` and failed at `i`, 
            # EVERY station between them is fundamentally flawed.
            # The earliest possible station that MIGHT work is the very next one!
            start_station = i + 1
            
            # Reset our tank for the new attempt!
            current_tank = 0
            
    # Because of the Global Check at the top, if we make it through the loop 
    # and lock in a `start_station`, it is guaranteed to be correct!
    return start_station


def demonstrate_gas_station():
    section_header("Algorithm: The Circular Gas Station")
    
    gas  = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    
    print(f"Gas available at stations: {gas}")
    print(f"Cost to drive to next  : {cost}\n")
    
    print("Executing O(N) Greedy Skip Algorithm...")
    start_index = can_complete_circuit(gas, cost)
    
    print(f"\nOptimal Starting Station: Index {start_index} (Expected: 3)")
    print("Proof:")
    print("Start at 3: Tank = 4 - 1 = 3")
    print("Drive to 4: Tank = 3 + 5 - 2 = 6")
    print("Drive to 0: Tank = 6 + 1 - 3 = 4")
    print("Drive to 1: Tank = 4 + 2 - 4 = 2")
    print("Drive to 2: Tank = 2 + 3 - 5 = 0. Circle complete!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `sum(gas) < sum(cost)` mathematically necessary?
   Answer: It acts as the absolute boundary condition. If the total energy in a closed physical system is less than the total energy required to traverse it, no routing magic can change the laws of physics. If we didn't check this first, the `start_station = i + 1` logic would blindly return an invalid station if no valid path existed.

2. Explain the "Telescoping Failure" proof exactly. Why can't we start at a station in the middle of a failed route?
   Answer: Let $T[i]$ be the gas tank. If we start at A, then $T[A] \\ge 0$. As we drive to B, the tank remains $\\ge 0$. If we fail arriving at C, it means $T[C] < 0$. If we had started at B instead, we wouldn't have the positive gas leftover from A. Our tank at C would be strictly worse (even more negative)! Therefore, no node between A and C can ever reach C.

3. How does this apply to other Competitive Programming problems?
   Answer: This "Greedy Skip" logic is identical to Kadane's Algorithm for Maximum Subarray Sum! In Kadane's, you maintain a running sum. If the sum drops below 0, you instantly throw the entire prefix away and start a brand new subarray at $i+1$, because a negative prefix can never contribute to a positive future. It's the exact same mathematical invariant!
"""

if __name__ == "__main__":
    demonstrate_gas_station()
    print("\n[SUCCESS] Laboratory: CP Greedy Tricks Completed.")
