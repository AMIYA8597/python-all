"""
# ==============================================================================
# LABORATORY: BELLMAN-FORD APPLICATIONS (ARBITRAGE & K-STOPS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You already know that Bellman-Ford handles negative weights and detects negative 
# cycles in O(V * E) time. 
# But did you know this algorithm is used by High-Frequency Traders to make 
# infinite money on Wall Street? By converting currency exchange rates into 
# negative logarithms, a Negative Cycle becomes an "Arbitrage Opportunity" 
# (e.g., converting USD -> EUR -> JPY -> USD and ending up with MORE USD than 
# you started with).
#
# Furthermore, Bellman-Ford has a unique property: after `K` iterations, it has 
# mathematically found the shortest paths using AT MOST `K` edges! This makes 
# it the perfect algorithm for routing problems with strict stop limits 
# (e.g., LeetCode #787: Cheapest Flights Within K Stops).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Model Currency Arbitrage as a Bellman-Ford Negative Cycle problem.
# - Solve "Cheapest Flights Within K Stops" by limiting Bellman-Ford iterations.
#
# ==============================================================================
"""

import math
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CURRENCY ARBITRAGE (NEGATIVE CYCLE DETECTION)
# ==============================================================================
def detect_arbitrage(currencies: List[str], rates: List[Tuple[int, int, float]]) -> bool:
    """
    Detects if an arbitrage opportunity exists.
    
    The Math:
    If we want to multiply rates: R1 * R2 * R3 > 1.0 (Profit!)
    We can take the negative log of both sides:
      -log(R1 * R2 * R3) < -log(1.0)
      -log(R1) + -log(R2) + -log(R3) < 0
      
    This means if we set the edge weights to -log(rate), a profitable sequence of 
    trades is mathematically identical to a Negative Weight Cycle!
    """
    num_currencies = len(currencies)
    # 1. Convert rates to negative logs
    edges = []
    for u, v, rate in rates:
        weight = -math.log(rate)
        edges.append((u, v, weight))
        
    # 2. Run Bellman-Ford
    # We initialize distances to 0. We don't care about reaching a specific node, 
    # we just want to find any negative cycle.
    dist = [0.0] * num_currencies
    
    # Relax V - 1 times
    for _ in range(num_currencies - 1):
        for u, v, weight in edges:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                
    # 3. The V-th Relaxation (Check for Negative Cycle)
    for u, v, weight in edges:
        if dist[u] + weight < dist[v] - 1e-9: # Floating point tolerance
            return True # Arbitrage found!
            
    return False

def demonstrate_arbitrage():
    section_header("Application: High-Frequency Trading (Arbitrage)")
    
    currencies = ["USD", "EUR", "GBP"]
    
    # Rates:
    # 1 USD = 0.90 EUR
    # 1 EUR = 0.85 GBP
    # 1 GBP = 1.35 USD
    
    rates = [
        (0, 1, 0.90), # USD to EUR
        (1, 2, 0.85), # EUR to GBP
        (2, 0, 1.35)  # GBP to USD
    ]
    
    print("Exchange Rates:")
    print(" 1 USD -> 0.90 EUR")
    print(" 1 EUR -> 0.85 GBP")
    print(" 1 GBP -> 1.35 USD")
    
    print("\nIf I start with 100 USD:")
    print(" 100 * 0.90 = 90 EUR")
    print(" 90 * 0.85 = 76.5 GBP")
    print(" 76.5 * 1.35 = 103.275 USD")
    print("I made $3.27 profit for free! This is a cycle > 1.0.")
    
    print("\nRunning Bellman-Ford with -log() weights...")
    has_arbitrage = detect_arbitrage(currencies, rates)
    print(f"Arbitrage Detected: {has_arbitrage}")


