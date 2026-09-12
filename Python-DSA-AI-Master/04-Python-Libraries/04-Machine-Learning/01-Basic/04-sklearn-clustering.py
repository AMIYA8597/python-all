"""
Scikit-Learn Clustering: A Textbook-Grade Interactive Lesson
============================================================

This module provides a comprehensive, textbook-grade interactive lesson on Clustering using Python's 
scikit-learn library. It covers the theoretical foundations, mathematical background, Big-O 
complexity analysis, and practical implementations of major clustering algorithms.

Mathematical Background
-----------------------
Clustering is an unsupervised learning technique aimed at grouping a set of objects such that 
objects in the same group (called a cluster) are more similar to each other than to those in 
other groups.

1. K-Means Clustering:
   Objective: Minimize the within-cluster sum of squares (WCSS), also known as inertia.
   Let X = {x_1, x_2, ..., x_n} be the set of data points, and C = {c_1, c_2, ..., c_k} be the set of k centroids.
   WCSS = Σ(from i=1 to k) Σ(x ∈ C_i) ||x - μ_i||^2
   where μ_i is the mean of points in C_i.
   Optimization usually proceeds via Lloyd's algorithm (Expectation-Maximization).

2. DBSCAN (Density-Based Spatial Clustering of Applications with Noise):
   Core concept: A point is a core point if it has at least 'min_samples' within a radius 'eps' (ε).
   ε-neighborhood: N_ε(p) = {q ∈ D | dist(p, q) ≤ ε}
   Allows discovery of non-linearly separable clusters and identification of noise (outliers).

3. Agglomerative (Hierarchical) Clustering:
   Builds a hierarchy of clusters using a bottom-up approach.
   Linkage criteria determine the distance between sets of observations:
   - Ward: Minimizes the variance of the clusters being merged.
   - Complete: Maximum distance between points of two clusters.
   - Average: Average distance between all points of two clusters.

Big-O Time & Space Complexity
-----------------------------
- K-Means:
  Time: O(t * k * n * d) where t = number of iterations, k = number of clusters, n = number of samples, d = dimensions.
  Space: O(k * d) to store centroids.
- DBSCAN:
  Time: O(n log n) with a spatial index (e.g., kd-tree) or O(n^2) without.
  Space: O(n * d) to store data, plus memory for spatial index.
- Agglomerative Clustering:
  Time: O(n^3) typically, or O(n^2 log n) with priority queues.
  Space: O(n^2) to store the distance matrix.

Real-World Applications
-----------------------
- Market Segmentation: Grouping customers by purchasing behavior.
- Document Clustering: Organizing large corpuses of texts/articles.
- Image Segmentation: Partitioning an image into multiple segments (pixels).
- Anomaly Detection: Identifying network intrusions or credit card fraud (noise in DBSCAN).

Interactive Exercises
-------------------
The `if __name__ == '__main__':` block at the bottom executes interactive test cases. 
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, Any, List
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import warnings

# Suppress some harmless warnings from scikit-learn for clean output
warnings.filterwarnings('ignore')

def generate_blob_data(n_samples: int = 300, centers: int = 4, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate isotropic Gaussian blobs for clustering.
    
    Parameters:
        n_samples (int): Total number of points equally divided among clusters.
        centers (int): The number of centers to generate.
        random_state (int): Seed for reproducibility.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: The generated features (X) and true cluster labels (y).
    """
    print(f"Generating {n_samples} samples across {centers} blobs...")
    X, y = make_blobs(n_samples=n_samples, centers=centers, cluster_std=0.60, random_state=random_state)
    return X, y

