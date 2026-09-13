"""
# ==============================================================================
# LABORATORY: LINEAR DIOPHANTINE EQUATIONS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are at a store. You need exactly $83 worth of goods.
# The cashier only accepts $5 bills and $12 bills.
# Can you pay exactly $83 using only those bills? 
# If so, how many $5 bills (x) and how many $12 bills (y) do you need?
#
# This is a Linear Diophantine Equation: A*x + B*y = C.
#
# The constraint is brutal: `x` and `y` MUST be integers. You cannot hand the 
# cashier 3.5 bills.
#
# How do we solve this? 
# In the previous lab, you learned the Extended Euclidean Algorithm. It finds 
# integer solutions to a very specific equation: A*x_g + B*y_g = GCD(A, B).
#
# We can use that result to solve for ANY target C!
# 1. First, check if a solution is mathematically possible. 
#    Bézout's Lemma dictates that a solution only exists if the target `C` is a 
#    perfect multiple of GCD(A, B). If C % GCD != 0, it is impossible!
# 2. If it is possible, find the multiplier `K = C / GCD(A, B)`.
# 3. Take the base coefficients from the Extended GCD and multiply them by K!
#    True_x = x_g * K
#    True_y = y_g * K
#
# Furthermore, if one solution exists, INFINITELY many solutions exist! You can 
# shift the balance between `x` and `y` mathematically to find all of them.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Verify Diophantine solvability (C % GCD == 0).
# - Scale Extended GCD coefficients to hit target C.
# - Generate the infinite family of solutions.
#
# ==============================================================================
"""

from typing import Tuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: Extended Euclidean Algorithm from Previous Lab ---
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y
# --------------------------------------------------------------


# ==============================================================================
# 3. DIOPHANTINE SOLVER ENGINE
# ==============================================================================
def solve_diophantine(a: int, b: int, c: int) -> Optional[Tuple[int, int, int, int, int]]:
    """
    Attempts to solve the Linear Diophantine Equation: A*x + B*y = C
    
    Returns: None if impossible.
    If possible, returns: (base_x, base_y, shift_x, shift_y, gcd)
    The infinite family of solutions can be generated using any integer `k`:
    Final_X = base_x + k * shift_x
    Final_Y = base_y - k * shift_y
    """
    # 1. Base GCD Check
    # Diophantine equations are highly sensitive to signs. 
    # We solve using absolute values to keep the math clean, then restore signs.
    abs_a, abs_b = abs(a), abs(b)
    
    gcd, x_g, y_g = extended_gcd(abs_a, abs_b)
    
    # 2. SOLVABILITY TRIGGER
    # If C is not a multiple of the GCD, it is mathematically impossible to reach C 
    # using A and B integer steps.
    if c % gcd != 0:
        return None
        
    # 3. SCALING TO TARGET C
    multiplier = c // gcd
    
    base_x = x_g * multiplier
    base_y = y_g * multiplier
    
    # 4. RESTORE ORIGINAL SIGNS
    if a < 0: base_x = -base_x
    if b < 0: base_y = -base_y
        
    # 5. CALCULATE THE SHIFT VECTORS
    # To generate infinite solutions, we can add a specific amount to X, as long 
    # as we subtract an equivalent mathematical weight from Y.
    # The minimum shift vectors are: shift_x = (B / GCD) and shift_y = (A / GCD).
    # Why? Because A*(B/GCD) - B*(A/GCD) = 0! It keeps the equation perfectly balanced!
    shift_x = b // gcd
    shift_y = a // gcd
    
    return base_x, base_y, shift_x, shift_y, gcd


def print_solution_family(result_tuple, iterations: int = 5):
    """
    Generates a few solutions from the infinite mathematical family.
    """
    base_x, base_y, shift_x, shift_y, gcd = result_tuple
    
    print("\nGenerating Infinite Solution Family:")
    print("Formula: X = base_x + (k * shift_x) | Y = base_y - (k * shift_y)")
    print(f"Base X: {base_x}, Base Y: {base_y}")
    print(f"Shift X: {shift_x}, Shift Y: {shift_y}")
    print("-" * 50)
    
    for k in range(-2, iterations - 2):
        x = base_x + (k * shift_x)
        y = base_y - (k * shift_y)
        print(f"k = {k:2} | x = {x:4}, y = {y:4}")


def demonstrate_diophantine():
    section_header("Algorithm: Linear Diophantine Equation")
    
    # Scenario: The Store. A = $5 bill, B = $12 bill. Target = $83.
    a = 5
    b = 12
    c = 83
    
    print(f"Equation: {a}x + {b}y = {c}")
    
    result = solve_diophantine(a, b, c)
    
    if result:
        print("\nSolution Exists!")
        base_x, base_y, shift_x, shift_y, gcd = result
        print(f"Base Solution: x = {base_x}, y = {base_y}")
        print(f"Verification: 5*({base_x}) + 12*({base_y}) = {5*base_x + 12*base_y}")
        
        # Let's see the other solutions!
        print_solution_family(result, iterations=5)
        
        print("\nNotice in the real-world store scenario, negative bills don't exist.")
        print("Looking at the table, k=0 gives x=-7 (Impossible).")
        print("But k=1 gives x=5, y=4! You can hand the cashier five $5 bills and four $12 bills!")
    else:
        print("\nNo integer solution exists.")
        
    section_header("Impossible Scenario")
    a2, b2, c2 = 4, 6, 11
    print(f"Equation: {a2}x + {b2}y = {c2}")
    print(f"GCD(4, 6) = 2. But 11 is not divisible by 2!")
    print("Result:", solve_diophantine(a2, b2, c2))


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must $C$ be a multiple of the GCD?
   Answer: Imagine an XY coordinate plane. You are standing at $(0, 0)$. Every time you take a step in the X direction, you move exactly $A$ units. Every time you step in the Y direction, you move exactly $B$ units. Because $A$ and $B$ are both perfectly divisible by their GCD, every single coordinate you can physically land on must ALSO be perfectly divisible by the GCD. It forms an invisible grid. If the target $C$ does not fall exactly on one of those grid lines, it is mathematically unreachable!

2. How do the Shift Vectors mathematically maintain the equation's balance?
   Answer: The equation is $Ax + By = C$. We want to change $x$ and $y$ without changing $C$. This means any change must evaluate to 0: $A(\Delta x) + B(\Delta y) = 0$. 
   Solving for the ratio gives: $\Delta x / \Delta y = -B / A$. 
   To find the absolute smallest integer step size, we divide both sides by their Greatest Common Divisor. 
   $\Delta x = B / \text{GCD}$ and $\Delta y = -A / \text{GCD}$. 
   If we add $\Delta x$ to $X$, we MUST add $\Delta y$ (which is negative) to $Y$. This perfectly offsets the scales!

3. Where is this used in competitive programming?
   Answer: 
   - Weight/Coin Change problems where you want to know if a specific combination is possible.
   - Finding the intersection point of two arithmetic progressions (e.g., two people jumping on a number line, will they ever land on the same spot?).
   - It is the foundational building block for the Chinese Remainder Theorem, which solves systems of simultaneous congruences.
"""

if __name__ == "__main__":
    demonstrate_diophantine()
    print("\n[SUCCESS] Laboratory: Linear Diophantine Equations Completed.")
