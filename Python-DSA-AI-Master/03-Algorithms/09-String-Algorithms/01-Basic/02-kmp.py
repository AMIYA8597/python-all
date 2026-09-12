"""
## A. Concept Name
Knuth-Morris-Pratt (KMP) Algorithm

## B. Core Idea
Searches for occurrences of a "word" (pattern) within a main "text string" by employing the observation that when a mismatch occurs, the word itself embodies sufficient information to determine where the next match could begin. This avoids redundant comparisons by precomputing an LPS (Longest Prefix Suffix) array.

## C. Real-World Analogy
Like sliding a patterned ruler over a text; when the pattern breaks, you shift the ruler to the right based on the repeating patterns within the ruler itself instead of starting over from the next character.

## D. Time Complexity
- Best Case: O(N) where N is text length
- Average Case: O(N + M) where M is pattern length
- Worst Case: O(N + M)

## E. Space Complexity
O(M) for storing the LPS array.

## F. In-Place
Not completely, requires O(M) auxiliary space for the LPS array.

## G. Stable
Not directly applicable (not a sorting algorithm), but finds matches in order.

## H. Recursive or Iterative
Iterative.

## I. Data Structure Used
Array / List (for LPS).

## J. Algorithmic Paradigm
String Matching / Precomputation.

## K. Pre-requisites
Arrays, String Manipulation, Loops.

## L. Applications
Text editors (search functionality), data scraping and parsing, bioinformatics (DNA sequence matching).

## M. Trade-offs
O(M) space overhead for building the LPS array. Excellent for long texts and small to medium patterns, but simple brute-force might be faster for very short patterns due to overhead.

## N. Common Mistakes
Off-by-one errors while building the LPS array. Forgetting that proper prefix means prefix strictly smaller than the substring.

## O. Optimization
The LPS array is an optimization over naive string matching to skip character comparisons.

## P. Testing Edge Cases
Empty pattern, pattern larger than text, no match found, text and pattern are identical, multiple overlapping matches.

## Q. Visual Trace
Text: A B A B D A B A C D A B A B C A B A B
Pattern: A B A B C
LPS of Pattern: [0, 0, 1, 2, 0]
Mismatch at D, we look up LPS for previous match.

## R. Interview Tips
Usually asked to test deep understanding of string matching. Often used as a sub-routine (e.g., check if a string is a rotation of another).

## S. Code Variants
Rabin-Karp, Boyer-Moore, Z Algorithm.

## T. Related Concepts
Prefix Array, Suffix Automaton.

## U. Further Reading
Introduction to Algorithms (CLRS) - String Matching Chapter.

## V. FAQ
Q: Can KMP be used for multiple patterns? A: For multiple patterns, Aho-Corasick is preferred over multiple KMP runs.

## W. Practice Problems
Implement `strStr()` (LeetCode 28). Check if one string is a rotation of another.

## X. Project Connection
Used as a core text searching utility in text processing tools and DNA sequence matchers within larger projects.
"""

from typing import List

def compute_lps_array(pattern: str) -> List[int]:
    """
    Computes the Longest Prefix Suffix (LPS) array.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # length of the previous longest prefix suffix
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

def kmp_search_basic(text: str, pattern: str) -> List[int]:
    """
    Basic KMP Search.
    
    Args:
        text: The string to search in.
        pattern: The substring to search for.
        
    Returns:
        List of starting indices where pattern is found in text.
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return []

    lps = compute_lps_array(pattern)
    i = 0  # index for text
    j = 0  # index for pattern
    result = []

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result


class KMPMatcher:
    """
    Professional implementation of KMP algorithm.
    Encapsulates state and provides clean API for multiple searches with same pattern.
    """
    def __init__(self, pattern: str):
        if not isinstance(pattern, str):
            raise ValueError("Pattern must be a string.")
        self.pattern = pattern
        self.m = len(pattern)
        self.lps = self._build_lps()

    def _build_lps(self) -> List[int]:
        """Builds LPS table efficiently."""
        if not self.pattern:
            return []
        
        lps = [0] * self.m
        length = 0
        i = 1
        
        while i < self.m:
            if self.pattern[i] == self.pattern[length]:
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

    def find_all(self, text: str) -> List[int]:
        """Finds all occurrences of the pattern in the given text."""
        if not text or not self.pattern:
            return []
            
        n = len(text)
        occurrences = []
        i = j = 0
        
        while (n - i) >= (self.m - j):
            if self.pattern[j] == text[i]:
                j += 1
                i += 1
                
            if j == self.m:
                occurrences.append(i - j)
                j = self.lps[j - 1]
            elif i < n and self.pattern[j] != text[i]:
                if j != 0:
                    j = self.lps[j - 1]
                else:
                    i += 1
                    
        return occurrences


if __name__ == "__main__":
    print("Testing KMP Algorithm...")
    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    
    matches_basic = kmp_search_basic(text, pattern)
    assert matches_basic == [10], f"Expected [10], got {matches_basic}"
    
    matcher = KMPMatcher(pattern)
    matches_prof = matcher.find_all(text)
    assert matches_prof == [10], f"Expected [10], got {matches_prof}"
    
    # Test multiple matches
    text2 = "AAAAABAAABA"
    pattern2 = "AAAA"
    matcher2 = KMPMatcher(pattern2)
    assert matcher2.find_all(text2) == [0, 1]
    
    print("All tests passed successfully.")
