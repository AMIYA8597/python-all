"""
Advanced Project: Custom Machine Learning Framework (Autograd & Neural Nets)

This script implements a micro-framework for deep learning from scratch using pure Python and NumPy.
It features a custom Tensor class with an automatic differentiation engine (autograd),
basic neural network layers, loss functions, and optimizers.

It culminates in training a Multi-Layer Perceptron (MLP) to solve the non-linear XOR problem.
"""

import numpy as np
import math
from typing import List, Tuple, Union, Optional, Callable

# ---------------------------------------------------------------------------
# 1. Autograd Engine & Tensor Class
# ---------------------------------------------------------------------------

class Tensor:
    """
    A Tensor is a multi-dimensional array that tracks its computation history
    to support automatic differentiation (backpropagation).
    """
    def __init__(self, data: Union[int, float, list, np.ndarray], _children: tuple = (), _op: str = '', requires_grad: bool = False):
        self.data = np.array(data, dtype=np.float64)
        self.grad = np.zeros_like(self.data, dtype=np.float64)
        
        # Autograd graph variables
        self._backward: Callable[[], None] = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.requires_grad = requires_grad

    def __repr__(self) -> str:
        return f"Tensor(data={self.data}, grad={self.grad})"

    def zero_grad(self) -> None:
        """Resets the gradient to zero."""
        self.grad = np.zeros_like(self.data)

    def backward(self) -> None:
        """
        Executes backpropagation starting from this tensor.
        Uses topological sort to ensure gradients are computed in the correct order.
        """
        topo = []
        visited = set()
        
        def build_topo(v: 'Tensor'):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
                
        build_topo(self)
        
        # Initialize the gradient of the root node (e.g., loss) to 1
        self.grad = np.ones_like(self.data)
        
        # Apply the chain rule backwards
        for node in reversed(topo):
            node._backward()

    # --- Mathematical Operations ---

    def __add__(self, other: Union['Tensor', float, int]) -> 'Tensor':
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, (self, other), '+')
        
        def _backward():
            # Handle broadcasting during backprop
            # If self.data is (1, 3) and other is (3, 3), gradients need to be summed along broadcasted axes
            
            def unbroadcast(grad, shape):
                """Sums out broadcasted dimensions."""
                if grad.shape == shape: return grad
                ndims_added = grad.ndim - len(shape)
                for _ in range(ndims_added): grad = grad.sum(axis=0)
                for i, dim in enumerate(shape):
                    if dim == 1: grad = grad.sum(axis=i, keepdims=True)
                return grad

            if self.requires_grad:
                self.grad += unbroadcast(out.grad, self.data.shape)
            if other.requires_grad:
                other.grad += unbroadcast(out.grad, other.data.shape)
                
        out._backward = _backward
        out.requires_grad = self.requires_grad or other.requires_grad
        return out

    def __mul__(self, other: Union['Tensor', float, int]) -> 'Tensor':
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data * other.data, (self, other), '*')
        
        def _backward():
            def unbroadcast(grad, shape):
                if grad.shape == shape: return grad
                ndims_added = grad.ndim - len(shape)
                for _ in range(ndims_added): grad = grad.sum(axis=0)
                for i, dim in enumerate(shape):
                    if dim == 1: grad = grad.sum(axis=i, keepdims=True)
                return grad

            if self.requires_grad:
                self.grad += unbroadcast(other.data * out.grad, self.data.shape)
            if other.requires_grad:
                other.grad += unbroadcast(self.data * out.grad, other.data.shape)
                
        out._backward = _backward
        out.requires_grad = self.requires_grad or other.requires_grad
        return out

    def __matmul__(self, other: 'Tensor') -> 'Tensor':
        """Matrix multiplication."""
        out = Tensor(self.data @ other.data, (self, other), '@')
        
        def _backward():
            if self.requires_grad:
                self.grad += out.grad @ other.data.T
            if other.requires_grad:
                other.grad += self.data.T @ out.grad
                
        out._backward = _backward
        out.requires_grad = self.requires_grad or other.requires_grad
        return out

    def sum(self) -> 'Tensor':
        """Sums all elements."""
        out = Tensor(np.sum(self.data), (self,), 'sum')
        
        def _backward():
            if self.requires_grad:
                self.grad += np.ones_like(self.data) * out.grad
        out._backward = _backward
        out.requires_grad = self.requires_grad
        return out

    # Non-linearities
    def relu(self) -> 'Tensor':
        """Rectified Linear Unit activation."""
        out = Tensor(np.maximum(0, self.data), (self,), 'relu')
        
        def _backward():
            if self.requires_grad:
                self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        out.requires_grad = self.requires_grad
        return out

    # Dunder overrides to support python builtins
    def __radd__(self, other): return self + other
    def __rmul__(self, other): return self * other
    def __sub__(self, other): return self + (other * -1)
    def __rsub__(self, other): return (self * -1) + other


