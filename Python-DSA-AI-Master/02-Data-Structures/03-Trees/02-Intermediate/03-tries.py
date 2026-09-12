"""
## A. Concept Name
Tries (Prefix Trees)

## B. One-Sentence Definition
A Trie is a tree-like data structure that stores a dynamic set of strings, where each node represents a single character of a string, allowing for fast retrieval based on string prefixes.

## C. Why Does This Exist?
Traditional structures like Hash Tables are great for exact matches, and Binary Search Trees are good for ordered data, but neither is efficient for prefix-based searches (like autocomplete or finding all words starting with "app"). Tries exist to solve the prefix matching problem optimally.

## D. Intuition
Instead of storing entire words in separate nodes, a Trie stores words path by path. Words that share a common prefix share the same ancestral nodes, meaning "cat" and "cab" share the nodes for 'c' and 'a', branching only at 't' and 'b'.

## E. Real-Life Analogy
Think of a physical dictionary. You don't read every word to find "zebra". You go to the 'z' section, then the 'ze' page, then 'zeb'. The trie works exactly like thumbing through the dictionary letter by letter.

## F. Mental Model
Visualize a tree where the root is empty. Each edge down represents a letter. A path from the root to a node spells out a prefix. A special flag (usually a boolean `is_end_of_word`) is placed on a node to signify that the path from the root to this node constitutes a complete word.

## G. Visual Explanation
Root
 |-- a (is_end=False)
 |   `-- p (is_end=False)
 |       `-- p (is_end=True) -> "app"
 |           `-- l (is_end=False)
 |               `-- e (is_end=True) -> "apple"
 |-- b (is_end=False)
     `-- a (is_end=False)
         `-- t (is_end=True) -> "bat"

## H. Formal Explanation
A trie is an ordered tree data structure used to store a dynamic set or associative array where the keys are usually strings. Unlike a binary search tree, no node in the tree stores the key associated with that node; instead, its position in the tree defines the key with which it is associated.

## I. Mathematical Foundation
Time Complexity is bounded by O(L) where L is the length of the string, which is typically much smaller than N (total strings) or the total characters in the dataset. Total space complexity is O(V * A) where V is the total number of nodes and A is the alphabet size, though space can be optimized (e.g., using hash maps for children).

## J. From-Scratch Implementation
(See the code below using `TrieNode` and `Trie` classes)

## K. Library / Production Implementation
Python doesn't have a built-in trie. Production systems often use specialized C/C++ implementations, or packages like `pytrie` or `datrie` (Double-Array Trie) for memory efficiency. 

## L. Trace (walk through example)
Insert "cat":
- Start at root.
- 'c' not in root's children. Add 'c' node. Move to 'c'.
- 'a' not in 'c's children. Add 'a' node. Move to 'a'.
- 't' not in 'a's children. Add 't' node. Move to 't'.
- Mark 't' node as `is_end_of_word = True`.

## M. Complexity
- **Time Complexity:**
  - Insert: O(L) where L is string length.
  - Search: O(L).
  - StartsWith: O(L).
- **Space Complexity:**
  - O(N * L * A) worst case, where N is number of words, L is max length, A is alphabet size.

## N. Common Mistakes
- Forgetting to mark `is_end_of_word = True` at the end of an insertion.
- Not checking the `is_end_of_word` flag during `search` (and just returning True if the path exists).
- Using a fixed array of size 26 for children when the input can contain uppercase, numbers, or symbols.

## O. Common Confusions
- **Trie vs Hash Map:** Why use a Trie if Hash Map has O(1) lookup? A Hash Map can't easily find all words starting with "auto", whereas a Trie can do this trivially. Hash Map lookup depends on string hashing which takes O(L) time anyway.
- **Trie vs Prefix Hash Map:** You could hash all prefixes, but that takes massive amounts of memory compared to a Trie's structural sharing.

## P. When To Use
- Autocomplete systems.
- Spell checkers.
- IP routing (Longest Prefix Matching).
- Boggle / Word Search solver algorithms on a grid.

## Q. When NOT To Use
- When you only need exact string matching (use Hash Table / `set`).
- When memory is highly constrained (standard tries have a high memory overhead per character; consider Radix Trees / Patricia Tries instead).

## R. Trade-offs
- **Pros:** Fast prefix lookups, no hash collisions, alphabetically ordered iteration is trivial.
- **Cons:** High memory usage due to node object overhead and empty pointers, poor cache locality compared to flat arrays.

## S. Debugging
- Check if your `is_end_of_word` is set correctly.
- Print the trie by recursively doing a Pre-order traversal to see the exact structure.
- Ensure you are iterating over the correct string (character by character).

## T. Memory Hook
"Trie to re-TRIE-ve the PREFIX." (The name comes from retrieval).

## U. Active Recall
- What is the time complexity of searching a word of length L?
- How does a Trie save space compared to a list of strings?
- What distinguishes a `search` method from a `starts_with` method?

## V. Practice
- Implement an autocomplete system.
- Solve Leetcode 208: Implement Trie (Prefix Tree).
- Solve Leetcode 212: Word Search II.

## W. Interview Question
"Design a data structure that supports adding new words and finding if a string matches any previously added string. The find method can contain the dot '.' character which acts as a wildcard matching any single character." (Design Add and Search Words Data Structure).

## X. Project Connection
Build a command-line autocomplete for your shell, or a fast dictionary spelling recommender for a text editor.
"""

from typing import Dict, List

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    """Basic/Intermediate Implementation of a Trie."""
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the trie."""
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Returns if the word is in the trie."""
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Returns if there is any word in the trie that starts with the given prefix."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def _get_words_from_node(self, node: TrieNode, prefix: str, results: List[str]):
        """Helper to collect all words starting from a given node."""
        if node.is_end_of_word:
            results.append(prefix)
        for char, child_node in node.children.items():
            self._get_words_from_node(child_node, prefix + char, results)

    def autocomplete(self, prefix: str) -> List[str]:
        """Advanced: Returns all words that start with the prefix."""
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]
        
        results: List[str] = []
        self._get_words_from_node(current, prefix, results)
        return results

# Performance Analysis:
# Time Complexity:
# - Insert/Search/StartsWith: O(L) where L is the length of the word
# Space Complexity: O(N * L) where N is the number of words, due to storing children

# Edge Cases:
# - Empty string insertion/search
# - Substring matching (handled correctly by is_end_of_word flag)
# - Very long common prefixes (compact tries / radix trees are more memory-efficient here)

def test_trie():
    trie = Trie()
    words = ["apple", "app", "application", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)

    assert trie.search("apple") is True
    assert trie.search("app") is True
    assert trie.search("appl") is False
    assert trie.starts_with("app") is True
    assert trie.starts_with("cat") is False

    suggestions = trie.autocomplete("ban")
    assert sorted(suggestions) == ["banana", "band", "bandana"]

    print("Trie basic tests passed!")

if __name__ == "__main__":
    test_trie()
