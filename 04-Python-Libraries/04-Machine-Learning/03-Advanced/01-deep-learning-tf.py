"""
# ==============================================================================
# LABORATORY: ADVANCED DEEP LEARNING (CNNs & CALLBACKS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Dense Neural Network (Multi-Layer Perceptron) connects every single 
# input pixel to every single neuron in the first layer. If you have a 1080p 
# colored image, the first layer alone would require 6.2 Million weights per neuron.
# The network would require Exabytes of RAM and would instantly overfit.
#
# To process images, we use Convolutional Neural Networks (CNNs).
# Instead of looking at the whole image at once, a CNN slides a small 3x3 "Filter" 
# across the image, mathematically scanning for specific geometric features 
# (edges, curves, corners). This requires 99.9% less RAM and achieves 
# state-of-the-art accuracy on Computer Vision tasks.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the math of Convolution (Conv2D) and Max Pooling.
# - Construct a Convolutional Neural Network (CNN) in Keras.
# - Master Keras Callbacks (EarlyStopping & ModelCheckpoint).
#
# ==============================================================================
"""

import numpy as np
import os

# Suppress annoying TensorFlow C++ logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# In a real environment: pip install tensorflow
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
    HAS_TF = True
except ImportError:
    HAS_TF = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CONVOLUTIONAL NEURAL NETWORKS (CNN)
# ==============================================================================
def demonstrate_cnn():
    section_header("Convolutional Neural Networks (Conv2D)")
    
    if not HAS_TF:
        print("[WARNING] TensorFlow not installed.")
        return
        
    print("A CNN uses mathematical 'Filters' to extract spatial features from images.")
    print("It then uses 'MaxPooling' to shrink the image, compressing the spatial ")
    print("information into high-level concepts (e.g. 'Is there a dog ear here?').\n")
    
    # 1. SYNTHETIC IMAGE DATA (100 color images, 64x64 pixels, 3 RGB channels)
    # Shape must be (batch, height, width, channels)
    X_train = np.random.rand(100, 64, 64, 3).astype('float32')
    y_train = np.random.randint(0, 2, 100) # Binary classification (Dog vs Cat)
    
    # 2. BUILD THE CNN ARCHITECTURE
    model = Sequential([
        # LAYER 1: Convolution
        # 32 filters, each 3x3 pixels. 
        # It scans the image and creates 32 new 'Feature Maps' highlighting edges.
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(64, 64, 3)),
        
        # LAYER 2: Max Pooling
        # Looks at 2x2 grids and keeps only the maximum value, shrinking the 
        # image size by exactly 50% (from 62x62 down to 31x31), saving massive RAM.
        MaxPooling2D(pool_size=(2, 2)),
        
        # LAYER 3: Second Convolution block (extracting deeper, complex features)
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        # LAYER 4: Flatten
        # The 2D feature maps must be flattened into a 1D vector before entering 
        # the final decision-making Dense layers.
        Flatten(),
        
        # LAYER 5: Dense + Dropout
        Dense(128, activation='relu'),
        # Dropout randomly turns off 50% of the neurons during training! 
        # This forces the network to learn robust features and prevents Overfitting!
        Dropout(0.5),
        
        # LAYER 6: Output
        # Binary classification requires 1 neuron with a Sigmoid activation.
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    print("CNN Architecture Successfully Compiled!")
    model.summary()


# ==============================================================================
# 4. KERAS CALLBACKS (EARLY STOPPING)
# ==============================================================================
def demonstrate_callbacks():
    section_header("Keras Callbacks (Automation during Training)")
    
    if not HAS_TF: return
    
    print("\nIf you tell the network to train for 500 Epochs, but it perfectly ")
    print("learns the data at Epoch 50, it will spend the next 450 Epochs ")
    print("catastrophically Overfitting. Callbacks automate this!")
    
    X_train = np.random.rand(100, 10)
    y_train = np.random.randint(0, 2, 100)
    X_val = np.random.rand(20, 10)
    y_val = np.random.randint(0, 2, 20)
    
    model = Sequential([
        Dense(32, activation='relu', input_shape=(10,)),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    
    # 1. EARLY STOPPING
    # Monitors the Validation Loss. If the Validation Loss stops improving for 
    # 5 consecutive epochs (patience=5), it completely halts the training process!
    early_stop = EarlyStopping(
        monitor='val_loss', 
        patience=5, 
        restore_best_weights=True # Automatically rolls back to the best version!
    )
    
    # 2. MODEL CHECKPOINT
    # Automatically saves the physical weights to the hard drive every time the 
    # model hits a new high score on the validation set.
    checkpoint = ModelCheckpoint(
        filepath='best_model.h5',
        monitor='val_loss',
        save_best_only=True
    )
    
    print("\nStarting Training with Callbacks...")
    # We pass the callbacks as a list!
    model.fit(
        X_train, y_train, 
        validation_data=(X_val, y_val),
        epochs=100, # We ask for 100, but EarlyStopping will likely halt it at ~10!
        callbacks=[early_stop, checkpoint],
        verbose=0 # Suppressing output for cleaner terminal
    )
    
    print("Training halted automatically by Early Stopping!")
    print("Best weights were successfully restored and saved to disk.")


def run_all_labs():
    demonstrate_cnn()
    demonstrate_callbacks()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why does a Convolutional Layer (`Conv2D`) use 99% fewer weights than a `Dense` layer when processing images?
   Answer: A Dense layer uses "Global Connectivity"—every input pixel connects to every neuron. An HD image has 2 million pixels, so a Dense layer with 100 neurons requires 200 million weights. A Conv2D layer uses "Parameter Sharing" and "Local Connectivity". It defines a single 3x3 filter (exactly 9 weights) and slides that exact same 9-weight filter across the entire 2-million-pixel image. It achieves state-of-the-art feature extraction using only 9 weights instead of 200 million!

2. What is the mathematical purpose of MaxPooling?
   Answer: Max Pooling reduces the spatial dimensions (Resolution) of the feature maps. By taking a 2x2 grid of pixels and keeping only the maximum value, it shrinks the image by 50% vertically and horizontally. This achieves two things: 1) It drastically reduces the RAM and computational power required for the next layers. 2) It introduces "Translation Invariance"—if a dog's ear shifts 1 pixel to the left in the original image, it will still fall into the same 2x2 pooling grid, meaning the output of the pooling layer remains mathematically identical. The network learns what a dog ear is, regardless of exactly where it is located.

3. Why is `restore_best_weights=True` critical when using the EarlyStopping callback?
   Answer: Early Stopping halts the training when the Validation Loss has degraded for $N$ consecutive epochs (the patience). This means the training actually stops *after* the model has already overfitted and gotten worse! If you don't use `restore_best_weights=True`, the model in RAM will retain the degraded, overfitted weights from the final epoch. With this flag set to True, Keras keeps a secret backup of the weights from the "peak" epoch and automatically rolls back to that perfect state before returning the model to you.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Deep Learning & CNNs Completed.")
