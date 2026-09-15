import os

markdown_content = """# The Transformer Block: Feed-Forward Networks, Residuals, and Layer Normalization

## 1. Introduction: The Engine of the Transformer Architecture

The Transformer architecture, introduced by Vaswani et al. in the landmark 2017 paper "Attention Is All You Need," revolutionized the field of Natural Language Processing (NLP) and, subsequently, Computer Vision (CV), audio processing, and computational biology. While the Multi-Head Self-Attention mechanism often claims the spotlight for its ability to model global dependencies, long-range interactions, and contextual relationships without recurrence or convolutions, attention alone is merely a routing mechanism. It determines *where* to look, but it does not inherently possess the non-linear processing power to deeply transform the features it routes.

The true workhorse that processes these attention-contextualized representations, regularizes the learning process, and allows for the construction of immensely deep and powerful neural networks is the **Transformer Block** (often referred to as a Transformer layer).

A single Transformer Block is a meticulously designed composite structure combining several critical components operating in a specific sequence:
1.  **Multi-Head Attention (MHA):** Calculates token-to-token interactions, aggregating context from across the entire sequence.
2.  **Point-Wise Feed-Forward Network (FFN):** A two-layer multi-layer perceptron (MLP) applied independently and identically to every sequence position, providing non-linear feature transformation.
3.  **Residual Connections (Skip Connections):** Additive bypasses that alleviate the vanishing gradient problem, allowing error gradients to flow directly through the network during backpropagation.
4.  **Normalization (LayerNorm or RMSNorm):** A technique to stabilize the hidden state dynamics, ensuring smooth, robust, and fast training.

Modern Large Language Models (LLMs) like GPT-4, LLaMA-3, Claude 3, and Gemini are essentially massive stacks of these uniform Transformer Blocks. A small model might have 12 blocks, while a state-of-the-art frontier model might have 96, 128, or even more blocks stacked sequentially. Understanding the intricate interplay between the FFN, the residual stream, and normalization is absolutely essential for grasping how these models scale to hundreds of billions or even trillions of parameters without collapsing during training. 

This chapter provides a textbook-level deep dive into these components, exploring their mathematics, their architectural significance, the intuition behind their design, modern variants, and complete PyTorch implementation details.

---

## 2. The Point-Wise Feed-Forward Network (FFN)

Following the Multi-Head Attention sublayer, the Transformer Block routes the output through a fully connected Feed-Forward Network (FFN). The crucial characteristic of this FFN is that it is applied **point-wise** (or position-wise). This means the exact same neural network, with the exact same weights, is applied independently to each token position in the sequence. 

If we have a sequence of 1,024 tokens, the FFN is essentially applied 1,024 times in parallel. There is no communication across positions within the FFN; all cross-token communication has already happened in the preceding Self-Attention sublayer.

### 2.1. Mathematical Formulation and Dimensionality

Let $x_i$ be the hidden representation of the token at position $i$ in the sequence, where $x_i \in \mathbb{R}^{d_{model}}$. The position-wise FFN consists of two linear transformations with a non-linear activation function in between:

$$ \text{FFN}(x_i) = \text{Activation}(x_i W_1 + b_1) W_2 + b_2 $$

Where:
*   $W_1 \in \mathbb{R}^{d_{model} \times d_{ff}}$ is the weight matrix of the first linear layer.
*   $b_1 \in \mathbb{R}^{d_{ff}}$ is the bias of the first linear layer.
*   $W_2 \in \mathbb{R}^{d_{ff} \times d_{model}}$ is the weight matrix of the second linear layer.
*   $b_2 \in \mathbb{R}^{d_{model}}$ is the bias of the second linear layer.

In terms of tensor operations across an entire sequence $X \in \mathbb{R}^{N \times d_{model}}$ (where $N$ is sequence length), this is often implemented as a 1D convolution with kernel size 1, or simply a standard linear layer applied over the last dimension.

### 2.2. The Expansion Factor: Creating Capacity

A defining feature of the FFN in Transformers is the inner dimensionality, $d_{ff}$ (often called the hidden dimension of the FFN). Typically, $d_{ff}$ is substantially larger than the model dimension $d_{model}$. 

In the original Transformer paper, Vaswani et al. used $d_{model} = 512$ and $d_{ff} = 2048$. This represents an **expansion factor of 4**. This ratio has remained standard practice for years, seen in models like BERT, GPT-2, and RoBERTa.

Why expand the dimensionality only to project it back down?
1.  **Feature Transformation:** Self-attention is fundamentally an averaging operation (a weighted sum of value vectors). While it contextualizes tokens, it doesn't apply highly complex non-linear transformations to the features themselves. The FFN acts as a universal function approximator for each token's feature vector. The expansion to $d_{ff}$ provides a high-dimensional space where complex non-linear combinations of features can be separated and learned effectively.
2.  **Parameter Dominance and Memorization:** In a standard Transformer, the FFN contains the vast majority of the block's parameters. If $d_{model} = d$, the attention layer has roughly $4d^2$ parameters (for Q, K, V, and Output projections), while the FFN has $2 \times d \times 4d = 8d^2$ parameters. The FFN constitutes two-thirds of the total parameters. The sheer scale of the FFN is what allows LLMs to memorize vast amounts of factual knowledge, linguistic patterns, and world state from their training data.

### 2.3. The FFN as a Key-Value Associative Memory

Groundbreaking research (such as "Transformer Feed-Forward Layers Are Key-Value Memories" by Geva et al.) has provided a compelling intuitive interpretation of the FFN.

We can view the two linear layers as a Key-Value memory system:
*   **The First Layer ($W_1$) acts as Keys:** The rows of $W_1^T$ can be seen as $d_{ff}$ different "keys" or pattern detectors. When a token representation $x_i$ is multiplied by $W_1$, the network computes the dot-product similarity between the token and each of the $d_{ff}$ keys. 
*   **The Activation Function acts as a Threshold/Gating mechanism:** The activation (like ReLU or GELU) ensures that only keys that have a high similarity to the input $x_i$ are "activated." If the dot product is negative, ReLU zeroes it out, meaning that specific memory cell is not triggered.
*   **The Second Layer ($W_2$) acts as Values:** The rows of $W_2$ correspond to "values" or concepts. If a specific index in the hidden state is activated (because the token matched a specific key in $W_1$), the corresponding row in $W_2$ is added to the output representation.

Under this lens, the FFN is continuously matching the contextualized token against a vast vocabulary of learned patterns, and retrieving specific feature updates to add back into the token's representation.

### 2.4. Evolution of Activation Functions

The choice of activation function between the two linear layers has evolved significantly:

1.  **ReLU (Rectified Linear Unit):** Used in the original Transformer. $\text{ReLU}(x) = \max(0, x)$. It is fast and prevents the vanishing gradient problem in the positive domain, but suffers from "dead neurons" if inputs consistently fall below zero.
2.  **GELU (Gaussian Error Linear Unit):** Popularized by BERT and GPT-2, GELU is a smooth approximation of ReLU. It weighs inputs by their percentile in a Gaussian distribution: $\text{GELU}(x) = x \Phi(x)$, where $\Phi(x)$ is the cumulative distribution function of the standard normal distribution. Unlike ReLU, GELU allows a small, non-zero gradient for negative values, which empirically leads to better convergence and final performance in deep networks.
3.  **Swish / SiLU (Sigmoid Linear Unit):** $\text{Swish}(x) = x \cdot \sigma(x)$. Functionally very similar to GELU, it is widely used in modern models.

### 2.5. Gated Linear Units (GLU) and SwiGLU

In current state-of-the-art models like LLaMA, PaLM, and Mistral, the standard two-layer FFN is replaced by a variant incorporating a **Gated Linear Unit (GLU)**. The most popular variant is **SwiGLU**.

A SwiGLU FFN involves three weight matrices ($W_1, W_2, W_3$) instead of two, and changes the information flow:

$$ \text{SwiGLU-FFN}(x_i) = \left( \text{Swish}(x_i W_1) \odot (x_i W_3) \right) W_2 $$

Here, the input $x_i$ is projected into two different spaces using $W_1$ and $W_3$. One projection passes through a Swish activation, acting as a dynamic gate that element-wise multiplies ($\odot$) the other linear projection. Finally, $W_2$ projects the result back to $d_{model}$.

To maintain the same parameter count as a standard FFN, the expansion factor is typically reduced from 4 to something like $\frac{8}{3}$ (e.g., in LLaMA, $d_{model} = 4096$, $d_{ff} = 11008$). Empirical studies (like the PaLM paper and Shazeer's GLU variants paper) show that SwiGLU consistently yields better scaling laws and downstream performance, justifying the slight increase in computational complexity.

---

## 3. Residual Connections (Skip Connections)

Deep neural networks face a fundamental mathematical obstacle known as the **vanishing gradient problem**. As the error signal is backpropagated from the loss function through dozens or hundreds of layers, repeated multiplication by weight matrices and derivatives of activation functions can cause the gradient to shrink exponentially toward zero. This effectively prevents the earlier layers from learning, stalling training completely.

To solve this, He et al. introduced **Residual Connections** (or Skip Connections) in the ResNet architecture for computer vision. The Transformer adopts this concept identically, making it possible to stack dozens or hundreds of blocks.

### 3.1. The Residual Paradigm: Learning the Delta

Instead of forcing a sublayer (like the Attention mechanism or the FFN) to learn the complete desired output mapping $\mathcal{H}(x)$, a residual connection forces the sublayer to learn a **residual mapping** $\mathcal{F}(x)$. The final output of the block is then the sum of the input and the residual mapping:

$$ \text{Output} = x + \text{Sublayer}(x) $$

This seemingly simple addition has profound implications for optimization:
1.  **Gradient Superhighways:** During backpropagation, the derivative of the output with respect to the input $x$ is:
    $$ \frac{\partial}{\partial x} (x + \mathcal{F}(x)) = 1 + \mathcal{F}'(x) $$
    The "$1$" is crucial. It ensures that the gradient can flow directly back through the addition operation entirely undiminished, bypassing the complex non-linear sublayer $\mathcal{F}(x)$. This allows networks to be stacked infinitely deep without gradients vanishing completely. The error signal reaches the very first layer as clearly as it reaches the last.
2.  **Identity Mapping as Baseline:** If a layer is not needed (i.e., it cannot extract any useful features beyond what is already present in the representation), the network can simply push the weights of $\mathcal{F}(x)$ toward zero. This reduces the layer to an identity function ($x + 0 = x$). This theoretical guarantee ensures that adding more layers to a network will strictly never degrade its performance (in training), making deep networks strictly more powerful than shallow ones.

### 3.2. The Residual Stream: The Backbone of the LLM

In the context of Transformers and LLMs, the central path passing through these additions is universally termed the **"Residual Stream"** (or sometimes the "Residual Bus").

Think of the residual stream as a high-bandwidth communication bus running linearly from the input embedding layer all the way to the final language modeling head. The tokens move along this bus. Each sublayer (Attention and FFN) acts as a station that reads from this bus, performs a computation, and writes the result back to the bus by *adding* its output.

*   **Attention writes context:** It reads the token representations, figures out what other tokens in the sequence are relevant, and writes this contextual information back to the specific token's representation in the stream.
*   **FFN writes transformed features:** It reads the newly contextualized vector, transforms it to extract higher-order features or retrieve memorized facts, and writes this transformation back.

Because the interaction with the stream is strictly additive, the original information (like the initial word embeddings) is never explicitly overwritten or destroyed. Instead, it is iteratively refined. A feature computed in Layer 2 can persist cleanly in the residual stream all the way to Layer 96. This additive property is why techniques like "Logit Lens" (probing the residual stream at intermediate layers) work so well to understand what an LLM is "thinking."

---

## 4. Layer Normalization (Add & Norm)

Normalization is a mandatory ingredient for training deep networks. Without it, the scale and variance of hidden activations tend to drift, explode, or collapse as they pass through successive layers and non-linearities. This phenomenon makes optimization extremely difficult, leading to divergent loss spikes, the need for microscopic learning rates, and extreme sensitivity to weight initialization.

### 4.1. Why not Batch Normalization?

In Convolutional Neural Networks (CNNs), **Batch Normalization (BatchNorm)** is the undisputed standard. BatchNorm normalizes features *across the batch dimension*. For a given channel/feature, it computes the mean and variance across all items in the current mini-batch.

However, BatchNorm is highly problematic for NLP and sequence modeling for several reasons:
1.  **Variable Sequence Lengths:** Text sentences have varying lengths. Padding is required to create a batch, which introduces zero-vectors that skew batch statistics.
2.  **Small Micro-Batch Sizes:** Due to massive memory constraints, large LLMs often train with very small micro-batch sizes per GPU (sometimes a batch size of 1). BatchNorm statistics become highly noisy, inaccurate, and unstable at small batch sizes.
3.  **Autoregressive Generation (Inference):** During inference (generating text one token at a time), there is no "batch" to compute statistics over. BatchNorm requires maintaining complicated exponentially moving averages during training to use at inference time, which is cumbersome and often leads to train-test divergence.

To resolve this, Ba et al. introduced **Layer Normalization (LayerNorm)**, which changes the axis of normalization. Instead of normalizing across the batch, LayerNorm normalizes **across the feature dimension for each individual sequence element independently**.

### 4.2. Mathematics of Layer Normalization

Given an input vector $x_i \in \mathbb{R}^{d_{model}}$ (the representation of a single token in the sequence at a specific layer), Layer Normalization calculates the mean ($\mu$) and variance ($\sigma^2$) across its $d_{model}$ features:

$$ \mu = \frac{1}{d_{model}} \sum_{j=1}^{d_{model}} x_{i, j} $$
$$ \sigma^2 = \frac{1}{d_{model}} \sum_{j=1}^{d_{model}} (x_{i, j} - \mu)^2 $$

The vector is then normalized to have zero mean and unit variance, and subsequently scaled and shifted by learnable parameters:

$$ \text{LayerNorm}(x_i) = \gamma \odot \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta $$

Where:
*   $\epsilon$ is a small constant (e.g., $1e-5$) added to the variance for numerical stability to avoid division by zero.
*   $\gamma \in \mathbb{R}^{d_{model}}$ is a learned scaling parameter (gain). It allows the network to undo the normalization if scaling is necessary.
*   $\beta \in \mathbb{R}^{d_{model}}$ is a learned shifting parameter (bias).
*   $\odot$ denotes element-wise multiplication.

Crucially, LayerNorm is completely independent of the batch size and the sequence length. A sequence of length 1 undergoes the exact same mathematical normalization logic as a sequence of length 8192.

### 4.3. RMSNorm: The Modern Successor

While standard LayerNorm is robust, calculating the mean and centering the data is computationally expensive. Recently, researchers discovered that centering the mean is not strictly necessary for the success of normalization in Transformers.

**Root Mean Square Normalization (RMSNorm)**, introduced by Zhang and Sennrich, simplifies LayerNorm by removing the mean-centering step and only normalizing by the Root Mean Square of the activations.

$$ \text{RMS}(x_i) = \sqrt{\frac{1}{d_{model}} \sum_{j=1}^{d_{model}} x_{i, j}^2 + \epsilon} $$
$$ \text{RMSNorm}(x_i) = \gamma \odot \frac{x_i}{\text{RMS}(x_i)} $$

Notice there is no mean $\mu$ calculation, and often the bias $\beta$ is also dropped. RMSNorm is strictly faster to compute (saving 10-20% time on normalization ops) while matching the performance of LayerNorm. It has become the de-facto standard in frontier models, heavily utilized in the LLaMA family, Mistral, and Gemma.

### 4.4. Pre-LN vs. Post-LN Architecture: A Critical Design Choice

The exact placement of the Normalization layer within the Transformer Block is a critical architectural decision that deeply impacts trainability. 

**Post-LN (The Original Design):**
The original 2017 Transformer paper placed the Layer Normalization *after* the residual addition. 

$$ x_{out} = \text{LayerNorm}(x_{in} + \text{Sublayer}(x_{in})) $$

While Post-LN works acceptably for shallower networks (like the original 6-layer Encoder/Decoder), researchers quickly found that it causes severe instabilities when scaling up to deeper networks (e.g., >12 layers). In Post-LN, the gradients near the output layer become exponentially larger than gradients near the input layer. This requires an extremely delicate learning rate "warm-up" schedule (starting with a tiny learning rate and slowly increasing it) to prevent the network from diverging in the first few thousand steps.

**Pre-LN (The Modern Standard):**
Modern architectures (including GPT-2, GPT-3, BERT variations, LLaMA, and almost all contemporary LLMs) use **Pre-LN**:

$$ x_{out} = x_{in} + \text{Sublayer}(\text{LayerNorm}(x_{in})) $$

In Pre-LN, the normalization is applied to the input *before* it enters the sublayer (Attention or FFN). The residual connection itself bypasses the normalization completely. 

This design ensures that the residual stream remains entirely uninterrupted and un-normalized from input to output. The variance of the stream grows linearly with depth, which keeps the variance of the gradients perfectly stable regardless of how many layers are stacked. Pre-LN models are significantly more robust, can often be trained with less aggressive warm-up, and converge much more reliably at massive scales.

---

## 5. Assembling the Complete Transformer Block

By combining these four elements—Attention, FFN, Residuals, and Normalization—we form the standard Transformer Block. There are two primary architectural variants depending on whether the block resides in an Encoder or a Decoder.

### 5.1. The Encoder Block

The Encoder block processes the entire input sequence simultaneously, building a rich, bidirectional, non-causal representation. It is the core of models like BERT (Bidirectional Encoder Representations from Transformers).

It consists of two sublayers. Assuming a modern Pre-LN configuration, the forward pass is:

1.  **Sublayer 1: Self-Attention**
    $$ \text{residual}_1 = \text{LayerNorm}(x) $$
    $$ h_1 = x + \text{MultiHeadSelfAttention}(\text{residual}_1) $$
2.  **Sublayer 2: Feed-Forward Network**
    $$ \text{residual}_2 = \text{LayerNorm}(h_1) $$
    $$ \text{output} = h_1 + \text{FFN}(\text{residual}_2) $$

### 5.2. The Decoder Block

The Decoder block is designed for sequence-to-sequence generation (like translation). It must not look ahead at future tokens (prevented by causal masking) and must integrate information from the Encoder's output. It contains three sublayers:

1.  **Sublayer 1: Masked Self-Attention (Causal)**
    $$ h_1 = x + \text{MaskedMultiHeadAttention}(\text{LayerNorm}(x)) $$
2.  **Sublayer 2: Cross-Attention** (Queries come from $h_1$, Keys/Values come from the Encoder output).
    $$ h_2 = h_1 + \text{CrossAttention}(\text{LayerNorm}(h_1), \text{EncoderOut}, \text{EncoderOut}) $$
3.  **Sublayer 3: Feed-Forward Network**
    $$ \text{output} = h_2 + \text{FFN}(\text{LayerNorm}(h_2)) $$

### 5.3. The Decoder-Only Block (LLM Standard)

Most modern Generative AI models (GPT, LLaMA, Claude) are **Decoder-Only** architectures. Because they do not have a separate encoder to attend to, the Cross-Attention sublayer is completely removed. 

Structurally, a Decoder-Only block is identical to an Encoder block, with the single difference that the Multi-Head Attention applies a **causal mask** (a lower-triangular matrix) to ensure tokens can only attend to previous tokens, not future ones.

---

## 6. The Deep Learning Hierarchy: What Happens in the Stack?

A single Transformer Block has a limited capacity to "understand" language. The true emergent power of LLMs arises when these blocks are stacked hierarchically. A base model might contain 12 blocks, while a frontier model might contain 96.

What happens as representations flow through this towering stack of blocks? Research using mechanistic interpretability and probing techniques has revealed a clear hierarchy of feature extraction:

1.  **Bottom Layers (Syntax and Lexical):** The first few layers closest to the embeddings focus on local, surface-level features. They resolve basic syntax, part-of-speech tagging, and immediate word associations. Attention heads here often look at neighboring tokens (previous word, next word) or identical words in the context.
2.  **Middle Layers (Semantics and Structure):** As representations move up, they become increasingly abstract. Middle layers begin resolving coreference (e.g., figuring out what the pronoun "it" refers to), syntactic parsing structures, and local semantics. The FFNs in these layers are highly active in injecting factual knowledge retrieved from their weights based on the context.
3.  **Top Layers (Context, Pragmatics, and Task Alignment):** The final layers hold highly contextualized, abstract representations of the entire input narrative. They combine information globally to resolve complex reasoning, logical deduction, sentiment analysis, long-range dependencies, and the specific task at hand. The very last layer transforms the representation into a space that can be easily projected into logits for the final next-word prediction.

This hierarchical feature extraction is conceptually analogous to Convolutional Neural Networks in vision, where early layers detect simple edges, middle layers detect textures and shapes, and final layers detect complex objects (like faces or cars). In LLMs, the "edges" are words and syntax, and the "objects" are complex thoughts, logic, and narratives.

---

## 7. Production-Grade PyTorch Implementation

Below is a robust, production-style implementation of a modern Decoder-Only Transformer Block in PyTorch. It utilizes Pre-LN architecture, RMSNorm, and a SwiGLU Feed-Forward Network, representing the exact architecture used in state-of-the-art models like LLaMA.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class RMSNorm(nn.Module):
    \"\"\"
    Root Mean Square Normalization (RMSNorm).
    Used in modern LLMs instead of standard LayerNorm for speed.
    \"\"\"
    def __init__(self, d_model: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        # Learnable scaling parameter (gamma)
        self.weight = nn.Parameter(torch.ones(d_model))

    def forward(self, x):
        # Calculate RMS: sqrt(mean(x^2) + eps)
        variance = x.pow(2).mean(-1, keepdim=True)
        x_normed = x * torch.rsqrt(variance + self.eps)
        # Apply scaling
        return self.weight * x_normed

class MultiHeadSelfAttention(nn.Module):
    \"\"\"
    Standard Multi-Head Attention.
    (Simplified for readability; assumes causal masking is handled externally or implicitly).
    \"\"\"
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.q_proj = nn.Linear(d_model, d_model, bias=False)
        self.k_proj = nn.Linear(d_model, d_model, bias=False)
        self.v_proj = nn.Linear(d_model, d_model, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.size()
        
        q = self.q_proj(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        k = self.k_proj(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        v = self.v_proj(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
            
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        context = torch.matmul(attn_weights, v)
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
        
        return self.out_proj(context)

class SwiGLUFeedForward(nn.Module):
    \"\"\"
    SwiGLU Feed-Forward Network used in LLaMA, PaLM, etc.
    d_ff is typically smaller (e.g. 8/3 * d_model) to match parameters of standard FFN.
    \"\"\"
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w3 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_ff, d_model, bias=False)

    def forward(self, x):
        # Swish(x * W1) * (x * W3)
        gate = F.silu(self.w1(x)) # SiLU is equivalent to Swish
        up = self.w3(x)
        # Element-wise multiplication, then project down
        return self.w2(gate * up)

class TransformerBlock(nn.Module):
    \"\"\"
    A complete Pre-LN (Pre-RMSNorm) Decoder-Only Transformer Block.
    \"\"\"
    def __init__(self, d_model: int, num_heads: int, d_ff: int, dropout: float = 0.0):
        super().__init__()
        
        # Sublayer 1: Attention and its pre-norm
        self.norm1 = RMSNorm(d_model)
        self.attention = MultiHeadSelfAttention(d_model, num_heads, dropout)
        
        # Sublayer 2: FFN and its pre-norm
        self.norm2 = RMSNorm(d_model)
        self.ffn = SwiGLUFeedForward(d_model, d_ff)
        
        self.dropout_layer = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        \"\"\"
        x shape: (batch_size, seq_len, d_model)
        \"\"\"
        # 1. Residual Stream 1: Attention
        # Apply RMSNorm -> Attention -> Dropout -> Add to residual stream
        attn_output = self.attention(self.norm1(x), mask)
        x = x + self.dropout_layer(attn_output)
        
        # 2. Residual Stream 2: FFN
        # Apply RMSNorm -> SwiGLU FFN -> Dropout -> Add to residual stream
        ffn_output = self.ffn(self.norm2(x))
        x = x + self.dropout_layer(ffn_output)
        
        return x

# Example Execution
if __name__ == "__main__":
    batch_size = 4
    seq_len = 1024
    d_model = 1024    
    num_heads = 16
    d_ff = 2730      # approx (8/3) * 1024

    # Dummy tensor representing embedded tokens
    dummy_input = torch.randn(batch_size, seq_len, d_model)
    
    # Causal Mask (lower triangular)
    causal_mask = torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).unsqueeze(0)
    
    # Initialize block
    block = TransformerBlock(d_model=d_model, num_heads=num_heads, d_ff=d_ff)
    
    # Forward Pass
    output = block(dummy_input, mask=causal_mask)
    
    print(f"Input shape:  {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
    print("Modern LLaMA-style Transformer Block forward pass successful.")
```

---

## 8. Conclusion

The Transformer Block is an architectural marvel of deep learning engineering, elegantly balancing competing computational requirements. 

*   The **Multi-Head Attention** mechanism provides global context and long-range routing, but is fundamentally linear with respect to value transformations. 
*   The **Point-Wise Feed-Forward Network (FFN)** provides massive non-linear capacity and associative memory, acting locally on each contextualized token to extract high-level semantic features. 
*   **Residual Connections** are the structural steel that guarantees this massive capacity can be stacked dozens or hundreds of layers deep by protecting the flow of gradients and creating an uninterrupted residual stream.
*   **Normalization** (especially modern Pre-RMSNorm) tames the numerical dynamics of the network, preventing activations from exploding and allowing for aggressive, stable training on trillions of tokens without the architecture imploding.

By understanding how these four elements—Attention, FFN, Add, and Norm—harmonize within a single block, you unlock the foundational mechanics underlying all modern Generative AI. Whether translating text, reasoning about complex code, or generating images, the repeated application of this simple yet profound sequence of operations builds the emergent, hierarchical representations that give LLMs their remarkable cognitive-like abilities.
"""

file_path = r"d:\work\python-all\16-Deep-Learning-and-CV-NLP\Transformers\04-Feed-Forward-and-Transformer-Block.md"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Successfully generated textbook-level markdown and saved to: {file_path}")
