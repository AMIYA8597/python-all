#!/usr/bin/env python3
"""
Data Science Fundamentals with Python
=====================================

This module provides comprehensive coverage of data science libraries and techniques:

1. NumPy - Numerical computing with arrays
2. Pandas - Data manipulation and analysis
3. Matplotlib/Seaborn - Data visualization
4. Statistical Analysis - Descriptive and inferential statistics
5. Data Preprocessing - Cleaning and transformation
6. Feature Engineering - Creating meaningful features
7. Time Series Analysis - Working with temporal data
8. Data I/O - Reading/writing various formats

Note: This module demonstrates concepts without requiring external libraries
by implementing core functionality and showing usage patterns.

Author: Python DSA Master
Date: 2024
"""

import math
import random
import statistics
from typing import List, Dict, Any, Union, Optional, Tuple
from collections import defaultdict, Counter
import json
import csv
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

# ==============================================================================
# NUMPY-LIKE ARRAY OPERATIONS
# ==============================================================================

class NDArray:
    """
    A simplified NumPy-like array implementation demonstrating core concepts.
    This shows how numerical arrays work under the hood.
    """
    
    def __init__(self, data: Union[List, List[List]], dtype: str = 'float64'):
        """Initialize N-dimensional array."""
        self.data = self._flatten_if_needed(data)
        self.dtype = dtype
        self.shape = self._calculate_shape(data)
        self.ndim = len(self.shape)
        self.size = self._calculate_size()
    
    def _flatten_if_needed(self, data):
        """Convert nested lists to flat list for internal storage."""
        if isinstance(data[0], (list, tuple)):
            # 2D array
            flat = []
            for row in data:
                flat.extend(row)
            return flat
        return data
    
    def _calculate_shape(self, data):
        """Calculate array shape."""
        if isinstance(data[0], (list, tuple)):
            return (len(data), len(data[0]))
        return (len(data),)
    
    def _calculate_size(self):
        """Calculate total number of elements."""
        size = 1
        for dim in self.shape:
            size *= dim
        return size
    
    def reshape(self, new_shape: Tuple[int, ...]) -> 'NDArray':
        """Reshape array to new dimensions."""
        new_size = 1
        for dim in new_shape:
            new_size *= dim
        
        if new_size != self.size:
            raise ValueError(f"Cannot reshape array of size {self.size} to {new_shape}")
        
        result = NDArray([0])  # Temporary
        result.data = self.data.copy()
        result.shape = new_shape
        result.ndim = len(new_shape)
        result.size = new_size
        result.dtype = self.dtype
        return result
    
    def __add__(self, other):
        """Element-wise addition."""
        if isinstance(other, NDArray):
            if self.shape != other.shape:
                raise ValueError("Shape mismatch for addition")
            result_data = [a + b for a, b in zip(self.data, other.data)]
        else:
            # Scalar addition
            result_data = [x + other for x in self.data]
        
        result = NDArray([0])
        result.data = result_data
        result.shape = self.shape
        result.ndim = self.ndim
        result.size = self.size
        result.dtype = self.dtype
        return result
    
    def __mul__(self, other):
        """Element-wise multiplication."""
        if isinstance(other, NDArray):
            if self.shape != other.shape:
                raise ValueError("Shape mismatch for multiplication")
            result_data = [a * b for a, b in zip(self.data, other.data)]
        else:
            # Scalar multiplication
            result_data = [x * other for x in self.data]
        
        result = NDArray([0])
        result.data = result_data
        result.shape = self.shape
        result.ndim = self.ndim
        result.size = self.size
        result.dtype = self.dtype
        return result
    
    def mean(self, axis=None):
        """Calculate mean along specified axis."""
        if axis is None:
            return sum(self.data) / len(self.data)
        
        # For demonstration, implement axis=0 for 2D arrays
        if self.ndim == 2 and axis == 0:
            rows, cols = self.shape
            means = []
            for col in range(cols):
                col_sum = sum(self.data[row * cols + col] for row in range(rows))
                means.append(col_sum / rows)
            return NDArray(means)
        
        return sum(self.data) / len(self.data)
    
    def sum(self, axis=None):
        """Calculate sum along specified axis."""
        if axis is None:
            return sum(self.data)
        
        if self.ndim == 2 and axis == 0:
            rows, cols = self.shape
            sums = []
            for col in range(cols):
                col_sum = sum(self.data[row * cols + col] for row in range(rows))
                sums.append(col_sum)
            return NDArray(sums)
        
        return sum(self.data)
    
    def max(self, axis=None):
        """Find maximum value."""
        if axis is None:
            return max(self.data)
        # Simplified implementation for demonstration
        return max(self.data)
    
    def min(self, axis=None):
        """Find minimum value."""
        if axis is None:
            return min(self.data)
        return min(self.data)
    
    def std(self):
        """Calculate standard deviation."""
        mean_val = self.mean()
        variance = sum((x - mean_val) ** 2 for x in self.data) / len(self.data)
        return math.sqrt(variance)
    
    def dot(self, other: 'NDArray') -> 'NDArray':
        """Matrix multiplication (dot product)."""
        if self.ndim != 2 or other.ndim != 2:
            raise ValueError("Dot product requires 2D arrays")
        
        if self.shape[1] != other.shape[0]:
            raise ValueError("Incompatible shapes for matrix multiplication")
        
        rows_a, cols_a = self.shape
        rows_b, cols_b = other.shape
        
        result_data = []
        for i in range(rows_a):
            for j in range(cols_b):
                dot_product = 0
                for k in range(cols_a):
                    a_val = self.data[i * cols_a + k]
                    b_val = other.data[k * cols_b + j]
                    dot_product += a_val * b_val
                result_data.append(dot_product)
        
        result = NDArray([0])
        result.data = result_data
        result.shape = (rows_a, cols_b)
        result.ndim = 2
        result.size = rows_a * cols_b
        result.dtype = self.dtype
        return result
    
    def to_2d_list(self) -> List[List]:
        """Convert to 2D Python list for display."""
        if self.ndim != 2:
            return self.data
        
        rows, cols = self.shape
        result = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(self.data[i * cols + j])
            result.append(row)
        return result
    
    def __str__(self):
        if self.ndim == 1:
            return f"NDArray({self.data})"
        else:
            return f"NDArray({self.to_2d_list()})"
    
    def __repr__(self):
        return self.__str__()

