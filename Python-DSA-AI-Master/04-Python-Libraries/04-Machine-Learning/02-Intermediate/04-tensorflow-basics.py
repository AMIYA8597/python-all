'''
===========================================================================
Module: 04-tensorflow-basics
Description: A comprehensive textbook-grade interactive lesson on TensorFlow.
             This module covers the foundational aspects of TensorFlow 2.x,
             including Tensor creation, manipulation, mathematical operations,
             automatic differentiation, and custom training loops.

Learning Objectives:
1. Understand the core concept of Tensors and computational graphs.
2. Master basic and advanced Tensor manipulations (reshaping, slicing, broadcasting).
3. Comprehend the mathematical background of Automatic Differentiation (Autodiff)
   and the Jacobian matrix.
4. Analyze the Big-O time and space complexity of common Tensor operations.
5. Implement custom optimization loops using `tf.GradientTape`.
6. Solve real-world problems such as Linear Regression from scratch.

Mathematical Background:
------------------------
TensorFlow is essentially a framework for defining and executing computational
graphs, heavily relying on multi-dimensional arrays called Tensors.

1. Tensors:
   A scalar is a rank-0 tensor.
   A vector is a rank-1 tensor.
   A matrix is a rank-2 tensor.
   An n-dimensional array is a rank-n tensor.

2. Matrix Multiplication (MatMul):
   Given A of shape (N, M) and B of shape (M, P), their product C = A @ B
   has shape (N, P).
   The element C_{i,j} is calculated as:
   C_{i,j} = \sum_{k=1}^{M} A_{i,k} * B_{k,j}

3. Automatic Differentiation (Autodiff):
   Let f: R^n -> R^m be a differentiable function. The derivative of f with
   respect to its input is represented by the Jacobian matrix J of size m x n:
   J_{i,j} = \partial f_i / \partial x_j

   TensorFlow uses reverse-mode autodiff (backpropagation), which is highly
   efficient for computing gradients of scalar-valued functions (m=1) with
   respect to high-dimensional inputs (large n).
   Time Complexity of reverse-mode autodiff: O(C), where C is the time taken
   to evaluate the forward pass. This is incredibly powerful!

Big-O Analysis:
---------------
Let N be the number of elements in a tensor.
- Element-wise operations (Add, Mul, ReLU):
  Time Complexity: O(N)
  Space Complexity: O(N) for creating a new tensor.
- Matrix Multiplication (N x M) @ (M x P):
  Time Complexity: O(N * M * P) naive, practically faster due to BLAS/cuBLAS.
  Space Complexity: O(N * P) for the output tensor.
- Reduction operations (Sum, Mean, Max):
  Time Complexity: O(N)
  Space Complexity: O(1) or O(Remaining Dimensions)

Prerequisites:
- Basic understanding of Python, Linear Algebra, and Calculus.
===========================================================================
'''

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple, Callable

# Standard data science and machine learning imports
try:
    import numpy as np
    import tensorflow as tf
except ImportError:
    print("This module requires 'numpy' and 'tensorflow'.")
    print("Please install them using: pip install numpy tensorflow")
    sys.exit(1)


def section_1_tensor_creation_and_properties() -> None:
    """
    Section 1: Tensor Creation and Properties.
    
    This section explores how to instantiate Tensors from Python objects,
    NumPy arrays, and TensorFlow's built-in initialization functions.
    It also covers essential properties like shape, dtype, and rank.
    """
    print("\n" + "="*60)
    print("SECTION 1: TENSOR CREATION AND PROPERTIES")
    print("="*60)
    
    # 1. Scalar (Rank-0 Tensor)
    # A scalar has no axes and represents a single number.
    scalar: tf.Tensor = tf.constant(42)
    print(f"\n[1] Scalar (Rank 0):")
    print(f"Value: {scalar.numpy()}, Shape: {scalar.shape}, Dtype: {scalar.dtype}")
    
    # 2. Vector (Rank-1 Tensor)
    # A vector has one axis, like a list of numbers.
    vector: tf.Tensor = tf.constant([1.0, 2.0, 3.0, 4.0], dtype=tf.float32)
    print(f"\n[2] Vector (Rank 1):")
    print(f"Value: {vector.numpy()}, Shape: {vector.shape}, Rank: {tf.rank(vector).numpy()}")
    
    # 3. Matrix (Rank-2 Tensor)
    # A matrix has two axes, typical of tabular data or grayscale images.
    matrix: tf.Tensor = tf.constant([[1, 2], [3, 4], [5, 6]], dtype=tf.int32)
    print(f"\n[3] Matrix (Rank 2):")
    print(f"Value:\n{matrix.numpy()}")
    print(f"Shape: {matrix.shape}")
    
    # 4. Built-in initializers (Zeros, Ones, Random)
    # Big-O: O(N) time and space where N is the total number of elements.
    zeros_tensor: tf.Tensor = tf.zeros(shape=(3, 2))
    ones_tensor: tf.Tensor = tf.ones(shape=(2, 3))
    random_normal: tf.Tensor = tf.random.normal(shape=(2, 2), mean=0.0, stddev=1.0)
    
    print(f"\n[4] Built-in Initializers:")
    print(f"Zeros:\n{zeros_tensor.numpy()}")
    print(f"Random Normal:\n{random_normal.numpy()}")
    
    # 5. Conversion to and from NumPy
    # TensorFlow integrates seamlessly with NumPy. Calling .numpy() on a tensor
    # returns a copy (or view) of the tensor as a NumPy array.
    np_array: np.ndarray = np.array([1, 2, 3])
    converted_tensor: tf.Tensor = tf.convert_to_tensor(np_array)
    reconverted_np: np.ndarray = converted_tensor.numpy()
    
    assert np.array_equal(np_array, reconverted_np), "NumPy conversion failed."
    print("\n[5] NumPy Integration: Successfully converted between NumPy and TensorFlow.")


