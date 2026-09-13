"""
Model Serving & APIs with FastAPI

This script demonstrates how to serve a Machine Learning model using FastAPI.
We create a REST API that accepts input data and returns predictions.

Prerequisites:
    pip install fastapi uvicorn scikit-learn pydantic numpy
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import uvicorn
import pickle
import os

# Define the request body schema
class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Initialize FastAPI app
app = FastAPI(
    title="Iris Flower Classification API",
    description="An API that predicts the species of an Iris flower based on its features.",
    version="1.0.0"
)

# Global variable to hold our model
model = None

# Mock function to simulate loading a model. 
# In reality, you'd load a .pkl file or from MLflow.
def load_or_train_model():
    model_path = "iris_model.pkl"
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    else:
        print("Training model for the first time...")
        iris = load_iris()
        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(iris.data, iris.target)
        with open(model_path, "wb") as f:
            pickle.dump(clf, f)
        return clf

@app.on_event("startup")
def startup_event():
    """Load the model when the application starts."""
    global model
    model = load_or_train_model()
    print("Model loaded successfully!")

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Iris Classification API is running."}

@app.post("/predict")
def predict(features: IrisFeatures):
    """
    Endpoint to make predictions.
    Expects a JSON payload matching the IrisFeatures schema.
    """
    try:
        # Extract features into a format the model expects
        data = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Make prediction
        prediction = model.predict(data)[0]
        
        # Map prediction to class name
        target_names = ["setosa", "versicolor", "virginica"]
        predicted_class = target_names[prediction]
        
        return {
            "prediction": int(prediction),
            "species": predicted_class
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("To test the API, open http://127.0.0.1:8000/docs in your browser.")
    uvicorn.run("02_fastapi_serving:app", host="127.0.0.1", port=8000, reload=True)
