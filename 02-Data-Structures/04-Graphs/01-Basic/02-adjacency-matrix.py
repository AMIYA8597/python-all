"""
# ==============================================================================
# LABORATORY: ADJACENCY MATRIX DEEP DIVE & MATRIX MATH
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# While Adjacency Lists are the standard for sparse graphs, Adjacency Matrices 
# unlock the power of Linear Algebra. 
# By representing a graph as a 2D Matrix, we can perform operations like Matrix 
# Multiplication. Squaring an Adjacency Matrix (A^2) magically tells you exactly 
# how many paths of length 2 exist between ANY two nodes! A^3 gives paths of 
# length 3, etc. This is used in network analysis, finding mutual friends 
# (path length 2), and PageRank algorithms.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how to calculate Node Degrees instantly using Row/Col sums.
# - Perform Matrix Multiplication on an Adjacency Matrix.
# - Prove that A^N finds the number of paths of length N.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATRIX SETUP AND DEGREES
# ==============================================================================
class GraphMatrix:
    def __init__(self, size: int):
        self.n = size
        self.matrix = [[0] * size for _ in range(size)]
        
    def add_edge(self, u: int, v: int, directed: bool = False):
        self.matrix[u][v] = 1
        if not directed:
            self.matrix[v][u] = 1

    def get_out_degree(self, u: int) -> int:
        """The out-degree of a node is the sum of its row."""
        return sum(self.matrix[u])
        
    def get_in_degree(self, u: int) -> int:
        """The in-degree of a node is the sum of its column."""
        total = 0
        for i in range(self.n):
            total += self.matrix[i][u]
        return total
        
    def display(self):
        print("    " + "  ".join(str(i) for i in range(self.n)))
        print("  " + "-" * (self.n * 3))
        for i, row in enumerate(self.matrix):
            print(f"{i} | {row}")

def demonstrate_degrees():
    section_header("Matrix Degrees (Row/Col Sums)")
    
    g = GraphMatrix(4)
    # Directed graph
    g.add_edge(0, 1, directed=True)
    g.add_edge(0, 2, directed=True)
    g.add_edge(2, 3, directed=True)
    g.add_edge(1, 3, directed=True)
    g.add_edge(3, 0, directed=True) # Cycle
    
    g.display()
    
    print("\nNode 0 Out-Degree (Row Sum):", g.get_out_degree(0))
    print("Node 3 In-Degree (Col Sum): ", g.get_in_degree(3))


# ==============================================================================
# 4. LINEAR ALGEBRA: PATHS OF LENGTH N
# ==============================================================================
def multiply_matrices(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    """Standard O(N^3) matrix multiplication."""
    n = len(A)
    # Initialize empty n x n matrix
    result = [[0] * n for _ in range(n)]
    
    # Dot product of rows and columns
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
                
    return result

def demonstrate_matrix_multiplication():
    section_header("Algorithm: Finding Paths via Matrix Multiplication")
    print("""
If A is our Adjacency Matrix, calculating A * A (which is A^2) gives us a new 
matrix where result[i][j] equals the exact number of paths of length 2 from 
Node i to Node j!

Why does this work?
In matrix multiplication, result[i][j] = sum(A[i][k] * A[k][j]) for all k.
A[i][k] is 1 if an edge exists from i to k.
A[k][j] is 1 if an edge exists from k to j.
1 * 1 = 1. So if both edges exist, it adds 1 to the path count!
    """)
    
    # Building a simple graph:
    # 0 -> 1 -> 2
    # 0 -> 3 -> 2
    # How many ways are there to get from 0 to 2 in exactly 2 steps?
    # Visually, there are 2 ways: (0->1->2) and (0->3->2). Let's prove it with math!
    
    g = GraphMatrix(4)
    g.add_edge(0, 1, directed=True)
    g.add_edge(1, 2, directed=True)
    g.add_edge(0, 3, directed=True)
    g.add_edge(3, 2, directed=True)
    
    print("Original Matrix (A^1 - Paths of length 1):")
    g.display()
    
    A_squared = multiply_matrices(g.matrix, g.matrix)
    
    print("\nSquared Matrix (A^2 - Paths of length 2):")
    print("    " + "  ".join(str(i) for i in range(4)))
    print("  " + "-" * 12)
    for i, row in enumerate(A_squared):
        print(f"{i} | {row}")
        
    print("\nLook at Row 0, Column 2 in the Squared Matrix.")
    print(f"Value = {A_squared[0][2]}.")
    print("The math perfectly proved there are exactly 2 paths of length 2 from Node 0 to Node 2!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In an Adjacency Matrix representing an undirected graph, what property does the matrix have?
   Answer: It is symmetric across the main diagonal. If `matrix[A][B] = 1`, then `matrix[B][A]` must also be `1`.

2. How do you find the "In-Degree" of a node using an Adjacency Matrix?
   Answer: You sum all the values in that node's Column. (The Out-Degree is the sum of the node's Row).

3. What does the matrix $A^3$ represent?
   Answer: If you multiply the adjacency matrix by itself 3 times, the resulting matrix $A^3$ will contain integers at `[i][j]` representing the exact number of distinct paths of length exactly 3 that exist between node `i` and node `j`.
"""

if __name__ == "__main__":
    demonstrate_degrees()
    demonstrate_matrix_multiplication()
    print("\n[SUCCESS] Laboratory: Adjacency Matrix Deep Dive Completed.")
