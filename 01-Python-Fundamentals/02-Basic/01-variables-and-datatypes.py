#!/usr/bin/env python3
"""
Python Variables and Data Types - Comprehensive Guide
===================================================

This module demonstrates Python's fundamental data types with multiple
implementations, performance benchmarks, and comprehensive testing.

Topics Covered:
- Basic data types (int, float, str, bool)
- Collections (list, tuple, set, dict)
- Type hints and modern Python features
- Memory management concepts
- Performance comparisons
- Real-world usage patterns

Author: Python DSA Master Course
Version: 1.0
"""

import sys
import timeit
import gc
from typing import List, Dict, Tuple, Set, Union, Optional, Any
from collections import namedtuple
from dataclasses import dataclass
import json


# ============================================================================
# SECTION 1: BASIC DATA TYPES
# ============================================================================

def basic_data_types_demo():
    """
    Demonstrates basic Python data types with detailed explanations.
    
    Time Complexity: O(1) for each assignment
    Space Complexity: O(1) for each variable
    """
    print("=== BASIC DATA TYPES DEMO ===")
    
    # Integer - arbitrary precision in Python
    x: int = 5
    big_int: int = 10**100  # Python handles big integers automatically
    
    # Float - IEEE 754 double precision
    y: float = 3.14
    scientific: float = 1.23e-4
    
    # String - immutable sequence of Unicode characters
    s: str = "Hello, World!"
    multiline: str = """This is a
    multiline string"""
    
    # Boolean - subclass of int
    flag: bool = True
    
    # NoneType - represents absence of value
    none_val: Optional[int] = None
    
    # Type inspection
    print(f"Integer {x}: type={type(x)}, size={sys.getsizeof(x)} bytes, id={id(x)}")
    print(f"Big int: {big_int}")
    print(f"Float {y}: type={type(y)}, size={sys.getsizeof(y)} bytes")
    print(f"String '{s}': type={type(s)}, size={sys.getsizeof(s)} bytes, length={len(s)}")
    print(f"Boolean {flag}: type={type(flag)}, isinstance(flag, int)={isinstance(flag, int)}")
    print(f"None: type={type(none_val)}")
    
    # Demonstrate mutability/immutability
    original_id = id(x)
    x += 1
    print(f"After x += 1: new_id={id(x)}, changed={original_id != id(x)}")
    
    return x, y, s, flag


def string_operations_demo():
    """
    Comprehensive string operations demonstration.
    
    Strings are immutable in Python - each operation creates new string objects.
    """
    print("\n=== STRING OPERATIONS DEMO ===")
    
    # String creation methods
    s1 = "Hello"
    s2 = 'World'  # Single quotes equivalent
    s3 = f"{s1}, {s2}!"  # f-string (Python 3.6+)
    s4 = "{}, {}!".format(s1, s2)  # .format() method
    s5 = "%s, %s!" % (s1, s2)  # % formatting (legacy)
    
    print(f"f-string: {s3}")
    print(f".format(): {s4}")
    print(f"% format: {s5}")
    
    # Common string methods
    text = "  Python Programming  "
    print(f"Original: '{text}'")
    print(f"strip(): '{text.strip()}'")
    print(f"lower(): '{text.lower()}'")
    print(f"upper(): '{text.upper()}'")
    print(f"replace(): '{text.replace('Python', 'Java')}'")
    
    # String slicing and indexing
    sample = "Hello, World!"
    print(f"\nString slicing examples with '{sample}':")
    print(f"sample[0]: '{sample[0]}'")
    print(f"sample[-1]: '{sample[-1]}'")
    print(f"sample[1:5]: '{sample[1:5]}'")
    print(f"sample[:5]: '{sample[:5]}'")
    print(f"sample[7:]: '{sample[7:]}'")
    print(f"sample[::2]: '{sample[::2]}'")  # Step
    print(f"sample[::-1]: '{sample[::-1]}'")  # Reverse
    
    # Memory efficiency consideration
    print(f"\nMemory sizes:")
    print(f"Short string 'hi': {sys.getsizeof('hi')} bytes")
    print(f"Long string: {sys.getsizeof('a' * 1000)} bytes")


# ============================================================================
# SECTION 2: COLLECTIONS
# ============================================================================

