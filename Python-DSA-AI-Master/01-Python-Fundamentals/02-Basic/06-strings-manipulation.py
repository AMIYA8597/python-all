r"""
## A. Concept Name
String Manipulation & Immutability

## B. One-Sentence Definition
Strings are immutable sequences of Unicode characters that can be sliced, formatted, searched, and transformed using built-in methods or regular expressions.

## C. Why Does This Exist?
Text is the most common form of unstructured data. We need efficient, predictable ways to clean, parse, search, and transform text (e.g., extracting emails from a document, formatting logs, cleaning user input).

## D. Intuition
Think of a string as a sealed box of alphabet blocks arranged in a row. You can look at the blocks, take photos of segments, and use those photos to build a new box of blocks, but you cannot pry open the original box and swap out a single block.

## E. Real-Life Analogy
A string is like a printed book. You can read it, you can photocopy pages (slicing), or you can write a new book incorporating parts of the old one (concatenation). But you cannot erase a letter printed on the page and overwrite it (immutability).

## F. Mental Model
String = Immutable Array of Characters.
Operations (replace, upper, slice) do not mutate the array; they allocate a new Array of Characters and return a reference to it.

## G. Visual Explanation
String Slicing: `text = "PYTHON"`
Indices (Positive):   0   1   2   3   4   5
                    +---+---+---+---+---+---+
                    | P | Y | T | H | O | N |
                    +---+---+---+---+---+---+
Indices (Negative):  -6  -5  -4  -3  -2  -1

text[1:4] -> "YTH" (starts at 1, goes up to but NOT including 4)
text[::-1] -> "NOHTYP" (reverses the string)

## H. Formal Explanation
In Python, strings (`str`) are immutable sequences of Unicode code points. Because they are immutable, operations that appear to modify a string (like `s += 'a'`) actually create an entirely new string object in memory. This immutability allows strings to be hashable (usable as dictionary keys) and thread-safe. For efficient building of large strings, accumulating substrings in a list and calling `''.join(list)` is preferred over repeated `+` concatenation.

## I. Mathematical Foundation (if applicable)
Let S be a string of length N.
Concatenating S with another string of length M requires allocating a new buffer of size N + M and copying both strings into it.
Repeatedly appending K characters one-by-one using `+=` takes O(K^2) time because at step i, we copy i characters.
Using `.join()` on a list of K characters takes O(K) time because it computes the total length once, allocates the buffer once, and copies everything in one pass.

## J. From-Scratch Implementation (if applicable)
(See python code below for basic ops, parsing, regex, and anagram from-scratch)

## K. Library / Production Implementation (if applicable)
Python provides robust built-in string methods (like `.split()`, `.join()`, `.replace()`) and the standard `re` module for complex regular expressions. Production systems often rely on f-strings (`f"{var}"`) for rapid formatting and `re` for tokenization.

## L. Trace (walk through example)
For `is_anagram("Listen", "Silent")`:
Step 1: Clean and lowercase both. s1 = "listen", s2 = "silent".
Step 2: Check lengths. len("listen") == 6, len("silent") == 6. Match!
Step 3: Build frequency map for s1.
        counts = {'l':1, 'i':1, 's':1, 't':1, 'e':1, 'n':1}
Step 4: Decrement for s2.
        's' -> counts['s'] becomes 0
        'i' -> counts['i'] becomes 0
        'l' -> counts['l'] becomes 0
        'e' -> counts['e'] becomes 0
        'n' -> counts['n'] becomes 0
        't' -> counts['t'] becomes 0
Step 5: All characters found and counts didn't drop below 0. Return True.

## M. Complexity
- Slicing: Time O(K) where K is the slice length. Space O(K) for the new string.
- Concatenation (+): Time O(N+M). Space O(N+M).
- `.join()`: Time O(N) where N is total length of all strings. Space O(N).
- `.replace()`, `.split()`: Time O(N). Space O(N).

## N. Common Mistakes
- Modifying by index: `s[0] = 'H'` (Raises TypeError: 'str' object does not support item assignment).
- Building large strings with `+=` in a loop (O(N^2) time complexity).
- Using `.strip()` to remove a substring. `.strip('abc')` removes ANY combination of 'a', 'b', and 'c' from the ends, not the exact string "abc".

## O. Common Confusions
- `.strip()` vs `.replace()` vs `.removeprefix()`: 
  - `.strip("xyz")` removes 'x', 'y', 'z' from both ends. 
  - `.replace("xyz", "")` removes the exact sequence "xyz" anywhere.
  - `.removeprefix("xyz")` (Python 3.9+) removes the exact sequence "xyz" only if it's at the start.
- `+` vs `.join()`: Use `+` for 2-3 strings. Use `.join()` for a list or loop of strings.

## P. When To Use
- `+` or f-strings for simple formatting.
- `.split()` and `.join()` for CSV or delimited data manipulation.
- `re` (Regex) for complex pattern extraction (emails, phone numbers, specific formats).

## Q. When NOT To Use
- Do not use string methods for parsing HTML/XML (use BeautifulSoup).
- Do not use Regex for full language parsing or when simple `.split()` or `in` operator suffices (Regex is slow and hard to read).

## R. Trade-offs
- Immutability vs Mutation: Immutability provides safety and allows hashing, but costs memory and performance when heavy modifications are required (hence `.join()` is preferred over `+=`).
- Regex vs String Methods: Regex handles complex patterns but is computationally heavier and less readable. Built-in methods are highly optimized and simpler.

## S. Debugging
- Issue: `TypeError: can only concatenate str (not "int") to str`
  Fix: Convert non-strings explicitly using `str(num)` or use f-strings `f"{num}"`.
- Issue: Unexpected characters stripped.
  Fix: Check if you meant to use `.removeprefix()`/`.removesuffix()` instead of `.strip()`.

## T. Memory Hook
"Strings are sealed. Slices take photos. Join builds walls."

## U. Active Recall
- Why is `"".join(list_of_strings)` faster than a loop with `+=`?
- What does `"hello"[::-1]` do?
- What is the difference between `.replace("foo", "")` and `.strip("foo")`?

## V. Practice
Exercise: Write a function that takes a sentence and returns the longest word. If there's a tie, return the first one. Ignore punctuation.
Solution:
```python
def longest_word(sentence: str) -> str:
    import re
    # Remove punctuation and split
    words = re.sub(r'[^\w\s]', '', sentence).split()
    if not words: return ""
    return max(words, key=len)
```

## W. Interview Question
Question: Write a function to check if two strings are anagrams of each other. (Ignore spaces and case).
(Implemented in code section below).

## X. Project Connection
- NLP Data Preprocessing: Lowercasing, removing punctuation, splitting into tokens (words).
- Prompt Engineering: Dynamically injecting context into LLM prompts using f-strings.
- Log Parsing: Using regex to extract timestamps, error codes, and metrics from raw text logs for monitoring AI training pipelines.
"""

