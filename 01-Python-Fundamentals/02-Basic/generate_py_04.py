import os

FILE_PATH = r"d:\work\python-all\01-Python-Fundamentals\02-Basic\04-functions-basics.py"

content = r'''"""
===============================================================================
PYTHON FUNDAMENTALS LABORATORY: FUNCTIONS DEEP DIVE
===============================================================================
Module: 04-functions-basics.py
Level: Advanced / Textbook-Level Laboratory Script
Estimated Time: 3-4 hours

This comprehensive laboratory manual explores the fundamental and advanced 
concepts of Python functions. Functions are the primary method of code 
organization and reuse in Python, and mastering them is essential for any 
serious Python developer.

TOPICS COVERED:
1. Anatomy of a Function & First-Class Functions
2. Positional vs. Keyword Arguments
3. Default Arguments and the "Mutable Default Trap"
4. Unpacking with *args and **kwargs
5. Scope and the LEGB Rule (Local, Enclosing, Global, Built-in)
6. The `global` and `nonlocal` Keywords
7. Closures and Factory Functions
8. Lambda (Anonymous) Functions
9. Higher-Order Functions (Map, Filter, Reduce Equivalents)
10. Active Recall and Interview Questions

Each section contains deep theoretical explanations, followed by 
executable code demonstrating the concepts, edge cases, and best practices.
Assertions are used throughout to verify expected behavior.

Let's begin!
===============================================================================
"""
import functools
import sys
from collections.abc import Callable


# =============================================================================
# SECTION 1: ANATOMY OF A FUNCTION & FIRST-CLASS FUNCTIONS
# =============================================================================
"""
In Python, a function is defined using the `def` keyword, followed by the 
function name, parentheses enclosing optional parameters, and a colon.
The function body is indented.

Crucially, functions in Python are "First-Class Citizens". This means they can be:
1. Assigned to variables or stored in data structures.
2. Passed as arguments to other functions.
3. Returned as values from other functions.

This property enables functional programming paradigms and powerful design patterns.
"""

def basic_function(name: str) -> str:
    """
    A simple function with a type hint indicating it takes a string and returns a string.
    """
    return f"Hello, {name}!"

# 1. Assigning a function to a variable
greeting_alias = basic_function
assert greeting_alias("Alice") == "Hello, Alice!"
assert greeting_alias is basic_function  # They point to the exact same object in memory

# 2. Storing functions in data structures
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b

math_operations = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply
}

assert math_operations["add"](10, 5) == 15
assert math_operations["multiply"](10, 5) == 50

# 3. Passing functions as arguments (Higher-Order Function concept)
def apply_operation(operation: Callable, x: int, y: int) -> int:
    """Applies the given operation function to x and y."""
    return operation(x, y)

assert apply_operation(add, 20, 30) == 50
assert apply_operation(subtract, 20, 30) == -10


# =============================================================================
# SECTION 2: POSITIONAL VS. KEYWORD ARGUMENTS
# =============================================================================
"""
When calling a function, arguments can be passed in two ways:
1. Positional Arguments: Mapped to parameters based on their position/order.
2. Keyword Arguments: Mapped to parameters explicitly by name.

Python 3.8+ introduced Positional-Only parameters (`/`) and 
Keyword-Only parameters (`*`) to give API designers more control.

- Parameters before `/` MUST be positional.
- Parameters after `*` MUST be keyword.
- Parameters between `/` and `*` can be either.
"""

def display_info(name, age, city):
    return f"{name} is {age} and lives in {city}."

# Positional call
assert display_info("Bob", 25, "New York") == "Bob is 25 and lives in New York."

# Keyword call (order doesn't matter)
assert display_info(city="London", name="Charlie", age=30) == "Charlie is 30 and lives in London."

# Mixed call (positional MUST come before keyword arguments)
assert display_info("Dave", city="Paris", age=40) == "Dave is 40 and lives in Paris."

# Syntax error if we put positional after keyword:
# display_info(name="Eve", 22, "Berlin") # SyntaxError: positional argument follows keyword argument

# --- Positional-Only and Keyword-Only Arguments ---
def advanced_greeting(name, /, greeting="Hello", *, punctuation="!"):
    """
    `name` is positional-only.
    `greeting` can be positional or keyword.
    `punctuation` is keyword-only.
    """
    return f"{greeting}, {name}{punctuation}"

# Valid calls
assert advanced_greeting("Frank") == "Hello, Frank!"
assert advanced_greeting("Grace", "Hi", punctuation=".") == "Hi, Grace."
assert advanced_greeting("Hank", greeting="Hey", punctuation="?") == "Hey, Hank?"

# Invalid calls (would raise TypeError):
# advanced_greeting(name="Ivy")  # TypeError: got some positional-only arguments passed as keyword arguments
# advanced_greeting("Jack", "Yo", ".")  # TypeError: takes from 1 to 2 positional arguments but 3 were given


# =============================================================================
# SECTION 3: DEFAULT ARGUMENTS AND THE MUTABLE DEFAULT TRAP
# =============================================================================
"""
Parameters can have default values. If an argument is not provided during the call,
the default is used. 

WARNING: THE MUTABLE DEFAULT TRAP!
Default arguments are evaluated ONLY ONCE, when the function is defined (at module load time),
not every time the function is called. If you use a mutable object (like a list or dict)
as a default, any modifications to it will persist across multiple calls.
"""

# The Trap
def bad_append(item, target_list=[]):
    """NEVER DO THIS. The `target_list` is shared across all calls."""
    target_list.append(item)
    return target_list

l1 = bad_append(1)
assert l1 == [1]

l2 = bad_append(2)
# You might expect l2 to be [2], but it's actually [1, 2] because the list is shared!
assert l2 == [1, 2]
assert l1 is l2  # They are exactly the same list object in memory!

# The Fix
def good_append(item, target_list=None):
    """
    Standard idiom: Use None as the default, and create the mutable object
    inside the function body if it's None.
    """
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list

l3 = good_append(1)
l4 = good_append(2)
assert l3 == [1]
assert l4 == [2]
assert l3 is not l4


# =============================================================================
# SECTION 4: UNPACKING WITH *args AND **kwargs
# =============================================================================
"""
Sometimes you don't know in advance how many arguments will be passed to your function.
Python provides `*args` and `**kwargs` to handle arbitrary numbers of arguments.

- `*args` collects extra positional arguments into a TUPLE.
- `**kwargs` collects extra keyword arguments into a DICTIONARY.

The names `args` and `kwargs` are conventions; you could use `*items` and `**options`,
but it's best to stick to the convention.
"""

def flexible_function(a, b, *args, **kwargs):
    result = {
        'a': a,
        'b': b,
        'args': args,
        'kwargs': kwargs
    }
    return result

res = flexible_function(1, 2, 3, 4, 5, x=10, y=20)
assert res['a'] == 1
assert res['b'] == 2
assert res['args'] == (3, 4, 5)  # A tuple
assert res['kwargs'] == {'x': 10, 'y': 20}  # A dictionary

# We can also use * and ** to UNPACK collections when CALLING functions
def sum_three(x, y, z):
    return x + y + z

numbers = [10, 20, 30]
# Unpacking the list into positional arguments
assert sum_three(*numbers) == 60

options = {'x': 5, 'y': 15, 'z': 25}
# Unpacking the dictionary into keyword arguments
assert sum_three(**options) == 45


# =============================================================================
# SECTION 5: SCOPE AND THE LEGB RULE
# =============================================================================
"""
Scope determines the visibility and lifetime of a variable.
When Python encounters a variable name, it searches for it in a specific order
known as the LEGB rule:

1. L - Local: Variables assigned within a function.
2. E - Enclosing (or Nonlocal): Variables in the local scope of any enclosing functions (closures).
3. G - Global: Variables assigned at the top-level of a module.
4. B - Built-in: Names preassigned in the built-in names module (e.g., `len`, `print`, `Exception`).
"""

x_global = "Global X"

def outer_scope_test():
    x_outer = "Enclosing X"
    
    def inner_scope_test():
        x_inner = "Local X"
        
        # Inner function has access to Local, Enclosing, and Global
        assert x_inner == "Local X"
        assert x_outer == "Enclosing X"
        assert x_global == "Global X"
        
        # It also has access to Built-ins
        assert isinstance(len, type(len)) 
        
    inner_scope_test()

outer_scope_test()

# Variable Shadowing
# An inner scope variable can 'shadow' (hide) a variable from an outer scope
# if they share the same name.

shadow_var = "Global"

def test_shadow():
    shadow_var = "Local"  # This shadows the global shadow_var
    assert shadow_var == "Local"

test_shadow()
assert shadow_var == "Global"  # Global was not modified


# =============================================================================
# SECTION 6: THE `global` AND `nonlocal` KEYWORDS
# =============================================================================
"""
By default, if you assign a value to a variable inside a function, Python treats it 
as a local variable. If you want to modify a variable from a broader scope, you 
must explicitly declare your intent using `global` or `nonlocal`.

- `global`: Tells Python to look for the variable in the module's global scope.
- `nonlocal` (Python 3+): Tells Python to look for the variable in the nearest 
  enclosing scope (excluding global).
"""

counter_global = 0

def increment_global():
    # counter_global += 1  # UnboundLocalError! Python thinks this is local because of the assignment.
    
    global counter_global
    counter_global += 1

increment_global()
increment_global()
assert counter_global == 2


def counter_factory():
    count = 0  # Enclosing scope variable
    
    def increment():
        # count += 1 # UnboundLocalError again!
        nonlocal count
        count += 1
        return count
        
    return increment

my_counter = counter_factory()
assert my_counter() == 1
assert my_counter() == 2
assert my_counter() == 3


# =============================================================================
# SECTION 7: CLOSURES AND FACTORY FUNCTIONS
# =============================================================================
"""
A closure occurs when a nested function captures and remembers the variables 
from its enclosing scope, even after the outer function has finished executing.

This is a powerful concept used for data hiding, state retention, and decorators.
The `counter_factory` in the previous section is an example of a closure.
"""

def power_factory(exponent):
    """
    Returns a function that raises a number to the given exponent.
    The `exponent` variable is "captured" in the closure of the inner function.
    """
    def power(base):
        return base ** exponent
    
    return power

square = power_factory(2)
cube = power_factory(3)

# The outer function `power_factory` has completed, but `square` and `cube` 
# still remember their respective `exponent` values!
assert square(4) == 16
assert cube(4) == 64

# Inspecting the closure
# Python stores closed-over variables in the `__closure__` attribute
assert square.__closure__[0].cell_contents == 2
assert cube.__closure__[0].cell_contents == 3


# =============================================================================
# SECTION 8: LAMBDA (ANONYMOUS) FUNCTIONS
# =============================================================================
"""
Lambda functions are small, anonymous (unnamed) inline functions defined using 
the `lambda` keyword. 

Syntax: `lambda arguments: expression`

- They can take any number of arguments.
- They can only contain a SINGLE expression.
- They inherently return the result of that expression (no `return` keyword needed).
- They are often used for short, throwaway functions, especially as arguments 
  to higher-order functions like `sort()`, `map()`, or `filter()`.
"""

# Equivalent to: def add(x, y): return x + y
lambda_add = lambda x, y: x + y
assert lambda_add(5, 7) == 12

# Common use case: Custom sorting
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

# Sort by age using a lambda
users_sorted_by_age = sorted(users, key=lambda user: user["age"])
assert users_sorted_by_age[0]["name"] == "Bob"
assert users_sorted_by_age[-1]["name"] == "Charlie"


# =============================================================================
# SECTION 9: HIGHER-ORDER FUNCTIONS (MAP, FILTER, REDUCE EQUIVALENTS)
# =============================================================================
"""
A higher-order function is a function that either:
1. Takes one or more functions as arguments.
2. Returns a function as its result.

Python has built-in higher-order functions like `map()` and `filter()`, and 
`reduce()` in the `functools` module. While list comprehensions are often preferred
in modern Python, understanding these concepts is crucial.
"""

numbers = [1, 2, 3, 4, 5]

# --- 1. map(function, iterable) ---
# Applies the function to every item in the iterable. Returns an iterator.
squared_iterator = map(lambda x: x ** 2, numbers)
squared_list = list(squared_iterator)
assert squared_list == [1, 4, 9, 16, 25]

# Equivalent list comprehension: [x**2 for x in numbers]

# --- 2. filter(function, iterable) ---
# Filters the iterable, keeping only elements where the function returns True.
evens_iterator = filter(lambda x: x % 2 == 0, numbers)
evens_list = list(evens_iterator)
assert evens_list == [2, 4]

# Equivalent list comprehension: [x for x in numbers if x % 2 == 0]

# --- 3. functools.reduce(function, iterable) ---
# Applies a rolling computation to sequential pairs of values in the iterable.
# For example, to sum a list: (((1+2)+3)+4)+5
total_sum = functools.reduce(lambda acc, x: acc + x, numbers)
assert total_sum == 15

total_product = functools.reduce(lambda acc, x: acc * x, numbers)
assert total_product == 120


# =============================================================================
# SECTION 10: ACTIVE RECALL & INTERVIEW QUESTIONS
# =============================================================================
"""
Test your knowledge with these common interview questions regarding functions.

Q1: What is the "Mutable Default Trap" and how do you avoid it?
A1: Default arguments are evaluated only once at definition time. If you use a 
    mutable object like `[]` or `{}`, the same instance is shared across all calls 
    that omit that argument. To avoid it, use `None` as the default and initialize 
    the mutable object inside the function body.

Q2: Explain the difference between `global` and `nonlocal`.
A2: `global` allows modification of a variable in the module's top-level scope.
    `nonlocal` allows modification of a variable in the nearest enclosing scope 
    (used inside closures/nested functions), but it stops searching before the global scope.

Q3: What does `*args` and `**kwargs` do in a function definition?
A3: `*args` captures all excess positional arguments into a tuple.
    `**kwargs` captures all excess keyword arguments into a dictionary.

Q4: Can a lambda function contain multiple statements (like an `if...else` block and a `for` loop)?
A4: No. Lambda functions are restricted to a single expression. You can use a 
    conditional expression (`x if condition else y`), but you cannot use full 
    statement blocks or loops.

Q5: Describe the LEGB rule.
A5: It is the order Python resolves variable names:
    Local (current function) -> 
    Enclosing (any enclosing functions) -> 
    Global (module level) -> 
    Built-in (Python's predefined names).
"""

# Edge Case Puzzle: Lambda in a loop (Late Binding)
def create_multipliers():
    """
    Common interview trap.
    You might expect [0, 1, 2, 3, 4], but you get [4, 4, 4, 4, 4].
    Why? Because lambdas use late binding. The variable `i` is looked up 
    when the lambda is CALLED, not when it is defined. By the time it is called,
    the loop has finished and `i` is 4.
    """
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)
    return multipliers

mults = create_multipliers()
assert mults[0](1) == 4  # Trap! Not 0
assert mults[2](1) == 4  # Trap! Not 2

# How to fix it? Capture `i` eagerly using a default argument.
def create_multipliers_fixed():
    multipliers = []
    for i in range(5):
        # i=i evaluates the current value of i at definition time
        multipliers.append(lambda x, i=i: x * i)
    return multipliers

mults_fixed = create_multipliers_fixed()
assert mults_fixed[0](1) == 0
assert mults_fixed[2](1) == 2
assert mults_fixed[4](1) == 4

print("All assertions passed. The Functions Deep Dive Laboratory is complete!")
'''

os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Generated and written to target file successfully.")
