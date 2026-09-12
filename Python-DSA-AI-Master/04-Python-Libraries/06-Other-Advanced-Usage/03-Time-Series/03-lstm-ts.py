"""
Module: 03-lstm-ts
Description: Textbook-grade interactive lesson on Long Short-Term Memory (LSTM) networks for Time Series Forecasting.

===========================================================================
LONG SHORT-TERM MEMORY (LSTM) NETWORKS FOR TIME SERIES FORECASTING
===========================================================================

Learning Objectives:
1. Understand the core mathematical concepts and architecture of LSTMs.
2. Build an LSTM cell from scratch using NumPy to demystify the internal workings.
3. Learn how to prepare time-series data for Sequence-to-Sequence / Sequence-to-Vector learning.
4. Implement a production-ready LSTM using PyTorch.
5. Analyze Time Complexity (Big-O) of LSTM forward and backward passes.
6. Solve a real-world Time Series forecasting challenge.

---------------------------------------------------------------------------
1. CONCEPT EXPLANATION & MATHEMATICAL BACKGROUND
---------------------------------------------------------------------------
Standard Recurrent Neural Networks (RNNs) suffer from the "vanishing gradient" problem 
when trying to learn long-term dependencies in sequence data.

LSTMs solve this by introducing a "memory cell" state (C_t) and three gating 
mechanisms that control the flow of information:
1. Forget Gate (f_t): Decides what information to discard from the previous cell state.
2. Input Gate (i_t): Decides what new information to store in the cell state.
3. Output Gate (o_t): Decides what to output based on the cell state.

Mathematical Equations for a single LSTM cell at time step t:
Let x_t be the input vector at time t.
Let h_{t-1} be the hidden state from the previous time step.

Forget Gate:
    f_t = sigmoid(W_f @ [h_{t-1}, x_t] + b_f)

Input Gate:
    i_t = sigmoid(W_i @ [h_{t-1}, x_t] + b_i)
    C_tilde_t = tanh(W_C @ [h_{t-1}, x_t] + b_C)  (Candidate memory)

Cell State Update:
    C_t = f_t * C_{t-1} + i_t * C_tilde_t

Output Gate:
    o_t = sigmoid(W_o @ [h_{t-1}, x_t] + b_o)
    h_t = o_t * tanh(C_t)

Where:
- @ denotes matrix multiplication.
- * denotes element-wise multiplication (Hadamard product).
- W and b are learnable weights and biases.

---------------------------------------------------------------------------
2. BIG-O COMPLEXITY ANALYSIS
---------------------------------------------------------------------------
Time Complexity per time step:
- Let d be the input dimension (features).
- Let h be the hidden state dimension (units).
- The concatenated vector [h_{t-1}, x_t] has dimension (h + d).
- The weight matrices (W_f, W_i, W_C, W_o) have dimensions h x (h + d).
- Matrix multiplication W @ [h_{t-1}, x_t] takes O(h * (h + d)) operations.
- Since there are 4 such multiplications, Time Complexity per step = O(h^2 + h*d).
- For a sequence of length T, total Forward Pass Time Complexity = O(T * (h^2 + h*d)).
- Backpropagation Through Time (BPTT) also takes O(T * (h^2 + h*d)).

Space Complexity:
- Storing the weights takes O(h * (h + d)).
- Storing the hidden states and cell states for all T steps (required for BPTT) takes O(T * h).
- Total Space Complexity = O(h^2 + h*d + T*h).

===========================================================================
"""

import math
import time
from typing import List, Tuple, Dict, Any, Optional

try:
    import numpy as np
    # Setting seed for reproducibility
    np.random.seed(42)
except ImportError:
    print("NumPy is required for the from-scratch implementation. Please install it.")
    np = None  # type: ignore

# Optional PyTorch import for the advanced implementation
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


# =============================================================================
# 1. HELPER FUNCTIONS: ACTIVATIONS
# =============================================================================

def sigmoid(x: 'np.ndarray') -> 'np.ndarray':
    """
    Computes the sigmoid activation function element-wise.
    
    Formula: sigmoid(x) = 1 / (1 + exp(-x))
    
    Args:
        x (np.ndarray): Input array.
        
    Returns:
        np.ndarray: Output array with values squeezed between 0 and 1.
    """
    # np.clip used to avoid overflow in exp
    x = np.clip(x, -500, 500)
    return 1.0 / (1.0 + np.exp(-x))

