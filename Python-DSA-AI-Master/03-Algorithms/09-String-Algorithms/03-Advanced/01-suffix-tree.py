"""
Module: Suffix Tree Algorithms

Learning Objectives:
1. Understand the concept of a suffix tree and its applications.
2. Learn how to construct a basic suffix tree.
3. Apply suffix trees to solve string matching and substring problems.

Concept Explanation:
A suffix tree is a compressed trie containing all the suffixes of the given text as their keys and positions in the text as their values. It allows particularly fast implementations of many important string operations.
Although optimal construction (Ukkonen's algorithm) takes O(N) time, a basic O(N^2) insertion method provides a great learning foundation for understanding the tree's structure and querying mechanism.
"""

import time
from typing import List, Dict, Optional

class SuffixTreeNode:
    def __init__(self):
        self.children: Dict[str, 'SuffixTreeNode'] = {}
        self.indexes: List[int] = []

    def insert_suffix(self, suffix: str, index: int) -> None:
        self.indexes.append(index)
        if len(suffix) > 0:
            char = suffix[0]
            if char not in self.children:
                self.children[char] = SuffixTreeNode()
            self.children[char].insert_suffix(suffix[1:], index)

class SuffixTree:
    """
    Basic O(N^2) Suffix Tree Implementation.
    """
    def __init__(self, text: str):
        self.text = text
        self.root = SuffixTreeNode()
        # Build the tree by inserting all suffixes
        for i in range(len(text)):
            self.root.insert_suffix(text[i:], i)

    def search(self, pattern: str) -> List[int]:
        """
        Search for a pattern in the suffix tree.
        Time Complexity: O(M) where M is the length of the pattern.
        """
        current = self.root
        for char in pattern:
            if char not in current.children:
                return []
            current = current.children[char]
        return current.indexes

def advanced_longest_repeated_substring(text: str) -> str:
    """
    Advanced implementation: Using a suffix tree-like approach to find the longest repeated substring.
    For simplicity in this demonstration, we'll simulate it using a basic tree structure.
    """
    st = SuffixTree(text)
    longest = ""
    
    def dfs(node: SuffixTreeNode, current_str: str):
        nonlocal longest
        # If a node has more than 1 index, it represents a repeated substring
        if len(node.indexes) > 1 and len(current_str) > len(longest):
            longest = current_str
        for char, child in node.children.items():
            dfs(child, current_str + char)
            
    dfs(st.root, "")
    return longest

def performance_analysis() -> None:
    print("\n--- Performance Analysis ---")
    text = "a" * 500 + "b"
    start = time.perf_counter()
    st = SuffixTree(text)
    build_time = time.perf_counter() - start
    
    start = time.perf_counter()
    res = st.search("a" * 50)
    search_time = time.perf_counter() - start
    
    print(f"Build Time (501 chars, O(N^2)): {build_time:.4f}s")
    print(f"Search Time (Pattern length 50, O(M)): {search_time:.6f}s")

def edge_cases() -> None:
    print("\n--- Edge Cases ---")
    st = SuffixTree("")
    print("Empty string search 'a':", st.search("a"))
    st_single = SuffixTree("a")
    print("Single char string search 'a':", st_single.search("a"))

def interview_challenge() -> None:
    """
    Interview Challenge:
    Given a string, find the longest repeated substring. If there are multiple, return any.
    """
    print("\n--- Interview Challenge ---")
    text = "banana"
    print(f"Longest repeated substring in '{text}':", advanced_longest_repeated_substring(text))

def run_tests() -> None:
    st = SuffixTree("banana")
    assert sorted(st.search("ana")) == [1, 3], "Test failed for 'ana'"
    assert st.search("nana") == [2], "Test failed for 'nana'"
    assert st.search("xyz") == [], "Test failed for 'xyz'"
    assert advanced_longest_repeated_substring("banana") in ["ana", "nan"], "LRS test failed"
    print("All tests passed!")

if __name__ == "__main__":
    print("Suffix Tree Algorithms\n" + "="*22)
    run_tests()
    edge_cases()
    interview_challenge()
    performance_analysis()
