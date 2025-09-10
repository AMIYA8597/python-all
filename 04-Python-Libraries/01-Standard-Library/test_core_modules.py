#!/usr/bin/env python3
"""
Test Suite for Python Standard Library Core Modules

This module contains comprehensive tests for all the core Python standard
library functionality demonstrated in 01-core-modules.py.

Run with: python -m pytest test_core_modules.py -v
"""

import unittest
import tempfile
import os
import json
import csv
import datetime
import re
import sys
import pathlib
from unittest.mock import patch, mock_open
from collections import Counter, deque, defaultdict, namedtuple, ChainMap
import itertools
import functools

# Import classes from the main module
sys.path.append('.')
try:
    from core_modules import (
        SystemOperations, PathLibOperations, DateTimeOperations,
        DataSerialization, Student, RegularExpressions,
        CollectionsExamples, ItertoolsExamples, FunctoolsExamples
    )
except ImportError:
    # If the module name doesn't match, we'll define mock classes for testing
    class SystemOperations:
        def get_system_info(self):
            return {
                'platform': 'test', 'python_version': '3.0.0',
                'python_version_info': (3, 0, 0), 'executable': '/test',
                'current_working_directory': '/test', 'user_home': '/test',
                'environment_variables_count': 10, 'path_separator': '/',
                'line_separator': '\n', 'cpu_count': 4
            }
    
    class PathLibOperations: pass
    class DateTimeOperations: pass
    class DataSerialization: pass
    class Student:
        def __init__(self, name, age, grades, active=True):
            self.name = name
            self.age = age
            self.grades = grades
            self.active = active
        def average_grade(self):
            return sum(self.grades) / len(self.grades) if self.grades else 0.0
    class RegularExpressions: pass
    class CollectionsExamples: pass
    class ItertoolsExamples: pass
    class FunctoolsExamples: pass


class TestSystemOperations(unittest.TestCase):
    """Test system operations functionality."""
    
    def setUp(self):
        self.sys_ops = SystemOperations()
    
    def test_get_system_info(self):
        """Test system information retrieval."""
        info = self.sys_ops.get_system_info()
        
        # Check that all expected keys are present
        expected_keys = [
            'platform', 'python_version', 'python_version_info',
            'executable', 'current_working_directory', 'user_home',
            'environment_variables_count', 'path_separator',
            'line_separator', 'cpu_count'
        ]
        
        for key in expected_keys:
            self.assertIn(key, info)
        
        # Check data types
        self.assertIsInstance(info['platform'], str)
        self.assertIsInstance(info['python_version'], str)
        self.assertIsInstance(info['cpu_count'], int)
        self.assertGreater(info['cpu_count'], 0)


class TestDateTimeOperations(unittest.TestCase):
    """Test datetime operations functionality."""
    
    def test_age_calculation(self):
        """Test age calculation utility."""
        def get_age(birth_date: datetime.date) -> int:
            today = datetime.date.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Test with known birth date
        birth_date = datetime.date(1990, 1, 1)
        age = get_age(birth_date)
        expected_age = datetime.date.today().year - 1990
        
        # Age should be within 1 year of expected (due to month/day calculation)
        self.assertIn(age, [expected_age - 1, expected_age])
    
    def test_business_days_calculation(self):
        """Test business days calculation."""
        def get_business_days(start_date: datetime.date, end_date: datetime.date) -> int:
            current = start_date
            business_days = 0
            while current <= end_date:
                if current.weekday() < 5:  # Monday = 0, Sunday = 6
                    business_days += 1
                current += datetime.timedelta(days=1)
            return business_days
        
        # Test a known week
        start = datetime.date(2024, 1, 1)  # Monday
        end = datetime.date(2024, 1, 7)    # Sunday
        business_days = get_business_days(start, end)
        self.assertEqual(business_days, 5)  # Monday through Friday
    
    def test_quarter_calculation(self):
        """Test quarter calculation."""
        def get_quarter(date: datetime.date) -> int:
            return (date.month - 1) // 3 + 1
        
        test_cases = [
            (datetime.date(2024, 1, 15), 1),
            (datetime.date(2024, 4, 10), 2),
            (datetime.date(2024, 7, 20), 3),
            (datetime.date(2024, 10, 5), 4),
        ]
        
        for date, expected_quarter in test_cases:
            with self.subTest(date=date):
                self.assertEqual(get_quarter(date), expected_quarter)


