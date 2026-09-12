"""
OpenCV Image Filtering and Convolutions (cv2)

This module provides a textbook-grade, interactive lesson on image filtering 
using OpenCV and NumPy. Image filtering is fundamental in Computer Vision (CV),
serving as the backbone for noise reduction, feature extraction (like edge detection), 
and image enhancement.

Mathematical Background:
------------------------
1. Convolution:
   The core operation in linear image filtering is 2D convolution (or cross-correlation).
   Given an image I and a kernel (or mask) K of size (2N+1) x (2N+1), the filtered
   image F at pixel (x, y) is computed as:

   F(x, y) = sum_{i=-N}^{N} sum_{j=-N}^{N} I(x+i, y+j) * K(i, j)

2. Gaussian Blur:
   A Gaussian filter is used for blurring images and removing noise. The weights 
   in the kernel are calculated using the 2D Gaussian function:
   G(x, y) = (1 / (2 * pi * sigma^2)) * e^(-(x^2 + y^2) / (2 * sigma^2))
   where sigma is the standard deviation.

3. Sobel Edge Detection:
   Sobel operators use 3x3 kernels to approximate the derivatives of the image 
   intensity in the x and y directions.
   Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]] * I
   Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]] * I
   Magnitude = sqrt(Gx^2 + Gy^2)

Big-O Analysis:
---------------
- Time Complexity: O(W * H * K_W * K_H)
  where (W, H) are the dimensions of the image, and (K_W, K_H) are the dimensions
  of the filter kernel. For separable kernels (like Gaussian and Sobel), the complexity
  can be reduced to O(W * H * (K_W + K_H)) by applying 1D filters successively.
- Space Complexity: O(W * H)
  To store the resulting filtered image of the same spatial dimensions.

Real-World Applications:
------------------------
1. Pre-processing: Removing noise (Gaussian, Median) before feeding images into neural networks.
2. Edge Detection: Extracting shapes for object recognition, lane detection in autonomous vehicles.
3. Image Sharpening: Enhancing medical imagery (X-rays, MRIs) for clearer diagnostics.
4. Morphological Operations: Cleaning up binary masks in background subtraction or segmentation tasks.
"""

import cv2
import numpy as np
import time
from typing import Tuple, Optional, Any

def create_synthetic_image(width: int = 400, height: int = 400) -> np.ndarray:
    """
    Creates a synthetic grayscale image containing distinct geometric shapes 
    and added Gaussian noise for testing filters.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.

    Returns:
        np.ndarray: A 2D numpy array representing the synthetic noisy image.
    """
    # Create a blank black image
    img = np.zeros((height, width), dtype=np.uint8)

    # Draw geometric shapes to create sharp edges
    cv2.rectangle(img, (50, 50), (150, 150), 255, -1)
    cv2.circle(img, (300, 100), 50, 200, -1)
    cv2.fillPoly(img, [np.array([[200, 250], [150, 350], [250, 350]])], 150)

    # Add Gaussian noise
    mean = 0
    stddev = 25
    noise = np.random.normal(mean, stddev, img.shape).astype(np.int16)
    
    # Add noise to image and clip values to valid uint8 range [0, 255]
    noisy_img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    return noisy_img

def apply_blurring_filters(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Demonstrates various blurring techniques in OpenCV.
    
    Blurring (Smoothing) is heavily used to remove high-frequency noise from images.

    Args:
        image (np.ndarray): The input grayscale or BGR image.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: A tuple containing results of 
        Mean Blur, Gaussian Blur, and Median Blur respectively.
    """
    print("Applying Blurring Filters...")
    
    # 1. Mean Blur (Averaging)
    # The kernel is a normalized box filter.
    # It takes the average of all pixels under the kernel area.
    # Complexity: O(W*H) typically implemented using integral images for speed.
    mean_blurred = cv2.blur(image, (5, 5))

    # 2. Gaussian Blur
    # Highly effective at removing Gaussian noise.
    # The (5, 5) is the kernel size (must be odd).
    # The third parameter (0) is sigmaX; if 0, it is computed from the kernel size.
    gaussian_blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # 3. Median Blur
    # Replaces the central pixel with the median of all pixels under the kernel area.
    # Highly effective against "salt and pepper" noise.
    # Preserves edges much better than mean or Gaussian blurring.
    median_blurred = cv2.medianBlur(image, 5)

    return mean_blurred, gaussian_blurred, median_blurred

def apply_edge_detection(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Demonstrates edge detection techniques using Sobel and Canny.

    Edge detection identifies points in a digital image at which the image 
    brightness changes sharply.

    Args:
        image (np.ndarray): The input grayscale image.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]: Sobel X, Sobel Y, and Canny Edge outputs.
    """
    print("Applying Edge Detection...")
    
    # It is standard practice to blur the image before edge detection to prevent
    # false edges caused by noise.
    blurred = cv2.GaussianBlur(image, (3, 3), 0)

    # 1. Sobel X
    # Computes horizontal gradients (vertical edges).
    # ddepth=cv2.CV_64F is used to avoid overflow when calculating derivatives.
    sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_x_abs = cv2.convertScaleAbs(sobel_x)

    # 2. Sobel Y
    # Computes vertical gradients (horizontal edges).
    sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_y_abs = cv2.convertScaleAbs(sobel_y)

    # 3. Canny Edge Detection
    # A multi-stage algorithm:
    #   a. Noise reduction (Gaussian)
    #   b. Gradient calculation (Sobel)
    #   c. Non-maximum suppression (thinning edges)
    #   d. Hysteresis thresholding (linking edges based on thresholds)
    # Thresholds: 50 (lower) and 150 (upper).
    canny_edges = cv2.Canny(blurred, 50, 150)

    return sobel_x_abs, sobel_y_abs, canny_edges

def apply_custom_kernel(image: np.ndarray) -> np.ndarray:
    """
    Applies a custom convolution kernel to the image.
    Here we demonstrate a sharpening filter.

    Sharpening works by emphasizing the differences between a pixel and its neighbors.

    Args:
        image (np.ndarray): The input image.

    Returns:
        np.ndarray: The sharpened image.
    """
    print("Applying Custom Sharpening Kernel...")
    
    # Define a 3x3 sharpening kernel
    # Center weight is positive and strong, surrounding weights are negative.
    # Sum of weights is 1, which maintains overall image brightness.
    kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)

    # cv2.filter2D applies an arbitrary linear filter (convolution).
    # ddepth=-1 means the output image will have the same depth as the source.
    sharpened = cv2.filter2D(image, -1, kernel)

    return sharpened

