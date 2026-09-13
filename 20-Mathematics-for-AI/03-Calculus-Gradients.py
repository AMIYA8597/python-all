"""
# 03 - Calculus: Derivatives, Gradients, and Gradient Descent

## A. Concept Name
Calculus for AI: Derivatives, Partial Derivatives, The Chain Rule, and Gradient Descent.

## B. One-Sentence Definition
Calculus in AI is the mathematics of measuring how a small change in a neural network's weights will affect its error (Loss), allowing the network to update those weights to minimize the error over time.

## C. Why Does This Exist?
A Neural Network is just a massive mathematical function with millions of parameters (weights). When it makes a prediction, it calculates a "Loss" (how wrong it was). But how does it know whether to increase or decrease a specific weight to make the Loss smaller next time? 
**Calculus** gives us the **Derivative** (the slope). It tells us exactly which direction is "downhill" towards zero error.

## D. Intuition & Real-World Analogy
Imagine you are blindfolded on a rugged mountain (the Loss Landscape) and your goal is to reach the lowest valley (minimum error). 
Because you are blindfolded, you can't see the valley. But you can feel the slope of the ground under your feet with your foot. 
- If the ground slopes *down to your left*, you take a step left.
- If it slopes *down to your right*, you take a step right.

In AI:
- The **Derivative/Gradient** is your foot feeling the slope.
- Taking a step is **Gradient Descent** (updating the weights).
- The size of your step is the **Learning Rate**.

## E. Core Mathematical Concepts

### 1. Derivative (1D)
Tells you the rate of change of a function `y = f(x)` at a specific point.
If `f(x) = x^2`, the derivative `f'(x) = 2x`.
If `x = 3`, the slope is 6. This means if you increase `x` slightly, `y` will increase 6 times as fast.

### 2. Partial Derivative & The Gradient (Multi-D)
In AI, we have millions of variables (weights), not just one `x`. 
A **Partial Derivative** measures how the Loss changes if we tweak just ONE weight, freezing all others.
The **Gradient** is simply a Vector containing all the partial derivatives. It points in the direction of the STEEPEST ASCENT. To minimize loss, we step in the *negative* direction of the gradient.

### 3. The Chain Rule (Backpropagation)
Neural networks are nested functions: `Layer3(Layer2(Layer1(x)))`.
To find how a weight in Layer 1 affects the final Loss, we must multiply the derivatives backwards through the layers. 
Formula: `dz/dx = (dz/dy) * (dy/dx)`. This is the mathematical engine of **Backpropagation**.

## F. Common Mistakes & Anti-Patterns
1. **Learning Rate Too High**: If your step size is massive, you will bounce back and forth across the valley and never reach the bottom (Divergence). The Loss becomes `NaN` (Not a Number) very quickly.
2. **Learning Rate Too Low**: If your step size is microscopic, it will take the AI billions of years to learn (Convergence is too slow).

## G. Interview Connection
**Q: "Explain how Gradient Descent works in a Neural Network."**
A: "We calculate the Loss based on the current predictions. We then use Backpropagation (applying the Chain Rule of calculus) to calculate the Gradient of the Loss with respect to every weight in the network. Finally, we update every weight by subtracting a small portion (the Learning Rate) of its gradient, effectively taking a step downhill in the loss landscape."

## H. Implementation & Guided Practice
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Manually Calculating a Derivative
# ==========================================
def demonstrate_derivatives():
    print("--- 1. Single Variable Derivative ---")
    # Function: f(x) = x^2
    # Derivative: f'(x) = 2x
    
    x = 3.0
    print(f"Let x = {x}")
    print(f"f(x) = x^2 = {x**2}")
    
    # Mathematical derivative
    exact_slope = 2 * x
    print(f"Exact derivative (2x): {exact_slope}")
    
    # Numerical derivative (how computers often approximate it if they can't do exact math)
    # limit as h -> 0 of (f(x + h) - f(x)) / h
    h = 0.0001
    approx_slope = (((x + h)**2) - (x**2)) / h
    print(f"Numerical approximation: {approx_slope:.4f}")


# ==========================================
# 2. Gradient Descent from Scratch
# ==========================================
def gradient_descent():
    """
    We want to find the minimum of the function f(x) = (x - 4)^2
    We know the minimum is at x = 4. Let's see if the AI can find it!
    """
    print("\n--- 2. Gradient Descent Algorithm ---")
    
    # The Loss Function: L(w) = (w - 4)^2
    # The Derivative: dL/dw = 2 * (w - 4)
    
    # 1. Initialize weight randomly (Blindfolded on the mountain)
    w = 10.0  
    learning_rate = 0.1
    epochs = 20
    
    print(f"Starting weight: {w:.4f}. Goal is to reach 4.0")
    
    for epoch in range(epochs):
        # Calculate current loss
        loss = (w - 4) ** 2
        
        # Calculate the gradient (slope) at current w
        gradient = 2 * (w - 4)
        
        # UPDATE RULE: w = w - (learning_rate * gradient)
        w = w - (learning_rate * gradient)
        
        if epoch % 5 == 0 or epoch == epochs - 1:
            print(f"Epoch {epoch:2d}: Loss = {loss:6.2f}, Gradient = {gradient:6.2f}, Updated w = {w:.4f}")
            
    print(f"Final weight found by Gradient Descent: {w:.4f}")


# ==========================================
# 3. Debugging: Learning Rate Issues
# ==========================================
def exploding_gradients():
    """
    What happens if the learning rate is too big?
    """
    print("\n--- 3. Debugging: Learning Rate Too High (Explosion) ---")
    w = 10.0
    learning_rate = 1.1 # WAY TOO HIGH!
    
    for epoch in range(5):
        gradient = 2 * (w - 4)
        w = w - (learning_rate * gradient)
        print(f"Epoch {epoch}: w = {w:8.2f} (Bouncing wildly!)")

## I. Active Recall Questions
"""
1. If the gradient of a weight is a positive number, should we increase or decrease the weight to minimize loss?
   *Answer: Decrease it. A positive gradient means the slope is going UP to the right. To go down, we must go left (decrease the weight).*
2. What is the Chain Rule used for in Deep Learning?
   *Answer: Backpropagation. It allows us to calculate how a weight in the very first layer affects the final output error by chaining together the derivatives of all intermediate layers.*
3. Why do we need a Learning Rate? Why not just subtract the full gradient?
   *Answer: The gradient only points in the right direction for a very tiny, microscopic distance. If you take a massive step using the full gradient, the landscape might have curved upwards in the meantime, causing you to overshoot the valley.*
"""

if __name__ == "__main__":
    print("========== CALCULUS: GRADIENT DESCENT MASTERCLASS ==========\n")
    demonstrate_derivatives()
    gradient_descent()
    exploding_gradients()
    print("\n========== MASTERCLASS COMPLETE ==========")
