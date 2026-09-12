# Model Serving with FastAPI

## What is Model Serving?

Model serving is the phase in the machine learning lifecycle where a trained machine learning model is deployed into a production environment so that it can receive data, make predictions, and return results to users or other downstream services. It bridges the gap between data science (training models) and software engineering (using models in real-world applications).

## Why FastAPI for Model Serving?

FastAPI has become the industry standard for serving machine learning models in Python, largely replacing older frameworks like Flask or Django for this specific use case. Here is why:

1. **Performance**: Built on Starlette and Pydantic, it is one of the fastest Python frameworks available, rivaling Node.js and Go.
2. **Asynchronous by Default**: natively supports `async` and `await`, allowing high concurrency which is crucial for handling multiple I/O-bound requests simultaneously.
3. **Automatic Documentation**: Automatically generates interactive API documentation (Swagger UI and ReDoc) based on OpenAPI standards.
4. **Data Validation**: Uses Pydantic for strong typing and automatic data validation, ensuring that the API only accepts well-formed data, reducing the risk of runtime errors during inference.

## Beginner Explanation

Imagine you have trained an ML model that predicts house prices based on the number of bedrooms and square footage. In your Jupyter notebook, you just call `model.predict(data)`. But how does a web or mobile app use this? 

You need to wrap this `predict` function inside a web server. FastAPI acts as a "waiter" in a restaurant. When an app sends a request (the customer's order) with the house details, FastAPI takes the request, hands it to your ML model (the chef), waits for the prediction (the food), and then returns the result to the app.

## Deep Technical Explanation

In production, model serving is rarely just wrapping a `predict` function. It involves a complex architecture designed for scale, reliability, and low latency.

1. **Data Serialization/Deserialization**: Incoming JSON requests must be efficiently parsed into Python objects and then converted into the numerical formats (like NumPy arrays or PyTorch tensors) required by the model. Pydantic handles the JSON parsing, while custom data pipelines handle the tensor conversion.
2. **Batching**: Machine learning models (especially deep learning models running on GPUs) are highly optimized for batched inputs. A high-performance serving layer often implements dynamic batching, where incoming independent requests are aggregated over a small time window (e.g., 5-10ms), passed to the model as a single batch, and then the results are split and returned to the respective callers.
3. **Model State Management**: Models are large objects. They should be loaded into memory exactly once when the application starts, not per request. FastAPI handles this efficiently using its `lifespan` event handlers.
4. **Concurrency & Threading**: ML inference is CPU/GPU bound, while receiving HTTP requests is I/O bound. FastAPI's async capabilities handle the I/O, but CPU-bound inference should ideally be offloaded to a thread pool or a separate worker process to avoid blocking the event loop.

## Practical Real-World Example

Here is a robust example of serving a Scikit-Learn model using FastAPI, complete with Pydantic validation, startup events, and error handling.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

# 1. Define the Request Data Model using Pydantic
class HouseFeatures(BaseModel):
    bedrooms: int = Field(..., gt=0, description="Number of bedrooms")
    bathrooms: float = Field(..., gt=0, description="Number of bathrooms")
    sqft_living: int = Field(..., gt=0, description="Square footage of the living space")
    
    class Config:
        json_schema_extra = {
            "example": {
                "bedrooms": 3,
                "bathrooms": 2.0,
                "sqft_living": 1500
            }
        }

# Global variable to hold our model
ml_models = {}

# 2. Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model on startup
    # In reality, you'd load this from S3, GCP, or a local path
    try:
        # For demonstration, we assume 'model.pkl' exists
        # ml_models["house_pricer"] = joblib.load("model.pkl")
        
        # Mocking a loaded model for the example to run
        class MockModel:
            def predict(self, data):
                return data[:, 0] * 100000 + data[:, 2] * 200
        ml_models["house_pricer"] = MockModel()
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        
    yield # Application runs during this yield
    
    # Clean up on shutdown
    ml_models.clear()
    print("Model unloaded.")

# 3. Initialize FastAPI app
app = FastAPI(
    title="House Price Predictor API",
    description="An API to predict house prices using a trained ML model.",
    version="1.0.0",
    lifespan=lifespan
)

# 4. Define the prediction endpoint
@app.post("/predict", tags=["Inference"])
async def predict_price(features: HouseFeatures):
    model = ml_models.get("house_pricer")
    if model is None:
        raise HTTPException(status_code=503, detail="Model is currently unavailable")
        
    try:
        # Convert Pydantic object to NumPy array for the model
        input_data = np.array([[
            features.bedrooms, 
            features.bathrooms, 
            features.sqft_living
        ]])
        
        # Perform inference
        # NOTE: For deep learning models, you should run this in a threadpool 
        # using run_in_threadpool to avoid blocking the async event loop.
        prediction = model.predict(input_data)
        
        # Return the result
        return {
            "predicted_price": float(prediction[0]),
            "currency": "USD"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "model_loaded": "house_pricer" in ml_models}

```

## Production Deployment Architecture

When deploying FastAPI in production, you never run the raw python script. The standard architecture involves:

1. **Uvicorn (ASGI Server)**: Translates HTTP requests into standard Python asynchronous calls.
2. **Gunicorn (Process Manager)**: Runs multiple Uvicorn worker processes to utilize multi-core CPUs.
   - Command: `gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py main:app`
3. **Docker**: Containerizes the application along with system dependencies (like C++ libraries for ML).
4. **Load Balancer (Nginx/Envoy)**: Distributes incoming traffic across multiple Docker containers.

## Common Mistakes & Performance Considerations

1. **Blocking the Event Loop**: The most common mistake in FastAPI ML serving. ML inference (e.g., `model.predict()`) is heavily CPU-bound. If called directly inside an `async def` function, it halts the entire event loop, preventing FastAPI from processing other incoming requests. 
   - *Fix*: Use `def` instead of `async def` for CPU-bound endpoints (FastAPI automatically runs these in an external threadpool), or use `starlette.concurrency.run_in_threadpool`.
2. **Loading Model per Request**: Instantiating the model inside the endpoint function destroys performance. 
   - *Fix*: Always load models at startup via `lifespan`.
3. **Memory Leaks**: Deep learning frameworks like TensorFlow and PyTorch can hold onto GPU memory aggressively. Ensure you monitor memory usage and manage graph allocations carefully.

## Security Concerns

1. **Adversarial Attacks**: Malicious inputs designed to exploit model weaknesses (e.g., sending extreme outlier values) can cause integer overflows, excessive memory consumption, or manipulated predictions. Strong Pydantic validation (using `gt`, `lt`, string length limits) is mandatory.
2. **Denial of Service (DoS)**: ML inference is expensive. Without rate limiting, an attacker can spam your endpoint, causing high compute costs and crashing servers. Implement rate limiting and authentication (e.g., API keys, JWT).
3. **Model Extraction**: If the API returns raw probabilities and confidence scores, attackers can use thousands of API calls to train a surrogate model, effectively stealing your intellectual property. Limit the precision of returned outputs.

## Realistic Interview Questions

1. **Q: How does FastAPI handle concurrent requests if Python has the Global Interpreter Lock (GIL)?**
   - *A: FastAPI uses asynchronous I/O via Starlette and `asyncio`. When a request is waiting for network/I/O (like a database call), it yields control to the event loop, allowing other requests to be processed. The GIL prevents concurrent CPU execution, but I/O-bound concurrency is highly effective. For CPU-bound ML inference, we use multiple processes (via Gunicorn) to bypass the GIL, or offload to thread pools.*
2. **Q: You notice your FastAPI model serving endpoint is dropping requests under high load. What is the first thing you investigate?**
   - *A: I would check if I am blocking the event loop. If I have an `async def` endpoint but I am running a synchronous, CPU-intensive `model.predict()` inside it without offloading to a thread pool, the server will block and drop new requests. I would also check CPU/Memory utilization and whether Gunicorn is configured with enough workers.*
3. **Q: How would you implement dynamic batching in a FastAPI application?**
   - *A: I would use a background task or a separate asynchronous queue (like `asyncio.Queue`). The endpoint receives requests, puts the data into the queue, and awaits an Event. A background worker continuously monitors the queue, pops a batch of items (up to a max size or max wait time), passes the batched tensor to the model, and then sets the Events with the corresponding results to resume the blocked endpoints.*

## Practical Exercises

1. **Basic Deployment**: Train a simple Logistic Regression model on the Iris dataset, save it using `joblib`, and build a FastAPI app to serve predictions.
2. **Validation Mastery**: Extend your API to use Pydantic validators that reject sepal lengths less than 0 or greater than 15. Return custom error messages.
3. **Dockerization**: Write a `Dockerfile` to containerize your FastAPI application using Uvicorn and Gunicorn, and run it locally exposing port 8000.
