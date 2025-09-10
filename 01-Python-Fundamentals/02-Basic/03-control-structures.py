#!/usr/bin/env python3
"""
Python Control Structures - Comprehensive Guide
==============================================

This module demonstrates Python's control structures with detailed explanations,
performance analysis, optimization techniques, and real-world applications.

Topics Covered:
- Conditional statements (if, elif, else)
- Loop structures (for, while)
- Loop control (break, continue, pass)
- List comprehensions and generator expressions
- Match statements (Python 3.10+)
- Exception handling in control flow
- Performance optimizations
- Real-world patterns and applications

Author: Python DSA Master Course
Version: 1.0
"""

import sys
import timeit
import random
from typing import List, Dict, Any, Iterator, Generator, Optional
from collections import defaultdict
import itertools


# ============================================================================
# SECTION 1: CONDITIONAL STATEMENTS
# ============================================================================

def conditional_statements_demo():
    """
    Comprehensive demonstration of conditional statements.
    """
    print("=== CONDITIONAL STATEMENTS DEMO ===")
    
    # Basic if-elif-else
    score = 85
    print(f"Score: {score}")
    
    if score >= 90:
        grade = 'A'
        print("Excellent work!")
    elif score >= 80:
        grade = 'B'
        print("Good job!")
    elif score >= 70:
        grade = 'C'
        print("Satisfactory")
    elif score >= 60:
        grade = 'D'
        print("Needs improvement")
    else:
        grade = 'F'
        print("Must retake")
    
    print(f"Grade: {grade}")
    
    # Ternary operator (conditional expression)
    age = 20
    status = "adult" if age >= 18 else "minor"
    print(f"Age {age}: {status}")
    
    # Nested conditionals
    weather = "sunny"
    temperature = 75
    
    if weather == "sunny":
        if temperature > 80:
            activity = "go to the beach"
        elif temperature > 60:
            activity = "have a picnic"
        else:
            activity = "enjoy indoor sunshine"
    elif weather == "rainy":
        activity = "stay inside and read"
    else:
        activity = "check the weather again"
    
    print(f"Weather: {weather}, Temperature: {temperature}°F")
    print(f"Recommendation: {activity}")
    
    # Multiple conditions with logical operators
    username = "admin"
    password = "secret123"
    is_active = True
    
    if username == "admin" and password == "secret123" and is_active:
        access = "Full access granted"
    elif username == "admin" and password == "secret123":
        access = "Account is deactivated"
    elif username == "admin":
        access = "Invalid password"
    else:
        access = "Invalid username"
    
    print(f"Login result: {access}")


def advanced_conditional_patterns():
    """
    Demonstrate advanced conditional patterns and best practices.
    """
    print(f"\n=== ADVANCED CONDITIONAL PATTERNS ===")
    
    # Guard clauses (early returns)
    def process_user_data(user_data):
        """Process user data with guard clauses."""
        if not user_data:
            return "Error: No user data provided"
        
        if "name" not in user_data:
            return "Error: Name is required"
        
        if "email" not in user_data:
            return "Error: Email is required"
        
        # Main processing logic
        return f"Welcome, {user_data['name']}! Email: {user_data['email']}"
    
    # Test guard clauses
    test_cases = [
        None,
        {},
        {"name": "Alice"},
        {"name": "Bob", "email": "bob@example.com"}
    ]
    
    print("Guard clause pattern:")
    for i, case in enumerate(test_cases, 1):
        result = process_user_data(case)
        print(f"  Test {i}: {result}")
    
    # Dictionary-based dispatch (alternative to long if-elif chains)
    def calculate_tax(income, state):
        """Calculate tax using dictionary dispatch."""
        tax_rates = {
            'CA': 0.13,
            'NY': 0.12,
            'TX': 0.08,
            'FL': 0.06
        }
        
        rate = tax_rates.get(state, 0.10)  # Default rate
        return income * rate
    
    print(f"\nDictionary dispatch pattern:")
    income = 50000
    for state in ['CA', 'TX', 'Unknown']:
        tax = calculate_tax(income, state)
        print(f"  Income: ${income}, State: {state}, Tax: ${tax:.2f}")
    
    # Conditional assignment patterns
    config = {"debug": True, "verbose": False}
    
    # Multiple ways to handle optional values
    log_level = config.get("log_level") or "INFO"
    debug_mode = config.get("debug", False)
    output_file = config.get("output") if config.get("output") else "stdout"
    
    print(f"\nConditional assignments:")
    print(f"  Log level: {log_level}")
    print(f"  Debug mode: {debug_mode}")
    print(f"  Output: {output_file}")


