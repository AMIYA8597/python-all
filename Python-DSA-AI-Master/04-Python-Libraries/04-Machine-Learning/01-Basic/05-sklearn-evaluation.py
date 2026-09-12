"""
Scikit-Learn Model Evaluation: A Textbook-Grade Interactive Lesson
==================================================================

Welcome to the definitive guide on Model Evaluation using Scikit-Learn (sklearn).
This module covers the theoretical foundations, mathematical equations, and
practical Python implementations for evaluating Machine Learning models.

Table of Contents
-----------------
1. Introduction to Model Evaluation
2. Classification Metrics
    2.1 Confusion Matrix
    2.2 Accuracy, Precision, Recall, F1-Score
    2.3 ROC Curve and AUC
3. Regression Metrics
    3.1 Mean Absolute Error (MAE)
    3.2 Mean Squared Error (MSE) & Root Mean Squared Error (RMSE)
    3.3 R-Squared (R²) Score
4. Cross-Validation
5. Real-World Applications
6. Big-O Complexity of Evaluation Metrics

1. Introduction to Model Evaluation
-----------------------------------
Training a model is only half the battle. To know if your model will perform well
on unseen data, you must rigorously evaluate it using appropriate metrics. 
Choosing the right metric depends on the problem domain (e.g., classification vs. regression)
and the specific business requirements (e.g., minimizing false positives vs. false negatives).

2. Classification Metrics
-------------------------
### 2.1 Confusion Matrix
A confusion matrix is a table used to describe the performance of a classification model.
It divides the predictions into four categories:
- True Positives (TP): Predicted Positive, Actual Positive
- True Negatives (TN): Predicted Negative, Actual Negative
- False Positives (FP): Predicted Positive, Actual Negative (Type I Error)
- False Negatives (FN): Predicted Negative, Actual Positive (Type II Error)

### 2.2 Accuracy, Precision, Recall, F1-Score
- **Accuracy**: (TP + TN) / (TP + TN + FP + FN)
- **Precision**: TP / (TP + FP)  -> "Of all positive predictions, how many were correct?"
- **Recall (Sensitivity)**: TP / (TP + FN) -> "Of all actual positives, how many did we find?"
- **F1-Score**: 2 * (Precision * Recall) / (Precision + Recall) -> Harmonic mean of Precision and Recall.

### 2.3 ROC Curve and AUC
The Receiver Operating Characteristic (ROC) curve plots the True Positive Rate (Recall)
against the False Positive Rate (FP / (FP + TN)) at various threshold settings.
The Area Under the Curve (AUC) represents the probability that the model ranks a random
positive example higher than a random negative example.

3. Regression Metrics
---------------------
### 3.1 Mean Absolute Error (MAE)
MAE = (1/n) * Σ|y_true - y_pred|
Measures the average magnitude of the errors without considering their direction.

### 3.2 Mean Squared Error (MSE) & RMSE
MSE = (1/n) * Σ(y_true - y_pred)²
RMSE = √MSE
Penalizes larger errors more heavily than MAE.

### 3.3 R-Squared (R²) Score
R² = 1 - (SS_res / SS_tot)
Where SS_res is the sum of squares of residuals, and SS_tot is the total sum of squares.
Indicates the proportion of the variance in the dependent variable that is predictable.

4. Cross-Validation
-------------------
Instead of a single train-test split, K-Fold Cross-Validation divides the data into K subsets.
The model is trained on K-1 subsets and evaluated on the remaining subset. This process is 
repeated K times, ensuring every data point is used for both training and validation.

5. Big-O Complexity
-------------------
Most evaluation metrics operate in O(N) time, where N is the number of samples, because they
require a single pass over the predictions and true values to compute sums or averages.
- Confusion Matrix: O(N)
- MSE / MAE / R²: O(N)
- ROC AUC: O(N log N) because it involves sorting the predictions by their probability scores.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any

# Scikit-Learn Imports
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score,
    f1_score, classification_report, roc_curve, auc, roc_auc_score,
    mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.model_selection import KFold, cross_val_score
from sklearn.datasets import make_classification, make_regression
from sklearn.linear_model import LogisticRegression, LinearRegression


class ClassificationEvaluator:
    """
    A comprehensive class for evaluating classification models.
    Provides methods to compute various metrics and explain their mathematical background.
    """
    
    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None):
        """
        Initialize the evaluator with true labels, predicted labels, and optionally, probabilities.
        
        Args:
            y_true: Ground truth (correct) target values.
            y_pred: Estimated targets as returned by a classifier.
            y_prob: Estimated probabilities for the positive class (used for ROC/AUC).
        """
        self.y_true = y_true
        self.y_pred = y_pred
        self.y_prob = y_prob

    def evaluate_basic_metrics(self) -> Dict[str, float]:
        """
        Calculates and returns Accuracy, Precision, Recall, and F1-Score.
        
        Time Complexity: O(N) where N is the number of samples.
        Space Complexity: O(1) auxiliary space.
        """
        metrics = {
            "Accuracy": accuracy_score(self.y_true, self.y_pred),
            "Precision": precision_score(self.y_true, self.y_pred, zero_division=0),
            "Recall": recall_score(self.y_true, self.y_pred, zero_division=0),
            "F1-Score": f1_score(self.y_true, self.y_pred, zero_division=0)
        }
        
        print("\n--- Basic Classification Metrics ---")
        for k, v in metrics.items():
            print(f"{k}: {v:.4f}")
            
        return metrics

    def display_confusion_matrix(self) -> np.ndarray:
        """
        Computes and displays the confusion matrix.
        
        Returns:
            The confusion matrix array.
        """
        cm = confusion_matrix(self.y_true, self.y_pred)
        print("\n--- Confusion Matrix ---")
        print(f"True Negatives (TN): {cm[0, 0]}")
        print(f"False Positives (FP): {cm[0, 1]} (Type I Error)")
        print(f"False Negatives (FN): {cm[1, 0]} (Type II Error)")
        print(f"True Positives (TP): {cm[1, 1]}")
        return cm

    def display_classification_report(self) -> str:
        """
        Generates a comprehensive classification report.
        """
        report = classification_report(self.y_true, self.y_pred)
        print("\n--- Classification Report ---")
        print(report)
        return report

    def evaluate_roc_auc(self) -> float:
        """
        Computes the ROC AUC score if probabilities are provided.
        
        Time Complexity: O(N log N) due to sorting required for ROC curve generation.
        """
        if self.y_prob is None:
            print("\nCannot compute ROC AUC: Probability scores (y_prob) not provided.")
            return 0.0
            
        auc_score = roc_auc_score(self.y_true, self.y_prob)
        print(f"\n--- ROC AUC Score ---\nAUC: {auc_score:.4f}")
        return auc_score


class RegressionEvaluator:
    """
    A comprehensive class for evaluating regression models.
    """
    
    def __init__(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Initialize the evaluator with true values and predicted values.
        """
        self.y_true = y_true
        self.y_pred = y_pred

    def evaluate_all(self) -> Dict[str, float]:
        """
        Calculates MAE, MSE, RMSE, and R2 score.
        
        Time Complexity: O(N) for all metrics.
        """
        mae = mean_absolute_error(self.y_true, self.y_pred)
        mse = mean_squared_error(self.y_true, self.y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_true, self.y_pred)
        
        metrics = {
            "Mean Absolute Error (MAE)": mae,
            "Mean Squared Error (MSE)": mse,
            "Root Mean Squared Error (RMSE)": rmse,
            "R-Squared (R2) Score": r2
        }
        
        print("\n--- Regression Metrics ---")
        for k, v in metrics.items():
            print(f"{k}: {v:.4f}")
            
        return metrics


