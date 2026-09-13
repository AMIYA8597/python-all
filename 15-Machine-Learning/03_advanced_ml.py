"""
Advanced Machine Learning Concepts
----------------------------------
This module provides advanced professional-grade implementations and concepts
related to Machine Learning in Python. It simulates advanced architectures
like Ensemble methods (Random Forests, Gradient Boosting concepts) and
incorporates type hints, extensive documentation, and tests.

### Why Advanced ML?
Basic models like Linear Regression or Decision Trees often fail to capture
complex, non-linear relationships or are prone to overfitting. Advanced
techniques like Ensembling combine multiple weak learners to create a strong,
robust model.

### Concepts Covered:
1.  **Ensemble Learning**: Combining predictions from multiple models.
    -   *Bagging* (Bootstrap Aggregating): e.g., Random Forest. Reduces variance.
    -   *Boosting*: e.g., Gradient Boosting, XGBoost. Reduces bias by focusing on errors of previous models.
2.  **Cross-Validation**: Ensuring the model generalizes well to unseen data.
3.  **Hyperparameter Tuning**: Finding the optimal configuration for models.
"""

import math
import random
from typing import List, Tuple, Dict, Any, Callable
from collections import Counter


class DecisionStump:
    """
    A simple Decision Stump (a decision tree with depth 1).
    Used as a weak learner in boosting algorithms.
    """
    def __init__(self) -> None:
        self.feature_index: int = 0
        self.threshold: float = 0.0
        self.polarity: int = 1
        self.alpha: float = 0.0 # Weight of this stump in the ensemble

    def predict(self, X: List[List[float]]) -> List[int]:
        """
        Predicts labels (+1 or -1) for input data X.
        
        Args:
            X: List of samples, where each sample is a list of features.
            
        Returns:
            List of predicted labels (+1 or -1).
        """
        n_samples = len(X)
        predictions = [1] * n_samples
        
        for i in range(n_samples):
            feature_val = X[i][self.feature_index]
            if self.polarity == 1:
                if feature_val < self.threshold:
                    predictions[i] = -1
            else:
                if feature_val > self.threshold:
                    predictions[i] = -1
                    
        return predictions


class AdaBoostClassifierCustom:
    """
    A custom implementation of the AdaBoost (Adaptive Boosting) algorithm.
    
    Beginner Explanation:
    Imagine a team of doctors diagnosing a rare disease. The first doctor makes some mistakes.
    The second doctor pays extra attention to the patients the first doctor misdiagnosed.
    The third pays attention to the second's mistakes, and so on. Finally, they vote,
    but the doctors who are generally more accurate get more say in the final decision.
    
    Technical Explanation:
    AdaBoost fits a sequence of weak learners (Decision Stumps here) on repeatedly
    modified versions of the data. The data modifications at each so-called boosting
    iteration consist of applying weights to each of the training samples. Initially,
    all weights are equal. For each successive iteration, the sample weights are individually
    modified and the learning algorithm is reapplied to the reweighted data. At a given step,
    those training examples that were incorrectly predicted by the boosted model induced at the
    previous step have their weights increased, whereas the weights are decreased for those
    that were predicted correctly.
    """
    
    def __init__(self, n_clf: int = 5) -> None:
        """
        Args:
            n_clf: Number of weak classifiers (stumps) to use.
        """
        self.n_clf = n_clf
        self.clfs: List[DecisionStump] = []

    def fit(self, X: List[List[float]], y: List[int]) -> None:
        """
        Fits the AdaBoost ensemble to the training data.
        
        Args:
            X: Training features.
            y: Training labels (+1 or -1).
        """
        n_samples, n_features = len(X), len(X[0])
        
        # Initialize weights to 1/N
        w = [1.0 / n_samples for _ in range(n_samples)]
        
        self.clfs = []
        for _ in range(self.n_clf):
            clf = DecisionStump()
            min_error = float('inf')
            
            # Find the best stump
            for feature_i in range(n_features):
                feature_values = [sample[feature_i] for sample in X]
                unique_values = set(feature_values)
                
                for threshold in unique_values:
                    # Test both polarities
                    for polarity in [1, -1]:
                        predictions = [1] * n_samples
                        for i in range(n_samples):
                            if polarity == 1:
                                if X[i][feature_i] < threshold:
                                    predictions[i] = -1
                            else:
                                if X[i][feature_i] > threshold:
                                    predictions[i] = -1
                        
                        # Calculate error
                        error = sum(w[i] for i in range(n_samples) if predictions[i] != y[i])
                        
                        if error < min_error:
                            clf.polarity = polarity
                            clf.threshold = threshold
                            clf.feature_index = feature_i
                            min_error = error
                            
            # Calculate alpha (weight of this classifier)
            # Add small epsilon to avoid division by zero
            EPS = 1e-10
            clf.alpha = 0.5 * math.log((1.0 - min_error + EPS) / (min_error + EPS))
            
            # Update sample weights
            predictions = clf.predict(X)
            for i in range(n_samples):
                w[i] *= math.exp(-clf.alpha * y[i] * predictions[i])
                
            # Normalize weights
            w_sum = sum(w)
            w = [weight / w_sum for weight in w]
            
            self.clfs.append(clf)

    def predict(self, X: List[List[float]]) -> List[int]:
        """
        Predicts labels for the input data using the weighted ensemble.
        """
        n_samples = len(X)
        clf_preds = [clf.alpha * float(pred) for clf in self.clfs for pred in clf.predict(X)]
        
        # Aggregate predictions
        y_pred = [0.0] * n_samples
        for clf in self.clfs:
            preds = clf.predict(X)
            for i in range(n_samples):
                y_pred[i] += clf.alpha * preds[i]
                
        # Return sign of aggregate prediction
        return [1 if p >= 0 else -1 for p in y_pred]


# =====================================================================
# Tests simulating advanced ML workflows
# =====================================================================

def generate_dummy_data(n_samples: int = 100) -> Tuple[List[List[float]], List[int]]:
    """Generates simple binary classification data."""
    X = []
    y = []
    for _ in range(n_samples):
        # Feature 1 and Feature 2
        f1 = random.uniform(0, 10)
        f2 = random.uniform(0, 10)
        X.append([f1, f2])
        # Simple non-linear boundary: y=1 if f1+f2 > 10 else -1
        if f1 + f2 > 10:
            y.append(1)
        else:
            y.append(-1)
    return X, y

def test_adaboost() -> None:
    """Tests the custom AdaBoost implementation."""
    print("Running AdaBoost Test...")
    X, y = generate_dummy_data(200)
    
    # Train-test split (80/20)
    split_idx = int(0.8 * len(X))
    X_train, y_train = X[:split_idx], y[:split_idx]
    X_test, y_test = X[split_idx:], y[split_idx:]
    
    # Train model
    clf = AdaBoostClassifierCustom(n_clf=10)
    clf.fit(X_train, y_train)
    
    # Evaluate
    predictions = clf.predict(X_test)
    accuracy = sum(1 for p, t in zip(predictions, y_test) if p == t) / len(y_test)
    
    print(f"Test Accuracy: {accuracy * 100:.2f}%")
    assert accuracy > 0.7, "Model accuracy is unexpectedly low."
    print("AdaBoost Test Passed!")

if __name__ == "__main__":
    test_adaboost()
    print("All advanced ML module tests passed successfully.")