# ============================================================================
# SECTION 2: LOOP STRUCTURES
# ============================================================================

def for_loop_demo():
    """
    Comprehensive demonstration of for loops and iteration patterns.
    """
    print(f"\n=== FOR LOOP DEMO ===")
    
    # Basic for loop with range
    print("Basic range iteration:")
    for i in range(5):
        print(f"  i = {i}")
    
    # Range with start, stop, step
    print(f"\nRange with parameters:")
    for i in range(2, 10, 2):  # start=2, stop=10, step=2
        print(f"  Even number: {i}")
    
    # Iterating over sequences
    fruits = ["apple", "banana", "cherry", "date"]
    print(f"\nIterating over list:")
    for fruit in fruits:
        print(f"  Fruit: {fruit}")
    
    # Enumerate for index and value
    print(f"\nEnumerate pattern:")
    for index, fruit in enumerate(fruits):
        print(f"  {index}: {fruit}")
    
    # Enumerate with custom start
    print(f"\nEnumerate with start=1:")
    for number, fruit in enumerate(fruits, start=1):
        print(f"  {number}. {fruit}")
    
    # Iterating over dictionaries
    student = {"name": "Alice", "age": 20, "grade": "A"}
    
    print(f"\nDictionary iteration:")
    print("Keys:")
    for key in student:  # Default: iterate over keys
        print(f"  {key}")
    
    print("Key-value pairs:")
    for key, value in student.items():
        print(f"  {key}: {value}")
    
    print("Values only:")
    for value in student.values():
        print(f"  {value}")
    
    # Zip for parallel iteration
    names = ["Alice", "Bob", "Charlie"]
    ages = [25, 30, 35]
    cities = ["New York", "London", "Tokyo"]
    
    print(f"\nZip for parallel iteration:")
    for name, age, city in zip(names, ages, cities):
        print(f"  {name}, {age}, lives in {city}")
    
    # Zip with unequal lengths
    numbers1 = [1, 2, 3, 4, 5]
    numbers2 = [10, 20, 30]
    
    print(f"\nZip with unequal lengths (stops at shortest):")
    for a, b in zip(numbers1, numbers2):
        print(f"  {a} + {b} = {a + b}")
    
    # itertools.zip_longest for unequal lengths
    print(f"\nzip_longest for unequal lengths:")
    for a, b in itertools.zip_longest(numbers1, numbers2, fillvalue=0):
        print(f"  {a} + {b} = {a + b}")


def while_loop_demo():
    """
    Comprehensive demonstration of while loops and patterns.
    """
    print(f"\n=== WHILE LOOP DEMO ===")
    
    # Basic while loop
    print("Basic while loop (countdown):")
    count = 5
    while count > 0:
        print(f"  Count: {count}")
        count -= 1
    print("  Blast off!")
    
    # While loop with condition change inside
    print(f"\nWhile loop with input processing:")
    numbers = [1, 2, 3, 0, 4, 5]  # Simulate input
    index = 0
    total = 0
    
    while index < len(numbers) and numbers[index] != 0:
        total += numbers[index]
        print(f"  Added {numbers[index]}, total: {total}")
        index += 1
    
    print(f"  Final total: {total} (stopped at zero or end)")
    
    # While True with break
    print(f"\nInfinite loop with break:")
    data = [10, 20, 30, -1, 40, 50]  # -1 is sentinel
    i = 0
    
    while True:
        if i >= len(data):
            print("  Reached end of data")
            break
        
        value = data[i]
        if value == -1:
            print("  Found sentinel value, stopping")
            break
        
        print(f"  Processing: {value}")
        i += 1
    
    # While loop for user input simulation
    print(f"\nSimulated user input loop:")
    responses = ["yes", "maybe", "yes", "no"]  # Simulate responses
    response_index = 0
    
    while response_index < len(responses):
        response = responses[response_index]
        print(f"  Response: {response}")
        
        if response.lower() == "no":
            print("  User said no, stopping")
            break
        elif response.lower() == "yes":
            print("  User confirmed, continuing")
        else:
            print("  Unclear response, asking again")
        
        response_index += 1