def list_operations_demo():
    """
    Comprehensive list operations with performance analysis.
    
    Lists are dynamic arrays with amortized O(1) append.
    """
    print("\n=== LIST OPERATIONS DEMO ===")
    
    # List creation methods
    list1 = [1, 2, 3, 4, 5]
    list2 = list(range(5))
    list3 = [x**2 for x in range(5)]  # List comprehension
    
    print(f"Direct: {list1}")
    print(f"range(): {list2}")
    print(f"Comprehension: {list3}")
    
    # List methods and operations
    numbers = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"\nOriginal list: {numbers}")
    
    # Mutating operations
    numbers.append(8)
    print(f"After append(8): {numbers}")
    
    numbers.insert(2, 99)
    print(f"After insert(2, 99): {numbers}")
    
    removed = numbers.pop()
    print(f"After pop(): {numbers}, removed: {removed}")
    
    numbers.remove(99)  # Remove first occurrence
    print(f"After remove(99): {numbers}")
    
    numbers.sort()
    print(f"After sort(): {numbers}")
    
    numbers.reverse()
    print(f"After reverse(): {numbers}")
    
    # Memory layout (conceptual)
    print(f"\nMemory analysis:")
    print(f"List size: {sys.getsizeof(numbers)} bytes")
    print(f"List length: {len(numbers)}")
    print(f"Bytes per element: {sys.getsizeof(numbers) / len(numbers):.2f}")
    
    return numbers


def dict_operations_demo():
    """
    Comprehensive dictionary operations demonstration.
    
    Dicts use hash tables with O(1) average case lookup.
    """
    print("\n=== DICTIONARY OPERATIONS DEMO ===")
    
    # Dictionary creation methods
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = dict(a=1, b=2, c=3)
    dict3 = {x: x**2 for x in range(1, 4)}  # Dict comprehension
    
    print(f"Literal: {dict1}")
    print(f"Constructor: {dict2}")
    print(f"Comprehension: {dict3}")
    
    # Dictionary operations
    student = {
        'name': 'Alice',
        'age': 20,
        'grades': [85, 92, 78, 96],
        'active': True
    }
    
    print(f"\nStudent data: {student}")
    
    # Access methods
    print(f"Name: {student['name']}")
    print(f"Age: {student.get('age', 'Unknown')}")
    print(f"GPA: {student.get('gpa', 'Not calculated')}")
    
    # Modification
    student['gpa'] = sum(student['grades']) / len(student['grades'])
    print(f"After adding GPA: {student}")
    
    # Iteration patterns
    print(f"\nIteration patterns:")
    print(f"Keys: {list(student.keys())}")
    print(f"Values: {list(student.values())}")
    print(f"Items: {list(student.items())}")
    
    # Dictionary methods
    print(f"\nDictionary methods:")
    backup = student.copy()
    print(f"Copied: {backup == student}")
    
    # Nested dictionaries
    nested = {
        'students': {
            'alice': {'grade': 95},
            'bob': {'grade': 87}
        },
        'metadata': {
            'course': 'Python DSA',
            'semester': 'Fall 2024'
        }
    }
    print(f"Nested access: {nested['students']['alice']['grade']}")
    
    return student


def set_operations_demo():
    """
    Set operations demonstration with mathematical set theory.
    """
    print("\n=== SET OPERATIONS DEMO ===")
    
    # Set creation
    set1 = {1, 2, 3, 4, 5}
    set2 = set([3, 4, 5, 6, 7])
    set3 = {x for x in range(1, 8) if x % 2 == 0}  # Set comprehension
    
    print(f"Set 1: {set1}")
    print(f"Set 2: {set2}")
    print(f"Even numbers: {set3}")
    
    # Set operations
    print(f"\nSet operations:")
    print(f"Union: {set1 | set2}")
    print(f"Intersection: {set1 & set2}")
    print(f"Difference: {set1 - set2}")
    print(f"Symmetric difference: {set1 ^ set2}")
    
    # Set methods
    colors = {'red', 'green', 'blue'}
    colors.add('yellow')
    print(f"After add: {colors}")
    
    colors.discard('green')  # Won't raise error if not found
    print(f"After discard: {colors}")
    
    # Practical use: removing duplicates
    numbers_with_dups = [1, 2, 2, 3, 3, 3, 4, 5, 5]
    unique_numbers = list(set(numbers_with_dups))
    print(f"Remove duplicates: {numbers_with_dups} -> {unique_numbers}")