def tanh(x: 'np.ndarray') -> 'np.ndarray':
    """
    Computes the hyperbolic tangent activation function element-wise.
    
    Formula: tanh(x) = (exp(x) - exp(-x)) / (exp(x) + exp(-x))
    
    Args:
        x (np.ndarray): Input array.
        
    Returns:
        np.ndarray: Output array with values squeezed between -1 and 1.
    """
    return np.tanh(x)


# =============================================================================
# 2. FROM-SCRATCH LSTM IMPLEMENTATION
# =============================================================================

class LSTMCellNumPy:
    """
    A single LSTM cell implemented from scratch using NumPy to demonstrate
    the internal gating mechanisms and mathematics.
    
    Attributes:
        input_size (int): Dimensionality of the input (x_t).
        hidden_size (int): Dimensionality of the hidden state (h_t) and cell state (C_t).
    """
    
    def __init__(self, input_size: int, hidden_size: int):
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # We need to initialize weights for 4 gates.
        # To make it efficient, we usually concatenate weights for [h_{t-1}, x_t].
        concat_size = self.input_size + self.hidden_size
        
        # Xavier/Glorot Initialization
        limit = np.sqrt(1.0 / concat_size)
        
        # Forget Gate weights and bias
        self.W_f = np.random.uniform(-limit, limit, (self.hidden_size, concat_size))
        # It's common practice to initialize the forget gate bias to 1 to encourage
        # remembering early in training.
        self.b_f = np.ones((self.hidden_size, 1))
        
        # Input Gate weights and bias
        self.W_i = np.random.uniform(-limit, limit, (self.hidden_size, concat_size))
        self.b_i = np.zeros((self.hidden_size, 1))
        
        # Candidate Cell State weights and bias
        self.W_C = np.random.uniform(-limit, limit, (self.hidden_size, concat_size))
        self.b_C = np.zeros((self.hidden_size, 1))
        
        # Output Gate weights and bias
        self.W_o = np.random.uniform(-limit, limit, (self.hidden_size, concat_size))
        self.b_o = np.zeros((self.hidden_size, 1))

    def forward(self, x_t: 'np.ndarray', h_prev: 'np.ndarray', C_prev: 'np.ndarray') -> Tuple['np.ndarray', 'np.ndarray']:
        """
        Executes a single forward step of the LSTM cell.
        
        Args:
            x_t (np.ndarray): Input vector at time t. Shape: (input_size, 1).
            h_prev (np.ndarray): Hidden state from time t-1. Shape: (hidden_size, 1).
            C_prev (np.ndarray): Cell state from time t-1. Shape: (hidden_size, 1).
            
        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - h_t: New hidden state. Shape: (hidden_size, 1).
                - C_t: New cell state. Shape: (hidden_size, 1).
        """
        # Ensure vectors are column vectors
        x_t = x_t.reshape(-1, 1)
        h_prev = h_prev.reshape(-1, 1)
        C_prev = C_prev.reshape(-1, 1)
        
        # Concatenate h_prev and x_t along the row axis
        # concat_input shape: (hidden_size + input_size, 1)
        concat_input = np.vstack((h_prev, x_t))
        
        # 1. Forget Gate: decides what to forget from the past cell state
        # f_t shape: (hidden_size, 1)
        f_t = sigmoid(np.dot(self.W_f, concat_input) + self.b_f)
        
        # 2. Input Gate: decides what new information to add
        # i_t shape: (hidden_size, 1)
        i_t = sigmoid(np.dot(self.W_i, concat_input) + self.b_i)
        
        # 3. Candidate Cell State: new candidate values that could be added to the state
        # C_tilde_t shape: (hidden_size, 1)
        C_tilde_t = tanh(np.dot(self.W_C, concat_input) + self.b_C)
        
        # 4. Update Cell State: combine old memory (forgotten appropriately) and new memory
        # C_t shape: (hidden_size, 1)
        C_t = f_t * C_prev + i_t * C_tilde_t
        
        # 5. Output Gate: decides what part of the cell state to output
        # o_t shape: (hidden_size, 1)
        o_t = sigmoid(np.dot(self.W_o, concat_input) + self.b_o)
        
        # 6. Hidden State: output based on the filtered cell state
        # h_t shape: (hidden_size, 1)
        h_t = o_t * tanh(C_t)
        
        return h_t, C_t

