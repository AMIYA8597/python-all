"""
# ==============================================================================
# LABORATORY: MLOps (DEPLOYMENT, SERIALIZATION, & DRIFT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A Jupyter Notebook with a 99% accuracy model provides zero business value.
# The value is only generated when that model is deployed to a Web Server 
# (e.g., FastAPI, AWS SageMaker) and generates live predictions for millions 
# of incoming users in milliseconds.
#
# The bridge between "Data Science" (Jupyter) and "Software Engineering" (AWS) 
# is called MLOps (Machine Learning Operations).
#
# You must know how to:
# 1. Serialize (Save) the trained mathematical weights to a physical file.
# 2. Deserialize (Load) the weights on a remote production server.
# 3. Monitor the model for "Data Drift" (The real world changing over time, 
#    rendering your static mathematical model obsolete).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master model Serialization using `joblib` for Scikit-Learn.
# - Understand the difference between Pickle and Joblib.
# - Understand Concept Drift and Data Drift monitoring.
#
# ==============================================================================
"""

import numpy as np
import os
import time

# In a real environment: pip install scikit-learn joblib
try:
    from sklearn.datasets import make_classification
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SERIALIZATION (SAVING TO DISK)
# ==============================================================================
def demonstrate_serialization():
    section_header("Model Serialization (Joblib)")
    
    if not HAS_JOBLIB:
        print("[WARNING] Joblib or Scikit-Learn not installed.")
        return
        
    print("When a model finishes `model.fit()`, the calculated weights only ")
    print("exist in volatile RAM. If the python script closes, the brain dies.")
    print("We must serialize the Python Object into a physical file on the hard drive.\n")
    
    # Train a model
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # 1. SAVE THE MODEL
    # Python has a built-in `pickle` module, but Scikit-Learn heavily recommends 
    # using `joblib`. Joblib is explicitly optimized for saving massive NumPy 
    # matrices extremely quickly.
    
    filename = "production_rf_model.pkl"
    joblib.dump(model, filename)
    
    print(f"Model successfully trained and saved to: {filename}")
    
    # Check the file size
    file_size_kb = os.path.getsize(filename) / 1024
    print(f"Physical File Size: {file_size_kb:.1f} KB")


# ==============================================================================
# 4. DESERIALIZATION (PRODUCTION SERVER)
# ==============================================================================
def demonstrate_deserialization():
    section_header("Deserialization (Loading on the Web Server)")
    
    if not HAS_JOBLIB: return
    
    filename = "production_rf_model.pkl"
    if not os.path.exists(filename):
        print("Model file not found. Run serialization first.")
        return
        
    print("Imagine this code is running on an AWS EC2 instance responding to ")
    print("live API requests (FastAPI / Flask). It does NOT call `.fit()`!\n")
    
    # 1. LOAD THE MODEL INTO RAM
    # In a real web server, you do this exactly ONCE when the server boots up.
    print("Server Booting... Loading AI Model into RAM...")
    start = time.perf_counter()
    loaded_model = joblib.load(filename)
    load_time = time.perf_counter() - start
    
    print(f"Model loaded in {load_time*1000:.2f} ms!")
    
    # 2. GENERATE PREDICTION FOR INCOMING API REQUEST
    # The server receives a JSON payload, converts it to a NumPy array...
    user_payload = np.random.rand(1, 20)
    
    start = time.perf_counter()
    prediction = loaded_model.predict(user_payload)
    pred_time = time.perf_counter() - start
    
    print(f"Live Prediction generated: Class {prediction[0]}")
    print(f"Inference Time: {pred_time*1000:.2f} ms (Ultra-fast for production!)")
    
    # Clean up the artifact
    if os.path.exists(filename):
        os.remove(filename)


# ==============================================================================
# 5. DATA DRIFT & CONCEPT DRIFT
# ==============================================================================
def demonstrate_drift():
    section_header("MLOps Monitoring: Data Drift")
    
    print("Machine Learning models do not age like fine wine. They degrade.")
    print("If you trained a model in 2019 to predict House Prices based on ")
    print("historical data, and deploy it in 2021... the 2021 COVID housing ")
    print("boom will make your model mathematically obsolete. It will drastically ")
    print("underprice every house.")
    
    print("\nTypes of Drift:")
    print("1. DATA DRIFT (Feature Drift): The distribution of the input X changes.")
    print("   Example: You trained a facial recognition model mostly on adults. ")
    print("   Suddenly, a new app trend causes millions of teenagers to upload ")
    print("   photos. The statistical distribution of the 'Age' feature has drifted.")
    
    print("2. CONCEPT DRIFT (Model Decay): The actual mathematical relationship ")
    print("   between X and y changes.")
    print("   Example: Spam filter. Hackers invent a completely new way to format ")
    print("   spam emails. The definition (Concept) of Spam has fundamentally ")
    print("   changed. Your model is instantly blind to it.")
    
    print("\nMLOps Solution:")
    print("Use tools like 'Evidently AI' or 'AWS SageMaker Model Monitor' to ")
    print("continuously track the statistical distributions of incoming live data.")
    print("If the Kolmogorov-Smirnov (KS) test proves the live data no longer ")
    print("matches the 2019 training data, trigger an automated CI/CD pipeline ")
    print("to retrain the model on fresh data!")


def run_all_labs():
    demonstrate_serialization()
    demonstrate_deserialization()
    demonstrate_drift()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Scikit-Learn strongly recommend `joblib` over the standard Python `pickle` module for saving models?
   Answer: Machine Learning models (especially Random Forests and KNNs) are backed by absolutely massive underlying NumPy matrices and arrays representing the weights and data. The standard `pickle` library is designed for general Python objects (dicts, lists) and is extremely slow and memory-inefficient when serializing large C-based NumPy arrays. `joblib` is a specialized library specifically engineered by the Scientific Python community to serialize and memory-map massive NumPy matrices to disk at maximum speed.

2. A model that predicted user purchasing behavior with 92% accuracy in January drops to 71% accuracy in December. Code hasn't changed. What happened?
   Answer: Concept Drift. The underlying relationship between the features ($X$) and the target ($y$) has fundamentally changed. A user's purchasing behavior in December is dominated by holiday shopping, gift-buying, and seasonal discounts. The mathematical rules the model learned in January are completely invalid for December. The MLOps solution is to implement an automated retraining pipeline that periodically updates the model weights using the most recent 30 days of rolling data.

3. Why MUST you save the `StandardScaler` (or `ColumnTransformer`) alongside the Model itself?
   Answer: If you train a model on $X$ data that has been scaled (Mean=0, Variance=1), the model's weights are mathematically calibrated to expect small floating-point numbers between -3.0 and 3.0. If you only deploy the Model to the web server, and a user inputs their raw Salary as `$95,000`, the model will receive the massive number `95000` and generate a catastrophic, wildly incorrect prediction. You must save the exact `StandardScaler` object that was fitted during training, load it onto the web server, and call `.transform(user_data)` BEFORE passing the data to the model. Best practice is to bind them together in a Scikit-Learn `Pipeline` and save the single Pipeline object!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: MLOps & Model Deployment Completed.")