def loop_control_demo():
    """
    Demonstrate loop control statements: break, continue, pass.
    """
    print(f"\n=== LOOP CONTROL DEMO ===")
    
    # Break statement
    print("Break statement (find first even number):")
    numbers = [1, 3, 7, 8, 9, 12, 15]
    for num in numbers:
        if num % 2 == 0:
            print(f"  Found first even number: {num}")
            break
        print(f"  {num} is odd, continuing...")
    
    # Continue statement
    print(f"\nContinue statement (skip negative numbers):")
    values = [1, -2, 3, -4, 5, 6, -7, 8]
    positive_sum = 0
    
    for value in values:
        if value < 0:
            print(f"  Skipping negative number: {value}")
            continue
        
        positive_sum += value
        print(f"  Added {value}, running sum: {positive_sum}")
    
    print(f"  Final positive sum: {positive_sum}")
    
    # Pass statement (placeholder)
    print(f"\nPass statement (placeholder implementation):")
    
    def process_data(data_type):
        if data_type == "json":
            print("  Processing JSON data...")
            # Actual JSON processing would go here
        elif data_type == "xml":
            print("  Processing XML data...")
            # Actual XML processing would go here
        elif data_type == "csv":
            pass  # TODO: Implement CSV processing
            print("  CSV processing not yet implemented")
        else:
            print("  Unknown data type")
    
    for data_format in ["json", "xml", "csv", "unknown"]:
        process_data(data_format)
    
    # Nested loop control
    print(f"\nNested loop control:")
    matrix = [
        [1, 2, 3],
        [4, 0, 6],  # 0 will cause break
        [7, 8, 9]
    ]
    
    found_zero = False
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == 0:
                print(f"  Found zero at position ({i}, {j})")
                found_zero = True
                break
            print(f"  matrix[{i}][{j}] = {value}")
        
        if found_zero:
            break
    
    # Using else clause with loops
    print(f"\nLoop else clause (executes if no break):")
    
    target = 15
    search_list = [1, 5, 10, 20, 25]
    
    for value in search_list:
        if value == target:
            print(f"  Found target {target}!")
            break
        print(f"  Checking {value}...")
    else:
        print(f"  Target {target} not found in list")
    
    # Successful search
    target = 10
    for value in search_list:
        if value == target:
            print(f"  Found target {target}!")
            break
        print(f"  Checking {value}...")
    else:
        print(f"  Target {target} not found in list")


# ============================================================================
# SECTION 3: COMPREHENSIONS
# ============================================================================

def list_comprehensions_demo():
    """
    Comprehensive demonstration of list comprehensions.
    """
    print(f"\n=== LIST COMPREHENSIONS DEMO ===")
    
    # Basic list comprehension
    numbers = range(10)
    squares = [x**2 for x in numbers]
    print(f"Squares: {squares}")
    
    # List comprehension with condition
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"Even squares: {even_squares}")
    
    # List comprehension with string processing
    words = ["hello", "world", "python", "programming"]
    capitalized = [word.capitalize() for word in words]
    long_words = [word for word in words if len(word) > 5]
    
    print(f"Capitalized: {capitalized}")
    print(f"Long words: {long_words}")
    
    # Nested list comprehension
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [item for row in matrix for item in row]
    print(f"Flattened matrix: {flattened}")
    
    # Creating multiplication table
    mult_table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
    print(f"5x5 multiplication table:")
    for row in mult_table:
        print(f"  {row}")
    
    # Complex list comprehension with multiple conditions
    numbers = range(1, 21)
    special_numbers = [
        x for x in numbers 
        if x % 2 == 0  # even
        if x % 3 != 0  # not divisible by 3
        if x > 5       # greater than 5
    ]
    print(f"Even numbers > 5, not divisible by 3: {special_numbers}")
    
    # List comprehension with function calls
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [x for x in range(2, 30) if is_prime(x)]
    print(f"Prime numbers under 30: {primes}")


