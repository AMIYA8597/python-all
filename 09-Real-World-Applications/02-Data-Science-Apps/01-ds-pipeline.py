\"\"\"
Module: 01-ds-pipeline.py
Topic: Data Science Pipelines & ETL in Python

This module demonstrates how to build robust Data Science pipelines, covering Extract, 
Transform, Load (ETL) processes, data validation, and handling large datasets.

Why it matters:
Data scientists spend a significant amount of time cleaning and preparing data. 
A well-architected data pipeline ensures reproducibility, handles missing values 
gracefully, and scales to handle large volumes of data without crashing. 
It forms the backbone of any machine learning or analytics system.

Learning Objectives:
1. Build an ETL pipeline using Generators for memory efficiency.
2. Implement data validation to catch dirty data early.
3. Understand how to use type hinting and dataclasses for structured data.

Beginner Explanation:
A data pipeline is like a water filtration system. You extract dirty water (raw data) 
from a source, run it through filters to remove impurities and add minerals (transform 
and clean), and finally store the clean water in a tank ready for drinking (load).

Advanced Explanation:
Modern data pipelines in Python heavily utilize generators to lazily evaluate data streams,
preventing Out-Of-Memory (OOM) errors when processing gigabytes of logs or CSVs. 
Data validation frameworks (like Pydantic or Great Expectations) ensure that the incoming 
data matches expected schemas, preventing downstream model drift or runtime crashes. 
Transformations are often vectorized using Pandas or NumPy for computational efficiency, 
but for sheer scale, row-wise generator pipelines or distributed systems (PySpark/Dask) are preferred.
\"\"\"

import csv
import io
from typing import Generator, Dict, Any, List, Optional
from dataclasses import dataclass

# ==========================================
# 1. Data Structures & Validation
# ==========================================

@dataclass
class UserTransaction:
    \"\"\"Schema for a valid transaction.\"\"\"
    user_id: int
    amount: float
    currency: str
    status: str

def validate_transaction(row: Dict[str, str]) -> Optional[UserTransaction]:
    \"\"\"
    Validates a raw data row and converts it to a structured dataclass.
    Returns None if the data is invalid (simulating dropping bad rows).
    \"\"\"
    try:
        user_id = int(row['user_id'])
        amount = float(row['amount'])
        if amount <= 0:
            return None # Ignore non-positive amounts
        return UserTransaction(
            user_id=user_id,
            amount=amount,
            currency=row['currency'].upper(),
            status=row['status'].lower()
        )
    except (ValueError, KeyError):
        return None # Data is missing or malformed

# ==========================================
# 2. Pipeline Implementation (Generator-based)
# ==========================================

def extract_data(csv_content: str) -> Generator[Dict[str, str], None, None]:
    \"\"\"
    EXTRACT phase: Yields rows one by one.
    In a real scenario, this would read from a file or network stream lazily.
    \"\"\"
    reader = csv.DictReader(io.StringIO(csv_content))
    for row in reader:
        yield row

def transform_data(raw_data_stream: Generator[Dict[str, str], None, None]) -> Generator[UserTransaction, None, None]:
    \"\"\"
    TRANSFORM phase: Validates and cleans the data stream.
    \"\"\"
    for raw_row in raw_data_stream:
        validated = validate_transaction(raw_row)
        if validated and validated.status == 'completed':
            # Apply transformation rule: convert everything to USD (mock rate)
            if validated.currency == 'EUR':
                validated.amount *= 1.1
                validated.currency = 'USD'
            yield validated

def load_data(clean_data_stream: Generator[UserTransaction, None, None]) -> float:
    \"\"\"
    LOAD phase: Aggregates or stores the data.
    Returns the total volume of successful USD transactions.
    \"\"\"
    total_volume = 0.0
    for transaction in clean_data_stream:
        total_volume += transaction.amount
    return total_volume


# ==========================================
# Complexity Analysis
# ==========================================
# Time Complexity: O(N) where N is the number of rows in the dataset. We process each row exactly once.
# Space Complexity: O(1) auxiliary space (excluding the output accumulator). Because we use generators,
#   we only ever hold one row in memory at a time, regardless of how large N is.

# ==========================================
# Interview Challenge
# ==========================================
# Challenge: You have a CSV file that is 50GB, but you only have 8GB of RAM.
# How do you find the top 10 users by transaction volume?
# Hint: Use a generator pipeline with a min-heap (heapq) or external sorting.

if __name__ == \"__main__\":
    # Mock raw data
    MOCK_CSV = \"\"\"user_id,amount,currency,status
1,100.50,USD,completed
2,50.00,EUR,completed
3,-10.00,USD,failed
4,invalid,USD,completed
5,200.00,USD,pending
\"\"\"
    
    print(\"Starting ETL Pipeline...\")
    # Pipeline execution is lazy until the `load_data` loop consumes the generator
    raw_stream = extract_data(MOCK_CSV)
    clean_stream = transform_data(raw_stream)
    total = load_data(clean_stream)
    
    print(f\"Total processed volume (USD): {total:.2f}\")
    
    # Assertions
    # 100.50 (USD, completed) + 50.00 * 1.1 (EUR -> USD, completed) = 155.50
    # ID 3 is negative (invalid), ID 4 is malformed, ID 5 is pending.
    assert abs(total - 155.50) < 0.01
    print(\"All assertions passed!\")
