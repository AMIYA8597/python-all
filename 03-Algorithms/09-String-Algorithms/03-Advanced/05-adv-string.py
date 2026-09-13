"""
# ==============================================================================
# LABORATORY: SUFFIX AUTOMATON (DAWG)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned the Suffix Tree (Ukkonen). It is O(N) time and space, but famously 
# requires ~300 lines of chaotic code to implement the Active Point logic.
#
# In 1985, Blumer et al. mathematically proved the existence of something even 
# more elegant: The Directed Acyclic Word Graph (DAWG), also known as the 
# Suffix Automaton.
#
# It is the mathematically SMALLEST possible Deterministic Finite Automaton (DFA) 
# that recognizes every single suffix (and therefore, every single substring) 
# of a string.
#
# Why is it better than a Suffix Tree?
# - It is built ONLINE (character by character left to right) in strict O(N) time.
# - The construction code is only ~30 lines long!
# - It uses significantly less memory overhead than a Suffix Tree.
# - It can instantly solve: Longest Common Substring, Number of Distinct Substrings, 
#   K-th Lexicographical Substring, and Pattern Matching.
#
# The Core Concept:
# Instead of storing characters, nodes represent "Endpos Equivalence Classes". 
# If two substrings ALWAYS appear in the exact same mathematical locations 
# in the text (e.g., they end at the exact same indices), they are collapsed 
# into the EXACT SAME NODE!
#
# Every node has:
# 1. `len`: The maximum length of a substring in this equivalence class.
# 2. `link`: The Suffix Link, pointing to the node representing the longest 
#    suffix of this class that is in a DIFFERENT equivalence class.
# 3. `transitions`: A map of character edges to other states.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Endpos Equivalence Classes.
# - Implement the O(N) online construction algorithm.
# - Count Distinct Substrings instantly.
#
# ==============================================================================
"""

from typing import Dict, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SUFFIX AUTOMATON ENGINE (O(N))
# ==============================================================================
class SuffixAutomatonNode:
    def __init__(self, length: int):
        # `length` is the MAXIMUM length of a string belonging to this state
        self.length = length
        
        # `link` points to the state representing the longest suffix of this 
        # state's strings that appears in MORE places in the original text.
        self.link = -1
        
        # Standard DFA transitions
        self.transitions: Dict[str, int] = {}


class SuffixAutomaton:
    def __init__(self, s: str):
        # We pre-allocate enough memory. A Suffix Automaton has at most 2N-1 states!
        n = len(s)
        self.states = [SuffixAutomatonNode(0) for _ in range(max(2, 2 * n))]
        
        # State 0 is the Root (empty string)
        self.size = 1
        
        # The state corresponding to the entire string we have processed so far
        self.last = 0
        
        for char in s:
            self._extend(char)
            
    def _extend(self, char: str):
        """
        Adds a single character to the Automaton in amortized O(1) time.
        """
        # 1. CREATE THE NEW STATE
        # This state represents the entire string read so far + the new char.
        # Its maximum length is exactly (last.length + 1).
        cur = self.size
        self.size += 1
        self.states[cur].length = self.states[self.last].length + 1
        
        # 2. UPDATE TRANSITIONS FROM PREVIOUS SUFFIXES
        # We must add an edge for `char` to all suffixes of the PREVIOUS string!
        # We walk back up the suffix links.
        p = self.last
        while p != -1 and char not in self.states[p].transitions:
            self.states[p].transitions[char] = cur
            p = self.states[p].link
            
        # CASE A: We reached the absolute Root. This character has NEVER been 
        # seen before! The suffix link for our new state is just the Root.
        if p == -1:
            self.states[cur].link = 0
            
        # CASE B: We found an ancestor `p` that ALREADY has a transition for `char`!
        else:
            q = self.states[p].transitions[char]
            
            # Subcase B1: The node `q` is a mathematically continuous extension of `p`.
            # We can simply set our suffix link to `q`!
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
                
            # Subcase B2: THE SPLIT!
            # The node `q` contains multiple strings of varying lengths, and we 
            # only want to link to the shorter suffixes.
            # We must literally SPLIT the state `q` into two distinct states!
            else:
                # Create a `clone` state. 
                # It copies the transitions and link from `q`, but its `length` 
                # is strictly bound to `p.length + 1`.
                clone = self.size
                self.size += 1
                
                self.states[clone].length = self.states[p].length + 1
                
                # Shallow copy the transitions and link
                self.states[clone].transitions = self.states[q].transitions.copy()
                self.states[clone].link = self.states[q].link
                
                # Redirect the original state and our new state to point to the clone!
                while p != -1 and self.states[p].transitions.get(char) == q:
                    self.states[p].transitions[char] = clone
                    p = self.states[p].link
                    
                self.states[q].link = clone
                self.states[cur].link = clone
                
        # Finally, update the `last` pointer for the next character!
        self.last = cur


