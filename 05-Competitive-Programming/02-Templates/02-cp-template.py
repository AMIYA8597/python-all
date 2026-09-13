"""
# ==============================================================================
# COMPETITIVE PROGRAMMING: THE ULTIMATE MASTER TEMPLATE
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When the contest clock starts, you do not have time to type out standard 
# imports, configure recursion limits, or write boilerplate test-case loops.
#
# Grandmasters have a master template saved in their IDE. When a new file is 
# created, this code is instantly injected. It contains every critical data 
# structure, Fast I/O handling, and Math configurations required to solve 
# 99% of competitive programming problems.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the standard imports required for CP.
# - Understand the structure of a multi-test-case `solve()` function.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MASTER TEMPLATE
# ==============================================================================
def display_master_template():
    section_header("The Master Python CP Template")
    
    print("Copy and paste this exact structure for all Codeforces / HackerRank contests:\n")
    
    template_code = """
import sys
import math
import heapq
import bisect
from collections import deque, defaultdict, Counter

# ==============================================================================
# FAST I/O CONFIGURATION
# ==============================================================================
# If running locally, you can pass a string to this script.
# In a judge environment, this automatically reads from stdin.

def solve():
    # Read the entire input file into a 1D list of string tokens
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    iterator = iter(input_data)
    
    # Optional: Many problems have a Test Case count (T).
    # If the problem does NOT have T, just remove this loop.
    try:
        T = int(next(iterator))
    except StopIteration:
        return
        
    results = []
    
    for _ in range(T):
        # ----------------------------------------------------------------------
        # WRITE YOUR LOGIC HERE FOR A SINGLE TEST CASE
        # ----------------------------------------------------------------------
        # Example: Read N (size of array)
        n = int(next(iterator))
        
        # Example: Read the array of integers
        arr = [int(next(iterator)) for _ in range(n)]
        
        # Algorithm (Example: Find Max)
        ans = max(arr)
        
        # Append to results
        results.append(str(ans))
        # ----------------------------------------------------------------------
        
    # Print all results separated by newline in one massive system call
    sys.stdout.write('\\n'.join(results) + '\\n')


# ==============================================================================
# MAIN EXECUTION THREAD (WITH RECURSION EXPANSION)
# ==============================================================================
if __name__ == '__main__':
    # Increase Recursion Depth for Deep DFS on massive Graphs
    sys.setrecursionlimit(2000000)
    
    # Optional: Increase thread stack size if you get Memory Errors in DFS
    # import threading
    # threading.stack_size(1024 * 1024 * 64)
    # thread = threading.Thread(target=solve)
    # thread.start()
    # thread.join()
    
    # Standard Execution
    solve()
"""
    print(template_code)


def run_all_labs():
    display_master_template()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why do we import `math`, `heapq`, `bisect`, and `collections` globally in the template?
   Answer: In competitive programming, you never know what algorithm a problem requires until you read it. If you realize halfway through writing a solution that you need a Priority Queue to find the Top K elements, stopping your thought process to scroll to the top of the file and type `import heapq` breaks your cognitive flow. Furthermore, if you forget the import, you will get a `NameError` on submission, wasting a penalty point. By including the 4 foundational pillars of Python data structures globally in the template, you guarantee they are always instantly available in memory.

2. In the template, why is `ans` explicitly cast to a string via `str(ans)` before appending to `results`?
   Answer: The final line of the template is `sys.stdout.write('\n'.join(results))`. The Python string `.join()` method is a highly optimized C-level function, but it absolutely requires every single element in the provided iterable to be a String type. If you append raw integers (like `42`) to the `results` list, `.join()` will immediately crash with a `TypeError: sequence item 0: expected str instance, int found`. Casting inside the loop ensures the final I/O blast executes flawlessly.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CP Master Template Completed.")
