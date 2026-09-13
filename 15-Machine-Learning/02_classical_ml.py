"""
# Classical Machine Learning: The Foundation of AI

## A. Concept Name
Classical Machine Learning (Linear Regression, Logistic Regression, Decision Trees)

## B. One-Sentence Definition
Classical Machine Learning involves algorithms that learn patterns from structured data using statistical and mathematical optimization, rather than relying on deep neural networks.

## C. Why Does This Exist? (What problem does it solve?)
Before Deep Learning, we still needed systems to make predictions (e.g., house prices) and classifications (e.g., spam vs. not spam). Classical ML solves these problems with high interpretability, low computational cost, and excellent performance on tabular data.

## D. Intuition & Real-Life Analogy
Imagine trying to draw a straight line through a scatter plot of house sizes vs. prices. 
- **Linear Regression** is you adjusting the ruler until the line fits the dots best.
- **Logistic Regression** is you drawing a line to separate red dots (spam) from blue dots (not spam).
- **Decision Trees** are like a flowchart or a game of "20 Questions" (e.g., "Is size > 2000 sqft? Yes -> Is location = City? No -> Price = $300k").

## E. Mental Model
```text
Data (X) + Labels (y)  ---> [ ML ALGORITHM ] ---> Trained Model
                                   | (Optimization / Loss Minimization)
New Data (X_new)       ---> [ TRAINED MODEL] ---> Predictions (y_pred)
```
Unlike traditional programming where you write the rules, in ML, you provide the answers and the data, and the algorithm *figures out the rules*.

## F. Formal Technical Explanation
- **Linear Regression:** Models the relationship between features and continuous target by fitting a linear equation. `y = w*x + b`. It minimizes the Mean Squared Error (MSE).
- **Logistic Regression:** Despite the name, it's for *classification*. It squashes the linear output through a Sigmoid function `1 / (1 + e^-z)` to output a probability between 0 and 1. It minimizes Log Loss (Cross-Entropy).
- **Decision Trees:** Recursively splits the data space into regions based on feature thresholds that maximize Information Gain (or minimize Gini Impurity).

## G. Mathematical Foundation
**Linear Regression Loss (MSE):**  
`J(w, b) = 1/N * sum( (y_actual - (w*x + b))^2 )`
To train the model, we use Calculus (Gradient Descent) to find the derivatives of J with respect to `w` and `b`, and update them to find the minimum error.

## H. Complexity Analysis
- **Decision Tree Training Time:** O(N * M * log N) where N is samples, M is features.
- **Linear Regression Inference Time:** O(M) (Just a dot product of weights and features). Extremely fast.

## I. Common Mistakes & Pitfalls
- **Feature Scaling:** Linear models (especially with regularization like Ridge/Lasso) require features to be scaled (e.g., StandardScaler). Decision Trees do *not* care about scaling.
- **Overfitting Trees:** A Decision Tree with no `max_depth` will grow until every leaf has 1 sample. It will memorize the training data and fail on new data (Overfitting).

## J. Common Confusions
- *Linear vs Logistic:* Linear outputs a continuous number (Price: $150,000). Logistic outputs a probability (Probability of Spam: 0.85), which is then mapped to a class (Spam).
- *Parameter vs Hyperparameter:* Parameters (`w`, `b`) are learned by the algorithm during training. Hyperparameters (`max_depth` in trees, `learning_rate`) are set by YOU before training.

## K. When To Use It
- Linear/Logistic Regression: When you need a simple, extremely fast, highly interpretable baseline.
- Decision Trees: When you have non-linear tabular data and you need to easily explain *why* a decision was made to stakeholders.

## L. When NOT To Use It
- Do not use Classical ML for unstructured data (images, audio, raw text). Use Deep Learning.
- Do not use a single Decision Tree for highly critical predictions; they are unstable. Use Ensembles (Random Forests, XGBoost).

## M. Trade-offs
- **Interpretability vs Performance:** Linear models are highly interpretable but struggle with complex patterns. Deep learning is a black box but handles complex patterns.

## N. Debugging Tips
- `ValueError: Expected 2D array, got 1D array instead`: Scikit-learn expects X to be a matrix (rows=samples, cols=features). If you have one feature, use `X.reshape(-1, 1)`.
- Model has 99% accuracy on train, 50% on test: You are severely overfitting. Limit `max_depth` or use regularization.

## O. Memory Hook
"Linear predicts the amount. Logistic predicts the category. Trees ask 20 questions."

## P. Active Recall Questions
1. Why is Logistic Regression used for classification if it has "regression" in the name?
2. How does a Decision Tree decide where to split the data?
3. What is the difference between a parameter and a hyperparameter?

## Q. Interview Questions & Answers
**Q: What does the 'fit' method actually do under the hood in Linear Regression?**
A: It calculates the optimal weights (`w`) and bias (`b`) that minimize a loss function (like Mean Squared Error) across the training dataset. This can be done via iterative optimization (Gradient Descent) or analytically via the Normal Equation.

## R. Project Connections
- **Finance:** Logistic regression is used as the baseline model for credit scoring.
- **E-commerce:** Linear regression predicts future inventory demand based on historical sales.
"""

