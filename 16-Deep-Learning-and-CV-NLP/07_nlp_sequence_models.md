# Sequence Models (RNN, LSTM, GRU)

## Prerequisites
- Deep Learning fundamentals (Feedforward Neural Networks, Backpropagation).
- Word Embeddings.
- PyTorch basics (tensors, `nn.Module`).

## Objectives
- Understand why standard Feedforward Networks fail for sequence data.
- Learn the architecture and recurrent nature of RNNs.
- Understand the Vanishing Gradient Problem.
- Learn how LSTMs and GRUs solve the vanishing gradient problem using gating mechanisms.

## Intuition
Language is sequential. The meaning of a word depends heavily on the words that came before it. Standard neural networks assume all inputs are independent of each other and require fixed-size inputs.
**Recurrent Neural Networks (RNNs)** solve this by maintaining a "hidden state" (memory) that is passed from one step of the sequence to the next. The network processes a sequence one element at a time, updating its hidden state based on the current input and the previous hidden state.
However, vanilla RNNs struggle to remember long-term dependencies due to the **Vanishing Gradient Problem** (gradients shrink exponentially as they are propagated backward through time).
**Long Short-Term Memory (LSTM)** networks introduce a "cell state" and three gates (Forget, Input, Output) to carefully regulate the flow of information, allowing the network to explicitly choose what to remember and what to forget over long sequences.

## Mathematics
### Vanilla RNN Update
Given input $x_t$ at time $t$ and previous hidden state $h_{t-1}$:
$$ h_t = \tanh(W_{xh} x_t + W_{hh} h_{t-1} + b_h) $$
$$ y_t = W_{hy} h_t + b_y $$

### LSTM Core Equations
1. **Forget Gate**: $f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$
2. **Input Gate**: $i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$
3. **Candidate Cell State**: $\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$
4. **Update Cell State**: $C_t = f_t * C_{t-1} + i_t * \tilde{C}_t$
5. **Output Gate**: $o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$
6. **New Hidden State**: $h_t = o_t * \tanh(C_t)$

## Code Reference
Refer to `07_nlp_sequence_models.py` for a PyTorch implementation of an LSTM classifier.

## Interview Questions
1. **Why do we need RNNs for NLP tasks?**
   *Answer:* Standard neural networks cannot handle variable-length inputs and do not capture the sequential order of data. RNNs share weights across time steps and maintain a hidden state representing past context.
2. **What is the vanishing gradient problem in RNNs?**
   *Answer:* During backpropagation through time, gradients are multiplied by the weight matrix many times. If eigenvalues of the weight matrix are $< 1$, the gradient shrinks exponentially, preventing the network from learning long-term dependencies.
3. **How does an LSTM solve the vanishing gradient problem?**
   *Answer:* The cell state $C_t$ has an additive connection (the $+ i_t * \tilde{C}_t$ part), allowing gradients to flow backwards through time without undergoing repeated matrix multiplications, preventing them from vanishing.