def tuple_operations_demo():
    """
    Tuple operations and use cases demonstration.
    
    Tuples are immutable sequences, often used for heterogeneous data.
    """
    print("\n=== TUPLE OPERATIONS DEMO ===")
    
    # Tuple creation
    point = (3, 4)
    coordinates = 10, 20  # Parentheses optional
    single_item = (42,)  # Note the comma for single-item tuple
    empty_tuple = ()
    
    print(f"Point: {point}")
    print(f"Coordinates: {coordinates}")
    print(f"Single item: {single_item}")
    print(f"Empty: {empty_tuple}")
    
    # Named tuples for structured data
    Point = namedtuple('Point', ['x', 'y'])
    Student = namedtuple('Student', ['name', 'age', 'gpa'])
    
    p1 = Point(3, 4)
    student = Student('Alice', 20, 3.8)
    
    print(f"\nNamed tuples:")
    print(f"Point: {p1}, x={p1.x}, y={p1.y}")
    print(f"Student: {student}, name={student.name}")
    
    # Tuple unpacking
    x, y = point
    name, age, gpa = student
    print(f"Unpacked point: x={x}, y={y}")
    print(f"Unpacked student: {name}, {age}, {gpa}")
    
    # Multiple assignment using tuples
    a, b = 1, 2
    a, b = b, a  # Elegant swap
    print(f"After swap: a={a}, b={b}")


# ============================================================================
# SECTION 3: MODERN PYTHON FEATURES
# ============================================================================

@dataclass
class Person:
    """
    Modern Python data class demonstration.
    
    Automatically generates __init__, __repr__, __eq__, etc.
    """
    name: str
    age: int
    email: Optional[str] = None
    scores: List[float] = None
    
    def __post_init__(self):
        if self.scores is None:
            self.scores = []
    
    @property
    def average_score(self) -> float:
        """Calculate average score with proper error handling."""
        return sum(self.scores) / len(self.scores) if self.scores else 0.0
    
    def add_score(self, score: float) -> None:
        """Add a score with validation."""
        if not 0 <= score <= 100:
            raise ValueError(f"Score must be between 0 and 100, got {score}")
        self.scores.append(score)


def modern_python_demo():
    """
    Demonstrate modern Python features including type hints and dataclasses.
    """
    print("\n=== MODERN PYTHON FEATURES DEMO ===")
    
    # Dataclass usage
    person1 = Person("Alice", 25, "alice@example.com")
    person2 = Person("Bob", 30)
    
    print(f"Person 1: {person1}")
    print(f"Person 2: {person2}")
    
    # Add scores
    person1.add_score(95.5)
    person1.add_score(87.2)
    person1.add_score(92.8)
    
    print(f"Person 1 average: {person1.average_score:.2f}")
    
    # Type annotations with Union and Optional
    def process_data(data: Union[List[int], Dict[str, int]], 
                    multiplier: float = 1.0) -> Union[List[float], Dict[str, float]]:
        """Process data with type safety."""
        if isinstance(data, list):
            return [x * multiplier for x in data]
        elif isinstance(data, dict):
            return {k: v * multiplier for k, v in data.items()}
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")
    
    # Usage examples
    numbers = [1, 2, 3, 4, 5]
    grades = {"math": 85, "physics": 92, "chemistry": 78}
    
    result1 = process_data(numbers, 2.0)
    result2 = process_data(grades, 1.1)
    
    print(f"Processed list: {result1}")
    print(f"Processed dict: {result2}")


# ============================================================================
# SECTION 4: PERFORMANCE BENCHMARKS
# ============================================================================

def benchmark_operations():
    """
    Performance benchmarks for common operations.
    """
    print("\n=== PERFORMANCE BENCHMARKS ===")
    
    # List vs tuple access
    list_data = list(range(1000))
    tuple_data = tuple(range(1000))
    
    def list_access():
        return sum(list_data)
    
    def tuple_access():
        return sum(tuple_data)
    
    list_time = timeit.timeit(list_access, number=10000)
    tuple_time = timeit.timeit(tuple_access, number=10000)
    
    print(f"List sum time: {list_time:.6f}s")
    print(f"Tuple sum time: {tuple_time:.6f}s")
    print(f"Tuple is {list_time/tuple_time:.2f}x faster for iteration")
    
    # List comprehension vs loop
    def list_comp():
        return [x**2 for x in range(1000)]
    
    def explicit_loop():
        result = []
        for x in range(1000):
            result.append(x**2)
        return result
    
    comp_time = timeit.timeit(list_comp, number=1000)
    loop_time = timeit.timeit(explicit_loop, number=1000)
    
    print(f"\nList comprehension: {comp_time:.6f}s")
    print(f"Explicit loop: {loop_time:.6f}s")
    print(f"Comprehension is {loop_time/comp_time:.2f}x faster")
    
    # Dictionary vs list lookup
    dict_lookup = {i: i**2 for i in range(1000)}
    list_lookup = [(i, i**2) for i in range(1000)]
    
    def dict_search():
        return dict_lookup.get(500, -1)
    
    def list_search():
        for key, value in list_lookup:
            if key == 500:
                return value
        return -1
    
    dict_search_time = timeit.timeit(dict_search, number=10000)
    list_search_time = timeit.timeit(list_search, number=10000)
    
    print(f"\nDict lookup: {dict_search_time:.6f}s")
    print(f"List search: {list_search_time:.6f}s")
    print(f"Dict is {list_search_time/dict_search_time:.0f}x faster for lookup")


