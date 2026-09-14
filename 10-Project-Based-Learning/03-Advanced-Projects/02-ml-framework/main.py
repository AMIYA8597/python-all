"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (NEURAL NETWORK FRAMEWORK)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer imports `tensorflow` or `pytorch`, types `model.fit()`, 
# and watches the Loss number go down. If you ask them *why* the number goes 
# down, they cannot answer. They treat AI as literal magic. When their model 
# fails to converge due to "Vanishing Gradients", they are mathematically helpless.
#
# A senior AI engineer builds a Neural Network framework from scratch using pure 
# Python and NumPy. They manually execute Forward Propagation (Matrix Multiplication), 
# compute the Loss (Mean Squared Error), and mathematically calculate the Partial 
# Derivatives of the error with respect to every single weight matrix (Backpropagation). 
# By architecting the Gradient Descent algorithm themselves, they demystify AI 
# into pure, deterministic Linear Algebra.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Matrix Multiplication (Dot Products) for Forward Propagation.
# - Execute algorithmic Backpropagation using Partial Derivatives (Calculus).
# - Architect a modular Deep Learning framework (Layers, Activations).
#
# ==============================================================================
"""

import math
import random
from typing import List

# Gracefully handle NumPy
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MATHEMATICAL PRIMITIVES (ACTIVATIONS & LOSS)
# ==============================================================================
class Sigmoid:
    """
    The Non-Linear Activation Function.
    If a Neural Network only uses linear math (y = mx + b), it mathematically 
    collapses into a single layer. We MUST inject non-linearity to learn complex shapes!
    """
    @staticmethod
    def forward(x):
        # Squeezes any number between 0 and 1
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def backward(x):
        # The exact Calculus Derivative of the Sigmoid function!
        s = Sigmoid.forward(x)
        return s * (1.0 - s)


class MeanSquaredError:
    """The Mathematical Loss Function."""
    @staticmethod
    def forward(predictions, targets):
        # Calculates the exact mathematical error (distance from the truth)
        return np.mean(np.square(predictions - targets))

    @staticmethod
    def backward(predictions, targets):
        # The exact Calculus Derivative of the MSE function!
        # This tells us WHICH DIRECTION to move the weights to reduce the error.
        return 2.0 * (predictions - targets) / predictions.size


# ==============================================================================
# 4. THE NEURAL NETWORK ARCHITECTURE
# ==============================================================================
class DenseLayer:
    """A fully-connected Neural Network layer."""
    def __init__(self, input_size: int, output_size: int):
        # We mathematically initialize the Weights to small random numbers.
        # Shape: (input_size, output_size)
        self.weights = np.random.randn(input_size, output_size) * 0.1
        # Biases initialize to zero. Shape: (1, output_size)
        self.biases = np.zeros((1, output_size))
        
        # State caches for Backpropagation!
        self.inputs = None
        self.z = None

    def forward(self, inputs):
        """
        Forward Propagation.
        Y = (X • W) + B
        """
        self.inputs = inputs
        # The Dot Product! This is the Heavy Math that GPUs accelerate.
        self.z = np.dot(inputs, self.weights) + self.biases
        return Sigmoid.forward(self.z)

    def backward(self, gradient, learning_rate: float):
        """
        Backpropagation (The Chain Rule of Calculus).
        """
        # 1. Gradient of the Activation Function
        sig_deriv = Sigmoid.backward(self.z)
        delta = gradient * sig_deriv
        
        # 2. Gradient of the Weights and Biases
        weights_gradient = np.dot(self.inputs.T, delta)
        biases_gradient = np.sum(delta, axis=0, keepdims=True)
        
        # 3. Calculate the gradient to pass BACKWARDS to the previous layer
        input_gradient = np.dot(delta, self.weights.T)
        
        # 4. GRADIENT DESCENT: Physically update the matrices to make the AI smarter!
        self.weights -= learning_rate * weights_gradient
        self.biases -= learning_rate * biases_gradient
        
        return input_gradient


class SequentialNetwork:
    """The execution engine that chains multiple layers together."""
    def __init__(self):
        self.layers: List[DenseLayer] = []
        
    def add(self, layer: DenseLayer):
        self.layers.append(layer)
        
    def train(self, X, Y, epochs: int, learning_rate: float):
        print(f"  [TRAINING INITIATED] Epochs: {epochs} | LR: {learning_rate}")
        
        for epoch in range(epochs):
            # --- FORWARD PASS ---
            current_output = X
            for layer in self.layers:
                current_output = layer.forward(current_output)
                
            predictions = current_output
            
            # --- LOSS CALCULATION ---
            loss = MeanSquaredError.forward(predictions, Y)
            
            if epoch % 1000 == 0:
                print(f"    -> Epoch {epoch:04d} | Mathematical Loss: {loss:.6f}")
                
            # --- BACKWARD PASS (LEARNING) ---
            # 1. Calculate the initial gradient of the error
            gradient = MeanSquaredError.backward(predictions, Y)
            
            # 2. Ripple the gradient backwards through every layer!
            for layer in reversed(self.layers):
                gradient = layer.backward(gradient, learning_rate)

    def predict(self, X):
        current_output = X
        for layer in self.layers:
            current_output = layer.forward(current_output)
        return current_output


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_neural_network():
    section_header("Project: Raw Neural Network Framework")
    
    if not HAS_NUMPY:
        print("  [ERROR] NumPy not installed. Run `pip install numpy`.")
        return
        
    print("  [SCENARIO] Training an AI to learn the XOR Logic Gate.")
    print("  XOR is a non-linear problem. A single neuron mathematically cannot solve it!")
    
    # The XOR Dataset (Inputs and Targets)
    X = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    
    Y = np.array([
        [0],
        [1],
        [1],
        [0]
    ])
    
    # Architect the AI
    nn = SequentialNetwork()
    # Hidden Layer: 2 Inputs -> 4 Neurons
    nn.add(DenseLayer(2, 4))
    # Output Layer: 4 Neurons -> 1 Output Answer
    nn.add(DenseLayer(4, 1))
    
    # Train the AI!
    nn.train(X, Y, epochs=5000, learning_rate=0.5)
    
    # Test the AI!
    print("\n  [INFERENCE TEST]")
    predictions = nn.predict(X)
    
    for i in range(len(X)):
        input_val = X[i]
        true_val = Y[i][0]
        pred_val = predictions[i][0]
        # We mathematically round it! > 0.5 is a 1, < 0.5 is a 0.
        rounded = 1 if pred_val > 0.5 else 0
        print(f"    -> Input {input_val} | Target: {true_val} | AI Predicts: {pred_val:.4f} => [{rounded}]")
        
    print("\n  [SUCCESS] The AI mathematically conquered the Non-Linear XOR problem!")


def run_all_labs():
    demonstrate_neural_network()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did we initialize the layer weights to `np.random.randn() * 0.1`? Why couldn't we just initialize all the weights mathematically to `0.0`?"
   Senior Answer: "The Symmetry Breaking Problem. If you initialize all weights in a Neural Network to exactly $0.0$, every single neuron in the Hidden Layer will execute the exact same mathematical Forward propagation. During Backpropagation, they will all receive the exact same Gradient, and they will all update by the exact same amount. The network mathematically collapses; $100$ hidden neurons will behave exactly like $1$ single neuron, permanently destroying the network's ability to learn complex patterns. Random initialization mathematically breaks this symmetry, allowing each individual neuron to learn a slightly different feature of the dataset."

2. Interviewer: "Why did we mathematically require a Non-Linear Activation Function (like `Sigmoid` or `ReLU`) after every Dense Layer?"
   Senior Answer: "Linear Collapse. A Dense Layer is purely linear math ($Y = XW + B$). If you stack $50$ Dense Layers on top of each other without an activation function, the math dictates that a series of linear transformations is mathematically equivalent to a *single* linear transformation. The $50$-layer Deep Neural Network collapses into a $1$-layer Linear Regression model, rendering it utterly incapable of solving non-linear problems like XOR, image recognition, or natural language processing. The Non-Linear activation function warps the mathematical space, allowing the network to draw complex, curved decision boundaries."

3. Interviewer: "Explain the architectural mechanics of 'Backpropagation' and the 'Chain Rule' of Calculus."
   Senior Answer: "Forward Propagation pushes the data through the matrices to generate a prediction. We then calculate the Loss (how mathematically wrong the prediction is). However, we need to know how to adjust the weights in Layer 1 to reduce that error, but Layer 1 is buried deep inside the network! Backpropagation uses the Calculus Chain Rule to mathematically trace the error backwards. We calculate the Partial Derivative of the Loss with respect to Layer 3, pass that gradient backward to calculate the derivative for Layer 2, and pass it backward again to Layer 1. This tells every single matrix exactly which direction (up or down) to adjust its weights to minimize the global error, forming the absolute foundation of all modern AI training."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Neural Network Framework) Completed.")
