"""
=============================================================================
MASTER CLASS: DECORATORS & GENERATORS
=============================================================================
This lesson covers two of Python's most powerful intermediate features:
Decorators (for meta-programming and code reuse) and Generators (for memory
efficient lazy evaluation).

=============================================================================
CONCEPT 1: DECORATORS
=============================================================================
## A. Concept Name
Python Decorators

## B. One-Sentence Definition
Decorators are functions that take another function as input, extend its behavior, and return a new function, all without modifying the original function's source code.

## C. Why Does This Exist?
In large systems, many functions share common boilerplate logic (e.g., logging, checking authentication, measuring performance, caching). Copying and pasting this logic into every function violates the DRY (Don't Repeat Yourself) principle and makes the codebase hard to maintain.

## D. Intuition
Imagine you want to wrap a gift. The gift is your core function. The wrapping paper is the decorator. The gift itself doesn't change, but how it is presented to the outside world (or the steps taken before/after opening it) is enhanced.

## E. Real-Life Analogy
Putting a rugged phone case on your smartphone. The phone's core functionality remains exactly the same, but you've dynamically added "shock resistance" behavior to it.

## F. Mental Model
A decorator is a function pipeline: `original_function -> decorator -> wrapped_function`. When you apply a decorator and call the function, you are actually executing the `wrapped_function` which secretly calls your `original_function` in the middle.

## G. Visual Explanation
  [ Input Arguments ] 
          │
          ▼
 ┌──────────────────────┐
 │ Wrapper Function     │
 │  (1) Add pre-logic   │
 │        │             │
 │        ▼             │
 │  ┌───────────────┐   │
 │  │ Original Func │   │
 │  └───────────────┘   │
 │        │             │
 │        ▼             │
 │  (2) Add post-logic  │
 └──────────────────────┘
          │
          ▼
     [ Output Result ]

## H. Formal Explanation
Decorators leverage Python's first-class functions (functions can be passed as arguments) and closures (inner functions remembering state from their enclosing scope). By using the syntactic sugar `@decorator`, Python translates:
    @decorator
    def foo(): pass
into:
    foo = decorator(foo)

## I. Mathematical Foundation (if applicable)
Function composition. If $f(x)$ is the original function and $g(x)$ is the wrapper mapping, the decorated execution is effectively $g(f)(x)$.

## J. From-Scratch Implementation (if applicable)
(See the code section below for `timer_decorator`)

## K. Library / Production Implementation (if applicable)
Python provides `functools.wraps`, which is a decorator used inside decorators to preserve the metadata (like docstrings and name) of the original function.

## L. Trace (walk through example)
- Python reads `@timer_decorator` above `def heavy_computation`.
- Python calls `timer_decorator(heavy_computation)`.
- `timer_decorator` creates the `wrapper` function and returns it.
- The name `heavy_computation` is now permanently bound to the `wrapper` function.
- User calls `heavy_computation(1_000_000)`.
- `wrapper(1_000_000)` executes:
  -> captures `start_time`
  -> calls original `func(1_000_000)`, getting result `499999500000`
  -> captures `end_time` and prints execution time.
  -> returns `499999500000`.

## M. Complexity
- Time Complexity: O(1) extra overhead to execute the wrapper. (The total time depends entirely on the wrapped function).
- Space Complexity: O(1) memory overhead. The closure stores a single reference to the original function.

## N. Common Mistakes
- Forgetting to `return result` inside the wrapper, causing the decorated function to silently return `None`.
- Forgetting `*args, **kwargs`, meaning the decorator crashes if applied to functions with different argument counts.
- Forgetting `@wraps(func)`, breaking documentation engines (Sphinx) and debuggers.

## O. Common Confusions
Decorators vs. Class Inheritance:
- Decorators modify behavior dynamically at runtime via composition (Wrapping).
- Inheritance modifies behavior statically at compile-time via rigid class hierarchies.
- Use Decorators for cross-cutting concerns (logging, timing) rather than creating a `TimedFunction` base class.

## P. When To Use
- Telemetry: Logging, profiling, and monitoring.
- Security: Checking user authentication (`@login_required`).
- Reliability: Retrying failed network calls automatically.
- Performance: Caching/Memoizing heavy function results.

## Q. When NOT To Use
- When the decorator heavily mutates the input arguments or return type in a way that violates the caller's expectations (violates Principle of Least Astonishment).
- On extremely tight, high-frequency inner loops where function call overhead is a bottleneck.

## R. Trade-offs
- Adding decorators increases the stack trace depth, which can sometimes make debugging slightly more complex, though it results in much cleaner and reusable application code.

## S. Debugging
- What breaks: Stack traces can be confusing because the error occurs inside `wrapper`.
- How to fix: Always use `@wraps`. If building decorators that take arguments (e.g., `@retry(retries=3)`), ensure you have exactly 3 levels of nested functions.

## T. Memory Hook (a short memorable principle)
"Functions Wrapping Functions." Decorators are Russian nesting dolls for your code.

## U. Active Recall (questions before answers)
- Q: What does `@my_dec` before `def foo()` translate to in raw Python?
- Q: Why is `*args, **kwargs` universally used inside the wrapper function?
- Q: What module provides the `@wraps` decorator, and why is it important?

## V. Practice (exercises)
Write a `@memoize` decorator that caches the results of a function based on its inputs.

## W. Interview Question
Write a `@retry(max_retries)` decorator that automatically re-runs a function if it raises an exception, up to `max_retries` times.

## X. Project Connection
- PyTorch uses decorators like `@torch.no_grad()` to disable gradient tracking.
- FastAPI/Flask use decorators extensively for routing: `@app.get("/users")`.
- AI Agent frameworks use decorators to expose standard python functions as "Tools".

=============================================================================
CONCEPT 2: GENERATORS
=============================================================================
## A. Concept Name
Generators & The `yield` Keyword

## B. One-Sentence Definition
Generators are functions that can pause their execution, yield multiple values one at a time, and maintain their internal state between successive calls.

## C. Why Does This Exist?
Processing massive datasets (like a 100GB text corpus for LLM training). If you try to load all that data into memory via a normal function returning a List, your program will crash with an OutOfMemory (OOM) error. Generators compute and provide one item at a time, keeping memory usage flat.

## D. Intuition
Think of a baker making cookies. 
- A Normal Function bakes 10,000 cookies, puts them all on a massive tray, and serves them at once. It takes a huge tray (memory) and you wait forever to get the first cookie.
- A Generator bakes one cookie, hands it to you, and freezes time. When you ask for the next cookie, time unfreezes, they bake the next one, and freeze again.

## E. Real-Life Analogy
A video streaming service (Netflix). It doesn't download the entire 10GB movie to your laptop before it starts playing. It streams (yields) the video chunks to you second-by-second on demand.

## F. Mental Model
A generator is a function with "bookmarks." When Python hits the `yield` keyword, it spits out the value, places a bookmark on that exact line of code, and pauses. When `next()` is called again, it resumes perfectly from the bookmark, keeping all variable values intact.

## G. Visual Explanation
 Normal Function (Return)       Generator (Yield)
 ┌──────────────────────┐      ┌──────────────────────┐
 │ compute all values   │      │ compute one value    │
 │ store in memory      │      │ yield value & PAUSE  │
 │ return whole list    │      │ (wait for next())    │
 └──────────┬───────────┘      │ resume, loop...      │
            │                  └──────────┬───────────┘
            ▼                             ▼ (one by one)
  [1, 2, 3, 4, 5, 6]              [1] -> [2] -> [3]

## H. Formal Explanation
Any function containing the `yield` keyword is technically a "generator function". Calling it does not execute the code inside; instead, it returns a generator iterator object. Execution only begins when `next()` is called on this object (usually implicitly via a `for` loop). Execution halts at `yield` and resumes on the next iteration. When the function returns or ends, a `StopIteration` exception is automatically raised.

## I. Mathematical Foundation (if applicable)
Lazy Evaluation. Generators can represent infinite mathematical sequences (like the Fibonacci sequence or the set of prime numbers) because they compute $f(n+1)$ only when explicitly requested, avoiding infinite loops.

## J. From-Scratch Implementation (if applicable)
(See the code section below for `fibonacci_generator`)

## K. Library / Production Implementation (if applicable)
Python's `itertools` module provides many production-ready generators for efficiently looping over data (e.g., `islice`, `chain`, `cycle`).

## L. Trace (walk through example)
- Call `gen = fibonacci_generator()`. State: Object created, code NOT run.
- Call `next(gen)`: Code starts. `a=0, b=1`. Hits `yield 0`. Returns 0 and PAUSES.
- Call `next(gen)`: Resumes. `a, b = 1, 1`. Loops back. Hits `yield 1`. Returns 1 and PAUSES.
- Call `next(gen)`: Resumes. `a, b = 1, 2`. Loops back. Hits `yield 1`. Returns 1 and PAUSES.
- Call `next(gen)`: Resumes. `a, b = 2, 3`. Loops back. Hits `yield 2`. Returns 2 and PAUSES.

## M. Complexity
- Time Complexity: O(1) per yielded item. O(N) to iterate over N items.
- Space Complexity: O(1) persistent memory footprint. This is the superpower. Whether you generate 10 items or 10 billion items, it uses the exact same tiny amount of RAM.

## N. Common Mistakes
- Assuming you can reuse a generator. Generators are one-time use! Once exhausted (StopIteration is reached), you must create a new one to iterate again.
- Trying to use `len(gen)`. Generators don't know their length because they haven't computed the future items yet!
- Trying to slice them like lists `gen[0:5]`. (Use `itertools.islice` instead).

## O. Common Confusions
Generators vs. Lists:
- Lists: Eagerly evaluated. Store everything in memory. Fast random access.
- Generators: Lazily evaluated. Store almost nothing in memory. Sequential access only.

## P. When To Use
- Reading massive text files or CSVs line by line.
- Web scraping/API pagination (yielding one page of results at a time).
- Deep Learning data loading pipelines.
- Stream processing.

## Q. When NOT To Use
- When you need to read the data multiple times (unless you recreate the generator).
- When you need fast random access (e.g., jump straight to the 10,000th element).
- When you need to sort the data (Sorting requires viewing all elements at once).

## R. Trade-offs
You trade rapid random access and reusable iteration for extreme memory efficiency.

## S. Debugging
- What breaks: "My for loop does nothing the second time I run it!"
- How to fix: Generators are consumed after one pass. Re-instantiate it, or if it's small enough, convert it to a list: `cached_data = list(gen)`.

## T. Memory Hook (a short memorable principle)
"Yield and Pause. Compute only on Demand."

## U. Active Recall (questions before answers)
- Q: What exception signals that a generator is out of items?
- Q: Why is `len()` not supported on generators?
- Q: What is the difference between `yield` and `return`?

## V. Practice (exercises)
Write a generator `prime_generator()` that yields prime numbers indefinitely.

## W. Interview Question
Write a generator `chunker(iterable, chunk_size)` that takes an iterable and yields chunks (lists) of size `chunk_size`. This is heavily used in building minibatches for neural networks!

## X. Project Connection
- PyTorch `DataLoader` uses generator patterns to yield batches of images from disk.
- Hugging Face `datasets` allows you to stream terabytes of internet text for LLM training via generators without filling your hard drive.
"""

