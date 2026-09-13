"""
# ==============================================================================
# LABORATORY 08: FILE HANDLING & CONTEXT MANAGERS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When Python opens a file, it requests a File Descriptor from the Operating 
# System. If a script opens many files without closing them, the OS runs out of 
# descriptors and crashes (Resource Leak). Understanding how the `with` statement 
# guarantees cleanup (even if an exception occurs) is critical for production code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master reading and writing files (Modes: r, w, a, x, b).
# - Understand the `with` statement and Context Managers.
# - Differentiate between reading lines, reading chunks, and reading all into memory.
# - Master string encodings when dealing with files (`utf-8`).
# - Transition from `os.path` to the modern `pathlib` module.
#
# ==============================================================================
"""

import os
import sys
from pathlib import Path

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# Helper filename
TEST_FILE = "lab08_dummy.txt"

# ==============================================================================
# 3. TRADITIONAL VS CONTEXT MANAGER FILE HANDLING
# ==============================================================================
def demonstrate_context_manager():
    """
    The old way: f = open(); f.read(); f.close()
    The modern way: with open() as f: f.read()
    """
    section_header("File Handling & The `with` Statement")
    
    # 1. THE DANGEROUS WAY (Manual cleanup)
    # If an exception occurs during write, f.close() is never hit!
    print("Writing file the dangerous way...")
    f = open(TEST_FILE, "w", encoding="utf-8")
    try:
        f.write("Line 1: Hello World\n")
        f.write("Line 2: Manual cleanup is risky.\n")
    finally:
        # We MUST use a finally block to guarantee closure in the manual way
        f.close() 

    # 2. THE IDIOMATIC WAY (Context Managers)
    # The `with` statement guarantees that f.close() is called automatically
    # as soon as the block exits, even if a massive crash happens inside.
    print("Appending file the idiomatic way (with statement)...")
    with open(TEST_FILE, "a", encoding="utf-8") as f:
        f.write("Line 3: Context managers are safe.\n")
        
    print("\nFile written successfully.")


# ==============================================================================
# 4. READING MODES & MEMORY TRAPS
# ==============================================================================
def demonstrate_reading():
    """
    Reading a 10GB file into RAM with `f.read()` will crash your server (OOM).
    You must iterate over the file line-by-line.
    """
    section_header("Reading & Memory Considerations")
    
    print("--- 1. read() [DANGER FOR LARGE FILES] ---")
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        content = f.read()  # Loads entire file into a single string in RAM
        print(f"Read {len(content)} bytes total.")
        
    print("\n--- 2. readlines() [DANGER FOR LARGE FILES] ---")
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines() # Loads entire file into a LIST of strings in RAM
        print(f"Read {len(lines)} lines total.")

    print("\n--- 3. Iterating the file object [SAFE FOR BIG DATA] ---")
    with open(TEST_FILE, "r", encoding="utf-8") as f:
        # A file object is an ITERATOR. It yields one line at a time.
        # This uses almost zero RAM, even for a 10GB file!
        for i, line in enumerate(f):
            # line still contains the trailing \n character
            clean_line = line.strip() 
            print(f"Processing line {i+1}: {clean_line}")


# ==============================================================================
# 5. ENCODING TRAPS
# ==============================================================================
def demonstrate_encoding():
    """
    If you don't specify `encoding="utf-8"`, Python uses the system default.
    On Mac/Linux, this is usually utf-8. 
    On Windows, this is often cp1252! 
    This means code works locally on Windows but crashes on a Linux server.
    ALWAYS SPECIFY ENCODING!
    """
    section_header("The Encoding Trap")
    
    emoji_file = "lab08_emoji.txt"
    text = "Data Science is 🔥"
    
    # 1. Write forcing utf-8
    with open(emoji_file, "w", encoding="utf-8") as f:
        f.write(text)
        
    # 2. If we read it correctly
    with open(emoji_file, "r", encoding="utf-8") as f:
        print("Successful utf-8 read:", f.read())
        
    # Cleanup
    if os.path.exists(emoji_file):
        os.remove(emoji_file)


# ==============================================================================
# 6. MODERN PATHLIB VS LEGACY OS.PATH
# ==============================================================================
def demonstrate_pathlib():
    """
    os.path operates on strings.
    pathlib (Python 3.4+) operates on Path objects using the `/` operator.
    """
    section_header("Pathlib: Modern File Paths")
    
    # Legacy way (String concatenation / os.path.join)
    current_dir_str = os.getcwd()
    legacy_path = os.path.join(current_dir_str, "data", "report.csv")
    print(f"Legacy os.path : {legacy_path}")
    
    # Modern way (Object-Oriented)
    current_dir = Path.cwd()
    
    # Pathlib uses the `/` operator heavily overloaded for path joining
    modern_path = current_dir / "data" / "report.csv"
    print(f"Modern Pathlib : {modern_path}")
    
    # Pathlib is extremely powerful for extracting components
    print(f"\nPathname : {modern_path.name}")
    print(f"Suffix   : {modern_path.suffix}")
    print(f"Parent   : {modern_path.parent}")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why should you always use `with open(...) as f:` instead of `f = open(...)`?
   Answer: The `with` statement creates a context manager that guarantees the file descriptor is closed when the block exits, even if an exception is thrown inside the block. This prevents OS resource leaks.

2. How do you read a 50GB log file in Python without running out of memory (OOM)?
   Answer: You iterate over the file object directly: `for line in f:`. This yields one line at a time into memory, rather than loading the whole file like `f.read()` or `f.readlines()` does.

3. Why is it a bug to omit `encoding="utf-8"` in `open()`?
   Answer: If omitted, Python relies on the OS default encoding. Windows might use cp1252, while Linux uses utf-8. This leads to cross-platform UnicodeDecodeErrors.

4. What is `pathlib` and why is it preferred over `os.path`?
   Answer: `pathlib` treats file paths as objects rather than strings, allowing intuitive concatenation with the `/` operator and easy extraction of extensions, names, and parent directories.
"""

if __name__ == "__main__":
    demonstrate_context_manager()
    demonstrate_reading()
    demonstrate_encoding()
    demonstrate_pathlib()
    
    # Final cleanup
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
        
    print("\n[SUCCESS] Laboratory 08 Completed.")
