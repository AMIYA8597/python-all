#!/usr/bin/env python3
"""
AVL Tree Implementation - Self-Balancing Binary Search Tree
===========================================================

This module demonstrates AVL tree implementation with automatic balancing,
detailed analysis of rotations, and performance comparisons with regular BST.

AVL Tree Properties:
- Binary search tree property maintained
- Balance factor of each node is -1, 0, or 1
- Height difference between left and right subtrees is at most 1
- Automatic rebalancing through rotations

Topics Covered:
- AVL tree properties and invariants
- Single and double rotations
- Balance factor calculation and maintenance
- Insertion with rebalancing
- Deletion with rebalancing
- Height-balanced tree operations
- Performance analysis vs regular BST
- Real-world applications

Author: Python DSA Master Course
Version: 1.0
"""

import sys
from typing import Optional, List, Tuple
from dataclasses import dataclass
import random
import time


# ============================================================================
# SECTION 1: AVL TREE NODE AND BASIC OPERATIONS
# ============================================================================

@dataclass
class AVLNode:
    """
    AVL Tree Node with height tracking.
    
    Properties:
    - val: node value
    - left: left child
    - right: right child
    - height: height of subtree rooted at this node
    """
    val: int
    left: Optional['AVLNode'] = None
    right: Optional['AVLNode'] = None
    height: int = 1  # Height of leaf node is 1
    
    def __str__(self) -> str:
        return f"{self.val}(h={self.height})"
    
    def __repr__(self) -> str:
        return f"AVLNode({self.val}, height={self.height})"


