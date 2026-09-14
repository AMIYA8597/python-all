"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (SCIENTIFIC MACHINE LEARNING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A biologist has a CSV file of 1,000 tumor samples with 30 different geometric 
# measurements (radius, texture, perimeter, area). They need to predict if a 
# new sample is Benign (safe) or Malignant (cancer). A junior developer tries 
# to write a Python script with 30 nested `if/else` statements: 
# `if radius > 15 and area < 800 and texture > 20...`. It is mathematically 
# impossible for a human to calculate the correct threshold combinations for 
# 30 dimensions. The script achieves 52% accuracy.
#
# A senior Data Scientist uses `scikit-learn`. They structure the 30 measurements 
# into a 1000x30 NumPy Feature Matrix (X) and the answers into a Target Vector (y). 
# They deploy a Support Vector Machine (SVM) algorithm. In 0.1 seconds, the 
# algorithm mathematically projects the 30-dimensional data into higher-dimensional 
# space, calculates the absolute perfect "Hyperplane" to divide the two classes, 
# and achieves 97.6% accuracy, saving human lives.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical architecture of the Feature Matrix (X) and Target (y).
# - Execute a Classification Algorithm (Support Vector Machine / Random Forest).
# - Execute algorithmic cross-validation and evaluation metrics.
#
# ==============================================================================
"""

import math

# Gracefully handle missing scikit-learn dependency
try:
    import numpy as np
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score, classification_report
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MACHINE LEARNING PIPELINE (CLASSIFICATION)
# ==============================================================================
def demonstrate_ml_pipeline():
    section_header("Scientific ML Pipeline (scikit-learn)")
    
    if not HAS_SKLEARN:
        print("  [ERROR] scikit-learn is not installed. Run `pip install scikit-learn numpy`.")
        return
        
    print("  [SCENARIO] Classifying Breast Cancer Tumors (Benign vs Malignant).")
    
    # --- 1. DATA INGESTION ---
    print("\n  [PHASE 1: THE MATHEMATICAL MATRICES]")
    # We load a famous scientific dataset directly from sklearn!
    dataset = datasets.load_breast_cancer()
    
    # X = The Feature Matrix (The 30 geometric measurements of the tumors)
    # y = The Target Vector (The answers! 0 = Malignant, 1 = Benign)
    X = dataset.data
    y = dataset.target
    
    print(f"    -> Feature Matrix (X) Shape: {X.shape} (569 tumors, 30 measurements each)")
    print(f"    -> Target Vector (y) Shape:  {y.shape} (569 labels)")


    # --- 2. DATA SPLITTING (TRAIN VS TEST) ---
    print("\n  [PHASE 2: ALGORITHMIC ISOLATION]")
    # If we train the algorithm on all 569 tumors, it will just memorize the answers!
    # We must mathematically hide 20% of the data in a "Test Set" to prove it 
    # actually learned the underlying geometry, not just rote memorization.
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42 # random_state ensures deterministic reproducibility!
    )
    
    print(f"    -> Training Matrix: {X_train.shape[0]} tumors.")
    print(f"    -> Testing Matrix:  {X_test.shape[0]} tumors (Hidden from the algorithm).")


    # --- 3. DATA SCALING (NORMALIZATION) ---
    print("\n  [PHASE 3: MATHEMATICAL NORMALIZATION]")
    # 'Area' might be mathematically huge (1000.0), while 'Smoothness' is tiny (0.05).
    # If we don't scale the data, the algorithm will mathematically assume 'Area'
    # is 20,000x more important just because the raw numbers are bigger!
    
    scaler = StandardScaler()
    # It calculates the Mean and Standard Deviation of the Training set, 
    # and forces all 30 columns to have a Mean of 0 and Variance of 1.
    X_train_scaled = scaler.fit_transform(X_train)
    # We MUST scale the Test set using the EXACT SAME math as the Training set!
    X_test_scaled = scaler.transform(X_test)
    
    print("    -> Feature Matrix Normalized via Z-Score calculation.")


    # --- 4. ALGORITHMIC TRAINING (THE FIT) ---
    print("\n  [PHASE 4: TRAINING THE SUPPORT VECTOR MACHINE (SVM)]")
    # We deploy an SVM with a Radial Basis Function (RBF) kernel!
    # It mathematically warps the 30-D space until it finds a flat plane 
    # that perfectly cuts the Malignant tumors away from the Benign tumors.
    
    model = SVC(kernel='rbf', C=1.0, random_state=42)
    
    print("    -> Initiating Gradient Descent...")
    model.fit(X_train_scaled, y_train) # This is where the Heavy Math happens!
    print("    -> Training Complete! The mathematical Hyperplane has been established.")


    # --- 5. ALGORITHMIC PREDICTION & EVALUATION ---
    print("\n  [PHASE 5: THE INFERENCE ENGINE]")
    # We feed the 114 hidden Test tumors into the trained model.
    # We ask it to mathematically guess if they are cancer or not.
    predictions = model.predict(X_test_scaled)
    
    # We calculate the mathematical Accuracy!
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"    -> The Algorithm achieved a mathematical accuracy of: {accuracy * 100:.2f}%")
    print("\n  [DETAILED MATHEMATICAL REPORT]")
    # Classification Report calculates Precision, Recall, and F1-Score!
    report = classification_report(y_test, predictions, target_names=dataset.target_names)
    print(report)


def run_all_labs():
    demonstrate_ml_pipeline()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is it mathematically mandatory to execute `train_test_split()` before training a Machine Learning model?"
   Senior Answer: "To prevent 'Overfitting'. If you feed $100\\%$ of your data into the algorithm during training, a complex algorithm (like a Deep Neural Network) will mathematically memorize the exact numeric values of every single row, rather than learning the generalized underlying geometric patterns. When you deploy it to Production and give it a brand new, unseen patient, it will catastrophically fail because it has never seen those exact numbers before. By mathematically hiding $20\\%$ of the data in a Test Set, you force the algorithm to train on the $80\\%$, and then you 'test' it on the $20\\%$. If it achieves $98\\%$ accuracy on the hidden $20\\%$, you have mathematical proof that the algorithm successfully generalized the geometry."

2. Interviewer: "Why did we use `StandardScaler.fit_transform()` on the Training set, but only `transform()` on the Test set? Why not `fit_transform()` the Test set too?"
   Senior Answer: "Data Leakage. The `fit()` function mathematically scans the matrix and calculates the Mean ($\mu$) and Standard Deviation ($\sigma$) of the columns. If you `fit()` the Test set, you are mathematically allowing the algorithm to 'see' the statistical distribution of the hidden future data. This artificially inflates your accuracy score and ruins the integrity of the scientific experiment. The Test set mathematically represents the 'Future' (Data from tomorrow). You cannot calculate the Mean of data that doesn't exist yet! Therefore, we `fit()` only the Training set, freeze those exact statistical constants, and rigidly apply them (`transform()`) to the Test set to ensure absolute mathematical isolation."

3. Interviewer: "In a medical context (like predicting Cancer), why is looking at raw 'Accuracy' extremely dangerous? Why must we look at 'Recall'?"
   Senior Answer: "Imagine a dataset with $99$ Healthy patients and $1$ Cancer patient. A totally broken algorithm that just blindly guesses 'Healthy' for every single person will mathematically achieve $99\\%$ Accuracy. The CEO will deploy it, and the $1$ Cancer patient will die because the algorithm missed them. Accuracy is mathematically useless on imbalanced datasets. 'Recall' (also known as Sensitivity) mathematically isolates the True Positives. It asks: 'Out of all the people who ACTUALLY had cancer, what percentage did the algorithm successfully catch?' In medicine, we will gladly accept a lower overall Accuracy (more False Alarms) to mathematically guarantee a Recall of $99.9\\%$ for the Malignant class, ensuring no dying patient is ever sent home."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Scientific Computing (Machine Learning) Completed.")
