"""
## A. Concept Name
Bloom Filters

## B. Prerequisites
- Hashing functions
- Arrays/Lists
- Probability concepts

## C. Why Learn This
Bloom filters are essential for high-performance systems where we need to quickly check if an item exists without storing the item itself, saving immense amounts of memory.

## D. Core Mechanics
A Bloom filter is a space-efficient probabilistic data structure. It uses an array of bits and multiple hash functions to test whether an element is a member of a set. False positive matches are possible, but false negatives are not.

## E. Implementation Details
The filter initializes a bit array of size `m` to 0. When an item is added, it is hashed by `k` different hash functions, which each map to one of the `m` array positions, setting them to 1. To check if an item is in the set, hash it again with the `k` functions and check if all corresponding bits are 1.

## F. Performance Analysis
- Time Complexity: O(k) for insertion and search, where k is the number of hash functions.
- Space Complexity: O(m) where m is the number of bits in the filter.

## G. Trade-offs
- Space vs. Accuracy: A larger bit array (m) reduces the false positive rate but takes more memory.
- Hash Count vs. Speed/Accuracy: More hash functions (k) can reduce false positives to a point but slow down operations and fill the filter faster.

## H. Edge Cases
- Determining the optimal size and number of hash functions to minimize false positives.
- Handling elements that generate colliding hashes across all functions.

## I. Common Pitfalls
- Not sizing the filter correctly for the expected number of items, leading to high false positive rates.
- Using slow cryptographic hash functions when non-cryptographic (like MurmurHash) would suffice and be faster.

## J. Interview Challenge
Design a system that quickly checks if a username is already taken.

## K. Code Structure
- `BloomFilter` class encapsulates the bit array and logic.
- `_get_size` and `_get_hash_count` calculate optimal parameters.
- `_get_hashes` provides the k hash values.

## L. Visual/Mental Model
Imagine a long row of light switches initially all off. When someone enters a room, they flip specific switches on based on their name. Later, to check if someone entered, you see if their specific combination of switches is on. If yes, they *probably* entered. If any are off, they *definitely* did not.

## M. Test Strategy
Testing probabilistic structures requires statistical validation (e.g., adding many items and measuring the actual false positive rate against the expected rate), alongside basic functional tests.

## N. Real-world Applications
- Malicious URL checking in web browsers.
- Preventing recommendations of articles a user has already read.
- Database query optimization (checking if a row exists before accessing disk).

## O. Variants
- Counting Bloom Filters: Allow deletion of items.
- Scalable Bloom Filters: Dynamically adapt to the number of items.

## P. Standard Library Equivalents
Python does not have a built-in Bloom filter. Third-party libraries like `pybloom` or `bloom-filter` are commonly used.

## Q. Best Practices
- Use fast, non-cryptographic hash families if security against adversarial inputs is not a concern.
- Carefully estimate the maximum number of items (n) before initializing.

## R. System Design Context
Used extensively in distributed systems (like Cassandra or Bigtable) to minimize expensive disk or network lookups for missing items.

## S. Historical Context
Invented by Burton Howard Bloom in 1970 to efficiently store a set of allowed words in a spell checker.

## T. Further Reading
- Wikipedia: Bloom Filter
- "Network Applications of Bloom Filters: A Survey"

## U. Related Patterns
- Hash Tables
- Cuckoo Filters

## V. Exercises
1. Implement a deletion operation (requires switching to a Counting Bloom Filter).
2. Measure the actual false positive rate by inserting 10,000 items and querying 10,000 different items.

## W. Solutions
(Self-guided exercises)

## X. Project Connection
Can be integrated into the caching layer of a web application project to prevent cache stampedes for non-existent keys.
"""

import math
import hashlib

class BloomFilter:
    def __init__(self, items_count: int, fp_prob: float):
        self.fp_prob = fp_prob
        self.size = self._get_size(items_count, fp_prob)
        self.hash_count = self._get_hash_count(self.size, items_count)
        self.bit_array = [False] * self.size

    def add(self, item: str) -> None:
        digests = self._get_hashes(item)
        for i in digests:
            self.bit_array[i] = True

    def check(self, item: str) -> bool:
        digests = self._get_hashes(item)
        for i in digests:
            if not self.bit_array[i]:
                return False
        return True

    def _get_size(self, n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

    def _get_hash_count(self, m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return int(k)

    def _get_hashes(self, item: str) -> list[int]:
        hashes = []
        for i in range(self.hash_count):
            h = hashlib.md5((item + str(i)).encode()).hexdigest()
            hashes.append(int(h, 16) % self.size)
        return hashes

# Tests
def test_bloom_filter():
    bf = BloomFilter(20, 0.05)
    bf.add("apple")
    bf.add("banana")
    
    assert bf.check("apple") is True
    assert bf.check("banana") is True
    # 'cherry' is extremely likely to return False
    # A true test for a probabilistic data structure needs statistical validation.
    assert bf.check("cherry") is False

if __name__ == "__main__":
    test_bloom_filter()
    print("02-bloom-filters.py tests passed successfully!")
