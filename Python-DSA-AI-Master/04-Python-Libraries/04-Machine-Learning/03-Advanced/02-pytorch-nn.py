"""
=============================================================================
PyTorch Neural Networks (torch.nn) - Masterclass & Textbook
=============================================================================

## A. Core Intuition & Mathematical Background
PyTorch's `torch.nn` module provides an elegant, highly modular framework
for defining and training neural networks. At its core, a neural network is
a composite mathematical function mapping inputs to target outputs.

1. **The Linear Layer (nn.Linear)**
   Given an input vector `x` of size `N`, a linear layer computes:
       y = xW^T + b
   where `W` is a weight matrix of size `M x N`, and `b` is a bias vector
   of size `M`.
   - **Time Complexity (Forward Pass):** O(M * N) per batch element.
   - **Space Complexity:** O(M * N) for weights, O(M) for biases.

2. **Activation Functions (e.g., nn.ReLU)**
   Non-linearities allow the network to learn complex mappings.
       ReLU(z) = max(0, z)
       Sigmoid(z) = 1 / (1 + exp(-z))
   - **Time Complexity:** O(N) where N is the size of the tensor.

3. **Loss Functions (e.g., nn.CrossEntropyLoss)**
   Quantifies the error between the prediction and the target.
   Cross-Entropy for classification:
       L = -sum(y_true * log(y_pred))

## B. PyTorch Architectures (nn.Module)
`nn.Module` is the base class for all neural network modules.
It provides critical functionalities:
- Keeping track of `nn.Parameter`s (weights and biases).
- Handling nested structures (modules within modules).
- Transferring parameters between devices (`.to(device)`).
- Toggling training/evaluation modes (`.train()`, `.eval()`).

## C. The Training Loop Paradigm
A typical training iteration involves:
1. `optimizer.zero_grad()`: Clear old gradients.
2. `outputs = model(inputs)`: Forward pass.
3. `loss = criterion(outputs, targets)`: Compute loss.
4. `loss.backward()`: Backpropagation (compute gradients).
5. `optimizer.step()`: Update weights.

## D. Advanced Layers: Convolutional and Recurrent
- **Convolutional Layers (`nn.Conv2d`)**: Apply filters over spatial data (like images)
  to extract local features and build hierarchical representations.
- **Recurrent Layers (`nn.LSTM`, `nn.GRU`)**: Maintain hidden states to process
  sequential data (like text or time-series).

## E. Best Practices & Optimization
- Use `nn.Sequential` for simple, sequential pipelines to reduce boilerplate.
- Prefer vectorized operations; avoid Python `for` loops inside `forward()`.
- Use `torch.compile` (in PyTorch 2.0+) for JIT compilation.
- Proper initialization (e.g., Xavier/Kaiming) speeds up convergence.

=============================================================================
"""

import math
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from typing import Tuple, List, Dict, Any, Callable

# Set random seed for reproducibility to ensure deterministic outcomes
torch.manual_seed(42)

# ===========================================================================
# 1. THE FOUNDATIONS: TENSORS AND NN PARAMETERS
# ===========================================================================

