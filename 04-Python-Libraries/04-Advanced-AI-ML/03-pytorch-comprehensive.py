#!/usr/bin/env python3
"""
PyTorch Comprehensive Guide for Deep Learning
==============================================

This module provides comprehensive coverage of PyTorch, a popular deep learning
framework known for its dynamic computation graphs and research-friendly design.
It covers neural networks, computer vision, natural language processing, and
advanced PyTorch features.

Topics Covered:
1. PyTorch Fundamentals & Tensor Operations
2. Neural Networks with torch.nn
3. Automatic Differentiation (Autograd)
4. Data Loading & Preprocessing
5. Training Loops & Optimization
6. Computer Vision with torchvision
7. Natural Language Processing with torchtext
8. Custom Datasets & Transforms
9. Model Saving, Loading & Deployment
10. Advanced Features (Distributed Training, Mixed Precision)

Key Components:
- torch: Core tensor operations
- torch.nn: Neural network modules
- torch.optim: Optimization algorithms
- torch.utils.data: Data loading utilities
- torchvision: Computer vision tools
- torchtext: Natural language processing
- torch.cuda: GPU acceleration

Author: Python DSA Master
Date: 2024
"""

import numpy as np
from typing import List, Dict, Tuple, Any, Optional, Union, Callable
import warnings
warnings.filterwarnings('ignore')

# Note: This module demonstrates PyTorch usage patterns and concepts.
# To run the actual code, install: pip install torch torchvision torchaudio

def demonstrate_pytorch_basics():
    """
    Demonstrate core PyTorch concepts without requiring installation.
    This shows the patterns and workflow used in PyTorch.
    """
    print("PyTorch Concepts and Patterns")
    print("=" * 50)
    
    # Typical PyTorch workflow
    workflow_steps = [
        "1. Data Loading & Preprocessing",
        "2. Model Definition (torch.nn.Module)", 
        "3. Loss Function & Optimizer Setup",
        "4. Training Loop Implementation",
        "5. Validation & Testing",
        "6. Model Saving & Loading",
        "7. Inference & Deployment"
    ]
    
    for step in workflow_steps:
        print(f"   {step}")
    
    print("\nCommon PyTorch Import Patterns:")
    imports = [
        "import torch",
        "import torch.nn as nn",
        "import torch.optim as optim",
        "import torch.nn.functional as F",
        "from torch.utils.data import DataLoader, Dataset, random_split",
        "import torchvision",
        "import torchvision.transforms as transforms",
        "from torchvision import datasets, models",
        "import torch.cuda.amp as amp  # Mixed precision training"
    ]
    
    for imp in imports:
        print(f"   {imp}")

class PyTorchTensorOperations:
    """Core PyTorch tensor operations and manipulations."""
    
    @staticmethod
    def tensor_basics():
        """Show basic tensor operations."""
        print("\n" + "="*50)
        print("PYTORCH TENSOR OPERATIONS")
        print("="*50)
        
        print("\n1. TENSOR CREATION")
        tensor_creation = [
            "import torch",
            "import numpy as np",
            "",
            "# Create tensors",
            "scalar = torch.tensor(5.0)",
            "vector = torch.tensor([1, 2, 3, 4])",
            "matrix = torch.tensor([[1, 2], [3, 4]])",
            "tensor_3d = torch.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])",
            "",
            "# Special tensors",
            "zeros = torch.zeros(3, 4)",
            "ones = torch.ones(2, 3)",
            "random_tensor = torch.randn(2, 3)  # Normal distribution",
            "uniform_tensor = torch.rand(2, 3)  # Uniform [0, 1)",
            "",
            "# From numpy",
            "np_array = np.array([1, 2, 3, 4])",
            "torch_tensor = torch.from_numpy(np_array)",
            "",
            "# Device specification",
            "cpu_tensor = torch.tensor([1, 2, 3], device='cpu')",
            "# gpu_tensor = torch.tensor([1, 2, 3], device='cuda')  # If CUDA available"
        ]
        
        for line in tensor_creation:
            print(f"   {line}")
        
        print("\n2. TENSOR OPERATIONS")
        tensor_ops = [
            "# Basic arithmetic",
            "a = torch.tensor([1, 2, 3])",
            "b = torch.tensor([4, 5, 6])",
            "addition = torch.add(a, b)  # or a + b",
            "multiplication = torch.mul(a, b)  # or a * b",
            "matrix_mult = torch.matmul(matrix1, matrix2)  # or matrix1 @ matrix2",
            "",
            "# Reshaping",
            "tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])",
            "reshaped = tensor.view(3, 2)  # or tensor.reshape(3, 2)",
            "transposed = tensor.t()  # or tensor.transpose(0, 1)",
            "",
            "# Reductions",
            "sum_all = torch.sum(tensor)",
            "sum_axis_0 = torch.sum(tensor, dim=0)",
            "mean_val = torch.mean(tensor.float())",
            "max_val, max_idx = torch.max(tensor, dim=1)",
            "",
            "# Indexing and slicing",
            "slice_tensor = tensor[0:2, 1:3]",
            "mask = tensor > 3",
            "masked_tensor = tensor[mask]"
        ]
        
        for line in tensor_ops:
            print(f"   {line}")
            
        print("\n3. AUTOGRAD & GRADIENTS")
        autograd = [
            "# Gradient computation",
            "x = torch.tensor(2.0, requires_grad=True)",
            "y = x ** 2",
            "y.backward()  # Compute gradients",
            "print(f'Gradient of x^2 at x=2: {x.grad}')",
            "",
            "# Multiple variables",
            "x = torch.tensor(2.0, requires_grad=True)",
            "y = torch.tensor(3.0, requires_grad=True)",
            "z = x**2 + y**2",
            "z.backward()",
            "print(f'dz/dx: {x.grad}, dz/dy: {y.grad}')",
            "",
            "# Gradient control",
            "with torch.no_grad():  # Disable gradient computation",
            "    result = model(input_data)  # No gradients computed",
            "",
            "# Detach from computation graph",
            "detached_tensor = tensor.detach()  # No gradients"
        ]
        
        for line in autograd:
            print(f"   {line}")

