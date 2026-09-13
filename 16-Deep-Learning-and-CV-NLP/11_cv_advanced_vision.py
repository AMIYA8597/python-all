"""
Advanced Vision Example: Transfer Learning
Loading a pre-trained ResNet18 and modifying it for a binary classification task.
"""

import torch
import torch.nn as nn
import torchvision.models as models

def create_transfer_learning_model(num_classes=2, freeze_features=True):
    """
    Creates a ResNet18 model for transfer learning.
    
    Args:
        num_classes: The number of classes for the new task.
        freeze_features: If True, freezes the convolutional base.
    """
    
    # 1. Load the pre-trained ResNet18 model
    # Weights are downloaded from PyTorch's model zoo
    # (Using weights parameter instead of pretrained=True for modern PyTorch)
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    
    # 2. Freeze the parameters in the feature extraction layers
    if freeze_features:
        for param in model.parameters():
            param.requires_grad = False
            
    # 3. Replace the final classification head
    # The original ResNet18 was trained on ImageNet (1000 classes).
    # We replace the final Fully Connected (fc) layer.
    
    # Get the number of input features to the final layer
    num_ftrs = model.fc.in_features
    
    # Replace it with a new layer (requires_grad is True by default for new layers)
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    return model

if __name__ == "__main__":
    # Suppose we are building a Hotdog vs. Not-Hotdog classifier (2 classes)
    model = create_transfer_learning_model(num_classes=2, freeze_features=True)
    
    print("--- Model's Final Layer ---")
    print(model.fc)
    
    print("\n--- Checking Trainable Parameters ---")
    # Let's verify which parameters will be updated during training
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    
    print(f"Total Parameters: {total_params:,}")
    print(f"Trainable Parameters: {trainable_params:,}")
    print("Notice how very few parameters are trainable compared to the total! This makes training fast.")
    
    # Dummy forward pass
    dummy_input = torch.randn(1, 3, 224, 224) # Standard ResNet input size
    output = model(dummy_input)
    print(f"\nOutput shape (Batch, num_classes): {output.shape}")
