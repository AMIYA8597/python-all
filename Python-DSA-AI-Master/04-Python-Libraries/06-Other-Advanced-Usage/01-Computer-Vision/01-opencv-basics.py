"""
## A. Concept Name
Computer Vision Basics with OpenCV

## B. One-Sentence Definition
OpenCV (Open Source Computer Vision Library) is a powerful, highly optimized library designed for real-time image processing, computer vision, and machine learning tasks.

## C. Why Does This Exist?
Images are fundamentally multi-dimensional matrices of numbers (pixels). OpenCV exists to provide a lightning-fast, C++ backed standard library for reading, manipulating, and analyzing these pixel matrices so you don't have to write raw array-looping algorithms from scratch.

## D. Intuition
Think of an image as an Excel spreadsheet. A grayscale image is a 2D spreadsheet where each cell contains a brightness value (0=black, 255=white). A color image is just three spreadsheets stacked on top of each other (Blue, Green, Red). OpenCV gives you tools to crop, filter, transform, and search through these spreadsheets efficiently.

## E. Real-Life Analogy
If NumPy is a scientific calculator for arrays, OpenCV is Photoshop for code. It provides all the filters, transformations, and layers, but you control them programmatically.

## F. Mental Model
1. **Load**: Disk -> RAM (NumPy Array in BGR format)
2. **Preprocess**: Resize, Grayscale, Blur, Normalize
3. **Analyze**: Edge Detection, Feature Extraction, Thresholding
4. **Act/Output**: Draw bounding boxes, save to disk, or feed into a Deep Learning model.

## G. Visual Explanation
Color Image Shape: `(Height, Width, Channels)`
e.g., a 1080p image is `(1080, 1920, 3)`

Coordinate System:
(0,0) ------> X (Width)
  |
  |
  v
  Y (Height)
*Note: This is inverted from standard math graphs where Y goes up.*

## H. Formal Explanation
OpenCV bridges image acquisition and machine learning. It provides implementations for image gradients (Sobel), morphological operations (erosion/dilation), geometric transformations (affine/perspective), and color space conversions. It uses NumPy as its core data structure in Python, making it highly interoperable with data science ecosystems.

## I. Mathematical Foundation
- **Grayscale conversion**: $Y = 0.299 R + 0.587 G + 0.114 B$
- **Convolution (Blur/Edges)**: An image is convolved with a Kernel (a small matrix).
  $G[i,j] = \sum_{u} \sum_{v} K[u,v] I[i-u, j-v]$

## J. Basic Implementation
See `basic_image_io()` below.

## K. Intermediate Implementation
See `image_processing_pipeline()` below.

## L. Advanced Implementation
See `edge_detection_and_contours()` below.

## M. Complexity
- **Time Complexity**: Most pixel-wise operations are $O(W \times H)$, where W is width and H is height.
- **Space Complexity**: $O(W \times H \times C)$, memory scales linearly with pixels and channels.

## N. Common Mistakes
- Forgetting that `cv2.imread()` loads images in **BGR** format, not **RGB**.
- Trying to display an image with matplotlib without converting BGR to RGB first.
- Modifying arrays using Python `for` loops instead of vectorized OpenCV/NumPy functions (which causes massive slowdowns).

## O. Common Confusions
- **(x, y) vs (row, col)**: OpenCV points like `(x, y)` map to NumPy indices as `array[y, x]`.

## P. When To Use
- Image preprocessing before feeding into a CNN (PyTorch/TensorFlow).
- Real-time video processing (webcam streams).
- Object tracking and simple face detection (Haar cascades).

## Q. When NOT To Use
- For high-level Deep Learning (use PyTorch/TF).
- When a simple web image manipulation is needed (Pillow/PIL is often easier).

## R. Trade-offs
- **Speed vs Pythonic Syntax**: OpenCV is extremely fast but sometimes has unintuitive C-style APIs compared to scikit-image.

## S. Debugging
- `cv2.imshow("Debug", img); cv2.waitKey(0)` is your print statement for computer vision.

## T. Memory Hook
"BGR and Y-down" -> Always remember OpenCV reads Blue-Green-Red, and Y=0 is at the top of the image.

## U. Active Recall
- How do you convert a color image to grayscale?
- Why are nested loops bad in OpenCV?

## V. Practice
- Load an image, crop the top-right quarter, convert it to grayscale, and save it.

## W. Interview Question
- "Why does OpenCV use BGR instead of RGB?"
  *Answer*: Historical reasons. Early camera manufacturers and Windows bitmap formats used BGR.

## X. Project Connection
OpenCV is the prerequisite for all major Computer Vision projects in this repository (Facial Recognition, Autonomous Driving lines, YOLO Object Detection pre-processing).
"""

