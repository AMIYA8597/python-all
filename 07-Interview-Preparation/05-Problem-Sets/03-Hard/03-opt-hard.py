"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - OPTIMIZATION HARD)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Extreme optimization problems test your ability to transcend naive Dynamic 
# Programming arrays and invent state-tracking mechanisms that operate in 
# strict O(1) Space or leverage Monotonic Data Structures.
#
# A junior engineer solves "Trapping Rain Water" by creating two massive O(N) 
# arrays to pre-compute the maximum heights from the left and right.
#
# A senior engineer realizes that the physical properties of water allow you to 
# track boundaries dynamically using a Two-Pointer collapse. By tracking just 
# two variables (`max_left` and `max_right`), they compute the exact water 
# volume in a single O(N) pass with flawless O(1) memory complexity.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master O(1) Space Two-Pointer collapses (Trapping Rain Water).
# - Master the Monotonic Stack (Largest Rectangle in Histogram).
# - Master 2D Matrix DP for String Parsing (Regular Expression Matching).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TRAPPING RAIN WATER (O(1) TWO-POINTER COLLAPSE)
# ==============================================================================
def trap_rain_water(height: List[int]) -> int:
    """
    Time: O(N) | Space: O(1)
    Given n non-negative integers representing an elevation map where the width 
    of each bar is 1, compute how much water it can trap after raining.
    """
    if not height: return 0
    
    left, right = 0, len(height) - 1
    
    # We maintain the absolute highest wall we have encountered so far on both sides!
    max_left = height[left]
    max_right = height[right]
    
    water_trapped = 0
    
    print(f"  Elevation Map: {height}")
    print("  Deploying Dual-Pointer Water Simulation...")
    
    while left < right:
        # Physics Principle: Water is strictly bound by the SHORTEST of the two walls!
        # If the left wall is shorter, it is mathematically the bottleneck for the 
        # left side. We process the left pointer!
        if max_left < max_right:
            left += 1
            # Update the max wall height for the left side!
            max_left = max(max_left, height[left])
            
            # The water trapped directly above this specific index is exactly 
            # (max_left - height[left]). If it's 0, it means it's a solid block!
            delta = max_left - height[left]
            water_trapped += delta
            if delta > 0: print(f"    -> Trapped {delta} units at index {left}")
            
        # If the right wall is shorter (or equal), it is the bottleneck! 
        # Process the right pointer!
        else:
            right -= 1
            max_right = max(max_right, height[right])
            
            delta = max_right - height[right]
            water_trapped += delta
            if delta > 0: print(f"    -> Trapped {delta} units at index {right}")
            
    print(f"  [SUCCESS] Total Water Volume: {water_trapped}")
    return water_trapped

def demonstrate_rain_water():
    section_header("Hard: Trapping Rain Water (O(1) Space)")
    
    height = [0,1,0,2,1,0,1,3,2,1,2,1]
    ans = trap_rain_water(height)
    print(f"\nResult: {ans} (Expected: 6)")


# ==============================================================================
# 4. LARGEST RECTANGLE IN HISTOGRAM (THE MONOTONIC STACK)
# ==============================================================================
def largestRectangleArea(heights: List[int]) -> int:
    """
    Time: O(N) | Space: O(N)
    Find the area of the largest rectangle in the histogram.
    
    We use a Monotonic Stack! The stack strictly contains bars that are in 
    ASCENDING height order. If we encounter a shorter bar, the upward trend is broken, 
    and we mathematically resolve all previous taller bars!
    """
    # Push a Tuple: (Index, Height)
    stack = []
    max_area = 0
    
    print(f"  Histogram: {heights}")
    
    for i, h in enumerate(heights):
        # We assume this current bar starts exactly at its own index.
        start_idx = i
        
        # TREND BREAKER!
        # If the current bar is SHORTER than the top of the stack, the taller bars 
        # in the stack CANNOT extend any further to the right! Their reign is over.
        while stack and stack[-1][1] > h:
            popped_idx, popped_height = stack.pop()
            
            # Calculate the final physical area of the dead bar!
            # Width = Current Index - Where the bar originally started
            width = i - popped_idx
            area = popped_height * width
            
            max_area = max(max_area, area)
            print(f"    -> [POP] Bar height {popped_height} resolved. Area: {area}")
            
            # CRITICAL OPTIMIZATION: 
            # Because our current bar is shorter, it can mathematically "extend backwards" 
            # and physically overlap the space previously occupied by the dead taller bar!
            # We permanently steal its starting index!
            start_idx = popped_idx
            
        # Push the current bar into the stack!
        stack.append((start_idx, h))
        
    # Once we reach the end of the array, any bars still left in the stack 
    # successfully extended all the way to the absolute right edge of the histogram!
    for popped_idx, popped_height in stack:
        width = len(heights) - popped_idx
        area = popped_height * width
        max_area = max(max_area, area)
        
    print(f"  [SUCCESS] Max Area: {max_area}")
    return max_area

