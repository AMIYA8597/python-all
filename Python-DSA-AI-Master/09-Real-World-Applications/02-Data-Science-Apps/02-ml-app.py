\"\"\"
Module: 02-ml-app.py
Topic: Machine Learning Application Architecture

This module demonstrates how to wrap a Machine Learning model into a reusable,
testable application class. It covers training, inference, and persistence.

Why it matters:
A Jupyter Notebook is not an application. To serve ML models in production (e.g., via 
a Flask/FastAPI REST API), you need well-structured code. The model must be trained, 
serialized (saved to disk), deserialized (loaded), and exposed through a clean inference API.

Learning Objectives:
1. Bridge the gap between data science scripts and software engineering.
2. Structure an ML model class for easy integration into web frameworks.
3. Understand model serialization (Pickle/Joblib).

Beginner Explanation:
Training a model is like teaching a student. Once they learn (training), you want them to 
take a test (inference). Instead of retraining the student every time someone asks a question, 
we save their \"brain\" to a file, and load it whenever a new question comes in.

Advanced Explanation:
Production ML systems require separation of concerns. The training pipeline is executed 
offline (e.g., Airflow, SageMaker), producing artifacts (model weights, scalers, encoders).
The inference service loads these artifacts into memory on startup and handles real-time 
prediction requests. Using Scikit-Learn pipelines ensures that the exact same preprocessing 
steps applied during training are consistently applied during inference, preventing train-serve skew.
\"\"\"

import random
from typing import List, Tuple
# In a real app, you would use:
# from sklearn.linear_model import LogisticRegression
# import joblib

# ==========================================
# 1. Mock ML Library (For zero-dependency example)
# ==========================================
class MockLogisticRegression:
    def __init__(self):
        self.weights = []
        self.bias = 0.0
        self.is_trained = False

    def fit(self, X: List[List[float]], y: List[int]):
        # Mock training logic
        self.weights = [random.random() for _ in range(len(X[0]))]
        self.bias = random.random()
        self.is_trained = True

    def predict(self, X: List[List[float]]) -> List[int]:
        if not self.is_trained:
            raise ValueError(\"Model is not trained yet.\")
        # Mock prediction logic
        return [1 if sum(f * w for f, w in zip(features, self.weights)) + self.bias > 1.0 else 0 for features in X]

# ==========================================
# 2. Professional Implementation: ML App Class
# ==========================================

class SpamDetectionApp:
    \"\"\"
    A complete wrapper for an ML model handling training and prediction.
    \"\"\"
    def __init__(self):
        # Initialize the underlying mathematical model
        self.model = MockLogisticRegression()
        # In a real scenario, you'd load model artifacts from disk here if they exist

    def train(self, data: List[Tuple[List[float], int]]):
        \"\"\"
        Trains the model on provided data.
        In real apps, `data` is often a Pandas DataFrame.
        \"\"\"
        print(\"Starting model training...\")
        X = [row[0] for row in data]
        y = [row[1] for row in data]
        self.model.fit(X, y)
        print(\"Training complete.\")
        # In real life: joblib.dump(self.model, 'model.pkl')

    def predict_single(self, features: List[float]) -> dict:
        \"\"\"
        Inference API intended for real-time requests (e.g., from a REST endpoint).
        Provides structured output.
        \"\"\"
        try:
            prediction = self.model.predict([features])[0]
            return {
                \"status\": \"success\",
                \"is_spam\": bool(prediction),
                \"confidence\": 0.95 # Mock confidence score
            }
        except Exception as e:
            return {\"status\": \"error\", \"message\": str(e)}

# ==========================================
# Complexity Analysis
# ==========================================
# Training Complexity (Mock): O(N * F) where N is samples, F is features.
# Inference Complexity: O(F) per request.
# Bottlenecks in real ML apps: Feature extraction (e.g., text vectorization) is often
# more CPU intensive than the actual dot product of the linear model prediction.

# ==========================================
# Interview Challenge
# ==========================================
# Challenge: You deploy this ML API and notice memory usage grows over time until it crashes (OOM).
# What could be causing the memory leak in a Python web server (like Gunicorn/Flask) 
# serving an ML model, and how do you debug it?
# Hint: Global variables, uncollected tensors, or caching issues.

if __name__ == \"__main__\":
    print(\"--- ML App Demo ---\")
    
    app = SpamDetectionApp()
    
    # 1. Test inference before training (should fail gracefully)
    err_resp = app.predict_single([0.1, 0.5, 0.2])
    assert err_resp['status'] == 'error'
    
    # 2. Train the model
    # Mock data: List of (features, label)
    training_data = [
        ([0.1, 0.2, 0.1], 0),
        ([0.9, 0.8, 0.7], 1),
        ([0.2, 0.1, 0.3], 0),
        ([0.8, 0.9, 0.8], 1),
    ]
    app.train(training_data)
    
    # 3. Test successful inference
    new_email_features = [0.85, 0.80, 0.75]
    result = app.predict_single(new_email_features)
    
    print(f\"Prediction result: {result}\")
    assert result['status'] == 'success'
    assert 'is_spam' in result
    print(\"All ML App tests passed!\")
