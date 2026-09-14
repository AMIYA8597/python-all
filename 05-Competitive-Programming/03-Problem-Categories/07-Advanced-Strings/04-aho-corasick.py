"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (AHO-CORASICK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are writing an antivirus scanner. You have a dictionary of 10,000 known 
# virus signatures (the Patterns). You are scanning a 1GB file (the Text).
#
# If you use the KMP algorithm, it searches for ONE pattern in O(N). 
# But you have 10,000 patterns! Running KMP 10,000 times will take O(10,000 * N) 
# time, which is too slow.
#
# The Aho-Corasick Algorithm (invented at Bell Labs in 1975, exactly what `fgrep` 
# uses under the hood) mathematically combines a Trie with KMP. 
# It builds a Trie of all 10,000 patterns, and then uses BFS to create KMP-style 
# "Failure Links" between the branches of the Trie!
#
# It scans the 1GB file exactly ONCE. It finds EVERY occurrence of EVERY virus 
# signature simultaneously in strict O(N + M + Z) time!
# (N = text length, M = total pattern length, Z = number of matches).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how a Trie merges multiple patterns.
# - Understand the architecture of Failure Links (The KMP crossover).
# - Implement the Aho-Corasick Automaton.
#
# ==============================================================================
"""

from collections import deque

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. AHO-CORASICK AUTOMATON
# ==============================================================================
class AhoCorasickNode:
    def __init__(self):
        self.children = {}
        # The KMP Failure Link. If we mismatch here, where do we jump?
        self.fail = None
        # Does this specific node mark the end of any dictionary words?
        self.output = []

class AhoCorasick:
    def __init__(self):
        self.root = AhoCorasickNode()

    def add_pattern(self, pattern: str) -> None:
        """Standard Trie Insertion"""
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = AhoCorasickNode()
            node = node.children[char]
        # Mark the end of the word
        node.output.append(pattern)

    def build_failure_links(self) -> None:
        """
        Builds the Failure Links using BFS.
        This is the absolute heart of Aho-Corasick! It answers: 
        "If I fail at 'SHE', but I know 'HE' is a valid prefix in another branch, 
        how do I instantly jump to 'HE'?"
        """
        queue = deque()
        
        # 1. The children of the Root fail directly back to the Root!
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
            
        # 2. BFS to set Failure Links for deeper nodes
        while queue:
            current_node = queue.popleft()
            
            for char, child in current_node.children.items():
                queue.append(child)
                
                # To find the Failure Link for `child`, we ask its Parent's Failure Link!
                fallback_node = current_node.fail
                
                # Keep falling back until we find a node that has `char` as a child,
                # OR we hit the absolute bottom (the root).
                while fallback_node is not None and char not in fallback_node.children:
                    fallback_node = fallback_node.fail
                    
                if fallback_node is None:
                    # We fell all the way to the root and found nothing.
                    child.fail = self.root
                else:
                    # We found a valid fallback! Connect the Failure Link!
                    child.fail = fallback_node.children[char]
                    
                    # CRITICAL: Output Link merging!
                    # If the fallback node marks the end of a shorter word, 
                    # our current node ALSO matches that shorter word!
                    # Example: Matching 'SHE' implicitly also matches 'HE'.
                    child.output.extend(child.fail.output)

    def search(self, text: str) -> dict[str, list[int]]:
        """
        Scans the text in exactly O(N) time, finding all occurrences of all patterns!
        """
        node = self.root
        results = { }
        
        for i, char in enumerate(text):
            # If the current character doesn't match, follow the Failure Links!
            while node is not None and char not in node.children:
                node = node.fail
                
            if node is None:
                # Completely failed, restart at the root
                node = self.root
            else:
                # Advance down the successful branch
                node = node.children[char]
                
            # Have we matched any dictionary words at this node?
            if node.output:
                for pattern in node.output:
                    if pattern not in results:
                        results[pattern] = []
                    # i is the END index. Start index = i - len(pattern) + 1
                    start_idx = i - len(pattern) + 1
                    results[pattern].append(start_idx)
                    
        return results

def demonstrate_aho_corasick():
    section_header("Aho-Corasick Algorithm")
    
    dictionary = ["he", "she", "his", "hers"]
    text = "ushers"
    
    print(f"Dictionary (Viruses): {dictionary}")
    print(f"Text to scan        : '{text}'")
    
    ac = AhoCorasick()
    for word in dictionary:
        ac.add_pattern(word)
        
    print("\nBuilding Failure Links (BFS)...")
    ac.build_failure_links()
    
    print("Scanning text in exactly O(N) time...")
    matches = ac.search(text)
    
    for word, indices in matches.items():
        print(f"Match found! '{word}' starts at indices: {indices}")
        
    print("\nNotice how matching 'she' mathematically guarantees we also matched 'he'!")


def run_all_labs():
    demonstrate_aho_corasick()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Aho-Corasick mathematically described as a combination of a Trie and KMP?
   Answer: A Trie allows you to check for multiple patterns simultaneously by merging their common prefixes (e.g., "HE" and "HERS" share the same "HE" branch). However, a standard Trie fails catastrophically if a mismatch occurs, forcing the algorithm to completely restart at the root. KMP solves the mismatch problem by using the LPS array to backtrack gracefully without resetting the text pointer. Aho-Corasick takes the KMP LPS backtracking concept and physically embeds it *across the branches* of the Trie as "Failure Links". It creates an indestructible web where a failure in one word's branch instantly teleports you to the valid prefix of an entirely different word's branch!

2. Explain the mechanism behind `child.output.extend(child.fail.output)` in the BFS builder. Why is this critical?
   Answer: This is known as Output Merging or the Dictionary Link. Imagine your dictionary contains "SHE" and "HE". You are scanning the text and perfectly match the node for "SHE". You proudly output "SHE". But wait, the string "SHE" mathematically contains the string "HE" inside of it! If you don't output "HE" right now, the algorithm completely misses it. The Failure Link of the "E" in "SHE" points directly to the "E" in "HE". By extending the output list during the BFS build phase, the "E" in "SHE" absorbs the fact that it is also a valid match for "HE". When the search hits "SHE", it instantly yields both words!

3. In the BFS failure link builder, why do we use a `while` loop (`while fallback_node is not None and char not in fallback_node.children: fallback_node = fallback_node.fail`)?
   Answer: This is identical to the `length = lps[length - 1]` loop in KMP. If a child node fails, we ask its Parent's Failure Link if it has a branch for `char`. If the Parent's fallback *also* fails, we don't just give up and go to the root! We ask the Parent's fallback's fallback! We recursively cascade down the failure links, attempting to salvage smaller and smaller suffix matches. The `while` loop guarantees we find the absolute longest valid suffix that exists anywhere in the entire Trie before we finally surrender and hit `None` (the root).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Strings (Aho-Corasick) Completed.")