class AVLTree:
    """
    AVL Tree implementation with automatic balancing.
    
    AVL Invariant: For any node n:
    - |height(n.left) - height(n.right)| <= 1
    - Both subtrees are also AVL trees
    - BST property maintained: left < node < right
    """
    
    def __init__(self):
        """Initialize empty AVL tree."""
        self.root: Optional[AVLNode] = None
        self.size: int = 0
    
    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of node (0 for None nodes)."""
        return node.height if node else 0
    
    def _get_balance_factor(self, node: Optional[AVLNode]) -> int:
        """
        Calculate balance factor of node.
        
        Balance Factor = height(left) - height(right)
        - Positive: left-heavy
        - Negative: right-heavy
        - Zero: balanced
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _update_height(self, node: AVLNode) -> None:
        """Update height of node based on children heights."""
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        node.height = 1 + max(left_height, right_height)
    
    # ========================================================================
    # ROTATION OPERATIONS
    # ========================================================================
    
    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Right rotation to fix left-heavy imbalance.
        
        Before rotation:     After rotation:
            y                    x
           / \                  / \
          x   C                A   y
         / \                      / \
        A   B                    B   C
        
        Time Complexity: O(1)
        """
        # Store nodes
        x = y.left
        B = x.right
        
        # Perform rotation
        x.right = y
        y.left = B
        
        # Update heights (order matters!)
        self._update_height(y)  # Update y first (now child)
        self._update_height(x)  # Update x second (now parent)
        
        return x  # New root of this subtree
    
    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Left rotation to fix right-heavy imbalance.
        
        Before rotation:     After rotation:
            x                    y
           / \                  / \
          A   y                x   C
             / \              / \
            B   C            A   B
        
        Time Complexity: O(1)
        """
        # Store nodes
        y = x.right
        B = y.left
        
        # Perform rotation
        y.left = x
        x.right = B
        
        # Update heights (order matters!)
        self._update_height(x)  # Update x first (now child)
        self._update_height(y)  # Update y second (now parent)
        
        return y  # New root of this subtree
    
    def _get_rotation_type(self, node: AVLNode) -> str:
        """Determine which rotation is needed for balancing."""
        balance = self._get_balance_factor(node)
        
        if balance > 1:  # Left heavy
            left_balance = self._get_balance_factor(node.left)
            if left_balance >= 0:
                return "RIGHT"  # Left-Left case
            else:
                return "LEFT_RIGHT"  # Left-Right case
        
        elif balance < -1:  # Right heavy
            right_balance = self._get_balance_factor(node.right)
            if right_balance <= 0:
                return "LEFT"  # Right-Right case
            else:
                return "RIGHT_LEFT"  # Right-Left case
        
        return "NONE"  # Already balanced
    
    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Rebalance node if necessary using appropriate rotations.
        
        Four cases:
        1. Left-Left: Right rotation
        2. Right-Right: Left rotation
        3. Left-Right: Left rotation on left child, then right rotation
        4. Right-Left: Right rotation on right child, then left rotation
        """
        # Update height first
        self._update_height(node)
        
        # Get balance factor
        balance = self._get_balance_factor(node)
        
        # Left heavy cases
        if balance > 1:
            # Left-Right case: convert to Left-Left
            if self._get_balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            
            # Left-Left case: right rotation
            return self._rotate_right(node)
        
        # Right heavy cases
        if balance < -1:
            # Right-Left case: convert to Right-Right
            if self._get_balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            
            # Right-Right case: left rotation
            return self._rotate_left(node)
        
        # Node is balanced
        return node
    
    # ========================================================================
    # INSERTION AND DELETION
    # ========================================================================
    
    def insert(self, val: int) -> None:
        """
        Insert value into AVL tree with automatic rebalancing.
        
        Time Complexity: O(log n)
        Space Complexity: O(log n) due to recursion
        """
        self.root = self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: Optional[AVLNode], val: int) -> AVLNode:
        """Recursive helper for insertion with rebalancing."""
        # Standard BST insertion
        if node is None:
            self.size += 1
            return AVLNode(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        else:
            # Duplicate values not allowed
            return node
        
        # Rebalance the node
        return self._rebalance(node)
    
    def delete(self, val: int) -> None:
        """
        Delete value from AVL tree with automatic rebalancing.
        
        Time Complexity: O(log n)
        Space Complexity: O(log n) due to recursion
        """
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node: Optional[AVLNode], val: int) -> Optional[AVLNode]:
        """Recursive helper for deletion with rebalancing."""
        # Standard BST deletion
        if node is None:
            return None
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node to delete found
            self.size -= 1
            
            # Case 1: Node with only right child or no child
            if node.left is None:
                return node.right
            
            # Case 2: Node with only left child
            if node.right is None:
                return node.left
            
            # Case 3: Node with two children
            # Find inorder successor (smallest in right subtree)
            successor = self._find_min_node(node.right)
            node.val = successor.val
            # Delete the successor
            node.right = self._delete_recursive(node.right, successor.val)
            self.size += 1  # Compensate for extra decrement
        
        # Rebalance the node
        return self._rebalance(node)
    
    def _find_min_node(self, node: AVLNode) -> AVLNode:
        """Find node with minimum value in subtree."""
        while node.left is not None:
            node = node.left
        return node
    
    # ========================================================================
    # SEARCH AND UTILITY OPERATIONS
    # ========================================================================
    
    def search(self, val: int) -> bool:
        """
        Search for value in AVL tree.
        
        Time Complexity: O(log n) - guaranteed due to balance
        Space Complexity: O(log n) recursive, O(1) iterative
        """
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[AVLNode], val: int) -> bool:
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
        """Iterative search (more space efficient)."""
        current = self.root
        
        while current is not None:
            if val == current.val:
                return True
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        
        return False
    
    def find_min(self) -> Optional[int]:
        """Find minimum value in AVL tree."""
        if self.root is None:
            return None
        return self._find_min_node(self.root).val
    
    def find_max(self) -> Optional[int]:
        """Find maximum value in AVL tree."""
        if self.root is None:
            return None
        
        current = self.root
        while current.right is not None:
            current = current.right
        return current.val
    
    def height(self) -> int:
        """Get height of AVL tree."""
        return self._get_height(self.root)
    
    def is_empty(self) -> bool:
        """Check if AVL tree is empty."""
        return self.root is None
    
    def __len__(self) -> int:
        """Return number of nodes in AVL tree."""
        return self.size
    
    def __contains__(self, val: int) -> bool:
        """Support 'in' operator."""
        return self.search(val)
    
    # ========================================================================
    # TRAVERSAL AND VALIDATION
    # ========================================================================
    
    def inorder_traversal(self) -> List[int]:
        """Inorder traversal (sorted order)."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[AVLNode], result: List[int]) -> None:
        """Recursive inorder traversal helper."""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)
    
    def level_order_traversal(self) -> List[List[int]]:
        """Level-order traversal with node heights."""
        if self.root is None:
            return []
        
        result = []
        queue = [(self.root, 0)]  # (node, level)
        current_level = -1
        
        while queue:
            node, level = queue.pop(0)
            
            if level > current_level:
                result.append([])
                current_level = level
            
            result[level].append(node.val)
            
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))
        
        return result
    
    def is_valid_avl(self) -> bool:
        """Validate if tree maintains AVL properties."""
        def validate(node: Optional[AVLNode], min_val: float, max_val: float) -> Tuple[bool, int]:
            if node is None:
                return True, 0
            
            # Check BST property
            if node.val <= min_val or node.val >= max_val:
                return False, 0
            
            # Recursively validate subtrees
            left_valid, left_height = validate(node.left, min_val, node.val)
            right_valid, right_height = validate(node.right, node.val, max_val)
            
            if not left_valid or not right_valid:
                return False, 0
            
            # Check AVL balance property
            if abs(left_height - right_height) > 1:
                return False, 0
            
            # Check height consistency
            expected_height = 1 + max(left_height, right_height)
            if node.height != expected_height:
                return False, 0
            
            return True, expected_height
        
        valid, _ = validate(self.root, float('-inf'), float('inf'))
        return valid
    
    def get_balance_info(self) -> List[Tuple[int, int, int]]:
        """Get balance factor information for all nodes."""
        result = []
        
        def collect_balance_info(node: Optional[AVLNode]) -> None:
            if node is not None:
                balance = self._get_balance_factor(node)
                result.append((node.val, node.height, balance))
                collect_balance_info(node.left)
                collect_balance_info(node.right)
        
        collect_balance_info(self.root)
        return result


