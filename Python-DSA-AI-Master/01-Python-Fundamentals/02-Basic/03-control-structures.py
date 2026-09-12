"""
# 03 - Control Structures: Conditionals, Loops, and Comprehensions

## A. Concept Name
Python Control Structures (Conditionals, Loops, Comprehensions, Pattern Matching)

## B. One-Sentence Definition
Control structures are the syntax blocks that dictate the order in which code executes, allowing programs to make decisions (if/else) and repeat actions (loops/comprehensions).

## C. Why Does This Exist?
A program that executes purely top-to-bottom can only do exactly one thing. Control structures allow a program to react dynamically to different inputs (branching) and process multiple pieces of data (iteration).

## D. Intuition
- **If/Else**: Like approaching a fork in a road with a sign. "If you are a car, take the highway; else, take the dirt road."
- **For Loop**: Like an assembly line worker. "For every item on this belt, paint it red."
- **While Loop**: Like boiling water. "While the water is not boiling, keep the heat on."

## E. Real-Life Analogy
**List Comprehension**: 
Instead of:
1. Get a basket.
2. For every apple in the tree:
3.   If the apple is red:
4.     Put it in the basket.

You simply say: "Give me a basket of all red apples from the tree."

## F. Mental Model
- Branching evaluates truthiness: `bool(expression)`.
- Iteration traverses over an `Iterable` protocol.
- Comprehensions are declarative single-pass filters/mappers over an iterable.

## G. Visual Explanation
```text
      [Condition]
     /           \
  True           False
  /               \
[If Block]     [Else Block]

      [Iterable]
          |
  (next item exists?) ---> False ---> [Else Block (if any)]
          | True
     [For Block]
          |
      (repeat)
```

## H. Formal Explanation
1. **Conditionals**: `if`, `elif`, `else`. Python uses "truthiness" to evaluate conditions.
2. **Loops**: 
   - `for x in iterable`: Iterates over collections (lists, strings, ranges).
   - `while condition`: Loops until a condition becomes False.
   - Loop modifiers: `break` (exit loop), `continue` (skip to next iteration), `pass` (do nothing).
3. **The `else` clause in loops**: Unique to Python. The `else` block executes *only if the loop finishes normally* (meaning it was NOT terminated by a `break`).
4. **Comprehensions**: Syntactic sugar for creating lists, dicts, or sets in a single line, optimized in C for performance.
5. **Structural Pattern Matching**: Introduced in Python 3.10 (`match / case`), it allows destructuring of complex objects (similar to switch-case in C, but much more powerful).

## I. Mathematical Foundation (if applicable)
N/A

## J. From-Scratch Implementation (if applicable)
N/A

## K. Library / Production Implementation (if applicable)
- Used implicitly everywhere in Python. Comprehensions heavily replace map/filter in Python codebases for better readability.

## L. Trace (walk through example)
Trace of a List Comprehension: `[x*2 for x in [1, 2] if x > 1]`
1. Python creates an empty list internally.
2. Iterates to first element: x = 1.
3. Evaluates condition: `1 > 1` -> False. (Skip).
4. Iterates to second element: x = 2.
5. Evaluates condition: `2 > 1` -> True.
6. Evaluates expression: `x * 2` -> 4.
7. Appends 4 to the internal list.
8. Returns `[4]`.

## M. Complexity
- List comprehension vs for-loop: Comprehensions are typically 20-30% faster 
  because the `append` mechanism happens at the C level inside the Python interpreter,
  avoiding the overhead of looking up the `.append` method on every iteration.

## N. Common Mistakes
1. Modifying a list while iterating over it.
   ```python
   # BUG: This will skip elements!
   for item in my_list:
       if item == "bad":
           my_list.remove(item)
   ```
   Fix: Iterate over a copy (`for item in my_list.copy():`) or use a comprehension.

## O. Common Confusions
`break` vs `continue` vs `pass`:
- `break`: Smashes the loop completely. You are out.
- `continue`: Skips the REST of the current iteration and jumps to the next one.
- `pass`: Does absolutely nothing. It is just a structural placeholder to avoid SyntaxErrors.

## P. When To Use
- Use comprehensions for simple mapping/filtering.
- Use pattern matching (`match/case`) when checking structure/types of dictionaries or complex tuples, avoiding deeply nested `if/elif` chains.

## Q. When NOT To Use
- Do NOT use comprehensions if the logic is complex (e.g., nested if/else with try/except blocks inside). If it spans more than 2 lines, write a standard for-loop for readability.

## R. Trade-offs
- **Comprehensions**: 
  - Pros: More concise, slightly faster.
  - Cons: Can become unreadable if overused or heavily nested.
- **Generators vs Comprehensions**: Comprehensions take $O(N)$ memory; generators take $O(1)$ memory.

## S. Debugging
Symptom: Infinite loop in a `while` statement.
Cause: The loop condition never evaluates to False because the variable isn't being updated.
Fix: Ensure the state variables driving the `while` condition are mutated inside the loop block.

## T. Memory Hook (a short memorable principle)
1. Loop `else` = "No Break". The `else` block runs if there was NO break.
2. Comprehension structure: `[WHAT_TO_KEEP for ITERATION if CONDITION]`

## U. Active Recall (questions before answers)
1. In a `for` loop, what happens if you put a `pass` statement? Does it skip the iteration?
2. Write a list comprehension that creates a list of the squares of all odd numbers from 1 to 10.
3. Why is `enumerate()` better than `range(len(lst))`?

## V. Practice (exercises)
Exercise 1: Write a function `clean_data(data)` that takes a list of strings, 
removes any empty strings, and converts the remaining strings to uppercase, 
using a single list comprehension.

## W. Interview Question
Q: How do you create a generator instead of a list comprehension? What is the benefit?
A: You use parentheses `()` instead of brackets `[]`. 
   E.g., `gen = (x*x for x in range(1000000))`. 
   The benefit is memory efficiency. A list comprehension generates all 1,000,000 items 
   in memory at once. A generator expression yields them one by one, using almost zero memory.

## X. Project Connection
In Data Science (Pandas), looping through dataframes using `for row in df.iterrows():` is famously slow.
However, list comprehensions are often used as a fast, native-Python way to clean a column of data before converting it back into a Pandas Series!
"""
from typing import List, Dict

