# Python Standard Library - Core Modules

This module provides comprehensive demonstrations and practical examples of Python's most essential standard library modules. It's designed to help developers master the core libraries that form the foundation of Python programming.

## 📁 Module Structure

```
01-Standard-Library/
├── README.md                    # This comprehensive guide
├── 01-core-modules.py          # Complete implementation with examples
├── test_core_modules.py        # Comprehensive test suite
└── __init__.py                 # Module initialization (if needed)
```

## 🎯 Learning Objectives

After completing this module, you will be able to:

- **System Operations**: Interact with the operating system, manage files, handle environment variables
- **Path Management**: Use modern path operations with pathlib for cross-platform compatibility
- **Date & Time**: Handle datetime operations, timezone management, and date calculations
- **Data Serialization**: Work with JSON and CSV for data exchange and storage
- **Text Processing**: Master regular expressions for pattern matching and validation
- **Advanced Collections**: Utilize specialized data structures from collections module
- **Functional Programming**: Apply itertools and functools for efficient data processing
- **Application Logging**: Implement proper logging practices for debugging and monitoring

## 📚 Covered Modules

### 1. System Operations (os, sys)
- **System Information**: Platform details, Python version, environment variables
- **File Operations**: Create, read, modify, and delete files and directories
- **Environment Management**: Get, set, and manipulate environment variables
- **Process Management**: Execute system commands and handle process information

### 2. Path Operations (pathlib)
- **Modern Path Handling**: Cross-platform path operations using pathlib
- **File System Navigation**: Directory traversal, file discovery, and path construction
- **File Properties**: Size, modification times, permissions, and metadata
- **Path Manipulation**: Joining, resolving, and normalizing paths

### 3. Date and Time (datetime, time)
- **Current Time**: Local time, UTC time, and timezone-aware operations
- **Date Arithmetic**: Adding/subtracting time periods, calculating differences
- **Formatting**: Convert between strings and datetime objects
- **Utility Functions**: Age calculation, business days, quarters, and time zones

### 4. Data Serialization (json, csv)
- **JSON Operations**: Serialize/deserialize Python objects to/from JSON
- **CSV Processing**: Read and write CSV files with various formats and delimiters
- **Data Validation**: Ensure data integrity during serialization/deserialization
- **Real-world Examples**: Configuration files, data export/import, API responses

### 5. Regular Expressions (re)
- **Pattern Matching**: Find, extract, and validate text patterns
- **Text Processing**: Clean, format, and transform text data
- **Input Validation**: Email, phone, URL, and password validation
- **Data Extraction**: Parse log files, extract structured data from text

### 6. Collections (collections)
- **Counter**: Count hashable objects efficiently
- **deque**: Double-ended queue for efficient append/pop operations
- **defaultdict**: Dictionary with default values for missing keys
- **namedtuple**: Lightweight object types with named fields
- **ChainMap**: Combine multiple dictionaries into a single view

### 7. Itertools (itertools)
- **Infinite Iterators**: count, cycle, repeat for generating sequences
- **Finite Iterators**: accumulate, chain, compress for data transformation
- **Combinatorial Iterators**: product, permutations, combinations for mathematical operations
- **Practical Applications**: Data chunking, pairwise iteration, flattening

### 8. Functional Programming (functools)
- **Function Composition**: reduce, partial for building complex functions from simple ones
- **Caching**: lru_cache for memoization and performance optimization
- **Decorators**: wraps for preserving function metadata
- **Single Dispatch**: Function overloading based on argument types

### 9. Logging (logging)
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Formatters**: Custom log message formatting
- **Handlers**: Console, file, and custom output destinations
- **Best Practices**: Structured logging, log rotation, performance considerations

## 🚀 Quick Start

### Running the Main Demonstration

```bash
# Navigate to the Standard Library directory
cd 04-Python-Libraries/01-Standard-Library

# Run the complete demonstration
python 01-core-modules.py
```

### Running Specific Sections

The main script is organized into sections. You can modify the `main()` function to run specific demonstrations:

```python
def main():
    # Run only datetime operations
    DateTimeOperations.demonstrate_datetime()
    DateTimeOperations.date_utilities()
    
    # Run only collections examples
    CollectionsExamples.demonstrate_collections()
```

### Running Tests

```bash
# Run all tests
python test_core_modules.py

# Run specific test class
python test_core_modules.py TestDateTimeOperations

# Run specific test method
python test_core_modules.py TestDataSerialization.test_json_serialization

# Run with verbose output
python test_core_modules.py -v
```

## 💡 Practical Examples

### File Organization Script
```python
import pathlib
from collections import defaultdict

def organize_files_by_extension(directory):
    """Organize files in a directory by their extensions."""
    base_path = pathlib.Path(directory)
    files_by_ext = defaultdict(list)
    
    for file_path in base_path.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower() or '.no_extension'
            files_by_ext[ext].append(file_path)
    
    return files_by_ext

# Usage
organized = organize_files_by_extension('/path/to/directory')
for ext, files in organized.items():
    print(f"{ext}: {len(files)} files")
```