def section_2_tensor_manipulation() -> None:
    """
    Section 2: Tensor Manipulation (Indexing, Slicing, Reshaping).
    
    Tensors are immutable. Operations like reshaping or slicing do not modify
    the original tensor but return a new one. Under the hood, TF often shares
    the memory buffer, making slicing O(1) in many cases.
    """
    print("\n" + "="*60)
    print("SECTION 2: TENSOR MANIPULATION")
    print("="*60)
    
    # Let's create a rank-3 tensor for demonstration
    # Shape: (Batch, Height, Width) -> (2, 3, 4)
    tensor_3d: tf.Tensor = tf.constant([
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]
    ])
    
    print(f"\nOriginal 3D Tensor Shape: {tensor_3d.shape}")
    
    # 1. Indexing & Slicing
    # Python standard slicing semantics apply here: [start:stop:step]
    first_batch = tensor_3d[0]
    first_row_all_batches = tensor_3d[:, 0, :]
    
    print(f"\n[1] Indexing and Slicing:")
    print(f"First batch shape: {first_batch.shape}")
    print(f"First row of all batches shape: {first_row_all_batches.shape}")
    
    # 2. Reshaping
    # Reshaping changes the view without changing the underlying data order.
    # Total number of elements must remain constant.
    # Total elements = 2 * 3 * 4 = 24
    reshaped_1d: tf.Tensor = tf.reshape(tensor_3d, [-1]) # Flatten to 1D
    reshaped_2d: tf.Tensor = tf.reshape(tensor_3d, [6, 4]) # 6 rows, 4 columns
    
    print(f"\n[2] Reshaping:")
    print(f"Flattened shape: {reshaped_1d.shape}")
    print(f"Reshaped to 6x4:\n{reshaped_2d.numpy()}")
    
    # 3. Transposing
    # Transposing swaps the axes.
    # Time Complexity: O(N) where N is total elements, as data may be copied or re-strided.
    transposed: tf.Tensor = tf.transpose(reshaped_2d) # Becomes 4x6
    print(f"\n[3] Transpose Shape (from 6x4): {transposed.shape}")
    
    # 4. Expanding & Squeezing Axes
    # Adding or removing axes of length 1.
    expanded: tf.Tensor = tf.expand_dims(tensor_3d, axis=-1) # Becomes (2, 3, 4, 1)
    squeezed: tf.Tensor = tf.squeeze(expanded, axis=-1) # Back to (2, 3, 4)
    
    print(f"\n[4] Expanding & Squeezing:")
    print(f"Expanded shape: {expanded.shape}")
    print(f"Squeezed shape: {squeezed.shape}")
    
    assert tensor_3d.shape == squeezed.shape, "Squeeze failed."