def conditional_truthiness():
    """Demonstrates how Python evaluates non-boolean values in conditions."""
    print("--- 1. Conditionals & Truthiness ---")
    
    # In Python, empty collections, 0, and None are considered "Falsy".
    # Everything else is "Truthy".
    items = []
    if not items:
        print("The list is empty! (evaluated to False)")
        
    name = "Alice"
    if name:
        print("The string is not empty! (evaluated to True)")


def pythonic_loops():
    """Demonstrates the proper way to loop in Python (avoiding range(len()))."""
    print("\n--- 2. Pythonic Loops (Enumerate & Zip) ---")
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    
    # ANTI-PATTERN: for i in range(len(names)):
    
    # PATTERN 1: enumerate (When you need the index AND the item)
    for idx, name in enumerate(names):
        print(f"Rank {idx+1}: {name}")
        
    # PATTERN 2: zip (When you need to iterate over two lists simultaneously)
    for name, score in zip(names, scores):
        print(f"{name} scored {score}")


def loop_else_clause():
    """Demonstrates the often-confusing 'else' clause on loops."""
    print("\n--- 3. Loop Else Clause ---")
    target = 99
    numbers = [1, 5, 10, 20]
    
    for num in numbers:
        if num == target:
            print(f"Found {target}!")
            break
    else:
        # This executes because the loop finished without hitting 'break'
        print(f"Searched all numbers. {target} was NOT found.")


def comprehensions():
    """Demonstrates list, dict, and set comprehensions."""
    print("\n--- 4. Comprehensions ---")
    
    # List comprehension (with condition)
    # [expression for item in iterable if condition]
    evens = [x for x in range(10) if x % 2 == 0]
    print(f"Evens: {evens}")
    
    # Dict comprehension
    squares_dict = {x: x*x for x in range(3)}
    print(f"Squares Dict: {squares_dict}")


def pattern_matching(user_data: dict):
    """Demonstrates Python 3.10+ Structural Pattern Matching."""
    print("\n--- 5. Pattern Matching (Python 3.10+) ---")
    match user_data:
        case {"role": "admin", "name": name}:
            print(f"Welcome, Administrator {name}!")
        case {"role": "guest"}:
            print("Welcome, Guest! You have limited access.")
        case _:
            print("Unknown user format.")


def clean_data(data: List[str]) -> List[str]:
    return [word.upper() for word in data if word.strip()]


if __name__ == "__main__":
    conditional_truthiness()
    pythonic_loops()
    loop_else_clause()
    comprehensions()
    
    # Pattern matching test
    pattern_matching({"role": "admin", "name": "Sarah"})
    
    # Practice validation
    raw_data = ["apple", "", "  ", "banana", "cherry"]
    cleaned = clean_data(raw_data)
    print(f"\nCleaned Data: {cleaned}")
    assert cleaned == ["APPLE", "BANANA", "CHERRY"], "Practice function failed!"
    print("\nAll concepts successfully demonstrated.")
