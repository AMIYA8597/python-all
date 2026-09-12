"""
MLOps Foundations: Experiment Tracking with MLflow

This script demonstrates how to use MLflow to track a machine learning experiment.
It trains a simple Random Forest model on the Iris dataset, logs hyperparameters,
metrics, and the trained model itself.

Prerequisites:
    pip install mlflow scikit-learn pandas
"""

import os
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

def load_data():
    """Load and prepare the Iris dataset."""
    print("Loading data...")
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name="target")
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_log_model(n_estimators: int, max_depth: int):
    """Train a Random Forest model and log it with MLflow."""
    X_train, X_test, y_train, y_test = load_data()

    # Set up MLflow tracking
    # mlflow.set_tracking_uri("http://localhost:5000") # Uncomment if using a remote server
    mlflow.set_experiment("Iris_Classification_Experiment")

    print(f"Training model with n_estimators={n_estimators}, max_depth={max_depth}...")

    # Start an MLflow run
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", 42)

        # Train model
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )
        model.fit(X_train, y_train)

        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="macro")
        recall = recall_score(y_test, y_pred, average="macro")

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)

        # Log the model
        mlflow.sklearn.log_model(model, "random_forest_model")

        print(f"Run completed. Accuracy: {accuracy:.4f}")
        print(f"Run ID: {mlflow.active_run().info.run_id}")

if __name__ == "__main__":
    # Example runs with different hyperparameters
    train_and_log_model(n_estimators=50, max_depth=3)
    train_and_log_model(n_estimators=100, max_depth=5)
    train_and_log_model(n_estimators=150, max_depth=10)
    
    print("\nTo view the MLflow UI, run the following command in your terminal:")
    print("mlflow ui")
