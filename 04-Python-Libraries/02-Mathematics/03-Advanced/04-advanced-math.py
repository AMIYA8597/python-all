"""
# ==============================================================================
# LABORATORY: SPARSE MATRICES & GRAPH MATH (SCIPY.SPARSE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Imagine you are modeling a Social Network (like Facebook). You have 2 Billion 
# users. You want to represent the "Friendship Graph" mathematically as an 
# Adjacency Matrix. 
#
# A Dense matrix would be 2 Billion x 2 Billion. That equals 4 Quintillion cells. 
# Storing that in RAM using 64-bit floats would require 32 Exabytes of RAM. 
# It is physically impossible to compute on modern Earth hardware.
#
# However, the average user only has 300 friends! This means 99.9999% of the 
# Matrix is exactly ZERO.
#
# `scipy.sparse` solves this. A Sparse Matrix mathematically behaves identically 
# to a Dense NumPy array, but internally, it ONLY stores the coordinates and 
# values of the Non-Zero elements! That 32 Exabyte matrix suddenly shrinks to 
# a few Gigabytes, allowing a single laptop to compute the matrix multiplications.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between Dense and Sparse memory storage.
# - Construct a CSR (Compressed Sparse Row) Matrix.
# - Execute matrix multiplication and Graph operations using sparse math.
#
# ==============================================================================
"""

import numpy as np
from scipy import sparse
import time
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DENSE VS SPARSE MEMORY OVERHEAD
# ==============================================================================
def demonstrate_memory():
    section_header("Dense vs Sparse Memory Storage")
    
    # Let's create a 10,000 x 10,000 Dense Matrix filled with Zeros.
    # Total cells: 100,000,000 (100 Million)
    n = 10_000
    print(f"Allocating {n} x {n} Dense Matrix in RAM...")
    
    dense_matrix = np.zeros((n, n), dtype=np.float64)
    
    # Let's manually add just 3 non-zero elements
    dense_matrix[0, 5] = 42.0
    dense_matrix[999, 999] = 17.0
    dense_matrix[5000, 20] = 99.0
    
    dense_bytes = dense_matrix.nbytes
    print(f"Dense Matrix RAM Usage: {dense_bytes / (1024**2):.2f} MB")
    
    # ---------------------------------------------------------
    # Now, let's convert it to a Compressed Sparse Row (CSR) matrix.
    # CSR strictly stores 3 arrays internally: Data, Row Pointers, Col Indices.
    csr_matrix = sparse.csr_matrix(dense_matrix)
    
    # Memory footprint of a CSR matrix is the sum of its internal arrays
    sparse_bytes = csr_matrix.data.nbytes + csr_matrix.indices.nbytes + csr_matrix.indptr.nbytes
    print(f"Sparse CSR RAM Usage  : {sparse_bytes} Bytes! ({sparse_bytes / 1024:.2f} KB)")
    
    compression_ratio = dense_bytes / sparse_bytes
    print(f"\nCompression Ratio: {compression_ratio:,.0f}x smaller!")


# ==============================================================================
# 4. CONSTRUCTING SPARSE MATRICES EFFICIENTLY
# ==============================================================================
def demonstrate_construction():
    section_header("Constructing Sparse Matrices (COO vs CSR)")
    
    # CRITICAL WARNING: You should NEVER construct a large Dense matrix and then 
    # convert it to Sparse (because allocating the Dense matrix will crash your RAM).
    # You must construct it sparsely from the very beginning!
    
    # We use the COO (Coordinate) format to easily build the matrix.
    # You just provide three 1D arrays: The Values, The X coords, The Y coords.
    
    data = np.array([42.0, 17.0, 99.0]) # The actual numbers
    rows = np.array([0, 999, 5000])     # The Y coordinates
    cols = np.array([5, 999, 20])       # The X coordinates
    
    print("Building COO (Coordinate) Matrix directly...")
    coo_matrix = sparse.coo_matrix((data, (rows, cols)), shape=(10_000, 10_000))
    print(f"Matrix built! Type: {type(coo_matrix)}")
    
    # COO format is great for building, but TERRIBLE for arithmetic (multiplication).
    # Before doing math, we always convert COO to CSR (Compressed Sparse Row)!
    csr_matrix = coo_matrix.tocsr()
    print("Converted to CSR for hyper-fast arithmetic.")


