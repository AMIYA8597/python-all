#!/usr/bin/env python3
"""
Advanced Python Programming Concepts
====================================

This module covers intermediate to advanced Python concepts that every
Python developer should master:

1. Decorators - Function and class decorators, functools
2. Context Managers - with statements, contextlib
3. Metaclasses - Class creation, metaclass programming
4. Descriptors - Property-like behavior, data validation
5. Generators and Iterators - Memory efficient iteration
6. Coroutines and Async Programming - asyncio, await/async
7. Concurrency - Threading, multiprocessing, concurrent.futures
8. Advanced OOP - Abstract classes, multiple inheritance, MRO
9. Memory Management - Garbage collection, weak references
10. Type Hints and Annotations - Static typing, mypy
11. Data Classes and Enums - Modern Python features
12. Advanced Built-ins - functools, itertools, collections
13. Metaprogramming - Dynamic code generation
14. Performance Optimization - Profiling, caching
15. Design Patterns - Common patterns in Python

Author: Python DSA Master
Date: 2024
"""

import functools
import asyncio
import threading
import multiprocessing
import concurrent.futures
import weakref
import gc
import time
import inspect
import types
from typing import Any, Dict, List, Optional, Union, Callable, Iterator, Generator
from typing import Protocol, TypeVar, Generic, Tuple, Set
from collections import namedtuple, defaultdict, deque, Counter, ChainMap
from contextlib import contextmanager, suppress, redirect_stdout
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, IntEnum, Flag, auto
import io
import sys

# ==============================================================================
# 1. DECORATORS - FUNCTION AND CLASS DECORATORS
# ==============================================================================

