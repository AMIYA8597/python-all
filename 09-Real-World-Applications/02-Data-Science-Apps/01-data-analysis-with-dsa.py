#!/usr/bin/env python3
"""
Data Science Applications with Data Structures and Algorithms
============================================================

This module demonstrates how data structures and algorithms are applied
in real-world data science applications, including data processing,
statistical analysis, machine learning, and visualization.

Author: Python DSA Master
Date: 2024
"""

import json
import time
import math
import random
import heapq
from typing import Dict, List, Tuple, Any, Optional, Set, Union
from collections import defaultdict, deque, Counter
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import statistics

# ==============================================================================
# DATA STRUCTURES FOR DATA SCIENCE
# ==============================================================================

class DataType(Enum):
    """Enumeration of common data types in data science."""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    TEXT = "text"
    MISSING = "missing"

@dataclass
class DataColumn:
    """Represents a data column with metadata."""
    name: str
    data_type: DataType
    values: List[Any] = field(default_factory=list)
    missing_count: int = 0
    unique_count: int = 0
    statistics: Dict[str, Any] = field(default_factory=dict)

class BloomFilter:
    """
    Bloom Filter for approximate membership testing.
    Useful for big data applications to quickly check if an item might exist.
    """
    
    def __init__(self, capacity: int, error_rate: float = 0.01):
        self.capacity = capacity
        self.error_rate = error_rate
        
        # Calculate optimal parameters
        self.bit_array_size = int(-(capacity * math.log(error_rate)) / (math.log(2) ** 2))
        self.hash_count = int((self.bit_array_size / capacity) * math.log(2))
        
        self.bit_array = [False] * self.bit_array_size
        self.items_added = 0
    
    def _hash_functions(self, item: str) -> List[int]:
        """Generate multiple hash values for an item."""
        hashes = []
        for i in range(self.hash_count):
            hash_val = hash(item + str(i)) % self.bit_array_size
            hashes.append(hash_val)
        return hashes
    
    def add(self, item: str) -> None:
        """Add an item to the bloom filter."""
        for hash_val in self._hash_functions(item):
            self.bit_array[hash_val] = True
        self.items_added += 1
    
    def might_contain(self, item: str) -> bool:
        """Check if an item might exist in the set."""
        return all(self.bit_array[hash_val] for hash_val in self._hash_functions(item))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bloom filter statistics."""
        return {
            'capacity': self.capacity,
            'items_added': self.items_added,
            'bit_array_size': self.bit_array_size,
            'hash_count': self.hash_count,
            'expected_error_rate': self.error_rate,
            'current_fill_ratio': sum(self.bit_array) / len(self.bit_array)
        }

class MinHashSignature:
    """
    MinHash for approximate similarity computation.
    Used for finding similar documents or datasets efficiently.
    """
    
    def __init__(self, num_hashes: int = 100):
        self.num_hashes = num_hashes
        self.signature = [float('inf')] * num_hashes
        self.hash_params = [(random.randint(1, 1000), random.randint(1, 1000)) 
                           for _ in range(num_hashes)]
    
    def update(self, shingles: Set[str]) -> None:
        """Update signature with a set of shingles."""
        for shingle in shingles:
            shingle_hash = hash(shingle)
            for i, (a, b) in enumerate(self.hash_params):
                hash_val = (a * shingle_hash + b) % (2**32)
                self.signature[i] = min(self.signature[i], hash_val)
    
    def jaccard_similarity(self, other: 'MinHashSignature') -> float:
        """Estimate Jaccard similarity with another signature."""
        matches = sum(1 for a, b in zip(self.signature, other.signature) if a == b)
        return matches / self.num_hashes

class TimeSeries:
    """
    Time series data structure with efficient operations.
    Uses binary search for time-based queries.
    """
    
    def __init__(self):
        self.data = []  # List of (timestamp, value) tuples
        self.sorted = True
    
    def add_point(self, timestamp: datetime, value: float) -> None:
        """Add a data point to the time series."""
        self.data.append((timestamp, value))
        if len(self.data) > 1 and timestamp < self.data[-2][0]:
            self.sorted = False
    
    def sort_if_needed(self) -> None:
        """Sort data by timestamp if needed."""
        if not self.sorted:
            self.data.sort(key=lambda x: x[0])
            self.sorted = True
    
    def get_range(self, start_time: datetime, end_time: datetime) -> List[Tuple[datetime, float]]:
        """Get data points within a time range using binary search."""
        self.sort_if_needed()
        
        # Binary search for start index
        start_idx = self._binary_search_time(start_time, True)
        end_idx = self._binary_search_time(end_time, False)
        
        return self.data[start_idx:end_idx + 1]
    
    def _binary_search_time(self, target_time: datetime, find_left: bool) -> int:
        """Binary search for time index."""
        left, right = 0, len(self.data) - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            if self.data[mid][0] == target_time:
                result = mid
                if find_left:
                    right = mid - 1
                else:
                    left = mid + 1
            elif self.data[mid][0] < target_time:
                if not find_left:
                    result = mid
                left = mid + 1
            else:
                if find_left:
                    result = mid
                right = mid - 1
        
        return result if result != -1 else (0 if find_left else len(self.data) - 1)
    
    def moving_average(self, window_size: int) -> List[Tuple[datetime, float]]:
        """Calculate moving average using sliding window."""
        self.sort_if_needed()
        if len(self.data) < window_size:
            return []
        
        result = []
        window_sum = sum(point[1] for point in self.data[:window_size])
        
        for i in range(window_size - 1, len(self.data)):
            if i >= window_size:
                window_sum += self.data[i][1] - self.data[i - window_size][1]
            
            avg = window_sum / window_size
            result.append((self.data[i][0], avg))
        
        return result

# ==============================================================================
# DATA PROCESSING ENGINE
# ==============================================================================

class DataProcessor:
    """
    High-performance data processing engine using optimized data structures.
    """
    
    def __init__(self):
        self.columns: Dict[str, DataColumn] = {}
        self.indices: Dict[str, Dict[Any, Set[int]]] = {}  # Inverted indices
        self.row_count = 0
        self.bloom_filters: Dict[str, BloomFilter] = {}
    
    def add_column(self, column: DataColumn) -> None:
        """Add a column to the processor."""
        self.columns[column.name] = column
        self.indices[column.name] = defaultdict(set)
        
        # Create bloom filter for categorical columns
        if column.data_type == DataType.CATEGORICAL:
            unique_values = len(set(column.values))
            self.bloom_filters[column.name] = BloomFilter(unique_values * 2)
            
            for value in column.values:
                if value is not None:
                    self.bloom_filters[column.name].add(str(value))
    
    def build_indices(self) -> None:
        """Build inverted indices for fast lookups."""
        for col_name, column in self.columns.items():
            self.indices[col_name].clear()
            
            for row_idx, value in enumerate(column.values):
                if value is not None:
                    self.indices[col_name][value].add(row_idx)
    
    def query(self, filters: Dict[str, Any]) -> Set[int]:
        """Query data using filters. Returns set of row indices."""
        if not filters:
            return set(range(self.row_count))
        
        result_sets = []
        
        for col_name, filter_value in filters.items():
            if col_name not in self.indices:
                continue
            
            # Use bloom filter for quick negative checks
            if col_name in self.bloom_filters:
                if not self.bloom_filters[col_name].might_contain(str(filter_value)):
                    return set()  # Definitely not present
            
            matching_rows = self.indices[col_name].get(filter_value, set())
            result_sets.append(matching_rows)
        
        # Intersect all result sets
        if result_sets:
            result = result_sets[0]
            for rs in result_sets[1:]:
                result = result.intersection(rs)
            return result
        
        return set()
    
    def aggregate(self, group_by: str, agg_column: str, agg_func: str) -> Dict[Any, float]:
        """Perform aggregation operations."""
        if group_by not in self.columns or agg_column not in self.columns:
            return {}
        
        groups = defaultdict(list)
        
        # Group data
        for row_idx in range(len(self.columns[group_by].values)):
            group_key = self.columns[group_by].values[row_idx]
            agg_value = self.columns[agg_column].values[row_idx]
            
            if group_key is not None and agg_value is not None:
                groups[group_key].append(agg_value)
        
        # Apply aggregation function
        result = {}
        for group_key, values in groups.items():
            if agg_func == 'sum':
                result[group_key] = sum(values)
            elif agg_func == 'mean':
                result[group_key] = statistics.mean(values)
            elif agg_func == 'count':
                result[group_key] = len(values)
            elif agg_func == 'min':
                result[group_key] = min(values)
            elif agg_func == 'max':
                result[group_key] = max(values)
        
        return result

# ==============================================================================
# MACHINE LEARNING UTILITIES
# ==============================================================================

class KDTree:
    """
    K-Dimensional Tree for efficient nearest neighbor searches.
    Used in machine learning for k-NN algorithms and spatial queries.
    """
    
    def __init__(self, points: List[List[float]], depth: int = 0):
        if not points:
            self.point = None
            self.left = None
            self.right = None
            return
        
        k = len(points[0])  # Dimension
        axis = depth % k
        
        # Sort points by axis
        points.sort(key=lambda x: x[axis])
        
        # Choose median as pivot
        median = len(points) // 2
        self.point = points[median]
        
        # Recursively build left and right subtrees
        self.left = KDTree(points[:median], depth + 1) if points[:median] else None
        self.right = KDTree(points[median + 1:], depth + 1) if points[median + 1:] else None
        self.axis = axis
    
    def distance(self, point1: List[float], point2: List[float]) -> float:
        """Calculate Euclidean distance between two points."""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))
    
    def nearest_neighbor(self, target: List[float], depth: int = 0) -> Optional[List[float]]:
        """Find the nearest neighbor to target point."""
        if self.point is None:
            return None
        
        k = len(target)
        axis = depth % k
        
        # Determine which subtree to search first
        if target[axis] < self.point[axis]:
            best = self._search_subtree(self.left, target, depth + 1)
            opposite_subtree = self.right
        else:
            best = self._search_subtree(self.right, target, depth + 1)
            opposite_subtree = self.left
        
        # Check if current point is better
        current_dist = self.distance(self.point, target)
        if best is None or current_dist < self.distance(best, target):
            best = self.point
            best_dist = current_dist
        else:
            best_dist = self.distance(best, target)
        
        # Check if we need to search the opposite subtree
        if abs(target[axis] - self.point[axis]) < best_dist:
            opposite_best = self._search_subtree(opposite_subtree, target, depth + 1)
            if opposite_best and self.distance(opposite_best, target) < best_dist:
                best = opposite_best
        
        return best
    
    def _search_subtree(self, subtree, target: List[float], depth: int) -> Optional[List[float]]:
        """Search a subtree for the nearest neighbor."""
        if subtree is None:
            return None
        return subtree.nearest_neighbor(target, depth)

class LSHForestForCosine:
    """
    Locality Sensitive Hashing for cosine similarity.
    Used for approximate nearest neighbor search in high-dimensional spaces.
    """
    
    def __init__(self, num_trees: int = 10, num_hashes: int = 16):
        self.num_trees = num_trees
        self.num_hashes = num_hashes
        self.trees = []
        self.vectors = {}
        self.next_id = 0
        
        # Generate random hyperplanes for each tree
        for _ in range(num_trees):
            hyperplanes = []
            for _ in range(num_hashes):
                # Random hyperplane in high-dimensional space
                hyperplanes.append([random.gauss(0, 1) for _ in range(100)])  # Assume 100D
            self.trees.append({
                'hyperplanes': hyperplanes,
                'buckets': defaultdict(list)
            })
    
    def add_vector(self, vector: List[float], item_id: str = None) -> str:
        """Add a vector to the LSH forest."""
        if item_id is None:
            item_id = f"item_{self.next_id}"
            self.next_id += 1
        
        self.vectors[item_id] = vector
        
        # Add to each tree
        for tree in self.trees:
            hash_signature = self._compute_hash(vector, tree['hyperplanes'])
            tree['buckets'][hash_signature].append(item_id)
        
        return item_id
    
    def _compute_hash(self, vector: List[float], hyperplanes: List[List[float]]) -> str:
        """Compute hash signature for a vector."""
        signature = []
        for hyperplane in hyperplanes:
            # Dot product with hyperplane
            dot_product = sum(v * h for v, h in zip(vector, hyperplane))
            signature.append('1' if dot_product >= 0 else '0')
        return ''.join(signature)
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        
        if norm_a == 0 or norm_b == 0:
            return 0
        
        return dot_product / (norm_a * norm_b)
    
    def query(self, query_vector: List[float], num_results: int = 10) -> List[Tuple[str, float]]:
        """Find similar vectors using LSH."""
        candidates = set()
        
        # Collect candidates from all trees
        for tree in self.trees:
            hash_signature = self._compute_hash(query_vector, tree['hyperplanes'])
            candidates.update(tree['buckets'].get(hash_signature, []))
        
        # Calculate actual similarities
        similarities = []
        for item_id in candidates:
            if item_id in self.vectors:
                similarity = self.cosine_similarity(query_vector, self.vectors[item_id])
                similarities.append((item_id, similarity))
        
        # Return top results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:num_results]

# ==============================================================================
# STATISTICAL ANALYSIS TOOLS
# ==============================================================================

class OnlineStatistics:
    """
    Online statistics computation using Welford's algorithm.
    Allows incremental computation of mean, variance, and other statistics.
    """
    
    def __init__(self):
        self.count = 0
        self.mean = 0.0
        self.m2 = 0.0  # Sum of squares of differences from mean
        self.min_val = float('inf')
        self.max_val = float('-inf')
        self.sum_val = 0.0
        
        # For quantile estimation
        self.values = []  # For exact quantiles (memory intensive)
        self.use_exact_quantiles = True
        self.max_values_stored = 10000
    
    def add_value(self, value: float) -> None:
        """Add a new value and update statistics."""
        self.count += 1
        self.sum_val += value
        
        # Update min/max
        self.min_val = min(self.min_val, value)
        self.max_val = max(self.max_val, value)
        
        # Welford's algorithm for mean and variance
        delta = value - self.mean
        self.mean += delta / self.count
        delta2 = value - self.mean
        self.m2 += delta * delta2
        
        # Store values for quantile computation
        if self.use_exact_quantiles and len(self.values) < self.max_values_stored:
            self.values.append(value)
        elif len(self.values) >= self.max_values_stored:
            self.use_exact_quantiles = False
            self.values.clear()
    
    def get_variance(self) -> float:
        """Get the population variance."""
        return self.m2 / self.count if self.count > 0 else 0.0
    
    def get_sample_variance(self) -> float:
        """Get the sample variance."""
        return self.m2 / (self.count - 1) if self.count > 1 else 0.0
    
    def get_std(self) -> float:
        """Get the population standard deviation."""
        return math.sqrt(self.get_variance())
    
    def get_sample_std(self) -> float:
        """Get the sample standard deviation."""
        return math.sqrt(self.get_sample_variance())
    
    def get_quantile(self, q: float) -> Optional[float]:
        """Get quantile (q between 0 and 1)."""
        if not self.use_exact_quantiles or not self.values:
            return None
        
        sorted_values = sorted(self.values)
        index = q * (len(sorted_values) - 1)
        
        if index == int(index):
            return sorted_values[int(index)]
        else:
            lower = sorted_values[int(index)]
            upper = sorted_values[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
    
    def get_summary(self) -> Dict[str, Any]:
        """Get complete statistical summary."""
        summary = {
            'count': self.count,
            'mean': self.mean,
            'variance': self.get_variance(),
            'std': self.get_std(),
            'min': self.min_val if self.count > 0 else None,
            'max': self.max_val if self.count > 0 else None,
            'sum': self.sum_val
        }
        
        if self.use_exact_quantiles:
            summary.update({
                'median': self.get_quantile(0.5),
                'q25': self.get_quantile(0.25),
                'q75': self.get_quantile(0.75)
            })
        
        return summary

class HyperLogLog:
    """
    HyperLogLog probabilistic cardinality estimator.
    Efficiently estimates the number of unique elements in large datasets.
    """
    
    def __init__(self, precision: int = 12):
        self.precision = precision
        self.m = 2 ** precision  # Number of buckets
        self.buckets = [0] * self.m
        self.alpha = self._get_alpha()
    
    def _get_alpha(self) -> float:
        """Get alpha constant based on number of buckets."""
        if self.m >= 128:
            return 0.7213 / (1 + 1.079 / self.m)
        elif self.m >= 64:
            return 0.709
        elif self.m >= 32:
            return 0.697
        else:
            return 0.673
    
    def add(self, item: str) -> None:
        """Add an item to the estimator."""
        # Hash the item
        item_hash = hash(item)
        
        # Use first p bits for bucket selection
        bucket_idx = item_hash & (self.m - 1)
        
        # Count leading zeros in remaining bits
        remaining_bits = item_hash >> self.precision
        leading_zeros = self._count_leading_zeros(remaining_bits) + 1
        
        # Update bucket with maximum value
        self.buckets[bucket_idx] = max(self.buckets[bucket_idx], leading_zeros)
    
    def _count_leading_zeros(self, value: int) -> int:
        """Count leading zeros in binary representation."""
        if value == 0:
            return 32  # Assuming 32-bit integers
        
        count = 0
        mask = 1 << 31
        while (value & mask) == 0:
            count += 1
            mask >>= 1
        return count
    
    def cardinality(self) -> int:
        """Estimate the cardinality."""
        # Calculate raw estimate
        raw_estimate = self.alpha * (self.m ** 2) / sum(2 ** (-bucket) for bucket in self.buckets)
        
        # Apply bias corrections
        if raw_estimate <= 2.5 * self.m:
            # Small range correction
            zeros = self.buckets.count(0)
            if zeros != 0:
                return int(self.m * math.log(self.m / float(zeros)))
        
        if raw_estimate <= (1.0/30.0) * (2 ** 32):
            return int(raw_estimate)
        else:
            # Large range correction
            return int(-1 * (2 ** 32) * math.log(1 - raw_estimate / (2 ** 32)))

# ==============================================================================
# DEMONSTRATION AND BENCHMARKING
# ==============================================================================

def create_sample_dataset() -> DataProcessor:
    """Create a sample dataset for demonstration."""
    processor = DataProcessor()
    
    # Generate sample data
    num_records = 10000
    categories = ['A', 'B', 'C', 'D', 'E']
    
    # Customer ID column
    customer_ids = [f"CUST_{i:06d}" for i in range(num_records)]
    id_column = DataColumn("customer_id", DataType.CATEGORICAL, customer_ids)
    
    # Age column
    ages = [random.randint(18, 80) for _ in range(num_records)]
    age_column = DataColumn("age", DataType.NUMERICAL, ages)
    
    # Category column
    category_values = [random.choice(categories) for _ in range(num_records)]
    category_column = DataColumn("category", DataType.CATEGORICAL, category_values)
    
    # Revenue column
    revenues = [round(random.uniform(100, 5000), 2) for _ in range(num_records)]
    revenue_column = DataColumn("revenue", DataType.NUMERICAL, revenues)
    
    # Add columns to processor
    processor.add_column(id_column)
    processor.add_column(age_column)
    processor.add_column(category_column)
    processor.add_column(revenue_column)
    processor.row_count = num_records
    
    return processor

def demo_data_processing():
    """Demonstrate data processing capabilities."""
    print("Data Processing Engine Demo")
    print("=" * 40)
    
    # Create dataset
    start_time = time.time()
    processor = create_sample_dataset()
    
    # Build indices
    processor.build_indices()
    setup_time = time.time() - start_time
    
    print(f"Dataset created and indexed in {setup_time:.4f} seconds")
    print(f"Records: {processor.row_count}")
    print(f"Columns: {len(processor.columns)}")
    
    # Query performance test
    start_time = time.time()
    results = processor.query({'category': 'A'})
    query_time = time.time() - start_time
    
    print(f"Query for category 'A': {len(results)} results in {query_time:.6f} seconds")
    
    # Aggregation test
    start_time = time.time()
    avg_revenue_by_category = processor.aggregate('category', 'revenue', 'mean')
    agg_time = time.time() - start_time
    
    print(f"Aggregation completed in {agg_time:.6f} seconds")
    print("Average revenue by category:")
    for category, avg_revenue in avg_revenue_by_category.items():
        print(f"  {category}: ${avg_revenue:.2f}")
    
    # Bloom filter statistics
    print("\nBloom Filter Statistics:")
    for col_name, bf in processor.bloom_filters.items():
        stats = bf.get_stats()
        print(f"  {col_name}: {stats['items_added']} items, "
              f"{stats['current_fill_ratio']:.4f} fill ratio")

def demo_time_series_analysis():
    """Demonstrate time series analysis."""
    print("\nTime Series Analysis Demo")
    print("=" * 40)
    
    # Create sample time series
    ts = TimeSeries()
    base_time = datetime.now() - timedelta(days=30)
    
    # Generate daily data points
    for i in range(30):
        timestamp = base_time + timedelta(days=i)
        value = 100 + 10 * math.sin(i * 0.2) + random.uniform(-5, 5)
        ts.add_point(timestamp, value)
    
    print(f"Created time series with {len(ts.data)} data points")
    
    # Query time range
    query_start = base_time + timedelta(days=10)
    query_end = base_time + timedelta(days=20)
    
    start_time = time.time()
    range_data = ts.get_range(query_start, query_end)
    query_time = time.time() - start_time
    
    print(f"Range query returned {len(range_data)} points in {query_time:.6f} seconds")
    
    # Moving average
    start_time = time.time()
    moving_avg = ts.moving_average(7)  # 7-day moving average
    ma_time = time.time() - start_time
    
    print(f"7-day moving average computed in {ma_time:.6f} seconds")
    print(f"Moving average points: {len(moving_avg)}")
    
    # Show sample data
    print("\nSample time series data (first 5 points):")
    for timestamp, value in ts.data[:5]:
        print(f"  {timestamp.strftime('%Y-%m-%d')}: {value:.2f}")

def demo_nearest_neighbor_search():
    """Demonstrate k-d tree and LSH for nearest neighbor search."""
    print("\nNearest Neighbor Search Demo")
    print("=" * 40)
    
    # Generate sample points for k-d tree
    points_2d = [[random.uniform(0, 100), random.uniform(0, 100)] for _ in range(1000)]
    
    # Build k-d tree
    start_time = time.time()
    kdtree = KDTree(points_2d)
    build_time = time.time() - start_time
    
    print(f"K-D tree built with {len(points_2d)} points in {build_time:.6f} seconds")
    
    # Search for nearest neighbor
    query_point = [50, 50]
    start_time = time.time()
    nearest = kdtree.nearest_neighbor(query_point)
    search_time = time.time() - start_time
    
    print(f"Nearest neighbor search completed in {search_time:.6f} seconds")
    print(f"Query point: {query_point}")
    print(f"Nearest neighbor: {nearest}")
    if nearest:
        distance = kdtree.distance(query_point, nearest)
        print(f"Distance: {distance:.4f}")
    
    # LSH Forest demo
    print("\nLSH Forest Demo:")
    lsh = LSHForestForCosine(num_trees=5, num_hashes=8)
    
    # Generate high-dimensional vectors
    vectors = []
    for i in range(100):
        vector = [random.gauss(0, 1) for _ in range(50)]  # 50-dimensional
        vectors.append(vector)
        lsh.add_vector(vector, f"doc_{i}")
    
    # Query
    query_vector = [random.gauss(0, 1) for _ in range(50)]
    start_time = time.time()
    similar_docs = lsh.query(query_vector, num_results=5)
    lsh_time = time.time() - start_time
    
    print(f"LSH query completed in {lsh_time:.6f} seconds")
    print("Top 5 similar documents:")
    for doc_id, similarity in similar_docs:
        print(f"  {doc_id}: similarity = {similarity:.4f}")

def demo_online_statistics():
    """Demonstrate online statistics computation."""
    print("\nOnline Statistics Demo")
    print("=" * 40)
    
    stats = OnlineStatistics()
    
    # Process streaming data
    start_time = time.time()
    for _ in range(100000):
        value = random.gauss(50, 15)  # Normal distribution
        stats.add_value(value)
    process_time = time.time() - start_time
    
    print(f"Processed {stats.count} values in {process_time:.4f} seconds")
    
    # Get statistics
    summary = stats.get_summary()
    print("\nStatistical Summary:")
    for key, value in summary.items():
        if value is not None:
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
    
    # HyperLogLog cardinality estimation
    print("\nHyperLogLog Cardinality Estimation:")
    hll = HyperLogLog(precision=12)
    
    # Add unique items
    unique_items = set()
    for i in range(50000):
        item = f"item_{random.randint(1, 10000)}"  # Some duplicates expected
        unique_items.add(item)
        hll.add(item)
    
    estimated_cardinality = hll.cardinality()
    actual_cardinality = len(unique_items)
    error_rate = abs(estimated_cardinality - actual_cardinality) / actual_cardinality
    
    print(f"Actual unique items: {actual_cardinality}")
    print(f"Estimated unique items: {estimated_cardinality}")
    print(f"Error rate: {error_rate:.4f} ({error_rate * 100:.2f}%)")

def demo_similarity_detection():
    """Demonstrate MinHash for similarity detection."""
    print("\nSimilarity Detection Demo")
    print("=" * 40)
    
    # Create sample documents
    documents = [
        "the quick brown fox jumps over the lazy dog",
        "a quick brown fox leaps over a lazy dog",
        "the fast brown fox jumps over the sleeping dog",
        "python is a powerful programming language for data science",
        "data science requires powerful programming languages like python"
    ]
    
    def get_shingles(text: str, k: int = 2) -> Set[str]:
        """Generate k-shingles from text."""
        words = text.lower().split()
        return set(' '.join(words[i:i+k]) for i in range(len(words) - k + 1))
    
    # Create MinHash signatures
    signatures = []
    for i, doc in enumerate(documents):
        minhash = MinHashSignature(num_hashes=100)
        shingles = get_shingles(doc, k=2)
        minhash.update(shingles)
        signatures.append((f"Doc_{i}", minhash))
    
    print("Document similarity matrix:")
    print("    ", end="")
    for i in range(len(documents)):
        print(f"Doc_{i:2d} ", end="")
    print()
    
    for i, (doc_id1, sig1) in enumerate(signatures):
        print(f"{doc_id1} ", end="")
        for j, (doc_id2, sig2) in enumerate(signatures):
            similarity = sig1.jaccard_similarity(sig2)
            print(f"{similarity:5.3f} ", end="")
        print()
    
    print("\nDocument pairs with high similarity (>0.3):")
    for i in range(len(signatures)):
        for j in range(i + 1, len(signatures)):
            similarity = signatures[i][1].jaccard_similarity(signatures[j][1])
            if similarity > 0.3:
                print(f"  {signatures[i][0]} - {signatures[j][0]}: {similarity:.3f}")

def main():
    """Run all demonstrations."""
    print("Data Science Applications with DSA - Comprehensive Demo")
    print("=" * 60)
    
    # Run all demos
    demo_data_processing()
    demo_time_series_analysis()
    demo_nearest_neighbor_search()
    demo_online_statistics()
    demo_similarity_detection()
    
    print("\n" + "=" * 60)
    print("All demonstrations completed successfully!")
    
    # Performance summary
    print("\nPerformance Insights:")
    print("- Bloom filters provide fast approximate membership testing")
    print("- K-D trees enable efficient nearest neighbor searches in low dimensions")
    print("- LSH enables approximate similarity search in high dimensions")
    print("- Online statistics allow incremental computation without storing all data")
    print("- MinHash provides fast similarity estimation for large datasets")
    print("- HyperLogLog efficiently estimates cardinality of massive datasets")

if __name__ == "__main__":
    main()
