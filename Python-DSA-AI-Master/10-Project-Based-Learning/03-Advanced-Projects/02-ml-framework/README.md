# Project: Custom Machine Learning Framework (Mini-Torch/SciKit)

## 1. Project Overview

### What is this project?
In this advanced project, you will build a micro Machine Learning framework from scratch using pure Python and NumPy. This framework will encompass building blocks for both traditional machine learning (like linear regression and k-means) and foundational deep learning (an automatic differentiation engine, multi-layer perceptrons, and basic optimizers). 

### Why does it exist?
Modern ML frameworks like PyTorch, TensorFlow, and Scikit-Learn abstract away the complex underlying mathematics and systems engineering. While incredibly useful for production, they can obscure *how* the algorithms actually work. By building a micro-framework from scratch, you develop a profound understanding of:
- Backpropagation and the Chain Rule (Automatic Differentiation).
- Vectorization and matrix calculus.
- How gradient descent updates weights.
- The architectural design of a scalable numerical library.

### Industry Use Cases
- **Foundational Knowledge:** Core requirement for ML Engineers and AI Researchers.
- **Embedded AI:** Creating highly optimized, minimal-dependency ML libraries for edge devices (IoT).
- **Custom Architectures:** When existing frameworks lack support for highly specialized, non-standard neural architectures.

---

## 2. Technical Architecture & Concepts

### Automatic Differentiation (Autograd)
At the heart of any modern neural network framework is an **Autograd** engine. It tracks all operations performed on tensors to compute gradients automatically.
- **Computation Graph:** We represent operations as a Directed Acyclic Graph (DAG). Nodes are tensors (variables or constants), and edges represent mathematical operations.
- **Forward Pass:** Computing the value of the final output (e.g., Loss).
- **Backward Pass:** Traversing the graph in reverse (topological sort) to compute the gradient of the output with respect to every leaf node using the chain rule.

### Core Modules to Implement:
1. **`Tensor` class:** A wrapper around NumPy arrays that tracks gradients (`grad`), the operation that created it (`_ctx`), and its children in the computation graph.
2. **`Module` class:** A base class for neural network layers (similar to `nn.Module` in PyTorch).
3. **`Linear` layer:** Computes $Y = XW + b$.
4. **`Loss` functions:** Mean Squared Error (MSE), Binary Cross Entropy (BCE).
5. **`Optimizer`:** Stochastic Gradient Descent (SGD) to update tensor data using computed gradients.

---

## 3. Implementation Steps

1. **Phase 1: The Tensor and Autograd Engine:**
   Implement scalar or vector tracking. Ensure basic operations (`add`, `mul`, `relu`) can correctly compute local gradients and accumulate them.
2. **Phase 2: Neural Network Layers:**
   Implement a `Linear` layer that initializes Weights and Biases as tensors requiring gradients. Implement activation functions.
3. **Phase 3: Loss and Optimization:**
   Implement the MSE loss function. Create an SGD optimizer that iterates over a model's parameters and updates them: $param = param - learning\_rate * grad$.
4. **Phase 4: Training Loop:**
   Combine everything to train a simple Multi-Layer Perceptron (MLP) on a toy dataset (e.g., XOR problem or synthetic regression data).

---

## 4. Advanced Concepts & Best Practices

- **Broadcasting:** Ensuring that your custom Tensor class gracefully handles NumPy's broadcasting rules during forward and backward passes. This is usually the hardest part of building autograd engines!
- **Topological Sort:** For the backward pass, you must ensure you calculate the gradient of a node only after all its dependencies have been calculated.
- **Memory Management:** In production frameworks, keeping the entire computation graph in memory is expensive. Concepts like `no_grad()` contexts are critical for inference.

---

## 5. Realistic Interview Questions

1. **System Design:** "How would you design the base `Tensor` class to support backpropagation?"
2. **Mathematics:** "Derive the gradient of the Loss with respect to the weights $W$ in a linear layer $Y = XW + b$."
3. **Debugging:** "If your custom neural network is outputting `NaN` for loss after a few epochs, what are the most likely causes and how do you fix them?" (Answer: Exploding gradients, learning rate too high, or numerical instability in log/exp functions).

---

## 6. Practical Exercises

- **Exercise 1:** Extend the framework to support the `Softmax` activation function and `Categorical Cross-Entropy` loss for multi-class classification.
- **Exercise 2:** Implement a `DataLoader` class that batches data and shuffles it per epoch.
- **Exercise 3:** Implement an advanced optimizer like `Adam` or `RMSprop`.
