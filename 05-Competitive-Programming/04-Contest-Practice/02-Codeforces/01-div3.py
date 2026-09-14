"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (CODEFORCES DIV-3)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Codeforces is the undisputed king of Competitive Programming. 
# While LeetCode gives you clean function signatures (`def solve(nums):`), 
# Codeforces forces you to read raw text from Standard Input (stdin) and print 
# raw text to Standard Output (stdout).
#
# Codeforces Division 3 contests are designed for beginners. The first two 
# problems (A and B) are almost always "Greedy Math" or "Implementation" problems.
# They don't require advanced data structures; they require logical deduction 
# and extremely fast, bug-free typing.
#
# In this lab, we will simulate a classic Div-3 Problem A: "Given N, find if 
# you can split it into two EVEN numbers." (The famous Watermelon problem).
# We will also simulate standard Codeforces I/O boilerplate.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master standard Python Fast I/O for Codeforces.
# - Understand the structure of "Multiple Test Cases" (T).
# - Master O(1) Greedy Math deduction.
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CODEFORCES FAST I/O BOILERPLATE
# ==============================================================================
def fast_io_example():
    """
    Codeforces problems can have 10^5 test cases.
    If you use standard `input()` and `print()`, Python will Time Limit Exceed (TLE).
    You MUST use `sys.stdin.read` to aggressively buffer all input into memory at once!
    """
    # This is a simulated string of what the raw Standard Input looks like.
    # The first number '3' means there are 3 test cases.
    # The following numbers are the test cases: 8, 2, 11.
    mock_stdin = "3\n8\n2\n11\n"
    
    print("Raw Codeforces Input:")
    print(mock_stdin.strip())
    
    # 1. Read everything at once and split by whitespace!
    # In a real contest, this would be: data = sys.stdin.read().split()
    data = mock_stdin.split()
    
    if not data:
        return
        
    # 2. The first token is ALWAYS the number of test cases (T)
    T = int(data[0])
    
    results = []
    
    # 3. Process each test case
    for i in range(1, T + 1):
        weight = int(data[i])
        
        # ----------------------------------------------------------------------
        # PROBLEM: THE WATERMELON (Div-3 Problem A)
        # You have a watermelon of weight W. Can you divide it into two parts 
        # such that BOTH parts weigh an strictly EVEN number of kilos?
        # (The parts do NOT have to be equal. E.g., 8 can be 2 and 6).
        # ----------------------------------------------------------------------
        
        # O(1) Math Deduction:
        # For a number to be split into two EVEN numbers, the number itself MUST be even.
        # (Even + Even = Even).
        # Is that it? No! There is a mathematical edge case.
        # What if W = 2? The only way to split 2 is 1 + 1. 
        # But 1 is an ODD number! Therefore, 2 fails. 
        # The true mathematical condition is: W must be EVEN, AND W must be > 2.
        
        if weight % 2 == 0 and weight > 2:
            results.append("YES")
        else:
            results.append("NO")
            
    # 4. Print all results joined by newlines!
    # In a real contest, this would be: sys.stdout.write('\n'.join(results) + '\n')
    print("\nCodeforces Output:")
    print('\n'.join(results))

def demonstrate_div3():
    section_header("Codeforces Div-3 (Math & I/O)")
    fast_io_example()
    print("\nNotice how the edge case '2' mathematically fails because it splits into 1+1.")
    print("Div-3 problems are entirely about finding these hidden mathematical traps!")


def run_all_labs():
    demonstrate_div3()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is `sys.stdin.read().split()` strictly mandatory for Python in Codeforces, instead of using a `for` loop with `input()`?
   Answer: The Python `input()` function is incredibly slow. Every time you call it, Python flushes buffers, checks for trailing carriage returns (`\r\n` on Windows vs `\n` on Linux), and allocates a new string object. If a problem has 200,000 test cases, calling `input()` 200,000 times introduces massive I/O overhead, easily adding 1.5 seconds to your execution time and guaranteeing a Time Limit Exceeded (TLE) crash. By using `sys.stdin.read().split()`, Python makes a single C-level system call to pull the entire 5MB text file into memory in 0.01 seconds, completely eliminating I/O bottlenecks.

2. In Div-3 Problem A (Watermelon), why is $O(1)$ mathematical deduction required instead of a `for` loop that checks all combinations?
   Answer: In this specific problem, $W \le 100$, so a `for` loop checking `for i in range(2, W): if i%2==0 and (W-i)%2==0:` would pass instantly. However, Div-3 Problems almost always have "Hard" variants where $W \le 10^{18}$. If you train your brain to write `for` loops for simple math problems, you will instantly fail when the constraints are raised. Competitive Programming demands that you always search for the $O(1)$ mathematical truth (e.g., Even + Even = Even, therefore W must be Even and $>2$).

3. What does it mean when a Codeforces problem explicitly states $\sum N \le 2 \cdot 10^5$?
   Answer: This is a crucial constraint! A problem might have $T = 10^5$ test cases. For each test case, you are given an array of size $N$. If the maximum value of $N$ is $2 \cdot 10^5$, you might panic, thinking: "If I process $10^5$ arrays of size $200,000$, my total operations will be $20 \text{ Billion}$, which is a TLE!" However, the $\sum N$ constraint mathematically guarantees that the *SUM* of all $N$s across ALL test cases combined will never exceed $200,000$. This instantly proves that an $O(N)$ or $O(N \log N)$ algorithm will pass effortlessly!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Codeforces Div-3 Completed.")
