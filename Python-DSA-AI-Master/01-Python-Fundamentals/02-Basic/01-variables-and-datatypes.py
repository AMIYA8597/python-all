"""
# 01 - Python Variables, References, and Data Types

## A. Concept Name
Python Variables, References, and Data Types

## B. One-Sentence Definition
In Python, variables are not buckets that hold data, but rather named references (tags) that point to objects residing in memory.

## C. Why Does This Exist?
A program needs to store, label, and retrieve information. Variables provide a human-readable way to access computer memory, while data types tell the computer what operations are safely allowed on that memory.

## D. Intuition
In languages like C, a variable is like a physical box of a specific size where you put a value. 
In Python, a variable is like a sticky note with a name written on it. You take this sticky note and slap it onto an object (the data) that lives in a giant warehouse (the heap). You can have multiple sticky notes attached to the exact same object.

## E. Real-Life Analogy
Imagine a car (the object). You might call it "my_car" (variable 1). Your spouse might call it "our_car" (variable 2). Both names refer to the exact same physical car. If the car gets painted red, both "my_car" and "our_car" will now be red, because there is only one car.

## F. Mental Model
Variable = Name/Reference (Sticky Note)
Object = Value + Type + Identity (The actual physical box in memory)

## G. Visual Explanation

```text
x = [1, 2, 3]
y = x

Namespace (Names)          Heap Memory (Objects)
-----------------          ---------------------
     'x' ---------------------> +----------------+
                                | Type: list     |
     'y' ---------------------> | Value: [1,2,3] |
                                | ID: 140123...  |
                                +----------------+
```
If we modify the object via `y` (e.g., `y.append(4)`), `x` will also see the change because they point to the same object.

## H. Formal Explanation
Python is **dynamically typed** and **strongly typed**.
- **Dynamically typed**: You do not declare the type of a variable. The type lives with the object, not the variable. The name simply points to the object.
- **Strongly typed**: Python will not silently convert types in operations that don't make sense (e.g., you cannot do `"hello" + 5`).

Every object in Python has:
1. **Identity**: A unique integer address in memory (obtained via `id()`).
2. **Type**: What kind of data it is (obtained via `type()`).
3. **Value**: The actual data.

## I. Mathematical / Memory Foundation
When you assign `x = 10`:
1. Python creates an integer object with the value 10 in memory.
2. It stores the address (e.g., `0x7ffee...`) of this object.
3. It binds the name `x` in the current namespace to this address.
If you check `sys.getsizeof(x)`, you will see it is much larger than a 4-byte integer in C, because the Python object contains a reference count, the type pointer, and the size, in addition to the actual integer value.

## J. Implementation & Examples
"""

import sys
from typing import List, Dict, Optional, Any

def demonstrate_references():
    """Shows how names point to the same memory object."""
    print("--- 1. Variable References ---")
    x = [1, 2, 3]
    y = x  # y is a new sticky note on the same list object!
    
    print(f"Original x: {x}")
    print(f"Original y: {y}")
    
    y.append(4)  # Mutating the object
    
    print(f"Modified y, so x is now: {x}")  # x changes too!
    print(f"Memory address of x: {id(x)}")
    print(f"Memory address of y: {id(y)}")
    assert id(x) == id(y), "x and y point to the exact same object in memory."


def demonstrate_immutability():
    """Shows that immutable types cannot be changed, only reassigned."""
    print("\n--- 2. Immutability ---")
    a = 10
    original_id = id(a)
    print(f"Initial a = {a}, ID = {original_id}")
    
    a = a + 1  # This creates a NEW integer object (11) and moves the 'a' sticky note.
    new_id = id(a)
    print(f"After a + 1, a = {a}, ID = {new_id}")
    assert original_id != new_id, "Integers are immutable; a new object was created."

def demonstrate_type_hints(user_id: int, username: str) -> str:
    """
    Type hints (PEP 484) do not enforce types at runtime but are 
    crucial for professional engineering, static analysis (mypy), and IDEs.
    """
    return f"User {username} has ID {user_id}"

