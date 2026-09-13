\"\"\"
File Automation Scripts Fundamentals

What is File Automation?
File automation refers to writing scripts that programmatically interact with the 
operating system's file system to create, read, update, move, delete, or organize files 
and directories. Industry use cases include log rotation, data ingestion pipelines, 
batch renaming, archiving backups, and ETL (Extract, Transform, Load) tasks.

Learning Objectives:
1. Understand the difference between the `os` module and the modern `pathlib` module.
2. Implement basic file operations (reading, writing, appending).
3. Build a professional-grade automated directory organizer using OOP and robust error handling.
4. Learn how to handle large files, permissions, and cross-platform path issues.

Concept Explanation:
An operating system organizes data hierarchically in directories (folders) and files. 
Scripts interact with this system via System Calls. Abstracting these system calls, Python 
provides standard libraries (`os`, `shutil`, `pathlib`) that allow you to traverse this 
hierarchy, modify metadata (timestamps, permissions), and manipulate data streams.

Beginner Explanation:
Think of your computer's files like a massive physical filing cabinet. Doing things by hand 
(clicking, dragging, renaming) takes forever. File automation is like hiring a robotic assistant 
who can instantly sort thousands of documents into the right folders based on a set of rules you define.

Advanced Explanation:
At the OS level, files are represented by file descriptors. When automating file operations, 
one must consider file locks, race conditions (if multiple processes access the same file), 
and disk I/O bottlenecks. Professional scripts use buffered reading/writing, asynchronous I/O 
for high concurrency, and atomic operations (like atomic renames) to prevent data corruption 
during unexpected crashes.

Performance Considerations:
- Memory: Never read a multi-gigabyte file entirely into memory using `.read()`. Use generators 
  or read line-by-line using `for line in file:`.
- I/O Bound: Disk operations are slow. Batch operations where possible.

Security Concerns:
- Path Traversal: If your script takes filenames from user input, a malicious user could pass 
  `../../etc/passwd` to access unauthorized files. Always validate and sanitize paths.
- Permissions: Avoid running automation scripts as `root` or Administrator unless absolutely necessary.
\"\"\"

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------------------------------------------------
# Basic Implementation
# ---------------------------------------------------------

