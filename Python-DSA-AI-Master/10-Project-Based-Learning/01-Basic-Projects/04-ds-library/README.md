# Data Structures Library (DS Library)

## 1. Project Overview
The **DS Library** is a comprehensive, production-grade Python library implementing fundamental Data Structures from scratch. While Python provides many built-in data structures (like lists, dicts, and sets), understanding and implementing core structures such as Linked Lists, Trees, Graphs, and Heaps is critical for foundational computer science knowledge, algorithm optimization, and technical interviews.

## 2. Purpose and Learning Outcomes
- **Memory Management & References**: Understand how nodes are connected via references (pointers) in Python to form complex structures like Trees and Linked Lists.
- **Time and Space Complexity**: Analyze the trade-offs of different data structures. Why is searching a Hash Table \(O(1)\) while searching an unsorted array is \(O(N)\)? Why use a Binary Search Tree instead of an Array?
- **Object-Oriented Programming (OOP)**: Leverage classes, inheritance, dunder methods (e.g., `__iter__`, `__len__`, `__str__`), and encapsulation to build reusable and pythonic APIs.
- **Testing and Verification**: Write rigorous unit tests using `pytest` or `unittest` to ensure that boundary conditions (e.g., deleting from an empty tree, handling hash collisions) are elegantly handled.

## 3. Data Structures Implemented
The library is designed to include the following core structures:
1. **Singly and Doubly Linked Lists**: Dynamic linear structures that allow efficient insertions and deletions.
2. **Stacks and Queues**: LIFO (Last-In-First-Out) and FIFO (First-In-First-Out) structures.
3. **Binary Search Trees (BST)**: Hierarchical structures for efficient \(O(\log N)\) searching, insertion, and deletion.
4. **Heaps (Min-Heap / Max-Heap)**: Priority queue implementations.
5. **Hash Tables**: Custom dictionary implementations dealing with collision resolution (chaining or open addressing).
6. **Graphs**: Adjacency list and adjacency matrix representations, along with Traversal algorithms (BFS, DFS).

## 4. Technical Requirements
- **Language**: Python 3.9+ (utilizing modern type hinting).
- **Libraries**: No third-party dependencies for the core logic. 
- **Testing**: `unittest` or `pytest` suite required for every module.

## 5. Architecture and Design
Each data structure should be implemented in its own module (e.g., `linked_list.py`, `bst.py`) and expose a clean, documented API.

### Design Principles:
- **Type Hinting**: All methods must include Python type hints (`typing` module) to clarify expected inputs and outputs.
- **Pythonic Interfaces**: Implement dunder methods where appropriate. A user should be able to call `len(my_linked_list)` or iterate via `for item in my_linked_list:`.
- **Exception Handling**: Raise built-in Python exceptions (`IndexError`, `KeyError`, `ValueError`) when operations are invalid, mimicking standard library behavior.

## 6. Usage Examples

```python
# Example: Using the Custom Singly Linked List
from ds_library.linked_list import SinglyLinkedList

# Initialization
ll = SinglyLinkedList()

# Appending elements
ll.append(10)
ll.append(20)
ll.append(30)

# Displaying
print(ll) # Output: 10 -> 20 -> 30 -> None

# Deletion
ll.delete_value(20)
print(ll) # Output: 10 -> 30 -> None
```

## 7. Future Enhancements & Advanced Topics
- **Self-Balancing Trees**: Extend the BST implementation to AVL Trees or Red-Black Trees to guarantee \(O(\log N)\) worst-case time complexities.
- **Tries (Prefix Trees)**: Implement a Trie structure for efficient string matching and autocomplete algorithms.
- **Graph Algorithms**: Add pathfinding algorithms like Dijkstra's, A*, or minimum spanning tree algorithms like Kruskal's or Prim's to the Graph module.

## 8. Common Interview Questions Supported by this Library
- "Reverse a Linked List."
- "Implement a Queue using Stacks."
- "Detect a cycle in a Directed Graph."
- "Find the lowest common ancestor in a Binary Search Tree."
Working through this project provides the exact foundational knowledge needed to tackle these problems confidently.
