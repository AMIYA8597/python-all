"""
Huffman Coding

Learning Objectives:
1. Understand prefix-free encoding.
2. Implement Huffman coding tree construction using priority queues.
3. Encode and decode text using Huffman trees.

Concept Explanation:
Huffman coding is a lossless data compression algorithm. The idea is to assign variable-length codes 
to input characters, lengths of the assigned codes are based on the frequencies of corresponding characters.
The most frequent character gets the smallest code and the least frequent character gets the largest code.
It uses a binary tree (Huffman tree) where leaves represent characters and edges represent bits (0/1).

Performance Analysis:
- Time Complexity: O(N log N) where N is number of unique characters.
- Space Complexity: O(N) to store the tree and code mapping.

Edge Cases:
- Empty string.
- String with only one unique character.

Interview Challenge:
"Implement Huffman encoding and decoding."
"""

import heapq
from collections import Counter
from typing import Dict, Any
import unittest

class Node:
    def __init__(self, char: str, freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    def __lt__(self, other):
        return self.freq < other.freq

def huffman_coding_basic(text: str) -> Dict[str, str]:
    """Basic implementation to generate Huffman codes for a string."""
    if not text:
        return {}
        
    freqs = Counter(text)
    if len(freqs) == 1:
        return {list(freqs.keys())[0]: "0"}
        
    heap = [Node(char, freq) for char, freq in freqs.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
        
    codes = {}
    
    def generate_codes(node, current_code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")
        
    generate_codes(heap[0], "")
    return codes

def huffman_encode(text: str, codes: Dict[str, str]) -> str:
    """Encode text using generated codes."""
    return "".join(codes[char] for char in text)

def huffman_decode(encoded_text: str, root: Node) -> str:
    """Decode text using the Huffman tree."""
    if not root:
        return ""
        
    decoded_text = ""
    current = root
    
    # Handle single character case
    if not root.left and not root.right:
        return root.char * len(encoded_text)
        
    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right
            
        if current.char is not None:
            decoded_text += current.char
            current = root
            
    return decoded_text

class HuffmanTree:
    """Advanced implementation encapsulating the tree and codes."""
    def __init__(self):
        self.root = None
        self.codes = {}
        
    def build(self, text: str):
        if not text:
            return
            
        freqs = Counter(text)
        heap = [Node(char, freq) for char, freq in freqs.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
            
        self.root = heap[0] if heap else None
        
        if self.root and not self.root.left and not self.root.right:
            self.codes[self.root.char] = "0"
            return
            
        def _generate(node, current):
            if node:
                if node.char is not None:
                    self.codes[node.char] = current
                _generate(node.left, current + "0")
                _generate(node.right, current + "1")
                
        _generate(self.root, "")

    def encode(self, text: str) -> str:
        if not self.codes:
            return ""
        return "".join(self.codes[char] for char in text)
        
    def decode(self, encoded: str) -> str:
        return huffman_decode(encoded, self.root)

class TestHuffman(unittest.TestCase):
    def test_basic(self):
        codes = huffman_coding_basic("BCCABBDDAECCBBAEDDCC")
        self.assertTrue('A' in codes)
        self.assertTrue('B' in codes)
        
    def test_advanced(self):
        tree = HuffmanTree()
        text = "hello world"
        tree.build(text)
        encoded = tree.encode(text)
        self.assertEqual(tree.decode(encoded), text)
        
    def test_single_char(self):
        tree = HuffmanTree()
        text = "aaaa"
        tree.build(text)
        encoded = tree.encode(text)
        self.assertEqual(tree.decode(encoded), text)

if __name__ == "__main__":
    unittest.main()
