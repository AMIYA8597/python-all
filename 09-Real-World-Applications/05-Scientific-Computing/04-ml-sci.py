\"\"\"
Scientific Computing in Python: Machine Learning for Science

What is it?
-----------
Using Machine Learning (ML) techniques applied specifically to scientific data to discover patterns, make predictions, and understand underlying physical/chemical/biological phenomena. We heavily rely on `scikit-learn` for traditional ML and `scipy`/`numpy` for data manipulation.

Why does it exist?
------------------
Traditional scientific computing relies on solving known governing equations (like Navier-Stokes for fluids or Schrödinger for quantum mechanics). However, many systems are too complex, or the equations are unknown. ML allows scientists to build data-driven models directly from experimental or simulated data.

Industry Use Cases:
-------------------
- Materials Science: Predicting properties (like bandgap or elasticity) of new chemical compounds without running expensive quantum mechanical simulations.
- Genomics: Classifying gene expression data to identify disease markers.
- Astronomy: Automatically classifying galaxies from telescope images.
- Climate Science: Downscaling global climate models to predict local weather phenomena using historical data.

Beginner Explanation:
---------------------
Imagine you have hundreds of measurements of different flowers (petal length, width, etc.) and you know their species. You want a rule to identify new flowers automatically. ML algorithms look at your old data (training data) and figure out the best rules. You can then use these rules on new flowers (testing data).

Advanced Technical Explanation:
-------------------------------
Scientific ML often requires models with high interpretability and adherence to physical constraints (Physics-Informed ML). Traditional models like Ridge/Lasso Regression, Support Vector Machines (SVM), and Random Forests are preferred over Deep Learning for tabular scientific data because their feature importance and decision boundaries can be rigorously analyzed.
We use Principal Component Analysis (PCA) to project high-dimensional scientific data onto a lower-dimensional orthogonal basis that captures maximal variance, often revealing underlying physical degrees of freedom. Regularization (L1/L2 penalties) is crucial in scientific domains to prevent overfitting on scarce experimental data (the "large P, small N" problem, where features outnumber samples).

Practical Examples Included:
1. Dimensionality Reduction (PCA) on a dataset.
2. Unsupervised Clustering (K-Means) to find natural groupings in data.
3. Supervised Regression (Ridge) to predict a continuous variable.
4. Model evaluation using cross-validation.

Performance Considerations:
---------------------------
- Model training can be computationally expensive. Use randomized solvers (e.g., `svd_solver='randomized'` in PCA) for very large scientific datasets.
- Ensure memory efficiency by using sparse matrices (via `scipy.sparse`) when most features are zero (e.g., one-hot encoded genomics data).

Security Concerns:
------------------
- Data poisoning: If experimental data used for training is maliciously altered, the resulting scientific model will be flawed.
- Serialization: Never unpickle untrusted ML models (`.pkl`), as `pickle` can execute arbitrary code. Use safer formats like ONNX.

Interview Questions:
--------------------
1. In a scientific context where we have 10,000 features but only 50 samples, what type of regression would you use and why?
   *Answer: I would use Lasso (L1 regularization) or Elastic Net. Ordinary Least Squares would be massively underdetermined and overfit. L1 regularization forces most feature coefficients to exactly zero, performing automatic feature selection, which is vital for interpretability in science.*
2. How does PCA calculate the principal components?
   *Answer: PCA computes the covariance matrix of the mean-centered data, and then calculates the eigenvalues and eigenvectors of this matrix. The eigenvectors correspond to the principal components, and the eigenvalues denote the variance explained by each component.*

Practical Exercises:
--------------------
1. Load the `load_diabetes` dataset from sklearn and build a Random Forest regressor. Plot the feature importances to see which factors matter most.
2. Implement a custom train-test split that ensures stratification, which is critical when dealing with imbalanced rare scientific events.
3. Use DBSCAN clustering instead of K-Means on a non-linearly separable dataset (like `make_moons`) and compare the results.
\"\"\"

import numpy as np
from sklearn.datasets import make_regression, make_blobs
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def demonstrate_pca():
    \"\"\"
    Demonstrates Principal Component Analysis (PCA) for dimensionality reduction.
    This is commonly used in science to visualize high-dimensional data or remove noise.
    \"\"\"
    print("\n--- Dimensionality Reduction (PCA) ---")
    # Simulate a high-dimensional dataset (e.g., 50 features per sample)
    # where only 3 features actually contain useful variance (the rest is noise)
    np.random.seed(42)
    X = np.random.randn(200, 50) 
    
    # Add strong covariance structure to simulate physical phenomena
    X[:, 0] = X[:, 1] * 2 + np.random.randn(200) * 0.1
    X[:, 2] = X[:, 1] * -1.5 + np.random.randn(200) * 0.1
    
    # Apply PCA to reduce down to 3 components
    pca = PCA(n_components=3)
    X_reduced = pca.fit_transform(X)
    
    explained_variance = pca.explained_variance_ratio_
    
    print(f"Original shape: {X.shape}, Reduced shape: {X_reduced.shape}")
    print(f"Explained variance ratio by top 3 components: {explained_variance}")
    print(f"Total variance explained: {sum(explained_variance) * 100:.2f}%")
    print("Notice how the first few components capture a disproportionate amount of variance due to the correlated features.")

def demonstrate_clustering():
    \"\"\"
    Demonstrates K-Means clustering.
    Used in science for things like identifying sub-populations of cells or astronomical object types.
    \"\"\"
    print("\n--- Unsupervised Clustering (K-Means) ---")
    # Generate synthetic clustered data (e.g., 4 distinct sub-species)
    X, true_labels = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
    
    # Initialize and fit K-Means
    kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42, n_init=10)
    kmeans.fit(X)
    
    # Get the cluster centers and predicted labels
    centers = kmeans.cluster_centers_
    predicted_labels = kmeans.labels_
    
    # In a real scenario, we don't have true_labels. We evaluate based on metrics like Silhouette score.
    print(f"Algorithm identified {len(centers)} clusters.")
    print("Cluster Centers coordinates:")
    for i, c in enumerate(centers):
        print(f"  Cluster {i}: [{c[0]:.2f}, {c[1]:.2f}]")


def demonstrate_regression():
    \"\"\"
    Demonstrates Ridge Regression (Linear Regression with L2 regularization).
    Used in science to predict physical properties while avoiding overfitting on small datasets.
    \"\"\"
    print("\n--- Supervised Regression (Ridge) ---")
    # Generate synthetic regression data (e.g., predicting temperature from various sensor readings)
    # n_informative=5 means only 5 out of 15 features actually affect the output
    X, y = make_regression(n_samples=100, n_features=15, n_informative=5, noise=10.0, random_state=42)
    
    # Split data into training and testing sets to evaluate generalization
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize Ridge regression model. Alpha is the regularization strength.
    # Higher alpha forces coefficients closer to zero, reducing model complexity.
    model = Ridge(alpha=1.0)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on unseen data
    predictions = model.predict(X_test)
    
    # Evaluate model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Model trained on {X_train.shape[0]} samples. Tested on {X_test.shape[0]} samples.")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"R-squared (R2) Score: {r2:.3f} (1.0 is perfect prediction)")
    
    # Show coefficients
    print("\nFeature Coefficients (Notice some are close to 0 due to regularization):")
    for i, coef in enumerate(model.coef_):
        print(f"  Feature {i:02d}: {coef:.2f}")

if __name__ == "__main__":
    print("Starting Scientific Machine Learning Demonstrations...")
    demonstrate_pca()
    demonstrate_clustering()
    demonstrate_regression()
    print("\nDemonstrations completed successfully.")
