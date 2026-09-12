"""
Computer Vision Basics with PyTorch
-----------------------------------
This script introduces fundamental Computer Vision concepts using PyTorch.
Topics covered:
1. Convolutional Neural Networks (CNN) Architecture
2. Image Transformations and Datasets
3. Object Detection Basics: Intersection over Union (IoU)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

# ==========================================
# 1. Convolutional Neural Network (CNN)
# ==========================================
class SimpleCNN(nn.Module):
    """
    A simple CNN architecture for image classification.
    Expects input shape: (Batch_Size, Channels, Height, Width)
    Example: 1x28x28 for MNIST grayscale images.
    """
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        # Convolutional Layer 1: 1 input channel, 16 output channels, 3x3 kernel
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU()
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Convolutional Layer 2: 16 input channels, 32 output channels, 3x3 kernel
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Fully Connected Layer
        # After two 2x2 poolings, a 28x28 image becomes 7x7.
        # 32 channels * 7 * 7 = 1568 flattened features
        self.fc1 = nn.Linear(32 * 7 * 7, 128)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(128, num_classes)
        
    def forward(self, x):
        # Feature Extraction
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.pool1(x)
        
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.pool2(x)
        
        # Flatten the tensor
        x = x.view(x.size(0), -1)
        
        # Classification
        x = self.fc1(x)
        x = self.relu3(x)
        x = self.fc2(x)
        return x

def test_cnn():
    print("=== 1. Testing CNN Architecture ===")
    model = SimpleCNN(num_classes=10)
    print(model)
    
    # Create a dummy batch of 4 grayscale images of size 28x28
    dummy_input = torch.randn(4, 1, 28, 28)
    
    # Forward pass
    output = model(dummy_input)
    print(f"\nInput shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape} (Batch Size, Num Classes)")
    print()

# ==========================================
# 2. Object Detection Basics: Intersection over Union (IoU)
# ==========================================
def calculate_iou(box1, box2):
    """
    Calculates Intersection over Union (IoU) between two bounding boxes.
    Boxes are in format [x1, y1, x2, y2] (top-left and bottom-right coordinates).
    """
    # Intersection coordinates
    x1_inter = max(box1[0], box2[0])
    y1_inter = max(box1[1], box2[1])
    x2_inter = min(box1[2], box2[2])
    y2_inter = min(box1[3], box2[3])
    
    # Intersection area
    inter_width = max(0, x2_inter - x1_inter)
    inter_height = max(0, y2_inter - y1_inter)
    inter_area = inter_width * inter_height
    
    # Areas of individual boxes
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    # Union area
    union_area = box1_area + box2_area - inter_area
    
    # IoU
    iou = inter_area / union_area if union_area > 0 else 0
    return iou

def test_iou():
    print("=== 2. Intersection over Union (IoU) ===")
    # Format: [x1, y1, x2, y2]
    boxA = [10, 10, 50, 50]
    boxB = [20, 20, 60, 60]  # Overlapping box
    boxC = [100, 100, 150, 150] # Non-overlapping box
    
    iou_AB = calculate_iou(boxA, boxB)
    iou_AC = calculate_iou(boxA, boxC)
    
    print(f"Box A: {boxA}")
    print(f"Box B: {boxB}")
    print(f"Box C: {boxC}")
    print(f"IoU(A, B): {iou_AB:.4f}")
    print(f"IoU(A, C): {iou_AC:.4f}")

if __name__ == "__main__":
    test_cnn()
    test_iou()
