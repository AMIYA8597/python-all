"""
Mathematics for Machine Learning, AI, and Data Science
=====================================================

This comprehensive module covers essential mathematical concepts needed for ML, AI, and Data Science.
Designed for beginners with clear explanations, practical examples, and implementations.

Topics Covered:
- Linear Algebra (Vectors, Matrices, Eigenvalues, SVD)
- Probability Theory (Distributions, Bayes' Theorem, Random Variables)
- Statistics (Descriptive, Inferential, Hypothesis Testing)
- Calculus (Derivatives, Gradients, Chain Rule, Optimization)
- Information Theory (Entropy, KL Divergence, Mutual Information)
- Optimization (Gradient Descent, Newton's Method, Constrained Optimization)

Author: Advanced AI/ML Mathematics Tutorial
Date: 2024
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. LINEAR ALGEBRA FUNDAMENTALS
# =============================================================================

class LinearAlgebra:
    """
    Linear Algebra concepts essential for ML/AI/Data Science
    """
    
    def __init__(self):
        self.name = "Linear Algebra for ML/AI"
        print(f"📐 {self.name} - Foundation of Machine Learning Mathematics")
    
    def vector_operations(self) -> None:
        """
        Demonstrate fundamental vector operations
        """
        print("\n" + "="*60)
        print("🔢 VECTOR OPERATIONS")
        print("="*60)
        
        # Create sample vectors
        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        
        print(f"Vector a: {a}")
        print(f"Vector b: {b}")
        
        # Vector addition
        addition = a + b
        print(f"\n➕ Vector Addition (a + b): {addition}")
        
        # Scalar multiplication
        scalar = 3
        scalar_mult = scalar * a
        print(f"🔢 Scalar Multiplication (3 * a): {scalar_mult}")
        
        # Dot product
        dot_product = np.dot(a, b)
        print(f"• Dot Product (a · b): {dot_product}")
        
        # Vector magnitude (Euclidean norm)
        magnitude_a = np.linalg.norm(a)
        magnitude_b = np.linalg.norm(b)
        print(f"📏 Magnitude of a: {magnitude_a:.4f}")
        print(f"📏 Magnitude of b: {magnitude_b:.4f}")
        
        # Unit vector
        unit_a = a / magnitude_a
        print(f"🎯 Unit vector of a: {unit_a}")
        
        # Cosine similarity
        cosine_sim = dot_product / (magnitude_a * magnitude_b)
        print(f"📐 Cosine Similarity: {cosine_sim:.4f}")
        
        print("\n💡 ML Application:")
        print("   - Dot product: Feature similarity, attention mechanisms")
        print("   - Cosine similarity: Document similarity, recommendation systems")
        print("   - Vector norms: Regularization, normalization")
    
    def matrix_operations(self) -> None:
        """
        Demonstrate fundamental matrix operations
        """
        print("\n" + "="*60)
        print("📊 MATRIX OPERATIONS")
        print("="*60)
        
        # Create sample matrices
        A = np.array([[1, 2, 3], 
                      [4, 5, 6]])
        B = np.array([[7, 8], 
                      [9, 10], 
                      [11, 12]])
        
        print("Matrix A:")
        print(A)
        print("\nMatrix B:")
        print(B)
        
        # Matrix multiplication
        C = np.dot(A, B)
        print(f"\n🔄 Matrix Multiplication (A × B):")
        print(C)
        
        # Transpose
        A_T = A.T
        print(f"\n🔄 Transpose of A:")
        print(A_T)
        
        # Square matrix for more operations
        D = np.array([[4, 2, 1], 
                      [2, 5, 3], 
                      [1, 3, 6]])
        print(f"\nSquare Matrix D:")
        print(D)
        
        # Determinant
        det_D = np.linalg.det(D)
        print(f"🎲 Determinant of D: {det_D:.4f}")
        
        # Inverse (if exists)
        if det_D != 0:
            D_inv = np.linalg.inv(D)
            print(f"↩️ Inverse of D:")
            print(D_inv)
            
            # Verify inverse
            identity_check = np.dot(D, D_inv)
            print(f"✅ D × D⁻¹ (should be identity):")
            print(np.round(identity_check, 4))
        
        print("\n💡 ML Application:")
        print("   - Matrix multiplication: Neural network forward pass")
        print("   - Transpose: Backpropagation, covariance matrices")
        print("   - Inverse: Solving linear systems, pseudo-inverse in regression")
    
    def eigenvalues_eigenvectors(self) -> None:
        """
        Demonstrate eigenvalues and eigenvectors - crucial for PCA, spectral methods
        """
        print("\n" + "="*60)
        print("🌟 EIGENVALUES & EIGENVECTORS")
        print("="*60)
        
        # Create a symmetric matrix for real eigenvalues
        A = np.array([[4, 2], 
                      [2, 3]])
        
        print("Matrix A:")
        print(A)
        
        # Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(A)
        
        print(f"\n🔢 Eigenvalues: {eigenvalues}")
        print(f"🎯 Eigenvectors:")
        print(eigenvectors)
        
        # Verify eigenvalue equation: A*v = λ*v
        for i, (λ, v) in enumerate(zip(eigenvalues, eigenvectors.T)):
            Av = np.dot(A, v)
            λv = λ * v
            print(f"\n✅ Verification for eigenvalue {i+1}:")
            print(f"   A*v = {Av}")
            print(f"   λ*v = {λv}")
            print(f"   Equal? {np.allclose(Av, λv)}")
        
        # Demonstrate PCA concept
        print("\n📊 PCA Demonstration:")
        
        # Generate correlated data
        np.random.seed(42)
        data = np.random.multivariate_normal([0, 0], [[2, 1.5], [1.5, 2]], 100)
        
        # Compute covariance matrix
        cov_matrix = np.cov(data.T)
        print("Covariance Matrix:")
        print(cov_matrix)
        
        # Eigendecomposition of covariance matrix
        eigenvals, eigenvecs = np.linalg.eig(cov_matrix)
        
        # Sort by eigenvalue (descending)
        idx = np.argsort(eigenvals)[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        print(f"\nPrincipal Components (Eigenvalues): {eigenvals}")
        print(f"Explained Variance Ratio: {eigenvals / np.sum(eigenvals)}")
        
        print("\n💡 ML Application:")
        print("   - PCA: Dimensionality reduction using eigenvectors")
        print("   - Spectral clustering: Graph Laplacian eigendecomposition")
        print("   - Stability analysis: Eigenvalues determine system stability")
    
    def singular_value_decomposition(self) -> None:
        """
        Demonstrate SVD - fundamental for matrix factorization, recommendation systems
        """
        print("\n" + "="*60)
        print("🔍 SINGULAR VALUE DECOMPOSITION (SVD)")
        print("="*60)
        
        # Create a sample matrix
        A = np.array([[1, 2, 3], 
                      [4, 5, 6], 
                      [7, 8, 9], 
                      [10, 11, 12]])
        
        print("Original Matrix A:")
        print(A)
        print(f"Shape: {A.shape}")
        
        # Perform SVD: A = U * Σ * V^T
        U, S, VT = np.linalg.svd(A, full_matrices=False)
        
        print(f"\n🔢 Singular Values: {S}")
        print(f"📊 U shape: {U.shape}")
        print(f"📊 S shape: {S.shape}")
        print(f"📊 V^T shape: {VT.shape}")
        
        # Reconstruct original matrix
        A_reconstructed = U @ np.diag(S) @ VT
        print(f"\n✅ Reconstruction Error: {np.linalg.norm(A - A_reconstructed):.10f}")
        
        # Low-rank approximation
        for rank in [1, 2]:
            A_approx = U[:, :rank] @ np.diag(S[:rank]) @ VT[:rank, :]
            error = np.linalg.norm(A - A_approx)
            print(f"📉 Rank-{rank} Approximation Error: {error:.4f}")
        
        # Demonstrate matrix factorization for recommendations
        print("\n🎬 Recommendation System Example:")
        
        # User-Item rating matrix (users × items)
        ratings = np.array([[5, 3, 0, 1],
                           [4, 0, 0, 1],
                           [1, 1, 0, 5],
                           [1, 0, 0, 4],
                           [0, 1, 5, 4]])
        
        print("User-Item Ratings Matrix:")
        print(ratings)
        
        # SVD on ratings matrix
        U_r, S_r, VT_r = np.linalg.svd(ratings, full_matrices=False)
        
        # Reconstruct with reduced dimensions
        k = 2  # latent factors
        ratings_approx = U_r[:, :k] @ np.diag(S_r[:k]) @ VT_r[:k, :]
        
        print(f"\nReconstructed Ratings (k={k} factors):")
        print(np.round(ratings_approx, 2))
        
        print("\n💡 ML Application:")
        print("   - Matrix Factorization: Collaborative filtering, topic modeling")
        print("   - Dimensionality Reduction: Data compression, noise reduction")
        print("   - Pseudoinverse: Linear regression, solving overdetermined systems")


# =============================================================================
# 2. PROBABILITY THEORY
# =============================================================================

class ProbabilityTheory:
    """
    Probability Theory concepts essential for ML/AI/Data Science
    """
    
    def __init__(self):
        self.name = "Probability Theory for ML/AI"
        print(f"🎲 {self.name} - Uncertainty and Randomness in AI")
    
    def basic_probability(self) -> None:
        """
        Demonstrate basic probability concepts
        """
        print("\n" + "="*60)
        print("🎯 BASIC PROBABILITY CONCEPTS")
        print("="*60)
        
        print("📚 Fundamental Rules:")
        print("1. P(A) ∈ [0, 1] - Probability is between 0 and 1")
        print("2. P(Ω) = 1 - Probability of sample space is 1")
        print("3. P(A ∪ B) = P(A) + P(B) - P(A ∩ B) - Addition rule")
        print("4. P(A|B) = P(A ∩ B) / P(B) - Conditional probability")
        
        # Simulate coin flips
        print("\n🪙 Coin Flip Simulation:")
        np.random.seed(42)
        n_flips = 10000
        coins = np.random.choice(['H', 'T'], n_flips)
        
        prob_heads = np.mean(coins == 'H')
        prob_tails = np.mean(coins == 'T')
        
        print(f"Number of flips: {n_flips}")
        print(f"P(Heads) = {prob_heads:.4f}")
        print(f"P(Tails) = {prob_tails:.4f}")
        print(f"Sum = {prob_heads + prob_tails:.4f}")
        
        # Law of Large Numbers demonstration
        flip_counts = np.arange(1, 1001)
        running_prob = np.cumsum(coins[:1000] == 'H') / flip_counts
        
        print(f"\n📈 Law of Large Numbers:")
        print(f"After 10 flips: P(H) ≈ {running_prob[9]:.4f}")
        print(f"After 100 flips: P(H) ≈ {running_prob[99]:.4f}")
        print(f"After 1000 flips: P(H) ≈ {running_prob[999]:.4f}")
        print(f"Converges to theoretical: 0.5000")
    
    def conditional_probability_bayes(self) -> None:
        """
        Demonstrate conditional probability and Bayes' theorem
        """
        print("\n" + "="*60)
        print("🧠 CONDITIONAL PROBABILITY & BAYES' THEOREM")
        print("="*60)
        
        print("🔍 Medical Diagnosis Example:")
        print("🏥 A medical test for a rare disease")
        
        # Parameters
        disease_prevalence = 0.01  # P(Disease) = 1%
        test_sensitivity = 0.95    # P(Positive|Disease) = 95%
        test_specificity = 0.98    # P(Negative|No Disease) = 98%
        
        # Calculate other probabilities
        no_disease = 1 - disease_prevalence  # P(No Disease)
        false_positive = 1 - test_specificity  # P(Positive|No Disease)
        
        print(f"\n📊 Given Information:")
        print(f"   P(Disease) = {disease_prevalence:.3f}")
        print(f"   P(Positive|Disease) = {test_sensitivity:.3f}")
        print(f"   P(Negative|No Disease) = {test_specificity:.3f}")
        
        # Bayes' Theorem: P(Disease|Positive) = P(Positive|Disease) * P(Disease) / P(Positive)
        p_positive = (test_sensitivity * disease_prevalence + 
                     false_positive * no_disease)
        
        p_disease_given_positive = (test_sensitivity * disease_prevalence) / p_positive
        
        print(f"\n🧮 Bayes' Theorem Calculation:")
        print(f"   P(Positive) = {p_positive:.4f}")
        print(f"   P(Disease|Positive) = {p_disease_given_positive:.4f}")
        
        print(f"\n💡 Interpretation:")
        print(f"   Even with a positive test, there's only a {p_disease_given_positive:.1%}")
        print(f"   chance of actually having the disease!")
        
        # Simulate the scenario
        print(f"\n🎲 Simulation with 100,000 people:")
        n_people = 100000
        
        # Generate population
        has_disease = np.random.random(n_people) < disease_prevalence
        
        # Generate test results
        test_results = np.zeros(n_people, dtype=bool)
        test_results[has_disease] = np.random.random(np.sum(has_disease)) < test_sensitivity
        test_results[~has_disease] = np.random.random(np.sum(~has_disease)) < false_positive
        
        # Calculate empirical probabilities
        true_positives = np.sum(has_disease & test_results)
        false_positives = np.sum(~has_disease & test_results)
        total_positives = true_positives + false_positives
        
        empirical_prob = true_positives / total_positives if total_positives > 0 else 0
        
        print(f"   People with disease: {np.sum(has_disease)}")
        print(f"   Positive tests: {total_positives}")
        print(f"   True positives: {true_positives}")
        print(f"   Empirical P(Disease|Positive): {empirical_prob:.4f}")
        print(f"   Theoretical: {p_disease_given_positive:.4f}")
        
        print(f"\n💡 ML Application:")
        print("   - Naive Bayes: Text classification, spam detection")
        print("   - Bayesian inference: Parameter estimation, uncertainty quantification")
        print("   - A/B testing: Statistical significance, conversion rates")
    
    def probability_distributions(self) -> None:
        """
        Demonstrate key probability distributions used in ML
        """
        print("\n" + "="*60)
        print("📈 PROBABILITY DISTRIBUTIONS")
        print("="*60)
        
        # Set up plotting
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Key Probability Distributions for ML/AI', fontsize=16)
        
        # 1. Uniform Distribution
        ax = axes[0, 0]
        x_uniform = np.linspace(0, 1, 1000)
        y_uniform = np.ones_like(x_uniform)
        ax.plot(x_uniform, y_uniform, 'b-', linewidth=2)
        ax.set_title('Uniform Distribution')
        ax.set_xlabel('x')
        ax.set_ylabel('Probability Density')
        ax.grid(True, alpha=0.3)
        
        print("🔸 Uniform Distribution:")
        print("   - All outcomes equally likely")
        print("   - ML use: Random initialization, data augmentation")
        
        # 2. Normal (Gaussian) Distribution
        ax = axes[0, 1]
        x_normal = np.linspace(-4, 4, 1000)
        y_normal = (1/np.sqrt(2*np.pi)) * np.exp(-0.5 * x_normal**2)
        ax.plot(x_normal, y_normal, 'g-', linewidth=2)
        ax.set_title('Normal Distribution')
        ax.set_xlabel('x')
        ax.set_ylabel('Probability Density')
        ax.grid(True, alpha=0.3)
        
        print("\n🔸 Normal Distribution:")
        print("   - Bell curve, symmetric around mean")
        print("   - ML use: Gaussian Naive Bayes, noise modeling")
        
        # 3. Exponential Distribution
        ax = axes[0, 2]
        x_exp = np.linspace(0, 5, 1000)
        λ = 1.0
        y_exp = λ * np.exp(-λ * x_exp)
        ax.plot(x_exp, y_exp, 'r-', linewidth=2)
        ax.set_title('Exponential Distribution')
        ax.set_xlabel('x')
        ax.set_ylabel('Probability Density')
        ax.grid(True, alpha=0.3)
        
        print("\n🔸 Exponential Distribution:")
        print("   - Models time between events")
        print("   - ML use: Survival analysis, reliability modeling")
        
        # 4. Bernoulli Distribution
        ax = axes[1, 0]
        x_bernoulli = [0, 1]
        p = 0.3
        y_bernoulli = [1-p, p]
        ax.bar(x_bernoulli, y_bernoulli, color='purple', alpha=0.7)
        ax.set_title('Bernoulli Distribution')
        ax.set_xlabel('Outcome')
        ax.set_ylabel('Probability')
        ax.set_xticks([0, 1])
        ax.grid(True, alpha=0.3)
        
        print("\n🔸 Bernoulli Distribution:")
        print("   - Single trial with two outcomes")
        print("   - ML use: Logistic regression, binary classification")
        
        # 5. Poisson Distribution
        ax = axes[1, 1]
        x_poisson = np.arange(0, 15)
        λ_poisson = 3.0
        y_poisson = np.exp(-λ_poisson) * (λ_poisson ** x_poisson) / np.array([np.math.factorial(x) for x in x_poisson])
        ax.bar(x_poisson, y_poisson, color='orange', alpha=0.7)
        ax.set_title('Poisson Distribution')
        ax.set_xlabel('Number of Events')
        ax.set_ylabel('Probability')
        ax.grid(True, alpha=0.3)
        
        print("\n🔸 Poisson Distribution:")
        print("   - Count of events in fixed interval")
        print("   - ML use: Count data modeling, anomaly detection")
        
        # 6. Beta Distribution
        ax = axes[1, 2]
        x_beta = np.linspace(0, 1, 1000)
        α, β = 2, 5
        from scipy.special import gamma
        y_beta = (x_beta**(α-1) * (1-x_beta)**(β-1)) / (gamma(α)*gamma(β)/gamma(α+β))
        ax.plot(x_beta, y_beta, 'm-', linewidth=2)
        ax.set_title('Beta Distribution')
        ax.set_xlabel('x')
        ax.set_ylabel('Probability Density')
        ax.grid(True, alpha=0.3)
        
        print("\n🔸 Beta Distribution:")
        print("   - Models probabilities and proportions")
        print("   - ML use: Bayesian inference, A/B testing priors")
        
        plt.tight_layout()
        plt.savefig('probability_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\n📊 Distribution plot saved as 'probability_distributions.png'")
    
    def central_limit_theorem(self) -> None:
        """
        Demonstrate Central Limit Theorem - foundation of statistical inference
        """
        print("\n" + "="*60)
        print("🎯 CENTRAL LIMIT THEOREM")
        print("="*60)
        
        print("📚 Theorem: Sample means approach normal distribution")
        print("    regardless of original population distribution")
        
        # Create non-normal population (exponential)
        np.random.seed(42)
        population_size = 100000
        λ = 2.0
        population = np.random.exponential(1/λ, population_size)
        
        print(f"\n🔸 Original Population (Exponential):")
        print(f"   Size: {population_size}")
        print(f"   Mean: {np.mean(population):.4f}")
        print(f"   Std: {np.std(population):.4f}")
        print(f"   Skewness: {len(population[population > np.mean(population)]) / len(population):.4f}")
        
        # Sample means for different sample sizes
        sample_sizes = [5, 10, 30, 100]
        n_samples = 1000
        
        print(f"\n📊 Sample Means Distribution:")
        
        for n in sample_sizes:
            # Generate sample means
            sample_means = []
            for _ in range(n_samples):
                sample = np.random.choice(population, n)
                sample_means.append(np.mean(sample))
            
            sample_means = np.array(sample_means)
            
            # Calculate statistics
            mean_of_means = np.mean(sample_means)
            std_of_means = np.std(sample_means)
            theoretical_std = np.std(population) / np.sqrt(n)
            
            print(f"   n={n:3d}: Mean={mean_of_means:.4f}, Std={std_of_means:.4f} (Theory: {theoretical_std:.4f})")
            
            # Test normality (approximate)
            from scipy import stats
            _, p_value = stats.normaltest(sample_means)
            print(f"         Normality test p-value: {p_value:.4f} ({'Normal' if p_value > 0.05 else 'Not Normal'})")
        
        print("\n💡 ML Application:")
        print("   - Confidence intervals: Model performance estimation")
        print("   - Hypothesis testing: A/B test significance")
        print("   - Bootstrap methods: Uncertainty quantification")


# =============================================================================
# 3. STATISTICS
# =============================================================================

class Statistics:
    """
    Statistical concepts essential for ML/AI/Data Science
    """
    
    def __init__(self):
        self.name = "Statistics for ML/AI"
        print(f"📊 {self.name} - Data Analysis and Inference")
    
    def descriptive_statistics(self) -> None:
        """
        Demonstrate descriptive statistics - summarizing data
        """
        print("\n" + "="*60)
        print("📈 DESCRIPTIVE STATISTICS")
        print("="*60)
        
        # Generate sample dataset
        np.random.seed(42)
        data = np.concatenate([
            np.random.normal(50, 10, 500),  # Main cluster
            np.random.normal(80, 5, 100),   # Smaller cluster
            np.random.uniform(20, 30, 50)   # Outliers
        ])
        
        print(f"Dataset size: {len(data)} samples")
        
        # Measures of Central Tendency
        mean = np.mean(data)
        median = np.median(data)
        
        # Mode (approximate for continuous data)
        hist, bin_edges = np.histogram(data, bins=30)
        mode_bin = np.argmax(hist)
        mode = (bin_edges[mode_bin] + bin_edges[mode_bin + 1]) / 2
        
        print(f"\n🎯 Central Tendency:")
        print(f"   Mean:   {mean:.2f}")
        print(f"   Median: {median:.2f}")
        print(f"   Mode:   {mode:.2f} (approximate)")
        
        # Measures of Dispersion
        variance = np.var(data)
        std_dev = np.std(data)
        range_val = np.max(data) - np.min(data)
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        
        print(f"\n📏 Dispersion:")
        print(f"   Variance:  {variance:.2f}")
        print(f"   Std Dev:   {std_dev:.2f}")
        print(f"   Range:     {range_val:.2f}")
        print(f"   IQR:       {iqr:.2f}")
        
        # Measures of Shape
        from scipy import stats
        skewness = stats.skew(data)
        kurtosis = stats.kurtosis(data)
        
        print(f"\n📐 Shape:")
        print(f"   Skewness:  {skewness:.2f} ({'Right' if skewness > 0 else 'Left'} skewed)")
        print(f"   Kurtosis:  {kurtosis:.2f} ({'Heavy' if kurtosis > 0 else 'Light'} tails)")
        
        # Percentiles
        percentiles = [5, 25, 50, 75, 95]
        percentile_values = np.percentile(data, percentiles)
        
        print(f"\n📊 Percentiles:")
        for p, v in zip(percentiles, percentile_values):
            print(f"   {p:2d}th: {v:.2f}")
        
        # Outlier Detection using IQR method
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        
        print(f"\n🚨 Outliers (IQR method):")
        print(f"   Count: {len(outliers)}")
        print(f"   Percentage: {len(outliers)/len(data)*100:.1f}%")
        print(f"   Range: [{lower_bound:.2f}, {upper_bound:.2f}]")
        
        print(f"\n💡 ML Application:")
        print("   - Feature scaling: Use mean/std for standardization")
        print("   - Outlier detection: Identify anomalies, data quality issues")
        print("   - Feature selection: Use variance to identify uninformative features")
    
    def correlation_analysis(self) -> None:
        """
        Demonstrate correlation analysis - relationships between variables
        """
        print("\n" + "="*60)
        print("🔗 CORRELATION ANALYSIS")
        print("="*60)
        
        # Generate correlated data
        np.random.seed(42)
        n_samples = 1000
        
        # Create variables with different correlation patterns
        x1 = np.random.normal(0, 1, n_samples)
        x2 = 0.8 * x1 + np.random.normal(0, 0.6, n_samples)  # Strong positive
        x3 = -0.6 * x1 + np.random.normal(0, 0.8, n_samples)  # Moderate negative
        x4 = np.random.normal(0, 1, n_samples)  # Independent
        
        # Create dataset
        data = np.column_stack([x1, x2, x3, x4])
        feature_names = ['X1', 'X2', 'X3', 'X4']
        
        # Pearson Correlation Matrix
        corr_matrix = np.corrcoef(data.T)
        
        print("📊 Pearson Correlation Matrix:")
        print("     ", "  ".join(f"{name:>6}" for name in feature_names))
        for i, row in enumerate(corr_matrix):
            print(f"{feature_names[i]:>4} ", "  ".join(f"{val:6.3f}" for val in row))
        
        # Interpret correlations
        print(f"\n🔍 Correlation Interpretation:")
        for i in range(len(feature_names)):
            for j in range(i+1, len(feature_names)):
                corr = corr_matrix[i, j]
                strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.3 else "Weak"
                direction = "positive" if corr > 0 else "negative"
                print(f"   {feature_names[i]}-{feature_names[j]}: {corr:6.3f} ({strength} {direction})")
        
        # Spearman Rank Correlation (for non-linear relationships)
        from scipy.stats import spearmanr
        
        print(f"\n📈 Spearman Rank Correlations:")
        for i in range(len(feature_names)):
            for j in range(i+1, len(feature_names)):
                corr, p_value = spearmanr(data[:, i], data[:, j])
                significance = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else ""
                print(f"   {feature_names[i]}-{feature_names[j]}: {corr:6.3f} {significance}")
        
        # Feature correlation with target (regression example)
        print(f"\n🎯 Target Correlation Example:")
        
        # Create synthetic target variable
        target = 2 * x1 + 1.5 * x2 - x3 + np.random.normal(0, 0.5, n_samples)
        
        target_corrs = []
        for i, feature in enumerate(feature_names):
            corr = np.corrcoef(data[:, i], target)[0, 1]
            target_corrs.append((feature, corr))
        
        # Sort by absolute correlation
        target_corrs.sort(key=lambda x: abs(x[1]), reverse=True)
        
        print("Feature importance by correlation with target:")
        for feature, corr in target_corrs:
            print(f"   {feature}: {corr:6.3f} ({'🔴' if abs(corr) > 0.5 else '🟡' if abs(corr) > 0.2 else '🟢'})")
        
        print(f"\n💡 ML Application:")
        print("   - Feature selection: Remove highly correlated features")
        print("   - Multicollinearity: Detect problematic correlations in regression")
        print("   - Exploratory analysis: Understand data relationships")
    
    def hypothesis_testing(self) -> None:
        """
        Demonstrate hypothesis testing - statistical inference
        """
        print("\n" + "="*60)
        print("🔬 HYPOTHESIS TESTING")
        print("="*60)
        
        print("📚 Hypothesis Testing Framework:")
        print("   H₀: Null hypothesis (status quo)")
        print("   H₁: Alternative hypothesis")
        print("   α: Significance level (Type I error rate)")
        print("   p-value: Probability of observing data if H₀ is true")
        print("   Decision: Reject H₀ if p-value < α")
        
        # Example 1: One-sample t-test
        print(f"\n🔸 One-Sample T-Test:")
        print("   Testing if sample mean differs from population mean")
        
        np.random.seed(42)
        population_mean = 100
        sample = np.random.normal(103, 15, 50)  # Sample with slightly higher mean
        
        from scipy import stats
        t_statistic, p_value = stats.ttest_1samp(sample, population_mean)
        
        print(f"   H₀: μ = {population_mean}")
        print(f"   H₁: μ ≠ {population_mean}")
        print(f"   Sample mean: {np.mean(sample):.2f}")
        print(f"   Sample size: {len(sample)}")
        print(f"   t-statistic: {t_statistic:.4f}")
        print(f"   p-value: {p_value:.4f}")
        print(f"   Decision (α=0.05): {'Reject H₀' if p_value < 0.05 else 'Fail to reject H₀'}")
        
        # Example 2: Two-sample t-test
        print(f"\n🔸 Two-Sample T-Test:")
        print("   Comparing means of two groups")
        
        group_a = np.random.normal(50, 10, 40)
        group_b = np.random.normal(55, 12, 35)
        
        t_stat, p_val = stats.ttest_ind(group_a, group_b)
        
        print(f"   H₀: μ₁ = μ₂")
        print(f"   H₁: μ₁ ≠ μ₂")
        print(f"   Group A: n={len(group_a)}, mean={np.mean(group_a):.2f}")
        print(f"   Group B: n={len(group_b)}, mean={np.mean(group_b):.2f}")
        print(f"   t-statistic: {t_stat:.4f}")
        print(f"   p-value: {p_val:.4f}")
        print(f"   Decision (α=0.05): {'Reject H₀' if p_val < 0.05 else 'Fail to reject H₀'}")
        
        # Example 3: Chi-square test for independence
        print(f"\n🔸 Chi-Square Test of Independence:")
        print("   Testing relationship between categorical variables")
        
        # Create contingency table (Ad clicked vs Device type)
        contingency_table = np.array([[20, 15, 10],   # Desktop: No click, Click, Purchase
                                     [25, 30, 20],   # Mobile
                                     [15, 10, 5]])   # Tablet
        
        chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency_table)
        
        print("   Contingency Table (Device × Outcome):")
        print("          No Click  Click  Purchase")
        print(f"   Desktop    {contingency_table[0, 0]:2d}     {contingency_table[0, 1]:2d}      {contingency_table[0, 2]:2d}")
        print(f"   Mobile     {contingency_table[1, 0]:2d}     {contingency_table[1, 1]:2d}      {contingency_table[1, 2]:2d}")
        print(f"   Tablet     {contingency_table[2, 0]:2d}     {contingency_table[2, 1]:2d}      {contingency_table[2, 2]:2d}")
        
        print(f"\n   χ² statistic: {chi2:.4f}")
        print(f"   Degrees of freedom: {dof}")
        print(f"   p-value: {p_chi2:.4f}")
        print(f"   Decision (α=0.05): {'Variables are dependent' if p_chi2 < 0.05 else 'Variables are independent'}")
        
        # Power Analysis
        print(f"\n🔸 Statistical Power Analysis:")
        print("   Power = P(Reject H₀ | H₁ is true)")
        
        effect_sizes = [0.2, 0.5, 0.8]  # Small, medium, large
        sample_sizes = [20, 50, 100]
        alpha = 0.05
        
        print("   Effect Size vs Sample Size vs Power:")
        print("   Effect    n=20    n=50    n=100")
        
        for effect in effect_sizes:
            powers = []
            for n in sample_sizes:
                # Approximate power calculation for t-test
                from scipy.stats import norm
                critical_t = stats.t.ppf(1 - alpha/2, n-1)
                ncp = effect * np.sqrt(n)  # Non-centrality parameter
                power = 1 - stats.t.cdf(critical_t, n-1, ncp) + stats.t.cdf(-critical_t, n-1, ncp)
                powers.append(power)
            
            print(f"   {effect:5.1f}    {powers[0]:.3f}   {powers[1]:.3f}   {powers[2]:.3f}")
        
        print(f"\n💡 ML Application:")
        print("   - A/B testing: Compare treatment effects")
        print("   - Feature significance: Test if features improve model")
        print("   - Model comparison: Statistical significance of performance differences")


# =============================================================================
# 4. CALCULUS FOR OPTIMIZATION
# =============================================================================

class Calculus:
    """
    Calculus concepts essential for ML/AI optimization
    """
    
    def __init__(self):
        self.name = "Calculus for ML/AI"
        print(f"📐 {self.name} - Optimization and Learning Algorithms")
    
    def derivatives_and_gradients(self) -> None:
        """
        Demonstrate derivatives and gradients - foundation of optimization
        """
        print("\n" + "="*60)
        print("📈 DERIVATIVES & GRADIENTS")
        print("="*60)
        
        print("📚 Key Concepts:")
        print("   Derivative: Rate of change of function")
        print("   Gradient: Vector of partial derivatives")
        print("   Used in: Gradient descent, backpropagation")
        
        # Example 1: Simple function f(x) = x² - 4x + 3
        print(f"\n🔸 Single Variable Function:")
        print("   f(x) = x² - 4x + 3")
        print("   f'(x) = 2x - 4")
        
        def f(x):
            return x**2 - 4*x + 3
        
        def f_prime(x):
            return 2*x - 4
        
        x_vals = np.linspace(-1, 5, 100)
        y_vals = f(x_vals)
        
        # Find critical point
        critical_point = 2  # Where f'(x) = 0
        
        print(f"   Critical point: x = {critical_point}")
        print(f"   f({critical_point}) = {f(critical_point)}")
        print(f"   f'({critical_point}) = {f_prime(critical_point)}")
        
        # Example 2: Multivariable function f(x,y) = x² + y² - 2x - 4y + 5
        print(f"\n🔸 Multivariable Function:")
        print("   f(x,y) = x² + y² - 2x - 4y + 5")
        print("   ∂f/∂x = 2x - 2")
        print("   ∂f/∂y = 2y - 4")
        print("   ∇f = [2x - 2, 2y - 4]")
        
        def f_multivar(x, y):
            return x**2 + y**2 - 2*x - 4*y + 5
        
        def gradient_f(x, y):
            return np.array([2*x - 2, 2*y - 4])
        
        # Find critical point where gradient = 0
        critical_x, critical_y = 1, 2
        
        print(f"   Critical point: ({critical_x}, {critical_y})")
        print(f"   f({critical_x}, {critical_y}) = {f_multivar(critical_x, critical_y)}")
        print(f"   ∇f({critical_x}, {critical_y}) = {gradient_f(critical_x, critical_y)}")
        
        # Numerical gradient computation
        print(f"\n🔸 Numerical Gradient Computation:")
        
        def numerical_gradient(func, x, h=1e-7):
            """Compute numerical gradient using finite differences"""
            grad = np.zeros_like(x)
            for i in range(len(x)):
                x_plus = x.copy()
                x_minus = x.copy()
                x_plus[i] += h
                x_minus[i] -= h
                grad[i] = (func(x_plus) - func(x_minus)) / (2 * h)
            return grad
        
        def test_function(x):
            return np.sum(x**2) - 2*x[0] - 4*x[1] + 5
        
        test_point = np.array([1.5, 2.5])
        analytical_grad = gradient_f(test_point[0], test_point[1])
        numerical_grad = numerical_gradient(test_function, test_point)
        
        print(f"   Test point: {test_point}")
        print(f"   Analytical gradient: {analytical_grad}")
        print(f"   Numerical gradient:  {numerical_grad}")
        print(f"   Difference: {np.abs(analytical_grad - numerical_grad)}")
    
    def chain_rule_backpropagation(self) -> None:
        """
        Demonstrate chain rule - foundation of backpropagation
        """
        print("\n" + "="*60)
        print("🔗 CHAIN RULE & BACKPROPAGATION")
        print("="*60)
        
        print("📚 Chain Rule:")
        print("   For composite function f(g(x)): df/dx = (df/dg) × (dg/dx)")
        print("   In neural networks: ∂Loss/∂w = ∂Loss/∂y × ∂y/∂w")
        
        # Example: Simple neural network forward and backward pass
        print(f"\n🧠 Neural Network Example:")
        print("   Network: Input → Linear → ReLU → Linear → Output")
        
        # Network parameters
        np.random.seed(42)
        W1 = np.random.randn(2, 3) * 0.5  # Input to hidden
        b1 = np.zeros(3)
        W2 = np.random.randn(3, 1) * 0.5  # Hidden to output
        b2 = np.zeros(1)
        
        # Input and target
        x = np.array([1.0, -0.5])
        target = np.array([1.0])
        
        print(f"   Input: {x}")
        print(f"   Target: {target}")
        
        # Forward pass
        print(f"\n🔄 Forward Pass:")
        
        # Layer 1: Linear transformation
        z1 = np.dot(W1.T, x) + b1
        print(f"   z1 = W1^T × x + b1 = {z1}")
        
        # ReLU activation
        a1 = np.maximum(0, z1)
        print(f"   a1 = ReLU(z1) = {a1}")
        
        # Layer 2: Linear transformation
        z2 = np.dot(W2.T, a1) + b2
        print(f"   z2 = W2^T × a1 + b2 = {z2}")
        
        # Output (identity activation)
        output = z2
        print(f"   output = {output}")
        
        # Loss (Mean Squared Error)
        loss = 0.5 * np.sum((output - target)**2)
        print(f"   Loss = 0.5 × (output - target)² = {loss:.6f}")
        
        # Backward pass (Backpropagation)
        print(f"\n🔙 Backward Pass:")
        
        # Gradient of loss with respect to output
        dL_doutput = output - target
        print(f"   ∂L/∂output = {dL_doutput}")
        
        # Gradient with respect to z2
        dL_dz2 = dL_doutput  # Identity activation
        print(f"   ∂L/∂z2 = {dL_dz2}")
        
        # Gradients with respect to W2 and b2
        dL_dW2 = np.outer(a1, dL_dz2)
        dL_db2 = dL_dz2
        print(f"   ∂L/∂W2 = a1 ⊗ ∂L/∂z2 = \n{dL_dW2}")
        print(f"   ∂L/∂b2 = {dL_db2}")
        
        # Gradient with respect to a1
        dL_da1 = np.dot(W2, dL_dz2)
        print(f"   ∂L/∂a1 = W2 × ∂L/∂z2 = {dL_da1}")
        
        # Gradient with respect to z1 (ReLU derivative)
        dL_dz1 = dL_da1 * (z1 > 0).astype(float)  # ReLU derivative
        print(f"   ∂L/∂z1 = ∂L/∂a1 × ReLU'(z1) = {dL_dz1}")
        
        # Gradients with respect to W1 and b1
        dL_dW1 = np.outer(x, dL_dz1)
        dL_db1 = dL_dz1
        print(f"   ∂L/∂W1 = x ⊗ ∂L/∂z1 = \n{dL_dW1}")
        print(f"   ∂L/∂b1 = {dL_db1}")
        
        # Gradient checking
        print(f"\n✅ Gradient Checking:")
        
        def compute_loss(W1_flat, W2_flat, b1_flat, b2_flat):
            """Compute loss for given parameters"""
            W1_test = W1_flat.reshape(2, 3)
            W2_test = W2_flat.reshape(3, 1)
            
            z1_test = np.dot(W1_test.T, x) + b1_flat
            a1_test = np.maximum(0, z1_test)
            z2_test = np.dot(W2_test.T, a1_test) + b2_flat
            
            return 0.5 * np.sum((z2_test - target)**2)
        
        # Numerical gradients
        h = 1e-7
        
        def numerical_grad_check(param, grad, param_name):
            """Check analytical vs numerical gradient"""
            param_flat = param.flatten()
            grad_flat = grad.flatten()
            
            numerical_grad = np.zeros_like(param_flat)
            for i in range(len(param_flat)):
                param_plus = param_flat.copy()
                param_minus = param_flat.copy()
                param_plus[i] += h
                param_minus[i] -= h
                
                if param_name == 'W1':
                    loss_plus = compute_loss(param_plus, W2.flatten(), b1, b2)
                    loss_minus = compute_loss(param_minus, W2.flatten(), b1, b2)
                elif param_name == 'W2':
                    loss_plus = compute_loss(W1.flatten(), param_plus, b1, b2)
                    loss_minus = compute_loss(W1.flatten(), param_minus, b1, b2)
                
                numerical_grad[i] = (loss_plus - loss_minus) / (2 * h)
            
            diff = np.abs(grad_flat - numerical_grad)
            max_diff = np.max(diff)
            
            print(f"   {param_name}: Max difference = {max_diff:.8f}")
            return max_diff < 1e-6
        
        # Check W1 and W2 gradients
        w1_check = numerical_grad_check(W1, dL_dW1, 'W1')
        w2_check = numerical_grad_check(W2, dL_dW2, 'W2')
        
        print(f"   Gradient check passed: {w1_check and w2_check}")
        
        print(f"\n💡 ML Application:")
        print("   - Backpropagation: Training neural networks")
        print("   - Gradient descent: Parameter optimization")
        print("   - Automatic differentiation: Modern ML frameworks")
    
    def optimization_methods(self) -> None:
        """
        Demonstrate optimization methods used in ML
        """
        print("\n" + "="*60)
        print("⚡ OPTIMIZATION METHODS")
        print("="*60)
        
        # Test function: f(x,y) = (x-2)² + (y-1)² + 0.1*sin(5*x)*sin(5*y)
        def objective(x):
            return (x[0] - 2)**2 + (x[1] - 1)**2 + 0.1 * np.sin(5*x[0]) * np.sin(5*x[1])
        
        def gradient(x):
            dx = 2*(x[0] - 2) + 0.5*np.cos(5*x[0])*np.sin(5*x[1])
            dy = 2*(x[1] - 1) + 0.5*np.sin(5*x[0])*np.cos(5*x[1])
            return np.array([dx, dy])
        
        print("🎯 Test Function:")
        print("   f(x,y) = (x-2)² + (y-1)² + 0.1×sin(5x)×sin(5y)")
        print("   Global minimum: (2, 1)")
        
        # Starting point
        x0 = np.array([0.0, 0.0])
        print(f"   Starting point: {x0}")
        
        # 1. Gradient Descent
        print(f"\n🔸 Gradient Descent:")
        
        def gradient_descent(x_start, learning_rate=0.01, max_iter=1000, tol=1e-6):
            x = x_start.copy()
            history = [x.copy()]
            
            for i in range(max_iter):
                grad = gradient(x)
                x_new = x - learning_rate * grad
                
                if np.linalg.norm(x_new - x) < tol:
                    break
                
                x = x_new
                history.append(x.copy())
            
            return x, history, i+1
        
        x_gd, history_gd, iter_gd = gradient_descent(x0, learning_rate=0.1)
        
        print(f"   Final point: ({x_gd[0]:.4f}, {x_gd[1]:.4f})")
        print(f"   Final value: {objective(x_gd):.6f}")
        print(f"   Iterations: {iter_gd}")
        
        # 2. Momentum
        print(f"\n🔸 Gradient Descent with Momentum:")
        
        def momentum_gd(x_start, learning_rate=0.01, momentum=0.9, max_iter=1000, tol=1e-6):
            x = x_start.copy()
            v = np.zeros_like(x)  # Velocity
            history = [x.copy()]
            
            for i in range(max_iter):
                grad = gradient(x)
                v = momentum * v - learning_rate * grad
                x_new = x + v
                
                if np.linalg.norm(x_new - x) < tol:
                    break
                
                x = x_new
                history.append(x.copy())
            
            return x, history, i+1
        
        x_mom, history_mom, iter_mom = momentum_gd(x0, learning_rate=0.1, momentum=0.9)
        
        print(f"   Final point: ({x_mom[0]:.4f}, {x_mom[1]:.4f})")
        print(f"   Final value: {objective(x_mom):.6f}")
        print(f"   Iterations: {iter_mom}")
        
        # 3. Adam Optimizer
        print(f"\n🔸 Adam Optimizer:")
        
        def adam_optimizer(x_start, learning_rate=0.01, beta1=0.9, beta2=0.999, 
                          epsilon=1e-8, max_iter=1000, tol=1e-6):
            x = x_start.copy()
            m = np.zeros_like(x)  # First moment
            v = np.zeros_like(x)  # Second moment
            history = [x.copy()]
            
            for i in range(max_iter):
                grad = gradient(x)
                
                # Update moments
                m = beta1 * m + (1 - beta1) * grad
                v = beta2 * v + (1 - beta2) * grad**2
                
                # Bias correction
                m_hat = m / (1 - beta1**(i+1))
                v_hat = v / (1 - beta2**(i+1))
                
                # Update parameters
                x_new = x - learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
                
                if np.linalg.norm(x_new - x) < tol:
                    break
                
                x = x_new
                history.append(x.copy())
            
            return x, history, i+1
        
        x_adam, history_adam, iter_adam = adam_optimizer(x0, learning_rate=0.1)
        
        print(f"   Final point: ({x_adam[0]:.4f}, {x_adam[1]:.4f})")
        print(f"   Final value: {objective(x_adam):.6f}")
        print(f"   Iterations: {iter_adam}")
        
        # Compare convergence
        print(f"\n📊 Convergence Comparison:")
        methods = ['Gradient Descent', 'Momentum', 'Adam']
        final_points = [x_gd, x_mom, x_adam]
        iterations = [iter_gd, iter_mom, iter_adam]
        
        for method, point, iters in zip(methods, final_points, iterations):
            error = np.linalg.norm(point - np.array([2, 1]))
            print(f"   {method:16}: {iters:3d} iterations, error: {error:.6f}")
        
        print(f"\n💡 ML Application:")
        print("   - SGD: Training neural networks, logistic regression")
        print("   - Momentum: Accelerated convergence, escape local minima")
        print("   - Adam: Adaptive learning rates, robust to hyperparameters")


# =============================================================================
# 5. INFORMATION THEORY
# =============================================================================

class InformationTheory:
    """
    Information Theory concepts for ML/AI
    """
    
    def __init__(self):
        self.name = "Information Theory for ML/AI"
        print(f"📡 {self.name} - Quantifying Information and Uncertainty")
    
    def entropy_and_information(self) -> None:
        """
        Demonstrate entropy and information content
        """
        print("\n" + "="*60)
        print("📊 ENTROPY & INFORMATION CONTENT")
        print("="*60)
        
        print("📚 Key Concepts:")
        print("   Entropy: H(X) = -Σ p(x) log p(x)")
        print("   Information: I(x) = -log p(x)")
        print("   Higher entropy = More uncertainty/information")
        
        # Example 1: Coin flip entropy
        print(f"\n🪙 Coin Flip Examples:")
        
        def entropy(probabilities):
            """Calculate entropy given probabilities"""
            # Remove zero probabilities to avoid log(0)
            p = np.array(probabilities)
            p = p[p > 0]
            return -np.sum(p * np.log2(p))
        
        # Fair coin
        fair_coin = [0.5, 0.5]
        fair_entropy = entropy(fair_coin)
        
        # Biased coin
        biased_coin = [0.9, 0.1]
        biased_entropy = entropy(biased_coin)
        
        # Deterministic "coin"
        deterministic = [1.0, 0.0]
        deterministic_entropy = entropy(deterministic)
        
        print(f"   Fair coin P(H)=0.5:        H = {fair_entropy:.3f} bits")
        print(f"   Biased coin P(H)=0.9:      H = {biased_entropy:.3f} bits")
        print(f"   Deterministic P(H)=1.0:    H = {deterministic_entropy:.3f} bits")
        
        # Example 2: Text entropy
        print(f"\n📝 Text Entropy Example:")
        
        text1 = "aaaaaaaa"  # Low entropy
        text2 = "abcdefgh"  # High entropy
        text3 = "aabbccdd"  # Medium entropy
        
        def text_entropy(text):
            """Calculate entropy of text based on character frequencies"""
            char_counts = {}
            for char in text:
                char_counts[char] = char_counts.get(char, 0) + 1
            
            total_chars = len(text)
            probabilities = [count / total_chars for count in char_counts.values()]
            
            return entropy(probabilities), char_counts
        
        for i, text in enumerate([text1, text2, text3], 1):
            h, counts = text_entropy(text)
            print(f"   Text {i}: '{text}' → H = {h:.3f} bits, {dict(counts)}")
        
        # Example 3: Decision tree entropy
        print(f"\n🌳 Decision Tree Example:")
        print("   Dataset: Weather conditions for playing tennis")
        
        # Sample dataset: [Sunny, Overcast, Rainy] × [Play, Don't Play]
        weather_data = {
            'Sunny': {'Play': 2, 'No': 3},
            'Overcast': {'Play': 4, 'No': 0},
            'Rainy': {'Play': 3, 'No': 2}
        }
        
        # Calculate total entropy
        total_play = sum(data['Play'] for data in weather_data.values())
        total_no = sum(data['No'] for data in weather_data.values())
        total_entropy = entropy([total_play/(total_play+total_no), total_no/(total_play+total_no)])
        
        print(f"   Total samples: {total_play + total_no} (Play: {total_play}, No: {total_no})")
        print(f"   Total entropy: {total_entropy:.3f} bits")
        
        # Calculate weighted entropy for each weather condition
        weighted_entropy = 0
        total_samples = total_play + total_no
        
        print(f"   Conditional entropies:")
        for weather, data in weather_data.items():
            play, no = data['Play'], data['No']
            condition_total = play + no
            if condition_total > 0:
                condition_entropy = entropy([play/condition_total, no/condition_total]) if play > 0 and no > 0 else 0
                weight = condition_total / total_samples
                weighted_entropy += weight * condition_entropy
                
                print(f"     {weather:8}: {condition_total} samples, H = {condition_entropy:.3f}, weight = {weight:.3f}")
        
        information_gain = total_entropy - weighted_entropy
        print(f"   Information Gain: {information_gain:.3f} bits")
        
        print(f"\n💡 ML Application:")
        print("   - Decision Trees: Information gain for splitting criteria")
        print("   - Feature Selection: Mutual information between features and target")
        print("   - Model Compression: Quantify information lost in compression")
    
    def mutual_information_kl_divergence(self) -> None:
        """
        Demonstrate mutual information and KL divergence
        """
        print("\n" + "="*60)
        print("🔗 MUTUAL INFORMATION & KL DIVERGENCE")
        print("="*60)
        
        # Mutual Information
        print("📚 Mutual Information:")
        print("   I(X;Y) = H(X) - H(X|Y) = Σ p(x,y) log[p(x,y)/(p(x)p(y))]")
        print("   Measures statistical dependence between variables")
        
        # Generate correlated data
        np.random.seed(42)
        n_samples = 1000
        
        # Independent variables
        x_indep = np.random.randint(0, 2, n_samples)
        y_indep = np.random.randint(0, 2, n_samples)
        
        # Dependent variables
        x_dep = np.random.randint(0, 2, n_samples)
        y_dep = np.logical_xor(x_dep, np.random.randint(0, 2, n_samples) == 0).astype(int)
        
        def mutual_information_discrete(x, y):
            """Calculate mutual information for discrete variables"""
            # Joint probability
            xy_counts = {}
            x_counts = {}
            y_counts = {}
            n = len(x)
            
            for xi, yi in zip(x, y):
                xy_counts[(xi, yi)] = xy_counts.get((xi, yi), 0) + 1
                x_counts[xi] = x_counts.get(xi, 0) + 1
                y_counts[yi] = y_counts.get(yi, 0) + 1
            
            # Calculate mutual information
            mi = 0
            for (xi, yi), count in xy_counts.items():
                p_xy = count / n
                p_x = x_counts[xi] / n
                p_y = y_counts[yi] / n
                
                if p_xy > 0 and p_x > 0 and p_y > 0:
                    mi += p_xy * np.log2(p_xy / (p_x * p_y))
            
            return mi
        
        mi_indep = mutual_information_discrete(x_indep, y_indep)
        mi_dep = mutual_information_discrete(x_dep, y_dep)
        
        print(f"\n🔸 Mutual Information Examples:")
        print(f"   Independent variables: I(X;Y) = {mi_indep:.4f} bits")
        print(f"   Dependent variables:   I(X;Y) = {mi_dep:.4f} bits")
        
        # KL Divergence
        print(f"\n📚 KL Divergence:")
        print("   D_KL(P||Q) = Σ p(x) log[p(x)/q(x)]")
        print("   Measures how one distribution differs from another")
        
        def kl_divergence(p, q):
            """Calculate KL divergence between two distributions"""
            # Add small epsilon to avoid log(0)
            epsilon = 1e-10
            p = np.array(p) + epsilon
            q = np.array(q) + epsilon
            
            # Normalize
            p = p / np.sum(p)
            q = q / np.sum(q)
            
            return np.sum(p * np.log(p / q))
        
        # Example distributions
        p_uniform = [0.25, 0.25, 0.25, 0.25]
        q_uniform = [0.25, 0.25, 0.25, 0.25]
        p_skewed = [0.7, 0.2, 0.08, 0.02]
        q_different = [0.1, 0.3, 0.4, 0.2]
        
        print(f"\n🔸 KL Divergence Examples:")
        
        kl_same = kl_divergence(p_uniform, q_uniform)
        kl_diff1 = kl_divergence(p_uniform, p_skewed)
        kl_diff2 = kl_divergence(p_skewed, p_uniform)
        kl_diff3 = kl_divergence(p_skewed, q_different)
        
        print(f"   D_KL(Uniform || Uniform):     {kl_same:.6f}")
        print(f"   D_KL(Uniform || Skewed):      {kl_diff1:.6f}")
        print(f"   D_KL(Skewed || Uniform):      {kl_diff2:.6f}")
        print(f"   D_KL(Skewed || Different):    {kl_diff3:.6f}")
        
        print(f"\n   Note: KL divergence is not symmetric!")
        print(f"   D_KL(P||Q) ≠ D_KL(Q||P) in general")
        
        # Cross-entropy
        print(f"\n📚 Cross-Entropy:")
        print("   H(P,Q) = -Σ p(x) log q(x) = H(P) + D_KL(P||Q)")
        print("   Used as loss function in classification")
        
        def cross_entropy(y_true, y_pred):
            """Calculate cross-entropy loss"""
            epsilon = 1e-15
            y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
            return -np.sum(y_true * np.log(y_pred))
        
        # Binary classification example
        y_true = np.array([1, 0, 1, 1, 0])  # True labels
        y_pred_good = np.array([0.9, 0.1, 0.8, 0.95, 0.05])  # Good predictions
        y_pred_bad = np.array([0.4, 0.6, 0.3, 0.2, 0.7])     # Bad predictions
        
        # Convert to one-hot for cross-entropy
        y_true_onehot = np.column_stack([1-y_true, y_true])
        y_pred_good_onehot = np.column_stack([1-y_pred_good, y_pred_good])
        y_pred_bad_onehot = np.column_stack([1-y_pred_bad, y_pred_bad])
        
        ce_good = np.mean([cross_entropy(yt, yp) for yt, yp in zip(y_true_onehot, y_pred_good_onehot)])
        ce_bad = np.mean([cross_entropy(yt, yp) for yt, yp in zip(y_true_onehot, y_pred_bad_onehot)])
        
        print(f"\n🔸 Cross-Entropy Loss Examples:")
        print(f"   Good predictions: {ce_good:.4f}")
        print(f"   Bad predictions:  {ce_bad:.4f}")
        
        print(f"\n💡 ML Application:")
        print("   - Feature Selection: Mutual information for feature relevance")
        print("   - Model Training: Cross-entropy loss for classification")
        print("   - Generative Models: KL divergence in VAE loss functions")
        print("   - Information Bottleneck: Trade-off between compression and prediction")


# =============================================================================
# 6. COMPREHENSIVE DEMONSTRATION
# =============================================================================

def comprehensive_demo():
    """
    Run comprehensive demonstration of all mathematical concepts
    """
    print("="*80)
    print("🎓 MATHEMATICS FOR MACHINE LEARNING, AI, AND DATA SCIENCE")
    print("   Comprehensive Tutorial and Implementation Guide")
    print("="*80)
    
    # Initialize all modules
    modules = [
        LinearAlgebra(),
        ProbabilityTheory(), 
        Statistics(),
        Calculus(),
        InformationTheory()
    ]
    
    print(f"\n📋 Tutorial Overview:")
    print(f"   ✅ Linear Algebra: Vectors, matrices, eigenvalues, SVD")
    print(f"   ✅ Probability Theory: Distributions, Bayes' theorem, CLT")
    print(f"   ✅ Statistics: Descriptive stats, correlation, hypothesis testing")
    print(f"   ✅ Calculus: Derivatives, gradients, optimization methods")
    print(f"   ✅ Information Theory: Entropy, mutual information, KL divergence")
    
    # Run demonstrations
    try:
        # Linear Algebra
        print(f"\n" + "🔶"*80)
        modules[0].vector_operations()
        modules[0].matrix_operations() 
        modules[0].eigenvalues_eigenvectors()
        modules[0].singular_value_decomposition()
        
        # Probability Theory
        print(f"\n" + "🔶"*80)
        modules[1].basic_probability()
        modules[1].conditional_probability_bayes()
        modules[1].probability_distributions()
        modules[1].central_limit_theorem()
        
        # Statistics
        print(f"\n" + "🔶"*80)
        modules[2].descriptive_statistics()
        modules[2].correlation_analysis()
        modules[2].hypothesis_testing()
        
        # Calculus
        print(f"\n" + "🔶"*80)
        modules[3].derivatives_and_gradients()
        modules[3].chain_rule_backpropagation()
        modules[3].optimization_methods()
        
        # Information Theory
        print(f"\n" + "🔶"*80)
        modules[4].entropy_and_information()
        modules[4].mutual_information_kl_divergence()
        
        print(f"\n" + "="*80)
        print("🎉 TUTORIAL COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        print(f"\n📚 Learning Summary:")
        print(f"   🧮 You've learned the mathematical foundations of ML/AI/Data Science")
        print(f"   📊 Each concept was demonstrated with practical examples")
        print(f"   💻 All implementations use only NumPy for educational clarity")
        print(f"   🔗 Direct connections to ML algorithms were highlighted")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Practice implementing these concepts from scratch")
        print(f"   2. Apply them to real ML problems (regression, classification, etc.)")
        print(f"   3. Explore advanced topics (manifold learning, optimal transport, etc.)")
        print(f"   4. Study specific algorithms that use these mathematical tools")
        
        print(f"\n💡 Key Takeaways:")
        print(f"   • Linear algebra powers neural networks and dimensionality reduction")
        print(f"   • Probability theory enables uncertainty quantification and Bayesian methods")
        print(f"   • Statistics provides tools for data analysis and model evaluation")
        print(f"   • Calculus enables optimization and gradient-based learning")
        print(f"   • Information theory quantifies uncertainty and model complexity")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        print("   Check your NumPy and SciPy installations")


# =============================================================================
# INTERACTIVE LEARNING UTILITIES
# =============================================================================

class MathematicsLearningPath:
    """
    Interactive learning path and utilities
    """
    
    def __init__(self):
        self.name = "Mathematics Learning Path"
        self.topics = {
            'linear_algebra': {
                'name': 'Linear Algebra',
                'prerequisites': [],
                'difficulty': 'Beginner',
                'concepts': ['Vectors', 'Matrices', 'Eigenvalues', 'SVD']
            },
            'probability': {
                'name': 'Probability Theory', 
                'prerequisites': [],
                'difficulty': 'Beginner',
                'concepts': ['Basic Probability', 'Bayes Theorem', 'Distributions']
            },
            'statistics': {
                'name': 'Statistics',
                'prerequisites': ['probability'],
                'difficulty': 'Intermediate', 
                'concepts': ['Descriptive Stats', 'Inference', 'Hypothesis Testing']
            },
            'calculus': {
                'name': 'Calculus',
                'prerequisites': ['linear_algebra'],
                'difficulty': 'Intermediate',
                'concepts': ['Derivatives', 'Chain Rule', 'Optimization']
            },
            'information_theory': {
                'name': 'Information Theory',
                'prerequisites': ['probability', 'statistics'],
                'difficulty': 'Advanced',
                'concepts': ['Entropy', 'Mutual Information', 'KL Divergence']
            }
        }
    
    def show_learning_path(self):
        """Display recommended learning path"""
        print("\n" + "="*60)
        print("🗺️  RECOMMENDED LEARNING PATH")
        print("="*60)
        
        levels = {
            'Beginner': [],
            'Intermediate': [],
            'Advanced': []
        }
        
        for topic_id, topic_info in self.topics.items():
            levels[topic_info['difficulty']].append(topic_info)
        
        for level, topics in levels.items():
            print(f"\n📚 {level} Level:")
            for i, topic in enumerate(topics, 1):
                prereqs = [self.topics[p]['name'] for p in topic.get('prerequisites', [])]
                prereq_str = f" (Prerequisites: {', '.join(prereqs)})" if prereqs else ""
                print(f"   {i}. {topic['name']}{prereq_str}")
                
                concepts_str = ", ".join(topic['concepts'])
                print(f"      Topics: {concepts_str}")
    
    def generate_practice_problems(self, topic: str = None):
        """Generate practice problems for given topic"""
        print("\n" + "="*60)
        print("📝 PRACTICE PROBLEMS")
        print("="*60)
        
        problems = {
            'linear_algebra': [
                "1. Calculate the dot product of vectors [1,2,3] and [4,5,6]",
                "2. Find the eigenvalues of matrix [[3,1],[1,3]]",
                "3. Compute the SVD of a 3×2 random matrix",
                "4. Verify that (AB)^T = B^T A^T for random matrices A and B"
            ],
            'probability': [
                "1. A bag contains 5 red and 3 blue balls. What's P(red then blue without replacement)?",
                "2. Given P(Disease)=0.01, P(Test+|Disease)=0.95, P(Test+|No Disease)=0.05, find P(Disease|Test+)",
                "3. Generate 1000 samples from Normal(μ=10, σ=2) and verify the mean",
                "4. Demonstrate the law of large numbers with coin flips"
            ],
            'statistics': [
                "1. Calculate mean, median, mode, and standard deviation of a dataset",
                "2. Test if two groups have different means using t-test",
                "3. Calculate correlation between two variables and interpret",
                "4. Perform chi-square test for independence on categorical data"
            ],
            'calculus': [
                "1. Find the derivative of f(x) = x³ - 2x² + x - 1",
                "2. Implement gradient descent to minimize f(x,y) = x² + y² - 2x - 4y + 5", 
                "3. Verify the chain rule: d/dx[f(g(x))] = f'(g(x))×g'(x)",
                "4. Compare convergence of SGD vs Adam optimizer"
            ],
            'information_theory': [
                "1. Calculate entropy of a biased coin with P(H)=0.7",
                "2. Find mutual information between two random variables",
                "3. Compute KL divergence between two normal distributions",
                "4. Calculate cross-entropy loss for a classification problem"
            ]
        }
        
        if topic and topic in problems:
            print(f"Practice problems for {self.topics[topic]['name']}:")
            for problem in problems[topic]:
                print(f"   {problem}")
        else:
            print("Practice problems for all topics:")
            for topic_id, problem_list in problems.items():
                print(f"\n🔸 {self.topics[topic_id]['name']}:")
                for problem in problem_list:
                    print(f"   {problem}")
    
    def show_ml_applications(self):
        """Show how each mathematical concept applies to ML"""
        print("\n" + "="*60)
        print("🤖 ML/AI APPLICATIONS")
        print("="*60)
        
        applications = {
            'Linear Algebra': {
                'Neural Networks': 'Matrix multiplication in forward pass, weight matrices',
                'PCA': 'Eigenvalue decomposition of covariance matrix',
                'Recommendation Systems': 'Matrix factorization (SVD) for collaborative filtering',
                'Computer Vision': 'Image transformations, feature extraction',
                'NLP': 'Word embeddings, attention mechanisms'
            },
            'Probability Theory': {
                'Naive Bayes': 'Bayes theorem for classification',
                'Bayesian Networks': 'Probabilistic reasoning and inference',
                'Gaussian Processes': 'Prior distributions over functions',
                'Monte Carlo Methods': 'Sampling-based algorithms',
                'Uncertainty Quantification': 'Model confidence estimation'
            },
            'Statistics': {
                'Hypothesis Testing': 'A/B testing, statistical significance',
                'Confidence Intervals': 'Model performance estimation',
                'Feature Selection': 'Statistical tests for feature importance',
                'Model Evaluation': 'Cross-validation, bootstrap methods',
                'Experimental Design': 'Controlled experiments, causal inference'
            },
            'Calculus': {
                'Gradient Descent': 'Parameter optimization in ML models',
                'Backpropagation': 'Chain rule for neural network training',
                'Lagrange Multipliers': 'Constrained optimization (SVM)',
                'Taylor Series': 'Function approximation, optimization',
                'Automatic Differentiation': 'Efficient gradient computation'
            },
            'Information Theory': {
                'Decision Trees': 'Information gain for splitting criteria',
                'Feature Selection': 'Mutual information for relevance',
                'Model Compression': 'Quantify information loss',
                'Generative Models': 'KL divergence in variational inference',
                'Cross-entropy Loss': 'Classification objective function'
            }
        }
        
        for math_area, ml_apps in applications.items():
            print(f"\n🔸 {math_area}:")
            for ml_method, description in ml_apps.items():
                print(f"   • {ml_method:20}: {description}")


if __name__ == "__main__":
    print("🎓 Mathematics for Machine Learning, AI, and Data Science")
    print("   Interactive Tutorial and Reference Implementation")
    print("\n" + "="*80)
    
    # Run comprehensive demonstration
    comprehensive_demo()
    
    # Show learning path and additional resources
    learning_path = MathematicsLearningPath()
    learning_path.show_learning_path()
    learning_path.generate_practice_problems()
    learning_path.show_ml_applications()
    
    print("\n" + "="*80)
    print("📖 End of Mathematics Tutorial")
    print("   Continue exploring and practicing these fundamental concepts!")
    print("="*80)
