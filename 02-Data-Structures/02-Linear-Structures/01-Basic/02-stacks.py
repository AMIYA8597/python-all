#!/usr/bin/env python3
"""
Stacks Implementation - Comprehensive Guide
==========================================

This module demonstrates stack implementations in Python with detailed analysis
of different approaches, performance comparisons, and real-world applications.

Topics Covered:
- Stack ADT and LIFO principle
- Multiple implementation approaches (list, deque, linked list)
- Performance analysis and optimization
- Stack applications (expression evaluation, undo/redo, etc.)
- Memory management considerations
- Thread-safe stack implementations

Author: Python DSA Master Course
Version: 1.0
"""

import sys
import time
import timeit
import threading
from typing import List, Any, Optional, Generic, TypeVar
from collections import deque
from dataclasses import dataclass

T = TypeVar('T')


# ============================================================================
# SECTION 1: STACK ADT AND BASIC IMPLEMENTATION
# ============================================================================

class Stack(Generic[T]):
    """
    Stack Abstract Data Type implementation using Python list.
    
    Stack follows LIFO (Last In, First Out) principle:
    - push(): Add element to top
    - pop(): Remove and return top element  
    - peek()/top(): View top element without removing
    - is_empty(): Check if stack is empty
    - size(): Get number of elements
    """
    
    def __init__(self):
        """Initialize empty stack."""
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """
        Add item to top of stack.
        
        Time Complexity: O(1) amortized
        Space Complexity: O(1)
        """
        self._items.append(item)
    
    def pop(self) -> T:
        """
        Remove and return top item from stack.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()
    
    def peek(self) -> T:
        """
        Return top item without removing it.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Raises:
            IndexError: If stack is empty
        """
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """
        Check if stack is empty.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self._items) == 0
    
    def size(self) -> int:
        """
        Get number of items in stack.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return len(self._items)
    
    def clear(self) -> None:
        """
        Remove all items from stack.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self._items.clear()
    
    def __len__(self) -> int:
        """Support len() function."""
        return self.size()
    
    def __bool__(self) -> bool:
        """Support bool() function."""
        return not self.is_empty()
    
    def __str__(self) -> str:
        """String representation (bottom to top)."""
        return f"Stack({self._items})"
    
    def __repr__(self) -> str:
        """Detailed representation."""
        return f"Stack(size={self.size()}, items={self._items})"


def demonstrate_basic_stack():
    """Demonstrate basic stack operations."""
    print("=== BASIC STACK DEMONSTRATION ===")
    
    stack = Stack[int]()
    
    # Test basic operations
    print(f"Empty stack: {stack}")
    print(f"Is empty: {stack.is_empty()}")
    
    # Push operations
    for i in range(1, 6):
        stack.push(i)
        print(f"After push({i}): {stack}")
    
    # Peek operation
    print(f"Top element (peek): {stack.peek()}")
    print(f"Stack after peek: {stack}")
    
    # Pop operations
    while not stack.is_empty():
        top = stack.pop()
        print(f"Popped: {top}, remaining: {stack}")
    
    # Error handling
    try:
        stack.pop()
    except IndexError as e:
        print(f"Error: {e}")
    
    try:
        stack.peek()
    except IndexError as e:
        print(f"Error: {e}")


# ============================================================================
# SECTION 2: ALTERNATIVE STACK IMPLEMENTATIONS
# ============================================================================

class DequeStack(Generic[T]):
    """
    Stack implementation using collections.deque.
    
    Deque provides O(1) operations at both ends and is thread-safe
    for append and pop operations from opposite ends.
    """
    
    def __init__(self):
        """Initialize empty stack using deque."""
        self._items: deque = deque()
    
    def push(self, item: T) -> None:
        """Add item to top of stack."""
        self._items.append(item)
    
    def pop(self) -> T:
        """Remove and return top item."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()
    
    def peek(self) -> T:
        """Return top item without removing."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Get number of items."""
        return len(self._items)
    
    def __str__(self) -> str:
        return f"DequeStack({list(self._items)})"


