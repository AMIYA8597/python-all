"""
## A. Concept Name
Advanced Type Hinting

## B. One-Sentence Definition
Advanced type hinting provides constructs like generics, structural subtyping (protocols), literals, and overloads to precisely describe complex types and enable robust static analysis.

## C. Why Does This Exist?
To help static type checkers (like mypy or pyright) identify potential bugs before runtime, improving code reliability, developer experience (autocomplete), and documentation without the need for extensive boilerplate unit tests.

## D. Intuition
Think of basic type hints as labels on boxes indicating what goes inside. Advanced type hints are like blueprints specifying the exact shape of the box, constraints on its contents across multiple boxes (Generics), or the rules for interacting with the box regardless of its material (Protocols).

## E. Real-Life Analogy
Basic type hints are like saying "I need a Vehicle". Generics are like saying "I need a Container holding specifically Cars". Protocols are like saying "I don't care what object it is, as long as it has a 'start_engine' method". Overloads are like a versatile tool that operates differently depending on whether you feed it wood or metal.

## F. Mental Model
The type checker is a fastidious inspector that runs *before* execution. It uses your hints to simulate the flow of data. When using `Generic[T]`, you create a placeholder `T` that gets locked to a specific type during instantiation. `Protocol` relies on structural typing (duck typing): "if it walks like a duck, it's a DuckType".

## G. Visual Explanation
Generics: 
Stack[T] -> locks T -> [ T1, T2, T3 ] all same type.

Protocol (Structural Subtyping):
Class A (has draw()) -----> Drawable
Class B (has draw()) -----> Drawable
Class C (no draw())  --X--> Drawable

## H. Formal Explanation
Python introduced type hints in 3.5 (PEP 484). Advanced features were added subsequently: Protocols in PEP 544 (structural subtyping), Literal in PEP 586, Optional/Union for union types, and Overload for defining multi-signature functions.

## I. Mathematical Foundation (if applicable)
Type theory concepts:
- **Nominal Subtyping:** A is a subtype of B if A is explicitly declared to inherit from B.
- **Structural Subtyping:** A is a subtype of B if A possesses all the properties/methods required by B.
- **Parametric Polymorphism:** Functions or classes that handle values identically without depending on their type (Generics).

## J. From-Scratch Implementation (if applicable)
See the code implementation below for a generic `Stack[T]`, a `Drawable` Protocol, and an overloaded `double` function.

## K. Library / Production Implementation (if applicable)
Python's standard library `typing` provides these constructs. Built-in collections like `list`, `dict` now natively support generics (`list[int]`). Modern frameworks like FastAPI and Pydantic heavily utilize advanced type hints for runtime validation and API schema generation.

## L. Trace (walk through example)
For the Generic Stack:
1. `s = Stack[int]()` -> `T` is bound to `int`.
2. `s.push(10)` -> Valid (`10` is int).
3. `s.push("a")` -> Static type error (expected int, got str).

## M. Complexity
- **Runtime:** Type hinting has **O(1)** runtime complexity overhead. In fact, standard type hints have zero runtime overhead as they are completely ignored by the Python interpreter during execution.
- **Space:** Zero overhead at runtime.

## N. Common Mistakes
- Confusing `Any` with `object` (`Any` disables type checking; `object` means any object, but you can only call methods common to all objects).
- Forgetting that `@overload` definitions need an actual implementation fallback without the decorator.
- Not using `Optional[T]` (or `T | None`) when a function can return `None`.

## O. Common Confusions
- **Nominal vs. Structural Subtyping:** Nominal requires explicit inheritance (`class Dog(Animal):`). Structural (`Protocol`) only requires the class to have the right methods, ignoring ancestry.
- **TypeVar vs Any:** `TypeVar` tracks the specific type. If a function takes `T` and returns `T`, passing an `int` means the checker knows it returns an `int`. If it takes `Any` and returns `Any`, the relation is lost.

## P. When To Use
- Use `Protocol` for duck typing and loose coupling.
- Use `Generic` and `TypeVar` for data structures and algorithms that are type-agnostic.
- Use `@overload` when a function's return type predictably changes based on input types.
- Use `Literal` for functions accepting a fixed set of specific values (e.g., status flags).

## Q. When NOT To Use
- In quick, throwaway scripts.
- When forcing types requires extreme meta-typing acrobatics that hinder readability without adding significant safety.

## R. Trade-offs
- **Pros:** Fewer runtime bugs, better IDE autocomplete, self-documenting code, easier and safer refactoring.
- **Cons:** Increased verbosity, steeper learning curve, occasional friction with the static type checker for dynamic patterns.

## S. Debugging
Use `mypy` or `pyright` to run static checks: `mypy my_script.py`. Use the `reveal_type(var)` function (understood specifically by type checkers) to see what type the checker infers for a given variable.

## T. Memory Hook (a short memorable principle)
"Protocols don't care who you are, only what you can do (Duck Typing). Generics don't care what you are, as long as you stay consistent."

## U. Active Recall (questions before answers)
1. What is the difference between `Protocol` and standard inheritance?
2. Why use `TypeVar` instead of `Any`?
3. What is the purpose of `@overload`?

## V. Practice (exercises)
1. Create a `Queue` class that is Generic.
2. Define a `Loggable` Protocol for objects with a `.log(message: str) -> None` method.

## W. Interview Question
"Write a generic function `first_item` that takes an Iterable of type T and returns an Optional[T]. If empty, return None. Explain how type checkers handle it."

## X. Project Connection
Advanced type hints are essential in building production-grade libraries, SDKs, and complex backend systems where data integrity and predictable contracts between modules are non-negotiable.
"""

