"""
Natural Language Processing (NLP) Basics
----------------------------------------
This script covers fundamental NLP components using PyTorch.
Topics covered:
1. Basic Tokenization and Vocabulary Generation
2. Word Embeddings (nn.Embedding)
3. Recurrent Neural Networks (RNN)
4. Basic Self-Attention Mechanism
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

# ==========================================
# 1. Text Processing: Vocabulary & Tokenization
# ==========================================
def build_vocab_and_tokenize():
    print("=== 1. Tokenization and Vocabulary ===")
    corpus = [
        "deep learning is fascinating",
        "natural language processing with pytorch",
        "learning is fun"
    ]
    
    # Simple whitespace tokenizer
    words = []
    for sentence in corpus:
        words.extend(sentence.split())
        
    unique_words = sorted(set(words))
    
    # Create word to index mapping (0 reserved for padding/unknown)
    word_to_idx = {word: idx + 1 for idx, word in enumerate(unique_words)}
    word_to_idx["<PAD>"] = 0
    idx_to_word = {idx: word for word, idx in word_to_idx.items()}
    
    print("Vocabulary:")
    print(word_to_idx)
    
    # Tokenize a sentence
    sample_sentence = "deep learning with pytorch"
    tokenized = [word_to_idx.get(w, 0) for w in sample_sentence.split()]
    print(f"\nTokenizing: '{sample_sentence}' -> {tokenized}")
    return word_to_idx

# ==========================================
# 2. Word Embeddings
# ==========================================
def test_embeddings(word_to_idx):
    print("\n=== 2. Word Embeddings ===")
    vocab_size = len(word_to_idx)
    embedding_dim = 4 # Small dimension for demonstration
    
    # Initialize Embedding layer
    embedding_layer = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
    
    # Input sequence (batch_size=1, seq_length=4)
    input_seq = torch.tensor([[word_to_idx["deep"], word_to_idx["learning"], word_to_idx["is"], word_to_idx["fun"]]])
    
    embedded_seq = embedding_layer(input_seq)
    print(f"Input shape: {input_seq.shape}")
    print(f"Embedded output shape: {embedded_seq.shape} (Batch, Seq_Len, Embedding_Dim)")
    print(f"Embedding for 'learning':\n{embedded_seq[0, 1, :]}")

# ==========================================
# 3. Recurrent Neural Networks (RNN)
# ==========================================
class SimpleRNNModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(SimpleRNNModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        # batch_first=True makes input shape (batch, seq, feature)
        self.rnn = nn.RNN(input_size=embedding_dim, hidden_size=hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # x shape: (batch_size, seq_length)
        embedded = self.embedding(x)
        # embedded shape: (batch_size, seq_length, embedding_dim)
        
        # RNN outputs: 
        # out: hidden states for every time step
        # hidden: hidden state of the final time step
        out, hidden = self.rnn(embedded)
        
        # We often use the final hidden state for sequence classification
        final_output = self.fc(hidden.squeeze(0))
        return final_output

def test_rnn(word_to_idx):
    print("\n=== 3. Simple RNN ===")
    model = SimpleRNNModel(vocab_size=len(word_to_idx), embedding_dim=8, hidden_dim=16, output_dim=2)
    
    # Dummy input
    input_seq = torch.tensor([[1, 2, 3], [4, 5, 0]]) # Batch of 2 sequences
    output = model(input_seq)
    print(f"RNN output shape (batch_size, output_dim): {output.shape}")

# ==========================================
# 4. Basic Self-Attention Mechanism
# ==========================================
def self_attention():
    print("\n=== 4. Self-Attention Mechanism ===")
    # Assume we have an embedded sequence (Batch=1, Seq_Len=3, Embedding_Dim=4)
    seq_len, d_model = 3, 4
    x = torch.randn(1, seq_len, d_model)
    
    # In practice, W_q, W_k, W_v are learnable linear layers
    # Here we just use the embeddings themselves for simplicity (Query = Key = Value = x)
    Q = x
    K = x
    V = x
    
    # 1. Calculate Attention Scores (Q * K^T)
    # Transpose K on the last two dimensions
    scores = torch.bmm(Q, K.transpose(1, 2)) 
    
    # 2. Scale the scores
    scale = d_model ** 0.5
    scaled_scores = scores / scale
    
    # 3. Apply Softmax to get Attention Weights
    attention_weights = F.softmax(scaled_scores, dim=-1)
    
    # 4. Multiply weights by Values
    context_vector = torch.bmm(attention_weights, V)
    
    print("Input (Q, K, V):")
    print(x[0])
    print("\nAttention Weights (Seq_Len x Seq_Len):")
    print(attention_weights[0])
    print("\nOutput Context Vector:")
    print(context_vector[0])

if __name__ == "__main__":
    word_to_idx = build_vocab_and_tokenize()
    test_embeddings(word_to_idx)
    test_rnn(word_to_idx)
    self_attention()
