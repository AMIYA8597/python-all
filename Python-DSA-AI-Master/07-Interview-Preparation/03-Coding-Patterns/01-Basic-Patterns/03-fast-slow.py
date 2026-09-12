"""
Fast and Slow Pointers Pattern - Comprehensive Guide

Learning Objectives:
- Understand the Fast and Slow Pointers (Tortoise and Hare) technique
- Implement cycle detection in linked lists and arrays
- Find the middle of a linked list or the start of a cycle
- Analyze time and space complexity

Concept Explanation:
The Fast and Slow pointer approach uses two pointers which move through the array (or sequence/linked list) at different speeds. This approach is quite useful when dealing with cyclic linked lists or arrays. By moving at different speeds (usually one pointer moves 1 step, the other 2 steps), if there is a cycle, the two pointers will eventually meet.

When to use:
- Problem involves a Linked List or Array
- Dealing with cycle detection
- Finding the middle element of a sequence
"""

from typing import Optional, List

class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

# Basic: LinkedList Cycle Detection
def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Given the head of a Singly LinkedList, write a function to determine if the LinkedList has a cycle in it or not.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    slow, fast = head, head
    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
        if slow == fast:
            return True
    return False


# Intermediate: Middle of the LinkedList
def find_middle_of_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Given the head of a Singly LinkedList, write a method to return the middle node of the LinkedList.
    If total number of nodes is even, return the second middle node.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


# Advanced: Start of LinkedList Cycle
def find_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Given the head of a Singly LinkedList that contains a cycle, write a function to find the starting node of the cycle.
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    cycle_length = 0
    slow, fast = head, head
    while fast is not None and fast.next is not None:
        fast = fast.next.next
        slow = slow.next
        if slow == fast:
            cycle_length = calculate_cycle_length(slow)
            break
            
    if cycle_length == 0:
        return None
        
    return find_start(head, cycle_length)

def calculate_cycle_length(slow: ListNode) -> int:
    current = slow
    cycle_length = 0
    while True:
        current = current.next
        cycle_length += 1
        if current == slow:
            break
    return cycle_length

def find_start(head: ListNode, cycle_length: int) -> ListNode:
    pointer1 = head
    pointer2 = head
    while cycle_length > 0:
        pointer2 = pointer2.next
        cycle_length -= 1
    while pointer1 != pointer2:
        pointer1 = pointer1.next
        pointer2 = pointer2.next
    return pointer1

def run_tests():
    print("Testing Fast & Slow Pointers...")
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    
    assert has_cycle(head) == False
    assert find_middle_of_linked_list(head).value == 3
    
    # create cycle
    head.next.next.next.next.next = head.next.next
    assert has_cycle(head) == True
    assert find_cycle_start(head).value == 3
    
    print("All tests passed.")

if __name__ == '__main__':
    run_tests()
