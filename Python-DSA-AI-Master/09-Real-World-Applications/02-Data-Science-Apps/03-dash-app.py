"""
Module: Data Science Dashboard Applications

Learning Objectives:
1. Understand the architecture of a Data Science dashboard backend.
2. Implement robust data aggregation and caching layers for frontend consumption.
3. Design object-oriented data services that feed UI components (like Dash, Streamlit).
4. Learn how to handle filtering and metric computation efficiently.

Concept Explanation:
Dashboards are the primary way data scientists communicate results and insights to stakeholders. 
While tools like Plotly Dash or Streamlit handle the frontend rendering, the backend must 
efficiently query, aggregate, and serve the data. A poorly designed backend will lead to a 
sluggish dashboard, especially when dealing with millions of rows. The focus here is on 
building a robust, memory-efficient data provider layer that caches expensive computations 
and handles complex filtering.

===========================================================================
Basic Implementation
===========================================================================
The basic approach often involves reloading and recomputing data every time a user 
changes a filter, which is highly inefficient.
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import statistics

# ---------------------------------------------------------------------------
# Basic Approach
# ---------------------------------------------------------------------------
def get_dashboard_metrics_basic(data: List[Dict[str, Any]], category_filter: str) -> Dict[str, float]:
    """
    Basic function to calculate metrics for a dashboard.
    Inefficient because it iterates through the entire dataset on every call.
    """
    filtered_data = [row for row in data if row['category'] == category_filter]
    
    if not filtered_data:
        return {"mean": 0.0, "max": 0.0, "count": 0}
        
    values = [row['value'] for row in filtered_data]
    return {
        "mean": sum(values) / len(values),
        "max": max(values),
        "count": len(values)
    }


# ===========================================================================
# Professional Implementation
# ===========================================================================

@dataclass
class DataPoint:
    """Represents a single row of data in our system."""
    id: int
    category: str
    timestamp: float
    value: float

class DashboardBackend:
    """
    Professional, optimized backend for a Data Science dashboard.
    
    Features:
    - Pre-indexes data by category for O(1) retrieval instead of O(N) scanning.
    - Uses caching for expensive aggregations.
    - Type-hinted and highly structured.
    """
    
    def __init__(self, raw_data: List[DataPoint]):
        self._raw_data = raw_data
        # Index data by category during initialization (O(N) time, O(N) space)
        self._category_index: Dict[str, List[DataPoint]] = defaultdict(list)
        self._build_index()
        
        # Simple cache for aggregated metrics
        self._metrics_cache: Dict[str, Dict[str, float]] = {}

    def _build_index(self) -> None:
        """Internal method to build indexes for faster querying."""
        for point in self._raw_data:
            self._category_index[point.category].append(point)

    def get_metrics_for_category(self, category: str) -> Dict[str, float]:
        """
        Retrieves aggregated metrics for a given category.
        Uses cached results if available to ensure sub-millisecond response times.
        """
        # Check cache first
        if category in self._metrics_cache:
            return self._metrics_cache[category]

        # Retrieve pre-filtered data in O(1) time
        filtered_data = self._category_index.get(category, [])
        
        if not filtered_data:
            result = {"mean": 0.0, "median": 0.0, "max": 0.0, "count": 0.0}
            self._metrics_cache[category] = result
            return result

        # Compute metrics
        values = [pt.value for pt in filtered_data]
        result = {
            "mean": sum(values) / len(values),
            "median": statistics.median(values),
            "max": max(values),
            "count": float(len(values))
        }
        
        # Store in cache
        self._metrics_cache[category] = result
        return result

    def get_time_series_data(self, category: str, downsample_factor: int = 1) -> List[Tuple[float, float]]:
        """
        Returns time-series data for rendering line charts.
        Implements a simple downsampling technique to avoid sending too many points to the UI.
        """
        filtered_data = self._category_index.get(category, [])
        # Sort by timestamp to ensure chronological order
        sorted_data = sorted(filtered_data, key=lambda x: x.timestamp)
        
        # Downsample: take every Nth point
        return [(pt.timestamp, pt.value) for pt in sorted_data[::downsample_factor]]


# ===========================================================================
# Complexity Analysis & Interview Challenge
# ===========================================================================
"""
Complexity Analysis:
- get_dashboard_metrics_basic: 
  Time Complexity: O(N) per query, where N is the total number of rows.
  Space Complexity: O(M) where M is the number of matching rows (creates a new list).

- DashboardBackend:
  Initialization Time: O(N) to build the index.
  Query Time (get_metrics_for_category): 
    - First call: O(M log M) if sorting is needed, or O(M) for basic stats, where M is category size.
    - Subsequent calls: O(1) due to caching.
  Space Complexity: O(N) for storing the index.

Interview Challenge:
Question: Your dashboard takes 10 seconds to load because the raw dataset has 50 million rows. 
          Memory is limited to 4GB. How would you redesign the backend?
Answer: 
1. Use an external database (like PostgreSQL or ClickHouse) or an OLAP engine (like DuckDB) 
   instead of loading everything into Python memory.
2. Pre-aggregate the data at the database level (e.g., daily summaries instead of raw events).
3. Implement a distributed cache (like Redis) for the aggregated results.
4. In Python, use generators or chunking if processing must be done locally.
"""

# ===========================================================================
# Example Usage & Tests
# ===========================================================================
if __name__ == "__main__":
    print("Testing Dashboard Backend...")
    
    # 1. Generate dummy data
    dataset = [
        DataPoint(id=1, category="A", timestamp=1.0, value=10.0),
        DataPoint(id=2, category="A", timestamp=2.0, value=20.0),
        DataPoint(id=3, category="B", timestamp=1.5, value=100.0),
        DataPoint(id=4, category="A", timestamp=3.0, value=15.0),
        DataPoint(id=5, category="B", timestamp=2.5, value=200.0),
    ]
    
    # 2. Test Basic
    raw_dicts = [{"category": p.category, "value": p.value} for p in dataset]
    basic_res = get_dashboard_metrics_basic(raw_dicts, "A")
    assert basic_res["count"] == 3
    assert basic_res["mean"] == 15.0
    
    # 3. Test Professional
    backend = DashboardBackend(dataset)
    
    # First call (computes and caches)
    metrics_a = backend.get_metrics_for_category("A")
    assert metrics_a["count"] == 3
    assert metrics_a["max"] == 20.0
    assert metrics_a["median"] == 15.0
    
    # Second call (returns cached O(1))
    metrics_a_cached = backend.get_metrics_for_category("A")
    assert metrics_a == metrics_a_cached
    
    # Test Time Series Downsampling
    ts_data = backend.get_time_series_data("A", downsample_factor=2)
    assert len(ts_data) == 2  # Takes 1st and 3rd element out of 3
    assert ts_data[0][1] == 10.0 # First value
    assert ts_data[1][1] == 15.0 # Third value
    
    print("All tests passed successfully!")
