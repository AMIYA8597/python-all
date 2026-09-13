"""
Advanced Tree Patterns (Trie, Segment Tree, etc.)
=================================================

Learning Objectives:
1. Understand the structure and use cases of advanced tree data structures.
2. Implement a Trie (Prefix Tree) for efficient string matching.
3. Learn Segment Tree basics for range queries.

Concept Explanation:
While standard binary search trees handle general dynamic datasets well, certain
problems require specialized trees. A Trie is excellent for string prefixes and
dictionary problems. A Segment Tree is used for range queries (like sum or min)
over an array where elements can be updated.

In this module, we focus heavily on the Trie pattern.
"""

from typing import List, Optional, Dict
import unittest
import time

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word: bool = False

class Trie:
    """Basic Implementation of a Prefix Tree."""
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
        """Returns if the word is in the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
        
    def startsWith(self, prefix: str) -> bool:
        """Returns if there is any word in the trie that starts with the given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

class AdvancedTrieFeatures:
    """Intermediate/Advanced Implementation: Word Search II."""
    
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Given an m x n board of characters and a list of strings words, return all words on the board.
        Uses Trie + Backtracking.
        """
        trie = Trie()
        for word in words:
            trie.insert(word)
            
        ROWS, COLS = len(board), len(board[0])
        res, visit = set(), set()
        
        def dfs(r: int, c: int, node: TrieNode, word: str):
            if (r < 0 or c < 0 or 
                r == ROWS or c == COLS or 
                (r, c) in visit or board[r][c] not in node.children):
                return
            
            visit.add((r, c))
            node = node.children[board[r][c]]
            word += board[r][c]
            if node.is_end_of_word:
                res.add(word)
                
            dfs(r + 1, c, node, word)
            dfs(r - 1, c, node, word)
            dfs(r, c + 1, node, word)
            dfs(r, c - 1, node, word)
            
            visit.remove((r, c))
            
        for r in range(ROWS):
            for c in range(COLS):
                dfs(r, c, trie.root, "")
                
        return list(res)

# --- Performance Analysis ---
# Trie Insert: O(L) where L is the length of the word.
# Trie Search: O(L). Space Complexity: O(N * L) for N words of length L.
# Edge Cases: Empty strings, very long words, characters outside a-z.

# --- Interview Challenge ---
# Implement a basic segment tree for range sum query.

class TestAdvancedTree(unittest.TestCase):
    def test_trie(self):
        trie = Trie()
        trie.insert("apple")
        self.assertTrue(trie.search("apple"))
        self.assertFalse(trie.search("app"))
        self.assertTrue(trie.startsWith("app"))
        trie.insert("app")
        self.assertTrue(trie.search("app"))

    def test_word_search(self):
        board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
        words = ["oath","pea","eat","rain"]
        solution = AdvancedTrieFeatures()
        res = solution.findWords(board, words)
        self.assertCountEqual(res, ["eat", "oath"])

if __name__ == '__main__':
    unittest.main()
