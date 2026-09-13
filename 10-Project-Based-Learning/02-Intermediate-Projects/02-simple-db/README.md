# Simple Key-Value Database Engine

## Problem Statement
Modern software applications, ranging from small embedded systems and mobile apps to massive distributed microservices, require efficient ways to store and retrieve data. Traditional relational databases (like PostgreSQL or MySQL) can be heavy, requiring significant setup, separate server processes, complex SQL query parsing, and substantial memory overhead. For many applications—such as caching layers, local configuration storage, or high-throughput event logging—a full SQL database is overkill. 

The problem is how to design a persistent storage system that is extremely lightweight, requires zero configuration or external processes, and provides blazingly fast read and write operations. The solution must ensure that data persists across application restarts (durability) while maintaining a minimal memory footprint. Specifically, we need to build an embedded Key-Value (KV) store from scratch that guarantees $O(1)$ read and write performance, handles graceful restarts, and provides a foundation for more advanced database concepts like Write-Ahead Logging (WAL) and background compaction.

## Learning Objectives
By completing this project, you will achieve a deep understanding of core database internals and low-level system design. Specifically, you will learn:
- **Disk I/O and File Handling:** How to efficiently read from and write to the filesystem using binary modes and precise byte-offset seeking.
- **Data Serialization:** Techniques for converting Python objects (strings, integers, dictionaries) into raw binary formats using modules like `struct` and `json`, and deserializing them back into memory.
- **Append-Only Storage Architecture:** Understanding why modern storage engines (like Bitcask, used in Riak) use append-only logs to maximize write throughput by avoiding random disk seeks.
- **In-Memory Indexing:** Designing a hash-based index to map keys to disk offsets, enabling instantaneous $O(1)$ read operations.
- **Crash Recovery & Durability:** Implementing initialization routines that sequentially scan the log file upon startup to reconstruct the in-memory index, ensuring no data is lost after a crash or restart.
- **Garbage Collection (Compaction):** Developing algorithms to prune stale or deleted records from an append-only log to reclaim disk space.
- **Concurrency & Atomicity (Bonus):** Exploring how checksums (CRC32) and atomic file renames protect against partial writes and data corruption.

## Functional Requirements
The database engine must satisfy the following core requirements:
1. **Initialize/Open Database:** The engine must accept a file path and open (or create) the underlying storage file. Upon opening, it must automatically rebuild its internal index from the existing file.
2. **Set (Write):** A method `set(key, value)` that stores a key-value pair. If the key already exists, the new value must overwrite the logical state of the old value. 
3. **Get (Read):** A method `get(key)` that retrieves the value associated with a key. It must return the value or a designated "Not Found" indicator (e.g., `None` or an Exception).
4. **Delete:** A method `delete(key)` that removes a key-value pair from the logical state of the database.
5. **Persistence:** Data must survive application termination. Restarting the engine on the same file must restore the exact state prior to termination.
6. **Compaction:** A method `compact()` that optimizes disk usage by removing old versions of updated keys and completely removing deleted keys, producing a newly compacted data file.

## Suggested Architecture / Data Flow
The architecture is heavily inspired by **Bitcask**. It relies on two main components: an **Append-Only Log (AOL) on Disk** and an **In-Memory Keydir (Hash Map)**.

### Data Flow Diagram
```mermaid
flowchart TD
    Client((Client App))
    Mem[In-Memory Index \n Dictionary: Key -> (Offset, Size)]
    Disk[(Append-Only Data File)]
    
    Client -- "set(key, val)" --> WriteLogic[Append to File]
    WriteLogic -- "1. Write Record" --> Disk
    WriteLogic -- "2. Update Index" --> Mem
    
    Client -- "get(key)" --> ReadLogic[Lookup Key]
    ReadLogic -- "1. Fetch Offset" --> Mem
    ReadLogic -- "2. Seek & Read" --> Disk
    Disk -- "3. Return Data" --> Client
    
    Client -- "delete(key)" --> DelLogic[Append Tombstone]
    DelLogic -- "1. Write Tombstone" --> Disk
    DelLogic -- "2. Remove from Index" --> Mem
    
    Crash[System Restart] --> InitLogic[Rebuild Index]
    InitLogic -- "Sequential Scan" --> Disk
    InitLogic -- "Reconstruct" --> Mem
```

### Record Structure on Disk
To efficiently parse the append-only log, every entry must follow a strict binary layout (a header followed by the payload). A common structure is:
- **Timestamp (4 bytes)**
- **Key Size (4 bytes)**
- **Value Size (4 bytes)**
- **Key (variable length bytes)**
- **Value (variable length bytes)**

*Note: A Value Size of `-1` (or a specific flag) can represent a tombstone for deletion.*

## Step-by-Step Implementation Guide

### Step 1: Basic Setup and File Handling
1. Create a class `SimpleDB`. Its constructor should accept a filename (e.g., `data.db`).
2. Open the file in append-binary mode (`ab+`). This ensures all new writes go to the end of the file.
3. Initialize an empty dictionary `self._index = {}`. This is your Keydir.

