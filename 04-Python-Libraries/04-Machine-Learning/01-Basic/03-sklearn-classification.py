"""
# ==============================================================================
# LABORATORY: CLASSIFICATION ALGORITHMS (SCIKIT-LEARN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Classification is the process of predicting discrete categories. 
# - Is this tumor Malignant (1) or Benign (0)?
# - Is this image a Cat, Dog, or Bird?
#
# Scikit-Learn provides an arsenal of Classification algorithms. Each algorithm 
# approaches the geometry of the data using entirely different mathematics:
# 1. Logistic Regression: Draws a rigid straight line (hyperplane) through the data.
# 2. Support Vector Machines (SVM): Uses the "Kernel Trick" to warp the universe 
#    into higher dimensions to find complex boundaries.
# 3. K-Nearest Neighbors (KNN): Memorizes the data and looks at the closest points.
# 4. Decision Trees: Uses `if/else` rules based on Information Theory (Entropy).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Logistic Regression is a Classifier, not a Regressor.
# - Execute Support Vector Machines (SVM) and understand the RBF Kernel.
# - Execute K-Nearest Neighbors (KNN) and understand the Curse of Dimensionality.
# - Execute Decision Trees and understand Gini Impurity.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd
import time

# In a real environment: pip install scikit-learn
try:
    from sklearn.datasets import make_classification, make_circles
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, f1_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. LOGISTIC REGRESSION (LINEAR CLASSIFICATION)
# ==============================================================================
def demonstrate_logistic():
    section_header("Logistic Regression (Sigmoid Function)")
    
    if not HAS_SKLEARN: return
    
    print("Logistic Regression calculates a linear equation ($WX + b$) exactly like ")
    print("Linear Regression, but it wraps the result in a 'Sigmoid' function ")
    print("which perfectly squashes any number (even 1,000,000) into a strict ")
    print("Probability between 0.0 and 1.0!\n")
    
    # Generate simple separable data
    X, y = make_classification(n_samples=500, n_features=2, n_informative=2, n_redundant=0, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    
    # Predict Probabilities
    # Instead of just returning [1, 0], we can ask for the exact probability!
    probs = clf.predict_proba(X_test)
    preds = clf.predict(X_test)
    
    print("Example Prediction:")
    print(f"Model Probability of Class 0: {probs[0][0]*100:.1f}%")
    print(f"Model Probability of Class 1: {probs[0][1]*100:.1f}%")
    print(f"Final Decision (Threshold 0.5): Class {preds[0]}")
    print(f"Accuracy: {accuracy_score(y_test, preds)*100:.1f}%")


# ==============================================================================
# 4. SUPPORT VECTOR MACHINES (THE KERNEL TRICK)
# ==============================================================================
def demonstrate_svm():
    section_header("Support Vector Machines & The Kernel Trick")
    
    if not HAS_SKLEARN: return
    
    print("What if the data cannot be separated by a straight line?")
    print("Imagine a target (a red bullseye surrounded by a blue ring).")
    
    # Generate non-linear data (Circles!)
    X, y = make_circles(n_samples=500, noise=0.1, factor=0.5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. ATTEMPT WITH LOGISTIC REGRESSION
    # It tries to draw a straight line through circles... and fails miserably.
    linear = LogisticRegression().fit(X_train, y_train)
    print(f"Logistic Regression Accuracy on Circles: {accuracy_score(y_test, linear.predict(X_test))*100:.1f}% (Total failure)")
    
    # 2. ATTEMPT WITH SVM (RBF KERNEL)
    # The Radial Basis Function (RBF) Kernel mathematically projects the 2D circles 
    # into a 3rd spatial dimension (Z-axis) where the red bullseye physically 
    # pops up like a mountain. The SVM then slices a flat plane underneath the 
    # mountain, achieving perfect separation without ever actually calculating 
    # the complex 3D math (The Kernel Trick!).
    svm = SVC(kernel='rbf', gamma='auto').fit(X_train, y_train)
    print(f"SVM (RBF Kernel) Accuracy on Circles : {accuracy_score(y_test, svm.predict(X_test))*100:.1f}% (Perfect!)")


# ==============================================================================
# 5. K-NEAREST NEIGHBORS (LAZY LEARNING)
# ==============================================================================
def demonstrate_knn():
    section_header("K-Nearest Neighbors (KNN)")
    
    if not HAS_SKLEARN: return
    
    print("KNN is a 'Lazy Learner'. It does absolutely zero math during the `.fit()` ")
    print("phase. It just memorizes the entire dataset into RAM.")
    print("During `.predict()`, it calculates the Euclidean distance to every ")
    print("single point in the dataset, finds the 'K' closest points, and takes a vote.")
    
    X, y = make_classification(n_samples=2000, n_features=20, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Must scale data for KNN!
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    start = time.perf_counter()
    knn = KNeighborsClassifier(n_neighbors=5)
    
    # "Training" takes 0.0001 seconds (just copying arrays)
    knn.fit(X_train, y_train)
    train_time = time.perf_counter() - start
    
    start = time.perf_counter()
    preds = knn.predict(X_test)
    pred_time = time.perf_counter() - start
    
    print(f"KNN Training Time  : {train_time:.6f} seconds (Instant)")
    print(f"KNN Prediction Time: {pred_time:.6f} seconds (Slow! Has to calculate millions of distances)")
    print(f"Accuracy: {accuracy_score(y_test, preds)*100:.1f}%")


# ==============================================================================
# 6. DECISION TREES (INFORMATION THEORY)
# ==============================================================================
def demonstrate_trees():
    section_header("Decision Trees (Entropy & Gini Impurity)")
    
    if not HAS_SKLEARN: return
    
    print("Decision Trees do not use geometry or distance. They use Boolean Logic.")
    print("At every step, the tree searches for the single Feature and Threshold ")
    print("that maximizes 'Information Gain' (separating the 1s from the 0s perfectly).")
    
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # max_depth prevents the tree from growing infinitely and overfitting.
    tree = DecisionTreeClassifier(max_depth=5, criterion='gini', random_state=42)
    tree.fit(X_train, y_train)
    
    print(f"Decision Tree Accuracy: {accuracy_score(y_test, tree.predict(X_test))*100:.1f}%")
    print(f"Tree Depth used: {tree.get_depth()}")
    print(f"Total logical splits (Leaves): {tree.get_n_leaves()}")
    
    # Trees natively calculate Feature Importance!
    importances = tree.feature_importances_
    most_important = np.argmax(importances)
    print(f"The Tree mathematically proved that Feature #{most_important} is the most critical variable!")


def run_all_labs():
    demonstrate_logistic()
    demonstrate_svm()
    demonstrate_knn()
    demonstrate_trees()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Logistic Regression called a 'Regression' if it is used for Classification?
   Answer: It is named after the underlying mathematical equation it uses: the continuous Logistic (Sigmoid) function. At its core, it still runs standard linear regression ($WX + b$) to calculate a continuous raw score (the log-odds). It then wraps that continuous score in the Sigmoid function to squash it into a continuous probability between $0.0$ and $1.0$. Because the underlying math is continuous regression, it keeps the name, even though we use an arbitrary threshold (e.g. $0.5$) to force it into discrete buckets.

2. What is the "Kernel Trick" in Support Vector Machines?
   Answer: When data cannot be separated by a straight 2D line (like a circle inside another circle), you must project the data into a higher dimension (3D or 4D) where it can be sliced by a flat plane. However, physically calculating the coordinates of millions of data points in 10,000-dimensional space requires immense computing power. The "Kernel Trick" is a mathematical shortcut (using Dot Products). It calculates the exact angle and distance between the points in the infinite-dimensional space without ever actually translating them there in RAM! It solves impossible geometries in milliseconds.

3. Why is KNN highly susceptible to the "Curse of Dimensionality"?
   Answer: KNN relies exclusively on the physical distance between points ($d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$). In 2D or 3D space, distance is meaningful. However, as the number of features (dimensions) grows to 50, 100, or 1000, the mathematical volume of the universe explodes exponentially. In a 1000-dimensional space, the points are spread so unimaginably far apart that the physical distance between the "closest" point and the "farthest" point becomes mathematically negligible. The algorithm effectively goes blind because everything is infinitely far away from everything else.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Classification Algorithms Completed.")
