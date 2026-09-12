"""
Module: 05-pytorch-basics
Description: A comprehensive, textbook-grade interactive lesson on PyTorch Basics.

===========================================================================
    TEXTBOOK-GRADE LESSON: PyTorch Basics for Deep Learning
===========================================================================

Learning Objectives:
1. Understand PyTorch Tensors, their creation, attributes, and operations.
2. Master Autograd (Automatic Differentiation), the engine of deep learning.
3. Learn `torch.nn` module to build Neural Networks.
4. Understand Data Loaders, Loss Functions, and Optimizers.
5. Build, train, and evaluate a fully-connected Neural Network from scratch.
6. Analyze Big-O complexity for Tensor operations and Neural Network layers.
7. Solve common Machine Learning interview challenges using PyTorch.

---------------------------------------------------------------------------
1. MATHEMATICAL BACKGROUND
---------------------------------------------------------------------------
PyTorch primarily operates on Tensors, which are generalization of vectors and 
matrices to potentially higher dimensions.

1. Scalar (0-D Tensor): A single number. e.g., x = 5
2. Vector (1-D Tensor): An array of numbers. e.g., v = [1, 2, 3]
3. Matrix (2-D Tensor): A 2D array of numbers. e.g., M = [[1, 2], [3, 4]]
4. n-D Tensor: An n-dimensional array.

Forward Pass in a Linear Layer:
    Y = XW^T + b
Where:
- X: Input tensor of shape (N, in_features)
- W: Weight tensor of shape (out_features, in_features)
- b: Bias tensor of shape (out_features)
- Y: Output tensor of shape (N, out_features)

Backpropagation (Autograd):
Given a loss function L(Y, Y_true), PyTorch automatically computes the gradients:
    ∂L/∂W = (∂L/∂Y) * X
    ∂L/∂b = (∂L/∂Y) * 1
Using the Chain Rule.

---------------------------------------------------------------------------
2. BIG-O COMPLEXITY
---------------------------------------------------------------------------
For a Linear Layer with input size (N, I) and output size (N, O):
- Time Complexity (Forward Pass): O(N * I * O) (Matrix Multiplication)
- Space Complexity: O(I * O) to store the weights, O(N * O) for output.
Tensor element-wise operations (e.g., Addition, ReLU):
- Time Complexity: O(E), where E is the total number of elements.
- Space Complexity: O(E) for the output tensor.

===========================================================================
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple

# Try to import torch, fallback gracefully if not installed in the environment
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch is not installed. Please install using `pip install torch`.")

# Set random seeds for reproducibility
if TORCH_AVAILABLE:
    torch.manual_seed(42)
random.seed(42)


# =========================================================================
# 1. TENSORS: THE BUILDING BLOCKS
# =========================================================================

def tensor_basics() -> None:
    """
    Demonstrates the creation, attributes, and operations of PyTorch Tensors.
    """
    if not TORCH_AVAILABLE: return
    print("\n" + "="*50)
    print("1. TENSOR BASICS")
    print("="*50)

    # 1.1 Tensor Creation
    # From a Python list
    t_list = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    
    # Zeros, Ones, Random
    t_zeros = torch.zeros((2, 3))
    t_ones = torch.ones((2, 3))
    t_rand = torch.rand((3, 3)) # Uniform distribution [0, 1)
    t_randn = torch.randn((3, 3)) # Normal distribution (mean=0, std=1)
    
    print(f"Tensor from List:\n{t_list}\n")
    print(f"Random Tensor:\n{t_rand}\n")

    # 1.2 Tensor Attributes
    print("--- Tensor Attributes ---")
    print(f"Shape: {t_rand.shape}")       # Output: torch.Size([3, 3])
    print(f"Data Type: {t_rand.dtype}")   # Output: torch.float32
    print(f"Device: {t_rand.device}\n")   # Output: cpu (or cuda:0)

    # 1.3 Tensor Operations
    print("--- Tensor Operations ---")
    # Element-wise addition
    a = torch.tensor([1, 2, 3])
    b = torch.tensor([4, 5, 6])
    print(f"a + b = {a + b}")
    
    # Matrix Multiplication
    mat1 = torch.tensor([[1, 2], [3, 4]])
    mat2 = torch.tensor([[5, 6], [7, 8]])
    matmul_result = torch.matmul(mat1, mat2)  # or mat1 @ mat2
    print(f"Matrix Multiplication:\n{matmul_result}\n")
    
    # 1.4 Reshaping
    t_flat = torch.arange(1, 13) # [1, 2, ..., 12]
    t_reshaped = t_flat.view(3, 4) # Reshape to 3x4 matrix
    print(f"Reshaped Tensor (view):\n{t_reshaped}\n")


# =========================================================================
# 2. AUTOGRAD: AUTOMATIC DIFFERENTIATION
# =========================================================================

def autograd_demonstration() -> None:
    """
    Demonstrates PyTorch's Autograd mechanism for computing gradients.
    """
    if not TORCH_AVAILABLE: return
    print("\n" + "="*50)
    print("2. AUTOGRAD (AUTOMATIC DIFFERENTIATION)")
    print("="*50)

    # We want to compute gradients with respect to x and y
    # requires_grad=True tells PyTorch to track operations on these tensors
    x = torch.tensor(2.0, requires_grad=True)
    y = torch.tensor(3.0, requires_grad=True)
    
    # Forward pass: Define a computational graph
    # z = x^2 + 3y
    z = x**2 + 3*y
    
    print(f"z = {z.item()}") # 2^2 + 3(3) = 4 + 9 = 13
    
    # Backward pass: Compute gradients
    z.backward()
    
    # Gradients are accumulated in the .grad attribute
    # dz/dx = 2x => at x=2, dz/dx = 4
    # dz/dy = 3 => at y=3, dz/dy = 3
    print(f"dz/dx: {x.grad.item()}") 
    print(f"dz/dy: {y.grad.item()}") 
    
    # IMPORTANT: PyTorch accumulates gradients.
    # In a training loop, you must zero the gradients (optimizer.zero_grad()) 
    # before the next backward pass.


# =========================================================================
# 3. NEURAL NETWORK MODULE (torch.nn)
# =========================================================================

if TORCH_AVAILABLE:
    class SimpleMLP(nn.Module):
        """
        A simple Multi-Layer Perceptron (MLP) for classification.
        Inherits from torch.nn.Module, the base class for all neural network modules.
        """
        def __init__(self, input_size: int, hidden_size: int, num_classes: int):
            super(SimpleMLP, self).__init__()
            # Define the layers
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_size, num_classes)
            
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Defines the forward computation.
            PyTorch automatically generates the backward pass based on this.
            """
            out = self.fc1(x)
            out = self.relu(out)
            out = self.fc2(out)
            return out


