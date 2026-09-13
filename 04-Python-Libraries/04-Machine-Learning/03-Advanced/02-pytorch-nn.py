"""
# ==============================================================================
# LABORATORY: ADVANCED PYTORCH (DATALOADERS & CNNs)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# In the PyTorch Basics lab, we pushed the entire synthetic dataset directly 
# into the model all at once. In the real world, your dataset might be 1,000,000 
# HD images. This is 10 Terabytes of data. It will never fit into your 16GB GPU.
#
# Advanced PyTorch solves this using the `Dataset` and `DataLoader` architecture.
# The DataLoader streams data from the hard drive, slices it into Minibatches 
# (e.g., 32 images at a time), and pipelines it into the GPU asynchronously.
#
# We will also construct a Convolutional Neural Network (CNN) in PyTorch, 
# demonstrating how to manage the complex transition between 2D Convolutional 
# layers and 1D Fully Connected (Dense) layers.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Inherit from `torch.utils.data.Dataset` to build a Custom Dataset.
# - Stream data efficiently using `torch.utils.data.DataLoader`.
# - Architect a PyTorch CNN (`nn.Conv2d`, `nn.MaxPool2d`).
# - Save and Load models using `state_dict()`.
#
# ==============================================================================
"""

import numpy as np

# In a real environment: pip install torch torchvision
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CUSTOM DATASETS AND DATALOADERS
# ==============================================================================
# To stream Terabytes of data, you MUST create a Custom Class that inherits 
# from Dataset. You only have to implement 3 magical dunder methods!

if HAS_TORCH:
    class ImageDataset(Dataset):
        def __init__(self, num_samples):
            # In a real app, this is where you load the list of filenames from 
            # the hard drive, NOT the actual images!
            self.num_samples = num_samples
            
        def __len__(self):
            # PyTorch needs to know how many total items exist to calculate Epochs.
            return self.num_samples
            
        def __getitem__(self, idx):
            # This is the magic. PyTorch asks for item #42.
            # You open the hard drive, read image #42, turn it into a Tensor, and return it.
            # We will just generate a random 1x28x28 grayscale image tensor.
            image = torch.rand(1, 28, 28)
            label = torch.randint(0, 10, (1,)).item()
            return image, label


def demonstrate_dataloaders():
    section_header("The DataLoader Architecture")
    
    if not HAS_TORCH:
        print("[WARNING] PyTorch not installed.")
        return
        
    print("The Dataset class defines HOW to get a single image.")
    print("The DataLoader class takes the Dataset, shuffles it, chops it into ")
    print("batches, and uses multiprocessing to stream it to the GPU!\n")
    
    # 1. Instantiate the Custom Dataset (1000 total images)
    dataset = ImageDataset(num_samples=1000)
    
    # 2. Instantiate the DataLoader
    # batch_size=32: The GPU will receive 32 images at exactly the same time.
    # shuffle=True: Critical for training! Prevents the model from memorizing the order.
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Let's pull the very first batch from the stream!
    images, labels = next(iter(dataloader))
    
    print(f"Batch Images Shape: {images.shape} (Batch, Channels, Height, Width)")
    print(f"Batch Labels Shape: {labels.shape}")


# ==============================================================================
# 4. CONVOLUTIONAL NEURAL NETWORKS (CNN) IN PYTORCH
# ==============================================================================
if HAS_TORCH:
    class PyTorchCNN(nn.Module):
        def __init__(self):
            super(PyTorchCNN, self).__init__()
            
            # Convolution Block 1
            # Input channels=1 (Grayscale). Output channels=16 (Extract 16 feature maps)
            self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, padding=1)
            self.relu1 = nn.ReLU()
            self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
            
            # After pooling, the 28x28 image shrinks to 14x14!
            
            # Fully Connected Block
            # We must flatten the 16 feature maps (which are now 14x14) into a 1D vector.
            # 16 * 14 * 14 = 3136
            self.flatten = nn.Flatten()
            self.fc1 = nn.Linear(in_features=3136, out_features=128)
            self.relu2 = nn.ReLU()
            
            # Output Layer (10 classes for digits 0-9)
            self.fc2 = nn.Linear(in_features=128, out_features=10)
            
        def forward(self, x):
            # Pass data through Convolution
            x = self.conv1(x)
            x = self.relu1(x)
            x = self.pool1(x)
            
            # Pass data through Fully Connected
            x = self.flatten(x)
            x = self.fc1(x)
            x = self.relu2(x)
            x = self.fc2(x)
            
            return x