def other_comprehensions_demo():
    """
    Demonstrate dictionary, set, and generator comprehensions.
    """
    print(f"\n=== OTHER COMPREHENSIONS DEMO ===")
    
    # Dictionary comprehension
    words = ["hello", "world", "python"]
    word_lengths = {word: len(word) for word in words}
    print(f"Word lengths: {word_lengths}")
    
    # Dictionary comprehension with condition
    numbers = range(1, 11)
    even_squares_dict = {x: x**2 for x in numbers if x % 2 == 0}
    print(f"Even squares dict: {even_squares_dict}")
    
    # Dictionary comprehension from existing dict
    original_prices = {"apple": 1.0, "banana": 0.5, "orange": 0.8}
    discounted_prices = {item: price * 0.8 for item, price in original_prices.items()}
    print(f"Discounted prices (20% off): {discounted_prices}")
    
    # Set comprehension
    text = "hello world"
    unique_chars = {char.lower() for char in text if char.isalpha()}
    print(f"Unique characters: {unique_chars}")
    
    # Set comprehension for finding duplicates
    data = [1, 2, 3, 2, 4, 3, 5, 1]
    seen = set()
    duplicates = {x for x in data if x in seen or seen.add(x)}
    duplicates.discard(None)  # Remove None from seen.add()
    print(f"Data: {data}")
    print(f"Finding duplicates with set comprehension: {list(seen)}")
    
    # Generator expression (memory efficient)
    def generator_demo():
        # Generator expression vs list comprehension memory usage
        import sys
        
        # List comprehension (creates full list in memory)
        list_comp = [x**2 for x in range(1000)]
        
        # Generator expression (lazy evaluation)
        gen_exp = (x**2 for x in range(1000))
        
        print(f"List comprehension memory: {sys.getsizeof(list_comp)} bytes")
        print(f"Generator expression memory: {sys.getsizeof(gen_exp)} bytes")
        
        # Using generator expression
        sum_of_squares = sum(x**2 for x in range(100))
        print(f"Sum of squares 0-99: {sum_of_squares}")
        
        # Generator expression with condition
        even_sum = sum(x for x in range(100) if x % 2 == 0)
        print(f"Sum of even numbers 0-99: {even_sum}")
    
    generator_demo()


# ============================================================================
# SECTION 4: MATCH STATEMENTS (PYTHON 3.10+)
# ============================================================================

def match_statements_demo():
    """
    Demonstrate match statements (structural pattern matching).
    Available in Python 3.10+
    """
    print(f"\n=== MATCH STATEMENTS DEMO ===")
    
    # Check Python version
    if sys.version_info >= (3, 10):
        print("Match statements are supported in this Python version")
        
        # Basic match statement
        def describe_animal(animal):
            match animal:
                case "dog":
                    return "Loyal companion"
                case "cat":
                    return "Independent hunter"
                case "bird":
                    return "Flying friend"
                case _:  # Default case
                    return "Unknown animal"
        
        animals = ["dog", "cat", "bird", "fish"]
        for animal in animals:
            description = describe_animal(animal)
            print(f"  {animal}: {description}")
        
        # Match with conditions (guards)
        def categorize_number(n):
            match n:
                case x if x < 0:
                    return "negative"
                case 0:
                    return "zero"
                case x if x > 0 and x <= 10:
                    return "small positive"
                case x if x > 10:
                    return "large positive"
        
        test_numbers = [-5, 0, 5, 15]
        print(f"\nNumber categorization:")
        for num in test_numbers:
            category = categorize_number(num)
            print(f"  {num}: {category}")
        
        # Match with data structures
        def process_data(data):
            match data:
                case {"type": "user", "name": str(name)}:
                    return f"User: {name}"
                case {"type": "product", "id": int(product_id), "price": float(price)}:
                    return f"Product #{product_id}: ${price}"
                case [first, *rest] if len(rest) > 0:
                    return f"List starting with {first}, {len(rest)} more items"
                case [single]:
                    return f"Single item: {single}"
                case []:
                    return "Empty list"
                case _:
                    return "Unknown data format"
        
        test_data = [
            {"type": "user", "name": "Alice"},
            {"type": "product", "id": 123, "price": 29.99},
            [1, 2, 3, 4],
            [42],
            [],
            "unknown"
        ]
        
        print(f"\nData processing with match:")
        for data in test_data:
            result = process_data(data)
            print(f"  {data} -> {result}")
    
    else:
        print(f"Match statements require Python 3.10+")
        print(f"Current version: {sys.version}")
        print("Demonstrating equivalent if-elif-else patterns:")
        
        # Equivalent patterns using if-elif-else
        def describe_animal_legacy(animal):
            if animal == "dog":
                return "Loyal companion"
            elif animal == "cat":
                return "Independent hunter"
            elif animal == "bird":
                return "Flying friend"
            else:
                return "Unknown animal"
        
        animals = ["dog", "cat", "bird", "fish"]
        for animal in animals:
            description = describe_animal_legacy(animal)
            print(f"  {animal}: {description}")


