"""
## A. Concept Name
Python Functions (Basics to Advanced)

## B. One-Sentence Definition
A function is a named, reusable block of code that encapsulates a specific task, accepts inputs, and optionally returns an output.

## C. Why Does This Exist?
To prevent code duplication (DRY principle), manage complexity by breaking down large problems into smaller chunks, and establish clear boundaries/interfaces for testing and modularity.

## D. Intuition
Imagine you have to write instructions to bake a cake 100 times. Instead of repeating the instructions 100 times, you write "BakeCake()" once, and just say "BakeCake()" whenever you need it. Functions give a name to a reusable process.

## E. Real-Life Analogy
A function is like a coffee machine. 
- Inputs (Arguments): Water and coffee beans.
- Process (Body): Heating, grinding, brewing.
- Output (Return value): A cup of coffee.
You don't need to know *how* the machine works internally to use it; you just need to know what to put in and what you get out.

## F. Mental Model
Think of a function as a mini-program within your program. It has its own isolated workspace (local scope). When you call a function, execution jumps to that mini-program, executes its code, and then jumps back with the result, destroying the local workspace.

## G. Visual Explanation
           +-------------------------+
Inputs --> | def function_name(args) | --> Local Scope (Private memory)
           |    # Do some work       | 
           |    return result        |
           +-------------------------+ --> Output returned to caller

## H. Formal Explanation
In Python, functions are first-class objects (instances of the `function` class). They can be assigned to variables, passed as arguments, and returned from other functions. The `def` keyword creates a function object and binds it to a name in the current namespace. Python uses "pass-by-object-reference" for arguments, meaning the function receives references to the exact objects passed by the caller.

## I. Mathematical Foundation (if applicable)
A function in programming closely mirrors a mathematical function f: X -> Y, mapping elements from an input domain X to an output codomain Y. Pure functions always map the same input to the same output without side effects, a foundational concept in functional programming.

## J. From-Scratch Implementation (if applicable)
(See code below for `configure_ml_pipeline`, `timer_decorator`, and `safe_append`)

## K. Library / Production Implementation (if applicable)
In production, standard library tools like `functools` enhance functions (e.g., `@lru_cache` for memoization, `partial` for freezing arguments). Frameworks like FastAPI or Flask use functions heavily to define API endpoints via decorators.

## L. Trace (walk through example)
Calling: `configure_ml_pipeline("ResNet", 50, 0.01, 0.9, author="Alice", version="1.2")`
1. `model_name` binds to "ResNet".
2. `epochs` binds to 50 (overriding the default 10).
3. `hyperparameters` collects the remaining positional args into a tuple: (0.01, 0.9).
4. `metadata` collects the remaining keyword args into a dict: {"author": "Alice", "version": "1.2"}.
5. Function body executes, constructing the `config` dictionary.
6. The `config` dictionary is returned to the caller.

## M. Complexity
- Time Complexity: Function call overhead in Python is generally O(1). The true complexity depends purely on the body's operations. 
- Space Complexity: Every function call creates a new stack frame. Deep recursion can lead to O(N) space and a `RecursionError`.
- Memory: Variables in the local scope are garbage collected after the function returns unless a reference is kept (e.g., in a closure).

## N. Common Mistakes
- **Mutable Default Arguments**: `def append(item, lst=[])`. The list `[]` is created ONCE when the function is defined. Subsequent calls share the exact same list.
- **Shadowing Built-ins**: Naming a variable `list` or `dict` inside a function overrides the built-in function in that scope.
- **Modifying Globals**: Trying to reassign a global variable without the `global` keyword creates a new local variable instead.

## O. Common Confusions
- ***args vs **kwargs**: `*args` unpacks/packs positional arguments into a tuple. `**kwargs` unpacks/packs keyword arguments into a dictionary.
- **Arguments vs Parameters**: Parameters are the names in the function definition (e.g., `model_name`). Arguments are the actual values passed in (e.g., `"ResNet"`).
- **Return vs Print**: `print()` outputs text to the console but evaluates to `None`. `return` sends a value back to the caller for further program use.

## P. When To Use
- When logic is repeated more than twice (Rule of Three).
- To make code self-documenting (e.g., `calculate_tfidf()` is clearer than raw math inline).
- To isolate tests (unit testing thrives on small, pure functions).

## Q. When NOT To Use
- When defining a function adds unnecessary abstraction to a trivial one-liner (though lambdas can sometimes be used here).
- If the function relies heavily on state and modifies multiple external variables across many invocations—consider a Class instead.

## R. Trade-offs
- **Pros**: Reusability, readability, easier testing, better modularity.
- **Cons**: Small function call overhead; splitting code into too many tiny functions can make execution flow hard to follow ("spaghetti code").

## S. Debugging
- `TypeError: func() missing 1 required positional argument`: You forgot to pass a required argument. Check the signature.
- `TypeError: func() got an unexpected keyword argument`: You misspelled a keyword argument or passed one that doesn't exist.
- `UnboundLocalError`: You tried to use and modify a global variable inside a function without declaring `global var_name`.

## T. Memory Hook (a short memorable principle)
"LEGB Rule for Scope": 
Python searches for variables in this order: Local -> Enclosing -> Global -> Built-in.

## U. Active Recall (questions before answers)
1. Why is `def func(lst=[])` dangerous? What is the fix?
2. What type of object does `*args` evaluate to inside a function?
3. How do you return multiple values from a function in Python?

## V. Practice (exercises)
Exercise: Write a function `safe_append` that takes an item and a list, and appends the item. It must NOT suffer from the mutable default argument trap. (Solution below)

## W. Interview Question
Q: Explain "pass-by-object-reference" in Python. If I pass a list to a function and append to it, does the original list change? What if I reassign the list to a new list inside the function?
A: Python passes references to objects. 
- If you modify a mutable object (like appending to a list), the original object IS modified because both the caller and the function point to the same memory address.
- If you REASSIGN the parameter (e.g., `lst = [1, 2, 3]`), you merely point the local variable to a new object. The original list outside the function remains completely unchanged.

## X. Project Connection
In frameworks like PyTorch or TensorFlow, functions heavily utilize *args and **kwargs to allow flexible network definitions. Decorators are used extensively, for instance `@torch.no_grad()` disables gradient computation, modifying the function's execution context dynamically without changing the core function logic.
"""

