"""
Sequence Models Example (PyTorch)
Demonstrates a simple LSTM model for Text Classification.
"""

import torch
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, num_layers=1):
        super(LSTMClassifier, self).__init__()
        
        # 1. Embedding Layer: Converts integer token IDs to dense vectors
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # 2. LSTM Layer
        # batch_first=True implies input shape is (batch, seq_len, features)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers, batch_first=True)
        
        # 3. Fully Connected Layer
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        # x shape: (batch_size, seq_len)
        
        # Embeddings: (batch_size, seq_len, embedding_dim)
        embedded = self.embedding(x)
        
        # LSTM output:
        # out shape: (batch_size, seq_len, hidden_dim) - hidden state of all time steps
        # hidden[0] shape: (num_layers, batch_size, hidden_dim) - final hidden state
        # hidden[1] shape: (num_layers, batch_size, hidden_dim) - final cell state
        out, (hidden, cell) = self.lstm(embedded)
        
        # We generally use the final hidden state for classification
        # We take the hidden state of the last layer: hidden[-1]
        final_hidden_state = hidden[-1]
        
        # Pass through fully connected layer
        logits = self.fc(final_hidden_state)
        return logits

if __name__ == "__main__":
    # Hyperparameters
    VOCAB_SIZE = 5000
    EMBEDDING_DIM = 100
    HIDDEN_DIM = 256
    OUTPUT_DIM = 2 # e.g., binary classification (positive/negative)
    
    # Initialize Model
    model = LSTMClassifier(VOCAB_SIZE, EMBEDDING_DIM, HIDDEN_DIM, OUTPUT_DIM)
    print(model)
    
    # Dummy Input: Batch of 3 sentences, each with length 10
    # Values are token IDs representing words
    dummy_input = torch.randint(0, VOCAB_SIZE, (3, 10))
    print(f"\nInput shape: {dummy_input.shape}")
    
    # Forward pass
    output = model(dummy_input)
    print(f"Output shape (logits): {output.shape}")
    print(output)
