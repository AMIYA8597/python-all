"""
# ==============================================================================
# LABORATORY: MODEL EVALUATION & TUNING (SCIKIT-LEARN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You trained a Machine Learning model. It achieved 99% Accuracy on the Test Set!
# Are you ready to deploy it to production? ABSOLUTELY NOT.
#
# Consider a dataset of 10,000 credit card transactions. Only 10 are Fraudulent (0.1%).
# If your model is a piece of hardcoded garbage that simply predicts "Not Fraud" 
# for every single transaction, it will achieve 99.9% Accuracy! But it entirely 
# failed its purpose. Accuracy is a deeply flawed metric for imbalanced data.
#
# Furthermore, how do you know your model is using the best possible parameters 
# (e.g., K=5 vs K=10 in KNN, or Max_Depth=10 vs 20 in Random Forest)? 
#
# You must use Advanced Evaluation Metrics (Precision, Recall, Confusion Matrix) 
# and rigorous K-Fold Cross-Validation to mathematically guarantee the safety 
# and optimization of your model before deployment.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Confusion Matrix (True Positives vs False Negatives).
# - Calculate Precision, Recall, and the F1-Score.
# - Execute K-Fold Cross Validation.
# - Execute GridSearchCV to mathematically brute-force the best Hyperparameters.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd

# In a real environment: pip install scikit-learn
try:
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.metrics import confusion_matrix, classification_report, f1_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CONFUSION MATRIX (PRECISION VS RECALL)
# ==============================================================================
def demonstrate_confusion_matrix():
    section_header("The Confusion Matrix & F1-Score")
    
    if not HAS_SKLEARN: return
    
    print("Scenario: Predicting Cancer (1 = Cancer, 0 = Healthy).")
    print("If a model says you don't have cancer, but you actually do, that is ")
    print("a False Negative. In medicine, a False Negative is fatal!")
    
    # Generate an highly Imbalanced Dataset (95% Healthy, 5% Cancer)
    X, y = make_classification(n_samples=1000, weights=[0.95, 0.05], random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    
    # 1. CONFUSION MATRIX
    # [True Negatives,  False Positives]
    # [False Negatives, True Positives ]
    cm = confusion_matrix(y_test, preds)
    
    print("\nConfusion Matrix:")
    print(f"[{cm[0][0]:3d} (True Neg)  |  {cm[0][1]:3d} (False Pos)]")
    print(f"[{cm[1][0]:3d} (False Neg) |  {cm[1][1]:3d} (True Pos) ]")
    
    print("\nAnalysis:")
    print(f"The model successfully found {cm[1][1]} Cancer patients.")
    print(f"However, it missed {cm[1][0]} Cancer patients (Fatal False Negatives!).")
    
    # 2. CLASSIFICATION REPORT (Precision & Recall)
    # Precision: When the model predicts Cancer, how often is it actually Cancer?
    # Recall: Out of ALL the real Cancer patients, how many did the model find?
    # F1-Score: The harmonic mean of Precision and Recall.
    print("\nClassification Report:")
    print(classification_report(y_test, preds))


# ==============================================================================
# 4. K-FOLD CROSS-VALIDATION
# ==============================================================================
def demonstrate_cross_validation():
    section_header("K-Fold Cross-Validation")
    
    if not HAS_SKLEARN: return
    
    print("A single Train/Test split relies on luck. What if the Test set ")
    print("randomly happens to contain all the easy questions?")
    print("K-Fold splits the data into 5 chunks. It trains on 4 chunks, tests on 1.")
    print("It repeats this 5 times, rotating the Test chunk until EVERY row ")
    print("has been used for testing exactly once! This guarantees true stability.\n")
    
    X, y = make_classification(n_samples=1000, random_state=42)
    
    clf = RandomForestClassifier(random_state=42)
    
    # Execute 5-Fold Cross Validation
    # Notice we pass the ENTIRE dataset (X, y) to cross_val_score! 
    # It handles the splitting automatically!
    cv_scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    
    print("Cross Validation Results (5 Folds):")
    for i, score in enumerate(cv_scores):
        print(f"Fold {i+1}: {score*100:.1f}%")
        
    print(f"\nFinal Verified Mean Accuracy: {cv_scores.mean()*100:.1f}% (+/- {cv_scores.std()*100:.1f}%)")


# ==============================================================================
# 5. HYPERPARAMETER TUNING (GRID SEARCH)
# ==============================================================================
def demonstrate_grid_search():
    section_header("GridSearchCV (Hyperparameter Optimization)")
    
    if not HAS_SKLEARN: return
    
    print("How do we know if SVM is better with an RBF kernel or a Linear kernel?")
    print("How do we know what 'C' value is best?")
    print("We use Grid Search to literally brute-force every mathematical combination!\n")
    
    X, y = make_classification(n_samples=500, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. DEFINE THE GRID (The parameters to test)
    # C: Regularization parameter
    # kernel: The mathematical projection method
    param_grid = {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf']
    }
    
    print(f"Testing {len(param_grid['C']) * len(param_grid['kernel'])} combinations...")
    
    # 2. INSTANTIATE THE GRID SEARCH
    # We pass the Base Model, the Grid, and tell it to use 3-Fold CV for EVERY combination!
    # (3 * 2 * 3-folds = 18 total model trainings!)
    svm = SVC(random_state=42)
    grid_search = GridSearchCV(estimator=svm, param_grid=param_grid, cv=3, n_jobs=-1, verbose=1)
    
    # 3. EXECUTE THE BRUTE-FORCE
    grid_search.fit(X_train, y_train)
    
    # 4. EXTRACT THE WINNER!
    print("\nGrid Search Complete!")
    print(f"Best Hyperparameters Found: {grid_search.best_params_}")
    print(f"Best Validation Accuracy  : {grid_search.best_score_*100:.1f}%")
    
    # The grid_search object automatically retrains the final model using the BEST 
    # parameters on the entire training set. We can predict immediately!
    best_model = grid_search.best_estimator_
    final_acc = accuracy_score(y_test, best_model.predict(X_test))
    
    print(f"Final Accuracy on Hidden Test Set: {final_acc*100:.1f}%")


def run_all_labs():
    demonstrate_confusion_matrix()
    demonstrate_cross_validation()
    demonstrate_grid_search()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Accuracy a useless metric for Fraud Detection (or any highly imbalanced dataset)?
   Answer: In a dataset where 99.9% of transactions are legitimate and 0.1% are fraud, a "dumb" model that blindly outputs "Legitimate" for every single row will mathematically achieve 99.9% Accuracy. However, the model is completely useless because it failed to catch a single instance of fraud (Recall = 0%). For imbalanced datasets, you MUST use the Confusion Matrix to calculate the F1-Score, which balances Precision (avoiding false alarms) and Recall (catching all the actual fraud).

2. What is the fundamental difference between Precision and Recall?
   Answer: Precision asks: "Out of all the people I *predicted* to have cancer, how many *actually* have it?" (High precision minimizes False Positives). Recall asks: "Out of all the people who *actually* have cancer in the real world, how many did I successfully find?" (High recall minimizes False Negatives). In medicine, Recall is usually prioritized because a False Negative (sending a sick patient home) is fatal, whereas a False Positive just requires a secondary follow-up test. 

3. Why is Cross-Validation superior to a single Train/Test split?
   Answer: A single 80/20 Train/Test split is subject to random variance. You might accidentally get "lucky" and have all the easy-to-predict rows fall into your Test set, resulting in an artificially high 99% accuracy that crashes to 80% in production. K-Fold Cross-Validation splits the data into 5 (or 10) chunks. It trains and tests the model 5 separate times, rotating the chunks so that every single row is used as a Test row exactly once. The final score is the average of all 5 tests, providing a mathematically robust, variance-resistant guarantee of how the model will perform in the real world.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Model Evaluation & Tuning Completed.")
