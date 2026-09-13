"""
# ==============================================================================
# LABORATORY: DEEP LEARNING ARCHITECTURE (PYTORCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# TensorFlow/Keras uses a highly abstracted `model.fit()` engine. It is 
# excellent for rapidly deploying standard architectures to production, but it 
# completely hides the underlying math.
#
# PyTorch is the undisputed king of Machine Learning Research. It forces you 
# to manually write the mathematics of the Training Loop (Forward Pass, Loss 
# Calculation, Backpropagation, Weight Update). 
#
# PyTorch uses a "Dynamic Computation Graph". This means the calculus engine 
# builds the graph on-the-fly exactly as your Python code executes, allowing 
# you to use standard Python `if/else` statements and `for` loops *inside* your 
# Neural Network architecture!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand PyTorch Tensors and `autograd`.
# - Construct an Object-Oriented Neural Network (`nn.Module`).
# - Manually implement the 5-step Deep Learning Training Loop.
#
# ==============================================================================
"""

import numpy as np

# In a real environment: pip install torch torchvision
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PYTORCH TENSORS & AUTOGRAD
# ==============================================================================
def demonstrate_tensors_autograd():
    section_header("PyTorch Tensors and Autograd")
    
    if not HAS_TORCH:
        print("[WARNING] PyTorch not installed. Install using: pip install torch")
        return
        
    print("Just like NumPy, PyTorch uses multidimensional arrays (Tensors).")
    print("However, PyTorch Tensors can be instantly moved to a GPU, and they ")
    print("natively track calculus gradients!\n")
    
    # 1. DEVICE PLACEMENT (CPU vs GPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"System is currently utilizing: {device}")
    
    # 2. TENSORS WITH AUTOGRAD
    # requires_grad=True tells the PyTorch calculus engine to track every single 
    # mathematical operation performed on this tensor to calculate the derivative later!
    x = torch.tensor(3.0, requires_grad=True)
    
    # Mathematical operation (Forward Pass)
    # y = 2x^2 + 5x
    y = 2 * (x ** 2) + 5 * x
    
    print(f"Equation: y = 2x^2 + 5x")
    print(f"Value of x : {x.item()}")
    print(f"Result (y) : {y.item()}")
    
    # 3. BACKPROPAGATION (The Magic)
    # The derivative of (2x^2 + 5x) is (4x + 5). 
    # If x=3, the gradient should be: 4(3) + 5 = 17!
    
    y.backward() # Calculates the calculus derivative instantly!
    
    print(f"Calculated Gradient (dy/dx): {x.grad.item()} (Exactly 17!)")


# ==============================================================================
# 4. OBJECT-ORIENTED NEURAL NETWORKS (nn.Module)
# ==============================================================================
# In PyTorch, you do not use a high-level `Sequential` wrapper. 
# You explicitly define the Network as an Object-Oriented Class.
# Every network MUST inherit from `nn.Module` and MUST implement `forward()`.

if HAS_TORCH:
    class SimpleClassifier(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super(SimpleClassifier, self).__init__()
            # Define the layers (the mathematical weights)
            # nn.Linear is PyTorch's name for a Dense/Fully-Connected layer (Y = WX + B)
            self.layer1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.layer2 = nn.Linear(hidden_size, num_classes)
            
        def forward(self, x):
            # Define EXACTLY how the data flows through the weights.
            # Because this is standard Python, you could literally put an `if/else` 
            # statement here to route data to different layers based on a condition!
            out = self.layer1(x)
            out = self.relu(out)
            out = self.layer2(out)
            # Note: We do NOT apply Softmax here. In PyTorch, the Loss Function 
            # (CrossEntropyLoss) mathematically applies Softmax internally for stability!
            return out


# ==============================================================================
# 5. THE MANUAL TRAINING LOOP
# ==============================================================================
def demonstrate_training_loop():
    section_header("The 5-Step PyTorch Training Loop")
    
    if not HAS_TORCH: return
    
    print("In Keras, you just call `model.fit()`. In PyTorch, you write the Loop.")
    print("This gives you absolute microscopic control over the mathematics.\n")
    
    # 1. GENERATE SYNTHETIC DATA
    # 100 samples, 10 features, 3 classes
    X_train = torch.randn(100, 10)
    # Target labels must be integers (LongTensor) for Classification
    y_train = torch.randint(0, 3, (100,), dtype=torch.long) 
    
    # 2. INSTANTIATE MODEL, LOSS, AND OPTIMIZER
    model = SimpleClassifier(input_size=10, hidden_size=32, num_classes=3)
    
    # CrossEntropyLoss expects RAW logits (no Softmax) and Integer targets (no One-Hot encoding)
    criterion = nn.CrossEntropyLoss()
    
    # The Optimizer needs to know EXACTLY which weights it is allowed to modify!
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    # 3. THE EPOCH LOOP
    epochs = 5
    for epoch in range(epochs):
        
        # --- THE 5 SACRED STEPS OF PYTORCH TRAINING ---
        
        # Step 1: Zero the Gradients!
        # PyTorch accumulates gradients by default. If you don't zero them, 
        # epoch 2 will add its gradients to epoch 1, and the math will explode.
        optimizer.zero_grad()
        
        # Step 2: The Forward Pass
        # Pass the data through the network to get the predictions.
        outputs = model(X_train)
        
        # Step 3: Calculate the Loss (Error)
        # Compare the predictions to the true answers.
        loss = criterion(outputs, y_train)
        
        # Step 4: The Backward Pass (Calculus)
        # Calculate the derivative of the Loss with respect to every single weight!
        loss.backward()
        
        # Step 5: The Optimizer Step (Update Weights)
        # Shift the weights slightly in the opposite direction of the gradient to reduce error.
        optimizer.step()
        
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
        
    print("\nTraining complete! The Loss decreased steadily.")


def run_all_labs():
    demonstrate_tensors_autograd()
    demonstrate_training_loop()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the difference between a Static Computation Graph (TensorFlow v1) and a Dynamic Computation Graph (PyTorch)?
   Answer: In a Static Graph, you define the entire Neural Network architecture *before* you run any data through it. It compiles the architecture into an immutable C++ graph, meaning you cannot easily use Python `if` statements or `while` loops inside the network. In a Dynamic Graph (PyTorch), the calculus graph is built *on the fly* as the Python code executes. This allows for extreme flexibility (e.g., dynamically changing the depth of the network based on the input data length, which is crucial for Natural Language Processing).

2. Why MUST you call `optimizer.zero_grad()` at the start of every PyTorch training step?
   Answer: By default, PyTorch *accumulates* (adds) gradients during the `.backward()` call. If you have 3 batches of data, and you don't clear the gradients, the gradients from Batch 3 will be physically added to the gradients of Batch 2 and Batch 1. The optimizer will take a massive, mathematically incorrect step, destroying the model. You must explicitly flush the gradients to zero before calculating the backward pass for a new batch.

3. Why do we not put a `Softmax` activation function on the final layer of a PyTorch classification model?
   Answer: Mathematical stability. If you apply Softmax manually, and then pass those probabilities into the standard PyTorch `nn.CrossEntropyLoss()`, you can encounter catastrophic floating-point arithmetic errors (like taking the `log(0)`). PyTorch's `CrossEntropyLoss` is engineered to accept raw, unscaled linear numbers (called "Logits") and applies the highly-optimized `LogSoftmax` function internally, guaranteeing perfect mathematical precision and preventing NaN crashes.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: PyTorch Deep Learning Architecture Completed.")