def neural_network_building() -> None:
    """
    Demonstrates instantiating and inspecting a Neural Network.
    """
    if not TORCH_AVAILABLE: return
    print("\n" + "="*50)
    print("3. BUILDING NEURAL NETWORKS (torch.nn)")
    print("="*50)

    model = SimpleMLP(input_size=10, hidden_size=20, num_classes=2)
    print(f"Model Architecture:\n{model}\n")
    
    # Inspecting parameters
    print("Model Parameters:")
    for name, param in model.named_parameters():
        print(f"Name: {name}, Shape: {param.shape}, Requires Grad: {param.requires_grad}")
    
    # Mocking an input batch (Batch Size = 5, Features = 10)
    mock_input = torch.randn(5, 10)
    output = model(mock_input)
    print(f"\nOutput Shape: {output.shape}") # Should be [5, 2]


# =========================================================================
# 4. TRAINING LOOP: PUTTING IT ALL TOGETHER
# =========================================================================

def complete_training_loop() -> None:
    """
    Demonstrates a full training loop: data generation, model definition,
    loss function, optimizer, and the epoch iteration.
    """
    if not TORCH_AVAILABLE: return
    print("\n" + "="*50)
    print("4. COMPLETE TRAINING LOOP")
    print("="*50)

    # 4.1 Generate Synthetic Data (Binary Classification)
    # 100 samples, 2 features
    X = torch.randn(100, 2)
    # Target label is 1 if sum of features > 0, else 0
    y = (X.sum(dim=1) > 0).long()
    
    # 4.2 DataLoaders
    # Wrap data in a TensorDataset
    dataset = TensorDataset(X, y)
    # DataLoader handles batching, shuffling, and multiprocessing
    dataloader = DataLoader(dataset, batch_size=10, shuffle=True)

    # 4.3 Initialize Model, Loss Function, and Optimizer
    model = SimpleMLP(input_size=2, hidden_size=8, num_classes=2)
    
    # CrossEntropyLoss combines nn.LogSoftmax() and nn.NLLLoss() in one single class.
    # It is standard for classification tasks.
    criterion = nn.CrossEntropyLoss()
    
    # Stochastic Gradient Descent (SGD) optimizer. Updates model parameters.
    # lr is the Learning Rate.
    optimizer = optim.SGD(model.parameters(), lr=0.1)
    
    # 4.4 Training Loop
    epochs = 10
    print(f"Starting Training for {epochs} epochs...\n")
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        
        for batch_X, batch_y in dataloader:
            # 1. Forward pass: compute predicted outputs by passing inputs to the model
            predictions = model(batch_X)
            
            # 2. Calculate the loss
            loss = criterion(predictions, batch_y)
            
            # 3. Clear the gradients of all optimized variables
            optimizer.zero_grad()
            
            # 4. Backward pass: compute gradient of the loss with respect to model parameters
            loss.backward()
            
            # 5. Perform a single optimization step (parameter update)
            optimizer.step()
            
            epoch_loss += loss.item()
            
        avg_loss = epoch_loss / len(dataloader)
        if (epoch + 1) % 2 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
            
    print("\nTraining completed successfully!")


