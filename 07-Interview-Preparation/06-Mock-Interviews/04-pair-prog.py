"""
Module: 04-pair-prog
Learning Objectives:
- Understand the dynamics of pair programming interviews.
- Practice collaborative coding and code review.
- Implement a practical utility function together.

This script simulates a pair programming task: Building a thread-safe Rate Limiter.
"""

import time
import threading
from typing import Dict

# --- Concept Explanation ---
# Pair programming interviews focus on collaboration.
# You act as the "driver" (typing) while the interviewer is the "navigator", or vice versa.
# It is important to talk through decisions, write tests first (TDD), and refactor.

# --- Implementation ---
class TokenBucketRateLimiter:
    """
    Thread-safe implementation of a Token Bucket Rate Limiter.
    """
    def __init__(self, capacity: int, fill_rate: float):
        """
        capacity: Maximum tokens the bucket can hold.
        fill_rate: Tokens added per second.
        """
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = capacity
        self.last_fill_time = time.time()
        self.lock = threading.Lock()

    def _add_tokens(self):
        now = time.time()
        time_passed = now - self.last_fill_time
        new_tokens = time_passed * self.fill_rate
        
        if new_tokens > 0:
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_fill_time = now

    def allow_request(self, tokens_required: int = 1) -> bool:
        """
        Checks if a request is allowed based on available tokens.
        """
        with self.lock:
            self._add_tokens()
            if self.tokens >= tokens_required:
                self.tokens -= tokens_required
                return True
            return False

# --- Performance Analysis ---
# Time: O(1) for allow_request.
# Space: O(1) state variables per user/system.

# --- Edge Cases ---
# 1. Very rapid requests (handled by lock).
# 2. Long periods of inactivity (handled by capacity cap).

# --- Interview Challenge ---
# Challenge: Extend this to be a multi-user rate limiter where each user has their own bucket.
# (Hint: Use a dictionary of user_id -> TokenBucket).

# --- Tests ---
def test_rate_limiter():
    # 2 tokens capacity, fills 1 token per second
    limiter = TokenBucketRateLimiter(capacity=2, fill_rate=1.0)
    
    assert limiter.allow_request() is True, "First request should pass"
    assert limiter.allow_request() is True, "Second request should pass"
    assert limiter.allow_request() is False, "Third request should fail (bucket empty)"
    
    # Wait for 1 second to replenish 1 token
    time.sleep(1.1)
    assert limiter.allow_request() is True, "Request should pass after wait"
    assert limiter.allow_request() is False, "Next request should fail again"
    
    print("All pair programming tests passed!")

if __name__ == "__main__":
    test_rate_limiter()
