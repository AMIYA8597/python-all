#!/usr/bin/env python3
"""
Binary Search Tree Implementation - Comprehensive Guide
======================================================

This module demonstrates binary search tree implementations with detailed analysis
of operations, traversal algorithms, and advanced BST concepts.

Topics Covered:
- BST properties and invariants
- Multiple implementation approaches
- Tree traversal algorithms (inorder, preorder, postorder, level-order)
- BST operations (insert, delete, search, min, max)
- Tree balancing concepts
- Performance analysis and optimization
- Real-world applications

Author: Python DSA Master Course
Version: 1.0
"""

import sys
from typing import Optional, List, Iterator, Tuple, Any
from collections import deque
from dataclasses import dataclass
import random


# ============================================================================
# SECTION 1: BASIC BST NODE AND IMPLEMENTATION
# ============================================================================

@dataclass
class TreeNode:
    """
    Binary Search Tree Node.
    
    Properties:
    - Left child contains values less than node value
    - Right child contains values greater than node value
    - No duplicate values (in basic implementation)
    """
    val: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None
    
    def __str__(self) -> str:
        return str(self.val)
    
    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class BinarySearchTree:
    """
    Binary Search Tree implementation with comprehensive operations.
    
    BST Invariant: For any node n:
    - All nodes in left subtree have values < n.val  
    - All nodes in right subtree have values > n.val
    - Both subtrees are also BSTs
    """
    
    def __init__(self):
        """Initialize empty BST."""
        self.root: Optional[TreeNode] = None
        self.size: int = 0
    
    def insert(self, val: int) -> None:
        """
        Insert value into BST.
        
        Time Complexity: O(h) where h is height
        - Best case (balanced): O(log n)
        - Worst case (skewed): O(n)
        Space Complexity: O(h) due to recursion stack
        """
        self.root = self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: Optional[TreeNode], val: int) -> TreeNode:
        """Recursive helper for insertion."""
        # Base case: create new node
        if node is None:
            self.size += 1
            return TreeNode(val)
        
        # Recursive cases
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        # If val == node.val, do nothing (no duplicates)
        
        return node
    
    def search(self, val: int) -> bool:
        """
        Search for value in BST.
        
        Time Complexity: O(h)
        Space Complexity: O(h) recursive, O(1) iterative
        """
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[TreeNode], val: int) -> bool:
        """Recursive search implementation."""
        if node is None:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def search_iterative(self, val: int) -> bool:
        """
        Iterative search implementation.
        
        More memory efficient than recursive version.
        """
        current = self.root
        
        while current is not None:
            if val == current.val:
                return True
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        
        return False
    
    def delete(self, val: int) -> None:
        """
        Delete value from BST.
        
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """Recursive helper for deletion."""
        if node is None:
            return None
        
        # Find the node to delete
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node to delete found
            self.size -= 1
            
            # Case 1: Node has no children (leaf)
            if node.left is None and node.right is None:
                return None
            
            # Case 2: Node has one child
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # Case 3: Node has two children
            # Find inorder successor (smallest value in right subtree)
            successor = self._find_min(node.right)
            node.val = successor.val
            # Delete the successor (which has at most one child)
            node.right = self._delete_recursive(node.right, successor.val)
            self.size += 1  # Compensate for the extra decrement
        
        return node
    
    def find_min(self) -> Optional[int]:
        """Find minimum value in BST."""
        if self.root is None:
            return None
        return self._find_min(self.root).val
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """Helper to find minimum node in subtree."""
        while node.left is not None:
            node = node.left
        return node
    
    def find_max(self) -> Optional[int]:
        """Find maximum value in BST."""
        if self.root is None:
            return None
        return self._find_max(self.root).val
    
    def _find_max(self, node: TreeNode) -> TreeNode:
        """Helper to find maximum node in subtree."""
        while node.right is not None:
            node = node.right
        return node
    
    def height(self) -> int:
        """
        Calculate height of BST.
        
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node: Optional[TreeNode]) -> int:
        """Recursive helper for height calculation."""
        if node is None:
            return -1  # Height of empty tree is -1
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return 1 + max(left_height, right_height)
    
    def is_empty(self) -> bool:
        """Check if BST is empty."""
        return self.root is None
    
    def __len__(self) -> int:
        """Return number of nodes in BST."""
        return self.size
    
    def __bool__(self) -> bool:
        """Return True if BST is not empty."""
        return not self.is_empty()
    
    def __contains__(self, val: int) -> bool:
        """Support 'in' operator."""
        return self.search(val)