import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score

# ==============================================================================
# 1. EDUCATIONAL FROM-SCRATCH IMPLEMENTATION (Linear Regression via Gradient Descent)
# ==============================================================================
class FromScratchLinearRegression:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        # Gradient Descent Optimization
        for _ in range(self.epochs):
            # y_pred = X.w + b
            y_predicted = np.dot(X, self.weights) + self.bias
            
            # Compute Gradients
            # dw = (1/N) * sum(2 * x_i * (y_pred_i - y_i))
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)

            # Update Parameters
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        return np.dot(X, self.weights) + self.bias

# ==============================================================================
# 2. INDUSTRY-STANDARD LIBRARY IMPLEMENTATION (Scikit-Learn)
# ==============================================================================
def run_sklearn_pipeline():
    print("\n--- Industry Standard: Scikit-Learn ---")
    
    # 1. Prepare Data
    X_reg, y_reg = make_regression(n_samples=200, n_features=1, noise=15, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    # 2. Train Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 3. Predict & Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Linear Regression MSE: {mse:.2f}")

    # Logistic Regression Example
    X_clf, y_clf = make_classification(n_samples=200, n_features=2, n_redundant=0, random_state=42)
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)
    
    clf = LogisticRegression()
    clf.fit(Xc_train, yc_train)
    acc = accuracy_score(yc_test, clf.predict(Xc_test))
    print(f"Logistic Regression Accuracy: {acc * 100:.2f}%")

# ==============================================================================
# 3. DELIBERATELY BUGGY IMPLEMENTATION
# ==============================================================================
def buggy_ml_pipeline():
    """
    BUGGY VERSION - Demonstrates Data Leakage
    """
    print("\n--- Buggy Pipeline (Data Leakage) ---")
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    
    # BUG: Normalizing the ENTIRE dataset before splitting.
    # The test set information (mean/std) "leaks" into the training set.
    # In reality, you must fit the scaler ONLY on X_train.
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X) # <-- LEAKAGE HERE
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    print("Model trained, but evaluation metrics are overly optimistic due to leakage!")

# ==============================================================================
# 4. TESTING & VALIDATION
# ==============================================================================
def run_tests():
    print("--- Running Tests ---")
    # Generate simple linear data: y = 2x + 1
    X = np.array([[1], [2], [3], [4]])
    y = np.array([3, 5, 7, 9])
    
    # Test Custom From-Scratch Model
    custom_model = FromScratchLinearRegression(learning_rate=0.05, epochs=500)
    custom_model.fit(X, y)
    
    # Predict for x = 5 (should be approx 11)
    pred = custom_model.predict(np.array([[5]]))
    
    # Assert prediction is very close to 11
    assert abs(pred[0] - 11.0) < 0.5, f"Custom model failed, predicted {pred[0]}"
    print("From-Scratch Gradient Descent passed!")

if __name__ == "__main__":
    run_tests()
    run_sklearn_pipeline()
    buggy_ml_pipeline()
