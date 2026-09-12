"""
Module: Decorators and Generators

Learning Objectives:
1. Understand how decorators work in Python, including closures and the @ syntax.
2. Learn how to write decorators with and without arguments.
3. Understand generators, the `yield` keyword, and their memory efficiency.
4. Learn how to build generator expressions and pipelines.

Interview Questions Covered:
- How do you create a decorator that measures function execution time?
- Write a generator that yields the Fibonacci sequence.
- Explain the difference between a list comprehension and a generator expression.
"""

import time
from typing import Callable, Any, Generator, List

# ---------------------------------------------------------
# Concept 1: Decorators
# ---------------------------------------------------------
def timer_decorator(func: Callable) -> Callable:
    """A decorator that prints the execution time of the function."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to execute.")
        return result
    return wrapper

@timer_decorator
def slow_function(delay: float) -> str:
    """A function that simulates a slow operation."""
    time.sleep(delay)
    return "Done"

# ---------------------------------------------------------
# Concept 2: Generators
# ---------------------------------------------------------
def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """A generator that yields the first n numbers in the Fibonacci sequence."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def generator_pipeline_example(numbers: List[int]) -> Generator[int, None, None]:
    """Demonstrates chaining generators for memory-efficient processing."""
    # Generator expression to square numbers
    squared = (x * x for x in numbers)
    # Generator expression to filter evens
    evens = (x for x in squared if x % 2 == 0)
    return evens

# ---------------------------------------------------------
# Tests and Main Execution
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- Decorator Example ---")
    slow_function(0.2)
    
    print("\n--- Generator Example ---")
    fib_gen = fibonacci_generator(10)
    print("Fibonacci sequence (first 10):", list(fib_gen))
    
    print("\n--- Generator Pipeline Example ---")
    nums = [1, 2, 3, 4, 5, 6]
    pipeline_result = generator_pipeline_example(nums)
    print("Squared evens from 1-6:", list(pipeline_result))