class LinkedStack(Generic[T]):
    """
    Stack implementation using linked list.
    
    Provides true O(1) operations without amortization concerns
    and doesn't require pre-allocation of memory.
    """
    
    @dataclass
    class _Node:
        data: T
        next: Optional['LinkedStack._Node'] = None
    
    def __init__(self):
        """Initialize empty stack."""
        self._head: Optional[self._Node] = None
        self._size: int = 0
    
    def push(self, item: T) -> None:
        """Add item to top of stack."""
        new_node = self._Node(item, self._head)
        self._head = new_node
        self._size += 1
    
    def pop(self) -> T:
        """Remove and return top item."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        
        data = self._head.data
        self._head = self._head.next
        self._size -= 1
        return data
    
    def peek(self) -> T:
        """Return top item without removing."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._head.data
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return self._head is None
    
    def size(self) -> int:
        """Get number of items."""
        return self._size
    
    def __str__(self) -> str:
        """String representation."""
        items = []
        current = self._head
        while current:
            items.append(current.data)
            current = current.next
        return f"LinkedStack({items})"


class ThreadSafeStack(Generic[T]):
    """
    Thread-safe stack implementation using locks.
    
    Safe for concurrent access from multiple threads.
    """
    
    def __init__(self):
        """Initialize thread-safe stack."""
        self._items: List[T] = []
        self._lock = threading.Lock()
    
    def push(self, item: T) -> None:
        """Thread-safe push operation."""
        with self._lock:
            self._items.append(item)
    
    def pop(self) -> T:
        """Thread-safe pop operation."""
        with self._lock:
            if not self._items:
                raise IndexError("pop from empty stack")
            return self._items.pop()
    
    def peek(self) -> T:
        """Thread-safe peek operation."""
        with self._lock:
            if not self._items:
                raise IndexError("peek from empty stack")
            return self._items[-1]
    
    def is_empty(self) -> bool:
        """Thread-safe empty check."""
        with self._lock:
            return len(self._items) == 0
    
    def size(self) -> int:
        """Thread-safe size check."""
        with self._lock:
            return len(self._items)


def compare_stack_implementations():
    """Compare different stack implementation approaches."""
    print(f"\n=== STACK IMPLEMENTATION COMPARISON ===")
    
    # Create instances
    list_stack = Stack[int]()
    deque_stack = DequeStack[int]()
    linked_stack = LinkedStack[int]()
    
    implementations = [
        ("List Stack", list_stack),
        ("Deque Stack", deque_stack), 
        ("Linked Stack", linked_stack)
    ]
    
    # Test basic operations
    print("Testing basic operations:")
    for name, stack in implementations:
        # Push operations
        for i in range(5):
            stack.push(i)
        
        print(f"{name}: {stack}")
        
        # Pop operations  
        while not stack.is_empty():
            stack.pop()


# ============================================================================
# SECTION 3: PERFORMANCE BENCHMARKING
# ============================================================================

def benchmark_stack_operations():
    """Benchmark different stack implementations."""
    print(f"\n=== PERFORMANCE BENCHMARKING ===")
    
    def benchmark_push_pop(stack_class, n_operations=100000):
        """Benchmark push and pop operations."""
        stack = stack_class()
        
        # Benchmark push operations
        start = time.perf_counter()
        for i in range(n_operations):
            stack.push(i)
        push_time = time.perf_counter() - start
        
        # Benchmark pop operations
        start = time.perf_counter()
        while not stack.is_empty():
            stack.pop()
        pop_time = time.perf_counter() - start
        
        return push_time, pop_time
    
    implementations = [
        ("List Stack", Stack),
        ("Deque Stack", DequeStack),
        ("Linked Stack", LinkedStack)
    ]
    
    n_ops = 50000
    print(f"Benchmarking {n_ops} operations:")
    
    for name, stack_class in implementations:
        push_time, pop_time = benchmark_push_pop(stack_class, n_ops)
        total_time = push_time + pop_time
        
        print(f"{name}:")
        print(f"  Push time: {push_time:.6f}s")
        print(f"  Pop time: {pop_time:.6f}s")  
        print(f"  Total time: {total_time:.6f}s")
        print(f"  Ops/sec: {(2 * n_ops) / total_time:.0f}")


