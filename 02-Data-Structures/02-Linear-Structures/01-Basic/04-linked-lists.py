#!/usr/bin/env python3
"""
Comprehensive Linked Lists Implementations
==========================================

This module provides complete implementations of different types of linked lists:
1. Singly Linked List
2. Doubly Linked List
3. Circular Linked List
4. Sorted Linked List
5. Skip List (Advanced)

All implementations include detailed explanations, complexity analysis,
and practical examples.

Author: Python DSA Master
Date: 2024
"""

from typing import Any, Optional, Iterator, Generic, TypeVar
import random

T = TypeVar('T')

# ==============================================================================
# SINGLY LINKED LIST
# ==============================================================================

class SinglyNode(Generic[T]):
    """Node for singly linked list."""
    def __init__(self, data: T):
        self.data: T = data
        self.next: Optional['SinglyNode[T]'] = None
    
    def __str__(self) -> str:
        return str(self.data)

class SinglyLinkedList(Generic[T]):
    """
    Singly Linked List implementation.
    
    Time Complexities:
    - Insert at head: O(1)
    - Insert at tail: O(n) without tail pointer, O(1) with tail pointer
    - Delete: O(n) for searching, O(1) for deletion once found
    - Search: O(n)
    - Access by index: O(n)
    
    Space Complexity: O(n)
    """
    
    def __init__(self):
        self._head: Optional[SinglyNode[T]] = None
        self._tail: Optional[SinglyNode[T]] = None
        self._size = 0
    
    def append(self, data: T) -> None:
        """Add element to end of list."""
        new_node = SinglyNode(data)
        
        if not self._head:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        
        self._size += 1
    
    def prepend(self, data: T) -> None:
        """Add element to beginning of list."""
        new_node = SinglyNode(data)
        
        if not self._head:
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head = new_node
        
        self._size += 1
    
    def insert(self, index: int, data: T) -> None:
        """Insert element at specific index."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        if index == self._size:
            self.append(data)
            return
        
        new_node = SinglyNode(data)
        current = self._head
        
        # Navigate to position before insertion point
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self._size += 1
    
    def delete(self, data: T) -> bool:
        """Delete first occurrence of data."""
        if not self._head:
            return False
        
        # If head needs to be deleted
        if self._head.data == data:
            self._head = self._head.next
            if self._size == 1:  # List becomes empty
                self._tail = None
            self._size -= 1
            return True
        
        current = self._head
        while current.next:
            if current.next.data == data:
                # Update tail if deleting last element
                if current.next == self._tail:
                    self._tail = current
                
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def delete_at_index(self, index: int) -> T:
        """Delete element at specific index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        if index == 0:
            data = self._head.data
            self._head = self._head.next
            if self._size == 1:
                self._tail = None
            self._size -= 1
            return data
        
        current = self._head
        for _ in range(index - 1):
            current = current.next
        
        data = current.next.data
        if current.next == self._tail:
            self._tail = current
        
        current.next = current.next.next
        self._size -= 1
        return data
    
    def find(self, data: T) -> int:
        """Find index of first occurrence of data."""
        current = self._head
        index = 0
        
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        
        return -1
    
    def get(self, index: int) -> T:
        """Get element at specific index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        current = self._head
        for _ in range(index):
            current = current.next
        
        return current.data
    
    def size(self) -> int:
        """Return size of list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self._size == 0
    
    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        if not self._head or not self._head.next:
            return
        
        self._tail = self._head
        prev = None
        current = self._head
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        
        self._head = prev
    
    def to_list(self) -> list[T]:
        """Convert linked list to Python list."""
        result = []
        current = self._head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __iter__(self) -> Iterator[T]:
        """Make linked list iterable."""
        current = self._head
        while current:
            yield current.data
            current = current.next
    
    def __str__(self) -> str:
        return " -> ".join(str(item) for item in self) + " -> None"

# ==============================================================================
# DOUBLY LINKED LIST
# ==============================================================================

class DoublyNode(Generic[T]):
    """Node for doubly linked list."""
    def __init__(self, data: T):
        self.data: T = data
        self.next: Optional['DoublyNode[T]'] = None
        self.prev: Optional['DoublyNode[T]'] = None

