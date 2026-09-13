"""
# ==============================================================================
# LABORATORY: ENSEMBLE TREE MODELS (RANDOM FORESTS & BOOSTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A single Decision Tree is highly interpretable, but it is mathematically 
# unstable. If you change a single row of training data, the entire Tree 
# architecture can completely flip. A single deep tree is almost guaranteed 
# to Overfit (memorize the data).
#
# To solve this, we use Ensemble Learning (The Wisdom of Crowds).
# 
# 1. BAGGING (Random Forest): Train 1,000 deep, overfitted Decision Trees in 
#    parallel. But trick each tree by giving it a slightly different, random 
#    subset of the data and a random subset of the columns. Then, average their 
#    answers. The Overfitting magically cancels out!
#
# 2. BOOSTING (Gradient Boosting): Train 1,000 shallow, weak Decision Trees 
#    sequentially. Tree #1 makes predictions. It will make mistakes. Tree #2 
#    is explicitly trained ONLY on the errors of Tree #1. Tree #3 fixes the 
#    errors of Tree #2. By the end, the ensemble is incredibly powerful.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a single Decision Tree.
# - Execute a Random Forest (Bagging) and extract Feature Importances.
# - Execute Gradient Boosting (Boosting) for state-of-the-art accuracy.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.metrics import accuracy_score
    import matplotlib.pyplot as plt
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE DECISION TREE (THE BASE ESTIMATOR)
# ==============================================================================
def demonstrate_single_tree():
    section_header("The Single Decision Tree")
    
    if not HAS_SKLEARN:
        print("[WARNING] Scikit-Learn not installed.")
        return
        
    print("A single tree splits the data using Boolean logic (if/else).")
    
    X, y = make_classification(n_samples=500, n_features=5, n_informative=3, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # max_depth=3 ensures we don't overfit to infinity.
    tree = DecisionTreeClassifier(max_depth=3, random_state=42)
    tree.fit(X_train, y_train)
    
    preds = tree.predict(X_test)
    print(f"Single Tree Accuracy: {accuracy_score(y_test, preds)*100:.1f}%\n")
    
    # We can physically visualize the Boolean logic of the tree!
    print("In a Jupyter notebook, you could run:")
    print("  plt.figure(figsize=(12, 8))")
    print("  plot_tree(tree, filled=True)")
    print("  plt.show()")


# ==============================================================================
# 4. RANDOM FORESTS (BAGGING)
# ==============================================================================
def demonstrate_random_forest():
    section_header("Random Forests (Bagging/Bootstrap Aggregating)")
    
    if not HAS_SKLEARN: return
    
    print("A Random Forest builds 100 Trees in parallel.")
    print("Each tree gets a bootstrapped random sample of rows, and a random ")
    print("subset of features at every split. This guarantees the trees are ")
    print("'Decorrelated' (they all look at the problem from different angles).\n")
    
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # n_estimators = 100 Trees
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    
    preds = rf.predict(X_test)
    print(f"Random Forest Accuracy: {accuracy_score(y_test, preds)*100:.1f}%\n")
    
    # Feature Importance
    # Because it builds 100 trees, it can mathematically prove which features 
    # were the most universally useful across the entire forest!
    importances = rf.feature_importances_
    
    print("Feature Importances:")
    for i, imp in enumerate(importances):
        if imp > 0.1: # Only print highly important features
            print(f"Feature {i:2d}: {imp*100:5.1f}% importance")


# ==============================================================================
# 5. GRADIENT BOOSTING (SEQUENTIAL ERROR CORRECTION)
# ==============================================================================
def demonstrate_gradient_boosting():
    section_header("Gradient Boosting (Sequential Correction)")
    
    if not HAS_SKLEARN: return
    
    print("Unlike a Random Forest (Parallel), Gradient Boosting is Sequential.")
    print("Tree 1 trains. Tree 2 calculates the exact 'Residual Errors' of ")
    print("Tree 1, and trains specifically to predict those errors.")
    print("This requires a learning rate (shrinkage) to prevent it from ")
    print("correcting too fast and immediately overfitting.\n")
    
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # n_estimators=100, learning_rate=0.1
    # Unlike RF, Boosting uses VERY shallow trees (max_depth=3)
    gbc = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    gbc.fit(X_train, y_train)
    
    preds = gbc.predict(X_test)
    print(f"Gradient Boosting Accuracy: {accuracy_score(y_test, preds)*100:.1f}%\n")
    print("Note: In Kaggle competitions, advanced Boosting variants like XGBoost ")
    print("and LightGBM are the undisputed champions for tabular data!")


def run_all_labs():
    demonstrate_single_tree()
    demonstrate_random_forest()
    demonstrate_gradient_boosting()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between Bagging (Random Forest) and Boosting (Gradient Boosting)?
   Answer: 
   - **Bagging (Parallel):** Random Forest builds 1,000 deep, overfitted trees independently and simultaneously. By averaging their answers (Wisdom of the Crowds), the variance and overfitting mathematically cancel out.
   - **Boosting (Sequential):** Gradient Boosting builds 1,000 shallow, weak trees one by one. Tree #2 specifically studies the mistakes of Tree #1 and tries to fix them. Tree #3 fixes the mistakes of Tree #2. It slowly builds a highly accurate model by mathematically minimizing the residual error through gradient descent.

2. Why does a Random Forest purposefully restrict each Tree to only see a random subset of Features (e.g. only 3 out of 10 columns)?
   Answer: To force "Decorrelation". If you have a dataset where "Salary" is an overwhelmingly powerful predictor, every single one of your 1,000 trees will automatically split on Salary at the very top. You would end up with 1,000 identical trees! By physically hiding the Salary column from 70% of the trees, you force those trees to explore other, weaker features (like Age or Location). This creates true diversity in the ensemble, making the final vote much stronger and robust to missing data.

3. Why do Tree-Based models not require Feature Scaling (Standardization)?
   Answer: Tree-based models (Decision Trees, Random Forest, XGBoost) do not calculate Euclidean distance or gradients based on geometry! They simply calculate Information Gain (Gini Impurity / Entropy) by creating Boolean thresholds (`if Age > 45:`). An `if/else` logical split operates exactly the same way whether the data ranges from $0$ to $100$ or from $0$ to $1,000,000$. The absolute scale of the number is mathematically irrelevant to the Information Theory splitting algorithm.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Ensemble Tree Models Completed.")
