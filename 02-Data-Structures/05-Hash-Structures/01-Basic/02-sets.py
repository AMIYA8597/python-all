"""
# ==============================================================================
# LABORATORY: SETS AND MATHEMATICAL OPERATIONS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You've learned that Hash Tables allow O(1) lookups by mapping a Key to a Value.
# But what if you don't care about the Value? What if you just want to know:
# "Has this user ID been seen before?" or "Which followers do Account A and 
# Account B have in common?"
#
# A `set` is literally a Hash Table where the Values are ignored. Because it uses 
# hashing, lookups, insertions, and deletions are strictly O(1) time.
# Furthermore, Python's `set` is heavily optimized in C to perform mathematical 
# operations (Union, Intersection, Difference) incredibly fast using bitwise-style 
# logic under the hood.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how a `set` operates as a key-only Hash Table.
# - Master mathematical set operations (`|`, `&`, `-`, `^`).
# - Understand the difference between `set` and `frozenset`.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. SET BASICS & HASHABILITY
# ==============================================================================
def demonstrate_set_basics():
    section_header("Concept: Hashability & Set Basics")
    
    # Sets only allow UNIQUE elements.
    my_set = {1, 2, 2, 3, 3, 3}
    print(f"Creating {{1, 2, 2, 3, 3, 3}} results in: {my_set}")
    
    print("\nBecause sets use Hash Tables, every element MUST be 'Hashable' (Immutable).")
    print("You can add strings, ints, floats, and tuples:")
    valid_set = {"Alice", 42, (1, 2)}
    print(f"Valid set: {valid_set}")
    
    try:
        print("\nBut if you try to add a list (mutable):")
        invalid_set = {[1, 2]}
    except TypeError as e:
        print(f"TypeError caught: {e}")
        print("Lists cannot be hashed because if you modify the list later, its hash changes, breaking the Hash Table's underlying array indexing!")


# ==============================================================================
# 4. MATHEMATICAL SET OPERATIONS
# ==============================================================================
def demonstrate_set_math():
    section_header("Algorithm: Mathematical Set Operations")
    
    # Imagine two groups of software engineers based on their skills
    python_devs = {"Alice", "Bob", "Charlie", "David"}
    java_devs = {"Charlie", "David", "Eve", "Frank"}
    
    print(f"Python Devs: {python_devs}")
    print(f"Java Devs  : {java_devs}")
    
    # 1. UNION (|)
    # Combines both sets, keeping only unique elements. Time: O(len(A) + len(B))
    all_devs = python_devs | java_devs
    print(f"\nUnion (A | B) - All developers:")
    print(f"  {all_devs}")
    
    # 2. INTERSECTION (&)
    # Elements present in BOTH sets. Time: O(min(len(A), len(B)))
    fullstack_devs = python_devs & java_devs
    print(f"\nIntersection (A & B) - Developers who know both:")
    print(f"  {fullstack_devs}")
    
    # 3. DIFFERENCE (-)
    # Elements in the first set, but NOT in the second. Time: O(len(A))
    pure_python = python_devs - java_devs
    print(f"\nDifference (A - B) - Developers who ONLY know Python:")
    print(f"  {pure_python}")
    
    # 4. SYMMETRIC DIFFERENCE (^)
    # Elements in exactly ONE of the sets (Excludes the intersection).
    one_language = python_devs ^ java_devs
    print(f"\nSymmetric Difference (A ^ B) - Developers who know exactly one language:")
    print(f"  {one_language}")


# ==============================================================================
# 5. SUBSETS AND SUPERSETS
# ==============================================================================
def demonstrate_subset_logic():
    section_header("Algorithm: Subsets and Supersets")
    
    # Imagine required permissions for an admin role
    required_permissions = {"read", "write", "delete"}
    
    user1_permissions = {"read", "write"}
    user2_permissions = {"read", "write", "delete", "execute"}
    
    print(f"Required: {required_permissions}")
    print(f"User 1  : {user1_permissions}")
    print(f"User 2  : {user2_permissions}")
    
    # `issubset` (<=) checks if all elements of A are inside B
    # `issuperset` (>=) checks if A contains all elements of B
    
    print("\nChecking if users meet the requirements:")
    print(f"Does User 1 have all required permissions? (Is Required a subset of User 1?)")
    print(f"  {required_permissions.issubset(user1_permissions)}") # False
    
    print(f"\nDoes User 2 have all required permissions? (Is Required a subset of User 2?)")
    print(f"  {required_permissions.issubset(user2_permissions)}") # True
    
    print(f"\nAlternatively, does User 2's permissions SUPERSET the requirements?")
    print(f"  {user2_permissions.issuperset(required_permissions)}") # True


# ==============================================================================
# 6. FROZEN SETS
# ==============================================================================
def demonstrate_frozenset():
    section_header("Concept: Frozensets (Immutable Sets)")
    
    print("A `set` is mutable (you can add/remove elements). Therefore, a `set`")
    print("itself CANNOT be used as a key in a dictionary, nor can it be placed")
    print("inside another set!")
    
    try:
        set_of_sets = {{1, 2}, {3, 4}}
    except TypeError as e:
        print(f"\nTypeError caught: {e}")
        
    print("\nTo fix this, Python provides `frozenset`. It is a set that can NEVER")
    print("be changed after creation. Because it is immutable, it is HASHABLE!")
    
    fs1 = frozenset([1, 2])
    fs2 = frozenset([3, 4])
    
    set_of_frozensets = {fs1, fs2}
    print(f"\nSuccessfully created a set of frozensets: {set_of_frozensets}")
    
    print("\nYou can also use a frozenset as a dictionary key:")
    matrix_cache = {
        frozenset(["A", "B"]): "Path Exists",
        frozenset(["B", "C"]): "Path Missing"
    }
    print(f"Cache lookup for A-B link: {matrix_cache[frozenset(['B', 'A'])]}")
    print("(Notice how the order 'B', 'A' didn't matter because it's a set!)")


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does `A & B` (Intersection) take O(min(len(A), len(B))) time?
   Answer: Python optimizes the intersection by iterating through the SMALLER set. For each element in the smaller set, it performs an O(1) Hash Table lookup in the LARGER set. Thus, the time is bound strictly by the size of the smaller set.

2. What is the difference between `add()` and `update()` on a set?
   Answer: `add(x)` inserts a single element `x` into the set. `update([x, y, z])` takes an iterable (like a list) and adds all of its elements to the set (effectively a Union).

3. Why would you use a `frozenset` as a dictionary key instead of a tuple?
   Answer: A tuple is ordered. `("A", "B")` is a different key than `("B", "A")`. If you are caching the distance between two cities, the direction doesn't matter. By using a `frozenset(["A", "B"])`, both `("A", "B")` and `("B", "A")` will hash to the exact same dictionary key instantly!
"""

if __name__ == "__main__":
    demonstrate_set_basics()
    demonstrate_set_math()
    demonstrate_subset_logic()
    demonstrate_frozenset()
    print("\n[SUCCESS] Laboratory: Sets and Math Completed.")
