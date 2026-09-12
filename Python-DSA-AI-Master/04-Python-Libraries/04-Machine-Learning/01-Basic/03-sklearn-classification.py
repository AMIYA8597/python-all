"""
Module: 03-sklearn-classification
Description: A textbook-grade, interactive lesson on Machine Learning Classification using Scikit-Learn.

=========================================================================================
THEORY AND MATHEMATICAL BACKGROUND
=========================================================================================
Classification is a core supervised machine learning problem where the objective is to 
predict the categorical class labels of new instances, based on past observations.

1. Logistic Regression
   - Concept: Models the probability that a given input belongs to a certain class.
   - Math: Uses the logistic (sigmoid) function to map predictions to probabilities.
     P(y=1|x) = 1 / (1 + e^-(w.T * x + b))
   - Objective: Maximize the log-likelihood or minimize the Log-Loss (Cross-Entropy Loss).
     J(w) = -1/m \sum [ y_i * log(h(x_i)) + (1-y_i) * log(1-h(x_i)) ]
   - Big-O: 
     Training: O(n_samples * n_features * n_iterations)
     Prediction: O(n_features)

2. K-Nearest Neighbors (KNN)
   - Concept: An instance-based learning algorithm that classifies a new sample based 
     on the majority class among its 'k' nearest neighbors in the feature space.
   - Math: Typically uses Euclidean distance: d(p, q) = sqrt(\sum (p_i - q_i)^2)
   - Big-O:
     Training: O(1) (or O(n log n) if using tree structures like KD-tree)
     Prediction: O(n_samples * n_features) (very slow for large datasets)

3. Support Vector Machines (SVM)
   - Concept: Finds the hyperplane that maximizes the margin between different classes.
   - Math: Solves the constrained optimization problem:
     min(w, b) 1/2 ||w||^2 subject to y_i(w.T * x_i + b) >= 1 (for hard margin)
     For non-linear data, uses the "Kernel Trick" (e.g., RBF, Polynomial).
   - Big-O:
     Training: O(n_samples^2 * n_features) to O(n_samples^3 * n_features)
     Prediction: O(n_support_vectors * n_features)

4. Decision Trees
   - Concept: A tree-like model of decisions based on feature values.
   - Math: Splits nodes based on a criterion like Gini Impurity or Information Gain (Entropy).
     Gini(D) = 1 - \sum (p_i)^2
     Entropy(D) = - \sum (p_i * log2(p_i))
   - Big-O:
     Training: O(n_samples * n_features * log(n_samples))
     Prediction: O(log(n_samples)) or O(max_depth)

5. Random Forests
   - Concept: An ensemble learning method that constructs a multitude of decision trees 
     at training time (bagging) and outputs the mode of the classes.
   - Big-O:
     Training: O(n_trees * n_samples * n_features * log(n_samples))
     Prediction: O(n_trees * max_depth)

=========================================================================================
EVALUATION METRICS
=========================================================================================
- Accuracy: (TP + TN) / (TP + TN + FP + FN) -> Overall correctness.
- Precision: TP / (TP + FP) -> Proportion of positive identifications that are correct.
- Recall (Sensitivity): TP / (TP + FN) -> Proportion of actual positives identified correctly.
- F1-Score: 2 * (Precision * Recall) / (Precision + Recall) -> Harmonic mean.
- ROC-AUC: Area under the Receiver Operating Characteristic curve (TPR vs FPR).

=========================================================================================
REAL-WORLD APPLICATIONS
=========================================================================================
- Email Spam Detection (Logistic Regression, Naive Bayes)
- Medical Diagnosis - Cancer detection (SVM, Random Forests)
- Customer Churn Prediction (Random Forests, Gradient Boosting)
- Image Recognition (KNN, CNNs)
"""

import warnings
import time
import math
from typing import Tuple, Dict, Any, List, Optional
import numpy as np
import pandas as pd

# Suppress warnings for cleaner output during the tutorial
warnings.filterwarnings("ignore")