# ============================================================================
# SECTION 2: VISUALIZATION AND ANALYSIS
# ============================================================================

def print_tree(node: Optional[AVLNode], level: int = 0, prefix: str = "Root: ") -> None:
    """
    Print AVL tree structure with heights and balance factors.
    """
    if node is not None:
        print(" " * (level * 4) + prefix + f"{node.val} (h={node.height}, bf={_get_balance_factor_for_display(node)})")
        
        if node.left is not None or node.right is not None:
            if node.left:
                print_tree(node.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            
            if node.right:
                print_tree(node.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


def _get_balance_factor_for_display(node: AVLNode) -> int:
    """Helper function for display purposes."""
    left_height = node.left.height if node.left else 0
    right_height = node.right.height if node.right else 0
    return left_height - right_height


def demonstrate_rotations():
    """Demonstrate different types of rotations."""
    print("=== ROTATION DEMONSTRATIONS ===")
    
    # Left-Left case (Right rotation needed)
    print("\n1. Left-Left Case (Right Rotation):")
    avl = AVLTree()
    values = [30, 20, 10]  # Causes left-left imbalance
    
    for val in values:
        avl.insert(val)
        print(f"  After inserting {val}:")
        print_tree(avl.root)
        print()
    
    # Right-Right case (Left rotation needed)
    print("\n2. Right-Right Case (Left Rotation):")
    avl2 = AVLTree()
    values = [10, 20, 30]  # Causes right-right imbalance
    
    for val in values:
        avl2.insert(val)
        print(f"  After inserting {val}:")
        print_tree(avl2.root)
        print()
    
    # Left-Right case
    print("\n3. Left-Right Case (Left-Right Rotation):")
    avl3 = AVLTree()
    values = [30, 10, 20]  # Causes left-right imbalance
    
    for val in values:
        avl3.insert(val)
        print(f"  After inserting {val}:")
        print_tree(avl3.root)
        print()
    
    # Right-Left case
    print("\n4. Right-Left Case (Right-Left Rotation):")
    avl4 = AVLTree()
    values = [10, 30, 20]  # Causes right-left imbalance
    
    for val in values:
        avl4.insert(val)
        print(f"  After inserting {val}:")
        print_tree(avl4.root)
        print()


# ============================================================================
# SECTION 3: PERFORMANCE COMPARISON
# ============================================================================

class SimpleBST:
    """Simple BST for comparison with AVL tree."""
    
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, val):
        self.root = self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node, val):
        if node is None:
            self.size += 1
            return self.Node(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        elif val > node.val:
            node.right = self._insert_recursive(node.right, val)
        
        return node
    
    def search(self, val):
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node, val):
        if node is None:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def height(self):
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        if node is None:
            return -1
        
        return 1 + max(self._height_recursive(node.left),
                      self._height_recursive(node.right))