from typing import (
    Any, Callable, Generic, Iterable, Literal, Optional, 
    Protocol, TypeVar, Union, overload
)

# --- 1. Basic Implementation: Literal and Union ---
# Literal restricts the type to specifically defined values.
Status = Literal["pending", "running", "failed", "completed"]

def process_task(task_id: int, status: Status) -> Union[bool, str]:
    """Uses Literal to restrict values and Union for multiple return types."""
    if status == "completed":
        return True
    elif status == "failed":
        return "Task Failed"
    return False


# --- 2. Intermediate Implementation: Generics and TypeVar ---
# TypeVar allows us to parameterize classes and functions.
T = TypeVar('T')

class Stack(Generic[T]):
    """A Generic Stack class that can hold elements of type T."""
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Pushes an item of type T onto the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Pops and returns an item of type T from the stack."""
        return self._items.pop()
    
    def is_empty(self) -> bool:
        """Checks if the stack is empty."""
        return len(self._items) == 0


# --- 3. Advanced Implementation: Protocols (Structural Subtyping) ---
class Drawable(Protocol):
    """
    Any object that has a `draw` method taking no arguments and returning a string
    is considered a Drawable. No need to inherit from this class.
    """
    def draw(self) -> str:
        ...

class Circle:
    # Notice this does not inherit from Drawable
    def draw(self) -> str:
        return "Drawing a Circle"

class Square:
    def draw(self) -> str:
        return "Drawing a Square"

def render_shape(shape: Drawable) -> None:
    """Accepts any object conforming to the Drawable Protocol."""
    print(shape.draw())


# --- 4. Advanced Implementation: Callable and Overload ---
@overload
def double(value: int) -> int: ...

@overload
def double(value: str) -> str: ...

@overload
def double(value: list[int]) -> list[int]: ...

def double(value: Any) -> Any:
    """
    Overloaded function that doubles ints, strings, or lists.
    The type checker reads the @overload definitions, while the runtime
    uses this generic implementation.
    """
    if isinstance(value, int):
        return value * 2
    elif isinstance(value, str):
        return value + value
    elif isinstance(value, list):
        return [x * 2 for x in value]
    raise TypeError("Unsupported type")

def execute_callback(callback: Callable[[int, int], int], x: int, y: int) -> int:
    """A function taking a Callable (function) as an argument."""
    return callback(x, y)


# --- 5. Interview Challenge Implementation ---
def first_item(items: Iterable[T]) -> Optional[T]:
    """
    Takes an Iterable of type T and returns an Optional[T].
    If the iterable is empty, it returns None.
    """
    try:
        # Create an iterator and get the first item
        iterator = iter(items)
        return next(iterator)
    except StopIteration:
        return None


# --- Tests ---
def run_tests() -> None:
    print("Testing Advanced Type Hinting...")

    # Test Literal and Union
    assert process_task(1, "completed") is True
    assert process_task(2, "failed") == "Task Failed"
    assert process_task(3, "running") is False

    # Test Generics
    int_stack = Stack[int]()
    int_stack.push(10)
    int_stack.push(20)
    assert int_stack.pop() == 20

    str_stack = Stack[str]()
    str_stack.push("hello")
    assert str_stack.pop() == "hello"

    # Test Protocols
    c = Circle()
    s = Square()
    render_shape(c) # Mypy verifies `c` has `.draw() -> str`
    render_shape(s)

    # Test Overloads
    assert double(5) == 10
    assert double("a") == "aa"
    assert double([1, 2]) == [2, 4]

    # Test Callable
    assert execute_callback(lambda a, b: a + b, 5, 3) == 8

    # Test Challenge
    assert first_item([1, 2, 3]) == 1
    assert first_item([]) is None
    assert first_item("hello") == "h"

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
