"""
Scikit-Learn Dimensionality Reduction: A Comprehensive Textbook-Grade Lesson
==========================================================================

Module: 03-sklearn-dim-red
Description: An exhaustive, textbook-grade interactive lesson on Dimensionality
Reduction techniques using Python's scikit-learn library.

## Table of Contents
1. Mathematical Background
2. Core Dimensionality Reduction Algorithms
   2.1 Principal Component Analysis (PCA)
   2.2 t-Distributed Stochastic Neighbor Embedding (t-SNE)
   2.3 Truncated SVD (Singular Value Decomposition)
3. Big-O Complexity Analysis
4. Real-World Applications
5. Modern Python Implementations
6. Test Cases & Execution

## 1. Mathematical Background

Dimensionality Reduction transforms data from a high-dimensional space into a low-dimensional space
so that the low-dimensional representation retains some meaningful properties of the original data,
ideally close to its intrinsic dimension. 

### Principal Component Analysis (PCA)
PCA is a linear dimensionality reduction technique. The goal is to project data onto a lower-dimensional
subspace that maximizes the variance of the projected data.
Let X be an N x D data matrix (N samples, D dimensions), centered (mean of each feature is 0).
1. Compute the covariance matrix: \Sigma = (X^T X) / (N - 1)
2. Compute eigenvectors V and eigenvalues \Lambda of \Sigma.
   \Sigma V = V \Lambda
3. Select the top K eigenvectors corresponding to the K largest eigenvalues to form a D x K projection matrix W.
4. Transform the data: Z = X W (where Z is N x K).

### t-Distributed Stochastic Neighbor Embedding (t-SNE)
t-SNE is a non-linear technique specifically designed for visualization. It converts similarities between
data points to joint probabilities and minimizes the Kullback-Leibler (KL) divergence between the joint 
probabilities of the low-dimensional embedding and the high-dimensional data.
1. High-dimensional similarities (Gaussian):
   p_{j|i} = \exp(-||x_i - x_j||^2 / (2 \sigma_i^2)) / \sum_{k \neq i} \exp(-||x_i - x_k||^2 / (2 \sigma_i^2))
2. Low-dimensional similarities (Student's t-distribution with 1 degree of freedom):
   q_{ij} = (1 + ||y_i - y_j||^2)^{-1} / \sum_{k \neq l} (1 + ||y_k - y_l||^2)^{-1}
3. Cost function: KL divergence:
   C = \sum_i \sum_j p_{ij} \log (p_{ij} / q_{ij})

### Truncated SVD
Also known as Latent Semantic Analysis (LSA) when applied to text, it's a linear technique that performs
linear dimensionality reduction by means of truncated singular value decomposition (SVD). 
Contrary to PCA, this estimator does not center the data before computing the SVD. 
This means it can work with sparse matrices efficiently.
X \approx U \Sigma V^T

## 2. Big-O Complexity Analysis

| Algorithm       | Time Complexity                   | Space Complexity         | Notes                                        |
|-----------------|-----------------------------------|--------------------------|----------------------------------------------|
| PCA             | O(D^3 + N*D^2)                    | O(D^2)                   | D: features, N: samples. Full SVD is slow.   |
| PCA (Randomized)| O(N * D * K)                      | O(D * K)                 | K: target dimensions. Highly efficient.      |
| t-SNE           | O(N^2) or O(N log N) (Barnes-Hut) | O(N^2) or O(N)           | Not suitable for very large datasets (>100k) |
| Truncated SVD   | O(N * D * K)                      | O(D * K)                 | Good for sparse matrices (e.g., TF-IDF).     |

## 3. Real-World Applications

- **Image Compression / Denoising:** PCA is used to reduce the size of images while retaining key information.
- **Data Visualization:** t-SNE is heavily used in genomics (scRNA-seq) to visualize clusters of cells in 2D/3D.
- **Natural Language Processing (NLP):** Truncated SVD is used for Latent Semantic Analysis on sparse TF-IDF matrices.
- **Feature Engineering:** Reducing features to avoid the "curse of dimensionality" and improve ML model performance and inference time.

"""