import time
from typing import Callable, List, Dict, Any, Tuple, Optional

def configure_ml_pipeline(
    model_name: str,                         # Positional argument
    epochs: int = 10,                        # Keyword argument with default
    *hyperparameters: float,                 # *args: arbitrary positional (Tuple)
    **metadata: str                          # **kwargs: arbitrary keyword (Dict)
) -> Dict[str, Any]:
    """
    Simulates configuring a Machine Learning pipeline to demonstrate argument types.
    """
    # Local scope: variables created here (like `config`) disappear after return.
    config = {
        "model": model_name,
        "epochs": epochs,
        "hyperparameters": hyperparameters,
        "metadata": metadata
    }
    return config

def timer_decorator(func: Callable) -> Callable:
    """
    A decorator (higher-order function) to measure execution time.
    Demonstrates first-class functions and closures.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Log] {func.__name__} executed in {end - start:.5f}s")
        return result
    return wrapper

@timer_decorator
def train_model(epochs: int) -> str:
    """Simulates training a model to demonstrate decorator usage."""
    total = 0
    for i in range(epochs * 10000):
        total += i  # Dummy work
    return f"Model trained for {epochs} epochs."


def safe_append(item: Any, target_list: Optional[List[Any]] = None) -> List[Any]:
    """
    Fix for the mutable default argument trap.
    """
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list


def demonstrate_interview_concept() -> None:
    """Demonstrates pass-by-object-reference behavior during interviews."""
    print("--- Interview Concept Demonstration ---")
    original_list = [1, 2]
    
    def modify_list(lst: List[int]) -> None:
        lst.append(3)      # Modifies the shared object
        lst = [9, 9, 9]    # Reassigns the local name 'lst', does NOT affect original
        lst.append(10)
    
    modify_list(original_list)
    print(f"Original list after function call: {original_list}") 
    assert original_list == [1, 2, 3] # Only the append(3) affected the caller

def main() -> None:
    print("--- 1. Testing ML Pipeline Config ---")
    config = configure_ml_pipeline("Transformer", 100, 0.001, 0.999, author="AI-Team", version="2.0")
    print(config)
    
    print("\n--- 2. Testing Decorator ---")
    result = train_model(500)
    print(result)
    
    print("\n--- 3. Testing Safe Append ---")
    list1 = safe_append("A")
    list2 = safe_append("B")
    print(f"List 1: {list1} | List 2: {list2}")
    assert list1 == ["A"] and list2 == ["B"]
    
    print("\n")
    demonstrate_interview_concept()

if __name__ == "__main__":
    main()