def memory_analysis():
    """
    Analyze memory usage of different data structures.
    """
    print("\n=== MEMORY ANALYSIS ===")
    
    # Compare memory usage
    data_structures = {
        'list[1000]': list(range(1000)),
        'tuple[1000]': tuple(range(1000)),
        'set{1000}': set(range(1000)),
        'dict{1000}': {i: i for i in range(1000)},
    }
    
    for name, data in data_structures.items():
        size = sys.getsizeof(data)
        print(f"{name}: {size:,} bytes ({size/1024:.2f} KB)")
    
    # Memory overhead demonstration
    empty_structures = {
        'empty list': [],
        'empty tuple': (),
        'empty set': set(),
        'empty dict': {},
        'empty string': '',
    }
    
    print(f"\nEmpty structure overhead:")
    for name, struct in empty_structures.items():
        print(f"{name}: {sys.getsizeof(struct)} bytes")


# ============================================================================
# SECTION 5: TESTING AND VALIDATION
# ============================================================================

def test_basic_operations():
    """
    Comprehensive tests for basic operations.
    """
    print("\n=== RUNNING TESTS ===")
    
    # Test basic types
    assert type(5) == int, "Integer type test failed"
    assert type(3.14) == float, "Float type test failed"
    assert type("hello") == str, "String type test failed"
    assert type(True) == bool, "Boolean type test failed"
    
    # Test collections
    test_list = [1, 2, 3]
    test_list.append(4)
    assert test_list == [1, 2, 3, 4], "List append test failed"
    
    test_dict = {'a': 1}
    test_dict['b'] = 2
    assert test_dict == {'a': 1, 'b': 2}, "Dict assignment test failed"
    
    test_set = {1, 2, 3}
    test_set.add(3)  # Should not duplicate
    assert len(test_set) == 3, "Set uniqueness test failed"
    
    # Test string operations
    assert "hello".upper() == "HELLO", "String upper test failed"
    assert "  test  ".strip() == "test", "String strip test failed"
    
    # Test comprehensions
    squares = [x**2 for x in range(5)]
    assert squares == [0, 1, 4, 9, 16], "List comprehension test failed"
    
    print("✅ All tests passed!")


