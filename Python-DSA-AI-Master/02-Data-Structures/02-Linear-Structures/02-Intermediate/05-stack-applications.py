"""
## A. Concept Name
Stack Applications (Expression Evaluation & Monotonic Stacks)

## B. One-Sentence Definition
Stack applications leverage the Last-In-First-Out (LIFO) property to solve problems involving nested structures, order reversal, or maintaining monotonic relationships.

## C. Why Does This Exist?
Stacks are essential for tracking state in processes where the most recently encountered item must be processed first. They provide an efficient mechanism (O(1) insertion and removal) to handle recursive patterns, syntax parsing, and historical state tracking without the overhead of actual recursion or complex array manipulations.

## D. Intuition
Think of reading a mathematical formula or waiting for a warmer day. When you encounter a closing parenthesis, you need to match it with the most recent open one. When waiting for a warmer day, any previous colder days are instantly resolved the moment a hot day arrives. The LIFO nature perfectly models these "resolve the most recent unresolved item first" scenarios.

## E. Real-Life Analogy
- Web Browser History: Clicking 'Back' takes you to the most recently visited page.
- Text Editor Undo: Pressing Ctrl+Z undoes the very last action you performed.
- Cafeteria Trays: Trays are added to the top and taken from the top. The first tray put down is the last one picked up.

## F. Mental Model
Visualize a vertical tube closed at the bottom. You can only drop items in from the top (push) and take items out from the top (pop). When parsing an expression or sequence, you push unresolved items into the tube. When a resolving condition occurs (like an operator or a warmer day), you pop items out of the tube until the condition is met.

## G. Visual Explanation
For Daily Temperatures `[73, 74, 75, 71, 69, 72, 76, 73]`:
Day 0 (73): Stack `[73]` (waiting for warmer)
Day 1 (74): 74 > 73! Pop 73. Day 0 waits 1 day. Stack `[74]`
Day 2 (75): 75 > 74! Pop 74. Day 1 waits 1 day. Stack `[75]`
Day 3 (71): 71 < 75. Stack `[75, 71]`
Day 4 (69): 69 < 71. Stack `[75, 71, 69]`
Day 5 (72): 72 > 69! Pop 69 (waited 1 day). 72 > 71! Pop 71 (waited 2 days). Stack `[75, 72]`
...and so on. The stack always remains sorted (monotonic decreasing).

## H. Formal Explanation
In computer science, a stack is an abstract data type that serves as a collection of elements with two principal operations: push (adds an element to the collection) and pop (removes the most recently added element). Stack applications apply this property to algorithms like Depth-First Search (DFS), expression parsing (Shunting Yard algorithm), and monotonic stacks (finding next greater/smaller elements).

## I. Mathematical Foundation
The operations of a stack map to the formal language theory of Pushdown Automata (PDA). A PDA is essentially a finite automaton equipped with a stack, making it capable of recognizing Context-Free Languages (CFLs), such as correctly matched parentheses or valid mathematical expressions.
- Space Complexity: $O(N)$ for storing elements.
- Time Complexity: Amortized $O(1)$ per element for monotonic stacks, resulting in $O(N)$ total time.

## J. From-Scratch Implementation
(See the `ExpressionEvaluator`, `ExpressionConverter`, and `interview_challenge_daily_temperatures` below for implementations)

## K. Library / Production Implementation
Python lists `[]` are typically used as stacks in practice (`append()` for push, `pop()` for pop). For thread-safe applications, `queue.LifoQueue` is used. The `collections.deque` can also serve as a fast stack.

## L. Trace (walk through example)
Evaluating Postfix: `["4", "13", "5", "/", "+"]`
1. Read "4": Push 4. Stack: `[4]`
2. Read "13": Push 13. Stack: `[4, 13]`
3. Read "5": Push 5. Stack: `[4, 13, 5]`
4. Read "/": Pop 5, Pop 13. Evaluate 13 / 5 = 2. Push 2. Stack: `[4, 2]`
5. Read "+": Pop 2, Pop 4. Evaluate 4 + 2 = 6. Push 6. Stack: `[6]`
Result: 6.

## M. Complexity
- Time Complexity: $O(N)$ where $N$ is the number of tokens or elements. Each element is pushed and popped at most once.
- Space Complexity: $O(N)$ in the worst case where all elements must be stored on the stack (e.g., strictly decreasing temperatures, or all numbers before operators).

## N. Common Mistakes
- **Popping from an empty stack:** Always check if the stack is non-empty before popping (`while stack:`).
- **Incorrect Order of Operands:** When evaluating `a - b` or `a / b` in postfix, the first popped value is `b` (right operand) and the second popped value is `a` (left operand).
- **Division Truncation:** In Python, `-3 // 2` is `-2`, but `int(-3 / 2)` is `-1`. Postfix evaluation usually requires truncation toward zero.

## O. Common Confusions
- **Monotonic Stacks:** "Why is it called monotonic?" Because the elements in the stack are strictly increasing or decreasing. When a new element violates the monotonicity, elements are popped until it is restored.
- **Infix vs Postfix vs Prefix:** Infix (`A + B`) is human-readable but requires parentheses. Postfix (`A B +`) and Prefix (`+ A B`) are unambiguous and require no parentheses, making them easy for computers to evaluate using stacks.

## P. When To Use
- Parsing syntax (brackets, math expressions, XML/HTML tags).
- Finding the "Next Greater" or "Next Smaller" element in an array (Monotonic Stack).
- Keeping track of state that needs to be reversed or undone (undo features, DFS).

## Q. When NOT To Use
- When you need First-In-First-Out (FIFO) processing. Use a Queue instead.
- When you need random access to elements by index. Use a List/Array.
- When finding minimums/maximums dynamically across arbitrary sliding windows. Use a Deque or Heap.

## R. Trade-offs
- **Stack via List vs Deque:** Python lists `append`/`pop` are fast amortized O(1), but occasionally trigger a large memory reallocation. `collections.deque` has consistent O(1) appends and pops but slightly more overhead per element.

## S. Debugging
- Print the stack at each iteration to visualize how it grows and shrinks.
- Ensure loop conditions for monotonic stacks correctly use strictly greater `>` or greater-equal `>=` depending on whether duplicates should be popped.

## T. Memory Hook
"Stacks are like Pringles: you can only eat the one on top, and you can only put one back on top. Resolve the newest problems first!"

## U. Active Recall
1. Why does evaluating a postfix expression not require parentheses?
2. In a monotonic decreasing stack, when do you push and when do you pop?
3. What happens if you try to pop from an empty stack in Python?

## V. Practice
1. Valid Parentheses (LeetCode #20)
2. Min Stack (LeetCode #155)
3. Largest Rectangle in Histogram (LeetCode #84)

## W. Interview Question
"Design a stack that supports push, pop, top, and retrieving the minimum element in constant time." (Min Stack)

## X. Project Connection
In a real-world compiler or interpreter project (like building a custom domain-specific language), you use a stack to implement a Shunting-Yard algorithm to parse the user's text into an Abstract Syntax Tree (AST), and then perhaps another stack to evaluate that tree.
"""

