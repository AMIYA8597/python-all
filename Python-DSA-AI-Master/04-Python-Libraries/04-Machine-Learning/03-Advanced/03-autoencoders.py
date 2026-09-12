"""
Module: 03-autoencoders
Description: Textbook-Grade Interactive Lesson on Autoencoders.

=============================================================================
                          AUTOENCODERS (AE)
=============================================================================

Learning Objectives:
1. Understand the theoretical and mathematical foundations of Autoencoders.
2. Construct and train Undercomplete, Sparse, and Denoising Autoencoders from scratch.
3. Comprehend the Big-O Time and Space Complexity of model training and inference.
4. Explore real-world applications: Dimensionality Reduction, Anomaly Detection, and Image Denoising.

-----------------------------------------------------------------------------
1. MATHEMATICAL BACKGROUND
-----------------------------------------------------------------------------
An Autoencoder is an unsupervised artificial neural network that learns to compress
and reconstruct data. It consists of two main parts:
- Encoder f(x): Maps the input x to a hidden representation h = f(x).
- Decoder g(h): Maps the hidden representation h back to a reconstruction r = g(h).

Mathematically, given an input x ∈ ℝ^d:
1. Encoder: h = σ(W_e * x + b_e)  where h ∈ ℝ^k, k < d (for undercomplete AE).
2. Decoder: r = σ(W_d * h + b_d)  where r ∈ ℝ^d.

The objective is to minimize the reconstruction error (Loss function L):
    L(x, r) = ||x - r||^2  (Mean Squared Error for continuous data)
    L(x, r) = - ∑ [x_i log(r_i) + (1 - x_i) log(1 - r_i)] (Binary Cross-Entropy for probabilities)

For a Denoising Autoencoder (DAE):
We intentionally corrupt x to x̃ (e.g., add Gaussian noise).
The model is trained to reconstruct the original x from x̃:
    L(x, g(f(x̃)))

-----------------------------------------------------------------------------
2. BIG-O COMPLEXITY ANALYSIS
-----------------------------------------------------------------------------
Let N be the batch size, d be the input dimension, and k be the bottleneck dimension.

Time Complexity:
- Forward Pass:
  Encoder (Dense): O(N * d * k)
  Decoder (Dense): O(N * k * d)
  Total Forward: O(N * d * k)
- Backward Pass: O(N * d * k)
Overall Training per epoch (M batches): O(M * N * d * k)

Space Complexity:
- Parameters: O(d * k + k * d) = O(d * k)
- Activations (per batch): O(N * (d + k))
Overall Space Complexity: O(d * k + N * (d + k))

-----------------------------------------------------------------------------
3. MODERN TYPE HINTS & EXHAUSTIVE COMMENTS
-----------------------------------------------------------------------------
This module makes extensive use of Python 3 type hints, structured as a textbook
to walk you through building and evaluating these models using PyTorch.
"""

import sys
import time
import math
import random
import logging
from typing import List, Dict, Any, Tuple, Optional, Callable

import numpy as np
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    import matplotlib.pyplot as plt
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    print("Warning: PyTorch or Matplotlib not found. Please install them to run this script fully.")
    print("pip install torch matplotlib numpy")

