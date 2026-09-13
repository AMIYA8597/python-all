# Embeddings, Vector Databases, and Semantic Search

## 1. Prerequisites
- **Linear Algebra:** Understanding of vectors, dot products, and multi-dimensional space.
- **NLP Basics:** Understanding that machines need text converted to numbers (tokenization).

## 2. Learning Objectives
- Understand what an embedding is and why it's a foundational breakthrough in AI.
- Learn how to calculate and interpret similarity metrics (Cosine Similarity, Dot Product, Euclidean Distance).
- Understand the difference between Dense Retrieval (Semantic Search) and Sparse Retrieval (Lexical Search).
- Learn how Vector Databases work and why Approximate Nearest Neighbor (ANN) is required for scale.

## 3. Why This Topic Exists
Computers do not understand English. They understand numbers. Historically, we mapped words to numbers using dictionaries (e.g., Apple=1, Banana=2). But in that system, the number 1 and 2 have no mathematical relationship representing the fact that they are both fruits.
**Embeddings** solve this by mapping words (or sentences, images, audio) into a continuous, high-dimensional vector space where the geometric distance between vectors directly correlates to their semantic similarity.

## 4. Real-World Motivation
- **Google Search:** Modern search engines use embeddings to understand the *intent* of your query, not just matching keywords.
- **Recommendation Systems:** Spotify embeds songs and users into the same vector space. If a user's vector is close to a song's vector, it gets recommended.
- **RAG (Retrieval-Augmented Generation):** Finding the exact paragraph in a million-page corporate wiki that answers a user's natural language question.

## 5. Beginner Intuition
Imagine mapping animals on a 2D graph. 
- X-axis is "Size" (0=tiny, 10=huge). 
- Y-axis is "Domestication" (0=wild, 10=pet).

- **Cat**: `[2, 9]`
- **Dog**: `[4, 9]`
- **Lion**: `[8, 1]`
- **Mouse**: `[1, 1]`

On this graph, the point for "Cat" is very close to "Dog", but far from "Lion". 
Modern LLM embeddings do exactly this, but instead of 2 dimensions created by humans, they use 1536 dimensions (or more) discovered automatically by a neural network reading the entire internet!

## 6. Formal Explanation

### Word2Vec to Contextual Embeddings
Early embeddings (Word2Vec, GloVe) assigned one fixed vector to every word. Problem: "Bank" (river) and "Bank" (money) shared the same vector.
Modern embeddings (like OpenAI's `text-embedding-3-small`, or BERT-based models) generate **contextual embeddings**. The vector for the entire sentence is calculated, meaning "Bank" gets a different vector depending on the surrounding words.

### The Magic Equation
Because these vectors capture meaning, you can do semantic arithmetic:
`Vector("King") - Vector("Man") + Vector("Woman") ≈ Vector("Queen")`

## 7. Mathematics of Similarity

How do we measure "closeness" between two vectors $A$ and $B$?

### 1. Dot Product
Calculates the projection of one vector onto another.
Formula: $A \cdot B = \sum_{i=1}^n A_i B_i$
If vectors are normalized (length of 1), Dot Product is extremely fast and equivalent to Cosine Similarity.

### 2. Cosine Similarity
Measures the *angle* between two vectors, regardless of their magnitude (length).
Formula: $\cos(\theta) = \frac{A \cdot B}{||A|| ||B||}$
- **1**: Vectors point in the exact same direction (identical meaning).
- **0**: Vectors are orthogonal (unrelated).
- **-1**: Vectors point in opposite directions (opposite meaning).

### 3. Euclidean Distance (L2)
Measures the straight-line distance between the endpoints of the vectors.
Formula: $d(A, B) = \sqrt{\sum_{i=1}^n (A_i - B_i)^2}$

## 8. Semantic Search vs. Lexical Search
- **Lexical (Keyword) Search (BM25):** If you search "automobile", it only looks for documents containing the exact word "automobile". It misses documents that only say "car".
- **Semantic Search:** You search "automobile". The query is embedded into a vector. The database finds documents with vectors close to the query. Since "car" and "automobile" have nearly identical vectors, it finds the document perfectly.

## 9. Vector Databases & ANN

If you have 100 documents, finding the closest vector to a query is easy: just calculate the cosine similarity against all 100 (k-Nearest Neighbors, or kNN). 
But if you have 1 billion documents, calculating 1 billion dot products for every search query is impossible in real-time.

**Vector Databases** (Pinecone, Milvus, Qdrant, Chroma, FAISS) solve this using **Approximate Nearest Neighbor (ANN)** algorithms.
- **HNSW (Hierarchical Navigable Small World):** The most common algorithm. It builds a multi-layered graph of vectors. It navigates the top (sparse) layer to find the general neighborhood, then drops down to denser layers to find the exact closest vectors. 
- **Trade-off:** ANN sacrifices a tiny fraction of accuracy (it might miss the true #1 closest vector 1% of the time) to achieve a 10,000x speedup.

## 10. Code Example: Embeddings and Cosine Similarity from Scratch

```python
import numpy as np

def cosine_similarity(vec_a, vec_b):
    # Dot product
    dot = np.dot(vec_a, vec_b)
    # Magnitudes
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    # Cosine
    return dot / (norm_a * norm_b)

# Simulated 3D Embeddings for intuition
# Dim 1: Royalty, Dim 2: Gender (1=M, -1=F), Dim 3: Age
vec_king = np.array([0.9, 1.0, 0.5])
vec_man = np.array([0.1, 1.0, 0.5])
vec_woman = np.array([0.1, -1.0, 0.5])
vec_queen = np.array([0.9, -1.0, 0.5])

print("Similarity (King, Man):", cosine_similarity(vec_king, vec_man))
print("Similarity (King, Queen):", cosine_similarity(vec_king, vec_queen))

# Vector Arithmetic: King - Man + Woman
calculated_queen = vec_king - vec_man + vec_woman
print("Calculated Vector:", calculated_queen)
print("Similarity (Calculated, Actual Queen):", cosine_similarity(calculated_queen, vec_queen))
```

## 11. Common Mistakes
1. **Comparing embeddings from different models:** You cannot compare an OpenAI embedding to a HuggingFace embedding. They exist in completely different vector spaces.
2. **Ignoring normalization:** If your vector database uses Dot Product for speed, but your embeddings are not normalized to a length of 1, documents with longer vectors (larger magnitudes) will unfairly dominate the search results.
3. **Using embeddings for exact matching:** Semantic search is bad at finding exact IDs, part numbers, or exact phrases. Use Hybrid Search (Semantic + BM25) for production apps.

## 12. Active Recall
1. Why does semantic search succeed where keyword search fails?
2. What is the mathematical difference between Cosine Similarity and Euclidean Distance?
3. Why do we need Vector Databases instead of just using NumPy arrays?
4. What is HNSW?

## 13. Interview Questions
**Q1: Explain the curse of dimensionality in the context of embeddings.**
*Answer:* As the number of dimensions increases (e.g., 1536), the volume of the space grows so fast that the available data becomes sparse. More problematically, in extremely high dimensions, the distance between any two random points tends to become almost identical, making similarity metrics less discriminative. Modern models carefully balance dimensionality (enough to capture nuance, not so much that distance breaks down).

**Q2: If you need to scale a vector search to 100 million documents, what architectural choices do you make?**
*Answer:* I would use a dedicated Vector DB with an HNSW index. To save RAM, I would use Product Quantization (PQ) or Scalar Quantization to compress the float32 vectors down to int8 or smaller, trading a small amount of recall accuracy for massive memory savings and search speed.
