"""
# ==============================================================================
# LABORATORY: COMPUTER VISION (IMAGE FUNDAMENTALS & TENSORS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer loads a 1920x1080 JPEG image using standard Python libraries, 
# resulting in a massive list of lists. They feed this directly into a PyTorch 
# model. The GPU violently crashes with an `InvalidShapeException`.
#
# A senior AI engineer understands the rigid mathematical shape of Image Tensors. 
# They know that OpenCV loads images as (Height x Width x Channels) in BGR format, 
# but PyTorch strictly requires (Channels x Height x Width) in RGB format. They 
# mathematically transpose the dimensions, normalize the pixel values from 0-255 
# down to 0.0-1.0 using Floating Point division, and push the perfectly formatted 
# Tensor to the GPU in 0.01 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Image Tensor Dimensionality (HWC vs CHW).
# - Execute RGB Channel extraction and manipulation.
# - Architect Data Normalization and basic Matrix Filtering.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (TENSOR SHAPE MANIPULATION)
# ==============================================================================
class CVFundamentalsSimulator:
    
    @staticmethod
    def simulate_image_loading_and_conversion():
        """
        [SECURE] Simulating the conversion from OpenCV format to PyTorch format.
        """
        print("  [INIT] Simulating OpenCV Image Load (H x W x C)...")
        
        # A tiny 2x2 Image with 3 Color Channels (Red, Green, Blue)
        # Shape: (Height=2, Width=2, Channels=3)
        # Pixels range from 0 to 255
        np.random.seed(42)
        opencv_image = np.random.randint(0, 256, size=(2, 2, 3), dtype=np.uint8)
        
        print(f"\n  [SHAPE: OpenCV / NumPy]")
        print(f"  -> {opencv_image.shape} (Height, Width, Channels)")
        
        print("\n  [EXECUTION] Converting to PyTorch Format (C x H x W)...")
        # In Numpy, we use `transpose` or `np.moveaxis` to physically reorder the dimensions
        # Old axes: (0=Height, 1=Width, 2=Channels)
        # New axes: (2=Channels, 0=Height, 1=Width)
        pytorch_image = np.transpose(opencv_image, (2, 0, 1))
        
        print(f"  [SHAPE: PyTorch Tensor]")
        print(f"  -> {pytorch_image.shape} (Channels, Height, Width)")
        
        print("\n  [EXECUTION] Normalizing Pixel Values (0-255 -> 0.0-1.0)...")
        # Neural Networks mathematically require small floating point numbers.
        # If we feed it 255, the Gradients will violently explode!
        normalized_tensor = pytorch_image.astype(np.float32) / 255.0
        
        print(f"  -> [FLAWLESS] Tensor successfully normalized. Max value is now {np.max(normalized_tensor):.2f}")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: IMAGE FILTERING
    # --------------------------------------------------------------------------
    @staticmethod
    def simulate_image_filtering():
        """
        [SECURE] Applying a basic mathematical filter to an image matrix.
        """
        print("\n  [INIT] Simulating a Grayscale Image Matrix (3x3)...")
        
        # 0 = Black, 255 = White
        image = np.array([
            [10, 10, 10],
            [10, 250, 10], # Bright white pixel in the center!
            [10, 10, 10]
        ], dtype=np.float32)
        
        print("  -> Original Image:")
        print(image)
        
        print("\n  [EXECUTION] Applying a 'Mean Blur' Filter (Smoothing)...")
        
        # A 3x3 filter where every value is 1/9. 
        # When multiplied against the image, it averages out the bright center pixel.
        blur_kernel = np.array([
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9],
            [1/9, 1/9, 1/9]
        ])
        
        # Matrix convolution simulation
        blurred_pixel = np.sum(image * blur_kernel)
        
        print(f"  -> The center pixel was 250.")
        print(f"  -> After mathematical convolution, the center pixel is now: {blurred_pixel:.2f}")
        print("  -> [FLAWLESS] The image was successfully blurred mathematically.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_cv_fundamentals():
    section_header("Computer Vision: Image Fundamentals")
    
    sim = CVFundamentalsSimulator()
    sim.simulate_image_loading_and_conversion()
    sim.simulate_image_filtering()


def run_all_labs():
    demonstrate_cv_fundamentals()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does PyTorch mandate the `(Channels, Height, Width)` tensor format instead of the standard OpenCV `(Height, Width, Channels)` format?"
   Senior Answer: "Memory Contiguity and GPU Optimization. When a GPU performs massive parallel Convolutional operations, it mathematically scans across the 2D spatial dimensions (Height and Width) of a single color channel at a time. By placing the 'Channels' dimension first (`CHW`), PyTorch mathematically guarantees that all the pixels for the 'Red' channel are stored in a perfectly contiguous block of VRAM. The GPU can blast through this contiguous memory via C++ pointers with zero Cache Misses. If the memory was `HWC`, the GPU would have to constantly jump over the Green and Blue bytes in RAM to process the Red pixels, destroying memory bandwidth."

2. Interviewer: "Why must we strictly normalize Image pixels from $0-255$ to $0.0-1.0$ before feeding them into a Neural Network?"
   Senior Answer: "Gradient Explosion and Activation Saturation. If you feed the raw integer $255$ into a Neural Network, it will hit a Dense layer and be multiplied by a weight. The resulting massive scalar will be pushed into an Activation Function (like Sigmoid or Tanh). A Sigmoid of $255$ instantly evaluates to $1.0$, completely saturating the mathematical limit of the function. The derivative of a saturated Sigmoid is exactly $0.0$. The gradient vanishes on the very first forward pass, and the network is mathematically paralyzed forever. Normalizing to $0.0-1.0$ keeps the input within the healthy, steep region of the activation functions."

3. Interviewer: "What is 'Data Augmentation', and why is it architecturally critical for Computer Vision models?"
   Senior Answer: "Mathematical Regularization against Overfitting. Deep CNNs contain millions of parameters and are prone to perfectly memorizing the exact pixel configuration of the training set. If you train a model to detect 'Cars', but every car in your dataset is facing Left, the model will fail in production if a car is facing Right. Data Augmentation dynamically applies mathematical transformations (Random Rotations, Horizontal Flips, Color Jitter, Zooming) to the images inside the DataLoader pipeline *while* they are being sent to the GPU. This artificially generates infinite variations of the dataset, forcing the network to learn the universal geometric structure of a 'Car', rather than memorizing the exact pixels."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CV (Fundamentals) Completed.")
