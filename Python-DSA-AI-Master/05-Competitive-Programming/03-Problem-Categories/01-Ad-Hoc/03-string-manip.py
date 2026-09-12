"""
=============================================================================
## A. Concept Name: String Manipulation (Ad-Hoc)
=============================================================================

## B. What is this?
String manipulation problems focus on transforming, parsing, or analyzing text data.
While strings are essentially arrays of characters, the algorithms used on them 
often differ from standard array problems due to string immutability in Python, 
character encodings, and common patterns like palindromes, anagrams, and substrings.

## C. Why does it exist?
Text is the most common format for data exchange (JSON, XML, CSV). 
Being able to parse, validate, and manipulate text rapidly and accurately is a 
foundational skill for any software engineer.

## D. Industry Use Cases
- Natural Language Processing (NLP) tokenization and cleaning.
- Implementing parsers for custom domain-specific languages (DSLs).
- Log file analysis and data extraction (regex replacements, log parsing).
- Cryptography and data obfuscation.

## E. Beginner Explanation
Imagine you need to check if a word is a palindrome (reads the same forwards and 
backwards, like "racecar"). In Python, you can easily do `s == s[::-1]`. 
But in interviews, you're often expected to implement the logic manually using 
two pointers (one at the beginning, one at the end, moving towards the center).

String problems often ask you to clean data (e.g., remove trailing spaces), 
find patterns, or convert strings into other data types.

## F. Deep Technical Explanation
Python strings are immutable. This means operations like `s[i] = 'a'` will throw 
an error. 
To modify strings efficiently:
1. Convert them to a list of characters: `chars = list(s)`. Modify the list, then 
   join back: `"".join(chars)`.
2. Understand ASCII and Unicode. Use `ord(c)` to get the integer value of a character, 
   and `chr(i)` to convert back. E.g., `ord('a')` is 97.
3. Be familiar with Python's built-in string methods: `.split()`, `.strip()`, 
   `.isdigit()`, `.isalpha()`, etc.

## G. Performance Considerations
- Repeatedly appending to a string using `+` in a loop creates a new string each time, 
  leading to O(N^2) complexity in many languages (though CPython has some optimizations, 
  it is considered bad practice).
- Searching for substrings using `in` is efficient in Python (using the Boyer-Moore-Horspool 
  algorithm), but for complex patterns, understand algorithms like KMP (Knuth-Morris-Pratt).

## H. Security Concerns
- Buffer overflows (not common in Python, but relevant in C/C++).
- SQL Injection and XSS: Always sanitize string inputs before evaluating them or 
  rendering them in a browser. Don't build SQL queries via raw string concatenation!

## I. Implementation Example
Below are examples of string manipulation implementations.

## J. Common Mistakes
1. Forgetting to handle empty strings or strings with only spaces.
2. In atoi, failing to clamp the values strictly within the 32-bit limits.
3. Forgetting that string slices in Python like `s[left:right]` take O(K) time, 
   where K is the slice length. 

## K. Interview Challenge
"Given a string, find the first non-repeating character in it and return its index."
Hint: Use a hash map (or an array of size 26 for letters) to count frequencies, 
then iterate through the string a second time.

## L. Exercise
Implement `strStr(haystack, needle)` which returns the index of the first occurrence 
of needle in haystack, or -1 if needle is not part of haystack. Try implementing it 
without using the built-in `.find()` method.

## X. Project Connection
String manipulation is fundamental in building web scraping tools, log analyzers, 
and text-based AI models. For instance, creating a fast parser for JSON data requires 
efficient string handling to tokenize and decode structures without performance bottlenecks.
"""

def my_atoi(s: str) -> int:
    """
    Converts a string to a 32-bit signed integer, mimicking the C atoi function.
    
    Rules:
    1. Read and ignore leading whitespace.
    2. Check for '+' or '-' sign.
    3. Read characters until a non-digit is encountered or end of string is reached.
    4. Clamp the integer to the 32-bit signed integer range [-2^31, 2^31 - 1].
    
    Time Complexity: O(N) where N is length of string.
    Space Complexity: O(1).
    """
    if not s:
        return 0
        
    n = len(s)
    i = 0
    sign = 1
    result = 0
    
    INT_MAX = 2**31 - 1
    INT_MIN = -2**31
    
    # 1. Skip leading whitespace
    while i < n and s[i] == ' ':
        i += 1
        
    if i == n:
        return 0
        
    # 2. Check sign
    if s[i] == '-':
        sign = -1
        i += 1
    elif s[i] == '+':
        i += 1
        
    # 3. Process digits
    while i < n and s[i].isdigit():
        digit = int(s[i])
        
        # 4. Check overflow/underflow before adding the digit
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            return INT_MAX if sign == 1 else INT_MIN
            
        result = result * 10 + digit
        i += 1
        
    return sign * result


def longest_palindromic_substring(s: str) -> str:
    """
    Finds the longest palindromic substring in s using the expand-around-center approach.
    
    Time Complexity: O(N^2)
    Space Complexity: O(1)
    """
    if not s or len(s) < 2:
        return s
        
    def expand_around_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    longest = ""
    for i in range(len(s)):
        # Odd length palindromes centered at i
        odd_pal = expand_around_center(i, i)
        if len(odd_pal) > len(longest):
            longest = odd_pal
            
        # Even length palindromes centered between i and i+1
        even_pal = expand_around_center(i, i + 1)
        if len(even_pal) > len(longest):
            longest = even_pal
            
    return longest

if __name__ == "__main__":
    # Test Atoi
    assert my_atoi("42") == 42
    assert my_atoi("   -42") == -42
    assert my_atoi("4193 with words") == 4193
    assert my_atoi("words and 987") == 0
    assert my_atoi("-91283472332") == -2147483648 # INT_MIN clamp
    
    # Test Longest Palindromic Substring
    assert longest_palindromic_substring("babad") in ["bab", "aba"]
    assert longest_palindromic_substring("cbbd") == "bb"
    
    print("All string manipulation problems tests passed successfully!")
