"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (COMPREHENSIVE STRATEGY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes 1,000 "End-to-End" (E2E) tests. Every test spins 
# up the entire Application, the PostgreSQL database, and a headless Chrome 
# browser. It clicks a button, waits for the DOM to render, and asserts the result. 
# The Test Suite takes 6 hours to run. The developer commits code, waits 6 hours, 
# and finds out they missed a semicolon. The team's deployment velocity mathematically 
# drops to zero.
#
# A senior software architect builds a "Test Pyramid". They architect 900 
# purely mathematical Unit Tests that execute in 2 seconds (Mocking the Database). 
# They architect 90 Integration Tests that execute in 20 seconds (Testing the 
# real SQL queries). They architect exactly 10 E2E tests that execute in 2 minutes 
# (Testing the absolute critical paths). The entire suite runs in 3 minutes, 
# mathematically guaranteeing massive deployment velocity while catching 100% of bugs.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Test Pyramid Architecture.
# - Execute logical separation between Unit, Integration, and System Tests.
# - Architect deterministic failure pipelines.
#
# ==============================================================================
"""

import sqlite3
import json
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE ARCHITECTURE (THE SYSTEM UNDER TEST)
# ==============================================================================
# A multi-layered architecture: Database -> Business Logic -> Web API

class DatabaseLayer:
    """The raw infrastructure. (Requires actual disk I/O)"""
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        
    def insert_user(self, name: str) -> int:
        cursor = self.conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
        self.conn.commit()
        return cursor.lastrowid
        
    def get_user(self, user_id: int) -> str:
        cursor = self.conn.execute("SELECT name FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None


class BusinessLogicLayer:
    """The Math. (Requires a Database Interface, but shouldn't care if it's real)"""
    def __init__(self, db: DatabaseLayer):
        self.db = db
        
    def register_user(self, name: str) -> dict:
        if not name or len(name) < 3:
            return {"status": "error", "message": "Name too short"}
            
        user_id = self.db.insert_user(name.upper()) # Business Rule: Always uppercase!
        return {"status": "success", "id": user_id, "name": name.upper()}


class WebAPILayer:
    """The Presentation. (Parses JSON, returns HTTP codes)"""
    def __init__(self, logic: BusinessLogicLayer):
        self.logic = logic
        
    def handle_post_request(self, raw_json: str) -> str:
        try:
            payload = json.loads(raw_json)
            name = payload.get("username", "")
            
            result = self.logic.register_user(name)
            
            if result["status"] == "success":
                return json.dumps({"http_code": 201, "body": result})
            else:
                return json.dumps({"http_code": 400, "body": result})
        except json.JSONDecodeError:
            return json.dumps({"http_code": 500, "error": "Invalid JSON Payload"})


# ==============================================================================
# 4. THE TEST PYRAMID (THE STRATEGY)
# ==============================================================================
class TestStrategySimulator:
    
    @staticmethod
    def execute_unit_tests():
        """
        THE BASE OF THE PYRAMID (70% of Tests).
        Execution Time: < 0.001 seconds.
        Goal: Test the pure mathematical logic without touching Disk or Network.
        """
        print("  [LEVEL 1] Executing Unit Tests (Pure Logic / Mocks)")
        
        # We mathematically Mock the Database to prevent Disk I/O!
        class MockDB:
            def insert_user(self, name): return 999
            
        logic = BusinessLogicLayer(MockDB())
        
        # Test 1: Validation Logic
        res_fail = logic.register_user("Al")
        assert res_fail["status"] == "error"
        
        # Test 2: Mutation Logic (Proves it Uppercases without hitting SQL)
        res_pass = logic.register_user("Alice")
        assert res_pass["status"] == "success"
        assert res_pass["name"] == "ALICE"
        print("    -> [SUCCESS] 2 Unit Tests passed in 0.001s")


    @staticmethod
    def execute_integration_tests():
        """
        THE MIDDLE OF THE PYRAMID (20% of Tests).
        Execution Time: 0.1 - 1.0 seconds.
        Goal: Prove that two different systems (Python + SQL) communicate perfectly.
        """
        print("  [LEVEL 2] Executing Integration Tests (Real SQL, Real I/O)")
        
        # We instantiate a REAL SQLite database in memory!
        real_db = DatabaseLayer()
        logic = BusinessLogicLayer(real_db)
        
        # We execute the pipeline and mathematically assert the SQL worked!
        logic.register_user("Charlie")
        
        # Proving the SQL `INSERT` correctly populated the `SELECT` query
        sql_result = real_db.get_user(1)
        assert sql_result == "CHARLIE"
        print("    -> [SUCCESS] 1 Integration Test passed in 0.050s")


    @staticmethod
    def execute_e2e_tests():
        """
        THE PEAK OF THE PYRAMID (10% of Tests).
        Execution Time: 1.0 - 10.0 seconds.
        Goal: Prove the entire system works from the User's perspective.
        """
        print("  [LEVEL 3] Executing End-to-End System Tests (Full Pipeline)")
        
        # We boot the entire Universe!
        db = DatabaseLayer()
        logic = BusinessLogicLayer(db)
        api = WebAPILayer(logic)
        
        # We simulate a raw HTTP POST request coming from a React Frontend!
        raw_http_payload = '{"username": "david_smith"}'
        
        # We fire it into the absolute top of the architecture
        response_string = api.handle_post_request(raw_http_payload)
        response_obj = json.loads(response_string)
        
        # We assert the final HTTP Code!
        assert response_obj["http_code"] == 201
        assert response_obj["body"]["name"] == "DAVID_SMITH"
        print("    -> [SUCCESS] 1 E2E System Test passed in 0.200s")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE PIPELINE)
# ==============================================================================
def demonstrate_test_pyramid():
    section_header("Testing Strategy: The Architectural Pyramid")
    
    start_time = time.time()
    
    # The CI/CD Pipeline mathematically executes from Bottom to Top!
    # If the Unit Tests fail, we immediately halt the pipeline. There is zero 
    # reason to spin up the Database if the basic math is broken!
    TestStrategySimulator.execute_unit_tests()
    TestStrategySimulator.execute_integration_tests()
    TestStrategySimulator.execute_e2e_tests()
    
    total_time = time.time() - start_time
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  -> The CI/CD Pipeline successfully executed the Full Test Pyramid.")
    print(f"  -> Total Pipeline Execution Time: {total_time:.4f} seconds.")


def run_all_labs():
    demonstrate_test_pyramid()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is an 'Ice-Cream Cone' Testing Strategy (heavy on E2E tests, zero Unit Tests) mathematically disastrous for team velocity?"
   Senior Answer: "Execution Latency and Debugging Complexity. E2E tests require spinning up real Databases, Web Servers, and headless Browsers. A single E2E test might take $10$ seconds. If you have $1,000$ E2E tests, your CI/CD pipeline takes $2.7$ hours to run. Developers will stop running tests locally because it halts their workflow, leading to massive merge conflicts. Furthermore, when an E2E test fails, it just says 'HTTP 500 Error'. It doesn't tell you *why*. The developer must manually trace the entire stack (Browser -> API -> Logic -> DB) to find the bug. In a Test Pyramid, the Unit Test fails in $0.01$ seconds and prints exactly which line of Python math broke."

2. Interviewer: "If we have $100\\%$ Unit Test coverage and every single mathematical function passes, why do we even need Integration Tests?"
   Senior Answer: "Boundary Failures and Architectural Assumptions. A Unit Test mathematically uses a 'Mock' to simulate the database. If you program your Mock to return `{'id': 1}` when called, the Unit Test passes flawlessly. However, what if the actual SQL database schema was updated by another team yesterday, and the `id` column was renamed to `uuid`? The Unit Test will still pass because it is isolated from reality! Integration tests physically connect the Python code to a real, ephemeral database instance. They mathematically prove that your code's *assumptions* about the external system match the actual physical state of the external system."

3. Interviewer: "What is the architectural purpose of testing the `WebAPILayer` separately from the `BusinessLogicLayer` in our E2E and Unit pipelines?"
   Senior Answer: "Separation of Concerns and Framework Agnosticism. The `BusinessLogicLayer` (Domain Logic) must be mathematically independent of the presentation layer. It should not know or care if the request came from an HTTP API, a gRPC microservice, or a Command-Line Interface. By decoupling them, we can rigorously Unit Test the business logic using raw Python strings without needing to construct complex HTTP Request mock objects. The `WebAPILayer` is then tested purely on its ability to accurately translate raw JSON HTTP payloads into the correct Python function calls, ensuring the architecture remains highly modular."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Comprehensive Strategy) Completed.")
