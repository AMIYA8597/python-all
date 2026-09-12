"""
04 - API Design in System Design
================================

What is API Design?
API (Application Programming Interface) design defines the contracts and mechanisms through 
which different software components communicate. In modern distributed systems, RESTful 
HTTP APIs or RPC (like gRPC) are heavily used.

Why it exists and Industry Use Cases:
- Decouples client (frontend, mobile) from the server (backend logic and DB).
- Allows third-party integrations (e.g., Stripe API, Twilio API).
- Ensures security, rate limiting, and predictable data formatting.

Key Concepts:
1. REST Principles: Resource-based URLs, statelessness, appropriate HTTP methods (GET, POST, PUT, DELETE), 
   and standard status codes.
2. Pagination: Returning large data sets in manageable chunks (e.g., offset-based, cursor-based) to 
   save network bandwidth and DB query time.
3. Rate Limiting: Restricting the number of requests a client can make in a given timeframe to 
   protect the system from DDoS attacks and abuse. (Algorithms: Token Bucket, Leaky Bucket, Sliding Window).
4. Idempotency: Ensuring that making the same request multiple times has the same effect as making it once 
   (crucial for retries in payment gateways).

Learning Objectives:
1. Understand how to design robust, production-ready APIs.
2. Implement a Token Bucket Rate Limiter.
3. Implement a mock API request handler that incorporates rate limiting and cursor-based pagination.
"""

import time
import math
from typing import Dict, List, Any, Tuple

# ============================================================================
# Basic Concept: Simple API Endpoint Function
# ============================================================================
USERS_DB = [{"id": i, "name": f"User_{i}"} for i in range(1, 101)]

def get_users_basic(limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
    """A basic offset-based pagination endpoint."""
    return USERS_DB[offset : offset + limit]

# ============================================================================
# Professional Implementation: Rate Limiter and Cursor Pagination
# ============================================================================
class TokenBucketRateLimiter:
    """
    A Token Bucket rate limiting algorithm.
    Tokens are added at a constant rate up to a burst capacity.
    Each API request consumes one token.
    """
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill_time = time.time()
        
    def _refill(self) -> None:
        """Calculate how many tokens to add based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill_time
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

    def allow_request(self) -> bool:
        """Check if a request is allowed (has tokens). Consume 1 token if so."""
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class APIHandler:
    """
    A professional mock API Handler simulating middleware execution.
    It applies Rate Limiting and provides a robust Cursor-based pagination endpoint.
    """
    def __init__(self):
        # Allow 3 requests burst, refill 1 request per second
        self.rate_limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=1.0)
        # Mock database sorted by ID
        self.data_store = [{"id": i, "name": f"Item_{i}", "created_at": time.time()} for i in range(1, 101)]

    def handle_request(self, endpoint: str, params: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        Simulate an HTTP request router/middleware.
        Returns a tuple of (HTTP Status Code, Response Body).
        """
        # 1. Rate Limiting Middleware
        if not self.rate_limiter.allow_request():
            return 429, {"error": "Too Many Requests. Rate limit exceeded."}

        # 2. Router
        if endpoint == "/items":
            return self._get_items(params)
        
        return 404, {"error": "Endpoint not found"}

    def _get_items(self, params: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        Cursor-based pagination implementation.
        More performant than offset-based for large datasets, as it doesn't 
        require the DB to scan through 'offset' number of rows.
        """
        limit = min(int(params.get("limit", 10)), 50) # Max limit 50
        cursor = params.get("cursor", None)
        
        results = []
        next_cursor = None
        
        # In a real DB, this would be: SELECT * FROM items WHERE id > cursor ORDER BY id LIMIT limit
        start_idx = 0
        if cursor is not None:
            # Find the index of the cursor. (In O(N) here for mock, DB does O(log N) with index)
            for i, item in enumerate(self.data_store):
                if item["id"] == cursor:
                    start_idx = i + 1
                    break
        
        results = self.data_store[start_idx : start_idx + limit]
        
        if len(results) > 0 and start_idx + limit < len(self.data_store):
            next_cursor = results[-1]["id"]
            
        response = {
            "data": results,
            "pagination": {
                "next_cursor": next_cursor,
                "has_more": next_cursor is not None,
                "limit": limit
            }
        }
        return 200, response


# ============================================================================
# Advanced Concepts & Interview Focus
# ============================================================================
"""
Common Interview Questions:
1. Why prefer Cursor-based pagination over Offset-based pagination?
   Answer: Offset pagination becomes very slow for deep pages (e.g., OFFSET 100000) because 
   the DB must fetch and discard the first 100,000 rows. Cursor pagination uses a specific 
   indexed pointer (e.g., WHERE id > 100000) allowing the DB to jump directly to the row via an index.

2. How would you design idempotency for a POST /charge endpoint?
   Answer: Require clients to send an 'Idempotency-Key' header (a UUID). The server stores this key 
   in a distributed cache or DB alongside the response. If a retry happens with the same key, 
   the server returns the cached response without processing the payment again.

3. Explain the difference between Token Bucket and Leaky Bucket algorithms.
   Answer: Token Bucket allows bursts of traffic up to the bucket capacity, processing them immediately. 
   Leaky Bucket processes requests at a strict, constant rate, smoothing out bursts (like a queue).

Complexity Analysis:
- Rate Limiter check: O(1) time complexity.
- Cursor Pagination DB query: O(log N + L) where N is table size (B-Tree traversal to cursor) 
  and L is the limit (rows fetched).

Security Considerations:
- Unbounded limits: Always hardcap the maximum `limit` a user can request to prevent 
  them from pulling massive amounts of data and causing out-of-memory errors on the server.
"""

# ============================================================================
# Tests / Example Usage
# ============================================================================
def test_api_design() -> None:
    print("Testing API Handler...")
    api = APIHandler()
    
    # Test 1: Successful initial request (Cursor Pagination)
    status, response = api.handle_request("/items", {"limit": 5})
    assert status == 200
    assert len(response["data"]) == 5
    assert response["data"][0]["id"] == 1
    assert response["pagination"]["next_cursor"] == 5
    
    # Test 2: Next page using cursor
    cursor = response["pagination"]["next_cursor"]
    status, response = api.handle_request("/items", {"limit": 5, "cursor": cursor})
    assert status == 200
    assert response["data"][0]["id"] == 6
    
    # Test 3: Rate Limiting (Burst capacity is 3. We've used 2. One more should pass, next should fail)
    status, response = api.handle_request("/items", {"limit": 1})
    assert status == 200 # Token 3 used
    
    status, response = api.handle_request("/items", {"limit": 1})
    assert status == 429 # Rate limited!
    assert "error" in response
    
    # Wait for token refill
    time.sleep(1.1)
    status, response = api.handle_request("/items", {"limit": 1})
    assert status == 200 # Refilled 1 token, should pass
    
    print("All API Design tests passed!\\n")

if __name__ == "__main__":
    test_api_design()
