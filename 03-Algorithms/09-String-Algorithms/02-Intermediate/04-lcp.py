"""
# ==============================================================================
# LABORATORY: LCP ARRAY & KASAI'S ALGORITHM
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the previous lab, you built the Suffix Array. It perfectly sorts every 
# suffix in alphabetical order. 
# 
# But the Suffix Array alone is just a search tool. To unlock the true 
# mathematical power of Strings, you need its companion: The LCP Array.
#
# LCP = Longest Common Prefix.
# The LCP Array stores the exact number of matching starting characters between 
# ADJACENT suffixes in the sorted Suffix Array!
#
# Why is this so insanely powerful?
#
# 1. The Longest Repeated Substring Problem:
#    How do you find the longest substring that appears at least twice in a text?
#    Answer: Just find the MAX VALUE in the LCP array! It takes O(N) time!
#
# 2. Number of Unique Substrings:
#    How many mathematically unique substrings exist in a string?
#    Answer: (N * (N+1) / 2) - sum(LCP Array). A 1-line $O(N)$ math formula!
#
# 3. Longest Common Substring (Between Two Different Strings):
#    Instead of $O(N \times M)$ Dynamic Programming, you concatenate String A 
#    and String B. Build the SA and LCP. Find the max LCP between a suffix from 
#    A and a suffix from B! Takes $O((N+M) \log^2 (N+M))$.
#
# Building the LCP naively by checking every character takes O(N^2) time.
# In 2001, Toru Kasai invented an algorithm that builds the LCP in strict 
# linear O(N) time, using a brilliant "Rank Array" optimization!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the structure of the LCP array.
# - Implement Kasai's O(N) LCP Construction.
# - Solve the Longest Repeated Substring using the LCP.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# --- Helper: The Suffix Array generator from the previous lab ---
def get_rank_pair(i: int, k: int, rank: List[int], n: int):
    return (rank[i], rank[i + k] if i + k < n else -1)

def build_suffix_array(s: str) -> List[int]:
    n = len(s)
    suffix_array = list(range(n))
    rank = [ord(c) for c in s]
    k = 1
    while k < n:
        suffix_array.sort(key=lambda i: get_rank_pair(i, k, rank, n))
        new_rank = [0] * n
        current_rank = 0
        new_rank[suffix_array[0]] = 0
        for i in range(1, n):
            if get_rank_pair(suffix_array[i-1], k, rank, n) == get_rank_pair(suffix_array[i], k, rank, n):
                new_rank[suffix_array[i]] = current_rank
            else:
                current_rank += 1
                new_rank[suffix_array[i]] = current_rank
        rank = new_rank
        k *= 2
    return suffix_array
# -----------------------------------------------------------------


# ==============================================================================
# 3. KASAI'S ALGORITHM (O(N) LCP ARRAY)
# ==============================================================================
def build_lcp_array(s: str, suffix_array: List[int]) -> List[int]:
    """
    Constructs the Longest Common Prefix (LCP) Array in O(N) time.
    lcp[i] = length of the longest common prefix between suffix_array[i-1] and suffix_array[i].
    """
    n = len(s)
    
    # 1. THE RANK ARRAY (Inverse Suffix Array)
    # The suffix array tells us: "What is the suffix at alphabetical rank i?"
    # The Rank Array tells us: "What is the alphabetical rank of the suffix starting at index i?"
    # We can build this from the Suffix Array in O(N) time.
    rank = [0] * n
    for rank_idx, suffix_start_idx in enumerate(suffix_array):
        rank[suffix_start_idx] = rank_idx
        
    lcp = [0] * n
    
    # `h` keeps track of the length of the currently verified LCP.
    h = 0
    
    # 2. THE KASAI LOOP
    # Instead of iterating through the SORTED suffixes, Kasai iterates through 
    # the original unsorted suffixes starting from index 0, 1, 2...
    for i in range(n):
        # We find the alphabetical rank of the suffix starting at `i`
        current_rank = rank[i]
        
        # If this suffix is the very first one alphabetically (rank 0), 
        # it has no predecessor to compare against!
        if current_rank > 0:
            
            # Find the starting index of the suffix that is directly BEFORE us 
            # in alphabetical order!
            previous_suffix_start = suffix_array[current_rank - 1]
            
            # Kasai's Magic Optimization:
            # We don't need to check characters from scratch! 
            # We KNOW from the previous loop iteration that at least `h` characters 
            # are mathematically guaranteed to match!
            # We just resume naive checking from `h` onwards!
            while (i + h < n) and (previous_suffix_start + h < n) and (s[i + h] == s[previous_suffix_start + h]):
                h += 1
                
            lcp[current_rank] = h
            
            # When we move to the next suffix in the original string (`i + 1`), 
            # we just dropped exactly 1 character from the front. 
            # Therefore, the guaranteed common prefix `h` must shrink by EXACTLY 1!
            if h > 0:
                h -= 1
                
    return lcp


# ==============================================================================
# 4. APPLICATIONS OF THE LCP ARRAY
# ==============================================================================
def find_longest_repeated_substring(s: str) -> str:
    """
    Uses the Suffix Array and LCP Array to find the longest repeated substring 
    in strict O(N log^2 N) time.
    """
    s_dollar = s + "$"
    sa = build_suffix_array(s_dollar)
    lcp = build_lcp_array(s_dollar, sa)
    
    max_lcp = 0
    max_index_in_sa = 0
    
    for i in range(1, len(lcp)):
        if lcp[i] > max_lcp:
            max_lcp = lcp[i]
            max_index_in_sa = i
            
    if max_lcp == 0:
        return ""
        
    start_index = sa[max_index_in_sa]
    return s_dollar[start_index : start_index + max_lcp]


def count_unique_substrings(s: str) -> int:
    """
    Math formula: Total Substrings - Sum(LCP)
    """
    s_dollar = s + "$"
    sa = build_suffix_array(s_dollar)
    lcp = build_lcp_array(s_dollar, sa)
    
    n = len(s)
    total_substrings = (n * (n + 1)) // 2
    
    # We sum the LCP, ignoring the dummy '$' interactions
    redundant_substrings = sum(lcp)
    
    return total_substrings - redundant_substrings


def demonstrate_lcp():
    section_header("Algorithm: LCP Array & Kasai's Theorem")
    
    text = "banana"
    text_dollar = text + "$"
    print(f"String: '{text_dollar}'")
    
    sa = build_suffix_array(text_dollar)
    lcp = build_lcp_array(text_dollar, sa)
    
    print("\nSuffix Array with LCP values:")
    print("Rank | SA | LCP | Suffix")
    print("---------------------------------")
    for i in range(len(sa)):
        idx = sa[i]
        suffix = text_dollar[idx:]
        print(f" {i:2}  | {idx:2} | {lcp[i]:3} | '{suffix}'")
        
    print("\nLCP Interpretation:")
    print("Look at Rank 3 ('ana$') and Rank 4 ('anana$').")
    print("They share the prefix 'ana' (Length 3). Thus, LCP[4] = 3!")
    
    section_header("LCP Array Applications")
    
    lrs = find_longest_repeated_substring(text)
    print(f"Longest Repeated Substring in '{text}': '{lrs}' (Length: {len(lrs)})")
    
    unique_count = count_unique_substrings(text)
    print(f"Total Unique Substrings in '{text}': {unique_count}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Kasai's algorithm guarantee $O(N)$ runtime?
   Answer: Look at the `h` variable. In the inner `while` loop, `h` increases. At the end of the outer loop, `h -= 1`. Because `h` starts at 0, drops by exactly 1 at every step, and can mathematically never exceed $N$ (the length of the string), the inner `while` loop (which strictly increments `h`) can only execute a maximum of $2N$ times across the ENTIRE lifespan of the algorithm. This perfectly identical logical bound guarantees $O(N)$.

2. Why is the Longest Repeated Substring always adjacent in the Suffix Array?
   Answer: The Suffix Array sorts strings alphabetically. If two suffixes share a massive prefix (like "BANANAS" and "BANANARAMA"), their alphabetical ranking forces them to be seated directly next to each other in the array! It is mathematically impossible for a longer common prefix to exist between two suffixes that are separated by a third suffix (because the third suffix would have been sorted between them based on that exact prefix). Therefore, a single linear $O(N)$ scan of adjacent cells (the LCP Array) is 100% guaranteed to find the global maximum.

3. How does the Unique Substrings formula work?
   Answer: Every single substring of a word is fundamentally just a "prefix of some suffix." The total number of prefixes across all suffixes is $(N \\times (N+1)) / 2$. However, when suffixes are sorted alphabetically, any prefix they share with their predecessor is a DUPLICATE substring we've already counted! Since the LCP array explicitly stores the exact number of shared prefixes between adjacent sorted suffixes, summing the entire LCP array gives the exact number of duplicates. Subtract duplicates from the total, and you get the mathematically pure Unique count!
"""

if __name__ == "__main__":
    demonstrate_lcp()
    print("\n[SUCCESS] Laboratory: LCP Array & Kasai's Algorithm Completed.")
