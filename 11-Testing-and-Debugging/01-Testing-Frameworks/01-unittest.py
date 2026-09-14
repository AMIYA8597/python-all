"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (MOCKING & DEPENDENCY INJECTION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a unit test for a function that calculates currency 
# exchange rates. The function calls an external HTTP API to get the current 
# rate of the Euro. When the CI/CD pipeline runs the test on a server with no 
# internet access, the test violently crashes. Worse, if the API rate-limits 
# the pipeline, the test randomly fails (Flaky Test), causing the entire 
# deployment to halt.
#
# A senior testing engineer understands "Dependency Mocking". They realize that 
# a Unit Test must only test the internal mathematical logic of the function, NOT 
# the external internet connection. They use `unittest.mock.patch` to mathematically 
# intercept the HTTP call at runtime and force it to instantly return a hardcoded 
# JSON string (`{"rate": 1.10}`). The test executes in 0.001 seconds, requires 
# zero internet, and mathematically guarantees the internal logic is flawless.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Dependency Injection and architectural isolation.
# - Execute `unittest.mock.patch` to hijack CPython function pointers at runtime.
# - Architect deterministic Test Doubles (Mocks, Stubs, Spies).
#
# ==============================================================================
"""

import unittest
from unittest.mock import patch, MagicMock
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CODE WE ARE TESTING)
# ==============================================================================
class BankAPI:
    """Simulates an external HTTP API that is slow, expensive, or requires internet."""
    def fetch_exchange_rate(self, currency: str) -> float:
        # We simulate a massive 5-second network delay!
        # If a Unit Test suite has 1,000 tests, this would take 1.3 hours to run!
        print(f"    [NETWORK] Reaching out to external Bank API for {currency}...")
        time.sleep(5) 
        if currency == "EUR": return 0.85
        if currency == "GBP": return 0.75
        raise ValueError("Unsupported Currency")


class FinancialProcessor:
    """The actual business logic we want to mathematically test."""
    def __init__(self, api: BankAPI):
        # We inject the dependency!
        self.api = api
        
    def convert_usd(self, amount: float, target_currency: str) -> float:
        """Converts USD to target currency by asking the external API for the rate."""
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
            
        rate = self.self_api_call_wrapper(target_currency)
        return round(amount * rate, 2)
        
    def self_api_call_wrapper(self, currency: str) -> float:
        # A wrapper to make patching easier to understand
        return self.api.fetch_exchange_rate(currency)


# ==============================================================================
# 4. THE AUTOMATED TEST SUITE (WITH MOCKING)
# ==============================================================================
class TestFinancialProcessor(unittest.TestCase):
    
    # --- TEST 1: THE DISASTER (No Mocking) ---
    # We do NOT run this test in the lab because it sleeps for 5 seconds.
    # def test_conversion_slow(self):
    #     api = BankAPI()
    #     processor = FinancialProcessor(api)
    #     result = processor.convert_usd(100.0, "EUR")
    #     self.assertEqual(result, 85.0)

    # --- TEST 2: THE ARCHITECTURAL SOLUTION (Mocking) ---
    # The `@patch` decorator dynamically hijacks the `fetch_exchange_rate` function 
    # pointer in the Python memory space precisely during this test execution!
    @patch.object(BankAPI, 'fetch_exchange_rate')
    def test_conversion_with_mock(self, mock_fetch: MagicMock):
        """Mathematically verifies logic without touching the internet."""
        
        # 1. ARRANGE: We command the hijacked pointer to return a fake, hardcoded value!
        # We bypass the 5-second sleep completely.
        mock_fetch.return_value = 0.90
        
        # We boot the engine
        api = BankAPI()
        processor = FinancialProcessor(api)
        
        # 2. ACT: We execute the function
        result = processor.convert_usd(100.0, "EUR")
        
        # 3. ASSERT: We mathematically prove the business logic ($100 * 0.90 = $90.00)
        self.assertEqual(result, 90.0)
        
        # 4. SPY ASSERTION: We mathematically prove that our business logic 
        # actually attempted to call the external API with the correct parameters!
        mock_fetch.assert_called_once_with("EUR")

    # --- TEST 3: EXCEPTION MOCKING (Failure Injection) ---
    @patch.object(BankAPI, 'fetch_exchange_rate')
    def test_conversion_api_failure(self, mock_fetch: MagicMock):
        """Mathematically simulates an external API outage."""
        # We command the hijacked pointer to violently crash!
        mock_fetch.side_effect = ValueError("API Outage")
        
        api = BankAPI()
        processor = FinancialProcessor(api)
        
        # We mathematically prove our system bubbles up the crash correctly
        with self.assertRaises(ValueError) as context:
            processor.convert_usd(100.0, "JPY")
            
        self.assertTrue("API Outage" in str(context.exception))


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE TEST RUNNER)
# ==============================================================================
def demonstrate_mocking():
    section_header("Unit Testing: Mocking Dependencies")
    
    print("  [EXECUTION] Booting the Automated Test Runner...")
    print("  The runner will execute Mocked tests in 0.001 seconds, completely bypassing")
    print("  the 5-second network delay hardcoded into the BankAPI.\n")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFinancialProcessor)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  Tests Run: {test_result.testsRun}")
    if test_result.wasSuccessful():
        print("  -> [FLAWLESS] The Financial Engine passed all tests via RAM-based Mocking!")


def run_all_labs():
    demonstrate_mocking()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If we are Mocking the external API to just return a hardcoded number, what exactly are we testing? Aren't we cheating the test?"
   Senior Answer: "Architectural Boundary Isolation. In a 'Unit Test', you are mathematically mandated to test ONLY the internal logic of a single function. In `convert_usd`, the logic is multiplying the `amount` by the `rate` and rounding to 2 decimal places. We are testing that multiplication and rounding logic. We are NOT testing if the European Central Bank API is currently online. If we want to test the actual internet connection, we write an 'Integration Test' (which runs separately and infrequently). Mocking ensures that if the Unit Test fails, it is a 100% mathematical guarantee that our Multiplication logic is broken, not our Wi-Fi."

2. Interviewer: "What is the architectural difference between `mock.return_value` and `mock.side_effect`?"
   Senior Answer: "Static payload versus Dynamic Execution. `return_value` mathematically commands the Mock object to instantly return a static payload (e.g., `0.90`) every single time it is called. It requires absolutely zero CPU evaluation. `side_effect` commands the Mock to dynamically execute Python code. You can use it to force the Mock to violently raise an Exception (`side_effect = ValueError()`), or you can assign it an Iterable (`side_effect = [0.90, 0.95]`) to return different values on sequential calls, allowing you to simulate complex network degradation or retry logic."

3. Interviewer: "Under the hood, how does the `@patch` decorator mathematically hijack a function pointer inside the CPython interpreter?"
   Senior Answer: "Dynamic Dict Mutation. In Python, everything is a first-class Object, and classes are backed by mathematical `__dict__` structures. When the `@patch` decorator wraps a test function, it executes a Context Manager during the setup phase. It dynamically locates the target function pointer in the global memory space (e.g., `BankAPI.fetch_exchange_rate`), temporarily stores the original memory address, and overwrites the `__dict__` entry with a pointer to a synthetic `MagicMock` object. When the test finishes, the teardown phase executes, and it flawlessly restores the original memory address, mathematically guaranteeing that subsequent tests are not poisoned by the synthetic mock."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Mocking) Completed.")
