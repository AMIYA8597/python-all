"""
## A. Concept Name
Advanced Trees: Suffix Trees

## B. Problem Statement
String matching, finding substrings, and finding the longest repeated substrings are fundamental operations in text processing, but naive approaches can be slow for large texts.

## C. Learning Objectives
1. Understand the purpose of a Suffix Tree in string matching.
2. Implement a basic (naive) Suffix Tree for educational purposes.
3. Use a Suffix Tree for fast substring searches.

## D. Concept Explanation
A Suffix Tree is a compressed trie containing all the suffixes of a given text as their keys and positions in the text as their values. 
Suffix trees allow particularly fast implementations of many important string operations like finding a substring, finding the longest repeated substring, etc.
While Ukkonen's algorithm constructs a suffix tree in O(N) time, we will explore a naive O(N^2) construction (uncompressed trie) to understand the underlying structure clearly.

## E. Performance Analysis
- Naive Construction: O(N^2) time complexity, where N is string length.
- Ukkonen's Construction (not shown): O(N) time complexity.
- Search (Substring): O(M) time complexity, where M is pattern length.
- Space Complexity: O(N^2) for naive, O(N) for compressed.

## F. Edge Cases Handled
- Searching for patterns that don't exist.
- Overlapping pattern matches.
- String ending with terminal character ($).

## G. Interview Challenge
Q: Why append a terminal character like '$' to the text?
A: It ensures that no suffix is a prefix of another suffix. This guarantees that every 
   suffix ends at a distinct leaf node, making the tree representation explicit and correct.

## X. Project Connection
Suffix trees are foundational for algorithms in bioinformatics (e.g., DNA sequence alignment) and search engines, where efficient text processing and pattern matching are critical for performance.
"""

from typing import Dict, List

class SuffixTreeNode:
    def __init__(self):
        self.children: Dict[str, 'SuffixTreeNode'] = {}
        # Stores indices of the suffixes that pass through this node
        self.indexes: List[int] = []

    def insert_suffix(self, suffix: str, index: int) -> None:
        """
        Insert a suffix into the tree recursively.
        """
        self.indexes.append(index)
        if len(suffix) > 0:
            char = suffix[0]
            if char not in self.children:
                self.children[char] = SuffixTreeNode()
            self.children[char].insert_suffix(suffix[1:], index)

    def search(self, pattern: str) -> List[int]:
        """
        Search for a pattern in the tree.
        """
        if len(pattern) == 0:
            return self.indexes
        
        char = pattern[0]
        if char in self.children:
            return self.children[char].search(pattern[1:])
        else:
            return []


class SuffixTree:
    def __init__(self, text: str):
        """
        Initialize and construct the suffix tree for the given text.
        """
        self.root = SuffixTreeNode()
        self.text = text
        # Append a special termination character '$' to ensure no suffix is a prefix of another
        if not text.endswith('$'):
            self.text += '$'
            
        self._construct_tree()

    def _construct_tree(self) -> None:
        """
        Naive construction: insert all suffixes one by one.
        O(N^2) where N is length of text.
        """
        for i in range(len(self.text)):
            suffix = self.text[i:]
            self.root.insert_suffix(suffix, i)

    def search(self, pattern: str) -> List[int]:
        """
        Search for a pattern and return starting indices in the original text.
        """
        return self.root.search(pattern)


def test_suffix_tree():
    print("--- Suffix Tree Operations ---")
    text = "banana"
    print(f"Building suffix tree for text: '{text}'")
    st = SuffixTree(text)

    patterns = ["nan", "ana", "ban", "xyz", "a"]
    for pat in patterns:
        indexes = st.search(pat)
        if indexes:
            print(f"Pattern '{pat}' found at indices: {indexes}")
            # Verify the match
            for idx in indexes:
                print(f"  -> matches substring: '{text[idx:idx+len(pat)]}'")
        else:
            print(f"Pattern '{pat}' NOT found.")

if __name__ == "__main__":
    test_suffix_tree()
