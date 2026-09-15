"""
# ==============================================================================
# LABORATORY: MLOPS (MODEL INFERENCE SERVING VIA FASTAPI)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior Data Scientist trains a fantastic model, saves it as `model.pkl`, 
# and hands it to the Frontend team. The Frontend team uses JavaScript. They 
# cannot read a Python Pickle file. The model is completely useless in production.
#
# A senior AI engineer understands "Microservice Architecture". They write a 
# high-performance FastAPI server. They load the `.pkl` file directly into the 
# server's RAM exactly once upon startup. They expose a `/predict` HTTP POST 
# endpoint that accepts JSON and returns JSON. The Frontend team simply sends 
# an HTTP request to the endpoint. The AI model is successfully integrated into 
# the global tech stack.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Model Serialization (Pickle / Joblib).
# - Architect a FastAPI REST endpoint for inference.
# - Execute asynchronous request handling for high throughput.
#
# ==============================================================================
"""

import json
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (MODEL SERIALIZATION & LOADING)
# ==============================================================================
class MockModel:
    """Simulates a trained Machine Learning Model loaded from disk."""
    
    def predict(self, feature_vector: list) -> float:
        # Simulate an arbitrary regression prediction
        base = 100.0
        for val in feature_vector:
            base += (val * 2.5)
        return base


class ModelRegistrySimulator:
    
    @staticmethod
    def load_model_from_disk(path: str) -> MockModel:
        """
        [SECURE] Model Loading.
        In production, this happens exactly ONCE during the server startup. 
        If you load the model on every single HTTP request, the server will crash 
        under load due to massive Disk I/O bottlenecks.
        """
        print(f"  [SERVER STARTUP] Loading model weights from '{path}' into RAM...")
        time.sleep(0.5) # Simulating Disk I/O
        return MockModel()


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: FASTAPI ENDPOINT SIMULATION
# ==============================================================================
class FastAPISimulator:
    """
    Simulates the routing and execution of a FastAPI `@app.post("/predict")` endpoint.
    """
    
    def __init__(self):
        # 1. Load the model globally into memory upon initialization!
        self.production_model = ModelRegistrySimulator.load_model_from_disk("s3://models/v3.pkl")
        print("  [SERVER STATUS] FastAPI listening on Port 8000.\n")

    def handle_predict_request(self, http_payload: str) -> str:
        """
        [SECURE] The REST Endpoint.
        Accepts raw JSON over HTTP, parses it into Python types, runs it through 
        the ML model, and returns a JSON HTTP Response.
        """
        print("  [NETWORK] Received incoming HTTP POST request at `/predict`.")
        
        try:
            # 1. Parse the incoming JSON Payload
            request_data = json.loads(http_payload)
            features = request_data.get("features")
            
            if not features or not isinstance(features, list):
                return json.dumps({"status": 400, "error": "Invalid Input Schema."})
                
            print(f"  -> Extracted features from JSON: {features}")
            
            # 2. Execute Inference using the globally loaded model!
            print("  -> Executing Neural Network Forward Pass...")
            prediction = self.production_model.predict(features)
            
            # 3. Construct the HTTP Response
            response = {
                "status": 200,
                "prediction_value": prediction,
                "model_version": "v3.0"
            }
            
            print("  [NETWORK] Returning JSON HTTP Response.")
            return json.dumps(response)
            
        except Exception as e:
            return json.dumps({"status": 500, "error": str(e)})


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_fastapi_serving():
    section_header("MLOps: Serving Models via FastAPI REST Endpoints")
    
    server = FastAPISimulator()
    
    # Simulate a Frontend Client sending an HTTP POST request
    client_payload = '{"features": [12.5, 4.0, 8.2]}'
    
    http_response = server.handle_predict_request(client_payload)
    
    print(f"\n  [FRONTEND CLIENT RECEIVED]")
    print(f"  {http_response}")
    
    print("\n  [FLAWLESS] The ML model successfully bridged the gap between Python ")
    print("  and the web. The JavaScript frontend has no idea how the model works, ")
    print("  it only knows how to securely send and receive JSON.")


def run_all_labs():
    demonstrate_fastapi_serving()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we load the Machine Learning Model at the global scope level in FastAPI, rather than inside the `@app.post` route function?"
   Senior Answer: "Disk I/O and Latency Bottlenecks. If you write `model = joblib.load('model.pkl')` inside the endpoint function, the server must physically read the $5$GB file from the SSD into RAM every single time a user makes a request. If $100$ users click 'predict' simultaneously, the server tries to read $500$GB of data from the disk and instantly crashes. By loading it globally outside the function, the $5$GB model is loaded exactly once when the server boots. The endpoint function simply references the memory pointer, reducing inference latency from $5.0$ seconds down to $0.01$ seconds."

2. Interviewer: "What is Pydantic, and why is it mandatory when building ML APIs with FastAPI?"
   Senior Answer: "Data Validation and Type Coercion. A Machine Learning model mathematically expects a strict vector of floats (e.g., `[1.5, 2.0]`). If a user sends a malicious or malformed JSON payload containing strings `['apple', 'banana']`, the ML model will crash with a cryptic Pandas/Numpy Exception. Pydantic allows you to define a strict Python Class schema. FastAPI automatically intercepts the incoming JSON, runs it through the Pydantic schema, and if the data is invalid, instantly returns an HTTP $422$ Validation Error to the client *before* the ML code even executes. It physically protects the ML engine from bad data."

3. Interviewer: "FastAPI is asynchronous (`async def`). But `model.predict()` is a synchronous, CPU-bound operation. How does this affect server concurrency?"
   Senior Answer: "Event Loop Blocking. If you place a heavy, $2$-second CPU-bound `model.predict()` call inside an `async def` route without awaiting it properly (or delegating it), it will completely block the Uvicorn Async Event Loop. For those $2$ seconds, the server cannot accept ANY other incoming HTTP requests; they will simply hang. To solve this, you must either define the route as a standard `def` (which forces FastAPI to run it in a separate background threadpool), or explicitly use `asyncio.to_thread(model.predict)` to offload the heavy CPU math away from the main network loop."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: MLOps (FastAPI Serving) Completed.")