# Configure logging for textbook-level output
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# =============================================================================
# CLASS 1: UNDERCOMPLETE AUTOENCODER
# =============================================================================
if HAS_TORCH:
    class UndercompleteAutoencoder(nn.Module):
        """
        An Undercomplete Autoencoder compresses the input to a smaller latent space,
        forcing the network to learn the most salient features of the training data.
        
        Architecture:
            Input Layer -> Hidden (Encoder) -> Bottleneck -> Hidden (Decoder) -> Output
        """
        def __init__(self, input_dim: int, hidden_dim: int, latent_dim: int) -> None:
            """
            Initialize the Autoencoder layers.
            
            Args:
                input_dim (int): Dimension of the input data (e.g., 784 for MNIST).
                hidden_dim (int): Dimension of the intermediate hidden layer.
                latent_dim (int): Dimension of the bottleneck/latent space (k < d).
            """
            super(UndercompleteAutoencoder, self).__init__()
            
            # Constraints Check
            if latent_dim >= input_dim:
                logging.warning("Latent dim should be less than input dim for an undercomplete AE.")
            
            # Encoder Architecture
            # We use Linear layers combined with ReLU activations for non-linearity
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(True),
                nn.Linear(hidden_dim, latent_dim),
                nn.ReLU(True)
            )
            
            # Decoder Architecture
            # Maps from latent space back to original input dimension
            # We use Sigmoid at the end to ensure outputs are between 0 and 1 (useful for normalized image data)
            self.decoder = nn.Sequential(
                nn.Linear(latent_dim, hidden_dim),
                nn.ReLU(True),
                nn.Linear(hidden_dim, input_dim),
                nn.Sigmoid()
            )
            
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Forward pass of the Autoencoder.
            
            Args:
                x (torch.Tensor): Input tensor of shape (batch_size, input_dim)
                
            Returns:
                torch.Tensor: Reconstructed tensor of shape (batch_size, input_dim)
            """
            # Compress the input into the latent representation
            latent = self.encoder(x)
            
            # Reconstruct the original input from the latent representation
            reconstructed = self.decoder(latent)
            
            return reconstructed

        def encode(self, x: torch.Tensor) -> torch.Tensor:
            """
            Extract the compressed representation. Used for dimensionality reduction.
            """
            return self.encoder(x)


# =============================================================================
# CLASS 2: DENOISING AUTOENCODER
# =============================================================================
if HAS_TORCH:
    class DenoisingAutoencoder(nn.Module):
        """
        A Denoising Autoencoder (DAE) learns to reconstruct the original input from
        a corrupted (noisy) version. This prevents the network from simply learning
        the identity function and improves feature robustness.
        """
        def __init__(self, input_dim: int, hidden_dim: int) -> None:
            """
            Initialize the DAE layers.
            """
            super(DenoisingAutoencoder, self).__init__()
            
            self.encoder = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(True),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(True)
            )
            
            self.decoder = nn.Sequential(
                nn.Linear(hidden_dim // 2, hidden_dim),
                nn.ReLU(True),
                nn.Linear(hidden_dim, input_dim),
                nn.Sigmoid()
            )
            
        def forward(self, x: torch.Tensor) -> torch.Tensor:
            latent = self.encoder(x)
            return self.decoder(latent)

        @staticmethod
        def add_noise(inputs: torch.Tensor, noise_factor: float = 0.2) -> torch.Tensor:
            """
            Add random Gaussian noise to the input tensors.
            
            Args:
                inputs (torch.Tensor): Original clean data.
                noise_factor (float): Multiplier for the noise intensity.
                
            Returns:
                torch.Tensor: Noisy data clipped to [0, 1].
            """
            noise = torch.randn_like(inputs) * noise_factor
            noisy_inputs = inputs + noise
            # Clip to ensure pixel values remain valid
            return torch.clamp(noisy_inputs, 0., 1.)


# =============================================================================
# HELPER: DATA GENERATION & TRAINING LOOP
# =============================================================================
def generate_synthetic_data(num_samples: int, input_dim: int) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Generates synthetic data for training the autoencoders.
    We simulate a dataset where the intrinsic dimensionality is lower than the input dimension.
    """
    logging.info(f"Generating {num_samples} synthetic samples of dimension {input_dim}")
    
    # Intrinsic latent factors (e.g., 3 underlying features)
    intrinsic_dim = 3
    latent_factors = np.random.rand(num_samples, intrinsic_dim)
    
    # Transformation matrix to project to higher dimensional space
    transform_matrix = np.random.rand(intrinsic_dim, input_dim)
    
    # Generate high dimensional data: X = Factors * Matrix + Noise
    data = np.dot(latent_factors, transform_matrix)
    
    # Normalize data to [0, 1] range for Sigmoid output compatibility
    data_min = data.min()
    data_max = data.max()
    normalized_data = (data - data_min) / (data_max - data_min)
    
    tensor_data = torch.FloatTensor(normalized_data)
    
    # Labels are not strictly needed for basic AE, but we return a dummy tensor for Dataset compatibility
    return tensor_data, torch.zeros(num_samples)


