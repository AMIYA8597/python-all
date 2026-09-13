"""
# ==============================================================================
# LABORATORY: TOWER OF HANOI (THE RECURSION MASTERCLASS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# The Tower of Hanoi is a mathematical game consisting of three rods and N disks 
# of different sizes. The rules are absolute:
# 1. You can only move one disk at a time.
# 2. You can only take the upper disk from one of the stacks.
# 3. No disk may be placed on top of a smaller disk.
#
# The objective is to move the entire stack to another rod.
# 
# Why do Computer Science professors love this puzzle? Because solving it manually 
# requires immense brainpower. But solving it with Recursion takes exactly 3 lines 
# of code. It teaches you to "Trust the Recursion". 
# 
# You don't need to trace every single disk move in your head. You just define 
# the macro-level state transitions, and the OS Call Stack automatically manages 
# the millions of micro-level moves perfectly!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the 3-step recursive paradigm (Trust the Recursion).
# - Understand why O(2^N) Time is mathematically optimal here.
# - Print the move sequence.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE RECURSIVE ENGINE
# ==============================================================================
# Global counter to track how many physical moves the algorithm executes
move_count = 0

def solve_hanoi(n: int, source: str, target: str, auxiliary: str) -> None:
    """
    Time Complexity: O(2^N)
    Space Complexity: O(N) (Max depth of the call stack)
    """
    global move_count
    
    # 1. THE BASE CASE
    # If there is only 1 disk left to move, just move it!
    # It is guaranteed to be safe to move to the target rod.
    if n == 1:
        move_count += 1
        print(f" Move disk 1 from {source} to {target}")
        return
        
    # 2. THE RECURSIVE STEP (TRUST THE RECURSION)
    # We want to move disk `n` to the `target`. 
    # But disks 1 through (n-1) are sitting on top of it!
    # So... we tell the recursion to magically move the top (n-1) disks out of 
    # the way, placing them on the `auxiliary` rod!
    # (Notice how `target` and `auxiliary` swap places in the arguments!)
    solve_hanoi(n - 1, source, auxiliary, target)
    
    # Now that the top (n-1) disks are out of the way on the auxiliary rod, 
    # disk `n` is exposed. Move it directly to the target!
    move_count += 1
    print(f" Move disk {n} from {source} to {target}")
    
    # Finally, we tell the recursion to magically take those (n-1) disks that 
    # we parked on the `auxiliary` rod, and move them onto the `target` rod 
    # so they sit perfectly on top of disk `n`!
    solve_hanoi(n - 1, auxiliary, target, source)


def demonstrate_hanoi():
    section_header("Algorithm: Tower of Hanoi")
    
    global move_count
    disks = 3
    print(f"Solving Tower of Hanoi for {disks} disks.")
    print("Rods: A (Source), C (Target), B (Auxiliary)\n")
    
    move_count = 0
    solve_hanoi(disks, 'A', 'C', 'B')
    
    print(f"\nTotal physical moves executed: {move_count}")
    print(f"Mathematical formula (2^N - 1): {2**disks - 1}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Fibonacci was $O(2^N)$ time and it was considered a catastrophe that needed to be optimized. Tower of Hanoi is also $O(2^N)$ time. Can we optimize it using Dynamic Programming?
   Answer: NO. In Fibonacci, we were doing redundant math (Overlapping Subproblems). In Tower of Hanoi, there are NO overlapping subproblems. Every single recursive call prints a unique physical move instruction. Mathematically, it requires exactly $2^N - 1$ physical moves to transfer the disks. It is impossible to solve it in fewer moves, so the $O(2^N)$ algorithm is mathematically perfectly optimal.

2. What does it mean to "Trust the Recursion"?
   Answer: It means you assume your recursive function ALREADY WORKS for $N-1$. When writing the code, you don't trace how the $N-1$ disks get to the auxiliary rod. You simply state: "Move $N-1$ disks to the auxiliary rod", write the code, and trust that the base case and the Call Stack will mathematically unwind correctly to execute that high-level command.

3. The Legend of Benares states there is a temple with 64 golden disks. When the monks finish moving all 64 disks, the universe will end. Assuming 1 move per second, when will it end?
   Answer: $2^{64} - 1$ moves. That is 18,446,744,073,709,551,615 seconds. Or roughly 585 Billion Years. (The universe is currently 13.8 billion years old).
"""

if __name__ == "__main__":
    demonstrate_hanoi()
    print("\n[SUCCESS] Laboratory: Tower of Hanoi Completed.")
