"""
Strassen's Matrix Multiplication.

Learning Objectives:
1. Understand matrix multiplication optimization.
2. Implement Strassen's divide and conquer approach.
3. Analyze subproblem reduction from 8 to 7.

Concept Explanation:
Strassen's algorithm reduces the number of recursive multiplications from 8 to 7,
improving the asymptotic complexity of matrix multiplication from O(n^3) to O(n^2.81).
"""

from typing import List

Matrix = List[List[int]]

def add_matrix(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def sub_matrix(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def split_matrix(A: Matrix):
    n = len(A) // 2
    A11 = [row[:n] for row in A[:n]]
    A12 = [row[n:] for row in A[:n]]
    A21 = [row[:n] for row in A[n:]]
    A22 = [row[n:] for row in A[n:]]
    return A11, A12, A21, A22

def strassen(A: Matrix, B: Matrix) -> Matrix:
    """Strassen algorithm for square matrices of power of 2."""
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # 7 products
    P1 = strassen(add_matrix(A11, A22), add_matrix(B11, B22))
    P2 = strassen(add_matrix(A21, A22), B11)
    P3 = strassen(A11, sub_matrix(B12, B22))
    P4 = strassen(A22, sub_matrix(B21, B11))
    P5 = strassen(add_matrix(A11, A12), B22)
    P6 = strassen(sub_matrix(A21, A11), add_matrix(B11, B12))
    P7 = strassen(sub_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(sub_matrix(add_matrix(P1, P4), P5), P7)
    C12 = add_matrix(P3, P5)
    C21 = add_matrix(P2, P4)
    C22 = add_matrix(sub_matrix(add_matrix(P1, P3), P2), P6)

    C = []
    for i in range(n // 2):
        C.append(C11[i] + C12[i])
    for i in range(n // 2):
        C.append(C21[i] + C22[i])
    return C

"""
Performance Analysis:
- Time Complexity: O(n^log_2(7)) ≈ O(n^2.81).
- Space Complexity: O(n^2) for submatrices.

Edge Cases:
- Matrix size not a power of 2 (pad with zeros).
- Small matrices (Strassen is slower than standard for small n, usually cutoff is used).

Interview Challenge:
How to handle non-square or non-power-of-2 matrices in Strassen's algorithm?
"""

def test_strassen():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    expected = [[19, 22], [43, 50]]
    assert strassen(A, B) == expected
    print("All tests passed.")

if __name__ == "__main__":
    test_strassen()