def generate_moon_data(n_samples: int = 300, noise: float = 0.05, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate two interleaving half circles (moons). Excellent for demonstrating DBSCAN.
    
    Parameters:
        n_samples (int): Total number of points.
        noise (float): Standard deviation of Gaussian noise added to the data.
        random_state (int): Seed for reproducibility.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Features (X) and labels (y).
    """
    print(f"Generating {n_samples} moon-shaped samples with {noise} noise...")
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=random_state)
    return X, y

def apply_kmeans(X: np.ndarray, n_clusters: int = 4) -> Dict[str, Any]:
    """
    Apply the K-Means clustering algorithm to the data.
    
    K-Means partitions the data into 'k' distinct non-overlapping subgroups.
    It expects spherical clusters of roughly equal sizes.
    
    Parameters:
        X (np.ndarray): The feature matrix of shape (n_samples, n_features).
        n_clusters (int): The predefined number of clusters 'k'.
        
    Returns:
        Dict[str, Any]: A dictionary containing the fitted model, predictions, and evaluation metrics.
    """
    print(f"\n--- Applying K-Means (k={n_clusters}) ---")
    model = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, max_iter=300, random_state=42)
    y_pred = model.fit_predict(X)
    
    # Calculate evaluation metrics
    sil_score = silhouette_score(X, y_pred) if len(np.unique(y_pred)) > 1 else -1.0
    
    print(f"K-Means Inertia (WCSS): {model.inertia_:.2f}")
    print(f"Silhouette Score: {sil_score:.3f} (closer to 1 is better)")
    
    return {
        "model": model,
        "predictions": y_pred,
        "silhouette": sil_score,
        "centroids": model.cluster_centers_
    }

def apply_dbscan(X: np.ndarray, eps: float = 0.3, min_samples: int = 5) -> Dict[str, Any]:
    """
    Apply the DBSCAN clustering algorithm.
    
    DBSCAN finds core samples of high density and expands clusters from them.
    It is effective for data which contains clusters of similar density and handles outliers.
    
    Parameters:
        X (np.ndarray): The feature matrix.
        eps (float): The maximum distance between two samples for one to be considered in the neighborhood of the other.
        min_samples (int): The number of samples in a neighborhood for a point to be considered as a core point.
        
    Returns:
        Dict[str, Any]: A dictionary with the model and predictions.
    """
    print(f"\n--- Applying DBSCAN (eps={eps}, min_samples={min_samples}) ---")
    model = DBSCAN(eps=eps, min_samples=min_samples)
    y_pred = model.fit_predict(X)
    
    n_clusters_ = len(set(y_pred)) - (1 if -1 in y_pred else 0)
    n_noise_ = list(y_pred).count(-1)
    
    print(f"Estimated number of clusters: {n_clusters_}")
    print(f"Estimated number of noise points: {n_noise_}")
    
    # Silhouette score is only valid if there are >= 2 clusters (excluding noise)
    if n_clusters_ >= 2:
        # Evaluate silhouette ignoring noise points if desired, but here we include them or mask them
        mask = y_pred != -1
        if len(set(y_pred[mask])) >= 2:
            sil_score = silhouette_score(X[mask], y_pred[mask])
            print(f"Silhouette Score (excluding noise): {sil_score:.3f}")
        else:
            sil_score = -1.0
    else:
        sil_score = -1.0
        
    return {
        "model": model,
        "predictions": y_pred,
        "n_clusters": n_clusters_
    }

def apply_agglomerative(X: np.ndarray, n_clusters: int = 4, linkage: str = 'ward') -> Dict[str, Any]:
    """
    Apply Agglomerative Hierarchical Clustering.
    
    Recursively merges the pair of clusters that minimally increases a given linkage distance.
    
    Parameters:
        X (np.ndarray): The feature matrix.
        n_clusters (int): The number of clusters to find.
        linkage (str): Which linkage criterion to use ('ward', 'complete', 'average', 'single').
        
    Returns:
        Dict[str, Any]: Dictionary with predictions and metrics.
    """
    print(f"\n--- Applying Agglomerative Clustering (n_clusters={n_clusters}, linkage='{linkage}') ---")
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
    y_pred = model.fit_predict(X)
    
    sil_score = silhouette_score(X, y_pred) if len(np.unique(y_pred)) > 1 else -1.0
    print(f"Silhouette Score: {sil_score:.3f}")
    
    return {
        "model": model,
        "predictions": y_pred,
        "silhouette": sil_score
    }

def plot_clusters(X: np.ndarray, y_pred: np.ndarray, title: str, centers: np.ndarray = None):
    """
    Helper function to visualize the clusters.
    
    Parameters:
        X (np.ndarray): Feature matrix.
        y_pred (np.ndarray): Cluster labels.
        title (str): Title for the plot.
        centers (np.ndarray, optional): Cluster centers to plot.
    """
    plt.figure(figsize=(8, 5))
    
    # Plot noise as black points
    unique_labels = set(y_pred)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise
            col = [0, 0, 0, 1]
            
        class_member_mask = (y_pred == k)
        xy = X[class_member_mask]
        plt.scatter(xy[:, 0], xy[:, 1], c=[col], edgecolors='k', s=50, label=f'Cluster {k}' if k != -1 else 'Noise')
        
    if centers is not None:
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75, marker='X', label='Centroids')
        
    plt.title(title)
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.legend(loc='best', fontsize='small')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

if __name__ == '__main__':
    print("=====================================================")
    print("   scikit-learn Clustering Interactive Textbook      ")
    print("=====================================================\n")
    
    # ---------------------------------------------------------
    # Scenario 1: Globular Clusters (Ideal for K-Means)
    # ---------------------------------------------------------
    print("SCENARIO 1: Globular Clusters (make_blobs)")
    X_blobs, y_blobs = generate_blob_data(n_samples=400, centers=4)
    
    # K-Means on Blobs
    km_results = apply_kmeans(X_blobs, n_clusters=4)
    # uncomment to plot:
    # plot_clusters(X_blobs, km_results["predictions"], "K-Means on Globular Data", centers=km_results["centroids"])
    
    # Agglomerative on Blobs
    agg_results = apply_agglomerative(X_blobs, n_clusters=4, linkage='ward')
    
    # ---------------------------------------------------------
    # Scenario 2: Non-Linear/Complex Geometry (Ideal for DBSCAN)
    # ---------------------------------------------------------
    print("\nSCENARIO 2: Non-Linear Geometry (make_moons)")
    X_moons, y_moons = generate_moon_data(n_samples=400, noise=0.08)
    
    # K-Means on Moons (Will fail to capture the moon shapes)
    print("\nTrying K-Means on Moon Data (Expect poor conceptual grouping):")
    km_moons = apply_kmeans(X_moons, n_clusters=2)
    
    # DBSCAN on Moons (Will perfectly capture the shapes)
    print("\nTrying DBSCAN on Moon Data (Expect excellent conceptual grouping):")
    db_moons = apply_dbscan(X_moons, eps=0.2, min_samples=5)
    
    print("\n=====================================================")
    print("Lesson Complete! Review the console output to understand")
    print("how different clustering algorithms respond to varying")
    print("geometries and densities.")
    print("=====================================================")