def section_3_mathematics_and_broadcasting() -> None:
    """
    Section 3: Mathematical Operations and Broadcasting.
    
    Broadcasting is a powerful mechanism that allows TensorFlow to work with
    arrays of different shapes when performing arithmetic operations.
    
    Mathematical Rule for Broadcasting:
    Starting from the trailing dimension, two dimensions are compatible if:
    1. They are equal.
    2. One of them is 1.
    """
    print("\n" + "="*60)
    print("SECTION 3: MATHEMATICS AND BROADCASTING")
    print("="*60)
    
    # 1. Element-wise Operations
    a = tf.constant([1.0, 2.0, 3.0])
    b = tf.constant([4.0, 5.0, 6.0])
    
    add_res = tf.add(a, b) # or a + b
    mul_res = tf.multiply(a, b) # or a * b
    
    print(f"\n[1] Element-wise Operations:")
    print(f"a + b: {add_res.numpy()}")
    print(f"a * b: {mul_res.numpy()}")
    
    # 2. Broadcasting Example
    # Scalar to Vector
    scalar = tf.constant(10.0)
    broad_add = a + scalar # Scalar is broadcasted to [10.0, 10.0, 10.0]
    
    # Vector to Matrix
    matrix = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]) # Shape (2, 3)
    # 'a' has shape (3,), which is treated as (1, 3). It broadcasts over the 2 rows.
    broad_matrix_add = matrix + a 
    
    print(f"\n[2] Broadcasting:")
    print(f"a + 10: {broad_add.numpy()}")
    print(f"Matrix + Vector (Broadcasting):\n{broad_matrix_add.numpy()}")
    
    # 3. Matrix Multiplication (Dot Product)
    # Let X be (3, 2) and Y be (2, 4). The result Z will be (3, 4).
    # Time Complexity: O(3 * 2 * 4) = O(24) operations.
    X = tf.constant([[1, 2], [3, 4], [5, 6]])
    Y = tf.constant([[7, 8, 9, 10], [11, 12, 13, 14]])
    
    Z = tf.matmul(X, Y) # or X @ Y
    print(f"\n[3] Matrix Multiplication:")
    print(f"X shape: {X.shape}, Y shape: {Y.shape}")
    print(f"X @ Y shape: {Z.shape}")
    print(f"Result:\n{Z.numpy()}")
    
    # 4. Reductions (Sum, Mean, Max, Min)
    # Reducing a tensor collapses specific dimensions.
    # Time Complexity: O(N) where N is the number of elements in the reduced dimensions.
    total_sum = tf.reduce_sum(Z)
    row_sum = tf.reduce_sum(Z, axis=1) # Sum across columns (reduces axis 1)
    
    print(f"\n[4] Reductions:")
    print(f"Total Sum: {total_sum.numpy()}")
    print(f"Row Sum (axis=1): {row_sum.numpy()}")


def section_4_autodiff_and_gradients() -> None:
    """
    Section 4: Automatic Differentiation and Gradients.
    
    Automatic Differentiation (Autodiff) is the foundation of modern Deep Learning.
    TensorFlow provides the `tf.GradientTape` API for automatic differentiation.
    
    Mathematical Example:
    Let f(x) = x^2 + 2x + 1
    The derivative is f'(x) = 2x + 2
    At x = 3.0:
    f(3) = 9 + 6 + 1 = 16
    f'(3) = 2(3) + 2 = 8
    
    tf.GradientTape records operations executed inside its context manager
    onto a "tape" to compute gradients later.
    """
    print("\n" + "="*60)
    print("SECTION 4: AUTODIFF AND GRADIENTS")
    print("="*60)
    
    # 1. Gradient of a scalar function
    x = tf.Variable(3.0) # We use tf.Variable for trainable parameters
    
    with tf.GradientTape() as tape:
        y = x**2 + 2*x + 1
        
    # Compute the gradient of y with respect to x
    dy_dx = tape.gradient(y, x)
    
    print("\n[1] Gradient of Scalar Function: f(x) = x^2 + 2x + 1 at x=3")
    print(f"y  = {y.numpy()}")
    print(f"dy/dx = {dy_dx.numpy()} (Expected: 8.0)")
    
    # 2. Gradient of Vector-valued functions (Jacobian)
    # Let f(w) = w_1^2 + w_2^2
    w = tf.Variable([2.0, 3.0])
    
    with tf.GradientTape() as tape:
        z = w[0]**2 + w[1]**2
        
    dz_dw = tape.gradient(z, w)
    print("\n[2] Gradient of Multi-variable Function: f(w) = w1^2 + w2^2 at w=[2, 3]")
    print(f"dz/dw = {dz_dw.numpy()} (Expected: [4.0, 6.0])")
    
    # 3. Watching Tensors
    # By default, GradientTape only tracks tf.Variable. To track standard
    # tf.Tensor, we must explicitly call `tape.watch()`.
    const_tensor = tf.constant(4.0)
    with tf.GradientTape() as tape:
        tape.watch(const_tensor)
        out = const_tensor ** 3
        
    dout_dconst = tape.gradient(out, const_tensor)
    print("\n[3] Watching Constant Tensors: f(c) = c^3 at c=4")
    print(f"dout/dconst = {dout_dconst.numpy()} (Expected: 3*4^2 = 48.0)")
    
    # 4. Higher-order Derivatives
    # Nesting GradientTapes allows computing second derivatives (Hessian).
    # Let f(x) = x^3. f'(x) = 3x^2, f''(x) = 6x.
    x_val = tf.Variable(2.0)
    with tf.GradientTape() as tape2:
        with tf.GradientTape() as tape1:
            y_val = x_val ** 3
        dy_dx = tape1.gradient(y_val, x_val)     # First derivative
    d2y_dx2 = tape2.gradient(dy_dx, x_val)       # Second derivative
    
    print("\n[4] Higher-order Derivatives: f(x) = x^3 at x=2")
    print(f"First derivative (dy/dx): {dy_dx.numpy()} (Expected: 12.0)")
    print(f"Second derivative (d2y/dx2): {d2y_dx2.numpy()} (Expected: 12.0)")


