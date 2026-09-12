"""
Module: 01-sklearn-trees
Description: A textbook-grade, comprehensive interactive lesson on Decision Trees using scikit-learn.

=========================================================================================
                        MASTERING DECISION TREES IN SCIKIT-LEARN
=========================================================================================

Learning Objectives:
1. Understand the core mathematical concepts behind Decision Trees:
   - Gini Impurity
   - Entropy and Information Gain
   - Mean Squared Error (for regression)
2. Master the usage of `DecisionTreeClassifier` and `DecisionTreeRegressor` in scikit-learn.
3. Learn advanced hyperparameter tuning and regularization techniques to prevent overfitting.
4. Visualize decision trees and interpret feature importance.
5. Apply Cost Complexity Pruning (Minimal Cost-Complexity Pruning).
6. Understand Time and Space Complexity (Big-O analysis).
7. Solve a real-world predictive modeling problem.

-----------------------------------------------------------------------------------------
MATHEMATICAL BACKGROUND
-----------------------------------------------------------------------------------------
A Decision Tree builds classification or regression models in the form of a tree structure.
It breaks down a dataset into smaller and smaller subsets while at the same time an 
associated decision tree is incrementally developed. The final result is a tree with 
decision nodes and leaf nodes.

1. Classification Criteria:
   a) Gini Impurity (default in sklearn):
      A measure of how often a randomly chosen element from the set would be incorrectly 
      labeled if it was randomly labeled according to the distribution of labels in the subset.
      Gini = 1 - sum(p_i^2) for i in classes
      Where p_i is the probability of an item belonging to class i.

   b) Entropy (Information Gain):
      A measure of the amount of uncertainty in the dataset.
      Entropy = - sum(p_i * log2(p_i))
      Information Gain = Entropy(Parent) - [Weighted Average] * Entropy(Children)
      The tree splits on the feature that maximizes Information Gain.

2. Regression Criteria:
   a) Mean Squared Error (MSE):
      Splits the data to minimize the variance of the target values in the children.
      MSE = 1/N * sum((y_i - y_hat)^2)

-----------------------------------------------------------------------------------------
BIG-O COMPLEXITY ANALYSIS
-----------------------------------------------------------------------------------------
Let 'n' be the number of samples, and 'm' be the number of features.

1. Time Complexity:
   - Training (Building the tree): 
     Finding the best split at each node requires evaluating all features and all possible 
     split points. For a balanced tree, the depth is O(log n).
     Training Time: O(n * m * log(n))
   - Prediction (Inference):
     Traversing the tree from root to a leaf node.
     Inference Time: O(log(n))

2. Space Complexity:
   - The tree structure itself stores the split conditions at each internal node and 
     the predictions at the leaves.
     Space: O(n) in the worst case (fully unpruned tree with 1 sample per leaf), but 
     usually much less O(2^d) where d is the max depth.

-----------------------------------------------------------------------------------------
MODERN TYPE HINTS & EXHAUSTIVE INLINE COMMENTS
-----------------------------------------------------------------------------------------
This lesson utilizes modern Python type hinting to explicitly define input and output 
types for all functions, ensuring code clarity and robustness.
"""

import sys
import time
import math
import random
import warnings
from typing import List, Dict, Any, Tuple, Optional

# Third-party imports for data manipulation and machine learning
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.datasets import make_classification, make_regression, load_breast_cancer
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text, plot_tree
    from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
except ImportError as e:
    print(f"Required library missing: {e}")
    print("Please install required packages using: pip install numpy pandas scikit-learn matplotlib")
    sys.exit(1)

# Suppress minor warnings for cleaner output in educational contexts
warnings.filterwarnings('ignore')


def concept_gini_impurity(class_probabilities: List[float]) -> float:
    """
    Calculates the Gini Impurity for a given set of class probabilities.
    
    Args:
        class_probabilities (List[float]): A list of probabilities for each class.
                                           Should sum to 1.0.
    
    Returns:
        float: The calculated Gini Impurity.
    """
    gini = 1.0 - sum(p ** 2 for p in class_probabilities)
    return gini


