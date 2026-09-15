"""
# ==============================================================================
# LABORATORY: MATHEMATICS FOR AI (CALCULUS & GRADIENTS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a Neural Network. They execute the forward pass and 
# see that the model is wrong. They have 1 Million weights. How do they know 
# which specific weight to increase, and which to decrease? Random guessing 
# would take billions of years.
#
# A senior AI engineer uses "Calculus". They calculate the "Derivative" (Slope) 
# of the Error relative to each specific weight. If the derivative is positive, 
# it mathematically proves that increasing the weight increases the error. 
# Therefore, the engineer subtracts the derivative from the weight, mathematically 
# forcing the error to decrease. This is Gradient Descent. It is the only reason 
# AI is capable of "learning".
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Derivatives (Instantaneous Rate of Change).
# - Execute Partial Derivatives for multi-variable functions.
# - Architect Gradient Descent to mathematically minimize Loss.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (CALCULUS & GRADIENT DESCENT)
# ==============================================================================
class CalculusMathematics:
    
    @staticmethod
    def simulate_derivative():
        """
        [SECURE] The Derivative (Slope).
        Formula: f(x) = x^2, f'(x) = 2x
        This tells us the steepness of the curve at any exact point.
        """
        print("  [INIT] Calculating the Derivative of f(x) = x^2...")
        
        # We are at position x = 3.0
        x = 3.0
        print(f"  -> Current Position (x): {x}")
        
        # The Loss (Error) is the physical height of the curve
        loss = x**2
        print(f"  -> Current Loss f(x): {loss}")
        
        # The Derivative (Slope) tells us which way the curve is pointing
        slope = 2 * x
        print(f"  -> Derivative (Slope) f'(x): {slope}")
        
        print("\n  [MATHEMATICAL PROOF] The slope is Positive (+6.0). This mathematically ")
        print("  proves that if we move forward (increase x), the Loss will INCREASE. ")
        print("  To minimize the Loss, we must move backwards (against the gradient).")

    @staticmethod
    def simulate_gradient_descent():
        """
        [SECURE] Gradient Descent Optimization.
        Formula: W_new = W_old - (Learning_Rate * Gradient)
        """
        print("\n  [INIT] Executing Gradient Descent to find the Global Minimum...")
        
        # 1. Random Initialization
        weight = 8.0  # Start far away from the perfect answer (which is 0.0)
        learning_rate = 0.1
        epochs = 5
        
        print(f"  -> Initial Weight: {weight}")
        print(f"  -> Learning Rate: {learning_rate}")
        
        # 2. The Training Loop (Backpropagation)
        for epoch in range(1, epochs + 1):
            
            # Step 1: Calculate current Loss: f(x) = x^2
            loss = weight**2
            
            # Step 2: Calculate the Gradient (Derivative): f'(x) = 2x
            gradient = 2 * weight
            
            # Step 3: Update the Weight (Gradient Descent!)
            # We subtract the gradient to mathematically force the loss downwards.
            weight_new = weight - (learning_rate * gradient)
            
            print(f"\n  [EPOCH {epoch}]")
            print(f"  -> Loss:     {loss:.4f}")
            print(f"  -> Gradient: {gradient:.4f}")
            print(f"  -> Weight updated from {weight:.4f} to {weight_new:.4f}")
            
            weight = weight_new
            
        print("\n  [FLAWLESS] The Weight mathematically converged towards 0.0, ")
        print("  and the Error (Loss) plummeted. The Artificial Intelligence 'Learned'.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_calculus():
    section_header("Mathematics for AI: Calculus & Gradients")
    
    math = CalculusMathematics()
    math.simulate_derivative()
    math.simulate_gradient_descent()


def run_all_labs():
    demonstrate_calculus()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the mathematical purpose of the 'Learning Rate' (Alpha) in Gradient Descent?"
   Senior Answer: "The Step Size constraint. The Derivative simply gives us the geometric Slope of the curve (the direction to step). If the slope is $6.0$ and we just subtract it directly ($W = W - 6.0$), the step might be so violently large that we mathematically overshoot the minimum valley and fly up the opposite side of the mountain (Divergence). The Learning Rate (e.g., $0.01$) acts as a geometric dampener. We calculate $W = W - (0.01 \\cdot 6.0)$, forcing the optimizer to take micro-steps down the hill, guaranteeing mathematical convergence at the absolute bottom."

2. Interviewer: "Explain the 'Chain Rule' in Calculus and why it is mandatory for Deep Learning Backpropagation."
   Senior Answer: "Derivative Composition. A Deep Neural Network is simply a nested mathematical function: $f(g(h(x)))$. The Final Loss depends on Layer 3, which depends on Layer 2, which depends on Layer 1. If we want to know how the weights in Layer 1 affect the Final Loss, we cannot calculate it directly. The Chain Rule states that the derivative of a nested function is the product of their individual derivatives: $\\frac{\\partial L}{\\partial W_1} = \\frac{\\partial L}{\\partial Y_3} \\cdot \\frac{\\partial Y_3}{\\partial Y_2} \\cdot \\frac{\\partial Y_2}{\\partial Y_1} \\cdot \\frac{\\partial Y_1}{\\partial W_1}$. Backpropagation is literally just the programmatic execution of the Calculus Chain Rule, multiplying gradients backward through the network topology."

3. Interviewer: "What is the 'Vanishing Gradient Problem' in Deep Recurrent Neural Networks (RNNs)?"
   Senior Answer: "Mathematical Underflow via the Chain Rule. When backpropagating through 100 layers, the Chain Rule requires multiplying 100 derivatives together. If the activation function is Sigmoid, its maximum derivative is $0.25$. Multiplying $0.25 \\cdot 0.25 \\cdot 0.25$ one hundred times mathematically crushes the final number to $0.0000001$ (Underflow). When this microscopically tiny gradient finally reaches Layer 1, the weight update is $0.0$. The early layers of the network physically cannot learn. This is solved by using the ReLU activation function (whose derivative is exactly $1.0$, allowing gradients to flow backward uncrushed) or by using ResNet Skip Connections."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Mathematics for AI (Calculus) Completed.")
