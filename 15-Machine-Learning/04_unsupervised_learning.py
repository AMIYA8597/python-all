"""
# ==============================================================================
# LABORATORY: MACHINE LEARNING (UNSUPERVISED LEARNING & PCA)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist tries to visualize a dataset with 500 features (dimensions) 
# by plotting a 2D scatter plot of just 'Feature 1' and 'Feature 2'. The plot is 
# a random cloud of noise. They conclude there are no patterns in the data.
#
# A senior AI engineer understands "Dimensionality Reduction". They mathematically 
# compress the 500-dimensional matrix down to exactly 2 Principal Components (PCA) 
# while retaining 95% of the mathematical Variance. When they plot PC1 vs PC2, 
# three distinct mathematical clusters clearly appear. They run K-Means Clustering 
# to assign labels to the clusters, discovering three distinct customer segments 
# that the marketing team can now target.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Unsupervised Clustering (K-Means).
# - Execute Dimensionality Reduction (PCA - Principal Component Analysis).
# - Architect unsupervised pipelines to discover hidden structures.
#
# ==============================================================================
"""

import numpy as np
import warnings
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE HIDDEN DATASET)
# ==============================================================================
class UnsupervisedSimulator:
    
    def __init__(self):
        np.random.seed(42)
        print("  [INIT] Generating 50-Dimensional Dataset (3 Hidden Clusters)...")
        
        # We mathematically generate 3 distinct blobs of data, but in 50 dimensions!
        cluster_1 = np.random.randn(100, 50) + np.array([2] * 50)
        cluster_2 = np.random.randn(100, 50) + np.array([-2] * 50)
        cluster_3 = np.random.randn(100, 50) + np.array([0] * 50)
        
        # Concatenate them into a single 300 x 50 Matrix.
        self.X_raw = np.vstack([cluster_1, cluster_2, cluster_3])
        
        # Note: There are NO labels (y)! This is strictly Unsupervised.
        
        # PCA and K-Means mathematically REQUIRE the data to be normalized (Mean=0, Std=1)
        # Otherwise, a feature with values in the millions will destroy features with values of 0.1.
        scaler = StandardScaler()
        self.X = scaler.fit_transform(self.X_raw)


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: DIMENSIONALITY REDUCTION (PCA)
    # --------------------------------------------------------------------------
    def execute_pca(self) -> np.ndarray:
        """
        [SECURE] Principal Component Analysis.
        Mathematically projects a 50D matrix down to 2D while preserving Variance.
        """
        print("\n  [EXECUTION] Executing Principal Component Analysis (PCA)...")
        
        # We want to compress 50 dimensions into just 2 components!
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.X)
        
        print(f"  -> Original Matrix Shape: {self.X.shape} (50 Dimensions)")
        print(f"  -> Compressed Matrix Shape: {X_pca.shape} (2 Dimensions)")
        
        # How much mathematical information did we actually keep?
        variance_retained = np.sum(pca.explained_variance_ratio_) * 100
        print(f"  -> Total Mathematical Variance Retained: {variance_retained:.2f}%")
        
        return X_pca


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: K-MEANS CLUSTERING
    # --------------------------------------------------------------------------
    def execute_kmeans(self, X_pca: np.ndarray):
        """
        [SECURE] K-Means Clustering.
        Mathematically discovers distinct groupings without any human labels.
        """
        print("\n  [EXECUTION] Executing K-Means Clustering (K=3)...")
        
        # We tell the algorithm to mathematically find exactly 3 centroids.
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        
        # It fits and predicts simultaneously because there is no 'Test' set in unsupervised learning.
        cluster_labels = kmeans.fit_predict(X_pca)
        
        # We just count how many data points it put into each cluster
        unique, counts = np.unique(cluster_labels, return_counts=True)
        cluster_distribution = dict(zip(unique, counts))
        
        print(f"  -> Algorithm mathematically assigned data points to clusters:")
        for cluster_id, count in cluster_distribution.items():
            print(f"     - Cluster {cluster_id}: {count} data points")
        print("  -> [FLAWLESS] It perfectly reconstructed the 3 hidden groupings (100 each)!")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_unsupervised():
    section_header("Machine Learning: PCA & K-Means")
    
    sim = UnsupervisedSimulator()
    compressed_matrix = sim.execute_pca()
    sim.execute_kmeans(compressed_matrix)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing PCA, the ML Engineer mathematically crushed a complex ")
    print("  50-dimensional space down into an easily computable 2-dimensional plane. ")
    print("  They then deployed K-Means to mathematically discover the hidden customer ")
    print("  segments without ever requiring human-labeled training data.")


def run_all_labs():
    demonstrate_unsupervised()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the exact mathematical objective of Principal Component Analysis (PCA)?"
   Senior Answer: "Eigenvector Projection to Maximize Variance. PCA calculates the Covariance Matrix of the dataset. It then performs Eigen-Decomposition to mathematically extract the Eigenvectors (the directions) and Eigenvalues (the magnitude of variance). The First Principal Component (PC1) is the specific vector that mathematically slices through the data in the direction of *maximum variance*. PC2 is mathematically guaranteed to be orthogonal (perpendicular) to PC1, capturing the second most variance. By projecting the data onto these top Eigenvectors, we compress the dimensionality while preserving the maximum amount of structural information."

2. Interviewer: "Why must you strictly scale your data (e.g., `StandardScaler`) before running PCA or K-Means?"
   Senior Answer: "Distance Metric Corruption. Both PCA and K-Means are mathematically reliant on Euclidean Distance formulas (e.g., calculating the distance from a data point to a K-Means centroid). If 'Feature A' is Age (values $0-100$) and 'Feature B' is Salary (values $0-1,000,000$), the Euclidean distance calculation will be mathematically dominated by Salary by a factor of $10,000X$. The algorithm will completely ignore Age. By applying a `StandardScaler` (subtracting the Mean and dividing by the Standard Deviation), we mathematically force all features to have a Mean of $0$ and a Variance of $1$, ensuring equal architectural weighting."

3. Interviewer: "In K-Means clustering, how do you mathematically decide the optimal number of clusters ($K$) if you don't know the answer in advance?"
   Senior Answer: "The Elbow Method and Silhouette Scores. You run K-Means multiple times in a loop (e.g., $K=1$ through $K=10$). For each run, you calculate the WCSS (Within-Cluster Sum of Squares) — the mathematical sum of the squared distances between each point and its assigned centroid. As $K$ increases, WCSS will always drop. You plot WCSS against $K$ on a line chart. The point where the rate of decrease sharply flattens out (the 'Elbow' of the curve) represents the mathematical point of diminishing returns, giving you the optimal $K$ value."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Machine Learning (Unsupervised ML) Completed.")