# ==============================================================================
# PANDAS-LIKE DATAFRAME
# ==============================================================================

@dataclass
class SeriesData:
    """Represents a single column of data (like pandas Series)."""
    values: List[Any]
    name: str
    dtype: str = 'object'
    
    def __post_init__(self):
        if not self.values:
            self.values = []
        
        # Infer dtype if not specified
        if self.dtype == 'object' and self.values:
            if all(isinstance(x, (int, float)) for x in self.values if x is not None):
                self.dtype = 'numeric'
            elif all(isinstance(x, str) for x in self.values if x is not None):
                self.dtype = 'string'

class DataFrame:
    """
    A simplified pandas DataFrame implementation.
    Demonstrates core data manipulation concepts.
    """
    
    def __init__(self, data: Dict[str, List[Any]]):
        """Initialize DataFrame from dictionary."""
        self.columns = list(data.keys())
        self.data = {}
        
        # Ensure all columns have same length
        max_length = max(len(values) for values in data.values()) if data else 0
        
        for col, values in data.items():
            # Pad shorter columns with None
            padded_values = values + [None] * (max_length - len(values))
            self.data[col] = SeriesData(padded_values, col)
        
        self.index = list(range(max_length))
        self.shape = (len(self.index), len(self.columns))
    
    def head(self, n: int = 5) -> 'DataFrame':
        """Return first n rows."""
        new_data = {}
        for col in self.columns:
            new_data[col] = self.data[col].values[:n]
        return DataFrame(new_data)
    
    def tail(self, n: int = 5) -> 'DataFrame':
        """Return last n rows."""
        new_data = {}
        for col in self.columns:
            new_data[col] = self.data[col].values[-n:]
        return DataFrame(new_data)
    
    def describe(self) -> Dict[str, Dict[str, float]]:
        """Generate descriptive statistics."""
        stats = {}
        
        for col in self.columns:
            series = self.data[col]
            if series.dtype == 'numeric':
                values = [v for v in series.values if v is not None]
                if values:
                    stats[col] = {
                        'count': len(values),
                        'mean': statistics.mean(values),
                        'std': statistics.stdev(values) if len(values) > 1 else 0,
                        'min': min(values),
                        'max': max(values),
                        '25%': statistics.quantiles(values, n=4)[0] if len(values) >= 4 else values[0],
                        '50%': statistics.median(values),
                        '75%': statistics.quantiles(values, n=4)[2] if len(values) >= 4 else values[-1],
                    }
        
        return stats
    
    def info(self) -> Dict[str, Any]:
        """Return DataFrame information."""
        info_data = {
            'shape': self.shape,
            'columns': self.columns,
            'dtypes': {col: self.data[col].dtype for col in self.columns},
            'memory_usage': len(str(self.data)),  # Simplified
            'null_counts': {}
        }
        
        for col in self.columns:
            null_count = sum(1 for v in self.data[col].values if v is None)
            info_data['null_counts'][col] = null_count
        
        return info_data
    
    def groupby(self, column: str) -> Dict[Any, 'DataFrame']:
        """Group DataFrame by column values."""
        if column not in self.columns:
            raise KeyError(f"Column '{column}' not found")
        
        groups = defaultdict(lambda: defaultdict(list))
        group_values = self.data[column].values
        
        for i, group_val in enumerate(group_values):
            for col in self.columns:
                groups[group_val][col].append(self.data[col].values[i])
        
        result = {}
        for group_val, group_data in groups.items():
            result[group_val] = DataFrame(group_data)
        
        return result
    
    def sort_values(self, by: str, ascending: bool = True) -> 'DataFrame':
        """Sort DataFrame by column values."""
        if by not in self.columns:
            raise KeyError(f"Column '{by}' not found")
        
        # Create list of (value, index) pairs
        sort_data = [(self.data[by].values[i], i) for i in range(len(self.index))]
        sort_data.sort(key=lambda x: x[0] if x[0] is not None else float('inf'), reverse=not ascending)
        
        # Reorder all columns based on sorted indices
        new_data = {}
        for col in self.columns:
            new_data[col] = [self.data[col].values[idx] for _, idx in sort_data]
        
        return DataFrame(new_data)
    
    def fillna(self, value: Any) -> 'DataFrame':
        """Fill missing values."""
        new_data = {}
        for col in self.columns:
            new_values = [value if v is None else v for v in self.data[col].values]
            new_data[col] = new_values
        return DataFrame(new_data)
    
    def dropna(self) -> 'DataFrame':
        """Drop rows with missing values."""
        valid_indices = []
        for i in range(len(self.index)):
            if all(self.data[col].values[i] is not None for col in self.columns):
                valid_indices.append(i)
        
        new_data = {}
        for col in self.columns:
            new_data[col] = [self.data[col].values[i] for i in valid_indices]
        
        return DataFrame(new_data)
    
    def filter_rows(self, condition_func) -> 'DataFrame':
        """Filter rows based on condition function."""
        new_data = defaultdict(list)
        
        for i in range(len(self.index)):
            row = {col: self.data[col].values[i] for col in self.columns}
            if condition_func(row):
                for col in self.columns:
                    new_data[col].append(row[col])
        
        return DataFrame(dict(new_data))
    
    def apply(self, func, column: str = None) -> Union['DataFrame', List[Any]]:
        """Apply function to DataFrame or specific column."""
        if column:
            if column not in self.columns:
                raise KeyError(f"Column '{column}' not found")
            return [func(x) for x in self.data[column].values]
        
        # Apply to each row
        results = []
        for i in range(len(self.index)):
            row = {col: self.data[col].values[i] for col in self.columns}
            results.append(func(row))
        return results
    
    def merge(self, other: 'DataFrame', on: str, how: str = 'inner') -> 'DataFrame':
        """Merge two DataFrames."""
        if on not in self.columns or on not in other.columns:
            raise KeyError(f"Merge key '{on}' not found in both DataFrames")
        
        # Create lookup for other DataFrame
        other_lookup = {}
        for i, val in enumerate(other.data[on].values):
            if val not in other_lookup:
                other_lookup[val] = []
            other_lookup[val].append(i)
        
        merged_data = defaultdict(list)
        
        for i, key_val in enumerate(self.data[on].values):
            if key_val in other_lookup:
                for other_idx in other_lookup[key_val]:
                    # Add all columns from left DataFrame
                    for col in self.columns:
                        merged_data[col].append(self.data[col].values[i])
                    
                    # Add columns from right DataFrame (excluding merge key)
                    for col in other.columns:
                        if col != on:
                            new_col = f"{col}_right" if col in self.columns else col
                            merged_data[new_col].append(other.data[col].values[other_idx])
            elif how == 'left':
                # Add left row with None for right columns
                for col in self.columns:
                    merged_data[col].append(self.data[col].values[i])
                for col in other.columns:
                    if col != on:
                        new_col = f"{col}_right" if col in self.columns else col
                        merged_data[new_col].append(None)
        
        return DataFrame(dict(merged_data))
    
    def to_dict(self) -> Dict[str, List[Any]]:
        """Convert DataFrame to dictionary."""
        return {col: self.data[col].values for col in self.columns}
    
    def to_csv(self, filename: str) -> None:
        """Save DataFrame to CSV file."""
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(self.columns)
            
            # Write data rows
            for i in range(len(self.index)):
                row = [self.data[col].values[i] for col in self.columns]
                writer.writerow(row)
    
    @classmethod
    def from_csv(cls, filename: str) -> 'DataFrame':
        """Load DataFrame from CSV file."""
        data = defaultdict(list)
        
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            
            for row in reader:
                for i, value in enumerate(row):
                    # Try to convert to number
                    try:
                        value = float(value)
                        if value.is_integer():
                            value = int(value)
                    except ValueError:
                        pass  # Keep as string
                    
                    data[headers[i]].append(value)
        
        return cls(dict(data))
    
    def __getitem__(self, key):
        """Get column or subset of DataFrame."""
        if isinstance(key, str):
            # Return single column
            return self.data[key].values
        elif isinstance(key, list):
            # Return subset of columns
            new_data = {col: self.data[col].values for col in key if col in self.columns}
            return DataFrame(new_data)
        
        raise KeyError(f"Invalid key: {key}")
    
    def __str__(self):
        """String representation of DataFrame."""
        lines = []
        
        # Header
        header = "   " + "  ".join(f"{col:>10}" for col in self.columns)
        lines.append(header)
        
        # Data rows (show first 5 and last 2 if more than 7 rows)
        num_rows = len(self.index)
        if num_rows <= 7:
            indices = list(range(num_rows))
        else:
            indices = list(range(5)) + list(range(num_rows - 2, num_rows))
            
        for i in indices:
            if i == 5 and num_rows > 7:
                lines.append("   " + "  ".join("..." for _ in self.columns))
            
            row_data = []
            for col in self.columns:
                val = self.data[col].values[i]
                if val is None:
                    row_data.append("None")
                else:
                    row_data.append(str(val))
            
            row = f"{i:2d} " + "  ".join(f"{val:>10}" for val in row_data)
            lines.append(row)
        
        lines.append(f"\n[{num_rows} rows x {len(self.columns)} columns]")
        return "\n".join(lines)

