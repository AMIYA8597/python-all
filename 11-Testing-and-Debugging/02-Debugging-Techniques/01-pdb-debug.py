"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (PDB & INTERACTIVE DEBUGGING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer encounters a `KeyError` inside a loop processing 5,000 JSON 
# objects. To debug it, they add `print(item)` inside the loop and re-run the 
# script. The terminal violently floods with 4,999 correct items before printing 
# the 1 broken item, which immediately scrolls off the screen. They spend 45 
# minutes scrolling through their terminal output trying to find the bug.
#
# A senior software engineer uses `pdb` (Python Debugger) or the `breakpoint()` 
# built-in. They mathematically command the Python Interpreter to execute the 
# first 4,999 items at full C-speed, and dynamically PAUSE the execution exactly 
# 1 millisecond before the `KeyError` occurs. They open an interactive terminal, 
# inspect the memory state, evaluate local variables, and mathematically prove 
# exactly why the dictionary key is missing, solving the bug in 30 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Interpreter Halting via `breakpoint()` / `pdb.set_trace()`.
# - Execute interactive Stack Frame navigation (`n`, `s`, `c`, `ll`).
# - Architect conditional debugging for massive datasets.
#
# ==============================================================================
"""

import pdb

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE BUGGY CODE)
# ==============================================================================
class DataProcessor:
    @staticmethod
    def process_financial_records(records: list):
        """
        Calculates the total revenue. 
        There is a fatal bug buried in the dataset!
        """
        total_revenue = 0.0
        
        for i, record in enumerate(records):
            
            # --- CONDITIONAL DEBUGGING ---
            # If we just put `breakpoint()` here, the script will pause on Record 0!
            # We don't want to hit 'c' (continue) 499 times to find the bug.
            # A senior developer writes a CONDITIONAL breakpoint!
            
            # In Python 3.7+, `breakpoint()` is the modern equivalent of `pdb.set_trace()`
            # We wrap it in a try/except to catch the exact mathematical anomaly!
            try:
                # The Bug: One of the records is missing the 'amount' key!
                price = float(record['amount'])
                qty = int(record['qty'])
                total_revenue += (price * qty)
                
            except KeyError as e:
                print(f"\n  [ERROR TRAPPED] Exception caught at Index {i}.")
                print(f"  [DEBUGGER] If this wasn't a lab, `breakpoint()` would pause execution here!")
                print(f"  [DEBUGGER] You could type `p record` to inspect the broken JSON.")
                # We comment this out so the CI/CD pipeline doesn't literally freeze!
                # breakpoint() 
                
        return total_revenue


# ==============================================================================
# 4. THE PDB COMMAND REFERENCE (THE CHEAT SHEET)
# ==============================================================================
"""
When `breakpoint()` pauses the execution, your terminal transforms into the 
interactive (Pdb) prompt. You have absolute control over the CPU!

--- CORE COMMANDS ---
[l] or [ll] (List)     -> Shows the Python code currently executing.
[n] (Next)             -> Executes the current line of code and pauses on the next line.
[s] (Step)             -> If the current line is a function, steps INSIDE the function!
[c] (Continue)         -> Resumes full execution speed until the next breakpoint.
[p var] (Print)        -> Evaluates and prints a variable (e.g., `p record['id']`).
[q] (Quit)             -> Violently kills the Python process.
[w] (Where)            -> Prints the Call Stack (who called this function?)
[u] / [d] (Up/Down)    -> Navigates UP or DOWN the Call Stack to inspect parent variables!
"""


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_debugging():
    section_header("Debugging: Interactive Python Debugger (PDB)")
    
    # We generate a dataset of 500 records.
    # Record 499 is mathematically corrupted!
    dataset = []
    for i in range(500):
        if i == 499:
            dataset.append({"id": i, "qty": 10}) # FATAL BUG: Missing 'amount'!
        else:
            dataset.append({"id": i, "amount": "9.99", "qty": 10})
            
    print("  [EXECUTION] Processing 500 financial records...")
    
    result = DataProcessor.process_financial_records(dataset)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By mathematically trapping the Exception and triggering `breakpoint()`, ")
    print("  the developer bypassed 499 useless print statements and instantly ")
    print("  halted the CPU exactly on the broken data structure.")


def run_all_labs():
    demonstrate_debugging()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is using `print()` statements to debug a large loop or a recursive algorithm considered an anti-pattern compared to `breakpoint()`?"
   Senior Answer: "Terminal Flooding and State Mutation. If a loop runs $10,000$ times and breaks on the final iteration, injecting a `print()` statement forces the CPU to execute $10,000$ I/O operations, violently flooding the terminal buffer and pushing the actual error off the screen. Worse, you cannot interact with the state. If `print(user)` shows an object, but you suddenly realize you need to see `user.parent.id`, you have to modify the code, restart the script, and wait again. `breakpoint()` halts the CPython interpreter in RAM. You can dynamically navigate the object tree, evaluate complex list comprehensions on the fly, and inspect the entire Call Stack without ever restarting the program."

2. Interviewer: "What is the architectural difference between the `next` (n) and `step` (s) commands in the Python Debugger?"
   Senior Answer: "Stack Frame Navigation. The `next` command treats the current line of code as a black box. If the line is `result = calculate_taxes(amount)`, pressing `n` will mathematically execute the *entire* `calculate_taxes` function at full C-speed, and pause the debugger on the very next line of the *current* function. The `step` command dives into the Call Stack. Pressing `s` will mathematically teleport your debugger *inside* the `calculate_taxes` function, pausing on line 1 of that file, allowing you to debug the internal mechanics of the child function."

3. Interviewer: "If the Python script crashes inside a 3rd-party library (like Pandas or Django), how can you use `pdb` to inspect your own variables before the crash happened?"
   Senior Answer: "Post-Mortem Debugging. Instead of blindly placing `breakpoint()` statements in your code, you execute the script directly through the debugger from the terminal: `python -m pdb main.py`. When the fatal Exception is thrown deep inside the Django framework, the script does *not* exit to the terminal. Instead, `pdb` intercepts the crash, freezes the exact memory state (the Core Dump), and opens the interactive prompt. You can then type `up` (`u`) multiple times to mathematically ascend the Call Stack, climbing out of the Django library and back into your own application code, allowing you to inspect exactly which invalid variable you passed to the framework that caused it to explode."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (PDB) Completed.")
