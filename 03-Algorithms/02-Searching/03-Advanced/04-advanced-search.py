"""
# ==============================================================================
# LABORATORY: TERNARY SEARCH (UNIMODAL FUNCTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You know that Binary Search finds an answer in O(log N) time by dividing the 
# search space in half. But Binary Search ONLY works if the function is 
# "Monotonic" (Strictly increasing or strictly decreasing, e.g. a sorted array).
#
# What if the function goes UP, hits a peak, and then goes DOWN? (Like a parabola, 
# or calculating the highest point of a thrown baseball). This is called a 
# "Unimodal Function".
#
# If you try to use Binary Search on a parabola, checking the exact middle tells 
# you NOTHING about which side the peak is on. 
# 
# "Ternary Search" solves this. Instead of cutting the search space into 2 halves, 
# it cuts it into 3 THIRDS. By comparing the two dividing lines, we can mathematically 
# prove which third of the graph DOES NOT contain the peak, and discard it!
# It achieves O(log3 N) time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Unimodal Functions.
# - Understand the Two Midpoints math (`mid1` and `mid2`).
# - Implement Ternary Search to find the Maximum (or Minimum) of a curve.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. UNIMODAL FUNCTION (THE PARABOLA)
# ==============================================================================
def f(x: float) -> float:
    """
    A mathematical Unimodal Function.
    Let's represent a baseball thrown in the air: y = -5x^2 + 20x + 10
    We want to find the exact X coordinate where the ball is at its maximum height.
    (From calculus, derivative is -10x + 20 = 0 -> x = 2. Max height is 30).
    """
    return -5 * (x**2) + 20 * x + 10


# ==============================================================================
# 4. TERNARY SEARCH IMPLEMENTATION
# ==============================================================================
def ternary_search_maximum(left: float, right: float, absolute_precision: float = 1e-6) -> float:
    """
    Finds the X coordinate that produces the MAXIMUM value of f(x).
    Time Complexity: O(log(N)) (Specifically Base 3/2).
    """
    
    # We loop until the search space is infinitesimally small
    while right - left > absolute_precision:
        
        # Cut the space into THIRDS using two midpoints
        # Length of a third is (right - left) / 3
        mid1 = left + (right - left) / 3.0
        mid2 = right - (right - left) / 3.0
        
        # Evaluate the function at both midpoints
        y1 = f(mid1)
        y2 = f(mid2)
        
        # LOGIC:
        # If y1 < y2, the graph is sloping UPWARDS towards the right. 
        # The peak CANNOT possibly be in the left-most third (before mid1).
        if y1 < y2:
            left = mid1
            
        # If y1 > y2, the graph is sloping DOWNWARDS towards the right.
        # The peak CANNOT possibly be in the right-most third (after mid2).
        elif y1 > y2:
            right = mid2
            
        # If y1 == y2, the peak must be perfectly between them!
        # We can discard BOTH the left-most and right-most thirds.
        else:
            left = mid1
            right = mid2
            
    # The search space is now basically 0. Return the exact middle.
    return (left + right) / 2.0


def demonstrate_ternary_search():
    section_header("Algorithm: Ternary Search (Finding a Peak)")
    
    print("Function: f(x) = -5x^2 + 20x + 10")
    print("This is a parabola opening downwards. We want to find the Peak (Max).")
    
    # Define our initial search boundaries
    # We know the ball was thrown between X=0 and X=10.
    start_x = -10.0
    end_x = 10.0
    
    print(f"\nInitial Search Space: [{start_x}, {end_x}]")
    
    optimal_x = ternary_search_maximum(start_x, end_x)
    max_height = f(optimal_x)
    
    print(f"\nCalculated Optimal X: {optimal_x:.6f} (Expected: 2.000000)")
    print(f"Calculated Max Height: {max_height:.6f} (Expected: 30.000000)")


# ==============================================================================
# 5. DISCRETE TERNARY SEARCH (ARRAYS)
# ==============================================================================
def ternary_search_array(arr: list[int]) -> int:
    """
    Finds the peak in a Unimodal Array (Strictly increasing, then strictly decreasing).
    E.g. [1, 3, 8, 12, 4, 2] -> Peak is 12.
    """
    left = 0
    right = len(arr) - 1
    
    while left < right:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        if arr[mid1] < arr[mid2]:
            left = mid1 + 1 # Peak is strictly to the right of mid1
        elif arr[mid1] > arr[mid2]:
            right = mid2 - 1 # Peak is strictly to the left of mid2
        else:
            # They are equal. Peak is between them.
            left = mid1 + 1
            right = mid2 - 1
            
    return arr[left]

def demonstrate_discrete_ternary():
    section_header("Algorithm: Discrete Ternary Search (Arrays)")
    
    arr = [1, 5, 9, 15, 22, 50, 42, 33, 10, 2, -5]
    print(f"Unimodal Array: {arr}")
    
    peak = ternary_search_array(arr)
    print(f"Calculated Peak: {peak} (Expected: 50)")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Binary Search fail on a Parabola?
   Answer: Binary search relies on checking `f(mid)` and comparing it to a Target. For a parabola, if `f(mid)` is 20, you don't know if the peak is to the left or the right, because the curve hits 20 twice! Ternary search compares TWO midpoints against EACH OTHER, analyzing the *slope* of the curve to determine direction.

2. Does Ternary Search take fewer steps than Binary Search?
   Answer: Actually, NO! Binary search reduces the search space by `1/2` (50%) every step. Ternary search reduces it by `2/3` (66%) every step. `1/2` is smaller than `2/3`, so Binary Search shrinks the space FASTER! However, we use Ternary Search because Binary Search is mathematically impossible on unimodal functions, not because it is faster.

3. Can Ternary Search find the minimum of a curve instead of a maximum?
   Answer: Yes! You just reverse the logic. If you are looking for a valley (minimum), and `f(mid1) < f(mid2)`, it means the curve is sloping UPWARDS to the right, so the valley MUST be to the left of `mid2`. You discard the right-most third.
"""

if __name__ == "__main__":
    demonstrate_ternary_search()
    demonstrate_discrete_ternary()
    print("\n[SUCCESS] Laboratory: Ternary Search Completed.")
