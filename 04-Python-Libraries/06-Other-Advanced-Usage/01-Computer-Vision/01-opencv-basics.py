"""
# ==============================================================================
# LABORATORY: COMPUTER VISION FOUNDATIONS (OPENCV)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Deep Learning CNNs (like ResNet) are incredible at classifying images. But 
# before you can feed a 4K video from a drone into a Neural Network, you must 
# mathematically process the pixels.
#
# You must crop the image, resize it, convert it to grayscale to save VRAM, 
# and perhaps isolate specific colors (like extracting only red traffic cones).
#
# OpenCV (Open Source Computer Vision Library) is the undisputed industry standard. 
# It is an ultra-fast C++ library with Python bindings. When you load an image 
# using OpenCV, it is immediately converted into a highly optimized NumPy array, 
# allowing you to mathematically manipulate millions of pixels in milliseconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand how images are represented mathematically (NumPy Matrices).
# - Master Color Spaces (BGR, RGB, Grayscale, HSV).
# - Execute geometric transformations (Resizing, Cropping).
#
# ==============================================================================
"""

import numpy as np
import os

# In a real environment: pip install opencv-python
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IMAGES AS NUMPY MATRICES
# ==============================================================================
def demonstrate_image_matrices():
    section_header("Images as Mathematical Matrices")
    
    if not HAS_CV2:
        print("[WARNING] OpenCV not installed. Install via: pip install opencv-python")
        return
        
    print("An image is literally just a giant grid of numbers.")
    print("Each pixel is represented by a number from 0 (Black) to 255 (White).\n")
    
    # 1. Create a pure black synthetic image (Grayscale)
    # Shape: 100 rows (Height) x 200 columns (Width)
    black_image = np.zeros((100, 200), dtype=np.uint8)
    
    print(f"Image Shape: {black_image.shape}")
    print(f"Data Type  : {black_image.dtype} (Unsigned Integer 8-bit)")
    
    # 2. Modify the pixels directly using NumPy slicing!
    # Let's draw a white square in the middle by setting pixels to 255
    black_image[25:75, 75:125] = 255
    
    print("\nSuccessfully manipulated raw pixels to draw a square.")
    print("In a real script, you would display it using:")
    print("  cv2.imshow('Image', black_image)")
    print("  cv2.waitKey(0)")
    
    # 3. Saving the image to disk
    temp_filename = "synthetic_square.jpg"
    cv2.imwrite(temp_filename, black_image)
    print(f"Image saved to disk as {temp_filename}")
    
    # Cleanup
    if os.path.exists(temp_filename):
        os.remove(temp_filename)


# ==============================================================================
# 4. COLOR SPACES (BGR VS RGB VS HSV)
# ==============================================================================
def demonstrate_color_spaces():
    section_header("Color Spaces (The BGR Trap)")
    
    if not HAS_CV2: return
    
    print("Most Python libraries (Matplotlib, PIL) use the RGB standard (Red, Green, Blue).")
    print("OpenCV was created in 1999 when digital cameras used the BGR standard!")
    print("If you load an image in OpenCV and plot it in Matplotlib without converting, ")
    print("the Blue and Red channels will swap, making human skin look like a blue alien!\n")
    
    # Create a synthetic COLOR image (Height, Width, 3 Channels)
    # 100x100 pixels, 3 color channels (B, G, R)
    bgr_image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    # Let's paint the entire image pure Red.
    # In BGR, channel 0 is Blue, channel 1 is Green, channel 2 is Red.
    bgr_image[:, :, 2] = 255 
    
    # 1. CONVERTING BGR TO RGB
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    
    # 2. CONVERTING TO GRAYSCALE
    # Deep Learning models (like MNIST) often use Grayscale to cut the tensor 
    # math by 66% (3 channels down to 1 channel).
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    
    print(f"Color Image Shape: {bgr_image.shape}")
    print(f"Grayscale Shape  : {gray_image.shape}\n")
    
    print("--- The HSV Color Space ---")
    print("RGB mixes colors using light. It is terrible for Object Tracking.")
    print("If a red ball moves into a shadow, its R, G, and B values all change drastically!")
    
    print("HSV (Hue, Saturation, Value) separates the physical Color (Hue) from ")
    print("the lighting (Value). In HSV, the red ball remains exactly the same ")
    print("Hue even in pitch black shadows!")
    
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    print("Successfully converted to HSV for robust color tracking.")