def timer_decorator(func):
    """Decorator to time function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def retry_decorator(max_attempts=3, delay=1):
    """Decorator to retry function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def validate_types(**expected_types):
    """Decorator for runtime type checking."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Check types
            for param_name, expected_type in expected_types.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(f"{param_name} must be {expected_type}, got {type(value)}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_decorator(maxsize=128):
    """Custom caching decorator."""
    def decorator(func):
        cache = {}
        cache_order = deque()
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            
            if key in cache:
                return cache[key]
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Store in cache
            if len(cache) >= maxsize:
                oldest_key = cache_order.popleft()
                del cache[oldest_key]
            
            cache[key] = result
            cache_order.append(key)
            return result
        
        wrapper.cache_info = lambda: f"Cache size: {len(cache)}/{maxsize}"
        wrapper.cache_clear = lambda: (cache.clear(), cache_order.clear())
        return wrapper
    return decorator

class CountCalls:
    """Class-based decorator to count function calls."""
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} has been called {self.count} times")
        return self.func(*args, **kwargs)
    
    def reset_count(self):
        self.count = 0

# Class decorator example
def add_methods(cls):
    """Class decorator that adds methods to a class."""
    def get_info(self):
        return f"Instance of {cls.__name__}"
    
    def class_method_example(cls):
        return f"Class method of {cls.__name__}"
    
    cls.get_info = get_info
    cls.class_method_example = classmethod(class_method_example)
    return cls

# ==============================================================================
# 2. CONTEXT MANAGERS
# ==============================================================================

class FileManager:
    """Custom context manager for file operations."""
    
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        print(f"Opening file {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing file {self.filename}")
        if self.file:
            self.file.close()
        
        if exc_type is not None:
            print(f"Exception occurred: {exc_value}")
            return False  # Don't suppress exception
        return True

@contextmanager
def timer_context():
    """Context manager using contextlib.contextmanager."""
    start_time = time.time()
    print("Timer started")
    try:
        yield
    finally:
        end_time = time.time()
        print(f"Timer ended. Elapsed: {end_time - start_time:.4f} seconds")

@contextmanager
def database_connection():
    """Simulate database connection context manager."""
    print("Connecting to database...")
    connection = {"status": "connected", "transactions": []}
    try:
        yield connection
    except Exception as e:
        print(f"Rolling back transaction due to: {e}")
        connection["transactions"].clear()
        raise
    finally:
        print("Closing database connection...")

class TemporaryValue:
    """Context manager to temporarily change a value."""
    
    def __init__(self, obj, attr, temp_value):
        self.obj = obj
        self.attr = attr
        self.temp_value = temp_value
        self.original_value = None
    
    def __enter__(self):
        self.original_value = getattr(self.obj, self.attr)
        setattr(self.obj, self.attr, self.temp_value)
        return self.temp_value
    
    def __exit__(self, exc_type, exc_value, traceback):
        setattr(self.obj, self.attr, self.original_value)

# ==============================================================================
# 3. METACLASSES
# ==============================================================================

class SingletonMeta(type):
    """Metaclass that creates singleton instances."""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    """Example singleton class."""
    
    def __init__(self):
        self.value = 0

class AttributeValidationMeta(type):
    """Metaclass that adds attribute validation."""
    
    def __new__(mcs, name, bases, dct):
        # Add validation to all methods that set attributes
        if '_validations' in dct:
            validations = dct['_validations']
            
            def __setattr__(self, key, value):
                if key in validations:
                    validator = validations[key]
                    if not validator(value):
                        raise ValueError(f"Invalid value for {key}: {value}")
                super(type(self), self).__setattr__(key, value)
            
            dct['__setattr__'] = __setattr__
        
        return super().__new__(mcs, name, bases, dct)

class ValidatedClass(metaclass=AttributeValidationMeta):
    """Class with validated attributes."""
    
    _validations = {
        'age': lambda x: isinstance(x, int) and x >= 0,
        'name': lambda x: isinstance(x, str) and len(x) > 0,
    }
    
    def __init__(self, name, age):
        self.name = name
        self.age = age

class AutoPropertyMeta(type):
    """Metaclass that automatically creates properties for attributes."""
    
    def __new__(mcs, name, bases, dct):
        # Find attributes marked with underscore prefix
        properties = {}
        for key, value in list(dct.items()):
            if key.startswith('_') and not key.startswith('__'):
                prop_name = key[1:]  # Remove underscore
                
                def make_property(attr_name):
                    def getter(self):
                        return getattr(self, attr_name)
                    
                    def setter(self, value):
                        print(f"Setting {attr_name} to {value}")
                        setattr(self, attr_name, value)
                    
                    return property(getter, setter)
                
                properties[prop_name] = make_property(key)
        
        dct.update(properties)
        return super().__new__(mcs, name, bases, dct)

# ==============================================================================
# 4. DESCRIPTORS
# ==============================================================================

class ValidatedAttribute:
    """Descriptor for validated attributes."""
    
    def __init__(self, validator=None, default=None):
        self.validator = validator
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, self.default)
    
    def __set__(self, obj, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        setattr(obj, self.private_name, value)
    
    def __delete__(self, obj):
        delattr(obj, self.private_name)

class TypedAttribute:
    """Descriptor that enforces type checking."""
    
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type}, got {type(value)}")
        setattr(obj, self.private_name, value)

class Person:
    """Example class using descriptors."""
    
    name = TypedAttribute(str)
    age = ValidatedAttribute(lambda x: isinstance(x, int) and x >= 0, 0)
    email = ValidatedAttribute(lambda x: '@' in x if x else True)
    
    def __init__(self, name, age, email=None):
        self.name = name
        self.age = age
        self.email = email

# ==============================================================================
# 5. GENERATORS AND ITERATORS
# ==============================================================================

class NumberRange:
    """Custom iterator for number ranges."""
    
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.step > 0 and self.current >= self.end) or \
           (self.step < 0 and self.current <= self.end):
            raise StopIteration
        
        value = self.current
        self.current += self.step
        return value

def fibonacci_generator():
    """Generator for Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def file_reader_generator(filename):
    """Generator for reading large files line by line."""
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return

def batch_generator(iterable, batch_size):
    """Generator that yields items in batches."""
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch

def infinite_counter(start=0, step=1):
    """Infinite generator with counter."""
    current = start
    while True:
        yield current
        current += step