def apply_morphological_operations(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies morphological transformations: Erosion and Dilation.
    
    These operations process images based on shapes. They are usually performed on 
    binary images (like masks or edges).

    Args:
        image (np.ndarray): The input image (will be binarized first).

    Returns:
        Tuple[np.ndarray, np.ndarray]: Eroded and Dilated images.
    """
    print("Applying Morphological Operations...")
    
    # Threshold the image to create a binary mask
    _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    # Create a structuring element (kernel)
    kernel = np.ones((5, 5), np.uint8)

    # 1. Erosion
    # Shrinks the bright regions (foreground).
    # A pixel in the original image will be considered 1 only if all the pixels 
    # under the kernel are 1, otherwise it is eroded (made to zero).
    eroded = cv2.erode(binary, kernel, iterations=1)

    # 2. Dilation
    # Expands the bright regions (foreground).
    # A pixel element is '1' if at least one pixel under the kernel is '1'.
    dilated = cv2.dilate(binary, kernel, iterations=1)

    return eroded, dilated

def performance_benchmark() -> None:
    """
    Measures the execution time of different filter operations to illustrate
    the real-world performance implications (Big-O in practice).
    """
    print("\n--- Performance Benchmarking ---")
    large_image = np.random.randint(0, 256, (2000, 2000), dtype=np.uint8)
    
    operations = {
        "Mean Blur (5x5)": lambda img: cv2.blur(img, (5, 5)),
        "Gaussian Blur (5x5)": lambda img: cv2.GaussianBlur(img, (5, 5), 0),
        "Gaussian Blur (21x21)": lambda img: cv2.GaussianBlur(img, (21, 21), 0),
        "Median Blur (5x5)": lambda img: cv2.medianBlur(img, 5),
        "Sobel Edge X (3x3)": lambda img: cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3),
    }

    for name, func in operations.items():
        start_time = time.perf_counter()
        func(large_image)
        end_time = time.perf_counter()
        elapsed = (end_time - start_time) * 1000 # milliseconds
        print(f"{name:25s} : {elapsed:.2f} ms")

def run_tests() -> None:
    """
    Automated test suite to ensure the filter functions execute correctly and
    return arrays of the correct shape and type.
    """
    print("\n--- Running Tests ---")
    test_img = create_synthetic_image(100, 100)
    
    # Test Blurring
    mean_b, gaussian_b, median_b = apply_blurring_filters(test_img)
    assert mean_b.shape == test_img.shape, "Mean blur shape mismatch"
    assert gaussian_b.dtype == np.uint8, "Gaussian blur dtype mismatch"
    
    # Test Edge Detection
    sobel_x, sobel_y, canny = apply_edge_detection(test_img)
    assert sobel_x.shape == test_img.shape, "Sobel shape mismatch"
    assert canny.max() > 0, "Canny found no edges in synthetic image"
    
    # Test Custom Filter
    sharpened = apply_custom_kernel(test_img)
    assert sharpened.shape == test_img.shape, "Sharpening shape mismatch"
    
    # Test Morphological
    eroded, dilated = apply_morphological_operations(test_img)
    # Using logical check to handle the case where the image may have been uniform
    assert np.array_equal(np.unique(eroded), [0, 255]) or len(np.unique(eroded)) <= 2, "Erosion not strictly binary"
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    print("=" * 60)
    print("OpenCV Filters and Convolutions Interactive Lesson")
    print("=" * 60)

    # 1. Generate Synthetic Data
    image = create_synthetic_image()
    print("Synthetic noisy image generated (400x400).")

    # 2. Apply Filters
    mean_b, gaussian_b, median_b = apply_blurring_filters(image)
    sobel_x, sobel_y, canny_edges = apply_edge_detection(image)
    sharpened = apply_custom_kernel(median_b)  # Best to sharpen a noise-reduced image
    eroded, dilated = apply_morphological_operations(image)
    
    # 3. Performance Benchmark
    performance_benchmark()

    # 4. Run Test Suite
    run_tests()

    print("\n=" * 60)
    print("Lesson Complete. In a GUI environment, you could use cv2.imshow()")
    print("to visualize the resultant images.")
    print("=" * 60)