# ============================================================================
# SECTION 5: PERFORMANCE ANALYSIS
# ============================================================================

def performance_analysis():
    """
    Analyze performance of different control structure patterns.
    """
    print(f"\n=== PERFORMANCE ANALYSIS ===")
    
    # List comprehension vs traditional loop
    def traditional_loop():
        result = []
        for i in range(1000):
            if i % 2 == 0:
                result.append(i**2)
        return result
    
    def list_comprehension():
        return [i**2 for i in range(1000) if i % 2 == 0]
    
    def generator_expression():
        return list(i**2 for i in range(1000) if i % 2 == 0)
    
    # Benchmark the approaches
    loop_time = timeit.timeit(traditional_loop, number=1000)
    comp_time = timeit.timeit(list_comprehension, number=1000)
    gen_time = timeit.timeit(generator_expression, number=1000)
    
    print(f"Performance comparison (1000 iterations):")
    print(f"  Traditional loop: {loop_time:.6f}s")
    print(f"  List comprehension: {comp_time:.6f}s") 
    print(f"  Generator expression: {gen_time:.6f}s")
    print(f"  List comp is {loop_time/comp_time:.1f}x faster than loop")
    
    # Dictionary lookup vs if-elif chain
    def if_elif_chain(value):
        if value == "A":
            return 1
        elif value == "B":
            return 2
        elif value == "C":
            return 3
        elif value == "D":
            return 4
        elif value == "E":
            return 5
        else:
            return 0
    
    lookup_dict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    
    def dict_lookup(value):
        return lookup_dict.get(value, 0)
    
    test_value = "C"
    
    if_elif_time = timeit.timeit(lambda: if_elif_chain(test_value), number=100000)
    dict_time = timeit.timeit(lambda: dict_lookup(test_value), number=100000)
    
    print(f"\nLookup performance comparison:")
    print(f"  If-elif chain: {if_elif_time:.6f}s")
    print(f"  Dictionary lookup: {dict_time:.6f}s")
    print(f"  Dict lookup is {if_elif_time/dict_time:.1f}x faster")
    
    # Early exit optimization
    def find_without_early_exit(target, data):
        found = False
        for item in data:
            if item == target:
                found = True
        return found
    
    def find_with_early_exit(target, data):
        for item in data:
            if item == target:
                return True
        return False
    
    large_list = list(range(10000))
    target = 50  # Early in the list
    
    no_exit_time = timeit.timeit(
        lambda: find_without_early_exit(target, large_list), 
        number=1000
    )
    early_exit_time = timeit.timeit(
        lambda: find_with_early_exit(target, large_list), 
        number=1000
    )
    
    print(f"\nEarly exit optimization:")
    print(f"  Without early exit: {no_exit_time:.6f}s")
    print(f"  With early exit: {early_exit_time:.6f}s")
    print(f"  Early exit is {no_exit_time/early_exit_time:.1f}x faster")


# ============================================================================
# SECTION 6: REAL-WORLD APPLICATIONS
# ============================================================================

