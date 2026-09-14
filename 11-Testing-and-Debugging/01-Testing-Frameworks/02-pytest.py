"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (PYTEST & ADVANCED FIXTURES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses the built-in `unittest` framework. To test 5 different 
# users logging into a system, they write 5 completely separate `test_user_X()` 
# functions, resulting in 300 lines of mathematically redundant boilerplate code. 
# They spend more time writing `self.assertEqual()` than writing business logic.
#
# A senior software engineer uses `pytest`. They understand that Python's `unittest` 
# is a heavy, Java-style OOP relic. `pytest` mathematically strips away the OOP 
# boilerplate. It uses raw Python `assert` statements and dynamically rewrites 
# the Python bytecode at runtime to generate massive, detailed crash reports. 
# Furthermore, the engineer uses `@pytest.mark.parametrize` to mathematically 
# compress 50 different edge-case tests into a single 5-line function, slashing 
# repository size by 80%.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `pytest` architecture (bypassing OOP `TestCase` inheritance).
# - Execute Dependency Injection via `@pytest.fixture`.
# - Architect Data-Driven Testing via `@pytest.mark.parametrize`.
#
# ==============================================================================
"""

import pytest

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CODE WE ARE TESTING)
# ==============================================================================
class ShoppingCart:
    """A standard e-commerce state machine."""
    def __init__(self):
        self.items = {}
        
    def add_item(self, product: str, price: float, quantity: int = 1):
        if price < 0 or quantity <= 0:
            raise ValueError("Invalid mathematical parameters for Cart.")
        if product in self.items:
            self.items[product]["quantity"] += quantity
        else:
            self.items[product] = {"price": price, "quantity": quantity}
            
    def calculate_total(self) -> float:
        total = sum(data["price"] * data["quantity"] for data in self.items.values())
        return round(total, 2)


# ==============================================================================
# 4. THE PYTEST ARCHITECTURE (THE TESTS)
# ==============================================================================
# Notice: We do NOT inherit from `unittest.TestCase`!
# Notice: We do NOT use `self.assertEqual()`! We just use pure Python `assert`!

# --- FIXTURES (DEPENDENCY INJECTION) ---
# Pytest Fixtures are a massive architectural upgrade over `unittest.setUp()`.
# Instead of polluting the global `self` state, Fixtures mathematically inject 
# the requested objects directly into the test function's arguments!

@pytest.fixture
def empty_cart() -> ShoppingCart:
    """Mathematically guarantees a pristine, empty cart for any test that requests it."""
    return ShoppingCart()

@pytest.fixture
def populated_cart(empty_cart: ShoppingCart) -> ShoppingCart:
    """Fixtures can mathematically inject OTHER Fixtures! (Chained Dependency Injection)"""
    empty_cart.add_item("Laptop", 1000.0, 1)
    empty_cart.add_item("Mouse", 50.0, 2)
    return empty_cart


# --- THE TESTS ---

def test_initial_cart_state(empty_cart: ShoppingCart):
    """Proves the Fixture successfully injected a pristine cart."""
    # Pytest magically intercepts this basic `assert`. If it fails, Pytest dynamically 
    # de-compiles the bytecode to tell you EXACTLY what values caused the failure!
    assert empty_cart.calculate_total() == 0.0
    assert len(empty_cart.items) == 0


def test_populated_cart_total(populated_cart: ShoppingCart):
    """Proves chained fixture injection."""
    # Laptop (1000) + 2 Mice (100) = 1100
    assert populated_cart.calculate_total() == 1100.0


def test_add_item_validation(empty_cart: ShoppingCart):
    """Proves exception handling without `self.assertRaises`."""
    # Pytest context manager for Exception validation
    with pytest.raises(ValueError, match="Invalid mathematical parameters"):
        empty_cart.add_item("Monitor", -300.0, 1)


# --- PARAMETRIZATION (DATA-DRIVEN TESTING) ---
# This is the most powerful feature in Pytest.
# We test 4 completely different edge cases using a single mathematical function!
@pytest.mark.parametrize(
    "product, price, qty, expected_total",
    [
        ("Keyboard", 100.0, 1, 100.0),     # Standard
        ("Cable", 9.99, 3, 29.97),         # Float Math
        ("Server", 5000.0, 10, 50000.0),   # Volume
        ("Sticker", 0.0, 500, 0.0)         # Edge Case: Free item
    ]
)
def test_massive_cart_permutations(empty_cart: ShoppingCart, product, price, qty, expected_total):
    """
    Pytest will mathematically execute this function 4 separate times, 
    injecting the specific row of data into the arguments on each pass!
    """
    empty_cart.add_item(product, price, qty)
    assert empty_cart.calculate_total() == expected_total


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE TEST RUNNER)
# ==============================================================================
def demonstrate_pytest():
    section_header("Unit Testing: The Pytest Architecture")
    
    print("  [EXECUTION] Normally, you run Pytest from the Terminal: `pytest test_cart.py`")
    print("  For this lab, we execute it programmatically...\n")
    
    # We execute pytest programmatically on THIS exact file!
    # -v = Verbose (show every test)
    # -q = Quiet (hide traceback clutter)
    pytest.main(["-v", "-q", __file__])
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  Notice how the parametrized test generated 4 distinct test outputs")
    print("  from a single block of Python code!")


def run_all_labs():
    demonstrate_pytest()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "How does `pytest` allow us to use the standard Python `assert x == y` statement, whereas `unittest` forces us to use `self.assertEqual(x, y)` to get decent error messages?"
   Senior Answer: "AST (Abstract Syntax Tree) Rewriting. In raw Python, if `assert 5 == 6` fails, the interpreter just throws an `AssertionError` with absolutely zero context about what the numbers were. `unittest` solves this using explicit methods (`assertEqual`) that manually capture and print the variables. `pytest` solves it at the compiler level. When you run Pytest, it physically intercepts the Python compilation process, reads the AST, and mathematically rewrites the bytecode of your `assert` statements at runtime. It injects complex introspection logic so that if the assert fails, it prints a massive, colored diff showing exactly what the left side and right side of the equation evaluated to."

2. Interviewer: "What is the architectural advantage of Pytest `@pytest.fixture` over standard `unittest.setUp()`?"
   Senior Answer: "Explicit Dependency Injection vs Implicit Global State. In `unittest`, `setUp()` runs blindly before every test and dumps objects into `self.obj`. If a test doesn't actually need that object, it wastes CPU cycles generating it anyway. More dangerously, `self` becomes a global dumping ground for state, making tests tightly coupled to the class architecture. Pytest Fixtures are mathematically injected *only* if the test function explicitly requests them in its arguments (`def test_a(empty_cart):`). This proves exactly what dependencies the test relies on, allows Fixtures to be shared globally across hundreds of files via `conftest.py`, and allows Fixtures to inject other Fixtures, forming a highly modular Dependency Graph."

3. Interviewer: "Why is `@pytest.mark.parametrize` mathematically superior to just writing a `for` loop inside a single test function?"
   Senior Answer: "Test Isolation and Failure Granularity. If you write a `for` loop to test $100$ edge cases inside `test_cart()`, and the $3$rd edge case fails, the `assert` statement throws an Exception. The Exception mathematically halts the entire function immediately! The remaining $97$ edge cases will never execute, blinding you to the true extent of the system failure. When you use `@pytest.mark.parametrize`, Pytest mathematically registers each row of data as an independent, fully isolated Test Case in the test runner. If the $3$rd parameter fails, Pytest logs the failure and flawlessly executes the remaining $97$ tests, providing an absolute, comprehensive health report of the architecture."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Pytest) Completed.")
