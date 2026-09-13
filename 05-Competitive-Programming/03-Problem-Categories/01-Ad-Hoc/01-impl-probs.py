"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (AD-HOC IMPLEMENTATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When you start a Codeforces contest, Problem A and Problem B are almost 
# never standard algorithmic patterns like "Dijkstra's" or "Dynamic Programming".
#
# They are "Ad-Hoc Implementation" problems.
#
# Ad-Hoc problems are purely logical puzzles. There is no textbook algorithm 
# to memorize. The problem gives you a strange, highly specific set of rules 
# (e.g., "A frog jumps 3 lily pads forward, 1 backward, unless the pad is red..."), 
# and your job is to translate those exact English rules into Python code 
# flawlessly and rapidly.
#
# The challenge is not computational complexity; the challenge is 
# Developer Speed, Edge Cases, and Bug-Free Code Architecture.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Translate complex, arbitrary rules into clean Python control flow.
# - Understand modulo arithmetic for circular array traversal.
# - Optimize naive simulations using mathematical shortcuts.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DIRECT RULE SIMULATION
# ==============================================================================
def simulate_water_jugs(instructions: list[str], max_capacity: int) -> int:
    """
    Problem: A water jug starts empty (0 liters). 
    Max capacity is `max_capacity`.
    - "FILL X" adds X liters, but any water overflowing spills and is lost.
    - "DRINK X" removes X liters, but you cannot drink more than what's inside.
    - "DOUBLE" doubles the current volume, capping at max_capacity.
    Return the final volume.
    
    Time Complexity: O(N), Space Complexity: O(1)
    """
    volume = 0
    
    for instruction in instructions:
        if instruction.startswith("FILL"):
            amount = int(instruction.split()[1])
            # Add water, but cap it at the max capacity using `min()`
            volume = min(max_capacity, volume + amount)
            
        elif instruction.startswith("DRINK"):
            amount = int(instruction.split()[1])
            # Remove water, but floor it at 0 using `max()`
            volume = max(0, volume - amount)
            
        elif instruction == "DOUBLE":
            volume = min(max_capacity, volume * 2)
            
    return volume

def demonstrate_simulation():
    section_header("Direct Rule Simulation")
    
    instructions = ["FILL 10", "DRINK 3", "DOUBLE", "FILL 50"]
    max_cap = 20
    
    print(f"Instructions: {instructions}")
    print(f"Max Capacity: {max_cap}")
    
    final = simulate_water_jugs(instructions, max_cap)
    print(f"\nFinal Volume: {final}")
    
    print("\nTakeaway: Use `min()` and `max()` to enforce strict upper and ")
    print("lower bounds elegantly, rather than writing massive nested if-statements.")


# ==============================================================================
# 4. CIRCULAR ARRAY TRAVERSAL (THE MODULO TRICK)
# ==============================================================================
def circular_josephus(n: int, k: int) -> int:
    """
    Problem: There are N people sitting in a circle, numbered 0 to N-1.
    Starting at person 0, you count K people and eliminate the Kth person.
    The circle shrinks, and you continue from the next person.
    Who is the last person standing?
    
    Naive approach: Build a list, pop elements, maintain pointer. O(N^2).
    Ad-Hoc Mathematical approach: O(N) recursive pattern!
    """
    winner = 0
    for i in range(1, n + 1):
        winner = (winner + k) % i
    return winner

def demonstrate_circular_math():
    section_header("Circular Array Simulation (The Modulo Trick)")
    
    print("If you are given a circular problem (e.g., a clock, or a round table), ")
    print("do NOT use a physical array and `.pop()` elements. That takes O(N^2) time.")
    print("Use the Modulo Operator `%` to mathematically 'wrap around' the circle.\n")
    
    n_people = 5
    k_steps = 2
    
    # People: 0, 1, 2, 3, 4
    # Round 1: kill 1 (remains 0, 2, 3, 4)
    # Round 2: kill 3 (remains 0, 2, 4)
    # Round 3: kill 0 (remains 2, 4)
    # Round 4: kill 4 (remains 2). Winner is 2!
    
    winner = circular_josephus(n_people, k_steps)
    print(f"N={n_people}, K={k_steps}. The last person standing is: {winner}")


