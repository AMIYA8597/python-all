"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (NVIDIA PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Nvidia interviews prioritize High-Performance Computing (HPC), GPU optimization 
# concepts, extreme memory efficiency, and Bitwise Mathematics. 
#
# A junior engineer solves problems using Python lists and multiple mathematical 
# operations (e.g., division, modulo). This is slow.
# 
# A senior engineer recognizes that Division and Modulo are extremely heavy CPU 
# operations, whereas Bitwise Shifts (`>>`, `<<`) and Bitwise AND (`&`) execute 
# directly on the Arithmetic Logic Unit (ALU) in exactly 1 clock cycle. 
# They manipulate bits directly to achieve blinding execution speeds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Bitwise Arithmetic (Counting bits, powers of 2).
# - Master Grid/Matrix mathematical boundaries (similar to GPU CUDA Grids).
# - Understand the hardware cost of mathematical operations.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. COUNTING BITS (THE BRIAN KERNIGHAN ALGORITHM)
# ==============================================================================
def count_bits_naive(n: int) -> int:
    """O(32) per number - Naive bit shifting"""
    count = 0
    # Must shift 32 times regardless of the number!
    while n > 0:
        if n & 1 == 1:
            count += 1
        n = n >> 1
    return count

def count_bits_kernighan(n: int) -> int:
    """
    Time: O(1) per set bit | Space: O(1)
    Nvidia Favorite!
    Instead of shifting 32 times, the Brian Kernighan algorithm jumps directly 
    from '1' bit to the next '1' bit, instantly ignoring all '0' bits!
    """
    count = 0
    while n > 0:
        # THE KERNIGHAN TRICK: n & (n - 1)
        # Subtracting 1 mathematically flips the right-most '1' bit to a '0', 
        # and turns all trailing '0's to '1's. 
        # Doing an AND operation with the original number physically annihilates 
        # the right-most '1' bit!
        
        print(f"    -> Current: {bin(n)} | Operation: {bin(n)} & {bin(n-1)}")
        n = n & (n - 1)
        print(f"       Result : {bin(n)}")
        count += 1
        
    return count

def demonstrate_bit_counting():
    section_header("Nvidia: Counting Bits (Kernighan's Algorithm)")
    
    number = 52 # Binary: 110100
    print(f"Task: Count the number of '1' bits in {number} ({bin(number)})")
    
    ans = count_bits_kernighan(number)
    print(f"\nResult: Found {ans} set bits.")
    print("Notice how the algorithm executed exactly 3 loops, bypassing the zeroes!")


# ==============================================================================
# 4. IS POWER OF TWO (THE 1-CYCLE MASTERCLASS)
# ==============================================================================
def is_power_of_two(n: int) -> bool:
    """
    Time: O(1) | Space: O(1)
    A junior uses a while loop: `while n % 2 == 0: n = n // 2`.
    A senior uses the ALU logic gate.
    """
    if n <= 0: return False
    
    # If a number is a power of 2, its binary representation has EXACTLY ONE '1' bit!
    # Examples: 
    # 2  -> 0010
    # 4  -> 0100
    # 8  -> 1000
    # 16 -> 10000
    
    # Since Kernighan's algorithm `n & (n - 1)` annihilates exactly one '1' bit,
    # if we apply it to a Power of 2, the number will instantly become ZERO!
    result = n & (n - 1)
    
    print(f"  Checking {n} ({bin(n)})")
    print(f"    -> {bin(n)} & {bin(n-1)} = {bin(result)}")
    
    return result == 0

def demonstrate_power_of_two():
    section_header("Nvidia: Is Power of Two (O(1) ALU Gate)")
    
    test_cases = [8, 14, 16]
    
    for tc in test_cases:
        ans = is_power_of_two(tc)
        print(f"Result for {tc}: {ans}\n")


def run_all_labs():
    demonstrate_bit_counting()
    demonstrate_power_of_two()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does subtracting 1 from a binary number mathematically allow us to target the right-most '1' bit?"
   Senior Answer: "In Binary arithmetic, subtracting 1 triggers a cascading borrow operation. The CPU scans from right to left, flipping every trailing `0` into a `1`, until it hits the very first `1` bit. It borrows from that `1` bit, flipping it into a `0`, and stops. Therefore, the expression `(n - 1)` perfectly inverts the right-most `1` bit and all trailing zeroes, while leaving the entire left prefix of the number completely untouched. When we evaluate `n & (n - 1)`, the untouched prefix remains identical ($1 \\& 1 = 1$), but the right-most `1` bit and the trailing zeroes perfectly annihilate each other ($1 \\& 0 = 0$, and $0 \\& 1 = 0$)."

2. Interviewer: "Why is `n & 1 == 1` inside a loop slower than Kernighan's algorithm for a 64-bit integer?"
   Senior Answer: "Using a naive bit shift `while n > 0: n = n >> 1` requires the CPU to iterate through every single bit up to the highest set bit. If the number is $2^{62}$, the `while` loop must execute 63 times, even if every other bit in the number is $0$! The CPU wastes 62 clock cycles checking zeroes. Kernighan's algorithm jumps directly from `1` bit to `1` bit. If the 64-bit integer only has three `1` bits, the loop executes exactly 3 times and instantly terminates. It is strictly bounded by the number of SET bits, not the absolute magnitude of the number."

3. Interviewer: "In High-Performance Computing (HPC) / CUDA programming, why do we desperately avoid modulo (`%`) and division (`/`) operations inside massive data loops?"
   Senior Answer: "Modulo and Division are algorithmically complex operations for the physical CPU hardware. A single integer division instruction can take 20 to 40 CPU clock cycles to execute, as it requires iterative subtraction circuits. Conversely, Bitwise AND (`&`), OR (`|`), XOR (`^`), and Bit Shifts (`<<`, `>>`) map directly to native transistors on the Arithmetic Logic Unit (ALU) and execute in precisely 1 clock cycle. In a CUDA kernel processing 10 Billion pixels, replacing a modulo `x % 2 == 0` with a bitwise `x & 1 == 0` removes 300 Billion wasted clock cycles, radically accelerating the frame rate."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Tech Companies Prep (Nvidia) Completed.")
