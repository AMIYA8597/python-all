"""
# ==============================================================================
# LABORATORY: STRUCTURAL PATTERN MATCHING (PYTHON 3.10+)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Introduced in Python 3.10, `match/case` is not just a switch-statement. It is 
# a powerful destructuring tool that can unpack JSON payloads, parse complex AST 
# trees, and validate object states cleanly. It replaces massive `if/elif/else` 
# blocks and `isinstance` checks.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand simple matching and the wildcard `_`.
# - Master sequence matching (lists/tuples) and the `*rest` operator.
# - Master dictionary (mapping) matching for JSON payloads.
# - Master Object matching and the `__match_args__` dunder attribute.
# - Use "Guard" clauses (`if`) inside cases.
#
# ==============================================================================
"""

from typing import Dict, Any, List
from dataclasses import dataclass

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SEQUENCE MATCHING & GUARDS
# ==============================================================================

def execute_command(command: str):
    """
    Destructures a string command into a list and matches specific structural patterns.
    """
    parts = command.split()
    
    match parts:
        # Matches exactly one word: "quit" or "exit"
        case ["quit"] | ["exit"]:
            print("  [System] Exiting gracefully.")
            
        # Matches exactly two words, binding the second word to `filename`
        case ["load", filename]:
            print(f"  [Action] Loading file: {filename}")
            
        # Matches exactly three words, but only if the guard clause is True
        case ["save", filename, force] if force == "--force":
            print(f"  [Action] Force saving file: {filename}")
            
        # Matches "drop" followed by ANY number of items (packed into `items`)
        case ["drop", *items]:
            print(f"  [Action] Dropping {len(items)} items: {items}")
            
        # The wildcard `_` acts as the default / fallback case
        case _:
            print(f"  [Error] Unknown command syntax: '{command}'")

def demonstrate_sequences():
    section_header("Sequence Matching and Guards")
    
    execute_command("load data.csv")
    execute_command("save data.csv --force")
    execute_command("save data.csv --soft") # Falls through to default due to guard
    execute_command("drop sword shield potion helmet")
    execute_command("quit")


# ==============================================================================
# 4. DICTIONARY (MAPPING) MATCHING
# ==============================================================================

def process_api_response(response: Dict[str, Any]):
    """
    Matches JSON-like payloads perfectly. Notice we don't have to specify 
    ALL the keys, just the ones we care about matching!
    """
    match response:
        # Matches if status=200 AND it has a 'data' key which contains a list
        case {"status": 200, "data": [*items]}:
            print(f"  [200 OK] Received {len(items)} items.")
            
        # Matches if status=404 (and binds the error message if it exists)
        case {"status": 404, "error": msg}:
            print(f"  [404 Not Found] {msg}")
            
        # Matches if status=500, extracting the trace, capturing all OTHER keys into **kwargs
        case {"status": 500, "trace": trace, **rest}:
            print(f"  [500 Server Error] Trace: {trace}")
            print(f"  [500] Additional context: {rest}")
            
        case _:
            print("  [Unknown] Invalid response format.")

def demonstrate_mapping():
    section_header("Dictionary (Mapping) Matching")
    
    process_api_response({"status": 200, "data": ["user1", "user2"], "timestamp": 1234})
    process_api_response({"status": 404, "error": "User not found"})
    process_api_response({"status": 500, "trace": "NullPointer", "server": "us-east-1"})


# ==============================================================================
# 5. OBJECT MATCHING & __MATCH_ARGS__
# ==============================================================================

@dataclass
class ClickEvent:
    x: int
    y: int
    button: str

@dataclass
class KeyEvent:
    key: str
    is_pressed: bool

def process_event(event: Any):
    match event:
        # We can match on the Class type and its attributes!
        case ClickEvent(x=0, y=0, button="left"):
            print("  [Event] Left click on the Origin (0,0).")
            
        # Dataclasses automatically generate `__match_args__`, allowing positional matching!
        # ClickEvent(x, y, button)
        case ClickEvent(x, y, "right"):
            print(f"  [Event] Right click at coordinates ({x}, {y}).")
            
        case KeyEvent(key="Esc", is_pressed=True):
            print("  [Event] Escape key PRESSED. Pausing game.")
            
        case KeyEvent(key, pressed):
            state = "pressed" if pressed else "released"
            print(f"  [Event] Key '{key}' was {state}.")
            
        case _:
            print("  [Event] Unrecognized event.")

def demonstrate_objects():
    section_header("Object Matching & __match_args__")
    
    process_event(ClickEvent(0, 0, "left"))
    process_event(ClickEvent(150, 200, "right"))
    process_event(KeyEvent("Esc", True))
    process_event(KeyEvent("Space", False))


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Is `match/case` identical to a `switch` statement in C or Java?
   Answer: No. A `switch` statement only evaluates equality on primitive values. Python's `match/case` performs structural destructuring, type checking, and length checking on complex nested data structures (lists, dicts, objects).

2. How do you unpack an arbitrary number of items in a sequence match?
   Answer: Use the `*` operator (e.g., `case ["drop", *items]:`).

3. When matching a dictionary, do you need to match all keys in the dictionary?
   Answer: No. Dictionary matching only checks for the PRESENCE of the specified keys. Extra keys in the dictionary are ignored unless captured with `**rest`.

4. Why can you do `case ClickEvent(0, 0, "left"):` on a dataclass, but not a normal class by default?
   Answer: Positional object matching requires the class to define the `__match_args__` tuple, which maps positional arguments to attribute names. The `@dataclass` decorator generates this automatically. For normal classes, you must define it manually, or use keyword matching: `case ClickEvent(x=0, y=0)`.
"""

if __name__ == "__main__":
    demonstrate_sequences()
    demonstrate_mapping()
    demonstrate_objects()
    print("\n[SUCCESS] Laboratory: Pattern Matching Completed.")