def real_world_applications():
    """
    Demonstrate real-world applications of control structures.
    """
    print(f"\n=== REAL-WORLD APPLICATIONS ===")
    
    # 1. Data validation and cleaning
    def clean_user_data(raw_data):
        """Clean and validate user data."""
        cleaned_data = []
        
        for entry in raw_data:
            # Skip empty entries
            if not entry:
                continue
            
            # Extract and validate fields
            try:
                name = entry.get("name", "").strip()
                email = entry.get("email", "").strip().lower()
                age = entry.get("age")
                
                # Validation rules
                if not name or len(name) < 2:
                    print(f"  Skipping entry: invalid name '{name}'")
                    continue
                
                if not email or "@" not in email:
                    print(f"  Skipping entry: invalid email '{email}'")
                    continue
                
                if not isinstance(age, int) or age < 0 or age > 150:
                    print(f"  Skipping entry: invalid age '{age}'")
                    continue
                
                # Clean and add valid entry
                cleaned_entry = {
                    "name": name.title(),
                    "email": email,
                    "age": age
                }
                cleaned_data.append(cleaned_entry)
                
            except Exception as e:
                print(f"  Error processing entry {entry}: {e}")
                continue
        
        return cleaned_data
    
    # Test data cleaning
    raw_data = [
        {"name": "alice smith", "email": "ALICE@EXAMPLE.COM", "age": 25},
        {"name": "", "email": "invalid", "age": 30},
        {"name": "Bob", "email": "bob@test.com", "age": -5},
        {"name": "Charlie", "email": "charlie@domain.com", "age": 35},
        None,
        {"name": "Diana", "age": 28},  # Missing email
    ]
    
    print("Data cleaning example:")
    clean_data = clean_user_data(raw_data)
    print("Cleaned data:")
    for entry in clean_data:
        print(f"  {entry}")
    
    # 2. Menu-driven application
    def menu_driven_calculator():
        """Simulate a menu-driven calculator."""
        print(f"\nMenu-driven calculator simulation:")
        
        # Simulate user choices
        user_inputs = [
            ("1", 10, 5),    # Addition
            ("2", 10, 3),    # Subtraction  
            ("3", 7, 8),     # Multiplication
            ("4", 20, 4),    # Division
            ("4", 10, 0),    # Division by zero
            ("5", 0, 0),     # Invalid choice
            ("6", 0, 0)      # Exit
        ]
        
        input_index = 0
        
        while input_index < len(user_inputs):
            choice, a, b = user_inputs[input_index]
            input_index += 1
            
            print(f"\nCalculator Menu:")
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            print("6. Exit")
            print(f"Choice: {choice}")
            
            if choice == "6":
                print("Goodbye!")
                break
            elif choice in ["1", "2", "3", "4"]:
                print(f"Numbers: {a}, {b}")
                
                if choice == "1":
                    result = a + b
                    operation = "addition"
                elif choice == "2":
                    result = a - b
                    operation = "subtraction"
                elif choice == "3":
                    result = a * b
                    operation = "multiplication"
                elif choice == "4":
                    if b == 0:
                        print("Error: Division by zero!")
                        continue
                    result = a / b
                    operation = "division"
                
                print(f"Result of {operation}: {result}")
            else:
                print("Invalid choice. Please try again.")
    
    menu_driven_calculator()
    
    # 3. Batch processing with error handling
    def batch_process_files():
        """Simulate batch file processing."""
        print(f"\nBatch file processing simulation:")
        
        # Simulate file processing
        files = [
            {"name": "data1.csv", "size": 1000, "corrupted": False},
            {"name": "data2.csv", "size": 0, "corrupted": False},      # Empty file
            {"name": "data3.csv", "size": 2000, "corrupted": True},    # Corrupted
            {"name": "data4.csv", "size": 1500, "corrupted": False},
            {"name": "data5.csv", "size": 500, "corrupted": False},
        ]
        
        processed_count = 0
        error_count = 0
        total_size = 0
        
        for i, file_info in enumerate(files, 1):
            print(f"\nProcessing file {i}/{len(files)}: {file_info['name']}")
            
            try:
                # Check for empty files
                if file_info["size"] == 0:
                    print("  Warning: Empty file, skipping...")
                    continue
                
                # Check for corruption
                if file_info["corrupted"]:
                    raise ValueError("File is corrupted")
                
                # Simulate processing
                print(f"  Processing {file_info['size']} bytes...")
                processed_count += 1
                total_size += file_info["size"]
                print("  Success!")
                
            except ValueError as e:
                print(f"  Error: {e}")
                error_count += 1
                continue
            
            except Exception as e:
                print(f"  Unexpected error: {e}")
                error_count += 1
                continue
        
        print(f"\nBatch processing complete:")
        print(f"  Files processed: {processed_count}")
        print(f"  Errors encountered: {error_count}")
        print(f"  Total data processed: {total_size} bytes")
    
    batch_process_files()


