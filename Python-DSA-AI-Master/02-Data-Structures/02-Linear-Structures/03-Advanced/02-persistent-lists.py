"""
## A. Concept Name
Persistent Lists

## B. Problem Statement
Data structures that maintain their previous versions when modified, allowing safe concurrency and functional programming paradigms.

## C. Learning Objectives
1. Understand the concept of Persistent Data Structures.
2. Implement a simple purely functional list.
3. Compare space/time constraints of immutability.

## D. Core Algorithms
Structural sharing by linking new heads to existing tails.

## E. Detailed Walkthrough
A persistent list consists of an empty state or a node with data and a reference to the next node. Prepending simply creates a new node pointing to the current list.

## F. Time & Space Complexity
- Prepend: O(1) time and space
- Append: O(N) time and space
- Access: O(N) time

## G. Edge Cases & Constraints
Empty list operations (head/tail).

## H. Common Pitfalls
Trying to mutate the list in place instead of returning a new version. Stack overflow on deep recursion.

## I. Refactoring & Best Practices
Use structural sharing. Leverage type hints. Handle empty states gracefully.

## J. Interview Patterns
Implementing functional queues using two persistent lists.

## K. Application Areas
Functional programming, undo/redo systems, time-travel debugging, concurrency.

## L. External Libraries
Pyrsistent, immutables.

## M. Scalability & System Design
Avoids locking in concurrent environments since data is immutable.

## N. Concurrency & Thread Safety
Inherently thread-safe due to immutability.

## O. Cloud & Microservices
Useful in event sourcing and immutable event logs.

## P. Test Coverage & CI/CD
Test empty list edge cases, sequence creation, structural sharing.

## Q. Debugging Strategies
Visualize list as a tree where multiple heads can point to the same tail.

## R. Performance Profiling
Memory usage may increase, garbage collection overhead due to many small objects.

## S. Real-world Variations
Persistent Vectors, Hash Array Mapped Tries (HAMT).

## T. Security & Compliance
Immutability prevents data tampering post-creation.

## U. Data Engineering & ML
Tracking version history of datasets and lineage.

## V. API Integration
Immutable payloads for consistent API responses.

## W. Cost Optimization
Memory reuse through structural sharing compared to deep copying.

## X. Project Connection
Foundational for advanced purely functional data structures and functional programming paradigms in Python projects.
"""

from typing import Any, Optional, Tuple

class PersistentList:
    """
    Basic/Intermediate Implementation of a purely functional (persistent) Linked List.
    Instead of modifying nodes, we create new nodes that point to existing ones (structural sharing).
    """
    def __init__(self, data: Any = None, next_node: Optional['PersistentList'] = None, empty: bool = True):
        self.data = data
        self.next = next_node
        self.is_empty = empty

    @staticmethod
    def empty() -> 'PersistentList':
        return PersistentList(empty=True)

    def prepend(self, data: Any) -> 'PersistentList':
        """O(1) prepend operation returning a new version of the list."""
        return PersistentList(data=data, next_node=self, empty=False)

    def head(self) -> Any:
        if self.is_empty:
            raise IndexError("head of empty list")
        return self.data

    def tail(self) -> 'PersistentList':
        if self.is_empty:
            raise IndexError("tail of empty list")
        return self.next  # type: ignore

    def to_list(self) -> list:
        res = []
        curr = self
        while not curr.is_empty:
            res.append(curr.data)
            curr = curr.next  # type: ignore
        return res

def interview_challenge_functional_queue() -> Tuple['FunctionalQueue', 'FunctionalQueue']:
    """
    Interview Challenge: Implement a purely functional Queue using two persistent lists.
    (Simplified structural representation)
    """
    class FunctionalQueue:
        def __init__(self, front: PersistentList, rear: PersistentList):
            self.front = front
            self.rear = rear

        def enqueue(self, item: Any) -> 'FunctionalQueue':
            return FunctionalQueue(self.front, self.rear.prepend(item))

        def dequeue(self) -> Tuple[Any, 'FunctionalQueue']:
            if self.front.is_empty:
                if self.rear.is_empty:
                    raise IndexError("dequeue from empty queue")
                # reverse rear and set to front
                curr = self.rear
                new_front = PersistentList.empty()
                while not curr.is_empty:
                    new_front = new_front.prepend(curr.data)
                    curr = curr.next  # type: ignore
                return new_front.head(), FunctionalQueue(new_front.tail(), PersistentList.empty())
            else:
                return self.front.head(), FunctionalQueue(self.front.tail(), self.rear)

    empty_q = FunctionalQueue(PersistentList.empty(), PersistentList.empty())
    q1 = empty_q.enqueue(1)
    q2 = q1.enqueue(2)
    return q1, q2


def run_tests() -> None:
    print("Testing PersistentList...")
    l1 = PersistentList.empty()
    l2 = l1.prepend(1)
    l3 = l2.prepend(2)
    
    # l1 should still be empty
    assert l1.is_empty == True
    # l2 should be [1]
    assert l2.to_list() == [1]
    # l3 should be [2, 1]
    assert l3.to_list() == [2, 1]

    print("Testing Interview Challenge...")
    q1, q2 = interview_challenge_functional_queue()
    val, _ = q1.dequeue()
    assert val == 1
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
