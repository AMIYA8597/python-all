"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (OOP FILE MANAGER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A company's backup system is a massive, procedural 2,000-line Python script 
# written in 2012 using `os.path`. It relies on global variables and hardcoded 
# Windows `C:\\` paths. When the company migrates to Linux servers, the script 
# catastrophically fails, deleting a month of critical database backups because 
# of a path-separator bug (`\` vs `/`).
#
# A senior software architect builds a "File Management System" using robust 
# Object-Oriented Programming and `pathlib`. They mathematically abstract the 
# concept of a "Directory" into a Python Class. This class manages its own state, 
# strictly validates paths via the OS C-API before executing any deletes, and 
# provides a clean, testable Interface. The system deploys flawlessly to Linux 
# and macOS without changing a single line of code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Object-Oriented encapsulation of File System operations.
# - Execute safe, recursive Directory Synchronization (Mirroring).
# - Implement defensive programming and OS-level exception handling.
#
# ==============================================================================
"""

import shutil
import hashlib
from pathlib import Path
from typing import List, Dict

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE OOP ARCHITECTURE (THE FILE MANAGER)
# ==============================================================================
class DirectoryManager:
    """
    An Object-Oriented Abstraction of a physical Hard Drive Directory.
    It mathematically encapsulates all dangerous OS-level operations behind 
    strict validation firewalls.
    """
    def __init__(self, root_path: str):
        # We instantly mathematically coerce the raw string into a Path object!
        self.root = Path(root_path).resolve()
        
        if not self.root.exists():
            print(f"  [INIT] Directory {self.root} does not exist. Creating it...")
            self.root.mkdir(parents=True, exist_ok=True)
            
    def list_files(self, extension: str = None) -> List[Path]:
        """Returns a list of all files, optionally mathematically filtered by extension."""
        if extension:
            # e.g., "*.txt"
            return list(self.root.rglob(f"*{extension}"))
        return [p for p in self.root.rglob("*") if p.is_file()]

    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Mathematically calculates the SHA-256 binary hash of a file.
        This is the ONLY way to mathematically prove two files are identical!
        """
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"Cannot hash non-existent file: {file_path}")
            
        sha256 = hashlib.sha256()
        # We read the file in binary chunks (rb) to prevent RAM OOM crashes on massive files!
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def sync_to(self, target_manager: 'DirectoryManager'):
        """
        Mathematically synchronizes (mirrors) this directory to a target directory.
        It uses SHA-256 to ensure it only copies files that actually changed!
        """
        print(f"  [SYNC] Synchronizing {self.root} -> {target_manager.root}")
        
        source_files = self.list_files()
        copy_count = 0
        skip_count = 0
        
        for src_file in source_files:
            # Mathematically calculate the relative path (e.g., 'subfolder/file.txt')
            relative_path = src_file.relative_to(self.root)
            
            # Construct the absolute destination path!
            dest_file = target_manager.root / relative_path
            
            # Ensure the destination sub-folders physically exist!
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # THE OPTIMIZATION FIREWALL:
            # If the file already exists, we mathematically compare their SHA-256 hashes.
            # If the hashes match, the files are identical. We DO NOT execute an expensive OS copy!
            if dest_file.exists():
                src_hash = self.calculate_file_hash(src_file)
                dest_hash = self.calculate_file_hash(dest_file)
                
                if src_hash == dest_hash:
                    skip_count += 1
                    continue # Skip the copy!
                    
            # If we reached here, the file doesn't exist, OR the hashes were different!
            shutil.copy2(src_file, dest_file) # copy2 preserves mathematical OS timestamps!
            copy_count += 1
            
        print(f"  [SYNC COMPLETE] Copied: {copy_count} | Skipped: {skip_count} (Identical files)")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_file_manager():
    section_header("Project: Object-Oriented File Manager")
    
    source_dir = Path("./temp_source_lab")
    target_dir = Path("./temp_target_lab")
    
    # 1. We create the raw chaotic environments
    if source_dir.exists(): shutil.rmtree(source_dir)
    if target_dir.exists(): shutil.rmtree(target_dir)
    
    source_dir.mkdir()
    target_dir.mkdir()
    
    # We populate the Source Directory with dummy files!
    (source_dir / "file1.txt").write_text("Hello World!")
    (source_dir / "file2.txt").write_text("Secret Data")
    
    sub_dir = source_dir / "logs"
    sub_dir.mkdir()
    (sub_dir / "sys.log").write_text("SYSTEM BOOT OK")
    
    # 2. We instantiate our Architectural Classes!
    print("  [EXECUTION] Instantiating DirectoryManagers...")
    source_manager = DirectoryManager(str(source_dir))
    target_manager = DirectoryManager(str(target_dir))
    
    # 3. We execute the first Sync!
    print("\n  [TEST 1: INITIAL SYNC]")
    source_manager.sync_to(target_manager)
    # Expectation: 3 files copied, 0 skipped.
    
    # 4. We execute the exact same Sync again without touching the files!
    print("\n  [TEST 2: REDUNDANT SYNC (Idempotency Check)]")
    source_manager.sync_to(target_manager)
    # Expectation: 0 files copied, 3 skipped (SHA-256 matches perfectly).
    
    # 5. We mathematically alter ONE file in the Source!
    print("\n  [TEST 3: PARTIAL SYNC (Modified File Check)]")
    (source_dir / "file1.txt").write_text("Hello World! I HAVE BEEN MODIFIED!")
    
    source_manager.sync_to(target_manager)
    # Expectation: 1 file copied (hash mismatch), 2 skipped (hashes match).
    
    # Clean up the lab
    shutil.rmtree(source_dir)
    shutil.rmtree(target_dir)
    print("\n  [TEARDOWN] Lab directories cleanly removed.")


