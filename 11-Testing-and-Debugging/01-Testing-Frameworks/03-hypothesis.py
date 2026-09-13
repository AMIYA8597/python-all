"""
Property-Based Testing with Hypothesis - Educational Script

Learning Objectives:
1. Understand the paradigm of property-based testing.
2. Learn how to use the `hypothesis` library.
3. Define strategies to generate random test data.
4. Discover edge cases automatically that manual tests might miss.
5. Combine `hypothesis` with standard test runners like `pytest`.

Concept Explanation:
Unlike example-based testing (where you provide specific inputs and outputs),
property-based testing verifies that certain *properties* hold true for a vast range of inputs.
`hypothesis` generates random data based on "strategies" and tries to falsify your assertions.
If it finds a failure, it "shrinks" the input to the smallest, simplest failing example.

Key Components:
- Strategies: Rules for generating data (e.g., integers, lists of strings, dictionaries).
- Given: Decorator to inject generated data into the test function.
- Properties: The invariants that should always be true for your function.
"""

from typing import List, Tuple, Any
from hypothesis import given, strategies as st
import pytest

# --- Basic Implementation: Simple Properties ---

def sort_list(lst: List[int]) -> List[int]:
    """A simple sorting wrapper."""
    return sorted(lst)

@given(st.lists(st.integers()))
def test_sort_list_properties(lst: List[int]) -> None:
    """
    Test properties of a sorting function:
    1. The result has the same length as the input.
    2. The result is ordered.
    3. The elements in the result are the same as the input.
    """
    result = sort_list(lst)
    
    # Property 1: Length is preserved
    assert len(result) == len(lst)
    
    # Property 2: Result is ordered
    for i in range(len(result) - 1):
        assert result[i] <= result[i+1]
        
    # Property 3: Elements are preserved
    assert set(result) == set(lst)

# --- Intermediate Implementation: Custom Strategies and Complex Types ---

def encode_rle(data: str) -> List[Tuple[str, int]]:
    """Run-length encoding."""
    if not data:
        return []
    
    encoded = []
    current_char = data[0]
    count = 1
    
    for char in data[1:]:
        if char == current_char:
            count += 1
        else:
            encoded.append((current_char, count))
            current_char = char
            count = 1
    encoded.append((current_char, count))
    return encoded

def decode_rle(encoded: List[Tuple[str, int]]) -> str:
    """Run-length decoding."""
    return "".join(char * count for char, count in encoded)

# Test the property that decoding an encoded string yields the original string
@given(st.text())
def test_rle_roundtrip(data: str) -> None:
    """Property: decode(encode(data)) == data"""
    encoded = encode_rle(data)
    decoded = decode_rle(encoded)
    assert decoded == data

# --- Advanced Implementation: State Machine Testing (Conceptual) ---
# Hypothesis also supports stateful testing (e.g., testing a database or API by generating
# random sequences of operations and asserting invariants after each step).
# For this script, we'll focus on advanced data generation.

@given(st.dictionaries(st.text(), st.integers()))
def test_dict_manipulation(d: dict[str, int]) -> None:
    """Testing dictionary operations with arbitrary string keys and integer values."""
    # Property: Copying a dictionary preserves its items
    d_copy = d.copy()
    assert d == d_copy
    
    # Property: Adding a new key increases length or updates value
    d_copy["__test_key__"] = 999
    assert "__test_key__" in d_copy
    assert d_copy["__test_key__"] == 999

# --- Performance Analysis ---
# Hypothesis runs a test multiple times (default 100) with different generated data.
# This makes it slower than standard unit tests.
# Use `settings(max_examples=...)` to control the number of runs.
# Profile tests using `hypothesis.settings(profile="...")`.

# --- Edge Cases ---
# Hypothesis is excellent at finding edge cases like empty lists, NaN, infinite floats,
# zero, negative zero, and complex Unicode characters.
# It automatically tests these boundary conditions first.

# --- Interview Challenge ---
# Challenge: A function `chunk_list(lst, n)` splits a list into sublists of size n.
# What are the properties of this function? Write a Hypothesis test for it.

def chunk_list(lst: List[Any], n: int) -> List[List[Any]]:
    if n <= 0:
        raise ValueError("n must be > 0")
    return [lst[i:i+n] for i in range(0, len(lst), n)]

@given(st.lists(st.integers()), st.integers(min_value=1, max_value=100))
def test_chunk_list_properties(lst: List[int], n: int) -> None:
    chunks = chunk_list(lst, n)
    
    # Property 1: The concatenated chunks equal the original list
    flattened = [item for chunk in chunks for item in chunk]
    assert flattened == lst
    
    # Property 2: All chunks except potentially the last have size n
    for chunk in chunks[:-1]:
        assert len(chunk) == n

if __name__ == "__main__":
    print("Run this file using: pytest 03-hypothesis.py -v")
    pytest.main([__file__, "-v"])