# =========================================================================
# 5. PERFORMANCE AND EDGE CASES
# =========================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and common PyTorch edge cases.
    """
    print("\n" + "="*50)
    print("5. PERFORMANCE ANALYSIS & EDGE CASES")
    print("="*50)
    print("1. Performance (GPU Utilization): Moving Tensors to GPU using `.to('cuda')`")
    print("   massively speeds up matrix multiplications for large datasets. CPU-GPU")
    print("   data transfer (D2H / H2D) is a bottleneck, minimize it.")
    print("2. Memory Leaks (Gradients): Always call `optimizer.zero_grad()`. Otherwise,")
    print("   gradients accumulate across batches, leading to incorrect updates and ")
    print("   potential OOM (Out of Memory) errors.")
    print("3. Memory Leaks (Evaluation): Use `with torch.no_grad():` during inference.")
    print("   This prevents PyTorch from building computational graphs, saving significant")
    print("   memory and compute.")
    print("4. Edge Case (Shape Mismatch): Broadcasting rules can lead to silent bugs.")
    print("   Always verify shapes using `.shape` before operations like MSE loss.")


# =========================================================================
# 6. INTERVIEW CHALLENGE
# =========================================================================

def interview_challenge() -> None:
    """
    Common Interview Challenge:
    Implement a custom Linear Layer (without using nn.Linear) that supports
    forward and backward passes via Autograd.
    """
    if not TORCH_AVAILABLE: return
    print("\n" + "="*50)
    print("6. INTERVIEW CHALLENGE: CUSTOM LINEAR LAYER")
    print("="*50)
    
    class CustomLinear(nn.Module):
        def __init__(self, in_features: int, out_features: int):
            super().__init__()
            # nn.Parameter automatically registers the tensor as a model parameter
            # Initialize weights randomly, bias as zeros
            self.weight = nn.Parameter(torch.randn(out_features, in_features))
            self.bias = nn.Parameter(torch.zeros(out_features))
            
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            # y = x @ W^T + b
            # x shape: (N, in_features)
            # weight shape: (out_features, in_features) -> transpose -> (in_features, out_features)
            # Output shape: (N, out_features)
            return torch.matmul(x, self.weight.t()) + self.bias
            
    custom_layer = CustomLinear(in_features=3, out_features=2)
    mock_input = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    
    print("Custom Layer Weights:\n", custom_layer.weight)
    print("Custom Layer Bias:\n", custom_layer.bias)
    
    output = custom_layer(mock_input)
    print(f"\nForward Pass Output (Shape {output.shape}):\n{output}")
    
    # Prove that autograd works
    loss = output.sum()
    loss.backward()
    
    print(f"\nGradient w.r.t weights (Autograd calculated):\n{custom_layer.weight.grad}")


# =========================================================================
# 7. UNIT TESTS
# =========================================================================

def run_tests() -> None:
    """
    Simple test suite to validate fundamental tensor shapes and operations.
    """
    if not TORCH_AVAILABLE: return
    print("\n" + "="*50)
    print("7. RUNNING TESTS")
    print("="*50)
    try:
        # Test 1: Tensor Shape
        t = torch.zeros((4, 5))
        assert t.shape == (4, 5), f"Shape mismatch: {t.shape}"
        
        # Test 2: Matrix Multiplication Shape
        a = torch.randn(10, 5)
        b = torch.randn(5, 20)
        c = a @ b
        assert c.shape == (10, 20), f"Matmul shape mismatch: {c.shape}"
        
        # Test 3: Model instantiation
        model = SimpleMLP(10, 20, 2)
        assert isinstance(model, nn.Module), "Model must inherit from nn.Module"
        
        print("All PyTorch tests passed successfully!")
    except AssertionError as e:
        print(f"Test Failed: {e}")
    except Exception as e:
        print(f"Unexpected Error during testing: {e}")


# =========================================================================
# MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":
    print("========== MASTERING PYTORCH BASICS ==========\n")
    
    tensor_basics()
    autograd_demonstration()
    neural_network_building()
    complete_training_loop()
    analyze_performance_and_edge_cases()
    interview_challenge()
    run_tests()
    
    print("\n========== END OF PYTORCH BASICS LESSON ==========\n")
