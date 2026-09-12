# High-Performance Data Structures in Python

## 1. What is this project?
This project focuses on implementing **High-Performance Data Structures** in Python. Standard Python data structures (like `dict`, `list`, `set`) are incredibly versatile, but they are built for general-purpose use. When you are processing millions of records, building a database engine, or writing a high-frequency trading system, the overhead of Python objects (pointers, reference counting, dynamic typing) becomes a massive bottleneck.

This project covers advanced structures designed for speed, memory efficiency, and specific workloads.

## 2. Why does this exist? (Industry Use Cases)
- **Database Engines**: Implementing LSM (Log-Structured Merge) trees or B-Trees used in Cassandra, RocksDB, or PostgreSQL.
- **Networking/Caching**: Implementing Bloom Filters or Cuckoo Filters to quickly test if an item is in a cache without hitting the database (used by CDN providers like Cloudflare).
- **Text Processing / Search Engines**: Implementing Tries and Suffix Trees for auto-complete systems and fast substring searches.
- **Big Data Processing**: Using memory-mapped files and `__slots__` to process data larger than RAM without memory bloat.

## 3. Beginner Explanation
Imagine you have a tiny box (RAM) and a million toys (data). If you put each toy in its own giant bubble wrap (standard Python objects), they won't fit in the box, and finding one takes forever. High-performance data structures are like custom-molded organizers that fit the toys perfectly without bubble wrap, allowing you to store 10x more toys and find them instantly.

## 4. Advanced Technical Explanation
Python's standard objects have a high memory footprint due to `PyObject` overhead (refcount, type pointer, dictionary for attributes). 
To achieve high performance in Python, we bypass these constraints using:
1. **`__slots__`**: Prevents the creation of `__dict__` for instances, saving memory.
2. **Bit Manipulation**: Storing multiple boolean/integer values in a single 64-bit integer.
3. **Probabilistic Data Structures**: Trading 100% accuracy for O(1) time and extreme space efficiency (e.g., Bloom Filter).
4. **Locality of Reference**: Designing structures that are cache-line friendly (though harder in pure Python, typically achieved using array modules or Cython).

## 5. What's Inside the Implementation (`main.py`)
1. **Bloom Filter**: A probabilistic data structure for set membership.
2. **Compact Trie**: A space-optimized prefix tree for fast string prefix matching.
3. **Memory-Optimized Structs**: Using `__slots__` and the `array` module for massive collections.

## 6. Common Mistakes & Pitfalls
- **Premature Optimization**: Don't use a Bloom Filter if a standard Python `set` easily fits in memory.
- **Hash Collisions in Bloom Filters**: Choosing the wrong array size or number of hash functions leads to high false-positive rates.
- **Python's GIL**: Pure Python data structures won't automatically scale across CPU cores. For multi-threading, you often need C extensions.

## 7. Interview Questions
1. **Question**: *Explain how a Bloom Filter works and when you would use it.*
   **Answer**: A Bloom filter uses a bit array and multiple hash functions. To insert an item, we hash it $k$ times and set the corresponding bits to 1. To check membership, we verify if all $k$ bits are 1. It guarantees no false negatives, but allows false positives. Used in front of databases to prevent expensive disk lookups for non-existent keys.
2. **Question**: *Why does Python's `list` append have amortized O(1) time complexity, and how is memory managed?*
   **Answer**: Python lists are dynamic arrays. They allocate more space than currently needed. When full, a new larger array is allocated (typically ~1.125x larger), and items are copied over. The cost of copying is amortized over the insertions.
3. **Question**: *How do `__slots__` save memory in Python?*
   **Answer**: By default, Python class instances have a `__dict__` to store dynamic attributes. `__slots__` tells Python to pre-allocate space for exactly the declared variables and skip creating the `__dict__`, significantly reducing memory overhead per instance.

## 8. Practical Exercises
1. Modify the `BloomFilter` in `main.py` to calculate the optimal size `m` and number of hash functions `k` based on an expected number of items and a target false positive rate.
2. Implement a `Count-Min Sketch` to keep track of frequency counts in a continuous data stream.
3. Profile the memory usage of 1 million standard class instances vs. 1 million instances using `__slots__` using the `tracemalloc` library.