def concept_entropy(class_probabilities: List[float]) -> float:
    """
    Calculates the Entropy for a given set of class probabilities.
    
    Args:
        class_probabilities (List[float]): A list of probabilities for each class.
                                           Should sum to 1.0.
    
    Returns:
        float: The calculated Entropy.
    """
    entropy = 0.0
    for p in class_probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def demonstrate_math_concepts() -> None:
    """
    Demonstrates the mathematical foundations of Decision Trees.
    """
    print("=" * 60)
    print("1. MATHEMATICAL FOUNDATIONS: GINI IMPURITY VS ENTROPY")
    print("=" * 60)
    
    # Example 1: Pure Node (All samples belong to one class)
    pure_probs = [1.0, 0.0]
    print(f"Pure Node Probabilities: {pure_probs}")
    print(f"  Gini Impurity: {concept_gini_impurity(pure_probs):.4f}")
    print(f"  Entropy:       {concept_entropy(pure_probs):.4f}\n")
    
    # Example 2: Maximum Impurity (Equal distribution among classes)
    mixed_probs = [0.5, 0.5]
    print(f"Maximum Impurity Probabilities (2 classes): {mixed_probs}")
    print(f"  Gini Impurity: {concept_gini_impurity(mixed_probs):.4f}")
    print(f"  Entropy:       {concept_entropy(mixed_probs):.4f}\n")
    
    # Example 3: Three Classes
    three_classes = [0.2, 0.3, 0.5]
    print(f"Three Classes Probabilities: {three_classes}")
    print(f"  Gini Impurity: {concept_gini_impurity(three_classes):.4f}")
    print(f"  Entropy:       {concept_entropy(three_classes):.4f}\n")


def build_and_evaluate_classifier(
    X_train: np.ndarray, 
    X_test: np.ndarray, 
    y_train: np.ndarray, 
    y_test: np.ndarray,
    criterion: str = 'gini',
    max_depth: Optional[int] = None
) -> DecisionTreeClassifier:
    """
    Builds, trains, and evaluates a Decision Tree Classifier.
    
    Args:
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Testing features.
        y_train (np.ndarray): Training labels.
        y_test (np.ndarray): Testing labels.
        criterion (str): The function to measure the quality of a split ('gini' or 'entropy').
        max_depth (Optional[int]): The maximum depth of the tree. If None, nodes are expanded 
                                   until all leaves are pure.
    
    Returns:
        DecisionTreeClassifier: The trained classifier model.
    """
    # 1. Initialize the classifier
    clf = DecisionTreeClassifier(
        criterion=criterion,
        max_depth=max_depth,
        random_state=42 # Set for reproducibility
    )
    
    # 2. Train the model
    start_time = time.time()
    clf.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    # 3. Make predictions
    y_pred = clf.predict(X_test)
    
    # 4. Evaluate performance
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Configuration : Criterion='{criterion}', Max Depth={max_depth}")
    print(f"Training Time       : {training_time:.6f} seconds (Big-O: O(n * m * log(n)))")
    print(f"Tree Depth Achieved : {clf.get_depth()}")
    print(f"Number of Leaves    : {clf.get_n_leaves()}")
    print(f"Accuracy Score      : {accuracy * 100:.2f}%\n")
    
    return clf


def basic_classification_tutorial() -> None:
    """
    Tutorial on building a basic Decision Tree Classifier using a synthetic dataset.
    """
    print("=" * 60)
    print("2. BASIC CLASSIFICATION WITH SYNTHETIC DATA")
    print("=" * 60)
    
    # Create a synthetic binary classification dataset
    # n_samples=1000 (Big-O analysis scaling point)
    # n_features=10 (Dimensions)
    X, y = make_classification(
        n_samples=1000, 
        n_features=10, 
        n_informative=5, 
        n_redundant=2, 
        random_state=42
    )
    
    # Split the dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("Training a fully grown tree (tends to overfit):")
    clf_unconstrained = build_and_evaluate_classifier(
        X_train, X_test, y_train, y_test, criterion='gini', max_depth=None
    )
    
    print("Training a constrained tree (prevents overfitting):")
    clf_constrained = build_and_evaluate_classifier(
        X_train, X_test, y_train, y_test, criterion='entropy', max_depth=4
    )


def regression_tutorial() -> None:
    """
    Tutorial on building a Decision Tree Regressor.
    Instead of predicting classes, regression trees predict continuous continuous values.
    """
    print("=" * 60)
    print("3. DECISION TREE REGRESSION")
    print("=" * 60)
    
    # Generate a nonlinear regression dataset
    # y = sin(x) + noise
    rng = np.random.RandomState(1)
    X = np.sort(5 * rng.rand(80, 1), axis=0)
    y = np.sin(X).ravel()
    y[::5] += 3 * (0.5 - rng.rand(16)) # Add noise to targets
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train two regressors with different depths
    regr_1 = DecisionTreeRegressor(max_depth=2, random_state=42)
    regr_2 = DecisionTreeRegressor(max_depth=5, random_state=42)
    
    regr_1.fit(X_train, y_train)
    regr_2.fit(X_train, y_train)
    
    # Predictions
    y_pred_1 = regr_1.predict(X_test)
    y_pred_2 = regr_2.predict(X_test)
    
    # Evaluate
    mse_1 = mean_squared_error(y_test, y_pred_1)
    mse_2 = mean_squared_error(y_test, y_pred_2)
    
    print("Regression Tree 1 (max_depth=2):")
    print(f"  MSE: {mse_1:.4f}")
    print("Regression Tree 2 (max_depth=5):")
    print(f"  MSE: {mse_2:.4f}")
    print("\nNote: A very deep regression tree will tightly fit the noise (overfitting).")
    print("      This is why hyperparameter tuning is critical.\n")


