"""
Word Embeddings Examples
Demonstrates concepts of Word2Vec embeddings and cosine similarity.
In practice, we use libraries like gensim or spaCy for pre-trained models.
Here we simulate embeddings and compute similarities.
"""

import math
from typing import List

# Simulating a small pre-trained embedding dictionary (dim=4)
# In reality, these vectors are learned via neural networks and are much larger (e.g., 300d)
embeddings = {
    "king":  [0.9, 0.1, 0.8, 0.1],
    "man":   [0.9, 0.1, 0.2, 0.1],
    "woman": [0.1, 0.9, 0.2, 0.1],
    "queen": [0.1, 0.9, 0.8, 0.1],
    "apple": [0.0, 0.0, 0.1, 0.9],
    "fruit": [0.1, 0.1, 0.1, 0.8]
}

def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(x * y for x, y in zip(v1, v2))

def magnitude(v: List[float]) -> float:
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates cosine similarity between two vectors."""
    mag_v1 = magnitude(v1)
    mag_v2 = magnitude(v2)
    if mag_v1 == 0 or mag_v2 == 0:
        return 0.0
    return dot_product(v1, v2) / (mag_v1 * mag_v2)

def vector_add(v1: List[float], v2: List[float]) -> List[float]:
    return [x + y for x, y in zip(v1, v2)]

def vector_sub(v1: List[float], v2: List[float]) -> List[float]:
    return [x - y for x, y in zip(v1, v2)]

if __name__ == "__main__":
    print("--- Semantic Similarity ---")
    sim_king_man = cosine_similarity(embeddings["king"], embeddings["man"])
    sim_king_apple = cosine_similarity(embeddings["king"], embeddings["apple"])
    
    print(f"Similarity (king, man): {sim_king_man:.4f}")
    print(f"Similarity (king, apple): {sim_king_apple:.4f}")
    
    print("\n--- Linear Analogies (king - man + woman = ?) ---")
    # v_king - v_man + v_woman
    v_analogy = vector_add(vector_sub(embeddings["king"], embeddings["man"]), embeddings["woman"])
    print(f"Resulting vector: {v_analogy}")
    
    # Check similarity with queen
    sim_analogy_queen = cosine_similarity(v_analogy, embeddings["queen"])
    print(f"Similarity with 'queen': {sim_analogy_queen:.4f}")
    
    # Find most similar word to the analogy vector (excluding original words ideally)
    best_word = None
    best_sim = -1
    for word, vec in embeddings.items():
        sim = cosine_similarity(v_analogy, vec)
        if sim > best_sim:
            best_sim = sim
            best_word = word
            
    print(f"Closest word to (king - man + woman) is: {best_word} (sim: {best_sim:.4f})")
