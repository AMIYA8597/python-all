# MLOps Foundations & MLflow

## 1. Introduction and Industry Use Cases

### What is MLOps?
Machine Learning Operations (MLOps) is the set of practices that aims to deploy and maintain machine learning models in production reliably and efficiently. It sits at the intersection of Machine Learning, DevOps, and Data Engineering.

### What is MLflow?
MLflow is an open-source platform developed by Databricks for managing the end-to-end machine learning lifecycle. It tackles the challenges of tracking experiments, packaging code into reproducible runs, and sharing and deploying models.

### Industry Use Cases
- **Experiment Tracking:** Data scientists run hundreds of experiments with different hyperparameters. MLflow logs all these parameters, metrics (like accuracy or RMSE), and artifacts (like plots or model weights) in a centralized dashboard.
- **Model Registry:** A central repository to manage the lifecycle of an ML model (e.g., transitioning a model from "Staging" to "Production").
- **Reproducibility:** Packaging training code and environment dependencies so anyone on the team can rerun the code and get the same results.

## 2. Beginner Explanation

Imagine baking a cake. You try 50 different recipes (experiments), changing the amount of sugar, flour, and baking time (hyperparameters). Without a notebook (MLflow), you'll forget which combination made the best cake (model). MLflow is your digital notebook that records exactly what went into every cake and how good it tasted (metrics). Once you find the best recipe, MLflow helps you package it and put it on the menu (deployment).

## 3. Deep Technical Explanation & Architectures

### The 4 Pillars of MLflow
1. **MLflow Tracking:** An API and UI for logging parameters, code versions, metrics, and output files when running ML code.
2. **MLflow Projects:** A standard format for packaging reusable data science code (using conda/docker environments).
3. **MLflow Models:** A standard format for packaging machine learning models that can be used in a variety of downstream tools (e.g., real-time serving through a REST API, or batch inference on Apache Spark).
4. **MLflow Model Registry:** A centralized model store, set of APIs, and UI, to collaboratively manage the full lifecycle of an MLflow Model.

### MLOps Architecture Lifecycle
Data Ingestion -> Data Preprocessing -> Model Training (Tracked via MLflow) -> Model Evaluation -> Model Registration (MLflow Registry) -> CI/CD Deployment -> Monitoring (Data drift, model decay).

## 4. Practical Python Example (MLflow Tracking)

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

# Generate dummy data
X = np.random.rand(100, 5)
y = X[:, 0] * 3 + np.random.rand(100)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Set the experiment name
mlflow.set_experiment("Random_Forest_Experiments")

def train_model(n_estimators, max_depth):
    # Start an MLflow run
    with mlflow.start_run():
        # 1. Log parameters
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        
        # Train model
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth)
        model.fit(X_train, y_train)
        
        # Predict and calculate metrics
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        
        # 2. Log metrics
        mlflow.log_metric("mse", mse)
        
        # 3. Log model artifact
        mlflow.sklearn.log_model(model, "random_forest_model")
        
        print(f"Run config: estimators={n_estimators}, depth={max_depth} | MSE={mse:.4f}")

# Run experiments
train_model(50, 5)
train_model(100, 10)
train_model(200, None)
```

## 5. Advanced Concepts and Internal Details

### Autologging
Instead of manually logging parameters and metrics, MLflow provides `mlflow.autolog()`. For supported libraries (Scikit-learn, XGBoost, PyTorch, TensorFlow), MLflow will automatically capture all hyperparameters, training metrics, and model artifacts without writing specific log statements.

### Model Signatures
When logging a model, it is best practice to include a model signature. A signature defines the schema of the model's inputs and outputs (e.g., column names and data types). This is crucial for downstream deployment tools to validate incoming inference requests.

## 6. Common Mistakes and Performance Considerations
- **Bloated Artifact Storage:** Logging massive datasets or unnecessary files as artifacts can fill up storage quickly. Keep artifacts limited to essential plots and model weights.
- **Ignoring Environments:** Failing to log `conda.yaml` or `requirements.txt` with the model makes reproducibility impossible. MLflow logs this by default with `log_model`, do not bypass it.
- **Production Database:** By default, MLflow logs to a local `./mlruns` directory. For production, configure MLflow to use a remote tracking server backed by a relational database (PostgreSQL/MySQL) for metadata and cloud storage (S3/GCS/Azure Blob) for artifacts.

## 7. Interview Questions and Exercises

### Interview Questions
1. **Q:** What is model drift, and how does MLOps help manage it?
   **A:** Model drift occurs when the statistical properties of the target variable or input features change over time, degrading model performance. MLOps systems include monitoring components to detect this drift and trigger automated retraining pipelines to update the model.
2. **Q:** Explain the purpose of the MLflow Model Registry.
   **A:** It acts as a central repository to manage the lifecycle of models, providing lineage, versioning, stage transitions (Staging -> Production), and annotations. It helps teams collaborate and know exactly which model version is deployed where.
3. **Q:** How do you serve an MLflow model as a REST API?
   **A:** You can use the MLflow CLI command `mlflow models serve -m <model_uri> -p 5000`. This spins up a local Flask/Gunicorn server hosting the model.

### Practical Exercise
**Experiment Pipeline:** 
1. Train a Logistic Regression and an XGBoost model on the Iris dataset. 
2. Use MLflow to track both experiments. 
3. Register the model with the highest accuracy in the MLflow Model Registry.
4. Transition the best model to the "Production" stage via the MLflow API.
