"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - STANDARD LIBRARY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I want you to build a caching system. If the cache is full, 
# evict the oldest item."
# 
# A junior engineer will spend 30 minutes writing a complex class with Hash Maps 
# and Linked Lists to implement an LRU (Least Recently Used) cache, and likely 
# introduce a bug.
#
# A senior Python engineer will write EXACTLY ONE LINE of code: 
# `@functools.lru_cache(maxsize=128)`
#
# FAANG interviewers want to see that you actually know the Python Standard 
# Library. Reinventing the wheel (e.g., using a List as a Queue, which causes 
# catastrophic O(N) performance instead of using `collections.deque`) proves 
# you lack production experience.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master `collections.deque` (Doubly Linked Lists for O(1) Queues).
# - Master `functools.lru_cache` (Memoization).
# - Master `collections.defaultdict` vs `dict.setdefault()`.
#
# ==============================================================================
"""

import collections
import functools
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DEQUE VS LIST (THE O(N) QUEUE DISASTER)
# ==============================================================================
def demonstrate_deque_vs_list():
    section_header("collections.deque (O(1) Front Insertion)")
    
    # We want to simulate a Queue (First-In, First-Out).
    # New people join the back. People are served from the front.
    
    print("Simulating a Queue of 100,000 items...")
    items = 100_000
    
    # --- BAD METHOD: USING A LIST ---
    bad_queue = list(range(items))
    start = time.perf_counter()
    while bad_queue:
        # pop(0) forces the CPU to shift 99,999 memory addresses to the left!
        bad_queue.pop(0) 
    end = time.perf_counter()
    list_time = end - start
    print(f"  -> List `pop(0)` Time:  {list_time:.4f} seconds (Catastrophic O(N^2) total)")
    
    # --- GOOD METHOD: USING A DEQUE ---
    good_queue = collections.deque(range(items))
    start = time.perf_counter()
    while good_queue:
        # popleft() simply moves a physical pointer. No memory shifting!
        good_queue.popleft() 
    end = time.perf_counter()
    deque_time = end - start
    print(f"  -> Deque `popleft()` Time: {deque_time:.4f} seconds (Perfect O(N) total)")
    
    print(f"\nThe Deque was {list_time / deque_time:.1f}x faster!")


# ==============================================================================
# 4. FUNCTOOLS.LRU_CACHE (MEMOIZATION)
# ==============================================================================

# Without caching, Fibonacci is O(2^N) - an exponential nightmare!
def fib_slow(n: int) -> int:
    if n <= 1: return n
    return fib_slow(n-1) + fib_slow(n-2)

# With caching, Fibonacci becomes strictly O(N)!
@functools.lru_cache(maxsize=128)
def fib_fast(n: int) -> int:
    if n <= 1: return n
    return fib_fast(n-1) + fib_fast(n-2)

def demonstrate_lru_cache():
    section_header("functools.lru_cache (Instant Memoization)")
    
    n = 35 # High enough to crash the slow function
    
    print(f"Calculating Fibonacci({n})...")
    
    print("\n--- SLOW METHOD (O(2^N)) ---")
    start = time.perf_counter()
    ans1 = fib_slow(n)
    end = time.perf_counter()
    print(f"  -> Result: {ans1} | Time: {end - start:.4f} seconds")
    
    print("\n--- FAST METHOD (LRU_CACHE) (O(N)) ---")
    start = time.perf_counter()
    ans2 = fib_fast(n)
    end = time.perf_counter()
    print(f"  -> Result: {ans2} | Time: {end - start:.6f} seconds")
    
    print("\nBy adding EXACTLY ONE LINE of code, we intercepted the recursive calls.")
    print("If the function had seen the input before, it instantly returned the ")
    print("cached output from a Hash Map, bypassing the exponential tree!")


# ==============================================================================
# 5. DEFAULTDICT (CLEAN DICTIONARY INITIALIZATION)
# ==============================================================================
def demonstrate_defaultdict():
    section_header("collections.defaultdict")
    
    logs = [("ERROR", "DB Crash"), ("INFO", "Login"), ("ERROR", "Timeout")]
    
    print("Task: Group logs by severity.")
    
    # --- BAD METHOD (KeyError checks) ---
    bad_dict = {}
    for level, msg in logs:
        if level not in bad_dict:
            bad_dict[level] = []
        bad_dict[level].append(msg)
        
    # --- GOOD METHOD (defaultdict) ---
    # We pass the `list` factory. If a key is missing, it instantly creates an empty list!
    good_dict = collections.defaultdict(list)
    for level, msg in logs:
        # NO KEY CHECKS REQUIRED!
        good_dict[level].append(msg)
        
    print("\nResult (defaultdict):")
    for k, v in good_dict.items():
        print(f"  {k}: {v}")


def run_all_labs():
    demonstrate_deque_vs_list()
    demonstrate_lru_cache()
    demonstrate_defaultdict()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is `list.pop(0)` an $O(N)$ operation, but `deque.popleft()` is $O(1)$?"
   Senior Answer: "A Python List is backed by a contiguous dynamic array in C. When you remove the element at index 0, you leave a physical hole in memory. Because the array must remain contiguous, the CPU must physically grab every single remaining element and shift them one memory address to the left. If there are 1 Million items, it performs 1 Million memory copies ($O(N)$). A `collections.deque` is backed by a Block-based Doubly Linked List. When you call `popleft()`, it does NOT move any data. It simply updates a C-pointer to point to the *next* block of memory, mathematically achieving perfect $O(1)$ performance regardless of size."

2. Interviewer: "How does `@functools.lru_cache` work under the hood, and what does 'LRU' stand for?"
   Senior Answer: "'LRU' stands for Least Recently Used. Under the hood, the decorator wraps your function in a closure that contains a Hash Map (Dictionary) and a Doubly Linked List. When you call `func(X)`, it checks the Hash Map. If `X` exists, it instantly returns the cached result ($O(1)$). If `X` does not exist, it runs the heavy function, stores `X` in the Hash Map, and places it at the 'Front' of the Linked List. If the cache exceeds its `maxsize` (e.g., 128), it physically looks at the 'Back' of the Linked List, finds the item that hasn't been used in the longest time (Least Recently Used), and violently deletes it from the Hash Map to free up RAM. It is a perfect O(1) Caching Engine."

3. Interviewer: "What is the difference between `collections.defaultdict(int)` and `collections.Counter`?"
   Senior Answer: "`defaultdict(int)` creates a dictionary where any missing key instantly evaluates to `0`. You must write a `for` loop to manually populate it (e.g., `for word in words: my_dict[word] += 1`). `collections.Counter` is a specialized subclass explicitly designed for counting. It is highly optimized in C. You don't write a loop at all; you simply pass the raw array directly to it: `counts = Counter(words)`. Furthermore, `Counter` provides powerful analytic methods like `.most_common(3)` which runs a specialized Heap algorithm to instantly extract the top frequencies."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Standard Library) Completed.")
