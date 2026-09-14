"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (AUTOMATION & FILE SYSTEMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A massive corporation downloads 10,000 messy files every day into a single 
# 'Downloads' folder. A junior engineer tries to clean it up using the legacy 
# `os.path` module. They manually concatenate strings `folder + "/" + file`, 
# run the script on a Windows server, and catastrophically crash the system 
# because Windows uses `\` instead of `/`.
#
# A senior engineer uses modern Python `pathlib`. They mathematically abstract 
# the file system into Object-Oriented Nodes. They write a 10-line script that 
# recursively scans the 10,000 files, reads their binary signatures or extensions, 
# and organizes them into perfectly structured Sub-Directories in 0.5 seconds, 
# running flawlessly on Linux, macOS, and Windows without changing a single line 
# of code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Object-Oriented File System paths using `pathlib`.
# - Execute advanced file operations (moving, copying, deleting) using `shutil`.
# - Master recursive directory traversal (Globbing).
#
# ==============================================================================
"""

import os
import shutil
import timeit
from pathlib import Path

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PREPARING THE CHAOS (THE TEST ENVIRONMENT)
# ==============================================================================
def create_chaotic_directory(base_path: Path):
    """Generates a massive, unorganized folder to simulate the real world."""
    print(f"  [INIT] Generating Chaos Directory at: {base_path}")
    
    # We ensure a clean slate!
    if base_path.exists():
        shutil.rmtree(base_path)
        
    base_path.mkdir(parents=True, exist_ok=True)
    
    # We generate 1,000 dummy files of various types
    extensions = ['.jpg', '.png', '.pdf', '.docx', '.csv', '.py', '.txt', '.mp4']
    for i in range(100):
        for ext in extensions:
            # We construct the path using pathlib's `/` operator (which works on Windows too!)
            file_path = base_path / f"file_{i}{ext}"
            file_path.touch() # Physically creates an empty file on the hard drive
            
    print(f"    -> Generated {len(extensions) * 100} chaotic files.")


# ==============================================================================
# 4. THE PATHLIB ABSTRACTION
# ==============================================================================
def demonstrate_pathlib_features():
    section_header("Object-Oriented Paths (pathlib)")
    
    print("  [SCENARIO] Analyzing a specific file path.")
    
    # We define a path. Note: this file doesn't actually have to exist yet!
    # The `/` operator has been mathematically overloaded in the `Path` class
    # to handle OS-specific path joining automatically!
    p = Path("/usr/local") / "bin" / "script.py"
    
    print(f"\n  [THE PATH OBJECT] {p}")
    print(f"    -> Name:   {p.name}")      # script.py
    print(f"    -> Stem:   {p.stem}")      # script (no extension)
    print(f"    -> Suffix: {p.suffix}")    # .py
    print(f"    -> Parent: {p.parent}")    # /usr/local/bin
    
    # To check if it physically exists on the hard drive:
    print(f"    -> Exists on Disk? {p.exists()}")


# ==============================================================================
# 5. THE AUTOMATION SCRIPT (THE CLEANUP)
# ==============================================================================
def automate_directory_cleanup(base_path: Path):
    section_header("Automation Execution: Directory Cleanup")
    
    print("  [EXECUTION] Commencing File System Analysis...")
    start_time = timeit.default_timer()
    
    # 1. We mathematically define our target folders based on extensions!
    CATEGORIES = {
        "Images": ['.jpg', '.jpeg', '.png', '.gif'],
        "Documents": ['.pdf', '.docx', '.txt'],
        "Data": ['.csv', '.xlsx', '.json'],
        "Code": ['.py', '.js', '.html'],
        "Media": ['.mp4', '.mp3']
    }
    
    # 2. We dynamically create the sub-directories!
    for folder_name in CATEGORIES.keys():
        target_dir = base_path / folder_name
        target_dir.mkdir(exist_ok=True)
        
    # 3. We recursively scan the directory!
    # `rglob("*")` is a generator that recursively finds every file and folder.
    # It evaluates lazily, so it won't crash RAM if there are 1,000,000 files!
    move_count = 0
    for file_path in base_path.rglob("*"):
        # We mathematically skip directories (we only want files)
        if file_path.is_dir():
            continue
            
        ext = file_path.suffix.lower()
        
        # We determine the destination!
        destination_folder = base_path / "Others"
        for category, extensions in CATEGORIES.items():
            if ext in extensions:
                destination_folder = base_path / category
                break
                
        # Ensure the 'Others' folder exists if needed
        destination_folder.mkdir(exist_ok=True)
        
        # 4. The physical Move operation!
        # We construct the final target path: base/Images/file_1.jpg
        target_path = destination_folder / file_path.name
        
        # We execute an OS-level atomic move!
        shutil.move(str(file_path), str(target_path))
        move_count += 1
        
    end_time = timeit.default_timer()
    print(f"\n  [SUCCESS] Organized {move_count} files into {len(CATEGORIES) + 1} specific folders.")
    print(f"  [METRICS] Execution Time: {end_time - start_time:.4f} seconds.")
    
    print("\n  [VERIFICATION] Reading the final directory structure:")
    for folder in base_path.iterdir():
        if folder.is_dir():
            # Count the files inside
            file_count = len(list(folder.glob("*")))
            print(f"    -> [DIR] {folder.name:<15} ({file_count} files)")


def run_all_labs():
    # We use a temporary directory for the lab
    lab_dir = Path("./temp_automation_lab")
    
    create_chaotic_directory(lab_dir)
    demonstrate_pathlib_features()
    automate_directory_cleanup(lab_dir)
    
    # Clean up after the lab is done!
    shutil.rmtree(lab_dir)
    print("\n  [TEARDOWN] Lab directory cleanly removed from the hard drive.")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why should we completely abandon the legacy `os.path` module and strictly use `pathlib` for all modern Python development?"
   Senior Answer: "`os.path` mathematically treats file paths as dumb Strings. If you write `path = folder + '/' + file`, you instantly create an OS-level bug. Linux uses `/`, Windows uses `\\`. You are forced to write `os.path.join(folder, file)` everywhere, resulting in dense, unreadable code. `pathlib` mathematically abstracts the file system into an Object-Oriented Interface. By simply writing `path = folder / file`, `pathlib` intercepts the division operator via the `__truediv__` dunder method, checks the underlying Operating System via the C-API, and automatically constructs a flawless `WindowsPath` or `PosixPath` object. It provides immediate property access (`.suffix`, `.parent`) without requiring string slicing."

2. Interviewer: "What is the architectural difference between `os.listdir()` and `pathlib.Path.rglob()` when analyzing massive directories?"
   Senior Answer: "`os.listdir()` is 'Shallow and Eager'. It only returns the files in the immediate directory, and it instantly physically loads all string names into a Python List in RAM. If a directory has $1,000,000$ files, it causes a massive RAM spike and latency halt. `pathlib.Path.rglob('*')` is 'Deep and Lazy'. The `r` stands for recursive, meaning it mathematically traverses all sub-directories infinitely deep. More importantly, it returns a Python Generator. It yields exactly one `Path` object at a time, keeping RAM consumption near $0.0$ bytes regardless of how massive the server's hard drive is."

3. Interviewer: "What is the difference between `shutil.move(src, dst)` and `shutil.copy(src, dst)`, and why is moving infinitely faster than copying on the same hard drive?"
   Senior Answer: "When you `copy` a file, the OS must physically allocate new magnetic sectors on the hard drive, read the binary payload of the original file into RAM, and write it to the new sectors. A $5$ GB file takes several seconds to copy. When you `move` a file *within the same physical hard drive partition*, the OS does not touch the $5$ GB binary payload at all. It simply executes a mathematical $O(1)$ update to the Master File Table (MFT) or Inode Table, pointing the new file name to the exact same physical magnetic sectors. Moving a $5$ GB file takes $0.001$ seconds because no actual data is moved, only the architectural pointer."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Automation (File Systems) Completed.")
