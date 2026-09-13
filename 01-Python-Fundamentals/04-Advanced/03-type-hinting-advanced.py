"""
# ==============================================================================
# LABORATORY: ADVANCED TYPE HINTING & STRUCTURAL SUBTYPING
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python is dynamically typed, but production codebases (especially with FastAPI 
# and Pydantic) rely heavily on static type hints. Advanced type hinting allows 
# tools like `mypy` to catch bugs before they ever reach production. Mastering 
# Generics and Protocols enables you to write highly reusable, type-safe APIs.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand basic vs advanced annotations (`Optional`, `Union`, `Literal`).
# - Master `Callable` for higher-order functions.
# - Understand Generics (`TypeVar`) for type-safe containers.
# - Master Structural Subtyping (Duck Typing) using `Protocol`.
# - Use `TypedDict` to strongly type JSON/Dictionary payloads.
#
# ==============================================================================
"""

from typing import (
    List, Dict, Union, Optional, Callable, 
    TypeVar, Generic, Literal, TypedDict, Any
)
# Note: Protocol is in typing (Python 3.8+)
from typing import Protocol

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. UNION, OPTIONAL, AND LITERAL
# ==============================================================================
# Optional[X] is exactly equivalent to Union[X, None].
# Literal restricts a value to a specific set of raw data values.

def process_status(status: Literal["pending", "running", "failed"], timeout: Optional[int] = None) -> Union[str, int]:
    if status == "failed":
        return -1
    return f"Processing {status} with timeout {timeout}"

def demonstrate_basic_advanced():
    section_header("Literal, Optional, and Union")
    print(process_status("running", 30))
    # process_status("unknown") # mypy would flag this as an Error!


# ==============================================================================
# 4. CALLABLE (TYPING FUNCTIONS)
# ==============================================================================
# Callable[[Arg1Type, Arg2Type], ReturnType]

def execute_operation(x: int, y: int, op: Callable[[int, int], int]) -> int:
    return op(x, y)

def add(a: int, b: int) -> int:
    return a + b

def demonstrate_callable():
    section_header("Callable (Higher-Order Functions)")
    res = execute_operation(10, 5, add)
    print(f"Callable execution result: {res}")


# ==============================================================================
# 5. GENERICS AND TYPEVAR
# ==============================================================================
# TypeVar allows us to create functions/classes that can operate on ANY type,
# while maintaining the relationship between inputs and outputs.

T = TypeVar('T')

def get_first_item(items: List[T]) -> T:
    """
    If we pass a List[int], this function promises to return an int.
    If we pass a List[str], it promises to return a str.
    If we used `Any` instead of `T`, we would lose this tracking!
    """
    if not items:
        raise ValueError("List is empty")
    return items[0]

# Generic Classes
class Box(Generic[T]):
    def __init__(self, item: T):
        self.item = item
        
    def get_item(self) -> T:
        return self.item

def demonstrate_generics():
    section_header("Generics and TypeVar")
    
    first_int = get_first_item([1, 2, 3])
    first_str = get_first_item(["a", "b", "c"])
    
    print(f"Generic function results: {first_int} (int), {first_str} (str)")
    
    int_box = Box[int](100)
    str_box = Box[str]("Hello")
    print(f"Generic class results: {int_box.get_item()}, {str_box.get_item()}")


# ==============================================================================
# 6. PROTOCOLS (STRUCTURAL SUBTYPING / DUCK TYPING)
# ==============================================================================
# In standard inheritance (Nominal Subtyping), a class must explicitly inherit 
# from a base class. 
# Protocol enables "Structural Subtyping": if it walks like a duck and quacks 
# like a duck, mypy accepts it as a duck, WITHOUT explicit inheritance!

class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    # Notice we DO NOT inherit from Drawable!
    def draw(self) -> None:
        print("  Drawing a Circle")

class Square:
    def draw(self) -> None:
        print("  Drawing a Square")

class Triangle:
    # Missing the draw method
    def sketch(self) -> None:
        print("  Sketching a Triangle")

def render_shape(shape: Drawable) -> None:
    shape.draw()

def demonstrate_protocols():
    section_header("Protocols (Static Duck Typing)")
    
    c = Circle()
    s = Square()
    t = Triangle()
    
    render_shape(c) # OK
    render_shape(s) # OK
    
    # render_shape(t) # mypy ERROR: Triangle is incompatible with Protocol 'Drawable'
    print("  Triangle omitted because it lacks a draw() method (mypy error).")


# ==============================================================================
# 7. TYPEDDICT (TYPING JSON/DICTIONARIES)
# ==============================================================================
# Dictionaries usually map str -> Any. This provides no autocomplete or safety.
# TypedDict defines a strict schema for a dictionary.

class UserPayload(TypedDict):
    id: int
    username: str
    is_active: bool
    # We can use total=False to make fields optional in advanced setups.

def process_api_payload(payload: UserPayload) -> None:
    # IDEs will now autocomplete payload["username"] !
    print(f"  Processed user: {payload['username']} (Active: {payload['is_active']})")

def demonstrate_typeddict():
    section_header("TypedDict (Dictionary Schemas)")
    
    data: UserPayload = {
        "id": 1,
        "username": "admin",
        "is_active": True
    }
    process_api_payload(data)


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why use `TypeVar` (Generics) instead of `Any`?
   Answer: `Any` turns off type checking entirely. `TypeVar` tracks the type dynamically. If a function takes `List[T]` and returns `T`, mypy knows that if you pass a list of strings, the return type is absolutely a string.

2. What is the difference between `Protocol` and `ABC` (Abstract Base Class)?
   Answer: ABCs require *Nominal* subtyping (a class MUST explicitly inherit from the ABC: `class MyClass(MyABC):`). Protocols provide *Structural* subtyping (Duck Typing). As long as the class implements the required methods, it satisfies the Protocol automatically without any explicit inheritance.

3. How do you type hint a function that takes a string and returns an integer?
   Answer: `Callable[[str], int]`

4. What is `Optional[str]` equivalent to?
   Answer: `Union[str, None]`. Note: In Python 3.10+, this is written more cleanly as `str | None`.
"""

if __name__ == "__main__":
    demonstrate_basic_advanced()
    demonstrate_callable()
    demonstrate_generics()
    demonstrate_protocols()
    demonstrate_typeddict()
    print("\n[SUCCESS] Laboratory: Advanced Type Hinting Completed.")