# ============================================================================
# SECTION 4: STACK APPLICATIONS
# ============================================================================

def balanced_parentheses(expression: str) -> bool:
    """
    Check if parentheses are balanced using stack.
    
    Example of classic stack application.
    """
    stack = Stack[str]()
    opening = {'(', '[', '{'}
    closing = {')', ']', '}'}
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty():
                return False
            if pairs[stack.pop()] != char:
                return False
    
    return stack.is_empty()


def evaluate_postfix(expression: str) -> float:
    """
    Evaluate postfix expression using stack.
    
    Args:
        expression: Space-separated postfix expression
        
    Returns:
        Result of evaluation
    """
    stack = Stack[float]()
    operators = {'+', '-', '*', '/'}
    
    tokens = expression.split()
    
    for token in tokens:
        if token in operators:
            if stack.size() < 2:
                raise ValueError("Invalid postfix expression")
            
            b = stack.pop()
            a = stack.pop()
            
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                result = a / b
            
            stack.push(result)
        else:
            try:
                number = float(token)
                stack.push(number)
            except ValueError:
                raise ValueError(f"Invalid token: {token}")
    
    if stack.size() != 1:
        raise ValueError("Invalid postfix expression")
    
    return stack.pop()


def infix_to_postfix(expression: str) -> str:
    """
    Convert infix expression to postfix using stack.
    
    Args:
        expression: Infix expression string
        
    Returns:
        Postfix expression string
    """
    stack = Stack[str]()
    result = []
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}
    
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()
    
    for token in tokens:
        if token.replace('.', '').replace('-', '').isdigit():
            # Operand
            result.append(token)
        elif token == '(':
            stack.push(token)
        elif token == ')':
            while not stack.is_empty() and stack.peek() != '(':
                result.append(stack.pop())
            if not stack.is_empty():
                stack.pop()  # Remove '('
        elif token in precedence:
            while (not stack.is_empty() and 
                   stack.peek() != '(' and
                   stack.peek() in precedence and
                   (precedence[stack.peek()] > precedence[token] or
                    (precedence[stack.peek()] == precedence[token] and 
                     token not in right_associative))):
                result.append(stack.pop())
            stack.push(token)
    
    while not stack.is_empty():
        result.append(stack.pop())
    
    return ' '.join(result)


class UndoRedoSystem:
    """
    Undo/Redo system implementation using two stacks.
    
    Demonstrates practical stack application in text editors,
    image editors, and other applications.
    """
    
    def __init__(self):
        self.undo_stack = Stack[str]()
        self.redo_stack = Stack[str]()
        self.current_state = ""
    
    def execute_command(self, new_state: str) -> None:
        """Execute a command and save state for undo."""
        self.undo_stack.push(self.current_state)
        self.current_state = new_state
        self.redo_stack.clear()  # Clear redo stack on new command
    
    def undo(self) -> bool:
        """Undo last command."""
        if self.undo_stack.is_empty():
            return False
        
        self.redo_stack.push(self.current_state)
        self.current_state = self.undo_stack.pop()
        return True
    
    def redo(self) -> bool:
        """Redo last undone command."""
        if self.redo_stack.is_empty():
            return False
        
        self.undo_stack.push(self.current_state)
        self.current_state = self.redo_stack.pop()
        return True
    
    def get_state(self) -> str:
        """Get current state."""
        return self.current_state
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return not self.undo_stack.is_empty()
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return not self.redo_stack.is_empty()


