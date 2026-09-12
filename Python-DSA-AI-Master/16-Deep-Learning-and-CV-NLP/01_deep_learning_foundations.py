"""
Deep Learning Foundations: Perceptron, Neural Networks, and Backpropagation
---------------------------------------------------------------------------
This script demonstrates the core foundations of Deep Learning from scratch using NumPy.
We will build:
1. A Simple Perceptron
2. A Multi-Layer Perceptron (MLP) with a hidden layer
3. Forward and Backward Propagation (Backpropagation)
"""

import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# ==========================================
# 1. Activation Functions and Their Derivatives
# ==========================================

def sigmoid(x):
    """Sigmoid activation function."""
    # np.clip to prevent overflow
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))

def sigmoid_derivative(x):
    """Derivative of the sigmoid function."""
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    """Rectified Linear Unit (ReLU) activation function."""
    return np.maximum(0, x)

def relu_derivative(x):
    """Derivative of the ReLU function."""
    return (x > 0).astype(float)

# ==========================================
# 2. Simple Perceptron (Single Neuron)
# ==========================================

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        self.weights = np.random.randn(input_size) * 0.01
        self.bias = 0.0
        self.learning_rate = learning_rate
        
    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        # Step function for binary classification (0 or 1)
        return np.where(linear_output >= 0.0, 1, 0)
        
    def fit(self, X, y, epochs=10):
        print("Training Simple Perceptron...")
        for epoch in range(epochs):
            errors = 0
            for xi, target in zip(X, y):
                prediction = self.predict(xi)
                update = self.learning_rate * (target - prediction)
                self.weights += update * xi
                self.bias += update
                errors += int(update != 0.0)
            if errors == 0:
                print(f"Converged at epoch {epoch + 1}")
                break
        print("Perceptron training finished.\n")

# ==========================================
# 3. Multi-Layer Perceptron (MLP) from Scratch
# ==========================================

class SimpleNeuralNetwork:
    """
    A simple 2-layer Neural Network (1 hidden layer, 1 output layer).
    Uses Sigmoid activation for hidden and output layers.
    """
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
        
        self.learning_rate = learning_rate
        
    def forward(self, X):
        """Forward propagation."""
        # Layer 1
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = sigmoid(self.Z1)
        
        # Layer 2
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = sigmoid(self.Z2)
        
        return self.A2
        
    def compute_loss(self, Y, Y_pred):
        """Mean Squared Error loss."""
        m = Y.shape[0]
        loss = (1 / (2 * m)) * np.sum(np.square(Y_pred - Y))
        return loss
        
    def backward(self, X, Y):
        """Backward propagation."""
        m = X.shape[0]
        
        # Output layer error
        dZ2 = self.A2 - Y  # Derivative of MSE with respect to Z2 (assuming linear output, simplifying)
        dW2 = (1 / m) * np.dot(self.A1.T, dZ2)
        db2 = (1 / m) * np.sum(dZ2, axis=0, keepdims=True)
        
        # Hidden layer error
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * sigmoid_derivative(self.Z1)
        dW1 = (1 / m) * np.dot(X.T, dZ1)
        db1 = (1 / m) * np.sum(dZ1, axis=0, keepdims=True)
        
        # Update weights and biases
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2

    def train(self, X, Y, epochs=10000):
        print("Training Neural Network...")
        for epoch in range(epochs):
            # Forward pass
            Y_pred = self.forward(X)
            
            # Compute loss
            loss = self.compute_loss(Y, Y_pred)
            
            # Backward pass
            self.backward(X, Y)
            
            if (epoch + 1) % 2000 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.4f}")
        print("Neural Network training finished.\n")

if __name__ == "__main__":
    print("=== Deep Learning Foundations ===\n")
    
    # Example 1: Logic OR Gate using Perceptron
    X_logic = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_or = np.array([0, 1, 1, 1])
    
    print("Testing Perceptron on Logical OR Gate:")
    perceptron = Perceptron(input_size=2)
    perceptron.fit(X_logic, y_or)
    
    for x_i in X_logic:
        print(f"Input: {x_i}, Prediction: {perceptron.predict(x_i)}")
    print("\n")
    
    # Example 2: XOR Gate using Multi-Layer Perceptron
    # (Perceptron cannot solve XOR, we need a hidden layer)
    y_xor = np.array([[0], [1], [1], [0]])
    
    print("Testing MLP on Logical XOR Gate:")
    nn = SimpleNeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=0.5)
    nn.train(X_logic, y_xor, epochs=10000)
    
    predictions = nn.forward(X_logic)
    for x_i, pred in zip(X_logic, predictions):
        print(f"Input: {x_i}, Prediction: {pred[0]:.4f} (Rounded: {np.round(pred[0])})")
