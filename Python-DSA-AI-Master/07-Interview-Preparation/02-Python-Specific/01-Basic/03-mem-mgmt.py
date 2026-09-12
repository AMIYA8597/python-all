"""
Python Memory Management: Interview Preparation

This module covers essential Python memory management concepts frequently asked in interviews.
Topics include:
- Reference Counting
- Garbage Collection (Cyclic GC)
- Object identity (is vs ==)
- Interning and Small Integer Caching
- Weak References

Beginner Explanation:
Python automatically handles memory for you. When you create a variable, Python allocates memory. 
When the variable is no longer needed, Python frees the memory. It mainly uses "reference counting" 
(keeping track of how many names point to an object) and a "Garbage Collector" (to clean up 
objects that reference each other, creating a cycle).

Technical Explanation:
CPython (the standard Python implementation) manages memory primarily via Reference Counting. 
Every object has a `ob_refcnt` field. When this count reaches zero, the object is immediately deallocated.
However, reference counting cannot resolve reference cycles (e.g., list A contains list B, and list B contains list A).
To handle cycles, Python has a generational Garbage Collector (GC) running periodically to detect 
and clean up unreachable cycles.
"""
import sys
import gc
import weakref

def demonstrate_ref_counting():
    """
    Demonstrates how reference counting works using sys.getrefcount.
    """
    # Create an object
    my_list = [1, 2, 3]
    # sys.getrefcount() returns the reference count.
    # Note: getrefcount adds an extra reference temporarily while it executes.
    initial_count = sys.getrefcount(my_list)
    
    # Create another reference to the same object
    my_list_ref2 = my_list
    count_after_ref2 = sys.getrefcount(my_list)
    
    assert count_after_ref2 == initial_count + 1
    
    # Remove a reference
    del my_list_ref2
    count_after_del = sys.getrefcount(my_list)
    
    assert count_after_del == initial_count

class Node:
    def __init__(self, value: int):
        self.value = value
        self.next = None

def demonstrate_cyclic_gc():
    """
    Demonstrates cyclic garbage collection.
    """
    # Force a manual garbage collection to start clean
    gc.collect()
    
    node1 = Node(1)
    node2 = Node(2)
    
    # Create a cyclic reference
    node1.next = node2
    node2.next = node1
    
    # Remove references from the local scope
    del node1
    del node2
    
    # At this point, the reference count of the objects created above is not zero
    # because they reference each other. 
    # However, they are unreachable from the root.
    # gc.collect() will find them and clean them up.
    unreachable_objects = gc.collect()
    # It usually returns the number of unreachable objects found and cleared.
    return unreachable_objects

def demonstrate_interning():
    """
    Demonstrates small integer caching and string interning.
    CPython caches integers from -5 to 256.
    """
    a = 256
    b = 256
    # 'is' checks for object identity (same memory address)
    assert a is b
    
    c = 257
    d = 257
    # For numbers > 256, they are evaluated at runtime (though sometimes compiled 
    # in the same code block they might be reused). Generally, in REPL they are different.
    # We use equality `==` to check value, not identity.
    assert c == d
    
    # Short strings are also often interned automatically
    s1 = "hello"
    s2 = "hello"
    assert s1 is s2

def demonstrate_weakref():
    """
    Demonstrates weak references, which allow you to refer to an object without 
    increasing its reference count. Useful for caching.
    """
    class BigObject:
        pass
    
    obj = BigObject()
    # Create a weak reference to obj
    r = weakref.ref(obj)
    
    # r() returns the object if it is still alive
    assert r() is obj
    
    del obj
    # Now the object is deallocated because the weak reference doesn't keep it alive
    assert r() is None

if __name__ == "__main__":
    demonstrate_ref_counting()
    demonstrate_cyclic_gc()
    demonstrate_interning()
    demonstrate_weakref()
    print("All memory management examples passed.")
