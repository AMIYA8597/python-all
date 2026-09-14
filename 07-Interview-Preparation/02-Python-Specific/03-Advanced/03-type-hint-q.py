"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PYTHON SPECIFICS - ADVANCED TYPE HINTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Interviewer: "I have a function that takes a List and returns the first element. 
# Write the Type Hints so that mypy knows that if I pass a List of Strings, 
# it returns a String, and if I pass a List of Ints, it returns an Int."
#
# A junior engineer writes: `def get_first(items: list[Any]) -> Any:`. 
# This instantly destroys the Type Checker! By returning `Any`, you silence 
# mypy completely, causing fatal bugs downstream because the compiler no longer 
# knows what the object is! You MUST use Generics (`TypeVar`).
#
# Interviewer: "I want to type-hint a parameter that accepts ANY object, as long 
# as it has a `.read()` method. Do I need to create a base class?"
#
# A junior engineer creates an Abstract Base Class and forces everything to 
# inherit from it. A senior engineer uses `typing.Protocol` to implement 
# 'Static Duck Typing' (Structural Subtyping).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Generics (`TypeVar`) to perfectly preserve return types.
# - Master Protocols (`typing.Protocol`) for Static Duck Typing.
# - Understand `Callable` and advanced Type Guards.
#
# ==============================================================================
"""

import typing

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. GENERICS (PRESERVING TYPE MATHEMATICS)
# ==============================================================================
# We define a Type Variable 'T'. It acts as a mathematical placeholder!
T = typing.TypeVar('T')

def bad_get_first(items: list[typing.Any]) -> typing.Any:
    """
    By returning Any, mypy completely forgets the data type!
    If we do `x = bad_get_first([1,2,3])`, mypy thinks `x` is Any.
    If we then do `x.lower()`, mypy will NOT throw a warning, and it will 
    crash violently at runtime.
    """
    return items[0]

def good_get_first(items: list[T]) -> T:
    """
    Using a Generic.
    If we pass a `list[int]`, 'T' instantly locks into 'int'.
    The function mathematically guarantees it will return an 'int'.
    If we then do `x.lower()`, mypy will catch the bug before you even run the code!
    """
    return items[0]

def demonstrate_generics():
    section_header("Generics (TypeVar)")
    
    print("If you use `Any`, you are actively sabotaging the Type Checker.")
    print("By using `TypeVar`, you create dynamic mathematical links between ")
    print("the input arguments and the return value.\n")
    
    list_of_ints = [1, 2, 3]
    list_of_strings = ["A", "B", "C"]
    
    print(f"Result (Ints): {good_get_first(list_of_ints)} (mypy knows this is an int!)")
    print(f"Result (Strs): {good_get_first(list_of_strings)} (mypy knows this is a str!)")


# ==============================================================================
# 4. PROTOCOLS (STATIC DUCK TYPING)
# ==============================================================================
class Readable(typing.Protocol):
    """
    A Protocol defines a mathematical 'Shape' or 'Contract'.
    It does NOT require inheritance. If a class happens to have a `.read()` 
    method, mypy will accept it as a `Readable`!
    """
    def read(self) -> str:
        ... # The ellipses (...) are mathematically required for Protocols

class NetworkStream:
    def read(self) -> str:
        return "Network Data 101010"

class FileStream:
    def read(self) -> str:
        return "File Data from Disk"
        
class BrokenStream:
    # Notice it is missing the `read` method entirely!
    def write(self, data):
        pass

def process_stream(stream: Readable):
    """
    This function accepts ANYTHING that fits the `Readable` Protocol!
    """
    print(f"  [STREAM] {stream.read()}")

def demonstrate_protocols():
    section_header("Protocols (Structural Subtyping)")
    
    print("Notice that NetworkStream and FileStream do NOT inherit from Readable!")
    print("They share zero ancestry. But because they both physically implement ")
    print("a `.read()` method, the Protocol mathematically accepts them.\n")
    
    n = NetworkStream()
    f = FileStream()
    b = BrokenStream()
    
    process_stream(n)
    process_stream(f)
    
    print("\nIf we tried to pass `BrokenStream` into `process_stream(b)`, ")
    print("mypy would instantly crash at compile time, saving production!")


# ==============================================================================
# 5. CALLABLE (TYPE-HINTING FUNCTIONS)
# ==============================================================================
def execute_callback(data: str, callback: typing.Callable[[str], int]) -> int:
    """
    The Callable type hint is extremely powerful.
    Syntax: Callable[[ArgType1, ArgType2], ReturnType]
    We are mathematically enforcing that the callback MUST accept exactly one 
    string, and MUST return exactly one integer.
    """
    return callback(data)

def valid_callback(text: str) -> int:
    return len(text)

def demonstrate_callable():
    section_header("Callable (Function Type Hints)")
    
    print("Executing a callback function securely...")
    result = execute_callback("Hello World", valid_callback)
    
    print(f"Result: {result} (mypy mathematically validated the function signature!)")


def run_all_labs():
    demonstrate_generics()
    demonstrate_protocols()
    demonstrate_callable()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the devastating danger of using `typing.Any`?"
   Senior Answer: "`Any` is an escape hatch that completely silences the static type checker (mypy). If a function returns `Any`, the type checker abandons all mathematical analysis on that variable for the rest of the script. If you later try to call a non-existent method on it, mypy will not warn you, and the program will crash violently at runtime. Instead of `Any`, you should use `Generics (TypeVar)` to preserve type continuity, or `object` if you truly want to indicate that the variable can be anything (because `object` forces you to explicitly `isinstance()` check it before calling methods on it, whereas `Any` lets you call anything blindly)."

2. Interviewer: "Explain the difference between `abc.ABC` (Abstract Base Classes) and `typing.Protocol`."
   Senior Answer: "Both are used to define strict architectural contracts. However, `abc.ABC` requires Nominal Subtyping (explicit inheritance: `class MyClass(MyABC):`). It enforces the contract heavily at *Runtime* (Instantiation Time). `typing.Protocol` uses Structural Subtyping (Static Duck Typing). You do NOT inherit from the Protocol! The classes remain completely unlinked. `mypy` statically analyzes the codebase at *Compile Time* to mathematically verify if the class's 'shape' (its methods) matches the Protocol. Protocols allow you to cleanly type-hint complex third-party libraries without forcing them to inherit from your custom ABCs."

3. Interviewer: "How do you type-hint a function that returns a Generator object?"
   Senior Answer: "You must use `typing.Generator[YieldType, SendType, ReturnType]`. A Generator is a complex state machine. It doesn't just return data; it can receive data via `gen.send()`, and it can return a final value when it crashes with `StopIteration`. For a simple generator that just yields integers (like `yield 1; yield 2`), you would type-hint it as `typing.Generator[int, None, None]`. Alternatively, you can use the simpler `typing.Iterator[int]` if you don't need the advanced `send()` semantics."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Interview Prep (Advanced Type Hinting) Completed.")
