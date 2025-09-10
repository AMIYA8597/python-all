#!/usr/bin/env python3
"""
Python Standard Library - Core Modules Comprehensive Guide
==========================================================

This module demonstrates essential Python standard library modules with practical
examples, best practices, and real-world applications.

Core Modules Covered:
- os: Operating system interface
- sys: System-specific parameters and functions
- pathlib: Object-oriented filesystem paths
- datetime: Date and time handling
- json: JSON encoder and decoder
- csv: CSV file reading and writing
- re: Regular expressions
- collections: Specialized container datatypes
- itertools: Functions creating iterators
- functools: Higher-order functions and operations

Topics Covered:
- File system operations and path manipulation
- Date/time processing and formatting
- Data serialization (JSON, CSV)
- Text processing with regular expressions
- Advanced data structures from collections
- Functional programming utilities
- Performance optimization techniques
- Error handling and logging
- Cross-platform compatibility

Author: Python DSA Master Course
Version: 1.0
"""

import sys
import os
import pathlib
import datetime
import time
import json
import csv
import re
import collections
import itertools
import functools
import logging
import tempfile
from typing import List, Dict, Any, Optional, Tuple, Iterator
from dataclasses import dataclass, asdict
from enum import Enum
import traceback


# ============================================================================
# SECTION 1: OS AND SYSTEM MODULES
# ============================================================================

