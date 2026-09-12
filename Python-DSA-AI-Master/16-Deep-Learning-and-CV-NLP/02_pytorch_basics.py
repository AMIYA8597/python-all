"""
PyTorch Basics and Intermediate
-------------------------------
This script covers the essentials of PyTorch, an open-source machine learning framework.
Topics covered:
1. Tensors and Basic Operations
2. Autograd (Automatic Differentiation)
3. Defining Neural Networks using torch.nn
4. Dataset and DataLoader
5. Complete Training Loop
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import numpy as np

def run_tensor_operations():
    print("=== 1. PyTorch Tensors ===")
    # Creating tensors
    t1 = torch.tensor([1, 2, 3])
    t2 = torch.zeros(2, 3)
    t3 = torch.randn(2, 3)  # Standard normal distribution
    
    print("Tensor 1:\n", t1)
    print("Tensor 2:\n", t2)
    print("Tensor 3:\n", t3)
    
    # Operations
    a = torch.tensor([1.0, 2.0])
    b = torch.tensor([3.0, 4.0])
    print("Addition:", a + b)
    print("Dot product:", torch.dot(a, b))
    
    # Reshaping
    t4 = torch.arange(6).view(2, 3)
    print("Reshaped Tensor (2x3):\n", t4)
    print()

def run_autograd():
    print("=== 2. Autograd (Automatic Differentiation) ===")
    # requires_grad=True tells PyTorch to track operations on this tensor
    x = torch.tensor([2.0], requires_grad=True)
    y = x ** 3 + 4 * x
    
    # Compute gradients (dy/dx)
    y.backward()
    
    # dy/dx = 3x^2 + 4. At x=2, dy/dx = 3(4) + 4 = 16
    print(f"y = x^3 + 4x, at x=2")
    print(f"dy/dx computed by autograd: {x.grad.item()}\n")

# ==========================================
# 3. Defining a Neural Network
# ==========================================
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNet, self).__init__()
        # Define layers
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # Define the forward pass
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

def run_training_loop():
    print("=== 3. Training Loop with torch.nn and DataLoader ===")
    
    # Generate some synthetic data (e.g., classifying points in 2D)
    np.random.seed(42)
    torch.manual_seed(42)
    
    X_np = np.random.randn(200, 2)
    # y = 1 if point is in quadrant 1 or 3, else 0
    Y_np = np.logical_xor(X_np[:, 0] > 0, X_np[:, 1] > 0).astype(np.float32)
    
    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X_np, dtype=torch.float32)
    Y_tensor = torch.tensor(Y_np, dtype=torch.float32).view(-1, 1) # Reshape to [200, 1]
    
    # Create DataLoader
    dataset = TensorDataset(X_tensor, Y_tensor)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    # Model, Loss, Optimizer
    input_size = 2
    hidden_size = 8
    output_size = 1
    
    model = SimpleNet(input_size, hidden_size, output_size)
    
    # Binary Cross Entropy with Logits Loss (combines Sigmoid + BCE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    epochs = 50
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch_X, batch_Y in dataloader:
            # 1. Forward pass
            outputs = model(batch_X)
            
            # 2. Compute loss
            loss = criterion(outputs, batch_Y)
            
            # 3. Zero the gradients
            optimizer.zero_grad()
            
            # 4. Backward pass
            loss.backward()
            
            # 5. Optimize (update weights)
            optimizer.step()
            
            epoch_loss += loss.item()
            
        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss/len(dataloader):.4f}")
            
    print("Training finished!")
    
    # Test on a few samples
    with torch.no_grad(): # Disable gradient tracking for inference
        test_pts = torch.tensor([[1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]])
        preds_logits = model(test_pts)
        preds_probs = torch.sigmoid(preds_logits)
        preds_classes = (preds_probs > 0.5).float()
        
        print("\nPredictions on Test Points:")
        for pt, prob, cls in zip(test_pts, preds_probs, preds_classes):
            print(f"Point: {pt.numpy()}, Probability: {prob.item():.4f}, Predicted Class: {int(cls.item())}")


if __name__ == "__main__":
    run_tensor_operations()
    run_autograd()
    run_training_loop()
