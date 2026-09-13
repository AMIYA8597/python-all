"""
## A. Concept Name
Suffix Trees

## B. Core Concept
A Suffix Tree is a compressed trie containing all the suffixes of the given text as their keys and positions in the text as their values. It is a fundamental data structure in string matching algorithms.

## C. Use Cases
- Fast exact string matching.
- Finding the longest repeated substring.
- Finding the longest common substring of multiple strings.
- Full-text search applications.

## D. AI/ML Applications
- Used in bioinformatics for DNA sequence analysis (e.g., searching for genome motifs).
- Natural Language Processing (NLP) for rapid pattern matching and substring analysis.
- Feature extraction in sequence-based machine learning models.

## E. Complexity
- Time Complexity: O(N) to build using Ukkonen's algorithm (O(N^2) for the naive approach shown here). Pattern matching takes O(M) where M is the length of the pattern.
- Space Complexity: O(N) since there are at most 2N nodes in a compressed suffix tree.

## F. Advanced Techniques
Suffix links and active points are crucial for achieving linear time construction in Ukkonen's algorithm, allowing the tree to be built online in O(N) time.

## X. Project Connection
Integrates with advanced NLP and genomics pipelines in our AI projects where extremely fast substring search and pattern recognition are critical before passing tokenized data to deep learning models.
"""

class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.indexes = []

class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.root = SuffixTreeNode()
        self.build_naive()

    def build_naive(self):
        """
        A naive O(N^2) construction.
        For production, use Ukkonen's algorithm for O(N) time.
        """
        for i in range(len(self.text)):
            current = self.root
            suffix = self.text[i:]
            for char in suffix:
                if char not in current.children:
                    current.children[char] = SuffixTreeNode()
                current = current.children[char]
                current.indexes.append(i)

    def search(self, pattern):
        """
        Searches for a pattern in the suffix tree.
        Returns a list of starting indices where the pattern occurs.
        """
        current = self.root
        for char in pattern:
            if char not in current.children:
                return []
            current = current.children[char]
        return current.indexes

def main():
    text = "banana$"
    print(f"Building suffix tree for text: '{text}'")
    tree = SuffixTree(text)
    
    patterns = ["nan", "ana", "a", "b", "xyz"]
    for pattern in patterns:
        indexes = tree.search(pattern)
        print(f"Pattern '{pattern}' found at indices: {indexes}")

if __name__ == "__main__":
    main()