## L. Trace (Step-by-Step)
"""
Trace of:
1. a = [1, 2]
2. b = a
3. b.append(3)
4. a = [9, 9]

Step 1: Create list object [1,2]. Bind 'a' to it.
Step 2: Bind 'b' to the exact same list object.
Step 3: Access object via 'b', mutate it to [1,2,3]. 'a' also sees [1,2,3].
Step 4: Create a BRAND NEW list object [9,9]. Move sticky note 'a' to this new object. 
        'b' still points to the old object [1,2,3].
"""

## M. Complexity / Memory
"""
Memory overhead:
- A C-integer is 4 or 8 bytes.
- A Python integer is at least 28 bytes (on 64-bit).
- A Python list has overhead for the list object itself, plus it stores pointers (8 bytes each) to the elements, not the elements themselves.
"""

## N. Common Mistakes
"""
1. Mutating a list passed into a function, expecting it to remain unchanged outside.
2. Using mutable default arguments in functions:
   def bad_func(my_list=[]):
       my_list.append(1)
       return my_list
   (The list is created ONCE when the function is defined, not each time it is called!)
"""

## O. Common Confusions
"""
| Concept             | Meaning                                                |
|---------------------|--------------------------------------------------------|
| Pass-by-value       | A copy of the value is passed (C++ default).           |
| Pass-by-reference   | A reference to the variable is passed.                 |
| Pass-by-object-ref  | Python's model: passing the reference to the object!   |

Is Python Pass-by-Value or Pass-by-Reference?
Neither. It is Pass-by-Object-Reference. If you mutate the object, the caller sees the change. If you reassign the variable inside the function, the caller does NOT see the change.
"""

## P. When To Use (Data Types)
"""
- list: When you need an ordered collection that changes size or contents.
- tuple: When the collection represents a fixed record, or needs to be hashable (e.g., dictionary keys).
- dict: When you need fast O(1) lookups via a key.
- set: When you need to ensure uniqueness or do fast O(1) membership testing (`x in my_set`).
"""

## S. Debugging
"""
Symptom: A variable changed its value seemingly out of nowhere.
Diagnosis: You assigned `a = b` where `b` is a list/dict, and modified `b` later.
Fix: Make a copy: `a = b.copy()` or `a = list(b)`.
"""

## T. Memory Hook
"""
1. Variables are STICKY NOTES, not boxes.
2. Assignment (`=`) NEVER copies data. It only copies the reference (moves the sticky note).
"""

## U. Active Recall
"""
1. What does the `id()` function return?
2. If `x = [1,2]`, and `y = x`, what happens to `x` if I do `y = [3,4]`? What if I do `y.append(3)`?
3. Why does `sys.getsizeof(1)` return 28 instead of 4 or 8?
"""

## V. Practice
"""
Exercise 1 - Debugging:
```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket
print(add_item("Apple"))
print(add_item("Banana"))
```
Why does the second call return `['Apple', 'Banana']` instead of just `['Banana']`? 
Rewrite the function to fix this.
"""
def add_item_fixed(item: str, basket: Optional[List[str]] = None) -> List[str]:
    # Correct implementation
    if basket is None:
        basket = []
    basket.append(item)
    return basket

## W. Interview Question
"""
Q: Explain the difference between `is` and `==` in Python.
A: `==` checks for equality of VALUE. Does the object `a` look the same as object `b`?
   `is` checks for equality of IDENTITY. Do the names `a` and `b` point to the EXACT SAME physical object in memory? (i.e., `id(a) == id(b)`).
"""

## X. Project Connection
"""
In AI engineering and Pandas, understanding references is critical. If you do `df2 = df1`, and modify `df2`, you corrupt `df1`. You must explicitly do `df2 = df1.copy()` to avoid data leakage during feature engineering.
"""

if __name__ == "__main__":
    demonstrate_references()
    demonstrate_immutability()
    
    # Practice validation
    print("\n--- Practice Validation ---")
    b1 = add_item_fixed("Apple")
    b2 = add_item_fixed("Banana")
    print(f"Basket 1: {b1}")
    print(f"Basket 2: {b2}")
    assert b1 == ["Apple"] and b2 == ["Banana"], "The default argument bug was not fixed!"
    print("\nAll concepts successfully demonstrated.")