# Generator expressions and comprehensions
def advanced_comprehensions_demo():
    """Demonstrate advanced comprehensions."""
    # Nested list comprehension
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for row in matrix for item in row]
    
    # Dictionary comprehension with condition
    squares = {x: x**2 for x in range(10) if x % 2 == 0}
    
    # Set comprehension
    unique_lengths = {len(word) for word in ["hello", "world", "python", "programming"]}
    
    # Generator expression
    sum_of_squares = sum(x**2 for x in range(100) if x % 3 == 0)
    
    return {
        'flattened': flattened,
        'squares': squares,
        'unique_lengths': unique_lengths,
        'sum_of_squares': sum_of_squares
    }

# ==============================================================================
# 6. ASYNC PROGRAMMING AND COROUTINES
# ==============================================================================

async def async_fetch_data(url, delay=1):
    """Simulate async data fetching."""
    print(f"Fetching data from {url}")
    await asyncio.sleep(delay)
    return f"Data from {url}"

async def async_process_urls(urls):
    """Process multiple URLs concurrently."""
    tasks = [async_fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def async_producer(queue, items):
    """Async producer for queue."""
    for item in items:
        await queue.put(item)
        print(f"Produced: {item}")
        await asyncio.sleep(0.1)

async def async_consumer(queue, consumer_id):
    """Async consumer for queue."""
    while True:
        try:
            item = await asyncio.wait_for(queue.get(), timeout=1.0)
            print(f"Consumer {consumer_id} consumed: {item}")
            queue.task_done()
            await asyncio.sleep(0.2)
        except asyncio.TimeoutError:
            print(f"Consumer {consumer_id} timeout")
            break

async def async_producer_consumer_demo():
    """Demonstrate async producer-consumer pattern."""
    queue = asyncio.Queue(maxsize=5)
    items = list(range(10))
    
    # Create producer and consumers
    producer = async_producer(queue, items)
    consumers = [async_consumer(queue, i) for i in range(3)]
    
    # Run producer
    await producer
    
    # Wait for all items to be processed
    await queue.join()

class AsyncContextManager:
    """Async context manager example."""
    
    async def __aenter__(self):
        print("Entering async context")
        await asyncio.sleep(0.1)
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        print("Exiting async context")
        await asyncio.sleep(0.1)
        return False

async def async_iterator_example():
    """Async iterator example."""
    class AsyncIterator:
        def __init__(self, max_value):
            self.max_value = max_value
            self.current = 0
        
        def __aiter__(self):
            return self
        
        async def __anext__(self):
            if self.current >= self.max_value:
                raise StopAsyncIteration
            await asyncio.sleep(0.1)
            self.current += 1
            return self.current - 1
    
    async for value in AsyncIterator(5):
        print(f"Async iterator value: {value}")

# ==============================================================================
# 7. CONCURRENCY - THREADING AND MULTIPROCESSING
# ==============================================================================

import threading
import queue
import multiprocessing
import concurrent.futures

class ThreadSafeCounter:
    """Thread-safe counter using locks."""
    
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self._value += 1
    
    def get_value(self):
        with self._lock:
            return self._value

def worker_thread(thread_id, shared_counter, num_operations):
    """Worker thread function."""
    for _ in range(num_operations):
        shared_counter.increment()
        time.sleep(0.001)
    print(f"Thread {thread_id} completed")

def threading_example():
    """Demonstrate threading with shared state."""
    counter = ThreadSafeCounter()
    threads = []
    num_threads = 5
    operations_per_thread = 100
    
    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(
            target=worker_thread,
            args=(i, counter, operations_per_thread)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print(f"Final counter value: {counter.get_value()}")

def cpu_intensive_task(n):
    """CPU-intensive task for multiprocessing demo."""
    result = sum(i * i for i in range(n))
    return result

def multiprocessing_example():
    """Demonstrate multiprocessing."""
    numbers = [100000, 200000, 300000, 400000, 500000]
    
    # Sequential execution
    start_time = time.time()
    sequential_results = [cpu_intensive_task(n) for n in numbers]
    sequential_time = time.time() - start_time
    
    # Parallel execution
    start_time = time.time()
    with multiprocessing.Pool() as pool:
        parallel_results = pool.map(cpu_intensive_task, numbers)
    parallel_time = time.time() - start_time
    
    print(f"Sequential time: {sequential_time:.4f} seconds")
    print(f"Parallel time: {parallel_time:.4f} seconds")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")
    
    return sequential_results == parallel_results

def concurrent_futures_example():
    """Demonstrate concurrent.futures."""
    urls = [f"http://example{i}.com" for i in range(5)]
    
    # ThreadPoolExecutor for I/O-bound tasks
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {
            executor.submit(lambda url: f"Data from {url}", url): url
            for url in urls
        }
        
        results = []
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                results.append(data)
            except Exception as e:
                print(f"URL {url} generated exception: {e}")
    
    return results

# ==============================================================================
# 8. ADVANCED OBJECT-ORIENTED PROGRAMMING
# ==============================================================================

class Animal(ABC):
    """Abstract base class for animals."""
    
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    @abstractmethod
    def make_sound(self):
        """Abstract method that must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def move(self):
        """Abstract method for movement."""
        pass
    
    def info(self):
        """Concrete method available to all subclasses."""
        return f"{self.name} is a {self.species}"

class Mammal(Animal):
    """Mammal class inheriting from Animal."""
    
    def __init__(self, name, species, fur_color):
        super().__init__(name, species)
        self.fur_color = fur_color
    
    def nurse_young(self):
        return f"{self.name} nurses its young"

class Bird(Animal):
    """Bird class inheriting from Animal."""
    
    def __init__(self, name, species, wingspan):
        super().__init__(name, species)
        self.wingspan = wingspan
    
    def fly(self):
        return f"{self.name} flies with {self.wingspan}m wingspan"

class Dog(Mammal):
    """Dog class with multiple inheritance example."""
    
    def __init__(self, name, breed, fur_color):
        super().__init__(name, "Canis familiaris", fur_color)
        self.breed = breed
    
    def make_sound(self):
        return "Woof!"
    
    def move(self):
        return "Running on four legs"
    
    def fetch(self):
        return f"{self.name} fetches the ball"

class FlyingMixin:
    """Mixin class for flying behavior."""
    
    def fly(self):
        return f"{self.name} is flying"

class SwimmingMixin:
    """Mixin class for swimming behavior."""
    
    def swim(self):
        return f"{self.name} is swimming"

class Duck(Bird, SwimmingMixin):
    """Duck class with multiple inheritance."""
    
    def __init__(self, name, wingspan):
        super().__init__(name, "Anas platyrhynchos", wingspan)
    
    def make_sound(self):
        return "Quack!"
    
    def move(self):
        return "Walking and swimming"

# Method Resolution Order (MRO) example
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

# ==============================================================================
# 9. MEMORY MANAGEMENT AND WEAK REFERENCES
# ==============================================================================

class Node:
    """Node class for circular reference demonstration."""
    
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []
        self._observers = []
    
    def add_child(self, child):
        child.parent = self  # This creates a circular reference
        self.children.append(child)
    
    def add_observer(self, observer):
        # Use weak reference to avoid circular references
        self._observers.append(weakref.ref(observer))
    
    def notify_observers(self, message):
        # Clean up dead references and notify live ones
        live_observers = []
        for obs_ref in self._observers:
            observer = obs_ref()
            if observer is not None:
                observer.notify(message)
                live_observers.append(obs_ref)
        self._observers = live_observers

class Observer:
    """Observer class for weak reference demo."""
    
    def __init__(self, name):
        self.name = name
    
    def notify(self, message):
        print(f"Observer {self.name} received: {message}")

def memory_usage_demo():
    """Demonstrate memory management concepts."""
    import sys
    
    # Show reference counting
    a = [1, 2, 3]
    print(f"Reference count for list: {sys.getrefcount(a)}")
    
    b = a  # Increase reference count
    print(f"Reference count after assignment: {sys.getrefcount(a)}")
    
    del b  # Decrease reference count
    print(f"Reference count after deletion: {sys.getrefcount(a)}")
    
    # Demonstrate garbage collection
    print(f"Garbage collection stats: {gc.get_stats()}")
    
    # Force garbage collection
    collected = gc.collect()
    print(f"Objects collected: {collected}")

class CacheWithWeakRefs:
    """Cache implementation using weak references."""
    
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
    
    def get_object(self, key, factory):
        """Get object from cache or create new one."""
        obj = self._cache.get(key)
        if obj is None:
            obj = factory()
            self._cache[key] = obj
            print(f"Created new object for key: {key}")
        else:
            print(f"Retrieved cached object for key: {key}")
        return obj

# ==============================================================================
# 10. DATA CLASSES AND ENUMS
# ==============================================================================

@dataclass
class Point:
    """Basic dataclass for 2D point."""
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

@dataclass
class Person:
    """Dataclass with various field types."""
    name: str
    age: int
    email: Optional[str] = None
    hobbies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

@dataclass(frozen=True)
class ImmutablePoint:
    """Immutable dataclass."""
    x: float
    y: float

class Color(Enum):
    """Basic enum for colors."""
    RED = 1
    GREEN = 2
    BLUE = 3

class Status(IntEnum):
    """Integer enum for status codes."""
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4

class Permission(Flag):
    """Flag enum for permissions."""
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()
    
    # Composite permissions
    READ_WRITE = READ | WRITE
    ALL = READ | WRITE | EXECUTE

# ==============================================================================
# 11. ADVANCED BUILT-INS AND STANDARD LIBRARY
# ==============================================================================

import itertools
import operator
from collections import namedtuple, defaultdict, deque, Counter, ChainMap

def itertools_examples():
    """Demonstrate advanced itertools usage."""
    
    # Infinite iterators
    counter = itertools.count(start=10, step=2)
    first_five = list(itertools.islice(counter, 5))
    
    # Cycle through values
    colors = itertools.cycle(['red', 'green', 'blue'])
    color_list = list(itertools.islice(colors, 10))
    
    # Repeat values
    repeated = list(itertools.repeat('hello', 3))
    
    # Combinatorial iterators
    data = ['A', 'B', 'C', 'D']
    permutations = list(itertools.permutations(data, 2))
    combinations = list(itertools.combinations(data, 2))
    combinations_with_replacement = list(itertools.combinations_with_replacement(data, 2))
    
    # Grouping
    data = [1, 1, 2, 2, 2, 3, 1, 1]
    grouped = [(k, list(g)) for k, g in itertools.groupby(data)]
    
    return {
        'count': first_five,
        'cycle': color_list,
        'repeat': repeated,
        'permutations': permutations,
        'combinations': combinations,
        'combinations_with_replacement': combinations_with_replacement,
        'grouped': grouped
    }

def functools_examples():
    """Demonstrate functools usage."""
    
    # Partial functions
    multiply = lambda x, y: x * y
    double = functools.partial(multiply, 2)
    triple = functools.partial(multiply, 3)
    
    # Reduce
    numbers = [1, 2, 3, 4, 5]
    sum_all = functools.reduce(operator.add, numbers)
    product_all = functools.reduce(operator.mul, numbers)
    
    # LRU Cache
    @functools.lru_cache(maxsize=128)
    def expensive_function(n):
        time.sleep(0.1)  # Simulate expensive operation
        return n ** 2
    
    # Single dispatch
    @functools.singledispatch
    def process_data(arg):
        return f"Processing {type(arg).__name__}: {arg}"
    
    @process_data.register
    def _(arg: int):
        return f"Processing integer: {arg * 2}"
    
    @process_data.register
    def _(arg: str):
        return f"Processing string: {arg.upper()}"
    
    @process_data.register
    def _(arg: list):
        return f"Processing list of {len(arg)} items"
    
    return {
        'double': double(5),
        'triple': triple(4),
        'sum': sum_all,
        'product': product_all,
        'dispatch_int': process_data(42),
        'dispatch_str': process_data("hello"),
        'dispatch_list': process_data([1, 2, 3])
    }

def collections_examples():
    """Demonstrate advanced collections usage."""
    
    # Named tuple
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(11, y=22)
    
    # Default dict
    dd = defaultdict(list)
    dd['colors'].append('red')
    dd['colors'].append('blue')
    
    # Deque (double-ended queue)
    dq = deque(['middle'])
    dq.appendleft('left')
    dq.append('right')
    
    # Counter
    text = "hello world"
    letter_count = Counter(text)
    most_common = letter_count.most_common(3)
    
    # ChainMap
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'b': 3, 'c': 4}
    combined = ChainMap(dict1, dict2)
    
    return {
        'point': p,
        'default_dict': dict(dd),
        'deque': list(dq),
        'counter': dict(letter_count),
        'most_common': most_common,
        'chainmap': dict(combined)
    }

# ==============================================================================
# 12. DESIGN PATTERNS
# ==============================================================================

# Singleton Pattern (using metaclass)
class DatabaseConnection(metaclass=SingletonMeta):
    """Singleton database connection."""
    
    def __init__(self):
        self.connection_string = "database://localhost:5432"
        self.is_connected = False
    
    def connect(self):
        if not self.is_connected:
            print("Connecting to database...")
            self.is_connected = True
        return self

# Factory Pattern
class Animal:
    def speak(self):
        raise NotImplementedError

class FactoryDog(Animal):
    def speak(self):
        return "Woof!"

class FactoryCat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    """Factory for creating animals."""
    
    _animals = {
        'dog': FactoryDog,
        'cat': FactoryCat
    }
    
    @classmethod
    def create_animal(cls, animal_type: str) -> Animal:
        if animal_type.lower() in cls._animals:
            return cls._animals[animal_type.lower()]()
        raise ValueError(f"Unknown animal type: {animal_type}")

# Observer Pattern
class Subject:
    """Subject in observer pattern."""
    
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify()

class Observer:
    """Observer in observer pattern."""
    
    def __init__(self, name):
        self.name = name
    
    def update(self, state):
        print(f"Observer {self.name} notified with state: {state}")

# Strategy Pattern
class SortStrategy(ABC):
    """Abstract strategy for sorting."""
    
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSort(SortStrategy):
    def sort(self, data):
        data = data.copy()
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class SortContext:
    """Context for sorting strategies."""
    
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data):
        return self._strategy.sort(data)

# ==============================================================================
# DEMONSTRATION FUNCTIONS
# ==============================================================================

def demonstrate_decorators():
    """Demonstrate decorator usage."""
    print("=== DECORATORS DEMONSTRATION ===")
    
    @timer_decorator
    @cache_decorator(maxsize=3)
    @validate_types(x=int, y=int)
    def add_numbers(x, y):
        time.sleep(0.1)  # Simulate work
        return x + y
    
    @CountCalls
    def greet(name):
        return f"Hello, {name}!"
    
    # Test decorators
    print(f"Result: {add_numbers(5, 3)}")
    print(f"Cached result: {add_numbers(5, 3)}")  # Should be faster
    
    print(f"Greeting: {greet('Alice')}")
    print(f"Greeting: {greet('Bob')}")
    
    print(f"Cache info: {add_numbers.cache_info()}")

def demonstrate_context_managers():
    """Demonstrate context manager usage."""
    print("\n=== CONTEXT MANAGERS DEMONSTRATION ===")
    
    # Custom context manager
    with timer_context():
        time.sleep(0.1)
        print("Some work done")
    
    # Database connection simulation
    with database_connection() as conn:
        conn["transactions"].append("SELECT * FROM users")
        print(f"Connection status: {conn['status']}")

def demonstrate_metaclasses():
    """Demonstrate metaclass usage."""
    print("\n=== METACLASSES DEMONSTRATION ===")
    
    # Singleton
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"Same instance: {db1 is db2}")
    
    # Validated class
    try:
        person = ValidatedClass("Alice", 25)
        print(f"Created person: {person.name}, {person.age}")
        person.age = -5  # Should raise error
    except ValueError as e:
        print(f"Validation error: {e}")

def demonstrate_async_programming():
    """Demonstrate async programming."""
    print("\n=== ASYNC PROGRAMMING DEMONSTRATION ===")
    
    async def main():
        # Simple async function
        urls = ["site1.com", "site2.com", "site3.com"]
        results = await async_process_urls(urls)
        print(f"Async results: {results}")
        
        # Async context manager
        async with AsyncContextManager():
            print("Inside async context")
        
        # Async iterator
        await async_iterator_example()
    
    # Run the async demo
    asyncio.run(main())

def demonstrate_concurrency():
    """Demonstrate threading and multiprocessing."""
    print("\n=== CONCURRENCY DEMONSTRATION ===")
    
    print("Threading example:")
    threading_example()
    
    print("\nMultiprocessing example:")
    multiprocessing_example()
    
    print("\nConcurrent futures example:")
    results = concurrent_futures_example()
    print(f"Results: {results}")

def demonstrate_advanced_oop():
    """Demonstrate advanced OOP concepts."""
    print("\n=== ADVANCED OOP DEMONSTRATION ===")
    
    # Abstract classes and inheritance
    dog = Dog("Buddy", "Golden Retriever", "Golden")
    print(f"Dog info: {dog.info()}")
    print(f"Dog sound: {dog.make_sound()}")
    print(f"Dog movement: {dog.move()}")
    
    duck = Duck("Donald", 0.5)
    print(f"Duck info: {duck.info()}")
    print(f"Duck sound: {duck.make_sound()}")
    print(f"Duck swimming: {duck.swim()}")
    
    # Method Resolution Order
    d = D()
    print("MRO demonstration:")
    d.method()
    print(f"MRO: {D.__mro__}")

def demonstrate_design_patterns():
    """Demonstrate design patterns."""
    print("\n=== DESIGN PATTERNS DEMONSTRATION ===")
    
    # Factory pattern
    dog = AnimalFactory.create_animal('dog')
    cat = AnimalFactory.create_animal('cat')
    print(f"Factory dog: {dog.speak()}")
    print(f"Factory cat: {cat.speak()}")
    
    # Observer pattern
    subject = Subject()
    observer1 = Observer("Observer1")
    observer2 = Observer("Observer2")
    
    subject.attach(observer1)
    subject.attach(observer2)
    subject.set_state("New State")
    
    # Strategy pattern
    data = [64, 34, 25, 12, 22, 11, 90]
    
    context = SortContext(BubbleSort())
    bubble_sorted = context.sort(data)
    print(f"Bubble sort: {bubble_sorted}")
    
    context.set_strategy(QuickSort())
    quick_sorted = context.sort(data)
    print(f"Quick sort: {quick_sorted}")

def main():
    """Run all advanced Python demonstrations."""
    print("Advanced Python Programming Concepts - Comprehensive Demonstration")
    print("=" * 80)
    
    demonstrate_decorators()
    demonstrate_context_managers()
    demonstrate_metaclasses()
    demonstrate_async_programming()
    demonstrate_concurrency()
    demonstrate_advanced_oop()
    demonstrate_design_patterns()
    
    print(f"\n{'=' * 80}")
    print("Advanced Python concepts demonstrated:")
    print("✓ Decorators (function and class decorators)")
    print("✓ Context Managers (with statements, contextlib)")
    print("✓ Metaclasses (class creation, validation)")
    print("✓ Descriptors (property-like behavior)")
    print("✓ Generators and Iterators (memory efficiency)")
    print("✓ Async Programming (asyncio, coroutines)")
    print("✓ Concurrency (threading, multiprocessing)")
    print("✓ Advanced OOP (ABC, multiple inheritance)")
    print("✓ Memory Management (weak references, GC)")
    print("✓ Data Classes and Enums")
    print("✓ Advanced Built-ins (itertools, functools)")
    print("✓ Design Patterns (Singleton, Factory, Observer, Strategy)")
    
    print("\nAdditional concepts covered:")
    print("- Type hints and annotations")
    print("- Metaprogramming techniques")
    print("- Performance optimization strategies")
    print("- Modern Python features (3.7+)")

if __name__ == "__main__":
    main()