# ==============================================================================
# 4. CHEAPEST FLIGHTS WITHIN K STOPS
# ==============================================================================
def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    """
    LeetCode #787: Cheapest Flights Within K Stops
    If K = 1, it means we can take at most 1 layover (which equals 2 edges).
    Therefore, we only run the Bellman-Ford outer loop exactly K + 1 times!
    """
    # Initialize distances to infinity
    prices = [float('inf')] * n
    prices[src] = 0
    
    # Run Bellman-Ford for exactly K + 1 iterations
    for _ in range(k + 1):
        # We MUST create a temporary copy of the prices array for this iteration.
        # Why? If we update `prices` in-place, a single iteration might traverse 
        # 3 edges simultaneously (A->B->C->D) if they happen to be processed in that 
        # exact order. We strictly want to simulate exactly 1 edge jump per iteration.
        temp_prices = prices.copy()
        
        for u, v, price in flights:
            if prices[u] == float('inf'):
                continue
            
            if prices[u] + price < temp_prices[v]:
                temp_prices[v] = prices[u] + price
                
        # Commit the changes for this iteration
        prices = temp_prices
        
    return prices[dst] if prices[dst] != float('inf') else -1

def demonstrate_k_stops():
    section_header("Application: Cheapest Flights Within K Stops")
    
    # 0 --(100)--> 1 --(100)--> 2 --(100)--> 3
    # |                                      ^
    # +-----------------(500)----------------+
    # 0 to 3 direct costs 500 (1 edge).
    # 0 to 1 to 2 to 3 costs 300 (3 edges, 2 stops).
    
    n = 4
    flights = [
        [0, 1, 100],
        [1, 2, 100],
        [2, 3, 100],
        [0, 3, 500]
    ]
    
    src, dst = 0, 3
    
    print("Flights Network:")
    print(" 0 -> 1 ($100), 1 -> 2 ($100), 2 -> 3 ($100)")
    print(" 0 -> 3 direct ($500)")
    
    # Scenario 1: K = 0 (Direct flights only)
    cost_0_stops = find_cheapest_price(n, flights, src, dst, 0)
    print(f"\nCheapest Flight with max 0 stops: ${cost_0_stops} (Expected: 500)")
    
    # Scenario 2: K = 1 (Max 1 stop)
    cost_1_stops = find_cheapest_price(n, flights, src, dst, 1)
    print(f"Cheapest Flight with max 1 stop: ${cost_1_stops} (Expected: 500, because 0->1->2->3 is 2 stops)")
    
    # Scenario 3: K = 2 (Max 2 stops)
    cost_2_stops = find_cheapest_price(n, flights, src, dst, 2)
    print(f"Cheapest Flight with max 2 stops: ${cost_2_stops} (Expected: 300, via 0->1->2->3)")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Bellman-Ford naturally solve the "At Most K Edges" problem?
   Answer: The outer loop of Bellman-Ford conceptually represents the maximum number of edges in the path. After 1 iteration, it finds all shortest paths using exactly 1 edge. After 2 iterations, it finds paths using at most 2 edges. If we artificially stop the loop at K + 1 iterations, it guarantees the path uses at most K stops.

2. In the K Stops algorithm, why do we use a `temp_prices` array instead of updating `prices` directly?
   Answer: If we process edge A->B and update B's distance, and then in the VERY SAME iteration we process edge B->C and update C's distance based on B's new value, we just traversed TWO edges in a single iteration. `temp_prices` ensures that iteration `i` only computes distances using the finalized values from iteration `i-1`.

3. How does `-log(x)` turn arbitrage into a shortest-path problem?
   Answer: Shortest path algorithms ADD weights (`dist = A + B`). But probabilities and exchange rates MULTIPLY (`profit = A * B`). The mathematical rule of logarithms states that `log(A * B) = log(A) + log(B)`. By taking the negative log, we convert multiplication into addition, and we convert profit (maximizing > 1) into a negative cycle (minimizing < 0).
"""

if __name__ == "__main__":
    demonstrate_arbitrage()
    demonstrate_k_stops()
    print("\n[SUCCESS] Laboratory: Bellman-Ford Applications Completed.")
