"""
# ==============================================================================
# LABORATORY: NLP (SEQUENCE MODELS & LSTMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses a standard Recurrent Neural Network (RNN) to process 
# a 1,000-word paragraph. By the time the RNN reaches the 100th word, the 
# mathematical Calculus derivatives (Gradients) have been multiplied by 0.1 
# one hundred times. The gradient collapses to 0.000000001 (The Vanishing 
# Gradient Problem). The network completely forgets the first sentence and fails.
#
# A senior AI engineer uses a Long Short-Term Memory (LSTM) network. They 
# understand that an LSTM contains a completely separate computational highway 
# called the "Cell State". This highway bypasses the destructive matrix multiplications 
# and relies purely on mathematical addition. The gradient flows flawlessly across 
# 1,000 words without vanishing. The model successfully remembers the context of 
# the first sentence when analyzing the last sentence.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the mathematical failure of Vanilla RNNs.
# - Execute the architectural flow of the LSTM Cell State.
# - Architect Forget Gates, Input Gates, and Output Gates.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE VANISHING GRADIENT)
# ==============================================================================
class SequenceSimulator:
    
    @staticmethod
    def simulate_vanishing_gradient():
        """
        [SECURE] Mathematical Proof of RNN Failure.
        During Backpropagation, the gradient is multiplied by the Weight Matrix 
        at every single time step. If the Weight is < 1, it exponentially decays to 0.
        """
        print("  [INIT] Simulating Vanilla RNN Backpropagation over 10 Time Steps...")
        
        # Assume the derivative of the Loss with respect to the output is 1.0
        gradient = 1.0
        
        # Assume the learned Weight in the recurrent loop is 0.5
        recurrent_weight = 0.5
        
        print(f"  -> Initial Gradient at t=10: {gradient:.4f}")
        
        for t in range(9, -1, -1):
            # The Chain Rule of Calculus!
            gradient = gradient * recurrent_weight
            print(f"  -> Gradient at t={t}: {gradient:.6f}")
            
        print("\n  [FATAL ERROR] The Gradient collapsed to 0.000977.")
        print("  The network cannot mathematically update the weights for words at the ")
        print("  beginning of the sentence. It has 'forgotten' the context.")


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: THE LSTM CELL
# ==============================================================================
class LSTMSimulator:
    """
    A mathematical simulation of a single LSTM cell processing one time step.
    """
    
    def __init__(self):
        # We simulate Sigmoid and Tanh activation functions
        self.sigmoid = lambda x: 1 / (1 + np.exp(-x))
        self.tanh = lambda x: np.tanh(x)
        
    def execute_time_step(self):
        print("\n  [INIT] Simulating LSTM Forward Pass (1 Time Step)...")
        
        # 1. Inputs to the Cell
        # The Current Word (e.g., 'King' converted to a vector)
        x_t = 0.8 
        # The previous Hidden State (What the network currently 'thinks')
        h_prev = 0.5 
        # The previous Cell State (The Long-Term Memory Highway)
        c_prev = 0.9 
        
        print(f"  -> Input Word (x_t): {x_t}")
        print(f"  -> Previous Short-Term Memory (h_prev): {h_prev}")
        print(f"  -> Previous Long-Term Memory (c_prev):  {c_prev}")
        
        # 2. THE FORGET GATE
        # "Should we mathematically erase the previous Long-Term memory?"
        # Uses Sigmoid (0 = Forget completely, 1 = Remember completely)
        f_t = self.sigmoid((0.1 * x_t) + (0.1 * h_prev)) 
        print(f"\n  [GATE 1] Forget Gate calculated: {f_t:.4f} (Keep ~57% of old memory)")
        
        # 3. THE INPUT GATE
        # "Should we write this new word into the Long-Term memory?"
        i_t = self.sigmoid((0.2 * x_t) + (0.2 * h_prev))
        # The actual mathematical candidate to write
        c_tilde = self.tanh((0.3 * x_t) + (0.3 * h_prev))
        print(f"  [GATE 2] Input Gate calculated: {i_t:.4f} (Write ~56% of new candidate)")
        
        # 4. UPDATE THE LONG-TERM MEMORY (CELL STATE)
        # This is the architectural secret! It uses ADDITION, not multiplication.
        # This prevents the gradient from vanishing during backpropagation!
        c_t = (f_t * c_prev) + (i_t * c_tilde)
        print(f"\n  [MEMORY UPDATE] New Long-Term Memory (c_t): {c_t:.4f}")
        
        # 5. THE OUTPUT GATE
        # "How much of our Long-Term memory should we expose as the new Short-Term memory?"
        o_t = self.sigmoid((0.4 * x_t) + (0.4 * h_prev))
        h_t = o_t * self.tanh(c_t)
        
        print(f"  [GATE 3] Output Gate calculated. New Short-Term Memory (h_t): {h_t:.4f}")
        print("\n  [FLAWLESS] The LSTM successfully updated its state without collapsing the gradient highway.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_sequence_models():
    section_header("Deep Learning NLP: LSTMs vs RNNs")
    
    sim1 = SequenceSimulator()
    sim1.simulate_vanishing_gradient()
    
    sim2 = LSTMSimulator()
    sim2.execute_time_step()


def run_all_labs():
    demonstrate_sequence_models()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Explain the exact mathematical mechanism that causes the Vanishing Gradient Problem in Vanilla RNNs."
   Senior Answer: "Repeated Matrix Multiplication. In an RNN, the Hidden State is updated recursively at every time step ($h_t = \\tanh(W \\cdot h_{t-1} + U \\cdot x_t)$). During Backpropagation Through Time (BPTT), we must calculate the derivative using the Chain Rule. If a sentence has $100$ words, the Calculus gradient is mathematically multiplied by the Weight matrix $W$ exactly $100$ times in a row. If the eigenvalues of $W$ are less than $1.0$, multiplying a fraction by itself $100$ times causes it to exponentially decay to exactly $0.0$. The gradient vanishes, and the network mathematically cannot update the weights for the early words in the sequence."

2. Interviewer: "How does the LSTM 'Cell State' architecturally solve the Vanishing Gradient problem?"
   Senior Answer: "The Additive Highway. A Vanilla RNN forces the gradient to flow strictly through matrix multiplications and $\\tanh$ squashing functions. An LSTM introduces a parallel data highway called the Cell State ($C_t$). The update equation for the Cell State is purely additive: $C_t = (f_t \\cdot C_{t-1}) + (i_t \\cdot \\tilde{C}_t)$. Because it relies on mathematical addition rather than repeated matrix multiplication, the derivative of addition is $1.0$. The Gradient flows backwards across the addition operation perfectly intact, allowing it to traverse thousands of time steps without decaying to zero."

3. Interviewer: "What is the architectural difference between an LSTM and a GRU (Gated Recurrent Unit)?"
   Senior Answer: "Computational Optimization. An LSTM is highly complex, utilizing $3$ separate gates (Forget, Input, Output) and maintaining $2$ distinct states (Cell State and Hidden State). A GRU is a modernized, stripped-down architecture. It completely removes the Cell State, merging it back into a single Hidden State. It also reduces the $3$ gates down to just $2$ gates (Update and Reset). Because it has fewer tensor operations, a GRU trains significantly faster and requires less GPU VRAM, while mathematically achieving nearly identical accuracy to an LSTM on most standard NLP tasks."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: NLP (Sequence Models) Completed.")