def benchmark_avl_vs_bst():
    """Compare AVL tree performance with regular BST."""
    print("\n=== PERFORMANCE COMPARISON: AVL vs Regular BST ===")
    
    sizes = [100, 500, 1000]
    
    for size in sizes:
        print(f"\nBenchmarking with {size} nodes:")
        
        # Create trees with worst-case data for BST (sorted)
        sorted_values = list(range(1, size + 1))
        
        # AVL Tree
        avl = AVLTree()
        start = time.perf_counter()
        for val in sorted_values:
            avl.insert(val)
        avl_insert_time = time.perf_counter() - start
        
        # Regular BST (will be skewed)
        bst = SimpleBST()
        start = time.perf_counter()
        for val in sorted_values:
            bst.insert(val)
        bst_insert_time = time.perf_counter() - start
        
        # Search benchmark
        search_values = random.sample(sorted_values, min(50, size))
        
        # AVL search
        start = time.perf_counter()
        for val in search_values:
            avl.search(val)
        avl_search_time = time.perf_counter() - start
        
        # BST search
        start = time.perf_counter()
        for val in search_values:
            bst.search(val)
        bst_search_time = time.perf_counter() - start
        
        print(f"  Insertion time:")
        print(f"    AVL Tree: {avl_insert_time:.6f}s")
        print(f"    BST:      {bst_insert_time:.6f}s")
        
        print(f"  Search time (50 elements):")
        print(f"    AVL Tree: {avl_search_time:.6f}s")
        print(f"    BST:      {bst_search_time:.6f}s")
        print(f"    Speedup:  {bst_search_time / avl_search_time:.1f}x")
        
        print(f"  Tree heights:")
        print(f"    AVL Tree: {avl.height()} (balanced)")
        print(f"    BST:      {bst.height()} (skewed)")


# ============================================================================
# SECTION 4: REAL-WORLD APPLICATIONS
# ============================================================================

class AutoBalancingIndex:
    """
    Database index using AVL tree for guaranteed performance.
    """
    
    def __init__(self):
        self.index = AVLTree()
        self.records = {}
    
    def insert_record(self, key: int, record: dict) -> None:
        """Insert record with guaranteed O(log n) performance."""
        self.index.insert(key)
        self.records[key] = record
    
    def find_record(self, key: int) -> Optional[dict]:
        """Find record with guaranteed O(log n) performance."""
        if self.index.search(key):
            return self.records[key]
        return None
    
    def get_stats(self) -> dict:
        """Get index statistics."""
        return {
            'size': len(self.index),
            'height': self.index.height(),
            'is_balanced': self.index.is_valid_avl(),
            'theoretical_min_height': self._calculate_min_height(len(self.index)),
            'theoretical_max_height': self._calculate_max_height(len(self.index))
        }
    
    def _calculate_min_height(self, n: int) -> int:
        """Calculate theoretical minimum height for n nodes."""
        if n <= 1:
            return 0
        import math
        return int(math.log2(n))
    
    def _calculate_max_height(self, n: int) -> int:
        """Calculate theoretical maximum height for AVL tree with n nodes."""
        if n <= 1:
            return 0
        # AVL trees have height at most 1.44 * log2(n)
        import math
        return int(1.44 * math.log2(n) + 2)


def demonstrate_applications():
    """Demonstrate real-world applications of AVL trees."""
    print("\n=== REAL-WORLD APPLICATIONS ===")
    
    print("1. Auto-Balancing Database Index:")
    index = AutoBalancingIndex()
    
    # Insert employee records
    employees = [
        (101, {"name": "Alice", "dept": "Engineering", "salary": 75000}),
        (205, {"name": "Bob", "dept": "Marketing", "salary": 65000}),
        (150, {"name": "Charlie", "dept": "Engineering", "salary": 80000}),
        (300, {"name": "Diana", "dept": "Finance", "salary": 70000}),
        (175, {"name": "Eve", "dept": "Engineering", "salary": 78000}),
        (225, {"name": "Frank", "dept": "Marketing", "salary": 68000}),
        (125, {"name": "Grace", "dept": "HR", "salary": 60000})
    ]
    
    for emp_id, record in employees:
        index.insert_record(emp_id, record)
        print(f"  Inserted employee {emp_id}: {record['name']}")
    
    stats = index.get_stats()
    print(f"\n  Index Statistics:")
    print(f"    Size: {stats['size']} records")
    print(f"    Height: {stats['height']}")
    print(f"    Is balanced: {stats['is_balanced']}")
    print(f"    Theoretical bounds: [{stats['theoretical_min_height']}, {stats['theoretical_max_height']}]")
    
    # Demonstrate fast lookups
    print(f"\n  Fast lookups:")
    test_ids = [150, 225, 999]
    for emp_id in test_ids:
        record = index.find_record(emp_id)
        if record:
            print(f"    Employee {emp_id}: {record['name']} ({record['dept']})")
        else:
            print(f"    Employee {emp_id}: Not found")


# ============================================================================
# SECTION 5: TESTING AND VALIDATION
# ============================================================================