class PyTorchNeuralNetworks:
    """Comprehensive neural network building with torch.nn."""
    
    @staticmethod
    def basic_networks():
        """Show basic neural network patterns."""
        print("\n" + "="*50)
        print("PYTORCH NEURAL NETWORKS")
        print("="*50)
        
        print("\n1. BASIC NEURAL NETWORK")
        basic_nn = [
            "import torch.nn as nn",
            "import torch.nn.functional as F",
            "",
            "# Method 1: Using nn.Sequential",
            "model = nn.Sequential(",
            "    nn.Linear(784, 128),",
            "    nn.ReLU(),",
            "    nn.Dropout(0.2),",
            "    nn.Linear(128, 64),",
            "    nn.ReLU(),",
            "    nn.Linear(64, 10)",
            ")",
            "",
            "# Method 2: Custom nn.Module",
            "class NeuralNetwork(nn.Module):",
            "    def __init__(self, input_size, hidden_size, num_classes):",
            "        super(NeuralNetwork, self).__init__()",
            "        self.fc1 = nn.Linear(input_size, hidden_size)",
            "        self.relu = nn.ReLU()",
            "        self.dropout = nn.Dropout(0.2)",
            "        self.fc2 = nn.Linear(hidden_size, num_classes)",
            "    ",
            "    def forward(self, x):",
            "        x = self.fc1(x)",
            "        x = self.relu(x)",
            "        x = self.dropout(x)",
            "        x = self.fc2(x)",
            "        return x",
            "",
            "# Usage",
            "model = NeuralNetwork(784, 128, 10)",
            "print(model)"
        ]
        
        for line in basic_nn:
            print(f"   {line}")
            
        print("\n2. CONVOLUTIONAL NEURAL NETWORK")
        cnn_example = [
            "class CNN(nn.Module):",
            "    def __init__(self, num_classes=10):",
            "        super(CNN, self).__init__()",
            "        # Convolutional layers",
            "        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)",
            "        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)",
            "        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)",
            "        ",
            "        # Pooling",
            "        self.pool = nn.MaxPool2d(2, 2)",
            "        ",
            "        # Fully connected layers",
            "        self.fc1 = nn.Linear(64 * 3 * 3, 128)",
            "        self.fc2 = nn.Linear(128, num_classes)",
            "        ",
            "        # Dropout",
            "        self.dropout = nn.Dropout(0.2)",
            "    ",
            "    def forward(self, x):",
            "        # Conv block 1",
            "        x = self.pool(F.relu(self.conv1(x)))",
            "        ",
            "        # Conv block 2",
            "        x = self.pool(F.relu(self.conv2(x)))",
            "        ",
            "        # Conv block 3",
            "        x = F.relu(self.conv3(x))",
            "        ",
            "        # Flatten for fully connected layers",
            "        x = x.view(-1, 64 * 3 * 3)",
            "        ",
            "        # Fully connected layers",
            "        x = F.relu(self.fc1(x))",
            "        x = self.dropout(x)",
            "        x = self.fc2(x)",
            "        ",
            "        return x"
        ]
        
        for line in cnn_example:
            print(f"   {line}")
            
        print("\n3. RECURRENT NEURAL NETWORK")
        rnn_example = [
            "class RNN(nn.Module):",
            "    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):",
            "        super(RNN, self).__init__()",
            "        self.embedding = nn.Embedding(vocab_size, embed_dim)",
            "        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)",
            "        self.fc = nn.Linear(hidden_dim, num_classes)",
            "        self.dropout = nn.Dropout(0.2)",
            "    ",
            "    def forward(self, x):",
            "        # Embedding",
            "        embedded = self.embedding(x)",
            "        ",
            "        # LSTM",
            "        lstm_out, (hidden, cell) = self.lstm(embedded)",
            "        ",
            "        # Use last hidden state",
            "        output = self.dropout(hidden[-1])",
            "        output = self.fc(output)",
            "        ",
            "        return output",
            "",
            "# Bidirectional LSTM",
            "class BiLSTM(nn.Module):",
            "    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):",
            "        super(BiLSTM, self).__init__()",
            "        self.embedding = nn.Embedding(vocab_size, embed_dim)",
            "        self.bilstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)",
            "        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 for bidirectional",
            "    ",
            "    def forward(self, x):",
            "        embedded = self.embedding(x)",
            "        lstm_out, (hidden, cell) = self.bilstm(embedded)",
            "        # Concatenate forward and backward hidden states",
            "        output = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)",
            "        output = self.fc(output)",
            "        return output"
        ]
        
        for line in rnn_example:
            print(f"   {line}")
    
    @staticmethod
    def advanced_architectures():
        """Show advanced neural network architectures."""
        print("\n" + "="*50)
        print("ADVANCED PYTORCH ARCHITECTURES")
        print("="*50)
        
        print("\n1. RESIDUAL NETWORK (RESNET)")
        resnet_block = [
            "class ResidualBlock(nn.Module):",
            "    def __init__(self, in_channels, out_channels, stride=1):",
            "        super(ResidualBlock, self).__init__()",
            "        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride, 1, bias=False)",
            "        self.bn1 = nn.BatchNorm2d(out_channels)",
            "        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False)",
            "        self.bn2 = nn.BatchNorm2d(out_channels)",
            "        ",
            "        # Shortcut connection",
            "        self.shortcut = nn.Sequential()",
            "        if stride != 1 or in_channels != out_channels:",
            "            self.shortcut = nn.Sequential(",
            "                nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),",
            "                nn.BatchNorm2d(out_channels)",
            "            )",
            "    ",
            "    def forward(self, x):",
            "        residual = x",
            "        ",
            "        out = F.relu(self.bn1(self.conv1(x)))",
            "        out = self.bn2(self.conv2(out))",
            "        ",
            "        out += self.shortcut(residual)  # Skip connection",
            "        out = F.relu(out)",
            "        ",
            "        return out"
        ]
        
        for line in resnet_block:
            print(f"   {line}")
            
        print("\n2. ATTENTION MECHANISM")
        attention = [
            "class Attention(nn.Module):",
            "    def __init__(self, hidden_dim):",
            "        super(Attention, self).__init__()",
            "        self.hidden_dim = hidden_dim",
            "        self.attn = nn.Linear(hidden_dim * 2, hidden_dim)",
            "        self.v = nn.Linear(hidden_dim, 1, bias=False)",
            "    ",
            "    def forward(self, hidden, encoder_outputs):",
            "        # hidden: [batch_size, hidden_dim]",
            "        # encoder_outputs: [batch_size, seq_len, hidden_dim]",
            "        ",
            "        batch_size = encoder_outputs.size(0)",
            "        seq_len = encoder_outputs.size(1)",
            "        ",
            "        # Repeat hidden state",
            "        hidden = hidden.unsqueeze(1).repeat(1, seq_len, 1)",
            "        ",
            "        # Calculate attention scores",
            "        energy = torch.tanh(self.attn(torch.cat((hidden, encoder_outputs), dim=2)))",
            "        attention = self.v(energy).squeeze(2)",
            "        ",
            "        # Apply softmax",
            "        attention_weights = F.softmax(attention, dim=1)",
            "        ",
            "        # Apply attention weights",
            "        context = torch.bmm(attention_weights.unsqueeze(1), encoder_outputs)",
            "        ",
            "        return context.squeeze(1), attention_weights"
        ]
        
        for line in attention:
            print(f"   {line}")
            
        print("\n3. TRANSFORMER BLOCK")
        transformer = [
            "class MultiHeadAttention(nn.Module):",
            "    def __init__(self, d_model, n_heads):",
            "        super(MultiHeadAttention, self).__init__()",
            "        self.d_model = d_model",
            "        self.n_heads = n_heads",
            "        self.d_k = d_model // n_heads",
            "        ",
            "        self.w_q = nn.Linear(d_model, d_model)",
            "        self.w_k = nn.Linear(d_model, d_model)",
            "        self.w_v = nn.Linear(d_model, d_model)",
            "        self.w_o = nn.Linear(d_model, d_model)",
            "    ",
            "    def forward(self, query, key, value, mask=None):",
            "        batch_size = query.size(0)",
            "        ",
            "        # Linear transformations",
            "        Q = self.w_q(query).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)",
            "        K = self.w_k(key).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)",
            "        V = self.w_v(value).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)",
            "        ",
            "        # Scaled dot-product attention",
            "        attention = self.scaled_dot_product_attention(Q, K, V, mask)",
            "        ",
            "        # Concatenate heads",
            "        attention = attention.transpose(1, 2).contiguous().view(",
            "            batch_size, -1, self.d_model)",
            "        ",
            "        return self.w_o(attention)"
        ]
        
        for line in transformer:
            print(f"   {line}")

