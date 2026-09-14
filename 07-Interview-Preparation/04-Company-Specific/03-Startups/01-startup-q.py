"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (STARTUPS - PRACTICAL PYTHON)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Unlike FAANG companies that obsess over O(1) mathematical proofs, Startups 
# operate in survival mode. Their interviews focus heavily on your ability to 
# write practical, production-ready Python code that integrates with APIs, 
# processes JSON data, and handles rate limiting / retries flawlessly.
#
# A junior engineer writes a script that crashes the entire backend if an external 
# API returns a 500 error, or if a JSON payload is missing a key.
# 
# A senior engineer writes resilient code. They wrap network calls in intelligent 
# Decorators that implement Exponential Backoff. They use `dict.get()` and 
# structural pattern matching to parse chaotic JSON feeds safely. They prioritize 
# execution speed and developer velocity over theoretical algorithmic purity.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Exponential Backoff Retry Decorator (Startup Essential).
# - Master chaotic JSON parsing and data aggregation.
# - Understand how to write resilient, fail-safe production Python.
#
# ==============================================================================
"""

import time
import random
import functools
from typing import Callable, Any, Dict, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EXPONENTIAL BACKOFF (THE RESILIENCY DECORATOR)
# ==============================================================================
def retry_with_backoff(retries: int = 3, backoff_in_seconds: float = 1.0):
    """
    A production-grade decorator that intercepts function crashes.
    If the function throws an Exception, it waits, doubles the wait time, and 
    tries again. This prevents a temporary API blip from destroying the server!
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            x = 0
            while True:
                try:
                    print(f"    [ATTEMPT {x+1}/{retries+1}] Executing {func.__name__}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        print(f"    [FATAL] Function '{func.__name__}' failed permanently: {e}")
                        raise # We ran out of retries! Bubble up the crash!
                    
                    # Calculate wait time: 1s, 2s, 4s, 8s...
                    sleep_time = backoff_in_seconds * (2 ** x) 
                    
                    # Add JITTER! (A random microsecond offset to prevent Thundering Herd attacks)
                    jitter = random.uniform(0, 0.1)
                    
                    print(f"    [ERROR] {e} | Retrying in {sleep_time + jitter:.2f} seconds...")
                    time.sleep(sleep_time + jitter)
                    x += 1
        return wrapper
    return decorator

# Let's simulate a chaotic Startup API that fails 80% of the time!
@retry_with_backoff(retries=3, backoff_in_seconds=0.5)
def unstable_api_call(user_id: int) -> dict:
    if random.random() < 0.8:
        raise ConnectionError("503 Service Unavailable (AWS Server Restarted)")
    return {"status": 200, "data": {"user_id": user_id, "name": "Startup CEO"}}

def demonstrate_backoff():
    section_header("Startup: Exponential Backoff API Resilience")
    
    # We force the random seed to guarantee a crash for demonstration purposes,
    # then reset it so it eventually succeeds!
    random.seed(42)
    
    try:
        data = unstable_api_call(101)
        print(f"\n  [SUCCESS] Payload received: {data}")
    except Exception as e:
        print("\n  [SYSTEM ALERT] The API completely failed even after backoffs.")


# ==============================================================================
# 4. CHAOTIC JSON AGGREGATION (REAL-WORLD DATA PARSING)
# ==============================================================================
def aggregate_user_spending(json_payload: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Time: O(N) | Space: O(U) where U is unique users.
    Startups often ingest messy, unstructured JSON logs. 
    Keys might be missing. Values might be strings instead of floats.
    We must parse it flawlessly without crashing.
    """
    spending_map = collections.defaultdict(float)
    
    print("  Processing Chaotic JSON Feed...")
    for entry in json_payload:
        # A junior writes: user = entry["user_id"]. This throws a KeyError and crashes!
        # A senior uses `.get()` with safe fallbacks!
        user = entry.get("user_id", "UNKNOWN_USER")
        
        # Financial amounts might be corrupted (e.g., "$100.50" instead of 100.5)
        raw_amount = entry.get("amount", 0)
        
        try:
            # Clean the data!
            if isinstance(raw_amount, str):
                raw_amount = raw_amount.replace("$", "").replace(",", "")
            
            clean_amount = float(raw_amount)
            spending_map[user] += clean_amount
            
        except ValueError:
            print(f"    [WARNING] Corrupted amount data for user {user}: '{raw_amount}'. Skipping.")
            
    return dict(spending_map)

def demonstrate_json_parsing():
    section_header("Startup: Chaotic JSON Aggregation")
    
    # Notice the missing keys, string formats, and total garbage data!
    feed = [
        {"user_id": "U1", "amount": 50.0},
        {"user_id": "U2", "amount": "$1,000.50"}, # String format!
        {"amount": 25.0}, # Missing User ID!
        {"user_id": "U1", "amount": "invalid_data"}, # Crash trigger!
        {"user_id": "U1", "amount": 10.0}
    ]
    
    ans = aggregate_user_spending(feed)
    
    print("\nFinal Cleaned Aggregation:")
    for user, total in ans.items():
        print(f"  User {user}: ${total:.2f}")


def run_all_labs():
    demonstrate_backoff()
    demonstrate_json_parsing()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Exponential Backoff decorator, why did you add a `random.uniform()` jitter to the sleep time?"
   Senior Answer: "If an AWS server goes down, 5,000 backend microservices might simultaneously fail and enter the Backoff protocol. If there is no random jitter, all 5,000 services will sleep for exactly 1.0 seconds, wake up, and blast the server simultaneously. The server will instantly crash again from the massive spike. They will all sleep for exactly 2.0 seconds, and blast it again. This is called a 'Thundering Herd' attack, and it creates a permanent denial-of-service loop. By adding a random jitter (e.g., $+0.04$s), the 5,000 requests mathematically spread out and stagger their retries, allowing the recovering server to process them sequentially without being overwhelmed."

2. Interviewer: "When parsing a massive stream of JSON dictionaries, why is `entry.get('key')` structurally superior to `entry['key']`?"
   Senior Answer: "In a dynamic Startup environment, database schemas and API payloads mutate rapidly. If you use bracket notation (`entry['key']`), and the external API drops that key from a single payload out of a million, the Python interpreter will throw a fatal `KeyError` and instantly crash your entire parsing pipeline. The `.get()` method intercepts the missing key gracefully and returns `None` (or a default fallback value), allowing the loop to safely sanitize the data anomaly, log a warning, and continue processing the remaining 999,999 logs without interrupting production."

3. Interviewer: "How do you evaluate whether to use a complex, mathematically optimal $O(N)$ algorithm, versus a simple, highly-readable $O(N^2)$ algorithm in a Startup environment?"
   Senior Answer: "It depends entirely on the bounded constraints of the dataset. If the array will never exceed 500 items, an $O(N^2)$ algorithm will take 1 millisecond. In a Startup, engineer time is vastly more expensive than CPU time. If the $O(N^2)$ code is 10x easier to read, debug, and maintain, it is the superior choice for a 500-item list. However, if the list is unbounded (e.g., processing all user logs), an $O(N^2)$ algorithm is a ticking time bomb. The moment the startup goes viral and hits 100,000 users, the $O(N^2)$ code will freeze the server for 20 minutes, causing a catastrophic outage. You must always mathematically bound your expected inputs."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Startup Prep (Practical Python) Completed.")
