"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (INTEL PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Intel interviews focus heavily on Low-Level Hardware interactions, Bit 
# manipulation, CPU architecture (Cache Lines, Endianness), and algorithmic 
# optimization for physical registers. 
#
# You will be asked questions about Endianness, Bit Masking, identifying if 
# numbers have opposite signs without using `if` statements, or reversing the 
# bits of a 32-bit integer.
#
# A junior engineer converts the number to a string `bin(n)`, reverses the string, 
# and parses it back to an integer. This requires heavy heap memory allocation 
# and takes thousands of clock cycles.
# 
# A senior engineer mathematically shifts the integer directly inside the CPU 
# register using `<<` and `>>`, executing the entire reversal natively on the 
# ALU in exactly 32 clock cycles with zero RAM allocation.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Bit Reversal (32-bit unsigned integers).
# - Master Bit Masking and extraction.
# - Understand Endianness and hardware-level sign checks.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. REVERSE BITS (THE 32-BIT SHIFT MASTERCLASS)
# ==============================================================================
def reverse_bits(n: int) -> int:
    """
    Time: O(1) (Strictly 32 operations) | Space: O(1)
    Reverses the bits of a given 32-bit unsigned integer.
    """
    result = 0
    print(f"  Starting State: {bin(n)[2:].zfill(32)}")
    
    # We must explicitly loop 32 times because a 32-bit integer has 32 bits, 
    # even if they are leading zeroes!
    for i in range(32):
        # 1. Extract the right-most bit of `n` using a Bitmask (n & 1)
        bit = n & 1
        
        # 2. Shift the `result` to the left to make physical room for the new bit!
        result = result << 1
        
        # 3. Drop the extracted bit into the newly created empty space on the right!
        # (result | bit) OR-ing with 0 is essentially an assignment.
        result = result | bit
        
        # 4. Shift `n` to the right to mathematically discard the bit we just processed!
        n = n >> 1
        
    print(f"  Final State   : {bin(result)[2:].zfill(32)}")
    return result

def demonstrate_reverse_bits():
    section_header("Intel: Reverse Bits (ALU Optimization)")
    
    number = 43261596 # Binary: 00000010100101000001111010011100
    print(f"Task: Reverse the 32 bits of {number}")
    
    ans = reverse_bits(number)
    print(f"\nResult: Base-10 Integer is {ans}")


# ==============================================================================
# 4. OPPOSITE SIGNS (THE XOR SIGN BIT HACK)
# ==============================================================================
def have_opposite_signs(x: int, y: int) -> bool:
    """
    Time: O(1) | Space: O(1)
    Determine if two integers have opposite signs WITHOUT using multiplication, 
    division, or conditional `< 0` checks.
    
    Mathematical Law: In Two's Complement representation, the Most Significant 
    Bit (MSB) determines the sign (0 for positive, 1 for negative).
    If we XOR two numbers, the MSB of the result will ONLY be 1 if their original 
    MSBs were different!
    """
    print(f"  Evaluating {x} and {y}")
    
    # The XOR operation:
    # (+) ^ (+) -> MSB is 0 ^ 0 = 0 (Positive)
    # (-) ^ (-) -> MSB is 1 ^ 1 = 0 (Positive)
    # (+) ^ (-) -> MSB is 0 ^ 1 = 1 (Negative!)
    
    # If the XOR result is mathematically less than 0, the sign bits were opposite!
    result = x ^ y
    print(f"    -> Result of {x} ^ {y} = {result}")
    
    return result < 0

def demonstrate_opposite_signs():
    section_header("Intel: Detect Opposite Signs (MSB XOR Hack)")
    
    test_cases = [
        (100, -50),
        (-20, -30),
        (5, 500)
    ]
    
    for x, y in test_cases:
        ans = have_opposite_signs(x, y)
        print(f"Are {x} and {y} opposite? {ans}")


def run_all_labs():
    demonstrate_reverse_bits()
    demonstrate_opposite_signs()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Reverse Bits algorithm, why do we mathematically force the loop to run exactly 32 times, instead of using a `while n > 0` loop?"
   Senior Answer: "If we use `while n > 0`, the loop will prematurely terminate the absolute millisecond we process the highest '1' bit. For example, if the input is `1` (which is `0000...0001` in 32-bit), the `while` loop extracts the `1`, shifts `n` to `0`, and terminates after exactly 1 loop! The reversed output would just be `1`. However, the absolute correct reversed value of a 32-bit `1` requires the `1` to be shifted 31 times to the left, generating `2,147,483,648`. The 32-bit boundary is a rigid hardware constraint; we MUST physically process and shift all the leading zeroes to mathematically construct the correct mirrored binary structure."

2. Interviewer: "Explain how the CPU hardware interprets the MSB (Most Significant Bit) in Two's Complement, and why $X \\oplus Y < 0$ proves they have opposite signs."
   Senior Answer: "Modern CPUs do not use a separate '+' or '-' symbol in memory; they use Two's Complement. In a 32-bit signed integer, the 31st bit (the MSB) acts as the Sign Flag: `0` means Positive, `1` means Negative. The Bitwise XOR operation (`^`) follows the rule of inequality: it outputs `1` ONLY if the two input bits are different. Therefore, if $X$ and $Y$ have opposite signs, one has an MSB of `1` and the other has an MSB of `0`. $1 \\oplus 0$ equals `1`. Because the resulting integer now has an MSB of `1`, the CPU hardware universally interprets it as a Negative number ($< 0$). If they had the same sign, $0 \\oplus 0$ or $1 \\oplus 1$ would both yield an MSB of `0` (Positive)."

3. Interviewer: "What is 'Endianness', and how does Big-Endian vs Little-Endian affect bitwise operators like `>>` and `&`?"
   Senior Answer: "Endianness dictates the physical byte-ordering in RAM. Little-Endian (Intel x86 architecture) stores the Least Significant Byte at the lowest memory address. Big-Endian (Network protocols, some ARM) stores the Most Significant Byte at the lowest address. However, this is purely a *memory layout* concept. Bitwise operators like `>>`, `<<`, and `&` are abstracted by the Compiler and execute inside the CPU ALU registers. The ALU mathematically guarantees that `n & 1` ALWAYS extracts the Least Significant Bit, and `n >> 1` ALWAYS shifts towards the Least Significant Bit, regardless of the underlying physical RAM Endianness. Bitwise math is mathematically platform-agnostic."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Tech Companies Prep (Intel) Completed.")