# ============================================================================
# SECTION 2: TREE TRAVERSAL ALGORITHMS
# ============================================================================

class TreeTraversal:
    """
    Collection of tree traversal algorithms.
    
    Different traversals serve different purposes:
    - Inorder: Gives sorted order for BST
    - Preorder: Useful for copying/serializing tree
    - Postorder: Useful for deletion/cleanup
    - Level-order: Breadth-first traversal
    """
    
    @staticmethod
    def inorder_recursive(root: Optional[TreeNode]) -> List[int]:
        """
        Inorder traversal: Left -> Root -> Right
        
        For BST, produces sorted order.
        Time Complexity: O(n)
        Space Complexity: O(h) recursion stack
        """
        result = []
        
        def inorder(node: Optional[TreeNode]) -> None:
            if node is not None:
                inorder(node.left)
                result.append(node.val)
                inorder(node.right)
        
        inorder(root)
        return result
    
    @staticmethod
    def inorder_iterative(root: Optional[TreeNode]) -> List[int]:
        """
        Iterative inorder traversal using stack.
        
        More memory efficient for deep trees.
        """
        result = []
        stack = []
        current = root
        
        while stack or current:
            # Go to leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            result.append(current.val)
            
            # Move to right subtree
            current = current.right
        
        return result
    
    @staticmethod
    def preorder_recursive(root: Optional[TreeNode]) -> List[int]:
        """
        Preorder traversal: Root -> Left -> Right
        
        Useful for creating copy of tree structure.
        """
        result = []
        
        def preorder(node: Optional[TreeNode]) -> None:
            if node is not None:
                result.append(node.val)
                preorder(node.left)
                preorder(node.right)
        
        preorder(root)
        return result
    
    @staticmethod
    def preorder_iterative(root: Optional[TreeNode]) -> List[int]:
        """Iterative preorder traversal."""
        if root is None:
            return []
        
        result = []
        stack = [root]
        
        while stack:
            node = stack.pop()
            result.append(node.val)
            
            # Push right first, then left (stack is LIFO)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return result
    
    @staticmethod
    def postorder_recursive(root: Optional[TreeNode]) -> List[int]:
        """
        Postorder traversal: Left -> Right -> Root
        
        Useful for deletion (children before parent).
        """
        result = []
        
        def postorder(node: Optional[TreeNode]) -> None:
            if node is not None:
                postorder(node.left)
                postorder(node.right)
                result.append(node.val)
        
        postorder(root)
        return result
    
    @staticmethod
    def postorder_iterative(root: Optional[TreeNode]) -> List[int]:
        """Iterative postorder traversal."""
        if root is None:
            return []
        
        result = []
        stack = []
        last_visited = None
        current = root
        
        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                peek_node = stack[-1]
                # If right child exists and hasn't been processed yet
                if peek_node.right and last_visited != peek_node.right:
                    current = peek_node.right
                else:
                    result.append(peek_node.val)
                    last_visited = stack.pop()
        
        return result
    
    @staticmethod
    def level_order(root: Optional[TreeNode]) -> List[List[int]]:
        """
        Level-order (breadth-first) traversal.
        
        Returns list of lists, each containing nodes at that level.
        """
        if root is None:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            level_size = len(queue)
            level_nodes = []
            
            for _ in range(level_size):
                node = queue.popleft()
                level_nodes.append(node.val)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            result.append(level_nodes)
        
        return result
    
    @staticmethod
    def level_order_flat(root: Optional[TreeNode]) -> List[int]:
        """Level-order traversal returning flat list."""
        if root is None:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result


def demonstrate_traversals():
    """Demonstrate different tree traversal algorithms."""
    print("=== TREE TRAVERSAL DEMONSTRATION ===")
    
    # Create sample BST
    #       4
    #      / \
    #     2   6
    #    / \ / \
    #   1  3 5  7
    
    bst = BinarySearchTree()
    values = [4, 2, 6, 1, 3, 5, 7]
    for val in values:
        bst.insert(val)
    
    print(f"BST created with values: {values}")
    print(f"Tree structure:")
    print("       4")
    print("      / \\")
    print("     2   6")
    print("    / \\ / \\")
    print("   1  3 5  7")
    
    # Demonstrate traversals
    root = bst.root
    
    print(f"\nInorder (sorted): {TreeTraversal.inorder_recursive(root)}")
    print(f"Inorder iterative: {TreeTraversal.inorder_iterative(root)}")
    
    print(f"\nPreorder: {TreeTraversal.preorder_recursive(root)}")
    print(f"Preorder iterative: {TreeTraversal.preorder_iterative(root)}")
    
    print(f"\nPostorder: {TreeTraversal.postorder_recursive(root)}")
    print(f"Postorder iterative: {TreeTraversal.postorder_iterative(root)}")
    
    print(f"\nLevel-order (by levels): {TreeTraversal.level_order(root)}")
    print(f"Level-order (flat): {TreeTraversal.level_order_flat(root)}")


