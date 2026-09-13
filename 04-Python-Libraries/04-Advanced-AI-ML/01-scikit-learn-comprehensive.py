"""
# ==============================================================================
# LABORATORY: PREDICTIVE MACHINE LEARNING (SCIKIT-LEARN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# If you need to predict whether an email is Spam, whether a patient has Cancer, 
# or what a House will sell for next month, you do not write hardcoded `if/else` 
# logic. You use Machine Learning.
#
# Scikit-Learn (sklearn) is the undisputed industry standard for traditional 
# Machine Learning in Python. It does not do Deep Learning (Neural Networks), 
# but it provides flawless, highly optimized C-implementations of Random Forests, 
# Support Vector Machines, Gradient Boosting, and K-Means Clustering.
#
# More importantly, it provides the "Estimator API"—a perfectly standardized 
# object-oriented interface (`.fit()`, `.predict()`) that allows you to swap 
# out entirely different mathematical algorithms with zero code changes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Scikit-Learn Estimator API (`fit`, `predict`).
# - Execute Supervised Classification (Random Forest).
# - Execute Unsupervised Clustering (K-Means).
# - Master Data Leakage prevention using `Pipeline` and `StandardScaler`.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from sklearn.cluster import KMeans
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SUPERVISED LEARNING (CLASSIFICATION)
# ==============================================================================
def demonstrate_classification():
    section_header("Supervised Learning (Random Forest Classification)")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed. Install using: pip install scikit-learn")
        return
        
    print("Scenario: Predicting whether a patient has Heart Disease (1=Yes, 0=No).")
    
    # 1. GENERATE SYNTHETIC DATA
    rng = np.random.default_rng(42)
    n_samples = 1000
    
    # Features (X)
    age = rng.uniform(30, 80, n_samples)
    cholesterol = rng.uniform(150, 300, n_samples)
    blood_pressure = rng.uniform(90, 180, n_samples)
    
    # Target (Y)
    # The probability of disease heavily depends on Age and BP!
    risk_score = (age * 0.4) + (cholesterol * 0.1) + (blood_pressure * 0.5)
    
    # If the risk score is in the top 40%, they have the disease (1). Otherwise (0).
    threshold = np.percentile(risk_score, 60)
    heart_disease = (risk_score > threshold).astype(int)
    
    X = pd.DataFrame({"Age": age, "Cholesterol": cholesterol, "BloodPressure": blood_pressure})
    y = heart_disease
    
    # 2. THE TRAIN / TEST SPLIT
    # CRITICAL: If you test the model on the exact same data it trained on, it will 
    # perfectly memorize the answers (Overfitting) and fail miserably in the real world.
    # We MUST withhold 20% of the data in a "Test Vault" that the model never sees!
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. INSTANTIATE THE ESTIMATOR
    # A Random Forest is an ensemble of 100 distinct Decision Trees voting together.
    clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    
    # 4. FIT THE MODEL (Training Phase)
    # The model mathematically analyzes X_train to figure out how it maps to y_train.
    clf.fit(X_train, y_train)
    print("Model successfully Trained (Fit) on 800 patients.")
    
    # 5. PREDICT (Testing Phase)
    # We ask the model to predict the disease status of the 200 hidden patients!
    predictions = clf.predict(X_test)
    
    # 6. EVALUATE
    accuracy = accuracy_score(y_test, predictions)
    print(f"\nModel Accuracy on unseen Test Data: {accuracy * 100:.2f}%\n")
    
    # The Classification Report shows Precision, Recall, and F1-Score for both classes!
    print("Detailed Classification Report:")
    print(classification_report(y_test, predictions))


# ==============================================================================
# 4. PREVENTING DATA LEAKAGE (PIPELINES & SCALERS)
# ==============================================================================
def demonstrate_pipelines():
    section_header("Data Leakage & Scikit-Learn Pipelines")
    
    if not HAS_SKLEARN: return
    
    print("Algorithms like Support Vector Machines (SVM) and K-Nearest Neighbors ")
    print("calculate the literal Euclidean distance between data points.")
    print("If Age is 0-100, and Salary is 0-100,000, the algorithm will completely ")
    print("ignore Age because the Salary math overwhelms it! We must SCALE the data.\n")
    
    # But if you scale the ENTIRE dataset BEFORE splitting into Train/Test, information 
    # from the Test set "leaks" into the Training set via the Mean calculation!
    # A `Pipeline` mathematically prevents this!
    
    # 1. GENERATE DATA
    X = np.random.rand(100, 2) * [100, 100000] # Massive scale imbalance
    y = np.random.randint(0, 2, 100)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. CONSTRUCT THE PIPELINE
    # The Pipeline chains together multiple steps into a single Object.
    # Step 1: StandardScaler (forces every column to have Mean=0, Variance=1).
    # Step 2: RandomForestClassifier.
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(random_state=42))
    ])
    
    # 3. FIT THE PIPELINE
    # MAGIC: The pipeline automatically calls `scaler.fit_transform()` on X_train, 
    # but strictly calls `scaler.transform()` on X_test during prediction, ensuring 
    # zero data leakage!
    pipeline.fit(X_train, y_train)
    
    preds = pipeline.predict(X_test)
    print(f"Pipeline successfully scaled the data and achieved Accuracy: {accuracy_score(y_test, preds):.2f}")


# ==============================================================================
# 5. UNSUPERVISED LEARNING (K-MEANS CLUSTERING)
# ==============================================================================
def demonstrate_clustering():
    section_header("Unsupervised Learning (K-Means)")
    
    if not HAS_SKLEARN: return
    
    print("In Unsupervised Learning, there is NO Target Variable (y).")
    print("You just dump raw data into the algorithm, and it finds mathematical ")
    print("patterns and groupings automatically (Clustering)!\n")
    
    # 1. GENERATE DATA
    # Simulating 3 distinct geographic clusters of customers.
    rng = np.random.default_rng(42)
    cluster_1 = rng.normal(loc=[10, 10], scale=1, size=(50, 2))
    cluster_2 = rng.normal(loc=[50, 50], scale=1, size=(50, 2))
    cluster_3 = rng.normal(loc=[10, 50], scale=1, size=(50, 2))
    
    # Combine them into a single unlabeled dataset
    X_unlabeled = np.vstack([cluster_1, cluster_2, cluster_3])
    
    # 2. INSTANTIATE THE K-MEANS ALGORITHM
    # We tell it to find exactly 3 clusters.
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    
    # 3. FIT AND PREDICT
    # Notice there is no `y` argument in the fit function!
    assigned_labels = kmeans.fit_predict(X_unlabeled)
    
    # 4. EXTRACT THE CENTROIDS
    centroids = kmeans.cluster_centers_
    
    print("K-Means successfully clustered the 150 unlabeled data points.")
    print("\nMathematical Coordinates of the 3 Discovered Centroids:")
    for i, center in enumerate(centroids):
        print(f"Cluster {i} Center: X={center[0]:.1f}, Y={center[1]:.1f}")
        
    print("\nNotice how closely they match our true hidden means: [10,10], [50,50], [10,50]!")


def run_all_labs():
    demonstrate_classification()
    demonstrate_pipelines()
    demonstrate_clustering()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between Supervised and Unsupervised Learning?
   Answer: In Supervised Learning (e.g., Random Forest), the dataset contains both Features ($X$) and explicitly labeled Targets ($y$). The algorithm acts as a "student" trying to learn the mathematical mapping from $X \rightarrow y$ using the provided answer key. In Unsupervised Learning (e.g., K-Means), the dataset contains ONLY Features ($X$). There is no answer key! The algorithm acts as a "detective", analyzing the geometry of the raw data to discover hidden clusters, structures, or anomalies without any human guidance.

2. What is Data Leakage, and how does the `Pipeline` object prevent it?
   Answer: Data Leakage occurs when information from the secret Test Set accidentally bleeds into the Training Phase, causing the model to artificially inflate its accuracy (and then fail in production). A classic mistake is calling `StandardScaler.fit_transform()` on the ENTIRE dataset before splitting it. The Scaler calculates the Mean of the entire dataset, meaning the Training data is now mathematically contaminated by the Test data! A Scikit-Learn `Pipeline` completely prevents this. When you call `pipeline.fit()`, it automatically fits the Scaler STRICTLY on the $X_{train}$ data. When you call `pipeline.predict()`, it scales $X_{test}$ using the saved $X_{train}$ mean, guaranteeing perfect mathematical isolation.

3. Why do algorithms like SVM and K-Means require Feature Scaling (Standardization), but Random Forests do not?
   Answer: SVM and K-Means rely heavily on spatial geometry and Euclidean distance calculations ($d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$). If $X$ is Age (0-100) and $Y$ is Salary (0-1,000,000), the massive numbers in the Salary column will mathematically completely overpower the Age column in the distance equation, rendering Age irrelevant. Scaling forces all columns to have a Mean of 0 and a Variance of 1, leveling the playing field. Random Forests do not calculate distance! They split data using Boolean logic (e.g., `if Age > 50: go left`). A Boolean threshold doesn't care if the data ranges from 0-100 or 0-1,000,000, making tree-based algorithms perfectly immune to unscaled data.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scikit-Learn Predictive Modeling Completed.")
