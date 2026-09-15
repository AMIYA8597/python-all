"""
# ==============================================================================
# LABORATORY: MLOPS (EXPERIMENT TRACKING WITH MLFLOW)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior Data Scientist trains 50 different Random Forest models on their 
# laptop over 3 weeks. They try to remember which hyperparameter combination 
# produced the 94% accuracy. They check their notebook: `model_final_v3_really_final.pkl`. 
# They deploy it to production. It has 60% accuracy. They lost the good model.
#
# A senior AI engineer understands "MLOps" (Machine Learning Operations). They 
# never rely on memory. They wrap their training loop in `mlflow`. Every single 
# hyperparameter (n_estimators, max_depth), every metric (accuracy, precision), 
# and the physical Model Artifact itself is automatically serialized and logged 
# to a centralized Tracking Server. When they need to deploy the 94% model, they 
# query the server, pull the exact artifact, and deploy it with total cryptographic 
# certainty.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Experiment Tracking architecture.
# - Execute MLflow parameter and metric logging.
# - Architect Model Artifact serialization (Model Registry).
#
# ==============================================================================
"""

import time
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (MLFLOW SIMULATOR)
# ==============================================================================
class MockMLflowClient:
    """Simulates the MLflow Tracking Server API."""
    
    def __init__(self):
        self.experiments = []
        self.current_run = None
        
    def start_run(self, run_name: str):
        print(f"\n  [MLFLOW] Starting Run: '{run_name}'")
        self.current_run = {
            "name": run_name,
            "params": {},
            "metrics": {},
            "artifacts": []
        }
        
    def log_param(self, key: str, value: any):
        print(f"  -> Logging Parameter: {key} = {value}")
        self.current_run["params"][key] = value
        
    def log_metric(self, key: str, value: float):
        print(f"  -> Logging Metric: {key} = {value:.4f}")
        self.current_run["metrics"][key] = value
        
    def log_model(self, model_name: str):
        print(f"  -> Serializing & Logging Model Artifact: '{model_name}.pkl'")
        self.current_run["artifacts"].append(f"{model_name}.pkl")
        
    def end_run(self):
        print("  [MLFLOW] Ending Run and flushing to Tracking Server.")
        self.experiments.append(self.current_run)
        self.current_run = None


class ModelTrainingPipeline:
    
    def __init__(self):
        self.mlflow = MockMLflowClient()
        
    def train_model(self, run_name: str, n_estimators: int, max_depth: int):
        """
        [SECURE] MLOps Training Loop.
        Notice how MLflow wraps the entire execution block!
        """
        self.mlflow.start_run(run_name)
        
        # 1. Log the configuration BEFORE training starts
        self.mlflow.log_param("n_estimators", n_estimators)
        self.mlflow.log_param("max_depth", max_depth)
        
        print(f"\n     [GPU] Training Random Forest with {n_estimators} trees...")
        time.sleep(0.5)
        
        # 2. Simulate mathematical training results
        # We simulate that higher depth gives better accuracy for this specific dataset
        base_accuracy = 0.70
        accuracy = base_accuracy + (max_depth * 0.02) + (random.uniform(-0.01, 0.01))
        loss = 1.0 - accuracy
        
        # 3. Log the final metrics
        print("     [GPU] Training Complete.")
        self.mlflow.log_metric("accuracy", accuracy)
        self.mlflow.log_metric("loss", loss)
        
        # 4. Serialize the Model to the Registry
        self.mlflow.log_model(f"rf_model_{run_name}")
        
        self.mlflow.end_run()


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_experiment_tracking():
    section_header("MLOps: MLflow Experiment Tracking")
    
    pipeline = ModelTrainingPipeline()
    
    # Run 1: Shallow Trees
    pipeline.train_model(run_name="Experiment_Alpha", n_estimators=50, max_depth=3)
    
    # Run 2: Deep Trees
    pipeline.train_model(run_name="Experiment_Beta", n_estimators=100, max_depth=10)
    
    print("\n  [TRACKING SERVER DASHBOARD]")
    for exp in pipeline.mlflow.experiments:
        print(f"  * Run: {exp['name']}")
        print(f"    - Params:  {exp['params']}")
        print(f"    - Metrics: {exp['metrics']}")
        print(f"    - Model:   {exp['artifacts'][0]}")
        
    print("\n  [FLAWLESS] The Senior Engineer can mathematically query the Tracking Server, ")
    print("  sort by 'metrics.accuracy DESC', and instantly retrieve the exact `.pkl` file ")
    print("  and Hyperparameters for Experiment_Beta to push into production.")


def run_all_labs():
    demonstrate_experiment_tracking()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we use an MLOps platform like MLflow instead of just writing metrics to a CSV file and saving `.pkl` files to a local folder?"
   Senior Answer: "Artifact Lineage and Reproducibility. A CSV file does not mathematically link a specific accuracy score to a physical model artifact. If you have 500 models in a folder, and a CSV with 500 rows, you rely entirely on naming conventions to connect them, which inevitably fails. MLflow establishes a cryptographic Hash (Run ID) that permanently binds the Hyperparameters, the Git Commit Hash of the code, the Accuracy Metric, and the physical `.pkl` binary artifact into a single, immutable database entry. This guarantees $100\\%$ reproducibility for audits and production deployments."

2. Interviewer: "What is the architectural difference between the MLflow 'Tracking Server' and the 'Model Registry'?"
   Senior Answer: "Experimentation vs Production Lifecycle. The Tracking Server is a massive mathematical dump. It holds the logs of all $5,000$ experimental runs the Data Science team executes, including the absolute failures. Once a model achieves a mathematically acceptable accuracy (e.g., $95\\%$), the Engineer manually promotes that specific artifact from the Tracking Server into the Model Registry. The Registry is a strict, version-controlled repository (like Git for Models). It manages the lifecycle state transitions: `Staging` -> `Production` -> `Archived`. CI/CD pipelines physically pull from the Registry, never from the Tracking Server."

3. Interviewer: "In an enterprise MLOps architecture, where are the physical heavy Model Artifacts (e.g., 5GB weights) actually stored?"
   Senior Answer: "External Blob Storage. The MLflow architecture is split into two physical data stores. The Backend Store (usually a PostgreSQL database) stores the lightweight metadata: parameters, metrics, tags, and Run IDs. The Artifact Store (usually AWS S3, Google Cloud Storage, or Azure Blob) stores the massive physical binary files (the weights, `.pkl` files, and tensorboard logs). MLflow PostgreSQL simply stores an `s3://` URI pointer mathematically linking the metadata row to the cloud storage bucket."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: MLOps (MLflow Experiment Tracking) Completed.")
