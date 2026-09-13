"""
Attention Mechanism Example (PyTorch)
Demonstrates Scaled Dot-Product Attention.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class ScaledDotProductAttention(nn.Module):
    def __init__(self):
        super(ScaledDotProductAttention, self).__init__()

    def forward(self, query, key, value, mask=None):
        """
        Args:
            query: Tensor of shape (batch, seq_len_q, d_k)
            key: Tensor of shape (batch, seq_len_k, d_k)
            value: Tensor of shape (batch, seq_len_v, d_v) # generally seq_len_k == seq_len_v
            mask: Optional mask tensor to hide future/padding tokens
        """
        d_k = query.size(-1)
        
        # 1. Dot product of Q and K^T
        # query shape: (batch, seq_len_q, d_k)
        # key.transpose(-2, -1) shape: (batch, d_k, seq_len_k)
        # scores shape: (batch, seq_len_q, seq_len_k)
        scores = torch.matmul(query, key.transpose(-2, -1))
        
        # 2. Scale by sqrt(d_k)
        scores = scores / math.sqrt(d_k)
        
        # Apply mask (e.g., for padding or causal masking in decoders)
        if mask is not None:
            # fill positions where mask is 0 with a very large negative number
            scores = scores.masked_fill(mask == 0, -1e9)
            
        # 3. Softmax to get attention probabilities
        # weights shape: (batch, seq_len_q, seq_len_k)
        attn_weights = F.softmax(scores, dim=-1)
        
        # 4. Multiply with Value
        # value shape: (batch, seq_len_k, d_v)
        # output shape: (batch, seq_len_q, d_v)
        output = torch.matmul(attn_weights, value)
        
        return output, attn_weights

if __name__ == "__main__":
    attention_layer = ScaledDotProductAttention()
    
    batch_size = 2
    seq_len = 4
    d_model = 8 # Dimension of our embeddings/states
    
    # Simulating Q, K, V for self-attention (they all come from the same input sequence)
    # Typically obtained by linear projections: Q = X * W_q, K = X * W_k, V = X * W_v
    Q = torch.randn(batch_size, seq_len, d_model)
    K = torch.randn(batch_size, seq_len, d_model)
    V = torch.randn(batch_size, seq_len, d_model)
    
    output, weights = attention_layer(Q, K, V)
    
    print(f"Input Queries shape: {Q.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Attention Weights shape: {weights.shape}")
    
    print("\nAttention Weights for Batch 0:")
    # rows sum to 1
    print(torch.round(weights[0] * 100) / 100) 