# ---------------------------------------------------------------------------
# 2. Neural Network Modules
# ---------------------------------------------------------------------------

class Module:
    """Base class for all neural network modules."""
    def zero_grad(self) -> None:
        for p in self.parameters():
            p.zero_grad()
            
    def parameters(self) -> List[Tensor]:
        return []

class Linear(Module):
    """A fully connected / dense layer."""
    def __init__(self, in_features: int, out_features: int):
        # Initialize weights with standard normal distribution scaled by sqrt(in_features) (He/Xavier approx)
        self.weight = Tensor(np.random.randn(in_features, out_features) / math.sqrt(in_features), requires_grad=True)
        self.bias = Tensor(np.zeros(out_features), requires_grad=True)

    def __call__(self, x: Tensor) -> Tensor:
        return (x @ self.weight) + self.bias

    def parameters(self) -> List[Tensor]:
        return [self.weight, self.bias]

class MLP(Module):
    """A simple Multi-Layer Perceptron."""
    def __init__(self, layer_sizes: List[int]):
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            self.layers.append(Linear(layer_sizes[i], layer_sizes[i+1]))

    def __call__(self, x: Tensor) -> Tensor:
        for i, layer in enumerate(self.layers):
            x = layer(x)
            if i < len(self.layers) - 1:
                x = x.relu() # Apply ReLU to all hidden layers
        return x
        
    def parameters(self) -> List[Tensor]:
        return [p for layer in self.layers for p in layer.parameters()]


# ---------------------------------------------------------------------------
# 3. Loss & Optimizers
# ---------------------------------------------------------------------------

def mse_loss(preds: Tensor, targets: Tensor) -> Tensor:
    """Mean Squared Error Loss."""
    diff = preds - targets
    return (diff * diff).sum() * (1.0 / preds.data.size)

class SGD:
    """Stochastic Gradient Descent Optimizer."""
    def __init__(self, parameters: List[Tensor], lr: float = 0.01):
        self.parameters = parameters
        self.lr = lr

    def step(self) -> None:
        for p in self.parameters:
            if p.requires_grad:
                p.data -= self.lr * p.grad

    def zero_grad(self) -> None:
        for p in self.parameters:
            p.zero_grad()


# ---------------------------------------------------------------------------
# 4. Main Execution (Training Loop)
# ---------------------------------------------------------------------------

def run_xor_training():
    """
    Trains an MLP on the XOR dataset. 
    XOR is non-linear and cannot be solved by a single linear layer.
    """
    print("--- Starting Neural Network Training (XOR Problem) ---")
    np.random.seed(42)

    # XOR Dataset
    X = Tensor([[0, 0], [0, 1], [1, 0], [1, 1]])
    Y = Tensor([[0], [1], [1], [0]])

    # Initialize model: 2 inputs -> 4 hidden units -> 1 output
    model = MLP([2, 4, 1])
    optimizer = SGD(model.parameters(), lr=0.1)

    epochs = 200
    for epoch in range(epochs):
        # 1. Forward pass
        preds = model(X)
        
        # 2. Compute Loss
        loss = mse_loss(preds, Y)
        
        # 3. Backward pass (Compute gradients)
        optimizer.zero_grad()
        loss.backward()
        
        # 4. Optimizer step (Update weights)
        optimizer.step()

        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch+1:03d} | Loss: {loss.data:.4f}")

    print("\n--- Training Complete. Evaluating Results ---")
    predictions = model(X)
    for i in range(4):
        pred_val = predictions.data[i][0]
        actual_val = Y.data[i][0]
        print(f"Input: {X.data[i]} | Target: {actual_val} | Prediction: {pred_val:.4f} -> Rounded: {round(pred_val)}")

if __name__ == "__main__":
    run_xor_training()
