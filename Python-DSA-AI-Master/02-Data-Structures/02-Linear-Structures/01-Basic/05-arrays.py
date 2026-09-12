"""
## A. Concept Name
Arrays (and Python `array` module)

## B. One-Sentence Definition
An array is a contiguous block of memory holding a fixed number of elements of the same data type.

## C. Why Does This Exist?
To store sequences of homogeneous data efficiently, minimizing memory overhead compared to generalized lists of object references.

## D. Intuition
Think of an array as a perfectly organized row of mailboxes, all the same size and back-to-back, so you can jump to any box instantly if you know its number.

## E. Real-Life Analogy
A standard egg carton. Every slot is exactly the same size, meant only for eggs (homogeneous), and they are physically adjacent to each other.

## F. Mental Model
Memory Address = Base_Address + (Index * Size_Of_Element). Because elements are identical in size and stored sequentially, calculating any element's memory address is instant.

## G. Visual Explanation
Memory: [ 10 ][ 20 ][ 30 ][ 40 ]
Index:    0    1    2    3
Addresses: 0x00 0x04 0x08 0x0C (assuming 4 bytes each)

## H. Formal Explanation
In computer science, an array is a linear data structure that stores elements of the same type in contiguous memory locations. In Python, the built-in `list` is a dynamic array of object references, whereas the `array` module provides true C-style typed arrays for basic numerical types.

## I. Mathematical Foundation
Address(A[i]) = Address(A[0]) + i * c
Where `i` is the index and `c` is the size of each element in bytes.

## J. From-Scratch Implementation
(See the `ArrayBasic`, `ArrayIntermediate`, and `ArrayAdvanced` classes below using Python's `array` module to manage C-style arrays.)

## K. Library / Production Implementation
Python's built-in `array` module (`import array`) is used for space-efficient storage of basic types. Python's built-in `list` is used for generic dynamic arrays. For high-performance numerical computing, `numpy.ndarray` is the industry standard.

## L. Trace (walk through example)
1. Initialize: `arr = array.array('i', [1, 2, 3])` -> Creates a continuous block of 3 integers.
2. Append: `arr.append(4)` -> Reallocates memory if necessary and adds 4 to the end.
3. Access: `arr[2]` -> Calculates memory offset for index 2 and returns `3`.

## M. Complexity
- Time:
  - Access (Read/Write by index): O(1)
  - Search (Unsorted): O(N)
  - Insert/Delete at end: O(1) amortized
  - Insert/Delete at beginning/middle: O(N) (requires shifting elements)
- Space: O(N) where N is the number of elements.

## N. Common Mistakes
- Confusing Python `list` with C-style arrays (lists use more memory and hold references).
- Assuming inserting into the middle of an array is O(1).
- Going out of bounds (IndexError).

## O. Common Confusions
- "Why use `array` instead of `list` in Python?" -> Use `array` only when you have a massive amount of purely numerical data and memory is a strict constraint. Otherwise, `list` is more versatile and performant enough.

## P. When To Use
- When you need fast O(1) index-based access.
- When memory efficiency is critical and data is homogeneous numerical types (using `array` or `numpy`).

## Q. When NOT To Use
- When you need frequent insertions and deletions at the beginning or middle.
- When data size fluctuates wildly (though dynamic arrays handle this, frequent resizes are costly).
- When storing heterogeneous data (use `list` or tuples).

## R. Trade-offs
- Fast access (O(1)) vs. slow arbitrary insertions/deletions (O(N)).
- Space efficiency (contiguous) vs. resizing overhead (dynamic arrays must allocate new memory and copy old data when full).

## S. Debugging
- Check boundary conditions (indices `0` to `n-1`).
- Verify the `typecode` matches the data you are trying to store.
- Ensure you are not confusing 0-indexed logic with 1-indexed human counting.

## T. Memory Hook
"Arrays are contiguous mailboxes."

## U. Active Recall
- What is the time complexity to access an element by index?
- Why is insertion in the middle O(N)?
- What does the `typecode` do in Python's `array` module?

## V. Practice
Implement functions to:
- Find the maximum element.
- Reverse the array in-place without using built-in methods.
- Remove all duplicates from a sorted array.

## W. Interview Question
"Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`." (Two Sum - see implementation below).

## X. Project Connection
Used in image processing (matrices of pixels), audio buffers, sensor data logging, and as the foundational building block for hash tables, heaps, and matrices.
"""

import array
from typing import List, Any

class ArrayBasic:
    """Basic Implementation using Python's array module."""
    def __init__(self, typecode: str, initial_data: List[Any]) -> None:
        self.arr = array.array(typecode, initial_data)

    def display(self) -> List[Any]:
        return self.arr.tolist()

    def append(self, item: Any) -> None:
        self.arr.append(item)

    def access(self, index: int) -> Any:
        return self.arr[index]

class ArrayIntermediate(ArrayBasic):
    """Intermediate operations: Searching and inserting."""
    def insert_at(self, index: int, item: Any) -> None:
        self.arr.insert(index, item)

    def find(self, item: Any) -> int:
        try:
            return self.arr.index(item)
        except ValueError:
            return -1

class ArrayAdvanced(ArrayIntermediate):
    """Advanced Operations: Reversing and memory analysis concepts."""
    def reverse_array(self) -> None:
        self.arr.reverse()

    def get_info(self) -> str:
        return f"Typecode: {self.arr.typecode}, Itemsize: {self.arr.itemsize} bytes, Buffer info: {self.arr.buffer_info()}"

def interview_challenge_two_sum(nums: List[int], target: int) -> List[int]:
    """
    Interview Challenge: Two Sum
    Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
    """
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []

def run_tests() -> None:
    print("Testing ArrayBasic...")
    ab = ArrayBasic('i', [1, 2, 3])
    ab.append(4)
    assert ab.access(3) == 4

    print("Testing ArrayIntermediate...")
    ai = ArrayIntermediate('i', [10, 20, 30])
    ai.insert_at(1, 15)
    assert ai.display() == [10, 15, 20, 30]
    assert ai.find(20) == 2

    print("Testing ArrayAdvanced...")
    aa = ArrayAdvanced('d', [1.1, 2.2, 3.3])
    aa.reverse_array()
    assert aa.display() == [3.3, 2.2, 1.1]
    print(aa.get_info())

    print("Testing Interview Challenge...")
    assert interview_challenge_two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert interview_challenge_two_sum([3, 2, 4], 6) == [1, 2]

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
