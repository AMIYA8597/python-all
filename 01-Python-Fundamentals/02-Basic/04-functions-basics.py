"""
# ==============================================================================
# LABORATORY 04: FUNCTIONS, SCOPE, AND CLOSURES
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In Python, functions are "first-class citizens" (objects). Understanding how 
# to pass functions around, unpack arguments (*args, **kwargs), manage the LEGB 
# scope rule, and construct closures is required for writing decorators, 
# callbacks in async code, and functional programming pipelines.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Positional, Keyword, and Keyword-Only arguments.
# - Master argument unpacking (*args, **kwargs).
# - Understand First-Class Functions and Higher-Order Functions.
# - Master the LEGB Rule (Local, Enclosing, Global, Built-in).
# - Understand closures and the `nonlocal` vs `global` keywords.
# - Learn when to use `lambda` functions (and when not to).
#
# ==============================================================================
"""

import sys
from typing import Callable, Any, List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

# ==============================================================================
# 3. ARGUMENTS: POSITIONAL, KEYWORD, AND FORCED KEYWORD
# ==============================================================================

# Normal function
def create_user(name: str, age: int, is_admin: bool = False):
    print(f"Created: {name}, Age: {age}, Admin: {is_admin}")

# Python 3+ allows FORCING keyword arguments by using a bare '*'
def create_user_strict(name: str, *, age: int, is_admin: bool = False):
    """
    The '*' means: Every argument after this point MUST be passed as a keyword 
    argument. This prevents bugs where someone accidentally passes a bool 
    to the wrong positional slot.
    """
    print(f"Strict Created: {name}, Age: {age}, Admin: {is_admin}")

# Python 3.8+ allows FORCING positional-only arguments using '/'
def add_coordinates(x: int, y: int, /, z: int = 0):
    """
    The '/' means: Every argument before this point MUST be passed positionally.
    You cannot do `add_coordinates(x=10, y=20)`.
    This is used heavily in C-extensions and the standard library.
    """
    print(f"Coordinates: {x}, {y}, {z}")

def demonstrate_arguments():
    section_header("Argument Types")
    
    create_user("Alice", 30) # Positional
    create_user(name="Bob", age=40, is_admin=True) # Keyword
    
    # create_user_strict("Charlie", 25) # ERROR: TypeError (age must be keyword)
    create_user_strict("Charlie", age=25)
    
    # add_coordinates(x=10, y=20) # ERROR: x and y are positional-only
    add_coordinates(10, 20, z=30)


# ==============================================================================
# 4. UNPACKING: *ARGS AND **KWARGS
# ==============================================================================

def calculate_sum(title: str, *args: int, **kwargs: str):
    """
    *args captures remaining positional arguments as a TUPLE.
    **kwargs captures remaining keyword arguments as a DICT.
    """
    print(f"Title: {title}")
    print(f"args (Tuple): {args}")
    print(f"kwargs (Dict): {kwargs}")
    
    total = sum(args)
    print(f"Sum: {total}")

def demonstrate_unpacking():
    section_header("*args and **kwargs")
    
    calculate_sum("My Sum", 1, 2, 3, 4, 5, mode="fast", user="admin")
    
    # Unpacking lists and dicts INTO a function call
    nums = [10, 20, 30]
    config = {"mode": "slow", "debug": "true"}
    
    print("\nUnpacking variables directly into function:")
    # *nums unpacks the list into positional arguments
    # **config unpacks the dict into keyword arguments
    calculate_sum("Unpacked", *nums, **config)


# ==============================================================================
# 5. FIRST-CLASS FUNCTIONS & HIGHER ORDER
# ==============================================================================

def shout(text: str) -> str:
    return text.upper() + "!!!"

def whisper(text: str) -> str:
    return text.lower() + "..."

def apply_transformation(func: Callable[[str], str], text: str) -> str:
    """This is a higher-order function because it accepts a function as an arg."""
    return func(text)

def demonstrate_first_class():
    section_header("First-Class Functions")
    
    # We can assign a function to a variable (no parentheses!)
    my_func = shout
    print(my_func("hello"))
    
    # We can pass functions to other functions
    print(apply_transformation(whisper, "HELLO THERE"))