class PyTorchTrainingLoop:
    """Comprehensive training loop patterns and optimization."""
    
    @staticmethod
    def basic_training():
        """Show basic training loop patterns."""
        print("\n" + "="*50)
        print("PYTORCH TRAINING LOOPS")
        print("="*50)
        
        print("\n1. BASIC TRAINING LOOP")
        basic_training = [
            "import torch.optim as optim",
            "",
            "# Setup",
            "model = NeuralNetwork()",
            "criterion = nn.CrossEntropyLoss()",
            "optimizer = optim.Adam(model.parameters(), lr=0.001)",
            "",
            "# Training loop",
            "def train_model(model, train_loader, criterion, optimizer, epochs):",
            "    model.train()  # Set model to training mode",
            "    ",
            "    for epoch in range(epochs):",
            "        running_loss = 0.0",
            "        correct = 0",
            "        total = 0",
            "        ",
            "        for batch_idx, (data, targets) in enumerate(train_loader):",
            "            # Zero gradients",
            "            optimizer.zero_grad()",
            "            ",
            "            # Forward pass",
            "            outputs = model(data)",
            "            loss = criterion(outputs, targets)",
            "            ",
            "            # Backward pass",
            "            loss.backward()",
            "            optimizer.step()",
            "            ",
            "            # Statistics",
            "            running_loss += loss.item()",
            "            _, predicted = outputs.max(1)",
            "            total += targets.size(0)",
            "            correct += predicted.eq(targets).sum().item()",
            "            ",
            "            if batch_idx % 100 == 0:",
            "                print(f'Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}')",
            "        ",
            "        # Epoch statistics",
            "        epoch_loss = running_loss / len(train_loader)",
            "        epoch_acc = 100. * correct / total",
            "        print(f'Epoch {epoch}: Loss {epoch_loss:.4f}, Accuracy {epoch_acc:.2f}%')"
        ]
        
        for line in basic_training:
            print(f"   {line}")
            
        print("\n2. VALIDATION LOOP")
        validation = [
            "def validate_model(model, val_loader, criterion):",
            "    model.eval()  # Set model to evaluation mode",
            "    val_loss = 0.0",
            "    correct = 0",
            "    total = 0",
            "    ",
            "    with torch.no_grad():  # Disable gradient computation",
            "        for data, targets in val_loader:",
            "            outputs = model(data)",
            "            loss = criterion(outputs, targets)",
            "            ",
            "            val_loss += loss.item()",
            "            _, predicted = outputs.max(1)",
            "            total += targets.size(0)",
            "            correct += predicted.eq(targets).sum().item()",
            "    ",
            "    val_loss /= len(val_loader)",
            "    val_acc = 100. * correct / total",
            "    ",
            "    print(f'Validation Loss: {val_loss:.4f}, Accuracy: {val_acc:.2f}%')",
            "    return val_loss, val_acc"
        ]
        
        for line in validation:
            print(f"   {line}")
            
        print("\n3. COMPLETE TRAINING WITH VALIDATION")
        complete_training = [
            "def train_with_validation(model, train_loader, val_loader, epochs=10):",
            "    criterion = nn.CrossEntropyLoss()",
            "    optimizer = optim.Adam(model.parameters(), lr=0.001)",
            "    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)",
            "    ",
            "    best_val_acc = 0.0",
            "    train_losses, val_losses = [], []",
            "    ",
            "    for epoch in range(epochs):",
            "        # Training",
            "        model.train()",
            "        train_loss = 0.0",
            "        ",
            "        for data, targets in train_loader:",
            "            optimizer.zero_grad()",
            "            outputs = model(data)",
            "            loss = criterion(outputs, targets)",
            "            loss.backward()",
            "            optimizer.step()",
            "            train_loss += loss.item()",
            "        ",
            "        # Validation",
            "        val_loss, val_acc = validate_model(model, val_loader, criterion)",
            "        ",
            "        # Learning rate scheduling",
            "        scheduler.step()",
            "        ",
            "        # Save best model",
            "        if val_acc > best_val_acc:",
            "            best_val_acc = val_acc",
            "            torch.save(model.state_dict(), 'best_model.pth')",
            "        ",
            "        # Record losses",
            "        train_losses.append(train_loss / len(train_loader))",
            "        val_losses.append(val_loss)",
            "    ",
            "    return train_losses, val_losses"
        ]
        
        for line in complete_training:
            print(f"   {line}")
    
    @staticmethod
    def advanced_training():
        """Show advanced training techniques."""
        print("\n" + "="*50)
        print("ADVANCED TRAINING TECHNIQUES")
        print("="*50)
        
        print("\n1. MIXED PRECISION TRAINING")
        mixed_precision = [
            "from torch.cuda.amp import autocast, GradScaler",
            "",
            "def train_with_amp(model, train_loader, epochs):",
            "    criterion = nn.CrossEntropyLoss()",
            "    optimizer = optim.Adam(model.parameters())",
            "    scaler = GradScaler()",
            "    ",
            "    for epoch in range(epochs):",
            "        for data, targets in train_loader:",
            "            optimizer.zero_grad()",
            "            ",
            "            # Forward pass with autocast",
            "            with autocast():",
            "                outputs = model(data)",
            "                loss = criterion(outputs, targets)",
            "            ",
            "            # Scaled backward pass",
            "            scaler.scale(loss).backward()",
            "            scaler.step(optimizer)",
            "            scaler.update()"
        ]
        
        for line in mixed_precision:
            print(f"   {line}")
            
        print("\n2. GRADIENT CLIPPING")
        grad_clipping = [
            "def train_with_grad_clipping(model, train_loader, max_norm=1.0):",
            "    criterion = nn.CrossEntropyLoss()",
            "    optimizer = optim.Adam(model.parameters())",
            "    ",
            "    for data, targets in train_loader:",
            "        optimizer.zero_grad()",
            "        outputs = model(data)",
            "        loss = criterion(outputs, targets)",
            "        loss.backward()",
            "        ",
            "        # Clip gradients",
            "        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)",
            "        ",
            "        optimizer.step()"
        ]
        
        for line in grad_clipping:
            print(f"   {line}")
            
        print("\n3. CUSTOM LOSS FUNCTIONS")
        custom_loss = [
            "class FocalLoss(nn.Module):",
            "    def __init__(self, alpha=1, gamma=2):",
            "        super(FocalLoss, self).__init__()",
            "        self.alpha = alpha",
            "        self.gamma = gamma",
            "    ",
            "    def forward(self, inputs, targets):",
            "        ce_loss = F.cross_entropy(inputs, targets, reduction='none')",
            "        pt = torch.exp(-ce_loss)",
            "        focal_loss = self.alpha * (1-pt)**self.gamma * ce_loss",
            "        return focal_loss.mean()",
            "",
            "# Contrastive Loss",
            "class ContrastiveLoss(nn.Module):",
            "    def __init__(self, margin=1.0):",
            "        super(ContrastiveLoss, self).__init__()",
            "        self.margin = margin",
            "    ",
            "    def forward(self, output1, output2, label):",
            "        euclidean_distance = F.pairwise_distance(output1, output2)",
            "        loss = torch.mean((1-label) * torch.pow(euclidean_distance, 2) +",
            "                         (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))",
            "        return loss"
        ]
        
        for line in custom_loss:
            print(f"   {line}")

