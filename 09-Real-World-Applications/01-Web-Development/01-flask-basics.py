"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (WEB DEVELOPMENT - FLASK BASICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer wants to build a web API. They look at Django, see 500 pages 
# of documentation, complex ORMs, and strict directory structures, and give up.
#
# A senior engineer understands "Microframeworks". They install `Flask`. In 
# exactly 5 lines of code, they bind a Python function to a TCP Network Socket 
# on Port 80, instantly exposing their mathematical logic to the entire global 
# internet via the HTTP protocol. Flask strips away the monolithic architecture, 
# providing absolute minimalist control over routing and requests.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the physical architecture of WSGI (Web Server Gateway Interface).
# - Master HTTP Routing and the Decorator Pattern (`@app.route`).
# - Master Request Parsing (JSON payloads) and Response Serialization.
#
# ==============================================================================
"""

# Gracefully handle the absence of Flask
try:
    from flask import Flask, request, jsonify
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    
import threading
import time
import requests

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MICROFRAMEWORK ARCHITECTURE (WSGI)
# ==============================================================================
# `__name__` tells Flask exactly where to look for hidden resources (templates/static)
if HAS_FLASK:
    app = Flask(__name__)

    # --- 1. THE ROUTING ENGINE (Decorator Pattern) ---
    # The `@app.route` decorator physically registers the string "/api/v1/status" 
    # into a central Hash Table (the URL Map). When an HTTP request hits the 
    # server, Flask hashes the URL path and instantly teleports execution to this function!
    @app.route('/api/v1/status', methods=['GET'])
    def health_check():
        """A standard GET endpoint returning JSON."""
        # Flask's `jsonify` automatically serializes the Python Dictionary into 
        # a JSON byte-string and injects the `Content-Type: application/json` header!
        return jsonify({
            "status": "online",
            "version": "1.0.0",
            "database": "connected"
        }), 200

    # --- 2. DYNAMIC ROUTING (URL Variables) ---
    # The `<string:username>` syntax intercepts the URL physically!
    # e.g., `/api/v1/users/admin` -> username="admin"
    @app.route('/api/v1/users/<string:username>', methods=['GET'])
    def get_user(username):
        """Dynamic URL parsing."""
        # In a real app, this queries a Database!
        known_users = ["admin", "ceo", "developer"]
        if username.lower() in known_users:
            return jsonify({"user": username, "status": "active"}), 200
        else:
            return jsonify({"error": "User not found"}), 404

    # --- 3. PAYLOAD PARSING (POST Requests) ---
    @app.route('/api/v1/data', methods=['POST'])
    def receive_data():
        """Intercepting and validating inbound JSON payloads."""
        # The `request` object is a Thread-Local global!
        # It mathematically points to the specific HTTP request of the CURRENT thread.
        if not request.is_json:
            return jsonify({"error": "Payload must be JSON"}), 400
            
        payload = request.get_json()
        
        # Validation
        if "sensor_id" not in payload or "temperature" not in payload:
            return jsonify({"error": "Missing required fields"}), 400
            
        # Processing (e.g., writing to Database)
        sensor = payload["sensor_id"]
        temp = payload["temperature"]
        
        return jsonify({
            "message": "Data received successfully",
            "processed": {"id": sensor, "status": "logged"}
        }), 201


# ==============================================================================
# 4. MATHEMATICAL PROOF OF EXECUTION
# ==============================================================================
def run_flask_server():
    """Boots the Flask WSGI server in the background."""
    # We turn off the massive Flask startup logging for the lab output
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Run on port 5050 to avoid conflicts
    app.run(host='127.0.0.1', port=5050, debug=False, use_reloader=False)

def demonstrate_flask_api():
    section_header("Performance Proof: Localhost API Execution")
    
    if not HAS_FLASK:
        print("  [ERROR] Flask is not installed. Run `pip install flask requests`.")
        return
        
    print("  [INIT] Booting Flask WSGI Server on a background OS Thread...")
    server_thread = threading.Thread(target=run_flask_server, daemon=True)
    server_thread.start()
    
    # Wait 1 second to ensure the TCP socket is fully bound to Port 5050
    time.sleep(1.0)
    
    base_url = "http://127.0.0.1:5050"
    
    print("\n  [TEST 1: Standard GET Request]")
    res1 = requests.get(f"{base_url}/api/v1/status")
    print(f"    -> Status Code: {res1.status_code}")
    print(f"    -> Response:    {res1.json()}")
    
    print("\n  [TEST 2: Dynamic Routing (Success)]")
    res2 = requests.get(f"{base_url}/api/v1/users/admin")
    print(f"    -> Status Code: {res2.status_code}")
    print(f"    -> Response:    {res2.json()}")
    
    print("\n  [TEST 3: Dynamic Routing (404 Not Found)]")
    res3 = requests.get(f"{base_url}/api/v1/users/hacker")
    print(f"    -> Status Code: {res3.status_code}")
    print(f"    -> Response:    {res3.json()}")
    
    print("\n  [TEST 4: POST Request (Valid JSON)]")
    payload = {"sensor_id": "XJ-99", "temperature": 42.5}
    res4 = requests.post(f"{base_url}/api/v1/data", json=payload)
    print(f"    -> Status Code: {res4.status_code}")
    print(f"    -> Response:    {res4.json()}")
    
    print("\n  [TEST 5: POST Request (Missing Fields Error)]")
    bad_payload = {"sensor_id": "XJ-99"} # Missing temperature!
    res5 = requests.post(f"{base_url}/api/v1/data", json=bad_payload)
    print(f"    -> Status Code: {res5.status_code}")
    print(f"    -> Response:    {res5.json()}")
    
    print("\n  [SHUTDOWN] Terminating Client. Background Server thread will die automatically.")


def run_all_labs():
    demonstrate_flask_api()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is WSGI (Web Server Gateway Interface), and why doesn't Flask just talk to the internet directly?"
   Senior Answer: "The internet speaks TCP/IP and HTTP bytes. Flask speaks Python Objects. They are mathematically incompatible. If Flask tried to bind directly to Port 80 and parse raw HTTP byte streams, it would be vulnerable to catastrophic security flaws (like Slowloris attacks) and terrible concurrency. WSGI (PEP 3333) is the architectural bridge. A robust C-level web server (like Gunicorn or Nginx) binds to the physical hardware port, handles the DDOS protection, SSL decryption, and OS-level socket buffering. Once the raw HTTP request is safely assembled, Gunicorn translates it into a standard Python Dictionary (the WSGI `environ`) and passes it to Flask. Flask executes the business logic, returns a WSGI response, and Gunicorn translates it back into HTTP bytes. Flask is just a WSGI Application, not a Web Server."

2. Interviewer: "The `request` object in Flask is imported globally at the top of the file. If 1,000 users send a POST request at the exact same millisecond, why doesn't User B accidentally read User A's `request` data?"
   Senior Answer: "This is the brilliance of 'Thread-Local Storage' (implemented via Werkzeug's `LocalProxy`). While `request` physically looks like a standard global variable, it is actually an intelligent proxy object. When you access `request.json`, the proxy mathematically queries the Operating System to identify the unique ID of the specific OS Thread currently executing the code. It uses that Thread ID as a key to look up the data in a hidden internal Dictionary. Because User A and User B are being processed on entirely different OS Threads (or Greenlets), they each cryptographically retrieve their own isolated HTTP payload, mathematically guaranteeing Thread Safety while maintaining a beautifully clean developer API."

3. Interviewer: "What is the architectural difference between Flask and Django, and when must you strictly choose one over the other?"
   Senior Answer: "Django is a 'Batteries-Included Monolith'. It enforces a rigid directory structure and ships with a deeply integrated ORM, Admin Panel, and Authentication system. It is mandatory when building a massive, data-heavy, full-stack CMS or monolithic SaaS where standard relational architecture is required. Flask is a 'Microframework'. It provides absolutely nothing except URL routing and WSGI compliance. You must manually install SQLAlchemy if you want a Database. It is mathematically mandatory when building high-speed microservices, serverless AWS Lambda functions, or simple REST APIs where the bloat of Django's 500-table Admin system would cause catastrophic memory overhead and architectural friction."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Web Development (Flask Basics) Completed.")