import time
import sys
from functools import wraps
from typing import Callable, Any, Generator, List, Tuple, Dict, Iterable

# =============================================================================
# DECORATORS IMPLEMENTATION
# =============================================================================

def timer_decorator(func: Callable) -> Callable:
    """
    A simple decorator to measure the execution time of a function.
    """
    # @wraps(func) copies the __name__, __doc__, and other metadata 
    # from the original 'func' to the 'wrapper'. Without this, the 
    # decorated function would falsely report its name as "wrapper".
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # 1. Pre-logic: Record the start time
        start_time = time.time()
        
        # 2. Core logic: Execute the original function
        # We use *args and **kwargs to support functions with ANY signature.
        result = func(*args, **kwargs)
        
        # 3. Post-logic: Record end time and print duration
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[Timer] Function '{func.__name__}' took {execution_time:.4f}s to run.")
        
        # 4. Return the result so the caller gets what they expect
        return result
    
    # Return the unexecuted wrapper function to replace the original function
    return wrapper


# Applying the decorator using syntactic sugar
@timer_decorator
def heavy_computation(n: int) -> int:
    """Simulates a heavy computation task."""
    total = 0
    for i in range(n):
        total += i
    return total

def memoize(func: Callable) -> Callable:
    """Practice Solution: Caches results of expensive function calls."""
    cache: Dict[Tuple, Any] = {}
    
    @wraps(func)
    def wrapper(*args: Any) -> Any:
        # Note: We only use args for cache keys here to keep it simple.
        if args in cache:
            print(f"[Cache Hit] Returning cached result for {args}")
            return cache[args]
        print(f"[Cache Miss] Computing result for {args}")
        result = func(*args)
        cache[args] = result
        return result
    return wrapper