def demo_numpy_lstm() -> None:
    """
    Demonstrates the basic usage of the from-scratch NumPy LSTM Cell.
    """
    if np is None:
        return
        
    print("\n" + "="*50)
    print("--- 1. NumPy From-Scratch LSTM Cell Demo ---")
    print("="*50)
    
    input_dim = 3  # e.g., temperature, humidity, pressure
    hidden_dim = 4 # Size of our hidden representations
    seq_length = 5 # Number of time steps
    
    # Initialize the cell
    lstm_cell = LSTMCellNumPy(input_size=input_dim, hidden_size=hidden_dim)
    
    # Initial states are typically zeros
    h_t = np.zeros((hidden_dim, 1))
    C_t = np.zeros((hidden_dim, 1))
    
    # Generate some random dummy sequence data (time_steps, input_dim)
    sequence = np.random.randn(seq_length, input_dim)
    
    print(f"Sequence length: {seq_length}")
    print(f"Input dimension per step: {input_dim}")
    print(f"Hidden dimension: {hidden_dim}\n")
    
    # Process the sequence step by step
    for t in range(seq_length):
        x_t = sequence[t]
        h_t, C_t = lstm_cell.forward(x_t, h_t, C_t)
        print(f"Time Step {t+1}:")
        print(f"  Input x_t: {x_t.round(3)}")
        print(f"  New Hidden State h_t (first 2 vals): {h_t.flatten()[:2].round(3)}")
        print(f"  New Cell State C_t (first 2 vals): {C_t.flatten()[:2].round(3)}")
    
    print("\nNumPy LSTM demo completed successfully.")


# =============================================================================
# 3. DATA PREPARATION FOR TIME SERIES
# =============================================================================

def create_sequences(data: List[float], seq_length: int) -> Tuple[List[List[float]], List[float]]:
    """
    Converts a 1D time series array into sequences of length `seq_length` and 
    their corresponding targets (the next value).
    
    This is crucial for Time Series Forecasting. For example, if we want to predict
    the stock price tomorrow based on the last 5 days, our seq_length is 5.
    
    Args:
        data (List[float]): The univariate time series data.
        seq_length (int): The number of past time steps used as input.
        
    Returns:
        Tuple[List[List[float]], List[float]]:
            - X: List of input sequences.
            - y: List of target values.
            
    Time Complexity: O(N) where N is the length of the data.
    Space Complexity: O(N * seq_length) to store the sequences.
    """
    X = []
    y = []
    for i in range(len(data) - seq_length):
        # The input is a sequence of length seq_length
        seq = data[i : i + seq_length]
        # The target is the value immediately following the sequence
        target = data[i + seq_length]
        X.append(seq)
        y.append(target)
        
    return X, y

def demo_data_preparation() -> None:
    """
    Demonstrates time series sliding window sequence creation.
    """
    print("\n" + "="*50)
    print("--- 2. Time Series Data Preparation Demo ---")
    print("="*50)
    
    # Dummy time series data: e.g., daily sales
    ts_data = [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0]
    seq_len = 3
    
    print(f"Original Time Series: {ts_data}")
    print(f"Sequence Length (Lookback Window): {seq_len}\n")
    
    X, y = create_sequences(ts_data, seq_len)
    
    for i in range(len(X)):
        print(f"Sample {i+1}: Input Sequence (X) = {X[i]} --> Target (y) = {y[i]}")


# =============================================================================
# 4. ADVANCED IMPLEMENTATION: PYTORCH LSTM FORECASTER
# =============================================================================

