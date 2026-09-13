"""
# ==============================================================================
# LABORATORY: ADVANCED STACK APPLICATIONS (MONOTONIC STACKS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Stacks are relatively simple (LIFO), but they are the secret weapon for solving 
# a massive class of O(N^2) problems in O(N) time. "Monotonic Stacks" are 
# notoriously difficult to wrap your head around, but they are guaranteed to show 
# up in FAANG interviews (e.g., Trapping Rain Water, Largest Rectangle in Histogram, 
# Next Greater Element). 
# Additionally, Stacks are the foundation of parsers, compilers, and UI systems 
# (Undo/Redo, Browser Forward/Back).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand and implement a Monotonic Stack for the "Next Greater Element" problem.
# - Build a Reverse Polish Notation (RPN) Calculator.
# - Design a Web Browser History using two Stacks.
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MONOTONIC STACKS: NEXT GREATER ELEMENT
# ==============================================================================
def next_greater_element(nums: List[int]) -> List[int]:
    """
    Problem: For every element in an array, find the first element to its right 
    that is strictly greater than it. If none exists, return -1.
    Example: [2, 1, 5, 3] -> [5, 5, -1, -1]
    
    Naive O(N^2): Use a nested loop to look ahead for every item.
    Optimal O(N): Use a Monotonic Decreasing Stack.
    
    A Monotonic Decreasing Stack keeps elements (or their indices) in strictly 
    decreasing order from bottom to top. When we encounter a number LARGER than 
    the top of the stack, we pop the stack. The new number is the "Next Greater Element" 
    for all the items we just popped!
    """
    n = len(nums)
    result = [-1] * n
    stack = [] # We store INDICES, not values!
    
    for i in range(n):
        # While the stack is not empty AND the current number is GREATER than 
        # the number represented by the index at the top of the stack...
        while stack and nums[i] > nums[stack[-1]]:
            # We found the next greater element for the item at 'popped_index'!
            popped_index = stack.pop()
            result[popped_index] = nums[i]
            
        # Push the current index onto the stack to wait for its next greater element
        stack.append(i)
        
    return result

def demonstrate_monotonic_stack():
    section_header("Algorithm: Next Greater Element (Monotonic Stack)")
    
    test_cases = [
        [2, 1, 2, 4, 3],
        [7, 3, 2, 6, 9, 1]
    ]
    
    for nums in test_cases:
        print(f"Input Array: {nums}")
        print(f"Result:      {next_greater_element(nums)}\n")


# ==============================================================================
# 4. PARSING: REVERSE POLISH NOTATION (POSTFIX)
# ==============================================================================
def evaluate_rpn(tokens: List[str]) -> int:
    """
    LeetCode #150: Evaluate Reverse Polish Notation
    Instead of writing `(2 + 1) * 3`, RPN writes `2 1 + 3 *`.
    This removes the need for parentheses entirely.
    
    Algorithm:
    1. If the token is a number, push it onto the stack.
    2. If the token is an operator (+, -, *, /), pop the top TWO numbers, 
       apply the operator, and push the result back onto the stack.
    3. The final result is the only number left on the stack.
    """
    stack = []
    
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            # Pop the operands (Remember: LIFO means the right operand is popped first!)
            right = stack.pop()
            left = stack.pop()
            
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            elif token == "/":
                # In Python, int(a / b) truncates toward zero, matching C++ behavior
                stack.append(int(left / right))
        else:
            # It's a number
            stack.append(int(token))
            
    return stack[0]

def demonstrate_rpn():
    section_header("Algorithm: Evaluate Reverse Polish Notation (RPN)")
    
    # Represents: ((2 + 1) * 3) = 9
    expr1 = ["2", "1", "+", "3", "*"]
    print(f"Expression: {expr1} -> Result: {evaluate_rpn(expr1)}")
    
    # Represents: (4 + (13 / 5)) = 6
    expr2 = ["4", "13", "5", "/", "+"]
    print(f"Expression: {expr2} -> Result: {evaluate_rpn(expr2)}")


# ==============================================================================
# 5. UI SYSTEMS: BROWSER HISTORY (TWO STACKS)
# ==============================================================================
class BrowserHistory:
    """
    LeetCode #1472: Design Browser History
    We maintain two stacks: a 'history' stack (Back) and a 'future' stack (Forward).
    """
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.future = []
        
    def visit(self, url: str) -> None:
        """Visits a new url. Clears forward history."""
        self.history.append(url)
        self.future.clear() # You can't go forward after visiting a new page
        print(f"Visited: {url}")
        
    def back(self, steps: int) -> str:
        """Move back up to 'steps' times."""
        while steps > 0 and len(self.history) > 1:
            # Pop from history and push to future
            url = self.history.pop()
            self.future.append(url)
            steps -= 1
        print(f"Went back to: {self.history[-1]}")
        return self.history[-1]
        
    def forward(self, steps: int) -> str:
        """Move forward up to 'steps' times."""
        while steps > 0 and self.future:
            # Pop from future and push to history
            url = self.future.pop()
            self.history.append(url)
            steps -= 1
        print(f"Went forward to: {self.history[-1]}")
        return self.history[-1]

def demonstrate_browser_history():
    section_header("Algorithm: Browser History (Two Stacks)")
    
    browser = BrowserHistory("google.com")
    browser.visit("reddit.com")
    browser.visit("github.com")
    
    browser.back(1)    # Back to reddit
    browser.back(1)    # Back to google
    browser.forward(1) # Forward to reddit
    browser.visit("stackoverflow.com") # Clears forward stack (github is lost)
    
    # Attempting to go forward will fail and just return the current page
    browser.forward(1) 


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a Monotonic Stack, and when do you use it?
   Answer: A stack where the elements are kept in strictly increasing or strictly decreasing order. It is used to solve problems where you need to find the "Next Greater/Smaller Element" in an array in O(N) time.

2. In an RPN Calculator, why must you be careful about the order of operands when popping from the stack?
   Answer: Because a stack is LIFO. When you pop two numbers to evaluate `A - B`, the FIRST number you pop is `B` (the right operand), and the SECOND number you pop is `A` (the left operand).

3. Why use Two Stacks for an Undo/Redo or Forward/Back system instead of a List with a pointer?
   Answer: While a list with an index pointer works, using two stacks conceptually guarantees that O(1) operations are preserved, and automatically handles the logic of "clearing the redo history" (by simply calling `.clear()` on the forward stack when a new action is performed).
"""

if __name__ == "__main__":
    demonstrate_monotonic_stack()
    demonstrate_rpn()
    demonstrate_browser_history()
    print("\n[SUCCESS] Laboratory: Advanced Stack Applications Completed.")