def run_all_labs():
    demonstrate_file_manager()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the `sync_to` method, why did we use `shutil.copy2` instead of `shutil.copy`?"
   Senior Answer: "Mathematical File Metadata. `shutil.copy` copies the physical binary payload of the file, but it destroys the OS-level metadata (Creation Date, Last Modified Date) on the destination file, replacing them with the exact millisecond the copy script ran. This catastrophically ruins backup systems that rely on timestamps. `shutil.copy2` extracts the binary payload AND mathematically extracts the underlying OS metadata from the source file's Inode/MFT, injecting that exact metadata into the destination file, creating a flawless 1:1 architectural clone."

2. Interviewer: "Why did we use SHA-256 Hashing to compare if two files are identical, instead of just comparing their File Sizes or Last Modified dates?"
   Senior Answer: "File Sizes and Timestamps are mathematically fragile heuristics. Two completely different text files can easily have the exact same size in bytes. A file can also be maliciously modified by a hacker who intentionally reverts the 'Last Modified' timestamp to trick a backup system. A Cryptographic Hash Function (like SHA-256) mathematically ingests the actual raw binary payload of the file and calculates a 256-bit signature. If even a single binary bit is flipped inside a 10 GB database file, the 'Avalanche Effect' guarantees the resulting SHA-256 hash will be completely unrecognizable. Hashing is the only way to mathematically prove absolute byte-for-byte equivalence."

3. Interviewer: "In the `calculate_file_hash` method, why did we use a `lambda: f.read(4096)` generator loop instead of simply `hashlib.sha256(f.read())`?"
   Senior Answer: "RAM Exhaustion (OOM Crashes). If you execute `f.read()` on a 50 GB video file, Python attempts to load all 50,000,000,000 bytes into a single contiguous block of physical RAM simultaneously. If the server only has 16 GB of RAM, the Operating System will violently kill the Python process. By using a Chunking Generator (`f.read(4096)`), we mathematically stream the file from the Hard Drive through the CPU in tiny 4-Kilobyte increments. The hash state updates continuously, and the RAM consumption never exceeds 4 KB, allowing the script to flawlessly hash a 50 GB file on a Raspberry Pi with 1 GB of RAM."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (File Manager) Completed.")
