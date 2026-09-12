"""
## A. Concept Name
Structural Pattern Matching

## B. One-Sentence Definition
Structural Pattern Matching is a powerful control flow mechanism in Python 3.10+ that allows you to match the structure and content of data, extract variables, and apply conditional logic in a clean, readable way.

## C. Why Does This Exist?
To replace complex, nested `if-elif-else` chains with a more declarative, readable syntax, and to easily destructure complex data structures like JSON, abstract syntax trees, or objects.

## D. Intuition
Imagine checking a package delivery. Instead of opening the box, checking if it's a book, then checking the title, you just ask "Does this match the shape of a book with title X?" and the matching system unpacks it for you instantly.

## E. Real-Life Analogy
Sorting mail at a post office. You have different bins based on patterns: "If it looks like a postcard from New York, put it here", "If it's a package heavier than 5kg, put it there". You match the shape and attributes of the item, not just its exact value.

## F. Mental Model
Think of it as a combination of a `switch` statement (checking values), destructuring assignment (unpacking tuples/lists/objects), and type checking (isinstance), all rolled into one fluent syntax.

## G. Visual Explanation
```
Data: {'type': 'click', 'x': 10, 'y': 20}
         |
    match data:
         |
    case {'type': 'click', 'x': x, 'y': y}: ---> Matches! 
                                                 Binds: x=10, y=20
```

## H. Formal Explanation
The `match` statement takes an expression and compares its value to successive patterns given as one or more `case` blocks. This is superficially similar to a switch statement in C, Java or JavaScript, but it's more similar to pattern matching in languages like Rust or Haskell. It can match types, structures, and values, and bind variables to parts of the matched structure.

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
N/A - This is a language-level syntax feature.

## K. Library / Production Implementation (if applicable)
N/A - Implemented in CPython's compiler and bytecode.

## L. Trace (walk through example)
Given `expr = ('+', 1, ('*', 2, 3))`
1. `match expr:` evaluates to the tuple.
2. `case int(val):` fails (it's a tuple, not an int).
3. `case ('+', left, right):` matches! `left` is bound to `1`, `right` is bound to `('*', 2, 3)`.
4. Returns `evaluate_ast(1) + evaluate_ast(('*', 2, 3))`

## M. Complexity
- Time Complexity: O(N) where N is the number of cases. However, Python optimizes literal matching to use dictionary lookups internally (O(1)) where possible. Object and sequence matching requires sequential checks.
- Space Complexity: O(1) beyond the bound variables.

## N. Common Mistakes
1. Forgetting that `case _:` must be the last case (it's a catch-all).
2. Using variables instead of literals in cases: `case my_var:` matches *anything* and binds it to `my_var`, it does *not* check if the value equals the existing `my_var`! To match against an existing variable's value, use a guard: `case x if x == my_var:`.
3. Not realizing that `_` doesn't bind a variable.

## O. Common Confusions
1. "Is it just a switch statement?" No, it destructures data and matches types/shapes, not just values.
2. "Why did my case with `Point(x, y)` match a different object?" Pattern matching for objects relies on `__match_args__` if keyword arguments are not explicitly used.

## P. When To Use
- Parsing complex, nested data structures (JSON, APIs).
- Processing commands or abstract syntax trees.
- Implementing state machines.
- When you have long `isinstance` and type-checking `if-elif` chains.

## Q. When NOT To Use
- Simple value comparisons where a dictionary mapping or basic `if-elif` is clearer.
- When supporting Python versions < 3.10.

## R. Trade-offs
- Readability: Greatly improves readability for complex structural checks, but might over-complicate simple value checks.
- Compatibility: Requires Python 3.10+.

## S. Debugging
- Check order of cases! The first match wins.
- Ensure variables in cases are meant to *bind*, not compare. If you want to compare against a constant, use dotted names (e.g., `Constants.VALUE`) or guards.

## T. Memory Hook (a short memorable principle)
"Match the shape, bind the parts."

## U. Active Recall (questions before answers)
1. What does `case _:` do?
2. How do you match a dictionary with keys "x" and "y"?
3. How do you check if a matched variable meets a condition?

## V. Practice (exercises)
Write a pattern matching function to process JSON-like responses:
`{"status": "success", "data": [...]}` or `{"status": "error", "message": "..."}`.

## W. Interview Question
Challenge: Write a function `evaluate_ast` that takes a nested tuple representing a mathematical expression and evaluates it. E.g., `('+', 1, ('*', 2, 3))` should return 7.

## X. Project Connection
Used heavily in CLI argument parsing, compilers, event handlers, and web framework routing.
"""

