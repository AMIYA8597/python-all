"""
# Embeddings and Vector Search: Beginner to Professional

## 1. What is an Embedding?
An embedding is a list of numbers (a vector) that captures the "meaning" of a piece of text (or image, or audio). 
Instead of comparing exact words (like searching for "fast" in a database), we compare the *meaning* of words.

## 2. Why does it exist?
Traditional databases use lexical search (keyword matching like BM25 or SQL `LIKE`). 
If a user searches for "automobile", a traditional database will completely miss a document that only says "car".
Embeddings solve this. Because "automobile" and "car" have similar *meanings*, their embedding vectors will be mathematically close to each other in vector space.

## 3. Intuition & Real-World Analogy
Imagine a massive 3D library where books are organized purely by concept.
- X-axis: How "technological" vs "biological" the book is.
- Y-axis: How "historical" vs "futuristic" the book is.
- Z-axis: How "positive" vs "negative" the tone is.

A book about "Apple iPhones" might be at coordinate (0.9, 0.5, 0.2).
A book about "Samsung Galaxys" might be at (0.85, 0.5, 0.2).
Because their coordinates are close, we instantly know they are similar, without even reading the titles. 
Real embedding models (like OpenAI's `text-embedding-3-small`) just use 1,536 dimensions instead of 3.

## 4. Formal Definition: Cosine Similarity
To find out how close two vectors are, we measure the angle between them. 
* Angle is 0° (Cosine = 1.0): Identical meaning.
* Angle is 90° (Cosine = 0.0): Unrelated.
* Angle is 180° (Cosine = -1.0): Opposite meaning.

$$ \text{Cosine Similarity} = \frac{A \cdot B}{||A|| \times ||B||} $$

## 5. When to use / When NOT to use
**Use Embeddings for:** Semantic search, clustering documents, classification features, RAG (Retrieval-Augmented Generation).
**Do NOT use Embeddings for:** Exact ID lookups, highly specific keyword matching (e.g., searching for a specific error code like "ERR_404_X"). For the best of both worlds, modern systems use **Hybrid Search** (Keyword + Semantic).

---
"""

import math
from typing import List, Dict, Tuple

# ============================================================================
# 1. CORE MATHEMATICS: COSINE SIMILARITY
# ============================================================================

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculates the cosine similarity between two vectors from scratch.
    In production, use `numpy.dot(v1, v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))`
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same dimensionality.")
        
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # ||A|| (Magnitude of vector 1)
    magnitude_vec1 = math.sqrt(sum(a * a for a in vec1))
    # ||B|| (Magnitude of vector 2)
    magnitude_vec2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude_vec1 == 0 or magnitude_vec2 == 0:
        return 0.0
        
    return dot_product / (magnitude_vec1 * magnitude_vec2)


# ============================================================================
# 2. EDUCATIONAL MOCK EMBEDDING MODEL
# ============================================================================

class EducationalEmbeddingModel:
    """
    A simulated embedding model mapping sentences to a 3D vector space.
    Dimensions represent:
    [ Tech/Nature,  Feline/Canine,  Action/Static ]
    """
    def __init__(self):
        self.embeddings = {
            # Animals (Nature: Positive)
            "The quick brown fox":      [0.9, -0.8,  0.8],  # Nature, Feline-ish, High Action
            "A fast orange fox":        [0.8, -0.7,  0.9],
            "The lazy dog":             [0.9,  0.9, -0.8],  # Nature, Canine, Static
            "A sleeping puppy":         [0.8,  0.8, -0.9],
            
            # Technology (Tech: Negative)
            "Latest smartphone specs":  [-0.9,  0.0,  0.2],
            "New mobile phone features":[-0.8,  0.1,  0.3],
            
            # Outlier
            "A robotic dog running":    [-0.5,  0.8,  0.8]   # Tech, Canine, Action
        }
        
    def embed(self, text: str) -> List[float]:
        """In reality, this passes text through a Transformer to get a vector."""
        if text not in self.embeddings:
            raise KeyError(f"Text not found in mock embeddings: '{text}'")
        return self.embeddings[text]


# ============================================================================
# 3. VECTOR DATABASE IMPLEMENTATION
# ============================================================================

