"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (IPDB & ADVANCED INTERACTIVITY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses `pdb` (Python Debugger) to inspect a complex nested 
# dictionary inside a JSON API response. When they type `p response_data`, the 
# terminal prints a massive, unformatted, monochromatic block of text spanning 
# 3 screens. It is mathematically impossible to read. Furthermore, `pdb` lacks 
# basic autocomplete, meaning they have to manually type out massive variable 
# names (`user_authentication_matrix_cache`) and misspell them 3 times.
#
# A senior software engineer uses `ipdb` (IPython Debugger). `ipdb` mathematically 
# injects the entire IPython interactive kernel into the debugging session. 
# It provides gorgeous Syntax Highlighting, making strings green and integers blue. 
# It provides Tab-Completion, allowing the engineer to type `user_auth<TAB>` and 
# instantly complete the variable. It formats massive JSON dictionaries beautifully. 
# Debugging becomes a high-speed, mathematically precise operation.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master IPython Debugger (`ipdb`) architecture.
# - Execute Advanced REPL Commands (`?`, `??`, `%magic`).
# - Understand developer ergonomics and syntax highlighting in CLI tools.
#
# ==============================================================================
"""

import sys

# Gracefully handle the ipdb dependency
try:
    import ipdb
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE COMPLEX DATA STRUCTURE)
# ==============================================================================
class AdvancedDataProcessor:
    @staticmethod
    def process_api_payload(payload: dict):
        """
        Processes a massively nested JSON payload.
        This is where standard `pdb` fails because the data is too ugly to read.
        """
        # Complex nested data!
        user_metadata = payload.get("metadata", {})
        auth_tokens = payload.get("security", {}).get("tokens", [])
        
        try:
            # Bug: We assume the first token is a dictionary, but it might be a string!
            primary_token = auth_tokens[0]
            token_expiry = primary_token["expiry_date"]
            
        except (IndexError, TypeError, KeyError) as e:
            print(f"\n  [ERROR TRAPPED] Exception caught: {type(e).__name__}")
            print(f"  [DEBUGGER] If this wasn't a lab, `ipdb.set_trace()` would pause here!")
            
            # --- IPDB INJECTION ---
            # In a real environment, you run this to get the beautiful colored debugger!
            # ipdb.set_trace()
            
            # Why is ipdb better?
            # 1. You type `p payload`. It prints with colors and perfect indentation!
            # 2. You type `auth_<TAB>`. It auto-completes to `auth_tokens`!
            # 3. You type `AdvancedDataProcessor??`. It prints the entire SOURCE CODE of the class!


# ==============================================================================
# 4. THE IPYTHON COMMAND REFERENCE (THE MAGIC)
# ==============================================================================
"""
`ipdb` inherits all the navigation commands from `pdb` (n, s, c, u, d), 
but injects the absolute mathematical power of IPython!

--- ADVANCED IPYTHON COMMANDS ---
[<TAB>]                   -> Auto-completes variable names, class methods, and imports!
[obj?]                    -> Prints the Docstring and basic metadata for ANY object.
[obj??]                   -> Prints the raw Python SOURCE CODE for the object/function!
[pp var]                  -> Pretty-Prints. Formats massive dictionaries flawlessly.
[!code]                   -> Executes a raw Python command if it conflicts with a pdb command.
                             (e.g., if you have a variable named 'c', typing 'c' continues the debugger. 
                             Typing '!c' evaluates the variable).
"""


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_ipdb():
    section_header("Debugging: IPython Debugger (IPDB)")
    
    if not HAS_LIBS:
        print("  [WARNING] `ipdb` is not installed. Run `pip install ipdb` in your real environment.")
    
    # We generate a hostile, heavily nested payload!
    hostile_payload = {
        "user_id": 9942,
        "metadata": {
            "last_login": "2024-01-01",
            "preferences": {"theme": "dark", "notifications": False}
        },
        "security": {
            # FATAL BUG: The API returned a string instead of a dictionary!
            "tokens": ["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"] 
        }
    }
    
    print("  [EXECUTION] Processing heavily nested JSON API Payload...")
    
    # Execute the buggy logic
    AdvancedDataProcessor.process_api_payload(hostile_payload)
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By utilizing `ipdb.set_trace()`, the developer gains access to Syntax ")
    print("  Highlighting, Auto-Complete, and Object Introspection (`??`), cutting ")
    print("  debugging time by 50% compared to standard `pdb`.")


def run_all_labs():
    demonstrate_ipdb()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the architectural mechanism that allows `ipdb` to provide Tab-Completion, whereas standard `pdb` cannot?"
   Senior Answer: "The Read-Eval-Print Loop (REPL) Kernel. Standard `pdb` runs on the basic CPython `cmd` module, which is a primitive text-processing loop. `ipdb` mathematically imports the massive `IPython` architecture. IPython utilizes the `prompt_toolkit` and the `jedi` autocompletion library. When you press `<TAB>`, IPython mathematically parses the current Abstract Syntax Tree (AST) of the debugger's local namespace, queries `jedi` for all valid methods, attributes, and variables in the current memory scope, and dynamically renders them in the terminal, providing IDE-level introspection within a raw CLI environment."

2. Interviewer: "If you are debugging a third-party library, how does the `??` (Double Question Mark) command in IPython/ipdb drastically improve debugging speed?"
   Senior Answer: "Dynamic Source Code Retrieval. If the script crashes inside `requests.get()`, and you are paused in `ipdb`, you might wonder exactly what the `get` function is mathematically doing. In standard `pdb`, you would have to leave the terminal, open your IDE, navigate to the `site-packages` directory, and hunt for the source file. In `ipdb`, typing `requests.get??` commands the IPython kernel to use Python's `inspect` module. It physically reads the `.py` file from the hard drive and prints the exact source code of the `get` function directly into your terminal, with full syntax highlighting, completely eliminating context-switching."

3. Interviewer: "Why should you never commit `import ipdb; ipdb.set_trace()` or `breakpoint()` into production code?"
   Senior Answer: "Blocking the Main Thread (Denial of Service). If a web server like Gunicorn or Uvicorn is running in Production, it is executing headless (without an attached interactive terminal). If the CPU hits `breakpoint()`, it halts execution and mathematically waits for a human to type a command on `stdin`. Because there is no terminal attached, the thread is permanently paralyzed. If $4$ users trigger that line of code, all $4$ worker processes freeze, and the entire web server goes completely offline, requiring a hard reboot. Breakpoints are mathematically fatal in non-interactive environments."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (IPDB) Completed.")
