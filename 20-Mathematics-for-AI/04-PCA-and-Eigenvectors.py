"""
# 04 - Linear Algebra: Eigenvectors & Dimensionality Reduction (PCA)

## A. Concept Name
Eigenvectors, Eigenvalues, and Principal Component Analysis (PCA).

## B. One-Sentence Definition
PCA is a mathematical technique that uses Eigenvectors to compress data by finding the directions (components) where the data varies the most, allowing us to reduce a 1000-dimensional dataset down to 2 or 3 dimensions while keeping most of the information.

## C. Why Does This Exist?
Real-world AI datasets have hundreds of columns (features). 
1. **The Curse of Dimensionality**: Too many features make ML models overfit and train incredibly slowly.
2. **Visualization**: Humans can only see in 2D or 3D. We cannot plot a 1000-dimensional dataset to see if there are clusters.
PCA solves both by mathematically squishing the data into fewer dimensions.

## D. Intuition & Real-World Analogy
Imagine a 3D cloud of points shaped like a giant pancake floating in the air. 
Even though the points exist in 3D (x, y, z), almost all the "shape" of the pancake is along 2 dimensions (its width and length). Its thickness is tiny.
If you took a photograph of the pancake from directly above, you'd capture 99% of its shape in a 2D image.
PCA is the mathematical camera. It finds the best angle to take the photo so you lose the least amount of information.
- The **Eigenvectors** are the axes of the camera (where it points).
- The **Eigenvalues** are how much information (variance) is captured by each axis.

## E. Core Mathematical Concepts

### 1. Covariance Matrix
Before doing PCA, we need to know how every feature relates to every other feature. The Covariance Matrix captures this. If Feature A goes up, does Feature B go up?

### 2. Eigenvectors
An Eigenvector of a matrix is a special vector that, when multiplied by the matrix, DOES NOT CHANGE DIRECTION, it only scales in size. In PCA, the eigenvectors of the Covariance Matrix represent the "Principal Components" (the new axes for our data).

### 3. Eigenvalues
A number attached to an Eigenvector telling you how much it scaled. In PCA, it tells you exactly how much "Variance" (information) is captured by that specific component.

## F. Common Mistakes & Anti-Patterns
1. **Forgetting to Standardize**: PCA is highly sensitive to the scale of the data. If 'Age' is 0-100 and 'Income' is 0-100,000, PCA will think Income is the only thing that matters because the variance is numerically larger. You MUST use Standard Scaler (mean=0, variance=1) before PCA.
2. **Using PCA on non-linear data**: PCA only finds linear correlations. If your data is shaped like a spiral, PCA will fail. You need t-SNE or UMAP for non-linear manifold learning.

## G. Interview Connection
**Q: "How do you decide how many Principal Components to keep?"**
A: "We look at the Explained Variance Ratio. We sort the eigenvalues from highest to lowest and calculate a cumulative sum. We typically keep enough components to explain 90% or 95% of the total variance in the dataset. This might reduce the dimensions from 500 down to 20, saving massive compute."

## H. Implementation & Guided Practice
"""

import numpy as np

# ==========================================
# 1. From-Scratch PCA Implementation
# ==========================================
def demonstrate_pca():
    print("--- 1. Principal Component Analysis (From Scratch) ---")
    
    # 1. Create a Fake Dataset: 5 samples, 3 features
    # Let's say: [Height(cm), Weight(kg), Shoe_Size]
    # Notice that Height and Weight are usually highly correlated!
    X = np.array([
        [170, 65, 40],
        [180, 75, 42],
        [160, 55, 38],
        [175, 70, 41],
        [165, 60, 39]
    ])
    
    print("Original Data (5 rows, 3 dimensions):")
    print(X)
    
    # STEP 1: Standardize the Data (Mean=0)
    # This is CRITICAL. Without this, PCA fails.
    mean = np.mean(X, axis=0)
    X_centered = X - mean
    
    # STEP 2: Calculate Covariance Matrix
    # We transpose X_centered so rows are features, columns are samples for the cov function
    cov_matrix = np.cov(X_centered.T)
    
    # STEP 3: Calculate Eigenvectors and Eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # STEP 4: Sort Eigenvectors by Eigenvalues (highest variance first)
    # argsort returns indices in ascending order, so we reverse it [::-1]
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]
    
    # Let's look at the Explained Variance
    total_variance = sum(sorted_eigenvalues)
    explained_variance = [(i / total_variance) * 100 for i in sorted_eigenvalues]
    
    print("\nExplained Variance by Component:")
    for i, exp_var in enumerate(explained_variance):
        print(f"Component {i+1}: {exp_var:.2f}% of information")
        
    # Notice that Component 1 holds 99.8% of the information!
    # This makes sense because Height, Weight, and Shoe Size all increase together.
    # It's basically a 1-dimensional dataset hiding in 3D!
    
    # STEP 5: Project the Data onto 2 Dimensions (Dimensionality Reduction)
    # We take the first 2 Eigenvectors (the columns)
    num_components = 2
    projection_matrix = sorted_eigenvectors[:, 0:num_components]
    
    # Final step: Multiply original data by projection matrix
    X_reduced = np.dot(X_centered, projection_matrix)
    
    print("\nReduced Data (5 rows, 2 dimensions):")
    print(X_reduced)


# ==========================================
# 2. Industry Standard: Scikit-Learn
# ==========================================
def demonstrate_sklearn_pca():
    print("\n--- 2. Scikit-Learn PCA (Production Standard) ---")
    try:
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
    except ImportError:
        print("Scikit-learn not installed. Skipping. Run: pip install scikit-learn")
        return
        
    X = np.array([
        [170, 65, 40],
        [180, 75, 42],
        [160, 55, 38],
        [175, 70, 41],
        [165, 60, 39]
    ])
    
    # 1. Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 2. Apply PCA
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X_scaled)
    
    print("Explained Variance Ratio:", pca.explained_variance_ratio_)
    print("Reduced Data Shape:", X_reduced.shape)
    print(X_reduced)


## I. Active Recall Questions
"""
1. Why do we need to calculate the Covariance Matrix before finding Eigenvectors?
   *Answer: The Covariance Matrix represents how the variables vary together. PCA's goal is to find the axes along which the variables vary the most. The eigenvectors of this matrix mathematically represent exactly those axes.*
2. If you have an image dataset where each image is 100x100 pixels, what is the dimension of a single data point before PCA?
   *Answer: 10,000 dimensions (100 * 100 = 10,000).*
3. What is the fundamental difference between standardizing data vs not standardizing it in PCA?
   *Answer: Without standardizing, features with large numeric scales (like House Price in dollars) will dominate features with small scales (like Number of Bedrooms), completely ruining the PCA results.*
"""

if __name__ == "__main__":
    print("========== PCA & EIGENVECTORS MASTERCLASS ==========\n")
    demonstrate_pca()
    demonstrate_sklearn_pca()
    print("\n========== MASTERCLASS COMPLETE ==========")
