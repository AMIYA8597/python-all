# Module 4: Feed-Forward Networks and the Transformer Block

## Prerequisites
- Module 3 (Multi-Head Attention)

## Objectives
- Understand the role of the **Position-wise Feed-Forward Network (FFN)**.
- Understand the importance of **Residual Connections** (Add) and **Layer Normalization** (Norm).
- Combine all components to form the **Transformer Encoder Block** and **Decoder Block**.

## Intuition

### Position-wise FFN
While the Self-Attention layer allows tokens to communicate with each other and gather context, it consists purely of linear projections and weighted averages. To introduce deep non-linear reasoning, we pass the output of the attention layer through a Feed-Forward Network. This FFN is applied to each position (each token) separately and identically. It processes the *contextualized* embedding to extract higher-level features.

### Add & Norm
Deep neural networks suffer from vanishing gradients. **Residual (Skip) Connections** ("Add") bypass a layer by adding its input to its output: `Output = Layer(x) + x`. This provides a direct path for gradients to flow backward.
**Layer Normalization** normalizes the inputs across the features (not the batch), stabilizing training and helping the model converge faster.

## Mathematics

### Feed-Forward Network
The FFN consists of two linear transformations with a ReLU (or GELU) activation in between.
Let $x$ be the representation of a single token:
$$ \text{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2 $$
Usually, the inner hidden layer is 4 times larger than $d_{model}$ (e.g., $d_{model}=512, d_{ff}=2048$).

### Add & Norm
For any sub-layer (Self-Attention or FFN), the output with Add & Norm is:
$$ \text{Output} = \text{LayerNorm}(x + \text{Sublayer}(x)) $$
Note: In modern architectures (like GPT-3, LLaMA), it is common to apply LayerNorm *before* the sub-layer (Pre-LN) instead of after (Post-LN), which further stabilizes training.
Pre-LN formulation:
$$ \text{Output} = x + \text{Sublayer}(\text{LayerNorm}(x)) $$

### The Transformer Encoder Block
1. Input $X$
2. Multi-Head Attention: $X_{att} = \text{MHA}(X, X, X)$
3. Add & Norm: $X_1 = \text{LayerNorm}(X + X_{att})$
4. Feed Forward: $X_{ff} = \text{FFN}(X_1)$
5. Add & Norm: $X_{out} = \text{LayerNorm}(X_1 + X_{ff})$

## Summary of the Full Architecture
An entire Transformer model consists of an **Encoder** (which processes the input text) and a **Decoder** (which generates the output text autoregressively).
- **Encoder:** N stacked Encoder blocks. Uses standard Self-Attention (no causal mask).
- **Decoder:** N stacked Decoder blocks. 
  - Uses **Masked** Self-Attention (to prevent looking into the future).
  - Contains an additional **Cross-Attention** layer, where Queries come from the Decoder, but Keys and Values come from the output of the Encoder.

## Interview Questions
1. **Why is the FFN called "position-wise"?**
   *Answer:* Because the exact same multi-layer perceptron (with the exact same weights) is applied independently to each position (token) in the sequence. There is no communication across positions in this layer.
2. **What is the difference between Batch Normalization and Layer Normalization, and why do Transformers use LayerNorm?**
   *Answer:* BatchNorm computes the mean and variance across the batch dimension for each feature. LayerNorm computes the mean and variance across the feature dimension for each token independently. Transformers process sequences of varying lengths, making batch statistics unstable (especially for long sequences with small batch sizes). LayerNorm is independent of batch size and sequence length.
