"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (UNIT TESTING BEST PRACTICES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a test called `test_everything()`. It is 250 lines 
# long. It initializes the database, creates a user, buys a product, refunds 
# the product, and asserts 45 different variables. When the test fails on 
# line 112, the entire pipeline crashes, and nobody knows if the failure was 
# caused by the checkout system, the refund system, or a database timeout. 
# The test is a "God Test" and is mathematically impossible to maintain.
#
# A senior testing engineer architects their suite using strict "Best Practices". 
# They use the AAA Pattern (Arrange, Act, Assert). They ensure a single test 
# has exactly ONE mathematical reason to fail (Single Responsibility Principle). 
# They use explicit, declarative test names (`test_refund_fails_when_receipt_invalid`).
# When a test fails in CI/CD, the engineer knows exactly what broke without 
# even looking at the code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the AAA Pattern (Arrange, Act, Assert).
# - Execute explicit, deterministic Test Naming Conventions.
# - Understand the anti-pattern of "God Tests" and Test Interdependence.
#
# ==============================================================================
"""

import unittest

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC
# ==============================================================================
class SubscriptionService:
    def __init__(self):
        self.active_users = []
        
    def upgrade_to_pro(self, user_id: str, payment_status: str) -> bool:
        if not user_id:
            raise ValueError("User ID cannot be empty.")
            
        if payment_status == "DECLINED":
            return False
            
        if user_id not in self.active_users:
            self.active_users.append(user_id)
            return True
            
        return False # Already a pro user


# ==============================================================================
# 4. THE JUNIOR ANTI-PATTERN (THE GOD TEST)
# ==============================================================================
class BadTestSubscriptionService(unittest.TestCase):
    """
    ANTI-PATTERN WARNING! 
    This is how you write terrible tests that developers hate maintaining.
    """
    def test_stuff(self): # BAD: Vague name
        # Doing 5 things at once
        svc = SubscriptionService()
        
        # Test 1
        res = svc.upgrade_to_pro("user1", "PAID")
        self.assertTrue(res)
        self.assertIn("user1", svc.active_users)
        
        # Test 2
        res2 = svc.upgrade_to_pro("user1", "PAID")
        self.assertFalse(res2) # Should fail because already pro
        
        # Test 3
        res3 = svc.upgrade_to_pro("user2", "DECLINED")
        self.assertFalse(res3)
        self.assertNotIn("user2", svc.active_users)
        
        # If Test 2 fails, Test 3 never runs! The developer is blind to Test 3's status!


# ==============================================================================
# 5. THE SENIOR ARCHITECTURE (AAA PATTERN & ISOLATION)
# ==============================================================================
class TestSubscriptionService(unittest.TestCase):
    """
    ARCHITECTURAL PURITY.
    Every single test validates exactly ONE path of execution.
    """
    
    def test_upgrade_adds_user_when_payment_succeeds(self):
        """Standard success path."""
        # --- ARRANGE (Setup the exact mathematical state) ---
        service = SubscriptionService()
        target_user = "usr_999"
        
        # --- ACT (Execute the exact function under test) ---
        result = service.upgrade_to_pro(target_user, "PAID")
        
        # --- ASSERT (Mathematically prove the state mutated correctly) ---
        self.assertTrue(result, "Service should return True on successful upgrade.")
        self.assertIn(target_user, service.active_users, "User ID was not added to the active list.")

    def test_upgrade_fails_when_payment_declined(self):
        """Negative path execution."""
        # ARRANGE
        service = SubscriptionService()
        target_user = "usr_888"
        
        # ACT
        result = service.upgrade_to_pro(target_user, "DECLINED")
        
        # ASSERT
        self.assertFalse(result, "Service should return False when payment is declined.")
        self.assertNotIn(target_user, service.active_users, "User was illegally granted Pro status on a declined card.")

    def test_upgrade_returns_false_for_existing_pro_user(self):
        """Edge case execution (Idempotency)."""
        # ARRANGE
        service = SubscriptionService()
        service.active_users.append("usr_777") # Pre-populate the state!
        
        # ACT
        result = service.upgrade_to_pro("usr_777", "PAID")
        
        # ASSERT
        self.assertFalse(result, "Service should return False if user is already upgraded.")
        # Ensure it wasn't added twice
        self.assertEqual(service.active_users.count("usr_777"), 1)


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE TEST RUNNER)
# ==============================================================================
def demonstrate_best_practices():
    section_header("Unit Testing: AAA Pattern Best Practices")
    
    print("  [EXECUTION] Booting Test Runner for the Architecturally Pure Suite...")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSubscriptionService)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  Tests Run: {test_result.testsRun}")
    if test_result.wasSuccessful():
        print("  -> [FLAWLESS] The AAA Pattern produced granular, deterministic validations.")


def run_all_labs():
    demonstrate_best_practices()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the AAA Pattern, and why does visually separating its blocks inside the test function matter architecturally?"
   Senior Answer: "Arrange, Act, Assert. It is the absolute foundational architecture of a clean Unit Test. 'Arrange' sets up the mock data, instantiates the class, and prepares the exact state. 'Act' is mathematically restricted to a *single* line of code: the invocation of the function being tested. 'Assert' executes the validation checks. Visually separating these blocks (often with whitespace or comments) forces the developer to maintain test purity. If the 'Act' phase requires $10$ lines of code, the developer instantly realizes their underlying Business Logic is tightly coupled and architecturally flawed, prompting a refactor of the actual application."

2. Interviewer: "Why is the 'God Test' anti-pattern (`test_everything`) so destructive to CI/CD pipelines?"
   Senior Answer: "Test Fragility and Masking. A 'God Test' violates the Single Responsibility Principle by asserting $20$ different behaviors sequentially. In Python `unittest`, the exact millisecond an `assert` fails, an Exception is thrown, and the entire test function halts permanently. If Assertion $\#3$ fails, Assertions $4$ through $20$ are completely bypassed and never execute. The CI/CD pipeline fails, but the developer is mathematically blind to the status of the remaining $17$ assertions. By splitting the God Test into $20$ independent AAA tests, the CI/CD pipeline evaluates every single assertion independently, providing a granular, $100\\%$ complete health report of the system, even if $5$ of the tests fail simultaneously."

3. Interviewer: "What is 'TDD' (Test-Driven Development), and how does it alter the mathematical flow of software engineering?"
   Senior Answer: "Red, Green, Refactor. Standard development writes the business logic first, and the test second (or never). TDD mathematically inverts this. You are forced to write the Unit Test *before* the business logic exists. The test attempts to run and violently fails (Red). You then write the absolute minimum amount of production code required to make the test pass (Green). Finally, you optimize the code without fear of breaking it (Refactor). TDD guarantees $100\\%$ test coverage, but more importantly, it forces the developer to design the function's API from the perspective of the *consumer*, resulting in highly modular, loosely coupled architecture."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Best Practices) Completed.")