class PyTorchDataHandling:
    """PyTorch data loading, preprocessing, and custom datasets."""
    
    @staticmethod
    def data_loading():
        """Show data loading patterns."""
        print("\n" + "="*50)
        print("PYTORCH DATA LOADING")
        print("="*50)
        
        print("\n1. BASIC DATA LOADING")
        basic_data = [
            "from torch.utils.data import DataLoader, Dataset, random_split",
            "import torchvision.transforms as transforms",
            "",
            "# Built-in datasets",
            "transform = transforms.Compose([",
            "    transforms.ToTensor(),",
            "    transforms.Normalize((0.5,), (0.5,))",
            "])",
            "",
            "train_dataset = torchvision.datasets.MNIST(",
            "    root='./data', train=True, download=True, transform=transform)",
            "",
            "test_dataset = torchvision.datasets.MNIST(",
            "    root='./data', train=False, download=True, transform=transform)",
            "",
            "# Data loaders",
            "train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)",
            "test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)",
            "",
            "# Iterate through data",
            "for batch_idx, (data, targets) in enumerate(train_loader):",
            "    print(f'Batch {batch_idx}: {data.shape}, {targets.shape}')",
            "    if batch_idx == 2:  # Just show first few batches",
            "        break"
        ]
        
        for line in basic_data:
            print(f"   {line}")
            
        print("\n2. CUSTOM DATASET")
        custom_dataset = [
            "class CustomDataset(Dataset):",
            "    def __init__(self, data, targets, transform=None):",
            "        self.data = data",
            "        self.targets = targets",
            "        self.transform = transform",
            "    ",
            "    def __len__(self):",
            "        return len(self.data)",
            "    ",
            "    def __getitem__(self, idx):",
            "        sample = self.data[idx]",
            "        target = self.targets[idx]",
            "        ",
            "        if self.transform:",
            "            sample = self.transform(sample)",
            "        ",
            "        return sample, target",
            "",
            "# Usage",
            "import numpy as np",
            "data = np.random.randn(1000, 28, 28)",
            "targets = np.random.randint(0, 10, 1000)",
            "",
            "custom_dataset = CustomDataset(data, targets)",
            "custom_loader = DataLoader(custom_dataset, batch_size=32, shuffle=True)"
        ]
        
        for line in custom_dataset:
            print(f"   {line}")
            
        print("\n3. IMAGE DATASET FROM FOLDER")
        image_dataset = [
            "from torchvision import datasets",
            "from PIL import Image",
            "import os",
            "",
            "class ImageFolderDataset(Dataset):",
            "    def __init__(self, root_dir, transform=None):",
            "        self.root_dir = root_dir",
            "        self.transform = transform",
            "        self.images = []",
            "        self.labels = []",
            "        ",
            "        # Load image paths and labels",
            "        for class_idx, class_name in enumerate(os.listdir(root_dir)):",
            "            class_dir = os.path.join(root_dir, class_name)",
            "            if os.path.isdir(class_dir):",
            "                for img_name in os.listdir(class_dir):",
            "                    img_path = os.path.join(class_dir, img_name)",
            "                    self.images.append(img_path)",
            "                    self.labels.append(class_idx)",
            "    ",
            "    def __len__(self):",
            "        return len(self.images)",
            "    ",
            "    def __getitem__(self, idx):",
            "        img_path = self.images[idx]",
            "        image = Image.open(img_path).convert('RGB')",
            "        label = self.labels[idx]",
            "        ",
            "        if self.transform:",
            "            image = self.transform(image)",
            "        ",
            "        return image, label",
            "",
            "# Or use torchvision's ImageFolder",
            "dataset = datasets.ImageFolder(root='path/to/data', transform=transform)"
        ]
        
        for line in image_dataset:
            print(f"   {line}")
    
    @staticmethod
    def data_transforms():
        """Show data transformation patterns."""
        print("\n" + "="*50)
        print("DATA TRANSFORMS")
        print("="*50)
        
        transforms_examples = [
            "import torchvision.transforms as transforms",
            "",
            "# Basic transforms",
            "basic_transform = transforms.Compose([",
            "    transforms.Resize((224, 224)),",
            "    transforms.ToTensor(),",
            "    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])",
            "])",
            "",
            "# Data augmentation",
            "augmentation_transform = transforms.Compose([",
            "    transforms.RandomResizedCrop(224),",
            "    transforms.RandomHorizontalFlip(p=0.5),",
            "    transforms.RandomRotation(degrees=10),",
            "    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),",
            "    transforms.ToTensor(),",
            "    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])",
            "])",
            "",
            "# Custom transform",
            "class CustomTransform:",
            "    def __init__(self, probability=0.5):",
            "        self.probability = probability",
            "    ",
            "    def __call__(self, image):",
            "        if torch.rand(1) < self.probability:",
            "            # Apply custom transformation",
            "            pass",
            "        return image",
            "",
            "# Different transforms for train/validation",
            "train_transform = transforms.Compose([",
            "    transforms.RandomHorizontalFlip(),",
            "    transforms.ToTensor(),",
            "    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))",
            "])",
            "",
            "val_transform = transforms.Compose([",
            "    transforms.ToTensor(),",
            "    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))",
            "])"
        ]
        
        for line in transforms_examples:
            print(f"   {line}")

