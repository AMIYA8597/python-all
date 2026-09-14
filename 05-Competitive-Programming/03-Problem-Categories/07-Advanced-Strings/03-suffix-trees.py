"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (SUFFIX ARRAYS & LCP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given a massive 100,000 character string (e.g., DNA sequence).
# You need to find the "Longest Repeated Substring" in the sequence.
#
# If you try to extract every possible substring and compare them, there are 
# O(N^2) substrings, and comparing them takes O(N), resulting in an O(N^3) 
# brute force catastrophe.
#
# Suffix Trees solve this in exactly O(N) time. However, building a Suffix Tree 
# from scratch (Ukkonen's Algorithm) is notoriously difficult and almost 
# impossible to debug during a high-pressure 45-minute coding interview.
#
# The Competitive Programming solution is the "Suffix Array" paired with the 
# "LCP Array" (Longest Common Prefix). It provides the exact same mathematical 
# power as a Suffix Tree, but can be coded flawlessly in 20 lines of Python.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a Suffix Array.
# - Understand Kasai's Algorithm for building the LCP Array in O(N) time.
# - Solve the Longest Repeated Substring problem in O(N).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SUFFIX ARRAY & KASAI'S LCP ALGORITHM
# ==============================================================================
def build_suffix_array_naive(s: str) -> list[int]:
    """
    Builds the Suffix Array.
    A Suffix Array is simply a mathematically sorted list of the STARTING INDICES 
    of all possible suffixes of a string.
    
    NOTE: This naive Python sort takes O(N^2 log N). 
    In strict CP, this is optimized to O(N log N) using a Rank Matrix, 
    but for Python, the built-in TimSort is heavily optimized in C and often passes!
    """
    suffixes = []
    n = len(s)
    
    for i in range(n):
        # We store a tuple: (The actual suffix string, The original starting index)
        suffixes.append((s[i:], i))
        
    # Sort them lexicographically (alphabetically)
    suffixes.sort()
    
    # Return just the indices!
    return [suffix[1] for suffix in suffixes]

def build_lcp_array(s: str, suffix_array: list[int]) -> list[int]:
    """
    Kasai's Algorithm: Builds the Longest Common Prefix (LCP) Array in O(N) time!
    The LCP array stores the length of the matching prefix between 
    suffix_array[i] and suffix_array[i-1].
    """
    n = len(s)
    lcp = [0] * n
    
    # Inverse Suffix Array
    # rank[i] tells us: "Where does the suffix starting at index `i` appear 
    # in the sorted Suffix Array?"
    rank = [0] * n
    for i in range(n):
        rank[suffix_array[i]] = i
        
    h = 0
    # Process suffixes in their ORIGINAL order (longest to shortest)
    for i in range(n):
        # If this is the absolute first suffix in the sorted array, 
        # it has no predecessor to compare against. LCP is 0.
        if rank[i] > 0:
            
            # Find the predecessor suffix in the sorted array
            j = suffix_array[rank[i] - 1]
            
            # Character matching loop!
            # We match characters one by one.
            while (i + h < n) and (j + h < n) and s[i + h] == s[j + h]:
                h += 1
                
            # Store the LCP length
            lcp[rank[i]] = h
            
            # KASAI'S MATHEMATICAL MAGIC:
            # If the current suffix shared `h` characters with its predecessor, 
            # the next suffix (which is just 1 character shorter) is mathematically 
            # guaranteed to share at least `h - 1` characters with its predecessor!
            # We do NOT reset `h` to 0! We just decrement it by 1!
            if h > 0:
                h -= 1
                
    return lcp

def longest_repeated_substring(s: str) -> str:
    """
    Finds the longest repeated substring in O(N) time using Suffix Array + LCP.
    """
    sa = build_suffix_array_naive(s)
    lcp = build_lcp_array(s, sa)
    
    # The longest repeated substring mathematically MUST be the maximum value 
    # in the LCP array!
    max_lcp = 0
    max_idx = 0
    
    for i in range(len(lcp)):
        if lcp[i] > max_lcp:
            max_lcp = lcp[i]
            max_idx = i
            
    if max_lcp == 0:
        return ""
        
    # The starting index of the winning suffix
    start_index = sa[max_idx]
    
    return s[start_index : start_index + max_lcp]

def demonstrate_suffix_array():
    section_header("Suffix Array & Longest Repeated Substring")
    
    text = "banana"
    print(f"String: {text}")
    
    sa = build_suffix_array_naive(text)
    lcp = build_lcp_array(text, sa)
    
    print("\nSorted Suffix Array Analysis:")
    print(" i | LCP | Suffix")
    print("-" * 25)
    for i in range(len(sa)):
        idx = sa[i]
        suffix = text[idx:]
        lcp_val = lcp[i]
        print(f"{i:2d} | {lcp_val:3d} | {suffix}")
        
    ans = longest_repeated_substring(text)
    print(f"\nLongest Repeated Substring: '{ans}'")
    print(f"Notice that LCP naturally finds 'ana' (length {len(ans)}) because ")
    print("sorting mathematically forces identical prefixes to sit right next to each other!")


def run_all_labs():
    demonstrate_suffix_array()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the definition of a Suffix Array, and why does sorting suffixes alphabetically instantly solve the Longest Repeated Substring problem?
   Answer: A Suffix Array is an array containing the starting indices of all suffixes of a string, sorted in strict alphabetical (lexicographical) order. If a string contains a repeating substring (like "ana" inside "banana"), those repeating occurrences will generate multiple suffixes that share the exact same starting prefix ("ana", "anana"). Because the array is alphabetically sorted, these similar suffixes are mathematically forced to sit directly adjacent to one another in the Suffix Array! Therefore, the Longest Repeated Substring will ALWAYS be the Longest Common Prefix (LCP) between two adjacent elements in the array. You never need to check non-adjacent elements!

2. Explain the fundamental mathematical trick behind Kasai's Algorithm that allows the LCP array to be built in $O(N)$ time instead of $O(N^2)$.
   Answer: A naive algorithm compares every adjacent suffix character by character, taking $O(N)$ time per pair, resulting in $O(N^2)$ total time. Kasai discovered a brilliant property: If you process the suffixes in their *original length order* (from longest to shortest), you can mathematically recycle your work. Suppose the suffix starting at index $i$ ("banana") shares a prefix of length $3$ ("ana") with its sorted neighbor. When you process the next suffix at index $i+1$ ("anana"), Kasai proved that it is guaranteed to share a prefix of at least length $3-1 = 2$ with *its* sorted neighbor! By executing `h -= 1` instead of `h = 0`, Kasai prevents the algorithm from ever rescanning those 2 characters, guaranteeing the inner `while` loop advances at most $O(N)$ times across the entire execution of the program!

3. Why is the Suffix Array overwhelmingly preferred over the Suffix Tree in modern Competitive Programming?
   Answer: Suffix Trees are visually beautiful but architecturally nightmarish. Implementing Ukkonen's $O(N)$ Suffix Tree requires complex active points, implicit states, suffix links, and complex memory management. A single bug will destroy the tree, making it nearly impossible to write under time pressure. The Suffix Array + LCP combo provides mathematically identical querying power (you can simulate a Suffix Tree traversal using LCP intervals), but requires only ~20 lines of flawless, easy-to-memorize code. Furthermore, Suffix Arrays allocate a single contiguous block of memory (an array of integers), drastically outperforming the CPU cache-misses generated by the massive linked-node structure of a Suffix Tree.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Suffix Arrays & LCP Completed.")
