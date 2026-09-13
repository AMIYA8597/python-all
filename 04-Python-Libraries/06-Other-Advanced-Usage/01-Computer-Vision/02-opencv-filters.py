"""
# ==============================================================================
# LABORATORY: ADVANCED IMAGE FILTERS & EDGE DETECTION (OPENCV)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Real-world images are noisy. If you take a photo of a license plate at night, 
# the image is covered in static (digital noise). If you feed that raw image 
# into an Optical Character Recognition (OCR) model, the static will completely 
# destroy the model's ability to read the letters.
#
# You must mathematically clean the image before inference.
# 
# 1. Blurring (Convolutions): A mathematical operation that slides a small 
#    matrix (a Kernel) over the image to average out local pixels, literally 
#    melting away static noise while preserving the large structures.
# 2. Edge Detection: Calculating the mathematical derivative of the pixels to 
#    find sudden jumps in brightness, allowing you to physically extract the 
#    geometric outlines of objects!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the math of Convolution Kernels.
# - Execute Gaussian and Median Blurring to destroy noise.
# - Execute Canny Edge Detection and Sobel Derivatives.
# - Execute Image Thresholding (Binarization).
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
# 3. BLURRING & DENOISING (CONVOLUTIONS)
# ==============================================================================
def demonstrate_blurring():
    section_header("Mathematical Blurring (Convolutions)")
    
    if not HAS_CV2:
        print("[WARNING] OpenCV not installed.")
        return
        
    print("We will generate a synthetic grayscale image covered in random static (Salt & Pepper noise).")
    
    # Generate 500x500 gray image
    image = np.ones((500, 500), dtype=np.uint8) * 127
    
    # Inject 5,000 random white and black noise pixels!
    for _ in range(5000):
        x, y = np.random.randint(0, 500, 2)
        image[x, y] = np.random.choice([0, 255])
        
    print("Image successfully corrupted with static noise.")
    
    # 1. GAUSSIAN BLUR
    # A Gaussian Kernel applies a weighted average. The center pixel is given the 
    # most weight, and neighboring pixels are given exponentially less weight.
    # (15, 15) is the Kernel Size. It must be an odd number!
    gaussian_blur = cv2.GaussianBlur(image, (15, 15), 0)
    
    # 2. MEDIAN BLUR (The Ultimate Noise Killer)
    # Instead of taking the Average, it looks at the 5x5 grid and takes the Median!
    # Because static noise is usually extreme (0 or 255), it is ALWAYS at the edges 
    # of the sorted list, meaning the Median mathematically deletes it perfectly!
    median_blur = cv2.medianBlur(image, 5)
    
    print("\nApplied Gaussian Blur (Smoothes image, but smears the noise).")
    print("Applied Median Blur (Mathematically obliterates the noise without smearing).")


# ==============================================================================
# 4. EDGE DETECTION (CALCULUS DERIVATIVES)
# ==============================================================================
def demonstrate_edge_detection():
    section_header("Edge Detection (Sobel & Canny)")
    
    if not HAS_CV2: return
    
    print("How does a self-driving car see the lane lines?")
    print("It calculates the mathematical derivative (the rate of change) of the pixels.")
    print("When the dark asphalt suddenly hits the bright white painted line, the ")
    print("pixel value jumps from 30 to 255. The derivative spikes massively!\n")
    
    # Synthetic image of a white square on a black background
    image = np.zeros((500, 500), dtype=np.uint8)
    image[100:400, 100:400] = 255
    
    # 1. SOBEL DERIVATIVE
    # Calculates the gradient in the X direction (vertical edges) and Y direction (horizontal edges)
    # We use cv2.CV_64F to prevent negative derivatives from wrapping around to 255!
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
    
    # 2. CANNY EDGE DETECTOR (The Industry Standard)
    # Canny is a highly advanced multi-stage algorithm:
    #   Step 1: Applies Gaussian Blur to kill noise.
    #   Step 2: Applies Sobel to find the intensity gradients.
    #   Step 3: Non-Maximum Suppression (Thins the edges down to exactly 1 pixel).
    #   Step 4: Hysteresis Thresholding (Connects broken lines).
    
    # Parameters 50 and 150 are the lower and upper Hysteresis thresholds.
    edges = cv2.Canny(image, 50, 150)
    
    print(f"Canny successfully extracted the exact geometric wireframe: {edges.shape}")
    print("If plotted, 'edges' would look like a 1-pixel thin white outline of a square.")


# ==============================================================================
# 5. THRESHOLDING (BINARIZATION)
# ==============================================================================
def demonstrate_thresholding():
    section_header("Thresholding (Binarization for OCR)")
    
    if not HAS_CV2: return
    
    print("Before feeding a scanned document into Tesseract OCR, you must ")
    print("Binarize it. Every pixel must become strictly Pure Black (0) or Pure White (255).\n")
    
    # Synthetic image of a "scanned document" with bad, uneven lighting
    # Gradient background from 0 to 255
    image = np.tile(np.linspace(0, 255, 500, dtype=np.uint8), (500, 1))
    
    # 1. GLOBAL THRESHOLDING
    # If pixel > 127, it becomes 255. Else, it becomes 0.
    # Problem: If the document has a shadow on the left side, the shadow will 
    # turn completely black and swallow the text!
    ret, thresh_global = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    # 2. ADAPTIVE THRESHOLDING (The OCR Savior)
    # Instead of using a global 127, it looks at a small 11x11 grid around EACH 
    # pixel. It calculates the local average lighting for that tiny area, and 
    # thresholds based on the local shadow! This perfectly extracts text from shadows.
    thresh_adaptive = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    print("Executed Global Thresholding.")
    print("Executed Adaptive Thresholding (Perfect for shadowed documents).")


def run_all_labs():
    demonstrate_blurring()
    demonstrate_edge_detection()
    demonstrate_thresholding()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is a Convolution Kernel, and why must its size (e.g., `(5, 5)`) always be an odd number?
   Answer: A Convolution Kernel is a tiny mathematical matrix that slides across the image. At every stop, it multiplies its values against the image pixels beneath it and sums the result to generate a brand new central pixel. The Kernel size MUST be an odd number (like $3 \times 3$, $5 \times 5$, or $15 \times 15$) because the math requires a true, absolute "Center" pixel. An even matrix like $4 \times 4$ does not have a single central pixel, making it geometrically impossible to map the calculated average back to a specific (x, y) coordinate.

2. Why is `cv2.medianBlur` vastly superior to `cv2.GaussianBlur` for removing "Salt and Pepper" static noise?
   Answer: A Gaussian Blur calculates a weighted average. If a $5 \times 5$ grid contains mostly dark gray pixels (value 50), but one pixel is a bright white static anomaly (value 255), the average of that grid will be heavily skewed upward. The blur will turn the single white dot into an ugly, smeared white smudge. A Median Blur takes all 25 pixels, sorts them numerically, and physically discards the extremes, selecting the exact middle value. Because the static noise (255) is an extreme outlier, it is pushed to the edge of the sorted list and mathematically deleted from existence, leaving the image perfectly sharp and noise-free.

3. Why do we apply Gaussian Blur *before* running the Canny Edge Detection algorithm?
   Answer: The Canny Edge Detector relies on the Sobel operator, which calculates the mathematical derivative (the rate of change) between neighboring pixels. Static noise (a random white pixel next to a random black pixel) represents an infinite rate of change, causing a massive derivative spike. If you run Canny on a noisy image, it will detect thousands of microscopic, fake "edges" around every single piece of static, completely masking the true edges of the object. Applying a Gaussian Blur melts away the high-frequency static noise, leaving only the massive, low-frequency structural edges for the derivative calculus to find.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: OpenCV Filters & Edge Detection Completed.")
