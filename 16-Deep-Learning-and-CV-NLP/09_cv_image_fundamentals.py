"""
Computer Vision Fundamentals
Applying Convolution kernels to a dummy image using NumPy.
"""

import numpy as np

def apply_2d_convolution(image, kernel):
    """
    Applies a 2D convolution (cross-correlation) without padding (Valid mode).
    """
    img_h, img_w = image.shape
    kernel_h, kernel_w = kernel.shape
    
    # Calculate output dimensions
    out_h = img_h - kernel_h + 1
    out_w = img_w - kernel_w + 1
    
    output = np.zeros((out_h, out_w))
    
    # Slide the kernel over the image
    for i in range(out_h):
        for j in range(out_w):
            # Extract the region of interest
            region = image[i:i+kernel_h, j:j+kernel_w]
            # Element-wise multiplication and sum
            output[i, j] = np.sum(region * kernel)
            
    return output

if __name__ == "__main__":
    # Create a 6x6 dummy grayscale image
    # Imagine a vertical edge in the middle: left side is 10 (dark), right is 200 (light)
    image = np.array([
        [10, 10, 10, 200, 200, 200],
        [10, 10, 10, 200, 200, 200],
        [10, 10, 10, 200, 200, 200],
        [10, 10, 10, 200, 200, 200],
        [10, 10, 10, 200, 200, 200],
        [10, 10, 10, 200, 200, 200],
    ])
    
    print("Original Image:")
    print(image)
    
    # Vertical Edge Detection Kernel (Sobel-like)
    vertical_kernel = np.array([
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ])
    
    print("\nVertical Edge Kernel:")
    print(vertical_kernel)
    
    # Apply convolution
    filtered_image = apply_2d_convolution(image, vertical_kernel)
    
    print("\nFiltered Image (Feature Map):")
    # Notice the high values exactly where the vertical edge occurs in the middle
    print(filtered_image)
