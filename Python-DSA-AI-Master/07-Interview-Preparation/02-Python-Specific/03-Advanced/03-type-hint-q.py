"""
Advanced Type Hinting in Python

Learning Objectives:
1. Master core `typing` module features (Generic, Protocol, Callable, Any).
2. Understand Structural Subtyping (Protocols / Duck Typing with types).
3. Use TypeVars to create generic functions and classes.
4. Implement practical type hinting for robust codebases.

Concept Explanation:
- Type hints do not affect runtime execution (except in specific libraries like Pydantic/FastAPI) but are essential for static analysis (mypy).
- `TypeVar` allows functions/classes to be parameterized by types.
- `Protocol` formalizes "duck typing" by defining an interface that a class must satisfy without explicit inheritance.

Interview Focus:
- What are Generics and why are they useful?
- Differentiate between structural (Protocol) and nominal (inheritance) subtyping.
- Write a generic function to reverse a sequence.
"""
from typing import List, Dict, TypeVar, Generic, Callable, Protocol, Sequence, Iterator

# ==========================================
# 1. TypeVars and Generics
# ==========================================

T = TypeVar('T')
U = TypeVar('U')

class Container(Generic[T]):
    """A generic container that holds items of type T."""
    def __init__(self, initial_items: List[T] = None):
        self.items = initial_items or []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_all(self) -> List[T]:
        return self.items

def reverse_sequence(seq: Sequence[T]) -> List[T]:
    """A generic function that reverses any sequence of type T."""
    return list(reversed(seq))

# ==========================================
# 2. Callables
# ==========================================

# Callable[[ArgType1, ArgType2], ReturnType]
def apply_function(items: List[T], func: Callable[[T], U]) -> List[U]:
    """Applies a function to a list of items."""
    return [func(item) for item in items]

# ==========================================
# 3. Protocols (Structural Subtyping)
# ==========================================

class Quacker(Protocol):
    """
    A Protocol defining structural requirements.
    Any class with a `quack` method returning a str is implicitly a Quacker.
    """
    def quack(self) -> str:
        ...

class Duck:
    def quack(self) -> str:
        return "Quack!"

class Person:
    def quack(self) -> str:
        return "I am impersonating a duck."

class Dog:
    def bark(self) -> str:
        return "Woof!"

def make_sound(entity: Quacker) -> str:
    """Accepts anything that implements the Quacker protocol."""
    return entity.quack()

# ==========================================
# Interview Challenge: Generic Cache
# ==========================================
# Implement a simple generic caching mechanism.

K = TypeVar('K')
V = TypeVar('V')

class Cache(Generic[K, V]):
    def __init__(self):
        self._storage: Dict[K, V] = {}
        
    def put(self, key: K, value: V) -> None:
        self._storage[key] = value
        
    def get(self, key: K) -> V | None: # Python 3.10+ union syntax (or Optional[V])
        return self._storage.get(key)
        
    def __contains__(self, key: K) -> bool:
        return key in self._storage

def test_type_hinting():
    # 1. Generics
    int_container = Container[int]()
    int_container.add(1)
    int_container.add(2)
    assert int_container.get_all() == [1, 2]
    
    # 2. Callables
    words = ["hello", "world"]
    lengths = apply_function(words, len)
    assert lengths == [5, 5]
    
    # 3. Protocols
    d = Duck()
    p = Person()
    assert make_sound(d) == "Quack!"
    assert make_sound(p) == "I am impersonating a duck."
    
    # Dog cannot be passed to make_sound according to type checkers (runtime it would fail too)
    
    # 4. Cache Challenge
    c = Cache[str, int]()
    c.put("one", 1)
    assert c.get("one") == 1
    assert c.get("two") is None
    
    print("All type hinting tests passed! (Note: Type hints are primarily checked by static analyzers like mypy).")

if __name__ == "__main__":
    test_type_hinting()
