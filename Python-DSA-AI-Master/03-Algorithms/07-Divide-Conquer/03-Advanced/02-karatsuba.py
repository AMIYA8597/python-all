\"\"\"
Karatsuba Multiplication (Divide and Conquer)
=============================================

1. Introduction & Why it Exists:
--------------------------------
Traditional multiplication algorithms (like the one taught in primary school) take 
O(N^2) time to multiply two N-digit numbers. Karatsuba algorithm is a divide and 
conquer approach that reduces the multiplication of two N-digit numbers to at most 
N^(log_2(3)) ≈ N^1.585 single-digit multiplications. It is significantly faster for 
large numbers and is implemented in the standard libraries of many languages, 
including Python, for large integer arithmetic.

2. Learning Objectives:
-----------------------
- Understand the math behind Karatsuba's trick.
- Implement a recursive Divide and Conquer multiplier.
- Handle base cases gracefully for performance.
- Analyze recursion trees and time complexity.

3. Concept Explanation:
-----------------------
Given two large numbers x and y, we can split them in half (base B, usually 10 or 2):
x = x1 * B^m + x0
y = y1 * B^m + y0

Standard multiplication gives 4 parts:
x * y = (x1*y1)*B^(2m) + (x1*y0 + x0*y1)*B^m + x0*y0

Karatsuba computes only 3 multiplications:
1. z2 = x1 * y1
2. z0 = x0 * y0
3. z1 = (x1 + x0) * (y1 + y0)

The middle term becomes: z1 - z2 - z0
Thus:
x * y = z2*B^(2m) + (z1 - z2 - z0)*B^m + z0
\"\"\"

def karatsuba(x: int, y: int) -> int:
    \"\"\"
    Professional grade Karatsuba multiplication for integers.
    \"\"\"
    # Base case for recursion: small numbers are faster with direct multiplication
    if x < 10 or y < 10:
        return x * y
        
    # Find the size of the numbers
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    
    # Multiplier
    bm = 10 ** m
    
    # Split the numbers
    x1, x0 = divmod(x, bm)
    y1, y0 = divmod(y, bm)
    
    # 3 recursive calls instead of 4
    z2 = karatsuba(x1, y1)
    z0 = karatsuba(x0, y0)
    z1 = karatsuba(x1 + x0, y1 + y0)
    
    # Combine results
    return (z2 * 10**(2*m)) + ((z1 - z2 - z0) * bm) + z0


if __name__ == \"__main__\":
    print(\"Testing Karatsuba Multiplication...\")
    
    test_cases = [
        (1234, 5678),
        (123456789, 987654321),
        (0, 100),
        (9, 9)
    ]
    
    for x, y in test_cases:
        expected = x * y
        actual = karatsuba(x, y)
        assert expected == actual, f\"Failed for {x} * {y}: Expected {expected}, got {actual}\"
        print(f\"{x} * {y} = {actual}\")
        
    print(\"All tests passed!\")
