"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (MACHINE LEARNING PIPELINE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a Machine Learning model using all of their data. 
# It achieves 99% accuracy on their laptop. They deploy it to Production. When 
# the model encounters brand-new real-world user data, it completely fails, 
# resulting in massive financial loss. They fell victim to "Data Overfitting".
#
# A senior Data Scientist understands the "Train/Test Split" architectural 
# requirement. They mathematically slice 20% of their dataset and hide it in a 
# cryptographic vault. They train the model on the 80%. They then force the model 
# to predict the hidden 20%. By verifying the model's accuracy on data it has 
# *never physically seen before*, they mathematically guarantee its generalized 
# performance in Production.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Train/Test Split (Preventing Data Leakage/Overfitting).
# - Master Feature Scaling (Standardization/Normalization).
# - Execute a mathematical classification prediction using `scikit-learn`.
#
# ==============================================================================
"""

import timeit
import random

# Gracefully handle missing scikit-learn dependency
try:
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MACHINE LEARNING ARCHITECTURE
# ==============================================================================
def demonstrate_ml_pipeline():
    section_header("The Scikit-Learn Pipeline: Train, Scale, Predict")
    
    if not HAS_SKLEARN:
        print("  [ERROR] scikit-learn is not installed.")
        print("  Run `pip install scikit-learn` to execute this lab.")
        return
        
    # --- 1. DATA GENERATION (The Extract Phase) ---
    print("  [PHASE 1: DATA GENERATION]")
    print("    Simulating 10,000 customers (10 features each).")
    print("    Target: Will this customer 'Churn' (Cancel their subscription)?")
    
    # X = The Features (Age, Login Frequency, Money Spent, etc.)
    # Y = The Target (0 = Active, 1 = Churned)
    X, y = make_classification(n_samples=10_000, n_features=10, 
                               n_informative=5, random_state=42)
                               
    print(f"    -> X shape (Features Matrix): {X.shape}")
    print(f"    -> y shape (Target Vector):   {y.shape}")
    
    
    # --- 2. TRAIN / TEST SPLIT (The Prevention of Overfitting) ---
    print("\n  [PHASE 2: TRAIN / TEST SPLIT]")
    # We mathematically quarantine 20% of the data! The model will NEVER see this 
    # during training. It represents the unknown future!
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    print(f"    -> Training Set (80%): {X_train.shape[0]} customers.")
    print(f"    -> Testing Set  (20%): {X_test.shape[0]} customers hidden in the vault.")
    
    
    # --- 3. FEATURE SCALING (Mathematical Standardization) ---
    print("\n  [PHASE 3: FEATURE SCALING]")
    # Machine Learning models use Gradient Descent (Calculus) to find patterns.
    # If Feature 1 (Age) ranges from 18 to 90, and Feature 2 (Income) ranges 
    # from 0 to 1,000,000, the Calculus violently breaks because the Income math 
    # completely eclipses the Age math!
    
    scaler = StandardScaler()
    # 1. The scaler mathematically calculates the Mean and Variance of the TRAINING data.
    # 2. It mathematically squashes ALL numbers to have a Mean of 0 and a StdDev of 1.
    X_train_scaled = scaler.fit_transform(X_train)
    
    # CRITICAL ARCHITECTURAL RULE: We ONLY `.transform()` the Test data!
    # If we `.fit_transform()` the Test data, we leak the mean of the future into the model!
    X_test_scaled = scaler.transform(X_test)
    print("    -> All features mathematically scaled to Z-Scores (Mean=0, StdDev=1).")
    
    
    # --- 4. MODEL TRAINING (The Fit) ---
    print("\n  [PHASE 4: MODEL TRAINING (Logistic Regression)]")
    model = LogisticRegression()
    
    start_train = timeit.default_timer()
    # The model mathematically iterates over the scaled data, adjusting its 
    # internal neural weights to map the Features (X) to the Target (Y).
    model.fit(X_train_scaled, y_train)
    end_train = timeit.default_timer()
    
    print(f"    -> Training complete in {end_train - start_train:.4f} seconds.")
    
    
    # --- 5. PREDICTION & VALIDATION (The Moment of Truth) ---
    print("\n  [PHASE 5: PREDICTION ON UNSEEN DATA]")
    # We unlock the vault and pass the 2,000 unknown customers into the model.
    # It mathematically calculates the probability of churn for each one!
    predictions = model.predict(X_test_scaled)
    
    # We compare the model's guesses against the REAL answers!
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"    -> Model Accuracy on Unseen Data: {accuracy * 100:.2f}%")
    
    if accuracy > 0.80:
        print("    -> [VERDICT] The model is generalized and safe for Production!")
    else:
        print("    -> [VERDICT] The model failed. Retrain with better features or algorithms.")


def run_all_labs():
    demonstrate_ml_pipeline()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Data Leakage' in Machine Learning, and why must you never run `.fit_transform()` on your Test Data when scaling features?"
   Senior Answer: "Data Leakage is a catastrophic architectural failure where information from the 'future' (the Test Data) accidentally bleeds into the model during Training. When executing Feature Scaling (e.g., `StandardScaler`), the scaler mathematically calculates the Mean and Standard Deviation of the dataset to squash the values. If you run `.fit_transform()` on the entire dataset *before* the Train/Test split, the Training Data is mathematically scaled using the Mean of the Test Data! The model secretly learns the mathematical distribution of the 'hidden' data, resulting in $99\\%$ accuracy during testing, but complete failure in Production. You must strictly `.fit()` the scaler ONLY on the Training Data, and apply that frozen mathematical logic (`.transform()`) to the Test Data."

2. Interviewer: "Why is Feature Scaling mathematically mandatory for algorithms like Logistic Regression, Neural Networks, or K-Nearest Neighbors?"
   Senior Answer: "Many Machine Learning algorithms rely on distance calculations (like Euclidean distance in KNN) or Gradient Descent (Calculus optimization in Neural Networks). If one feature represents 'Age' (ranging from $18$ to $90$) and another represents 'Yearly Income' (ranging from $\\$20,000$ to $\\$500,000$), the sheer mathematical magnitude of the Income feature will violently dominate the Calculus calculations. The algorithm will falsely assume that Income is a million times more important than Age purely because the raw numbers are bigger. By scaling all features (Standardization or Normalization), we mathematically force all dimensions onto an identical geometric scale (e.g., between $-1$ and $1$), allowing the algorithm to find the true underlying correlation rather than being blinded by raw magnitude."

3. Interviewer: "If a model achieves $99\\%$ accuracy on the Training Data, but only $50\\%$ accuracy on the Test Data, what has architecturally happened, and how do you fix it?"
   Senior Answer: "The model has catastrophically 'Overfit'. It failed to learn the underlying mathematical *rules* of the data; instead, it simply memorized the exact answers for the Training Set, like a student memorizing an exam key without understanding the subject. When presented with the Test Data (questions it hasn't seen before), it fails completely. To resolve Overfitting, you must constrain the model's complexity. You can apply 'Regularization' (L1/L2 penalties that mathematically punish the model for relying too heavily on specific features), reduce the depth of Decision Trees, introduce 'Dropout' layers in Neural Networks, or simply gather significantly more training data to force the model to generalize."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Data Science (Machine Learning) Completed.")