def demonstrate_stack_applications():
    """Demonstrate various stack applications."""
    print(f"\n=== STACK APPLICATIONS DEMONSTRATION ===")
    
    # 1. Balanced Parentheses
    print("1. Balanced Parentheses Check:")
    test_expressions = [
        "((()))",
        "([{}])",
        "((())",
        "([)]",
        "{[()]}"
    ]
    
    for expr in test_expressions:
        result = balanced_parentheses(expr)
        print(f"  '{expr}': {'Balanced' if result else 'Not balanced'}")
    
    # 2. Postfix Evaluation
    print(f"\n2. Postfix Expression Evaluation:")
    postfix_expressions = [
        "3 4 +",
        "3 4 + 2 *",
        "3 4 + 2 * 5 -",
        "15 7 1 1 + - / 3 * 2 1 1 + + -"
    ]
    
    for expr in postfix_expressions:
        try:
            result = evaluate_postfix(expr)
            print(f"  '{expr}' = {result}")
        except ValueError as e:
            print(f"  '{expr}' = Error: {e}")
    
    # 3. Infix to Postfix Conversion
    print(f"\n3. Infix to Postfix Conversion:")
    infix_expressions = [
        "3 + 4",
        "3 + 4 * 2",
        "(3 + 4) * 2",
        "3 + 4 * 2 - 5",
        "((15 / (7 - (1 + 1))) * 3) - (2 + (1 + 1))"
    ]
    
    for expr in infix_expressions:
        postfix = infix_to_postfix(expr)
        print(f"  '{expr}' -> '{postfix}'")
    
    # 4. Undo/Redo System
    print(f"\n4. Undo/Redo System:")
    editor = UndoRedoSystem()
    
    print(f"  Initial state: '{editor.get_state()}'")
    
    # Execute commands
    editor.execute_command("Hello")
    print(f"  After 'Hello': '{editor.get_state()}'")
    
    editor.execute_command("Hello World")
    print(f"  After 'Hello World': '{editor.get_state()}'")
    
    editor.execute_command("Hello World!")
    print(f"  After 'Hello World!': '{editor.get_state()}'")
    
    # Undo operations
    editor.undo()
    print(f"  After undo: '{editor.get_state()}'")
    
    editor.undo()
    print(f"  After undo: '{editor.get_state()}'")
    
    # Redo operations
    editor.redo()
    print(f"  After redo: '{editor.get_state()}'")
    
    # New command clears redo
    editor.execute_command("Hello Python")
    print(f"  After 'Hello Python': '{editor.get_state()}'")
    print(f"  Can redo: {editor.can_redo()}")


# ============================================================================
# SECTION 5: ADVANCED STACK CONCEPTS
# ============================================================================

class MinStack:
    """
    Stack that supports finding minimum element in O(1) time.
    
    Uses auxiliary stack to track minimum values.
    """
    
    def __init__(self):
        self.stack = Stack[int]()
        self.min_stack = Stack[int]()
    
    def push(self, value: int) -> None:
        """Push value onto stack."""
        self.stack.push(value)
        
        if self.min_stack.is_empty() or value <= self.min_stack.peek():
            self.min_stack.push(value)
    
    def pop(self) -> int:
        """Pop value from stack."""
        if self.stack.is_empty():
            raise IndexError("pop from empty stack")
        
        value = self.stack.pop()
        if value == self.min_stack.peek():
            self.min_stack.pop()
        
        return value
    
    def peek(self) -> int:
        """Get top value."""
        return self.stack.peek()
    
    def get_min(self) -> int:
        """Get minimum value in O(1) time."""
        if self.min_stack.is_empty():
            raise IndexError("get_min from empty stack")
        return self.min_stack.peek()
    
    def is_empty(self) -> bool:
        """Check if empty."""
        return self.stack.is_empty()


class StackWithMax:
    """
    Stack that efficiently tracks maximum element.
    
    Demonstrates space-time tradeoff optimization.
    """
    
    def __init__(self):
        self.stack = Stack[tuple]()  # (value, max_so_far)
    
    def push(self, value: int) -> None:
        """Push value with current max."""
        if self.stack.is_empty():
            self.stack.push((value, value))
        else:
            current_max = max(value, self.stack.peek()[1])
            self.stack.push((value, current_max))
    
    def pop(self) -> int:
        """Pop value."""
        if self.stack.is_empty():
            raise IndexError("pop from empty stack")
        return self.stack.pop()[0]
    
    def peek(self) -> int:
        """Get top value."""
        if self.stack.is_empty():
            raise IndexError("peek from empty stack")
        return self.stack.peek()[0]
    
    def get_max(self) -> int:
        """Get maximum value in O(1) time."""
        if self.stack.is_empty():
            raise IndexError("get_max from empty stack")
        return self.stack.peek()[1]
    
    def is_empty(self) -> bool:
        """Check if empty."""
        return self.stack.is_empty()


