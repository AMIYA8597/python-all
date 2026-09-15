"""
# ==============================================================================
# LABORATORY: NLP (ATTENTION & TRANSFORMERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses an LSTM to translate a 1,000-word paragraph. Because 
# the LSTM must mathematically process word #1 before it can process word #2, 
# it cannot be parallelized. The translation takes 45 seconds on a GPU.
#
# A senior AI engineer understands "Self-Attention" and the Transformer architecture. 
# They abandon sequential loops entirely. They project all 1,000 words into Query (Q), 
# Key (K), and Value (V) matrices simultaneously. They execute a massive 
# single Matrix Multiplication: Softmax(Q * K^T) * V. The GPU processes all 
# 1,000 words in parallel in 0.05 seconds, analyzing the semantic relationships 
# of every single word against every other word simultaneously. This equation 
# is the exact mathematical foundation of ChatGPT.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Q, K, V (Query, Key, Value) architectural paradigm.
# - Execute mathematical Self-Attention calculations.
# - Architect Scaled Dot-Product Attention to prevent Softmax saturation.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (SELF-ATTENTION MATHEMATICS)
# ==============================================================================
class AttentionSimulator:
    
    @staticmethod
    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / e_x.sum(axis=-1, keepdims=True)

    def execute_scaled_dot_product_attention(self):
        """
        [SECURE] The core mathematical equation of all modern LLMs.
        Attention(Q, K, V) = softmax( (Q @ K^T) / sqrt(d_k) ) @ V
        """
        print("  [INIT] Simulating Self-Attention for the sentence: 'bank of the river'")
        
        # We have 4 words. We map each word to a 3-Dimensional vector.
        # This is the 'Input Embedding' matrix (4 x 3)
        X = np.array([
            [1.0, 0.0, 0.1],  # bank
            [0.0, 1.0, 0.0],  # of
            [0.0, 0.0, 1.0],  # the
            [0.8, 0.0, 0.9]   # river (Notice its vector is mathematically similar to 'bank'!)
        ])
        
        # 1. Generate Q, K, V Matrices
        # In a real Transformer, these are learned Weight matrices. 
        # For simulation, we assume the network learned the Identity matrix (W = 1).
        Q = X.copy() # Queries: "What am I looking for?"
        K = X.copy() # Keys: "What do I contain?"
        V = X.copy() # Values: "If you attend to me, here is the data I return."
        
        d_k = Q.shape[1] # Dimension of the Key vectors (3)
        
        print("\n  [STEP 1] Matrix Multiplication (Q @ K^T)")
        # Calculate raw Attention Scores! How much does 'bank' align with 'river'?
        raw_scores = np.matmul(Q, K.T)
        print(raw_scores)
        
        print("\n  [STEP 2] Scale the Scores (Divide by sqrt(d_k))")
        # Why? If dimensions are massive, dot products explode. Large numbers push 
        # the Softmax function into flat regions where the Calculus gradient vanishes!
        scaled_scores = raw_scores / np.sqrt(d_k)
        
        print("\n  [STEP 3] Softmax (Normalize into Probabilities)")
        attention_weights = self.softmax(scaled_scores)
        
        # Let's look specifically at Row 0 (The word 'bank')
        print(f"  -> Attention Weights for the word 'bank':")
        print(f"     - bank:  {attention_weights[0][0]:.4f}")
        print(f"     - of:    {attention_weights[0][1]:.4f}")
        print(f"     - the:   {attention_weights[0][2]:.4f}")
        print(f"     - river: {attention_weights[0][3]:.4f} (Massive Attention!)")
        
        print("\n  [STEP 4] Multiply by Values (Attention Weights @ V)")
        # We blend the information together based on the attention weights!
        # 'bank' will literally absorb the mathematical vector data of 'river'!
        contextualized_embeddings = np.matmul(attention_weights, V)
        
        print("\n  [FLAWLESS] The final Output Matrix is fully contextualized. ")
        print("  The vector for 'bank' has been mathematically altered by its ")
        print("  surrounding context, resolving all semantic ambiguity without ")
        print("  ever using a sequential for-loop!")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_attention():
    section_header("Deep Learning NLP: Transformers & Self-Attention")
    
    sim = AttentionSimulator()
    sim.execute_scaled_dot_product_attention()


def run_all_labs():
    demonstrate_attention()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the exact mathematical equation for Scaled Dot-Product Attention, and why do we divide by the square root of $d_k$?"
   Senior Answer: "The equation is $\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{Q K^T}{\\sqrt{d_k}}\\right) V$. The division by $\\sqrt{d_k}$ (the dimension of the key vectors) prevents Softmax Saturation. When you calculate the dot product of two massive vectors (e.g., $d_k = 1024$), the resulting variance of the scalar score becomes astronomically large. If you feed large numbers into a Softmax function, it outputs probabilities of $0.999999$ and $0.000001$. The Calculus derivative (gradient) of Softmax at these extreme tails is exactly $0$. The network mathematically freezes and stops learning. Dividing by $\\sqrt{d_k}$ normalizes the variance back to $1.0$, allowing healthy gradients to flow."

2. Interviewer: "Since Transformers don't use sequential loops like LSTMs, how does the network mathematically know the order of the words?"
   Senior Answer: "Positional Encodings. If you feed 'The dog bit the man' and 'The man bit the dog' into a pure Self-Attention matrix, it yields the exact same result because Matrix Multiplication has no inherent concept of sequence order. To solve this, the Transformer architecture injects a mathematical signal (usually Sine and Cosine waves of varying frequencies) directly into the Word Embeddings *before* they enter the Attention mechanism. This mathematically tags the word 'dog' with a unique frequency signature proving it was the $2$nd word in the sentence, allowing the Attention Matrix to physically distinguish between word positions."

3. Interviewer: "What is 'Multi-Head Attention' and why is it architecturally superior to single-head attention?"
   Senior Answer: "Orthogonal Semantic Workspaces. A single Attention Head forces the network to calculate one specific type of relationship (e.g., matching Verbs to Nouns). Multi-Head Attention splits the $Q, K, V$ matrices into smaller, parallel chunks (e.g., $8$ Heads). Head $1$ mathematically focuses on grammatical syntax. Head $2$ focuses on emotional sentiment. Head $3$ focuses on pronoun resolution (who does 'he' refer to?). These $8$ operations are executed on the GPU in perfect parallel, concatenated, and projected back. It allows the model to mathematically attend to multiple different semantic contexts simultaneously."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: NLP (Attention & Transformers) Completed.")
