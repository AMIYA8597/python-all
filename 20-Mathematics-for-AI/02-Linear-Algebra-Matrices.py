"""
# ==============================================================================
# LABORATORY: MATHEMATICS FOR AI (LINEAR ALGEBRA & MATRICES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a Neural Network using a `for` loop to multiply 
# $1,000$ inputs against $1,000$ weights. The CPU executes $1,000,000$ operations 
# sequentially. It takes 5 seconds to run one forward pass.
#
# A senior AI engineer understands "Matrix Multiplication". They pack all $1,000$ 
# inputs into a single Matrix (X) and all $1,000$ weights into a single Matrix (W). 
# They execute a single mathematical command: `X @ W`. The GPU intercepts this 
# matrix operation and executes all $1,000,000$ calculations in parallel across 
# thousands of CUDA cores. The forward pass completes in 0.001 seconds. 
# AI is impossible without Matrix Mathematics.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Matrix Dimensions (Rows x Columns).
# - Execute the Dot Product (Matrix Multiplication).
# - Architect Matrix Transposition ($W^T$) to align dimensions.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (MATRIX MATHEMATICS)
# ==============================================================================
class MatrixMathematics:
    
    @staticmethod
    def simulate_neural_network_layer():
        """
        [SECURE] Matrix Multiplication (The Forward Pass).
        Formula: Output = X @ W
        (M x N) @ (N x P) = (M x P)
        """
        print("  [INIT] Simulating a Neural Network Dense Layer via Matrices...")
        
        # 1. The Input Matrix (X)
        # Represents 2 samples, each with 3 features. Dimensions: (2 x 3)
        X = np.array([
            [1.0, 2.0, 3.0],  # Sample 1
            [4.0, 5.0, 6.0]   # Sample 2
        ])
        
        # 2. The Weights Matrix (W)
        # Represents 3 input features mapped to 4 output neurons. Dimensions: (3 x 4)
        W = np.array([
            [0.1, 0.2, 0.3, 0.4],
            [0.5, 0.6, 0.7, 0.8],
            [0.9, 1.0, 1.1, 1.2]
        ])
        
        print(f"  -> Matrix X Dimensions: {X.shape} (Batch=2, Features=3)")
        print(f"  -> Matrix W Dimensions: {W.shape} (Input=3, Output=4)")
        
        # 3. The Matrix Multiplication (Dot Product)
        # The inner dimensions MUST match! (2 x 3) @ (3 x 4) -> Valid!
        # The result will take the outer dimensions: (2 x 4)
        output = np.dot(X, W)
        
        print(f"\n  [EXECUTION] Calculating (X @ W)...")
        print(f"  -> Output Matrix Dimensions: {output.shape} (Batch=2, Output=4)")
        print(f"  -> Output Matrix Values:\n{output}")

    @staticmethod
    def simulate_transposition():
        """
        [SECURE] Matrix Transposition.
        Swaps rows and columns. Required to fix dimension mismatches during Backpropagation.
        """
        print("\n  [INIT] Simulating Matrix Transposition ($W^T$)...")
        
        # Original Matrix (3 x 2)
        W = np.array([
            [1, 2],
            [3, 4],
            [5, 6]
        ])
        
        print(f"  -> Original W Dimensions: {W.shape}")
        print(f"  -> W Values:\n{W}")
        
        # Transposed Matrix (2 x 3)
        W_T = W.T
        
        print(f"\n  -> Transposed W^T Dimensions: {W_T.shape}")
        print(f"  -> W^T Values:\n{W_T}")
        
        print("\n  [MATHEMATICAL PROOF] The columns mathematically became the rows. ")
        print("  This geometric rotation is strictly required to route Error Gradients ")
        print("  backwards through the network during training.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_matrices():
    section_header("Mathematics for AI: Matrices")
    
    math = MatrixMathematics()
    math.simulate_neural_network_layer()
    math.simulate_transposition()


def run_all_labs():
    demonstrate_matrices()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Matrix A is (128, 512) and Matrix B is (256, 512), can you mathematically calculate A @ B?"
   Senior Answer: "No, a Dimension Mismatch Error will occur. The fundamental rule of Matrix Multiplication states that the inner dimensions must exactly match. A is $(128 \\times 512)$ and B is $(256 \\times 512)$. The inner dimensions ($512$ and $256$) do not equal each other. To solve this, we must Transpose Matrix B to align the geometry. By calculating $A \\cdot B^T$, the operation becomes $(128 \\times 512) \\cdot (512 \\times 256)$. The inner $512$ dimensions now match, and the resulting output matrix will geometrically collapse to the outer dimensions: $(128 \\times 256)$."

2. Interviewer: "What is 'Broadcasting' in NumPy, and why is it mathematically dangerous if misused?"
   Senior Answer: "Implicit Dimension Expansion. If you add a Matrix $(100 \\times 100)$ and a scalar Vector $(1 \\times 100)$, NumPy will not throw an error. It will automatically 'Broadcast' (duplicate) the vector $100$ times to match the matrix dimensions and execute the addition. This is incredibly useful for adding Biases ($X \\cdot W + B$). However, it is mathematically dangerous because if you accidentally slice an array incorrectly and end up with a $(100 \\times 1)$ array instead of a $(100,)$ vector, NumPy will silently broadcast it across the wrong axis, creating a massive $(100 \\times 100)$ matrix of garbage data without throwing an error."

3. Interviewer: "Why are GPUs strictly required for Matrix Multiplication in Large Language Models?"
   Senior Answer: "SIMD Architecture. A standard CPU has 16 powerful cores designed for complex sequential logic. A GPU has $10,000$ weak cores designed for SIMD (Single Instruction, Multiple Data). Matrix Multiplication ($X \\cdot W$) is purely a collection of millions of independent dot products (multiply-adds) that do not rely on each other. A CPU calculates them one by one. A GPU mathematically maps each pixel/neuron to a dedicated CUDA core and computes all $1,000,000$ multiplications simultaneously on a single clock cycle."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Mathematics for AI (Matrices) Completed.")
