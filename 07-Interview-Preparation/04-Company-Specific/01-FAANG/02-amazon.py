"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (FAANG - AMAZON PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Amazon interviews prioritize Object-Oriented Design (OOD), extreme string 
# parsing, and Data Structures involving Heaps (Priority Queues). 
# You will be asked questions like "Design an Amazon Locker System" or 
# "Find the Top K Most Frequent Words in a massive text file."
#
# A junior engineer uses a standard sorting algorithm to find the Top K items, 
# resulting in O(N log N) time complexity. 
# A senior engineer uses Python's `heapq` module to maintain a strict Min-Heap 
# of exactly size K, discarding the smallest elements dynamically. This reduces 
# time complexity to O(N log K), and space complexity to an absolute O(K). 
# If N is 1 Billion and K is 10, the senior engineer wins the job.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Python's `heapq` module (Min-Heaps and Max-Heaps).
# - Master the "Top K Elements" algorithm in O(N log K) time.
# - Master Object-Oriented string parsing and frequency maps (`collections.Counter`).
#
# ==============================================================================
"""

import heapq
import collections
from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. TOP K FREQUENT WORDS (THE HEAPQ MASTERCLASS)
# ==============================================================================
class WordFreq:
    """
    A custom wrapper class because Amazon often asks for complex sorting rules!
    Rule: Sort by frequency (descending), then alphabetically (ascending).
    Because we are using a Min-Heap of size K, we must mathematically INVERT 
    the comparison logic so that the 'worst' words (lowest freq, or highest alphabet)
    are ejected first!
    """
    def __init__(self, word: str, freq: int):
        self.word = word
        self.freq = freq
        
    def __lt__(self, other):
        # If frequencies are identical, we want to eject the one that comes LATER 
        # in the alphabet (e.g., 'z' should be ejected before 'a').
        if self.freq == other.freq:
            return self.word > other.word
        # Otherwise, eject the one with the LOWER frequency.
        return self.freq < other.freq

def top_k_frequent_words(words: List[str], k: int) -> List[str]:
    """
    Time: O(N log K) | Space: O(N) for Hash Map, O(K) for Heap
    Amazon explicitly forbids O(N log N) complete sorting here.
    """
    # 1. Build the Frequency Map (O(N) Time, O(N) Space)
    freq_map = collections.Counter(words)
    print(f"  Frequency Map Generated: {dict(freq_map)}")
    
    # 2. Maintain a Min-Heap of size strictly K (O(N log K) Time, O(K) Space)
    min_heap = []
    
    for word, count in freq_map.items():
        # Push the custom object onto the heap
        heapq.heappush(min_heap, WordFreq(word, count))
        
        # If the heap exceeds size K, instantly eject the 'smallest/worst' item!
        if len(min_heap) > k:
            ejected = heapq.heappop(min_heap)
            print(f"    -> Heap exceeded size {k}! Ejected: '{ejected.word}' (Freq: {ejected.freq})")
            
    # 3. Extract the final K elements. 
    # Because it's a Min-Heap, the absolute smallest is popped first.
    # We must reverse the list to get descending order!
    result = []
    while min_heap:
        result.append(heapq.heappop(min_heap).word)
        
    return result[::-1]

def demonstrate_amazon_heap():
    section_header("Amazon: Top K Frequent Elements (O(N log K))")
    
    words = ["i", "love", "amazon", "i", "love", "coding", "amazon", "aws", "i"]
    k = 2
    
    print(f"Words Array: {words}")
    print(f"Target (K) : {k} most frequent words.\n")
    
    ans = top_k_frequent_words(words, k)
    print(f"\nFinal Top {k} List: {ans}")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If I ask you to find the Top K elements, why is using `list.sort()` an immediate failure?"
   Senior Answer: "Calling `list.sort()` forces the CPU to execute Timsort on the entire array, sorting every single element regardless of whether it is in the Top K or not. This takes $O(N \\log N)$ time and potentially massive temporary memory allocations. If the file contains 10 Billion words and you only want the Top 10, sorting the other 9,999,999,990 words is an algorithmic disaster. By using a Priority Queue (Min-Heap) bounded to exactly size K, we instantly discard any element that is mathematically proven to not be in the Top 10. Inserting into a size K heap is $O(\\log K)$. Therefore, scanning the file takes exactly $O(N \\log K)$ time, and uses exactly $O(K)$ memory, achieving massive theoretical scalability."

2. Interviewer: "Python's `heapq` module only provides a Min-Heap natively. If a problem explicitly requires a Max-Heap (e.g., finding the K Smallest elements), how do you adapt it?"
   Senior Answer: "Because Python does not have a native `max_heapq` implementation, we achieve it via mathematical negation. When pushing integers onto the heap, we multiply them by `-1`. Therefore, the absolute largest positive number becomes the absolute smallest negative number, naturally rising to the top of the Min-Heap. When popping elements, we simply multiply them by `-1` again to restore their original mathematical state. This perfectly simulates a Max-Heap in $O(1)$ constant overhead. For custom Objects, we simply override the `__lt__` (less than) dunder method to invert the comparison logic."

3. Interviewer: "In the Top K Frequent Words problem, what does `collections.Counter` do under the hood, and what is its time complexity?"
   Senior Answer: "Under the hood, `collections.Counter` is a C-optimized subclass of the Python `dict`. It iterates over the iterable in a single $O(N)$ pass. For each element, it performs a highly optimized $O(1)$ Hash Table lookup and increments the associated integer value. Because it is implemented directly in the CPython C API, it completely bypasses the Python interpreter's bytecode evaluation loop, making it astronomically faster and more memory-efficient than manually writing `if word in dict: dict[word] += 1` inside a Python `for` loop."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: FAANG Prep (Amazon) Completed.")
