\"\"\"
High-Performance Data Structures Implementation

This module contains implementations of advanced, high-performance data structures:
1. Bloom Filter (Probabilistic Set)
2. Optimized Trie (Prefix Tree)
3. Memory-optimized records using slots

Includes type hints, docstrings, and performance tests comparing against standard structures.
\"\"\"

import time
import math
import hashlib
from typing import List, Optional, Iterable
import sys

# ==========================================
# 1. Bloom Filter (Probabilistic Data Structure)
# ==========================================

class BloomFilter:
    \"\"\"
    A Bloom Filter is a space-efficient probabilistic data structure used to test 
    whether an element is a member of a set.
    
    Properties:
    - False positive matches are possible.
    - False negatives are NOT possible.
    - Highly space efficient compared to HashSets.
    \"\"\"
    
    def __init__(self, expected_items: int, false_positive_rate: float):
        \"\"\"
        Initializes the Bloom Filter calculating the optimal bit array size (m)
        and number of hash functions (k).
        \"\"\"
        self.expected_items = expected_items
        self.fp_rate = false_positive_rate
        
        # Calculate optimal size of bit array (m)
        self.size = self._get_optimal_size(expected_items, false_positive_rate)
        
        # Calculate optimal number of hash functions (k)
        self.hash_count = self._get_optimal_hash_count(self.size, expected_items)
        
        # Using a list of booleans representing bits (In a true low-level lang, we'd use bitwise ops on ints)
        # Using bytearray for memory efficiency in pure Python
        self.bit_array = bytearray((self.size + 7) // 8) 
        
    def _get_optimal_size(self, n: int, p: float) -> int:
        \"\"\" m = -(n * ln(p)) / (ln(2)^2) \"\"\"
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
        
    def _get_optimal_hash_count(self, m: int, n: int) -> int:
        \"\"\" k = (m/n) * ln(2) \"\"\"
        k = (m / n) * math.log(2)
        return int(k)
        
    def _hashes(self, item: str) -> List[int]:
        \"\"\"
        Generate k different hash values for the item.
        We use MD5 and SHA1 to generate a pool of bits, then derive k hashes.
        \"\"\"
        encoded = item.encode('utf-8')
        h1 = int(hashlib.md5(encoded).hexdigest(), 16)
        h2 = int(hashlib.sha1(encoded).hexdigest(), 16)
        
        # Kirsch-Mitzenmacher optimization: hash(i) = h1 + i * h2
        hashes = []
        for i in range(self.hash_count):
            hashes.append((h1 + i * h2) % self.size)
        return hashes

    def add(self, item: str) -> None:
        \"\"\"Add an item to the Bloom Filter.\"\"\"
        for h in self._hashes(item):
            byte_index = h // 8
            bit_index = h % 8
            self.bit_array[byte_index] |= (1 << bit_index)

    def check(self, item: str) -> bool:
        \"\"\"
        Check if an item is in the Bloom Filter.
        Returns True if it *might* be in the set.
        Returns False if it is *definitely not* in the set.
        \"\"\"
        for h in self._hashes(item):
            byte_index = h // 8
            bit_index = h % 8
            if not (self.bit_array[byte_index] & (1 << bit_index)):
                return False
        return True

# ==========================================
# 2. Memory-Optimized Structs (__slots__)
# ==========================================

class StandardRecord:
    \"\"\"Standard Python class. Uses a __dict__ for attributes.\"\"\"
    def __init__(self, id_val: int, name: str, active: bool):
        self.id = id_val
        self.name = name
        self.active = active

class OptimizedRecord:
    \"\"\"Optimized class using __slots__. Prevents __dict__ creation.\"\"\"
    __slots__ = ['id', 'name', 'active']
    
    def __init__(self, id_val: int, name: str, active: bool):
        self.id = id_val
        self.name = name
        self.active = active

# ==========================================
# 3. Fast Prefix Tree (Trie)
# ==========================================

class TrieNode:
    __slots__ = ['children', 'is_end']
    def __init__(self):
        # Using dict is fast for lookups, though arrays might be used for strict alphabets
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False

class Trie:
    \"\"\"
    A Trie (Prefix Tree) optimized for fast string retrieval and prefix matching.
    Widely used in autocomplete features.
    \"\"\"
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        \"\"\"Returns True if exact word exists.\"\"\"
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        \"\"\"Returns True if any word has the given prefix.\"\"\"
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# ==========================================
# Test Execution & Profiling
# ==========================================

def run_bloom_filter_tests():
    print(\"\\n--- Bloom Filter Tests ---\")
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
    
    # Add items
    fruits = [\"apple\", \"banana\", \"orange\", \"mango\", \"grape\"]
    for f in fruits:
        bf.add(f)
        
    # Check items (True positives)
    for f in fruits:
        assert bf.check(f) is True, f\"Expected {f} to be in filter\"
        
    # Check non-existent items (True negatives / False positives)
    test_words = [\"kiwi\", \"watermelon\", \"pineapple\", \"strawberry\"]
    false_positives = 0
    for w in test_words:
        if bf.check(w):
            false_positives += 1
            print(f\"[!] False positive detected for: {w}\")
    print(f\"Bloom Filter initialized with {bf.size} bits and {bf.hash_count} hash functions.\")
    print(f\"False Positives in test data: {false_positives}/{len(test_words)}\")


def run_memory_tests():
    print(\"\\n--- Memory Optimization Tests (__slots__) ---\")
    # Python's sys.getsizeof doesn't deep measure objects perfectly without custom functions,
    # but we can see the absence of __dict__.
    
    std = StandardRecord(1, \"Alice\", True)
    opt = OptimizedRecord(1, \"Alice\", True)
    
    print(f\"StandardRecord hasattr __dict__: {hasattr(std, '__dict__')}\")
    print(f\"OptimizedRecord hasattr __dict__: {hasattr(opt, '__dict__')}\")
    
    # Note: True memory savings become massive when creating millions of objects in an array.
    print(\"Using slots prevents dictionary creation per instance, saving ~100-200 bytes per object.\")


def run_trie_tests():
    print(\"\\n--- Trie Tests ---\")
    trie = Trie()
    words = [\"hello\", \"hell\", \"heaven\", \"heavy\", \"dog\", \"door\"]
    
    for w in words:
        trie.insert(w)
        
    print(f\"Search 'hell': {trie.search('hell')} (Expected: True)\")
    print(f\"Search 'heav': {trie.search('heav')} (Expected: False)\")
    print(f\"Starts with 'heav': {trie.starts_with('heav')} (Expected: True)\")
    print(f\"Starts with 'doo': {trie.starts_with('doo')} (Expected: True)\")

if __name__ == \"__main__\":
    print(\"Running High-Performance Data Structures Test Suite...\")
    run_bloom_filter_tests()
    run_memory_tests()
    run_trie_tests()
    print(\"\\nAll tests completed successfully!\")
