"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (CLI AUTOMATION & ARGPARSE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer writes a data processing script. To change the target file 
# or the processing speed, the user must physically open `script.py` in an IDE, 
# find line 42, modify a hardcoded variable, save the file, and run it. When 
# deployed to a remote Linux server via SSH, the user has no IDE and accidentally 
# deletes half the script while using `vim`.
#
# A senior engineer understands "Command Line Interfaces" (CLI). They mathematically 
# decouple the Configuration from the Execution. They use `argparse` to create 
# professional, Unix-standard command-line arguments (like `--input`, `--verbose`). 
# The script becomes a standalone executable tool. Any sysadmin can dynamically 
# alter the script's behavior at runtime from the Linux terminal without ever 
# looking at a single line of Python code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architecture of Command Line Interfaces (CLI).
# - Execute dynamic parameter injection using `argparse`.
# - Differentiate between Positional Arguments and Optional Flags.
#
# ==============================================================================
"""

import argparse
import time
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE EXECUTION)
# ==============================================================================
# The Business Logic should NEVER contain `sys.argv` or CLI parsing.
# It should strictly accept parameters. This ensures the function can be 
# mathematically tested or imported by other modules cleanly!

def execute_data_processing(input_file: str, output_file: str, retries: int, verbose: bool):
    """The core engine of the script."""
    
    if verbose:
        print(f"  [DEBUG] Engine initialized with {retries} max retries.")
        print(f"  [DEBUG] Target Input: {input_file}")
        
    print(f"  [PROCESSING] Analyzing {input_file}...")
    
    # Simulating work or failure
    attempt = 1
    while attempt <= retries:
        if verbose:
            print(f"  [DEBUG] Attempt {attempt}/{retries}...")
            
        time.sleep(0.2) # Simulating I/O
        
        # Simulate a successful execution on the 2nd attempt!
        if attempt == 2 or retries == 1:
            print(f"  [SUCCESS] Data mathematically transformed and saved to {output_file}.")
            return
            
        if verbose:
            print("  [DEBUG] Network timeout. Retrying...")
            
        attempt += 1
        
    print(f"  [ERROR] Catastrophic failure after {retries} attempts.")


# ==============================================================================
# 4. THE CLI ARCHITECTURE (ARGPARSE)
# ==============================================================================
def create_cli_parser() -> argparse.ArgumentParser:
    """Constructs the mathematical routing of the Command Line Interface."""
    
    # 1. Initialize the Parser
    parser = argparse.ArgumentParser(
        description="Advanced Data Processing CLI Tool",
        epilog="Example: python 05-script-opt.py data.csv output.json --retries 3 --verbose"
    )
    
    # 2. POSITIONAL ARGUMENTS (Mandatory!)
    # The user MUST provide these, exactly in order!
    parser.add_argument(
        "input", 
        type=str, 
        help="The absolute or relative path to the raw data file."
    )
    
    parser.add_argument(
        "output", 
        type=str, 
        help="The destination path for the transformed data."
    )
    
    # 3. OPTIONAL ARGUMENTS (Flags!)
    # The user can omit these. They have mathematically defined default values!
    parser.add_argument(
        "-r", "--retries", 
        type=int, 
        default=1, 
        help="Number of times to retry on network failure. (Default: 1)"
    )
    
    # 4. BOOLEAN FLAGS (Store True)
    # If the user types `--verbose`, the variable becomes True. If omitted, False.
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable advanced mathematical debugging output."
    )
    
    return parser


def simulate_cli_execution():
    section_header("Command Line Interface (Argparse) Simulation")
    
    print("  [SCENARIO] A Sysadmin runs your script from a Linux Bash Terminal.")
    
    # We must manually construct the parser for the simulation
    parser = create_cli_parser()
    
    print("\n  [TEST 1: The Help Menu (`--help`)]")
    print("    -> Command: `python 05-script-opt.py --help`")
    # `argparse` automatically generates a beautiful, standard Unix help menu!
    parser.print_help()
    
    print("\n  [TEST 2: Standard Execution (Positional Only)]")
    print("    -> Command: `python 05-script-opt.py raw_data.csv final_data.json`")
    print("    -> Execution Output:")
    
    # We simulate parsing the Bash string!
    args_2 = parser.parse_args(["raw_data.csv", "final_data.json"])
    execute_data_processing(args_2.input, args_2.output, args_2.retries, args_2.verbose)
    
    print("\n  [TEST 3: Advanced Execution (Flags Enabled)]")
    print("    -> Command: `python 05-script-opt.py raw_data.csv final_data.json --retries 3 --verbose`")
    print("    -> Execution Output:")
    
    args_3 = parser.parse_args(["raw_data.csv", "final_data.json", "--retries", "3", "--verbose"])
    execute_data_processing(args_3.input, args_3.output, args_3.retries, args_3.verbose)


def run_all_labs():
    simulate_cli_execution()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why should we use the `argparse` module instead of simply reading the `sys.argv` list directly?"
   Senior Answer: "Reading `sys.argv` directly is highly dangerous and scales catastrophically. If you write `input_file = sys.argv[1]`, and the user runs the script without any arguments, `sys.argv` only contains 1 element (the script name). The script will violently crash with an `IndexError`. Furthermore, `sys.argv` strictly reads all inputs as Strings; you have to manually parse Integers and Booleans. `argparse` mathematically intercepts the Bash execution, automatically handles `IndexErrors` by generating a graceful 'Missing required argument' message, automatically coerces strings into Integers (`type=int`), automatically generates the `--help` manual, and standardizes optional flags (`--verbose`), transforming a fragile script into a robust Unix executable."

2. Interviewer: "What is the architectural difference between a Positional Argument and an Optional Flag?"
   Senior Answer: "A Positional Argument (e.g., `parser.add_argument('input')`) is structurally mandatory. Its mathematical identity is determined strictly by its physical position in the Bash string. If the user types `python script.py data.csv out.json`, the script knows `data.csv` is the input solely because it is the first string provided. An Optional Flag (e.g., `parser.add_argument('--retries')`) is non-mandatory and position-independent. The user can type `python script.py --retries 3 data.csv out.json` or put the flag at the very end. The `argparse` engine uses the `--` prefix to mathematically identify the key-value pair regardless of its location in the string."

3. Interviewer: "Why did we mathematically separate the `execute_data_processing` function from the `create_cli_parser` function?"
   Senior Answer: "Because of the 'Separation of Concerns' architectural design pattern. If you intertwine CLI parsing directly inside your business logic (e.g., `if args.verbose: do_math()`), your business logic becomes permanently coupled to the Terminal. If you later want to trigger that exact same data processing logic from a Flask Web API or a Pytest testing suite, you cannot, because the function expects a Bash `argparse` object! By mathematically decoupling them, `execute_data_processing` remains a pure, testable Python function that only accepts standard parameters (Strings, Ints), while the CLI Parser acts merely as a 'Translation Layer' between the Linux Terminal and the pure Python engine."
"""

if __name__ == "__main__":
    # In a real environment, you would use this block to run the parser against actual `sys.argv`!
    # Example:
    # parser = create_cli_parser()
    # args = parser.parse_args()
    # execute_data_processing(args.input, args.output, args.retries, args.verbose)
    
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Automation (CLI & Argparse) Completed.")
