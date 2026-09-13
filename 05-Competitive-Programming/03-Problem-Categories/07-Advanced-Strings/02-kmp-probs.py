"""
## A. Concept Name
Knuth-Morris-Pratt (KMP) Algorithm Problems

## B. Core Concept
The KMP algorithm is used for pattern matching in strings. It preprocesses the pattern to find the Longest Proper Prefix which is also a Suffix (LPS) array, which allows the algorithm to skip unnecessary comparisons.

## C. Key Components
1. LPS Array Computation: Computes the length of the longest proper prefix that is also a suffix for every prefix of the pattern.
2. Pattern Matching: Uses the LPS array to find all occurrences of the pattern in the text in O(N + M) time.

## D. Best Practices
1. Properly handle 0-indexing for arrays.
2. Use LPS array to avoid redundant comparisons.
3. Keep logic clean when matching fails by correctly jumping `j = lps[j-1]`.

## E. Real-world Analogies
Imagine searching for a specific sequence of musical notes in a long piece. Instead of restarting the search from the next note every time there's a mismatch, you jump ahead based on the repeating sequences you've already identified within your target sequence.

## F. Memory Model / Data Flow
- `text`: The string in which we are searching.
- `pattern`: The string we want to find.
- `lps`: Array of size equal to pattern length, storing skip values.
Data flows from text characters matching against pattern characters. On mismatch, pattern index skips backward based on `lps`.

## G. Common Pitfalls
1. Re-calculating the LPS unnecessarily.
2. Out of bounds index errors when `j=0` and a mismatch occurs.
3. Forgetting to increment indices correctly after a match is found to find overlapping matches.

## H. Code Structure
- `compute_lps(pattern)`: Function to generate the LPS array.
- `kmp_search(text, pattern)`: Function to perform the actual search.

## I. Edge Cases
- Empty text or empty pattern.
- Pattern longer than text.
- Pattern not found in text.
- Text consists of all identical characters.

## J. Algorithmic Complexity
- Time Complexity: O(N + M) where N is the length of text and M is the length of pattern.
- Space Complexity: O(M) for storing the LPS array.

## K. AI Prompting
To use AI for generating KMP code: "Write a Python function implementing the KMP algorithm to find all starting indices of a pattern in a text string. Include the LPS array computation."

## L. Diagram / Visual
Text:    A B A B D A B A C D A B A B C
Pattern: A B A B C
LPS:     0 0 1 2 0

## M. Step-by-Step Execution
1. Compute LPS for the pattern.
2. Initialize pointers `i = 0` for text, `j = 0` for pattern.
3. If `text[i] == pattern[j]`, increment both.
4. If `j == len(pattern)`, match found! Add index to results, set `j = lps[j-1]`.
5. Else if mismatch and `j > 0`, set `j = lps[j-1]`.
6. Else if mismatch and `j == 0`, increment `i`.

## N. Alternate Approaches
- Naive String Matching (O(N*M))
- Rabin-Karp Algorithm (O(N+M) average, uses hashing)
- Z Algorithm (O(N+M), uses Z-array)

## O. Related Concepts
- Longest Palindromic Substring
- String Automaton
- Trie Data Structure

## P. Testing & Debugging
- Test with pattern completely matching the text.
- Test with pattern not in text.
- Test with repeating characters.
- Use print statements inside the mismatch block to see the `j` pointer jumps.

## Q. Optimization Techniques
- Avoid unnecessary function calls inside the loops.
- Use early termination if the remaining text length is less than the remaining pattern length.

## R. Security/Safety
- Ensure large texts do not cause memory issues; although KMP only needs O(M) extra space, loading the entire text might be an issue. Process text in chunks if necessary (streaming KMP).

## S. Deployment/Scale
- KMP is highly suitable for streaming data as it processes the text strictly linearly without looking back.

## T. Modern Python Features
- Use type hinting (`List[int]`, `str`).
- Use generator functions if yielding matches one by one is preferred over returning a list.

## U. Interactive Exploration
Try modifying the pattern to "AAAAA" and text to "AAAAAAAA" to see how overlapping matches are found.

## V. Exercises
1. Modify KMP to count the number of occurrences of the pattern.
2. Use KMP to find the shortest repeating substring that makes up a given string.

## W. Additional Resources
- Introduction to Algorithms (CLRS)
- Competitive Programming 3 by Steven Halim

## X. Project Connection
KMP is foundational for text editors (find/replace), bioinformatics (DNA sequence matching), and intrusion detection systems (matching signatures in network packets).
"""

from typing import List

def compute_lps(pattern: str) -> List[int]:
    """
    Computes the Longest Proper Prefix which is also Suffix (LPS) array.
    """
    m = len(pattern)
    if m == 0:
        return []
        
    lps = [0] * m
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Finds all occurrences of a pattern in a text using the KMP algorithm.
    Returns a list of starting indices.
    """
    if not pattern:
        return []
    
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    
    res = []
    i = 0  # index for text
    j = 0  # index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            
        if j == m:
            res.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
    return res

if __name__ == "__main__":
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    matches = kmp_search(text, pattern)
    print(f"Matches found at indices: {matches}")