def demonstrate_cross_validation() -> None:
    """
    Demonstrates K-Fold Cross Validation using scikit-learn.
    Cross-validation provides a more robust estimate of model performance
    compared to a single train/test split.
    """
    print("\n==============================================")
    print("Demonstrating K-Fold Cross-Validation")
    print("==============================================")
    
    # Generate a synthetic dataset
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    model = LogisticRegression()
    
    # K-Fold CV with k=5
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    # Evaluate model
    scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')
    
    print(f"Scores for each fold: {scores}")
    print(f"Mean Accuracy: {scores.mean():.4f}")
    print(f"Standard Deviation: {scores.std():.4f}")


def run_classification_scenario() -> None:
    """
    Simulates a real-world classification scenario: Diagnosing a rare disease.
    """
    print("\n==============================================")
    print("Real-World Scenario: Rare Disease Diagnosis")
    print("==============================================")
    
    # Generate imbalanced dataset (rare disease)
    X, y = make_classification(
        n_samples=1000, n_features=5, weights=[0.9, 0.1], 
        random_state=42, flip_y=0.05
    )
    
    # Train a model
    model = LogisticRegression()
    model.fit(X, y)
    
    # Predictions
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]
    
    evaluator = ClassificationEvaluator(y_true=y, y_pred=y_pred, y_prob=y_prob)
    evaluator.evaluate_basic_metrics()
    evaluator.display_confusion_matrix()
    evaluator.display_classification_report()
    evaluator.evaluate_roc_auc()
    
    print("\n[Analysis]: Notice how Accuracy might be high due to the class imbalance,")
    print("but Recall for the positive class (the disease) is the crucial metric here.")
    print("We want to minimize False Negatives (telling a sick person they are healthy).")


def run_regression_scenario() -> None:
    """
    Simulates a real-world regression scenario: Predicting house prices.
    """
    print("\n==============================================")
    print("Real-World Scenario: House Price Prediction")
    print("==============================================")
    
    # Generate synthetic housing data
    X, y = make_regression(n_samples=500, n_features=3, noise=15.0, random_state=42)
    
    # Train a model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predictions
    y_pred = model.predict(X)
    
    evaluator = RegressionEvaluator(y_true=y, y_pred=y_pred)
    evaluator.evaluate_all()
    
    print("\n[Analysis]: R2 score tells us how much variance in house prices our model explains.")
    print("RMSE tells us, on average, how far off our predictions are in actual dollar amounts.")


if __name__ == '__main__':
    print("Starting Scikit-Learn Model Evaluation Lesson...\n")
    
    # 1. Classification
    run_classification_scenario()
    
    # 2. Regression
    run_regression_scenario()
    
    # 3. Cross Validation
    demonstrate_cross_validation()
    
    print("\nLesson complete. Experiment with different models and parameters!")
