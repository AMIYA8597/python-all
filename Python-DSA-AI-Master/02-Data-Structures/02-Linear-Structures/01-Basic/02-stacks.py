"""
## A. Concept Name
Stack

## B. One-Sentence Definition
A stack is a linear data structure that follows the Last-In-First-Out (LIFO) principle, where elements are added and removed from the same end.

## C. Why Does This Exist?
Stacks exist to manage temporary data where the most recently added item needs to be accessed first, such as tracking history, managing function calls, or parsing expressions.

## D. Intuition
Think of a stack as building upwards; you can only interact with the very top item. To get to items underneath, you must first remove what's on top.

## E. Real-Life Analogy
A stack of plates at a buffet. You add plates to the top of the stack, and when someone needs a plate, they take one from the top. The first plate put down is the last one taken.

## F. Mental Model
A vertical tube with a solid bottom. Items (blocks) are dropped in from the top. To retrieve a block, you must pull out the topmost blocks until you reach the one you want. 

## G. Visual Explanation
Empty Stack: []
Push(1):     [1]
Push(2):     [1, 2] <- Top
Push(3):     [1, 2, 3] <- Top
Pop() -> 3:  [1, 2] <- Top

## H. Formal Explanation
A stack is an abstract data type (ADT) characterized by two primary operations: `push`, which adds an element to the collection, and `pop`, which removes the most recently added element that was not yet removed. The order of operations is Last-In-First-Out (LIFO).

## I. Mathematical Foundation
A stack can be modeled as a sequence S = (s_1, s_2, ..., s_n) where push(x) results in S' = (s_1, s_2, ..., s_n, x) and pop() removes and returns s_n, leaving S'' = (s_1, s_2, ..., s_{n-1}).

## J. From-Scratch Implementation
Implemented below using Python lists (`BasicStack`) and linked lists (`LinkedListStack`).

## K. Library / Production Implementation
In production Python, use `collections.deque` for thread-safe and performant stacks. A standard Python list `[]` can also act as a stack using `.append()` and `.pop()`.

## L. Trace (walk through example)
1. Initialize `stack = []`
2. `push("A")` -> `["A"]`
3. `push("B")` -> `["A", "B"]`
4. `peek()` -> Returns `"B"`, stack remains `["A", "B"]`
5. `pop()` -> Returns `"B"`, stack becomes `["A"]`
6. `pop()` -> Returns `"A"`, stack becomes `[]`

## M. Complexity
- Time Complexity: O(1) for Push, Pop, Peek. O(N) for Search.
- Space Complexity: O(N) where N is the number of elements in the stack.

## N. Common Mistakes
- Calling `pop()` or `peek()` on an empty stack (raises an IndexError).
- Using `insert(0, val)` on a list to simulate a stack (which is O(N) time) instead of `append(val)`.

## O. Common Confusions
- **Stack vs Queue:** Stack is LIFO (Last-In-First-Out), Queue is FIFO (First-In-First-Out).
- **Call Stack:** The system's call stack is just a stack data structure used by the runtime to keep track of active subroutines.

## P. When To Use
- Depth-First Search (DFS) algorithms.
- Reversing items.
- Undo/Redo mechanisms.
- Balancing symbols (like parentheses matching).
- Evaluating postfix/prefix expressions.

## Q. When NOT To Use
- When you need FIFO behavior (use a Queue).
- When you need to access elements by index randomly (use an Array/List).
- When you need to frequently search for elements (use a Set or Hash Map).

## R. Trade-offs
- Lists provide excellent cache locality but occasionally require O(N) resizing operations.
- Linked list stacks never resize but use extra memory for pointers and have worse cache locality.

## S. Debugging
- Print the stack from bottom to top to visualize its state.
- Check if the stack is unexpectedly empty before a pop/peek operation.

## T. Memory Hook
"Pancakes on a plate." (LIFO: Last pancake on is the first one eaten).

## U. Active Recall
- What is the time complexity of a stack `pop()` operation?
- How does a stack differ from a queue?
- Can you search a stack in O(1) time?

## V. Practice
- Implement a Min-Stack (tracks minimum element in O(1)).
- Implement a stack using queues.
- Evaluate a postfix expression.

## W. Interview Question
"Valid Parentheses": Given a string containing just `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid. (Implementation below).

## X. Project Connection
Can be used in an undo/redo feature for a text editor or managing the browser history for forward/backward navigation.
"""

from typing import Any, List, Optional
import collections

class BasicStack:
    """Basic Implementation: Using Python list."""
    def __init__(self) -> None:
        self.items: List[Any] = []

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def push(self, item: Any) -> None:
        self.items.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self) -> int:
        return len(self.items)

class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None

class LinkedListStack:
    """Intermediate Implementation: Using Linked List for dynamic sizing."""
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self._size = 0

    def is_empty(self) -> bool:
        return self.head is None

    def push(self, data: Any) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        popped_node = self.head
        self.head = self.head.next  # type: ignore
        self._size -= 1
        return popped_node.data  # type: ignore

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.head.data  # type: ignore

class MinStack:
    """Advanced Implementation: Stack that supports retrieving the minimum element in O(1) time."""
    def __init__(self) -> None:
        self.stack: List[int] = []
        self.min_stack: List[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        if self.stack:
            if self.stack[-1] == self.min_stack[-1]:
                self.min_stack.pop()
            self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]

def interview_challenge_valid_parentheses(s: str) -> bool:
    """
    Interview Challenge: Valid Parentheses.
    Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
    """
    stack = BasicStack()
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top_element = stack.pop() if not stack.is_empty() else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.push(char)
    return stack.is_empty()

def run_tests() -> None:
    print("Testing BasicStack...")
    bs = BasicStack()
    bs.push(1)
    bs.push(2)
    assert bs.pop() == 2
    assert bs.peek() == 1

    print("Testing LinkedListStack...")
    lls = LinkedListStack()
    lls.push("A")
    lls.push("B")
    assert lls.pop() == "B"

    print("Testing MinStack...")
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    assert ms.get_min() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.get_min() == -2

    print("Testing Interview Challenge...")
    assert interview_challenge_valid_parentheses("()[]{}") == True
    assert interview_challenge_valid_parentheses("(]") == False
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
