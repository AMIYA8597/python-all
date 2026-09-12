"""
Module: Aho-Corasick Algorithm

Learning Objectives:
1. Understand the Aho-Corasick automaton and its components (trie, failure links, output links).
2. Learn how to construct the automaton from a set of keywords.
3. Apply the algorithm for efficient multi-pattern string search.

Concept Explanation:
The Aho-Corasick algorithm is a string-searching algorithm that locates elements of a finite set of strings (the "dictionary") within an input text. It constructs a finite-state machine (resembling a trie with additional links) in O(m) time, where m is the total length of all dictionary words. The search then processes the text in O(n + z) time, where n is the length of the text and z is the number of matches.
"""

from collections import deque
import time
from typing import List, Dict, Set, Tuple

class AhoNode:
    def __init__(self):
        self.children: Dict[str, 'AhoNode'] = {}
        self.fail: 'AhoNode' = None
        self.output: List[str] = []

class AhoCorasick:
    def __init__(self, words: List[str]):
        self.root = AhoNode()
        self._build_trie(words)
        self._build_automaton()

    def _build_trie(self, words: List[str]) -> None:
        for word in words:
            current = self.root
            for char in word:
                if char not in current.children:
                    current.children[char] = AhoNode()
                current = current.children[char]
            current.output.append(word)

    def _build_automaton(self) -> None:
        queue = deque()
        # Initialize fail states for root's children to root
        for char, node in self.root.children.items():
            node.fail = self.root
            queue.append(node)

        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                queue.append(child)
                fail_node = current.fail
                
                while fail_node and char not in fail_node.children:
                    if fail_node == self.root:
                        break
                    fail_node = fail_node.fail
                
                if fail_node and char in fail_node.children:
                    child.fail = fail_node.children[char]
                else:
                    child.fail = self.root
                
                if child.fail:
                    child.output.extend(child.fail.output)

    def search(self, text: str) -> Dict[str, List[int]]:
        """
        Searches the text and returns a dictionary mapping found words to their start indices.
        """
        results = {}
        current = self.root
        
        for i, char in enumerate(text):
            while current and char not in current.children:
                if current == self.root:
                    break
                current = current.fail
            
            if current and char in current.children:
                current = current.children[char]
            else:
                current = self.root
                
            for word in current.output:
                start_idx = i - len(word) + 1
                if word not in results:
                    results[word] = []
                results[word].append(start_idx)
                
        return results

def performance_analysis() -> None:
    print("\n--- Performance Analysis ---")
    words = ["he", "she", "his", "hers"] * 100
    text = "ushers" * 1000
    
    start = time.perf_counter()
    ac = AhoCorasick(words)
    build_time = time.perf_counter() - start
    
    start = time.perf_counter()
    ac.search(text)
    search_time = time.perf_counter() - start
    
    print(f"Build Time: {build_time:.4f}s")
    print(f"Search Time (Length {len(text)}): {search_time:.4f}s")

def edge_cases() -> None:
    print("\n--- Edge Cases ---")
    ac = AhoCorasick([])
    print("Empty dictionary search 'text':", ac.search("text"))
    ac2 = AhoCorasick(["test"])
    print("Empty text search:", ac2.search(""))
    
def interview_challenge() -> None:
    """
    Challenge: Censor offensive words in a text using Aho-Corasick.
    """
    print("\n--- Interview Challenge ---")
    bad_words = ["bad", "ugly", "nasty"]
    text = "This is a bad and ugly world, but not nasty."
    ac = AhoCorasick(bad_words)
    matches = ac.search(text)
    
    # Simple replace logic
    text_list = list(text)
    for word, indices in matches.items():
        for idx in indices:
            for i in range(idx, idx + len(word)):
                text_list[i] = '*'
                
    censored = "".join(text_list)
    print("Original:", text)
    print("Censored:", censored)

def run_tests() -> None:
    ac = AhoCorasick(["he", "she", "his", "hers"])
    res = ac.search("ushers")
    assert res == {'he': [2], 'she': [1], 'hers': [2]}
    print("All tests passed!")

if __name__ == "__main__":
    print("Aho-Corasick Algorithm\n" + "="*22)
    run_tests()
    edge_cases()
    interview_challenge()
    performance_analysis()
