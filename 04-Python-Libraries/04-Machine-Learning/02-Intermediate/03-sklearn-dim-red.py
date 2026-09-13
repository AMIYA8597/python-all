"""
# ==============================================================================
# LABORATORY: ADVANCED DIMENSIONALITY REDUCTION & MANIFOLD LEARNING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have a dataset of 10,000 images, and each image is 100x100 pixels.
# When flattened, each image is a row with 10,000 columns (features).
# Training a Random Forest on a 10,000-column dataset will completely crash 
# your computer due to the Curse of Dimensionality.
#
# Dimensionality Reduction solves this by compressing the data.
# 1. PCA (Principal Component Analysis): A linear, mathematical technique using 
#    Singular Value Decomposition (SVD) to find the axes of maximum variance. 
#    It compresses 10,000 columns into 50 columns while keeping 99% of the signal.
# 
# 2. t-SNE (t-Distributed Stochastic Neighbor Embedding): A non-linear Manifold 
#    Learning algorithm. It is arguably the most powerful algorithm on earth for 
#    visualizing high-dimensional data in 2D or 3D space.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Execute PCA and understand Explained Variance Curves.
# - Execute t-SNE and understand Non-Linear Manifold Learning.
# - Understand why you should NEVER use t-SNE as a preprocessing step for ML models.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.datasets import load_digits
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PRINCIPAL COMPONENT ANALYSIS (PCA) COMPRESSION
# ==============================================================================
def demonstrate_pca():
    section_header("PCA Compression & Explained Variance")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed.")
        return
        
    print("We will use the 'Digits' dataset (Handwritten numbers 0-9).")
    print("Each image is 8x8 pixels, meaning the dataset has 64 Dimensions.\n")
    
    # Load dataset
    digits = load_digits()
    X = digits.data  # Shape: (1797, 64)
    y = digits.target
    
    # Scale Data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. FIT PCA WITHOUT SPECIFYING COMPONENTS
    # If we don't specify n_components, PCA calculates all 64 Eigenvectors!
    pca = PCA().fit(X_scaled)
    
    # 2. THE EXPLAINED VARIANCE RATIO
    # This array tells us exactly how much "Information" is held by each of the 64 new columns.
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    
    # Find how many components are needed to reach 90% variance!
    n_90 = np.argmax(cumulative_variance >= 0.90) + 1
    
    print(f"Original Dimensions: 64")
    print(f"Dimensions required to keep 90% of the information: {n_90}")
    print(f"We can delete {64 - n_90} columns of data and barely lose any signal!")
    
    # 3. APPLY COMPRESSION
    pca_optimal = PCA(n_components=n_90)
    X_compressed = pca_optimal.fit_transform(X_scaled)
    print(f"\nSuccessfully compressed dataset from shape {X_scaled.shape} to {X_compressed.shape}")


# ==============================================================================
# 4. MANIFOLD LEARNING (t-SNE) FOR VISUALIZATION
# ==============================================================================
def demonstrate_tsne():
    section_header("Manifold Learning (t-SNE Visualization)")
    
    if not HAS_SKLEARN: return
    
    print("PCA is linear. If the 64-Dimensional handwritten digits are twisted ")
    print("in a complex non-linear 'Manifold' shape (like a Swiss Roll), PCA ")
    print("will just flatten it into a chaotic mess.")
    print("t-SNE calculates the probabilities that two points are 'Neighbors' ")
    print("in 64D space, and mathematically forces them to be Neighbors in 2D space!\n")
    
    digits = load_digits()
    X = digits.data
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 1. INITIALIZE t-SNE
    # n_components=2 because we want to plot this on a 2D X/Y graph!
    # perplexity is a critical hyperparameter (usually 5 to 50) that balances 
    # local vs global geometry.
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    
    print("Executing t-SNE... (This takes heavy computation)")
    
    # t-SNE does NOT have a separate .transform() method! 
    # It can only run fit_transform() on the exact dataset provided.
    X_2d = tsne.fit_transform(X_scaled)
    
    print(f"Successfully warped the 64D dataset into a 2D map: {X_2d.shape}")
    
    print("\nIf you plotted X_2d in Matplotlib, you would see 10 perfectly ")
    print("separated islands of dots! The algorithm successfully separated the ")
    print("0s, 1s, 2s, etc., WITHOUT ever being told what the labels were (Unsupervised)!")


def run_all_labs():
    demonstrate_pca()
    demonstrate_tsne()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental mathematical difference between PCA and t-SNE?
   Answer: PCA is a purely linear algebraic operation. It calculates the Covariance Matrix and extracts the orthogonal Eigenvectors (Principal Components) that capture the maximum variance. It literally just rotates the axes of the universe and flattens the data. 
   t-SNE is Non-Linear. It calculates the Gaussian probability of every point being a "neighbor" to every other point in high-dimensional space. It then creates a random 2D map, calculates the Student-t distribution probabilities on the 2D map, and uses Gradient Descent (Kullback-Leibler divergence) to violently drag the 2D points around until the 2D probabilities perfectly match the high-dimensional probabilities.

2. Why should you NEVER use t-SNE as a preprocessing step for a Machine Learning pipeline (like Random Forest)?
   Answer: Two critical reasons:
   1. **No `.transform()` method:** t-SNE is nonparametric. It learns a specific mapping for the exact training data provided. If you train a model on t-SNE data, and then deploy it to production, t-SNE physically cannot map a *new, single* incoming user data point into the existing 2D space. (PCA, however, saves the Eigenvectors and can easily project new points).
   2. **Distance Distortion:** t-SNE preserves *local* neighborhoods perfectly, but violently distorts *global* distances. The empty white space between two clusters on a t-SNE map is mathematically meaningless. A machine learning model training on t-SNE coordinates will learn false global geometric rules.

3. Why is it standard practice to run PCA *before* running t-SNE?
   Answer: t-SNE scales terribly with the number of dimensions ($O(N^2)$ distance calculations). If you have a 10,000-dimensional dataset, t-SNE might take 3 days to run and will suffer from severe random noise. The industry standard is to first run PCA to compress the 10,000 dimensions down to a dense, noise-free 50 dimensions (retaining 95% of the variance). Then, you feed those 50 dimensions into t-SNE to warp them down to 2 dimensions for beautiful visualization. This is 100x faster and mathematically more stable.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Dimensionality Reduction Completed.")
