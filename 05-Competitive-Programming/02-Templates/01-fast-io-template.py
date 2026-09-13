"""
# ==============================================================================
# COMPETITIVE PROGRAMMING TEMPLATE: FAST I/O (INPUT/OUTPUT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In platforms like Codeforces or HackerRank, the judge feeds your program 
# massive text files via Standard Input (stdin) and reads your Standard Output (stdout).
#
# If a problem has N = 1,000,000 integers to read, using Python's default 
# `input()` function in a loop will cause a "Time Limit Exceeded" (TLE) error 
# before your algorithm even starts running!
#
# Why? `input()` is heavily buffered and strips trailing newlines one line 
# at a time, incurring massive system call overhead. `print()` flushes the 
# I/O buffer to the console on every single call, completely freezing execution.
#
# To survive, you must use Fast I/O. You read the ENTIRE input file into RAM 
# in a single system call (`sys.stdin.read()`), split it by whitespace, and 
# maintain a pointer to iterate through the tokens.
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    # We still use print for this educational lab, but in a real contest,
    # you would use sys.stdout.write
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 2. THE FAST I/O TEMPLATE (COPY-PASTE THIS INTO CODEFORCES)
# ==============================================================================
def fast_io_example():
    section_header("Fast I/O Example Execution")
    
    print("In a real Codeforces environment, you would use this exact template:")
    
    print("""
import sys

def solve():
    # 1. READ EVERYTHING AT ONCE (Single System Call)
    # read() dumps the entire file into a single massive string.
    # split() creates a list of strings, automatically handling spaces AND newlines!
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
        
    # 2. CREATE AN ITERATOR
    # Using an iterator prevents us from tracking an index manually.
    iterator = iter(input_data)
    
    try:
        # Example: The first token is the number of Test Cases (T)
        T = int(next(iterator))
        
        # We collect our answers in a list, NOT by printing immediately!
        results = []
        
        for _ in range(T):
            # Example: Read N and M for this test case
            N = int(next(iterator))
            M = int(next(iterator))
            
            # Example Algorithm: Just sum them up
            ans = N + M
            
            # Append the string representation to our results
            results.append(str(ans))
            
        # 3. FAST OUTPUT
        # Join all answers with a newline and execute ONE single print/write call.
        sys.stdout.write('\\n'.join(results) + '\\n')
        
    except StopIteration:
        # Failsafe in case the input file ends unexpectedly
        pass

if __name__ == '__main__':
    solve()
    """)
    
    print("This template can process 1,000,000 integers in ~0.2 seconds in Python.")
    print("Standard `input()` loops would take ~2.5 seconds (Instant TLE!).")


# ==============================================================================
# 3. RECURSION LIMIT EXPANSION
# ==============================================================================
def demonstrate_recursion_limit():
    section_header("Expanding the Call Stack (For Deep DFS)")
    
    print("If a problem requires Depth-First Search (DFS) on a Graph with 10^5 nodes, ")
    print("Python will crash with: `RecursionError: maximum recursion depth exceeded`.")
    print("Python limits the call stack to 1,000 by default to prevent OS crashes.\n")
    
    print("You MUST include this at the top of your file for Graph problems:\n")
    
    print("```python")
    print("import sys")
    print("import threading")
    print("")
    print("# 1. Tell Python interpreter to allow deeper stacks")
    print("sys.setrecursionlimit(2000000)")
    print("")
    print("# 2. Tell the OS to allocate a massive memory stack for the thread (e.g. 64MB)")
    print("threading.stack_size(1024 * 1024 * 64)")
    print("")
    print("def main_logic():")
    print("    solve()")
    print("")
    print("# 3. Execute your code inside the newly allocated Thread!")
    print("thread = threading.Thread(target=main_logic)")
    print("thread.start()")
    print("thread.join()")
    print("```")


def run_all_labs():
    fast_io_example()
    demonstrate_recursion_limit()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `sys.stdin.read().split()` perfectly handle bad formatting in test cases?
   Answer: In competitive programming, the input files are often dirty. A test case might provide 5 integers separated by spaces, but the next test case provides 5 integers separated by completely random combinations of spaces, tabs, and newlines. If you use `input().split(' ')`, it will fail catastrophically if there are double spaces or newlines. `sys.stdin.read()` pulls the entire file into a string. Calling `.split()` with no arguments automatically defaults to splitting by *any whitespace character* (space, tab, newline, carriage return) and completely strips empty strings, yielding a flawless, sanitized 1D list of tokens!

2. Why is `sys.stdout.write('\n'.join(results))` exponentially faster than calling `print()` in a loop?
   Answer: I/O (Input/Output) operations are System Calls. The CPU has to stop its math execution, request permission from the Operating System kernel to access the standard output buffer, flush the buffer to the terminal, and return control. This context switching is massively expensive. Calling `print()` 1,000,000 times triggers 1,000,000 OS context switches. By storing all answers in a Python list, joining them into a single massive string in RAM, and executing `sys.stdout.write()` exactly ONCE, you reduce the OS context switches from 1,000,000 down to 1. This drastically cuts execution time and prevents TLEs.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Fast I/O Template Completed.")