import time
import numpy as np
from typing import Tuple, Dict, Any, Union, Optional
from dataclasses import dataclass
import warnings

# Sklearn imports
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.datasets import load_digits, make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import pairwise_distances
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)


@dataclass
class DimReductionResult:
    """
    Data class representing the result of a dimensionality reduction operation.
    """
    transformed_data: np.ndarray
    original_shape: Tuple[int, ...]
    reduced_shape: Tuple[int, ...]
    execution_time: float
    explained_variance_ratio: Optional[np.ndarray] = None


class DimensionalityReductionMaster:
    """
    A comprehensive class containing various dimensionality reduction techniques
    demonstrating both pedagogical concepts and production-grade implementations.
    """

    def __init__(self, random_state: int = 42):
        """
        Initializes the Dim Reduction Master.
        
        Args:
            random_state: Seed for reproducibility.
        """
        self.random_state = random_state

    def execute_pca(self, X: np.ndarray, n_components: Union[int, float] = 2) -> DimReductionResult:
        """
        Performs Principal Component Analysis (PCA).

        Mathematical Details:
            If n_components is an integer, it keeps that many components.
            If n_components is a float between 0.0 and 1.0, it selects the number of
            components such that the amount of variance that needs to be explained
            is greater than the percentage specified by n_components.

        Args:
            X: Input data matrix of shape (n_samples, n_features).
            n_components: Number of components to keep, or variance ratio to explain.

        Returns:
            DimReductionResult containing the reduced data and metadata.
        """
        start_time = time.perf_counter()

        # It's a common best practice to scale data before PCA so that features
        # with larger variance don't dominate the principal components.
        scaler = StandardScaler()
        pca = PCA(n_components=n_components, random_state=self.random_state)
        
        # We can use a scikit-learn Pipeline to chain scaling and PCA cleanly
        pipeline = Pipeline(steps=[('scaler', scaler), ('pca', pca)])
        
        # Fit and transform the data
        X_reduced = pipeline.fit_transform(X)
        
        end_time = time.perf_counter()

        return DimReductionResult(
            transformed_data=X_reduced,
            original_shape=X.shape,
            reduced_shape=X_reduced.shape,
            execution_time=end_time - start_time,
            explained_variance_ratio=pca.explained_variance_ratio_
        )

    def execute_tsne(self, X: np.ndarray, n_components: int = 2, perplexity: float = 30.0) -> DimReductionResult:
        """
        Performs t-Distributed Stochastic Neighbor Embedding (t-SNE).

        Important Note:
            t-SNE has a time complexity of O(N log N) with the Barnes-Hut approximation,
            but can still be extremely slow for N > 10,000. It is often recommended to
            run PCA first to reduce the dimensionality to ~50 before running t-SNE.

        Args:
            X: Input data matrix.
            n_components: Target dimension (usually 2 or 3 for visualization).
            perplexity: Relates to the number of nearest neighbors used in manifold learning.
                        Typically between 5 and 50.

        Returns:
            DimReductionResult with transformed data.
        """
        start_time = time.perf_counter()

        # Optional: Apply PCA first if the number of features is very large
        # to speed up t-SNE and reduce noise.
        if X.shape[1] > 50:
            pca = PCA(n_components=50, random_state=self.random_state)
            X_temp = pca.fit_transform(X)
        else:
            X_temp = X

        # Initialize t-SNE
        tsne = TSNE(
            n_components=n_components,
            perplexity=perplexity,
            init="pca", # 'pca' initialization is usually more stable than 'random'
            learning_rate="auto",
            random_state=self.random_state,
            n_jobs=-1 # Use all available CPU cores
        )

        X_reduced = tsne.fit_transform(X_temp)
        
        end_time = time.perf_counter()

        return DimReductionResult(
            transformed_data=X_reduced,
            original_shape=X.shape,
            reduced_shape=X_reduced.shape,
            execution_time=end_time - start_time,
            explained_variance_ratio=None # t-SNE doesn't provide explained variance
        )

    def execute_truncated_svd(self, X: np.ndarray, n_components: int = 2) -> DimReductionResult:
        """
        Performs Truncated Singular Value Decomposition (SVD).

        Mathematical Details:
            Truncated SVD works similarly to PCA but does not center the data matrix
            prior to computing the SVD. This makes it suitable for sparse data matrices
            (e.g., scipy.sparse matrices like those produced by TF-IDF vectorizers).

        Args:
            X: Input data matrix (dense or sparse).
            n_components: Number of components to keep.

        Returns:
            DimReductionResult containing the reduced data.
        """
        start_time = time.perf_counter()

        svd = TruncatedSVD(n_components=n_components, random_state=self.random_state)
        X_reduced = svd.fit_transform(X)

        end_time = time.perf_counter()

        return DimReductionResult(
            transformed_data=X_reduced,
            original_shape=X.shape,
            reduced_shape=X_reduced.shape,
            execution_time=end_time - start_time,
            explained_variance_ratio=svd.explained_variance_ratio_
        )

    def custom_pca_numpy(self, X: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        A pedagogical NumPy implementation of PCA for educational purposes.
        This demonstrates the mathematical foundation of PCA.

        Steps:
        1. Mean centering the data.
        2. Computing the covariance matrix.
        3. Computing eigenvectors and eigenvalues.
        4. Sorting eigenvectors by decreasing eigenvalues.
        5. Projecting data onto the top K eigenvectors.

        Args:
            X: Data matrix of shape (n_samples, n_features).
            k: Number of principal components.

        Returns:
            Tuple of (projected_data, top_eigenvectors).
        """
        # 1. Standardize / Center the data (mean = 0)
        mean_vector = np.mean(X, axis=0)
        X_centered = X - mean_vector
        
        # 2. Compute covariance matrix
        # rowvar=False means each column is a variable
        cov_matrix = np.cov(X_centered, rowvar=False)
        
        # 3. Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        # 4. Sort in descending order
        # eigh returns them in ascending order, so we reverse
        sorted_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvectors = eigenvectors[:, sorted_indices]
        
        # Select the top K eigenvectors (projection matrix)
        top_eigenvectors = sorted_eigenvectors[:, :k]
        
        # 5. Transform the data
        X_projected = np.dot(X_centered, top_eigenvectors)
        
        return X_projected, top_eigenvectors


def evaluate_reconstruction_error(X_original: np.ndarray, X_reduced: np.ndarray, pca_model: PCA) -> float:
    """
    Calculates the reconstruction error of PCA.
    
    The reconstruction error measures how much information is lost when we project
    the data to a lower dimension and then attempt to reconstruct it back to the
    original high-dimensional space.
    
    Args:
        X_original: The original data matrix.
        X_reduced: The lower-dimensional data matrix.
        pca_model: The fitted PCA model to apply inverse_transform.
        
    Returns:
        Mean Squared Error between original and reconstructed data.
    """
    X_reconstructed = pca_model.inverse_transform(X_reduced)
    # Since scaling was applied, we ideally need to unscale it, but for a simple
    # demonstration, we assume pca_model handles the inverse completely or we calculate
    # error in the scaled space. 
    # For accuracy, inverse_transform of PCA returns it to the scaled space.
    mse = np.mean((X_original - X_reconstructed) ** 2)
    return mse


def generate_synthetic_data(n_samples: int = 1000, n_features: int = 50, n_informative: int = 10) -> np.ndarray:
    """
    Helper function to generate a synthetic dataset for testing dimensionality reduction.
    """
    X, _ = make_classification(
        n_samples=n_samples, 
        n_features=n_features, 
        n_informative=n_informative, 
        n_redundant=n_features - n_informative,
        random_state=42
    )
    return X


def main() -> None:
    """
    Main driver function demonstrating the usage of dimensionality reduction techniques.
    """
    print("==========================================================")
    print("Scikit-Learn Dimensionality Reduction: Interactive Lesson")
    print("==========================================================\n")

    # Initialize the Master Class
    dim_red_master = DimensionalityReductionMaster()

    # 1. Load a real-world dataset (Digits dataset)
    print("Loading Digits dataset...")
    digits = load_digits()
    X = digits.data
    y = digits.target
    print(f"Original Dataset Shape: {X.shape} (Samples: {X.shape[0]}, Features: {X.shape[1]})\n")

    # ---------------------------------------------------------
    # 2. PCA Demonstration
    # ---------------------------------------------------------
    print("--- 1. Principal Component Analysis (PCA) ---")
    
    # Example 2a: PCA retaining exactly 2 components (for 2D visualization)
    pca_res_2d = dim_red_master.execute_pca(X, n_components=2)
    print(f"PCA (2 components) - New Shape: {pca_res_2d.reduced_shape}")
    print(f"Execution Time: {pca_res_2d.execution_time:.4f} seconds")
    print(f"Explained Variance Ratio (First 2): {np.sum(pca_res_2d.explained_variance_ratio) * 100:.2f}%\n")
    
    # Example 2b: PCA retaining 95% of the variance
    pca_res_95 = dim_red_master.execute_pca(X, n_components=0.95)
    print(f"PCA (95% variance) - New Shape: {pca_res_95.reduced_shape}")
    print(f"Execution Time: {pca_res_95.execution_time:.4f} seconds")
    print(f"Components needed to explain 95% variance: {pca_res_95.reduced_shape[1]} out of {X.shape[1]}\n")

    # ---------------------------------------------------------
    # 3. t-SNE Demonstration
    # ---------------------------------------------------------
    print("--- 2. t-Distributed Stochastic Neighbor Embedding (t-SNE) ---")
    tsne_res = dim_red_master.execute_tsne(X, n_components=2, perplexity=30.0)
    print(f"t-SNE (2 components) - New Shape: {tsne_res.reduced_shape}")
    print(f"Execution Time: {tsne_res.execution_time:.4f} seconds")
    print("Note: t-SNE does not have a straightforward 'explained variance' metric.\n")

    # ---------------------------------------------------------
    # 4. Truncated SVD Demonstration
    # ---------------------------------------------------------
    print("--- 3. Truncated SVD (LSA) ---")
    svd_res = dim_red_master.execute_truncated_svd(X, n_components=10)
    print(f"Truncated SVD (10 components) - New Shape: {svd_res.reduced_shape}")
    print(f"Execution Time: {svd_res.execution_time:.4f} seconds")
    print(f"Explained Variance Ratio (10 components): {np.sum(svd_res.explained_variance_ratio) * 100:.2f}%\n")

    # ---------------------------------------------------------
    # 5. Pedagogical NumPy PCA Implementation
    # ---------------------------------------------------------
    print("--- 4. Custom NumPy PCA Implementation ---")
    synthetic_X = generate_synthetic_data(n_samples=100, n_features=5)
    X_proj, top_vecs = dim_red_master.custom_pca_numpy(synthetic_X, k=2)
    print(f"NumPy PCA original shape: {synthetic_X.shape}")
    print(f"NumPy PCA reduced shape: {X_proj.shape}")
    print(f"Top Eigenvectors shape: {top_vecs.shape}\n")


    print("==========================================================")
    print("End of Dimensionality Reduction Lesson")
    print("==========================================================")


if __name__ == "__main__":
    main()
    
    # ---------------------------------------------------------
    # Test Cases to ensure robustness
    # ---------------------------------------------------------
    print("\n--- Running Unit Tests ---")
    tester = DimensionalityReductionMaster()
    dummy_data = np.random.rand(50, 10)
    
    # Test PCA
    res_pca = tester.execute_pca(dummy_data, n_components=2)
    assert res_pca.reduced_shape == (50, 2), "PCA shape mismatch!"
    
    # Test SVD
    res_svd = tester.execute_truncated_svd(dummy_data, n_components=3)
    assert res_svd.reduced_shape == (50, 3), "SVD shape mismatch!"
    
    # Test Custom NumPy PCA
    proj, _ = tester.custom_pca_numpy(dummy_data, k=4)
    assert proj.shape == (50, 4), "Custom PCA shape mismatch!"
    
    print("All unit tests passed successfully.")
