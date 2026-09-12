"""
Debugging Strategies Masterclass

Learning Objectives:
1. Understand high-level methodologies for debugging (e.g., Rubber Duck, Divide and Conquer).
2. Implement structured logging as a proactive debugging strategy.
3. Learn how to isolate bugs using binary search (bisection) principles.

Concept Explanation:
Debugging is not just about tools; it's a systematic process of deduction.
- Rubber Duck Debugging: Explaining your code line-by-line to an inanimate object.
- Divide and Conquer / Bisection: Narrowing down the source of an error by halving the search space.
- Defensive Programming: Using assertions and strict typing to catch errors early.
- Structured Logging: Emitting logs with context (JSON) rather than plain text for easier querying.
"""

import logging
import json
import unittest
from typing import List, Callable, Any

# --- Basic Implementation ---
def setup_structured_logging():
    """Sets up a basic structured logger."""
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_obj = {
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "line": record.lineno
            }
            return json.dumps(log_obj)

    logger = logging.getLogger("strategy_logger")
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding multiple handlers in tests
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(JsonFormatter())
        logger.addHandler(ch)
    
    return logger

logger = setup_structured_logging()

def defensive_division(a: float, b: float) -> float:
    """Demonstrates defensive programming using assertions."""
    assert isinstance(a, (int, float)), "a must be numeric"
    assert isinstance(b, (int, float)), "b must be numeric"
    if b == 0:
        logger.error("Attempted division by zero", extra={"a": a, "b": b})
        raise ValueError("Cannot divide by zero")
    return a / b

# --- Intermediate Implementation ---
def find_first_failing_commit(commits: List[int], is_failing: Callable[[int], bool]) -> int:
    """
    Demonstrates Divide and Conquer (Bisection) strategy.
    Finds the first commit that fails using binary search O(log N).
    commits are ordered sequentially.
    """
    left, right = 0, len(commits) - 1
    first_failing = -1
    
    while left <= right:
        mid = (left + right) // 2
        if is_failing(commits[mid]):
            first_failing = commits[mid]
            right = mid - 1 # Look earlier
        else:
            left = mid + 1 # Look later
            
    return first_failing

# --- Advanced Implementation ---
class SystemStateObserver:
    """Demonstrates tracing state changes to debug complex interactions."""
    def __init__(self):
        self.state_history = []
        self._current_state = "INIT"

    @property
    def state(self):
        return self._current_state

    @state.setter
    def state(self, new_state: str):
        logger.info(f"State transition: {self._current_state} -> {new_state}")
        self.state_history.append((self._current_state, new_state))
        self._current_state = new_state

    def simulate_process(self):
        self.state = "PROCESSING"
        try:
            # Simulate work
            res = defensive_division(10, 0)
        except ValueError:
            self.state = "ERROR"
        else:
            self.state = "COMPLETED"

# --- Performance Analysis ---
"""
Performance Analysis:
- Structured logging (JSON parsing) is slower than plain text logging. Use asynchronously 
  or in background threads for high-throughput systems.
- Bisection (Binary Search) reduces debugging time from O(N) to O(log N) when searching 
  through ordered historical data (like git commits).
- Assertions (`assert`) can be globally disabled in Python using the `-O` flag, 
  incurring zero performance penalty in production.
"""

# --- Edge Cases ---
"""
Edge Cases Handled:
- Handled all-passing or all-failing commit histories in binary search.
- Safe division handling zero and invalid types.
"""

# --- Interview Challenge ---
"""
Interview Challenge:
Question: What is Rubber Duck Debugging and why does it work?
Answer: It is the process of explaining your code line-by-line to an inanimate object. 
It works because the act of verbalizing assumptions forces the brain to evaluate them critically, 
often revealing logical flaws that reading code silently masks.
"""

# --- Tests ---
class TestDebuggingStrategies(unittest.TestCase):
    def test_defensive_division(self):
        self.assertEqual(defensive_division(10, 2), 5.0)
        with self.assertRaises(ValueError):
            defensive_division(10, 0)
        with self.assertRaises(AssertionError):
            defensive_division("10", 2)

    def test_bisection(self):
        commits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # Suppose commit 6 and onwards fail
        def is_failing(c): return c >= 6
        
        first = find_first_failing_commit(commits, is_failing)
        self.assertEqual(first, 6)

        # All pass
        def all_pass(c): return False
        self.assertEqual(find_first_failing_commit(commits, all_pass), -1)

    def test_state_observer(self):
        obs = SystemStateObserver()
        obs.simulate_process()
        self.assertEqual(obs.state, "ERROR")
        self.assertEqual(len(obs.state_history), 2)
        self.assertEqual(obs.state_history[0], ("INIT", "PROCESSING"))
        self.assertEqual(obs.state_history[1], ("PROCESSING", "ERROR"))

if __name__ == "__main__":
    print("Running Debugging Strategies Masterclass Tests...")
    unittest.main()