### Step 2: Implementing the Write (`set`) Operation
1. Serialize the key and value into bytes (e.g., using `key.encode('utf-8')`).
2. Calculate the lengths of the encoded key and value.
3. Pack the header using Python's `struct` module (e.g., `struct.pack('<III', timestamp, key_len, val_len)`).
4. Get the current file position using `file.tell()`. This will be the offset you save in your index.
5. Write the header, then the key, then the value to the file. Ensure you call `file.flush()` (and optionally `os.fsync()`) to push data from OS buffers to physical disk.
6. Update `self._index[key] = (offset, size_of_record)`.

### Step 3: Implementing the Read (`get`) Operation
1. Check if the key exists in `self._index`. If not, return `None`.
2. Retrieve the `(offset, size)` tuple from the index.
3. Seek to the specific `offset` in the file using `file.seek(offset)`.
4. Read the exact number of bytes specified by `size`.
5. Unpack the header to determine the lengths of the key and value.
6. Extract the value bytes and deserialize them back to a string (or original object type), then return it.

### Step 4: Implementing Deletion
1. When `delete(key)` is called, check if the key exists in the index.
2. If it does, write a special "Tombstone" record to the disk. This is just a normal write operation but with a special marker (like a zero-length value or a specific tombstone flag in the header).
3. Remove the key from `self._index`.

### Step 5: Crash Recovery (Building the Index on Startup)
1. In the `SimpleDB` constructor, before allowing any reads/writes, read the entire file sequentially from the beginning (offset 0).
2. While not at the end of the file (EOF):
   - Read the header to get key/value sizes.
   - Read the key and value.
   - If it's a valid value, add/update the key in the in-memory index with its offset.
   - If it's a tombstone, remove the key from the in-memory index.
   - Advance your reading offset pointer.
3. This process guarantees that only the *latest* state of a key is stored in memory, and deleted keys are properly ignored.

### Step 6: Implementing Compaction
1. Create a `compact()` method.
2. Open a new temporary file (e.g., `data.db.compact`).
3. Iterate over the keys in your `self._index`.
4. For each key, use `get(key)` to fetch the current, valid value.
5. Write this key-value pair to the new temporary file.
6. Update a temporary in-memory index with the new offsets.
7. Once all valid keys are written, safely swap the files (e.g., using `os.rename()` or `shutil.move()` to replace `data.db` with `data.db.compact`).
8. Replace the old `self._index` with the new temporary index.

## Expected Edge Cases & Challenges
- **Partial Writes:** If the system crashes precisely while writing a record (e.g., header is written, but value is not), the sequential scan on startup will fail due to corrupted byte alignments. *Solution:* Use checksums (CRC32) in the header. If the calculated checksum of the payload doesn't match the header, discard the record as a partial write.
- **Memory Limits:** The hash index stores all keys in memory. If you have 100 million keys, memory consumption will skyrocket. *Solution:* This is a known limitation of Bitcask. You must ensure keys are small, or partition databases.
- **Concurrency (Multi-threading/Multi-processing):** Multiple threads calling `set()` simultaneously might interleave bytes in the file. *Solution:* Wrap disk writes in a threading `Lock()`. If multiple processes are involved, you need OS-level file locks (e.g., `fcntl` on Linux).
- **Compaction Race Conditions:** What happens if a client calls `set()` while a background `compact()` is running? Handling this smoothly requires complex locking or immutable file structures (like LSM Trees).

## Testing Strategy
- **Basic CRUD Tests:** Write unit tests that instantiate the DB, `set` a key, `get` the key, `delete` the key, and verify `get` returns `None`.
- **Persistence Tests:**
  1. Write multiple keys to DB.
  2. Forcibly close/delete the DB instance object.
  3. Re-instantiate the DB object pointing to the same file.
  4. Assert that all previously written keys are accessible and correct.
- **Compaction Tests:** Write a key 100 times. Check the file size. Run `compact()`. Check the file size again (it should drastically reduce to only contain 1 record).
- **Binary Data Tests:** Test storing values that contain null bytes (`\x00`), newlines, or Unicode characters to ensure serialization logic is robust.
- **Failure Injection (Advanced):** Manually truncate the last 5 bytes of the data file to simulate a partial write crash, and ensure the DB initialization logic handles it gracefully without throwing fatal exceptions.

## Extension Ideas
1. **CRC32 Data Integrity:** Add checksums to your record header to validate that data hasn't suffered from bit-rot or partial writes.
2. **Range Queries (B-Tree):** Swap the Python dictionary for an in-memory B-Tree or Red-Black Tree. This allows you to implement queries like `get_range("user_100", "user_200")`.
3. **Data Types:** Use Python's `json` or `msgpack` to allow storing lists, dictionaries, or custom objects as values, rather than just raw bytes or strings.
4. **Background Compaction:** Move the `compact()` method into a separate background thread that runs automatically when the file reaches a certain size threshold (e.g., > 10MB) or when the percentage of dead records (stale updates + tombstones) exceeds 50%.
5. **Caching Layer:** Introduce an LRU (Least Recently Used) cache in memory for the *values*, so hot keys don't require disk I/O on every read.