class SystemOperations:
    """Comprehensive system operations using os and sys modules."""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get comprehensive system information."""
        return {
            'platform': sys.platform,
            'python_version': sys.version,
            'python_version_info': sys.version_info,
            'executable': sys.executable,
            'current_working_directory': os.getcwd(),
            'user_home': os.path.expanduser('~'),
            'environment_variables_count': len(os.environ),
            'path_separator': os.sep,
            'line_separator': repr(os.linesep),
            'cpu_count': os.cpu_count(),
        }
    
    @staticmethod
    def environment_operations():
        """Demonstrate environment variable operations."""
        print("=== ENVIRONMENT VARIABLE OPERATIONS ===")
        
        # Get environment variable with default
        path = os.environ.get('PATH', 'Not found')
        print(f"PATH length: {len(path)} characters")
        
        # Set temporary environment variable
        test_var = 'PYTHON_DSA_TEST'
        os.environ[test_var] = 'test_value'
        print(f"Set {test_var}: {os.environ.get(test_var)}")
        
        # Remove environment variable
        if test_var in os.environ:
            del os.environ[test_var]
            print(f"Removed {test_var}: {os.environ.get(test_var, 'Not found')}")
        
        # Get all environment variables with specific prefix
        python_vars = {k: v for k, v in os.environ.items() if 'PYTHON' in k.upper()}
        print(f"Python-related environment variables: {len(python_vars)}")
        for var, value in list(python_vars.items())[:3]:  # Show first 3
            print(f"  {var}: {value[:50]}{'...' if len(value) > 50 else ''}")
    
    @staticmethod
    def file_system_operations():
        """Demonstrate file system operations."""
        print("\n=== FILE SYSTEM OPERATIONS ===")
        
        # Create temporary directory for demonstration
        temp_dir = tempfile.mkdtemp(prefix='python_dsa_')
        print(f"Created temporary directory: {temp_dir}")
        
        try:
            # File and directory operations
            test_file = os.path.join(temp_dir, 'test_file.txt')
            test_subdir = os.path.join(temp_dir, 'subdir')
            
            # Create file
            with open(test_file, 'w') as f:
                f.write("Hello, Python DSA Master!")
            print(f"Created file: {test_file}")
            
            # Create directory
            os.makedirs(test_subdir, exist_ok=True)
            print(f"Created directory: {test_subdir}")
            
            # File information
            stat_info = os.stat(test_file)
            print(f"File size: {stat_info.st_size} bytes")
            print(f"File modified: {datetime.datetime.fromtimestamp(stat_info.st_mtime)}")
            
            # List directory contents
            contents = os.listdir(temp_dir)
            print(f"Directory contents: {contents}")
            
            # Walk directory tree
            print("Directory tree:")
            for root, dirs, files in os.walk(temp_dir):
                level = root.replace(temp_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                sub_indent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{sub_indent}{file}")
        
        finally:
            # Clean up (in real code, use context managers or try/finally)
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Cleaned up temporary directory")


class PathLibOperations:
    """Modern path operations using pathlib."""
    
    @staticmethod
    def demonstrate_pathlib():
        """Demonstrate pathlib for modern path handling."""
        print("\n=== PATHLIB OPERATIONS ===")
        
        # Create Path objects
        current_dir = pathlib.Path.cwd()
        home_dir = pathlib.Path.home()
        
        print(f"Current directory: {current_dir}")
        print(f"Home directory: {home_dir}")
        
        # Path manipulation
        data_path = current_dir / "data" / "files" / "example.txt"
        print(f"Constructed path: {data_path}")
        print(f"Path parts: {data_path.parts}")
        print(f"Parent directory: {data_path.parent}")
        print(f"File name: {data_path.name}")
        print(f"File stem: {data_path.stem}")
        print(f"File suffix: {data_path.suffix}")
        
        # Path properties and methods
        print(f"Is absolute: {data_path.is_absolute()}")
        print(f"Exists: {data_path.exists()}")
        
        # Working with temporary files using pathlib
        temp_dir = pathlib.Path(tempfile.mkdtemp(prefix='pathlib_demo_'))
        try:
            # Create nested directories
            nested_path = temp_dir / "level1" / "level2" / "level3"
            nested_path.mkdir(parents=True, exist_ok=True)
            print(f"Created nested directories: {nested_path}")
            
            # Create files
            for i in range(3):
                file_path = nested_path / f"file_{i}.txt"
                file_path.write_text(f"Content of file {i}")
                print(f"Created: {file_path}")
            
            # Find files with glob patterns
            txt_files = list(temp_dir.glob("**/*.txt"))
            print(f"Found .txt files: {[f.name for f in txt_files]}")
            
            # File operations
            example_file = txt_files[0] if txt_files else None
            if example_file:
                content = example_file.read_text()
                print(f"File content: {content}")
                
                # File statistics
                stat = example_file.stat()
                print(f"File size: {stat.st_size} bytes")
                print(f"Modified: {datetime.datetime.fromtimestamp(stat.st_mtime)}")
        
        finally:
            # Cleanup
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


# ============================================================================
# SECTION 2: DATE AND TIME OPERATIONS
# ============================================================================

class DateTimeOperations:
    """Comprehensive date and time operations."""
    
    @staticmethod
    def demonstrate_datetime():
        """Demonstrate datetime module capabilities."""
        print("\n=== DATETIME OPERATIONS ===")
        
        try:
            # Current date and time
            now = datetime.datetime.now()
            utc_now = datetime.datetime.utcnow()
            
            print(f"Current local time: {now}")
            print(f"Current UTC time: {utc_now}")
            
            # Date and time components
            print(f"Year: {now.year}, Month: {now.month}, Day: {now.day}")
            print(f"Hour: {now.hour}, Minute: {now.minute}, Second: {now.second}")
            print(f"Weekday: {now.strftime('%A')} ({now.weekday()})")
            print(f"Day of year: {now.timetuple().tm_yday}")
            
            # Date arithmetic
            tomorrow = now + datetime.timedelta(days=1)
            last_week = now - datetime.timedelta(weeks=1)
            print(f"Tomorrow: {tomorrow.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Last week: {last_week.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Date formatting and parsing
            formatted_date = now.strftime("%B %d, %Y at %I:%M %p")
            print(f"Formatted: {formatted_date}")
            
            # Parse date string
            date_string = "2024-12-25 10:30:00"
            parsed_date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            print(f"Parsed date: {parsed_date}")
            
            # Time zones (basic demonstration)
            # Create timezone-aware datetime
            utc_tz = datetime.timezone.utc
            utc_dt = datetime.datetime.now(utc_tz)
            print(f"UTC datetime: {utc_dt}")
        
            # Time calculations
            start_time = time.time()
            time.sleep(0.1)  # Small delay for demonstration
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"Operation took: {elapsed:.3f} seconds")
            
        except Exception as e:
            print(f"Error in datetime operations: {e}")
    
    @staticmethod
    def date_utilities():
        """Useful date utility functions."""
        print("\n=== DATE UTILITIES ===")
        
        def get_age(birth_date: datetime.date) -> int:
            """Calculate age from birth date."""
            today = datetime.date.today()
            return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        def get_business_days(start_date: datetime.date, end_date: datetime.date) -> int:
            """Calculate business days between two dates."""
            current = start_date
            business_days = 0
            while current <= end_date:
                if current.weekday() < 5:  # Monday = 0, Sunday = 6
                    business_days += 1
                current += datetime.timedelta(days=1)
            return business_days
        
        def get_quarter(date: datetime.date) -> int:
            """Get quarter of the year (1-4)."""
            return (date.month - 1) // 3 + 1
        
        # Demonstrate utilities
        birth_date = datetime.date(1990, 5, 15)
        age = get_age(birth_date)
        print(f"Age for birth date {birth_date}: {age} years")
        
        start = datetime.date(2024, 1, 1)
        end = datetime.date(2024, 1, 31)
        business_days = get_business_days(start, end)
        print(f"Business days in January 2024: {business_days}")
        
        today = datetime.date.today()
        quarter = get_quarter(today)
        print(f"Current quarter: Q{quarter}")


# ============================================================================
# SECTION 3: DATA SERIALIZATION (JSON, CSV)
# ============================================================================

@dataclass
class Student:
    """Example data class for serialization."""
    name: str
    age: int
    grades: List[float]
    active: bool = True
    
    def average_grade(self) -> float:
        """Calculate average grade."""
        return sum(self.grades) / len(self.grades) if self.grades else 0.0


class DataSerialization:
    """Demonstrate JSON and CSV operations."""
    
    @staticmethod
    def demonstrate_json():
        """Demonstrate JSON operations."""
        print("\n=== JSON OPERATIONS ===")
        
        # Create sample data
        students = [
            Student("Alice Johnson", 20, [85.5, 92.0, 88.5]),
            Student("Bob Smith", 19, [78.0, 85.5, 90.0]),
            Student("Carol Davis", 21, [92.5, 89.0, 94.5])
        ]
        
        # Convert to JSON-serializable format
        students_dict = [asdict(student) for student in students]
        
        # Serialize to JSON
        json_string = json.dumps(students_dict, indent=2)
        print("JSON serialization:")
        print(json_string[:200] + "...")
        
        # Save to file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        try:
            with open(temp_file.name, 'w') as f:
                json.dump(students_dict, f, indent=2)
            print(f"Saved to file: {temp_file.name}")
            
            # Load from file
            with open(temp_file.name, 'r') as f:
                loaded_data = json.load(f)
            
            # Reconstruct objects
            loaded_students = [Student(**data) for data in loaded_data]
            print(f"Loaded {len(loaded_students)} students from JSON")
            
            for student in loaded_students:
                avg = student.average_grade()
                print(f"  {student.name}: Average grade {avg:.1f}")
        
        finally:
            try:
                temp_file.close()
                os.unlink(temp_file.name)
            except (PermissionError, FileNotFoundError):
                pass  # Ignore cleanup errors
    
    @staticmethod
    def demonstrate_csv():
        """Demonstrate CSV operations."""
        print("\n=== CSV OPERATIONS ===")
        
        # Sample data
        sales_data = [
            {'date': '2024-01-01', 'product': 'Laptop', 'quantity': 5, 'price': 999.99},
            {'date': '2024-01-01', 'product': 'Mouse', 'quantity': 20, 'price': 25.99},
            {'date': '2024-01-02', 'product': 'Keyboard', 'quantity': 15, 'price': 75.00},
            {'date': '2024-01-02', 'product': 'Monitor', 'quantity': 8, 'price': 299.99},
        ]
        
        # Write CSV file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
        try:
            with open(temp_file.name, 'w', newline='') as csvfile:
                fieldnames = ['date', 'product', 'quantity', 'price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(sales_data)
            
            print(f"Written CSV file: {temp_file.name}")
            
            # Read CSV file
            with open(temp_file.name, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                loaded_data = list(reader)
            
            print(f"Loaded {len(loaded_data)} records from CSV:")
            
            # Process data
            total_revenue = 0
            for row in loaded_data:
                quantity = int(row['quantity'])
                price = float(row['price'])
                revenue = quantity * price
                total_revenue += revenue
                print(f"  {row['date']}: {row['product']} - {quantity} × ${price} = ${revenue:.2f}")
            
            print(f"Total revenue: ${total_revenue:.2f}")
            
            # Write with custom formatting
            temp_file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
            with open(temp_file2.name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='|', quotechar='"')
                writer.writerow(['Product', 'Total Quantity', 'Average Price'])
                
                # Aggregate data
                products = {}
                for row in loaded_data:
                    product = row['product']
                    quantity = int(row['quantity'])
                    price = float(row['price'])
                    
                    if product in products:
                        products[product]['quantity'] += quantity
                        products[product]['prices'].append(price)
                    else:
                        products[product] = {'quantity': quantity, 'prices': [price]}
                
                for product, data in products.items():
                    avg_price = sum(data['prices']) / len(data['prices'])
                    writer.writerow([product, data['quantity'], f"${avg_price:.2f}"])
            
            print(f"Written aggregated CSV: {temp_file2.name}")
            
            # Display aggregated data
            with open(temp_file2.name, 'r') as csvfile:
                content = csvfile.read()
                print("Aggregated data:")
                print(content)
        
        finally:
            try:
                temp_file.close()
                os.unlink(temp_file.name)
            except (PermissionError, FileNotFoundError):
                pass
            try:
                temp_file2.close()
                os.unlink(temp_file2.name)
            except (PermissionError, FileNotFoundError):
                pass


# ============================================================================
# SECTION 4: REGULAR EXPRESSIONS
# ============================================================================

class RegularExpressions:
    """Comprehensive regular expression examples."""
    
    @staticmethod
    def demonstrate_regex():
        """Demonstrate regular expression operations."""
        print("\n=== REGULAR EXPRESSIONS ===")
        
        # Sample text data
        text_data = """
        Contact Information:
        John Doe - john.doe@email.com - Phone: (555) 123-4567
        Jane Smith - jane.smith@company.org - Phone: +1-555-987-6543
        Bob Johnson - bob@website.net - Phone: 555.456.7890
        Alice Brown - alice_brown@domain.co.uk - Mobile: (044) 20-1234-5678
        
        Dates in text: 2024-01-15, 03/25/2024, December 31, 2023
        URLs: https://www.example.com, http://test.org/page?id=123
        IP Addresses: 192.168.1.1, 10.0.0.255, 172.16.254.1
        """
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text_data)
        print(f"Found emails: {emails}")
        
        # Phone number extraction (multiple formats)
        phone_patterns = [
            r'\(\d{3}\)\s*\d{3}-\d{4}',  # (555) 123-4567
            r'\+?1?-?\d{3}[-.]?\d{3}[-.]?\d{4}',  # Various formats
            r'\(\d{3}\)\s*\d{2}-\d{4}-\d{4}'  # International
        ]
        
        all_phones = []
        for pattern in phone_patterns:
            phones = re.findall(pattern, text_data)
            all_phones.extend(phones)
        
        print(f"Found phone numbers: {all_phones}")
        
        # Date extraction (multiple formats)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'[A-Za-z]+ \d{1,2}, \d{4}'  # Month DD, YYYY
        ]
        
        all_dates = []
        for pattern in date_patterns:
            dates = re.findall(pattern, text_data)
            all_dates.extend(dates)
        
        print(f"Found dates: {all_dates}")
        
        # URL extraction
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text_data)
        print(f"Found URLs: {urls}")
        
        # IP address extraction
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ips = re.findall(ip_pattern, text_data)
        print(f"Found IP addresses: {ips}")
    
    @staticmethod
    def text_processing_examples():
        """Demonstrate text processing with regex."""
        print("\n=== TEXT PROCESSING WITH REGEX ===")
        
        # Sample messy text
        messy_text = """
        Hello!!!   This  is    a   MESSY   text with    lots of   
        extra    spaces and  multiple!!!   punctuation marks???
        
        Phone numbers: 123-456-7890, (555) 123 4567
        Emails: user@domain.com, admin@site.org
        """
        
        # Clean extra whitespace
        cleaned = re.sub(r'\s+', ' ', messy_text.strip())
        print(f"Cleaned whitespace:\n{cleaned}")
        
        # Remove excessive punctuation
        clean_punct = re.sub(r'[!?]{2,}', '!', cleaned)
        print(f"Cleaned punctuation:\n{clean_punct}")
        
        # Extract and format phone numbers
        phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
        
        def format_phone(match):
            # Remove all non-digits
            digits = re.sub(r'[^\d]', '', match.group(1))
            # Format as (XXX) XXX-XXXX
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        
        formatted_text = re.sub(phone_pattern, format_phone, clean_punct)
        print(f"Formatted phone numbers:\n{formatted_text}")
        
        # Validate and extract data with groups
        data_pattern = r'(\w+@[\w.-]+\.\w+)|(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
        matches = re.finditer(data_pattern, messy_text)
        
        print("Extracted data with categories:")
        for match in matches:
            if match.group(1):  # Email
                print(f"  Email: {match.group(1)}")
            elif match.group(2):  # Phone
                print(f"  Phone: {match.group(2)}")
    
    @staticmethod
    def validation_examples():
        """Demonstrate input validation with regex."""
        print("\n=== INPUT VALIDATION ===")
        
        validation_patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$',
            'zipcode': r'^\d{5}(-\d{4})?$',
            'ssn': r'^\d{3}-\d{2}-\d{4}$',
            'credit_card': r'^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$',
            'strong_password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        }
        
        test_data = {
            'email': ['user@domain.com', 'invalid-email', 'test@site.co.uk'],
            'phone': ['(555) 123-4567', '555.123.4567', '123-456', '555-123-4567'],
            'zipcode': ['12345', '12345-6789', '1234', '12345-67890'],
            'strong_password': ['Password123!', 'weak', 'NoSpecial123', 'NOLOWER123!']
        }
        
        for data_type, pattern in validation_patterns.items():
            if data_type in test_data:
                print(f"\n{data_type.upper()} validation:")
                compiled_pattern = re.compile(pattern)
                for test_value in test_data[data_type]:
                    is_valid = bool(compiled_pattern.match(test_value))
                    status = "✓" if is_valid else "✗"
                    print(f"  {status} {test_value}")


# ============================================================================
# SECTION 5: COLLECTIONS MODULE
# ============================================================================

class CollectionsExamples:
    """Demonstrate collections module specialized containers."""
    
    @staticmethod
    def demonstrate_collections():
        """Demonstrate collections module containers."""
        print("\n=== COLLECTIONS MODULE ===")
        
        # Counter - count occurrences
        text = "hello world this is a test hello world"
        word_count = collections.Counter(text.split())
        print(f"Word counts: {dict(word_count)}")
        print(f"Most common words: {word_count.most_common(3)}")
        
        # Counter arithmetic
        count1 = collections.Counter(['a', 'b', 'c', 'a'])
        count2 = collections.Counter(['a', 'b', 'b', 'd'])
        print(f"Counter 1: {dict(count1)}")
        print(f"Counter 2: {dict(count2)}")
        print(f"Sum: {dict(count1 + count2)}")
        print(f"Intersection: {dict(count1 & count2)}")
        
        # defaultdict - default values for missing keys
        dd = collections.defaultdict(list)
        
        # Group data by category
        data = [('fruit', 'apple'), ('vegetable', 'carrot'), 
                ('fruit', 'banana'), ('vegetable', 'broccoli')]
        
        for category, item in data:
            dd[category].append(item)
        
        print(f"Grouped data: {dict(dd)}")
        
        # defaultdict with different default types
        int_dd = collections.defaultdict(int)
        for char in "hello world":
            int_dd[char] += 1
        print(f"Character count: {dict(int_dd)}")
        
        # deque - double-ended queue
        dq = collections.deque(['center'])
        dq.appendleft('left')
        dq.append('right')
        print(f"Deque: {list(dq)}")
        
        # Rotating deque
        dq.rotate(1)
        print(f"After rotate(1): {list(dq)}")
        dq.rotate(-2)
        print(f"After rotate(-2): {list(dq)}")
        
        # Limited size deque
        limited_dq = collections.deque(maxlen=3)
        for i in range(5):
            limited_dq.append(i)
            print(f"Added {i}: {list(limited_dq)}")
        
        # namedtuple - named fields
        Point = collections.namedtuple('Point', ['x', 'y'])
        Student = collections.namedtuple('Student', ['name', 'age', 'grade'])
        
        p1 = Point(10, 20)
        s1 = Student('Alice', 20, 'A')
        
        print(f"Point: {p1}, x={p1.x}, y={p1.y}")
        print(f"Student: {s1.name}, age {s1.age}, grade {s1.grade}")
        
        # namedtuple methods
        print(f"Point fields: {p1._fields}")
        print(f"Point as dict: {p1._asdict()}")
        
        # ChainMap - combine multiple mappings
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'b': 3, 'c': 4}
        dict3 = {'c': 5, 'd': 6}
        
        chain = collections.ChainMap(dict1, dict2, dict3)
        print(f"ChainMap: {dict(chain)}")
        print(f"Key 'b' value: {chain['b']}")  # Returns first occurrence
        print(f"All mappings: {list(chain.maps)}")


# ============================================================================
# SECTION 6: ITERTOOLS MODULE
# ============================================================================

class ItertoolsExamples:
    """Demonstrate itertools for functional programming."""
    
    @staticmethod
    def demonstrate_itertools():
        """Demonstrate itertools functions."""
        print("\n=== ITERTOOLS MODULE ===")
        
        # Infinite iterators
        print("Infinite iterators (showing first 5):")
        
        # count - arithmetic progression
        counter = itertools.count(10, 2)  # Start at 10, step 2
        print(f"count(10, 2): {list(itertools.islice(counter, 5))}")
        
        # cycle - infinite repetition
        colors = itertools.cycle(['red', 'green', 'blue'])
        print(f"cycle colors: {list(itertools.islice(colors, 8))}")
        
        # repeat - repeat value
        repeated = itertools.repeat('hello', 3)
        print(f"repeat 'hello' 3 times: {list(repeated)}")
        
        # Iterators terminating on shortest input
        print("\nTerminating iterators:")
        
        # accumulate - cumulative results
        numbers = [1, 2, 3, 4, 5]
        cumsum = list(itertools.accumulate(numbers))
        print(f"accumulate sum: {cumsum}")
        
        cumproduct = list(itertools.accumulate(numbers, lambda x, y: x * y))
        print(f"accumulate product: {cumproduct}")
        
        # chain - flatten sequences
        list1 = [1, 2, 3]
        list2 = ['a', 'b', 'c']
        list3 = [10, 20]
        chained = list(itertools.chain(list1, list2, list3))
        print(f"chain multiple lists: {chained}")
        
        # compress - filter with boolean mask
        data = ['a', 'b', 'c', 'd', 'e']
        mask = [1, 0, 1, 0, 1]
        compressed = list(itertools.compress(data, mask))
        print(f"compress with mask: {compressed}")
        
        # dropwhile and takewhile
        numbers = [1, 3, 5, 8, 10, 12, 7, 9]
        dropped = list(itertools.dropwhile(lambda x: x < 8, numbers))
        print(f"dropwhile < 8: {dropped}")
        
        taken = list(itertools.takewhile(lambda x: x < 8, numbers))
        print(f"takewhile < 8: {taken}")
        
        # filterfalse - opposite of filter
        odds = list(itertools.filterfalse(lambda x: x % 2 == 0, numbers))
        print(f"filter odd numbers: {odds}")
        
        # groupby - group consecutive elements
        data = [1, 1, 2, 2, 2, 3, 1, 1]
        grouped = [(k, list(g)) for k, g in itertools.groupby(data)]
        print(f"groupby consecutive: {grouped}")
        
        # Combinatorial iterators
        print("\nCombinatorial iterators:")
        
        items = ['A', 'B', 'C', 'D']
        
        # product - Cartesian product
        product_result = list(itertools.product(items[:2], repeat=2))
        print(f"product AB with repeat=2: {product_result}")
        
        # permutations - r-length permutations
        perms = list(itertools.permutations(items[:3], 2))
        print(f"permutations of ABC, length 2: {perms}")
        
        # combinations - r-length combinations
        combs = list(itertools.combinations(items, 3))
        print(f"combinations of ABCD, length 3: {combs}")
        
        # combinations_with_replacement
        combs_repl = list(itertools.combinations_with_replacement(items[:2], 3))
        print(f"combinations with replacement AB, length 3: {combs_repl}")
    
    @staticmethod
    def practical_itertools_examples():
        """Practical examples using itertools."""
        print("\n=== PRACTICAL ITERTOOLS EXAMPLES ===")
        
        # Recipe: flatten nested list
        def flatten(nested_list):
            return itertools.chain.from_iterable(nested_list)
        
        nested = [[1, 2], [3, 4, 5], [6]]
        flattened = list(flatten(nested))
        print(f"Flatten nested list: {flattened}")
        
        # Recipe: pairwise (Python 3.10+ has this built-in)
        def pairwise(iterable):
            a, b = itertools.tee(iterable)
            next(b, None)
            return zip(a, b)
        
        data = [1, 2, 3, 4, 5]
        pairs = list(pairwise(data))
        print(f"Pairwise iteration: {pairs}")
        
        # Recipe: consume n items from iterator
        def consume(iterator, n):
            collections.deque(itertools.islice(iterator, n), maxlen=0)
        
        # Recipe: nth item
        def nth(iterable, n, default=None):
            return next(itertools.islice(iterable, n, None), default)
        
        numbers = range(100)
        tenth_item = nth(numbers, 10)
        print(f"10th item (0-indexed): {tenth_item}")
        
        # Recipe: chunk data
        def chunked(iterable, n):
            iterator = iter(iterable)
            while True:
                chunk = list(itertools.islice(iterator, n))
                if not chunk:
                    break
                yield chunk
        
        data = range(15)
        chunks = list(chunked(data, 4))
        print(f"Chunked data (size 4): {chunks}")
        
        # Recipe: roundrobin
        def roundrobin(*iterables):
            iterators = [iter(it) for it in iterables]
            while iterators:
                for i, it in enumerate(iterators):
                    try:
                        yield next(it)
                    except StopIteration:
                        iterators.pop(i)
                        break
        
        list1 = [1, 2, 3]
        list2 = ['a', 'b', 'c', 'd']
        list3 = [10, 20]
        roundrobin_result = list(roundrobin(list1, list2, list3))
        print(f"Round-robin: {roundrobin_result}")


# ============================================================================
# SECTION 7: FUNCTOOLS MODULE
# ============================================================================

class FunctoolsExamples:
    """Demonstrate functools for functional programming."""
    
    @staticmethod
    def demonstrate_functools():
        """Demonstrate functools functions."""
        print("\n=== FUNCTOOLS MODULE ===")
        
        # reduce - apply function cumulatively
        numbers = [1, 2, 3, 4, 5]
        sum_result = functools.reduce(lambda x, y: x + y, numbers)
        print(f"reduce sum: {sum_result}")
        
        product_result = functools.reduce(lambda x, y: x * y, numbers)
        print(f"reduce product: {product_result}")
        
        # partial - partial function application
        def multiply(x, y, z):
            return x * y * z
        
        double = functools.partial(multiply, 2)  # Fix first argument
        triple = functools.partial(multiply, 3)  # Fix first argument
        
        print(f"double(3, 4): {double(3, 4)}")  # 2 * 3 * 4 = 24
        print(f"triple(2, 5): {triple(2, 5)}")  # 3 * 2 * 5 = 30
        
        # partialmethod - method version of partial
        class Calculator:
            def __init__(self, base=0):
                self.base = base
            
            def add(self, x, y):
                return self.base + x + y
            
            # Create specialized methods
            add_ten = functools.partialmethod(add, 10)
            add_hundred = functools.partialmethod(add, 100)
        
        calc = Calculator(5)
        print(f"add_ten(3): {calc.add_ten(3)}")  # 5 + 10 + 3 = 18
        print(f"add_hundred(2): {calc.add_hundred(2)}")  # 5 + 100 + 2 = 107
        
        # wraps - preserve function metadata in decorators
        def my_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"Calling {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        
        @my_decorator
        def greet(name):
            """Greet a person by name."""
            return f"Hello, {name}!"
        
        print(f"Function name: {greet.__name__}")
        print(f"Function doc: {greet.__doc__}")
        print(f"Result: {greet('Alice')}")
        
        # lru_cache - least recently used cache
        @functools.lru_cache(maxsize=128)
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        # Time fibonacci calculation
        import time
        start = time.time()
        result = fibonacci(35)
        cached_time = time.time() - start
        
        print(f"fibonacci(35) = {result}")
        print(f"Cached calculation time: {cached_time:.4f} seconds")
        print(f"Cache info: {fibonacci.cache_info()}")
        
        # singledispatch - function overloading
        @functools.singledispatch
        def process_data(arg):
            print(f"Processing unknown type: {type(arg).__name__}")
        
        @process_data.register
        def _(arg: int):
            print(f"Processing integer: {arg}")
            return arg * 2
        
        @process_data.register
        def _(arg: str):
            print(f"Processing string: {arg}")
            return arg.upper()
        
        @process_data.register
        def _(arg: list):
            print(f"Processing list: {arg}")
            return len(arg)
        
        # Test single dispatch
        print("\nSingle dispatch examples:")
        process_data(42)
        process_data("hello")
        process_data([1, 2, 3, 4])
        process_data(3.14)


# ============================================================================
# SECTION 8: LOGGING MODULE
# ============================================================================

class LoggingExamples:
    """Demonstrate logging module for application logging."""
    
    @staticmethod
    def demonstrate_logging():
        """Demonstrate logging configuration and usage."""
        print("\n=== LOGGING MODULE ===")
        
        # Basic logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create logger
        logger = logging.getLogger('PythonDSAExample')
        
        # Different log levels
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        
        # Logging with variables
        user = "Alice"
        action = "login"
        logger.info(f"User {user} performed {action}")
        
        # Logging exceptions
        try:
            result = 1 / 0
        except ZeroDivisionError:
            logger.exception("Division by zero error occurred")
        
        # Custom logger with file handler
        file_logger = logging.getLogger('FileLogger')
        file_logger.setLevel(logging.DEBUG)
        
        # Create temp log file
        temp_log = tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False)
        try:
            # File handler
            file_handler = logging.FileHandler(temp_log.name)
            file_handler.setLevel(logging.DEBUG)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers to logger
            file_logger.addHandler(file_handler)
            file_logger.addHandler(console_handler)
            
            # Test logging
            file_logger.debug("Debug message (only in file)")
            file_logger.info("Info message (only in file)")
            file_logger.warning("Warning message (file and console)")
            file_logger.error("Error message (file and console)")
            
            # Read and display log file
            with open(temp_log.name, 'r') as f:
                log_content = f.read()
                print(f"\nLog file contents:")
                print(log_content)
        
        finally:
            # Cleanup handlers
            for handler in file_logger.handlers[:]:
                handler.close()
                file_logger.removeHandler(handler)
            
            try:
                temp_log.close()
                os.unlink(temp_log.name)
            except (PermissionError, FileNotFoundError):
                pass  # Ignore cleanup errors


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Python Standard Library - Core Modules Comprehensive Guide")
    print("=" * 70)
    
    try:
        # System operations
        sys_ops = SystemOperations()
        info = sys_ops.get_system_info()
        print("=== SYSTEM INFORMATION ===")
        for key, value in info.items():
            print(f"{key}: {value}")
        
        sys_ops.environment_operations()
        sys_ops.file_system_operations()
        
        # Path operations
        PathLibOperations.demonstrate_pathlib()
        
        # Date and time
        DateTimeOperations.demonstrate_datetime()
        DateTimeOperations.date_utilities()
        
        # Data serialization
        DataSerialization.demonstrate_json()
        DataSerialization.demonstrate_csv()
        
        # Regular expressions
        RegularExpressions.demonstrate_regex()
        RegularExpressions.text_processing_examples()
        RegularExpressions.validation_examples()
        
        # Collections
        CollectionsExamples.demonstrate_collections()
        
        # Itertools
        ItertoolsExamples.demonstrate_itertools()
        ItertoolsExamples.practical_itertools_examples()
        
        # Functools
        FunctoolsExamples.demonstrate_functools()
        
        # Logging
        LoggingExamples.demonstrate_logging()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 70}")
        print("Python Standard Library demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Build a file organizer using os and pathlib that sorts files by extension.

2. Create a log analyzer that processes server log files using regex.

3. Implement a data pipeline using itertools for processing large datasets.

4. Build a configuration manager using JSON and validation with regex.

5. Create a backup utility using datetime for timestamping and pathlib for file operations.

6. Implement a word frequency analyzer using collections.Counter and CSV output.

7. Build a caching decorator using functools that persists to disk.

8. Create a data validator using multiple regex patterns and collections.

9. Implement a file watcher using os that logs changes with proper logging.

10. Build a CSV data processor that handles multiple formats and exports to JSON.

ADVANCED CHALLENGES:

1. Create a distributed logging system with multiple handlers
2. Build a data serialization system supporting multiple formats
3. Implement a file sync utility with conflict resolution
4. Create a regex-based template engine
5. Build a functional programming library using itertools and functools
6. Implement a configuration system with environment variable support
7. Create a data migration tool between different formats
8. Build a text processing pipeline with pluggable components
9. Implement a cache invalidation system with datetime-based expiry
10. Create a cross-platform system monitoring tool

SYSTEM APPLICATIONS:

1. Log management and analysis systems
2. Data ETL (Extract, Transform, Load) pipelines
3. Configuration management tools
4. File processing and organization systems
5. System monitoring and alerting tools
"""
