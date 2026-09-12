"""
## A. Concept Name
Fast I/O for Competitive Programming

## B. Motivation
Python's built-in `input()` function has a lot of overhead. It reads a line from sys.stdin, strips the trailing newline character, and converts it to a string. `print()` has overhead to process arguments, add spaces, and append newlines.
In competitive programming, when the input size exceeds 10^5 lines, this overhead can result in a Time Limit Exceeded (TLE) error.

## C. How it Works
To avoid this overhead, we use `sys.stdin.readline` which reads directly without extra processing (it keeps the trailing newline). For output, we use `sys.stdout.write`.
For even faster execution (when allowed by the platform), we can read all input at once into a byte buffer using `os.read(0, os.fstat(0).st_size)` and parse it iteratively.

## D. Advanced Usage
`os.read()` combined with a custom byte parser avoids decoding overhead, avoids creating intermediate lists of strings, and processes bytes on-the-fly, reducing both memory overhead and string manipulation times.

## X. Project Connection
Used across all advanced data structure implementations and competitive programming solutions in this workspace to guarantee execution within standard time limits.
"""

import sys
import os
import io
from typing import List, Tuple, Generator

# ==============================================================================
# Basic Fast I/O Setup (Most common in CP)
# ==============================================================================
# Simply reassign input for the entire file.
input = sys.stdin.readline

def read_int() -> int:
    """Reads a single integer from a line."""
    return int(input())

def read_ints() -> List[int]:
    """Reads multiple space-separated integers from a line."""
    return list(map(int, input().split()))

def read_string() -> str:
    """Reads a string and strips whitespace (including newline)."""
    return input().strip()

# ==============================================================================
# Professional Wrapper (For extreme cases like PyPy / large test cases)
# ==============================================================================
class FastIO:
    """
    A professional I/O wrapper handling byte-level operations.
    Use this when the platform has extremely strict time limits.
    """
    def __init__(self):
        # Read the entire input from standard input (file descriptor 0)
        self.buffer = io.BytesIO(os.read(0, os.fstat(0).st_size))
        # Pre-allocate output buffer
        self.out_buffer = io.BytesIO()

    def readline(self) -> bytes:
        return self.buffer.readline()

    def read_int(self) -> int:
        """Read an integer handling negative signs."""
        b = self.buffer.read(1)
        while b and b <= b' ':
            b = self.buffer.read(1)
        if not b:
            return 0
        sign = 1
        if b == b'-':
            sign = -1
            b = self.buffer.read(1)
        res = 0
        while b > b' ':
            res = res * 10 + (b[0] - 48)
            b = self.buffer.read(1)
        return res * sign

    def write(self, string: str):
        self.out_buffer.write(string.encode())

    def flush(self):
        os.write(1, self.out_buffer.getvalue())

# ==============================================================================
# Example Usage and Tests
# ==============================================================================
def example_solve():
    """
    Simulated competitive programming solve function.
    Reads N, then N integers, and prints their sum.
    """
    # Assuming standard fast I/O setup for tests
    # If this was a real CP problem:
    # n = read_int()
    # arr = read_ints()
    # sys.stdout.write(f"{sum(arr)}\n")
    pass


if __name__ == "__main__":
    # Test suite for Fast I/O wrapper mock
    print("Testing Fast I/O concepts...")
    
    # We mock os.read and os.write behavior for the test
    original_read = os.read
    original_fstat = os.fstat
    original_write = os.write
    
    try:
        class MockStat:
            st_size = 1024
        
        test_input = b"5\n1 2 -3 4 5\n"
        
        def mock_read(fd, size):
            return test_input if fd == 0 else b""
            
        def mock_fstat(fd):
            return MockStat()
            
        captured_out = b""
        def mock_write(fd, data):
            nonlocal captured_out
            captured_out = data
            
        os.read = mock_read
        os.fstat = mock_fstat
        os.write = mock_write
        
        # Test FastIO class
        fio = FastIO()
        n = fio.read_int()
        assert n == 5, f"Expected 5, got {n}"
        
        arr = [fio.read_int() for _ in range(5)]
        assert arr == [1, 2, -3, 4, 5], f"Expected [1, 2, -3, 4, 5], got {arr}"
        
        fio.write(f"Sum is {sum(arr)}\n")
        fio.flush()
        assert captured_out == b"Sum is 9\n", "Output buffer mismatch"
        
        print("All tests passed! Fast I/O templates are ready to use.")
        
    finally:
        # Restore environment
        os.read = original_read
        os.fstat = original_fstat
        os.write = original_write

"""
Interview Challenge:
Question: Why might `os.read(0, ...)` be faster than `sys.stdin.read().split()`?
Answer: `sys.stdin.read().split()` does several things: it reads the bytes, decodes them to string (which takes time), creates a massive string in memory, and then creates a huge list of substrings when `split()` is called. `os.read()` combined with a custom byte parser avoids decoding overhead, avoids creating intermediate lists of strings, and processes bytes on-the-fly, reducing both memory overhead and string manipulation times.
"""
