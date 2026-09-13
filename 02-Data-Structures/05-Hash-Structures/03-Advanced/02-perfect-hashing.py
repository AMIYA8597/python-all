"""
# ==============================================================================
# LABORATORY: PERFECT HASHING (O(1) WORST-CASE, ZERO COLLISIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You learned that Cuckoo Hashing guarantees O(1) worst-case lookups by forcing 
# items to move around. But the insertion process is chaotic.
# 
# What if you have a dataset that is STATIC? (e.g., A dictionary of Python's 
# reserved keywords, or a list of predefined Country Codes). Once it's built, 
# it never changes.
#
# The "Fredman-Komlós-Szemerédi (FKS) Perfect Hashing" algorithm mathematically 
# guarantees ABSOLUTELY ZERO COLLISIONS. It achieves strict O(1) worst-case 
# lookups without any probing, chaining, or evictions.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Two-Level Hashing architecture.
# - Understand the math of squaring bucket sizes (Size = K^2).
# - Implement a Perfect Hash Table for a static dataset.
#
# ==============================================================================
"""

import random
from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MATH OF K^2 (THE BIRTHDAY PARADOX IN REVERSE)
# ==============================================================================
def explain_perfect_hashing_math():
    section_header("Concept: The Math of Zero Collisions")
    print("""
If we have K items, and we want to guarantee ZERO collisions when we hash them, 
how big does the array need to be?
Math proves that if the array is size K^2, the probability of ANY two items 
colliding is LESS THAN 50%.

FKS Perfect Hashing uses a Two-Level System:
1. Level 1: Hash the N items into an array of size N. Collisions WILL happen.
2. Level 2: For any bucket that has a collision (say, 3 items collided), we 
   create a "Secondary Hash Table" strictly for that bucket. 
   The size of this secondary table will be 3^2 = 9!
   
Because the secondary table is size K^2, the chances of collision are < 50%. 
So, we just pick a random hash function, try it, and if it collides, we pick 
a new random hash function and try again. It usually finds a perfect, zero-collision 
hash function on the first or second try!

Wait, doesn't K^2 take up too much memory?
Math proves that the SUM of all K^2 sizes across all buckets will always be 
strictly less than O(N). The memory footprint is highly efficient!
    """)


# ==============================================================================
# 4. PERFECT HASHING IMPLEMENTATION
# ==============================================================================
class UniversalHashFunction:
    """
    A mathematical hash function that can be randomized by changing `a` and `b`.
    Formula: ((a * key + b) % Prime) % Capacity
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.prime = 10**9 + 7 # A large prime
        # a must be 1 to prime-1. b must be 0 to prime-1.
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)
        
    def hash(self, key: int) -> int:
        return ((self.a * key + self.b) % self.prime) % self.capacity


class PerfectHashTable:
    def __init__(self, keys: List[int]):
        """
        Builds the Two-Level Perfect Hash Table for a STATIC list of keys.
        """
        self.n = len(keys)
        
        # Level 1 Hash Function and Array
        self.level1_hash = UniversalHashFunction(self.n)
        
        # We temporarily group collided keys into simple lists
        level1_buckets: List[List[int]] = [[] for _ in range(self.n)]
        
        for key in keys:
            idx = self.level1_hash.hash(key)
            level1_buckets[idx].append(key)
            
        # Level 2 Arrays and Hash Functions
        # We store tuples of (Secondary_Hash_Function, Secondary_Array)
        self.level2: List[Optional[tuple]] = [None] * self.n
        
        # Build the zero-collision secondary tables
        for i in range(self.n):
            bucket_keys = level1_buckets[i]
            k = len(bucket_keys)
            
            if k == 0:
                continue
                
            if k == 1:
                # No collision! Just store it directly with a dummy hash function
                dummy_hash = UniversalHashFunction(1)
                self.level2[i] = (dummy_hash, [bucket_keys[0]])
                continue
                
            # Collision exists! We need a secondary table of size K^2
            sec_capacity = k * k
            
            # Keep trying random hash functions until we get ZERO collisions!
            while True:
                sec_hash = UniversalHashFunction(sec_capacity)
                sec_table = [None] * sec_capacity
                collision_found = False
                
                for key in bucket_keys:
                    sec_idx = sec_hash.hash(key)
                    if sec_table[sec_idx] is not None:
                        collision_found = True
                        break # Abort this hash function and try a new one!
                    sec_table[sec_idx] = key
                    
                if not collision_found:
                    # Success! We found a perfect hash function for this bucket.
                    self.level2[i] = (sec_hash, sec_table)
                    break

    def contains(self, key: int) -> bool:
        """
        O(1) WORST CASE LOOKUP.
        Exactly 2 hash calculations and 2 array accesses.
        """
        # 1. Level 1 Hash
        idx1 = self.level1_hash.hash(key)
        
        # If the primary bucket is completely empty, the key doesn't exist
        if self.level2[idx1] is None:
            return False
            
        # 2. Level 2 Hash
        sec_hash, sec_table = self.level2[idx1]
        idx2 = sec_hash.hash(key)
        
        # Check the exact spot in the secondary table
        return sec_table[idx2] == key

def demonstrate_perfect_hashing():
    section_header("Algorithm: FKS Perfect Hashing")
    
    # We must use integers for this specific Universal Hash Formula.
    # In reality, strings are just converted to integers first.
    static_keys = [10, 22, 37, 40, 52, 60, 70, 72, 85, 99]
    
    print(f"Building Perfect Hash Table for static keys: {static_keys}")
    pht = PerfectHashTable(static_keys)
    
    print("\nLookup Tests (Guaranteed exactly 2 memory accesses):")
    
    print(f" Contains 37? {pht.contains(37)} (Expected: True)")
    print(f" Contains 72? {pht.contains(72)} (Expected: True)")
    print(f" Contains 99? {pht.contains(99)} (Expected: True)")
    
    print(f" Contains 42? {pht.contains(42)} (Expected: False)")
    print(f" Contains 90? {pht.contains(90)} (Expected: False)")
    
    print("\nNotice that there is NO PROBING. There are NO LINKED LISTS.")
    print("If multiple items collided in Level 1, they were spaced out perfectly")
    print("in Level 2 by a custom-tailored Hash Function that was randomly rolled")
    print("until it achieved 0 collisions!")


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does Perfect Hashing only work for Static datasets?
   Answer: Because we create secondary arrays of exact size `K^2` and brute-force a random hash function until it achieves zero collisions for those exact `K` items. If you add a NEW item later, it might collide with the existing items in the secondary table, breaking the "Perfect" zero-collision guarantee and requiring a full recalculation of that bucket.

2. Why is the secondary array size `K^2` instead of just `K`?
   Answer: The Birthday Paradox. If you put 10 items into an array of size 10, the probability of a collision is 99.999%. You would have to roll a random hash function millions of times to find a perfect one. If you put 10 items into an array of size 100 (10^2), the probability of collision drops below 50%. You will likely find a perfect hash function on the first or second attempt!

3. Does `K^2` cause memory bloat? (e.g. what if 1000 items collide in one bucket, requiring an array of 1,000,000?)
   Answer: Statistically, this will not happen. A good Level 1 Hash Function distributes the items relatively evenly. Mathematical proofs show that the expected sum of all `K_i^2` across the entire table is bounded strictly by `O(N)`. It is incredibly memory efficient.
"""

if __name__ == "__main__":
    explain_perfect_hashing_math()
    demonstrate_perfect_hashing()
    print("\n[SUCCESS] Laboratory: Perfect Hashing Completed.")