# ==============================================================================
# 5. GEOMETRIC TRANSFORMATIONS (RESIZING & CROPPING)
# ==============================================================================
def demonstrate_geometry():
    section_header("Geometric Transformations")
    
    if not HAS_CV2: return
    
    print("Neural Networks have fixed input sizes (e.g., ResNet requires 224x224).")
    print("You must resize 4K images down to 224x224 before inference.\n")
    
    # Synthetic 4K image (3840 x 2160)
    image_4k = np.zeros((2160, 3840, 3), dtype=np.uint8)
    print(f"Original Shape: {image_4k.shape}")
    
    # 1. RESIZING
    # Notice the syntax trap! OpenCV expects (Width, Height) for resizing, 
    # but NumPy returns (Height, Width) from .shape!
    resized_image = cv2.resize(image_4k, (224, 224))
    print(f"Resized for CNN: {resized_image.shape} (Note: Aspect ratio was destroyed!)")
    
    # 2. CROPPING
    # Cropping doesn't require an OpenCV function! Because the image is a NumPy 
    # array, you just use standard Python slice notation.
    # We want a 500x500 box from the top left corner:
    cropped_image = image_4k[0:500, 0:500]
    print(f"Cropped ROI    : {cropped_image.shape}")


def run_all_labs():
    demonstrate_image_matrices()
    demonstrate_color_spaces()
    demonstrate_geometry()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why must images be cast to `numpy.uint8` instead of standard `float64`?
   Answer: Memory efficiency and hardware standards. A standard uncompressed 1080p RGB image has roughly 6.2 million individual values. If you store these as 64-bit floats (which take 8 bytes each), a single image consumes 50 Megabytes of RAM. `uint8` stands for Unsigned Integer 8-bit. An 8-bit integer takes exactly 1 byte and can represent exactly 256 unique values ($2^8$), perfectly capturing the standard 0-255 pixel intensity scale. This drops the memory footprint to just 6.2 Megabytes per image, allowing you to load massive batches into GPU VRAM for deep learning.

2. A teammate loads an image using `cv2.imread()`, passes it into a PyTorch model, and the model completely fails to identify the object. What is the most likely bug?
   Answer: The BGR Trap. Standard Pre-Trained Deep Learning models (like those on PyTorch Hub or Hugging Face) are trained on datasets loaded with PIL or Matplotlib, which natively use the RGB color space. OpenCV `imread()` natively loads images in the legacy BGR color space. If you pass a BGR tensor into an RGB-trained Neural Network, the Red and Blue channels are physically swapped. The network will see the world in completely distorted alien colors, causing catastrophic classification failure. You MUST call `cv2.cvtColor(image, cv2.COLOR_BGR2RGB)` before passing the tensor to PyTorch.

3. Why is the HSV color space vastly superior to RGB for Computer Vision tasks like "Tracking a yellow tennis ball"?
   Answer: RGB is a combinatorial color space based on mixing light. If a yellow tennis ball rolls from bright sunlight into the shadow of a tree, its absolute Red, Green, and Blue pixel values will all drop drastically. An RGB threshold filter will instantly lose track of the ball. HSV separates the structural components of light. `Hue` represents the actual wavelength (the pure physical color), `Saturation` represents the intensity, and `Value` represents the brightness. When the ball rolls into the shadow, the `Value` drops, but the `Hue` remains mathematically identical! You can track the ball flawlessly by filtering purely on the `Hue` channel, rendering the tracking algorithm completely immune to dynamic lighting changes.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: OpenCV Computer Vision Basics Completed.")
