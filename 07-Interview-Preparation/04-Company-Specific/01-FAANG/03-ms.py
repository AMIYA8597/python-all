"""
Module: Microsoft Interview Questions (Python)

Learning Objectives:
- Master complex matrix traversal patterns (e.g., Spiral Matrix).
- Understand deep copy of complex data structures (e.g., Linked List with Random Pointers).

Concept Explanation:
Microsoft commonly asks matrix manipulation, string parsing, and linked list problems. They test edge case handling heavily, especially in matrices and parsing.

Performance Analysis:
- Spiral Matrix: Time O(M*N), Space O(1) excluding output array.
- Copy List with Random Pointer: Time O(N), Space O(N) or O(1) depending on approach.
"""

from typing import List, Optional

# Basic/Intermediate: Spiral Matrix
def spiral_order(matrix: List[List[int]]) -> List[int]:
    """Returns elements of the matrix in spiral order."""
    if not matrix:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse right
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        
        # Traverse down
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        if top <= bottom:
            # Traverse left
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
            
        if left <= right:
            # Traverse up
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
            
    return result


# Advanced: Copy List with Random Pointer
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copy_random_list(head: 'Optional[Node]') -> 'Optional[Node]':
    """Creates a deep copy of a linked list with random pointers (O(1) space)."""
    if not head:
        return None
        
    # Step 1: Interweave cloned nodes
    curr = head
    while curr:
        new_node = Node(curr.val, curr.next)
        curr.next = new_node
        curr = new_node.next
        
    # Step 2: Assign random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
        
    # Step 3: Separate the lists
    curr = head
    cloned_head = head.next
    while curr:
        cloned_node = curr.next
        curr.next = cloned_node.next
        if cloned_node.next:
            cloned_node.next = cloned_node.next.next
        curr = curr.next
        
    return cloned_head


def test_microsoft_questions():
    print("Testing Spiral Matrix...")
    matrix1 = [[1,2,3],[4,5,6],[7,8,9]]
    assert spiral_order(matrix1) == [1,2,3,6,9,8,7,4,5]
    matrix2 = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    assert spiral_order(matrix2) == [1,2,3,4,8,12,11,10,9,5,6,7]
    print("Passed.")

if __name__ == "__main__":
    test_microsoft_questions()
    print("All Microsoft interview tests passed!")
