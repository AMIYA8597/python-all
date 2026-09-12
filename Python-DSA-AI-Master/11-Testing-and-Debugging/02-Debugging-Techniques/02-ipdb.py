"""
IPDB Debugging Masterclass

Learning Objectives:
1. Understand the enhancements ipdb provides over standard pdb.
2. Learn how to utilize IPython features (tab completion, syntax highlighting) during debugging.
3. Master debugging complex data structures interactively.

Concept Explanation:
ipdb exports functions to access the IPython debugger, which features tab completion, 
syntax highlighting, better tracebacks, and better object introspection compared to standard pdb.
It integrates seamlessly into IPython and Jupyter environments.

Common usage:
`import ipdb; ipdb.set_trace()`
or using breakpoint() with `PYTHONBREAKPOINT=ipdb.set_trace`
"""

import sys
import unittest
from typing import List, Dict, Any

try:
    import ipdb
except ImportError:
    # Fallback to pdb if ipdb is not installed for testing purposes
    import pdb as ipdb

# --- Basic Implementation ---
def string_processor(texts: List[str]) -> List[str]:
    """Basic function to demonstrate ipdb interactive exploration."""
    processed = []
    for text in texts:
        # If we injected ipdb.set_trace() here, we could use tab completion on 'text'
        processed.append(text.strip().lower())
    return processed

# --- Intermediate Implementation ---
def deep_dict_lookup(data: Dict[str, Any], path: str) -> Any:
    """Demonstrates traversing deep data structures where syntax highlighting helps."""
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            # ipdb.set_trace() would let us inspect 'current' visually
            return None
    return current

# --- Advanced Implementation ---
class InteractiveDataExplorer:
    """Advanced class showing how ipdb helps with object introspection."""
    def __init__(self, dataset: List[Dict[str, Any]]):
        self.dataset = dataset
        self.index = {row['id']: row for row in dataset if 'id' in row}

    def find_anomalies(self) -> List[Dict[str, Any]]:
        anomalies = []
        for row in self.dataset:
            # Complex condition where ipdb's `?` operator is useful to inspect objects
            if row.get('value', 0) > 1000 or row.get('status') == 'ERROR':
                anomalies.append(row)
        return anomalies

# --- Performance Analysis ---
"""
Performance Analysis:
- ipdb has slightly more overhead on startup compared to pdb due to IPython initialization.
- It is strictly for development and debugging, never for production.
- Memory footprint is larger because of the IPython shell.
"""

# --- Edge Cases ---
"""
Edge Cases Handled:
- Missing keys in deep dictionary lookups.
- Missing 'id' fields when indexing datasets.
- Handled gracefully returning None or skipping records rather than crashing.
"""

# --- Interview Challenge ---
"""
Interview Challenge:
Question: How can you globally change the built-in `breakpoint()` behavior to use ipdb?
Answer: Set the environment variable `PYTHONBREAKPOINT=ipdb.set_trace` before running the script.
"""

# --- Tests ---
class TestIPDBDebugging(unittest.TestCase):
    def test_string_processor(self):
        res = string_processor([" Hello ", "WORLD", "  ipdb  "])
        self.assertEqual(res, ["hello", "world", "ipdb"])

    def test_deep_dict_lookup(self):
        data = {'user': {'profile': {'name': 'Alice', 'age': 30}}}
        self.assertEqual(deep_dict_lookup(data, 'user.profile.name'), 'Alice')
        self.assertIsNone(deep_dict_lookup(data, 'user.settings.theme'))

    def test_interactive_explorer(self):
        data = [
            {'id': 1, 'value': 100, 'status': 'OK'},
            {'id': 2, 'value': 1500, 'status': 'OK'},
            {'id': 3, 'value': 50, 'status': 'ERROR'}
        ]
        explorer = InteractiveDataExplorer(data)
        anomalies = explorer.find_anomalies()
        self.assertEqual(len(anomalies), 2)

if __name__ == "__main__":
    print("Running IPDB Debugging Masterclass Tests...")
    unittest.main()
