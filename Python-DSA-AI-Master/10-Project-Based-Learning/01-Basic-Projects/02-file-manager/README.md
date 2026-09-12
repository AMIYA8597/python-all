# File Manager Project Specification

## 1. What is this and why does it exist?
The File Manager project is a command-line utility for organizing, navigating, and manipulating the file system programmatically. 

In the software industry, tasks involving file manipulation—such as parsing logs, organizing incoming data dumps, data engineering pipelines, or automated deployment scripts—rely heavily on robust file system interaction. Building a file manager from scratch provides hands-on experience with operating system interfaces (OS modules), exception handling (missing files, permission errors), and data persistence.

## 2. Educational Explanations

### Beginner Explanation
Think of Windows Explorer or macOS Finder. You click on folders to open them, copy files, and delete things you don't need. This project builds a text-based version of that. Instead of clicking, you type commands like `copy file.txt new_folder/`. We use Python's built-in libraries to talk to the operating system and ask it to move data around on the hard drive.

### Deep Technical Explanation
Python provides multiple ways to interact with the file system. Historically, the `os` and `os.path` modules were used. Modern Python (3.4+) introduced `pathlib`, which provides an object-oriented interface for paths. This project leverages `pathlib` for path manipulations and `shutil` for high-level operations like copying directory trees.

A robust file manager must handle various edge cases:
- Race conditions (Time-of-check to time-of-use, TOCTOU) where a file is deleted between checking its existence and opening it.
- Symlinks and recursive directory loops.
- File lock issues (on Windows) or insufficient permissions (POSIX/Windows).

## 3. Project Requirements & Specifications

### Features
1. **List Directory Contents (`ls`):** Display files and directories, file sizes, and modification dates.
2. **Change Directory (`cd`):** Navigate to different absolute or relative paths.
3. **Copy (`cp`):** Copy files or entire directories.
4. **Move/Rename (`mv`):** Move files or directories, or rename them in place.
5. **Delete (`rm`):** Safely delete files or directories.
6. **Search (`find`):** Recursively search for files matching a pattern or extension.

### Constraints
- Must use `pathlib` exclusively for path representations (no string concatenation for paths).
- Must use Python's `logging` module to track operations and errors, rather than `print` for system logs.
- Provide a clean, robust Object-Oriented architecture.

## 4. Common Mistakes & Considerations
- **String Concatenation for Paths:** Using `path + "/" + filename` is a critical error. It fails cross-platform. Always use `pathlib.Path(path) / filename` or `os.path.join()`.
- **Silent Failures:** Failing to catch `PermissionError` or `FileNotFoundError` will crash the application unexpectedly. 
- **Destructive Actions:** Ensure destructive actions (like deleting directories) have safeguards or prompt for confirmation if they are interactive.
- **Large Directories:** Listing a directory with 100,000 files using a blocking call can freeze the app. Using `os.scandir()` or `pathlib.Path.iterdir()` provides iterators which are more memory efficient.

## 5. Security Concerns
- **Directory Traversal:** If this file manager is ever hooked up to a web interface, user inputs like `../../etc/passwd` could expose sensitive system files. Always resolve and validate paths against a restricted "jail" directory if handling untrusted input.
- **Execution of Untrusted Files:** Do not automatically execute or open files with external programs without validation.

## 6. Interview Questions
1. What is the difference between `os.path` and `pathlib`? Which do you prefer and why?
2. Explain a Time-of-check to time-of-use (TOCTOU) bug in the context of file deletion.
3. How would you handle searching for a file in a deeply nested directory structure with millions of files without running out of memory?

## 7. Practical Exercises
- **Exercise 1:** Implement a feature to calculate the total size of a directory recursively.
- **Exercise 2:** Add a 'dry-run' mode that logs what *would* be deleted or moved, without actually performing the operation.
- **Exercise 3:** Implement an auto-organizer feature that looks at a directory (like Downloads) and moves files into subdirectories based on their extensions (`.jpg` to `Images/`, `.pdf` to `Documents/`).
