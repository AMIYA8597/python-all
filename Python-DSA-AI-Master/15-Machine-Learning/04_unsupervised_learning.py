"""
Unsupervised Learning
This script covers:
1. K-Means Clustering
2. DBSCAN
3. Principal Component Analysis (PCA)
"""

from sklearn.datasets import make_blobs, load_digits
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np

def kmeans_clustering_example():
    print("--- K-Means Clustering ---")
    # Generate blob data
    X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
    
    kmeans = KMeans(n_clusters=4, random_state=0, n_init='auto')
    kmeans.fit(X)
    
    print(f"Cluster Centers:\n{kmeans.cluster_centers_}")
    print(f"Silhouette Score: {silhouette_score(X, kmeans.labels_):.3f}")

def dbscan_clustering_example():
    print("\n--- DBSCAN Clustering ---")
    # DBSCAN does not need the number of clusters a priori
    X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
    
    # Scale data for DBSCAN
    X_scaled = StandardScaler().fit_transform(X)
    
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    labels = dbscan.fit_predict(X_scaled)
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    
    print(f"Estimated number of clusters: {n_clusters_}")
    print(f"Estimated number of noise points: {n_noise_}")

def pca_example():
    print("\n--- Principal Component Analysis (PCA) ---")
    # Load high-dimensional data (digits: 64 features)
    digits = load_digits()
    X = digits.data
    
    print(f"Original shape: {X.shape}")
    
    # Standardize features
    X_scaled = StandardScaler().fit_transform(X)
    
    # Apply PCA
    pca = PCA(n_components=2) # Reduce to 2 dimensions for visualization
    X_pca = pca.fit_transform(X_scaled)
    
    print(f"Reduced shape: {X_pca.shape}")
    print(f"Explained Variance Ratio: {pca.explained_variance_ratio_}")
    print(f"Total variance explained by 2 components: {sum(pca.explained_variance_ratio_) * 100:.2f}%")

if __name__ == "__main__":
    kmeans_clustering_example()
    dbscan_clustering_example()
    pca_example()
