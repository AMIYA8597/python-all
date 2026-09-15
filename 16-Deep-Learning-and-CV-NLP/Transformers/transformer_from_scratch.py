"""
# ==============================================================================
# LABORATORY: TRANSFORMERS (BUILDING A GPT DECODER FROM SCRATCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer imports `from transformers import GPT2Model`. They can 
# generate text, but when the model hallucinates or fails to understand a 
# long prompt, they have absolutely no idea what went wrong mathematically.
#
# A senior AI engineer builds the Transformer from scratch. They physically code 
# the `Query @ Key^T` matrix multiplications. They physically code the Triangular 
# Causal Mask (Negative Infinity). They physically code the Residual Connections 
# and LayerNorm. When the model fails, they know exactly which mathematical 
# tensor is saturating and how to fix it.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Multi-Head Attention Mathematics.
# - Architect a Causal Mask to prevent "peeking at the future".
# - Build the full GPT-style Transformer Decoder Block.
#
# ==============================================================================
"""

import math
import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MATHEMATICAL HELPER FUNCTIONS
# ==============================================================================
def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Stable Softmax implementation."""
    # Subtracting the max prevents np.exp() from overflowing to Infinity!
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / e_x.sum(axis=axis, keepdims=True)

def layer_norm(x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """
    [SECURE] Layer Normalization.
    Normalizes the values across the embedding dimension to have Mean 0, Variance 1.
    This strictly prevents exploding gradients during deep backpropagation.
    """
    mean = np.mean(x, axis=-1, keepdims=True)
    var = np.var(x, axis=-1, keepdims=True)
    # (x - mean) / standard_deviation
    return (x - mean) / np.sqrt(var + eps)


# ==============================================================================
# 4. THE CORE ARCHITECTURE: SCALED DOT-PRODUCT ATTENTION
# ==============================================================================
class ScaledDotProductAttention:
    
    @staticmethod
    def forward(Q: np.ndarray, K: np.ndarray, V: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
        """
        [SECURE] The Heart of ChatGPT.
        Attention(Q, K, V) = softmax( (Q @ K^T) / sqrt(d_k) ) @ V
        """
        d_k = Q.shape[-1]
        
        # 1. Query @ Key.Transpose
        # Calculates the raw similarity scores between every token and every other token.
        scores = np.matmul(Q, K.swapaxes(-2, -1))
        
        # 2. Scale by sqrt(d_k)
        # Prevents the scores from becoming astronomically large and destroying the Softmax gradient.
        scaled_scores = scores / math.sqrt(d_k)
        
        # 3. Apply the Causal Mask (If Autoregressive Generation)
        if mask is not None:
            # We aggressively replace the 'future' tokens with Negative Infinity!
            # When Softmax looks at Negative Infinity, it calculates e^(-Inf) = 0.0.
            # This mathematically prevents the model from cheating by looking ahead!
            scaled_scores = np.where(mask == 0, -1e9, scaled_scores)
            
        # 4. Softmax (Convert to Probabilities)
        attention_weights = softmax(scaled_scores)
        
        # 5. Multiply by Values
        output = np.matmul(attention_weights, V)
        return output, attention_weights


# ==============================================================================
# 5. THE TRANSFORMER BLOCK (GPT DECODER)
# ==============================================================================
class TransformerDecoderBlock:
    """
    A full GPT-style Transformer Block!
    Architecture:
    Input -> LayerNorm -> Self-Attention -> Residual Add 
          -> LayerNorm -> FeedForward -> Residual Add -> Output
    """
    
    def __init__(self, embed_dim: int):
        self.embed_dim = embed_dim
        
        # In a real framework (PyTorch), these would be trainable Neural Network Linear Layers!
        # For this simulation, we use random fixed weights to prove the Tensor math flows flawlessly.
        np.random.seed(42)
        
        # Q, K, V Projection Matrices
        self.W_q = np.random.randn(embed_dim, embed_dim) * 0.1
        self.W_k = np.random.randn(embed_dim, embed_dim) * 0.1
        self.W_v = np.random.randn(embed_dim, embed_dim) * 0.1
        
        # Point-Wise Feed Forward Network (FFN)
        # Usually expands the dimension by 4x, then compresses it back!
        self.W_ff1 = np.random.randn(embed_dim, embed_dim * 4) * 0.1
        self.W_ff2 = np.random.randn(embed_dim * 4, embed_dim) * 0.1
        
    def relu(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)
        
    def forward(self, x: np.ndarray, mask: np.ndarray) -> np.ndarray:
        print("  -> Entering Transformer Block...")
        print(f"     * Initial Input Tensor Shape: {x.shape}")
        
        # ---------------------------------------------------------
        # ATTENTION SUB-LAYER
        # ---------------------------------------------------------
        # Pre-Norm Architecture (Modern Standard used in GPT-3/4)
        norm_x = layer_norm(x)
        
        # Project into Q, K, V
        Q = np.matmul(norm_x, self.W_q)
        K = np.matmul(norm_x, self.W_k)
        V = np.matmul(norm_x, self.W_v)
        
        # Execute Attention!
        attention_out, _ = ScaledDotProductAttention.forward(Q, K, V, mask)
        
        # RESIDUAL CONNECTION 1: Add the original input back!
        x = x + attention_out
        print("     * Attention & Residual 1 Completed.")
        
        # ---------------------------------------------------------
        # FEED-FORWARD SUB-LAYER
        # ---------------------------------------------------------
        norm_x = layer_norm(x)
        
        # Linear -> ReLU -> Linear
        ff_out = np.matmul(norm_x, self.W_ff1)
        ff_out = self.relu(ff_out)
        ff_out = np.matmul(ff_out, self.W_ff2)
        
        # RESIDUAL CONNECTION 2: Add the input back!
        x = x + ff_out
        print("     * Feed-Forward & Residual 2 Completed.")
        
        return x


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_transformer():
    section_header("Transformers: Generative Pre-Trained Transformer (GPT) From Scratch")
    
    # 1. The Setup
    batch_size = 1
    seq_length = 4  # e.g., "The", "cat", "sat", "on"
    embed_dim = 64  # Size of the vector representing each word
    
    # We generate a fake input sequence (normally this comes from an Embedding Layer + Positional Encoding)
    print("  [INIT] Generating Input Sequence (Batch=1, Seq=4, EmbedDim=64)...")
    input_sequence = np.random.randn(batch_size, seq_length, embed_dim)
    
    # 2. The Causal Mask (Triangular Matrix)
    # 1 = Allowed to look. 0 = Masked out (Future).
    # [1, 0, 0, 0] -> Word 1 can only look at Word 1
    # [1, 1, 0, 0] -> Word 2 can look at Word 1 and 2
    # [1, 1, 1, 0] -> Word 3 can look at 1, 2, 3
    # [1, 1, 1, 1] -> Word 4 can look at everything
    causal_mask = np.tril(np.ones((seq_length, seq_length)))
    
    print("\n  [CAUSAL MASK]")
    print(causal_mask)
    
    # 3. The Execution
    print("\n  [EXECUTION] Pushing data through a GPT Decoder Block...")
    gpt_block = TransformerDecoderBlock(embed_dim=embed_dim)
    
    final_output = gpt_block.forward(input_sequence, mask=causal_mask)
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  -> Final Output Tensor Shape: {final_output.shape}")
    print("  -> [FLAWLESS] The matrix mathematics preserved the dimensionality perfectly ")
    print("     across Attention, LayerNorm, and Feed-Forward networks, while strictly ")
    print("     preventing future information leakage via the Causal Mask!")


def run_all_labs():
    demonstrate_transformer()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why are 'Residual Connections' ($X + \\text{Attention}(X)$) mathematically required in a $100$-layer Transformer?"
   Senior Answer: "The Vanishing Gradient and Feature Identity. If a Transformer is $100$ layers deep, the Backpropagation calculus gradient must multiply through $100$ complex Attention matrices. The gradient will exponentially vanish to zero. A Residual Connection physically adds the original unmodified Tensor ($X$) directly to the output of the sub-layer. The mathematical derivative of $X + Y$ is exactly $1.0 + Y'$. This physical $1.0$ acts as an unobstructed highway, allowing the gradient to bypass the matrix multiplications and flow backwards from Layer $100$ all the way to Layer $1$ completely intact. Furthermore, it ensures the model never 'forgets' the original input word embedding."

2. Interviewer: "Explain exactly how the Triangular Causal Mask prevents the model from 'cheating' during training."
   Senior Answer: "Negative Infinity prior to Softmax. In an Autoregressive model (GPT), we train the network to predict Word $4$ using only Words $1, 2, 3$. Because the Attention Matrix $Q \\cdot K^T$ calculates all words simultaneously in parallel, Word $3$ accidentally calculates its similarity score against Word $4$ (the future!). The Triangular Causal Mask mathematically intervenes. It overwrites the upper triangle of the score matrix with Negative Infinity ($-1e9$). When the Softmax function processes $-1e9$, it computes $e^{-1e9}$, which is exactly $0.0$. Thus, Word $3$ pays $0.0\\%$ attention to Word $4$. The 'future' is mathematically annihilated."

3. Interviewer: "What is the architectural difference between 'Pre-Norm' (used in GPT-3) and 'Post-Norm' (used in the original 'Attention is All You Need' paper)?"
   Senior Answer: "Gradient Stability. The original paper used Post-Norm: $X = \\text{LayerNorm}(X + \\text{Sublayer}(X))$. This means the Residual Highway must pass *through* a LayerNorm operation at every single step, which slightly distorts the pristine gradient flow. Modern architectures (GPT-2, GPT-3, LLaMA) use Pre-Norm: $X = X + \\text{Sublayer}(\\text{LayerNorm}(X))$. Here, the LayerNorm is pushed *inside* the sub-layer branch. The main Residual Highway is now pure, unadulterated mathematical addition from Layer $1$ to Layer $100$. Pre-Norm allows models to scale to billions of parameters without training instability or gradient explosion."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Transformers (From Scratch) Completed.")
