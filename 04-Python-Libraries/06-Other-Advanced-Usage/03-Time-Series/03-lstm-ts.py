"""
# ==============================================================================
# LABORATORY: DEEP LEARNING TIME SERIES (LSTMs)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# ARIMA relies on strict linear regression. It assumes that if the temperature 
# dropped 2 degrees yesterday, it will have the exact same mathematical effect 
# today as it did 10 years ago.
#
# But the real world is highly non-linear.
#
# To capture massive, complex, non-linear relationships across time, we use 
# Deep Learning. However, a standard Neural Network (Multi-Layer Perceptron) 
# has no concept of Time. If you pass in Tuesday's data, it completely forgets 
# Monday's data.
#
# We solve this using Recurrent Neural Networks (RNNs), specifically Long 
# Short-Term Memory (LSTM) networks. An LSTM has a literal "Memory Cell" 
# that loops back onto itself. As it steps through time, it mathematically 
# learns what information to "Remember" and what to "Forget", allowing it to 
# connect a pattern from Day 1 directly to an outcome on Day 100!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Recurrent Neural Networks (RNNs).
# - Understand the math of the LSTM (Forget Gate, Input Gate, Output Gate).
# - Construct a Sliding Window dataset to train an LSTM in PyTorch/TensorFlow.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RNNs AND THE VANISHING GRADIENT PROBLEM
# ==============================================================================
def demonstrate_rnn_architecture():
    section_header("RNNs and the Vanishing Gradient")
    
    print("A standard Neural Network feeds data Forward: Input -> Hidden -> Output.")
    
    print("\nA Recurrent Neural Network (RNN) feeds data Forward AND Sideways!")
    print("At Time=1, it processes Monday's data, and outputs a Hidden State.")
    print("At Time=2, it processes Tuesday's data AND the Hidden State from Monday!")
    
    print("\n--- The Fatal Flaw of RNNs ---")
    print("Imagine a 100-word sentence: 'I grew up in France... [95 words]... I speak fluent __.'")
    print("To predict 'French', the network must connect step 100 to step 5.")
    
    print("\nDuring Backpropagation, the Calculus gradient must chain-rule backwards ")
    print("through 95 multiplication steps. Because the weights are usually < 1.0, ")
    print("multiplying 0.5 * 0.5 * 0.5... ninety-five times results in exactly 0.0.")
    print("The gradient 'Vanishes'. The network physically cannot learn long-term ")
    print("dependencies. It forgets 'France' by step 10.")


# ==============================================================================
# 4. THE LSTM ARCHITECTURE (GATES)
# ==============================================================================
def demonstrate_lstm_architecture():
    section_header("The LSTM Architecture (Memory Cells)")
    
    print("In 1997, Hochreiter and Schmidhuber invented the LSTM to solve the ")
    print("Vanishing Gradient. They added a conveyor belt called the 'Cell State' ")
    print("that runs straight through the entire network with almost zero multiplication, ")
    print("allowing gradients to flow backwards flawlessly!")
    
    print("\nThe LSTM controls this conveyor belt using 3 Mathematical 'Gates':\n")
    
    print("1. THE FORGET GATE (Sigmoid)")
    print("   Looks at Yesterday's Memory and Today's Input.")
    print("   Calculates a number between 0.0 and 1.0.")
    print("   If it outputs 0.0, it violently deletes the old memory (e.g., the ")
    print("   subject of the sentence changed from 'Alice' to 'Bob').")
    
    print("\n2. THE INPUT GATE (Sigmoid + Tanh)")
    print("   Decides what *new* information from Today is actually important ")
    print("   enough to be written onto the conveyor belt.")
    
    print("\n3. THE OUTPUT GATE (Sigmoid)")
    print("   Takes the newly updated conveyor belt memory, filters it, and ")
    print("   outputs the final prediction for Today.")


# ==============================================================================
# 5. THE SLIDING WINDOW (TIME SERIES DATA PREP)
# ==============================================================================
def demonstrate_sliding_window():
    section_header("The Sliding Window Architecture")
    
    print("You cannot just pass a flat CSV into an LSTM. You must restructure ")
    print("the data into a 3D Tensor: [Batch_Size, Time_Steps, Features].")
    print("We use a 'Sliding Window'.\n")
    
    # 1. Raw Sequential Data (e.g., Stock Prices for 10 days)
    data = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    print(f"Raw Data: {data}")
    
    # 2. Define the Window Size
    # We want to use the past 3 days (Time_Steps=3) to predict the 4th day.
    window_size = 3
    
    X = []
    y = []
    
    print("\nExecuting Sliding Window:")
    for i in range(len(data) - window_size):
        # Extract 3 days of features
        window_x = data[i : i+window_size]
        # Extract the 4th day as the target label
        target_y = data[i + window_size]
        
        X.append(window_x)
        y.append(target_y)
        
        print(f"Features (X): {window_x} ---> Target (y): {target_y}")
        
    X = np.array(X)
    y = np.array(y)
    
    print(f"\nFinal X Tensor Shape: {X.shape}")
    print("This is a 2D matrix. Before passing to PyTorch/TensorFlow, you MUST ")
    print("reshape it to 3D by adding the 'Features' dimension: X.reshape(7, 3, 1)")
    print("This perfectly matches: [7 Samples, 3 Time_Steps, 1 Feature(Price)].")


def run_all_labs():
    demonstrate_rnn_architecture()
    demonstrate_lstm_architecture()
    demonstrate_sliding_window()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the "Vanishing Gradient" problem in a standard Recurrent Neural Network (RNN).
   Answer: In an RNN, processing a sequence of 100 time steps requires unrolling the network 100 times. During Backpropagation Through Time (BPTT), the calculus chain rule requires multiplying the weight matrices together 100 times. Because neural network weights are typically initialized between -1.0 and 1.0 (often near 0.1), multiplying $0.1 \times 0.1 \times 0.1 \dots$ exponentially shrinks the number. By step 10, the gradient (the error signal) literally hits 0.00000. Because the gradient is zero, the weights for the earliest time steps physically cannot update. The network suffers from permanent amnesia and cannot learn long-term dependencies.

2. How does the LSTM's "Cell State" physically solve the Vanishing Gradient problem?
   Answer: Instead of passing the hidden state through a harsh non-linear activation (like `tanh`) at every single step (which crushes gradients), the LSTM introduces a secondary pathway called the "Cell State" (the conveyor belt). Information flows straight down this conveyor belt using only linear addition ($\dots + C_{t-1}$). Because the derivative of Addition is exactly 1.0, the gradient passes backward through the addition gates perfectly, without shrinking. This creates an uninterrupted "gradient highway" allowing the error signal to travel 1,000 steps backward in time without vanishing!

3. Why is it absolutely mandatory to restructure Time Series data into a 3D Tensor `[Samples, Time_Steps, Features]` before feeding it to an LSTM?
   Answer: A standard Neural Network expects 2D data: `[Batch_Size, Features]`. It processes every row independently. An LSTM expects a chronological sequence for every single row! 
   - `Samples` (Batch Size) is the number of sequences you are training on simultaneously.
   - `Time_Steps` (The Window) is how far back in time the LSTM must unroll its memory loop (e.g., look back 30 days).
   - `Features` is the number of variables at each specific time step (e.g., Price, Volume, and RSI = 3 features). 
   Without this strict 3D geometry, the deep learning compiler does not know how many times to unroll the recurrent loop in memory!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Deep Learning Time Series (LSTMs) Completed.")
