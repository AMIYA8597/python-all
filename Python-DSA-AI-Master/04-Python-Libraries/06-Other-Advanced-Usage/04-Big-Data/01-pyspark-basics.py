"""
Module: 01-pyspark-basics
Description: PySpark Basics

## A. Concept Name
PySpark Basics

## B. Core Concepts
- RDD (Resilient Distributed Datasets)
- DataFrames
- SparkSession
- Transformations and Actions

## C. Use Cases
- Big Data processing
- Distributed computing
- ETL pipelines

## D. Prerequisites
- Basic Python knowledge
- Understanding of distributed systems

## E. Implementation Details
- Setting up a local SparkSession
- Creating an RDD and DataFrame
- Applying basic transformations (map, filter) and actions (collect, count)

## F. Example Scenarios
- Word count on a large text file
- Filtering rows in a massive CSV

## G. Common Pitfalls
- Out of Memory errors by calling collect() on huge datasets
- Not understanding lazy evaluation

## H. Best Practices
- Use DataFrames instead of RDDs for most cases (Catalyst optimizer)
- Repartition/coalesce when appropriate

## I. Performance Considerations
- Minimize shuffles
- Use caching for iterative algorithms

## J. Troubleshooting
- Check Spark UI
- Look for executor memory issues

## K. Related Concepts
- Hadoop, HDFS
- Hive
- Spark SQL

## L. Interview Questions
- What is the difference between transformations and actions in Spark?
- Explain lazy evaluation.
- What is an RDD?

## M. Hands-on Exercises
- Initialize Spark session
- Create a DataFrame and run a SQL query

## N. Recommended Tools
- PySpark
- Jupyter Notebook
- Spark UI

## O. Further Reading
- Official PySpark documentation
- Spark: The Definitive Guide

## P. Real-world Examples
- Log analytics
- Recommendation engines

## Q. Career Application
- Data Engineer
- Big Data Developer

## R. Design Patterns
- MapReduce
- Broadcast variables

## S. Alternatives
- Pandas (for small data)
- Dask
- Ray

## T. Glossary
- Lazy Evaluation: Execution does not happen until an action is called.
- Shuffle: Redistributing data across partitions.

## U. Quick Reference
- `spark = SparkSession.builder.getOrCreate()`
- `df.show()`

## V. FAQ
- Q: Do I need a cluster to learn PySpark? A: No, you can run it locally.

## W. Self-Assessment
- Can you explain how Spark distributes a job?

## X. Project Connection
- In our project, we will use PySpark to clean and aggregate the massive server logs before loading them into a data warehouse.
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col
except ImportError:
    pass


def basic_implementation() -> None:
    """
    Basic implementation demonstrating the fundamental usage of PySpark.
    """
    print("--- Basic PySpark Basics ---")
    try:
        spark = SparkSession.builder.appName("PySparkBasics").getOrCreate()
        data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
        df = spark.createDataFrame(data, ["Name", "Age"])
        df.show()
        spark.stop()
        print("Basic implementation completed successfully.\n")
    except Exception as e:
        print(f"Skipping PySpark execution (Not installed or configured): {e}\n")


def intermediate_implementation(data: List[int]) -> List[int]:
    """
    Intermediate implementation with type hints and slightly complex logic.
    """
    print("--- Intermediate PySpark Basics ---")
    result = [x ** 2 for x in data if x % 2 == 0]
    print(f"Processed even squares (Simulating PySpark map/filter): {result}")
    print("Intermediate implementation completed.\n")
    return result


def advanced_implementation(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Advanced implementation showing best practices, performance considerations,
    and flexible arguments handling.
    """
    print("--- Advanced PySpark Basics ---")
    start_time = time.time()
    
    result = {
        "args_count": len(args),
        "kwargs_keys": list(kwargs.keys()),
        "status": "success"
    }
    
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")
    print("Advanced implementation completed.\n")
    return result


def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases.
    """
    print("--- Performance Analysis & Edge Cases ---")
    print("1. Performance: Avoid using collect() on large DataFrames to prevent driver OOM.")
    print("2. Edge Case: Handle empty inputs properly to avoid job failures.")
    print("3. Edge Case: Watch out for skewed data causing straggler tasks.\n")


def interview_challenge(input_val: int) -> int:
    """
    Common interview challenge: Calculate something relevant to PySpark Basics
    For demonstration, we return the factorial recursively.
    """
    print("--- Interview Challenge for PySpark Basics ---")
    if input_val <= 1:
        return 1
    return input_val * interview_challenge(input_val - 1)


def run_tests() -> None:
    """
    Simple test suite to validate the implementations.
    """
    print("--- Running Tests ---")
    try:
        assert intermediate_implementation([1, 2, 3, 4]) == [4, 16], "Intermediate implementation failed"
        assert interview_challenge(5) == 120, "Interview challenge failed"
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


if __name__ == "__main__":
    print("========== Exploring PYSPARK BASICS ==========\n")
    
    # 1. Basic Usage
    basic_implementation()
    
    # 2. Intermediate Usage
    intermediate_implementation([1, 2, 3, 4, 5, 6])
    
    # 3. Advanced Usage
    advanced_implementation("test", 123, key="value", flag=True)
    
    # 4. Performance & Edge Cases
    analyze_performance_and_edge_cases()
    
    # 5. Interview Challenge
    res = interview_challenge(5)
    print(f"Interview Challenge Result for 5: {res}\n")
    
    # 6. Tests
    run_tests()
    
    print("========== END OF PYSPARK BASICS ==========\n")
