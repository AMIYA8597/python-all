"""
## A. Concept Name
Mathematics for Machine Learning

## B. Analogy
Think of Math in ML as the engine of a car. You don't necessarily need to know how to build the engine from scratch to drive the car (use ML libraries), but understanding how the engine works allows you to tune it, fix it when it breaks, and build better models.

## C. Core Idea
Machine Learning is fundamentally applied mathematics. It relies heavily on Linear Algebra for data representation, Calculus for optimization, and Statistics for making inferences from data.

## D. Why it Matters
Without math, ML algorithms are "black boxes." Math provides the theoretical foundation to understand why an algorithm works, choose the right model, and diagnose problems like overfitting or slow convergence.

## E. Real-World Example
- Linear Algebra: Recommender systems using matrix factorization (like Netflix).
- Calculus: Training neural networks using backpropagation (Gradient Descent).
- Statistics: A/B testing on websites to determine which layout yields higher conversion rates.

## F. Prerequisites
- Basic algebra and arithmetic
- Python programming (NumPy, SciPy)

## G. Linear Algebra
Deals with vectors, matrices, and linear transformations. Essential for handling high-dimensional data (e.g., images, text).

## H. Calculus
Focuses on rates of change. In ML, partial derivatives and gradients are used to minimize error functions (loss) during model training.

## I. Statistics & Probability
Provides the framework for quantifying uncertainty, evaluating model performance, and understanding data distributions.

## J. Optimization
The bridge between calculus and ML. Finding the minimum of a loss function to get the best model parameters.

## K. Common Operations (Linear Algebra)
Dot product, matrix multiplication, transpose, inverse, eigenvectors/eigenvalues.

## L. Common Operations (Calculus)
Derivatives (analytical and numerical), gradients, chain rule.

## M. Common Operations (Statistics)
Mean, median, variance, standard deviation, probability distributions (e.g., Normal/Gaussian).

## N. NumPy for Math
Python's `numpy` library is the industry standard for numerical computing, providing highly optimized C-based operations for vectors and matrices.

## O. SciPy for Statistics
`scipy.stats` extends NumPy with advanced statistical functions and probability distributions.

## P. Matplotlib for Visualization
Visualizing data and mathematical functions is crucial for intuition. `matplotlib.pyplot` is the standard tool.

## Q. Complexity / Performance
Vectorized operations in NumPy are significantly faster compared to Python `for` loops. Always vectorize when possible!

## R. Edge Cases & Pitfalls
- Matrix multiplication dimension mismatches.
- Singular matrices (cannot be inverted).
- Numerical instability in calculus.

## S. Best Practices
- Use `np.dot` or the `@` operator for matrix multiplication.
- Prefer numerical stability (e.g., using log-probabilities).
- Always check the shape of your arrays (`arr.shape`) when debugging.

## T. Debugging Tips
If a mathematical operation fails, print the `.shape` and `.dtype` of your arrays. 90% of linear algebra errors in ML are dimension mismatches.

## U. Exercises
1. Implement a function to calculate the Euclidean distance between two vectors.
2. Manually verify the matrix multiplication result of two 3x3 matrices.
3. Write a gradient descent step for the function f(x) = x^2 + 5x + 6.

## V. Related Concepts
- Principal Component Analysis (PCA)
- Gradient Descent
- Bayesian Inference

## W. Summary
Math is the language of ML. Linear algebra organizes the data, calculus optimizes the learning, and statistics validates the results.

## X. Project Connection
In any ML project, you will represent your dataset as a matrix (Linear Algebra), use optimization algorithms to train your model (Calculus), and evaluate its accuracy (Statistics). The operations in this file are the building blocks of every model you will build.
"""

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def linear_algebra_basics():
    print("--- Linear Algebra Basics ---")
    # Vectors
    v = np.array([1, 2, 3])
    u = np.array([4, 5, 6])
    print(f"Vector v: {v}")
    print(f"Vector u: {u}")
    print(f"Dot product: np.dot(v, u) = {np.dot(v, u)}")
    
    # Matrices
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(f"\nMatrix A:\n{A}")
    print(f"Matrix B:\n{B}")
    
    print(f"\nMatrix Multiplication A @ B:\n{A @ B}")
    
    # Matrix Transpose
    print(f"\nTranspose of A:\n{A.T}")
    
    # Matrix Inverse
    A_inv = np.linalg.inv(A)
    print(f"\nInverse of A:\n{A_inv}")
    print(f"A @ A_inv (Should be Identity Matrix):\n{np.round(A @ A_inv, 2)}")
    
    # Eigenvalues and Eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"\nEigenvalues of A: {eigenvalues}")
    print(f"Eigenvectors of A:\n{eigenvectors}")

def calculus_basics():
    print("\n--- Calculus Basics ---")
    # In ML, calculus is mostly about finding gradients for optimization (like Gradient Descent).
    # Let's approximate a derivative numerically.
    # Function: f(x) = x^2
    # Derivative: f'(x) = 2x
    
    def f(x):
        return x**2
        
    def numerical_derivative(f, x, h=1e-5):
        return (f(x + h) - f(x)) / h
        
    x = 3.0
    print(f"Function: f(x) = x^2")
    print(f"Numerical Derivative at x={x}: {numerical_derivative(f, x)}")
    print(f"Analytical Derivative at x={x}: {2 * x}")

def statistics_basics():
    print("\n--- Statistics Basics ---")
    data = np.array([2, 4, 4, 4, 5, 5, 7, 9])
    print(f"Data: {data}")
    
    # Mean, Median, Variance, Standard Deviation
    print(f"Mean: {np.mean(data)}")
    print(f"Median: {np.median(data)}")
    print(f"Variance: {np.var(data)}")
    print(f"Standard Deviation: {np.std(data)}")
    
    # Probability Distributions
    print("\nNormal Distribution Example:")
    # Generating normal distribution data
    mu, sigma = 0, 0.1 # mean and standard deviation
    s = np.random.normal(mu, sigma, 1000)
    print(f"Generated 1000 samples with mean {mu} and std {sigma}.")
    print(f"Sample mean: {np.mean(s):.4f}")
    print(f"Sample std: {np.std(s):.4f}")

if __name__ == "__main__":
    linear_algebra_basics()
    calculus_basics()
    statistics_basics()