class SimpleVectorDB:
    """
    An in-memory Vector Database using Exact K-Nearest Neighbors (KNN).
    
    Note on Production scaling:
    This uses a "Brute Force" search (O(N) time).
    Production databases (Pinecone, Milvus, FAISS) use Approximate Nearest Neighbors (ANN)
    algorithms like HNSW (Hierarchical Navigable Small World) to achieve O(log N) search time.
    """
    def __init__(self):
        self.collection: List[Dict] = []
        
    def add(self, doc_id: str, text: str, vector: List[float]):
        """Ingests a document and its vector embedding into the DB."""
        self.collection.append({"id": doc_id, "text": text, "vector": vector})
        
    def search(self, query_vector: List[float], top_k: int = 2) -> List[Tuple[str, float]]:
        """Scans ALL vectors, calculates similarity, and returns the top K matches."""
        results = []
        for item in self.collection:
            sim = cosine_similarity(query_vector, item["vector"])
            results.append((item["text"], sim))
            
        # Sort descending by similarity score
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


# ============================================================================
# DEBUGGING EXERCISE: Find the Bug!
# ============================================================================
def buggy_euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    Euclidean distance is another way to measure vector closeness.
    BUG: What is wrong with this implementation?
    """
    dist = 0
    for a, b in zip(vec1, vec2):
        dist += (a - b)
    return math.sqrt(dist) 
    # Solution: We must square the difference before adding! 
    # Should be: dist += (a - b) ** 2
    # Without squaring, negative and positive differences cancel each other out.

# ============================================================================
# ACTIVE RECALL & INTERVIEW PREPARATION
# ============================================================================
"""
Q: What is the difference between Cosine Similarity and Euclidean Distance?
A: Euclidean distance measures the straight-line distance between two points. 
   Cosine similarity measures the ANGLE between them. Cosine similarity is generally 
   preferred in NLP because it ignores the magnitude (length) of the vector, 
   focusing purely on the directional "meaning".

Q: If you double the length of a vector, how does its Cosine Similarity to another vector change?
A: It does not change. Cosine similarity normalizes magnitude. The angle remains identical.

Q: Why don't we use exact KNN (like this script) in production for 100 million documents?
A: Time complexity. Calculating 100 million cosine similarities for a single user query 
   takes too long. We use Approximate Nearest Neighbors (ANN) indexes like HNSW.
"""


def main():
    print("=== Semantic Search & Embeddings System ===\n")
    
    embedder = EducationalEmbeddingModel()
    db = SimpleVectorDB()
    
    # 1. Ingest Documents
    print("1. Ingesting documents into Vector DB...")
    documents = [
        "The quick brown fox",
        "The lazy dog",
        "Latest smartphone specs"
    ]
    
    for i, doc in enumerate(documents):
        vec = embedder.embed(doc)
        db.add(doc_id=f"doc_{i}", text=doc, vector=vec)
        print(f"   [+] Added: '{doc}' -> {vec}")
        
    # 2. Perform Semantic Search
    queries = [
        "A fast orange fox",
        "New mobile phone features",
        "A sleeping puppy"
    ]
    
    print("\n2. Querying Vector DB...")
    for query in queries:
        query_vec = embedder.embed(query)
        print(f"\n   Query: '{query}' -> {query_vec}")
        
        results = db.search(query_vec, top_k=1)
        match_text, score = results[0]
        
        print(f"   -> Top Match: '{match_text}' (Score: {score:.4f})")

    print("\n[Concept Check]: Notice how 'A fast orange fox' perfectly matched 'The quick brown fox'")
    print("even though they share almost no exact words! This is the power of Embeddings.")

# ============================================================================
# MEMORY ANCHOR
# ============================================================================
"""
## MEMORY ANCHOR
### One sentence to remember
Embeddings map concepts into a multi-dimensional space where mathematically close vectors represent semantically similar meanings.

### Three things not to confuse
1. Keyword Search vs Vector Search: Keyword finds exact words; Vector finds meanings.
2. Cross-Encoder vs Bi-Encoder: Bi-Encoders (used here) embed documents independently for fast retrieval. Cross-Encoders compare two strings directly (slower, but more accurate for reranking).
3. KNN vs ANN: KNN is 100% accurate but slow O(N). ANN is fast O(log N) but slightly approximate.
"""

if __name__ == "__main__":
    main()