from typing import List

class ExpressionEvaluator:
    """Basic/Intermediate Application: Evaluate Reverse Polish Notation (Postfix)."""
    @staticmethod
    def eval_postfix(tokens: List[str]) -> int:
        stack = []
        for token in tokens:
            if token not in "+-*/":
                stack.append(int(token))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(int(a / b))  # truncate toward zero
        return stack[0]

class ExpressionConverter:
    """Advanced Application: Convert Infix to Postfix."""
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    @staticmethod
    def infix_to_postfix(expression: str) -> str:
        stack = []
        output = []
        for char in expression:
            if char.isalnum():
                output.append(char)
            elif char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != '(' and ExpressionConverter.PRECEDENCE.get(char, 0) <= ExpressionConverter.PRECEDENCE.get(stack[-1], 0):
                    output.append(stack.pop())
                stack.append(char)
        while stack:
            output.append(stack.pop())
        return "".join(output)

def interview_challenge_daily_temperatures(temperatures: List[int]) -> List[int]:
    """
    Interview Challenge: Daily Temperatures.
    Given an array of integers temperatures represents the daily temperatures, return an array answer such that
    answer[i] is the number of days you have to wait after the ith day to get a warmer temperature.
    """
    res = [0] * len(temperatures)
    stack = []  # stores pair: [temp, index]
    for i, t in enumerate(temperatures):
        while stack and t > stack[-1][0]:
            stackT, stackInd = stack.pop()
            res[stackInd] = i - stackInd
        stack.append([t, i])
    return res

def run_tests() -> None:
    print("Testing ExpressionEvaluator...")
    assert ExpressionEvaluator.eval_postfix(["2", "1", "+", "3", "*"]) == 9
    assert ExpressionEvaluator.eval_postfix(["4", "13", "5", "/", "+"]) == 6

    print("Testing ExpressionConverter...")
    assert ExpressionConverter.infix_to_postfix("a+b*c") == "abc*+"
    assert ExpressionConverter.infix_to_postfix("(a+b)*c") == "ab+c*"

    print("Testing Interview Challenge...")
    assert interview_challenge_daily_temperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
