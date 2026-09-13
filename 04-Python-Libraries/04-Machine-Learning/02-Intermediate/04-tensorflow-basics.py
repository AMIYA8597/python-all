"""
# ==============================================================================
# LABORATORY: DEEP LEARNING FOUNDATIONS (TENSORFLOW & KERAS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Scikit-Learn is incredible for tabular data (CSV files, Excel sheets).
# But if you feed a 4K video or a 1,000-page book into a Random Forest, it will 
# fail completely. Complex perceptual data requires Deep Learning (Neural Networks).
#
# TensorFlow is Google's flagship open-source Deep Learning framework. 
# At its core, it is a highly optimized C++/CUDA engine for multiplying massive 
# matrices (Tensors) across thousands of GPU cores simultaneously, and automatically 
# calculating the calculus derivatives (AutoDiff) required for Backpropagation.
#
# Keras is the high-level Python API built on top of TensorFlow. It allows you 
# to stack Neural Network "Layers" like Lego bricks in just a few lines of code.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the `tf.Tensor` (the fundamental data structure of Deep Learning).
# - Construct a Deep Neural Network using the Keras `Sequential` API.
# - Understand Optimizers (Adam) and Loss Functions (Categorical Crossentropy).
# - Train a Neural Network to classify handwritten digits (MNIST).
#
# ==============================================================================
"""

import numpy as np
import os

# Suppress annoying TensorFlow C++ logging in the terminal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# In a real environment: pip install tensorflow
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Flatten, Input
    from tensorflow.keras.utils import to_categorical
    HAS_TF = True
except ImportError:
    HAS_TF = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CORE TENSORFLOW (TENSORS & GRADIENTS)
# ==============================================================================
def demonstrate_tensors():
    section_header("TensorFlow Core: Tensors and AutoDiff")
    
    if not HAS_TF:
        print("[WARNING] TensorFlow not installed. Install using: pip install tensorflow")
        return
        
    print("A Tensor is simply a multidimensional array (like a NumPy array), ")
    print("but it is explicitly engineered to live in GPU VRAM and track calculus.\n")
    
    # 1. CONSTANTS (Immutable)
    # A Matrix (Rank-2 Tensor)
    matrix = tf.constant([
        [1.0, 2.0],
        [3.0, 4.0]
    ])
    
    print(f"Tensor Shape: {matrix.shape}")
    print(f"Tensor DataType: {matrix.dtype}")
    
    # 2. VARIABLES (Mutable)
    # Variables are used to store the Weights and Biases of a Neural Network!
    # They change during training.
    weight = tf.Variable(5.0)
    
    # 3. AUTOMATIC DIFFERENTIATION (GradientTape)
    # TensorFlow contains a calculus engine. It literally records every mathematical 
    # operation on a "Tape". When you ask for the derivative, it plays the tape backwards!
    
    # Equation: y = x^2 (where x = weight)
    # Derivative: dy/dx = 2x
    # If x=5, then dy/dx = 10! Let's prove TensorFlow knows calculus:
    
    with tf.GradientTape() as tape:
        y = weight ** 2
        
    # Calculate the gradient (derivative) of y with respect to 'weight'
    gradient = tape.gradient(y, weight)
    
    print(f"\nEquation: y = x^2")
    print(f"Value of x : {weight.numpy()}")
    print(f"Calculated Gradient (dy/dx): {gradient.numpy()} (Exactly 2*5!)")


