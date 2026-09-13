"""
## A. Concept Name
FastAPI Deployment

## B. Concept Explanation
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints. This module demonstrates a basic deployment setup for an ML model or generic API using FastAPI.

## C. Prerequisites
- Python 3.7+
- fastapi
- uvicorn

## D. Use Cases
- Serving Machine Learning models.
- Building RESTful APIs.
- Microservices.

## E. Code Implementation
See the implementation details below this docstring.

## F. Key Takeaways
- FastAPI provides automatic interactive API documentation (Swagger UI).
- `uvicorn` is used as the ASGI server to run the application.
- API endpoints are defined using decorators like `@app.get` or `@app.post`.

## X. Project Connection
This basic FastAPI setup serves as the foundation for more complex MLOps pipelines where models are deployed and consumed via REST APIs.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Initialize the FastAPI application
app = FastAPI(title="Basic FastAPI Deployment API", version="1.0.0")

# Define input schema
class PredictionRequest(BaseModel):
    feature_1: float
    feature_2: float

# Define output schema
class PredictionResponse(BaseModel):
    prediction: float

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to the basic FastAPI deployment API!"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Dummy prediction endpoint.
    In a real scenario, this would load an ML model and generate predictions.
    """
    prediction = request.feature_1 * 0.5 + request.feature_2 * 0.5
    return PredictionResponse(prediction=prediction)

if __name__ == "__main__":
    # Run the application using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
