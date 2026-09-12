"""
Module: Advanced String Hashing (Double Hashing)

Learning Objectives:
1. Understand why single modulo hashing might lead to collisions in large inputs.
2. Implement Double Hashing to drastically reduce collision probabilities.
3. Use prefix hashes to query substring hashes in O(1) time.

Concept Explanation:
Advanced string hashing often uses polynomial rolling hash with two different bases and two different prime moduli (Double Hashing). By calculating the hash of prefixes, the hash of any substring can be retrieved in O(1) time, allowing for rapid comparisons of substrings.
"""

import time
from typing import List, Tuple

class AdvancedStringHash:
    def __init__(self, text: str):
        self.text = text
        self.n = len(text)
        
        self.p1, self.p2 = 31, 37
        self.m1, self.m2 = 10**9 + 7, 10**9 + 9
        
        self.hash1 = [0] * (self.n + 1)
        self.hash2 = [0] * (self.n + 1)
        self.pow1 = [1] * (self.n + 1)
        self.pow2 = [1] * (self.n + 1)
        
        self._build_hashes()

    def _build_hashes(self) -> None:
        for i in range(self.n):
            c = ord(self.text[i]) - ord('a') + 1
            self.hash1[i + 1] = (self.hash1[i] * self.p1 + c) % self.m1
            self.hash2[i + 1] = (self.hash2[i] * self.p2 + c) % self.m2
            self.pow1[i + 1] = (self.pow1[i] * self.p1) % self.m1
            self.pow2[i + 1] = (self.pow2[i] * self.p2) % self.m2

    def get_hash(self, i: int, j: int) -> Tuple[int, int]:
        """
        Returns the double hash of substring text[i:j+1] (0-indexed, inclusive).
        """
        length = j - i + 1
        h1 = (self.hash1[j + 1] - self.hash1[i] * self.pow1[length]) % self.m1
        if h1 < 0: h1 += self.m1
            
        h2 = (self.hash2[j + 1] - self.hash2[i] * self.pow2[length]) % self.m2
        if h2 < 0: h2 += self.m2
            
        return (h1, h2)

def performance_analysis() -> None:
    print("\n--- Performance Analysis ---")
    text = "abc" * 10000
    start = time.perf_counter()
    ash = AdvancedStringHash(text)
    build_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for i in range(1000):
        ash.get_hash(0, 50)
    query_time = time.perf_counter() - start
    
    print(f"Prefix Hashes Build Time (Length 30000): {build_time:.4f}s")
    print(f"1000 Substring Hash Queries Time: {query_time:.6f}s")

def edge_cases() -> None:
    print("\n--- Edge Cases ---")
    try:
        ash = AdvancedStringHash("")
        print("Empty string hash built successfully.")
    except Exception as e:
        print("Error with empty string:", e)

def interview_challenge() -> None:
    """
    Challenge: Find the longest common prefix of two substrings in O(log(min_len)) using binary search + string hashing.
    """
    print("\n--- Interview Challenge ---")
    text = "abacaba"
    ash = AdvancedStringHash(text)
    
    def lcp(i: int, j: int) -> int:
        low, high = 1, min(len(text) - i, len(text) - j)
        ans = 0
        while low <= high:
            mid = (low + high) // 2
            if ash.get_hash(i, i + mid - 1) == ash.get_hash(j, j + mid - 1):
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        return ans

    print(f"LCP of 'aba...' (idx 0) and 'aba...' (idx 4): {lcp(0, 4)}")
    print(f"LCP of 'aca...' (idx 2) and 'aba...' (idx 0): {lcp(2, 0)}")

def run_tests() -> None:
    ash = AdvancedStringHash("abacaba")
    assert ash.get_hash(0, 2) == ash.get_hash(4, 6) # 'aba' == 'aba'
    assert ash.get_hash(0, 1) == ash.get_hash(4, 5)
    assert ash.get_hash(0, 3) != ash.get_hash(1, 4) # 'abac' != 'baca'
    print("All tests passed!")

if __name__ == "__main__":
    print("Advanced String Hashing\n" + "="*23)
    run_tests()
    edge_cases()
    interview_challenge()
    performance_analysis()
