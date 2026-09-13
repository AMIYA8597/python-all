# Module 1: Tokens, Embeddings, and Positional Information

## Prerequisites
- Basic understanding of linear algebra (vectors, matrices, dot products).
- Familiarity with basic neural network concepts (weights, forward pass).
- Understanding of how text is represented digitally (strings, characters).

## Objectives
- Understand how text is broken down into **tokens**.
- Learn how discrete tokens are mapped to continuous **embeddings**.
- Comprehend the necessity and mathematics of **positional encoding**.

## Intuition

### Tokens
Neural networks cannot process raw text. We must convert text into numbers. The first step is **tokenization**, where a string is chopped into smaller pieces called tokens (words, subwords, or characters). A vocabulary is then built, assigning a unique integer ID to each token.

### Embeddings
If we just feed integer IDs to a neural network, the model would assume that ID `2` is twice as "large" as ID `1`, which makes no semantic sense. Instead, we map each token ID to a high-dimensional vector (e.g., $d_{model} = 512$). This continuous space allows the network to capture semantic relationships (e.g., "king" - "man" + "woman" $\approx$ "queen"). 

### Positional Information
Unlike Recurrent Neural Networks (RNNs) that process tokens sequentially (word by word), Transformers process all tokens simultaneously. This parallel processing is highly efficient but completely ignores the order of the words. To the attention mechanism, "The dog bit the man" and "The man bit the dog" look identical. We must inject **positional information** into the embeddings so the model knows *where* each word is in the sequence.

## Mathematics

### Embedding Matrix
Let $V$ be the vocabulary size and $d$ be the embedding dimension. The embedding matrix is $E \in \mathbb{R}^{V \times d}$. 
Given a token ID $i$, the embedding is the $i$-th row of $E$.

### Positional Encoding (Sinusoidal)
The original Transformer uses sine and cosine functions of different frequencies to generate a positional encoding (PE) vector of size $d$ for each position $pos$.

For a position $pos$ and dimension $i$ (where $0 \le i < d$):

$$ PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right) $$
$$ PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right) $$

The final input to the Transformer is the element-wise sum of the token embedding and the positional encoding:
$$ X = \text{Embedding}(Tokens) + \text{PositionalEncoding} $$

## Code

```python
import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        # Create a matrix of shape (max_len, d_model)
        pe = torch.zeros(max_len, d_model)
        
        # Position indices: (max_len, 1)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # Div term for frequencies
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        # Apply sin to even indices, cos to odd indices
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # Add batch dimension: (1, max_len, d_model)
        pe = pe.unsqueeze(0)
        
        # Register as buffer (not a trainable parameter)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x shape: (batch_size, seq_len, d_model)
        seq_len = x.size(1)
        # Add positional encoding to the input embeddings
        x = x + self.pe[:, :seq_len, :]
        return x
```

## Numerical Example
Suppose $d = 4$. Let's calculate the PE for position $pos = 1$:
- $i=0$: $PE_{(1, 0)} = \sin(1 / 10000^{0/4}) = \sin(1) \approx 0.841$
- $i=0$: $PE_{(1, 1)} = \cos(1 / 10000^{0/4}) = \cos(1) \approx 0.540$
- $i=1$: $PE_{(1, 2)} = \sin(1 / 10000^{2/4}) = \sin(1/100) = \sin(0.01) \approx 0.010$
- $i=1$: $PE_{(1, 3)} = \cos(1 / 10000^{2/4}) = \cos(1/100) = \cos(0.01) \approx 0.999$

So $PE_{pos=1} = [0.841, 0.540, 0.010, 0.999]$.

## Interview Questions
1. **Why do we add positional encodings instead of concatenating them to the embeddings?**
   *Answer:* Adding keeps the dimensionality constant (saving memory and parameters). In high-dimensional spaces, addition operates similarly to orthogonal concatenation, allowing the model to easily separate the semantic meaning (embedding) from the spatial meaning (PE) during the linear projections in attention.
2. **Why use sinusoidal functions for positional encodings?**
   *Answer:* They allow the model to easily learn to attend by relative positions, because for any fixed offset $k$, $PE_{pos+k}$ can be represented as a linear function of $PE_{pos}$. They can also extrapolate to sequence lengths longer than those seen during training.
