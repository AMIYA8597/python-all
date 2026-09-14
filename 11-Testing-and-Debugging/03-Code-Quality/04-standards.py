"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (CODING STANDARDS & PEP-8)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes an algorithm. It is mathematically flawless. But 
# they use Single-Letter Variables (`a`, `b`, `c`), they don't leave spaces 
# around operators (`x=y+1`), and they write a 300-character line of code that 
# stretches off the screen. Six months later, the system breaks. The original 
# developer is on vacation. A senior engineer looks at the code and literally 
# cannot understand what it does because the visual parsing complexity is O(N^2).
#
# A senior software architect enforces "PEP-8" (Python Enhancement Proposal 8). 
# PEP-8 is the absolute, mathematically proven global standard for Python syntax. 
# It dictates exactly where spaces go, how variables are named, and strictly 
# caps lines at 88 characters. When code complies perfectly with PEP-8, it achieves 
# "Cognitive Invisibility". Developers stop reading the *syntax* and start reading 
# the *business logic*, slashing onboarding and debugging time by 75%.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master PEP-8 Naming Conventions (snake_case vs PascalCase).
# - Execute Syntactical Readability (Whitespace, Line Length, Indentation).
# - Understand the "Zen of Python" (Explicit is better than implicit).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE "BAD" CODE)
# ==============================================================================
# WARNING: This code mathematically executes perfectly, but architecturally, 
# it is an absolute disaster that violates every rule of PEP-8.

def do_math(a,b,c=10):
    # No spaces around operators, single letter variables, mixed case
    if a>b:
        Result=a*b+c
    else:
        Result=a/b-c
    # Massive line length, impossible to read on a split-screen monitor
    final_output_string_that_is_way_too_long = "The result of the calculation between the two numbers is exactly: " + str(Result)
    return final_output_string_that_is_way_too_long


# ==============================================================================
# 4. THE ARCHITECTURAL SOLUTION (PEP-8 COMPLIANT)
# ==============================================================================
# This is the EXACT same logic, completely refactored to align with PEP-8 
# and the Zen of Python.

def calculate_financial_projection(revenue: float, costs: float, tax_rate: float = 10.0) -> str:
    """
    Calculates the final projection based on revenue vs costs.
    
    Args:
        revenue: Total incoming capital.
        costs: Total outgoing capital.
        tax_rate: The base tax modifier (defaults to 10.0).
    """
    # PEP-8: Spaces around operators (` > `, ` * `, ` + `)
    # Naming: snake_case for functions and variables, highly descriptive
    if revenue > costs:
        base_projection = (revenue * costs) + tax_rate
    else:
        base_projection = (revenue / costs) - tax_rate
        
    # PEP-8: f-strings for readability, avoiding massive string concatenation
    # Line length mathematically capped under 88 characters (Black formatter standard)
    return f"The final financial projection is exactly: {base_projection:.2f}"


# ==============================================================================
# 5. THE ZEN OF PYTHON (TIM PETERS)
# ==============================================================================
class ZenOfPythonSimulator:
    """
    The Zen of Python is a collection of 19 "Guiding Principles" for writing 
    computer programs that influence the design of the Python language.
    """
    @staticmethod
    def show_principles():
        print("  [THE ZEN OF PYTHON] Core Architectural Principles:")
        print("  1. Beautiful is better than ugly.")
        print("  2. Explicit is better than implicit.")
        print("  3. Simple is better than complex.")
        print("  4. Flat is better than nested.")
        print("  5. Sparse is better than dense.")
        print("  6. Readability counts.")
        print("  7. Errors should never pass silently.")


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_coding_standards():
    section_header("Code Quality: PEP-8 & Coding Standards")
    
    print("  [SCENARIO A: THE UNREADABLE CODE]")
    try:
        res1 = do_math(50.0, 20.0)
        print(f"    -> Executed successfully, but the syntax was painful.")
    except Exception as e:
        print(e)
        
    print("\n  [SCENARIO B: THE PEP-8 CODE]")
    try:
        # The variables are completely self-documenting!
        res2 = calculate_financial_projection(revenue=50.0, costs=20.0)
        print(f"    -> {res2}")
        print(f"    -> Executed successfully. Syntax was cognitively effortless.")
    except Exception as e:
        print(e)
        
    print("\n  [ARCHITECTURE PROOF]")
    ZenOfPythonSimulator.show_principles()


def run_all_labs():
    demonstrate_coding_standards()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does PEP-8 mandate that lines of code should generally not exceed 79 or 88 characters?"
   Senior Answer: "Split-Screen Ergonomics and Visual Parsing. In modern software engineering, developers rarely code in a single massive window. They use split-screen monitors (Code on the left, Terminal/Diff on the right) or 3-way merge conflict resolution screens. If a line of code is $200$ characters long, it mathematically forces the developer to scroll horizontally, breaking their flow state, or it forces the IDE to apply 'Word Wrap', which visually destroys the indentation logic of the Python script. Capping line length at 88 characters (the standard for the `Black` formatter) mathematically guarantees that the code will render flawlessly on any monitor, terminal, or GitHub Pull Request UI."

2. Interviewer: "What does 'Explicit is better than implicit' mean in the context of Python architecture?"
   Senior Answer: "Eradicating Magic. 'Implicit' code relies on hidden mechanics or assumed global state (e.g., importing `from math import *` and magically using `sin()` without knowing where it came from). This creates bugs that are mathematically impossible to trace. 'Explicit' code leaves a rigid, traceable mathematical paper trail. You write `import math`, and then you explicitly write `math.sin()`. When the next developer reads the code, they know with absolute $100\\%$ certainty exactly which library is executing the logic, dramatically reducing debugging time."

3. Interviewer: "Why is 'Flat is better than nested' a core architectural principle?"
   Senior Answer: "Cognitive Complexity Limits. When you write an `if` statement inside a `for` loop inside another `if` statement, you create physical indentation 'nesting'. The human brain can only hold about $4$ to $7$ discrete pieces of information in short-term memory (Miller's Law). Deeply nested code mathematically exceeds this cognitive limit because the developer must remember the state of $3$ different parent conditions just to understand the current line of code. By refactoring the logic to be 'Flat' (using 'Guard Clauses' to `return` early or `continue` early), the developer only ever has to hold $1$ mathematical state in their head at a time, eliminating logical errors."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Code Quality (Standards & PEP-8) Completed.")