import cv2
import numpy as np
import os
import sys

def create_synthetic_image(height=400, width=400):
    """
    Creates a synthetic image (NumPy array) for testing purposes
    so we don't rely on an external image file.
    """
    # Create a black image (H, W, 3) with uint8 type
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Draw a blue rectangle
    # cv2.rectangle(img, pt1(x,y), pt2(x,y), color(B,G,R), thickness)
    cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), -1)
    
    # Draw a green circle
    cv2.circle(img, (300, 100), 50, (0, 255, 0), -1)
    
    # Draw a red line
    cv2.line(img, (50, 300), (350, 300), (0, 0, 255), 5)
    
    return img

def basic_image_io():
    """
    Demonstrates basic Image I/O and properties.
    """
    print("--- Basic Image Operations ---")
    img = create_synthetic_image()
    
    # 1. Properties
    print(f"Shape: {img.shape} -> (Height: {img.shape[0]}, Width: {img.shape[1]}, Channels: {img.shape[2]})")
    print(f"Data type: {img.dtype}")
    print(f"Memory size: {img.size} bytes")
    
    # 2. Saving an image
    cv2.imwrite("synthetic_test.jpg", img)
    print("Saved image to 'synthetic_test.jpg'")
    
    # 3. Reading an image
    loaded_img = cv2.imread("synthetic_test.jpg")
    if loaded_img is None:
        print("Error: Could not load image.")
    else:
        print("Successfully loaded image from disk.")
    
    # Cleanup
    if os.path.exists("synthetic_test.jpg"):
        os.remove("synthetic_test.jpg")

def image_processing_pipeline():
    """
    Demonstrates a standard pre-processing pipeline for ML.
    """
    print("\n--- Intermediate: Processing Pipeline ---")
    img = create_synthetic_image()
    
    # 1. Resize (often needed to fit model input sizes like 224x224)
    resized = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    print(f"Resized shape: {resized.shape}")
    
    # 2. Convert to Grayscale (reduces dimensionality from 3 to 1)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    print(f"Grayscale shape: {gray.shape}")
    
    # 3. Gaussian Blur (removes high-frequency noise)
    # The kernel (5x5) defines how much to blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 4. Normalization (Scaling pixel values from 0-255 to 0.0-1.0)
    # Critical for Neural Networks
    normalized = blurred.astype("float32") / 255.0
    print(f"Normalized range: Min={normalized.min()}, Max={normalized.max()}")

def edge_detection_and_contours():
    """
    Demonstrates advanced feature extraction using Canny Edge Detection
    and Contour finding.
    """
    print("\n--- Advanced: Edge Detection & Contours ---")
    img = create_synthetic_image()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Canny Edge Detection
    # Uses gradient thresholding to find boundaries
    edges = cv2.Canny(gray, threshold1=100, threshold2=200)
    print(f"Edges detected (non-zero pixels): {cv2.countNonZero(edges)}")
    
    # 2. Find Contours
    # RETR_EXTERNAL retrieves only the extreme outer contours
    # CHAIN_APPROX_SIMPLE compresses horizontal/vertical/diagonal segments
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    print(f"Found {len(contours)} external contours.")
    
    # 3. Draw contours on a copy of the original image
    result_img = img.copy()
    cv2.drawContours(result_img, contours, -1, (0, 255, 255), 2)
    print("Drew contours on result image.")

def deliberate_bug_exercise():
    """
    Deliberately broken code to teach debugging OpenCV.
    """
    print("\n--- Debugging Exercise ---")
    print("Look at the code in `deliberate_bug_exercise()`.")
    print("Task: Try to modify a pixel using a slow double for-loop.")
    
    img = create_synthetic_image(100, 100)
    
    # BUG/ANTI-PATTERN: Never do this in production OpenCV
    # Modifying pixels in Python loops is incredibly slow.
    """
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            img[y, x] = [255, 255, 255] # Setting to white
    """
    
    # THE FIX: Use NumPy vectorization or broadcasting
    img[:, :] = [255, 255, 255]
    print("Fixed slow pixel iteration by using NumPy slicing: img[:, :] = [255, 255, 255]")

if __name__ == "__main__":
    basic_image_io()
    image_processing_pipeline()
    edge_detection_and_contours()
    deliberate_bug_exercise()
    print("\nOpenCV Basics Module Executed Successfully.")
