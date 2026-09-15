"""
# ==============================================================================
# LABORATORY: DEEP LEARNING (NATURAL LANGUAGE PROCESSING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to process text by assigning random integers to words. 
# They assign "King" = 1, "Man" = 2, and "Apple" = 3. A Neural Network receives 
# these integers and mathematically concludes that an "Apple" is 3x more valuable 
# than a "King", and that "Man" + "King" = "Apple". The model fails completely.
#
# A senior AI engineer understands "Word Embeddings" (Word2Vec) and "Attention". 
# They mathematically map words into a 300-dimensional continuous floating-point 
# vector space. In this space, similar concepts are physically closer together. 
# The engineer proves mathematically that: Vector("King") - Vector("Man") + 
# Vector("Woman") is physically located right next to Vector("Queen"). The model 
# learns the mathematical architecture of human semantic logic.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Tokenization (Sub-word vs Word level).
# - Execute Vector Embeddings and Cosine Similarity.
# - Architect the Self-Attention mechanism (Transformer core).
#
# ==============================================================================
"""

import numpy as np
import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (VECTOR EMBEDDINGS)
# ==============================================================================
class NLPSimulator:
    
    @staticmethod
    def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """Calculates the exact angle between two vectors in N-Dimensional space."""
        dot_product = np.dot(vec_a, vec_b)
        magnitude_a = np.linalg.norm(vec_a)
        magnitude_b = np.linalg.norm(vec_b)
        return dot_product / (magnitude_a * magnitude_b)

    def execute_embeddings(self):
        """
        [SECURE] Simulating Word2Vec Embeddings.
        We map words to a 3-Dimensional semantic space for visibility.
        [Royalty, Masculinity, Edibility]
        """
        print("  [INIT] Mapping Words to a 3D Semantic Vector Space...")
        
        # [Royalty, Masculinity, Edibility]
        vocab = {
            "King":  np.array([0.95,  0.90, 0.01]),
            "Queen": np.array([0.95, -0.90, 0.01]),
            "Man":   np.array([0.01,  0.90, 0.01]),
            "Woman": np.array([0.01, -0.90, 0.01]),
            "Apple": np.array([0.01,  0.01, 0.95])
        }
        
        print("\n  [EXECUTION] Calculating Cosine Similarity (Semantic Closeness)...")
        
        sim_king_man = self.cosine_similarity(vocab["King"], vocab["Man"])
        sim_king_apple = self.cosine_similarity(vocab["King"], vocab["Apple"])
        
        print(f"  -> Similarity (King vs Man):   {sim_king_man:.4f} (High!)")
        print(f"  -> Similarity (King vs Apple): {sim_king_apple:.4f} (Zero!)")
        
        print("\n  [EXECUTION] The Famous NLP Equation: King - Man + Woman = ?")
        # Mathematically calculate the vector!
        result_vector = vocab["King"] - vocab["Man"] + vocab["Woman"]
        
        # Check which word it is closest to!
        sim_queen = self.cosine_similarity(result_vector, vocab["Queen"])
        sim_apple = self.cosine_similarity(result_vector, vocab["Apple"])
        
        print(f"  -> Similarity to Queen: {sim_queen:.4f} (Nearly perfect 1.0 match!)")
        print(f"  -> Similarity to Apple: {sim_apple:.4f}")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: SELF-ATTENTION (THE TRANSFORMER)
    # --------------------------------------------------------------------------
    def execute_attention(self):
        """
        [SECURE] Simulating the 'Attention is All You Need' mechanism.
        "The bank of the river" vs "The bank on Wall Street"
        How does the word 'bank' know which definition to use? By looking at its neighbors!
        """
        print("\n  [INIT] Simulating Self-Attention Matrix...")
        
        sentence = ["The", "bank", "of", "the", "river"]
        
        # We simulate the Attention Scores (Query dot Key matrix).
        # Read this matrix as: "How much attention should the row word pay to the column word?"
        # The word 'bank' (Row 1) pays massive attention to 'river' (Col 4)
        attention_matrix = np.array([
            [1.0, 0.0, 0.0, 0.0, 0.0], # The
            [0.1, 1.0, 0.1, 0.1, 0.8], # bank (Looks at 'river'!)
            [0.0, 0.0, 1.0, 0.0, 0.0], # of
            [0.0, 0.0, 0.0, 1.0, 0.0], # the
            [0.0, 0.8, 0.0, 0.0, 1.0], # river (Looks at 'bank'!)
        ])
        
        print(f"  -> Word: '{sentence[1]}'")
        print(f"  -> Attention weights: {list(zip(sentence, attention_matrix[1]))}")
        print("  -> [FLAWLESS] The mathematical attention mechanism routed contextual ")
        print("     information from 'river' directly into 'bank', instantly resolving ")
        print("     the semantic ambiguity. This is how ChatGPT works.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_nlp():
    section_header("Deep Learning: Natural Language Processing")
    
    sim = NLPSimulator()
    sim.execute_embeddings()
    sim.execute_attention()


def run_all_labs():
    demonstrate_nlp()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why are Sub-word Tokenizers (like BPE - Byte Pair Encoding) mathematically superior to Word-level tokenizers?"
   Senior Answer: "The Out-Of-Vocabulary (OOV) Catastrophe. If a Word-level tokenizer encounters the word 'unbelievable', but it only learned 'believe' during training, it violently crashes or replaces the word with an `<UNK>` token, losing all semantic meaning. A Sub-word tokenizer (like OpenAI's Tiktoken for ChatGPT) mathematically breaks down rare words into morphological chunks. It tokenizes 'unbelievable' into `['un', 'believ', 'able']`. The Neural Network has mathematically seen 'un' and 'able' millions of times, allowing it to instantly infer the grammatical prefix and suffix, perfectly generalizing to words it has never explicitly seen."

2. Interviewer: "Explain the mathematical difference between Euclidean Distance and Cosine Similarity when comparing Word Embeddings."
   Senior Answer: "Magnitude vs Angle. In a 300-Dimensional vector space, the word 'Dog' might appear in a document $1$ time, producing a vector of magnitude $1$. If it appears $500$ times in another document, the resulting TF-IDF/Embedding vector will have a magnitude of $500$. If you use Euclidean Distance ($x_2 - x_1$), the mathematical distance between these two vectors is massive, leading the algorithm to conclude they are different concepts. Cosine Similarity explicitly divides the dot product by the magnitude of the vectors, effectively normalizing them. It mathematically measures only the *Angle* between the vectors. The angle between 'Dog' and 'Dog' is exactly $0$ degrees (Similarity $1.0$), regardless of vector length."

3. Interviewer: "What specific architectural flaw in LSTMs/RNNs did the Transformer's 'Self-Attention' mechanism solve?"
   Senior Answer: "The Sequential Bottleneck and the Vanishing Gradient. LSTMs must mathematically process text sequentially. To understand word $100$, it must process word $1$ through $99$ in a strict `for` loop, which makes GPU parallelization physically impossible and causes the mathematical gradient to vanish over long distances. The Transformer completely eliminated the sequential loop. The Self-Attention matrix mathematically compares *every word with every other word* simultaneously in a single O(1) Matrix Multiplication ($Q \\cdot K^T$). This allows Transformers to process 8,000-word documents in perfect parallel on a GPU, unlocking the era of LLMs."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Deep Learning (NLP & Transformers) Completed.")
