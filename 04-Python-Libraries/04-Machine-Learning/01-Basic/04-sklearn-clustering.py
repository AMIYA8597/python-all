"""
# ==============================================================================
# LABORATORY: CLUSTERING & DIMENSIONALITY REDUCTION (SCIKIT-LEARN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Unsupervised Learning is entirely different from Supervised Learning. 
# You are given a massive dataset with ZERO labels. You don't know the "answers".
# You must rely on the algorithm to blindly discover mathematical structure.
#
# This comes in two major flavors:
# 1. CLUSTERING (K-Means, DBSCAN): Grouping similar data points together. 
#    Used for Customer Segmentation, Anomaly Detection (Fraud), and Image Compression.
# 2. DIMENSIONALITY REDUCTION (PCA): Squashing a 10,000-dimensional dataset 
#    (like high-res images) down to 50 dimensions while mathematically preserving 
#    99% of the original variance (information). This defeats the Curse of 
#    Dimensionality and makes models train 1000x faster!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Centroid-based clustering (K-Means).
# - Understand Density-based clustering (DBSCAN) for finding anomalies.
# - Execute Principal Component Analysis (PCA) to compress high-dimensional data.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.datasets import make_blobs, make_moons
    from sklearn.cluster import KMeans, DBSCAN
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. K-MEANS CLUSTERING (CENTROID BASED)
# ==============================================================================
def demonstrate_kmeans():
    section_header("K-Means Clustering (Centroids)")
    
    if not HAS_SKLEARN: return
    
    print("K-Means places K random 'Centroids' (gravity wells) on the map.")
    print("Every point is assigned to its closest Centroid. The Centroids then ")
    print("move to the exact center of their points. This repeats until equilibrium.\n")
    
    # 1. GENERATE UNLABELED DATA
    # 3 distinct clusters
    X, true_labels = make_blobs(n_samples=300, centers=3, cluster_std=1.0, random_state=42)
    
    # 2. INITIALIZE K-MEANS
    # You MUST explicitly tell K-Means exactly how many clusters to look for.
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    
    # 3. FIT AND PREDICT
    predicted_clusters = kmeans.fit_predict(X)
    
    centroids = kmeans.cluster_centers_
    
    print("K-Means discovered 3 clusters!")
    for i, c in enumerate(centroids):
        print(f"Centroid {i}: X={c[0]:.2f}, Y={c[1]:.2f}")
        
    # The "Inertia" is the sum of squared distances of samples to their closest cluster center.
    # We want this number to be as low as possible!
    print(f"\nModel Inertia (Tightness of clusters): {kmeans.inertia_:.2f}")


# ==============================================================================
# 4. DBSCAN (DENSITY BASED & ANOMALIES)
# ==============================================================================
def demonstrate_dbscan():
    section_header("DBSCAN (Density-Based Spatial Clustering)")
    
    if not HAS_SKLEARN: return
    
    print("K-Means assumes clusters are perfectly spherical. If your data is shaped ")
    print("like two crescent moons intertwined, K-Means will fail catastrophically.")
    print("DBSCAN finds 'dense regions' of points. It can find ANY shape, and ")
    print("it explicitly labels isolated points as Outliers (-1)!\n")
    
    # 1. GENERATE INTERTWINED MOONS (Non-spherical)
    X, _ = make_moons(n_samples=200, noise=0.05, random_state=42)
    
    # K-MEANS ATTEMPT (Will Fail)
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10).fit(X)
    
    # DBSCAN ATTEMPT
    # eps: The maximum distance between two points for them to be considered "neighbors".
    # min_samples: Minimum neighbors required to form a "dense core".
    dbscan = DBSCAN(eps=0.2, min_samples=5).fit(X)
    
    print("DBSCAN executed successfully.")
    
    labels = dbscan.labels_
    unique_labels = np.unique(labels)
    print(f"Clusters found by DBSCAN: {len(unique_labels)} (Including the -1 Outlier class)")
    
    # Count the anomalies
    anomalies = np.sum(labels == -1)
    print(f"Total Anomalies/Outliers identified: {anomalies}")


# ==============================================================================
# 5. PRINCIPAL COMPONENT ANALYSIS (PCA)
# ==============================================================================
def demonstrate_pca():
    section_header("Dimensionality Reduction (PCA)")
    
    if not HAS_SKLEARN: return
    
    print("Imagine a dataset with 50 features. It is impossible to visualize in 3D.")
    print("PCA uses Matrix Eigenvectors to mathematically rotate the universe ")
    print("and project the 50D data down onto a 2D flat plane, while perfectly ")
    print("preserving the maximum possible variance (information) of the data!\n")
    
    # Generate 50-Dimensional Data!
    rng = np.random.default_rng(42)
    X = rng.normal(0, 1, (1000, 50))
    
    # Let's say only the first 5 columns actually contain signal, the rest are noise.
    X[:, 5:] = X[:, 5:] * 0.1 # Shrink the variance of the noise
    
    # ALWAYS SCALE DATA BEFORE PCA
    # PCA maximizes Variance. If a column is unscaled (e.g. Salary vs Age), the 
    # massive Salary variance will completely dominate the Eigenvectors!
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. INSTANTIATE PCA (We want exactly 2 Dimensions back!)
    pca = PCA(n_components=2)
    
    # 2. TRANSFORM
    X_compressed = pca.fit_transform(X_scaled)
    
    print(f"Original Shape  : {X_scaled.shape} (1000 rows, 50 columns)")
    print(f"Compressed Shape: {X_compressed.shape} (1000 rows, 2 columns)")
    
    # 3. EXPLAINED VARIANCE
    # How much of the original 50-dimensional "information" did we successfully 
    # cram into our 2-dimensional matrix?
    variance_ratio = pca.explained_variance_ratio_
    total_variance = np.sum(variance_ratio)
    
    print("\nVariance Preserved:")
    print(f"Principal Component 1 (X-axis): {variance_ratio[0]*100:.1f}%")
    print(f"Principal Component 2 (Y-axis): {variance_ratio[1]*100:.1f}%")
    print(f"Total Information Retained  : {total_variance*100:.1f}%")
    print("(We deleted 48 columns but kept almost all the mathematical signal!)")


def run_all_labs():
    demonstrate_kmeans()
    demonstrate_dbscan()
    demonstrate_pca()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental flaw of K-Means clustering?
   Answer: K-Means makes two massive mathematical assumptions: 1) Clusters are perfectly spherical (because it uses raw Euclidean distance radiating outward from a central centroid), and 2) Clusters have roughly similar variance (size). If your data is shaped like a crescent moon, or a donut, or a long line, K-Means will completely fail and just chop the shapes in half. Furthermore, you must explicitly tell K-Means how many clusters ($K$) exist before it even starts, which is often impossible to know in 100-dimensional space!

2. How does DBSCAN inherently detect Outliers?
   Answer: K-Means forces every single data point to join a cluster, even if it is a million miles away from the centroid. DBSCAN evaluates "Density". If a point doesn't have a minimum number of neighbors (`min_samples`) within a specific radius (`eps`), it refuses to merge that point into a cluster. Instead, it mathematically flags that isolated point with the label `-1` (Noise/Outlier). This makes DBSCAN one of the most powerful algorithms for Fraud Detection and Anomaly Detection in cybersecurity.

3. Why MUST you scale data (StandardScaler) before performing PCA?
   Answer: PCA relies on calculating the Covariance Matrix and extracting its Eigenvectors to find the axes of "Maximum Variance". If you don't scale the data, a feature with large numbers (e.g., Salary ranging from $\$0 - \$1,000,000$) will mathematically exhibit an astronomical variance compared to a feature with small numbers (e.g., Age ranging from $0 - 100$). PCA will mistakenly conclude that "Salary" is the absolute most important Principal Component in the universe, completely ignoring the structural information contained in the Age column. Standardizing forces all columns to have a Variance of $1.0$, allowing PCA to find true geometric correlation instead of just massive numbers.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scikit-Learn Clustering & PCA Completed.")
