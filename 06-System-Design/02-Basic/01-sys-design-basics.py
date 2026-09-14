"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (INTERNET BASICS & CACHING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When a user types `www.google.com` into their browser, an incredibly complex 
# chain of distributed systems fires in milliseconds.
#
# First, the browser doesn't know what "google.com" is. It queries the Domain 
# Name System (DNS) to resolve the human string into a mathematical IP address.
#
# Second, the user might be in Australia, but the main database is in New York. 
# The speed of light is too slow; the user would suffer 300ms of lag. The system 
# intercepts the request using a Content Delivery Network (CDN) to serve images 
# directly from Sydney, cutting latency to 10ms.
#
# Third, the request hits a Reverse Proxy (like Nginx) which acts as a shield, 
# stripping SSL and routing traffic.
#
# Fourth, the backend needs to read the user's profile. Querying the SQL database 
# takes 50ms. The backend uses a Cache (like Redis) to store the profile in RAM, 
# fetching it in 0.5ms.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand DNS Resolution.
# - Differentiate Forward vs Reverse Proxies.
# - Master Caching Strategies (Cache-Aside vs Write-Through).
#
# ==============================================================================
"""

import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE REVERSE PROXY SHIELD
# ==============================================================================
class ReverseProxy:
    """
    Simulates Nginx or HAProxy.
    Sits IN FRONT of your web servers, intercepting all internet traffic.
    """
    def __init__(self):
        self.internal_servers = {
            "/api/users": "Server-Alpha-10.0.0.1",
            "/api/payments": "Server-Beta-10.0.0.2"
        }
        
    def handle_request(self, path: str) -> str:
        print(f"[Reverse Proxy] Intercepted incoming request for: {path}")
        print("[Reverse Proxy] Terminating SSL/TLS connection (CPU intensive!)...")
        
        if path in self.internal_servers:
            internal_ip = self.internal_servers[path]
            print(f"[Reverse Proxy] Routing unencrypted traffic to internal DB at {internal_ip}")
            return f"Success from {internal_ip}"
        else:
            return "404 Not Found"

def demonstrate_reverse_proxy():
    section_header("Reverse Proxy Architecture")
    proxy = ReverseProxy()
    print("User types: https://my-app.com/api/users")
    response = proxy.handle_request("/api/users")
    print(f"\nUser receives: {response}")
    print("\nThe user has NO IDEA that 'Server-Alpha-10.0.0.1' exists.")
    print("The Reverse Proxy perfectly shields the internal architecture from the internet!")


# ==============================================================================
# 4. CACHING STRATEGIES (REDIS SIMULATION)
# ==============================================================================
class SlowDatabase:
    def __init__(self):
        self.data = {"user_1": "John Doe Profile Data"}
        
    def read(self, key: str) -> str:
        print("[SQL DB] Executing expensive disk seek... (50ms)")
        time.sleep(0.05) # Simulate slow disk I/O
        return self.data.get(key, "Null")
        
    def write(self, key: str, value: str) -> None:
        print("[SQL DB] Executing expensive disk write... (50ms)")
        time.sleep(0.05)
        self.data[key] = value

class RedisCache:
    def __init__(self):
        self.cache = {}
        
    def get(self, key: str) -> str:
        print("[Redis] Checking lightning-fast RAM... (0.5ms)")
        return self.cache.get(key, None)
        
    def set(self, key: str, value: str) -> None:
        print("[Redis] Writing to RAM... (0.5ms)")
        self.cache[key] = value

class CacheAsideApp:
    """
    Cache-Aside (Lazy Loading):
    The Application is fully responsible for managing both the Cache and the DB.
    It checks the Cache first. If it misses, it fetches from DB, and THEN manually 
    updates the Cache for the future.
    """
    def __init__(self):
        self.db = SlowDatabase()
        self.cache = RedisCache()
        
    def get_user(self, user_id: str) -> str:
        # 1. Check Cache!
        cached_data = self.cache.get(user_id)
        
        if cached_data is not None:
            print("[APP] Cache HIT! Returning instantly.")
            return cached_data
            
        # 2. Cache MISS! Fallback to SQL Database.
        print("[APP] Cache MISS! Falling back to database...")
        db_data = self.db.read(user_id)
        
        # 3. Manually populate the cache for the NEXT time!
        if db_data != "Null":
            print("[APP] Populating Cache with fetched DB data...")
            self.cache.set(user_id, db_data)
            
        return db_data

def demonstrate_cache_aside():
    section_header("Caching Strategy (Cache-Aside)")
    
    app = CacheAsideApp()
    
    print("--- First Request (Cold Cache) ---")
    start = time.time()
    data = app.get_user("user_1")
    end = time.time()
    print(f"Time Taken: {(end - start)*1000:.2f} ms")
    
    print("\n--- Second Request (Warm Cache) ---")
    start = time.time()
    data = app.get_user("user_1")
    end = time.time()
    print(f"Time Taken: {(end - start)*1000:.2f} ms")
    print("\nThe second request bypassed the slow SQL disk entirely by reading purely from RAM!")


def run_all_labs():
    demonstrate_reverse_proxy()
    demonstrate_cache_aside()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the fundamental difference between a Forward Proxy and a Reverse Proxy?
   Answer: A Forward Proxy shields the CLIENT. (e.g., A corporate VPN). When you are at work and go to Facebook, your computer sends the request to the corporate Forward Proxy. The proxy sends the request to Facebook. Facebook thinks the Proxy is the one making the request; it has no idea who you are. A Reverse Proxy shields the SERVER. (e.g., Nginx, Cloudflare). When you go to Google, you hit Google's Reverse Proxy. The proxy then quietly fetches the data from a hidden internal database. You have no idea what internal IP address actually served your data. Forward = Protects the Requester. Reverse = Protects the Responder.

2. Explain the "Cache-Aside" (Lazy Loading) strategy and its fatal flaw regarding Data Staleness.
   Answer: In Cache-Aside, the application first asks the Cache (Redis). If the data isn't there (a Miss), it asks the Database (SQL), and then explicitly writes that data back into the Cache so the next request is fast. The flaw is Data Staleness. Suppose User A updates their profile. The application writes the new profile to the SQL database. But what about the old profile currently sitting in Redis? If the application forgets to explicitly manually delete or overwrite the Redis entry, Redis will continue infinitely serving the old, stale profile to all future users! This is why Cache Invalidation (setting Time-To-Live TTLs) is notoriously considered one of the hardest problems in Computer Science.

3. What is a CDN (Content Delivery Network) and how does it defeat the speed of light?
   Answer: A CDN is essentially a globally distributed network of massive Caches explicitly designed for static files (Images, CSS, JS, Videos). If a Netflix server is in California, a user in London physically cannot pull the video faster than the speed of light allows across fiber optic cables (~150ms round trip). This causes buffering. A CDN places a physical proxy server in London. The first time a London user requests the video, the London CDN pulls it from California. But it caches the video locally. For the next 10 million London users, they pull the video from the server located 5 miles down the street from their house, resulting in 5ms latency, effectively subverting geographic latency constraints.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Basics & Caching) Completed.")
