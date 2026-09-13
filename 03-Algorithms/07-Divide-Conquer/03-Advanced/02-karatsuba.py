"""
# ==============================================================================
# LABORATORY: KARATSUBA ALGORITHM (FAST INTEGER MULTIPLICATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# How does a computer multiply $1234 \\times 5678$?
# In grade school, you learned to multiply every digit of the bottom number 
# against every digit of the top number, and then add the shifted rows.
# If a number has N digits, this takes O(N^2) time.
#
# If you are doing cryptography (RSA) and need to multiply two massive 
# 2,048-bit numbers, O(N^2) is agonizingly slow.
#
# In 1960, a 23-year-old student named Anatoly Karatsuba attended a seminar 
# by the legendary Andrey Kolmogorov. Kolmogorov conjectured that O(N^2) was 
# the absolute mathematical limit for multiplication.
# Within a week, Karatsuba invented a Divide & Conquer trick that proved 
# Kolmogorov wrong.
#
# A naive D&C algorithm chops the numbers in half, resulting in 4 recursive 
# multiplications. (O(N^2) time).
# Karatsuba found an algebraic trick using addition and subtraction to calculate 
# the middle terms, reducing it to ONLY 3 recursive multiplications!
#
# Recurrence: T(N) = 3 * T(N/2) + O(N)
# Master Theorem: O(N^log2(3)) = O(N^1.585)
# 
# This algorithm is so profound that it is literally built directly into 
# Python's C-source code for multiplying massive integers!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the algebraic formulation of number splitting.
# - Implement the 3-multiplication Karatsuba trick.
# - Understand why Python's large integers are so fast.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. KARATSUBA MULTIPLICATION ENGINE (O(N^1.585))
# ==============================================================================
def karatsuba(x: int, y: int) -> int:
    """
    Multiplies two integers using Karatsuba's Divide and Conquer algorithm.
    Time Complexity: O(N^1.585) where N is the number of digits.
    """
    
    # 1. BASE CASE
    # If the numbers are small enough (single digit), just multiply them directly!
    # The algebraic overhead of Karatsuba makes it slower than basic hardware 
    # multiplication for tiny numbers.
    if x < 10 or y < 10:
        return x * y
        
    # 2. DIVIDE (Determine the split point)
    # Calculate the size (number of digits) of the numbers.
    n = max(len(str(x)), len(str(y)))
    
    # The split point `m` is half the digits.
    m = n // 2
    
    # We split x into two halves: x1 (left half), x0 (right half).
    # e.g. 1234 -> x1 = 12, x0 = 34
    # Mathematically: 1234 = 12 * 10^2 + 34
    x1 = x // (10 ** m)
    x0 = x % (10 ** m)
    
    # We split y into two halves: y1 (left half), y0 (right half).
    y1 = y // (10 ** m)
    y0 = y % (10 ** m)
    
    # 3. CONQUER (The 3 Magical Multiplications)
    # Instead of doing x1*y1, x1*y0, x0*y1, x0*y0 (4 multiplications)...
    # We only do 3!
    
    # z2 = The high-order product
    z2 = karatsuba(x1, y1)
    
    # z0 = The low-order product
    z0 = karatsuba(x0, y0)
    
    # z1 = The middle-order product
    # We multiply the SUMS of the halves!
    # (x1 + x0) * (y1 + y0) = (x1*y1) + (x1*y0) + (x0*y1) + (x0*y0)
    # Notice that this contains the middle terms we want: (x1*y0) + (x0*y1).
    # It ALSO contains (x1*y1) and (x0*y0). But wait... we ALREADY calculated 
    # those! That's just z2 and z0!
    # So we simply subtract them away!
    z1 = karatsuba(x1 + x0, y1 + y0) - z2 - z0
    
    # 4. COMBINE (Algebraic Reassembly)
    # Final Formula: z2 * 10^(2m) + z1 * 10^m + z0
    result = (z2 * (10 ** (2 * m))) + (z1 * (10 ** m)) + z0
    
    return result


def demonstrate_karatsuba():
    section_header("Algorithm: Karatsuba Multiplication")
    
    x = 12345678901234567890
    y = 98765432109876543210
    
    print(f"X = {x}")
    print(f"Y = {y}")
    
    print("\nExecuting O(N^1.585) Karatsuba Divide & Conquer...")
    result = karatsuba(x, y)
    
    print(f"\nResult: {result}")
    
    # Verify with Python's built-in multiplier (which secretly uses Karatsuba!)
    expected = x * y
    print(f"Verification: {expected}")
    assert result == expected
    
    print("\nThe Magic Explained:")
    print("For a 4-digit number like 1234 * 5678:")
    print(" x1=12, x0=34 | y1=56, y0=78")
    print(" z2 = 12 * 56 = 672")
    print(" z0 = 34 * 78 = 2652")
    print(" z1 = (12+34) * (56+78) = 46 * 134 = 6164. Then subtract 672 and 2652 = 2840.")
    print(" Final = (672 * 10000) + (2840 * 100) + 2652 = 6,720,000 + 284,000 + 2652 = 7,006,652.")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does changing 4 multiplications to 3 matter?
   Answer: It alters the exponent in the Master Theorem. A recurrence of $T(N) = 4T(N/2) + O(N)$ evaluates to $O(N^{\\log_2(4)}) = O(N^2)$. By reducing it to 3 multiplications, the recurrence becomes $T(N) = 3T(N/2) + O(N)$, which evaluates to $O(N^{\\log_2(3)}) = O(N^{1.585})$. As $N$ (the number of digits) grows to thousands or millions, the difference between squared and 1.585 is staggering.

2. Does Python actually use Karatsuba under the hood?
   Answer: YES. In CPython (the default Python implementation), integer multiplication checks the bit-length of the numbers. If the numbers are small, it uses hardware $O(N^2)$ grade-school multiplication. If the numbers exceed a certain threshold (typically around 70 decimal digits), the C source code physically branches and executes a highly optimized C-implementation of Karatsuba's algorithm!

3. Is there anything faster than Karatsuba?
   Answer: Yes. Toom-Cook multiplication is a generalization that splits the number into 3 parts (Toom-3) yielding $O(N^{1.465})$. For impossibly massive numbers (millions of digits), the Schönhage-Strassen algorithm uses the Fast Fourier Transform (FFT) to achieve $O(N \\log N \\log \\log N)$!
"""

if __name__ == "__main__":
    demonstrate_karatsuba()
    print("\n[SUCCESS] Laboratory: Karatsuba Algorithm Completed.")