if TORCH_AVAILABLE:
    class PyTorchLSTMForecaster(nn.Module):
        """
        A production-grade PyTorch implementation of an LSTM model for Time Series
        forecasting. It consists of an LSTM layer followed by a Fully Connected 
        (Linear) layer to map the hidden state to the predicted output.
        """
        
        def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, output_dim: int):
            """
            Args:
                input_dim (int): Number of expected features in the input `x`
                hidden_dim (int): Number of features in the hidden state `h`
                num_layers (int): Number of recurrent layers (e.g., 2 for a stacked LSTM)
                output_dim (int): Dimensionality of the output prediction.
            """
            super(PyTorchLSTMForecaster, self).__init__()
            self.hidden_dim = hidden_dim
            self.num_layers = num_layers
            
            # The core LSTM layer
            # batch_first=True means inputs should be shaped (batch_size, seq_len, input_dim)
            self.lstm = nn.LSTM(
                input_size=input_dim, 
                hidden_size=hidden_dim, 
                num_layers=num_layers, 
                batch_first=True
            )
            
            # Fully connected layer to map from hidden state space to output space
            self.fc = nn.Linear(hidden_dim, output_dim)
            
        def forward(self, x: 'torch.Tensor') -> 'torch.Tensor':
            """
            Forward pass of the model.
            
            Args:
                x (torch.Tensor): Input tensor of shape (batch_size, seq_len, input_dim).
                
            Returns:
                torch.Tensor: Predictions of shape (batch_size, output_dim).
            """
            # Initialize hidden state and cell state with zeros.
            # Shape: (num_layers, batch_size, hidden_dim)
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).requires_grad_()
            
            # We need to detach as we are doing truncated backpropagation through time (BPTT)
            # Or in this simple setup, just passing zeros is fine for each new sequence.
            
            # Forward propagate LSTM
            # out shape: (batch_size, seq_len, hidden_dim)
            # _ contains the final hidden and cell states
            out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
            
            # We only care about the prediction at the *last* time step for sequence-to-vector task.
            # out[:, -1, :] gets the hidden state at the final time step for all sequences in the batch.
            out = self.fc(out[:, -1, :]) 
            return out


def demo_pytorch_lstm() -> None:
    """
    Demonstrates training a PyTorch LSTM on a simple sine wave time series.
    """
    if not TORCH_AVAILABLE:
        print("PyTorch not available. Skipping advanced implementation.")
        return
        
    print("\n" + "="*50)
    print("--- 3. PyTorch LSTM Forecasting (Sine Wave) Demo ---")
    print("="*50)
    
    # 1. Generate Dummy Data (Sine wave)
    # 100 data points from 0 to 10
    time_axis = np.linspace(0, 10, 100)
    data = np.sin(time_axis).tolist()
    
    seq_length = 5
    X_list, y_list = create_sequences(data, seq_length)
    
    # Convert lists to PyTorch Tensors
    # X shape needs to be (batch_size, seq_length, input_dim) -> (95, 5, 1)
    X_tensor = torch.tensor(X_list, dtype=torch.float32).unsqueeze(-1)
    # y shape needs to be (batch_size, output_dim) -> (95, 1)
    y_tensor = torch.tensor(y_list, dtype=torch.float32).unsqueeze(-1)
    
    # 2. Initialize Model, Loss, and Optimizer
    input_dim = 1
    hidden_dim = 16
    num_layers = 1
    output_dim = 1
    
    model = PyTorchLSTMForecaster(input_dim, hidden_dim, num_layers, output_dim)
    criterion = nn.MSELoss() # Mean Squared Error for regression
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    # 3. Training Loop
    epochs = 50
    start_time = time.time()
    
    print(f"Training on {len(X_tensor)} sequences for {epochs} epochs...")
    for epoch in range(epochs):
        model.train()
        
        # Zero the gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)
        
        # Backward pass and optimize
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"  Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}")
            
    end_time = time.time()
    print(f"Training completed in {end_time - start_time:.4f} seconds.")
    
    # 4. Quick Evaluation
    model.eval()
    with torch.no_grad():
        test_seq = torch.tensor(data[-seq_length:], dtype=torch.float32).unsqueeze(0).unsqueeze(-1)
        pred = model(test_seq)
        
        # We predict the value that should logically follow the end of our sine wave
        actual_next_time = time_axis[-1] + (time_axis[1] - time_axis[0])
        actual_next_val = math.sin(actual_next_time)
        
        print(f"\nEvaluating final prediction:")
        print(f"  Input sequence (last {seq_length} points): {[round(x, 4) for x in data[-seq_length:]]}")
        print(f"  Predicted next value: {pred.item():.4f}")
        print(f"  Actual expected sine value: {actual_next_val:.4f}")


# =============================================================================
# 5. PERFORMANCE, EDGE CASES & BEST PRACTICES
# =============================================================================