def explore_nn_parameters() -> None:
    """
    Demonstrates the difference between regular tensors and nn.Parameter.
    nn.Parameter automatically registers itself to an nn.Module when assigned
    as an attribute, meaning it will be returned in model.parameters() and
    optimized by an optimizer.
    """
    print("\n" + "="*60)
    print("1. EXPLORING NN PARAMETERS")
    print("="*60)
    
    # A standard tensor, even with requires_grad=True, is just a tensor.
    standard_tensor = torch.randn(3, 3, requires_grad=True)
    
    # An nn.Parameter is a subclass of torch.Tensor
    parameter_tensor = nn.Parameter(torch.randn(3, 3))
    
    print(f"Standard Tensor type: {type(standard_tensor)}")
    print(f"nn.Parameter type: {type(parameter_tensor)}")
    print(f"Does nn.Parameter require grad by default? {parameter_tensor.requires_grad}")

    class SimpleModel(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.param = nn.Parameter(torch.randn(2, 2))
            self.tensor = torch.randn(2, 2, requires_grad=True)
            
    model = SimpleModel()
    
    # Only 'param' will appear in model.parameters()
    print("\nParameters registered in SimpleModel (notice how 'tensor' is missing!):")
    for name, param in model.named_parameters():
        print(f" - {name}: shape {param.shape}")
        
    print("\nTakeaway: Always use nn.Parameter (or standard layers like nn.Linear) "
          "so the optimizer can track and update the weights.")


# ===========================================================================
# 2. BUILDING BLOCKS: LINEAR LAYERS AND ACTIVATIONS
# ===========================================================================

def analyze_linear_layer() -> None:
    """
    Deep dive into nn.Linear. We will look at its weights, biases, and
    prove the mathematical operation y = xW^T + b.
    """
    print("\n" + "="*60)
    print("2. ANALYZING NN.LINEAR")
    print("="*60)
    
    # Define input size (in_features) and output size (out_features)
    in_features = 4
    out_features = 3
    
    # Initialize linear layer
    linear = nn.Linear(in_features, out_features)
    
    print(f"Linear layer representation: {linear}")
    print(f"Weight matrix shape (out_features, in_features): {linear.weight.shape}")
    print(f"Bias vector shape (out_features): {linear.bias.shape}")
    
    # Create dummy input data (Batch Size, in_features)
    batch_size = 2
    x = torch.randn(batch_size, in_features)
    
    # Forward pass using the PyTorch module
    y_module = linear(x)
    
    # Forward pass using mathematical formulation: xW^T + b
    # .t() transposes the weight matrix. 
    y_math = torch.matmul(x, linear.weight.t()) + linear.bias
    
    print("\nInput tensor x:")
    print(x)
    print("\nPyTorch Module Output y:")
    print(y_module)
    print("\nMathematical Formulation Output y:")
    print(y_math)
    
    # Validate equality
    # allclose is used because floating point arithmetic may have precision variations
    is_equal = torch.allclose(y_module, y_math, atol=1e-6)
    print(f"\nAre the outputs mathematically equivalent? {'YES' if is_equal else 'NO'}")


# ===========================================================================
# 3. ADVANCED LAYERS: CONVOLUTIONS (CNNs)
# ===========================================================================

def explore_conv2d_layer() -> None:
    """
    Demonstrates the mechanics of the nn.Conv2d layer which is the
    fundamental building block for Computer Vision.
    """
    print("\n" + "="*60)
    print("3. EXPLORING CONVOLUTIONAL LAYERS (nn.Conv2d)")
    print("="*60)
    
    # We will simulate processing a 1-channel grayscale image
    in_channels = 1
    out_channels = 16  # Number of filters
    kernel_size = 3    # 3x3 filter
    stride = 1
    padding = 1        # Padding to preserve spatial dimensions
    
    conv_layer = nn.Conv2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=kernel_size,
        stride=stride,
        padding=padding
    )
    
    print(conv_layer)
    
    # Create dummy image: (Batch_Size, Channels, Height, Width)
    batch_size = 4
    height, width = 28, 28
    dummy_images = torch.randn(batch_size, in_channels, height, width)
    
    print(f"Input shape: {dummy_images.shape}")
    
    # Apply convolution
    output_feature_maps = conv_layer(dummy_images)
    
    print(f"Output shape: {output_feature_maps.shape}")
    print("Notice the spatial dimensions (28x28) are preserved due to padding=1.")
    
    # Number of parameters in Conv2d
    params = sum(p.numel() for p in conv_layer.parameters())
    print(f"\nTotal parameters in this Conv layer: {params}")
    print(f"Calculation: (kernel_size^2 * in_channels * out_channels) + out_channels (bias)")
    print(f"             (3*3 * 1 * 16) + 16 = 144 + 16 = {params}")


# ===========================================================================
# 4. MODULAR DESIGN: CUSTOM NEURAL NETWORKS
# ===========================================================================