def hyperparameter_tuning_and_pruning() -> None:
    """
    Demonstrates hyperparameter tuning using GridSearchCV and 
    Cost Complexity Pruning to find the optimal tree architecture.
    """
    print("=" * 60)
    print("4. HYPERPARAMETER TUNING & COST COMPLEXITY PRUNING")
    print("=" * 60)
    
    # Load a real-world dataset: Breast Cancer Wisconsin
    data = load_breast_cancer()
    X, y = data.data, data.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )
    
    # --- Approach A: Grid Search CV ---
    print("--- Approach A: GridSearchCV ---")
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [3, 5, 7, 10, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    dt = DecisionTreeClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=dt, param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')
    
    print("Performing Grid Search (this explores multiple combinations of hyperparameters)...")
    grid_search.fit(X_train, y_train)
    
    best_dt = grid_search.best_estimator_
    print(f"Best Parameters: {grid_search.best_params_}")
    
    y_pred = best_dt.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy with Best Estimator: {acc * 100:.2f}%\n")
    
    # --- Approach B: Cost Complexity Pruning (ccp_alpha) ---
    print("--- Approach B: Cost Complexity Pruning ---")
    print("Pruning removes parts of the tree that do not provide power to classify instances.")
    
    clf = DecisionTreeClassifier(random_state=42)
    # Determine alphas for the pruning path
    path = clf.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities
    
    print(f"Found {len(ccp_alphas)} candidate alpha values for pruning.")
    
    clfs = []
    for alpha in ccp_alphas:
        clf_pruned = DecisionTreeClassifier(random_state=42, ccp_alpha=alpha)
        clf_pruned.fit(X_train, y_train)
        clfs.append(clf_pruned)
        
    # Remove the trivial tree (only one node)
    clfs = clfs[:-1]
    ccp_alphas = ccp_alphas[:-1]
    
    train_scores = [c.score(X_train, y_train) for c in clfs]
    test_scores = [c.score(X_test, y_test) for c in clfs]
    
    best_idx = np.argmax(test_scores)
    best_alpha = ccp_alphas[best_idx]
    best_test_score = test_scores[best_idx]
    
    print(f"Optimal ccp_alpha: {best_alpha:.5f}")
    print(f"Optimal Test Score after Pruning: {best_test_score * 100:.2f}%\n")
    

def interpretability_and_visualization() -> None:
    """
    Shows how to interpret a trained decision tree by looking at feature importances
    and exporting the tree as text.
    """
    print("=" * 60)
    print("5. INTERPRETABILITY AND FEATURE IMPORTANCE")
    print("=" * 60)
    
    data = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )
    
    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(X_train, y_train)
    
    # 1. Feature Importances
    # Calculated as the normalized total reduction of the criterion brought by that feature.
    print("--- Top 5 Most Important Features ---")
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    for i in range(5):
        feature_idx = indices[i]
        feature_name = data.feature_names[feature_idx]
        print(f"{i+1}. {feature_name}: {importances[feature_idx]:.4f}")
    print()
    
    # 2. Text Representation
    print("--- Text Representation of the Tree ---")
    tree_rules = export_text(clf, feature_names=list(data.feature_names))
    # Print only the first few lines to avoid spamming the console
    print("\n".join(tree_rules.split("\n")[:10]))
    print("... (truncated for brevity) ...\n")