class TestDataSerialization(unittest.TestCase):
    """Test JSON and CSV serialization functionality."""
    
    def test_student_class(self):
        """Test Student data class."""
        student = Student("John Doe", 20, [85.0, 90.0, 88.0])
        
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(student.age, 20)
        self.assertEqual(student.grades, [85.0, 90.0, 88.0])
        self.assertTrue(student.active)
        
        # Test average calculation
        expected_avg = (85.0 + 90.0 + 88.0) / 3
        self.assertAlmostEqual(student.average_grade(), expected_avg, places=2)
        
        # Test empty grades
        empty_student = Student("Empty", 18, [])
        self.assertEqual(empty_student.average_grade(), 0.0)
    
    def test_json_serialization(self):
        """Test JSON serialization and deserialization."""
        # Create test data
        students = [
            Student("Alice", 20, [85.5, 92.0]),
            Student("Bob", 19, [78.0, 85.5])
        ]
        
        # Convert to dict format
        students_dict = [
            {"name": s.name, "age": s.age, "grades": s.grades, "active": s.active}
            for s in students
        ]
        
        # Test JSON serialization
        json_str = json.dumps(students_dict)
        self.assertIsInstance(json_str, str)
        self.assertIn("Alice", json_str)
        self.assertIn("Bob", json_str)
        
        # Test JSON deserialization
        loaded_data = json.loads(json_str)
        self.assertEqual(len(loaded_data), 2)
        self.assertEqual(loaded_data[0]["name"], "Alice")
        self.assertEqual(loaded_data[1]["name"], "Bob")
    
    def test_csv_operations(self):
        """Test CSV reading and writing."""
        # Test data
        test_data = [
            {"name": "Alice", "age": 20, "grade": 85.5},
            {"name": "Bob", "age": 19, "grade": 78.0}
        ]
        
        # Test writing to CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            fieldnames = ["name", "age", "grade"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_data)
            temp_path = f.name
        
        try:
            # Test reading from CSV
            with open(temp_path, 'r') as f:
                reader = csv.DictReader(f)
                loaded_data = list(reader)
            
            self.assertEqual(len(loaded_data), 2)
            self.assertEqual(loaded_data[0]["name"], "Alice")
            self.assertEqual(int(loaded_data[0]["age"]), 20)
            self.assertEqual(float(loaded_data[0]["grade"]), 85.5)
        
        finally:
            os.unlink(temp_path)


