"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (MOCK INTERVIEWS - LIVE PAIR PROGRAMMING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Unlike algorithmic whiteboard interviews where the interviewer acts as a silent 
# judge, Pair Programming interviews simulate a real day on the job. You will be 
# dropped into an existing, undocumented, broken codebase and asked to add a 
# feature or fix a bug while the interviewer "pairs" with you.
#
# A junior engineer ignores the interviewer, aggressively deletes code they don't 
# understand, breaks the test suite, and fails to communicate their intent.
#
# A senior engineer treats the interviewer as a teammate. They read the existing 
# code aloud, write unit tests *before* modifying the core logic (TDD), use IDE 
# debugging tools explicitly, and continuously solicit feedback ("I'm thinking 
# of refactoring this monolithic function into two smaller ones, what do you think?").
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Codebase Navigation (Reading undocumented code).
# - Master Test-Driven Development (TDD) in a live environment.
# - Master Collaborative Communication.
#
# ==============================================================================
"""

import time
import sys
import unittest

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

def simulate_typing(text: str, delay: float = 0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ==============================================================================
# 3. THE EXISTING CODEBASE (DELIBERATELY BUGGY)
# ==============================================================================
# In a pair programming interview, you are given code like this and told:
# "Our inventory system is crashing when users try to buy out-of-stock items, 
# and the discount logic is mathematically incorrect. Please fix it and add tests."

class InventorySystem:
    def __init__(self):
        self.inventory = {"laptop": 5, "mouse": 10, "keyboard": 0}
        
    def purchase_item(self, item: str, quantity: int, has_coupon: bool):
        # BUG 1: Does not handle items that do not exist in the dictionary!
        # BUG 2: Allows purchasing more items than are physically in stock!
        self.inventory[item] -= quantity
        
        base_price = 100
        # BUG 3: Applies discount incorrectly (multiplies by 0.2 instead of subtracting 20%)
        if has_coupon:
            return (base_price * quantity) * 0.2
        return base_price * quantity


# ==============================================================================
# 4. LIVE PAIR PROGRAMMING SIMULATION
# ==============================================================================
def live_coding_simulation():
    section_header("Live Simulation: Pair Programming & TDD")
    
    simulate_typing("INTERVIEWER: 'Here is our `InventorySystem`. It has a few bugs. Can you fix them?'")
    
    simulate_typing("\n[STAGE 1: CODEBASE NAVIGATION (Reading Aloud)]")
    simulate_typing("CANDIDATE: 'Let me read through the existing code first.'")
    simulate_typing("CANDIDATE: 'I see a dictionary acting as a database. I see a `purchase_item` method.'")
    simulate_typing("CANDIDATE: 'Immediately, I notice that `self.inventory[item] -= quantity` will throw a `KeyError` if the item isn't mapped.'")
    simulate_typing("CANDIDATE: 'It also doesn't check if `self.inventory[item] < quantity`, allowing negative stock.'")
    simulate_typing("INTERVIEWER: 'Great catches. How do you want to proceed?'")
    
    simulate_typing("\n[STAGE 2: TEST-DRIVEN DEVELOPMENT (TDD)]")
    simulate_typing("CANDIDATE: 'Before I change the core logic, I am going to write a Unit Test that mathematically enforces the correct behavior. That way, we have a safety net.'")
    
    # --------------------------------------------------------------------------
    # CANDIDATE WRITES TESTS FIRST
    # --------------------------------------------------------------------------
    simulate_typing("\n--- WRITING TESTS ---")
    simulate_typing("def test_out_of_stock(self):")
    simulate_typing("    system = InventorySystem()")
    simulate_typing("    with self.assertRaises(ValueError):")
    simulate_typing("        system.purchase_item('keyboard', 1, False)")
    
    simulate_typing("\n[STAGE 3: REFACTORING (Collaborative)]")
    simulate_typing("CANDIDATE: 'Now I will refactor the core logic to make the tests pass.'")
    simulate_typing("CANDIDATE: 'I'm thinking of throwing a `ValueError` for invalid stock. Does that align with our error-handling standards?'")
    simulate_typing("INTERVIEWER: 'Yes, `ValueError` is perfectly fine here.'")
    
    # --------------------------------------------------------------------------
    # CANDIDATE FIXES THE CODE
    # --------------------------------------------------------------------------
    simulate_typing("\n--- FIXING CORE LOGIC ---")
    
    class FixedInventorySystem:
        def __init__(self):
            self.inventory = {"laptop": 5, "mouse": 10, "keyboard": 0}
            
        def purchase_item(self, item: str, quantity: int, has_coupon: bool):
            # FIX 1: Explicit Dictionary Check
            if item not in self.inventory:
                raise KeyError(f"Item '{item}' does not exist in the catalog.")
                
            # FIX 2: Mathematical Stock Check
            if self.inventory[item] < quantity:
                raise ValueError(f"Insufficient stock for '{item}'.")
                
            self.inventory[item] -= quantity
            
            base_price = 100
            total_price = base_price * quantity
            
            # FIX 3: Correct Discount Mathematics
            if has_coupon:
                return total_price * 0.8 # 20% off means they pay 80%
            return total_price
            
    simulate_typing("CANDIDATE: 'The fixes are implemented. Dictionary bounds are protected, stock mathematics are validated, and the discount calculation now subtracts instead of overriding.'")
    simulate_typing("INTERVIEWER: 'Looks solid. Good job treating this like a real production environment.'")


def run_all_labs():
    live_coding_simulation()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is Test-Driven Development (TDD) highly recommended in a Pair Programming interview, even if the interviewer doesn't explicitly ask for tests?"
   Senior Answer: "In a Pair Programming interview, the interviewer is evaluating your engineering maturity. Junior developers write chaotic code and test it by printing to the console. Senior developers establish mathematical contracts (Unit Tests) *before* mutating architecture. Writing a test first proves that you deeply understand the edge cases (e.g., triggering a `ValueError` on zero stock), and it gives the interviewer confidence that you are a safe, predictable developer who will not break the production codebase if hired."

2. Interviewer: "If you encounter a piece of code you don't understand during the interview, what is the optimal way to handle it?"
   Senior Answer: "You must never silently delete it or ignore it. Pair programming is a test of communication. The optimal approach is to explicitly vocalize your confusion to your 'pair' (the interviewer). Say: 'I am looking at line 42. It seems to be caching the result, but I don't fully understand the invalidation logic. Could you explain the architectural intent here?' This demonstrates humility, team-oriented problem solving, and prevents you from catastrophically breaking a system you don't fully comprehend."

3. Interviewer: "In the fixed code, why use `raise ValueError` instead of just `return False` or `return 'Error'` when a user tries to buy an out-of-stock item?"
   Senior Answer: "Returning a boolean or a string from a function that normally returns a numeric `float` (the price) violently breaks the Type Contract of the function (violating Python Type Hinting standards). Furthermore, if the caller forgets to check if the return value is `False`, they might accidentally bill the customer for `$0.00`! By explicitly raising an Exception (`ValueError`), we halt the physical execution thread. The caller is mathematically forced to acknowledge and handle the failure via a `try/except` block, guaranteeing that corrupted state data cannot propagate further into the payment systems."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Mock Interviews (Live Pair Programming) Completed.")
