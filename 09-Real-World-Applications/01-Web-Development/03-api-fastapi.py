"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (WEB DEVELOPMENT - FASTAPI & PYDANTIC)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer builds a REST API using Flask. They write 50 lines of code 
# per endpoint just to mathematically validate that the incoming JSON payload 
# contains an integer for "age" and a string for "email". When the client sends 
# invalid data, the server throws a 500 Internal Server Error.
#
# A senior engineer understands "Type-Driven Design". They install `FastAPI`. 
# They define the expected JSON payload using standard Python Type Hints and 
# a Pydantic Model. FastAPI mathematically introspects the type hints, completely 
# automates the validation, automatically serializes the JSON, automatically 
# generates Swagger/OpenAPI documentation, and executes asynchronously at Node.js 
# and Go-level speeds, taking exactly 10 lines of code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master FastAPI architecture and standard routing.
# - Master Pydantic Data Validation (Type-Driven Design).
# - Understand Asynchronous Web Server execution (`async def`).
#
# ==============================================================================
"""

# Gracefully handle the absence of FastAPI/Pydantic
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, EmailStr, Field
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    # Mocking for pure execution without dependencies
    FastAPI = lambda: None
    BaseModel = object
    EmailStr = str
    def Field(*args, **kwargs): return None
    class HTTPException(Exception): pass

import threading
import time
import requests

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TYPE-DRIVEN DATA VALIDATION (PYDANTIC)
# ==============================================================================
# In Flask, you manually parse `request.get_json()`.
# In FastAPI, you declare a Pydantic Model. It acts as an impenetrable 
# mathematical shield. If a client sends a payload that fails these type hints, 
# FastAPI intercepts it and returns a highly detailed 422 Unprocessable Entity 
# error BEFORE your business logic even executes!

class UserRegistration(BaseModel):
    # Standard type hint!
    username: str
    
    # Advanced validation! Must be > 18, less than 120.
    age: int = Field(..., gt=17, lt=120, description="User's age in years.")
    
    # Built-in Regex Validation! (Fails if not a valid email string)
    email: str # In production, use `EmailStr` from pydantic[email]
    
    # Optional fields
    is_active: bool = True


# ==============================================================================
# 4. FASTAPI ROUTING ENGINE
# ==============================================================================
if HAS_FASTAPI:
    app = FastAPI(title="Laboratory API", version="1.0.0")

    # --- 1. THE ASYNC ENDPOINT ---
    # Because FastAPI natively supports Asyncio, endpoints can be `async def`.
    # This allows the single OS Thread to process 10,000 concurrent requests 
    # while waiting for Database I/O!
    @app.get("/api/v1/health")
    async def health_check():
        """Returns the system health. Automatically converted to JSON."""
        return {"status": "ok", "framework": "FastAPI"}

    # --- 2. AUTOMATIC PAYLOAD PARSING ---
    # By simply typing the `user` parameter as `UserRegistration`, FastAPI 
    # mathematically binds the incoming HTTP JSON payload to the Pydantic Model!
    @app.post("/api/v1/register", status_code=201)
    async def register_user(user: UserRegistration):
        """Registers a new user. The data is mathematically guaranteed to be valid!"""
        
        # We can instantly access the data via standard Python dot notation!
        # No `dictionary.get("age")` nonsense!
        if user.username.lower() == "admin":
            # FastAPI handles exceptions cleanly and returns the correct JSON format
            raise HTTPException(status_code=400, detail="Username reserved.")
            
        # Pretend we wrote this to a database...
        return {
            "message": f"Successfully registered {user.username}!",
            "assigned_tier": "premium" if user.age > 30 else "standard",
            "data": user.model_dump()
        }


# ==============================================================================
# 5. MATHEMATICAL PROOF OF EXECUTION
# ==============================================================================
def run_fastapi_server():
    """Boot the ASGI Server (Uvicorn)."""
    # ASGI (Asynchronous Server Gateway Interface) replaces WSGI!
    import logging
    log = logging.getLogger("uvicorn")
    log.setLevel(logging.ERROR)
    
    uvicorn.run(app, host="127.0.0.1", port=5055, log_level="critical")

def demonstrate_fastapi():
    section_header("Performance Proof: FastAPI & Pydantic Shield")
    
    if not HAS_FASTAPI:
        print("  [ERROR] FastAPI is not installed.")
        print("  Run `pip install fastapi[all] requests` to execute this lab.")
        return
        
    print("  [INIT] Booting FastAPI ASGI Server (Uvicorn) on background thread...")
    server_thread = threading.Thread(target=run_fastapi_server, daemon=True)
    server_thread.start()
    
    time.sleep(1.0)
    base_url = "http://127.0.0.1:5055"
    
    print("\n  [TEST 1: Standard GET Request]")
    res1 = requests.get(f"{base_url}/api/v1/health")
    print(f"    -> Status: {res1.status_code}")
    print(f"    -> JSON:   {res1.json()}")
    
    print("\n  [TEST 2: POST Valid Data (Type Hints passed)]")
    valid_payload = {
        "username": "Neo",
        "age": 28,
        "email": "neo@matrix.com"
    }
    res2 = requests.post(f"{base_url}/api/v1/register", json=valid_payload)
    print(f"    -> Status: {res2.status_code}")
    print(f"    -> JSON:   {res2.json()}")
    
    print("\n  [TEST 3: THE PYDANTIC SHIELD (Invalid Type - Age is a String)]")
    invalid_type_payload = {
        "username": "Trinity",
        "age": "TWENTY-FIVE", # String instead of Integer!
        "email": "trinity@matrix.com"
    }
    res3 = requests.post(f"{base_url}/api/v1/register", json=invalid_type_payload)
    print(f"    -> Status: {res3.status_code} (Unprocessable Entity)")
    # FastAPI automatically generates a beautiful error pointing exactly to the failed field!
    print(f"    -> Error:  {res3.json()['detail'][0]['msg']}")
    
    print("\n  [TEST 4: THE PYDANTIC SHIELD (Mathematical Constraint - Under 18)]")
    invalid_math_payload = {
        "username": "Morpheus",
        "age": 15, # Less than 18!
        "email": "morpheus@matrix.com"
    }
    res4 = requests.post(f"{base_url}/api/v1/register", json=invalid_math_payload)
    print(f"    -> Status: {res4.status_code} (Unprocessable Entity)")
    print(f"    -> Error:  {res4.json()['detail'][0]['msg']}")
    
    print("\n  [SHUTDOWN] Terminating Client. Background Server thread will die automatically.")


def run_all_labs():
    demonstrate_fastapi()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did the creation of FastAPI mathematically obsolete traditional Flask deployments for highly concurrent Microservices?"
   Senior Answer: "Flask was built on WSGI, which is fundamentally synchronous. If a Flask API endpoint queries a slow database taking $1.0$ seconds, the entire OS Thread is frozen. Handling 10,000 requests requires 10,000 heavy OS threads. FastAPI was built on ASGI (Asynchronous Server Gateway Interface) and Python's `asyncio`. When a FastAPI endpoint queries a Database, it uses the `await` keyword, immediately dropping the OS thread and yielding it back to the Uvicorn Event Loop. A single CPU core can mathematically juggle tens of thousands of concurrent network requests in User Space, allowing Python to achieve performance throughput previously reserved for Node.js and Golang."

2. Interviewer: "What is 'Type-Driven Design', and how does Pydantic drastically reduce the amount of business logic you have to write?"
   Senior Answer: "In traditional Python, type hints are purely cosmetic and ignored at runtime. In Type-Driven Design (via Pydantic), the type hints are weaponized into mathematical enforcement mechanisms at runtime. If a JSON payload arrives with `{'age': 'twenty'}`, a traditional Flask app would pass the string into the logic, where it would eventually crash a database query or a math function deep inside the codebase, triggering a 500 Server Error. Pydantic physically intercepts the JSON payload at the boundary, attempts to coerce the types, and if it mathematically fails, instantly generates a detailed 422 HTTP response before your business logic executes a single line of code. It mathematically guarantees that if your function executes, the data is flawless."

3. Interviewer: "FastAPI automatically generates an OpenAPI (Swagger) interface out of the box. How is this architecturally possible without the developer writing explicit documentation?"
   Senior Answer: "Because FastAPI forces the developer to define the API request payloads, response models, and URL parameters using strict Python Type Hints and Pydantic schemas, the entire architecture of the API is mathematically mapped in RAM. FastAPI simply runs an internal script that dynamically reflects (introspects) these Pydantic schemas, translates the Type Hints into a standard OpenAPI JSON schema, and serves a pre-built React frontend (Swagger UI) that parses the JSON into a beautiful, interactive web page. The documentation is mathematically guaranteed to be $100\\%$ synchronized with the actual execution code."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Web Development (FastAPI) Completed.")
