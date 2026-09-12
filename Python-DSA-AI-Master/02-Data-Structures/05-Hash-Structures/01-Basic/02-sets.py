"""
## A. Concept Name
Sets and Mathematical Set Operations

## B. One-Sentence Definition
A set is an unordered collection of distinct, hashable objects that supports fast membership testing and mathematical operations like union and intersection.

## C. Why Does This Exist?
To efficiently manage collections of unique items and perform mathematical set operations natively, optimizing lookups to O(1) compared to O(N) for lists.

## D. Intuition
Imagine a VIP club where everyone must have a unique ID to enter. If you try to enter with an ID already inside, you are ignored. Also, the club doesn't care what order people stand in, just whether they are inside or not.

## E. Real-Life Analogy
A collection of distinct ingredients needed for a recipe. Having "salt" written twice on your list doesn't mean you have two types of salt; you simply have salt. When combining lists from two chefs, you merge duplicates to form a single master ingredient list.

## F. Mental Model
Dictionary keys without the values. Under the hood, a set is just a hash table containing only keys.

## G. Visual Explanation
Adding to Set {1, 2, 3}:
add(2) -> {1, 2, 3} (already exists, ignored)
add(4) -> {1, 2, 3, 4}

Union A | B:
A = {1, 2}
B = {2, 3}
A | B -> {1, 2, 3}

## H. Formal Explanation
In Python, a `set` is a mutable, unordered collection of immutable (hashable) items. Its implementation relies on a hash table, ensuring average-case O(1) time complexity for additions, removals, and membership checks. Set operations (union, intersection, difference, symmetric difference) map directly to their formal mathematical definitions.

## I. Mathematical Foundation
Sets represent mathematical sets. Let A and B be sets:
- Union (A ∪ B): elements in A or B
- Intersection (A ∩ B): elements in both A and B
- Difference (A \ B): elements in A but not in B
- Symmetric Difference (A ∆ B): elements in A or B, but not both

## J. From-Scratch Implementation
(See code below)

## K. Library / Production Implementation
Python has the built-in `set` (mutable) and `frozenset` (immutable).

## L. Trace (walk through example)
1. s = {1, 2}
2. s.add(2) -> hash(2) exists, ignore. s is {1, 2}
3. s.add(3) -> hash(3) is new, add. s is {1, 2, 3}
4. 2 in s -> hash(2) checked -> O(1) returns True.

## M. Complexity
- Time Complexity:
  - Add/Remove/Search: O(1) average, O(N) worst case (due to hash collisions).
  - Union: O(len(s1) + len(s2))
  - Intersection: O(min(len(s1), len(s2)))
- Space Complexity: O(N) where N is the number of elements.

## N. Common Mistakes
- Using `{}` to create an empty set. This creates an empty dictionary. Use `set()` instead.
- Trying to add mutable (unhashable) elements like lists or dictionaries to a set, which raises a `TypeError`.
- Relying on the order of items in a set (sets are unordered).

## O. Common Confusions
- "Set vs Frozenset": `set` is mutable (you can add/remove items), but unhashable. `frozenset` is immutable and hashable, allowing it to be used as a dictionary key or an element in another set.

## P. When To Use
- Removing duplicates from a list.
- Fast membership testing (checking if an element exists in a collection).
- Finding common or differing elements between multiple collections.

## Q. When NOT To Use
- When the order of elements matters (use a list or tuple).
- When you need to associate values with keys (use a dictionary).
- When elements are unhashable (e.g., lists of lists).

## R. Trade-offs
- Time vs Space: Sets provide O(1) lookups but consume more memory than lists due to the underlying hash table overhead.

## S. Debugging
- If you get `TypeError: unhashable type: 'list'`, you are trying to put a list inside a set. Convert the inner list to a tuple.

## T. Memory Hook
"Set = Unique & Unordered." Think of it as a bag of unique marbles.

## U. Active Recall
1. How do you initialize an empty set?
2. What is the time complexity of checking if an item is in a set vs a list?
3. Why can't you add a list to a set?

## V. Practice
- Longest Consecutive Sequence (LeetCode #128)
- Intersection of Two Arrays (LeetCode #349)

## W. Interview Question
"Given an unsorted array of integers, how would you find the length of the longest consecutive elements sequence in O(N) time?" (Solution below uses a set for O(1) lookups).

## X. Project Connection
In Machine Learning or Data Engineering pipelines, sets are often used to find unique categorical values, track processed items to avoid duplicate work, and quickly filter out invalid IDs using set differences.
"""

from typing import Set, List, Any

