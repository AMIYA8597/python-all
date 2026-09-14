"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (FAANG - MICROSOFT PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Microsoft interviews have a massive historical focus on core Data Structures 
# implemented in C/C++, which translates in Python to intense pointer manipulation. 
# They will ask you to reverse Linked Lists, detect cycles, clone Graphs, and 
# rotate 2D Matrices completely in-place without allocating a single extra byte 
# of memory.
#
# A junior engineer reverses a Linked List by appending all the values to a Python 
# List, reversing the List, and building a brand new Linked List. This wastes O(N) 
# memory and destroys the original memory addresses. 
# A senior engineer physically rewires the internal memory pointers in a single 
# O(N) pass using O(1) space, achieving perfect structural inversion.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master strictly In-Place Linked List inversion.
# - Master 2D Matrix mathematical rotation (Transpose + Reverse).
# - Understand constant space O(1) constraints.
#
# ==============================================================================
"""

from typing import List, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. REVERSE A LINKED LIST (THE O(1) IN-PLACE MASTERCLASS)
# ==============================================================================
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_list(values: List[int]) -> ListNode:
    if not values: return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def print_list(head: ListNode, prefix: str = ""):
    vals = []
    curr = head
    while curr:
        vals.append(str(curr.val))
        curr = curr.next
    print(f"{prefix}{' -> '.join(vals)}")

def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Time: O(N) | Space: O(1)
    Physically rewires the pointers backwards.
    """
    prev = None
    curr = head
    
    print("  Starting pointer rewiring sequence...")
    while curr:
        # 1. We MUST save the next node before we sever the connection!
        # If we don't, the rest of the list is permanently lost to Garbage Collection!
        next_temp = curr.next
        
        # 2. SEVER AND REWIRE: Make the current node point BACKWARDS to `prev`
        curr.next = prev
        print(f"    -> Node [{curr.val}] rewired to point to Node [{prev.val if prev else 'None'}]")
        
        # 3. SHIFT THE WINDOW FORWARD
        prev = curr       # The current node becomes the 'prev' for the next iteration
        curr = next_temp  # Move to the saved next node!
        
    # When `curr` hits None (end of list), `prev` is resting on the absolute FINAL node.
    # Therefore, `prev` is the NEW HEAD of the reversed list!
    return prev

def demonstrate_reverse_ll():
    section_header("Microsoft: Reverse Linked List (O(1) In-Place)")
    
    head = build_list([10, 20, 30, 40])
    print_list(head, "  Original List: ")
    
    new_head = reverse_linked_list(head)
    
    print_list(new_head, "\n  Reversed List: ")


# ==============================================================================
# 4. ROTATE MATRIX (THE MATHEMATICAL TRANSPOSE)
# ==============================================================================
def rotate_matrix_in_place(matrix: List[List[int]]) -> None:
    """
    Time: O(N^2) | Space: O(1)
    You are given an N x N 2D matrix representing an image.
    Rotate the image by 90 degrees (clockwise) IN-PLACE.
    
    Attempting to calculate the exact corner coordinates and swapping 4 elements 
    at a time is a nightmare of index logic (`matrix[i][j] = matrix[n-1-j][i]`).
    
    A senior engineer uses Linear Algebra! 
    Rotating 90 degrees clockwise is mathematically identical to:
    1. Transposing the matrix (swapping rows for columns: M[i][j] <-> M[j][i]).
    2. Reversing every row left-to-right.
    """
    n = len(matrix)
    
    # PHASE 1: TRANSPOSE (Mirror across the top-left to bottom-right diagonal)
    print("  Phase 1: Transposing the Matrix...")
    for i in range(n):
        # We only iterate j from i to n. If we iterated from 0 to n, we would 
        # swap everything twice, instantly undoing the transpose!
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            
    for row in matrix: print(f"    {row}")
            
    # PHASE 2: REVERSE ROWS
    print("\n  Phase 2: Reversing every Row left-to-right...")
    for i in range(n):
        matrix[i].reverse()
        
    for row in matrix: print(f"    {row}")

def demonstrate_rotate_matrix():
    section_header("Microsoft: Rotate Image Matrix (O(1) In-Place)")
    
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("Original Matrix:")
    for row in matrix: print(f"  {row}")
    print()
    
    rotate_matrix_in_place(matrix)


def run_all_labs():
    demonstrate_reverse_ll()
    demonstrate_rotate_matrix()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "When reversing a Linked List, why is it absolutely mandatory to allocate the `next_temp` variable at the very start of the loop?"
   Senior Answer: "Because a Linked List is held together purely by physical memory pointers. In the line `curr.next = prev`, we physically sever the pointer connecting the current node to the rest of the list. The absolute millisecond that line executes, the entire remaining subset of the Linked List becomes mathematically unreachable. If there are no other variables pointing to it, the Python Garbage Collector will instantly flag it as dead memory and annihilate it. By assigning `next_temp = curr.next` *before* the severing operation, we establish a permanent 'anchor' in RAM, guaranteeing safe traversal to the next node."

2. Interviewer: "Why does the Matrix Transpose loop `for j in range(i, n)` instead of `for j in range(n)`?"
   Senior Answer: "Transposing a matrix mathematically means reflecting the elements across its primary diagonal (from top-left to bottom-right). If the loop was `for j in range(n)`, when $i=0$ and $j=2$, we swap `M[0][2]` with `M[2][0]`. However, later in the loop, when $i=2$ and $j=0$, we swap `M[2][0]` back with `M[0][2]`. We mathematically undo every single operation we just performed, leaving the matrix totally unchanged! By starting the inner loop at $j=i$, we strictly only process the upper-right triangle of the matrix, mirroring it flawlessly into the lower-left triangle exactly once."

3. Interviewer: "If an algorithm requires you to reverse a string or an array in Python, should you use `[::-1]`, `.reverse()`, or write a custom Two-Pointer `while left < right` loop?"
   Senior Answer: "It depends heavily on the constraint parameters. If the constraint is strict $O(1)$ Space, you MUST use `.reverse()` for Lists because it is an in-place C-level mutation. You CANNOT use `[::-1]` because slicing in Python forces the interpreter to allocate a brand new array in memory, violating the $O(1)$ space constraint! For Strings, because Python Strings are mathematically Immutable, `.reverse()` does not exist, and `[::-1]` is perfectly acceptable as you are forced to allocate $O(N)$ space regardless. If the interviewer explicitly says 'Do not use built-in functions', you must fall back to the raw `while left < right` Two-Pointer swap implementation."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: FAANG Prep (Microsoft) Completed.")
