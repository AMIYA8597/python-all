"""
# ==============================================================================
# LABORATORY: STACKS (LIFO)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Stacks follow the Last-In, First-Out (LIFO) principle. They are the underlying 
# architecture of the Python function Call Stack (which causes RecursionError if 
# it gets too deep). They are also the standard mechanism for backtracking 
# algorithms, Depth-First Search (DFS), and parsing expressions.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Build a safe, object-oriented Stack using a Python list.
# - Understand how a standard list provides O(1) performance for stacks.
# - Solve a classic FAANG interview problem: Valid Parentheses.
# - Understand how to convert a recursive function into an iterative one using a Stack.
#
# ==============================================================================
"""

from typing import Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IMPLEMENTING A SAFE STACK
# ==============================================================================
class Stack:
    """
    We wrap a standard Python list.
    We only expose `append` (push) and `pop`, which are both O(1) operations.
    This prevents users from doing O(N) operations like `insert(0, x)` or 
    accessing items in the middle of the stack.
    """
    def __init__(self):
        self._data = []
        
    def push(self, item: Any) -> None:
        """Push an item onto the top of the stack. (O(1))"""
        self._data.append(item)
        
    def pop(self) -> Any:
        """Remove and return the top item. (O(1))"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()
        
    def peek(self) -> Optional[Any]:
        """Return the top item without removing it. (O(1))"""
        if self.is_empty():
            return None
        return self._data[-1]
        
    def is_empty(self) -> bool:
        return len(self._data) == 0
        
    def __len__(self) -> int:
        return len(self._data)

def demonstrate_stack_implementation():
    section_header("Stack Implementation")
    
    stack = Stack()
    
    print("Pushing: A, B, C")
    stack.push("A")
    stack.push("B")
    stack.push("C")
    
    print(f"Top item (peek): {stack.peek()}")
    print(f"Stack size: {len(stack)}")
    
    print("\nPopping items:")
    while not stack.is_empty():
        print(f" Popped: {stack.pop()}")


# ==============================================================================
# 4. CLASSIC INTERVIEW PROBLEM: VALID PARENTHESES
# ==============================================================================
def is_valid_parentheses(s: str) -> bool:
    """
    LeetCode #20: Valid Parentheses.
    Time Complexity: O(N)
    Space Complexity: O(N) (For the stack)
    """
    stack = Stack()
    # Map closing brackets to their corresponding opening brackets
    bracket_map = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in bracket_map.values(): # It's an opening bracket
            stack.push(char)
        elif char in bracket_map.keys(): # It's a closing bracket
            if stack.is_empty():
                return False # Closing bracket with no opening bracket
            top_element = stack.pop()
            if top_element != bracket_map[char]:
                return False # Mismatched brackets
                
    # If the stack is empty, all brackets were matched.
    return stack.is_empty()

def demonstrate_valid_parentheses():
    section_header("Algorithm: Valid Parentheses")
    
    test_cases = [
        "()",
        "()[]{}",
        "(]",
        "([)]",
        "{[]}"
    ]
    
    for test in test_cases:
        result = is_valid_parentheses(test)
        print(f"'{test:<6}' -> {'Valid' if result else 'Invalid'}")


# ==============================================================================
# 5. RECURSION VS EXPLICIT STACK (DFS)
# ==============================================================================
# We simulate traversing a file system directory tree.

directory_tree = {
    "root": ["folder1", "folder2"],
    "folder1": ["fileA.txt", "fileB.txt"],
    "folder2": ["folder3"],
    "folder3": ["fileC.txt"],
    "fileA.txt": [], "fileB.txt": [], "fileC.txt": []
}

def dfs_recursive(node: str):
    """
    Uses the Python interpreter's Call Stack.
    Dangerous if the tree is deeper than 1000 levels (RecursionError).
    """
    print(f" Visiting (Recursive): {node}")
    for child in directory_tree.get(node, []):
        dfs_recursive(child)

def dfs_iterative(start_node: str):
    """
    Uses an explicit Heap-allocated Stack.
    Can handle millions of levels of depth without crashing.
    """
    stack = Stack()
    stack.push(start_node)
    
    while not stack.is_empty():
        node = stack.pop()
        print(f" Visiting (Iterative): {node}")
        
        # We push children in reverse order so the first child is processed first
        # (This makes it match the exact output order of the recursive version)
        children = directory_tree.get(node, [])
        for child in reversed(children):
            stack.push(child)

def demonstrate_dfs():
    section_header("Recursion vs Explicit Stacks (DFS)")
    
    print("--- 1. Recursive DFS (Call Stack) ---")
    dfs_recursive("root")
    
    print("\n--- 2. Iterative DFS (Explicit Stack) ---")
    dfs_iterative("root")


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is a standard Python `list` perfectly fine to use as a Stack?
   Answer: A stack only requires operations at one end (the top). In a Python list, `append()` and `pop()` operate on the right side of the dynamic array, which are $O(1)$ amortized time.

2. How do you convert a recursive algorithm into an iterative one?
   Answer: By creating an explicit `Stack` object and pushing the function's state/arguments onto the stack inside a `while not stack.is_empty():` loop.

3. Why use an explicit stack instead of recursion?
   Answer: The Python call stack is limited (default 1000 frames) to prevent C-stack overflows. An explicit stack allocates memory on the heap, allowing for millions of items without raising a `RecursionError`.
"""

if __name__ == "__main__":
    demonstrate_stack_implementation()
    demonstrate_valid_parentheses()
    demonstrate_dfs()
    print("\n[SUCCESS] Laboratory: Stacks Completed.")
