"""
## A. Concept Name
Trie (Prefix Tree) Problems

## B. Intuition / Analogy
Imagine a filing cabinet where the first letter determines the drawer, the second determines the folder, and so on.

## C. Core Logic
A tree structure where each node represents a character, and paths from root to node represent strings.

## D. Time Complexity
Insert/Search: O(L) where L is the length of the string.

## E. Space Complexity
O(N * L * Alphabet_Size) where N is number of strings.

## F. Implementation Details
Nodes contain a hash map or array of children and a boolean flag `is_end_of_word`.

## G. Common Variants
- Bitwise Trie for maximum XOR problems
- Compressed Trie / Radix Tree

## H. Edge Cases
- Empty strings
- Strings that are prefixes of other strings

## I. Common Pitfalls
- Forgetting to mark `is_end_of_word` during insertion.

## J. Testing Strategies
Test with overlapping prefixes, identical strings, and empty strings.

## K. Related Concepts
- Suffix Trees
- Suffix Automata
- Aho-Corasick Algorithm

## L. Design Patterns
Node-based tree traversal.

## M. Memory Management
Python garbage collection handles unreferenced nodes natively.

## N. Performance Optimization
Use arrays instead of dicts for children if the alphabet is small and dense.

## O. Scalability
Distributed Tries can be used for massive datasets in production.

## P. Debugging Techniques
Print traversal path to visualize prefix sharing.

## Q. Refactoring Potential
Abstracting the Trie Node into its own class for clarity.

## R. Code Readability
Meaningful variable names like `curr_node`.

## S. Maintenance
Keep operations simple, modular, and well-commented.

## T. Security Implications
DOS attacks with deeply nested tries (excessive memory consumption).

## U. Best Practices
Encapsulate node logic to prevent external modification of the tree structure.

## V. Alternative Approaches
Hash sets for exact match (O(1)), but they lack fast prefix search capabilities.

## W. Future Enhancements
Add deletion operation and autocomplete suggestion generators.

## X. Project Connection
Used in the AI Engine's Natural Language Processing module for fast tokenization and autocomplete features.
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word: str) -> None:
        """Inserts a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        
    def search(self, word: str) -> bool:
        """Returns True if the word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        """Returns True if there is any previously inserted word that has the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

if __name__ == "__main__":
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True
    trie.insert("app")
    assert trie.search("app") is True
    print("All basic Trie operations passed!")