class MultiLayerPerceptron(nn.Module):
    """
    A robust, scalable Multi-Layer Perceptron (MLP) implementation.
    
    Architecture:
    - Input Layer (in_dim -> hidden_dim)
    - Activation (ReLU)
    - Dropout (Regularization)
    - Hidden Layer (hidden_dim -> hidden_dim)
    - Activation (ReLU)
    - Output Layer (hidden_dim -> out_dim)
    
    Attributes:
        in_dim (int): Dimensionality of input features.
        hidden_dim (int): Number of units in hidden layers.
        out_dim (int): Dimensionality of output features.
        dropout_prob (float): Probability of zeroing an element in Dropout.
    """
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int, dropout_prob: float = 0.2) -> None:
        super().__init__() # CRITICAL: Must call super() to initialize internal Module state
        
        # 1. Defining standard, non-sequential layers
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.relu1 = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout_prob)
        
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.relu2 = nn.ReLU()
        
        self.fc3 = nn.Linear(hidden_dim, out_dim)
        
        # Demonstrating explicit weight initialization (Kaiming/He Initialization)
        self._initialize_weights()
        
    def _initialize_weights(self) -> None:
        """
        Applies Kaiming Normal initialization to linear layers.
        This mitigates vanishing/exploding gradients in deep networks,
        especially when using ReLU activations.
        """
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Defines the computation performed at every call.
        
        Args:
            x (torch.Tensor): Input tensor of shape (batch_size, in_dim).
            
        Returns:
            torch.Tensor: Output tensor of shape (batch_size, out_dim).
        """
        # Pass through Layer 1
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout(x)
        
        # Pass through Layer 2
        x = self.fc2(x)
        x = self.relu2(x)
        
        # Pass through Output Layer
        x = self.fc3(x)
        
        return x

def explore_mlp() -> None:
    """
    Instantiates and tests the MultiLayerPerceptron model.
    """
    print("\n" + "="*60)
    print("4. CUSTOM NEURAL NETWORK ARCHITECTURE (MLP)")
    print("="*60)
    
    # Configuration
    batch_size = 4
    in_dim = 10
    hidden_dim = 16
    out_dim = 2
    
    # Instantiation
    model = MultiLayerPerceptron(in_dim, hidden_dim, out_dim)
    print("Model Architecture:")
    print(model)
    
    # Print number of trainable parameters
    num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\nTotal trainable parameters: {num_params}")
    
    # Dummy input
    x = torch.randn(batch_size, in_dim)
    
    # Training Mode vs Eval Mode
    # Crucial for layers like Dropout and BatchNorm that behave differently
    model.train() # Activates Dropout
    output_train = model(x)
    print(f"\nOutput in train mode (Dropout active):\n{output_train}")
    
    model.eval() # Deactivates Dropout
    with torch.no_grad(): # Disables gradient tracking for inference saving memory and compute
        output_eval = model(x)
    print(f"\nOutput in eval mode (Dropout inactive):\n{output_eval}")


# ===========================================================================
# 5. TRAINING PARADIGM: LOSS AND OPTIMIZATION
# ===========================================================================

def training_loop_demonstration() -> None:
    """
    A comprehensive demonstration of the PyTorch training loop on synthetic data.
    We will build a simple binary classification model using nn.Sequential.
    """
    print("\n" + "="*60)
    print("5. THE TRAINING LOOP PARADIGM")
    print("="*60)
    
    # 1. Create a simple model using nn.Sequential
    model = nn.Sequential(
        nn.Linear(2, 16),
        nn.ReLU(),
        nn.Linear(16, 1) # Outputting raw logits
    )
    
    # 2. Define Loss function and Optimizer
    # BCEWithLogitsLoss combines Sigmoid + Binary Cross Entropy for numerical stability
    criterion = nn.BCEWithLogitsLoss()
    
    # Adam optimizer: Adaptive moment estimation
    # Implements weight decay (L2 Regularization) automatically if specified
    optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
    
    # 3. Generate synthetic data
    # Let's say inputs are 2D coordinates. 
    # Target is 1 if x0 + x1 > 0 else 0 (Linear Decision Boundary)
    num_samples = 2000
    X = torch.randn(num_samples, 2)
    y = (X[:, 0] + X[:, 1] > 0).float().unsqueeze(1) # Shape: (2000, 1)
    
    # Batch processing setup
    batch_size = 64
    num_epochs = 5
    dataset_size = len(X)
    
    print(f"Training a model for {num_epochs} epochs on {dataset_size} samples...")
    start_time = time.time()
    
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        model.train() # Ensure in training mode
        
        # Iterate over batches
        for i in range(0, dataset_size, batch_size):
            # Get batch
            X_batch = X[i:i+batch_size]
            y_batch = y[i:i+batch_size]
            
            # --- THE HOLY TRINITY OF PYTORCH TRAINING ---
            
            # Step A: Zero the gradients
            # By default, gradients accumulate in PyTorch. We must clear them.
            optimizer.zero_grad()
            
            # Step B: Forward pass
            logits = model(X_batch)
            loss = criterion(logits, y_batch)
            
            # Step C: Backward pass & Optimization
            loss.backward() # Computes gradients (dLoss / dWeights)
            optimizer.step() # Updates weights using computed gradients
            
            # --------------------------------------------
            
            epoch_loss += loss.item() * X_batch.size(0)
            
        epoch_loss /= dataset_size
        print(f"Epoch {epoch+1}/{num_epochs} - Loss: {epoch_loss:.4f}")
        
    print(f"Training completed in {time.time() - start_time:.4f} seconds.")
    
    # Evaluation
    model.eval()
    with torch.no_grad():
        test_x = torch.tensor([[2.0, 2.0], [-2.0, -2.0], [0.1, 0.1], [-0.1, -0.1]])
        test_logits = model(test_x)
        # Apply sigmoid to convert logits to probabilities
        test_probs = torch.sigmoid(test_logits)
        test_preds = (test_probs > 0.5).int()
        
    print("\nEvaluation on test points:")
    for point, prob, pred in zip(test_x, test_probs, test_preds):
        print(f"Point {point.tolist()} -> Prob: {prob.item():.4f}, Class: {pred.item()}")


# ===========================================================================
# 6. ADVANCED ARCHITECTURE: A DEEP AUTOENCODER
# ===========================================================================

class AutoEncoder(nn.Module):
    """
    An Autoencoder compresses input data into a latent representation (bottleneck)
    and then reconstructs the original data. 
    Useful for dimensionality reduction, anomaly detection, and generative tasks.
    """
    def __init__(self, input_dim: int, latent_dim: int) -> None:
        super().__init__()
        
        # Encoder: Compresses the input dimension down to latent_dim
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, latent_dim)
        )
        
        # Decoder: Reconstructs the original dimension from latent_dim
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim),
            nn.Sigmoid() # Restricts output to [0, 1] for images
        )
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Returns both the reconstructed image and the latent embedding.
        """
        latent = self.encoder(x)
        reconstructed = self.decoder(latent)
        return reconstructed, latent