@memoize
def expensive_add(a: int, b: int) -> int:
    time.sleep(0.5) # Simulate expensive work
    return a + b

def retry(max_retries: int = 3) -> Callable:
    """
    Interview Solution: Parameterized Decorator for retrying failed functions.
    Notice the 3 levels of nesting! 
    1. Factory (takes arguments)
    2. Decorator (takes function)
    3. Wrapper (takes function arguments)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[Retry] Attempt {attempts}/{max_retries} failed: {e}")
            raise RuntimeError(f"[Retry] Failed permanently after {max_retries} attempts.")
        return wrapper
    return decorator

@retry(max_retries=3)
def unstable_network_call() -> str:
    """Simulates a function that fails randomly."""
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network timeout!")
    return "200 OK Response"


# =============================================================================
# GENERATORS IMPLEMENTATION
# =============================================================================

def fibonacci_generator() -> Generator[int, None, None]:
    """
    An infinite generator that yields the Fibonacci sequence.
    This would be impossible with a normal list-returning function!
    """
    a, b = 0, 1
    
    while True: # Infinite loop! Safe because of 'yield'
        # Yield the current value and PAUSE here.
        yield a
        
        # When next() is called, execution RESUMES here.
        a, b = b, a + b


def is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0: return False
    return True

def prime_generator() -> Generator[int, None, None]:
    """Practice Solution: Infinite prime number generator."""
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

def chunker(iterable: Iterable[Any], chunk_size: int) -> Generator[List[Any], None, None]:
    """
    Interview Solution: Yield successive n-sized chunks from an iterable.
    This is extremely common in ML for batching.
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
            
    # Don't forget the last partial chunk!
    if chunk:
        yield chunk