### Log Analysis Tool
```python
import re
from collections import Counter
from datetime import datetime

def analyze_web_logs(log_file):
    """Analyze web server logs for insights."""
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    status_pattern = r' (\d{3}) '
    
    ips = Counter()
    status_codes = Counter()
    
    with open(log_file) as f:
        for line in f:
            # Extract IP addresses
            ip_match = re.search(ip_pattern, line)
            if ip_match:
                ips[ip_match.group()] += 1
            
            # Extract status codes
            status_match = re.search(status_pattern, line)
            if status_match:
                status_codes[status_match.group(1)] += 1
    
    return ips.most_common(10), status_codes.most_common()
```

### Data Processing Pipeline
```python
import json
import csv
import itertools
from functools import reduce

def process_sales_data(json_file, output_csv):
    """Process sales data and generate summary report."""
    # Load data
    with open(json_file) as f:
        sales_data = json.load(f)
    
    # Group by product
    grouped = itertools.groupby(
        sorted(sales_data, key=lambda x: x['product']),
        key=lambda x: x['product']
    )
    
    # Calculate totals
    summary = []
    for product, sales in grouped:
        sales_list = list(sales)
        total_quantity = sum(s['quantity'] for s in sales_list)
        total_revenue = sum(s['quantity'] * s['price'] for s in sales_list)
        avg_price = total_revenue / total_quantity if total_quantity else 0
        
        summary.append({
            'product': product,
            'total_quantity': total_quantity,
            'total_revenue': total_revenue,
            'average_price': avg_price
        })
    
    # Write to CSV
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ['product', 'total_quantity', 'total_revenue', 'average_price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)
```

## 🎓 Practice Exercises

### Beginner Level

1. **File Organizer**: Create a script that organizes files in a directory by extension using os/pathlib
2. **Date Calculator**: Build a utility that calculates age, days between dates, and business days
3. **Text Validator**: Implement email, phone, and URL validation using regex
4. **Simple Logger**: Create a basic logging system for a hypothetical application

### Intermediate Level

5. **Data Converter**: Build a tool that converts between JSON, CSV, and other formats
6. **Log Analyzer**: Parse server logs and extract meaningful statistics
7. **Configuration Manager**: Create a system for managing application configuration with JSON and validation
8. **Word Frequency Counter**: Analyze text files and generate word frequency reports

### Advanced Level

9. **Data Pipeline**: Build a complete ETL pipeline using multiple standard library modules
10. **System Monitor**: Create a tool that monitors system resources and logs alerts
11. **Backup Utility**: Implement a file backup system with timestamping and organization
12. **API Client**: Build a robust HTTP client with logging, error handling, and data serialization

## 🔧 Performance Tips

### Collections Performance
- Use `Counter` instead of manual dictionary counting
- Use `deque` for frequent append/pop operations at both ends
- Use `defaultdict` to avoid key existence checks

### Regex Performance
- Compile patterns that are used multiple times
- Use raw strings (r"pattern") for regex patterns
- Consider alternatives for simple string operations

### Itertools Efficiency
- Chain iterators instead of concatenating lists
- Use `itertools.compress` for filtering with boolean sequences
- Leverage combinatorial functions for mathematical operations

### Caching Strategies
- Use `@lru_cache` for expensive function calls
- Be mindful of memory usage with large caches
- Consider cache invalidation for long-running programs

## 📖 Additional Resources

### Official Documentation
- [Python Standard Library](https://docs.python.org/3/library/)
- [pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)
- [re — Regular expression operations](https://docs.python.org/3/library/re.html)
- [collections — Specialized container datatypes](https://docs.python.org/3/library/collections.html)

### Best Practices
- [PEP 8 — Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Regular Expression Best Practices](https://docs.python.org/3/howto/regex.html)

### Further Learning
- Advanced Python Patterns and Idioms
- Performance Optimization Techniques
- Third-party Libraries Building on Standard Library

## 🤝 Contributing

If you find any issues or have suggestions for improvements:

1. Check the code for correctness and completeness
2. Verify that all examples run successfully
3. Ensure tests pass and provide good coverage
4. Add new examples or exercises if beneficial
5. Update documentation to reflect any changes

## 📝 Notes

- **Python Version**: Code is compatible with Python 3.7+
- **Dependencies**: Uses only standard library modules (no external dependencies)
- **Platform**: Cross-platform compatible (Windows, macOS, Linux)
- **Testing**: Comprehensive test suite included for verification
- **Documentation**: Extensive inline comments and docstrings

This module serves as a comprehensive foundation for understanding Python's standard library and forms the basis for more advanced library usage and third-party package integration.
