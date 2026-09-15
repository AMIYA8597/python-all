"""
# ==============================================================================
# LABORATORY: MACHINE LEARNING (ADVANCED ML & XGBOOST)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist trains a single Decision Tree on a dataset. The tree 
# makes wild, erratic predictions because it is highly sensitive to statistical 
# noise. The accuracy on the test set is 65%.
#
# A senior AI engineer understands "Gradient Boosting". Instead of training one 
# massive tree, they train 1,000 tiny, weak trees sequentially. Tree #2 mathematically 
# analyzes the exact errors made by Tree #1, and optimizes its weights specifically 
# to fix those errors using Calculus (Gradient Descent). Tree #3 fixes the errors 
# of Tree #2. They use XGBoost (Extreme Gradient Boosting), which optimizes this 
# calculus using C++ and GPU acceleration. The accuracy hits 94%, winning a 
# Kaggle competition.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Ensemble Methods (Bagging vs Boosting).
# - Execute XGBoost mathematical architecture.
# - Architect Hyperparameter Optimization (GridSearchCV).
#
# ==============================================================================
"""

import numpy as np
import warnings
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE ENSEMBLE)
# ==============================================================================
class AdvancedMLSimulator:
    
    def __init__(self):
        np.random.seed(42)
        print("  [INIT] Generating Complex Non-Linear Dataset (1,000 rows)...")
        self.X = np.random.rand(1000, 5)
        # Complex non-linear target requiring an advanced model!
        self.y = (self.X[:, 0]**2 + np.sin(self.X[:, 1] * 10) > 0.5).astype(int)
        
        # Proper Architectural Split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: GRADIENT BOOSTING
    # --------------------------------------------------------------------------
    def execute_gradient_boosting(self):
        """
        [SECURE] Sequential Error Correction (Boosting).
        """
        print("\n  [EXECUTION] Training Gradient Boosting Machine...")
        
        # We simulate XGBoost using sklearn's built-in Gradient Boosting
        # n_estimators: The number of sequential trees to build.
        # learning_rate: How aggressively each tree corrects the previous tree's errors.
        model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
        model.fit(self.X_train, self.y_train)
        
        predictions = model.predict(self.X_test)
        acc = accuracy_score(self.y_test, predictions)
        
        print(f"  -> Gradient Boosting Accuracy: {acc * 100:.2f}%")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: HYPERPARAMETER OPTIMIZATION
    # --------------------------------------------------------------------------
    def execute_grid_search(self):
        """
        [SECURE] Grid Search CV.
        Mathematically tests multiple combinations of hyperparameters to find the absolute best model.
        """
        print("\n  [EXECUTION] Executing Hyperparameter Grid Search (Calculus Tuning)...")
        
        model = GradientBoostingClassifier()
        
        # The Grid of parameters to test!
        param_grid = {
            'n_estimators': [50, 100],
            'learning_rate': [0.01, 0.1],
            'max_depth': [2, 3]
        }
        
        # cv=3 means 3-Fold Cross Validation.
        # It will train 2 * 2 * 2 = 8 combinations, across 3 folds = 24 total models!
        print("  -> Architecting 24 models in RAM to mathematically prove the best configuration...")
        grid = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
        grid.fit(self.X_train, self.y_train)
        
        print(f"  -> Best Hyperparameters Found: {grid.best_params_}")
        
        best_model = grid.best_estimator_
        predictions = best_model.predict(self.X_test)
        acc = accuracy_score(self.y_test, predictions)
        
        print(f"  -> Optimized Accuracy: {acc * 100:.2f}%")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_advanced_ml():
    section_header("Machine Learning: XGBoost & Grid Search")
    
    sim = AdvancedMLSimulator()
    sim.execute_gradient_boosting()
    sim.execute_grid_search()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing Gradient Boosting, the ML algorithm sequentially corrected ")
    print("  its own mathematical errors. By wrapping it in a GridSearchCV, the ")
    print("  Senior Engineer automated the discovery of the mathematically optimal ")
    print("  hyperparameters, guaranteeing peak deployment accuracy.")


def run_all_labs():
    demonstrate_advanced_ml()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the mathematical difference between Bagging (Random Forests) and Boosting (XGBoost)?"
   Senior Answer: "Parallel vs Sequential Architecture. Bagging (Bootstrap Aggregating) trains $1,000$ Decision Trees completely independently and simultaneously in parallel (e.g., using $16$ CPU cores). Each tree sees a slightly different random subset of the data. The final prediction is a democratic vote. Boosting trains trees sequentially. Tree $1$ makes predictions. We calculate the Calculus Gradient (the Error). Tree $2$ is then mathematically trained *specifically* on the Error residuals of Tree $1$. Because they learn from previous mistakes, Boosting models (XGBoost) almost always achieve higher accuracy than Bagging models, but they are inherently harder to parallelize during training."

2. Interviewer: "Why do we use Cross-Validation (K-Fold) during Hyperparameter tuning instead of just checking the Test set?"
   Senior Answer: "Information Leakage via Iteration. If you run a `for` loop testing $100$ different hyperparameter combinations and check the accuracy against the Test Set every single time, you are mathematically 'peeking' at the Test Set. You will eventually select the parameters that got lucky on that specific Test Set, causing you to Overfit to the Test Set! K-Fold Cross Validation temporarily slices the *Training* set into $K$ pieces (folds). It trains on $K-1$ folds and validates on the $1$ remaining fold, rotating until it mathematically proves the best parameters without ever looking at the quarantined Test Set."

3. Interviewer: "What is the 'Learning Rate' in Gradient Boosting, and how does it relate to the number of trees (`n_estimators`)?"
   Senior Answer: "The Step Size in Gradient Descent. The Learning Rate ($\eta$) mathematically scales the contribution of each individual tree. If the Learning Rate is $1.0$, Tree $2$ completely overrides the errors of Tree $1$. This causes mathematical oscillation and Overfitting. If the Learning Rate is tiny (e.g., $0.01$), each tree only makes a micro-adjustment. Therefore, there is a strict inverse mathematical relationship: If you lower the Learning Rate, you *must* increase the number of trees (`n_estimators`) to allow the model enough mathematical steps to reach the optimal minimum. Tiny steps require more steps."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Machine Learning (Advanced ML) Completed.")