# ============================================================================
# SECTION 7: ADVANCED PATTERNS
# ============================================================================

def advanced_control_patterns():
    """
    Demonstrate advanced control structure patterns.
    """
    print(f"\n=== ADVANCED CONTROL PATTERNS ===")
    
    # State machine pattern
    class SimpleStateMachine:
        def __init__(self):
            self.state = "idle"
            self.data = ""
        
        def process_input(self, input_char):
            if self.state == "idle":
                if input_char.isalpha():
                    self.state = "reading_word"
                    self.data = input_char
                elif input_char.isdigit():
                    self.state = "reading_number"
                    self.data = input_char
                # Ignore other characters in idle state
            
            elif self.state == "reading_word":
                if input_char.isalpha():
                    self.data += input_char
                else:
                    # Word complete
                    result = f"Word: {self.data}"
                    self._reset()
                    return result
            
            elif self.state == "reading_number":
                if input_char.isdigit():
                    self.data += input_char
                else:
                    # Number complete
                    result = f"Number: {self.data}"
                    self._reset()
                    return result
            
            return None
        
        def _reset(self):
            self.state = "idle"
            self.data = ""
    
    # Test state machine
    print("State machine pattern:")
    sm = SimpleStateMachine()
    test_input = "hello123world456!"
    
    for char in test_input:
        result = sm.process_input(char)
        if result:
            print(f"  {result}")
    
    # Final state
    if sm.state != "idle":
        if sm.state == "reading_word":
            print(f"  Final word: {sm.data}")
        elif sm.state == "reading_number":
            print(f"  Final number: {sm.data}")
    
    # Pipeline pattern
    def pipeline_processing():
        """Demonstrate pipeline pattern with generators."""
        print(f"\nPipeline processing pattern:")
        
        def data_source():
            """Generate raw data."""
            for i in range(20):
                yield f"item_{i}"
        
        def filter_stage(data_stream):
            """Filter items (keep only even indices)."""
            for i, item in enumerate(data_stream):
                if i % 2 == 0:
                    yield item
        
        def transform_stage(data_stream):
            """Transform items (uppercase)."""
            for item in data_stream:
                yield item.upper()
        
        def batch_stage(data_stream, batch_size=3):
            """Batch items into groups."""
            batch = []
            for item in data_stream:
                batch.append(item)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            
            # Yield remaining items
            if batch:
                yield batch
        
        # Build and execute pipeline
        pipeline = batch_stage(
            transform_stage(
                filter_stage(
                    data_source()
                )
            )
        )
        
        for batch_num, batch in enumerate(pipeline, 1):
            print(f"  Batch {batch_num}: {batch}")
    
    pipeline_processing()
    
    # Retry pattern with exponential backoff
    def retry_with_backoff():
        """Demonstrate retry pattern with exponential backoff."""
        print(f"\nRetry pattern with exponential backoff:")
        
        import time
        
        def unreliable_operation(attempt):
            """Simulate an unreliable operation."""
            # Fail first few attempts, succeed on later attempts
            if attempt < 3:
                raise ConnectionError(f"Connection failed on attempt {attempt}")
            return f"Success on attempt {attempt}"
        
        max_retries = 5
        base_delay = 0.1  # Start with 100ms delay
        
        for operation_id in range(1, 3):  # Try two operations
            print(f"\nOperation {operation_id}:")
            
            for attempt in range(1, max_retries + 1):
                try:
                    result = unreliable_operation(attempt)
                    print(f"  {result}")
                    break  # Success, exit retry loop
                
                except ConnectionError as e:
                    if attempt == max_retries:
                        print(f"  Final failure: {e}")
                        break
                    
                    # Calculate exponential backoff delay
                    delay = base_delay * (2 ** (attempt - 1))
                    print(f"  {e}, retrying in {delay:.3f}s...")
                    
                    # In real code, would use time.sleep(delay)
                    # For demo, we'll just show the delay calculation
    
    retry_with_backoff()


# ============================================================================
# SECTION 8: TESTING AND VALIDATION
# ============================================================================

