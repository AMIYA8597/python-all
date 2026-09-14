"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - EXCEPTION HANDLING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have a function that opens a network socket, reads data, and 
# returns. If an error occurs, it catches it and returns None. What is the fatal 
# flaw?"
# 
# A junior engineer might not see the issue. A senior engineer knows that the 
# network socket was NEVER mathematically closed because the function exited early. 
# This causes a massive "File Descriptor Leak" that will crash the server in 3 days.
# You must master the `finally` block and Context Managers (`with`) to mathematically 
# guarantee resource cleanup, regardless of catastrophic exceptions.
#
# Interviewer: "Explain the philosophy of EAFP vs LBYL in Python."
# If you write `if key in dict: return dict[key]`, you are using LBYL (Look Before 
# You Leap). In Python, this is considered an anti-pattern because it requires 
# two separate Dictionary lookups, wasting CPU cycles. You should use EAFP (Easier 
# to Ask for Forgiveness than Permission).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master EAFP (Easier to Ask for Forgiveness) vs LBYL.
# - Understand the horrific edge cases of the `finally` block.
# - Master Context Managers (`with` statement / `__enter__` and `__exit__`).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. EAFP VS LBYL (PYTHON'S CORE PHILOSOPHY)
# ==============================================================================
def lbyl_approach(data: dict, key: str):
    """
    Look Before You Leap (LBYL).
    Common in Java/C++.
    """
    # LOOKUP 1: Scans the Hash Table to see if the key exists.
    if key in data:
        # LOOKUP 2: Scans the Hash Table AGAIN to physically retrieve the data.
        return data[key]
    return "Not Found"

def eafp_approach(data: dict, key: str):
    """
    Easier to Ask for Forgiveness than Permission (EAFP).
    The idiomatic Python way.
    """
    try:
        # LOOKUP 1: Just aggressively attempt to grab it!
        return data[key]
    except KeyError:
        return "Not Found"

def demonstrate_eafp():
    section_header("EAFP vs LBYL")
    
    my_dict = {"server_status": "ONLINE"}
    
    print("In Python, Exception blocks (`try/except`) are mathematically ")
    print("ultra-lightweight. They cost almost 0 CPU cycles if no exception is raised.")
    
    print("\nLBYL requires 2 dictionary lookups (Wasteful!).")
    print("EAFP requires exactly 1 dictionary lookup (Optimal!).")
    
    print(f"\nResult EAFP: {eafp_approach(my_dict, 'server_status')}")


# ==============================================================================
# 4. THE `finally` BLOCK EDGE CASES
# ==============================================================================
def terrifying_finally_edge_case():
    """
    What happens if you return inside a `try`, but also return inside a `finally`?
    """
    try:
        print("  [TRY] Attempting to return 'SUCCESS'...")
        return "SUCCESS"
    finally:
        print("  [FINALLY] The finally block intercepts the return statement!")
        # NEVER DO THIS IN PRODUCTION.
        # Returning inside a finally block completely destroys and overrides 
        # any return value or exception that occurred in the try/except blocks!
        return "CRITICAL_OVERRIDE"

def demonstrate_finally():
    section_header("The `finally` Block Edge Cases")
    
    print("The `finally` block is mathematically guaranteed to execute, even if ")
    print("the program is actively crashing, or if a `return` was triggered.\n")
    
    result = terrifying_finally_edge_case()
    
    print(f"\nThe function actually returned: {result}")
    print("The `finally` block violently swallowed the 'SUCCESS' return!")


# ==============================================================================
# 5. CONTEXT MANAGERS (__enter__ and __exit__)
# ==============================================================================
class SafeNetworkSocket:
    """
    A custom Context Manager. It mathematically guarantees that `close()` is 
    called, completely replacing the need for messy try/finally blocks!
    """
    def __init__(self, ip: str):
        self.ip = ip
        
    def __enter__(self):
        """Fires the millisecond the `with` block opens."""
        print(f"  [ENTER] Opening socket connection to {self.ip}...")
        # You can return the object itself to be used as the `as` variable
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Fires the millisecond the `with` block closes, OR if the code crashes!
        If it crashed, the exception details are passed in here.
        """
        print(f"  [EXIT] Cleaning up! Closing socket connection to {self.ip}...")
        if exc_type is not None:
            print(f"         (Intercepted a crash: {exc_value})")
            
        # If we return True, we mathematically Swallow the exception and stop the crash!
        # If we return False, the exception continues to bubble up and crashes the script.
        return False

def demonstrate_context_managers():
    section_header("Context Managers (`with` statement)")
    
    print("Executing a Safe Network Socket...")
    
    try:
        with SafeNetworkSocket("192.168.1.1") as sock:
            print("  [MAIN] Connected! Attempting to send data...")
            # We violently crash the program!
            raise ConnectionError("Network Cable Unplugged!")
    except ConnectionError:
        print("  [MAIN] Handled the exception.")
        
    print("\nNotice that even though the code violently crashed, the `__exit__` ")
    print("cleanup method was mathematically guaranteed to fire!")


def run_all_labs():
    demonstrate_eafp()
    demonstrate_finally()
    demonstrate_context_managers()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does Python strongly prefer EAFP (`try/except`) over LBYL (`if key in dict`) for dictionary lookups, when Java strongly prefers the opposite?"
   Senior Answer: "In Java/C++, Exception Objects are astronomically heavy. Creating an Exception requires the OS to capture the entire CPU call stack, heavily pausing the thread. Therefore, you must use LBYL (`if obj != null`) to avoid the massive cost of Exceptions. In CPython, `try/except` blocks are heavily optimized. Establishing a `try` block costs almost zero CPU cycles. If no error occurs, EAFP is mathematically faster because it only requires 1 Hash Table lookup instead of 2. You only pay a CPU penalty if the exception actually fires, making EAFP the absolute optimal pattern for the 'Happy Path'."

2. Interviewer: "I wrote a `try` block that raises an Exception, an `except` block that raises a NEW Exception, and a `finally` block that has a `return` statement. What happens?"
   Senior Answer: "The `finally` block possesses absolute execution supremacy. When the `except` block raises the new Exception, Python pauses the crash and jumps into the `finally` block to execute cleanup code. Because the `finally` block hits a `return` statement, Python interprets this as a graceful exit. It violently swallows and deletes the active Exception, completely hiding the crash from the rest of the application, and simply returns the value. This is why placing a `return` statement inside a `finally` block is considered a catastrophic anti-pattern that destroys error visibility."

3. Interviewer: "How does the `with` statement (Context Manager) eliminate the need for `finally` blocks?"
   Senior Answer: "When you open a File or a Network Socket, you must guarantee it closes, even if the code crashes, to prevent File Descriptor leaks. Historically, this required messy `try...finally: file.close()` boilerplate everywhere. The `with` statement completely automates this. Under the hood, the object must implement the `__enter__` and `__exit__` dunder methods. The `with` keyword automatically executes `__enter__` at the start, and mathematically guarantees that `__exit__` will execute at the end, seamlessly passing any raised Exceptions directly into `__exit__` so the object can elegantly tear down its own C-level resources before allowing the crash to propagate."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Exception Handling) Completed.")
