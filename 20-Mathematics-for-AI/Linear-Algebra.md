# Linear Algebra for AI

## Prerequisites
- Basic understanding of Python and array programming (e.g., NumPy).
- Familiarity with basic algebra (variables, equations, and coordinates).
- Basic geometric understanding (points and lines in 2D/3D space).

## Objectives
- Understand **Vectors** and **Matrices** as the primary data structures for AI.
- Grasp vector operations (**Dot Products**) and their geometric intuition.
- Understand matrix multiplication as **Linear Transformations**.
- Learn the concepts of **Eigenvalues** and **Eigenvectors**.
- See how **PCA** (Principal Component Analysis) uses linear algebra for dimensionality reduction.
- Explicitly connect these mathematical foundations to ML/AI algorithms (e.g., neural network layers, similarity metrics).

## Intuition
Linear algebra is the foundational language of data in Machine Learning. In AI, almost all data—be it images, text, or sound—is transformed into arrays of numbers known as tensors.
- **Vectors:** Think of vectors as points in space or arrows. In ML, a vector typically represents a single data point's features (e.g., a patient's age, blood pressure, and heart rate).
- **Matrices:** Matrices are collections of vectors. They can represent an entire dataset (rows are examples, columns are features) or a linear transformation (like the weights connecting neurons in a neural network).
- **Dot Products:** A measure of similarity or alignment between two vectors. Used extensively in cosine similarity, attention mechanisms in transformers, and basic neural network activations.
- **Transformations:** Multiplying an input vector by a matrix translates, rotates, or scales the vector into a new space.
- **Eigenvalues/Eigenvectors:** Reveal the intrinsic fundamental axes of data. They are crucial for understanding how data varies and form the mathematical bedrock for Principal Component Analysis (PCA).

## Mathematics

### 1. Vectors and Matrices
A vector $\mathbf{v} \in \mathbb{R}^n$ is an $n$-tuple of real numbers.
A matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$ is a rectangular array with $m$ rows and $n$ columns.

### 2. Dot Products
For vectors $\mathbf{a}, \mathbf{b} \in \mathbb{R}^n$, the algebraic dot product is:
$$ \mathbf{a} \cdot \mathbf{b} = \sum_{i=1}^n a_i b_i $$
Geometrically, it relates to the angle $\theta$ between them:
$$ \mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\| \|\mathbf{b}\| \cos(\theta) $$
**AI Connection**: If $\mathbf{a}$ and $\mathbf{b}$ are normalized (length 1), the dot product is exactly $\cos(\theta)$. A dot product near $1$ means the vectors are highly similar (pointing in the same direction), $0$ means they are orthogonal (uncorrelated), and $-1$ means opposite. This is the basis of similarity search and recommender systems.

### 3. Linear Transformations (Matrix Multiplication)
For $\mathbf{A} \in \mathbb{R}^{m \times n}$ and $\mathbf{B} \in \mathbb{R}^{n \times p}$, their product $\mathbf{C} = \mathbf{A}\mathbf{B}$ is an $m \times p$ matrix formed by taking the dot product of rows of $\mathbf{A}$ and columns of $\mathbf{B}$.
**AI Connection**: A single layer in a feedforward neural network computes $\mathbf{y} = \sigma(\mathbf{W}\mathbf{x} + \mathbf{b})$, where $\mathbf{W}$ is a weight matrix. Multiplying by $\mathbf{W}$ transforms the input features $\mathbf{x}$ into a new representation.

### 4. Eigenvalues and Eigenvectors
For a square matrix $\mathbf{A}$, a non-zero vector $\mathbf{v}$ is an eigenvector if applying $\mathbf{A}$ to it only scales it, without changing its direction:
$$ \mathbf{A}\mathbf{v} = \lambda \mathbf{v} $$
where $\lambda$ is a scalar known as the eigenvalue.

### 5. Principal Component Analysis (PCA)
**AI Connection**: PCA is a dimensionality reduction technique. It calculates the covariance matrix of the data and finds its eigenvectors. These eigenvectors represent the directions (principal components) of maximum variance in the data. The corresponding eigenvalues tell us how much variance is captured along each eigenvector. By keeping only the top $k$ eigenvectors, we compress the data while retaining the most critical information.

## Code Connection
```python
import numpy as np

# 1. Vectors & Dot Product (Similarity)
v1 = np.array([1, 2, 3])
v2 = np.array([4, -5, 6])
dot_product = np.dot(v1, v2)
print(f"Dot Product: {dot_product}")

# 2. Matrices & Linear Transformations (Neural Net Layer)
W = np.random.randn(4, 3) # Weight matrix (4 output neurons, 3 input features)
x = np.random.randn(3, 1) # Input feature vector
bias = np.random.randn(4, 1)
y = W @ x + bias          # Linear transformation
print(f"Output shape: {y.shape}")

# 3. Eigenvalues & Eigenvectors for PCA
A = np.array([[2.5, 0.5], 
              [0.5, 1.5]]) # Sample covariance matrix
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Eigenvalues: {eigenvalues}")
print(f"Eigenvectors:\n{eigenvectors}")
```
*(Refer to `01-Linear-Algebra-Vectors.py`, `02-Linear-Algebra-Matrices.py`, and `04-PCA-and-Eigenvectors.py` for hands-on, runnable scripts).*

## Interview Questions
1. **How do you geometrically interpret the dot product of two vectors, and why is it useful in NLP?**
   - *Answer*: Geometrically, the dot product is related to the cosine of the angle between two vectors. In NLP, word embeddings (like Word2Vec) represent words as vectors. The dot product (or cosine similarity) between two word vectors measures their semantic similarity.
2. **What does a matrix-vector multiplication represent in a Neural Network?**
   - *Answer*: It represents a linear transformation mapping the input features from one vector space to another. The matrix contains the learned weights of the network layer.
3. **Can you explain PCA intuitively using Eigenvectors?**
   - *Answer*: PCA aims to find the axes along which the data varies the most to reduce dimensionality while preserving information. These optimal axes (principal components) are exactly the eigenvectors of the data's covariance matrix, and the eigenvalues indicate the magnitude of variance explained by each axis.