# ==============================================================================
# DATA VISUALIZATION CONCEPTS
# ==============================================================================

class DataVisualizer:
    """
    Simplified visualization concepts demonstrating matplotlib/seaborn patterns.
    Shows data preparation and analysis patterns used in visualization.
    """
    
    @staticmethod
    def prepare_histogram_data(data: List[float], bins: int = 10) -> Dict[str, List]:
        """Prepare data for histogram (like matplotlib.hist)."""
        if not data:
            return {'counts': [], 'bins': []}
        
        min_val, max_val = min(data), max(data)
        bin_width = (max_val - min_val) / bins
        
        bin_edges = [min_val + i * bin_width for i in range(bins + 1)]
        counts = [0] * bins
        
        for value in data:
            bin_index = min(int((value - min_val) / bin_width), bins - 1)
            counts[bin_index] += 1
        
        return {
            'counts': counts,
            'bin_edges': bin_edges,
            'bin_centers': [(bin_edges[i] + bin_edges[i + 1]) / 2 for i in range(bins)]
        }
    
    @staticmethod
    def calculate_correlation_matrix(df: DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate correlation matrix for numeric columns."""
        numeric_cols = [col for col in df.columns if df.data[col].dtype == 'numeric']
        correlation_matrix = {}
        
        for col1 in numeric_cols:
            correlation_matrix[col1] = {}
            values1 = [v for v in df.data[col1].values if v is not None]
            
            for col2 in numeric_cols:
                values2 = [v for v in df.data[col2].values if v is not None]
                
                # Calculate Pearson correlation coefficient
                if len(values1) == len(values2) and len(values1) > 1:
                    mean1, mean2 = statistics.mean(values1), statistics.mean(values2)
                    
                    numerator = sum((x - mean1) * (y - mean2) for x, y in zip(values1, values2))
                    
                    sum_sq1 = sum((x - mean1) ** 2 for x in values1)
                    sum_sq2 = sum((y - mean2) ** 2 for y in values2)
                    
                    denominator = math.sqrt(sum_sq1 * sum_sq2)
                    
                    correlation = numerator / denominator if denominator != 0 else 0
                    correlation_matrix[col1][col2] = correlation
                else:
                    correlation_matrix[col1][col2] = 0
        
        return correlation_matrix
    
    @staticmethod
    def prepare_scatter_plot_data(x_data: List[float], y_data: List[float]) -> Dict[str, Any]:
        """Prepare scatter plot data and calculate trend line."""
        if len(x_data) != len(y_data) or len(x_data) < 2:
            return {'x': x_data, 'y': y_data, 'trend_line': None}
        
        # Calculate linear regression line (y = mx + b)
        n = len(x_data)
        sum_x = sum(x_data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_data, y_data))
        sum_x2 = sum(x * x for x in x_data)
        
        # Slope (m) and intercept (b)
        denominator = n * sum_x2 - sum_x * sum_x
        if denominator != 0:
            m = (n * sum_xy - sum_x * sum_y) / denominator
            b = (sum_y - m * sum_x) / n
            
            # Generate trend line points
            min_x, max_x = min(x_data), max(x_data)
            trend_x = [min_x, max_x]
            trend_y = [m * x + b for x in trend_x]
            
            # Calculate R-squared
            y_mean = statistics.mean(y_data)
            ss_tot = sum((y - y_mean) ** 2 for y in y_data)
            ss_res = sum((y_data[i] - (m * x_data[i] + b)) ** 2 for i in range(n))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            trend_line = {
                'x': trend_x,
                'y': trend_y,
                'slope': m,
                'intercept': b,
                'r_squared': r_squared
            }
        else:
            trend_line = None
        
        return {
            'x': x_data,
            'y': y_data,
            'trend_line': trend_line
        }

# ==============================================================================
# STATISTICAL ANALYSIS
# ==============================================================================

class StatisticalAnalyzer:
    """Statistical analysis functions commonly used in data science."""
    
    @staticmethod
    def descriptive_statistics(data: List[float]) -> Dict[str, float]:
        """Calculate comprehensive descriptive statistics."""
        if not data:
            return {}
        
        cleaned_data = [x for x in data if x is not None]
        if not cleaned_data:
            return {}
        
        n = len(cleaned_data)
        sorted_data = sorted(cleaned_data)
        
        stats = {
            'count': n,
            'mean': statistics.mean(cleaned_data),
            'median': statistics.median(cleaned_data),
            'mode': statistics.mode(cleaned_data) if n > 0 else None,
            'std': statistics.stdev(cleaned_data) if n > 1 else 0,
            'var': statistics.variance(cleaned_data) if n > 1 else 0,
            'min': min(cleaned_data),
            'max': max(cleaned_data),
            'range': max(cleaned_data) - min(cleaned_data),
            'q1': statistics.quantiles(cleaned_data, n=4)[0] if n >= 4 else cleaned_data[0],
            'q3': statistics.quantiles(cleaned_data, n=4)[2] if n >= 4 else cleaned_data[-1],
            'skewness': StatisticalAnalyzer._calculate_skewness(cleaned_data),
            'kurtosis': StatisticalAnalyzer._calculate_kurtosis(cleaned_data)
        }
        
        stats['iqr'] = stats['q3'] - stats['q1']
        
        return stats
    
    @staticmethod
    def _calculate_skewness(data: List[float]) -> float:
        """Calculate skewness (measure of asymmetry)."""
        if len(data) < 3:
            return 0
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data)
        
        if std_val == 0:
            return 0
        
        n = len(data)
        skewness = sum(((x - mean_val) / std_val) ** 3 for x in data) / n
        return skewness
    
    @staticmethod
    def _calculate_kurtosis(data: List[float]) -> float:
        """Calculate kurtosis (measure of tail heaviness)."""
        if len(data) < 4:
            return 0
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data)
        
        if std_val == 0:
            return 0
        
        n = len(data)
        kurtosis = sum(((x - mean_val) / std_val) ** 4 for x in data) / n - 3
        return kurtosis
    
    @staticmethod
    def outlier_detection_iqr(data: List[float], k: float = 1.5) -> Dict[str, Any]:
        """Detect outliers using IQR method."""
        if len(data) < 4:
            return {'outliers': [], 'lower_bound': None, 'upper_bound': None}
        
        cleaned_data = [x for x in data if x is not None]
        quartiles = statistics.quantiles(cleaned_data, n=4)
        q1, q3 = quartiles[0], quartiles[2]
        iqr = q3 - q1
        
        lower_bound = q1 - k * iqr
        upper_bound = q3 + k * iqr
        
        outliers = [x for x in cleaned_data if x < lower_bound or x > upper_bound]
        
        return {
            'outliers': outliers,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outlier_indices': [i for i, x in enumerate(data) if x in outliers]
        }
    
    @staticmethod
    def hypothesis_testing_t_test(sample1: List[float], sample2: List[float]) -> Dict[str, float]:
        """Simplified two-sample t-test implementation."""
        if len(sample1) < 2 or len(sample2) < 2:
            return {'error': 'Insufficient data for t-test'}
        
        n1, n2 = len(sample1), len(sample2)
        mean1, mean2 = statistics.mean(sample1), statistics.mean(sample2)
        var1, var2 = statistics.variance(sample1), statistics.variance(sample2)
        
        # Pooled standard deviation
        pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
        pooled_std = math.sqrt(pooled_var)
        
        # Standard error
        se = pooled_std * math.sqrt(1/n1 + 1/n2)
        
        # t-statistic
        t_stat = (mean1 - mean2) / se if se != 0 else 0
        
        # Degrees of freedom
        df = n1 + n2 - 2
        
        return {
            't_statistic': t_stat,
            'degrees_of_freedom': df,
            'mean_difference': mean1 - mean2,
            'standard_error': se,
            'pooled_std': pooled_std
        }

# ==============================================================================
# DATA PREPROCESSING
# ==============================================================================

class DataPreprocessor:
    """Data preprocessing utilities commonly used in data science."""
    
    @staticmethod
    def normalize_minmax(data: List[float]) -> List[float]:
        """Min-Max normalization to scale data to [0, 1]."""
        if not data:
            return data
        
        min_val, max_val = min(data), max(data)
        if min_val == max_val:
            return [0.5] * len(data)  # All values are the same
        
        return [(x - min_val) / (max_val - min_val) for x in data]
    
    @staticmethod
    def standardize_zscore(data: List[float]) -> List[float]:
        """Z-score standardization (mean=0, std=1)."""
        if len(data) < 2:
            return data
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data)
        
        if std_val == 0:
            return [0] * len(data)
        
        return [(x - mean_val) / std_val for x in data]
    
    @staticmethod
    def encode_categorical(categories: List[str]) -> Dict[str, Any]:
        """One-hot encoding for categorical variables."""
        unique_categories = list(set(categories))
        
        # Create binary matrix
        encoded = {}
        for category in unique_categories:
            encoded[f'is_{category}'] = [1 if cat == category else 0 for cat in categories]
        
        return {
            'encoded_data': encoded,
            'original_categories': categories,
            'unique_categories': unique_categories,
            'category_mapping': {cat: i for i, cat in enumerate(unique_categories)}
        }
    
    @staticmethod
    def handle_missing_values(data: List[Any], strategy: str = 'mean') -> List[Any]:
        """Handle missing values with various strategies."""
        if not data:
            return data
        
        # Separate None values from actual data
        valid_data = [x for x in data if x is not None]
        
        if not valid_data:
            return data  # All values are None
        
        if strategy == 'mean':
            # Only for numeric data
            if all(isinstance(x, (int, float)) for x in valid_data):
                fill_value = statistics.mean(valid_data)
            else:
                fill_value = max(set(valid_data), key=valid_data.count)  # Mode for non-numeric
        elif strategy == 'median':
            if all(isinstance(x, (int, float)) for x in valid_data):
                fill_value = statistics.median(valid_data)
            else:
                fill_value = max(set(valid_data), key=valid_data.count)
        elif strategy == 'mode':
            fill_value = max(set(valid_data), key=valid_data.count)
        elif strategy == 'forward_fill':
            # Forward fill strategy
            result = []
            last_valid = valid_data[0] if valid_data else None
            for value in data:
                if value is not None:
                    last_valid = value
                    result.append(value)
                else:
                    result.append(last_valid)
            return result
        else:
            fill_value = 0  # Default
        
        return [fill_value if x is None else x for x in data]
    
    @staticmethod
    def create_polynomial_features(data: List[float], degree: int = 2) -> Dict[str, List[float]]:
        """Create polynomial features."""
        features = {'x1': data}  # Original feature
        
        for d in range(2, degree + 1):
            features[f'x{d}'] = [x ** d for x in data]
        
        # Interaction terms for multiple original features (simplified)
        if degree >= 2:
            features['x1_squared'] = [x ** 2 for x in data]
        
        return features
    
    @staticmethod
    def create_time_features(timestamps: List[datetime]) -> Dict[str, List[int]]:
        """Extract time-based features from datetime objects."""
        features = {
            'year': [dt.year for dt in timestamps],
            'month': [dt.month for dt in timestamps],
            'day': [dt.day for dt in timestamps],
            'hour': [dt.hour for dt in timestamps],
            'day_of_week': [dt.weekday() for dt in timestamps],  # 0=Monday, 6=Sunday
            'day_of_year': [dt.timetuple().tm_yday for dt in timestamps],
            'is_weekend': [1 if dt.weekday() >= 5 else 0 for dt in timestamps],
            'quarter': [((dt.month - 1) // 3) + 1 for dt in timestamps]
        }
        
        return features

# ==============================================================================
# DEMONSTRATION AND EXAMPLES
# ==============================================================================

def demonstrate_numpy_like_operations():
    """Demonstrate NumPy-like array operations."""
    print("NumPy-like Array Operations Demonstration")
    print("=" * 50)
    
    # Create arrays
    arr1 = NDArray([1, 2, 3, 4, 5])
    arr2 = NDArray([2, 4, 6, 8, 10])
    
    print(f"Array 1: {arr1}")
    print(f"Array 2: {arr2}")
    print(f"Shape: {arr1.shape}, Size: {arr1.size}")
    
    # Basic operations
    print(f"\nAddition: {arr1 + arr2}")
    print(f"Scalar multiplication: {arr1 * 3}")
    print(f"Mean: {arr1.mean():.2f}")
    print(f"Standard deviation: {arr1.std():.2f}")
    print(f"Sum: {arr1.sum()}")
    
    # 2D array operations
    matrix_data = [[1, 2, 3], [4, 5, 6]]
    matrix = NDArray(matrix_data)
    print(f"\n2D Array: {matrix}")
    print(f"Shape: {matrix.shape}")
    print(f"Column means: {matrix.mean(axis=0)}")
    
    # Matrix multiplication
    mat1 = NDArray([[1, 2], [3, 4]])
    mat2 = NDArray([[5, 6], [7, 8]])
    print(f"\nMatrix 1:\n{mat1}")
    print(f"Matrix 2:\n{mat2}")
    print(f"Dot product:\n{mat1.dot(mat2)}")

def demonstrate_dataframe_operations():
    """Demonstrate pandas-like DataFrame operations."""
    print("\nDataFrame Operations Demonstration")
    print("=" * 50)
    
    # Create sample data
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
        'age': [25, 30, 35, 28, 32],
        'salary': [50000, 60000, 70000, 55000, 65000],
        'department': ['IT', 'HR', 'IT', 'Finance', 'IT'],
        'bonus': [5000, None, 7000, 4000, 6000]
    }
    
    df = DataFrame(data)
    print("Original DataFrame:")
    print(df)
    
    # Basic operations
    print(f"\nDataFrame shape: {df.shape}")
    print("\nDataFrame info:")
    info = df.info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Descriptive statistics
    print("\nDescriptive statistics:")
    stats = df.describe()
    for col, col_stats in stats.items():
        print(f"\n{col}:")
        for stat, value in col_stats.items():
            print(f"  {stat}: {value:.2f}")
    
    # Data manipulation
    print("\nFirst 3 rows:")
    print(df.head(3))
    
    print("\nSorted by salary (descending):")
    sorted_df = df.sort_values('salary', ascending=False)
    print(sorted_df)
    
    # Filtering
    print("\nIT department employees:")
    it_employees = df.filter_rows(lambda row: row['department'] == 'IT')
    print(it_employees)
    
    # Grouping
    print("\nGroup by department:")
    groups = df.groupby('department')
    for dept, group_df in groups.items():
        print(f"\n{dept} department:")
        print(f"  Count: {group_df.shape[0]}")
        if 'salary' in group_df.columns:
            avg_salary = statistics.mean([s for s in group_df['salary'] if s is not None])
            print(f"  Average salary: ${avg_salary:,.2f}")
    
    # Handle missing values
    print("\nFilling missing bonus values with mean:")
    filled_df = df.fillna(value=5500)  # Approximate mean of existing bonuses
    print(filled_df)

def demonstrate_statistical_analysis():
    """Demonstrate statistical analysis capabilities."""
    print("\nStatistical Analysis Demonstration")
    print("=" * 50)
    
    # Generate sample data
    random.seed(42)
    sample_data = [random.gauss(50, 15) for _ in range(100)]
    sample_data.extend([random.gauss(55, 10) for _ in range(50)])  # Different distribution
    
    # Descriptive statistics
    stats = StatisticalAnalyzer.descriptive_statistics(sample_data)
    print("Descriptive Statistics:")
    for stat, value in stats.items():
        if isinstance(value, float):
            print(f"  {stat}: {value:.3f}")
        else:
            print(f"  {stat}: {value}")
    
    # Outlier detection
    outlier_info = StatisticalAnalyzer.outlier_detection_iqr(sample_data)
    print(f"\nOutlier Detection (IQR method):")
    print(f"  Number of outliers: {len(outlier_info['outliers'])}")
    print(f"  Lower bound: {outlier_info['lower_bound']:.2f}")
    print(f"  Upper bound: {outlier_info['upper_bound']:.2f}")
    
    # Histogram data preparation
    hist_data = DataVisualizer.prepare_histogram_data(sample_data, bins=15)
    print(f"\nHistogram preparation:")
    print(f"  Bins: {len(hist_data['counts'])}")
    print(f"  Max count: {max(hist_data['counts'])}")
    print(f"  Data range: {min(sample_data):.2f} to {max(sample_data):.2f}")

def demonstrate_data_preprocessing():
    """Demonstrate data preprocessing techniques."""
    print("\nData Preprocessing Demonstration")
    print("=" * 50)
    
    # Sample data with various issues
    numeric_data = [10, 20, None, 30, 100, 25, 15]  # Has missing value and outlier
    categorical_data = ['A', 'B', 'A', 'C', 'B', 'A', 'C']
    
    print("Original numeric data:", numeric_data)
    
    # Handle missing values
    cleaned_data = DataPreprocessor.handle_missing_values(numeric_data, strategy='mean')
    print("After handling missing values (mean):", cleaned_data)
    
    # Normalization
    normalized_data = DataPreprocessor.normalize_minmax(cleaned_data)
    print("Min-Max normalized:", [f"{x:.3f}" for x in normalized_data])
    
    # Standardization
    standardized_data = DataPreprocessor.standardize_zscore(cleaned_data)
    print("Z-score standardized:", [f"{x:.3f}" for x in standardized_data])
    
    # Categorical encoding
    print(f"\nOriginal categorical data: {categorical_data}")
    encoded_result = DataPreprocessor.encode_categorical(categorical_data)
    print("One-hot encoded:")
    for feature, values in encoded_result['encoded_data'].items():
        print(f"  {feature}: {values}")
    
    # Time features
    timestamps = [
        datetime(2024, 1, 15, 10, 30),
        datetime(2024, 6, 20, 14, 45),
        datetime(2024, 12, 25, 9, 15)
    ]
    time_features = DataPreprocessor.create_time_features(timestamps)
    print(f"\nTime feature extraction:")
    for feature, values in time_features.items():
        print(f"  {feature}: {values}")
    
    # Polynomial features
    simple_data = [1, 2, 3, 4, 5]
    poly_features = DataPreprocessor.create_polynomial_features(simple_data, degree=3)
    print(f"\nPolynomial features (degree 3):")
    for feature, values in poly_features.items():
        print(f"  {feature}: {values}")

def main():
    """Run all data science demonstrations."""
    print("Data Science Fundamentals - Comprehensive Demonstration")
    print("=" * 70)
    
    demonstrate_numpy_like_operations()
    demonstrate_dataframe_operations()
    demonstrate_statistical_analysis()
    demonstrate_data_preprocessing()
    
    print("\n" + "=" * 70)
    print("Data Science Concepts Covered:")
    print("- Array operations and linear algebra")
    print("- Data manipulation and analysis with DataFrames")
    print("- Statistical analysis and hypothesis testing")
    print("- Data preprocessing and feature engineering")
    print("- Missing value handling and outlier detection")
    print("- Data visualization preparation")
    print("- Time series feature extraction")
    print("\nNext Steps for Real Projects:")
    print("- Install: numpy, pandas, matplotlib, seaborn, scipy, scikit-learn")
    print("- Use real libraries for production data science work")
    print("- Explore advanced topics: machine learning, deep learning, etc.")

if __name__ == "__main__":
    main()