def basic_file_writer_and_reader(filename: str, content: str) -> None:
    \"\"\"
    A basic procedural function to write content to a file and read it back.
    Uses the older but ubiquitous built-in open() paradigm.
    \"\"\"
    print(\"--- Running Basic File Ops ---\")
    
    # Write to file (w mode overwrites)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f\"Wrote content to {filename}\")
        
    # Read from file
    with open(filename, 'r', encoding='utf-8') as f:
        read_content = f.read()
        print(f\"Read from {filename}: {read_content}\")

# ---------------------------------------------------------
# Professional Implementation
# ---------------------------------------------------------

class DirectoryOrganizer:
    \"\"\"
    A professional-grade class designed to organize files in a directory based on their extensions.
    Uses the modern `pathlib` and robust error handling.
    \"\"\"
    
    # Mapping of category names to their respective file extensions
    DEFAULT_MAPPING: Dict[str, List[str]] = {
        \"Images\": [\".jpg\", \".jpeg\", \".png\", \".gif\", \".svg\"],
        \"Documents\": [\".pdf\", \".docx\", \".txt\", \".xlsx\", \".csv\", \".md\"],
        \"Audio\": [\".mp3\", \".wav\", \".flac\"],
        \"Video\": [\".mp4\", \".mkv\", \".avi\"],
        \"Code\": [\".py\", \".js\", \".html\", \".css\", \".json\", \".cpp\"],
        \"Archives\": [\".zip\", \".tar\", \".gz\", \".rar\"]
    }

    def __init__(self, target_directory: str, extension_mapping: Optional[Dict[str, List[str]]] = None):
        \"\"\"
        Initializes the organizer.
        
        Args:
            target_directory (str): The directory to organize.
            extension_mapping: Custom mapping of Folder Name -> List of extensions.
        \"\"\"
        self.target_dir = Path(target_directory).resolve()
        self.mapping = extension_mapping or self.DEFAULT_MAPPING
        
        # Invert the mapping for O(1) lookups: {'.pdf': 'Documents', '.jpg': 'Images'}
        self.ext_to_folder: Dict[str, str] = {}
        for folder, extensions in self.mapping.items():
            for ext in extensions:
                self.ext_to_folder[ext.lower()] = folder

        if not self.target_dir.exists():
            raise FileNotFoundError(f\"Target directory does not exist: {self.target_dir}\")
        if not self.target_dir.is_dir():
            raise NotADirectoryError(f\"Target path is not a directory: {self.target_dir}\")

    def organize(self) -> Dict[str, int]:
        \"\"\"
        Iterates through the target directory and moves files into categorized subfolders.
        
        Returns:
            Dict[str, int]: A summary of how many files were moved into each category.
        \"\"\"
        logging.info(f\"Starting organization of {self.target_dir}\")
        stats: Dict[str, int] = {folder: 0 for folder in self.mapping.keys()}
        stats[\"Others\"] = 0
        
        # Iterate over all items in the directory
        for item in self.target_dir.iterdir():
            if item.is_file():
                # Extract the extension (e.g., '.txt')
                ext = item.suffix.lower()
                
                # Determine destination folder name
                folder_name = self.ext_to_folder.get(ext, \"Others\")
                
                # Create destination path
                dest_dir = self.target_dir / folder_name
                
                try:
                    # Create the folder if it doesn't exist
                    dest_dir.mkdir(exist_ok=True)
                    
                    # Define the final path for the file
                    dest_file = dest_dir / item.name
                    
                    # Handle name collisions (if a file with the same name already exists in the dest)
                    if dest_file.exists():
                        timestamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")
                        new_name = f\"{item.stem}_{timestamp}{item.suffix}\"
                        dest_file = dest_dir / new_name
                    
                    # Move the file
                    shutil.move(str(item), str(dest_file))
                    stats[folder_name] += 1
                    logging.debug(f\"Moved {item.name} -> {folder_name}/\")
                    
                except PermissionError:
                    logging.error(f\"Permission denied to move {item.name}. Skipping.\")
                except Exception as e:
                    logging.error(f\"Unexpected error moving {item.name}: {e}. Skipping.\")
                    
        logging.info(f\"Organization complete. Stats: {stats}\")
        return stats


# ---------------------------------------------------------
# Complexity Analysis & Interview Challenge
# ---------------------------------------------------------
\"\"\"
Complexity Analysis (DirectoryOrganizer.organize):
- Time Complexity: O(N) where N is the number of files in the directory. Dictionary lookup for 
  the extension is O(1). Moving the file is dependent on the OS and filesystem, but generally O(1) 
  if moving within the same drive (it just updates the file index pointer).
- Space Complexity: O(1) additional space (or O(E) where E is the number of extensions in the mapping).

Interview Challenge:
Question: You need to write a script that deletes files older than 30 days in a log directory. 
The directory contains over 10 million files. If you use `os.listdir()`, the script crashes due to Out-Of-Memory (OOM). 
How do you solve this?

Answer Guide:
1. Issue: `os.listdir()` loads all 10 million filenames into a Python list in memory at once.
2. Solution: Use `os.scandir()` (or `pathlib.Path.iterdir()`), which returns an iterator. It yields 
   directory entries one by one without loading the entire list into memory.
3. Bonus: `os.scandir()` also caches file metadata (like timestamps), saving you from making a 
   separate `os.stat()` system call for every single file, massively speeding up execution time.
\"\"\"

# ---------------------------------------------------------
# Example Usage and Tests (Main Guard)
# ---------------------------------------------------------
if __name__ == \"__main__\":
    print(\"\\n=== File Automation App Execution ===\")
    
    # 1. Test Basic implementation
    test_file = \"basic_test_doc.txt\"
    basic_file_writer_and_reader(test_file, \"Hello, Automated World!\")
    
    # 2. Setup a dummy environment for the Professional implementation
    test_dir = Path(\"dummy_sort_dir\")
    test_dir.mkdir(exist_ok=True)
    
    # Create some dummy files to sort
    (test_dir / \"image1.jpg\").touch()
    (test_dir / \"image2.png\").touch()
    (test_dir / \"report.pdf\").touch()
    (test_dir / \"script.py\").touch()
    (test_dir / \"unknown_file.xyz\").touch()
    
    print(\"\\n--- Professional Directory Organizer ---\")
    try:
        organizer = DirectoryOrganizer(str(test_dir))
        stats = organizer.organize()
        
        # Assertions to ensure functionality
        assert stats[\"Images\"] == 2, \"Should have moved 2 images.\"
        assert stats[\"Documents\"] == 1, \"Should have moved 1 document.\"
        assert stats[\"Code\"] == 1, \"Should have moved 1 code file.\"
        assert stats[\"Others\"] == 1, \"Should have moved 1 unknown file to 'Others'.\"
        
        assert (test_dir / \"Images\" / \"image1.jpg\").exists(), \"File not correctly placed.\"
        assert (test_dir / \"Others\" / \"unknown_file.xyz\").exists(), \"Unknown file not handled.\"
        
        print(\"All assertions passed successfully! Directory Organizer works.\")
        
    finally:
        # Cleanup: Remove the dummy files and directories recursively
        if os.path.exists(test_file):
            os.remove(test_file)
            
        if test_dir.exists():
            shutil.rmtree(str(test_dir))
            print(\"Cleaned up dummy files.\")

    print(\"=== Execution Complete ===\")
