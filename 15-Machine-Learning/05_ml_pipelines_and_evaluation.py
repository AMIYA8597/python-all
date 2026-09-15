"""
# ==============================================================================
# LABORATORY: MACHINE LEARNING (PIPELINES & EVALUATION METRICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior data scientist trains an algorithm to detect a rare genetic disease 
# (present in 1% of the population). The model returns 99% accuracy. They 
# celebrate and deploy it to a hospital. Weeks later, the hospital discovers 
# the model mathematically hardcoded a "False" return for every patient. 
# It achieved 99% accuracy by completely ignoring the disease. Patients die.
#
# A senior AI engineer understands the mathematical trap of "Class Imbalance". 
# They completely ignore the "Accuracy" metric. They deploy a strict Evaluation 
# matrix focusing on "Recall" (the mathematical ability to capture True Positives) 
# and the F1-Score. Furthermore, they architect a Scikit-Learn `Pipeline` to 
# mathematically fuse Data Scaling, Imputation, and Model Training into a single 
# serialized object, guaranteeing zero Data Leakage during production inference.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Scikit-Learn Pipelines (`Pipeline`, `ColumnTransformer`).
# - Execute Advanced Evaluation (Precision, Recall, F1, Confusion Matrix).
# - Architect Data Leakage prevention during preprocessing.
#
# ==============================================================================
"""

import numpy as np
import pandas as pd
import warnings

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

warnings.filterwarnings("ignore")

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE IMBALANCED DATASET)
# ==============================================================================
class MLPipelineSimulator:
    
    def __init__(self):
        print("  [INIT] Generating Imbalanced Dataset (95% Negative, 5% Positive)...")
        np.random.seed(42)
        
        # We simulate 10,000 patients. 
        # Features: Age (Num), Blood Pressure (Num), Blood Type (Cat)
        n_samples = 10000
        
        data = {
            'Age': np.random.normal(50, 15, n_samples),
            'Blood_Pressure': np.random.normal(120, 20, n_samples),
            # Introduce some NaNs to require Imputation!
            'Blood_Type': np.random.choice(['A', 'B', 'O', 'AB', np.nan], n_samples),
        }
        self.X = pd.DataFrame(data)
        
        # Highly Imbalanced Target! Only 5% have the rare disease.
        self.y = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])
        
        # Strict Partitioning
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: SCIKIT-LEARN PIPELINES
    # --------------------------------------------------------------------------
    def build_and_train_pipeline(self) -> Pipeline:
        """
        [SECURE] The Pipeline Architecture.
        Fuses Imputation, Scaling, Encoding, and Modeling into ONE unified object.
        """
        print("\n  [EXECUTION] Architecting the Data Pipeline...")
        
        # 1. Define how to mathematically treat Numerical features
        numeric_features = ['Age', 'Blood_Pressure']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])
        
        # 2. Define how to mathematically treat Categorical features
        categorical_features = ['Blood_Type']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        # 3. Fuse them using a ColumnTransformer
        preprocessor = ColumnTransformer(transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
        # 4. Attach the ML Model to the end of the Pipeline
        # We use `class_weight='balanced'` to mathematically penalize the model 
        # heavily if it gets the rare 5% class wrong!
        full_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42))
        ])
        
        print("  -> Firing `.fit()` on the unified Pipeline...")
        # A single `.fit()` command executes all imputation, scaling, encoding, and training!
        full_pipeline.fit(self.X_train, self.y_train)
        
        return full_pipeline


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: EVALUATION METRICS
    # --------------------------------------------------------------------------
    def evaluate_model(self, pipeline: Pipeline):
        """
        [SECURE] Evaluating True Performance (Ignoring 'Accuracy').
        """
        print("\n  [ANALYSIS] Evaluating Model via Precision, Recall, and F1...")
        
        # The `.predict()` automatically routes the new Test data through the Imputers and Scalers!
        predictions = pipeline.predict(self.X_test)
        
        # 1. The Confusion Matrix
        # [ True Negatives (TN)   |  False Positives (FP) ]
        # [ False Negatives (FN)  |  True Positives (TP)  ]
        cm = confusion_matrix(self.y_test, predictions)
        print("\n  [CONFUSION MATRIX]")
        print(f"  True Negatives:  {cm[0][0]:,} | False Positives: {cm[0][1]:,}")
        print(f"  False Negatives: {cm[1][0]:,} | True Positives:  {cm[1][1]:,}")
        
        # 2. The Classification Report (Precision, Recall, F1)
        print("\n  [CLASSIFICATION REPORT]")
        print(classification_report(self.y_test, predictions, target_names=['Healthy (0)', 'Disease (1)']))


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_pipelines():
    section_header("Machine Learning: Pipelines & Metrics")
    
    sim = MLPipelineSimulator()
    model_pipeline = sim.build_and_train_pipeline()
    sim.evaluate_model(model_pipeline)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By architecting a Scikit-Learn `Pipeline`, the ML Engineer guaranteed ")
    print("  that mathematical Imputation parameters (like the Median Age) were ")
    print("  calculated STRICTLY on the Training Set, preventing Data Leakage. ")
    print("  Furthermore, by analyzing 'Recall' instead of 'Accuracy', they proved ")
    print("  the model's actual capability to detect the rare disease.")


def run_all_labs():
    demonstrate_pipelines()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Define Precision and Recall mathematically. If you are predicting Cancer, which one do you optimize for?"
   Senior Answer: "Precision is $TP / (TP + FP)$. It answers: 'Out of all the people the model claimed have cancer, how many actually do?' Recall is $TP / (TP + FN)$. It answers: 'Out of all the people who ACTUALLY have cancer in reality, how many did the model successfully catch?' In medical diagnostics (Cancer), you mathematically optimize for Recall. A False Positive (telling a healthy person they have cancer) is stressful but solved by a secondary biopsy. A False Negative (missing the cancer and sending a sick patient home) is fatal. Therefore, we tune the model to aggressively catch all True Positives, even if it hurts Precision."

2. Interviewer: "What is Data Leakage in Preprocessing, and how does a Scikit-Learn `Pipeline` mathematically prevent it?"
   Senior Answer: "The Global Imputation Trap. A junior developer will take the entire dataset (Train + Test), calculate the Mean Age, and fill all missing values globally *before* calling `train_test_split`. This mathematically leaks information from the Test Set into the Training Set because the Training Set is now influenced by the Mean of the Test Set! A Scikit-Learn `Pipeline` guarantees that when you call `pipeline.fit(X_train)`, the `StandardScaler` and `SimpleImputer` mathematically calculate their Means/Medians strictly utilizing the `X_train` rows. When you call `pipeline.predict(X_test)`, it applies those exact saved metrics to the Test Set, perfectly simulating a real-world production deployment."

3. Interviewer: "What does `class_weight='balanced'` physically do to the Loss Function inside a Random Forest or Logistic Regression model?"
   Senior Answer: "Mathematical Penalization. In an imbalanced dataset (99% Class 0, 1% Class 1), the algorithm's Loss Function will simply learn to ignore Class 1 because ignoring it yields 99% accuracy. Setting `class_weight='balanced'` alters the underlying Calculus. It mathematically instructs the Cost Function to apply a massive penalty (e.g., $99x$ larger) when the model makes a mistake on the rare Class 1, and a tiny penalty ($1x$) when it mistakes Class 0. This violently forces the algorithm's Gradient Descent to mathematically care about the minority class."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Machine Learning (Pipelines & Evaluation) Completed.")