# =============================================================================
# MASTER CLASS EXECUTION & TESTS
# =============================================================================
def run_master_class() -> None:
    print("\n" + "="*50)
    print("DECORATORS & GENERATORS: LIVE DEMO")
    print("="*50 + "\n")

    # --- Decorator Tests ---
    print("--- 1. Testing Decorators ---")
    
    print("Running @timer_decorator:")
    res = heavy_computation(1_000_000)
    
    print("\nRunning @memoize decorator:")
    expensive_add(10, 20) # Miss
    expensive_add(10, 20) # Hit
    
    print("\nRunning @retry decorator:")
    try:
        success = unstable_network_call()
        print(success)
    except Exception as e:
        print(f"Ultimately failed: {e}")

    # --- Generator Tests ---
    print("\n--- 2. Testing Generators ---")
    
    print("Fibonacci Generator (First 10):")
    fib = fibonacci_generator()
    fib_list = [next(fib) for _ in range(10)]
    print(fib_list)
    assert fib_list == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    print("\nPrime Generator (First 5):")
    primes = prime_generator()
    prime_list = [next(primes) for _ in range(5)]
    print(prime_list)
    assert prime_list == [2, 3, 5, 7, 11]

    print("\nChunker Generator (Batching):")
    data = list(range(1, 11))
    batches = list(chunker(data, chunk_size=3))
    print(f"Data: {data}")
    for i, batch in enumerate(batches):
        print(f"Batch {i+1}: {batch}")
    assert batches == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

    # --- Performance Proof ---
    print("\n--- 3. Generator Memory Proof ---")
    n = 5_000_000
    list_comp = [x * 2 for x in range(n)]       # Eager evaluation
    gen_expr = (x * 2 for x in range(n))        # Lazy evaluation
    
    print(f"Memory for list of {n} items: {sys.getsizeof(list_comp) / 1024 / 1024:.2f} MB")
    print(f"Memory for generator of {n} items: {sys.getsizeof(gen_expr)} Bytes!")
    
    print("\nMaster Class tests passed successfully!")


if __name__ == "__main__":
    run_master_class()