# ============================================================================
# SECTION 3: ADVANCED BST OPERATIONS
# ============================================================================

class AdvancedBST(BinarySearchTree):
    """
    Extended BST with advanced operations.
    """
    
    def find_kth_smallest(self, k: int) -> Optional[int]:
        """
        Find kth smallest element (1-indexed).
        
        Time Complexity: O(h + k)
        Space Complexity: O(h)
        """
        def inorder_kth(node: Optional[TreeNode], count: List[int]) -> Optional[int]:
            if node is None:
                return None
            
            # Check left subtree first
            result = inorder_kth(node.left, count)
            if result is not None:
                return result
            
            # Process current node
            count[0] += 1
            if count[0] == k:
                return node.val
            
            # Check right subtree
            return inorder_kth(node.right, count)
        
        if k <= 0 or k > self.size:
            return None
        
        return inorder_kth(self.root, [0])
    
    def find_kth_largest(self, k: int) -> Optional[int]:
        """Find kth largest element (1-indexed)."""
        return self.find_kth_smallest(self.size - k + 1)
    
    def range_query(self, low: int, high: int) -> List[int]:
        """
        Find all values in range [low, high].
        
        Time Complexity: O(h + k) where k is number of nodes in range
        Space Complexity: O(h + k)
        """
        result = []
        
        def range_search(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            
            # If current value is in range, it might be in result
            if low <= node.val <= high:
                # Check left subtree
                if node.left:
                    range_search(node.left)
                
                # Add current value
                result.append(node.val)
                
                # Check right subtree
                if node.right:
                    range_search(node.right)
            
            # If current value is greater than high, only check left
            elif node.val > high:
                if node.left:
                    range_search(node.left)
            
            # If current value is less than low, only check right
            elif node.val < low:
                if node.right:
                    range_search(node.right)
        
        range_search(self.root)
        return result
    
    def lowest_common_ancestor(self, p: int, q: int) -> Optional[int]:
        """
        Find lowest common ancestor of two values.
        
        Time Complexity: O(h)
        Space Complexity: O(1) iterative, O(h) recursive
        """
        def lca_recursive(node: Optional[TreeNode]) -> Optional[TreeNode]:
            if node is None:
                return None
            
            # Both values are in left subtree
            if p < node.val and q < node.val:
                return lca_recursive(node.left)
            
            # Both values are in right subtree
            elif p > node.val and q > node.val:
                return lca_recursive(node.right)
            
            # Values are on different sides, or one equals current node
            else:
                return node
        
        lca_node = lca_recursive(self.root)
        return lca_node.val if lca_node else None
    
    def is_valid_bst(self) -> bool:
        """
        Validate if tree maintains BST property.
        
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def validate(node: Optional[TreeNode], min_val: float, max_val: float) -> bool:
            if node is None:
                return True
            
            # Check if current node violates BST property
            if node.val <= min_val or node.val >= max_val:
                return False
            
            # Recursively validate subtrees with updated bounds
            return (validate(node.left, min_val, node.val) and
                    validate(node.right, node.val, max_val))
        
        return validate(self.root, float('-inf'), float('inf'))
    
    def diameter(self) -> int:
        """
        Find diameter of tree (longest path between any two nodes).
        
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        max_diameter = [0]
        
        def height_and_diameter(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            
            left_height = height_and_diameter(node.left)
            right_height = height_and_diameter(node.right)
            
            # Diameter through this node
            current_diameter = left_height + right_height
            max_diameter[0] = max(max_diameter[0], current_diameter)
            
            # Return height of subtree rooted at this node
            return 1 + max(left_height, right_height)
        
        height_and_diameter(self.root)
        return max_diameter[0]
    
    def path_sum(self, target: int) -> List[List[int]]:
        """
        Find all root-to-leaf paths that sum to target.
        
        Time Complexity: O(n * h) worst case
        Space Complexity: O(h)
        """
        result = []
        
        def dfs(node: Optional[TreeNode], current_path: List[int], current_sum: int) -> None:
            if node is None:
                return
            
            # Add current node to path
            current_path.append(node.val)
            current_sum += node.val
            
            # If leaf node and sum equals target
            if node.left is None and node.right is None and current_sum == target:
                result.append(current_path[:])  # Copy current path
            else:
                # Continue searching in subtrees
                dfs(node.left, current_path, current_sum)
                dfs(node.right, current_path, current_sum)
            
            # Backtrack
            current_path.pop()
        
        dfs(self.root, [], 0)
        return result


def demonstrate_advanced_operations():
    """Demonstrate advanced BST operations."""
    print(f"\n=== ADVANCED BST OPERATIONS ===")
    
    # Create BST with more values
    bst = AdvancedBST()
    values = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    for val in values:
        bst.insert(val)
    
    print(f"BST created with values: {values}")
    
    # Kth smallest/largest
    print(f"\n1st smallest: {bst.find_kth_smallest(1)}")
    print(f"5th smallest: {bst.find_kth_smallest(5)}")
    print(f"1st largest: {bst.find_kth_largest(1)}")
    print(f"3rd largest: {bst.find_kth_largest(3)}")
    
    # Range query
    print(f"\nRange [5, 12]: {bst.range_query(5, 12)}")
    print(f"Range [1, 6]: {bst.range_query(1, 6)}")
    
    # LCA
    print(f"\nLCA(2, 6): {bst.lowest_common_ancestor(2, 6)}")
    print(f"LCA(1, 15): {bst.lowest_common_ancestor(1, 15)}")
    print(f"LCA(10, 14): {bst.lowest_common_ancestor(10, 14)}")
    
    # Validation
    print(f"\nIs valid BST: {bst.is_valid_bst()}")
    
    # Diameter
    print(f"Tree diameter: {bst.diameter()}")
    
    # Path sum
    target_sum = 15
    paths = bst.path_sum(target_sum)
    print(f"\nPaths summing to {target_sum}:")
    for path in paths:
        print(f"  {' -> '.join(map(str, path))} = {sum(path)}")


# ============================================================================
# SECTION 4: PERFORMANCE ANALYSIS AND BENCHMARKING
# ============================================================================

def benchmark_bst_operations():
    """Benchmark BST operations for different tree shapes."""
    print(f"\n=== PERFORMANCE BENCHMARKING ===")
    
    import time
    
    def create_balanced_bst(n: int) -> BinarySearchTree:
        """Create a balanced BST."""
        bst = BinarySearchTree()
        values = list(range(1, n + 1))
        random.shuffle(values)
        for val in values:
            bst.insert(val)
        return bst
    
    def create_skewed_bst(n: int) -> BinarySearchTree:
        """Create a skewed (worst-case) BST."""
        bst = BinarySearchTree()
        for i in range(1, n + 1):
            bst.insert(i)
        return bst
    
    # Test sizes
    sizes = [1000, 5000, 10000]
    
    for size in sizes:
        print(f"\nBenchmarking with {size} nodes:")
        
        # Create trees
        balanced_bst = create_balanced_bst(size)
        skewed_bst = create_skewed_bst(size)
        
        # Benchmark search operations
        search_values = random.sample(range(1, size + 1), min(100, size))
        
        # Balanced tree search
        start = time.perf_counter()
        for val in search_values:
            balanced_bst.search(val)
        balanced_time = time.perf_counter() - start
        
        # Skewed tree search
        start = time.perf_counter()
        for val in search_values:
            skewed_bst.search(val)
        skewed_time = time.perf_counter() - start
        
        print(f"  Search 100 elements:")
        print(f"    Balanced BST: {balanced_time:.6f}s")
        print(f"    Skewed BST: {skewed_time:.6f}s")
        print(f"    Speedup: {skewed_time / balanced_time:.1f}x")
        
        # Tree properties
        print(f"  Tree heights:")
        print(f"    Balanced BST: {balanced_bst.height()}")
        print(f"    Skewed BST: {skewed_bst.height()}")


# ============================================================================
# SECTION 5: REAL-WORLD APPLICATIONS
# ============================================================================

class DatabaseIndex:
    """
    Simplified database index using BST.
    
    Demonstrates BST usage in database systems for fast lookups.
    """
    
    def __init__(self):
        self.index = BinarySearchTree()
        self.records = {}  # Value -> Record mapping
    
    def insert_record(self, key: int, record: dict) -> None:
        """Insert a record with given key."""
        self.index.insert(key)
        self.records[key] = record
    
    def find_record(self, key: int) -> Optional[dict]:
        """Find record by key."""
        if self.index.search(key):
            return self.records[key]
        return None
    
    def range_scan(self, low: int, high: int) -> List[dict]:
        """Find all records with keys in range."""
        if not hasattr(self.index, 'range_query'):
            return []
        
        keys_in_range = self.index.range_query(low, high)
        return [self.records[key] for key in keys_in_range]
    
    def delete_record(self, key: int) -> bool:
        """Delete record by key."""
        if self.index.search(key):
            self.index.delete(key)
            del self.records[key]
            return True
        return False


class PriorityQueue:
    """
    Priority queue implementation using BST.
    
    Supports operations with priorities as integers.
    """
    
    def __init__(self):
        self.bst = BinarySearchTree()
        self.items = {}  # Priority -> List of items
        self.size = 0
    
    def enqueue(self, item: Any, priority: int) -> None:
        """Add item with given priority."""
        if priority not in self.items:
            self.bst.insert(priority)
            self.items[priority] = []
        
        self.items[priority].append(item)
        self.size += 1
    
    def dequeue(self) -> Optional[Tuple[Any, int]]:
        """Remove and return highest priority item."""
        if self.size == 0:
            return None
        
        max_priority = self.bst.find_max()
        if max_priority is None:
            return None
        
        item = self.items[max_priority].pop()
        self.size -= 1
        
        if not self.items[max_priority]:
            del self.items[max_priority]
            self.bst.delete(max_priority)
        
        return item, max_priority
    
    def peek(self) -> Optional[Tuple[Any, int]]:
        """View highest priority item without removing."""
        if self.size == 0:
            return None
        
        max_priority = self.bst.find_max()
        if max_priority is None or not self.items[max_priority]:
            return None
        
        return self.items[max_priority][-1], max_priority
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.size == 0


def demonstrate_applications():
    """Demonstrate real-world BST applications."""
    print(f"\n=== REAL-WORLD APPLICATIONS ===")
    
    # Database Index demonstration
    print("1. Database Index Simulation:")
    db_index = DatabaseIndex()
    
    # Insert some records
    records = [
        (101, {"name": "Alice", "age": 25, "dept": "Engineering"}),
        (205, {"name": "Bob", "age": 30, "dept": "Marketing"}),
        (150, {"name": "Charlie", "age": 28, "dept": "Engineering"}),
        (300, {"name": "Diana", "age": 32, "dept": "Finance"}),
        (175, {"name": "Eve", "age": 26, "dept": "Engineering"})
    ]
    
    for emp_id, record in records:
        db_index.insert_record(emp_id, record)
    
    # Demonstrate lookups
    print(f"  Find employee 150: {db_index.find_record(150)}")
    print(f"  Find employee 999: {db_index.find_record(999)}")
    
    # Range scan
    print(f"  Employees with IDs 140-200:")
    for record in db_index.range_scan(140, 200):
        print(f"    {record}")
    
    # Priority Queue demonstration
    print(f"\n2. Priority Queue Simulation:")
    pq = PriorityQueue()
    
    # Add tasks with priorities
    tasks = [
        ("Fix critical bug", 10),
        ("Write documentation", 3),
        ("Code review", 7),
        ("Deploy to production", 9),
        ("Team meeting", 4)
    ]
    
    for task, priority in tasks:
        pq.enqueue(task, priority)
        print(f"  Enqueued: '{task}' (priority {priority})")
    
    print(f"\n  Processing tasks by priority:")
    while not pq.is_empty():
        task, priority = pq.dequeue()
        print(f"  Processing: '{task}' (priority {priority})")


# ============================================================================
# SECTION 6: TESTING AND VALIDATION
# ============================================================================

def test_bst_operations():
    """Comprehensive testing of BST operations."""
    print(f"\n=== TESTING BST OPERATIONS ===")
    
    # Basic operations test
    print("Testing basic operations:")
    bst = BinarySearchTree()
    
    # Test empty BST
    assert bst.is_empty(), "New BST should be empty"
    assert len(bst) == 0, "Empty BST should have size 0"
    assert bst.find_min() is None, "Empty BST min should be None"
    assert bst.find_max() is None, "Empty BST max should be None"
    
    # Test insertions
    values = [5, 3, 7, 1, 4, 6, 8]
    for val in values:
        bst.insert(val)
    
    assert len(bst) == len(values), f"Size should be {len(values)}"
    assert not bst.is_empty(), "BST with elements should not be empty"
    
    # Test search
    for val in values:
        assert bst.search(val), f"Should find {val}"
        assert val in bst, f"Should find {val} using 'in' operator"
    
    assert not bst.search(10), "Should not find 10"
    assert 10 not in bst, "Should not find 10 using 'in' operator"
    
    # Test min/max
    assert bst.find_min() == 1, "Min should be 1"
    assert bst.find_max() == 8, "Max should be 8"
    
    # Test traversals
    inorder = TreeTraversal.inorder_recursive(bst.root)
    assert inorder == sorted(values), "Inorder should give sorted order"
    
    # Test deletion
    bst.delete(3)  # Node with two children
    assert not bst.search(3), "Should not find deleted node"
    assert len(bst) == len(values) - 1, "Size should decrease"
    
    bst.delete(1)  # Leaf node
    bst.delete(8)  # Leaf node
    assert len(bst) == len(values) - 3, "Size should decrease"
    
    print("  Basic operations: All tests passed!")
    
    # Advanced operations test
    print("Testing advanced operations:")
    advanced_bst = AdvancedBST()
    test_values = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]
    for val in test_values:
        advanced_bst.insert(val)
    
    # Test kth smallest/largest
    assert advanced_bst.find_kth_smallest(1) == 1, "1st smallest should be 1"
    assert advanced_bst.find_kth_smallest(8) == 8, "8th smallest should be 8"
    assert advanced_bst.find_kth_largest(1) == 15, "1st largest should be 15"
    
    # Test validation
    assert advanced_bst.is_valid_bst(), "BST should be valid"
    
    # Test LCA
    assert advanced_bst.lowest_common_ancestor(1, 3) == 2, "LCA(1,3) should be 2"
    assert advanced_bst.lowest_common_ancestor(1, 15) == 8, "LCA(1,15) should be 8"
    
    print("  Advanced operations: All tests passed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Binary Search Tree Implementation - Comprehensive Demonstration")
    print("=" * 70)
    
    try:
        # Basic BST operations
        bst = BinarySearchTree()
        print("=== BASIC BST DEMONSTRATION ===")
        
        values = [8, 3, 10, 1, 6, 9, 14, 4, 7, 13]
        print(f"Inserting values: {values}")
        
        for val in values:
            bst.insert(val)
        
        print(f"BST size: {len(bst)}")
        print(f"BST height: {bst.height()}")
        print(f"Min value: {bst.find_min()}")
        print(f"Max value: {bst.find_max()}")
        
        # Search demonstrations
        search_values = [6, 15, 1, 12]
        for val in search_values:
            found = bst.search(val)
            print(f"Search {val}: {'Found' if found else 'Not found'}")
        
        # Run all demonstrations
        demonstrate_traversals()
        demonstrate_advanced_operations()
        benchmark_bst_operations()
        demonstrate_applications()
        test_bst_operations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 70}")
        print("Binary Search Tree demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement iterative versions of insert and delete operations.

2. Create a BST that allows duplicate values.

3. Implement Morris traversal for O(1) space inorder traversal.

4. Build a balanced BST from sorted array.

5. Implement BST serialization and deserialization.

6. Create a threaded BST for efficient inorder traversal.

7. Implement range sum queries on BST.

8. Build BST with parent pointers for easier navigation.

9. Create persistent BST (immutable with sharing).

10. Implement BST with lazy deletion.

ALGORITHM CHALLENGES:

1. Convert BST to sorted doubly linked list
2. Find pair with given sum in BST
3. Merge two BSTs efficiently
4. Find inorder successor/predecessor
5. Convert sorted list to balanced BST
6. Count nodes in given range
7. Find maximum path sum in BST
8. Implement BST iterator
9. Clone BST with random pointers
10. Find median in stream using BSTs

ADVANCED TOPICS:

1. Self-balancing trees (AVL, Red-Black)
2. B-trees for external storage
3. Treap (randomized BST)
4. Splay trees (self-adjusting)
5. Persistent data structures

SYSTEM DESIGN:

1. Database indexing with BSTs
2. File system directory structure
3. Expression parsing and evaluation
4. Decision trees for ML
5. Game trees for AI (minimax)
"""