def train_autoencoder(model: nn.Module, 
                      dataloader: 'DataLoader', 
                      epochs: int = 20, 
                      learning_rate: float = 1e-3,
                      is_denoising: bool = False) -> List[float]:
    """
    Standard training loop for an Autoencoder.
    
    Args:
        model: The neural network model.
        dataloader: PyTorch DataLoader containing the training data.
        epochs: Number of times to iterate over the dataset.
        learning_rate: Optimizer learning rate.
        is_denoising: If True, applies noise to the inputs before passing to model.
        
    Returns:
        List[float]: History of loss values per epoch.
    """
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    loss_history = []
    
    logging.info(f"Starting training for {epochs} epochs...")
    for epoch in range(epochs):
        epoch_loss = 0.0
        
        for batch_features, _ in dataloader:
            
            if is_denoising:
                # Add noise to inputs, but target is still the CLEAN inputs
                inputs = DenoisingAutoencoder.add_noise(batch_features)
                targets = batch_features
            else:
                # Standard AE: Input and target are the same
                inputs = batch_features
                targets = batch_features
                
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
            
        avg_loss = epoch_loss / len(dataloader)
        loss_history.append(avg_loss)
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            logging.info(f"Epoch [{epoch + 1}/{epochs}], Loss: {avg_loss:.6f}")
            
    return loss_history


# =============================================================================
# APPLICATION 1: DIMENSIONALITY REDUCTION (ANOMALY DETECTION)
# =============================================================================
def anomaly_detection_demo() -> None:
    """
    Demonstrates using an Autoencoder for Anomaly Detection.
    An AE trained on normal data will reconstruct normal data well (low MSE).
    When presented with anomalous data, the reconstruction error will be significantly higher.
    """
    print("\n" + "="*50)
    print("--- REAL-WORLD APP: ANOMALY DETECTION ---")
    print("="*50)
    
    if not HAS_TORCH:
        print("PyTorch missing. Skipping demo.")
        return

    # 1. Prepare Normal Data
    normal_data, _ = generate_synthetic_data(1000, 20)
    dataset = TensorDataset(normal_data, torch.zeros(1000))
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # 2. Initialize & Train Autoencoder
    model = UndercompleteAutoencoder(input_dim=20, hidden_dim=12, latent_dim=3)
    train_autoencoder(model, dataloader, epochs=20, learning_rate=0.01)
    
    # 3. Evaluation on Normal vs Anomalous Data
    model.eval()
    with torch.no_grad():
        # Evaluate normal sample
        test_normal = normal_data[0:5]
        recon_normal = model(test_normal)
        mse_normal = torch.mean((test_normal - recon_normal)**2, dim=1)
        
        # Create anomalous samples (pure random noise)
        test_anomaly = torch.rand(5, 20)
        recon_anomaly = model(test_anomaly)
        mse_anomaly = torch.mean((test_anomaly - recon_anomaly)**2, dim=1)
        
    print("\n[Results]")
    print(f"Mean Reconstruction Error (Normal Data):   {mse_normal.mean().item():.6f}")
    print(f"Mean Reconstruction Error (Anomalous Data): {mse_anomaly.mean().item():.6f}")
    print("\nConclusion: The Autoencoder fails to reconstruct anomalies, yielding higher loss.")


# =============================================================================
# APPLICATION 2: IMAGE DENOISING
# =============================================================================
def image_denoising_demo() -> None:
    """
    Demonstrates a Denoising Autoencoder using synthetic image-like vectors.
    """
    print("\n" + "="*50)
    print("--- REAL-WORLD APP: SIGNAL DENOISING ---")
    print("="*50)
    
    if not HAS_TORCH:
        return

    # 1. Prepare Data
    data, _ = generate_synthetic_data(1000, 64) # Treat as 8x8 'images' flattened
    dataset = TensorDataset(data, torch.zeros(1000))
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # 2. Train Denoising AE
    dae_model = DenoisingAutoencoder(input_dim=64, hidden_dim=32)
    train_autoencoder(dae_model, dataloader, epochs=20, learning_rate=0.01, is_denoising=True)
    
    # 3. Test Denoising Capabilities
    dae_model.eval()
    with torch.no_grad():
        clean_sample = data[0:1]
        noisy_sample = DenoisingAutoencoder.add_noise(clean_sample, noise_factor=0.3)
        denoised_sample = dae_model(noisy_sample)
        
        mse_noisy = torch.mean((clean_sample - noisy_sample)**2).item()
        mse_denoised = torch.mean((clean_sample - denoised_sample)**2).item()
        
    print("\n[Results]")
    print(f"MSE between Clean and Noisy:    {mse_noisy:.6f}")
    print(f"MSE between Clean and Denoised: {mse_denoised:.6f}")
    print("Conclusion: DAE successfully reconstructed a cleaner signal from noisy input.")


