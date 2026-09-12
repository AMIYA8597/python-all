"""
Flask Web Development Basics

This module provides a comprehensive, production-ready guide to building web applications
with Flask, a lightweight WSGI web application framework for Python.

Why it exists:
Flask is heavily used in the industry for microservices, quick API prototyping, and full-stack
web applications. It provides the essential tools for web routing, request handling, and response
formatting without enforcing a specific project layout or forcing the use of specific libraries (like Django does).

Beginner Explanation:
Imagine you own a restaurant. The waiter takes a customer's order (the HTTP Request), walks to
the kitchen, tells the chef what to make, and then brings the food back (the HTTP Response).
Flask is the system that connects the waiter to the right chef based on what the customer ordered (Routing).

Deep Technical Explanation:
Flask relies on the Werkzeug WSGI toolkit and the Jinja2 template engine. It uses decorators
to bind URLs to Python functions. In a production environment, Flask's built-in development
server should never be used; instead, it sits behind a production WSGI server (like Gunicorn)
and a reverse proxy (like Nginx).

This file demonstrates:
1. App initialization and Configuration.
2. Routing and HTTP Methods.
3. Request parsing (JSON, Query parameters).
4. Error Handling.
5. Unit testing a Flask application.

Run this file directly to start the development server.
"""

from flask import Flask, request, jsonify, make_response, abort
from typing import Dict, Any, Tuple
import unittest
import json

# ============================================================================
# 1. Application Setup & Configuration
# ============================================================================
# We initialize the Flask application. In a real app, config would be loaded
# from environment variables or a separate config.py file.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret-key-for-development-only'

# Mock Database for demonstration purposes
USERS_DB = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob", "role": "user"}
}

# ============================================================================
# 2. Routing and Endpoints
# ============================================================================

@app.route('/', methods=['GET'])
def index() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint.
    Returns a simple JSON response indicating the API is running.
    """
    return jsonify({"message": "Welcome to the Flask API", "status": "healthy"}), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """
    Fetch a user by ID. Demonstrates URL parameters and 404 handling.
    """
    user = USERS_DB.get(user_id)
    if not user:
        # abort(404) triggers the error handler defined below
        abort(404, description=f"User {user_id} not found.")
    
    return jsonify({"id": user_id, "data": user}), 200


@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user. Demonstrates parsing JSON request bodies.
    
    Expected JSON: {"name": "Charlie", "role": "user"}
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 415
    
    data: Dict[str, Any] = request.get_json()
    
    # Input validation
    if 'name' not in data or 'role' not in data:
        return jsonify({"error": "Missing required fields: 'name', 'role'"}), 400
        
    new_id = max(USERS_DB.keys()) + 1 if USERS_DB else 1
    USERS_DB[new_id] = {"name": data['name'], "role": data['role']}
    
    return jsonify({"message": "User created", "id": new_id}), 201


@app.route('/api/search', methods=['GET'])
def search():
    """
    Search endpoint demonstrating URL query parameters.
    Example: /api/search?q=Alice&limit=10
    """
    query = request.args.get('q', default='', type=str)
    limit = request.args.get('limit', default=10, type=int)
    
    # Dummy search logic
    results = [{"match": "item1"}, {"match": "item2"}]
    
    return jsonify({
        "query": query,
        "limit": limit,
        "results": results[:limit]
    }), 200

# ============================================================================
# 3. Global Error Handling
# ============================================================================

@app.errorhandler(404)
def resource_not_found(e):
    """Provides a consistent JSON response for 404 errors."""
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Generic fallback for unhandled exceptions."""
    return jsonify(error="An internal server error occurred."), 500

# ============================================================================
# 4. Interview Questions & Considerations
# ============================================================================
"""
Common Interview Questions:
Q1: What is the difference between Django and Flask?
A1: Django is a "batteries-included" framework (ORM, admin panel, auth built-in). Flask is a micro-framework; it provides routing and templating but leaves database and auth decisions to the developer.

Q2: How does Flask handle concurrent requests?
A2: Flask's development server is synchronous by default (though it supports threading). In production, WSGI servers like Gunicorn with gevent or async workers handle concurrency. Flask 2.0+ also supports async route handlers natively using Python's `async def`.

Q3: What is the Application Context vs. Request Context?
A3: Request context keeps track of request-level data (`request`, `session`). Application context keeps track of application-level data (`current_app`, `g`). They are dynamically bound to the current thread/greenlet handling the request.

Security Concerns:
- Cross-Site Scripting (XSS): Ensure Jinja templates auto-escape HTML (done by default).
- CSRF: If using forms/sessions, implement CSRF protection (e.g., using Flask-WTF).
- Secrets: Never hardcode `SECRET_KEY` in source control.
"""

# ============================================================================
# 5. Unit Tests
# ============================================================================

class FlaskBasicTests(unittest.TestCase):
    
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True 

    def test_index_health_check(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_get_existing_user(self):
        response = self.app.get('/api/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['data']['name'], 'Alice')

    def test_get_missing_user(self):
        response = self.app.get('/api/users/999')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        payload = {"name": "Dave", "role": "admin"}
        response = self.app.post('/api/users', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    def test_create_user_bad_request(self):
        payload = {"name": "Eve"} # Missing role
        response = self.app.post('/api/users', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    # When running normally, start the server or the tests.
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Remove 'test' so unittest framework doesn't get confused
        sys.argv.pop(1)
        unittest.main()
    else:
        # Run development server
        app.run(host='0.0.0.0', port=5000)
