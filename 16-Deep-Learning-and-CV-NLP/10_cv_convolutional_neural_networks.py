"""
# ==============================================================================
# LABORATORY: COMPUTER VISION (CNN ARCHITECTURES & MATHEMATICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to design a Convolutional Neural Network (CNN) from 
# scratch. They pass a 224x224 image through 10 Convolutional Layers with no 
# Padding. By layer 10, the spatial dimension of the image mathematically 
# shrinks to 0x0. The network violently crashes during the forward pass.
#
# A senior AI engineer understands "Tensor Mathematics". They calculate the exact 
# output shape of every Convolutional layer using the formula: 
# Output = [ (Input - FilterSize + (2 * Padding)) / Stride ] + 1
# They intentionally use `Padding=1` and `Stride=1` to perfectly preserve the 
# 224x224 dimension during convolution, and then strategically use Max Pooling 
# to mathematically halve the dimensions (112x112 -> 56x56 -> 28x28).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Output Shape Mathematical Formula.
# - Execute Convolution + Padding + Stride simulations.
# - Architect spatial compression via Max Pooling.
#
# ==============================================================================
"""

import math

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (TENSOR MATHEMATICS)
# ==============================================================================
class CNNSimulator:
    
    @staticmethod
    def calculate_output_shape(input_size: int, filter_size: int, padding: int, stride: int) -> int:
        """
        [SECURE] The universal mathematical formula for CNN spatial dimensions.
        Calculates the Width (or Height) of the output Tensor.
        """
        output = ((input_size - filter_size + (2 * padding)) / stride) + 1
        return math.floor(output)

    def simulate_vgg16_architecture(self):
        """
        [SECURE] Simulating the exact mathematical tensor flow of VGG16.
        VGG16 processes 224x224 RGB images using strict 3x3 Kernels and 2x2 Max Pooling.
        """
        print("  [INIT] Architecting VGG16 Tensor Flow...")
        
        # Initial Image (Channels, Height, Width)
        channels, height, width = 3, 224, 224
        print(f"\n  [INPUT] Original Image Shape: ({channels}, {height}, {width})")
        
        # ---------------------------------------------------------
        # BLOCK 1: Convolution -> Convolution -> Max Pooling
        # ---------------------------------------------------------
        print("\n  [BLOCK 1]")
        
        # Conv 1: 64 Filters, 3x3 Kernel, Padding=1, Stride=1
        new_height = self.calculate_output_shape(height, filter_size=3, padding=1, stride=1)
        new_width = self.calculate_output_shape(width, filter_size=3, padding=1, stride=1)
        channels = 64
        print(f"  -> Conv1 (64 Filters, 3x3, P=1, S=1): Shape = ({channels}, {new_height}, {new_width})")
        
        # Conv 2: 64 Filters, 3x3 Kernel, Padding=1, Stride=1
        new_height = self.calculate_output_shape(new_height, filter_size=3, padding=1, stride=1)
        new_width = self.calculate_output_shape(new_width, filter_size=3, padding=1, stride=1)
        print(f"  -> Conv2 (64 Filters, 3x3, P=1, S=1): Shape = ({channels}, {new_height}, {new_width})")
        
        # Max Pooling: 2x2 Kernel, Stride=2, Padding=0
        new_height = self.calculate_output_shape(new_height, filter_size=2, padding=0, stride=2)
        new_width = self.calculate_output_shape(new_width, filter_size=2, padding=0, stride=2)
        print(f"  -> MaxPool (2x2, S=2):                Shape = ({channels}, {new_height}, {new_width})")
        
        print("  -> Notice how Padding=1 completely protected the 224x224 dimension ")
        print("     during Convolution, and MaxPool perfectly halved it to 112x112.")
        
        # ---------------------------------------------------------
        # BLOCK 2: Convolution -> Convolution -> Max Pooling
        # ---------------------------------------------------------
        print("\n  [BLOCK 2]")
        channels = 128
        new_height = self.calculate_output_shape(new_height, filter_size=3, padding=1, stride=1)
        new_width = self.calculate_output_shape(new_width, filter_size=3, padding=1, stride=1)
        print(f"  -> Conv3 (128 Filters, 3x3, P=1):     Shape = ({channels}, {new_height}, {new_width})")
        
        new_height = self.calculate_output_shape(new_height, filter_size=3, padding=1, stride=1)
        new_width = self.calculate_output_shape(new_width, filter_size=3, padding=1, stride=1)
        print(f"  -> Conv4 (128 Filters, 3x3, P=1):     Shape = ({channels}, {new_height}, {new_width})")
        
        new_height = self.calculate_output_shape(new_height, filter_size=2, padding=0, stride=2)
        new_width = self.calculate_output_shape(new_width, filter_size=2, padding=0, stride=2)
        print(f"  -> MaxPool (2x2, S=2):                Shape = ({channels}, {new_height}, {new_width})")
        
        print("\n  [FLAWLESS] The architectural pattern is clear. As the spatial ")
        print("  resolution drops (224 -> 112 -> 56), the mathematical depth ")
        print("  of the feature maps dramatically expands (3 -> 64 -> 128).")


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_cnn_architecture():
    section_header("Computer Vision: CNN Architectures")
    
    sim = CNNSimulator()
    sim.simulate_vgg16_architecture()


def run_all_labs():
    demonstrate_cnn_architecture()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the mathematical purpose of 'Padding=1' when using a 3x3 Convolutional Filter?"
   Senior Answer: "Boundary Preservation. When a 3x3 filter slides across an image without padding (Valid Convolution), the center of the filter can never mathematically reach the outermost border pixels. Because of this, a 224x224 image will physically shrink to 222x222 after just one pass. If you have 50 layers, the image rapidly shrinks to 0x0. By mathematically wrapping the image in a 1-pixel border of zeros ('Padding=1'), the 3x3 filter can perfectly align its center with the edge pixels. The output shape mathematically remains 224x224 (Same Convolution)."

2. Interviewer: "What is the 'Receptive Field' of a Convolutional Neuron?"
   Senior Answer: "The Spatial Horizon. A single neuron in Layer 1 (using a 3x3 filter) mathematically 'sees' a 3x3 patch of the original image. A single neuron in Layer 2 (also using a 3x3 filter) looks at a 3x3 patch of Layer 1. But because each of *those* pixels in Layer 1 was calculated from a 3x3 patch of the original image, the single neuron in Layer 2 actually has a 'Receptive Field' of 5x5 relative to the original image! As you go deeper into the network, the Receptive Field expands exponentially. By Layer 20, a single mathematical pixel in the feature map contains the aggregated information of the entire 224x224 original image."

3. Interviewer: "How did the ResNet (Residual Network) architecture solve the Vanishing Gradient problem for ultra-deep 150-layer CNNs?"
   Senior Answer: "Identity Skip Connections. In a standard VGG architecture, the mathematical Calculus gradient must flow backwards through 150 consecutive layers of Matrix Multiplications and ReLUs. As proven in RNNs, repeated multiplication causes the gradient to vanish to zero. ResNet introduced an architectural bypass: $H(x) = F(x) + x$. The input tensor ($x$) physically bypasses the Convolutional block and is mathematically ADDED directly to the output. Because the derivative of Addition is exactly $1.0$, this creates an unobstructed 'Gradient Superhighway' that allows the error signal to flow backwards from Layer 150 to Layer 1 perfectly intact."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CV (CNN Architectures) Completed.")
