"""
# ==============================================================================
# COMPETITIVE PROGRAMMING: LOCAL DEBUGGING TEMPLATE
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When your code fails a test case in Codeforces, your instinct is to add 
# `print(my_array)` in the middle of your loops to see what went wrong.
#
# DO NOT DO THIS!
#
# Codeforces and HackerRank read your EXACT `stdout` to verify the answer. 
# If you leave `print(my_array)` in your code when you hit Submit, the Judge 
# will read your debug output as part of your official answer, and immediately 
# fail you with a "Wrong Answer" (WA) error.
#
# You need a Debug Protocol that perfectly isolates Debug information from 
# Official Output, and automatically disables itself when running on the 
# Judge's server!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand `sys.stderr` vs `sys.stdout`.
# - Implement a Local Debugger snippet.
#
# ==============================================================================
"""

import sys
import os

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE STANDARD ERROR (STDERR) PROTOCOL
# ==============================================================================
def demonstrate_stderr():
    section_header("Using sys.stderr for Safe Debugging")
    
    print("Every terminal has two output streams:")
    print("1. Standard Output (stdout): Where your official answers go.")
    print("2. Standard Error (stderr): Where crash logs and debug info go.")
    
    print("\nIf you print to `stderr`, it will show up on your local screen, ")
    print("but the Codeforces grading bot will completely IGNORE IT!")
    
    # Writing to stderr
    sys.stderr.write("[DEBUG] This is invisible to the Codeforces grading bot!\n")
    
    # You can also use the print function's file parameter!
    print("[DEBUG] The array is currently: [1, 2, 3]", file=sys.stderr)


# ==============================================================================
# 4. THE AUTO-DISABLING DEBUG SNIPPET
# ==============================================================================
def demonstrate_auto_debugger():
    section_header("The Auto-Disabling Debugger")
    
    print("Writing `file=sys.stderr` 100 times is annoying.")
    print("Instead, we create a global `debug()` function.")
    print("Even better, we configure it to ONLY run on your local laptop, ")
    print("and automatically turn itself off when submitted to LeetCode!\n")
    
    print("```python")
    print("import sys")
    print("import os")
    
    print("\n# Check if we are running locally by looking for a custom environment variable,")
    print("# or checking if the script is running in an interactive terminal.")
    print("# Online judges do not run in interactive TTY terminals.")
    print("LOCAL_DEV = sys.stdout.isatty() or os.environ.get('CP_LOCAL') == '1'")
    
    print("\ndef dbg(*args, **kwargs):")
    print("    if LOCAL_DEV:")
    print("        # Force the print to go to stderr")
    print("        print('[DEBUG]', *args, file=sys.stderr, **kwargs)")
    print("    # If running on the judge server, this function instantly returns,")
    print("    # costing zero I/O overhead!")
    
    print("\n# Example Usage:")
    print("def solve():")
    print("    arr = [5, 2, 9]")
    print("    dbg('Initial Array:', arr)  # Prints locally, ignored on Server")
    print("    arr.sort()")
    print("    dbg('Sorted Array:', arr)   # Prints locally, ignored on Server")
    print("    print(arr[0])               # Official stdout answer!")
    print("```")
    
    print("\nBy injecting this snippet into your Master Template, you never have ")
    print("to manually delete your debug print statements before clicking Submit again!")


def run_all_labs():
    demonstrate_stderr()
    demonstrate_auto_debugger()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a standard `print("DEBUG: arr is empty")` cause a "Wrong Answer" (WA) on Competitive Programming platforms?
   Answer: Online Judges do not physically read your code to see if it is correct. They run your code and pipe the `Standard Output` (stdout) stream into a text file, and then compare that text file character-by-character against the official answer key text file. If the answer key says `42`, but your program outputs `DEBUG: arr is empty\n42`, the text files do not match. The judge instantly fails you for a Wrong Answer.

2. How does `print(..., file=sys.stderr)` bypass the grading bot?
   Answer: The Operating System maintains completely separate data streams for normal output (`stdout`) and diagnostic output (`stderr`). The grading bot is explicitly configured to pipe and read *only* the `stdout` stream to check your answer. When you redirect your print statement to `sys.stderr`, the bytes travel through a completely different pipeline. The data will still render on your physical computer monitor (because the terminal merges both streams for human viewing), but the grading bot's automated text-matcher will never see it, keeping your official `stdout` stream perfectly clean!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Debugging Template Completed.")
