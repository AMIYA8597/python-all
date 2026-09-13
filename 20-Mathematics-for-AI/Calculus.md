# Calculus for AI

## Prerequisites
- Familiarity with basic mathematical functions (polynomials, exponentials, logarithms).
- Understanding of limits and slopes of lines.
- Basic linear algebra (vectors and matrices).

## Objectives
- Understand **Derivatives** and **Partial Derivatives**.
- Grasp the **Chain Rule** and its paramount importance in deep learning.
- Understand **Gradients**, **Jacobians**, and their geometric meanings.
- Learn how **Optimization** algorithms (like Gradient Descent) use calculus to train models.
- Explicitly connect mathematical calculus concepts to ML/AI mechanics (e.g., Backpropagation).

## Intuition
Calculus in AI is the engine of learning and optimization. While linear algebra dictates how data is represented and passed through a model, calculus determines how the model updates its internal weights to get better at its task.
- **Derivatives:** Measure the rate of change. They answer the question: "If I tweak this weight slightly, how much will the error (loss) change?"
- **Partial Derivatives:** Isolate the effect of a single variable in a multivariable function, which is critical since neural networks have millions of parameters.
- **Gradients:** Point in the direction of the steepest ascent of a function. By moving in the opposite direction, we minimize the error.
- **The Chain Rule:** Allows us to compute derivatives of complex, nested functions. A deep neural network is just one giant nested function.
- **Optimization (Gradient Descent):** The iterative process of calculating the gradient and taking a step downwards to find the minimum of the loss function.

## Mathematics

### 1. Derivatives and Partial Derivatives
For a single-variable function $f(x)$, the derivative $f'(x)$ or $\frac{df}{dx}$ is the slope of the tangent line.
For a multivariable function $f(x, y, z)$, the partial derivative $\frac{\partial f}{\partial x}$ is the derivative with respect to $x$ while treating $y$ and $z$ as constants.

### 2. Gradients
The gradient of a scalar-valued multivariable function $f(x_1, \dots, x_n)$ is a vector containing all its partial derivatives:
$$ \nabla f = \left[ \frac{\partial f}{\partial x_1}, \frac{\partial f}{\partial x_2}, \dots, \frac{\partial f}{\partial x_n} \right]^T $$
**AI Connection**: Let $L(\mathbf{w})$ be the loss function of a neural network with weights $\mathbf{w}$. To minimize $L$, we compute $\nabla L(\mathbf{w})$ and update the weights iteratively: 
$$ \mathbf{w}_{new} = \mathbf{w}_{old} - \alpha \nabla L(\mathbf{w}_{old}) $$
where $\alpha$ is the learning rate. This is Gradient Descent.

### 3. The Chain Rule
If a variable $z$ depends on $y$, and $y$ depends on $x$, then $z$ depends on $x$ via the intermediate variable $y$. The chain rule states:
$$ \frac{dz}{dx} = \frac{dz}{dy} \cdot \frac{dy}{dx} $$
**AI Connection (Backpropagation)**: A deep neural network computes an output via nested functions: $L = Loss(f_3(f_2(f_1(\mathbf{x}))))$. To find how a weight in the first layer $f_1$ affects the final Loss $L$, we multiply the local gradients backwards from the output layer to the input layer. This makes computing gradients for deep networks highly efficient.

### 4. Jacobians
If we have a vector-valued function $\mathbf{f}: \mathbb{R}^n \rightarrow \mathbb{R}^m$, its Jacobian matrix $\mathbf{J}$ contains all first-order partial derivatives. It represents the gradient of a vector-valued function:
$$ J_{i,j} = \frac{\partial f_i}{\partial x_j} $$
**AI Connection**: The Jacobian is essential when computing derivatives through layers that output multiple values, such as a Softmax activation layer, ensuring the gradients flow correctly through multidimensional transformations.

## Code Connection
```python
import numpy as np

# Gradient Descent Intuition
# Let's say we have a loss function: L(w) = w^2 + 5
def loss_function(w):
    return w**2 + 5

# The derivative of L(w) with respect to w is 2w
def gradient(w):
    return 2 * w

w = 10.0          # Initial weight guess
learning_rate = 0.1 # Step size

print(f"Initial weight: {w}, Initial Loss: {loss_function(w)}")

for epoch in range(1, 16):
    grad = gradient(w)
    w = w - learning_rate * grad # Gradient Descent Update Step
    print(f"Epoch {epoch:02d}: w = {w:.4f}, Loss = {loss_function(w):.4f}")
```
*(Refer to `03-Calculus-Gradients.py` for hands-on, runnable scripts).*

## Interview Questions
1. **Why do we subtract the gradient in Gradient Descent?**
   - *Answer*: The gradient vector points in the direction of the steepest *ascent* of the function (where the loss increases fastest). Since our goal is to minimize the loss, we must step in the exact opposite direction, which is the negative gradient.
2. **What is the Chain Rule, and how does Backpropagation utilize it?**
   - *Answer*: The Chain Rule is a formula to compute the derivative of a composite function. Backpropagation is the algorithmic application of the chain rule. It calculates the gradient of the loss function with respect to each weight by working backward from the output layer, multiplying the local partial derivatives along the computational graph.
3. **What is the "Vanishing Gradient" problem, and why does it occur?**
   - *Answer*: In deep networks, gradients are calculated by multiplying many derivatives using the chain rule. If these derivatives are small (e.g., less than 1, as seen with Sigmoid or Tanh activations), their product becomes exponentially smaller as it propagates back to earlier layers. This causes the earlier layers to learn very slowly or not at all.