# ==============================================================================
# 6. SCOPE: THE LEGB RULE
# ==============================================================================
"""
Python resolves variables by checking scopes in this exact order:
1. Local (L) - Inside the current function.
2. Enclosing (E) - Inside enclosing functions (if nested).
3. Global (G) - At the top level of the module.
4. Built-in (B) - Python's built-in names (print, len, Exception).
"""

GLOBAL_VAR = "I am Global"

def outer_function():
    enclosing_var = "I am Enclosing"
    
    def inner_function():
        local_var = "I am Local"
        # Can read all three!
        print(f"Inner sees: {local_var}, {enclosing_var}, {GLOBAL_VAR}")
        
    inner_function()

def demonstrate_scope():
    section_header("Scope & LEGB Rule")
    outer_function()


# ==============================================================================
# 7. MUTATING SCOPE: global AND nonlocal
# ==============================================================================

counter = 0

def increment_global():
    # To modify a global variable, you MUST declare it global.
    # Otherwise, Python creates a local shadow variable.
    global counter
    counter += 1

def run_counter():
    internal_count = 0
    
    def increment_internal():
        # To modify an enclosing variable, use nonlocal.
        nonlocal internal_count
        internal_count += 1
        
    increment_internal()
    increment_internal()
    print(f"Internal count modified via nonlocal: {internal_count}")

def demonstrate_scope_mutation():
    section_header("Scope Mutation (global / nonlocal)")
    
    increment_global()
    print(f"Global counter: {counter}")
    
    run_counter()


# ==============================================================================
# 8. CLOSURES
# ==============================================================================

def make_multiplier(n: int) -> Callable[[int], int]:
    """
    A closure occurs when a nested function captures and remembers the variables 
    from its enclosing scope, even AFTER the enclosing function has finished execution!
    """
    def multiplier(x: int) -> int:
        return x * n  # 'n' is captured from the enclosing scope
    return multiplier

def demonstrate_closures():
    section_header("Closures")
    
    times_3 = make_multiplier(3)
    times_5 = make_multiplier(5)
    
    # Even though make_multiplier has finished, times_3 remembers n=3
    print(f"times_3(10) = {times_3(10)}")
    print(f"times_5(10) = {times_5(10)}")
    
    # We can inspect the closure cells!
    print(f"Closure data for times_3: {times_3.__closure__[0].cell_contents}")


# ==============================================================================
# 9. LAMBDA FUNCTIONS
# ==============================================================================

def demonstrate_lambdas():
    """
    Lambdas are anonymous, single-expression functions.
    They are mainly used for passing a short function to sort(), map(), or filter().
    """
    section_header("Lambda Functions")
    
    users = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35}
    ]
    
    # Sort the dictionary by age using a lambda
    users_sorted = sorted(users, key=lambda u: u["age"])
    print("Users sorted by age:")
    for u in users_sorted:
        print(f"  {u}")
        
    # Map example
    nums = [1, 2, 3, 4]
    squares = list(map(lambda x: x**2, nums))
    print(f"\nSquares via map/lambda: {squares}")


# ==============================================================================
# 10. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the LEGB rule.
   Answer: Local, Enclosing, Global, Built-in. It is the order Python searches for a variable name.

2. What is the difference between *args and **kwargs?
   Answer: *args packs positional arguments into a tuple. **kwargs packs keyword arguments into a dictionary.

3. What is a closure?
   Answer: A function that remembers the state of its enclosing scope even after the outer function has finished executing.

4. When do you use `global` vs `nonlocal`?
   Answer: Use `global` to modify a module-level variable from inside a function. Use `nonlocal` to modify a variable in an outer (but non-global) nested function.

5. What does the `*` do in `def func(a, *, b):`?
   Answer: It forces `b` to be passed as a keyword argument (e.g. `func(1, b=2)`). `func(1, 2)` will raise a TypeError.
"""

if __name__ == "__main__":
    demonstrate_arguments()
    demonstrate_unpacking()
    demonstrate_first_class()
    demonstrate_scope()
    demonstrate_scope_mutation()
    demonstrate_closures()
    demonstrate_lambdas()
    print("\n[SUCCESS] Laboratory 04 Completed.")
