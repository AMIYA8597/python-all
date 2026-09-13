"""
# ==============================================================================
# LABORATORY: CONVEX HULL TRICK (CHT) & LINEAR ENVELOPES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The "Convex Hull Trick" (CHT) is one of the most advanced Dynamic Programming 
# optimizations, typically only seen in competitive programming (Codeforces, ICPC) 
# and hyper-optimized financial engines.
#
# Suppose your DP state transition equation looks like this:
# dp[i] = min( dp[j] + M_j * X_i ) for all j < i
#
# A naive loop takes O(N^2) time.
# But look closely at the math inside the `min()` function. 
# It is the equation of a line: y = m*x + c
# Where `m` (Slope) = M_j
# Where `x` (Variable) = X_i
# Where `c` (Y-Intercept) = dp[j]
#
# Every previous state `j` is physically representing a straight Line on a graph!
# If you draw 100 straight lines on a graph, and you want to find the MINIMUM 
# `y` value for a given `x`, you don't need to check all 100 lines. You only 
# care about the lines that form the "Lower Envelope" (the mathematical boundary 
# at the bottom of the graph). This boundary is a Convex Hull!
#
# By maintaining this Convex Hull of lines using a Monotonic Double-Ended Queue 
# (Deque), we can instantly query the optimal line in O(1) time, shattering the 
# O(N^2) limit and dropping the algorithm to O(N)!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Recognize the `y = mx + c` pattern in DP equations.
# - Understand the intersection of two lines.
# - Maintain a Lower Envelope (Convex Hull) using a Monotonic Deque.
#
# ==============================================================================
"""

from collections import deque
from typing import List, Tuple

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CONVEX HULL ENGINE
# ==============================================================================
class ConvexHullTrick:
    def __init__(self):
        # Stores tuples of (slope `m`, intercept `c`)
        # We maintain a Deque so we can prune useless lines from both the 
        # front (for querying) and the back (for inserting).
        self.hull = deque()
        
    def _intersection_x(self, line1: Tuple[float, float], line2: Tuple[float, float]) -> float:
        """
        Given y1 = m1*x + c1 and y2 = m2*x + c2
        They intersect when y1 = y2.
        m1*x + c1 = m2*x + c2
        x = (c2 - c1) / (m1 - m2)
        """
        m1, c1 = line1
        m2, c2 = line2
        
        # If slopes are parallel, intersection is at infinity (or handled by pruning)
        if m1 == m2:
            return float('-inf') if c1 < c2 else float('inf')
            
        return (c2 - c1) / (m1 - m2)
        
    def add_line(self, m: float, c: float):
        """
        Add a new line y = m*x + c to the Hull.
        We assume lines are added in strictly DECREASING order of slope `m`.
        (This is a requirement for the standard O(N) CHT deque).
        """
        line3 = (m, c)
        
        # We need at least 2 lines in the hull to check if the new line makes 
        # the previous line obsolete.
        while len(self.hull) >= 2:
            line2 = self.hull[-1]
            line1 = self.hull[-2]
            
            # Line 2 becomes completely obsolete (swallowed by the envelope) IF:
            # The X-intersection of Line 1 and Line 3 occurs BEFORE the 
            # X-intersection of Line 1 and Line 2.
            x13 = self._intersection_x(line1, line3)
            x12 = self._intersection_x(line1, line2)
            
            if x13 <= x12:
                # Line 2 is useless. Pop it from the back!
                self.hull.pop()
            else:
                # The hull remains strictly convex. Stop pruning.
                break
                
        self.hull.append(line3)

    def query(self, x: float) -> float:
        """
        Find the minimum y value for a given x.
        We assume queries `x` are strictly INCREASING.
        (This allows us to prune from the front of the Deque in O(1) time).
        """
        # If the intersection of the first two lines occurs BEFORE our target `x`, 
        # it means the first line is now higher than the second line for all 
        # future queries. The first line is completely obsolete!
        while len(self.hull) >= 2:
            line1 = self.hull[0]
            line2 = self.hull[1]
            
            x12 = self._intersection_x(line1, line2)
            
            if x12 <= x:
                # Line 1 is dead. Pop it from the front!
                self.hull.popleft()
            else:
                break
                
        # The line at the front of the deque is guaranteed to be optimal for `x`!
        best_m, best_c = self.hull[0]
        return best_m * x + best_c


# ==============================================================================
# 4. DP APPLICATION
# ==============================================================================
def demonstrate_cht():
    section_header("Algorithm: Convex Hull Trick (Lower Envelope)")
    
    print("Simulating a DP Equation: dp[i] = min(dp[j] + M[j] * X[i])")
    
    cht = ConvexHullTrick()
    
    # Adding lines in strictly decreasing order of slope (M[j]).
    print("\nAdding Lines (Previous DP States):")
    
    print("1. y = -2x + 10")
    cht.add_line(-2, 10)
    
    print("2. y = -4x + 20")
    cht.add_line(-4, 20)
    
    print("3. y = -6x + 35")
    cht.add_line(-6, 35)
    
    print("\nQuerying strictly increasing X values (X[i]):")
    
    x_queries = [1, 2, 4, 8, 10]
    for x in x_queries:
        best_y = cht.query(x)
        print(f" Query X = {x:2d} -> Optimal Minimum Y = {best_y}")
        
    print("\nWithout CHT, answering Q queries for N lines takes O(Q * N).")
    print("With CHT, because we use a Monotonic Deque, it is O(Q + N)!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must the slopes ($m$) be added in strictly decreasing order?
   Answer: Because we are building the "Lower Envelope" from left to right. If the slopes are randomly ordered, adding a line in the middle of the envelope requires an $O(\\log N)$ Binary Search to find its insertion point, and we must use a complex self-balancing Red-Black Tree (Li-Chao Tree) instead of a simple $O(1)$ Deque.

2. Why do we pop lines from the FRONT of the queue during `query(x)`?
   Answer: We assume the queries `x` are strictly increasing (moving right across the graph). As we move right, the steep lines that were optimal on the left side of the graph become permanently suboptimal compared to flatter lines. By popping them, we instantly retrieve the new optimal line in $O(1)$ amortized time without having to scan the whole array.

3. Is CHT common in standard FAANG interviews?
   Answer: NO. The Convex Hull Trick is mathematical overkill for 99% of Software Engineering roles. It is usually reserved for highly specialized Quantitative Trading interviews (where optimizing mathematical models from $O(N^2)$ to $O(N)$ saves millions of dollars in latency) or Competitive Programming grandmasters.
"""

if __name__ == "__main__":
    demonstrate_cht()
    print("\n[SUCCESS] Laboratory: Convex Hull Trick Completed.")
