"""
# ==============================================================================
# LABORATORY: DEEP UNSUPERVISED LEARNING (AUTOENCODERS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# What if you want to compress an image? PCA is a great dimensionality reduction 
# algorithm, but it is strictly linear. Deep Learning can compress data 
# non-linearly using an Autoencoder.
#
# An Autoencoder is a Neural Network trained to literally copy its Input to its 
# Output. However, there is a catch: the middle of the network has a severe 
# "Bottleneck" layer (e.g., squashing 784 pixels down to 32 neurons).
#
# Because the data MUST pass through this 32-neuron bottleneck (the "Latent Space"), 
# the network is forced to learn extremely efficient compression algorithms.
#
# 1. ENCODER: Compresses the 784D image into a dense 32D Latent Vector.
# 2. DECODER: Uncompresses the 32D Latent Vector back into a 784D image.
#
# This is the foundational architecture behind modern Generative AI (Variational 
# Autoencoders) and Image Denoising!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Encoder/Decoder Latent Space architecture.
# - Construct an Autoencoder in Keras.
# - Understand how Autoencoders can be used to mathematically remove noise from images.
#
# ==============================================================================
"""

import numpy as np
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# In a real environment: pip install tensorflow
try:
    import tensorflow as tf
    from tensorflow.keras.models import Model, Sequential
    from tensorflow.keras.layers import Dense, Input
    HAS_TF = True
except ImportError:
    HAS_TF = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. BUILDING AN AUTOENCODER (KERAS FUNCTIONAL API)
# ==============================================================================
def demonstrate_autoencoder():
    section_header("The Autoencoder Architecture")
    
    if not HAS_TF:
        print("[WARNING] TensorFlow not installed.")
        return
        
    print("We will build an Autoencoder to compress 784-pixel images down ")
    print("to a 32-dimensional Latent Vector, and then reconstruct them.\n")
    
    # 1. SYNTHETIC DATA
    # 1000 images, each 784 pixels (Flattened 28x28)
    X_train = np.random.rand(1000, 784).astype('float32')
    
    # 2. THE ENCODER
    # We use the Keras Functional API (Not Sequential) because we want to be able 
    # to slice the network in half later!
    
    input_img = Input(shape=(784,))
    # Compress 784 -> 128
    encoded = Dense(128, activation='relu')(input_img)
    # Compress 128 -> 32 (THE BOTTLENECK / LATENT SPACE)
    latent_space = Dense(32, activation='relu')(encoded)
    
    # 3. THE DECODER
    # Decompress 32 -> 128
    decoded = Dense(128, activation='relu')(latent_space)
    # Decompress 128 -> 784 (Reconstruction!)
    # Sigmoid ensures output pixels are strictly between [0.0, 1.0]
    output_img = Dense(784, activation='sigmoid')(decoded)
    
    # 4. THE FULL AUTOENCODER MODEL
    # Input is the raw image. Output is the reconstructed image.
    autoencoder = Model(inputs=input_img, outputs=output_img)
    
    # 5. COMPILE
    # Loss is Mean Squared Error (We want the output pixels to perfectly match the input pixels)
    autoencoder.compile(optimizer='adam', loss='mse')
    
    print("Autoencoder Architecture Compiled!")
    autoencoder.summary()
    
    print("\nNotice how the data squeezes from 784 -> 128 -> 32 -> 128 -> 784.")
    
    # 6. TRAINING (UNSUPERVISED)
    # Notice that X is BOTH the input AND the target! We have no `y` labels!
    print("\nTraining Phase (Input = Target):")
    autoencoder.fit(
        X_train, X_train, # <--- The Magic
        epochs=3, 
        batch_size=256,
        verbose=1
    )
    
    print("\nAutoencoder trained! It has successfully learned how to compress.")


# ==============================================================================
# 4. ISOLATING THE ENCODER
# ==============================================================================
def demonstrate_encoder_isolation():
    section_header("Extracting the Latent Space")
    
    if not HAS_TF: return
    
    print("Once trained, you can chop the Autoencoder in half!")
    print("You can extract just the Encoder part to use as a massive data compressor.")
    print("You feed it a 784D image, and it outputs a 32D vector (96% compression)!\n")
    
    # (Rebuilding quickly for isolation demonstration)
    input_img = Input(shape=(784,))
    latent_space = Dense(32, activation='relu')(input_img) # Simple 1-layer encoder
    output_img = Dense(784, activation='sigmoid')(latent_space)
    
    # The Full Model
    autoencoder = Model(input_img, output_img)
    
    # THE ISOLATED ENCODER MODEL
    # We define a new model that starts at the input and STOPS at the Latent Space!
    encoder_only = Model(input_img, latent_space)
    
    # Generate 1 single test image
    test_image = np.random.rand(1, 784).astype('float32')
    
    # Pass it through the Encoder
    compressed_image = encoder_only.predict(test_image, verbose=0)
    
    print(f"Original Image Shape: {test_image.shape}")
    print(f"Compressed Vector Shape: {compressed_image.shape}")
    print("\nYou can now store millions of images as tiny 32D vectors in a database, ")
    print("and use Cosine Similarity to find 'visually similar' images instantly!")


def run_all_labs():
    demonstrate_autoencoder()
    demonstrate_encoder_isolation()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. How does an Autoencoder differ from PCA for Dimensionality Reduction?
   Answer: PCA calculates orthogonal Eigenvectors to find a linear projection of maximum variance. Because it is linear algebra, PCA can only capture linear relationships. An Autoencoder uses deep, non-linear neural networks (with Activation Functions like ReLU). This allows the Autoencoder to learn highly complex, non-linear manifolds and compress data far more efficiently than PCA ever could.

2. What is a "Denoising Autoencoder"?
   Answer: Standard Autoencoders map $X_{clean} \rightarrow X_{clean}$. A Denoising Autoencoder maps $X_{dirty} \rightarrow X_{clean}$. You take a dataset of crisp, high-quality images. You artificially inject Gaussian static (noise) to create corrupted versions. During training, you feed the corrupted image into the Input, but you set the Loss function target to be the original, clean image. Because the noisy static is completely random, it cannot fit through the tiny Latent Space bottleneck. The network is forced to mathematically ignore the noise and only pass through the core "concepts" of the image. The Decoder then reconstructs a perfectly crisp image from those concepts!

3. Why do we isolate the Encoder model after training?
   Answer: In production applications (like Google Images reverse search), you do not want to compare massive 10-Megabyte images to each other pixel-by-pixel (it would take days). You isolate the Encoder, run your entire image library through it, and save the resulting tiny 32-Dimensional vectors (Embeddings) to a database. When a user uploads a new image, you pass it through the Encoder to get a 32D vector, and instantly calculate the vector distance against the database to find mathematically identical images in milliseconds.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Autoencoders Completed.")
