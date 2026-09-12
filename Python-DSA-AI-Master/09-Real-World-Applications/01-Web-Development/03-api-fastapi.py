"""
FastAPI: Modern, Fast, and Typed Web APIs

Learning Objectives:
1. Understand the philosophy and benefits of FastAPI.
2. Master Pydantic for data validation and serialization.
3. Learn to build asynchronous endpoints.
4. Professional implementation details including dependency injection and OpenAPI generation.

Concept Explanation:
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
Key features include:
- High performance (on par with NodeJS and Go).
- Automatic interactive API documentation (Swagger UI).
- Data validation and serialization via Pydantic.
- Editor support out of the box (autocompletion everywhere).

Industry use cases include Microservices, Machine Learning Model deployment (serving APIs), Backend systems for Single Page Applications (SPAs), and IoT backends.

Below is a complete script demonstrating FastAPI paradigms, using standard library constructs to simulate the framework's behavior so the concepts can be tested locally without installing Uvicorn/FastAPI, though real-world code uses the `fastapi` module.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
import json
from datetime import datetime

# ==========================================
# 1. Pydantic-like Data Validation (Mock)
# ==========================================
# In FastAPI, you would use `from pydantic import BaseModel`

class MockBaseModel:
    """Mock for Pydantic BaseModel to illustrate typed validation."""
    def __init__(self, **kwargs):
        annotations = self.__annotations__
        for key, expected_type in annotations.items():
            val = kwargs.get(key)
            if val is None and hasattr(self, key):
                val = getattr(self, key)
            if val is not None and not isinstance(val, expected_type):
                try:
                    val = expected_type(val) # Attempt basic cast
                except Exception:
                    raise TypeError(f"Validation Error: '{key}' must be of type {expected_type.__name__}")
            setattr(self, key, val)
    
    def dict(self):
        return {k: getattr(self, k) for k in self.__annotations__.keys()}

class Item(MockBaseModel):
    name: str
    price: float
    is_offer: bool = False
    
# ==========================================
# 2. FastAPI Application Concept (Mock)
# ==========================================
# In FastAPI, you would do:
# from fastapi import FastAPI
# app = FastAPI()

class MockFastAPI:
    def __init__(self):
        self.routes = {}

    def get(self, path: str):
        def decorator(func):
            self.routes[(path, 'GET')] = func
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes[(path, 'POST')] = func
            return func
        return decorator
        
    def simulate_request(self, path: str, method: str, body: Optional[Dict] = None, **kwargs) -> Dict:
        func = self.routes.get((path, method))
        if not func:
            return {"status_code": 404, "detail": "Not Found"}
            
        try:
            # Simulate parsing body to Pydantic model if required by type hints
            import inspect
            sig = inspect.signature(func)
            bound_args = {}
            for param_name, param in sig.parameters.items():
                if issubclass(param.annotation, MockBaseModel):
                    if body is None:
                        return {"status_code": 422, "detail": "Missing request body"}
                    bound_args[param_name] = param.annotation(**body)
                elif param_name in kwargs:
                    bound_args[param_name] = param.annotation(kwargs[param_name])
            
            result = func(**bound_args)
            return {"status_code": 200, "data": result}
        except TypeError as e:
            return {"status_code": 422, "detail": str(e)}
        except Exception as e:
            return {"status_code": 500, "detail": str(e)}

app = MockFastAPI()

# ==========================================
# 3. Defining Endpoints
# ==========================================

@app.get("/")
def read_root() -> Dict[str, str]:
    """A simple root endpoint."""
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None) -> Dict[str, Any]:
    """An endpoint with path and query parameters."""
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item) -> Dict[str, Any]:
    """An endpoint receiving a Pydantic model for JSON body."""
    return {"item_name": item.name, "price_with_tax": item.price * 1.2, "offer": item.is_offer}


# ==========================================
# Usage Example & Tests
# ==========================================
def run_tests():
    print("--- Running FastAPI Concepts Tests ---")
    
    # 1. Test Root GET
    resp = app.simulate_request("/", "GET")
    assert resp["status_code"] == 200
    assert resp["data"] == {"Hello": "World"}
    print("Root GET passed.")
    
    # 2. Test Path Param GET
    resp = app.simulate_request("/items/{item_id}", "GET", item_id=42, q="search")
    assert resp["status_code"] == 200
    assert resp["data"] == {"item_id": 42, "q": "search"}
    print("Path Parameter GET passed.")
    
    # 3. Test POST with valid body
    valid_body = {"name": "Laptop", "price": 1000.0}
    resp = app.simulate_request("/items/", "POST", body=valid_body)
    assert resp["status_code"] == 200
    assert resp["data"]["price_with_tax"] == 1200.0
    print("POST with Valid Body passed.")
    
    # 4. Test POST with invalid body (Type Validation)
    invalid_body = {"name": "Laptop", "price": "not_a_number"}
    resp = app.simulate_request("/items/", "POST", body=invalid_body)
    assert resp["status_code"] == 422
    assert "Validation Error" in resp["detail"]
    print("POST Validation Error passed.")

    print("All FastAPI concepts tests passed successfully.")

if __name__ == "__main__":
    run_tests()

"""
Complexity Analysis & Architecture Discussion:
- Performance: FastAPI utilizes Starlette for web routing and Pydantic for validation, making it extremely fast. Utilizing async/await (`async def`) allows non-blocking I/O operations, drastically increasing throughput for database queries and external API calls.
- Scalability: Perfect for Microservices architecture. Dockerizes easily and runs efficiently with workers via Gunicorn + Uvicorn.
- Auto-Docs: FastAPI automatically generates OpenAPI (Swagger) and ReDoc documentation based on the Python type hints, keeping docs always synchronized with the code.

Interview Challenge:
Q: What is Dependency Injection in FastAPI, and why is it useful?
A: FastAPI has a powerful Dependency Injection system accessible via `Depends()`. 
   It allows you to declare functions that provide required resources (like database sessions, current authenticated user, etc.) to your endpoint.
   It promotes code reusability, modularity, and makes testing significantly easier by allowing dependencies to be overridden in tests.
"""
