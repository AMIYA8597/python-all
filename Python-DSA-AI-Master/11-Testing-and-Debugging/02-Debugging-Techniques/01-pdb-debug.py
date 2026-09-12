"""
PDB Debugging Masterclass

Learning Objectives:
1. Understand the core features of the Python Debugger (pdb).
2. Learn how to set breakpoints, step through code, and inspect variables.
3. Master advanced pdb commands (e.g., conditional breakpoints, commands on breakpoints).
4. Apply pdb debugging techniques to trace complex program state.

Concept Explanation:
pdb is the built-in interactive source code debugger for Python programs. It supports
setting (conditional) breakpoints, stepping line by line, inspecting stack frames, and 
evaluating arbitrary Python code in the context of any stack frame.

Key commands:
- `l` (list): show code around current line
- `n` (next): execute current line, step over functions
- `s` (step): execute current line, step into functions
- `c` (continue): continue execution until next breakpoint
- `p` (print): evaluate and print expression
- `b` (break): set a breakpoint
- `q` (quit): quit the debugger
"""

import pdb
import sys
import unittest
from typing import List, Dict, Any, Optional

# --- Basic Implementation ---
def buggy_sum(numbers: List[int]) -> int:
    """A buggy sum function for basic pdb demonstration."""
    total = 0
    for num in numbers:
        # A common mistake: converting list item to string or logic error
        if isinstance(num, str):
            # We will use pdb.set_trace() in tests if needed, but here we just simulate the bug
            pass
        total += num
    return total

# --- Intermediate Implementation ---
def divide_elements(data: Dict[str, Any], keys: List[str]) -> List[float]:
    """Demonstrates debugging exceptions and conditional breakpoints."""
    results = []
    for key in keys:
        try:
            val = data[key]
            # Potential zero division error
            res = 100 / val
            results.append(res)
        except ZeroDivisionError:
            # We could inject pdb.post_mortem() here in a real debugging scenario
            results.append(float('inf'))
        except KeyError:
            results.append(None)
    return results

# --- Advanced Implementation ---
class ComplexDataProcessor:
    """Advanced class to demonstrate stepping and frame inspection."""
    def __init__(self, data: List[int]):
        self.data = data
        self.processed = False

    def _internal_transform(self, val: int) -> int:
        # A complex internal method where we might want to step into
        temp = val * 2
        temp = temp - (val // 2)
        return temp

    def process(self) -> List[int]:
        result = []
        for x in self.data:
            # You can set a conditional breakpoint here in pdb:
            # b 76, x == 0
            val = self._internal_transform(x)
            result.append(val)
        self.processed = True
        return result

# --- Performance Analysis ---
"""
Performance Analysis:
- Using pdb adds significant overhead because it uses sys.settrace() to trace every
  line of execution. It should never be enabled in production environments.
- Conditional breakpoints evaluate a Python expression at every line/call, slowing
  down execution further.
"""

# --- Edge Cases ---
"""
Edge Cases Handled:
- Catching exceptions like KeyError and ZeroDivisionError to prevent sudden crashes
  while debugging.
- Handling mixed types in basic implementations.
"""

# --- Interview Challenge ---
"""
Interview Challenge:
Question: How do you trigger a debugger automatically when an unhandled exception occurs?
Answer: You can override `sys.excepthook` or use `pdb.pm()` / `pdb.post_mortem()` after an exception is caught.

def custom_excepthook(type, value, tb):
    import traceback, pdb
    traceback.print_exception(type, value, tb)
    pdb.post_mortem(tb)
sys.excepthook = custom_excepthook
"""

# --- Tests ---
class TestPDBDebugging(unittest.TestCase):
    def test_buggy_sum(self):
        self.assertEqual(buggy_sum([1, 2, 3]), 6)
        with self.assertRaises(TypeError):
            buggy_sum([1, "2", 3]) # Bug triggered

    def test_divide_elements(self):
        data = {'a': 10, 'b': 0, 'c': 5}
        res = divide_elements(data, ['a', 'b', 'c', 'd'])
        self.assertEqual(res, [10.0, float('inf'), 20.0, None])

    def test_complex_processor(self):
        processor = ComplexDataProcessor([10, 0, 5])
        res = processor.process()
        self.assertEqual(res, [15, 0, 8])

if __name__ == "__main__":
    print("Running PDB Debugging Masterclass Tests...")
    unittest.main()