def section_5_custom_training_loop() -> None:
    """
    Section 5: Custom Training Loop - Optimization from Scratch.
    
    We will build a simple custom training loop using Gradient Descent to find
    the minimum of a mathematical function.
    
    Objective Function (Loss): f(x) = (x - 4)^2
    The minimum is obviously at x = 4, where f(4) = 0.
    
    Algorithm (Gradient Descent):
    x_{t+1} = x_t - learning_rate * \nabla f(x_t)
    
    Time Complexity per step: O(1) for this scalar function.
    """
    print("\n" + "="*60)
    print("SECTION 5: CUSTOM TRAINING LOOP (OPTIMIZATION)")
    print("="*60)
    
    # Initialize parameter at a random guess
    x = tf.Variable(-10.0)
    learning_rate = 0.1
    epochs = 50
    
    print(f"Initial x: {x.numpy():.4f}")
    
    # Training Loop
    start_time = time.time()
    for epoch in range(epochs):
        with tf.GradientTape() as tape:
            # Forward pass: compute loss
            loss = (x - 4.0) ** 2
            
        # Backward pass: compute gradient
        grad = tape.gradient(loss, x)
        
        # Optimizer step (Gradient Descent)
        # x.assign_sub performs: x = x - learning_rate * grad
        x.assign_sub(learning_rate * grad)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1:02d}: Loss = {loss.numpy():.4f}, x = {x.numpy():.4f}")
            
    end_time = time.time()
    
    print(f"\nOptimization finished in {end_time - start_time:.4f} seconds.")
    print(f"Final x value: {x.numpy():.4f} (Expected: ~4.0)")
    print("This demonstrates the core mechanism behind training Deep Learning models.")