class DoublyLinkedList(Generic[T]):
    """
    Doubly Linked List implementation.
    
    Time Complexities:
    - Insert at head/tail: O(1)
    - Delete at head/tail: O(1)
    - Delete by value: O(n)
    - Search: O(n)
    - Access by index: O(n)
    
    Space Complexity: O(n) - uses more memory than singly linked list
    """
    
    def __init__(self):
        self._head: Optional[DoublyNode[T]] = None
        self._tail: Optional[DoublyNode[T]] = None
        self._size = 0
    
    def append(self, data: T) -> None:
        """Add element to end of list."""
        new_node = DoublyNode(data)
        
        if not self._head:
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        
        self._size += 1
    
    def prepend(self, data: T) -> None:
        """Add element to beginning of list."""
        new_node = DoublyNode(data)
        
        if not self._head:
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        
        self._size += 1
    
    def insert(self, index: int, data: T) -> None:
        """Insert element at specific index."""
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.prepend(data)
            return
        
        if index == self._size:
            self.append(data)
            return
        
        new_node = DoublyNode(data)
        
        # Decide whether to traverse from head or tail
        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next
        else:
            current = self._tail
            for _ in range(self._size - index - 1):
                current = current.prev
        
        # Insert before current
        new_node.next = current
        new_node.prev = current.prev
        current.prev.next = new_node
        current.prev = new_node
        
        self._size += 1
    
    def delete(self, data: T) -> bool:
        """Delete first occurrence of data."""
        current = self._head
        
        while current:
            if current.data == data:
                self._delete_node(current)
                return True
            current = current.next
        
        return False
    
    def _delete_node(self, node: DoublyNode[T]) -> None:
        """Helper method to delete a specific node."""
        if node.prev:
            node.prev.next = node.next
        else:
            self._head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:
            self._tail = node.prev
        
        self._size -= 1
    
    def delete_at_index(self, index: int) -> T:
        """Delete element at specific index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        # Navigate to the node
        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next
        else:
            current = self._tail
            for _ in range(self._size - index - 1):
                current = current.prev
        
        data = current.data
        self._delete_node(current)
        return data
    
    def get(self, index: int) -> T:
        """Get element at specific index."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        
        # Optimize by choosing direction
        if index <= self._size // 2:
            current = self._head
            for _ in range(index):
                current = current.next
        else:
            current = self._tail
            for _ in range(self._size - index - 1):
                current = current.prev
        
        return current.data
    
    def reverse(self) -> None:
        """Reverse the doubly linked list in-place."""
        current = self._head
        
        while current:
            # Swap next and prev pointers
            current.next, current.prev = current.prev, current.next
            current = current.prev  # Move to next node (which is now prev)
        
        # Swap head and tail
        self._head, self._tail = self._tail, self._head
    
    def size(self) -> int:
        """Return size of list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self._size == 0
    
    def __iter__(self) -> Iterator[T]:
        """Forward iterator."""
        current = self._head
        while current:
            yield current.data
            current = current.next
    
    def reverse_iter(self) -> Iterator[T]:
        """Reverse iterator."""
        current = self._tail
        while current:
            yield current.data
            current = current.prev
    
    def __str__(self) -> str:
        return " <-> ".join(str(item) for item in self)

# ==============================================================================
# CIRCULAR LINKED LIST
# ==============================================================================

class CircularLinkedList(Generic[T]):
    """
    Circular Linked List implementation.
    
    The last node points back to the first node, forming a circle.
    """
    
    def __init__(self):
        self._head: Optional[SinglyNode[T]] = None
        self._size = 0
    
    def append(self, data: T) -> None:
        """Add element to end of circular list."""
        new_node = SinglyNode(data)
        
        if not self._head:
            self._head = new_node
            new_node.next = new_node  # Points to itself
        else:
            # Find last node
            current = self._head
            while current.next != self._head:
                current = current.next
            
            current.next = new_node
            new_node.next = self._head
        
        self._size += 1
    
    def prepend(self, data: T) -> None:
        """Add element to beginning of circular list."""
        new_node = SinglyNode(data)
        
        if not self._head:
            self._head = new_node
            new_node.next = new_node
        else:
            # Find last node
            current = self._head
            while current.next != self._head:
                current = current.next
            
            new_node.next = self._head
            current.next = new_node
            self._head = new_node
        
        self._size += 1
    
    def delete(self, data: T) -> bool:
        """Delete first occurrence of data."""
        if not self._head:
            return False
        
        # If only one node
        if self._size == 1 and self._head.data == data:
            self._head = None
            self._size = 0
            return True
        
        # If head needs to be deleted
        if self._head.data == data:
            # Find last node
            current = self._head
            while current.next != self._head:
                current = current.next
            
            current.next = self._head.next
            self._head = self._head.next
            self._size -= 1
            return True
        
        # Search for node to delete
        current = self._head
        while current.next != self._head:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, data: T) -> int:
        """Find index of first occurrence of data."""
        if not self._head:
            return -1
        
        current = self._head
        index = 0
        
        while True:
            if current.data == data:
                return index
            current = current.next
            index += 1
            
            if current == self._head:  # Completed circle
                break
        
        return -1
    
    def size(self) -> int:
        """Return size of list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self._size == 0
    
    def display(self, max_rounds: int = 2) -> str:
        """Display circular list with indication of circularity."""
        if not self._head:
            return "Empty"
        
        items = []
        current = self._head
        count = 0
        max_items = self._size * max_rounds
        
        while count < max_items:
            items.append(str(current.data))
            current = current.next
            count += 1
            
            if current == self._head and count >= self._size:
                items.append("...")
                break
        
        return " -> ".join(items) + " -> (back to start)"