def demonstrate_histogram():
    section_header("Hard: Largest Rectangle in Histogram (Monotonic Stack)")
    
    heights = [2, 1, 5, 6, 2, 3]
    ans = largestRectangleArea(heights)
    print(f"\nResult: {ans} (Expected: 10 [Area from 5 and 6])")


# ==============================================================================
# 5. REGULAR EXPRESSION MATCHING (2D DYNAMIC PROGRAMMING)
# ==============================================================================
def isMatch(text: str, pattern: str) -> bool:
    """
    Time: O(T * P) | Space: O(T * P)
    Implement regular expression matching with support for '.' and '*'.
    '.' Matches any single character.
    '*' Matches zero or more of the preceding element.
    """
    # DP Matrix: dp[i][j] is True if text[:i] mathematically matches pattern[:j]
    T, P = len(text), len(pattern)
    dp = [[False] * (P + 1) for _ in range(T + 1)]
    
    # Base Case: Empty text and Empty pattern is a perfect match!
    dp[0][0] = True
    
    # Initialize the first row (Empty text, but active pattern)
    # E.g., Text="" and Pattern="a*b*". The '*' can represent ZERO characters, 
    # so the pattern can completely collapse into an empty string!
    for j in range(1, P + 1):
        if pattern[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
            
    print(f"  Text: '{text}' | Pattern: '{pattern}'")
    
    for i in range(1, T + 1):
        for j in range(1, P + 1):
            
            # The current characters match perfectly (or it's a wildcard '.')!
            if pattern[j - 1] == '.' or pattern[j - 1] == text[i - 1]:
                # We inherit the True/False state from the upper-left diagonal!
                dp[i][j] = dp[i - 1][j - 1]
                
            # THE STAR OPERATOR (The complex branch)
            elif pattern[j - 1] == '*':
                
                # Scenario A: The '*' represents ZERO occurrences of the previous char.
                # We mathematically delete the '*' and the character preceding it (j - 2).
                zero_occurrences = dp[i][j - 2]
                
                # Scenario B: The '*' represents ONE OR MORE occurrences.
                # The preceding character must perfectly match our current text character!
                # If it does, we inherit the state from exactly ONE row above (i - 1), 
                # maintaining the exact same pattern position (j)!
                one_or_more = False
                prev_char = pattern[j - 2]
                if prev_char == '.' or prev_char == text[i - 1]:
                    one_or_more = dp[i - 1][j]
                    
                dp[i][j] = zero_occurrences or one_or_more
                
    return dp[T][P]

def demonstrate_regex():
    section_header("Hard: Regular Expression Matching (2D DP)")
    
    text = "aab"
    pattern = "c*a*b"
    ans = isMatch(text, pattern)
    print(f"\nResult: {ans} (Expected: True)")


def run_all_labs():
    demonstrate_rain_water()
    demonstrate_histogram()
    demonstrate_regex()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 'Trapping Rain Water', why does checking `max_left < max_right` mathematically guarantee that we can calculate the water for `left` without even knowing what is happening in the middle of the array?"
   Senior Answer: "Water volume is defined by the shortest bounding wall. If `max_left` is currently $5$ and `max_right` is currently $10$, the absolute maximum water level possible on the left side is capped at $5$. Even if there is a massive wall of height $100$ somewhere in the unseen middle of the array, it mathematically cannot change the fact that the water will spill out over the $5$ wall on the left edge. Because `max_left` is strictly smaller, it is the absolute defining bottleneck for that specific column, allowing us to safely calculate `max_left - height[left]` and advance the pointer without any future visibility."

2. Interviewer: "What is a 'Monotonic Stack', and why does 'Largest Rectangle in Histogram' require it instead of a normal Stack?"
   Senior Answer: "A Monotonic Stack is a stack that enforces a strict mathematical ordering (either purely Ascending or purely Descending). In the Histogram problem, as long as the bars are getting taller (Ascending), the theoretical maximum rectangle continues to organically expand to the right. We push them into the stack. The moment we hit a shorter bar, the ascending 'trend' is violently broken. The taller bars in the stack are physically blocked from expanding any further. A Monotonic Stack automatically detects this trend break, violently popping and mathematically finalizing the area of all the blocked taller bars until the stack's ascending order is restored."

3. Interviewer: "In the 2D DP Regex Matching, how does the `*` operator simulate checking 'one or more' occurrences without using an expensive internal `while` loop?"
   Senior Answer: "If the preceding pattern character matches the current text character, we resolve the state using `dp[i - 1][j]`. The `i - 1` means we are looking at the DP state for the *previous* character in the text, but the `j` means we are keeping the *exact same* `*` pattern active! By looking directly UP in the DP matrix, we organically inherit the result of previous matches. If the text is `aaaa` and the pattern is `a*`, the matrix evaluates the 4th `a` by looking at the result for the 3rd `a`, which looked at the 2nd, which looked at the 1st. This elegantly chains the state transitions together, simulating an infinite loop using $O(1)$ matrix lookups."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (Optimization Hard) Completed.")