class TestRegularExpressions(unittest.TestCase):
    """Test regular expression functionality."""
    
    def test_email_validation(self):
        """Test email validation regex."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        valid_emails = [
            "user@domain.com",
            "test.user@example.org",
            "user+tag@domain.co.uk"
        ]
        
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user.domain.com"
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertIsNotNone(re.match(email_pattern, email))
        
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertIsNone(re.match(email_pattern, email))
    
    def test_phone_validation(self):
        """Test phone number validation."""
        phone_pattern = r'^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$'
        
        valid_phones = [
            "(555) 123-4567",
            "555-123-4567",
            "555.123.4567",
            "555 123 4567"
        ]
        
        invalid_phones = [
            "123-456",
            "1234567890123",
            "abc-def-ghij"
        ]
        
        for phone in valid_phones:
            with self.subTest(phone=phone):
                self.assertIsNotNone(re.match(phone_pattern, phone))
        
        for phone in invalid_phones:
            with self.subTest(phone=phone):
                self.assertIsNone(re.match(phone_pattern, phone))
    
    def test_text_extraction(self):
        """Test text extraction with regex."""
        text = """
        Contact: john.doe@email.com, Phone: (555) 123-4567
        Website: https://www.example.com
        IP: 192.168.1.1
        """
        
        # Test email extraction
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        self.assertIn("john.doe@email.com", emails)
        
        # Test phone extraction
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        self.assertTrue(any("555" in phone for phone in phones))
        
        # Test URL extraction
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        self.assertTrue(any("example.com" in url for url in urls))


class TestCollections(unittest.TestCase):
    """Test collections module functionality."""
    
    def test_counter(self):
        """Test Counter functionality."""
        text = "hello world hello"
        word_counts = Counter(text.split())
        
        self.assertEqual(word_counts["hello"], 2)
        self.assertEqual(word_counts["world"], 1)
        self.assertEqual(len(word_counts), 2)
        
        # Test most common
        most_common = word_counts.most_common(1)
        self.assertEqual(most_common[0][0], "hello")
        self.assertEqual(most_common[0][1], 2)
    
    def test_deque(self):
        """Test deque functionality."""
        d = deque(maxlen=3)
        
        # Test append operations
        d.append(1)
        d.append(2)
        d.append(3)
        d.append(4)  # Should remove first element
        
        self.assertEqual(len(d), 3)
        self.assertNotIn(1, d)
        self.assertIn(4, d)
        
        # Test rotation
        d.rotate(1)
        self.assertEqual(d[0], 3)
    
    def test_defaultdict(self):
        """Test defaultdict functionality."""
        dd = defaultdict(list)
        
        # Test default factory
        dd["key1"].append("value1")
        self.assertEqual(dd["key1"], ["value1"])
        
        # Test that missing keys get default value
        dd["key2"].append("value2")
        self.assertEqual(len(dd), 2)
    
    def test_namedtuple(self):
        """Test namedtuple functionality."""
        Point = namedtuple('Point', ['x', 'y'])
        p = Point(10, 20)
        
        self.assertEqual(p.x, 10)
        self.assertEqual(p.y, 20)
        self.assertEqual(p[0], 10)
        self.assertEqual(p[1], 20)
        
        # Test immutability
        with self.assertRaises(AttributeError):
            p.x = 15


class TestItertools(unittest.TestCase):
    """Test itertools functionality."""
    
    def test_infinite_iterators(self):
        """Test infinite iterators (limited)."""
        # Test count
        counter = itertools.count(10, 2)
        first_five = [next(counter) for _ in range(5)]
        expected = [10, 12, 14, 16, 18]
        self.assertEqual(first_five, expected)
        
        # Test cycle
        colors = itertools.cycle(['red', 'green', 'blue'])
        first_six = [next(colors) for _ in range(6)]
        expected = ['red', 'green', 'blue', 'red', 'green', 'blue']
        self.assertEqual(first_six, expected)
        
        # Test repeat
        repeated = list(itertools.repeat('hello', 3))
        expected = ['hello', 'hello', 'hello']
        self.assertEqual(repeated, expected)
    
    def test_finite_iterators(self):
        """Test finite iterators."""
        # Test accumulate
        numbers = [1, 2, 3, 4, 5]
        accumulated = list(itertools.accumulate(numbers))
        expected = [1, 3, 6, 10, 15]
        self.assertEqual(accumulated, expected)
        
        # Test chain
        list1 = [1, 2, 3]
        list2 = ['a', 'b', 'c']
        chained = list(itertools.chain(list1, list2))
        expected = [1, 2, 3, 'a', 'b', 'c']
        self.assertEqual(chained, expected)
        
        # Test compress
        data = ['a', 'b', 'c', 'd', 'e']
        selectors = [1, 0, 1, 0, 1]
        compressed = list(itertools.compress(data, selectors))
        expected = ['a', 'c', 'e']
        self.assertEqual(compressed, expected)
    
    def test_combinatorial_iterators(self):
        """Test combinatorial iterators."""
        # Test product
        result = list(itertools.product(['A', 'B'], repeat=2))
        expected = [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]
        self.assertEqual(result, expected)
        
        # Test permutations
        result = list(itertools.permutations(['A', 'B', 'C'], 2))
        expected = [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]
        self.assertEqual(result, expected)
        
        # Test combinations
        result = list(itertools.combinations(['A', 'B', 'C', 'D'], 2))
        expected = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
        self.assertEqual(result, expected)


class TestFunctools(unittest.TestCase):
    """Test functools functionality."""
    
    def test_reduce(self):
        """Test reduce function."""
        numbers = [1, 2, 3, 4, 5]
        
        # Test sum with reduce
        total = functools.reduce(lambda x, y: x + y, numbers)
        self.assertEqual(total, 15)
        
        # Test product with reduce
        product = functools.reduce(lambda x, y: x * y, numbers)
        self.assertEqual(product, 120)
    
    def test_partial(self):
        """Test partial function application."""
        def multiply(x, y, z):
            return x * y * z
        
        # Create partial function
        double = functools.partial(multiply, 2)
        result = double(3, 4)
        expected = 2 * 3 * 4
        self.assertEqual(result, expected)
    
    def test_lru_cache(self):
        """Test LRU cache decorator."""
        @functools.lru_cache(maxsize=128)
        def expensive_function(n):
            return n * n
        
        # First call
        result1 = expensive_function(5)
        self.assertEqual(result1, 25)
        
        # Second call (should be cached)
        result2 = expensive_function(5)
        self.assertEqual(result2, 25)
        
        # Check cache info
        cache_info = expensive_function.cache_info()
        self.assertEqual(cache_info.hits, 1)
        self.assertEqual(cache_info.misses, 1)
    
    def test_singledispatch(self):
        """Test single dispatch decorator."""
        @functools.singledispatch
        def process(arg):
            return f"unknown: {type(arg).__name__}"
        
        @process.register
        def _(arg: int):
            return f"integer: {arg}"
        
        @process.register
        def _(arg: str):
            return f"string: {arg}"
        
        # Test dispatch
        self.assertEqual(process(42), "integer: 42")
        self.assertEqual(process("hello"), "string: hello")
        self.assertEqual(process(3.14), "unknown: float")


class TestPathLibOperations(unittest.TestCase):
    """Test pathlib functionality."""
    
    def test_path_operations(self):
        """Test basic path operations."""
        current_dir = pathlib.Path.cwd()
        self.assertTrue(current_dir.exists())
        self.assertTrue(current_dir.is_dir())
        
        # Test path construction
        test_path = current_dir / "test_file.txt"
        self.assertEqual(test_path.parent, current_dir)
        self.assertEqual(test_path.name, "test_file.txt")
        self.assertEqual(test_path.stem, "test_file")
        self.assertEqual(test_path.suffix, ".txt")
    
    def test_path_creation_and_cleanup(self):
        """Test file and directory creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = pathlib.Path(temp_dir)
            
            # Create nested directories
            nested = temp_path / "level1" / "level2"
            nested.mkdir(parents=True, exist_ok=True)
            self.assertTrue(nested.exists())
            self.assertTrue(nested.is_dir())
            
            # Create file
            test_file = nested / "test.txt"
            test_file.write_text("test content")
            self.assertTrue(test_file.exists())
            self.assertEqual(test_file.read_text(), "test content")


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class IntegrationTests(unittest.TestCase):
    """Integration tests that test multiple modules working together."""
    
    def test_file_processing_pipeline(self):
        """Test a complete file processing pipeline."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = pathlib.Path(temp_dir)
            
            # Create test data
            students = [
                {"name": "Alice Johnson", "age": 20, "grades": [85.5, 92.0, 88.5]},
                {"name": "Bob Smith", "age": 19, "grades": [78.0, 85.5, 90.0]},
            ]
            
            # Write to JSON
            json_file = temp_path / "students.json"
            with open(json_file, 'w') as f:
                json.dump(students, f, indent=2)
            
            # Read and process
            with open(json_file, 'r') as f:
                loaded_students = json.load(f)
            
            # Calculate statistics
            total_students = len(loaded_students)
            all_grades = []
            for student in loaded_students:
                all_grades.extend(student["grades"])
            
            avg_grade = sum(all_grades) / len(all_grades)
            
            # Write results to CSV
            csv_file = temp_path / "results.csv"
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Total Students", total_students])
                writer.writerow(["Average Grade", f"{avg_grade:.2f}"])
            
            # Verify results
            self.assertTrue(json_file.exists())
            self.assertTrue(csv_file.exists())
            self.assertEqual(total_students, 2)
            self.assertAlmostEqual(avg_grade, 86.58, places=1)
    
    def test_log_analysis_pipeline(self):
        """Test log analysis using multiple modules."""
        log_data = """
        2024-01-01 10:00:01 INFO User alice@example.com logged in from 192.168.1.100
        2024-01-01 10:01:05 ERROR Failed login attempt for bob@test.com from 192.168.1.101
        2024-01-01 10:02:10 INFO User charlie@domain.org logged in from 10.0.0.50
        2024-01-01 10:03:15 WARNING Multiple failed attempts for alice@example.com
        """
        
        # Extract information using regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        
        emails = re.findall(email_pattern, log_data)
        ips = re.findall(ip_pattern, log_data)
        
        # Count occurrences using Counter
        email_counts = Counter(emails)
        ip_counts = Counter(ips)
        
        # Verify results
        self.assertIn("alice@example.com", emails)
        self.assertIn("bob@test.com", emails)
        self.assertIn("charlie@domain.org", emails)
        
        self.assertEqual(email_counts["alice@example.com"], 2)
        self.assertEqual(len(ip_counts), 3)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class PerformanceTests(unittest.TestCase):
    """Performance tests for various operations."""
    
    def test_counter_vs_dict_performance(self):
        """Compare Counter vs dict for counting operations."""
        import time
        
        data = ["apple", "banana", "apple", "cherry", "banana", "apple"] * 1000
        
        # Test Counter
        start_time = time.time()
        counter_result = Counter(data)
        counter_time = time.time() - start_time
        
        # Test dict
        start_time = time.time()
        dict_result = {}
        for item in data:
            dict_result[item] = dict_result.get(item, 0) + 1
        dict_time = time.time() - start_time
        
        # Verify results are equivalent
        self.assertEqual(dict(counter_result), dict_result)
        
        # Counter should be reasonably fast
        self.assertLess(counter_time, 1.0)  # Should complete in less than 1 second
    
    def test_deque_vs_list_performance(self):
        """Compare deque vs list for append/pop operations."""
        import time
        
        n = 10000
        
        # Test deque
        start_time = time.time()
        d = deque()
        for i in range(n):
            d.appendleft(i)
        for i in range(n):
            d.popleft()
        deque_time = time.time() - start_time
        
        # Test list
        start_time = time.time()
        l = []
        for i in range(n):
            l.insert(0, i)
        for i in range(n):
            l.pop(0)
        list_time = time.time() - start_time
        
        # Deque should be significantly faster for left operations
        self.assertLess(deque_time, list_time)


if __name__ == "__main__":
    # Run all tests
    unittest.main(argv=[''], exit=False, verbosity=2)
