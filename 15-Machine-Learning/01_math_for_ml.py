"""
# ==============================================================================
# LABORATORY: MACHINE LEARNING (MATHEMATICS FOR ML)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses `sklearn.linear_model.LinearRegression`. They pass in 
# a dataset with 5 features and 1,000 rows. The model outputs a prediction. 
# They have absolutely no idea what physically occurred inside the computer. 
# It is just "AI Magic".
#
# A senior AI engineer understands Linear Algebra. They know that the dataset is 
# a Matrix (1000 x 5) and the Model Weights are a Vector (5 x 1). They know the 
# prediction is mathematically just a Dot Product (Matrix Multiplication). Because 
# they understand the math, they know exactly how to scale the hardware (GPUs), 
# debug exploding gradients in Calculus, and optimize the dimensional shapes 
# to prevent catastrophic crashes in Production.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Linear Algebra (Vectors, Matrices, Dot Products).
# - Execute matrix dimensionality alignment.
# - Architect foundational Calculus (The Derivative / Gradient).
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (LINEAR ALGEBRA & DOT PRODUCTS)
# ==============================================================================
class MathematicalEngine:
    
    @staticmethod
    def execute_dot_product():
        """
        Simulates how a Neural Network makes a prediction (Forward Pass).
        """
        print("  [INIT] Simulating Neural Network Forward Pass...")
        
        # 1. The Inputs (e.g., A house has 3 bedrooms, 2 baths, 1500 sqft)
        # This is a 1D Vector (Shape: 3)
        features = np.array([3.0, 2.0, 1500.0])
        print(f"  -> Input Features Vector: {features} (Shape: {features.shape})")
        
        # 2. The Weights (The learned parameters of the ML Model)
        # This is a 1D Vector (Shape: 3)
        weights = np.array([50000.0, 25000.0, 150.0])
        print(f"  -> Model Weights Vector:  {weights} (Shape: {weights.shape})")
        
        # 3. The Bias (The Y-intercept)
        bias = 10000.0
        
        # 4. THE DOT PRODUCT
        # Math: (3 * 50,000) + (2 * 25,000) + (1500 * 150) + Bias
        # This is executed in C / Assembly language under the hood!
        prediction = np.dot(features, weights) + bias
        
        print(f"\n  [EXECUTION] np.dot(features, weights) + bias")
        print(f"  -> Predicted House Price: ${prediction:,.2f}")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: MATRIX MULTIPLICATION
    # --------------------------------------------------------------------------
    @staticmethod
    def execute_matrix_multiplication():
        """
        Simulates how a GPU processes a "Batch" of 4 houses simultaneously.
        """
        print("\n  [INIT] Simulating GPU Batch Processing (Matrix Math)...")
        
        # A Matrix! (4 rows, 3 columns). Shape: (4, 3)
        # 4 Houses, 3 Features each.
        batch_features = np.array([
            [3.0, 2.0, 1500.0],
            [4.0, 3.0, 2000.0],
            [2.0, 1.0, 900.0],
            [5.0, 4.0, 3500.0]
        ])
        print(f"  -> Batch Features Matrix Shape: {batch_features.shape}")
        
        # The Weights must be reshaped to align!
        # From Shape (3,) to a Column Vector Shape (3, 1)
        weights_col = np.array([[50000.0], [25000.0], [150.0]])
        print(f"  -> Weights Column Vector Shape: {weights_col.shape}")
        
        # 4. MATRIX MULTIPLICATION (A @ B)
        # Mathematical Rule: Inner dimensions must match! (4, 3) @ (3, 1) = (4, 1)
        predictions = np.matmul(batch_features, weights_col) + 10000.0
        
        print(f"\n  [EXECUTION] np.matmul(Batch, Weights)")
        print(f"  -> Resulting Shape: {predictions.shape}")
        for i, pred in enumerate(predictions):
            print(f"    -> House {i+1} Prediction: ${pred[0]:,.2f}")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_math():
    section_header("Machine Learning: Mathematical Foundations")
    
    MathematicalEngine.execute_dot_product()
    MathematicalEngine.execute_matrix_multiplication()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By packing multiple rows into a single Matrix (Batch), the ML Engineer ")
    print("  mathematically delegates the 'for loop' to the GPU. The GPU uses ")
    print("  SIMD to calculate all 4 predictions in the exact same clock cycle.")


def run_all_labs():
    demonstrate_math()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Matrix A has shape $(100, 10)$ and Matrix B has shape $(5, 10)$, can you mathematically perform $A \\cdot B$ (Matrix Multiplication)?"
   Senior Answer: "No, Dimensionality Mismatch. The absolute law of Matrix Multiplication is that the inner dimensions must match: $(M \\times N) \\cdot (N \\times K) = (M \\times K)$. Matrix A's inner dimension is $10$. Matrix B's outer dimension is $5$. $10 \\neq 5$. The compiler will violently crash with a `ValueError`. To solve this mathematically, we must apply a Transpose operation to Matrix B ($B^T$), flipping it to $(10, 5)$. Then, $(100, 10) \\cdot (10, 5)$ mathematically resolves to a perfectly valid $(100, 5)$ output matrix."

2. Interviewer: "What is a 'Tensor', and how does it relate to Vectors and Matrices in Deep Learning?"
   Senior Answer: "An N-Dimensional Array. A Scalar is a $0$-dimensional Tensor (a single number like `5`). A Vector is a $1$-dimensional Tensor (`[1, 2, 3]`). A Matrix is a $2$-dimensional Tensor (rows and columns). In Deep Learning (e.g., PyTorch or TensorFlow), we process images. A color image has height, width, and $3$ color channels (RGB), making it a $3D$ Tensor. If we process a Batch of $64$ images simultaneously on a GPU, the data structure mathematically becomes a $4D$ Tensor of shape `(64, 3, 224, 224)`. 'TensorFlow' literally means the flow of these multi-dimensional arrays through the mathematical operations of the network."

3. Interviewer: "Why do we use Calculus (Derivatives) in Machine Learning training?"
   Senior Answer: "Gradient Descent Optimization. When an ML model makes a prediction, we calculate the Error (Cost Function). Our goal is to minimize this Error. In Calculus, the derivative of a function at a specific point mathematically represents the slope of the tangent line (the instantaneous rate of change). By calculating the derivative (the Gradient) of the Error with respect to every single Weight in the network, we mathematically discover the exact direction to adjust the Weights to make the Error go down. We then step in the opposite direction of the gradient to reach the local minimum."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Machine Learning (Math Foundations) Completed.")
