# Transformers from First Principles

Welcome to the **Transformers from First Principles** curriculum. This module dives deep into the architecture that revolutionized Natural Language Processing (NLP) and Computer Vision (CV): the Transformer.

## Curriculum Structure

1. **[01-Introduction-and-Embeddings.md](./01-Introduction-and-Embeddings.md)**
   - Tokens and Tokenization
   - Input Embeddings
   - Positional Encoding (injecting sequence order)

2. **[02-Self-Attention.md](./02-Self-Attention.md)**
   - Queries, Keys, and Values
   - Scaled Dot-Product Attention
   - Softmax and Attention Scores
   - Numerical Examples and Matrix Operations

3. **[03-Multi-Head-Attention-and-Masking.md](./03-Multi-Head-Attention-and-Masking.md)**
   - Multi-Head Attention Mechanism
   - Causal (Look-ahead) Masking for Autoregressive Generation
   - Padding Masks

4. **[04-Feed-Forward-and-Transformer-Block.md](./04-Feed-Forward-and-Transformer-Block.md)**
   - Position-wise Feed-Forward Networks (FFN)
   - Add & Norm (Residual connections and Layer Normalization)
   - The complete Transformer Block

5. **[transformer_from_scratch.py](./transformer_from_scratch.py)**
   - A complete, documented, from-scratch implementation of the Transformer components in PyTorch.
