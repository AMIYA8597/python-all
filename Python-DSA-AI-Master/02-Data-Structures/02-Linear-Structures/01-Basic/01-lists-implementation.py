"""
## A. Concept Name
Python Lists (Dynamic Arrays)

## B. One-Sentence Definition
A Python list is a mutable, ordered collection of items implemented as a dynamic array that can grow and shrink in size.

## C. Why Does This Exist?
Lists provide a flexible and efficient way to store sequences of data without needing to know the size of the data upfront.

## D. Intuition
Think of a list as a contiguous block of memory with extra space at the end. When it fills up, a new, larger block is allocated, and the old items are moved over.

## E. Real-Life Analogy
It's like a bookshelf where you can always add more books. If the shelf gets full, you buy a bigger shelf, move all your books there, and continue adding new ones.

## F. Mental Model
A dynamic array keeps track of a fixed-size underlying array, its capacity, and the current number of elements (length).

## G. Visual Explanation
[ A | B | C | _ ] (Length = 3, Capacity = 4)
Adding 'D' fills it: [ A | B | C | D ] (Length = 4, Capacity = 4)
Adding 'E' resizes it (e.g., doubling): [ A | B | C | D | E | _ | _ | _ ] (Length = 5, Capacity = 8)

## H. Formal Explanation
In CPython, lists are implemented as arrays of pointers to Python objects. The array has an allocated capacity, which is typically larger than the number of items. This over-allocation gives lists an amortized O(1) time complexity for appending new elements.

## I. Mathematical Foundation
Amortized analysis shows that while resizing takes O(N) time, it happens infrequently enough (e.g., doubling capacity) that the average time per append is O(1). Cost of N appends is N + (1 + 2 + 4 + ... + N/2) = N + N - 1 = O(N), so O(1) per append.

## J. From-Scratch Implementation
See `CustomList` and `DynamicArray` classes below.

## K. Library / Production Implementation
Python's built-in `list` class handles everything dynamically. CPython's source uses `listobject.c`.

## L. Trace (walk through example)
da = DynamicArray()
da.append(10) -> n=1, capacity=1 -> [10]
da.append(20) -> n=2, capacity=2 -> resize from 1 to 2 -> [10, 20]
da.append(30) -> n=3, capacity=4 -> resize from 2 to 4 -> [10, 20, 30, _]

## M. Complexity
- Time: Append O(1) amortized, Insert/Delete arbitrary index O(N), Access O(1), Pop end O(1), Pop beginning O(N)
- Space: O(N) where N is the number of elements

## N. Common Mistakes
Modifying a list while iterating over it, or assuming insert(0, item) is fast (it's O(N)).

## O. Common Confusions
Confusing Python lists (dynamic arrays) with Linked Lists. Python lists are contiguous in memory.

## P. When To Use
When you need fast indexed access, ordered data, or frequent additions/removals from the end of the collection.

## Q. When NOT To Use
When you need fast insertions/deletions at the beginning or middle of the collection (use `collections.deque` or a Linked List).

## R. Trade-offs
Fast access and appends vs. slow arbitrary inserts/deletes. Wastes some memory due to over-allocation.

## S. Debugging
Use `sys.getsizeof()` to see how a list's memory consumption grows in jumps rather than smoothly.

## T. Memory Hook
"Lists are Elastic Arrays"

## U. Active Recall
1. What is the time complexity of appending to a Python list?
2. How does a dynamic array resize itself?

## V. Practice
Implement a `pop()` method for the `DynamicArray` class that also shrinks the array if it is less than 25% full.

## W. Interview Question
Find the duplicate number in an array. See `interview_challenge_find_duplicate` below.

## X. Project Connection
Used almost everywhere in Python projects for storing collections of items, e.g., storing rows read from a CSV file.
"""

from typing import Any, List, TypeVar
import time

T = TypeVar('T')

class CustomList:
    """Basic Implementation: A simple wrapper around Python's list."""
    def __init__(self) -> None:
        self.data: List[Any] = []

    def append(self, item: Any) -> None:
        self.data.append(item)

    def get(self, index: int) -> Any:
        return self.data[index]

    def remove(self, item: Any) -> None:
        self.data.remove(item)

class DynamicArray:
    """Intermediate Implementation: Understanding dynamic arrays."""
    def __init__(self, capacity: int = 1) -> None:
        self.n = 0
        self.capacity = capacity
        self.A = self._make_array(self.capacity)

    def __len__(self) -> int:
        return self.n

    def __getitem__(self, k: int) -> Any:
        if not 0 <= k < self.n:
            raise IndexError('invalid index')
        return self.A[k]

    def append(self, obj: Any) -> None:
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        self.A[self.n] = obj
        self.n += 1

    def _resize(self, c: int) -> None:
        B = self._make_array(c)
        for k in range(self.n):
            B[k] = self.A[k]
        self.A = B
        self.capacity = c

    def _make_array(self, c: int) -> List[Any]:
        return [None] * c

class AdvancedListOps:
    """Advanced Implementation: List comprehension and functional tools."""
    @staticmethod
    def flatten_list(nested_list: List[Any]) -> List[Any]:
        flat_list: List[Any] = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(AdvancedListOps.flatten_list(item))
            else:
                flat_list.append(item)
        return flat_list

def interview_challenge_find_duplicate(nums: List[int]) -> int:
    """
    Interview Challenge: Find the duplicate number.
    Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.
    There is only one repeated number in nums, return this repeated number.
    """
    tortoise = nums[0]
    hare = nums[0]
    while True:
        tortoise = nums[tortoise]
        hare = nums[nums[hare]]
        if tortoise == hare:
            break
    ptr1 = nums[0]
    ptr2 = tortoise
    while ptr1 != ptr2:
        ptr1 = nums[ptr1]
        ptr2 = nums[ptr2]
    return ptr1

def run_tests() -> None:
    print("Testing CustomList...")
    cl = CustomList()
    cl.append(1)
    cl.append(2)
    assert cl.get(1) == 2

    print("Testing DynamicArray...")
    da = DynamicArray()
    da.append(10)
    da.append(20)
    assert len(da) == 2
    assert da[1] == 20

    print("Testing AdvancedListOps...")
    nested = [1, [2, 3], [4, [5, 6]]]
    assert AdvancedListOps.flatten_list(nested) == [1, 2, 3, 4, 5, 6]

    print("Testing Interview Challenge...")
    assert interview_challenge_find_duplicate([1, 3, 4, 2, 2]) == 2
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
