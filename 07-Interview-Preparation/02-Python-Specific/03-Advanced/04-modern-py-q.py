"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - MODERN PYTHON)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I noticed you wrote `if match: result = match.group(1)` on a 
# separate line. How would you compress this logic using Python 3.8 features?"
#
# If you don't know the Walrus Operator (`:=`), you look like a developer who 
# hasn't updated their skills since 2018. 
#
# Interviewer: "I have a function `def connect(host, port)`. I want to guarantee 
# that nobody can call it like `connect(port=80, host='localhost')`. I want to 
# mathematically enforce positional arguments only."
#
# If you don't know the `/` and `*` function signature modifiers introduced in 
# Python 3.8, you will fail the API design portion of the interview.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Walrus Operator (`:=`) for Assignment Expressions.
# - Master Positional-Only (`/`) and Keyword-Only (`*`) arguments.
# - Understand Structural Pattern Matching (Deep Dives and Guards).
#
# ==============================================================================
"""

import re
from dataclasses import dataclass

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE WALRUS OPERATOR (:=)
# ==============================================================================
def demonstrate_walrus():
    section_header("The Walrus Operator (Assignment Expressions)")
    
    data = "ERROR: Failed to connect to DB."
    
    print("--- THE OLD WAY (Python 3.7) ---")
    match = re.search(r"ERROR: (.*)", data)
    if match:
        print(f"  Old way extracted: {match.group(1)}")
        
    print("\n--- THE NEW WAY (Python 3.8+) ---")
    # The Walrus Operator allows you to ASSIGN a variable and EVALUATE it in the 
    # exact same mathematical statement!
    if (match := re.search(r"ERROR: (.*)", data)):
        print(f"  Walrus extracted : {match.group(1)}")
        
    print("\nThis saves lines of code and tightly scopes variables inside While ")
    print("loops (e.g., `while (chunk := file.read(8192)): process(chunk)`).")


# ==============================================================================
# 4. API DESIGN: POSITIONAL-ONLY (/) & KEYWORD-ONLY (*)
# ==============================================================================
def strict_api_function(host, port, /, *, timeout, retries=3):
    """
    `/` means: Everything BEFORE this slash MUST be Positional-Only!
    `*` means: Everything AFTER this star MUST be Keyword-Only!
    
    Why? If you change the internal variable name of 'host' to 'ip_address' later,
    you will break 1,000 users' code if they were calling `connect(host='...')`.
    By forcing Positional-Only, they CANNOT use the keyword, giving you absolute 
    freedom to rename your internal variables without breaking external APIs!
    """
    print(f"  [API] Connecting to {host}:{port} (Timeout: {timeout}s, Retries: {retries})")

def demonstrate_api_design():
    section_header("API Design (Positional & Keyword Modifiers)")
    
    print("Executing a highly strict API function...")
    
    # SUCCESS
    strict_api_function("127.0.0.1", 8080, timeout=5)
    
    # CRASH 1: Trying to use a Keyword for a Positional-Only arg
    # strict_api_function(host="127.0.0.1", port=8080, timeout=5) -> TypeError!
    
    # CRASH 2: Trying to use a Positional for a Keyword-Only arg
    # strict_api_function("127.0.0.1", 8080, 5) -> TypeError!
    
    print("\nThe `/` modifier protects the API designer (Allows renaming variables).")
    print("The `*` modifier protects the API consumer (Forces explicit readability for booleans/configs).")


# ==============================================================================
# 5. PATTERN MATCHING (DEEP DATA EXTRACTION)
# ==============================================================================
@dataclass
class Point:
    x: int
    y: int

def evaluate_coordinates(pt: Point):
    """
    Python 3.10 match/case doesn't just match dictionaries; it perfectly 
    destructures Custom Objects and Dataclasses!
    """
    match pt:
        case Point(x=0, y=0):
            print("  [Match] Dead Center (Origin).")
        case Point(x=0, y=y_val):
            # Mathematically extracts the Y value dynamically!
            print(f"  [Match] On the Y-Axis at {y_val}.")
        case Point(x=x_val, y=0):
            print(f"  [Match] On the X-Axis at {x_val}.")
        case Point(x=x_val, y=y_val) if x_val == y_val:
            # Guard Clause! (Executes arbitrary Python code during the match!)
            print(f"  [Match] On the diagonal (y=x) at {x_val}.")
        case Point(x=x_val, y=y_val):
            print(f"  [Match] Somewhere in space at {x_val}, {y_val}.")

def demonstrate_pattern_matching_deep():
    section_header("Pattern Matching (Object Destructuring)")
    
    pts = [Point(0, 0), Point(0, 5), Point(3, 3), Point(10, 20)]
    
    for p in pts:
        evaluate_coordinates(p)


def run_all_labs():
    demonstrate_walrus()
    demonstrate_api_design()
    demonstrate_pattern_matching_deep()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "When designing a public API library (like Requests or Django), why is the Positional-Only modifier (`/`) absolutely critical?"
   Senior Answer: "When you expose a function like `def calculate(value):`, users will naturally call it using Keyword Arguments: `calculate(value=10)`. Two years later, you decide the variable name `value` is confusing, and you rename it to `def calculate(temperature):`. You just completely shattered the codebase of every single user who relied on the `value=` keyword! By forcing the API to be Positional-Only (`def calculate(value, /):`), users are mathematically forbidden from writing `value=10`. They MUST write `calculate(10)`. Because the keyword is never exposed to the public, you can freely rename your internal variables 100 times without ever breaking backward compatibility."

2. Interviewer: "Why did Python introduce the Walrus Operator (`:=`)? Isn't it just an ugly shortcut?"
   Senior Answer: "The Walrus operator is NOT just syntactic sugar; it solves a severe architectural scope leak. Without the Walrus operator, if you want to read a file chunk by chunk, you must write a massive `while True:` loop, read the chunk, check `if not chunk: break`, and then process it. This leaks variables into the wider scope and breaks readability. The Walrus operator allows you to write `while (chunk := file.read(1024)): process(chunk)`. It evaluates the network/file I/O, assigns it to a variable, and runs the boolean truthiness check mathematically in a single execution step, creating perfect, tightly-scoped loop architectures."

3. Interviewer: "In Python 3.10's `match/case`, what is a 'Guard Clause' and why is it necessary?"
   Senior Answer: "Structural Pattern Matching is purely declarative; it mathematically matches the *shape* of an object (e.g., `case Point(x, y):`). However, it cannot execute complex mathematical logic natively (e.g., checking if `x > y`). A Guard Clause (`if x > y`) allows you to inject arbitrary, Turing-complete Python code directly into the pattern match. The CPython engine will first verify the structural shape, extract the variables into local scope, and then execute the Guard Clause. If the Guard returns `False`, the match is instantly aborted and execution falls through to the next `case` statement smoothly, providing immense algorithmic flexibility."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Modern Python) Completed.")
