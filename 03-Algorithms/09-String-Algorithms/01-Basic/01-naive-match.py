"""
# ==============================================================================
# LABORATORY: NAIVE STRING MATCHING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You press `Ctrl+F` in your browser to search for a word on a webpage.
# How does the computer physically find your `pattern` string (length M) 
# hidden inside the massive `text` string (length N)?
#
# The most fundamental baseline is the Naive String Matching Algorithm.
# 1. Align the pattern with the very beginning of the text.
# 2. Check every character one by one.
# 3. If a character mismatches, STOP. 
# 4. Shift the pattern exactly 1 space to the right, and start checking again!
#
# The fatal flaw of the Naive algorithm is its absolute lack of "Memory".
# Imagine the Text is "AAAAAAAAAB" and the Pattern is "AAAAAB".
# - Shift 0: Checks 5 'A's, fails on 'B'.
# - Shift 1: Shifts right by 1. IT COMPLETELY FORGETS IT JUST SAW 5 'A's. 
#            It painstakingly checks 4 'A's again, and fails on 'B'.
# 
# Because of this amnesia, the Time Complexity in the absolute worst-case is 
# exactly O(N * M). If the webpage is 1 Million characters, and you search for 
# a 1,000 character string of repeated letters, it will execute 1 Billion checks!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the sliding window index math (`N - M + 1`).
# - Implement the double loop architecture.
# - Understand the pathological worst-case scenario.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. NAIVE STRING MATCHING ENGINE (O(N * M))
# ==============================================================================
def naive_string_match(text: str, pattern: str) -> List[int]:
    """
    Returns a list of all starting indices in `text` where `pattern` is found.
    """
    n = len(text)
    m = len(pattern)
    
    # Edge cases
    if m == 0: return []
    if m > n: return []
    
    found_indices = []
    
    # 1. THE SLIDING WINDOW OUTER LOOP
    # We slide the window from index 0 up to `n - m`. 
    # Why `n - m`? Because if the remaining text is SHORTER than the pattern, 
    # it is mathematically impossible for the pattern to fit!
    for i in range(n - m + 1):
        
        match_found = True
        
        # 2. THE CHARACTER CHECK INNER LOOP
        for j in range(m):
            
            # Compare the j-th character of the pattern with the (i + j)-th 
            # character of the text!
            if text[i + j] != pattern[j]:
                match_found = False
                break # Mismatch! Instantly halt the inner loop.
                
        # 3. VERIFICATION
        if match_found:
            found_indices.append(i)
            
    return found_indices


def demonstrate_naive_match():
    section_header("Algorithm: Naive String Search")
    
    # --- Best Case / Average Case (English Text) ---
    text1 = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    pattern1 = "THE"
    
    print(f"Text: '{text1}'")
    print(f"Pattern: '{pattern1}'")
    
    indices = naive_string_match(text1, pattern1)
    print(f"Found at indices: {indices}")
    
    # --- The Pathological Worst-Case ---
    section_header("The Pathological Worst-Case O(N*M)")
    
    text2 = "A" * 50 + "B"
    pattern2 = "A" * 10 + "B"
    
    print(f"Text: '{text2}'")
    print(f"Pattern: '{pattern2}'")
    print("\nObservation:")
    print("The inner loop will successfully check 10 'A's before finally failing on the 'B'.")
    print("The outer loop shifts by 1, and the inner loop stupidly repeats the 10 'A' checks!")
    print("This requires 40 * 10 = 400 operations to search a tiny 50-character string!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the outer loop bound `n - m + 1` instead of `n`?
   Answer: Optimization and safety. If the text is "HELLO" (length 5) and the pattern is "LL" (length 2), the maximum possible starting index is `5 - 2 = 3` (which is the letter 'L'). If the loop started at index 4 ('O'), the inner loop would attempt to read `text[4 + 1]`, throwing a fatal `IndexError: string index out of range`. 

2. Why is Naive Search still used in the real world?
   Answer: In practical, real-world English text (or source code), the pathological case `AAAAAAAB` almost never occurs. When searching English text, the FIRST character of the pattern usually mismatches immediately. If it mismatches immediately, the inner loop halts in $O(1)$ time! Therefore, the practical average-case time complexity of Naive Search on normal text is practically $O(N)$! The overhead of building complex memory tables (like KMP or Rabin-Karp) is often slower for short patterns!

3. How do modern programming languages actually implement `string.find()`?
   Answer: They do not use pure Naive, nor do they use KMP. Modern languages (like Python, Rust, and glibc C) use the "Two-Way String Matching" algorithm or "Boyer-Moore-Horspool". Boyer-Moore looks at the LAST character of the pattern first. If it mismatches, it can skip the window forward by the ENTIRE LENGTH of the pattern instantly, achieving Sub-Linear $O(N/M)$ speed in practice!
"""

if __name__ == "__main__":
    demonstrate_naive_match()
    print("\n[SUCCESS] Laboratory: Naive String Matching Completed.")
