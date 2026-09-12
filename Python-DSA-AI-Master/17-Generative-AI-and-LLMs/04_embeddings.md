# Embeddings, Vector Databases, and Semantic Search

To make language models understand text practically, we need a mathematical representation of words and sentences. This is where embeddings come in.

## 1. Embeddings
An embedding is a representation of data (text, images, audio) as a dense vector of real numbers. The key property of embeddings is that **semantically similar concepts are placed close together in the vector space.**

For example, the vector for "King" might be close to the vector for "Queen", and `Vector("King") - Vector("Man") + Vector("Woman") ≈ Vector("Queen")`.

### How are they created?
Embedding models (like OpenAI's `text-embedding-ada-002`, or open-source ones like `SentenceTransformers`) process text and output a fixed-size array of floats (e.g., 768 or 1536 dimensions).

## 2. Distance Metrics
To find similar texts, we calculate the distance between their embedding vectors.
- **Cosine Similarity:** Measures the angle between two vectors. (Range: -1 to 1. 1 means exactly the same direction). Widely used for text.
- **Euclidean Distance (L2):** Measures the straight-line distance between two points in the space.
- **Dot Product:** Magnitude and angle combined. Used often if vectors are normalized.

## 3. Vector Databases
When dealing with millions of documents, calculating the cosine similarity against every single document (Brute Force / KNN) is too slow.

**Vector Databases** (like Pinecone, Milvus, ChromaDB, FAISS) are specialized databases optimized for storing and querying these high-dimensional vectors efficiently.
They use **Approximate Nearest Neighbor (ANN)** algorithms (like HNSW - Hierarchical Navigable Small World) to perform sub-millisecond searches across huge datasets, trading a tiny bit of accuracy for massive speed gains.

## 4. Semantic Search
Traditional search relies on keyword matching (Lexical search, e.g., BM25). If you search for "automobile", it won't find documents containing "car" unless they also contain "automobile".

**Semantic Search** uses embeddings. The query is converted into an embedding, and the vector DB returns the closest document embeddings. Because "automobile" and "car" have similar vectors, Semantic Search effortlessly bridges the vocabulary gap.
