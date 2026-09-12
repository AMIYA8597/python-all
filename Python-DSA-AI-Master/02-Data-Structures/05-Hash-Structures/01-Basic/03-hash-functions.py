"""
## A. Concept Name
Hash Functions and Hashing

## B. Analogy
Imagine a library where books are organized by the first letter of their title. The function mapping "Harry Potter" to the 'H' section is a hash function. It tells you exactly where to put and find the book without checking every shelf.

## C. Core Principles
1. Determinism: A specific input must always yield the exact same hash output during a program's lifecycle.
2. Uniformity: Hash functions should evenly distribute outputs to minimize collisions.
3. Efficiency: Calculating the hash must be fast, ideally O(1).
4. `__hash__` and `__eq__`: In Python, if `a == b`, then `hash(a) == hash(b)` must be true.

## D. Common Pitfalls
1. Hashing mutable objects: If an object's properties change after being hashed and stored in a dictionary, it will be lost.
2. Inconsistent `__eq__` and `__hash__`: Overriding one without the other can break dictionary lookups.
3. Ignoring collisions: Collisions are inevitable and degrade hash map performance from O(1) to O(N).

## E. Code Implementation
(The module code below demonstrates these concepts through basic hashing, custom hashable objects, collision simulation, and a custom HashMap.)

## F. Advanced Concepts
1. Open Addressing: Python's dict handles collisions by finding the next empty slot (probing).
2. SIPHash: Python mitigates Hash Denial of Service (DoS) by randomly salting string/bytes hashes.
3. Chaining: Another collision resolution technique using linked lists (demonstrated below).

## X. Project Connection
In AI and DSA projects, efficient lookups are critical. State caching (memoization) for search algorithms, deduplication of generated nodes, and rapid data retrieval all rely heavily on dictionary lookups, which fundamentally depend on robust and efficient hash functions.
"""

from typing import Any, Dict, List

# ---------------------------------------------------------
# Basic Implementation: Python's Built-in Hashing
# ---------------------------------------------------------

def basic_hashing() -> None:
    """Demonstrates built-in hash() function behavior."""
    
    # Hashing integers (often just returns the integer itself in Python)
    print(f"Hash of 42: {hash(42)}")
    
    # Hashing strings
    print(f"Hash of 'Hello': {hash('Hello')}")
    
    # Hashing tuples (Immutable, therefore hashable)
    print(f"Hash of (1, 2): {hash((1, 2))}")
    
    # Unhashable types
    try:
        hash([1, 2, 3]) # Lists are mutable!
    except TypeError as e:
        print(f"Expected Error: {e}")

# ---------------------------------------------------------
# Professional Implementation: Custom Hashable Objects
# ---------------------------------------------------------

class Point2D:
    """
    A 2D Point class demonstrating correct __hash__ and __eq__ implementation.
    This allows Point2D instances to be used in sets or as dict keys.
    """
    
    # __slots__ improves memory efficiency for small objects created many times
    __slots__ = ('_x', '_y')
    
    def __init__(self, x: float, y: float):
        # We make attributes "private" to signal they shouldn't change
        # If they change, the hash changes, which breaks Hash Tables.
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __eq__(self, other: Any) -> bool:
        """
        Defines equality. If two points have the same x and y, they are equal.
        """
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        Generates a hash based on the immutable components of the object.
        RULE: If a == b, then hash(a) == hash(b).
        A common pattern is to hash a tuple of the object's crucial attributes.
        """
        return hash((self.x, self.y))
    
    def __repr__(self) -> str:
        return f"Point2D({self.x}, {self.y})"


# ---------------------------------------------------------
# Deep Dive: Simulating Hash Collisions (Theory)
# ---------------------------------------------------------

class BadHashPoint:
    """
    A purposefully bad hash implementation to demonstrate collisions.
    It always returns the same hash!
    """
    def __init__(self, name: str):
        self.name = name
        
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, BadHashPoint): return False
        return self.name == other.name
        
    def __hash__(self) -> int:
        return 42 # TERRIBLE HASH FUNCTION! 100% Collision rate.

def demonstrate_collisions() -> None:
    """
    Python dictionaries use 'Open Addressing' to handle collisions.
    When we insert multiple BadHashPoints, they all hash to 42.
    Python has to do extra work (probing) to find empty slots for the new keys.
    When looking them up, it hashes to 42, then uses `__eq__` to check every 
    item in the collision chain until it finds the right one.
    This degrades Dictionary performance from O(1) to O(N).
    """
    collision_dict: Dict[BadHashPoint, int] = {}
    
    # This works, but internally it's doing O(N) work per insertion
    p1 = BadHashPoint("A")
    p2 = BadHashPoint("B")
    p3 = BadHashPoint("C")
    
    collision_dict[p1] = 100
    collision_dict[p2] = 200
    collision_dict[p3] = 300
    
    assert collision_dict[p2] == 200
    
    # Proof they have the same hash
    assert hash(p1) == hash(p2) == hash(p3)


# ---------------------------------------------------------
# Interview Challenge: Design a Hash Map
# ---------------------------------------------------------
class SimpleHashMap:
    """
    Interview Question: Design a simple Hash Map from scratch without using built-in dicts.
    
    This implementation uses chaining (linked lists / sub-lists) for collision resolution,
    which is different from Python's built-in open addressing, but very common in interviews.
    """
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        # Create an array of empty lists (the 'buckets')
        self.buckets: List[List[Any]] = [[] for _ in range(self.capacity)]
        self.size = 0
        
    def _get_hash(self, key: Any) -> int:
        """Compute the bucket index for a given key."""
        return hash(key) % self.capacity
        
    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair. O(1) average, O(N) worst case."""
        index = self._get_hash(key)
        bucket = self.buckets[index]
        
        # Check if key already exists, update if so
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
                
        # If key doesn't exist, append it (collision chaining)
        bucket.append((key, value))
        self.size += 1
        
    def get(self, key: Any) -> Any:
        """Retrieve a value by key. O(1) average, O(N) worst case."""
        index = self._get_hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        return -1 # Or raise KeyError
        
    def remove(self, key: Any) -> None:
        """Remove a key-value pair."""
        index = self._get_hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return


if __name__ == "__main__":
    print("Running basic hashing...")
    basic_hashing()
    
    print("Running Custom Hashable Object (Point2D)...")
    p1 = Point2D(1.0, 2.0)
    p2 = Point2D(1.0, 2.0)
    p3 = Point2D(3.0, 4.0)
    
    # Because __eq__ and __hash__ are defined correctly:
    assert p1 == p2
    assert p1 != p3
    
    # We can use them in a set
    point_set = {p1, p3}
    assert p2 in point_set # True, because p1 == p2 and hash(p1) == hash(p2)
    assert len(point_set) == 2 # p1 and p2 are identical, so p2 isn't added again if we tried
    
    print("Running Collision Demonstration...")
    demonstrate_collisions()
    
    print("Running SimpleHashMap Interview Challenge...")
    my_map = SimpleHashMap(capacity=5)
    my_map.put("apple", 50)
    my_map.put("banana", 100)
    # Force a potential collision or just test update
    my_map.put("apple", 75) 
    
    assert my_map.get("apple") == 75
    assert my_map.get("banana") == 100
    assert my_map.get("grape") == -1
    
    my_map.remove("apple")
    assert my_map.get("apple") == -1
    
    print("All tests passed successfully!")