def explore_autoencoder() -> None:
    """
    Demonstrates the initialization and a forward pass of an Autoencoder.
    """
    print("\n" + "="*60)
    print("6. ADVANCED: AUTOENCODER ARCHITECTURE")
    print("="*60)
    
    input_dim = 100 # E.g., a flattened 10x10 image
    latent_dim = 8  # Highly compressed representation (Bottleneck)
    
    model = AutoEncoder(input_dim, latent_dim)
    print("Autoencoder Model Structure:")
    print(model)
    
    # Dummy image data (normalized between 0 and 1)
    batch_size = 5
    dummy_images = torch.rand(batch_size, input_dim)
    
    reconstructed_images, latent_vectors = model(dummy_images)
    
    print(f"\nOriginal Input shape: {dummy_images.shape}")
    print(f"Latent Bottleneck shape: {latent_vectors.shape}")
    print(f"Reconstructed Output shape: {reconstructed_images.shape}")
    
    # Calculate Mean Squared Error loss between original and reconstructed
    mse_loss = F.mse_loss(reconstructed_images, dummy_images)
    print(f"Initial MSE Loss (Untrained): {mse_loss.item():.4f}")


# ===========================================================================
# 7. RECURRENT NEURAL NETWORKS (RNNs) / LSTMs
# ===========================================================================

