"""
Longest Palindromic Substring - Manacher's Algorithm

Learning Objectives:
1. Understand the problem of finding the longest palindromic substring.
2. Recognize the overlapping subproblem nature of palindromes.
3. Learn how Manacher's algorithm achieves O(N) time complexity by avoiding redundant checks.
4. Understand the string transformation step (inserting special characters) to handle even and odd length palindromes uniformly.

Concept Explanation:
Finding the longest palindromic substring naively takes O(N^3) time. Expanding around center takes O(N^2) time.
Manacher's Algorithm finds the longest palindromic substring in linear time O(N). 
It works by maintaining the center and right boundary of the palindrome that reaches furthest to the right.
It uses previously computed palindrome lengths (exploiting the symmetry of palindromes) to skip redundant 
comparisons when processing new centers.

A crucial trick in Manacher's is transforming the string (e.g., "aba" -> "^#a#b#a#$") so that all palindromes
(both even and odd lengths) can be found using the same logic (centering at characters or the inserted `#`).

Industry Use Cases:
- Text processing and pattern recognition.
- Data compression algorithms.
- Bioinformatics (finding palindromic sequences in DNA).

Common Mistakes:
- Failing to handle boundaries (which is why `^` and `$` are added in the transformed string).
- Not correctly updating the `center` and `right` boundary variables.
- Incorrectly mapping the index from the transformed string back to the original string.
"""

def manacher_basic(s: str) -> str:
    """
    Basic implementation of Manacher's Algorithm.
    """
    if not s:
        return ""

    # Transform string to handle even/odd lengths uniformly
    # "aba" -> "^#a#b#a#$"
    t = "^#" + "#".join(s) + "#$"
    n = len(t)
    p = [0] * n  # p[i] will store the radius of the longest palindrome around center i
    
    center = 0
    right = 0
    
    for i in range(1, n - 1):
        i_mirror = 2 * center - i  # Mirror of i with respect to center
        
        # If i is within the right boundary, we can use the precomputed mirror value
        if right > i:
            p[i] = min(right - i, p[i_mirror])
            
        # Expand palindrome centered at i
        # We don't need bounds checking because of ^ and $
        while t[i + 1 + p[i]] == t[i - 1 - p[i]]:
            p[i] += 1
            
        # If palindrome centered at i expands past right, adjust center and right
        if i + p[i] > right:
            center = i
            right = i + p[i]
            
    # Find the maximum element in p
    max_len = 0
    center_index = 0
    for i in range(1, n - 1):
        if p[i] > max_len:
            max_len = p[i]
            center_index = i
            
    # Extract the longest palindrome from original string
    start = (center_index - 1 - max_len) // 2
    return s[start: start + max_len]


class ManacherAlgorithm:
    """
    Professional implementation of Manacher's algorithm for Longest Palindromic Substring.
    """
    def __init__(self, text: str):
        self.text = text
        self._transformed = self._transform(text)
        self._p = [0] * len(self._transformed)
        self._longest_palindrome = ""
        self._computed = False

    @staticmethod
    def _transform(s: str) -> str:
        """Transforms string to insert separators."""
        if not s:
            return "^$"
        return "^#" + "#".join(s) + "#$"

    def solve(self) -> str:
        """Finds and returns the longest palindromic substring."""
        if self._computed:
            return self._longest_palindrome
            
        if not self.text:
            return ""

        t = self._transformed
        p = self._p
        n = len(t)
        
        center = 0
        right = 0
        max_len = 0
        center_index = 0

        for i in range(1, n - 1):
            mirror = 2 * center - i
            
            if right > i:
                p[i] = min(right - i, p[mirror])
                
            while t[i + (1 + p[i])] == t[i - (1 + p[i])]:
                p[i] += 1
                
            if i + p[i] > right:
                center = i
                right = i + p[i]
                
            if p[i] > max_len:
                max_len = p[i]
                center_index = i

        start = (center_index - 1 - max_len) // 2
        self._longest_palindrome = self.text[start: start + max_len]
        self._computed = True
        
        return self._longest_palindrome

"""
Complexity Analysis:
- Time Complexity: O(N) where N is the length of the string.
  The while loop expands the right boundary, and the right boundary can only increase up to 2*N.
  Thus, the total number of character comparisons is bounded by O(N).
- Space Complexity: O(N) to store the transformed string and the lengths array `P`.

Interview Challenge:
Question: How does the dummy character insertion (`#`) fix the problem of even length palindromes?
Answer: Even length palindromes don't have a single character center. By inserting `#` between all characters, every palindrome (even or odd length in the original string) becomes an odd-length palindrome in the transformed string, perfectly centered on a character (which might be a `#` for even-length palindromes or a real character for odd-length).
"""

if __name__ == "__main__":
    print("Testing Manacher's Algorithm...")
    
    test_str = "babad"
    result_basic = manacher_basic(test_str)
    assert result_basic in ["bab", "aba"], f"Failed for {test_str}: {result_basic}"
    
    test_str2 = "cbbd"
    solver = ManacherAlgorithm(test_str2)
    assert solver.solve() == "bb", f"Failed for {test_str2}: {solver.solve()}"
    
    print("All tests passed successfully.")
