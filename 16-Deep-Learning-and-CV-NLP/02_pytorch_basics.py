"""
# 02 - Deep Learning: PyTorch Masterclass

## A. Concept Name
PyTorch: Tensors, Autograd, Neural Networks (nn.Module), and the Training Loop.

## B. One-Sentence Definition
PyTorch is a highly-flexible Deep Learning framework that replaces NumPy arrays with GPU-accelerated "Tensors" and uses a dynamic engine ("Autograd") to automatically calculate calculus derivatives, allowing you to train massive neural networks without writing math by hand.

## C. Why Does This Exist?
If you built a Neural Network using NumPy, you would have to calculate the derivatives (Gradients) for every single weight by hand using the Chain Rule. If you change your network architecture, you have to rewrite all the calculus.
PyTorch fixes this. You define the network, do a forward pass, and call `.backward()`. PyTorch mathematically traces exactly what happened and computes the gradients for you instantly. 
Also, NumPy only runs on CPUs. PyTorch Tensors run on NVIDIA GPUs, making matrix multiplications 10,000x faster.

## D. Intuition & Real-World Analogy
- **Tensor**: A NumPy array that has a passport to travel to the GPU.
- **Autograd (requires_grad=True)**: A tape recorder. When you do math with this tensor, PyTorch records every operation. When you hit "Rewind" (`.backward()`), it plays the math in reverse to calculate the gradients.
- **Optimizer**: The steering wheel. It uses the gradients to adjust the weights in the right direction.

## E. The 5 Steps of the PyTorch Training Loop
For EVERY batch of data, you MUST do these 5 things in this exact order:
1. `outputs = model(inputs)`: **Forward Pass** (Make a prediction).
2. `loss = criterion(outputs, labels)`: **Calculate Loss** (How wrong was the prediction?).
3. `optimizer.zero_grad()`: **Clear Gradients** (Wipe the tape recorder clean from the last batch).
4. `loss.backward()`: **Backward Pass** (Calculate the gradients for this batch).
5. `optimizer.step()`: **Update Weights** (Adjust the weights using the gradients).

## F. Common Mistakes & Anti-Patterns
1. **Forgetting `optimizer.zero_grad()`**: If you forget this, PyTorch will ADD the new gradients to the old gradients from the last batch. Your weights will explode instantly.
2. **Device Mismatch Error**: `RuntimeError: Expected all tensors to be on the same device`. You sent your model to the GPU (`model.to('cuda')`), but forgot to send your data to the GPU (`inputs.to('cuda')`).
3. **Using Softmax before CrossEntropyLoss**: In PyTorch, `nn.CrossEntropyLoss` and `nn.BCEWithLogitsLoss` automatically apply Softmax/Sigmoid inside them for numerical stability. If you apply Softmax manually beforehand, you ruin the math.

## G. Interview Connection
**Q: "What is the difference between model.train() and model.eval()?"**
A: "`model.train()` enables features like Dropout and Batch Normalization to act normally during training. `model.eval()` turns them off during testing/inference so the model's output is deterministic."

## H. Implementation & Guided Practice
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# ==========================================
# 1. Tensors & Autograd (The Tape Recorder)
# ==========================================
def demonstrate_autograd():
    print("--- 1. Autograd (Automatic Differentiation) ---")
    
    # We want PyTorch to calculate the derivative of y = 3x^2 at x = 2
    # Mathematically: dy/dx = 6x. So at x=2, the gradient should be 12.
    
    # requires_grad=True tells PyTorch: "Record every operation that happens to this tensor!"
    x = torch.tensor([2.0], requires_grad=True)
    print(f"Tensor x: {x}")
    
    # Forward operation
    y = 3 * (x ** 2)
    print(f"y = 3x^2 = {y.item()}")
    
    # The magic of PyTorch:
    y.backward()
    
    # The gradient is stored inside x.grad
    print(f"Calculated Gradient (dy/dx): {x.grad.item()}  <-- Exactly 12.0!")
    print("PyTorch did the calculus for us!\n")

# ==========================================
# 2. Defining a Neural Network
# ==========================================
class XORNetwork(nn.Module):
    """
    A simple FeedForward Neural Network to solve the XOR problem.
    XOR cannot be solved by a linear model; it requires a hidden layer and non-linearity.
    """
    def __init__(self):
        # ALWAYS call the parent class init
        super(XORNetwork, self).__init__()
        
        # Define the layers
        self.hidden = nn.Linear(in_features=2, out_features=8)
        self.activation = nn.ReLU()
        self.output = nn.Linear(in_features=8, out_features=1)
        
    def forward(self, x):
        # Define how data flows through the network
        x = self.hidden(x)
        x = self.activation(x)
        x = self.output(x)
        return x

# ==========================================
# 3. The Holy Grail: The PyTorch Training Loop
# ==========================================
def run_training_loop():
    print("--- 2. The Complete PyTorch Training Loop ---")
    
    # 1. Device Configuration
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 2. Generate XOR Data
    # Inputs: (0,0), (0,1), (1,0), (1,1)
    # Outputs:  0,     1,     1,     0
    X = torch.tensor([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    Y = torch.tensor([[0.0],      [1.0],      [1.0],      [0.0]])
    
    # 3. Create DataLoader (Handles batching and shuffling)
    dataset = TensorDataset(X, Y)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    
    # 4. Initialize Model, Loss, and Optimizer
    model = XORNetwork().to(device)
    
    # BCEWithLogitsLoss = Sigmoid + Binary Cross Entropy Loss.
    # It takes RAW network outputs (logits) and computes loss with high numerical stability.
    criterion = nn.BCEWithLogitsLoss()
    
    # Optimizer defines HOW we update weights. Adam is the industry standard.
    optimizer = optim.Adam(model.parameters(), lr=0.1)
    
    # 5. THE TRAINING LOOP
    epochs = 100
    model.train() # Set to training mode
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        
        for batch_x, batch_y in dataloader:
            # Move data to GPU (if available)
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            
            # STEP 1: Forward Pass
            outputs = model(batch_x)
            
            # STEP 2: Calculate Loss
            loss = criterion(outputs, batch_y)
            
            # STEP 3: Zero the Gradients (CRITICAL)
            optimizer.zero_grad()
            
            # STEP 4: Backward Pass (Calculate Gradients)
            loss.backward()
            
            # STEP 5: Optimizer Step (Update Weights)
            optimizer.step()
            
            epoch_loss += loss.item()
            
        if (epoch + 1) % 25 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {epoch_loss/len(dataloader):.4f}")
            
    print("\n--- 3. Inference / Evaluation ---")
    model.eval() # Set to evaluation mode (disables Dropout/BatchNorm if we had them)
    with torch.no_grad(): # CRITICAL: Turns off Autograd tape recorder to save RAM and speed up inference
        test_inputs = X.to(device)
        raw_logits = model(test_inputs)
        
        # We must manually apply Sigmoid to get probabilities between 0 and 1
        probabilities = torch.sigmoid(raw_logits)
        
        # Convert probabilities to classes (0 or 1)
        predictions = (probabilities >= 0.5).float()
        
        print("Inputs:\n", test_inputs.cpu().numpy())
        print("Predictions:\n", predictions.cpu().numpy())
        print("Target:\n", Y.numpy())


## I. Active Recall Questions
"""
1. Why must you call `optimizer.zero_grad()` in the training loop?
   *Answer: By default, PyTorch ACCUMULATES gradients on every backward pass. If you don't zero them out, the gradients from batch 2 will be added to the gradients of batch 1, ruining the weight updates.*
2. Why do we wrap inference code in `with torch.no_grad():`?
   *Answer: Because we are not training the model, we don't need to calculate gradients. `torch.no_grad()` turns off the Autograd engine, which halves memory usage and makes inference much faster.*
3. What is the difference between `nn.BCELoss` and `nn.BCEWithLogitsLoss`?
   *Answer: `nn.BCELoss` expects probabilities (you must apply Sigmoid yourself). `nn.BCEWithLogitsLoss` expects raw logits and applies Sigmoid internally using the Log-Sum-Exp trick, which prevents numerical underflow/overflow errors.*
"""

if __name__ == "__main__":
    print("========== PYTORCH MASTERCLASS ==========\n")
    demonstrate_autograd()
    run_training_loop()
    print("\n========== MASTERCLASS COMPLETE ==========")
