"""
# ==============================================================================
# LABORATORY: DEEP LEARNING (COMPUTER VISION & CNNS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to build an Image Classifier using standard Linear 
# Layers (Dense Networks). They flatten a 1024x1024 RGB image into a single 
# 1D array of 3,145,728 pixels. They connect this to a hidden layer of 1,000 
# neurons. The resulting weight matrix contains 3 Billion parameters. The GPU 
# violently runs out of memory, and the model completely destroys the spatial 
# 2D relationship of the pixels (a nose is no longer above a mouth).
#
# A senior AI engineer understands Convolutional Neural Networks (CNNs). They 
# use a 3x3 Convolutional Kernel. Instead of 3 Billion parameters, the Kernel 
# mathematically contains exactly 9 parameters. It slides across the 2D image, 
# mathematically extracting edges, textures, and spatial hierarchies regardless 
# of where they appear in the image (Translation Invariance). The model trains 
# flawlessly on a 4GB GPU and achieves 99% accuracy.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Convolutional Mathematics (Kernels & Strides).
# - Execute Spatial Compression (Max Pooling).
# - Architect Transfer Learning (ResNet / Pre-trained weights).
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CONVOLUTIONAL KERNEL)
# ==============================================================================
class ComputerVisionSimulator:
    
    @staticmethod
    def execute_convolution():
        """
        [SECURE] Mathematical Convolution (Edge Detection).
        We simulate sliding a 3x3 filter over a 5x5 image matrix.
        """
        print("  [INIT] Simulating 2D Convolution on an Image...")
        
        # A 5x5 Grayscale Image (0 = Black, 10 = White)
        # Notice there is a bright vertical line of 10s in the middle!
        image = np.array([
            [0, 0, 10, 0, 0],
            [0, 0, 10, 0, 0],
            [0, 0, 10, 0, 0],
            [0, 0, 10, 0, 0],
            [0, 0, 10, 0, 0]
        ])
        
        # A 3x3 Vertical Edge Detection Kernel
        # This kernel mathematically subtracts the left pixels from the right pixels!
        kernel = np.array([
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ])
        
        print("\n  [IMAGE TENSOR (5x5)]")
        print(image)
        
        print("\n  [CONVOLUTION KERNEL (3x3)] - Vertical Edge Detector")
        print(kernel)
        
        # Simulate the sliding window! (Assuming Stride=1, No Padding)
        # Output shape will be (5-3+1) x (5-3+1) = 3x3
        output = np.zeros((3, 3))
        
        print("\n  [EXECUTION] Sliding the Kernel across the Image...")
        for row in range(3):
            for col in range(3):
                # Extract the 3x3 chunk of the image
                chunk = image[row:row+3, col:col+3]
                
                # Mathematical Convolution: Element-wise multiplication, then SUM!
                dot_product = np.sum(chunk * kernel)
                output[row, col] = dot_product
                
        print("\n  [FEATURE MAP (3x3)]")
        print(output)
        
        print("\n  -> [MATHEMATICAL PROOF] The Kernel successfully detected the bright ")
        print("     vertical edge, returning massive positive values (30) exactly where ")
        print("     the transition from Black (0) to White (10) occurred!")


    # --------------------------------------------------------------------------
    # THE ARCHITECTURAL PATTERN: TRANSFER LEARNING
    # --------------------------------------------------------------------------
    @staticmethod
    def execute_transfer_learning():
        """
        [SECURE] Transfer Learning Architecture.
        """
        print("\n  [INIT] Architecting Transfer Learning (ResNet50)...")
        print("  -> Downloading pre-trained ResNet50 (trained on 14 Million ImageNet photos).")
        print("  -> Freezing the Convolutional Base (requires_grad = False).")
        print("  -> Slicing off the final 1000-class fully-connected layer.")
        print("  -> Attaching a new 2-class layer (Cats vs Dogs).")
        print("  -> Training ONLY the final layer on our 500 images.")
        
        print("\n  [FLAWLESS] We mathematically leveraged Google's $50,000 GPU training ")
        print("  budget to extract edges/textures perfectly. We achieved 99% accuracy ")
        print("  on our Cats vs Dogs dataset in just 45 seconds of training.")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_cv():
    section_header("Computer Vision: Convolutional Neural Networks")
    
    sim = ComputerVisionSimulator()
    sim.execute_convolution()
    sim.execute_transfer_learning()


def run_all_labs():
    demonstrate_cv()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is 'Translation Invariance' in a Convolutional Neural Network (CNN), and why do Dense (Linear) Networks fail at it?"
   Senior Answer: "Spatial Independence. If you train a Dense Linear Network to recognize a cat, and the cat is always in the center of the image, the network assigns massive Weights specifically to the pixels in the exact center of the $1D$ flattened array. If you show it an image where the cat is in the top-left corner, it completely fails because those specific center weights multiply against background pixels (Zero). A CNN achieves Translation Invariance by using a single $3 \\times 3$ Kernel that mathematically slides across the entire image. If it learns the mathematical pattern of a 'Cat Ear', it will successfully trigger that Kernel regardless of whether the ear is in the center, top-left, or bottom-right."

2. Interviewer: "What is the mathematical purpose of a Max Pooling layer?"
   Senior Answer: "Dimensionality Compression and Spatial Hierarchy. A Convolutional layer extracts high-resolution features. If we process a $224 \\times 224$ image with $64$ filters, we generate massive amounts of data. A Max Pooling layer (e.g., $2 \\times 2$ window, Stride $2$) slides across the Feature Map and mathematically selects only the absolute maximum value in that $4$-pixel window, discarding the other $3$. This compresses the Tensor from $224 \\times 224$ down to $112 \\times 112$, destroying exactly $75\\%$ of the computational overhead while retaining the most dominant mathematical features. It forces the network to look at the 'Bigger Picture'."

3. Interviewer: "Explain the architecture of Transfer Learning. Why do we 'freeze' the base layers?"
   Senior Answer: "Gradient Conservation. When you download a model like ResNet50, the early Convolutional layers have already perfectly learned the universal mathematics of visual reality (edges, curves, gradients, textures) by looking at $14$ Million images. If you do not 'freeze' these layers (`requires_grad=False`), your tiny new dataset of $500$ medical X-Rays will send massive, erratic Calculus gradients backward through the entire network, violently destroying the perfect weights ResNet already learned (Catastrophic Forgetting). By freezing the base, we mathematically protect the universal feature extractors and solely train a brand new Linear Classifier at the very end of the network."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Deep Learning (Computer Vision) Completed.")
