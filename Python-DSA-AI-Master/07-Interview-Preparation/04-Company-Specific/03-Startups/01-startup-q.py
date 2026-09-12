"""
Module: Startup Interview Questions - Practical Implementations
Learning Objectives:
1. Understand the types of questions commonly asked in startup interviews.
2. Implement a Token Bucket Rate Limiter (common system design/coding question).
3. Practice writing clean, production-ready code with type hints.

Concept Explanation:
Startups often look for engineers who can build practical, scalable systems quickly.
Questions frequently revolve around APIs, rate limiting, caching, and concurrent data processing.
A Token Bucket algorithm is a common way to implement rate limiting, ensuring APIs aren't overwhelmed.

Imports, Type Hints, and Edge Cases are handled below.
"""

import time
import threading
from typing import Dict, Tuple

class TokenBucketRateLimiter:
    """
    A thread-safe Token Bucket Rate Limiter.
    """
    def __init__(self, capacity: int, refill_rate: float):
        """
        :param capacity: Maximum number of tokens the bucket can hold.
        :param refill_rate: Number of tokens added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = float(capacity)
        self.last_refill_time = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        """Refill tokens based on time elapsed."""
        now = time.time()
        elapsed = now - self.last_refill_time
        tokens_to_add = elapsed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = now

    def allow_request(self, tokens_needed: int = 1) -> bool:
        """
        Check if a request can be allowed.
        """
        with self.lock:
            self._refill()
            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False

class APIGateway:
    """
    Simulates an API Gateway using the Rate Limiter.
    """
    def __init__(self):
        # Allow 5 requests per second max per user
        self.user_limits: Dict[str, TokenBucketRateLimiter] = {}

    def handle_request(self, user_id: str) -> str:
        if user_id not in self.user_limits:
            self.user_limits[user_id] = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
        
        if self.user_limits[user_id].allow_request():
            return f"Request from {user_id} processed successfully."
        else:
            return f"Request from {user_id} rate limited. Try again later."

def main():
    gateway = APIGateway()
    user_id = "startup_founder"

    print("Sending 7 rapid requests...")
    for i in range(7):
        print(f"Req {i+1}:", gateway.handle_request(user_id))
        time.sleep(0.1) # Simulate slight network delay
        
    print("\nWaiting for 2 seconds to refill tokens...")
    time.sleep(2.0)
    
    print("\nSending another request...")
    print("Req 8:", gateway.handle_request(user_id))

if __name__ == "__main__":
    main()
