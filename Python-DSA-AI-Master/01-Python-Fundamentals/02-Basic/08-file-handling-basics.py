"""
## A. Concept Name
File Handling and Context Managers (I/O Operations)

## B. One-Sentence Definition
File handling is the secure mechanism by which a program reads from and writes to a computer's non-volatile storage (disk), ensuring data persistence beyond the program's execution.

## C. Why Does This Exist?
RAM (Random Access Memory) is volatile; anything stored in variables disappears the moment your script finishes executing or crashes. If you are scraping the web, running an ML model, or collecting user input, you need a way to save that data permanently. File handling provides the standardized OS-level interface to persist data to the hard drive and retrieve it later.

## D. Intuition
Imagine your Python program is a person working at a desk (RAM). The desk is small, and when the person leaves for the day, the desk is wiped clean. If they want to keep their work, they must put it in a filing cabinet (the hard drive). To do this, they have to unlock a specific drawer (open the file), put the paper in (write), and then firmly lock the drawer (close the file). If they forget to lock it, someone else might mess with the papers, or the drawer might get stuck.

## E. Real-Life Analogy
Think of a file like checking out a library book.
- **`open()`**: You check out the book. The librarian (Operating System) notes that YOU have the book. Nobody else can modify it.
- **`read()` / `write()`**: You read the book or make notes in it.
- **`close()`**: You return the book. The librarian checks it back in so others can use it.
If you never return it, the library runs out of books (running out of File Descriptors). Context managers (`with` statements) act like a personal assistant who guarantees the book is returned the second you stop reading it, even if you fall asleep (your program crashes).

## F. Mental Model
Think of file handling as a "pipe" or "stream" connecting your fast, temporary RAM to your slow, permanent Hard Drive. 
- You do not interact with the hard drive directly. You ask the Operating System to open a pipe.
- The OS provides a "file descriptor" (a handle to the pipe).
- Data flows through the pipe in chunks (buffers).
- Closing the file "flushes" the pipe, forcing any remaining data out of the RAM buffer and permanently onto the disk, and then destroys the pipe.

## G. Visual Explanation
```text
+-------------------+       +-----------------------+       +-------------------+
| Python Program    |       | Operating System (OS) |       | Hard Drive (Disk) |
| (RAM)             |       |                       |       |                   |
|                   | open()|   +---------------+   |       |                   |
| f = open('data')  | ----> |   | File Handle   | --------> | [ File 'data' ]   |
|                   |       |   +---------------+   |       |                   |
|                   | write |                       |       |                   |
| f.write("Hello")  | ----> |   [ OS RAM Buffer ]   |       |                   |
|                   |       |         |             |       |                   |
|                   | close |         v (Flush)     |       |                   |
| f.close()         | ----> |   Write to Disk!      | ----> | [ "Hello" ]       |
+-------------------+       +-----------------------+       +-------------------+
```
*Notice the OS Buffer: Writing to a file doesn't immediately write to disk. The OS groups writes together for efficiency. Calling `close()` (or using `with`) guarantees the buffer is flushed to the actual physical disk.*

## H. Formal Explanation
In Python, the `open()` built-in function requests the OS to open a file and returns an `io.TextIOWrapper` (or `io.BufferedReader` for binary) object. This object contains a file descriptor (an integer identifying the open file in the OS kernel). Because open files consume OS resources and hold locks, they must be closed. 
Python introduced the `with` statement (Context Managers) via PEP 343. A Context Manager is any object that implements the `__enter__()` and `__exit__()` magic methods. When `with open(...) as f:` is used, `f.__enter__()` returns the file object, and `f.__exit__()` is guaranteed to be called when the block ends (even if an exception is raised), which safely invokes `f.close()`.

## I. Mathematical Foundation (if applicable)
While not strictly mathematical, file handling relies on Big-O space complexity optimizations.
- `f.read()` loads the entire file into RAM. Space Complexity: O(N) where N is file size.
- `for line in f:` creates an iterator yielding one line at a time. Space Complexity: O(1) per line.
When dealing with Gigabytes of data in AI, O(1) space complexity via lazy evaluation (generators/iterators) is mathematically mandatory to avoid Out Of Memory (OOM) errors.

## J. From-Scratch Implementation (if applicable)
(See code below)

## K. Library / Production Implementation (if applicable)
In production, while built-in file handling works perfectly, large-scale data manipulation often relies on optimized libraries. For structured data, `pandas` and `polars` manage CSVs or DataFrames, and big data often uses Parquet files via `pyarrow` or `fastparquet` for columnar storage optimizations.

## L. Trace (walk through example)
Let's trace `with open('data.txt', 'w') as f: f.write('hi')`:
1. **`open(...)`** is called. Python asks the OS to open 'data.txt'.
2. The OS checks permissions, creates the file, and gives Python a File Descriptor (e.g., ID 5).
3. The `with` statement calls `__enter__` on the file object, assigning it to the variable `f`.
4. **`f.write('hi')`** is executed. The string 'hi' is sent to the OS memory buffer, NOT immediately to the hard drive.
5. The indented block ends.
6. The `with` statement automatically calls `f.__exit__()`.
7. `f.__exit__()` calls `f.close()`.
8. Python tells the OS to close File Descriptor 5.
9. The OS says "Wait, I have 'hi' in my buffer!" and physically flushes (writes) 'hi' to the hard drive.
10. The file is locked, closed, and saved.

## M. Complexity
- **Time Complexity:** I/O Operations are notoriously slow. Reading a file from an SSD takes ~milliseconds, which is 100,000x slower than reading from RAM (nanoseconds).
- **Space/Memory Complexity:**
    - `content = f.read()`: O(N) Space. If the file is 10GB, you consume 10GB of RAM. Your program will crash on a standard laptop.
    - `for line in f:`: O(1) Space. You only hold a single line of text in memory at any given nanosecond. You can process a 100GB file on a laptop with 8GB of RAM.

## N. Common Mistakes
1. **Forgetting `encoding='utf-8'`**: If you omit this, Windows uses `cp1252` and Mac/Linux uses `utf-8`. Your code will work on your Mac, but crash with `UnicodeDecodeError` on your teammate's Windows machine.
2. **Not using `with`**: Opening a file with `f = open()` and forgetting `f.close()`. This leads to resource leaks and locked files (you try to delete the file later and Windows says "File is open in another program").
3. **Forgetting `newline=''` for CSVs**: Leads to double-spacing in CSV files on Windows.
4. **Using `readlines()` instead of iteration**: `f.readlines()` reads the entire file into a list of strings in RAM (O(N) memory). Don't use it for large files.

## O. Common Confusions
- **`'w'` vs `'a'`**: `'w'` completely deletes everything in the file before writing. `'a'` leaves existing content alone and adds to the bottom.
- **`json.load()` vs `json.loads()`**: 
  - `load()` (no s): Reads directly from a **file**.
  - `loads()` (with s): Reads from a **string** already in memory.
- **`os.path` vs `pathlib`**: `pathlib` is the modern, object-oriented way to handle paths in Python 3. `os.path` is the legacy string-based way. Prefer `pathlib.Path`.

## P. When To Use
- Saving configuration settings (JSON/YAML).
- Logging system events (Text/CSV).
- Storing/Loading Machine Learning datasets.
- Saving ML model weights and checkpoints.

## Q. When NOT To Use
- **High Concurrency**: If 100 users are trying to write to the same text file simultaneously, it will corrupt. Use a Database (PostgreSQL, SQLite) instead.
- **Relational Data**: If you have Complex data querying needs ("Get all users older than 30 who live in NY"), parsing a CSV every time is slow. Use SQL.

## R. Trade-offs
- **In-memory Processing vs. Streaming**: Reading entire files into memory is faster but memory-bound. Streaming (line-by-line) is slightly slower due to I/O overhead per iteration but is highly memory-efficient and scalable to infinite file sizes.

## S. Debugging
- **`FileNotFoundError`**: You opened a file in `'r'` mode but it doesn't exist. Fix: Check your file path, or use `Path(filepath).exists()` to check beforehand.
- **`PermissionError`**: You tried to write to a file that is read-only, or open in another program (like Excel). Fix: Close the file in Excel, or check OS permissions.
- **`UnicodeDecodeError`**: You tried to read a file with the wrong encoding. Fix: Explicitly specify `encoding='utf-8'` in `open()`.

## T. Memory Hook
"Always WITH a file, to keep the memory light. 
Loop line-by-line, and set utf-8 to read it right."

## U. Active Recall
1. Why is the `with` statement required for professional Python file handling?
2. What is the Big-O space complexity of `f.read()` vs `for line in f:`?
3. Why must you include `encoding='utf-8'` in your `open()` function?
4. What is the difference between `json.dump()` and `json.dumps()`?

## V. Practice
**Exercise:** Write a function that takes a large log file. Count how many times the word "ERROR" appears, without loading the whole file into RAM.

**Solution:**
```python
def count_errors(log_file_path: str) -> int:
    error_count = 0
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "ERROR" in line:
                error_count += 1
    return error_count
```

## W. Interview Question
**Question:** "You are given a 50GB CSV file containing transaction logs. Your server only has 8GB of RAM. How do you find the user ID with the highest number of transactions?"
**Answer:** "I cannot use `pandas.read_csv()` or `f.read()` because O(N) space will cause an Out Of Memory (OOM) error. I will use Python's built-in `csv.reader` combined with a Context Manager (`with open(...)`) to read the file as a stream/generator. This processes the file line-by-line in O(1) space. To track the counts, I will maintain a `collections.defaultdict(int)` in RAM, mapping User ID to count. Because the number of unique users is much smaller than 50GB, the dictionary will fit perfectly in my 8GB of RAM."

## X. Project Connection
In Machine Learning:
1. **Model Checkpointing:** During a 5-day PyTorch training run, we use file I/O to save `.pt` (PyTorch) weight files to disk every epoch. If the server crashes, we use `torch.load()` (which uses file I/O under the hood) to resume.
2. **Tokenization/Vocabs:** Saving a HuggingFace tokenizer's vocabulary mappings to `vocab.json`.
3. **Data Loading:** When processing ImageNet (1.2 million images, 150GB), we don't load all images into RAM. We use file paths and open the image files batch-by-batch using lazy-loading paradigms.
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Any

# ---------------------------------------------------------
# A. Basic Text File Operations
# ---------------------------------------------------------
def text_file_operations(filepath: str) -> None:
    """Demonstrates basic file reading and writing using Context Managers."""
    
    # 1. Writing ('w' mode) - OVERWRITES the file if it exists
    # ALWAYS use encoding='utf-8'. Windows defaults to cp1252, Mac/Linux to utf-8.
    with open(filepath, mode='w', encoding='utf-8') as f:
        f.write("Line 1: AI Masterclass\n")
        f.write("Line 2: File Handling\n")
    # Block ends -> f.__exit__() called -> f.close() executed -> OS Buffer flushed to disk.

    # 2. Appending ('a' mode) - Adds to the end without deleting existing content
    with open(filepath, mode='a', encoding='utf-8') as f:
        f.write("Line 3: The magic of context managers.\n")

    # 3. Reading ('r' mode) - Reading line-by-line (O(1) memory)
    print("--- Reading File ---")
    with open(filepath, mode='r', encoding='utf-8') as f:
        # f is an iterator. We loop over it directly.
        for line_number, line in enumerate(f, start=1):
            # line includes the trailing '\n', so we use .strip() to remove it
            print(f"{line_number}: {line.strip()}")


# ---------------------------------------------------------
# B. Working with Structured Data (JSON)
# ---------------------------------------------------------
def json_operations(filepath: Path, data: Dict[str, Any]) -> Dict[str, Any]:
    """Demonstrates handling JSON, the lingua franca of web and AI APIs."""
    
    # Write JSON directly to file
    with open(filepath, mode='w', encoding='utf-8') as f:
        # json.dump (with no 's') writes directly to the file stream
        # indent=4 makes it human-readable (pretty-printed)
        json.dump(data, f, indent=4)
        
    # Read JSON directly from file
    with open(filepath, mode='r', encoding='utf-8') as f:
        # json.load reads the stream and parses it into a Python dictionary
        loaded_data = json.load(f)
        
    return loaded_data


# ---------------------------------------------------------
# C. Working with Tabular Data (CSV)
# ---------------------------------------------------------
def csv_operations(filepath: Path, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Demonstrates handling CSV files securely."""
    
    if not data:
        return []
        
    fieldnames = list(data[0].keys())
    
    # Write CSV
    # CRITICAL: Always use newline='' in Python 3 when opening CSVs.
    # Otherwise, the csv module and the OS will both add newlines, resulting in blank rows on Windows.
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
    # Read CSV
    results = []
    with open(filepath, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append(row)
            
    return results

def main() -> None:
    print("--- File Handling Basics Masterclass ---")
    
    test_dir = Path("test_data_temp")
    test_dir.mkdir(exist_ok=True)
    
    try:
        txt_file = test_dir / "lesson.txt"
        text_file_operations(str(txt_file))
        
        json_file = test_dir / "config.json"
        config_data = {"learning_rate": 0.001, "batch_size": 32, "model": "ResNet"}
        loaded_config = json_operations(json_file, config_data)
        print("\n--- JSON Read ---")
        print(f"Loaded config batch size: {loaded_config['batch_size']}")
        
        csv_file = test_dir / "dataset.csv"
        csv_data = [
            {"id": "1", "feature_a": 0.5, "label": "cat"},
            {"id": "2", "feature_a": 0.8, "label": "dog"}
        ]
        loaded_csv = csv_operations(csv_file, csv_data)
        print("\n--- CSV Read ---")
        print(f"First row label: {loaded_csv[0]['label']}")
        
        print("\nAll file handling examples executed successfully!")
        
    finally:
        # Cleanup
        for file in test_dir.iterdir():
            file.unlink()
        test_dir.rmdir()

if __name__ == "__main__":
    main()