from dataclasses import dataclass
from typing import Any, Dict, Union


# --- Basic Implementation: Literal and Sequence Matching ---
def http_status(status: int) -> str:
    """Basic matching of literal values."""
    match status:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:  # Wildcard match (default case)
            return "Unknown status"


def process_command(command: str) -> str:
    """Matching sequences (lists/tuples) and capturing variables."""
    match command.split():
        case ["quit" | "exit" | "bye"]:
            return "Quitting program"
        case ["load", filename]:
            return f"Loading {filename}..."
        case ["save", filename]:
            return f"Saving to {filename}..."
        case ["move", x, y]:
            return f"Moving to ({x}, {y})"
        case _:
            return "Invalid command"


# --- Intermediate Implementation: Mapping and Guard Matching ---
def handle_event(event: Dict[str, Any]) -> str:
    """Matching dictionary structures and using guards."""
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"Clicked at {x}, {y}"
        case {"type": "keypress", "key": key} if key in ["esc", "q"]:
            return "Escape sequence triggered"
        case {"type": "keypress", "key": key}:
            return f"Pressed {key}"
        case _:
            return "Unknown event"


# --- Advanced Implementation: Object Pattern Matching ---
@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    start: Point
    end: Point


def analyze_shape(shape: Any) -> str:
    """Matching custom objects using structural matching."""
    match shape:
        case Point(x=0, y=0):
            return "Origin point"
        case Point(x=x, y=y) if x == y:
            return f"Point on the diagonal: {x}, {y}"
        case Point(x, y):
            return f"Point at {x}, {y}"
        case Line(start=Point(x=0, y=0), end=Point(x=x, y=y)):
            return f"Line starting from origin to {x}, {y}"
        case _:
            return "Not a recognized shape"


# --- Interview Challenge Solution ---
def evaluate_ast(expr: Union[int, tuple]) -> int:
    """
    Evaluates a nested tuple representing a mathematical expression.
    E.g., `('+', 1, ('*', 2, 3))` returns 7.
    """
    match expr:
        case int(val):
            return val
        case ('+', left, right):
            return evaluate_ast(left) + evaluate_ast(right)
        case ('*', left, right):
            return evaluate_ast(left) * evaluate_ast(right)
        case ('-', left, right):
            return evaluate_ast(left) - evaluate_ast(right)
        case _:
            raise ValueError("Invalid expression AST")


# --- Tests ---
def run_tests() -> None:
    print("Testing Pattern Matching...")

    # Literal matching
    assert http_status(200) == "OK"
    assert http_status(999) == "Unknown status"

    # Sequence matching
    assert process_command("load data.txt") == "Loading data.txt..."
    assert process_command("move 10 20") == "Moving to (10, 20)"
    assert process_command("invalid") == "Invalid command"

    # Mapping matching
    assert handle_event({"type": "click", "x": 100, "y": 200}) == "Clicked at 100, 200"
    assert handle_event({"type": "keypress", "key": "q"}) == "Escape sequence triggered"
    assert handle_event({"type": "keypress", "key": "a"}) == "Pressed a"

    # Object matching
    assert analyze_shape(Point(0, 0)) == "Origin point"
    assert analyze_shape(Point(5, 5)) == "Point on the diagonal: 5, 5"
    assert analyze_shape(Point(10, 20)) == "Point at 10, 20"
    assert analyze_shape(Line(Point(0, 0), Point(5, 10))) == "Line starting from origin to 5, 10"

    # AST Challenge
    ast = ('+', 1, ('*', 2, 3))
    assert evaluate_ast(ast) == 7

    print("All tests passed!")


if __name__ == "__main__":
    import sys
    if sys.version_info >= (3, 10):
        run_tests()
    else:
        print("Pattern matching requires Python 3.10 or higher. Skipping tests.")