def test_avl_operations():
    """Comprehensive testing of AVL tree operations."""
    print("\n=== TESTING AVL TREE OPERATIONS ===")
    
    # Basic operations test
    print("Testing basic operations:")
    avl = AVLTree()
    
    # Test empty tree
    assert avl.is_empty(), "New AVL tree should be empty"
    assert len(avl) == 0, "Empty AVL tree should have size 0"
    assert avl.height() == 0, "Empty AVL tree should have height 0"
    
    # Test insertions with automatic balancing
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for val in values:
        avl.insert(val)
        assert avl.is_valid_avl(), f"AVL property violated after inserting {val}"
    
    assert len(avl) == len(values), f"Size should be {len(values)}"
    assert not avl.is_empty(), "AVL tree with elements should not be empty"
    
    # Test search operations
    for val in values:
        assert avl.search(val), f"Should find {val}"
        assert val in avl, f"Should find {val} using 'in' operator"
    
    assert not avl.search(100), "Should not find 100"
    assert 100 not in avl, "Should not find 100 using 'in' operator"
    
    # Test traversal gives sorted order
    inorder = avl.inorder_traversal()
    assert inorder == sorted(values), "Inorder should give sorted order"
    
    # Test deletion with rebalancing
    delete_values = [30, 70, 50]  # Test different deletion cases
    for val in delete_values:
        avl.delete(val)
        assert avl.is_valid_avl(), f"AVL property violated after deleting {val}"
        assert not avl.search(val), f"Should not find deleted value {val}"
    
    print("  Basic operations: All tests passed!")
    
    # Stress test with many insertions
    print("Stress testing with random insertions:")
    avl_stress = AVLTree()
    stress_values = random.sample(range(1, 1001), 200)
    
    for val in stress_values:
        avl_stress.insert(val)
        assert avl_stress.is_valid_avl(), f"AVL property violated during stress test at {val}"
    
    # Verify height is logarithmic
    expected_max_height = int(1.44 * (len(stress_values).bit_length()) + 2)
    actual_height = avl_stress.height()
    assert actual_height <= expected_max_height, f"Height {actual_height} exceeds maximum {expected_max_height}"
    
    print(f"  Stress test: Inserted {len(stress_values)} values")
    print(f"  Tree height: {actual_height} (max allowed: {expected_max_height})")
    print("  Stress test: All tests passed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("AVL Tree Implementation - Self-Balancing BST Demonstration")
    print("=" * 70)
    
    try:
        # Basic AVL operations
        avl = AVLTree()
        print("=== BASIC AVL TREE DEMONSTRATION ===")
        
        values = [50, 30, 70, 20, 40, 60, 80]
        print(f"Inserting values: {values}")
        
        for val in values:
            avl.insert(val)
        
        print(f"\nFinal tree structure:")
        print_tree(avl.root)
        
        print(f"\nAVL Tree properties:")
        print(f"Size: {len(avl)}")
        print(f"Height: {avl.height()}")
        print(f"Is valid AVL: {avl.is_valid_avl()}")
        print(f"Inorder traversal: {avl.inorder_traversal()}")
        
        # Balance factor information
        balance_info = avl.get_balance_info()
        print(f"\nBalance factors (value, height, balance_factor):")
        for info in sorted(balance_info):
            print(f"  Node {info[0]}: height={info[1]}, balance_factor={info[2]}")
        
        # Run all demonstrations
        demonstrate_rotations()
        benchmark_avl_vs_bst()
        demonstrate_applications()
        test_avl_operations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 70}")
        print("AVL Tree demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement iterative versions of AVL insertion and deletion.

2. Add support for duplicate values in AVL tree.

3. Implement AVL tree with parent pointers for easier navigation.

4. Create an AVL tree that stores key-value pairs.

5. Implement range query operations for AVL tree.

6. Add tree serialization and deserialization for AVL trees.

7. Implement rank and select operations (find kth element).

8. Create persistent AVL tree (immutable with structural sharing).

9. Implement concurrent AVL tree with thread-safety.

10. Build AVL tree with lazy deletion for better performance.

ADVANCED CHALLENGES:

1. Implement other self-balancing trees (Red-Black, Splay)
2. Compare AVL vs Red-Black tree performance
3. Implement B-tree for external storage
4. Create weight-balanced binary trees
5. Implement scapegoat tree
6. Build randomized search tree (Treap)
7. Implement interval tree using AVL as base
8. Create order statistic tree with AVL balancing
9. Build augmented AVL tree for range queries
10. Implement fractional cascading with AVL trees

THEORETICAL ANALYSIS:

1. Prove AVL tree height is O(log n)
2. Analyze rotation frequency in dynamic sequences
3. Study space overhead of height storage
4. Compare different balancing strategies
5. Analyze cache performance of tree operations

SYSTEM DESIGN APPLICATIONS:

1. Database B-tree index with AVL principles
2. Memory allocator with balanced free lists
3. Expression evaluation with balanced parse trees
4. File system directory structure
5. Network routing table implementation
"""