try:
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score, 
        roc_auc_score, confusion_matrix, classification_report
    )
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
except ImportError:
    print("Scikit-Learn is required for this module. Please install it using 'pip install scikit-learn'.")
    import sys
    sys.exit(1)


# =========================================================================================
# HELPER FUNCTIONS
# =========================================================================================
def generate_dataset(n_samples: int = 1000, n_features: int = 20, random_state: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates a synthetic binary classification dataset.
    
    Args:
        n_samples (int): Number of instances.
        n_features (int): Number of features (variables).
        random_state (int): Random seed for reproducibility.
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: The feature matrix X and target vector y.
    """
    print(f"[Dataset Generation] Creating synthetic dataset with {n_samples} samples and {n_features} features...")
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=10,
        n_redundant=5,
        n_classes=2,
        weights=[0.6, 0.4], # Slight class imbalance
        random_state=random_state
    )
    return X, y


def preprocess_data(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Splits the data into training and testing sets and scales the features.
    
    Scaling is critical for distance-based algorithms like KNN and SVM!
    
    Args:
        X: Feature matrix.
        y: Target vector.
        
    Returns:
        Tuple: X_train, X_test, y_train, y_test
    """
    print("[Preprocessing] Splitting dataset into 80% train and 20% test...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("[Preprocessing] Standardizing features (mean=0, std=1)...")
    scaler = StandardScaler()
    
    # Fit on training data ONLY, then transform both
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, y_prob: Optional[np.ndarray] = None) -> Dict[str, float]:
    """
    Computes standard classification evaluation metrics.
    
    Args:
        y_true: Ground truth labels.
        y_pred: Predicted labels.
        y_prob: Predicted probabilities for the positive class (used for ROC-AUC).
        
    Returns:
        Dictionary containing metric names and their corresponding values.
    """
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1-Score": f1_score(y_true, y_pred)
    }
    
    if y_prob is not None:
        metrics["ROC-AUC"] = roc_auc_score(y_true, y_prob)
        
    return metrics


def print_metrics(model_name: str, metrics: Dict[str, float]) -> None:
    """Pretty prints the metrics."""
    print(f"\n[{model_name}] Performance Metrics:")
    for metric_name, value in metrics.items():
        print(f"  -> {metric_name}: {value:.4f}")


# =========================================================================================
# LESSON 1: BASIC CLASSIFIERS (LOGISTIC REGRESSION & KNN)
# =========================================================================================
def basic_classifiers(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> None:
    """
    Demonstrates training, predicting, and evaluating basic classifiers.
    """
    print("\n" + "="*60)
    print("LESSON 1: BASIC CLASSIFIERS (LOGISTIC REGRESSION & KNN)")
    print("="*60)
    
    # 1. Logistic Regression
    print("\n--- 1. Logistic Regression ---")
    print("Training Logistic Regression model...")
    start_time = time.time()
    
    # Initialize model
    lr_model = LogisticRegression(random_state=42, solver='liblinear')
    
    # Train
    lr_model.fit(X_train, y_train)
    
    # Predict
    lr_pred = lr_model.predict(X_test)
    lr_prob = lr_model.predict_proba(X_test)[:, 1] # Probability of positive class (1)
    
    lr_time = time.time() - start_time
    print(f"Logistic Regression trained in {lr_time:.4f} seconds.")
    
    lr_metrics = evaluate_model(y_test, lr_pred, lr_prob)
    print_metrics("Logistic Regression", lr_metrics)
    
    # 2. K-Nearest Neighbors (KNN)
    print("\n--- 2. K-Nearest Neighbors (KNN) ---")
    print("Training KNN (k=5) model...")
    start_time = time.time()
    
    knn_model = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2) # p=2 -> Euclidean distance
    knn_model.fit(X_train, y_train)
    
    knn_pred = knn_model.predict(X_test)
    knn_prob = knn_model.predict_proba(X_test)[:, 1]
    
    knn_time = time.time() - start_time
    print(f"KNN trained and predicted in {knn_time:.4f} seconds.")
    
    knn_metrics = evaluate_model(y_test, knn_pred, knn_prob)
    print_metrics("KNN (k=5)", knn_metrics)


