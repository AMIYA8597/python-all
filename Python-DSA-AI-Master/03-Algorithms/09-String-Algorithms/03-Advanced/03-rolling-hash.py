"""
Module: Rolling Hash Algorithm

Learning Objectives:
1. Understand the concept of a rolling hash and its benefits for substring search.
2. Implement the Rabin-Karp algorithm using a rolling hash.
3. Manage hash collisions effectively.

Concept Explanation:
A rolling hash is a hash function where the input is hashed in a window that moves through the input. As the window moves, the hash value can be updated efficiently (in O(1) time) without recalculating the hash for the entire window from scratch. It forms the basis of the Rabin-Karp string matching algorithm.
"""

import time
from typing import List, Tuple

class RollingHash:
    def __init__(self, base: int = 256, prime: int = 101):
        self.base = base
        self.prime = prime

    def rabin_karp_search(self, pattern: str, text: str) -> List[int]:
        m = len(pattern)
        n = len(text)
        if m == 0 or n == 0 or m > n:
            return []

        results = []
        p_hash = 0
        t_hash = 0
        h = 1

        # The value of h would be "pow(base, m-1) % prime"
        for i in range(m - 1):
            h = (h * self.base) % self.prime

        # Calculate the hash value of pattern and first window of text
        for i in range(m):
            p_hash = (self.base * p_hash + ord(pattern[i])) % self.prime
            t_hash = (self.base * t_hash + ord(text[i])) % self.prime

        # Slide the pattern over text one by one
        for i in range(n - m + 1):
            # Check the hash values of current window of text and pattern.
            if p_hash == t_hash:
                # Check for characters one by one to handle collisions
                match = True
                for j in range(m):
                    if text[i + j] != pattern[j]:
                        match = False
                        break
                if match:
                    results.append(i)

            # Calculate hash value for next window of text
            if i < n - m:
                t_hash = (self.base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % self.prime
                # We might get negative value of t_hash, converting it to positive
                if t_hash < 0:
                    t_hash = t_hash + self.prime

        return results

def performance_analysis() -> None:
    print("\n--- Performance Analysis ---")
    rh = RollingHash()
    text = "A" * 10000 + "B"
    pattern = "A" * 1000 + "B"
    
    start = time.perf_counter()
    rh.rabin_karp_search(pattern, text)
    search_time = time.perf_counter() - start
    print(f"Rabin-Karp Search Time (Text len 10000, Pattern len 1000): {search_time:.4f}s")

def edge_cases() -> None:
    print("\n--- Edge Cases ---")
    rh = RollingHash()
    print("Pattern longer than text:", rh.rabin_karp_search("longer", "short"))
    print("Empty pattern:", rh.rabin_karp_search("", "text"))

def interview_challenge() -> None:
    """
    Challenge: Find repeated DNA sequences of length 10 using a rolling hash concept.
    """
    print("\n--- Interview Challenge ---")
    def find_repeated_dna(s: str) -> List[str]:
        L = 10
        if len(s) < L:
            return []
        
        seen = set()
        repeated = set()
        
        # Simplified rolling hash or just using Python's efficient string slicing + hashing
        for i in range(len(s) - L + 1):
            seq = s[i:i+L]
            if seq in seen:
                repeated.add(seq)
            else:
                seen.add(seq)
        return list(repeated)
        
    dna = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    print("Repeated DNA Sequences (len 10):", find_repeated_dna(dna))

def run_tests() -> None:
    rh = RollingHash()
    assert rh.rabin_karp_search("TEST", "THIS IS A TEST TEXT") == [10]
    assert rh.rabin_karp_search("AABA", "AABAACAADAABAABA") == [0, 9, 12]
    print("All tests passed!")

if __name__ == "__main__":
    print("Rolling Hash Algorithm\n" + "="*22)
    run_tests()
    edge_cases()
    interview_challenge()
    performance_analysis()