# ==============================================================================
# 4. APPLICATIONS OF THE AUTOMATON
# ==============================================================================
def count_distinct_substrings(automaton: SuffixAutomaton) -> int:
    """
    Counts total distinct substrings in strict O(N) time!
    Every state in the DAWG mathematically represents exactly:
    (state.length - link.length) distinct substrings!
    """
    total = 0
    for i in range(1, automaton.size):
        # We skip State 0 (Root) because it represents the empty string.
        state = automaton.states[i]
        link_state = automaton.states[state.link]
        
        total += (state.length - link_state.length)
        
    return total

def is_substring(automaton: SuffixAutomaton, pattern: str) -> bool:
    """
    O(M) exact pattern matching! Identical to a Suffix Tree.
    Just start at the Root and follow the DFA transitions!
    """
    current_state = 0
    
    for char in pattern:
        if char not in automaton.states[current_state].transitions:
            return False
        current_state = automaton.states[current_state].transitions[char]
        
    return True


def demonstrate_dawg():
    section_header("Algorithm: Suffix Automaton (DAWG)")
    
    text = "abcbc"
    print(f"Building Suffix Automaton for '{text}'...")
    
    dawg = SuffixAutomaton(text)
    
    print(f"Total States allocated: {dawg.size} (Max Bound: {2 * len(text) - 1})")
    
    section_header("O(1) Math: Distinct Substrings")
    
    distinct_count = count_distinct_substrings(dawg)
    print(f"Total Unique Substrings in '{text}': {distinct_count}")
    
    section_header("O(M) DFA Pattern Matching")
    
    patterns = ["bc", "bcb", "cbc", "a", "abcd", "bca"]
    
    for pat in patterns:
        found = is_substring(dawg, pat)
        print(f"Searching for '{pat:4}' -> {'FOUND!' if found else 'Not Found'}")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does the `clone` state do in Subcase B2?
   Answer: Imagine we are adding 'C' to "ABABC". 
   State $p$ represents the suffix "AB". It has a transition on 'C' to State $q$.
   But State $q$ ALREADY represents the massive string "ABCABC". 
   If we set our new suffix link to $q$, we are mathematically claiming that "ABC" is equivalent to "ABCABC"! This is false. They appear in different places in the string!
   We MUST physically split State $q$ into two pieces: 
   1. The `clone` (representing the shorter string "ABC").
   2. The original $q$ (representing the longer string "ABCABC").
   By separating them, the Automaton preserves mathematical purity.

2. Why is the maximum number of states $2N - 1$?
   Answer: 
   - Every time we read a character, we create EXACTLY 1 new state (`cur`). For a string of length $N$, that is $N$ states. 
   - The only other time a state is created is during Subcase B2, when we create a `clone` state. 
   Mathematical proofs show that the `clone` condition can trigger at most $N - 1$ times across the entire lifespan of the string. 
   Therefore, $N + (N - 1) = 2N - 1$. The space complexity is rigidly bounded to $O(N)$!

3. Which is practically better: Suffix Tree or Suffix Automaton?
   Answer: Suffix Automaton. The mathematical state-machine implementation is roughly 30 lines of code, whereas Ukkonen's Suffix Tree requires hundreds of lines of complex edge-splitting logic. The Suffix Automaton is the preferred "God-Tier" string data structure for competitive programmers because it is easier to memorize, takes $O(N)$ memory, and solves every single string problem a Suffix Tree can solve!
"""

if __name__ == "__main__":
    demonstrate_dawg()
    print("\n[SUCCESS] Laboratory: Suffix Automaton Completed.")
