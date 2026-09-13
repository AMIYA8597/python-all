"""
Convolutional Neural Networks Example (PyTorch)
Demonstrates a simple CNN architecture for image classification.
"""

import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        
        # Block 1: Conv -> ReLU -> Pool
        # Input shape: (Batch, Channels=3, H=32, W=32)
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1, stride=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        # Output after Block 1: (Batch, 16, 16, 16)
        
        # Block 2: Conv -> ReLU -> Pool
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1, stride=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        # Output after Block 2: (Batch, 32, 8, 8)
        
        # Fully Connected Classifier
        # Flattened size = 32 channels * 8 height * 8 width
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(32 * 8 * 8, 128)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, num_classes)
        
    def forward(self, x):
        # Feature extraction
        x = self.pool1(self.relu1(self.conv1(x)))
        x = self.pool2(self.relu2(self.conv2(x)))
        
        # Classification
        x = self.flatten(x)
        x = self.relu3(self.fc1(x))
        logits = self.fc2(x)
        
        return logits

if __name__ == "__main__":
    # Create the model
    model = SimpleCNN(num_classes=10)
    print(model)
    
    # Dummy image tensor: Batch of 4 images, 3 channels (RGB), 32x32 pixels
    # PyTorch format is NCHW (Batch, Channel, Height, Width)
    dummy_images = torch.randn(4, 3, 32, 32)
    print(f"\nInput shape: {dummy_images.shape}")
    
    # Forward pass
    output = model(dummy_images)
    print(f"Output shape (logits): {output.shape}")