# ==============================================================================
# 5. MATHEMATICAL SHORTCUTS (SKIPPING TIME)
# ==============================================================================
def math_shortcut_frog_jump(a: int, b: int, k: int) -> int:
    """
    Problem: A frog jumps `a` meters to the right, then `b` meters to the left.
    It does this repeatedly. Where is it after `k` total jumps?
    
    Constraints: k <= 10^14.
    If you simulate this with a loop `for _ in range(k):`, you get a TLE!
    """
    # Jumps happen in pairs: Right, then Left.
    # Total full pairs:
    pairs = k // 2
    
    # Net distance of one full pair:
    net_distance_per_pair = a - b
    
    # Position after all full pairs:
    final_pos = pairs * net_distance_per_pair
    
    # If K is odd, there is one final jump to the Right!
    if k % 2 == 1:
        final_pos += a
        
    return final_pos

def demonstrate_math_shortcut():
    section_header("Bypassing Simulation with Math")
    
    print("In Codeforces Div2-A, a problem often sounds like a simulation: ")
    print("'Run this loop K times'. But if K = 10^14, the loop will run for 30 hours!")
    print("You must find the O(1) mathematical formula.\n")
    
    a = 5  # Right
    b = 2  # Left
    k = 10**9 + 1 # 1 Billion and 1 jumps!
    
    print(f"Jump Right: {a}, Jump Left: {b}, Total Jumps: {k}")
    
    result = math_shortcut_frog_jump(a, b, k)
    print(f"Final Position: {result}")
    
    print("\nBecause we used O(1) math instead of a loop, it executed in 0.000 seconds!")


def run_all_labs():
    demonstrate_simulation()
    demonstrate_circular_math()
    demonstrate_math_shortcut()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. When a problem asks you to constrain a value between a minimum and a maximum boundary, why should you use `min()` and `max()` instead of `if/else` statements?
   Answer: Code brevity and bug reduction. Writing `if volume > max_cap: volume = max_cap` takes two lines and increases cyclomatic complexity. Writing `volume = min(max_cap, volume + amount)` forces the value to the exact mathematical ceiling in a single, elegant line of code. Similarly, `volume = max(0, volume - amount)` forces a mathematical floor. This prevents nested if-statement spaghetti and significantly reduces the chance of missing an edge case during a high-speed contest.

2. A problem asks you to simulate a pointer moving $K$ steps to the right on an array of length $N$. If the pointer falls off the right edge, it wraps around to index 0. How do you calculate the final index in $O(1)$ time?
   Answer: You use the Modulo operator (`%`). The formula is `final_index = (start_index + K) % N`. The modulo operator returns the remainder of division. If you start at index 3, move 15 steps on an array of size 5, `(3 + 15) = 18`. `18 % 5 = 3`. The pointer mathematically wraps around the array exactly 3 full times and perfectly lands back at index 3 in $O(1)$ time, completely avoiding a slow $O(K)$ `while` loop.

3. Why do Codeforces "Ad-Hoc" problems often result in "Time Limit Exceeded" (TLE) if you follow the exact instructions in the problem description?
   Answer: The problem description is often a deliberate trap. The story might explicitly instruct you to "Simulate the frog jumping $10^{14}$ times." A junior developer will write a `for` loop that iterates $10^{14}$ times. Python processes roughly $10^7$ iterations per second, meaning the loop will take 115 days to finish, triggering an instant TLE. The core challenge of Ad-Hoc problems is recognizing when a literal simulation must be bypassed using an $O(1)$ mathematical formula (like finding the net-distance of a jump-pair and multiplying it).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Ad-Hoc Implementation Completed.")
