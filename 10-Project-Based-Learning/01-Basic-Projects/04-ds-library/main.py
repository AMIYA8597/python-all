"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (CUSTOM DATA STRUCTURES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer needs a queue to process 1,000,000 tasks. They use a 
# standard Python `list`. To dequeue a task, they execute `list.pop(0)`. 
# Because a list is a dynamic C-array, Python mathematically forces all 999,999 
# remaining items to physically shift one memory block to the left. The program 
# takes 14 hours to execute due to catastrophic O(N) memory shifting.
#
# A senior software engineer understands "Data Structures". They implement a 
# Custom Linked List (or use `collections.deque`). When they pop the first item, 
# the algorithm simply changes a single memory pointer (`head = head.next`). 
# The other 999,999 items remain perfectly frozen in RAM. The pop operation is 
# executed in mathematically flawless O(1) time. The 14-hour script finishes in 
# 0.2 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master memory allocation architecture (Pointers vs Contiguous Arrays).
# - Execute a mathematical Singly Linked List (O(1) insertion/deletion).
# - Implement a Stack (LIFO) and Queue (FIFO) using pure OOP Nodes.
#
# ==============================================================================
"""

import timeit

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE NODE ARCHITECTURE
# ==============================================================================
# A Node is a single, isolated block of memory. It holds a payload (data), 
# and a mathematical pointer (memory address) to the next Node in RAM.
# Unlike arrays, Nodes do NOT need to be stored contiguously on the silicon!

class Node:
    def __init__(self, data):
        self.data = data
        self.next: 'Node' = None  # The architectural memory pointer!


# ==============================================================================
# 4. THE LINKED LIST (O(1) INSERTION)
# ==============================================================================
class SinglyLinkedList:
    def __init__(self):
        self.head: Node = None # Pointer to the first element
        self.tail: Node = None # Pointer to the last element (for O(1) appends!)
        self.length = 0

    def append(self, data):
        """
        O(1) Constant Time.
        Because we mathematically track the `tail`, we never have to traverse 
        the list to add a new item!
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node # Link the old tail to the new node
            self.tail = new_node      # Update the tail pointer
        self.length += 1

    def pop_first(self):
        """
        O(1) Constant Time.
        We mathematically sever the connection to the first node. 
        Python's Garbage Collector will eventually delete the orphaned node from RAM.
        """
        if self.head is None:
            raise IndexError("Pop from an empty list.")
            
        popped_data = self.head.data
        self.head = self.head.next # Shift the pointer!
        
        self.length -= 1
        if self.length == 0:
            self.tail = None
            
        return popped_data

    def display(self) -> list:
        """O(N) Traversal. Useful for debugging."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE O(N) VS O(1) PERFORMANCE TEST)
# ==============================================================================
def demonstrate_data_structures():
    section_header("Data Structures: The Big-O Memory Crash")
    
    # We will simulate popping the first element 100,000 times!
    ITEMS = 100_000
    
    # --- TEST 1: THE PYTHON LIST (O(N) CATASTROPHE) ---
    print(f"  [TEST 1] Python Standard `list`: Popping Index 0 {ITEMS:,} times.")
    
    python_list = list(range(ITEMS))
    
    start_list = timeit.default_timer()
    while python_list:
        # EVERY single pop forces the CPU to physically shift thousands of integers in RAM!
        python_list.pop(0) 
    end_list = timeit.default_timer()
    
    time_list = end_list - start_list
    print(f"    -> [CATASTROPHE] Execution Time: {time_list:.4f} seconds.")


    # --- TEST 2: THE CUSTOM LINKED LIST (O(1) PERFECTION) ---
    print(f"\n  [TEST 2] Custom `LinkedList`: Popping Head {ITEMS:,} times.")
    
    linked_list = SinglyLinkedList()
    for i in range(ITEMS):
        linked_list.append(i)
        
    start_ll = timeit.default_timer()
    while linked_list.head:
        # This is a mathematical pointer shift. No memory blocks are moved!
        linked_list.pop_first()
    end_ll = timeit.default_timer()
    
    time_ll = end_ll - start_ll
    print(f"    -> [PERFECTION] Execution Time: {time_ll:.4f} seconds.")
    
    
    # --- CONCLUSION ---
    if time_ll > 0:
        speedup = time_list / time_ll
        print(f"\n  [CONCLUSION] The Linked List was {speedup:.0f}x faster!")
        print("  By understanding computer memory architecture, you averted a server crash.")


def run_all_labs():
    demonstrate_data_structures()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "If a Linked List is mathematically $10,000\\times$ faster at inserting and deleting items than a standard Array, why don't we use Linked Lists for everything?"
   Senior Answer: "Cache Locality and Traversal Speed. In a standard C-Array (a Python List), the $1,000,000$ integers are physically stored in a perfectly contiguous block of silicon in RAM. When the CPU reads index $0$, it automatically pre-fetches the next $64$ bytes into the ultra-fast L1 CPU Cache. Arrays are mathematically $O(1)$ for random access (`arr[500]`). A Linked List is composed of isolated Nodes scattered randomly across billions of bytes of RAM. To find the $500^{th}$ Node, the CPU must mathematically traverse all $499$ previous pointers. The CPU cannot pre-fetch the data, resulting in catastrophic 'Cache Misses'. Therefore, Arrays are vastly superior for reading and searching, while Linked Lists are only superior for aggressive front-end insertions and deletions."

2. Interviewer: "What is a 'Queue', what is a 'Stack', and how do they mathematically differ?"
   Senior Answer: "They are abstract architectural wrappers around lists or arrays. A Queue enforces a FIFO (First-In, First-Out) mathematical constraint. Like a line at a grocery store, elements are appended to the Tail and popped from the Head. Queues are mandatory for tasks like web server request routing or breadth-first search algorithms. A Stack enforces a LIFO (Last-In, First-Out) mathematical constraint. Like a stack of plates, elements are 'Pushed' onto the Top and 'Popped' off the Top. Stacks are mandatory for tracking browser history (the 'Back' button) or executing Depth-First Search algorithms. In Python, a Stack can be perfectly executed using a standard List (`append()` and `pop()`), but a Queue MUST be executed using `collections.deque` to prevent $O(N)$ memory shifting."

3. Interviewer: "When we execute `self.head = self.head.next`, what mathematically happens to the original `head` Node in the computer's memory?"
   Senior Answer: "It becomes an 'Orphan'. In low-level languages like C or C++, if you shift a pointer without explicitly commanding the OS to `free()` the original memory block, that data remains permanently locked in RAM, causing a catastrophic 'Memory Leak'. However, Python utilizes an automated 'Garbage Collector' based on Reference Counting. When we shift the pointer to `next`, the Reference Count for the original Node mathematically drops to exactly $0$. The Python Virtual Machine detects this $0$, instantly executes a deletion sequence, and physically returns those bytes to the Operating System, ensuring absolute memory integrity without developer intervention."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Data Structures) Completed.")
