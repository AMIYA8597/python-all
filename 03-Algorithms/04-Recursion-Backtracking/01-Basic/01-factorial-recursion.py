"""
# ==============================================================================
# LABORATORY: RECURSION FUNDAMENTALS & THE CALL STACK
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Recursion is when a function calls itself. 
# 
# While iterative loops (`for`, `while`) are the default way to repeat code in 
# most languages, Recursion is mathematically elegant and uniquely suited to 
# exploring complex branching data structures like Trees and Graphs.
#
# To master Recursion, you must stop thinking about the Code, and start thinking 
# about the OS Call Stack. Every time a function calls itself, it PAUSES its 
# current execution, saves its local variables to RAM, and puts a new "Frame" 
# on top of the Call Stack.
#
# If you don't provide a "Base Case" to stop the recursion, the Call Stack will 
# grow infinitely until it consumes all your RAM, crashing your program with a 
# "StackOverflowError" (or RecursionError in Python).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Base Case vs Recursive Step.
# - Understand how the OS Call Stack consumes O(N) memory.
# - Understand Python's Recursion Limit.
# - Concept: Tail Recursion (and why Python ignores it).
#
# ==============================================================================
"""

import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RECURSION MECHANICS (FACTORIAL)
# ==============================================================================
def factorial_recursive(n: int) -> int:
    """
    Calculates N! (N * N-1 * N-2 ... * 1).
    Time Complexity: O(N)
    Space Complexity: O(N) due to the Call Stack!
    """
    # 1. THE BASE CASE
    # Without this, the function would call itself with -1, -2, -3... infinitely.
    if n <= 1:
        return 1
        
    # 2. THE RECURSIVE STEP
    # Notice that the multiplication `n * ...` CANNOT happen yet!
    # The CPU must PAUSE this function, push it to the stack, and resolve 
    # the inner function call first.
    return n * factorial_recursive(n - 1)

def factorial_iterative(n: int) -> int:
    """
    Calculates N! using a loop.
    Time Complexity: O(N)
    Space Complexity: O(1) (Only uses a single integer variable in RAM).
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def demonstrate_factorial():
    section_header("Algorithm: Recursion Mechanics")
    
    n = 5
    print(f"Calculating Factorial of {n}...")
    print(f"Recursive Result: {factorial_recursive(n)}")
    print(f"Iterative Result: {factorial_iterative(n)}")
    
    print("\nTracing the Call Stack for factorial(5):")
    print(" 1. factorial(5) pauses. Needs 5 * factorial(4)")
    print(" 2. factorial(4) pauses. Needs 4 * factorial(3)")
    print(" 3. factorial(3) pauses. Needs 3 * factorial(2)")
    print(" 4. factorial(2) pauses. Needs 2 * factorial(1)")
    print(" 5. factorial(1) hits BASE CASE! Returns 1.")
    print(" 6. Stack unwinds: 2 * 1 = 2")
    print(" 7. Stack unwinds: 3 * 2 = 6")
    print(" 8. Stack unwinds: 4 * 6 = 24")
    print(" 9. Stack unwinds: 5 * 24 = 120 (Final Answer)")


# ==============================================================================
# 4. PYTHON'S RECURSION LIMIT
# ==============================================================================
def demonstrate_stack_overflow():
    section_header("Concept: The Stack Overflow")
    
    # Python sets a hard limit on how deep the Call Stack can go.
    # This prevents poorly written code from locking up the entire OS memory.
    limit = sys.getrecursionlimit()
    print(f"Python's default recursion limit is: {limit} frames.")
    
    print("""
If you call `factorial_recursive(2000)`, Python will instantly throw a 
RecursionError before it even attempts to do the math!

You CAN bypass this using `sys.setrecursionlimit(5000)`, but it is highly 
discouraged. If an algorithm requires a recursion depth of 5,000, you should 
rewrite it Iteratively (using a `while` loop and your own `list` to act as a stack).
    """)


# ==============================================================================
# 5. TAIL RECURSION
# ==============================================================================
def factorial_tail_recursive(n: int, accumulator: int = 1) -> int:
    """
    Tail Recursion passes the running total down into the next function call!
    Notice the `return factorial(...)` has NO multiplication attached to it!
    """
    if n <= 1:
        return accumulator
    return factorial_tail_recursive(n - 1, n * accumulator)

def explain_tail_recursion():
    section_header("Concept: Tail Call Optimization (TCO)")
    print("""
In standard recursion `return n * func(n-1)`, the OS MUST keep the current 
function alive in RAM because it still has to do the multiplication `n * ...` 
after the inner function finishes.

In Tail Recursion `return func(n-1, acc)`, there is absolutely nothing left 
for the current function to do! It passes the answer directly back.

In functional languages like Haskell or Scala, the compiler recognizes this and 
implements "Tail Call Optimization" (TCO). It instantly deletes the current 
frame from RAM before calling the next one, dropping the Space Complexity from 
O(N) down to a mathematically perfect O(1)!

Does Python do this?
NO.
Guido van Rossum (creator of Python) explicitly rejected Tail Call Optimization. 
He argued it makes debugging stack traces impossible. In Python, Tail Recursion 
will still consume O(N) memory and will still trigger a Stack Overflow.
    """)


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the Space Complexity of a Recursive Function?
   Answer: It is directly proportional to the maximum depth of the Call Stack. If a function calls itself $N$ times deeply, it is $O(N)$ Space. Note: If a function branches (like `func(n-1) + func(n-2)`), the Space is NOT $O(2^N)$, it is only $O(N)$ because the left branch fully executes and pops off the stack before the right branch starts! The maximum depth is only $N$.

2. If a recursive algorithm crashes with a Stack Overflow, how do you fix it without raising the OS limit?
   Answer: You rewrite the algorithm Iteratively using a `while` loop, and simulate the recursion manually by pushing items into a standard Array/List. The OS Call Stack is highly limited (a few Megabytes). A standard Python `list` is allocated in the Heap Memory (Gigabytes). You will never overflow the Heap.

3. Why did Python reject Tail Call Optimization (TCO)?
   Answer: When a program crashes, developers rely on the "Traceback" (the history of the call stack) to figure out what went wrong. TCO physically deletes the history of the call stack as it runs to save RAM. If a crash occurs deep in a tail-optimized function, the stack trace is completely empty, making debugging incredibly difficult.
"""

if __name__ == "__main__":
    demonstrate_factorial()
    demonstrate_stack_overflow()
    explain_tail_recursion()
    print("\n[SUCCESS] Laboratory: Recursion Fundamentals Completed.")