def advanced_test_cases():
    """
    Advanced test cases covering edge cases and error conditions.
    """
    print("\n=== ADVANCED TEST CASES ===")
    
    # Test edge cases
    try:
        # Empty sequence operations
        empty_list = []
        assert len(empty_list) == 0
        assert sum(empty_list) == 0
        
        # Division by zero handling
        result = 10 / 0 if False else "avoided"
        assert result == "avoided"
        
        # None handling
        value = None
        assert value is None
        assert value != False
        assert value != 0
        
        # Large number handling
        big_num = 10**1000
        assert str(big_num).count('0') == 1000
        
        print("✅ Advanced tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


# ============================================================================
# SECTION 6: REAL-WORLD EXAMPLES
# ============================================================================

def word_frequency_counter(text: str) -> Dict[str, int]:
    """
    Real-world example: Count word frequency in text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary mapping words to their frequencies
        
    Time Complexity: O(n) where n is the number of words
    Space Complexity: O(k) where k is the number of unique words
    """
    # Clean and tokenize
    words = text.lower().replace('.', '').replace(',', '').split()
    
    # Count frequencies
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    
    return frequency


def data_processing_pipeline():
    """
    Demonstrate a real-world data processing pipeline.
    """
    print("\n=== REAL-WORLD DATA PROCESSING PIPELINE ===")
    
    # Sample data: student records
    raw_data = [
        "Alice,85,92,78",
        "Bob,90,87,95",
        "Charlie,78,85,88",
        "Diana,95,98,92"
    ]
    
    # Step 1: Parse raw data
    students = []
    for line in raw_data:
        parts = line.split(',')
        name = parts[0]
        scores = [int(score) for score in parts[1:]]
        students.append({
            'name': name,
            'scores': scores,
            'average': sum(scores) / len(scores)
        })
    
    print("Step 1 - Parsed data:")
    for student in students:
        print(f"  {student}")
    
    # Step 2: Data analysis
    all_averages = [student['average'] for student in students]
    class_average = sum(all_averages) / len(all_averages)
    top_student = max(students, key=lambda s: s['average'])
    
    print(f"\nStep 2 - Analysis:")
    print(f"  Class average: {class_average:.2f}")
    print(f"  Top student: {top_student['name']} ({top_student['average']:.2f})")
    
    # Step 3: Generate report
    report = {
        'total_students': len(students),
        'class_average': round(class_average, 2),
        'top_performer': top_student['name'],
        'grade_distribution': {
            'A': len([s for s in students if s['average'] >= 90]),
            'B': len([s for s in students if 80 <= s['average'] < 90]),
            'C': len([s for s in students if s['average'] < 80])
        }
    }
    
    print(f"\nStep 3 - Report:")
    print(json.dumps(report, indent=2))
    
    return report


# ============================================================================
# SECTION 7: INTERACTIVE EXERCISES
# ============================================================================

def interactive_quiz():
    """
    Interactive quiz for self-assessment.
    """
    print("\n=== INTERACTIVE QUIZ ===")
    
    questions = [
        {
            'question': "What is the output of: print(type(5))?",
            'options': ["<class 'int'>", "<type 'int'>", "int", "integer"],
            'correct': 0
        },
        {
            'question': "Which of these creates an empty dictionary?",
            'options': ["[]", "()", "{}", "set()"],
            'correct': 2
        },
        {
            'question': "What's the time complexity of dict lookup?",
            'options': ["O(n)", "O(log n)", "O(1) average", "O(n²)"],
            'correct': 2
        }
    ]
    
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"  {j + 1}. {option}")
        
        # In real interactive version, would get user input
        # For demo, show correct answer
        correct_answer = q['options'][q['correct']]
        print(f"Correct answer: {correct_answer}")
        score += 1
    
    print(f"\nQuiz complete! Score: {score}/{len(questions)}")
    return score


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all demonstrations.
    """
    print("Python Variables and Data Types - Comprehensive Demonstration")
    print("=" * 60)
    
    try:
        # Run all demonstrations
        basic_data_types_demo()
        string_operations_demo()
        list_operations_demo()
        dict_operations_demo()
        set_operations_demo()
        tuple_operations_demo()
        modern_python_demo()
        benchmark_operations()
        memory_analysis()
        test_basic_operations()
        advanced_test_cases()
        data_processing_pipeline()
        interactive_quiz()
        
        # Word frequency example
        sample_text = "Python is amazing. Python is powerful. Amazing Python!"
        freq = word_frequency_counter(sample_text)
        print(f"\nWord frequencies: {freq}")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup and final stats
        print(f"\n{'=' * 60}")
        print("Demonstration complete!")
        print(f"Python version: {sys.version}")
        print(f"Memory usage: {sys.getsizeof(locals())} bytes")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES (For students to complete)
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement a function to find the second largest number in a list without sorting.

2. Create a dictionary that maps each character in a string to its frequency.

3. Write a function that merges two dictionaries, combining values for duplicate keys.

4. Implement a simple calculator using different data types appropriately.

5. Create a data structure to represent a library catalog with books, authors, and genres.

6. Write a function that converts between different temperature scales using appropriate data types.

7. Implement a simple cache using a dictionary with size limits.

8. Create a function that validates email addresses and returns structured data about them.

9. Build a simple contact manager using classes and appropriate data structures.

10. Implement a function that analyzes text and returns comprehensive statistics.

MUSCLE MEMORY DRILLS:

Daily practice these patterns for 15 minutes:
- List comprehensions: [expr for item in iterable if condition]
- Dict comprehensions: {k: v for k, v in items if condition}
- Multiple assignment: a, b = b, a
- String formatting: f"{variable:.2f}"
- Exception handling: try/except/else/finally blocks

PERFORMANCE TIPS:

1. Use list comprehensions instead of explicit loops when possible
2. Use dict.get() instead of checking if key exists
3. Use 'in' operator for membership testing in sets/dicts
4. Use tuple unpacking for multiple assignments
5. Use enumerate() instead of range(len()) for indexed loops
"""
