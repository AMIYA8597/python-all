"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (WEB PERFORMANCE & SCALING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer launches their startup on HackerNews. The traffic spikes 
# from 10 users a minute to 5,000 users a second. Their web server crashes 
# instantly because the homepage executes a 2-second SQL Database query for 
# every single user.
#
# A senior engineer understands "Architectural Scalability". They deploy Redis 
# as an In-Memory caching layer. The first user triggers the 2-second Database 
# query. The result is mathematically serialized into Redis RAM. The next 4,999 
# users never touch the database. The Python server fetches the data directly 
# from Redis RAM in 0.001 seconds, effortlessly handling the traffic spike 
# without upgrading the hardware.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master In-Memory Caching (Redis architecture).
# - Understand Content Delivery Networks (CDNs).
# - Prove the CPU latency differences between Disk I/O and RAM I/O.
#
# ==============================================================================
"""

import time
import timeit
import hashlib

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BOTTLENECK (DISK I/O & RELATIONAL JOINS)
# ==============================================================================
def execute_complex_database_query():
    """
    Simulates a heavy PostgreSQL Query.
    e.g., SELECT * FROM products JOIN reviews ON ... GROUP BY ... ORDER BY ...
    Disk I/O is mathematically the slowest component of any server.
    """
    time.sleep(1.0) # Simulating a 1-second physical disk read!
    return {"data": "Massive Payload of Trending Products"}


# ==============================================================================
# 4. THE IN-MEMORY CACHE (REDIS SIMULATION)
# ==============================================================================
# Redis is a NoSQL Database that lives entirely in RAM!
# It mathematically avoids touching the physical Hard Drive.
class RedisSimulation:
    def __init__(self):
        self.memory = {}
        
    def get(self, key: str):
        # A dictionary lookup is O(1) in RAM! (0.000001 seconds)
        return self.memory.get(key)
        
    def set(self, key: str, value: any, ttl: int):
        # In reality, Redis automatically deletes the key after `ttl` seconds!
        self.memory[key] = value

REDIS_CACHE = RedisSimulation()


def get_homepage_data():
    """
    The Optimized Endpoint.
    It mathematically protects the Database using the Cache!
    """
    cache_key = "api:v1:homepage_trending"
    
    # 1. Attempt to fetch from RAM! (Cache Hit)
    cached_data = REDIS_CACHE.get(cache_key)
    if cached_data:
        return cached_data, "CACHE HIT"
        
    # 2. Cache Miss! (Only the very first user experiences this)
    db_data = execute_complex_database_query()
    
    # 3. Save to RAM for the next user! (Expire after 60 seconds)
    REDIS_CACHE.set(cache_key, db_data, ttl=60)
    
    return db_data, "CACHE MISS"


def demonstrate_caching_architecture():
    section_header("Performance Proof: In-Memory Caching (Redis Pattern)")
    
    print("  [SCENARIO] 5 Users request the Homepage simultaneously.")
    
    print("\n  [NAIVE ARCHITECTURE (No Cache)]")
    start_naive = timeit.default_timer()
    for i in range(1, 6):
        # The database is hammered 5 times!
        execute_complex_database_query()
        print(f"    -> User {i}: Waited 1.00s (Database Hit)")
    end_naive = timeit.default_timer()
    print(f"    -> Total Time: {end_naive - start_naive:.2f} seconds")
    
    
    print("\n  [OPTIMIZED ARCHITECTURE (Redis Cache)]")
    # Resetting the cache for the test
    REDIS_CACHE.memory = {}
    
    start_opt = timeit.default_timer()
    for i in range(1, 6):
        data, status = get_homepage_data()
        if status == "CACHE MISS":
            print(f"    -> User {i}: Waited 1.00s ({status} - Database Hit)")
        else:
            print(f"    -> User {i}: Waited 0.00s ({status} - RAM Hit!)")
            
    end_opt = timeit.default_timer()
    print(f"    -> Total Time: {end_opt - start_opt:.2f} seconds")
    
    print("\n  [CONCLUSION] Caching collapsed the server execution time from 5.0s down to 1.0s!")
    print("  If 5,000 users hit the site, the naive architecture takes 5,000 seconds.")
    print("  The cached architecture still takes exactly 1.0 second!")


# ==============================================================================
# 5. ETAGS (CLIENT-SIDE CACHING)
# ==============================================================================
def generate_etag(data: str) -> str:
    """Generates an MD5 hash of the payload to serve as a cryptographic ETag."""
    return hashlib.md5(data.encode()).hexdigest()

def demonstrate_etags():
    section_header("Bandwidth Optimization: HTTP ETags")
    
    # The server has 10MB of data.
    massive_payload = "A" * 10_000_000 
    payload_hash = generate_etag(massive_payload)
    
    print("  [SCENARIO] Client requests a 10MB JSON payload.")
    
    print("\n  [REQUEST 1 (Initial Download)]")
    print(f"    -> Client Request:  GET /api/data")
    print(f"    -> Server Response: 200 OK")
    print(f"    -> Server Headers:  ETag: \"{payload_hash}\"")
    print("    -> Bandwidth Cost:  10 MB transferred over the network.")
    
    print("\n  [REQUEST 2 (5 Minutes Later)]")
    print("    The client already has the 10MB file in its browser cache.")
    print("    It wants to know if the data has mathematically changed!")
    print(f"    -> Client Request:  GET /api/data")
    print(f"    -> Client Headers:  If-None-Match: \"{payload_hash}\"")
    
    # Server logic!
    server_current_hash = generate_etag(massive_payload)
    
    if server_current_hash == payload_hash:
        print(f"    -> Server Response: 304 NOT MODIFIED")
        print("    -> Bandwidth Cost:  0 MB transferred!")
        print("    (The server mathematically proved the data hasn't changed. The client")
        print("     loads the 10MB file instantly from its own local Hard Drive!)")


def run_all_labs():
    demonstrate_caching_architecture()
    demonstrate_etags()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we deploy Redis as a caching layer instead of just storing the data in a standard Python Global Dictionary?"
   Senior Answer: "Storing a global dictionary in Python RAM (Local Caching) works for a single process on a single server. But modern web backends are horizontally scaled across multiple physical servers (e.g., $10$ AWS EC2 instances running $40$ Gunicorn processes). If Server A fetches the DB data and saves it to a local Python dictionary, Server B is mathematically blind to it! If a request hits Server B, it will hit the Database again. Redis solves this by acting as an external, distributed, central RAM database. All $40$ Python processes mathematically connect to the exact same Redis instance via TCP, guaranteeing $100\\%$ cache coherence and protecting the DB across the entire global server fleet."

2. Interviewer: "What is a Content Delivery Network (CDN) like Cloudflare, and how does it protect the Python Web Server from catastrophic traffic spikes?"
   Senior Answer: "A CDN is a globally distributed network of reverse-proxy cache servers sitting *in front* of your Python application. When a user in Japan requests your website, the request hits a Cloudflare server physically located in Tokyo, not your origin server in New York. If Cloudflare has the HTML/CSS/Images cached in Tokyo, it returns the data instantly, $0$ network packets ever reach New York. By caching static assets at the CDN edge, $90\\%$ of internet traffic is physically absorbed by Cloudflare's massive hardware, mathematically shielding your fragile Python WSGI server from DDOS attacks and traffic spikes."

3. Interviewer: "If caching makes everything so incredibly fast, why is 'Cache Invalidation' considered one of the hardest problems in Computer Science?"
   Senior Answer: "Because of 'Stale Data'. If an E-Commerce site caches the price of a MacBook as $\\$2,000$ in Redis for $24$ hours, and the CEO changes the price in the PostgreSQL database to $\\$1,500$ an hour later, the Database and the Cache are mathematically desynchronized. For the next $23$ hours, the Python server will blindly serve the stale $\\$2,000$ price from Redis. The engineering complexity lies in architecting 'Event-Driven Invalidation'. The exact millisecond the SQL row updates, the Python backend must fire a message broker event to forcefully delete the specific `api:v1:macbook_price` key from Redis, forcing the next user to cleanly hit the Database and re-sync the Cache. This distributed state management is incredibly prone to race conditions."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Web Development (Performance) Completed.")
