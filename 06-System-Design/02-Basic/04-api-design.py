"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (API DESIGN & RATE LIMITING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have perfectly scaled your databases and load balancers. Suddenly, a 
# malicious script hits your API with 100,000 requests per second. Your 
# database is instantly crushed, and your AWS bill is $50,000 for the day.
#
# You must protect your system using Rate Limiting algorithms (like the Token 
# Bucket) at the API Gateway.
#
# Furthermore, what happens when a user clicks "Submit Payment" on a terrible 
# 3G network? The request hits the server, the server charges their credit card, 
# but the response ("Success") is lost in the 3G network. The user sees a blank 
# screen, clicks "Submit Payment" again, and is charged twice!
#
# Your API must be mathematically "Idempotent". Making the exact same API call 
# 100 times should have the exact same effect as making it once.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand REST vs GraphQL vs gRPC.
# - Master Idempotency Keys for safe retries.
# - Implement the Token Bucket Rate Limiting Algorithm.
#
# ==============================================================================
"""

import time
import threading

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IDEMPOTENCY (SAFE RETRIES)
# ==============================================================================
class PaymentGateway:
    def __init__(self):
        # Database of previously processed transactions!
        self.processed_idempotency_keys = set()
        self.user_balance = 1000
        
    def charge_credit_card(self, user_id: str, amount: int, idempotency_key: str) -> str:
        """
        An Idempotent API endpoint.
        The client generates a unique UUID (Idempotency Key) for the transaction.
        If the network drops and the client retries, they send the SAME key.
        The server recognizes the key and mathematically blocks the duplicate charge!
        """
        print(f"[API RECEIVE] Request to charge ${amount}. Key: {idempotency_key}")
        
        if idempotency_key in self.processed_idempotency_keys:
            print("  -> [IDEMPOTENCY TRIGGERED] We already processed this exact key!")
            print("  -> Returning the cached 'Success' response without charging again.")
            return "SUCCESS_CACHED"
            
        # Processing a brand new transaction...
        self.user_balance -= amount
        self.processed_idempotency_keys.add(idempotency_key)
        print(f"  -> [NEW TRANSACTION] Successfully charged. Balance: ${self.user_balance}")
        
        return "SUCCESS_NEW"

def demonstrate_idempotency():
    section_header("API Idempotency (Safe Retries)")
    
    api = PaymentGateway()
    
    print("User initiates a payment of $100. Key: 'uuid-999'")
    api.charge_credit_card("user_A", 100, "uuid-999")
    
    print("\nThe user's 3G network drops! They panic and click 'Pay' two more times!")
    api.charge_credit_card("user_A", 100, "uuid-999")
    api.charge_credit_card("user_A", 100, "uuid-999")
    
    print("\nBecause the API is Idempotent, they were only charged once!")


# ==============================================================================
# 4. RATE LIMITING (TOKEN BUCKET ALGORITHM)
# ==============================================================================
class TokenBucketRateLimiter:
    """
    The famous Token Bucket Algorithm used by AWS, Stripe, and Google.
    - You have a Bucket that can hold a maximum of N tokens.
    - Every second, a background process adds R tokens to the bucket.
    - Every API request costs 1 token.
    - If the bucket is empty, the API request is violently rejected (HTTP 429).
    This beautifully allows "bursts" of traffic (up to N), but strictly limits 
    the sustained rate (to R).
    """
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate_per_sec
        self.last_refill_timestamp = time.time()
        
        # Thread lock for concurrent access
        self.lock = threading.Lock()

    def allow_request(self) -> bool:
        with self.lock:
            now = time.time()
            
            # 1. Mathematically calculate how many tokens should have been 
            # added since the last time we checked!
            time_elapsed = now - self.last_refill_timestamp
            tokens_to_add = time_elapsed * self.refill_rate
            
            if tokens_to_add > 0:
                # Add tokens, but cap it at the physical bucket capacity!
                self.tokens = min(self.capacity, self.tokens + tokens_to_add)
                self.last_refill_timestamp = now
                
            # 2. Check if we have a token to spend!
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            else:
                return False

def demonstrate_token_bucket():
    section_header("API Rate Limiting (Token Bucket)")
    
    # Bucket can hold max 3 tokens. Refills at 1 token per second.
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_sec=1.0)
    
    print("Bucket Capacity: 3. Refill Rate: 1/sec.")
    print("\nSimulating a massive burst of 5 instantaneous API requests:")
    
    for i in range(5):
        if limiter.allow_request():
            print(f"  Req {i+1}: SUCCESS (Token spent)")
        else:
            print(f"  Req {i+1}: HTTP 429 TOO MANY REQUESTS (Bucket Empty!)")
            
    print("\nWaiting 2.5 seconds for the bucket to refill...")
    time.sleep(2.5)
    
    print("\nSimulating another burst of 3 requests:")
    for i in range(3):
        if limiter.allow_request():
            print(f"  Req {i+1}: SUCCESS (Token spent)")
        else:
            print(f"  Req {i+1}: HTTP 429 TOO MANY REQUESTS (Bucket Empty!)")


def run_all_labs():
    demonstrate_idempotency()
    demonstrate_token_bucket()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the difference between REST, GraphQL, and gRPC.
   Answer: 
   - REST is the standard. It uses HTTP verbs (GET, POST) and URLs mapped to resources (`/users/123`). It suffers from Over-fetching (returning a massive JSON when you only wanted the user's name) and Under-fetching (requiring 5 separate API calls to assemble a page).
   - GraphQL was invented by Facebook to fix this. It exposes a single endpoint (`/graphql`). The client sends a mathematically precise query describing exactly the shape of the data it wants, and the server returns exactly that.
   - gRPC was invented by Google for purely internal microservice-to-microservice communication. It abandons heavy JSON/HTTP in favor of raw binary Protobufs over HTTP/2. It is blisteringly fast, utilizing multiplexing and binary compression, but cannot be easily read by human browsers.

2. What is an Idempotency Key, and who generates it (the Client or the Server)?
   Answer: An Idempotency Key is a unique string (like a UUIDv4) that mathematically identifies a specific logical action. It MUST be generated by the CLIENT. If the server generated it, the client would have to make an API call to get the key, which itself could fail in a network drop! By having the client generate the key locally (e.g., when the user clicks 'Checkout'), the client can blindly retry the `POST /charge` request 100 times. The server looks at the UUID, checks its database, sees it already charged that UUID, and intercepts all 99 retries, returning a cached success without double-charging.

3. In the Token Bucket algorithm, why do we use `time_elapsed * refill_rate` instead of a physical background `while True` loop that sleeps for 1 second?
   Answer: If you have 100,000 users, running 100,000 independent `while True` sleep threads just to add tokens to their buckets would completely crash the CPU with context-switching overhead. The Token Bucket algorithm is mathematically lazy! It stores the *timestamp* of the last interaction. When a user finally makes a request, it calculates the exact time difference (e.g., 5.34 seconds), mathematically multiplies it by the refill rate, and instantly deposits the correct fractional amount of tokens. It does zero work in the background, making it an $O(1)$ ultra-lightweight algorithm!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (API Design) Completed.")
