"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (CODE REVIEWS & MYPY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer pushes 50 files to a Pull Request. Another developer spends 
# 3 hours manually reviewing the code, leaving comments like "You forgot a type hint", 
# "This line is too long", and "You have trailing whitespace here". The review 
# process degrades into petty arguments about formatting, destroying team morale 
# and wasting expensive engineering time on syntax problems.
#
# A senior software architect automates the misery away. They install "pre-commit" 
# hooks and `mypy` (Static Type Checker). When the junior developer types `git commit`, 
# the pipeline intercepts the commit *before* it hits the server. It automatically 
# reformats the code (Black), strips trailing whitespace, and mathematically verifies 
# every Type Hint in the system. The commit is rejected locally until it is flawless. 
# Code Reviews become purely about System Architecture and Business Logic.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Static Type Checking via `mypy`.
# - Execute algorithmic Code Formatting (Black / Ruff).
# - Architect automated Code Review pipelines (Pre-Commit Hooks).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE "BAD" TYPES)
# ==============================================================================
# Python is mathematically dynamically typed. The interpreter allows this code to run!
# BUT... `mypy` will mathematically reject it during Static Analysis!

class DynamicTypeDisaster:
    @staticmethod
    def calculate_discount(price, discount_percent):
        """
        Missing Type Hints! 
        Is price a float? An int? A string?
        """
        return price * (1 - (discount_percent / 100))
        
    @staticmethod
    def execute_disaster():
        # The Python interpreter will happily attempt this and VIOLENTLY CRASH at runtime.
        # "TypeError: unsupported operand type(s) for /: 'str' and 'int'"
        try:
            DynamicTypeDisaster.calculate_discount("One Hundred Dollars", "20")
        except TypeError as e:
            pass


# ==============================================================================
# 4. THE ARCHITECTURAL SOLUTION (MYPY & TYPE HINTS)
# ==============================================================================
# We mathematically enforce the variable types using the `typing` module!

from typing import List, Dict, Optional, Union

class StronglyTypedEngine:
    """
    A mathematically flawless, statically typed engine.
    """
    @staticmethod
    def calculate_discount(price: float, discount_percent: float) -> float:
        """
        By declaring the inputs as floats, `mypy` will scan the entire repository 
        looking for any developer who attempts to pass a string into this function.
        """
        return price * (1.0 - (discount_percent / 100.0))

    @staticmethod
    def process_order(user_id: int, items: List[Dict[str, Union[str, float]]]) -> Optional[str]:
        """
        Advanced Typing: We mathematically define exactly what the complex Dictionary looks like!
        """
        if not items:
            return None # We return an Optional string!
            
        total_price = sum(item["price"] for item in items if isinstance(item["price"], (int, float)))
        return f"Order {user_id} Processed: ${total_price:.2f}"


# ==============================================================================
# 5. THE AUTOMATED PIPELINE SIMULATOR
# ==============================================================================
class PreCommitSimulator:
    """Simulates what happens when a developer types `git commit`."""
    
    @staticmethod
    def run_pre_commit_hooks():
        print("  [GIT HOOK] Intercepting `git commit` command...")
        
        # 1. Formatter (Black / Ruff)
        print("  [HOOK 1] Executing Black Formatter...")
        print("    -> [AUTO-FIX] Re-wrapped line 42 to comply with 88-character limit.")
        
        # 2. Linter (Ruff / Flake8)
        print("  [HOOK 2] Executing Ruff Linter...")
        print("    -> [AUTO-FIX] Removed unused import 'os'.")
        
        # 3. Static Type Checker (Mypy)
        print("  [HOOK 3] Executing Mypy Type Checker...")
        print("    -> [FATAL ERROR] main.py:45: Argument 1 to 'calculate_discount' has incompatible type 'str'; expected 'float'")
        
        print("\n  [RESULT] The commit has been mathematically REJECTED by the local machine.")
        print("  The developer must fix the type error before pushing to GitHub.")


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_code_review():
    section_header("Code Quality: Pre-Commit Hooks & Mypy")
    
    PreCommitSimulator.run_pre_commit_hooks()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By forcing Mypy and Black to run LOCALLY via git hooks, the Code Review ")
    print("  process is mathematically shielded from syntactical garbage. Human reviewers ")
    print("  can now focus entirely on Business Logic, Security, and Scalability.")


def run_all_labs():
    demonstrate_code_review()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If Python is a dynamically typed language, why do senior engineers spend so much time writing Type Hints (e.g., `def func(x: int) -> str:`) if the Python interpreter completely ignores them at runtime?"
   Senior Answer: "Static Analysis and IDE Introspection. You are correct that the CPython interpreter mathematically ignores type hints; they do not speed up execution. However, we write them for two critical architectural tools. First, `mypy`. Mypy mathematically reads the AST before runtime and detects $90\\%$ of all `TypeErrors` and `AttributeErrors` (the most common bugs in Python). Second, the IDE (VS Code / PyCharm). Without type hints, if you type `user.`, the IDE doesn't know what `user` is and provides zero autocomplete. With type hints, the IDE mathematically knows `user` is a `User` object, instantly auto-completes `user.get_email()`, and flags an error if you pass a string instead of an int, slashing debugging time."

2. Interviewer: "What is the architectural purpose of a 'Pre-Commit Hook', and why is it superior to just running Linters in the CI/CD Pipeline on GitHub/GitLab?"
   Senior Answer: "The Developer Feedback Loop. If you rely purely on GitHub Actions, the developer commits the code, pushes it to the server, waits $5$ minutes for the pipeline to boot up, and *then* finds out they left a trailing whitespace. They have to fix it, commit again, and push again. This is a massive velocity sink. A 'Pre-Commit Hook' is a shell script that mathematically embeds itself directly into the `.git/hooks` directory on the developer's local laptop. When they type `git commit`, the hook runs instantly locally. It auto-formats the code and blocks the commit immediately if `mypy` fails. The bad code mathematically never touches the remote server, preserving a flawless Git history."

3. Interviewer: "In a Code Review, a Junior Developer argues that the Black code formatter is 'ugly' and they prefer to format their dictionaries manually. How do you respond architecturally?"
   Senior Answer: "Eliminating the Concept of 'Preference'. The purpose of an algorithmic auto-formatter like Black is not to write 'pretty' code; it is to mathematically enforce absolute uniformity across a massive codebase. If $50$ developers use $50$ different formatting preferences, the code becomes unreadable, and `git diff` becomes mathematically polluted with massive merge conflicts over spaces versus tabs. Black is 'uncompromising'. It takes away the developer's ability to choose. By executing Black in the Pre-Commit hook, we mathematically annihilate all formatting arguments, ensuring that every single file in the repository looks exactly like it was written by the same robot, optimizing cognitive parsing speed for the entire team."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Code Quality (Code Reviews & Mypy) Completed.")
