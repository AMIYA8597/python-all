"""
Module: Advanced String Algorithms Mastery (KMP & Z-Algorithm)

Learning Objectives:
1. Synthesize knowledge of advanced string matching techniques.
2. Implement the Z-Algorithm and understand its Z-array.
3. Compare prefix-based matching (KMP/Z) with hash-based matching.

Concept Explanation:
The Z-Algorithm finds all occurrences of a pattern in a text in linear time O(N + M). It builds a Z-array where Z[i] is the length of the longest substring starting from text[i] which is also a prefix of the text. It's often used by concatenating Pattern + '$' + Text.
"""

import time
from typing import List

def build_z_array(s: str) -> List[int]:
    n = len(s)
    z = [0] * n
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

def z_algorithm_search(pattern: str, text: str) -> List[int]:
    if not pattern or not text:
        return []
    
    concat = pattern + "$" + text
    z_array = build_z_array(concat)
    
    results = []
    p_len = len(pattern)
    for i in range(len(concat)):
        if z_array[i] == p_len:
            # i - p_len - 1 gives the correct index in the original text
            results.append(i - p_len - 1)
    return results

def performance_analysis() -> None:
    print("\n--- Performance Analysis ---")
    text = "A" * 100000 + "B"
    pattern = "A" * 1000
    
    start = time.perf_counter()
    z_algorithm_search(pattern, text)
    search_time = time.perf_counter() - start
    print(f"Z-Algorithm Search Time (Text 100,000, Pattern 1,000): {search_time:.4f}s")

def edge_cases() -> None:
    print("\n--- Edge Cases ---")
    print("Empty pattern:", z_algorithm_search("", "text"))
    print("Pattern larger than text:", z_algorithm_search("toolong", "short"))
    print("No match:", z_algorithm_search("xyz", "abc"))

def interview_challenge() -> None:
    """
    Challenge: Determine if one string is a cyclic rotation of another.
    """
    print("\n--- Interview Challenge ---")
    def is_rotation(s1: str, s2: str) -> bool:
        if len(s1) != len(s2) or not s1:
            return False
        concat = s2 + s2
        # Using Z-algorithm to find s1 in s2+s2
        matches = z_algorithm_search(s1, concat)
        return len(matches) > 0

    s1 = "waterbottle"
    s2 = "erbottlewat"
    print(f"Is '{s2}' a rotation of '{s1}'? {is_rotation(s1, s2)}")

def run_tests() -> None:
    assert z_algorithm_search("aab", "baabaaab") == [1, 5]
    assert z_algorithm_search("abc", "abcabcabc") == [0, 3, 6]
    assert build_z_array("abacaba")[4] == 3
    print("All tests passed!")

if __name__ == "__main__":
    print("Advanced String Algorithms Mastery\n" + "="*34)
    run_tests()
    edge_cases()
    interview_challenge()
    performance_analysis()
