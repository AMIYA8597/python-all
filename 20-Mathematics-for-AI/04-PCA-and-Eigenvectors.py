"""
# ==============================================================================
# LABORATORY: MATHEMATICS FOR AI (PCA & EIGENVECTORS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior Data Scientist has a dataset with 10,000 features. They feed all 
# 10,000 columns into a Neural Network. The model violently overfits the noise 
# and takes 3 weeks to train.
#
# A senior AI engineer understands "Dimensionality Reduction". They realize that 
# 9,900 of those features are just redundant mathematical noise. They calculate 
# the Covariance Matrix, extract the "Eigenvectors", and project the data onto 
# the 100 most important mathematical axes (Principal Component Analysis). 
# They crush 10,000 dimensions down to 100 dimensions while retaining 99% of 
# the actual information variance. The model trains in 5 minutes and generalizes perfectly.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Covariance Matrices (Feature Variance).
# - Execute Eigenvalue & Eigenvector decomposition.
# - Architect PCA for mathematically crushing High-Dimensional space.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (EIGEN-DECOMPOSITION & PCA)
# ==============================================================================
class DimensionalityReduction:
    
    @staticmethod
    def simulate_eigenvectors():
        """
        [SECURE] Eigenvectors and Eigenvalues.
        Formula: A * v = lambda * v
        An Eigenvector is a special vector that does not change direction when 
        a matrix transforms it; it only stretches (scaled by the Eigenvalue).
        """
        print("  [INIT] Calculating Eigenvectors & Eigenvalues...")
        
        # A simple 2x2 Matrix (Transformation Matrix)
        A = np.array([
            [4, 1],
            [2, 3]
        ])
        
        # NumPy automatically calculates the Eigen-Decomposition
        eigenvalues, eigenvectors = np.linalg.eig(A)
        
        print(f"  -> Transformation Matrix A:\n{A}")
        print(f"\n  -> Eigenvalues (The Stretching Factor): {eigenvalues}")
        print(f"  -> Eigenvectors (The Unchanging Axes):\n{eigenvectors}")
        
        print("\n  [MATHEMATICAL PROOF] The first Eigenvector represents the primary axis ")
        print("  of the transformation space. In Machine Learning, this represents the ")
        print("  direction of MAXIMUM information variance in the dataset.")

    @staticmethod
    def simulate_pca():
        """
        [SECURE] Principal Component Analysis (PCA).
        We will compress a 3D dataset down to a 2D dataset by dropping the 
        weakest Eigenvector.
        """
        print("\n  [INIT] Executing Principal Component Analysis (PCA)...")
        np.random.seed(42)
        
        # 1. The Raw Dataset: 5 Samples, 3 Dimensions (X, Y, Z)
        X = np.random.rand(5, 3)
        print(f"  -> Original Data Shape: {X.shape}")
        
        # 2. Center the data (Subtract the mean)
        X_centered = X - np.mean(X, axis=0)
        
        # 3. Calculate the Covariance Matrix (3x3)
        # We set rowvar=False because our columns are the variables (features).
        cov_matrix = np.cov(X_centered, rowvar=False)
        
        # 4. Extract Eigenvalues and Eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # 5. Sort them by the highest Eigenvalue!
        # The highest eigenvalue contains the MOST information (variance).
        sorted_indices = np.argsort(eigenvalues)[::-1]
        sorted_eigenvectors = eigenvectors[:, sorted_indices]
        sorted_eigenvalues = eigenvalues[sorted_indices]
        
        # 6. Dimensionality Reduction!
        # We want to compress from 3D to 2D. We take only the top 2 Eigenvectors.
        k = 2
        projection_matrix = sorted_eigenvectors[:, :k]
        
        print(f"  -> Projection Matrix Shape: {projection_matrix.shape} (3 dimensions down to 2)")
        
        # 7. Project the original data into the new, smaller subspace!
        X_compressed = np.dot(X_centered, projection_matrix)
        
        print(f"\n  [EXECUTION] Projecting data...")
        print(f"  -> Compressed Data Shape: {X_compressed.shape}")
        
        # 8. Calculate Information Retention
        total_variance = sum(eigenvalues)
        retained_variance = sum(sorted_eigenvalues[:k])
        retention_ratio = (retained_variance / total_variance) * 100
        
        print(f"\n  [FLAWLESS] We mathematically deleted an entire dimension of data, ")
        print(f"  yet we retained {retention_ratio:.2f}% of the original variance (information). ")
        print("  This drastically speeds up Machine Learning without sacrificing accuracy.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_pca():
    section_header("Mathematics for AI: PCA & Eigenvectors")
    
    math = DimensionalityReduction()
    math.simulate_eigenvectors()
    math.simulate_pca()


def run_all_labs():
    demonstrate_pca()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the physical meaning of an 'Eigenvector' in the context of Principal Component Analysis?"
   Senior Answer: "The Axis of Maximum Variance. Imagine looking at a 3D cloud of data points shaped like a cigar. The longest axis of that cigar contains the most mathematical variance (the most spread out data, meaning the most information). If you calculate the Covariance Matrix of that cloud, the first Eigenvector mathematically points exactly down the length of the cigar. The corresponding Eigenvalue tells you exactly how much of the dataset's total variance is captured along that specific axis."

2. Interviewer: "Why must we 'Center' the dataset (subtract the mean) before executing PCA?"
   Senior Answer: "Origin Alignment. PCA mathematically acts as a geometric rotation of the coordinate axes to align with the data's variance. A rotation in Linear Algebra always occurs strictly around the Origin point $(0,0,0)$. If the data cloud is physically located at coordinates $(100, 100, 100)$, attempting to rotate the axes at $(0,0,0)$ will completely destroy the geometry. By subtracting the mean, we physically slide the entire data cloud so its exact center of mass sits perfectly at $(0,0,0)$, allowing the Covariance Matrix to accurately measure the spread."

3. Interviewer: "If I have a dataset with $1,000$ features, how do I mathematically decide whether to reduce it to $50$ components or $100$ components in PCA?"
   Senior Answer: "Cumulative Explained Variance Thresholding. You do not guess. You calculate all $1,000$ Eigenvalues and sort them descending. You then calculate the Cumulative Sum of the Eigenvalues, divided by the Total Sum. This gives you a curve from $0.0$ to $1.0$. The industry standard is to select $k$ components such that the Cumulative Variance hits exactly $0.95$ ($95\\%$ retention). If the first $87$ Eigenvectors sum to $95\\%$ of the total variance, you definitively drop the remaining $913$ dimensions. They are mathematically proven to be negligible noise."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Mathematics for AI (PCA) Completed.")