def explore_lstm_layer() -> None:
    """
    Explores recurrent layers used for sequence data like text and time-series.
    """
    print("\n" + "="*60)
    print("7. EXPLORING RECURRENT LAYERS (nn.LSTM)")
    print("="*60)
    
    input_size = 10   # e.g. dimensionality of word embeddings
    hidden_size = 20  # size of hidden state vector
    num_layers = 2    # stacking 2 LSTMs
    
    # batch_first=True means inputs should be (batch_size, sequence_length, input_size)
    lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
    
    print(lstm)
    
    batch_size = 3
    seq_length = 5
    
    # Sequence of embeddings
    dummy_sequence = torch.randn(batch_size, seq_length, input_size)
    print(f"Input sequence shape: {dummy_sequence.shape} -> (Batch, Seq_Len, Features)")
    
    # LSTM returns the output sequence AND the final hidden states
    out, (h_n, c_n) = lstm(dummy_sequence)
    
    print(f"Output sequence shape: {out.shape} -> (Batch, Seq_Len, Hidden_Size)")
    print(f"Final Hidden State h_n shape: {h_n.shape} -> (Num_Layers, Batch, Hidden_Size)")
    print(f"Final Cell State c_n shape: {c_n.shape} -> (Num_Layers, Batch, Hidden_Size)")


# ===========================================================================
# 8. TESTS AND EDGE CASES
# ===========================================================================

def test_shape_mismatches() -> None:
    """
    Demonstrates a common PyTorch error: shape mismatches in matrix multiplication.
    """
    print("\n" + "="*60)
    print("8. EDGE CASES & COMMON ERRORS")
    print("="*60)
    
    linear = nn.Linear(10, 5) # Expects input of size (..., 10)
    
    bad_input = torch.randn(3, 8) # Oops, features dimension is 8, not 10
    
    print("Attempting to pass input of shape (3, 8) to nn.Linear(10, 5)...")
    try:
        linear(bad_input)
    except RuntimeError as e:
        print(f"Caught Expected Exception:\n\t{e}")
        print("\nFix: Ensure that the last dimension of the input matches `in_features` of the linear layer.")

def run_all_tests() -> None:
    """
    Suite of assertions to validate core behaviors.
    """
    print("\n--- Running Unit Tests ---")
    
    # Test 1: MLP instantiation and forward pass
    mlp = MultiLayerPerceptron(10, 20, 5)
    test_tensor = torch.randn(2, 10)
    out = mlp(test_tensor)
    assert out.shape == (2, 5), f"Expected shape (2, 5), got {out.shape}"
    
    # Test 2: AutoEncoder
    ae = AutoEncoder(20, 3)
    ae_in = torch.rand(1, 20)
    reconstructed, latent = ae(ae_in)
    assert reconstructed.shape == (1, 20), "AutoEncoder output shape mismatch."
    assert latent.shape == (1, 3), "AutoEncoder latent shape mismatch."
    
    print("All unit tests passed successfully! The implementation is robust.")


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PYTORCH NEURAL NETWORKS (TORCH.NN) - MASTERCLASS INTERACTIVE LESSON")
    print("=" * 70)
    
    explore_nn_parameters()
    analyze_linear_layer()
    explore_conv2d_layer()
    explore_mlp()
    training_loop_demonstration()
    explore_autoencoder()
    explore_lstm_layer()
    test_shape_mismatches()
    run_all_tests()
    
    print("\n" + "=" * 70)
    print("LESSON COMPLETED SUCCESSFULLY.")
    print("=" * 70)