class PyTorchComputerVision:
    """Computer vision specific techniques with torchvision."""
    
    @staticmethod
    def pretrained_models():
        """Show pre-trained model usage."""
        print("\n" + "="*50)
        print("PRETRAINED MODELS & TRANSFER LEARNING")
        print("="*50)
        
        pretrained_examples = [
            "from torchvision import models",
            "",
            "# Load pre-trained models",
            "resnet18 = models.resnet18(pretrained=True)",
            "resnet50 = models.resnet50(pretrained=True)",
            "vgg16 = models.vgg16(pretrained=True)",
            "densenet121 = models.densenet121(pretrained=True)",
            "",
            "# Feature extraction (freeze all layers)",
            "for param in resnet18.parameters():",
            "    param.requires_grad = False",
            "",
            "# Replace final layer for new task",
            "num_classes = 10",
            "resnet18.fc = nn.Linear(resnet18.fc.in_features, num_classes)",
            "",
            "# Fine-tuning (unfreeze some layers)",
            "def set_parameter_requires_grad(model, feature_extracting):",
            "    if feature_extracting:",
            "        for param in model.parameters():",
            "            param.requires_grad = False",
            "",
            "# Fine-tune only the last few layers",
            "set_parameter_requires_grad(resnet18, True)",
            "for param in resnet18.fc.parameters():",
            "    param.requires_grad = True",
            "",
            "# Custom classifier head",
            "class CustomClassifier(nn.Module):",
            "    def __init__(self, backbone, num_classes):",
            "        super(CustomClassifier, self).__init__()",
            "        self.backbone = backbone",
            "        self.backbone.fc = nn.Identity()  # Remove original classifier",
            "        ",
            "        # Custom head",
            "        self.classifier = nn.Sequential(",
            "            nn.Linear(2048, 512),  # ResNet50 features",
            "            nn.ReLU(),",
            "            nn.Dropout(0.5),",
            "            nn.Linear(512, num_classes)",
            "        )",
            "    ",
            "    def forward(self, x):",
            "        features = self.backbone(x)",
            "        return self.classifier(features)",
            "",
            "model = CustomClassifier(models.resnet50(pretrained=True), num_classes=10)"
        ]
        
        for line in pretrained_examples:
            print(f"   {line}")
    
    @staticmethod
    def object_detection():
        """Show object detection patterns."""
        print("\n" + "="*50)
        print("OBJECT DETECTION")
        print("="*50)
        
        detection_examples = [
            "# Using torchvision object detection models",
            "import torchvision.transforms as T",
            "",
            "# Load pre-trained detection model",
            "model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)",
            "model.eval()",
            "",
            "# Inference function",
            "def detect_objects(image, model, threshold=0.5):",
            "    transform = T.Compose([T.ToTensor()])",
            "    image_tensor = transform(image).unsqueeze(0)",
            "    ",
            "    with torch.no_grad():",
            "        predictions = model(image_tensor)",
            "    ",
            "    # Filter predictions by confidence",
            "    boxes = predictions[0]['boxes'][predictions[0]['scores'] > threshold]",
            "    labels = predictions[0]['labels'][predictions[0]['scores'] > threshold]",
            "    scores = predictions[0]['scores'][predictions[0]['scores'] > threshold]",
            "    ",
            "    return boxes, labels, scores",
            "",
            "# Custom object detection model",
            "class SimpleYOLO(nn.Module):",
            "    def __init__(self, num_classes):",
            "        super(SimpleYOLO, self).__init__()",
            "        self.backbone = models.resnet18(pretrained=True)",
            "        self.backbone.fc = nn.Identity()",
            "        ",
            "        # Detection head",
            "        self.detection_head = nn.Sequential(",
            "            nn.Linear(512, 1024),",
            "            nn.ReLU(),",
            "            nn.Linear(1024, (num_classes + 5) * 3)  # 3 anchor boxes",
            "        )",
            "    ",
            "    def forward(self, x):",
            "        features = self.backbone(x)",
            "        detections = self.detection_head(features)",
            "        return detections.view(x.size(0), 3, -1)  # Reshape for anchor boxes"
        ]
        
        for line in detection_examples:
            print(f"   {line}")

