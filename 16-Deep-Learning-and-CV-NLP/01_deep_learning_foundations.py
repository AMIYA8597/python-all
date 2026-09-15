"""
# ==============================================================================
# LABORATORY: DEEP LEARNING (FOUNDATIONS & PYTORCH)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to write a Neural Network from scratch in pure Python. 
# They write nested `for` loops to multiply the matrices and manually calculate 
# the Calculus derivatives for 100,000 parameters. The script takes 3 weeks to 
# train on a CPU.
#
# A senior AI engineer uses PyTorch. They understand that PyTorch is fundamentally 
# a mathematical Tensor library built on C++ and CUDA. They write a `forward()` 
# function to define the mathematical graph. When they call `loss.backward()`, 
# PyTorch's `autograd` engine traverses the computational graph backwards, executing 
# the Calculus Chain Rule across 100,000 parameters on the GPU in 0.001 seconds. 
# The model trains in 5 minutes.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master PyTorch Tensors and GPU execution (`.to('cuda')`).
# - Architect a Neural Network class (`nn.Module`).
# - Execute Automatic Differentiation (`autograd`) and Gradient Descent.
#
# ==============================================================================
"""

import numpy as np
# We simulate PyTorch architecture using NumPy for the Laboratory environment 
# so it mathematically executes on any machine without requiring massive pip installs.
# We will build an identical conceptual mock of the PyTorch API!

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PYTORCH API (SIMULATED FOR EDUCATION)
# ==============================================================================
class Tensor:
    """A simulated PyTorch Tensor that tracks its own Calculus gradients!"""
    def __init__(self, data, requires_grad=False):
        self.data = np.array(data)
        self.requires_grad = requires_grad
        self.grad = np.zeros_like(self.data, dtype=float)

    def zero_grad(self):
        """Wipes the gradients before the next iteration."""
        self.grad = np.zeros_like(self.data, dtype=float)

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, requires_grad={self.requires_grad})"


class LinearLayer:
    """Simulates torch.nn.Linear(in_features, out_features)"""
    def __init__(self, in_features: int, out_features: int):
        # Initialize Weights randomly, and Bias to zeros
        # Weights shape: (in_features, out_features)
        self.weights = Tensor(np.random.randn(in_features, out_features) * 0.1, requires_grad=True)
        self.bias = Tensor(np.zeros(out_features), requires_grad=True)
        
    def forward(self, x: Tensor) -> Tensor:
        """The Forward Pass: Y = X @ W + B"""
        # Save X for the backward pass!
        self.x_cache = x
        
        out_data = np.dot(x.data, self.weights.data) + self.bias.data
        return Tensor(out_data)


# ==============================================================================
# 4. THE BUSINESS LOGIC (THE NEURAL NETWORK ARCHITECTURE)
# ==============================================================================
class SimpleNeuralNet:
    """Simulates a subclass of torch.nn.Module"""
    def __init__(self):
        # A simple network with 1 Hidden Layer
        self.fc1 = LinearLayer(in_features=3, out_features=16) # Hidden Layer
        self.fc2 = LinearLayer(in_features=16, out_features=1) # Output Layer
        
    def relu(self, x: Tensor) -> Tensor:
        """Activation Function: max(0, x)"""
        return Tensor(np.maximum(0, x.data))

    def forward(self, x: Tensor) -> Tensor:
        """Defines the Mathematical Computational Graph!"""
        # Pass through Layer 1
        out = self.fc1.forward(x)
        # Pass through Non-Linear Activation
        out = self.relu(out)
        # Pass through Layer 2 (Output)
        out = self.fc2.forward(out)
        return out


class DLSimulator:
    
    def execute_training_step(self):
        print("\n  [INIT] Architecting Neural Network...")
        model = SimpleNeuralNet()
        
        # 1. THE DATA
        # A batch of 4 inputs, each with 3 features
        X_batch = Tensor(np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
            [0.1, 0.2, 0.3]
        ]))
        
        # 2. THE FORWARD PASS
        print("\n  [FORWARD PASS] Pushing Data through the Graph...")
        predictions = model.forward(X_batch)
        print(f"  -> Raw Output Shape: {predictions.data.shape}")
        
        # 3. THE CALCULUS (AUTOGRAD SIMULATION)
        print("\n  [BACKWARD PASS] Simulating `loss.backward()` (Calculus Chain Rule)...")
        print("  -> Calculating Partial Derivatives (Gradients) for all Weights and Biases.")
        
        # We manually simulate populating the gradients
        model.fc1.weights.grad = np.random.randn(*model.fc1.weights.data.shape)
        model.fc2.weights.grad = np.random.randn(*model.fc2.weights.data.shape)
        
        # 4. THE OPTIMIZER (GRADIENT DESCENT)
        print("\n  [OPTIMIZER] Simulating `optimizer.step()`...")
        learning_rate = 0.01
        
        # W = W - (Learning_Rate * Gradient)
        model.fc1.weights.data -= learning_rate * model.fc1.weights.grad
        model.fc2.weights.data -= learning_rate * model.fc2.weights.grad
        
        print("  -> Weights successfully updated in the opposite direction of the Gradient!")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_deep_learning():
    section_header("Deep Learning: PyTorch Architecture & Autograd")
    
    sim = DLSimulator()
    sim.execute_training_step()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By architecting a Computational Graph, the Deep Learning framework ")
    print("  mathematically tracks every matrix multiplication in the Forward Pass. ")
    print("  This allows the Autograd engine to automatically execute the Calculus ")
    print("  Chain Rule backwards, eliminating the need to write manual derivatives.")


def run_all_labs():
    demonstrate_deep_learning()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the mathematical purpose of an Activation Function like ReLU (`max(0, x)`) between Neural Network layers?"
   Senior Answer: "To Break Mathematical Linearity. If you stack 50 Linear Layers (`X @ W + B`) on top of each other without an activation function, the mathematics collapses. A linear combination of a linear combination is mathematically just a single linear combination. The 50-layer network physically acts exactly like a 1-layer network, and is incapable of learning complex, curved patterns (like a circle or a face). By wrapping the output in a non-linear Activation Function like ReLU, we introduce mathematical 'bends' and 'thresholds' into the Tensor, allowing the network to approximate ANY mathematical function in the universe (Universal Approximation Theorem)."

2. Interviewer: "Explain exactly what `loss.backward()` physically executes in PyTorch."
   Senior Answer: "The Calculus Chain Rule via Computational Graphs. During the `forward()` pass, PyTorch builds a Directed Acyclic Graph (DAG) in RAM, recording exactly which Tensors interacted with each other. When you execute `loss.backward()`, the Autograd engine traverses that exact graph in reverse. It applies the mathematical Chain Rule of calculus at every single node, calculating the partial derivative (the Gradient) of the Loss with respect to every single Weight Tensor in the entire network. These gradients are stored in the `.grad` attribute of the Weights."

3. Interviewer: "Why do we call `optimizer.zero_grad()` at the very beginning of a PyTorch training loop?"
   Senior Answer: "Gradient Accumulation Prevention. PyTorch mathematically accumulates (sums) gradients in the `.grad` attribute by design, which is highly useful for training massive models across multiple micro-batches when GPU RAM is constrained. However, in standard training, if you don't explicitly wipe the `.grad` attributes to zero at the start of a new loop, the gradients from Loop 2 will mathematically add themselves to the gradients from Loop 1. By Loop 50, the Gradients will be massively inflated, causing the Gradient Descent optimizer to take a catastrophic step into infinity, violently exploding the model weights."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Deep Learning (Foundations) Completed.")
