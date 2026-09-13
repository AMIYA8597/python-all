"""
# ==============================================================================
# LABORATORY: BLOOM FILTERS (PROBABILISTIC STRUCTURES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Imagine you are building Google Chrome's "Malicious URL Warning" feature. 
# There are 100 Million malicious URLs. Storing them in a Python `set` would 
# take Gigabytes of RAM on the user's laptop. That is unacceptable.
#
# Alternatively, what if you manage a database (like Cassandra), and a user 
# requests a record that DOES NOT EXIST. Searching the slow Hard Drive to confirm 
# it doesn't exist is a massive waste of time.
#
# A "Bloom Filter" solves both problems. It is a Probabilistic Data Structure 
# that uses a tiny Array of Bits (0s and 1s) and multiple Hash Functions.
# 
# The magic rule of a Bloom Filter:
# - It can say "DEFINITELY NOT in the set" (100% accurate).
# - It can say "PROBABLY in the set" (Might be a False Positive).
#
# By checking the Bloom Filter first, databases can instantly abort 99% of 
# useless disk lookups using only Kilobytes of RAM!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of a Bit Array and Multiple Hash Functions.
# - Understand why False Positives happen.
# - Understand why False Negatives are mathematically impossible.
# - Implement a Bloom Filter from scratch.
#
# ==============================================================================
"""

import hashlib
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BLOOM FILTER IMPLEMENTATION
# ==============================================================================
class BloomFilter:
    """
    A space-efficient probabilistic data structure.
    """
    def __init__(self, items_expected: int, false_positive_rate: float):
        """
        Dynamically calculates the optimal bit array size (M) and number of 
        hash functions (K) based on the desired false positive rate.
        """
        # M = -(N * ln(P)) / (ln(2)^2)
        self.size = int(-(items_expected * math.log(false_positive_rate)) / (math.log(2)**2))
        
        # K = (M / N) * ln(2)
        self.num_hashes = int((self.size / items_expected) * math.log(2))
        
        # The bit array (initialized to all 0s)
        # Note: In C/C++, you would use actual binary bits to save space.
        # Python's list of booleans is fine for demonstration.
        self.bit_array = [False] * self.size
        
        print(f"Bloom Filter Initialized:")
        print(f" Expected Items: {items_expected}")
        print(f" Target False Positive Rate: {false_positive_rate * 100}%")
        print(f" Calculated Bit Array Size (M): {self.size} bits")
        print(f" Calculated Hash Functions (K): {self.num_hashes}")

    def _get_hashes(self, item: str) -> list[int]:
        """
        Generates K different hash values for the given item.
        We simulate K different hash functions by appending an integer to the string 
        and running it through MD5.
        """
        hashes = []
        for i in range(self.num_hashes):
            # E.g., "apple0", "apple1", "apple2"
            seeded_string = f"{item}{i}".encode('utf-8')
            
            # Use MD5, grab the hex, convert to integer, and modulo by bit array size
            hash_int = int(hashlib.md5(seeded_string).hexdigest(), 16)
            hashes.append(hash_int % self.size)
            
        return hashes

    def add(self, item: str) -> None:
        """
        Adds an item to the Bloom Filter by setting its K hashed indices to True (1).
        """
        hashes = self._get_hashes(item)
        for h in hashes:
            self.bit_array[h] = True

    def check(self, item: str) -> bool:
        """
        Checks if an item is in the Bloom Filter.
        If ANY of its K hashed indices are False (0), the item is DEFINITELY NOT in the set.
        If ALL of its K hashed indices are True (1), the item is PROBABLY in the set.
        """
        hashes = self._get_hashes(item)
        for h in hashes:
            if not self.bit_array[h]:
                return False # 100% guarantee it's not here
        return True # Probably here

def demonstrate_bloom_filter():
    section_header("Algorithm: Bloom Filter")
    
    # We expect to insert 5 malicious URLs, and we want a 10% false positive rate
    bf = BloomFilter(items_expected=5, false_positive_rate=0.10)
    
    malicious_urls = [
        "evil.com",
        "phishing.net",
        "steal-passwords.org",
        "virus.exe.com",
        "bad-guy.io"
    ]
    
    print("\nInserting Malicious URLs into the Bloom Filter...")
    for url in malicious_urls:
        bf.add(url)
        
    print("\nChecking URLs against the Bloom Filter:")
    
    # These were inserted, so they MUST return True
    test_urls_in_set = ["evil.com", "phishing.net"]
    for url in test_urls_in_set:
        result = bf.check(url)
        print(f" {url:20} -> {result} (Expected: True)")
        
    # These were NEVER inserted
    test_urls_not_in_set = ["google.com", "wikipedia.org", "python.org"]
    for url in test_urls_not_in_set:
        result = bf.check(url)
        print(f" {url:20} -> {result} (Expected: False)")
        
    print("\nHow to interpret the results:")
    print("If it said 'False' for google.com, it means Google is 100% safe.")
    print("If it said 'True' for evil.com, the browser will now perform a SLOW, ")
    print("expensive check against a real Database on the Hard Drive to verify ")
    print("that it wasn't a False Positive!")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why are False Negatives impossible in a Bloom Filter?
   Answer: When you add an item, you permanently flip its specific 3 bits to `1`. Those bits can NEVER be flipped back to `0`. When you check for that item later, the filter looks at those exact same 3 bits. Since they were flipped to `1` and can never be erased, the filter will ALWAYS read them as `1` and return True.

2. Why do False Positives happen?
   Answer: Imagine Item A flips bits `[1, 5, 8]`. Item B flips bits `[2, 7, 9]`. 
   Now you check if Item C is in the filter. Item C happens to hash to `[1, 7, 8]`. 
   The filter checks bit 1 (True because of A), bit 7 (True because of B), and bit 8 (True because of A). The filter returns True! Item C is a False Positive caused by overlapping bits from other items.

3. Can you DELETE an item from a standard Bloom Filter?
   Answer: NO! If you try to delete Item A by flipping its bits `[1, 5, 8]` back to `0`, you might accidentally flip bit 8 to `0`. But wait! Item C also relied on bit 8. By "deleting" A, you just corrupted the filter, and now Item C will return a False Negative! (To support deletion, you must use a complex variation called a Counting Bloom Filter).
"""

if __name__ == "__main__":
    demonstrate_bloom_filter()
    print("\n[SUCCESS] Laboratory: Bloom Filters Completed.")
