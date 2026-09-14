"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - BASICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When interviewing for a Python-heavy role (Backend Engineer, Data Engineer),
# solving algorithmic problems is not enough. Interviewers will relentlessly 
# grill you on the deep internal mechanics of the Python language itself to 
# separate senior developers from beginners who just memorized syntax.
#
# A junior developer says: "A list is mutable, a tuple is immutable."
# A senior developer says: "Because a tuple is immutable, CPython statically 
# allocates its memory at compile time and calculates its hash, allowing it to 
# be used as a Dictionary Key. Lists require dynamic overallocation and cannot 
# be hashed."
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Identity (`is`) vs Equality (`==`) (The Integer Caching Trap).
# - Master Mutability (The Mutable Default Argument Trap).
# - Understand List comprehensions vs Generator expressions.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IDENTITY (`is`) VS EQUALITY (`==`)
# ==============================================================================
def demonstrate_is_vs_equals():
    section_header("Identity (`is`) vs Equality (`==`)")
    
    print("1. Equality (`==`) compares the mathematical VALUES.")
    print("2. Identity (`is`) compares the physical MEMORY ADDRESSES (Pointers).")
    
    list_a = [1, 2, 3]
    list_b = [1, 2, 3]
    
    print(f"\nlist_a = {list_a}")
    print(f"list_b = {list_b}")
    print(f"list_a == list_b : {list_a == list_b} (Same Values)")
    print(f"list_a is list_b : {list_a is list_b} (Different Memory Addresses!)")
    
    # THE CPYTHON INTEGER CACHING TRAP
    print("\n--- THE CPYTHON CACHE TRAP ---")
    print("CPython pre-caches small integers (-5 to 256) in memory at startup!")
    
    a = 100
    b = 100
    print(f"a = 100, b = 100")
    print(f"a is b : {a is b} (Because 100 is inside the cached range [-5, 256])")
    
    x = 1000
    y = 1000
    print(f"\nx = 1000, y = 1000")
    print(f"x is y : {x is y} (Because 1000 is NOT cached. CPython allocates two separate memory blocks!)")


# ==============================================================================
# 4. THE MUTABLE DEFAULT ARGUMENT TRAP
# ==============================================================================
def bad_append(element: int, target_list: list = []) -> list:
    """
    FATAL FLAW! 
    Default arguments are evaluated exactly ONCE at *function definition time* 
    (when the Python script is first read by the interpreter), NOT every time 
    the function is called!
    """
    target_list.append(element)
    return target_list

def good_append(element: int, target_list: list = None) -> list:
    """
    Correct way! 
    `None` is immutable. We create a fresh list at *function execution time*.
    """
    if target_list is None:
        target_list = []
    target_list.append(element)
    return target_list

def demonstrate_mutable_defaults():
    section_header("The Mutable Default Argument Trap")
    
    print("Executing `bad_append(1)`:")
    print(bad_append(1))
    
    print("Executing `bad_append(2)` (Expecting [2], but getting something terrifying...):")
    print(bad_append(2))
    
    print("Executing `bad_append(3)`:")
    print(bad_append(3))
    
    print("\nWhy? The `target_list=[]` was created ONCE when the script started.")
    print("Every time you call the function without a list, it reuses that EXACT SAME ")
    print("physical memory block! You are silently leaking data across function calls.")
    
    print("\nExecuting `good_append(1)`:")
    print(good_append(1))
    print("Executing `good_append(2)`:")
    print(good_append(2))


# ==============================================================================
# 5. LIST COMPREHENSIONS VS GENERATOR EXPRESSIONS
# ==============================================================================
import sys

def demonstrate_comprehensions():
    section_header("List Comprehensions vs Generators")
    
    print("Both synthesize data sequentially. The difference is Memory (RAM).")
    
    # 1. List Comprehension (Brackets [])
    # EAGER evaluation. Calculates all 100,000 items instantly and stores them in RAM.
    list_comp = [x * 2 for x in range(100_000)]
    
    # 2. Generator Expression (Parentheses ())
    # LAZY evaluation. Returns a State Machine object that calculates ONE item at a time.
    gen_expr = (x * 2 for x in range(100_000))
    
    print(f"\nMemory used by List Comprehension : {sys.getsizeof(list_comp):>8} bytes")
    print(f"Memory used by Generator Expression : {sys.getsizeof(gen_expr):>8} bytes")
    print("\nThe Generator uses O(1) memory, regardless of whether you request ")
    print("10 items or 10 Trillion items!")


def run_all_labs():
    demonstrate_is_vs_equals()
    demonstrate_mutable_defaults()
    demonstrate_comprehensions()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the difference between a List and a Tuple in Python?"
   Senior Answer: "The primary difference is mutability. Lists are mutable; they can grow and shrink dynamically. To support this, CPython over-allocates memory for Lists. Tuples are strictly immutable. Because their size is permanently fixed at creation, CPython allocates their exact memory mathematically, making them much faster and lighter. Furthermore, because Tuples are immutable, their internal state can be mathematically hashed into a unique integer (`hash()`), which means Tuples can be used as Keys in a Dictionary. Lists cannot be hashed and will instantly throw a `TypeError` if used as a Dictionary Key."

2. Interviewer: "I wrote `def add_user(user, db=[]):`. My users are showing up in other people's sessions. Why?"
   Senior Answer: "You fell into the Mutable Default Argument Trap. In Python, default arguments are physically evaluated and allocated in RAM exactly *once* when the `def` keyword is parsed by the interpreter at startup. That `[]` list is permanently anchored to the function object itself. Every time you call `add_user` without providing a `db` argument, it injects the new user into that exact same, globally-shared list object in memory, causing a massive cross-session data leak. To fix it, you must write `db=None`, and then inside the function evaluate `if db is None: db = []`. This guarantees a brand new, isolated list is allocated dynamically at *execution time*."

3. Interviewer: "Explain when you would use a Generator Expression `(...)` instead of a List Comprehension `[...]`."
   Senior Answer: "If I need to mathematically slice the data, reverse it, jump around indexes (`data[5]`), or iterate over it multiple times, I MUST use a List Comprehension because the data must be physically manifested in RAM to support random access. However, if I am processing a 500GB log file and I only need to iterate straight forward through it *once* to calculate a sum, using a List Comprehension will instantly trigger an Out-Of-Memory (OOM) crash. I must use a Generator Expression, which uses strictly $O(1)$ memory by yielding and garbage-collecting exactly one item at a time, completely bypassing RAM limits."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Python Basics) Completed.")
