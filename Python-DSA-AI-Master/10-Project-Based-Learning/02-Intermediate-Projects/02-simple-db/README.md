# Simple Key-Value Database Engine

## Project Overview
This project builds a simple, embedded Key-Value database from scratch in Python. It demonstrates core database concepts such as disk-based storage, indexing, serialization, and basic durability guarantees (Write-Ahead Logging).

## Industry Use Cases
- **Embedded Databases:** Used in mobile apps or local desktop apps (e.g., SQLite, RocksDB, LevelDB) for persistent state storage without needing a network connection.
- **Caching Systems:** Principles are similar to systems like Redis or Memcached, mapping keys to values for fast retrieval.
- **Config Management:** Storing application configurations or user preferences locally.

## Beginner Explanation
A database is essentially a system that stores information and allows you to find it quickly later. While you could just write everything to a text file, finding specific data in a huge text file requires reading the whole thing, which is slow.
This project creates a database that uses an "index" (like a table of contents in a book) kept in memory (RAM), while the actual data is saved securely on the hard drive. When you ask for a key, the database checks the index to find the exact location on the hard drive and goes straight there to fetch the value instantly.

## Technical Explanation (Deep Dive)
At the core of this database is an Append-Only Log (AOL) storage mechanism and an In-Memory Hash Map for indexing (commonly associated with architectures like Bitcask).

1. **Storage (Append-Only Log):**
   Every insert or update is appended to the end of a file. This makes write operations incredibly fast ($O(1)$ disk I/O) because it avoids seeking random locations on disk. Deletions are also handled by appending a special "tombstone" marker for the key.

2. **Indexing (In-Memory Hash Map):**
   To ensure fast reads, the engine maintains a Python dictionary mapping the `key` to a tuple containing `(file_offset, data_size)`. When a read is requested, the system does an $O(1)$ lookup in the dictionary to find the byte offset, seeks to that offset in the file, and reads the specific number of bytes.

3. **Crash Recovery:**
   When the database engine restarts, it reads the append-only log sequentially from the beginning to reconstruct the in-memory index, resolving the latest values for any updated keys.

4. **Compaction (Garbage Collection):**
   Because updates and deletes append new records rather than overwriting old ones, the file grows indefinitely. A compaction background process reads the file, keeps only the latest values for active keys, writes them to a new file, and swaps the files, reclaiming wasted space.

## Realistic Interview Questions
1. **What happens if the system crashes while writing a record?**
   *Answer:* In a robust system, you'd implement a Write-Ahead Log (WAL) or ensure atomic writes using checksums. If a record is partially written, the checksum will fail on crash recovery, and the partial record will be discarded.
2. **Why use an Append-Only design instead of updating records in place (like B-Trees)?**
   *Answer:* Append-only logs maximize write throughput by utilizing sequential disk I/O, which is much faster than random disk I/O (especially on HDDs). It also prevents data corruption from partial overwrites and makes concurrency management easier.
3. **What is the limitation of the Bitcask-like architecture described here?**
   *Answer:* All keys must fit entirely in RAM (memory). If you have billions of keys, the hash index will consume all available memory.

## Practical Exercises
- **Implement Compaction:** Write a `compact()` method that creates a new data file with only the valid, non-deleted, latest keys, then replaces the old file.
- **Implement Checksums:** Add a CRC32 checksum to each stored record. When reading, verify the checksum to detect data corruption.
- **Add Range Queries:** Think about how you would modify the index (e.g., using a balanced Binary Search Tree or B-Tree instead of a Hash Map) to support querying keys within a certain range.