def analyze_performance_and_edge_cases() -> None:
    """
    Analyzes performance bottlenecks and discusses edge cases for LSTMs.
    """
    print("\n" + "="*50)
    print("--- 4. Performance Analysis & Best Practices ---")
    print("="*50)
    print("1. Data Normalization:")
    print("   LSTMs are highly sensitive to unscaled data due to the sigmoid/tanh activations.")
    print("   Always scale your time series (e.g., Min-Max scaling or Standardization) before training.")
    print("\n2. Vanishing Gradients (Mitigation):")
    print("   While LSTMs solve this better than standard RNNs, extremely long sequences (>1000 steps)")
    print("   can still cause issues. Consider Truncated BPTT or Attention mechanisms.")
    print("\n3. Overfitting:")
    print("   Time series data is often noisy and limited. Use Dropout (in LSTM layers) and Regularization.")
    print("\n4. Lookahead Bias (Data Leakage):")
    print("   CRITICAL EDGE CASE: Ensure that your target 'y' contains strictly future information relative to 'X'.")
    print("   Accidentally including future data in your input sequence invalidates the model.")
    print("\n5. Stationarity:")
    print("   Neural networks often struggle with strong trends or seasonality. Sometimes it is beneficial")
    print("   to difference the time series (predicting change rather than absolute value) beforehand.\n")


# =============================================================================
# 6. INTERVIEW CHALLENGE: ROLLING WINDOW AVERAGES
# =============================================================================

def moving_average(data: List[float], window_size: int) -> List[float]:
    """
    Common Pre-processing Interview Challenge for Time Series:
    Given a list of floats, compute the Simple Moving Average (SMA) for a given window size.
    
    Args:
        data (List[float]): The time series data.
        window_size (int): The size of the moving window.
        
    Returns:
        List[float]: The moving averages. The length will be len(data) - window_size + 1.
        
    Time Complexity: O(N) using a sliding window sum approach.
    Space Complexity: O(N) to store the result.
    """
    if window_size <= 0 or not data or window_size > len(data):
        return []
        
    result = []
    current_sum = sum(data[:window_size])
    result.append(current_sum / window_size)
    
    # O(N) sliding window approach instead of O(N * window_size)
    for i in range(window_size, len(data)):
        current_sum = current_sum - data[i - window_size] + data[i]
        result.append(current_sum / window_size)
        
    return result

def test_moving_average() -> None:
    """Tests the moving average interview challenge."""
    print("\n" + "="*50)
    print("--- 5. Interview Challenge: Fast Moving Average ---")
    print("="*50)
    
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    window = 3
    expected = [20.0, 30.0, 40.0] # (10+20+30)/3=20, (20+30+40)/3=30, (30+40+50)/3=40
    
    result = moving_average(data, window)
    
    print(f"Data: {data}")
    print(f"Window Size: {window}")
    print(f"Computed Moving Average: {result}")
    
    assert [round(x, 4) for x in result] == expected, "Moving average failed!"
    print("Test passed successfully!")


# =============================================================================
# 7. MAIN EXECUTION & TESTS
# =============================================================================

def run_tests() -> None:
    """
    Simple test suite to validate the purely algorithmic components.
    """
    print("\n" + "="*50)
    print("--- 6. Running Unit Tests ---")
    print("="*50)
    
    try:
        # Test sequences
        X, y = create_sequences([1, 2, 3, 4, 5], 2)
        assert X == [[1, 2], [2, 3], [3, 4]]
        assert y == [3, 4, 5]
        
        # Test moving average edge cases
        assert moving_average([1,2], 5) == []
        assert moving_average([], 2) == []
        
        print("All core algorithmic tests passed successfully!")
    except AssertionError as e:
        print(f"Test Failed: {e}")


if __name__ == "__main__":
    print(f"\n{'#'*60}")
    print(f"     ADVANCED PYTHON: LONG SHORT-TERM MEMORY (LSTM)     ")
    print(f"{'#'*60}\n")
    
    # 1. Math and From-Scratch Demo
    demo_numpy_lstm()
    
    # 2. Data Preparation
    demo_data_preparation()
    
    # 3. Advanced Deep Learning Implementation
    demo_pytorch_lstm()
    
    # 4. Performance & Edge Cases
    analyze_performance_and_edge_cases()
    
    # 5. Interview Challenge
    test_moving_average()
    
    # 6. Core Unit Tests
    run_tests()
    
    print(f"\n{'#'*60}")
    print(f"          END OF 03-LSTM-TS INTERACTIVE LESSON          ")
    print(f"{'#'*60}\n")