# =========================================================================================
# LESSON 2: ADVANCED NON-LINEAR CLASSIFIERS (SVM & DECISION TREES)
# =========================================================================================
def advanced_classifiers(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> None:
    """
    Demonstrates SVM (with Kernels) and Decision Trees.
    """
    print("\n" + "="*60)
    print("LESSON 2: ADVANCED NON-LINEAR CLASSIFIERS")
    print("="*60)
    
    # 1. Support Vector Machine (SVM)
    print("\n--- 1. Support Vector Machine (SVM) ---")
    print("Training SVM with RBF Kernel (probability=True for AUC estimation)...")
    start_time = time.time()
    
    # C is the regularization parameter. Gamma defines the RBF kernel influence.
    svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', probability=True, random_state=42)
    svm_model.fit(X_train, y_train)
    
    svm_pred = svm_model.predict(X_test)
    svm_prob = svm_model.predict_proba(X_test)[:, 1]
    
    svm_time = time.time() - start_time
    print(f"SVM trained in {svm_time:.4f} seconds.")
    
    svm_metrics = evaluate_model(y_test, svm_pred, svm_prob)
    print_metrics("SVM (RBF Kernel)", svm_metrics)
    
    # 2. Decision Tree
    print("\n--- 2. Decision Tree Classifier ---")
    print("Training Decision Tree (max_depth=5 to prevent severe overfitting)...")
    start_time = time.time()
    
    dt_model = DecisionTreeClassifier(criterion='gini', max_depth=5, random_state=42)
    dt_model.fit(X_train, y_train)
    
    dt_pred = dt_model.predict(X_test)
    dt_prob = dt_model.predict_proba(X_test)[:, 1]
    
    dt_time = time.time() - start_time
    print(f"Decision Tree trained in {dt_time:.4f} seconds.")
    
    dt_metrics = evaluate_model(y_test, dt_pred, dt_prob)
    print_metrics("Decision Tree", dt_metrics)
    
    # Feature Importance (Unique to Tree-based models)
    print("\nDecision Tree Feature Importances (Top 3):")
    importances = dt_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    for i in range(3):
        print(f"  Feature {indices[i]}: {importances[indices[i]]:.4f}")


# =========================================================================================
# LESSON 3: ENSEMBLE LEARNING & HYPERPARAMETER TUNING
# =========================================================================================
def ensemble_and_tuning(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> None:
    """
    Demonstrates Random Forests and GridSearchCV for hyperparameter optimization.
    """
    print("\n" + "="*60)
    print("LESSON 3: ENSEMBLE LEARNING & HYPERPARAMETER TUNING")
    print("="*60)
    
    print("\n--- Random Forest Classifier ---")
    print("Random Forest builds multiple trees and averages them to prevent overfitting.")
    
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_prob = rf_model.predict_proba(X_test)[:, 1]
    
    rf_metrics = evaluate_model(y_test, rf_pred, rf_prob)
    print_metrics("Random Forest (Default)", rf_metrics)
    
    # GridSearchCV for hyperparameter tuning
    print("\n--- Hyperparameter Tuning using GridSearchCV ---")
    print("Grid Search exhaustively tries all combinations of provided hyperparameter values.")
    print("We will tune a simpler model (Decision Tree) for speed demonstration.")
    
    # Define hyperparameter grid
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 3, 5, 7, 10],
        'min_samples_split': [2, 5, 10]
    }
    
    # Setup grid search with 5-fold cross validation
    grid_search = GridSearchCV(
        estimator=DecisionTreeClassifier(random_state=42),
        param_grid=param_grid,
        cv=StratifiedKFold(n_splits=5),
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    print("Running GridSearchCV...")
    start_time = time.time()
    grid_search.fit(X_train, y_train)
    gs_time = time.time() - start_time
    
    print(f"GridSearchCV completed in {gs_time:.4f} seconds.")
    print(f"Best Parameters Found: {grid_search.best_params_}")
    print(f"Best Cross-Validation Accuracy: {grid_search.best_score_:.4f}")
    
    # Evaluate best model on test set
    best_dt = grid_search.best_estimator_
    best_pred = best_dt.predict(X_test)
    best_prob = best_dt.predict_proba(X_test)[:, 1]
    
    best_metrics = evaluate_model(y_test, best_pred, best_prob)
    print_metrics("Tuned Decision Tree", best_metrics)


# =========================================================================================
# INTERVIEW CHALLENGE: IMPLEMENTING KNN FROM SCRATCH
# =========================================================================================
class CustomKNN:
    """
    Common Interview Challenge: Implement the K-Nearest Neighbors classification algorithm 
    from scratch without using Scikit-Learn's estimators.
    """
    def __init__(self, k: int = 3):
        self.k = k
        self.X_train = None
        self.y_train = None
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """Stores the training data. KNN has no real 'training' phase."""
        self.X_train = X
        self.y_train = y
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predicts classes for the given dataset."""
        predictions = [self._predict_single(x) for x in X]
        return np.array(predictions)
        
    def _predict_single(self, x: np.ndarray) -> int:
        """Predicts class for a single instance."""
        # 1. Compute Euclidean distances between x and all points in X_train
        distances = [np.sqrt(np.sum((x_train - x) ** 2)) for x_train in self.X_train]
        
        # 2. Get the indices of the k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        
        # 3. Extract the labels of the k nearest neighbor training samples
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        
        # 4. Return the most common class label (Majority vote)
        # using a simple frequency count via list count or dictionary
        counts = {}
        for label in k_nearest_labels:
            counts[label] = counts.get(label, 0) + 1
            
        most_common_label = max(counts, key=counts.get)
        return most_common_label


def run_interview_challenge(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> None:
    """
    Validates the custom KNN implementation against the test set.
    """
    print("\n" + "="*60)
    print("INTERVIEW CHALLENGE: CUSTOM KNN IMPLEMENTATION")
    print("="*60)
    
    print("Instantiating Custom KNN (k=5)...")
    
    # We will use a smaller subset of the test data for speed since our custom implementation 
    # uses pure python loops and isn't vectorized via numpy operations like sklearn.
    subset_size = 100
    X_test_small = X_test[:subset_size]
    y_test_small = y_test[:subset_size]
    
    custom_knn = CustomKNN(k=5)
    custom_knn.fit(X_train, y_train)
    
    start_time = time.time()
    custom_preds = custom_knn.predict(X_test_small)
    custom_time = time.time() - start_time
    
    accuracy = accuracy_score(y_test_small, custom_preds)
    print(f"Custom KNN achieved Accuracy of {accuracy:.4f} on a {subset_size}-sample test subset.")
    print(f"Prediction time: {custom_time:.4f} seconds.")


# =========================================================================================
# MAIN EXECUTION
# =========================================================================================
def main():
    print(f"========== Exploring SCIKIT-LEARN CLASSIFICATION ==========\n")
    
    # 0. Data Setup
    X, y = generate_dataset(n_samples=2000, n_features=15, random_state=123)
    X_train, X_test, y_train, y_test = preprocess_data(X, y)
    print(f"\nData shapes:")
    print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
    print(f"X_test: {X_test.shape}, y_test: {y_test.shape}")
    
    # 1. Basic Models
    basic_classifiers(X_train, X_test, y_train, y_test)
    
    # 2. Advanced Models
    advanced_classifiers(X_train, X_test, y_train, y_test)
    
    # 3. Ensemble & Tuning
    ensemble_and_tuning(X_train, X_test, y_train, y_test)
    
    # 4. Interview Challenge (Custom Code)
    run_interview_challenge(X_train, X_test, y_train, y_test)
    
    print(f"\n========== END OF SCIKIT-LEARN CLASSIFICATION ==========\n")

if __name__ == "__main__":
    main()