# ==============================================================================
# SORTED LINKED LIST
# ==============================================================================

class SortedLinkedList(Generic[T]):
    """
    Sorted Linked List that maintains elements in sorted order.
    
    All insertions maintain the sorted property.
    """
    
    def __init__(self, reverse: bool = False):
        self._head: Optional[SinglyNode[T]] = None
        self._size = 0
        self._reverse = reverse  # True for descending order
    
    def insert(self, data: T) -> None:
        """Insert data while maintaining sorted order."""
        new_node = SinglyNode(data)
        
        # Empty list or insert at beginning
        if not self._head or self._should_insert_before(data, self._head.data):
            new_node.next = self._head
            self._head = new_node
            self._size += 1
            return
        
        # Find correct position
        current = self._head
        while current.next and not self._should_insert_before(data, current.next.data):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self._size += 1
    
    def _should_insert_before(self, new_data: T, existing_data: T) -> bool:
        """Determine if new_data should be inserted before existing_data."""
        if self._reverse:
            return new_data > existing_data
        else:
            return new_data < existing_data
    
    def delete(self, data: T) -> bool:
        """Delete first occurrence of data."""
        if not self._head:
            return False
        
        # Delete head
        if self._head.data == data:
            self._head = self._head.next
            self._size -= 1
            return True
        
        current = self._head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def search(self, data: T) -> bool:
        """Search for data (optimized for sorted list)."""
        current = self._head
        
        while current:
            if current.data == data:
                return True
            
            # Early termination for sorted list
            if self._should_insert_before(data, current.data):
                break
            
            current = current.next
        
        return False
    
    def size(self) -> int:
        """Return size of list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if list is empty."""
        return self._size == 0
    
    def __iter__(self) -> Iterator[T]:
        """Make list iterable."""
        current = self._head
        while current:
            yield current.data
            current = current.next
    
    def __str__(self) -> str:
        order = "DESC" if self._reverse else "ASC"
        return f"SortedList({order}): {' -> '.join(str(item) for item in self)}"

# ==============================================================================
# SKIP LIST (Advanced)
# ==============================================================================

class SkipListNode(Generic[T]):
    """Node for skip list with multiple forward pointers."""
    def __init__(self, data: T, level: int):
        self.data = data
        self.forward = [None] * (level + 1)