# =============================================================================
# INTERVIEW CHALLENGE: AUTOENCODER BOTTLENECK ANALYSIS
# =============================================================================
def interview_challenge() -> None:
    """
    Common Interview Question:
    "If an Autoencoder has linear activations and a Mean Squared Error loss, 
    what classical machine learning algorithm does it become equivalent to?"
    
    Answer: Principal Component Analysis (PCA).
    
    Let's prove this programmatically by comparing the reconstruction error of PCA 
    vs a Linear Autoencoder.
    """
    print("\n" + "="*50)
    print("--- INTERVIEW CHALLENGE: PCA vs LINEAR AE ---")
    print("="*50)
    
    if not HAS_TORCH:
        return
        
    # Generate structured data
    X, _ = generate_synthetic_data(500, 10)
    X_np = X.numpy()
    
    # 1. PCA Implementation (using SVD)
    # Center the data
    mean_X = np.mean(X_np, axis=0)
    X_centered = X_np - mean_X
    
    # Covariance matrix and Eigen decomposition
    cov = np.cov(X_centered, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Sort descending
    sorted_idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, sorted_idx]
    
    # Take top 2 components
    W_pca = eigenvectors[:, :2]
    
    # Encode and Decode using PCA
    X_pca_encoded = np.dot(X_centered, W_pca)
    X_pca_decoded = np.dot(X_pca_encoded, W_pca.T) + mean_X
    pca_mse = np.mean((X_np - X_pca_decoded)**2)
    
    # 2. Linear Autoencoder
    class LinearAE(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Linear(10, 2, bias=False) # Linear activation, no bias for exact PCA comparison
            self.decoder = nn.Linear(2, 10, bias=False)
            
        def forward(self, x):
            return self.decoder(self.encoder(x))
            
    ae = LinearAE()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(ae.parameters(), lr=0.01)
    
    # Train Linear AE
    X_tensor = torch.FloatTensor(X_centered) # Train on centered data like PCA
    for _ in range(1000):
        optimizer.zero_grad()
        out = ae(X_tensor)
        loss = criterion(out, X_tensor)
        loss.backward()
        optimizer.step()
        
    # AE Reconstruction Error
    with torch.no_grad():
        ae_decoded = ae(X_tensor).numpy() + mean_X
    ae_mse = np.mean((X_np - ae_decoded)**2)
    
    print(f"PCA Reconstruction MSE:       {pca_mse:.6f}")
    print(f"Linear AE Reconstruction MSE: {ae_mse:.6f}")
    print("\nInsight: A Linear Autoencoder minimizes the same objective space as PCA.")
    print("Therefore, their reconstruction errors converge to very similar values.")


# =============================================================================
# UNIT TESTS
# =============================================================================
def run_tests() -> None:
    """
    Test suite to validate the architecture and dimensions of the models.
    """
    print("\n" + "="*50)
    print("--- RUNNING TESTS ---")
    print("="*50)
    
    if not HAS_TORCH:
        print("Skipping tests due to missing PyTorch.")
        return
        
    try:
        # Test Undercomplete AE
        batch_size = 16
        in_dim = 100
        lat_dim = 10
        model = UndercompleteAutoencoder(in_dim, 50, lat_dim)
        dummy_input = torch.rand(batch_size, in_dim)
        
        # Test Output Dimension
        output = model(dummy_input)
        assert output.shape == (batch_size, in_dim), f"Expected shape {(batch_size, in_dim)}, got {output.shape}"
        
        # Test Encoding Dimension
        encoded = model.encode(dummy_input)
        assert encoded.shape == (batch_size, lat_dim), f"Expected shape {(batch_size, lat_dim)}, got {encoded.shape}"
        
        print("✅ Undercomplete Autoencoder Tests Passed!")
        
        # Test Denoising AE Shape
        dae = DenoisingAutoencoder(in_dim, 50)
        dae_out = dae(dummy_input)
        assert dae_out.shape == (batch_size, in_dim), "DAE output shape mismatch."
        print("✅ Denoising Autoencoder Tests Passed!")
        
    except AssertionError as e:
        print(f"❌ Test Failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    print(f"========== EXPLORING AUTOENCODERS ==========\n")
    
    # 1. Anomaly Detection
    anomaly_detection_demo()
    
    # 2. Image/Signal Denoising
    image_denoising_demo()
    
    # 3. Interview Challenge
    interview_challenge()
    
    # 4. Run Architecture Tests
    run_tests()
    
    print(f"\n========== END OF AUTOENCODERS ==========\n")