# ==============================================================================
# 5. SPARSE MATRIX MULTIPLICATION (GRAPH RANDOM WALKS)
# ==============================================================================
def demonstrate_multiplication():
    section_header("Sparse Matrix Arithmetic (Graph Random Walks)")
    
    # Let's model a tiny Graph (e.g. 5 webpages linking to each other).
    # Webpage 0 links to 1 and 2.
    # Webpage 1 links to 2.
    # Webpage 2 links to 0, 3, 4.
    
    edges = [
        (0, 1), (0, 2),
        (1, 2),
        (2, 0), (2, 3), (2, 4)
    ]
    
    # Extract rows and cols
    rows = np.array([e[0] for e in edges])
    cols = np.array([e[1] for e in edges])
    data = np.ones(len(edges)) # Every link has a weight of 1
    
    # Build the Adjacency Matrix
    adj_matrix = sparse.csr_matrix((data, (rows, cols)), shape=(5, 5))
    
    print("Adjacency Matrix (Dense View):")
    print(adj_matrix.toarray()) # Safe to view because it's only 5x5
    
    # MATRIX MULTIPLICATION
    # If you multiply an Adjacency Matrix by itself (A @ A), the resulting matrix 
    # tells you exactly how many paths exist between two nodes that take EXACTLY 
    # 2 jumps! (A @ A @ A tells you 3 jumps!).
    
    # Using the standard `@` operator. SciPy perfectly handles Sparse @ Sparse!
    two_jumps = adj_matrix @ adj_matrix
    
    print("\nAdjacency Matrix Squared (Paths of length 2):")
    print(two_jumps.toarray())
    
    print(f"\nPaths from Node 0 to Node 3 taking exactly 2 jumps: {two_jumps[0, 3]}")
    # Proof: 0 -> 2 -> 3 (That is 1 path!).


def run_all_labs():
    demonstrate_memory()
    demonstrate_construction()
    demonstrate_multiplication()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Dense matrix containing only Zeros still consume massive amounts of RAM?
   Answer: A Dense Numpy Array (like `np.zeros`) physically allocates a 64-bit float in system RAM for every single cell in the requested shape, regardless of whether the value is $0$, $1$, or $99$. A $10,000 \times 10,000$ matrix requires 100 million physical memory addresses ($100M \times 8 \text{ bytes} \approx 800 \text{ MB}$). A Sparse Matrix bypasses this by completely ignoring $0$s. It only allocates memory to track the Coordinates and Values of the non-zero elements, crushing the memory footprint.

2. What is the difference between COO and CSR sparse formats?
   Answer: 
   - COO (Coordinate Format) stores exactly three 1D arrays of identical length: `data`, `row_indices`, `col_indices`. It is extremely intuitive to build and append data to, but it is highly inefficient for mathematical multiplication.
   - CSR (Compressed Sparse Row) severely compresses the `row_indices` array into a pointer array (`indptr`). This makes the matrix impossible to easily modify (inserting a new value requires shifting the entire pointer array in RAM), but it makes matrix-vector multiplications ($A \times x$) blisteringly fast, as the CPU can sequentially iterate through the rows with perfect cache locality. 
   **Best Practice:** Build your data in COO, then call `.tocsr()` before running your algorithms!

3. How does multiplying a Graph Adjacency Matrix by itself reveal the number of paths?
   Answer: This is a fundamental theorem of Spectral Graph Theory. When you perform the dot product of Row $i$ and Column $j$ during matrix multiplication, you are essentially asking: "Does Node $i$ connect to any Node $K$, AND does that Node $K$ connect to Node $j$?" If both links exist ($1 \times 1 = 1$), it adds a count to the final cell $C_{ij}$. Thus, $A^N$ mathematically computes the exact number of physical paths of length $N$ between every pair of nodes in the graph!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: SciPy Sparse Matrices Completed.")