def section_6_real_world_application() -> None:
    """
    Section 6: Real-World Application - Linear Regression.
    
    Let's apply our knowledge to a practical Machine Learning problem.
    We will generate synthetic data for a linear relationship with noise,
    and then train a Linear Regression model from scratch.
    
    Mathematical Model:
    y_pred = W * X + b
    
    Loss Function (Mean Squared Error - MSE):
    L = (1/N) * \sum_{i=1}^{N} (y_true_i - y_pred_i)^2
    """
    print("\n" + "="*60)
    print("SECTION 6: REAL-WORLD APPLICATION (LINEAR REGRESSION)")
    print("="*60)
    
    # 1. Generate Synthetic Data
    # True relationship: y = 3.5 * X + 1.2
    N_SAMPLES = 1000
    true_W = 3.5
    true_b = 1.2
    
    # Random normal inputs X
    X = tf.random.normal(shape=(N_SAMPLES, 1))
    # Gaussian noise
    noise = tf.random.normal(shape=(N_SAMPLES, 1), mean=0.0, stddev=0.5)
    
    # Target variables Y
    Y = true_W * X + true_b + noise
    
    print(f"Dataset generated. Shape of X: {X.shape}, Shape of Y: {Y.shape}")
    print(f"True parameters: W = {true_W}, b = {true_b}")
    
    # 2. Define the Model
    class LinearRegressionModel:
        def __init__(self) -> None:
            # Initialize weights randomly, bias to 0
            self.W = tf.Variable(tf.random.normal(shape=(1, 1), mean=0.0, stddev=1.0))
            self.b = tf.Variable(tf.zeros(shape=(1,)))
            
        def __call__(self, x: tf.Tensor) -> tf.Tensor:
            # Forward pass: W * x + b
            return tf.matmul(x, self.W) + self.b
            
    model = LinearRegressionModel()
    
    # 3. Define the Loss Function (MSE)
    def mse_loss(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
        return tf.reduce_mean(tf.square(y_true - y_pred))
        
    # 4. Training Loop
    epochs = 200
    learning_rate = 0.05
    
    print("\nTraining started...")
    start_time = time.time()
    
    for epoch in range(epochs):
        with tf.GradientTape() as tape:
            # Forward pass
            predictions = model(X)
            # Compute loss
            loss = mse_loss(Y, predictions)
            
        # Backward pass
        gradients = tape.gradient(loss, [model.W, model.b])
        
        # Gradient Descent step
        model.W.assign_sub(learning_rate * gradients[0])
        model.b.assign_sub(learning_rate * gradients[1])
        
        if (epoch + 1) % 40 == 0:
            print(f"Epoch {epoch+1:03d} | Loss: {loss.numpy():.4f} | "
                  f"W: {model.W.numpy()[0][0]:.4f} | b: {model.b.numpy()[0]:.4f}")
                  
    end_time = time.time()
    print(f"\nTraining completed in {end_time - start_time:.4f} seconds.")
    print(f"Learned Parameters : W = {model.W.numpy()[0][0]:.4f}, b = {model.b.numpy()[0]:.4f}")
    print(f"True Parameters    : W = {true_W:.4f}, b = {true_b:.4f}")
    
    # Evaluate accuracy simply by checking how close parameters are
    w_error = abs(model.W.numpy()[0][0] - true_W)
    b_error = abs(model.b.numpy()[0] - true_b)
    
    if w_error < 0.2 and b_error < 0.2:
        print("-> The model successfully converged to the true parameters!")
    else:
        print("-> The model failed to converge optimally.")


def run_tests() -> None:
    """
    Test Suite: Ensuring structural correctness and math consistency.
    This suite acts as an integrated unit test to validate the fundamental
    expectations of TensorFlow operations taught in this lesson.
    """
    print("\n" + "="*60)
    print("TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Tensor types and shapes
        a = tf.constant([[1, 2], [3, 4]])
        assert a.shape == (2, 2), "Test 1 Failed: Shape mismatch."
        assert a.dtype == tf.int32, "Test 1 Failed: Dtype mismatch."
        
        # Test 2: Broadcasting addition
        b = tf.constant([10, 20])
        c = a + b
        expected_c = np.array([[11, 22], [13, 24]])
        assert np.array_equal(c.numpy(), expected_c), "Test 2 Failed: Broadcasting addition."
        
        # Test 3: Matrix multiplication
        x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
        y = tf.constant([[5.0, 6.0], [7.0, 8.0]])
        z = tf.matmul(x, y)
        expected_z = np.array([[19.0, 22.0], [43.0, 50.0]])
        assert np.array_equal(z.numpy(), expected_z), "Test 3 Failed: MatMul."
        
        # Test 4: Autodiff
        v = tf.Variable(3.0)
        with tf.GradientTape() as tape:
            loss = v ** 3
        grad = tape.gradient(loss, v)
        assert tf.math.abs(grad - 27.0) < 1e-5, "Test 4 Failed: Autodiff."
        
        print("All internal tests passed successfully! "
              "The library behaves exactly as detailed in the lesson.")
              
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """
    Main Execution Block.
    Running this module will guide the user through the interactive lesson.
    """
    print("******************************************************************")
    print("        WELCOME TO THE TENSORFLOW BASICS MASTERCLASS              ")
    print("******************************************************************")
    print("This script will guide you through the fundamental concepts of")
    print("TensorFlow, including Tensors, Operations, Autodiff, and basic ML.")
    print("Ensure you read the source code comments for theoretical insights!")
    
    time.sleep(1)
    section_1_tensor_creation_and_properties()
    
    time.sleep(1)
    section_2_tensor_manipulation()
    
    time.sleep(1)
    section_3_mathematics_and_broadcasting()
    
    time.sleep(1)
    section_4_autodiff_and_gradients()
    
    time.sleep(1)
    section_5_custom_training_loop()
    
    time.sleep(1)
    section_6_real_world_application()
    
    time.sleep(1)
    run_tests()
    
    print("\n" + "*"*66)
    print("    CONGRATULATIONS! YOU COMPLETED THE TENSORFLOW BASICS MODULE.  ")
    print("*"*66 + "\n")