def real_world_application() -> None:
    """
    Simulates a real-world application: Customer Churn Prediction.
    This demonstrates end-to-end data processing, modeling, and evaluation.
    """
    print("=" * 60)
    print("6. REAL-WORLD APPLICATION: CUSTOMER CHURN PREDICTION")
    print("=" * 60)
    
    # Creating a mock dataset representing customer metrics
    print("Generating synthetic customer data (Age, Tenure, Balance, NumProducts, IsActive)...")
    np.random.seed(42)
    n_customers = 5000
    
    # Features
    age = np.random.normal(40, 10, n_customers)
    tenure = np.random.randint(0, 10, n_customers)
    balance = np.random.normal(50000, 20000, n_customers)
    num_products = np.random.randint(1, 4, n_customers)
    is_active = np.random.randint(0, 2, n_customers)
    
    X = np.column_stack((age, tenure, balance, num_products, is_active))
    
    # Target: Churn (1 = Yes, 0 = No)
    # Let's invent a rule: Old age + low activity + high balance = higher churn probability
    churn_prob = (age / 100) * 0.3 + (1 - is_active) * 0.4 + (balance / 100000) * 0.2
    y = (churn_prob > np.percentile(churn_prob, 75)).astype(int) # Top 25% churn
    
    print(f"Dataset Size: {n_customers} samples. Classes: {np.bincount(y)}")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Model Training with class weights to handle mild imbalance
    clf = DecisionTreeClassifier(
        max_depth=5, 
        class_weight='balanced', 
        random_state=42
    )
    clf.fit(X_train, y_train)
    
    # Evaluation
    y_pred = clf.predict(X_test)
    print("\nClassification Report (Precision, Recall, F1-Score):")
    print(classification_report(y_test, y_pred, target_names=["Stayed", "Churned"]))
    
    feature_names = ["Age", "Tenure", "Balance", "NumProducts", "IsActive"]
    importances = clf.feature_importances_
    most_important_idx = np.argmax(importances)
    print(f"Insight: The most critical factor for predicting churn is '{feature_names[most_important_idx]}'.\n")


def interview_challenge() -> None:
    """
    Solves a common interview challenge regarding Decision Trees.
    Challenge: How do you implement a function to calculate the Information Gain of a split?
    """
    print("=" * 60)
    print("7. INTERVIEW CHALLENGE: CALCULATING INFORMATION GAIN")
    print("=" * 60)
    
    def calculate_information_gain(
        parent_counts: List[int], 
        left_counts: List[int], 
        right_counts: List[int]
    ) -> float:
        """
        Calculates Information Gain of a binary split based on class counts.
        """
        def get_entropy(counts: List[int]) -> float:
            total = sum(counts)
            if total == 0: return 0.0
            probs = [c / total for c in counts]
            return concept_entropy(probs)
            
        parent_total = sum(parent_counts)
        left_total = sum(left_counts)
        right_total = sum(right_counts)
        
        parent_entropy = get_entropy(parent_counts)
        left_entropy = get_entropy(left_counts)
        right_entropy = get_entropy(right_counts)
        
        # Weighted average of children's entropy
        weighted_child_entropy = (left_total / parent_total) * left_entropy + \
                                 (right_total / parent_total) * right_entropy
                                 
        return parent_entropy - weighted_child_entropy

    # Test the interview challenge function
    parent = [30, 30] # 30 positive, 30 negative
    left_child = [25, 5]
    right_child = [5, 25]
    
    ig = calculate_information_gain(parent, left_child, right_child)
    print(f"Parent Node: {parent} (Entropy: {concept_entropy([0.5, 0.5]):.4f})")
    print(f"Left Child : {left_child}")
    print(f"Right Child: {right_child}")
    print(f"Information Gain achieved by this split: {ig:.4f}\n")


def run_tests() -> None:
    """
    A robust test suite validating mathematical foundations and core logic.
    """
    print("=" * 60)
    print("8. RUNNING UNIT TESTS")
    print("=" * 60)
    
    try:
        # 1. Test Gini Impurity
        # Pure node gini should be 0
        assert math.isclose(concept_gini_impurity([1.0, 0.0]), 0.0), "Gini pure node failed"
        # 50/50 split should be 0.5
        assert math.isclose(concept_gini_impurity([0.5, 0.5]), 0.5), "Gini 50/50 failed"
        
        # 2. Test Entropy
        # Pure node entropy should be 0
        assert math.isclose(concept_entropy([1.0, 0.0]), 0.0), "Entropy pure node failed"
        # 50/50 split entropy should be 1.0
        assert math.isclose(concept_entropy([0.5, 0.5]), 1.0), "Entropy 50/50 failed"
        
        print("All mathematical foundations tests passed successfully! ✅")
        
    except AssertionError as e:
        print(f"Test Suite Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("\n" + "#" * 70)
    print("     PYTHON DSA & AI MASTER: SCIKIT-LEARN DECISION TREES")
    print("#" * 70 + "\n")
    
    # 1. Mathematical Concepts
    demonstrate_math_concepts()
    
    # 2. Basic Usage (Classification)
    basic_classification_tutorial()
    
    # 3. Regression Trees
    regression_tutorial()
    
    # 4. Hyperparameter Tuning & Pruning
    hyperparameter_tuning_and_pruning()
    
    # 5. Interpretability
    interpretability_and_visualization()
    
    # 6. Real World Application
    real_world_application()
    
    # 7. Interview Challenge
    interview_challenge()
    
    # 8. Testing Suite
    run_tests()
    
    print("\n" + "#" * 70)
    print("               LESSON COMPLETED SUCCESSFULLY")
    print("#" * 70 + "\n")
