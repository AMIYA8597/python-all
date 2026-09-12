"""
## A. Concept Name
Aho-Corasick Algorithm

## B. Core Idea
Aho-Corasick is a string-searching algorithm that locates elements of a finite set of strings (the "dictionary") within an input text simultaneously. It constructs a finite state machine (a trie with failure links) in linear time.

## C. Why It Matters
When you need to find multiple patterns in a text, naive searching takes O(N * M) time where N is text length and M is total pattern length. Aho-Corasick achieves this in O(N + M + Z) time, where Z is the number of matches. This is crucial for applications like intrusion detection systems, antivirus software, and natural language processing.

## D. Real-World Analogy
Imagine you are looking for several specific words in a book. Instead of scanning the book from beginning to end for the first word, and then scanning it again for the second word, you build a special checklist. You read the book exactly once, word by word, and your checklist instantly tells you if you've just completed reading any of your target words.

## E. Visual Representation
Trie structure with failure links:
       (root)
       /    \
      a      b
     / \    ...
    b   c
If matching 'ab' fails at 'b', the failure link points to the longest proper suffix that is also a prefix in the trie.

## F. Prerequisites
- Trie (Prefix Tree) data structure
- Breadth-First Search (BFS)
- State machines concepts

## G. Common Pitfalls
- Forgetting to add matches from the failure link state to the current state (dictionary links / output links).
- Implementing BFS incorrectly when building failure links.

## H. Step-by-Step Implementation
1. Build a Trie from the given dictionary of patterns.
2. Build failure links using BFS.
3. Traverse the text using the built state machine and collect matches.

## I. Time & Space Complexity
- Time Complexity: O(M + N + Z) where M is the total length of all patterns, N is the length of the text, and Z is the number of matches.
- Space Complexity: O(M * K) where M is the total length of patterns and K is the alphabet size.

## J. Testing & Edge Cases
- Overlapping patterns
- Patterns that are substrings of other patterns
- Empty text or empty pattern list

## K. Practice Problems
- Find all occurrences of dictionary words in a string
- Virus signature matching

## L. Optimization Tricks
- Use a 1D array instead of objects for Trie nodes to improve cache locality.
- Dictionary (output) links to skip states that don't have pattern matches but their failure links do.

## M. Standard Library / Existing Solutions
Python's `re` module for regex, or external libraries like `pyahocorasick`.

## N. Common Variations
- Aho-Corasick automaton with transition tables for faster execution at the cost of space.

## O. Interactive Exploration
Try tracing the algorithm manually with patterns "he", "she", "his", "hers" and text "ushers".

## P. Code Structure
The implementation consists of a `TrieNode` class, and an `AhoCorasick` class that encapsulates the logic for adding patterns, building the automaton, and searching text.

## Q. Debugging Tips
Print the nodes and their failure links to verify the BFS phase. Ensure output links (or match lists) are correctly merged.

## R. Security Implications
Can be used for fast filtering of malicious keywords or payloads in network streams.

## S. Maintenance & Readability
Keep the node structure clean. Separate the trie building and failure link building phases logically.

## T. Performance Benchmarks
Compare Aho-Corasick with a naive multiple pattern search for large texts and many patterns to see the efficiency gains.

## U. Further Reading
- Wikipedia: Aho-Corasick algorithm
- Original paper by Alfred V. Aho and Margaret J. Corasick (1975)

## V. Community Wisdom
Aho-Corasick is often overkill for just a few small patterns, where simple search or standard regex might suffice. It shines when the dictionary is large.

## W. Future Trends
Integration with hardware acceleration (FPGA/GPU) for high-speed network packet inspection.

## X. Project Connection
Can be used in a fast text-processing pipeline, such as a log analyzer or a code scanner.
"""

from collections import deque
from typing import List, Dict, Tuple

class TrieNode:
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.fail: 'TrieNode' = None
        self.output: List[str] = []

class AhoCorasick:
    def __init__(self):
        self.root = TrieNode()
        
    def add_pattern(self, pattern: str):
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.output.append(pattern)
        
    def build(self):
        queue = deque()
        
        # Initialize failure links for root's children
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
            
        while queue:
            current_node = queue.popleft()
            
            for char, child in current_node.children.items():
                queue.append(child)
                
                # Find failure link for child
                fail_node = current_node.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                    
                if fail_node:
                    child.fail = fail_node.children[char]
                else:
                    child.fail = self.root
                    
                # Merge outputs from the failure link
                if child.fail:
                    child.output.extend(child.fail.output)
                    
    def search(self, text: str) -> List[Tuple[int, str]]:
        result = []
        node = self.root
        
        for i, char in enumerate(text):
            while node and char not in node.children:
                node = node.fail
                
            if node:
                node = node.children[char]
            else:
                node = self.root
                
            for pattern in node.output:
                # i is the end index of the matched pattern
                start_index = i - len(pattern) + 1
                result.append((start_index, pattern))
                
        return result

if __name__ == "__main__":
    # Example usage demonstrating Aho-Corasick matching
    ac = AhoCorasick()
    patterns = ["he", "she", "his", "hers"]
    for p in patterns:
        ac.add_pattern(p)
    ac.build()
    
    text = "ushers"
    print(f"Searching in '{text}' for patterns: {patterns}")
    matches = ac.search(text)
    for start, pattern in matches:
        print(f"Match found: '{pattern}' at index {start}")
