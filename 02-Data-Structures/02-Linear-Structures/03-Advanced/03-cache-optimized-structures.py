"""
# ==============================================================================
# LABORATORY: CACHE-OPTIMIZED STRUCTURES (B-TREES & DATA LOCALITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Big-O notation lies to you. It assumes that fetching data from memory always 
# takes exactly O(1) time. In reality, modern CPUs have Caches (L1, L2, L3) that 
# are 100x faster than main RAM. If you iterate through a Linked List or a Binary 
# Tree, the CPU must fetch random sectors of RAM (pointer chasing), causing Cache 
# Misses. A contiguous Array, despite having identical Big-O complexity for some 
# algorithms, will execute 10x to 50x faster because of Cache Locality.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand why Linked Lists are avoided in High-Performance Computing (HPC).
# - Compare Binary Search (Array) vs Binary Search Tree (Pointer Chasing).
# - Understand the architecture of B-Trees (The foundation of SQL Databases).
#
# ==============================================================================
"""

import timeit
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE CACHE MISS DISASTER (ARRAY VS LINKED LIST)
# ==============================================================================
class Node:
    __slots__ = ['val', 'next']
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def demonstrate_cache_misses():
    """
    We will create 500,000 items in an array and 500,000 items in a Linked List.
    We will then traverse both. According to Big-O, both are O(N).
    In reality, the array will obliterate the Linked List due to cache locality.
    """
    section_header("Cache Misses: Array vs Linked List (O(N) vs O(N))")
    
    N = 500_000
    
    # 1. Contiguous Array
    arr = list(range(N))
    
    def traverse_array():
        total = 0
        for x in arr:
            total += x
        return total
        
    # 2. Scattered Linked List
    # We purposefully allocate them dynamically so they scatter in the heap
    head = Node(0)
    curr = head
    for i in range(1, N):
        curr.next = Node(i)
        curr = curr.next
        
    def traverse_linked_list():
        total = 0
        curr = head
        while curr:
            total += curr.val
            curr = curr.next
        return total
        
    print(f"Traversing {N:,} elements (Calculating Sum)...")
    
    t_arr = timeit.timeit(traverse_array, number=10)
    t_ll = timeit.timeit(traverse_linked_list, number=10)
    
    print(f"Array Time (Cache Friendly):  {t_arr:.4f}s")
    print(f"Linked List (Pointer Chasing):{t_ll:.4f}s")
    print(f"-> The Array is {t_ll/t_arr:.2f}x faster despite both being O(N)!")
    print("Why? The CPU loads 64 bytes (a cache line) at a time. The array gives")
    print("the CPU the next several items for 'free'. The Linked List forces the")
    print("CPU to wait for main RAM (cache miss) on every single node.")


# ==============================================================================
# 4. BINARY SEARCH VS BINARY SEARCH TREE (BST)
# ==============================================================================
def demonstrate_binary_search_vs_bst():
    """
    Searching a balanced BST takes O(log N).
    Binary searching a sorted array takes O(log N).
    Which is faster? The array, because navigating the tree requires random 
    memory access (pointer chasing), whereas the array provides cache locality.
    """
    section_header("Search: Sorted Array vs BST (O(log N) vs O(log N))")
    print("If you need to search data quickly, DO NOT build a Binary Search Tree.")
    print("Sort an Array and use the `bisect` module (Binary Search).")
    print("It uses significantly less memory (no left/right pointers) and executes")
    print("faster due to CPU Cache predictability.")
    print("\nThe ONLY reason to use a BST is if you need to rapidly INSERT data")
    print("and maintain sorted order (O(log N) insert vs O(N) array insert).")


# ==============================================================================
# 5. B-TREES (THE DATABASE SOLUTION)
# ==============================================================================
def demonstrate_b_trees():
    """
    If arrays are slow to insert (O(N)), and BSTs are slow to read because of 
    cache misses, what do databases (PostgreSQL/MySQL) use?
    They use B-Trees (Balanced Trees).
    """
    section_header("B-Trees (Cache-Optimized Trees)")
    print("""
A standard Binary Search Tree has 1 value per node, and 2 children.
This means traversing down 10 levels requires 10 cache misses (RAM fetches).

A B-Tree (used in databases) solves this by packing multiple values into a 
SINGLE node (e.g., 100 values per node), and having 101 children. 
These 100 values are stored as a contiguous ARRAY inside the node!

When the CPU fetches the node, it pulls the entire array of 100 values into 
the L1 Cache simultaneously. It then performs a blazing-fast Binary Search 
INSIDE the cached node to find the correct child pointer.

Result: A B-Tree flattens the tree. A database with 1 Billion rows can be 
stored in a B-Tree that is only 3 or 4 levels deep. This means finding ANY 
row in a 1 Billion row database requires a MAXIMUM of 4 cache misses (or 
4 disk I/O reads).
    """)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a CPU Cache make Arrays significantly faster than Linked Lists?
   Answer: The CPU reads RAM in 64-byte chunks called Cache Lines. Because an array is contiguous in memory, fetching one element brings the next several elements into the ultra-fast L1 cache for free. A Linked List's nodes are scattered randomly in memory, causing a "Cache Miss" (forcing the CPU to wait for RAM) on almost every iteration.

2. If a Binary Search Tree (BST) and Binary Search on an array are both O(log N) for searching, which is faster in reality?
   Answer: Binary Search on an array is significantly faster due to Cache Locality and the lack of pointer-chasing overhead.

3. How does a B-Tree optimize for Cache Locality compared to a standard Binary Tree?
   Answer: Instead of storing 1 value per node, a B-Tree stores a large array of values in a single node. This array is fetched into the CPU cache entirely, allowing the CPU to quickly binary-search the node's contents to find the correct child pointer. This drastically reduces the height of the tree, minimizing expensive RAM/Disk reads.
"""

if __name__ == "__main__":
    demonstrate_cache_misses()
    demonstrate_binary_search_vs_bst()
    demonstrate_b_trees()
    print("\n[SUCCESS] Laboratory: Cache-Optimized Structures Completed.")
