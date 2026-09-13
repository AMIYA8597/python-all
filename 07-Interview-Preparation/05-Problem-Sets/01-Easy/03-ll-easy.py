"""
Linked List Easy Problem Set

Learning Objectives:
1. Understand node manipulation and reference updates.
2. Master dummy nodes and multiple pointers techniques.
3. Handle edge cases like empty lists or single nodes safely.

Concepts Explained:
- Linked Lists consist of nodes where each node contains data and a reference to the next node.
- They are not stored contiguously in memory, meaning O(n) access time, but O(1) insertion/deletion at a known node.
- Fast and Slow pointer (Floyd's Tortoise and Hare) is crucial for cycle detection and finding the middle.
"""

from typing import Optional
import time

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Given the head of a singly linked list, reverse the list, and return the reversed list.
    Iterative approach: O(n) time, O(1) space.
    """
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev

def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    You are given the heads of two sorted linked lists list1 and list2.
    Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.
    """
    dummy = ListNode(-1)
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
        
    current.next = list1 if list1 is not None else list2
    
    return dummy.next

def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Given head, the head of a linked list, determine if the linked list has a cycle in it.
    Uses Floyd's Cycle Finding Algorithm (Slow and Fast pointers).
    """
    if not head or not head.next:
        return False
        
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
        
    return True

def create_linked_list(arr):
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def linked_list_to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def performance_analysis():
    print("Performance Analysis for Reverse List:")
    head = create_linked_list(list(range(10000)))
    start = time.time()
    reverse_list(head)
    print(f"Time taken: {time.time() - start:.6f} seconds")

# Interview Challenge: Find the middle node of a linked list
def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def test_ll_easy():
    print("Testing Reverse List...")
    head = create_linked_list([1, 2, 3, 4, 5])
    reversed_head = reverse_list(head)
    assert linked_list_to_list(reversed_head) == [5, 4, 3, 2, 1]
    
    print("Testing Merge Two Lists...")
    l1 = create_linked_list([1, 2, 4])
    l2 = create_linked_list([1, 3, 4])
    merged = merge_two_lists(l1, l2)
    assert linked_list_to_list(merged) == [1, 1, 2, 3, 4, 4]
    
    print("Testing Middle Node...")
    head = create_linked_list([1, 2, 3, 4, 5])
    assert middle_node(head).val == 3
    
    print("All tests passed!")

if __name__ == "__main__":
    test_ll_easy()
    performance_analysis()