import re
from typing import List, Dict

# ==========================================
# From-Scratch Implementation
# ==========================================

def basic_string_ops(text: str) -> str:
    """Demonstrates slicing, casing, and basic methods."""
    # Slicing: [start:stop:step]
    reversed_text = text[::-1]
    
    # Casing
    upper_text = text.upper()
    title_text = text.title()
    
    # Strip whitespace
    cleaned = text.strip()
    
    return f"{cleaned} | {reversed_text}"


def parse_and_format_csv(line: str) -> str:
    """
    Parses a comma-separated string, cleans the data, 
    and formats it beautifully using List Comprehensions and .join().
    """
    # Split by comma
    parts = line.split(',')
    
    # Clean whitespace and build a formatted string
    cleaned_parts = [p.strip().capitalize() for p in parts]
    
    # Efficient joining - much faster than += in a loop
    formatted_line = " -> ".join(cleaned_parts)
    return formatted_line


def extract_emails(text: str) -> List[str]:
    """
    Uses regex to find all valid email addresses in a block of text.
    Regex is essential for complex string parsing tasks.
    """
    # Pattern: [word chars] + @ + [word chars] + . + [2-4 word chars]
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)


# ==========================================
# Interview Question Implementation
# ==========================================
def is_anagram(s1: str, s2: str) -> bool:
    """
    Checks if s1 and s2 are anagrams.
    Time Complexity: O(N) using counting.
    Space Complexity: O(1) since character set is fixed (e.g., 26 letters).
    """
    # Clean inputs
    s1 = s1.replace(" ", "").lower()
    s2 = s2.replace(" ", "").lower()
    
    # Quick length check
    if len(s1) != len(s2):
        return False
        
    # Build frequency map for s1
    counts: Dict[str, int] = {}
    for char in s1:
        counts[char] = counts.get(char, 0) + 1
        
    # Check against s2
    for char in s2:
        if char not in counts or counts[char] == 0:
            return False
        counts[char] -= 1
        
    return True


if __name__ == "__main__":
    print("--- String Manipulation & Immutability Masterclass ---\n")
    
    # Basic ops
    res1 = basic_string_ops("  Python is Fun  ")
    print("1. Basic Ops:", res1)
    assert "Python is Fun" in res1
    
    # Parsing
    csv_line = " apple , BANANA, cherry "
    res2 = parse_and_format_csv(csv_line)
    print("2. Parse & Format:", res2)
    assert res2 == "Apple -> Banana -> Cherry"
    
    # Regex
    doc = "Contact us at support@example.com or sales@company.org for info."
    emails = extract_emails(doc)
    print("3. Regex Emails:", emails)
    assert emails == ["support@example.com", "sales@company.org"]
    
    # Interview Challenge
    print("4. Anagram Check (Listen vs Silent):", is_anagram("Listen", "Silent"))
    assert is_anagram("Listen", "Silent") == True
    assert is_anagram("Hello", "World") == False

    print("\nAll tests passed successfully!")
