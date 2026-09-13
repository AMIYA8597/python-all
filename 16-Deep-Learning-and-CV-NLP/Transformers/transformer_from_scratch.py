import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Linear projections for Q, K, V
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        
        # Final output projection
        self.W_o = nn.Linear(d_model, d_model)
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        # Q, K, V shape: (batch_size, num_heads, seq_len, d_k)
        
        # 1. Q * K^T
        # K.transpose(-2, -1) swaps the last two dimensions -> (batch_size, num_heads, d_k, seq_len)
        # scores shape: (batch_size, num_heads, seq_len, seq_len)
        scores = torch.matmul(Q, K.transpose(-2, -1))
        
        # 2. Scale by sqrt(d_k)
        scores = scores / math.sqrt(self.d_k)
        
        # 3. Apply mask (if provided)
        if mask is not None:
            # Mask contains 0s for tokens to hide, 1s for tokens to keep.
            # We fill the 0 positions with -1e9 (close to negative infinity)
            scores = scores.masked_fill(mask == 0, -1e9)
            
        # 4. Softmax
        attention_weights = F.softmax(scores, dim=-1)
        
        # 5. Multiply by V
        # output shape: (batch_size, num_heads, seq_len, d_k)
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights

    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.size()
        
        # 1. Linear projections
        # x is (batch_size, seq_len, d_model)
        Q = self.W_q(x)
        K = self.W_k(x)
        V = self.W_v(x)
        
        # 2. Split into multiple heads
        # Reshape to (batch_size, seq_len, num_heads, d_k)
        # Transpose to (batch_size, num_heads, seq_len, d_k)
        Q = Q.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        
        # 3. Apply Scaled Dot-Product Attention
        x, self.attention_weights = self.scaled_dot_product_attention(Q, K, V, mask)
        
        # 4. Concatenate heads
        # Transpose back to (batch_size, seq_len, num_heads, d_k)
        # Contiguous is required before view() after transpose
        # View reshapes back to (batch_size, seq_len, d_model)
        x = x.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        
        # 5. Final linear projection
        output = self.W_o(x)
        
        return output

class PositionWiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ff)
        self.fc2 = nn.Linear(d_ff, d_model)
        self.relu = nn.ReLU()

    def forward(self, x):
        # x shape: (batch_size, seq_len, d_model)
        return self.fc2(self.relu(self.fc1(x)))

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        # Post-LN Architecture (Original Transformer)
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        
        self.ffn = PositionWiseFeedForward(d_model, d_ff)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # 1. Multi-Head Attention
        att_output = self.attention(x, mask)
        # 2. Add & Norm
        x = self.norm1(x + self.dropout1(att_output))
        
        # 3. Position-wise Feed Forward
        ffn_output = self.ffn(x)
        # 4. Add & Norm
        x = self.norm2(x + self.dropout2(ffn_output))
        
        return x

# ==========================================
# Testing the implementation
# ==========================================
if __name__ == "__main__":
    batch_size = 2
    seq_len = 5
    d_model = 512
    num_heads = 8
    d_ff = 2048
    
    # Dummy input sequence (e.g. word embeddings + positional encoding)
    x = torch.randn(batch_size, seq_len, d_model)
    
    # Causal Mask (Lower Triangular matrix)
    # 1s allow attention, 0s block attention (future tokens)
    # shape: (seq_len, seq_len), PyTorch broadcasting handles batch & heads
    causal_mask = torch.tril(torch.ones((seq_len, seq_len)))
    
    print("Causal Mask:")
    print(causal_mask)
    
    # Initialize Transformer Block
    block = TransformerBlock(d_model, num_heads, d_ff)
    
    # Forward Pass
    output = block(x, mask=causal_mask)
    
    print("\nInput shape:", x.shape)
    print("Output shape:", output.shape)