# ==============================================================================
# 4. KERAS NEURAL NETWORKS (SEQUENTIAL API)
# ==============================================================================
def demonstrate_keras_network():
    section_header("Building a Deep Neural Network (Keras)")
    
    if not HAS_TF: return
    
    print("We will build a fully connected Deep Neural Network (Multi-Layer Perceptron)")
    print("to classify 28x28 pixel images of handwritten digits (0-9).\n")
    
    # 1. SYNTHETIC DATA GENERATION (Simulating MNIST)
    # 1000 images. Each image is a 28x28 grid of pixels (Values 0 to 255)
    X_train = np.random.randint(0, 255, (1000, 28, 28))
    # Labels (0 through 9)
    y_train = np.random.randint(0, 10, 1000)
    
    # 2. DATA PREPROCESSING
    # Neural Networks HATE large numbers (it causes gradient explosion).
    # We MUST scale the pixels from [0, 255] down to [0.0, 1.0]!
    X_train = X_train.astype('float32') / 255.0
    
    # 3. ONE-HOT ENCODING
    # The network outputs 10 separate probabilities (one for each digit).
    # We must convert the label '7' into a vector: [0,0,0,0,0,0,0,1,0,0]
    y_train_encoded = to_categorical(y_train, num_classes=10)
    
    # 4. ARCHITECTING THE NETWORK
    # `Sequential` means the data flows in a straight line from Input to Output.
    model = Sequential([
        # Layer 1: Input. Flattens the 2D 28x28 image into a 1D vector of 784 pixels.
        Input(shape=(28, 28)),
        Flatten(),
        
        # Layer 2: First Hidden Layer. 128 Neurons.
        # ReLU (Rectified Linear Unit) activation introduces non-linearity.
        # Without ReLU, the network is just a giant linear regression model!
        Dense(units=128, activation='relu'),
        
        # Layer 3: Second Hidden Layer. 64 Neurons.
        Dense(units=64, activation='relu'),
        
        # Layer 4: Output Layer. Exactly 10 Neurons (one for each class 0-9).
        # Softmax activation squashes the 10 outputs so they sum exactly to 1.0 (Probabilities!)
        Dense(units=10, activation='softmax')
    ])
    
    # 5. COMPILING THE ENGINE
    # The architecture is just a blueprint. We must compile it into C++/CUDA.
    # Optimizer: Adam (The industry standard gradient descent algorithm).
    # Loss: Categorical Crossentropy (The mathematical penalty for classification errors).
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("Neural Network Architecture successfully compiled!")
    model.summary()
    
    # 6. TRAINING THE NETWORK
    print("\nTraining Phase (Forward Pass + Backpropagation):")
    # epochs=3: The network will look at the entire dataset 3 times.
    # batch_size=32: It updates its weights after every 32 images (Mini-Batch Gradient Descent).
    model.fit(X_train, y_train_encoded, epochs=3, batch_size=32, verbose=1)
    
    print("\nNetwork trained! (Accuracy is low because data is synthetic random noise).")


def run_all_labs():
    demonstrate_tensors()
    demonstrate_keras_network()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Neural Network require non-linear Activation Functions like ReLU?
   Answer: A Dense (Fully Connected) layer performs a strictly linear mathematical operation: $Y = WX + B$. If you stack 5 Dense layers on top of each other without an activation function, the mathematics completely collapses into a single linear equation. The network would be absolutely incapable of learning complex, non-linear patterns (like the curved shape of a dog's ear). An activation function like ReLU (`if x < 0: return 0, else: return x`) forcibly bends the math, allowing the network to approximate any continuous function in the universe (Universal Approximation Theorem).

2. What is the difference between `SparseCategoricalCrossentropy` and `CategoricalCrossentropy`?
   Answer: Both are Loss functions used for multi-class classification (e.g., predicting 10 different digit classes). 
   - You use **CategoricalCrossentropy** when your labels are One-Hot Encoded (e.g., `y = [0, 0, 1, 0, 0]`). 
   - You use **SparseCategoricalCrossentropy** when your labels are raw integers (e.g., `y = 2`). The "Sparse" version automatically handles the conversion under the hood, saving massive amounts of RAM when dealing with thousands of classes (like translating a vocabulary of 50,000 words).

3. What exactly is an "Epoch" versus a "Batch"?
   Answer: 
   - A **Batch** is a subset of the data (e.g., 32 images). The GPU processes 32 images simultaneously, calculates the average error, and adjusts the network's weights exactly once. 
   - An **Epoch** occurs when the network has seen the *entire dataset* exactly one time. If you have 3,200 images and a Batch Size of 32, it will take 100 weight updates (steps) to complete 1 Epoch. You usually train a network for multiple Epochs so it can repeatedly study the data until the loss converges.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: TensorFlow & Keras Foundations Completed.")