# ---------------------------------------------------------
# Basic Implementation: Creating and Using Sets
# ---------------------------------------------------------

def basic_set_operations() -> None:
    """Demonstrates basic set creation and manipulation."""
    
    # Creation
    my_set: Set[int] = {1, 2, 3, 4, 4, 5} # Duplicates are automatically removed
    assert len(my_set) == 5
    
    empty_set = set() # Note: {} creates an empty dictionary, not an empty set!
    
    # Adding and Removing
    my_set.add(6)
    assert 6 in my_set
    
    my_set.remove(6) # Raises KeyError if not found
    my_set.discard(99) # Removes if present, does nothing if not found (safer)
    
    popped_element = my_set.pop() # Removes and returns an arbitrary element
    
    my_set.clear() # Empties the set
    assert len(my_set) == 0

# ---------------------------------------------------------
# Professional Implementation: Mathematical Operations
# ---------------------------------------------------------

def find_common_elements(list1: List[Any], list2: List[Any]) -> List[Any]:
    """
    Finds common elements between two lists using sets for optimal performance.
    
    Time Complexity: O(N + M) where N and M are the lengths of the lists.
    Space Complexity: O(N + M) to store the sets.
    """
    # Convert lists to sets to unlock O(1) lookups and set math
    set1 = set(list1)
    set2 = set(list2)
    
    # Intersection (&): Elements present in BOTH sets
    common_set = set1.intersection(set2) # or set1 & set2
    return list(common_set)

def advanced_set_math() -> None:
    """Demonstrates advanced mathematical set operations."""
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}
    
    # Union (|): Elements in A, or B, or both
    assert a.union(b) == {1, 2, 3, 4, 5, 6}
    assert (a | b) == {1, 2, 3, 4, 5, 6}
    
    # Intersection (&): Elements in both A and B
    assert a.intersection(b) == {3, 4}
    assert (a & b) == {3, 4}
    
    # Difference (-): Elements in A but NOT in B
    assert a.difference(b) == {1, 2}
    assert (a - b) == {1, 2}
    
    # Symmetric Difference (^): Elements in A or B, but NOT both
    assert a.symmetric_difference(b) == {1, 2, 5, 6}
    assert (a ^ b) == {1, 2, 5, 6}
    
    # Subsets and Supersets
    c = {1, 2}
    assert c.issubset(a)   # True, all elements of c are in a
    assert a.issuperset(c) # True, a contains all elements of c

# ---------------------------------------------------------
# Advanced Concept: Frozensets
# ---------------------------------------------------------
def demonstrate_frozenset() -> None:
    """
    frozenset is an immutable version of a Python set.
    Because it is immutable, it is hashable. 
    This means a frozenset can be used as a key in a dictionary or an element in another set.
    """
    immutable_set = frozenset([1, 2, 3])
    
    # immutable_set.add(4)  <-- This would raise an AttributeError
    
    # We can use it as a dictionary key!
    graph_edges = {
        frozenset(["A", "B"]): 5, # Distance between A and B is 5 (undirected edge)
        frozenset(["B", "C"]): 10
    }
    
    # Order doesn't matter for the lookup!
    assert graph_edges[frozenset(["B", "A"])] == 5

# ---------------------------------------------------------
# Interview Challenge: Longest Consecutive Sequence
# ---------------------------------------------------------
def longest_consecutive(nums: List[int]) -> int:
    """
    Given an unsorted array of integers, return the length of the longest consecutive elements sequence.
    You must write an algorithm that runs in O(N) time.
    
    Example: [100, 4, 200, 1, 3, 2] -> 4 (Sequence is [1, 2, 3, 4])
    
    Explanation: By converting the array to a set, we get O(1) lookups.
    We iterate through the set. We only start building a sequence if the current number is the
    START of a sequence (i.e., `num - 1` is not in the set). This prevents redundant counting.
    """
    num_set = set(nums)
    longest_streak = 0
    
    for num in num_set:
        # Check if it's the start of a sequence
        if (num - 1) not in num_set:
            current_num = num
            current_streak = 1
            
            # Count upwards
            while (current_num + 1) in num_set:
                current_num += 1
                current_streak += 1
                
            longest_streak = max(longest_streak, current_streak)
            
    return longest_streak


if __name__ == "__main__":
    print("Running Set basic operations...")
    basic_set_operations()
    
    print("Running Set math operations...")
    advanced_set_math()
    
    print("Running Frozenset demonstration...")
    demonstrate_frozenset()
    
    print("Running Interview Challenge: Longest Consecutive Sequence...")
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    
    print("All tests passed successfully!")
