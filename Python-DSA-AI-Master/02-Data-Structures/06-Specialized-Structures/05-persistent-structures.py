"""
## A. Concept Name
Persistent Data Structures

## B. Learning Objectives
1. Understand the concept of persistency in data structures.
2. Differentiate between partial and full persistence.
3. Implement a simple persistent linked list (stack).

## C. Concept Explanation
A persistent data structure always preserves its previous version when it is modified. Such structures are effectively immutable, as their operations do not update the structure in-place, but instead always yield a new updated structure. Path copying is a common technique to achieve this efficiently without copying the entire structure.

## D. Code Implementation
See the `PersistentNode` and `PersistentStack` classes below.

## E. Performance Analysis
- Time Complexity: O(1) for push and pop.
- Space Complexity: O(1) additional space per operation (just one node created).

## F. Edge Cases
- Popping from an empty stack.
- Accessing old versions (they remain intact indefinitely as long as referenced, due to Python garbage collection).

## G. Interview Challenge
Implement a Persistent Segment Tree to query the state of an array at a specific point in time.

## X. Project Connection
Persistent structures are crucial in AI for maintaining historical states (e.g., in backtracking search, Monte Carlo Tree Search, or storing environments in Reinforcement Learning), immutable functional programming, and version control systems.
"""

from typing import Any, Optional, Tuple

class PersistentNode:
    def __init__(self, value: Any, next_node: Optional['PersistentNode'] = None):
        self.value = value
        self.next = next_node

class PersistentStack:
    def __init__(self, head: Optional[PersistentNode] = None):
        self.head = head

    def push(self, value: Any) -> 'PersistentStack':
        """Creates a new stack version with the pushed element."""
        new_head = PersistentNode(value, self.head)
        return PersistentStack(new_head)

    def pop(self) -> Tuple['PersistentStack', Optional[Any]]:
        """Returns the new stack version and the popped value."""
        if not self.head:
            return self, None
        return PersistentStack(self.head.next), self.head.value

    def peek(self) -> Optional[Any]:
        if self.head:
            return self.head.value
        return None

# Tests
def test_persistent_stack():
    s0 = PersistentStack()
    s1 = s0.push(10)
    s2 = s1.push(20)
    
    assert s0.peek() is None
    assert s1.peek() == 10
    assert s2.peek() == 20
    
    s3, val = s2.pop()
    assert val == 20
    assert s3.peek() == 10
    assert s2.peek() == 20 # Original version s2 remains unchanged

if __name__ == "__main__":
    test_persistent_stack()
    print("05-persistent-structures.py tests passed successfully!")