class SkipList(Generic[T]):
    """
    Skip List implementation for fast search, insertion, and deletion.
    
    Average Time Complexities:
    - Search: O(log n)
    - Insert: O(log n)
    - Delete: O(log n)
    
    Space Complexity: O(n log n)
    """
    
    def __init__(self, max_level: int = 16, p: float = 0.5):
        self.max_level = max_level
        self.p = p  # Probability for level promotion
        self.level = 0
        self.header = SkipListNode(None, max_level)
        self._size = 0
    
    def _random_level(self) -> int:
        """Generate random level for new node."""
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level
    
    def search(self, data: T) -> bool:
        """Search for data in skip list."""
        current = self.header
        
        # Start from highest level and move down
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].data is not None and
                   current.forward[i].data < data):
                current = current.forward[i]
        
        # Move to next node at level 0
        current = current.forward[0]
        return current and current.data == data
    
    def insert(self, data: T) -> None:
        """Insert data into skip list."""
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # Find position for insertion
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].data is not None and
                   current.forward[i].data < data):
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # If data already exists, don't insert duplicate
        if current and current.data == data:
            return
        
        # Generate random level for new node
        new_level = self._random_level()
        
        # If new level is greater than current level, update header
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level
        
        # Create new node and update pointers
        new_node = SkipListNode(data, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
        
        self._size += 1
    
    def delete(self, data: T) -> bool:
        """Delete data from skip list."""
        update = [None] * (self.max_level + 1)
        current = self.header
        
        # Find node to delete
        for i in range(self.level, -1, -1):
            while (current.forward[i] and 
                   current.forward[i].data is not None and
                   current.forward[i].data < data):
                current = current.forward[i]
            update[i] = current
        
        current = current.forward[0]
        
        # If node found, delete it
        if current and current.data == data:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            
            # Update level if necessary
            while self.level > 0 and not self.header.forward[self.level]:
                self.level -= 1
            
            self._size -= 1
            return True
        
        return False
    
    def display_levels(self) -> None:
        """Display skip list structure level by level."""
        print(f"Skip List (size: {self._size}, levels: {self.level + 1})")
        for i in range(self.level, -1, -1):
            print(f"Level {i}: ", end="")
            current = self.header.forward[i]
            while current:
                print(f"{current.data}", end="")
                if current.forward[i]:
                    print(" -> ", end="")
                current = current.forward[i]
            print(" -> None")
    
    def size(self) -> int:
        """Return size of skip list."""
        return self._size
    
    def to_list(self) -> list[T]:
        """Convert skip list to sorted list."""
        result = []
        current = self.header.forward[0]
        while current:
            result.append(current.data)
            current = current.forward[0]
        return result

# ==============================================================================
# DEMONSTRATION AND TESTING
# ==============================================================================

def demonstrate_linked_lists():
    """Demonstrate all linked list implementations."""
    
    print("Comprehensive Linked Lists Demonstration")
    print("=" * 50)
    
    # 1. Singly Linked List
    print("\n1. Singly Linked List:")
    sll = SinglyLinkedList()
    
    for i in [3, 1, 4, 1, 5]:
        sll.append(i)
    
    print(f"   After insertions: {sll}")
    print(f"   Size: {sll.size()}")
    print(f"   Element at index 2: {sll.get(2)}")
    print(f"   Find 4: index {sll.find(4)}")
    
    sll.reverse()
    print(f"   After reverse: {sll}")
    
    sll.delete(1)
    print(f"   After deleting 1: {sll}")
    
    # 2. Doubly Linked List
    print("\n2. Doubly Linked List:")
    dll = DoublyLinkedList()
    
    for i in [10, 20, 30, 40]:
        dll.append(i)
    
    print(f"   Forward: {dll}")
    print(f"   Backward: {' <-> '.join(str(item) for item in dll.reverse_iter())}")
    
    dll.insert(2, 25)
    print(f"   After inserting 25 at index 2: {dll}")
    
    deleted = dll.delete_at_index(1)
    print(f"   Deleted element at index 1: {deleted}")
    print(f"   Current list: {dll}")
    
    # 3. Circular Linked List
    print("\n3. Circular Linked List:")
    cll = CircularLinkedList()
    
    for i in ['A', 'B', 'C']:
        cll.append(i)
    
    print(f"   Circular structure: {cll.display()}")
    print(f"   Find 'B': index {cll.find('B')}")
    
    cll.delete('B')
    print(f"   After deleting 'B': {cll.display()}")
    
    # 4. Sorted Linked List
    print("\n4. Sorted Linked List:")
    sorted_asc = SortedLinkedList()
    sorted_desc = SortedLinkedList(reverse=True)
    
    data = [5, 2, 8, 1, 9, 3]
    for item in data:
        sorted_asc.insert(item)
        sorted_desc.insert(item)
    
    print(f"   Ascending: {sorted_asc}")
    print(f"   Descending: {sorted_desc}")
    
    print(f"   Search 8 in ascending: {sorted_asc.search(8)}")
    print(f"   Search 10 in ascending: {sorted_asc.search(10)}")
    
    # 5. Skip List
    print("\n5. Skip List:")
    skip_list = SkipList()
    
    data = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
    for item in data:
        skip_list.insert(item)
    
    skip_list.display_levels()
    print(f"   Sorted order: {skip_list.to_list()}")
    print(f"   Search 12: {skip_list.search(12)}")
    print(f"   Search 15: {skip_list.search(15)}")
    
    skip_list.delete(12)
    print(f"   After deleting 12: {skip_list.to_list()}")

def benchmark_linked_lists():
    """Benchmark different linked list operations."""
    import time
    
    print("\nLinked List Performance Benchmark")
    print("=" * 40)
    
    test_size = 10000
    test_data = list(range(test_size))
    
    # Benchmark insertions
    print(f"Insertion benchmark ({test_size} elements):")
    
    # Singly Linked List - append
    start_time = time.time()
    sll = SinglyLinkedList()
    for item in test_data:
        sll.append(item)
    sll_append_time = time.time() - start_time
    
    # Singly Linked List - prepend
    start_time = time.time()
    sll2 = SinglyLinkedList()
    for item in test_data:
        sll2.prepend(item)
    sll_prepend_time = time.time() - start_time
    
    # Doubly Linked List - append
    start_time = time.time()
    dll = DoublyLinkedList()
    for item in test_data:
        dll.append(item)
    dll_append_time = time.time() - start_time
    
    # Skip List - insert
    start_time = time.time()
    skip_list = SkipList()
    for item in random.sample(test_data, min(1000, test_size)):  # Smaller sample for skip list
        skip_list.insert(item)
    skip_insert_time = time.time() - start_time
    
    print(f"  Singly LL append:    {sll_append_time:.6f} seconds")
    print(f"  Singly LL prepend:   {sll_prepend_time:.6f} seconds")
    print(f"  Doubly LL append:    {dll_append_time:.6f} seconds")
    print(f"  Skip List insert:    {skip_insert_time:.6f} seconds (1000 elements)")
    
    # Benchmark access
    print(f"\nAccess benchmark (middle element):")
    middle_index = test_size // 2
    
    # Singly Linked List
    start_time = time.time()
    sll_middle = sll.get(middle_index)
    sll_access_time = time.time() - start_time
    
    # Doubly Linked List
    start_time = time.time()
    dll_middle = dll.get(middle_index)
    dll_access_time = time.time() - start_time
    
    print(f"  Singly LL get({middle_index}):  {sll_access_time:.6f} seconds")
    print(f"  Doubly LL get({middle_index}):  {dll_access_time:.6f} seconds")
    print(f"  Speedup (Doubly/Singly): {sll_access_time/dll_access_time:.2f}x")

def main():
    """Main demonstration function."""
    demonstrate_linked_lists()
    benchmark_linked_lists()
    
    print("\n" + "=" * 50)
    print("Key Takeaways:")
    print("- Singly Linked List: Simple, memory efficient")
    print("- Doubly Linked List: Bidirectional traversal, faster deletions")
    print("- Circular Linked List: Useful for round-robin scheduling")
    print("- Sorted Linked List: Maintains order automatically")
    print("- Skip List: Probabilistic data structure, O(log n) operations")
    print("- Choose based on use case and performance requirements")

if __name__ == "__main__":
    main()