def create_pytorch_cheat_sheet():
    """Create a comprehensive PyTorch cheat sheet."""
    print("\n" + "="*70)
    print("PYTORCH COMPREHENSIVE CHEAT SHEET")
    print("="*70)
    
    sections = {
        "ESSENTIAL IMPORTS": [
            "import torch",
            "import torch.nn as nn",
            "import torch.optim as optim",
            "import torch.nn.functional as F",
            "from torch.utils.data import DataLoader, Dataset",
            "import torchvision",
            "import torchvision.transforms as transforms"
        ],
        
        "BASIC WORKFLOW": [
            "# 1. Data preparation",
            "transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])",
            "dataset = torchvision.datasets.MNIST(root='./data', train=True, transform=transform)",
            "dataloader = DataLoader(dataset, batch_size=64, shuffle=True)",
            "",
            "# 2. Model definition",
            "class Net(nn.Module):",
            "    def __init__(self):",
            "        super(Net, self).__init__()",
            "        self.fc1 = nn.Linear(784, 128)",
            "        self.fc2 = nn.Linear(128, 10)",
            "    def forward(self, x):",
            "        x = x.view(-1, 784)",
            "        x = F.relu(self.fc1(x))",
            "        return self.fc2(x)",
            "",
            "# 3. Training setup",
            "model = Net()",
            "criterion = nn.CrossEntropyLoss()",
            "optimizer = optim.Adam(model.parameters(), lr=0.001)",
            "",
            "# 4. Training loop",
            "for data, target in dataloader:",
            "    optimizer.zero_grad()",
            "    output = model(data)",
            "    loss = criterion(output, target)",
            "    loss.backward()",
            "    optimizer.step()"
        ],
        
        "COMMON LAYERS": [
            "# Fully Connected",
            "nn.Linear(in_features, out_features)",
            "",
            "# Convolutional",
            "nn.Conv2d(in_channels, out_channels, kernel_size)",
            "nn.MaxPool2d(kernel_size, stride)",
            "",
            "# Recurrent",
            "nn.LSTM(input_size, hidden_size, num_layers)",
            "nn.GRU(input_size, hidden_size)",
            "",
            "# Normalization",
            "nn.BatchNorm2d(num_features)",
            "nn.LayerNorm(normalized_shape)",
            "",
            "# Activation",
            "nn.ReLU(), nn.LeakyReLU(), nn.Sigmoid(), nn.Tanh()",
            "",
            "# Regularization",
            "nn.Dropout(p=0.5)"
        ],
        
        "PERFORMANCE TIPS": [
            "# Use DataLoader with multiple workers",
            "DataLoader(dataset, batch_size=64, num_workers=4)",
            "",
            "# Pin memory for faster GPU transfer",
            "DataLoader(dataset, pin_memory=True)",
            "",
            "# Use appropriate device",
            "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')",
            "model.to(device), data.to(device)",
            "",
            "# Enable mixed precision training",
            "from torch.cuda.amp import autocast, GradScaler",
            "",
            "# Gradient clipping",
            "torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)",
            "",
            "# Model checkpointing",
            "torch.save(model.state_dict(), 'model.pth')"
        ]
    }
    
    for section, content in sections.items():
        print(f"\n{section}:")
        print("-" * len(section))
        for line in content:
            print(f"   {line}")

def main():
    """Main function to demonstrate all PyTorch concepts."""
    print("PYTORCH COMPREHENSIVE GUIDE")
    print("=" * 70)
    print("This module covers all major aspects of PyTorch for deep learning")
    print("To run actual code, install: pip install torch torchvision torchaudio")
    
    demonstrate_pytorch_basics()
    PyTorchTensorOperations.tensor_basics()
    PyTorchNeuralNetworks.basic_networks()
    PyTorchNeuralNetworks.advanced_architectures()
    PyTorchTrainingLoop.basic_training()
    PyTorchTrainingLoop.advanced_training()
    PyTorchDataHandling.data_loading()
    PyTorchDataHandling.data_transforms()
    PyTorchComputerVision.pretrained_models()
    PyTorchComputerVision.object_detection()
    create_pytorch_cheat_sheet()
    
    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print("1. Install PyTorch: pip install torch torchvision torchaudio")
    print("2. Practice with PyTorch tutorials: https://pytorch.org/tutorials/")
    print("3. Explore PyTorch Lightning for high-level training")
    print("4. Check PyTorch Hub for pre-trained models")
    print("5. Try Google Colab for free GPU training")

if __name__ == "__main__":
    main()
