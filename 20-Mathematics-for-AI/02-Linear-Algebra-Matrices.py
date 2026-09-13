"""
# 02 - Linear Algebra: Matrices and Neural Networks

## A. Concept Name
Matrices, Matrix Multiplication, Dot Products, and the Neural Network Forward Pass.

## B. One-Sentence Definition
A matrix is a 2D grid of numbers (an array of vectors) used to represent datasets, weights in a neural network, or linear transformations (like rotating an image) applied to vectors.

## C. Why Does This Exist?
While a vector represents a single item (e.g., one image, one word), a matrix allows us to process MILLIONS of items simultaneously. This is called **Batch Processing**.
More importantly, in a Neural Network, the "knowledge" of the model is stored in Weight Matrices. When data passes through the network, the mathematical operation happening is Matrix Multiplication. GPUs exist almost entirely to do Matrix Multiplication extremely fast.

## D. Intuition & Real-World Analogy
Imagine a spreadsheet. 
- A single row (e.g., one customer's age, income, and score) is a **Vector**.
- The entire table of 10,000 customers is a **Matrix**.

Now imagine you want to calculate a "Credit Score" based on Age and Income. You have a formula:
`Score = (Age * 2) + (Income * 0.5)`
The weights `[2, 0.5]` are a Vector.
Instead of looping over all 10,000 rows in Python, you mathematically multiply the Customer Matrix by the Weight Vector. The computer does it all at once!

## E. Core Mathematical Concepts

### 1. Matrix Shape (Dimensions)
A matrix has rows (m) and columns (n). We denote this as `(m, n)`.
In AI: `(batch_size, features)` is the standard shape for input data.

### 2. Matrix Multiplication (Dot Product)
To multiply Matrix A by Matrix B, you take the dot product of the ROWS of A with the COLUMNS of B.
**CRITICAL RULE**: To multiply an `(m, n)` matrix by an `(n, p)` matrix, the inner dimensions `n` MUST match! The resulting shape will be `(m, p)`.

### 3. Transpose
Flipping a matrix over its diagonal, turning rows into columns and columns into rows.
In AI: We often have to transpose a Weight matrix to make the inner dimensions match for multiplication.

## F. Common Mistakes & Anti-Patterns
1. **Dimension Mismatch Error**: The most common error in Deep Learning (PyTorch/TensorFlow) is `RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x128 and 256x64)`. You must ensure the inner dimensions match (e.g., `128 != 256`).
2. **Confusing Element-wise Multiplication with Matrix Multiplication**:
   - `A * B` (in NumPy) multiplies them element-by-element (like adding corresponding pixels).
   - `A @ B` (or `np.dot(A, B)`) performs true Matrix Multiplication (dot products of rows/cols).

## G. Interview Connection
**Q: "Explain how a linear layer in a Neural Network computes its output."**
A: "A linear layer performs the operation `Y = XW^T + b`. Here, `X` is the input matrix of shape (batch_size, input_features). `W` is the weight matrix. We multiply them using matrix multiplication, which computes the dot product of every input with every weight vector, and then we add the bias vector `b`."

## H. Implementation & Guided Practice
"""

import numpy as np

# ==========================================
# 1. Basic Matrix Operations in NumPy
# ==========================================
def basic_matrix_math():
    print("--- 1. Basic Matrix Operations ---")
    
    # Create a 2x3 matrix
    A = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])
    print(f"Matrix A (shape {A.shape}):\n{A}")
    
    # Transpose (Swaps rows and columns -> becomes 3x2)
    A_T = A.T
    print(f"\nTranspose of A (shape {A_T.shape}):\n{A_T}")
    
    # Element-wise multiplication vs Matrix multiplication
    B = np.array([
        [1, 1, 1],
        [2, 2, 2]
    ])
    
    print(f"\nElement-wise (A * B):\n{A * B}")
    
    # Matrix Multiplication (Dot Product)
    # A is (2,3). To multiply, the second matrix MUST have 3 rows.
    # So we multiply A (2x3) by A_T (3x2). Result should be (2,2).
    dot_product = np.dot(A, A_T)
    # Python 3.5+ supports the @ operator for matrix multiplication!
    dot_product_at = A @ A_T 
    
    print(f"\nMatrix Multiplication (A @ A_T):\n{dot_product}")


# ==========================================
# 2. AI Application: Neural Network Forward Pass
# ==========================================
def neural_network_forward_pass():
    """
    This is EXACTLY what happens inside `torch.nn.Linear(3, 2)` in PyTorch!
    """
    print("\n--- 2. AI Application: Neural Network Forward Pass ---")
    
    # 1. Input Data (Batch of 4 items, 3 features each) -> Shape: (4, 3)
    # Features might be: [Age, Income, Credit Score]
    X = np.array([
        [25, 50000, 700],
        [45, 120000, 800],
        [30, 60000, 650],
        [22, 20000, 550]
    ])
    
    # 2. Weights (3 input features mapping to 2 output neurons) -> Shape: (3, 2)
    # Neuron 1 might predict "Loan Default Risk"
    # Neuron 2 might predict "Credit Card Approval"
    W = np.array([
        [0.1, -0.2],
        [0.5,  0.8],
        [-0.1, 0.4]
    ])
    
    # 3. Biases (1 for each output neuron) -> Shape: (2,)
    b = np.array([10.0, -5.0])
    
    print(f"Input X shape: {X.shape}")
    print(f"Weights W shape: {W.shape}")
    print(f"Biases b shape: {b.shape}")
    
    # 4. THE FORWARD PASS: Y = XW + b
    # X (4,3) @ W (3,2) -> Result is (4,2)
    # Then NumPy "broadcasts" the bias (2,) across all 4 rows.
    Z = (X @ W) + b
    
    print("\nOutput Predictions (Z):")
    print(Z)
    print(f"Output shape: {Z.shape} -> (4 items, 2 predictions each)")
    

# ==========================================
# 3. Debugging Exercise: Shape Mismatch
# ==========================================
def buggy_matrix_multiplication():
    print("\n--- 3. Debugging Exercise: Dimension Mismatch ---")
    A = np.array([[1, 2, 3], [4, 5, 6]]) # (2, 3)
    B = np.array([[1, 2], [3, 4]])       # (2, 2)
    
    print("Attempting to multiply A (2,3) with B (2,2)...")
    try:
        C = A @ B
    except ValueError as e:
        print(f"CRASH! ValueError caught: {e}")
        print("Fix: Inner dimensions must match! You cannot multiply (2,3) by (2,2).")


## I. Active Recall Questions
"""
1. What does it mean if you get `ValueError: mat1 and mat2 shapes cannot be multiplied (32x128 and 64x10)`?
   *Answer: You are trying to perform matrix multiplication, but the inner dimensions do not match. The first matrix has 128 columns, but the second matrix has 64 rows. They must be equal (e.g., 128x128).*
2. What is the difference between `A * B` and `A @ B` in Python/NumPy?
   *Answer: `A * B` is element-wise multiplication (multiplying position [0][0] with [0][0]). `A @ B` is actual Matrix Multiplication (taking the dot product of rows and columns).*
3. Why are GPUs used for Deep Learning?
   *Answer: Deep Learning is almost entirely composed of massive Matrix Multiplications. CPUs have a few powerful cores. GPUs have thousands of smaller cores designed specifically to perform thousands of dot products in parallel.*
"""

if __name__ == "__main__":
    print("========== LINEAR ALGEBRA: MATRICES MASTERCLASS ==========\n")
    basic_matrix_math()
    neural_network_forward_pass()
    buggy_matrix_multiplication()
    print("\n========== MASTERCLASS COMPLETE ==========")