def test_control_structures():
    """
    Test control structure implementations.
    """
    print(f"\n=== TESTING CONTROL STRUCTURES ===")
    
    # Test conditional logic
    def grade_calculator(score):
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    # Test cases for grading
    test_cases = [
        (95, 'A'),
        (85, 'B'),
        (75, 'C'),
        (65, 'D'),
        (55, 'F'),
        (100, 'A'),
        (0, 'F')
    ]
    
    print("Testing grade calculator:")
    for score, expected in test_cases:
        result = grade_calculator(score)
        status = "✅" if result == expected else "❌"
        print(f"  Score {score}: {result} {status}")
    
    # Test loop logic
    def factorial(n):
        if n < 0:
            return None
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    
    factorial_tests = [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
        (-1, None)
    ]
    
    print(f"\nTesting factorial function:")
    for n, expected in factorial_tests:
        result = factorial(n)
        status = "✅" if result == expected else "❌"
        print(f"  factorial({n}): {result} {status}")
    
    # Test comprehension equivalence
    def fibonacci_traditional(n):
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib
    
    def fibonacci_comprehension(n):
        if n <= 0:
            return []
        elif n == 1:
            return [0]
        
        fib = [0, 1]
        [fib.append(fib[-1] + fib[-2]) for _ in range(n-2)]
        return fib
    
    print(f"\nTesting Fibonacci implementations:")
    for n in [0, 1, 5, 10]:
        trad_result = fibonacci_traditional(n)
        comp_result = fibonacci_comprehension(n)
        match = trad_result == comp_result
        status = "✅" if match else "❌"
        print(f"  n={n}: traditional={len(trad_result)}, comprehension={len(comp_result)} {status}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function to run all control structure demonstrations.
    """
    print("Python Control Structures - Comprehensive Demonstration")
    print("=" * 60)
    
    try:
        # Run all demonstrations
        conditional_statements_demo()
        advanced_conditional_patterns()
        for_loop_demo()
        while_loop_demo()
        loop_control_demo()
        list_comprehensions_demo()
        other_comprehensions_demo()
        match_statements_demo()
        performance_analysis()
        real_world_applications()
        advanced_control_patterns()
        test_control_structures()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 60}")
        print("Control structures demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement FizzBuzz using different approaches:
   - Traditional if-elif-else
   - Dictionary dispatch
   - List comprehension

2. Create a number guessing game that:
   - Uses while loop for game continuation
   - Implements input validation
   - Tracks number of attempts

3. Build a text analyzer that uses:
   - Nested loops for character analysis
   - Dictionary comprehension for frequency counting
   - Generator expressions for memory efficiency

4. Implement pattern matching (or equivalent) for:
   - Command-line argument parsing
   - HTTP status code handling
   - File type processing

5. Create a data processing pipeline using:
   - Generator functions for each stage
   - Exception handling for errors
   - Progress tracking

6. Implement different sorting algorithms and compare:
   - Bubble sort (nested loops)
   - Selection sort (loop with min finding)
   - Quick sort (recursion + loops)

7. Build a simple state machine for:
   - String parsing
   - Game state management
   - Protocol handling

8. Create validation functions using:
   - Complex boolean expressions
   - Early return patterns
   - Comprehensive error messages

9. Implement search algorithms:
   - Linear search with early exit
   - Binary search with loop/recursion
   - Performance comparison

10. Build a menu system that handles:
    - Nested menus
    - Input validation
    - Error recovery

MUSCLE MEMORY DRILLS:

Practice these patterns daily:
- for item in collection:
- for i, item in enumerate(collection):
- for key, value in dict.items():
- while condition:
- if condition: ... elif condition: ... else: ...
- [expression for item in iterable if condition]
- {key: value for item in iterable}
- try: ... except Exception: ... finally: ...

PERFORMANCE TIPS:

1. Use list comprehensions over explicit loops when possible
2. Use generator expressions for large datasets
3. Prefer 'in' operator for membership testing
4. Use early returns to avoid deeply nested conditions
5. Consider dictionary dispatch for multiple conditions
6. Use enumerate() instead of range(len())
7. Break out of loops as early as possible
8. Use built-in functions like any(), all(), sum()
"""
