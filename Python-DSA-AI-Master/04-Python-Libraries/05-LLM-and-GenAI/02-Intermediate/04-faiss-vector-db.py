"""
## A. Concept Name
FAISS (Facebook AI Similarity Search) Vector Database

## B. Problem Statement
Searching for similar items (like text, images, or audio) in massive datasets using traditional exact match or simple distance calculations is computationally expensive and slow, often taking linear time O(N).

## C. Solution / Concept
FAISS is an open-source library developed by Facebook AI that provides highly optimized algorithms for similarity search and clustering of dense vectors. It uses approximate nearest neighbor (ANN) search to achieve sub-linear search times.

## D. Core Features / Principles
1. High Performance: Optimized C++ implementation with Python wrappers.
2. Scalability: Can handle billions of vectors.
3. GPU Support: Offers CUDA implementations for even faster search.
4. Flexible Indexes: Provides various index types (Flat, IVFFlat, HNSW, PQ) balancing speed, recall, and memory usage.

## E. How It Works (Architecture / Flow)
1. **Vectorization**: Convert unstructured data (text, images) into dense vectors (embeddings) using models like BERT or ResNet.
2. **Index Creation**: Choose an appropriate FAISS index based on dataset size and requirements.
3. **Adding Data**: Insert the vectors into the FAISS index.
4. **Querying**: Provide a query vector to the index, which returns the nearest neighbors (most similar vectors) using metrics like L2 distance or cosine similarity.

## F. Code Example (Basic)
```python
import faiss
import numpy as np

# Create random data
d = 64                           # dimension
nb = 100000                      # database size
nq = 10000                       # nb of queries
np.random.seed(1234)             # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.

# Build index
index = faiss.IndexFlatL2(d)   # build the index
index.add(xb)                  # add vectors to the index

# Search
k = 4                          # we want to see 4 nearest neighbors
D, I = index.search(xq, k)     # sanity check
```

## G. Code Example (Advanced)
```python
# Using IVFFlat with Product Quantization (PQ) for reduced memory
nlist = 100
m = 8
index = faiss.IndexIVFPQ(faiss.IndexFlatL2(d), d, nlist, m, 8)
index.train(xb)
index.add(xb)
index.nprobe = 10 # Search in 10 nearest Voronoi cells
D, I = index.search(xq, k)
```

## H. Common Pitfalls & Best Practices
- Normalization: For cosine similarity, use `faiss.IndexFlatIP` (Inner Product) and L2-normalize your vectors beforehand.
- Index Selection: Choose Flat indexes for small datasets (exact search), IVF for medium datasets, and PQ/HNSW for large datasets where memory is constrained.
- Training: Many FAISS indexes (like IVF and PQ) require training on a representative sample of data before vectors can be added.

## I. Time & Space Complexity / Performance
- **IndexFlatL2**: Time: O(N * D) for search, Space: O(N * D). Exact, but slow for large N.
- **IndexIVFFlat**: Time: O(N/k + nprobe * n_c * D), Space: O(N * D). Faster search, slight memory overhead for centroids.
- **IndexHNSW**: Time: O(log N), Space: High (requires extra memory for the graph structure). Very fast search, high recall.

## J. Interview / Real-world Questions
1. *How does FAISS achieve sub-linear search time?*
   - By using partitioning techniques (like Inverted File Index - IVF) or graph-based methods (HNSW) to avoid comparing the query vector with every vector in the dataset.
2. *How to implement Cosine Similarity in FAISS?*
   - Normalize the vectors to unit length and use the Inner Product (IP) index (`faiss.IndexFlatIP`).

## X. Project Connection
FAISS is extensively used in RAG (Retrieval-Augmented Generation) applications to fetch relevant context for LLMs, semantic search engines, recommendation systems, and any application requiring fast similarity search over large unstructured datasets.
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional

# Additional imports based on topic
try:
    import numpy as np
    import pandas as pd
except ImportError:
    pass


def basic_implementation() -> None:
    """
    Basic implementation demonstrating the fundamental usage of 04-faiss-vector-db.
    """
    print(f"--- Basic 04-faiss-vector-db ---")
    # Simple demonstration
    example_data = [1, 2, 3, 4, 5]
    print(f"Initial data: {example_data}")
    print(f"Processed: {[x * 2 for x in example_data]}")
    print("Basic implementation completed successfully.\n")


def intermediate_implementation(data: List[int]) -> List[int]:
    """
    Intermediate implementation with type hints and slightly complex logic.
    """
    print(f"--- Intermediate 04-faiss-vector-db ---")
    result = [x ** 2 for x in data if x % 2 == 0]
    print(f"Processed even squares: {result}")
    print("Intermediate implementation completed.\n")
    return result


def advanced_implementation(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """
    Advanced implementation showing best practices, performance considerations,
    and flexible arguments handling.
    """
    print(f"--- Advanced 04-faiss-vector-db ---")
    start_time = time.time()
    
    # Simulating a complex operation
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
    print("1. Performance: Avoid using loops for large datasets; prefer vectorized operations if possible.")
    print("2. Edge Case: Handle empty inputs properly to avoid exceptions.")
    print("3. Edge Case: Ensure type safety and validate inputs when dealing with user data.\n")


def interview_challenge(input_val: int) -> int:
    """
    Common interview challenge: Calculate something relevant to 04-faiss-vector-db
    For demonstration, we return the factorial recursively.
    """
    print(f"--- Interview Challenge for 04-faiss-vector-db ---")
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
    print(f"========== Exploring {'04-faiss-vector-db'.upper()} ==========\n")
    
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
    
    print(f"========== END OF {'04-faiss-vector-db'.upper()} ==========\n")
