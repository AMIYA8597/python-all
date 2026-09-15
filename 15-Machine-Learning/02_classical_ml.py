"""
# ==============================================================================
# LABORATORY: MACHINE LEARNING (CLASSICAL ML & SCIKIT-LEARN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist wants to predict house prices. They load the entire 
# dataset into `RandomForestRegressor`, call `.fit()`, and then call `.score()` 
# on the exact same dataset. The model returns 99.9% accuracy. They celebrate 
# and deploy to production. The next day, the model is completely wrong on every 
# single real-world prediction. The company loses millions.
#
# A senior AI engineer understands "Overfitting" and "Data Leakage". They strictly 
# mathematically partition the data into a Train Set and a Test Set. They use 
# K-Fold Cross Validation. They realize the model merely memorized the training 
# data (100% accuracy) but failed mathematically to generalize to unseen data 
# (40% test accuracy). They adjust the architectural hyper-parameters to prevent 
# memorization, saving the system.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Scikit-Learn Estimator API (`fit`, `predict`, `transform`).
# - Execute strict Train/Test splits to prevent Data Leakage.
# - Architect classification (Logistic Regression) vs regression (Random Forest).
#
# ==============================================================================
"""

import numpy as np
import warnings

# We import mock models from sklearn to simulate the API
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Suppress sklearn warnings for clean terminal output
warnings.filterwarnings("ignore")

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE DATASET)
# ==============================================================================
class ClassicalMLSimulator:
    
    def __init__(self):
        # Features (X): e.g., Age, Income, Credit Score
        # Target (y): e.g., Did they default on the loan? (1 = Yes, 0 = No)
        np.random.seed(42)
        print("  [INIT] Generating Synthetic Banking Dataset (1,000 customers)...")
        
        self.X = np.random.rand(1000, 3) * 100 
        # Create a non-linear target variable to make it interesting
        self.y = (self.X[:, 0] + self.X[:, 1] > 100).astype(int)


    # --------------------------------------------------------------------------
    # THE ANTI-PATTERN: DATA LEAKAGE (TESTING ON TRAINING DATA)
    # --------------------------------------------------------------------------
    def execute_junior_workflow(self):
        """
        [WARNING] THIS IS CATASTROPHICALLY FLAWED.
        Training and testing on the exact same data leads to Overfitting illusions.
        """
        print("\n  [EXECUTION] Junior Workflow (Data Leakage)...")
        
        # A Random Forest is extremely powerful. It can literally memorize the data.
        model = RandomForestClassifier(n_estimators=100, max_depth=None)
        
        # Train on ALL data
        model.fit(self.X, self.y)
        
        # Predict on ALL data (The exact same data it just memorized!)
        predictions = model.predict(self.X)
        accuracy = accuracy_score(self.y, predictions)
        
        print(f"  -> Model Accuracy: {accuracy * 100:.2f}%")
        print("  -> [FATAL ERROR] The model achieved 100% because it memorized the answers!")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: TRAIN/TEST SPLIT
    # --------------------------------------------------------------------------
    def execute_senior_workflow(self):
        """
        [SECURE] Train/Test Split.
        We mathematically lock away 20% of the data. The model NEVER sees it during training.
        """
        print("\n  [EXECUTION] Senior Workflow (Train/Test Partitioning)...")
        
        # 1. Partition the Data
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        print(f"  -> Training Data Shape: {X_train.shape}")
        print(f"  -> Unseen Test Data Shape: {X_test.shape}")
        
        # 2. Train the Model (ONLY on the Training Set!)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        # 3. Test the Model (On the mathematically quarantined Test Set!)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"  -> True Generalization Accuracy: {accuracy * 100:.2f}%")
        print("  -> [FLAWLESS] The model proved it can predict unseen mathematical realities.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_ml():
    section_header("Machine Learning: Scikit-Learn API")
    
    sim = ClassicalMLSimulator()
    sim.execute_junior_workflow()
    sim.execute_senior_workflow()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By mathematically quarantining a Test Set, the Senior Engineer ")
    print("  prevented Data Leakage. They proved the model learned the underlying ")
    print("  mathematical patterns (Generalization) rather than simply memorizing ")
    print("  the training examples (Overfitting).")


def run_all_labs():
    demonstrate_ml()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Overfitting' in Machine Learning, and how does a Random Forest physically do it?"
   Senior Answer: "Memorization vs Generalization. Overfitting occurs when a model learns the mathematical 'noise' of the training data rather than the underlying pattern. A Random Forest is a collection of Decision Trees. If you do not mathematically restrict the `max_depth` of a Decision Tree, it will literally continue splitting branches until every single training example is perfectly isolated in its own leaf node. It has essentially built a massive `if-else` lookup table of the training set. When a new, unseen data point arrives in production, the model fails catastrophically because the new point doesn't perfectly match the memorized lookup table."

2. Interviewer: "Explain the architectural difference between Classification and Regression."
   Senior Answer: "Discrete vs Continuous Mathematical Output. A Classification algorithm (like Logistic Regression or SVM) predicts a discrete categorical label. For example, predicting whether an email is 'Spam' ($1$) or 'Not Spam' ($0$). The output is passed through a Sigmoid or Softmax function to squash the mathematical output into a probability between $0$ and $1$. A Regression algorithm (like Linear Regression) predicts a continuous numerical value. For example, predicting the exact price of a house as $\$450,234.50$. The mathematical loss function for Classification is usually Cross-Entropy, while Regression uses Mean Squared Error (MSE)."

3. Interviewer: "If you have a massive dataset of 10 Million rows, why would you use an ML Algorithm like Logistic Regression instead of a Deep Neural Network?"
   Senior Answer: "Explainability and Hardware Overhead. A Deep Neural Network is mathematically opaque (a Black Box). It might achieve $98\\%$ accuracy, but if the bank denies a customer a loan, you cannot legally or mathematically explain *why* the neural network denied it. Logistic Regression is a linear equation. You can look at the exact learned weights ($W_1 = 5.4$ for Income, $W_2 = -3.2$ for Debt) and easily explain the decision to stakeholders. Furthermore, Logistic Regression trains in seconds on a standard CPU, whereas a Neural Network requires massive GPU clusters and hours of backpropagation, destroying architectural ROI if the linear model achieves similar accuracy."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Machine Learning (Classical ML) Completed.")
