"""
# ==============================================================================
# LABORATORY 06: STRING MANIPULATION, ENCODING, AND INTERNING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Strings in Python 3 are Unicode by default, making them incredibly powerful 
# but memory-heavy. Understanding string immutability, efficient concatenation, 
# advanced f-string formatting, and the difference between bytes and strings 
# is essential for API engineering, Data Science parsing, and NLP.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand String Immutability and the CPython "Interning" optimization.
# - Master efficient concatenation (`.join()` vs `+`).
# - Master advanced f-string debugging (`f"{var=}"`).
# - Understand the difference between `str` (Unicode) and `bytes` (UTF-8/ASCII).
# - Use the `re` module for basic regex text manipulation.
#
# ==============================================================================
"""

import sys
import timeit
import re

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. IMMUTABILITY & CPYTHON INTERNING
# ==============================================================================
def demonstrate_interning():
    """
    Strings are immutable. But to save memory, CPython automatically "interns" 
    (caches and reuses) short strings that look like identifiers (letters, 
    numbers, underscores).
    """
    section_header("Immutability & String Interning")
    
    # These strings are identical and look like identifiers, so CPython interns them.
    a = "hello_world"
    b = "hello_world"
    print(f"a is b (Interned): {a is b}")
    
    # Strings with spaces or special characters are often NOT interned automatically.
    c = "hello world!"
    d = "hello world!"
    # Note: In a script/module, the compiler might optimize this to True,
    # but in the REPL, it is usually False. We use sys.intern() to force it.
    print(f"c is d (Special chars): {c is d}")
    
    # Forced Interning (useful in NLP for massive dictionaries to save memory)
    e = sys.intern("hello world!")
    f = sys.intern("hello world!")
    print(f"e is f (Forced intern): {e is f}")


# ==============================================================================
# 4. EFFICIENT CONCATENATION (O(N^2) TRAP)
# ==============================================================================
def demonstrate_concatenation():
    """
    Because strings are immutable, `a = a + b` creates a BRAND NEW string 
    object in memory and copies the contents of both.
    Doing this in a loop causes O(N^2) time complexity.
    Always use `"".join(list_of_strings)` for O(N) concatenation.
    """
    section_header("Efficient Concatenation Trap")
    
    words = ["hello", "world", "from", "python"] * 1000
    
    # Method 1: The bad way (using +)
    def bad_concat():
        s = ""
        for w in words:
            s += w
        return s
        
    # Method 2: The good way (using .join)
    def good_concat():
        return "".join(words)
        
    bad_time = timeit.timeit(bad_concat, number=100)
    good_time = timeit.timeit(good_concat, number=100)
    
    print(f"Using `+=` inside loop: {bad_time:.4f} seconds (O(N^2))")
    print(f"Using `"".join()`:      {good_time:.4f} seconds (O(N))")
    print(f".join() is {bad_time/good_time:.1f}x faster!")


# ==============================================================================
# 5. ADVANCED F-STRINGS (PYTHON 3.8+)
# ==============================================================================
def demonstrate_fstrings():
    """
    f-strings are evaluated at runtime using C-level formatting.
    They support math, formatting specifications, and debugging.
    """
    section_header("Advanced f-strings")
    
    user = "Alice"
    score = 95.1234
    
    # Standard formatting
    print(f"Score for {user} is {score:.2f}")
    
    # Padding and alignment
    # > right align, < left align, ^ center
    print(f"|{user:>10}| (Right aligned, 10 chars)")
    print(f"|{user:^10}| (Center aligned, 10 chars)")
    
    # Python 3.8+ Debugging syntax (variable=)
    x = 10
    y = 25
    print(f"\nDebugging: {x=}, {y=}, {x*y=}")
    
    # Date formatting directly in the f-string
    import datetime
    now = datetime.datetime.now()
    print(f"Today is: {now:%Y-%m-%d %H:%M}")


# ==============================================================================
# 6. ENCODING: STR VS BYTES
# ==============================================================================
def demonstrate_encoding():
    """
    Python 3 `str` objects are Unicode (text).
    Python 3 `bytes` objects are raw 8-bit values (binary).
    You ENCODE a str to get bytes. You DECODE bytes to get a str.
    """
    section_header("Encoding: str vs bytes")
    
    text = "Hello 🌍" # Unicode string
    print(f"String: {text} (Length: {len(text)})")
    
    # Encode to UTF-8 bytes
    encoded_bytes = text.encode('utf-8')
    print(f"\nBytes:  {encoded_bytes}")
    print(f"Length of bytes: {len(encoded_bytes)} (Notice the emoji takes 4 bytes!)")
    
    # Decode back to string
    decoded_text = encoded_bytes.decode('utf-8')
    assert text == decoded_text, "Decoding restored the original text."


# ==============================================================================
# 7. REGEX: BASIC TEXT PROCESSING
# ==============================================================================
def demonstrate_regex():
    """
    The `re` module provides regular expression matching operations.
    Always use raw strings `r"..."` for regex patterns to prevent Python 
    from escaping characters like `\n` or `\b`.
    """
    section_header("Regular Expressions (re module)")
    
    text = "Please contact admin@example.com or support-team@company.org for help."
    
    # Standard email regex pattern (simplified)
    # Using r"" ensures \w is treated as regex word-character, not an escape code.
    pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    
    # re.findall() returns a list of all matches
    emails = re.findall(pattern, text)
    print(f"Found emails: {emails}")
    
    # re.sub() replaces matches
    redacted = re.sub(pattern, "[REDACTED]", text)
    print(f"Redacted text: {redacted}")


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is concatenating strings in a loop (`s += new_string`) a bad idea?
   Answer: Strings are immutable. `+=` creates a brand new string and copies the memory every iteration, resulting in O(N^2) complexity. Use `"".join(list)` instead.

2. What is string interning?
   Answer: CPython caches and reuses memory for short, identifier-like strings. You can manually force it using `sys.intern()` to save memory when parsing large datasets with repeated strings (like NLP tokens).

3. What does `f"{variable=}"` do?
   Answer: Introduced in Python 3.8, it prints both the variable name and its value for easy debugging (e.g., `variable=10`).

4. What is the difference between `str` and `bytes`?
   Answer: `str` represents human-readable Unicode text. `bytes` represents raw machine-readable binary data. You encode `str` to `bytes` (e.g. for network transmission) and decode `bytes` to `str`.
"""

if __name__ == "__main__":
    demonstrate_interning()
    demonstrate_concatenation()
    demonstrate_fstrings()
    demonstrate_encoding()
    demonstrate_regex()
    print("\n[SUCCESS] Laboratory 06 Completed.")