def demonstrate_advanced_stacks():
    """Demonstrate advanced stack implementations."""
    print(f"\n=== ADVANCED STACK DEMONSTRATIONS ===")
    
    # MinStack demonstration
    print("1. MinStack (O(1) minimum):")
    min_stack = MinStack()
    
    values = [3, 5, 2, 1, 4]
    for val in values:
        min_stack.push(val)
        print(f"  Push {val}: min = {min_stack.get_min()}")
    
    while not min_stack.is_empty():
        val = min_stack.pop()
        min_val = min_stack.get_min() if not min_stack.is_empty() else "empty"
        print(f"  Pop {val}: min = {min_val}")
    
    # StackWithMax demonstration
    print(f"\n2. StackWithMax (O(1) maximum):")
    max_stack = StackWithMax()
    
    values = [3, 5, 2, 8, 1]
    for val in values:
        max_stack.push(val)
        print(f"  Push {val}: max = {max_stack.get_max()}")
    
    while not max_stack.is_empty():
        val = max_stack.pop()
        max_val = max_stack.get_max() if not max_stack.is_empty() else "empty"
        print(f"  Pop {val}: max = {max_val}")


# ============================================================================
# SECTION 6: TESTING AND VALIDATION
# ============================================================================

def test_stack_implementations():
    """Comprehensive testing of stack implementations."""
    print(f"\n=== TESTING STACK IMPLEMENTATIONS ===")
    
    def test_stack_interface(stack_class, name):
        """Test stack interface compliance."""
        print(f"Testing {name}:")
        
        stack = stack_class()
        
        # Test empty stack
        assert stack.is_empty(), "New stack should be empty"
        assert stack.size() == 0, "New stack should have size 0"
        
        # Test push operations
        for i in range(5):
            stack.push(i)
            assert not stack.is_empty(), "Stack with items should not be empty"
            assert stack.peek() == i, f"Top should be {i}"
            assert stack.size() == i + 1, f"Size should be {i + 1}"
        
        # Test pop operations
        for i in range(4, -1, -1):
            assert stack.peek() == i, f"Top should be {i}"
            assert stack.pop() == i, f"Pop should return {i}"
            assert stack.size() == i, f"Size should be {i}"
        
        # Test empty stack errors
        try:
            stack.pop()
            assert False, "Should raise error on empty pop"
        except IndexError:
            pass
        
        try:
            stack.peek()
            assert False, "Should raise error on empty peek"
        except IndexError:
            pass
        
        print(f"  {name}: All tests passed!")
    
    # Test all implementations
    implementations = [
        (Stack, "List Stack"),
        (DequeStack, "Deque Stack"),
        (LinkedStack, "Linked Stack")
    ]
    
    for stack_class, name in implementations:
        test_stack_interface(stack_class, name)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Stacks Implementation - Comprehensive Demonstration")
    print("=" * 55)
    
    try:
        demonstrate_basic_stack()
        compare_stack_implementations()
        benchmark_stack_operations()
        demonstrate_stack_applications()
        demonstrate_advanced_stacks()
        test_stack_implementations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 55}")
        print("Stack implementation demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement a stack that supports getting minimum in O(1) without extra space.

2. Design a stack that can efficiently reverse its contents.

3. Create a stack-based calculator for complex expressions.

4. Implement browser history using stacks.

5. Build a stack-based maze solver.

6. Create a stack for function call simulation.

7. Implement next greater element using stack.

8. Design histogram maximum area using stack.

9. Create balanced symbol checker for code.

10. Build stack-based expression tree builder.

ALGORITHM CHALLENGES:

1. Valid parentheses with multiple types
2. Evaluate reverse Polish notation
3. Basic calculator with +, -, *, /
4. Remove duplicate letters using stack
5. Daily temperatures problem
6. Largest rectangle in histogram
7. Decode string using stack
8. Asteroid collision simulation
9. Remove K digits to make smallest
10. Score of parentheses

SYSTEM DESIGN:

1. Design undo/redo system for text editor
2. Build call stack for programming language
3. Create browser back/forward system
4. Design stack-based memory allocator
5. Implement recursive function call stack
"""