def demonstrate_cnn_and_saving():
    section_header("PyTorch CNN & State Dictionaries")
    
    if not HAS_TORCH: return
    
    # 1. INSTANTIATE THE CNN
    model = PyTorchCNN()
    
    # Pass a dummy batch of 32 images to verify the architecture works
    dummy_input = torch.rand(32, 1, 28, 28)
    output = model(dummy_input)
    
    print("CNN Architecture successfully passed a forward propagation test!")
    print(f"Output Shape: {output.shape} (32 images, 10 probabilities each)\n")
    
    # 2. SAVING THE MODEL (state_dict)
    # You NEVER save the physical Python object. You only save the `state_dict`, 
    # which is a lightweight Dictionary containing exactly the raw Matrix Weights.
    
    print("Extracting the state_dict (The Neural Weights):")
    state_dict = model.state_dict()
    for layer_name, weights in state_dict.items():
        print(f" - {layer_name}: {weights.shape}")
        
    # In a real application:
    # torch.save(model.state_dict(), 'cnn_weights.pth')
    # 
    # To load it later:
    # new_model = PyTorchCNN()
    # new_model.load_state_dict(torch.load('cnn_weights.pth'))


def run_all_labs():
    demonstrate_dataloaders()
    demonstrate_cnn_and_saving()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is the PyTorch DataLoader architecture essential for modern Deep Learning?
   Answer: Deep Learning datasets (like ImageNet or massive video files) often exceed 100 Terabytes. Your GPU only has 16GB of VRAM, and your system RAM is likely 32GB. You physically cannot load the dataset into memory using Pandas or NumPy. The `Dataset` class acts as a pointer, storing only the filepaths on the hard drive. The `DataLoader` acts as a highly optimized stream. During training, it uses multiple CPU worker threads to read 32 images from the hard drive, convert them to Tensors, and stream them into the GPU's VRAM. Once the GPU is done processing that batch, the DataLoader deletes them from VRAM and streams the next 32, allowing you to train on infinite amounts of data.

2. In PyTorch CNNs, what is the most common cause of the `RuntimeError: mat1 and mat2 shapes cannot be multiplied`?
   Answer: This error almost always occurs at the transition point between the 2D Convolutional layers and the 1D Linear (Dense) layers. When you run an image through `Conv2d` and `MaxPool2d`, the spatial dimensions (height and width) shrink mathematically based on the kernel size, stride, and padding. If a 28x28 image goes through a 2x2 MaxPool, it becomes 14x14. If you have 16 filters, the final shape is $16 \times 14 \times 14$. When you Flatten this, it becomes a 1D vector of length $3,136$. If you hardcode `nn.Linear(in_features=4000)`, PyTorch will attempt to multiply a vector of 3,136 into a matrix expecting 4,000, causing a catastrophic shape mismatch.

3. Why do we save models using `torch.save(model.state_dict())` instead of just saving the whole model object?
   Answer: If you save the entire model object (using `torch.save(model)`), Python uses standard Pickle serialization. This binds the saved file to the exact directory structure, class names, and PyTorch versions present when it was saved. If you change a class name or update PyTorch, the file will completely break upon loading. The `state_dict` is just a standard Python Dictionary that maps the Layer Names (Strings) to the raw Tensor Weights (Matrices). It is incredibly lightweight, completely independent of the Python class structure, and is the universally accepted industry standard for transferring and deploying PyTorch models.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced PyTorch Completed.")
