"""
## A. Concept Name
Transformer Block and Self-Attention Mechanism

## B. Analogy
Imagine a reading group where instead of reading a book linearly word-by-word (like an RNN), everyone looks at a whole sentence simultaneously. Each person is assigned a word and tries to understand its meaning by paying "attention" to other relevant words in the sentence. Multi-head attention is like having different people analyze the same sentence for different things (e.g., one looks for grammar, another for emotion, another for entities).

## C. Core Mechanism
1. **Self-Attention**: Computes a weighted sum of `Values`, where the weight is determined by the compatibility (dot product) of a `Query` with a `Key`.
2. **Multi-Head Attention**: Splits the embedding into multiple heads, performs self-attention in parallel, and concatenates the results.
3. **Feed-Forward Network**: Applied to each position separately and identically, adding non-linearity.
4. **Layer Normalization & Residual Connections**: Stabilize training and allow gradients to flow easily through deep networks.

## D. Time & Space Complexity
- **Time Complexity**: $O(N^2 \cdot d)$ where $N$ is sequence length and $d$ is embedding dimension. The $N^2$ term comes from the attention matrix calculation.
- **Space Complexity**: $O(N^2 \cdot h)$ to store the attention scores for each head $h$.

## E. Common Pitfalls
- Forgetting to scale the dot product by $\sqrt{d_k}$. Without this, the dot products can grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients.
- Incorrectly masking sequences, especially for decoder self-attention where future tokens must be masked.

## X. Project Connection
This module serves as the foundational building block for modern Generative AI and Large Language Models (LLMs). By understanding this basic Transformer Block, you are equipped to tackle architectures like GPT, BERT, and LLaMA within this learning repository.
"""

import math

# Try to import torch, fallback to a mock explanation if not available
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("PyTorch is not installed. This script requires PyTorch to run the actual model code.")
    print("You can install it using: pip install torch")

if HAS_TORCH:
    class SelfAttention(nn.Module):
        """
        A simple implementation of Scaled Dot-Product Attention.
        """
        def __init__(self, embed_size, heads):
            super(SelfAttention, self).__init__()
            self.embed_size = embed_size
            self.heads = heads
            self.head_dim = embed_size // heads

            assert (self.head_dim * heads == embed_size), "Embed size needs to be divisible by heads"

            self.values = nn.Linear(self.head_dim, self.head_dim, bias=False)
            self.keys = nn.Linear(self.head_dim, self.head_dim, bias=False)
            self.queries = nn.Linear(self.head_dim, self.head_dim, bias=False)
            self.fc_out = nn.Linear(heads * self.head_dim, embed_size)

        def forward(self, values, keys, query, mask):
            N = query.shape[0]
            value_len, key_len, query_len = values.shape[1], keys.shape[1], query.shape[1]

            # Split the embedding into self.heads different pieces
            values = values.reshape(N, value_len, self.heads, self.head_dim)
            keys = keys.reshape(N, key_len, self.heads, self.head_dim)
            queries = query.reshape(N, query_len, self.heads, self.head_dim)

            values = self.values(values)
            keys = self.keys(keys)
            queries = self.queries(queries)

            # Einsum does matrix multiplication for query*keys for each training example
            # with every other training example, don't be confused by einsum
            # it's just a way to do batch matrix multiplication
            energy = torch.einsum("nqhd,nkhd->nhqk", [queries, keys])

            if mask is not None:
                energy = energy.masked_fill(mask == 0, float("-1e20"))

            attention = torch.softmax(energy / (self.embed_size ** (1 / 2)), dim=3)

            out = torch.einsum("nhql,nlhd->nqhd", [attention, values]).reshape(
                N, query_len, self.heads * self.head_dim
            )

            out = self.fc_out(out)
            return out

    class TransformerBlock(nn.Module):
        """
        A standard Transformer Block with Self-Attention and FeedForward Neural Network.
        """
        def __init__(self, embed_size, heads, dropout, forward_expansion):
            super(TransformerBlock, self).__init__()
            self.attention = SelfAttention(embed_size, heads)
            self.norm1 = nn.LayerNorm(embed_size)
            self.norm2 = nn.LayerNorm(embed_size)

            self.feed_forward = nn.Sequential(
                nn.Linear(embed_size, forward_expansion * embed_size),
                nn.ReLU(),
                nn.Linear(forward_expansion * embed_size, embed_size),
            )
            self.dropout = nn.Dropout(dropout)

        def forward(self, value, key, query, mask):
            attention = self.attention(value, key, query, mask)

            # Add skip connection, run through normalization and finally dropout
            x = self.dropout(self.norm1(attention + query))
            forward = self.feed_forward(x)
            out = self.dropout(self.norm2(forward + x))
            return out

    def main():
        print("--- Transformer Architecture Basics ---")
        # Define hyperparams
        embed_size = 256
        heads = 8
        dropout = 0.1
        forward_expansion = 4
        
        # Create a dummy batch of sequences
        # Batch size = 32, Sequence Length = 10, Embedding Size = 256
        batch_size = 32
        seq_length = 10
        x = torch.randn((batch_size, seq_length, embed_size))
        
        print(f"Input shape: {x.shape} (Batch, Seq_Len, Embed_Dim)")
        
        # Initialize the block
        block = TransformerBlock(embed_size, heads, dropout, forward_expansion)
        
        # Forward pass (using x as query, key, and value for self-attention)
        out = block(x, x, x, mask=None)
        
        print(f"Output shape: {out.shape} (Matches input shape)")
        print("Transformer block execution successful! The model processed the sequence in parallel.")

if __name__ == "__main__":
    if HAS_TORCH:
        main()
