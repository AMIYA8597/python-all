"""
Module: 04-cv-advanced
Description: Comprehensive textbook-grade interactive lesson on Advanced Computer Vision (CV) in Python.

Learning Objectives:
1. Master advanced image processing techniques such as Feature Detection, Matching, and Optical Flow.
2. Understand mathematical foundations behind algorithms like Harris Corner Detection, SIFT/ORB, and Lucas-Kanade.
3. Implement Object Detection, Contour Analysis, and Image Segmentation using traditional CV methods.
4. Analyze Big-O time and space complexities for each algorithm.
5. Solve a real-world interview challenge focusing on object tracking and feature extraction.

Concept Explanation:
Advanced Computer Vision bridges the gap between simple image filtering and full-scale scene understanding. 
Before deep learning dominated, classic CV relied heavily on rigorous mathematical models of light, gradients, 
and pixel intensities. Mastering these foundations is essential because they are often more computationally 
efficient than deep learning models, require no training data, and are used extensively in SLAM (Simultaneous 
Localization and Mapping), medical imaging, and real-time edge devices.

Key Concepts:
- Feature Detection: Finding points of interest (corners, blobs) that are invariant to scaling, rotation, and illumination.
- Optical Flow: Estimating the motion of objects between consecutive frames caused by camera or object movement.
- Segmentation: Partitioning an image into multiple segments (sets of pixels) to simplify its representation.
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple, Union

try:
    import cv2
    import numpy as np
except ImportError:
    print("OpenCV or NumPy is missing. Please install via: pip install opencv-python numpy")
    sys.exit(1)


# =====================================================================
# 1. MATHEMATICAL BACKGROUND & BIG-O ANALYSIS
# =====================================================================
#
# Feature Detection (e.g., Harris Corner Detector)
# Mathematical Foundation:
# A corner is a point whose local neighborhood stands out in all directions.
# We consider the local auto-correlation function:
# E(u, v) = sum_{x,y} w(x,y) [I(x+u, y+v) - I(x, y)]^2
# Where w(x,y) is a window function (e.g., Gaussian), and I(x,y) is the image intensity.
# By Taylor expansion, this becomes a quadratic form involving the structure tensor M:
# M = [I_x^2   I_x I_y]
#     [I_x I_y I_y^2  ]
# The corner response function R is:
# R = det(M) - k * (trace(M))^2
#
# Big-O Analysis (Feature Detection on NxM image):
# - Gradients calculation: O(N * M)
# - Structure Tensor smoothing: O(N * M)
# - Corner response calculation: O(N * M)
# Overall Time Complexity: O(N * M)
# Overall Space Complexity: O(N * M) for gradient images and response maps.
#
# Optical Flow (Lucas-Kanade Method)
# Mathematical Foundation:
# Assumes brightness constancy and spatial coherence (neighboring pixels move similarly).
# I(x, y, t) = I(x+dx, y+dy, t+dt)
# By Taylor expansion: I_x * u + I_y * v + I_t = 0
# Solved via least squares for a window of pixels.
#
# Big-O Analysis (Lucas-Kanade):
# - Time: O(W^2 * K) where W is window size, K is number of keypoints.
# - Space: O(W^2) per keypoint for matrices.
# =====================================================================


def generate_synthetic_image(width: int = 512, height: int = 512) -> np.ndarray:
    """
    Generates a synthetic grayscale image containing basic geometric shapes 
    to be used for feature detection and segmentation demonstrations.
    
    Args:
        width (int): Image width.
        height (int): Image height.
        
    Returns:
        np.ndarray: A grayscale synthetic image.
    """
    image = np.zeros((height, width), dtype=np.uint8)
    
    # Add a rectangle
    cv2.rectangle(image, (50, 50), (200, 200), 255, -1)
    
    # Add a circle
    cv2.circle(image, (350, 150), 80, 150, -1)
    
    # Add a rotated triangle (polygon)
    pts = np.array([[100, 400], [250, 450], [150, 300]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(image, [pts], 200)
    
    # Add some noise to make it realistic
    noise = np.random.normal(0, 15, (height, width)).astype(np.uint8)
    image = cv2.add(image, noise)
    
    return image


def feature_detection_and_matching() -> None:
    """
    Demonstrates advanced feature detection using ORB (Oriented FAST and Rotated BRIEF).
    ORB is a fast robust local feature detector, an efficient alternative to SIFT/SURF.
    
    Time Complexity:
    - FAST corner detection: O(N) where N is number of pixels.
    - BRIEF descriptor extraction: O(K * P) where K is number of keypoints, P is patch size.
    Overall: Highly efficient, suitable for real-time applications.
    """
    print("--- 1. Feature Detection and Matching (ORB) ---")
    
    # Create an image and a slightly transformed version of it
    img1 = generate_synthetic_image()
    rows, cols = img1.shape
    # Rotate and translate img1 to create img2
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 15, 1) # 15 degrees rotation
    M[0, 2] += 20 # Translate X
    M[1, 2] -= 10 # Translate Y
    img2 = cv2.warpAffine(img1, M, (cols, rows))
    
    start_time = time.time()
    
    # Initialize ORB detector
    orb = cv2.ORB_create(nfeatures=500)
    
    # Find keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    
    if des1 is None or des2 is None:
        print("Failed to compute descriptors.")
        return

    # Use Brute-Force Matcher with Hamming distance (since ORB uses binary descriptors)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # Match descriptors
    matches = bf.match(des1, des2)
    
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)
    
    end_time = time.time()
    
    print(f"Detected {len(kp1)} keypoints in Image 1.")
    print(f"Detected {len(kp2)} keypoints in Image 2.")
    print(f"Found {len(matches)} matches.")
    if matches:
        print(f"Top 5 match distances: {[m.distance for m in matches[:5]]}")
    print(f"Execution time: {end_time - start_time:.4f} seconds\n")
    

def optical_flow_simulation() -> None:
    """
    Demonstrates Dense Optical Flow using the Farneback method.
    Unlike sparse optical flow (Lucas-Kanade) which only tracks specific keypoints,
    dense optical flow computes the motion vector for EVERY pixel.
    
    Mathematical concept (Farneback):
    Approximates the neighborhood of each pixel in two frames with quadratic polynomials.
    By observing how the polynomial coefficients change under translation, 
    the displacement field is computed.
    
    Time Complexity: O(N * I) where N is number of pixels, I is number of iterations.
    Space Complexity: O(N) to store optical flow vectors (u, v) for each pixel.
    """
    print("--- 2. Dense Optical Flow (Farneback) ---")
    
    # Create two synthetic frames simulating motion
    frame1 = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(frame1, (100, 100), 30, 255, -1)
    
    frame2 = np.zeros((200, 200), dtype=np.uint8)
    cv2.circle(frame2, (120, 110), 30, 255, -1) # Moved by (20, 10)
    
    start_time = time.time()
    
    # Calculate Dense Optical Flow using Gunnar Farneback's algorithm
    # flow is a 2D array of vectors: flow[..., 0] is the u-component (dx), flow[..., 1] is the v-component (dy)
    flow = cv2.calcOpticalFlowFarneback(
        prev=frame1, next=frame2, flow=None,
        pyr_scale=0.5, levels=3, winsize=15, 
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    
    end_time = time.time()
    
    # Analyze the resulting flow field
    # Extract flow vectors inside the object region (around the circle in frame1)
    mask = frame1 > 0
    u_flow = flow[..., 0][mask]
    v_flow = flow[..., 1][mask]
    
    mean_u = np.mean(u_flow)
    mean_v = np.mean(v_flow)
    
    print(f"Calculated Mean Motion Vector: dx = {mean_u:.2f}, dy = {mean_v:.2f}")
    print(f"Expected Motion Vector: dx = 20.00, dy = 10.00")
    print(f"Optical Flow computation time: {end_time - start_time:.4f} seconds\n")


def image_segmentation_watershed() -> None:
    """
    Demonstrates image segmentation using the Watershed algorithm.
    Watershed treats the image intensity as a topographic map, finding the 
    "catchment basins" and "watershed ridge lines".
    
    Time Complexity: O(N) or O(N log N) depending on the implementation (e.g., using priority queues).
    Space Complexity: O(N) for markers and distance transforms.
    """
    print("--- 3. Image Segmentation (Watershed) ---")
    
    # Create overlapping circles to simulate objects needing segmentation
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.circle(img, (120, 150), 60, (255, 255, 255), -1)
    cv2.circle(img, (180, 150), 60, (255, 255, 255), -1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Binarize
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 2. Noise removal (morphological opening)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # 3. Sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    
    # 4. Finding sure foreground area using Distance Transform
    # Distance transform calculates distance to the closest zero pixel for each pixel
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    
    # 5. Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    
    # 6. Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    
    # Mark the region of unknown with zero
    markers[unknown == 255] = 0
    
    # 7. Apply Watershed
    markers = cv2.watershed(img, markers)
    
    # Markers will be -1 at the boundaries
    boundaries = (markers == -1).sum()
    objects = ret - 1 # Subtract background component
    
    print(f"Segmented {objects} distinct object(s).")
    print(f"Identified {boundaries} boundary pixels using Watershed algorithm.")
    print("Watershed segmentation completed successfully.\n")


def contour_analysis() -> None:
    """
    Demonstrates contour detection and shape analysis (moments, area, perimeter).
    
    Mathematical background (Image Moments):
    Moments are weighted averages of image pixel intensities.
    M_{pq} = sum_x sum_y x^p y^q I(x, y)
    Centroid: (M_10 / M_00, M_01 / M_00)
    """
    print("--- 4. Contour Analysis & Shape Descriptors ---")
    
    image = np.zeros((300, 300), dtype=np.uint8)
    # Draw an L-shape polygon
    pts = np.array([[50, 50], [100, 50], [100, 200], [200, 200], [200, 250], [50, 250]], np.int32)
    cv2.fillPoly(image, [pts], 255)
    
    # Find contours
    # cv2.RETR_EXTERNAL: retrieves only the extreme outer contours
    # cv2.CHAIN_APPROX_SIMPLE: compresses horizontal, vertical, and diagonal segments
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No contours found.")
        return
        
    cnt = contours[0]
    
    # 1. Area and Perimeter
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    
    # 2. Moments & Centroid
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        cx, cy = 0, 0
        
    # 3. Convex Hull
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area if hull_area > 0 else 0
    
    print(f"Contour Area: {area}")
    print(f"Contour Perimeter: {perimeter:.2f}")
    print(f"Centroid: ({cx}, {cy})")
    print(f"Solidity (Area / Convex Hull Area): {solidity:.4f}")
    print("Contour analysis completed.\n")


def interview_challenge(video_frames: List[np.ndarray]) -> List[Tuple[int, int]]:
    """
    Common Interview Challenge: Motion Tracking Tracker
    
    Problem Statement:
    You are given a list of binary frames (video). In these frames, a single object 
    (represented by white pixels) is moving. 
    Write a function to return the trajectory (list of (x,y) centroids) of the object.
    
    Constraints:
    - Frames are same size binary NumPy arrays.
    - O(N * M) time complexity per frame where N, M are dimensions.
    
    Args:
        video_frames: List of 2D binary numpy arrays.
        
    Returns:
        List of tuples representing (x, y) centroid of the object in each frame.
    """
    print("--- 5. Interview Challenge: Object Trajectory Tracking ---")
    trajectory = []
    
    start_time = time.time()
    for idx, frame in enumerate(video_frames):
        # Calculate moments
        M = cv2.moments(frame)
        
        # Calculate centroid
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = -1, -1 # Object lost or not present
            
        trajectory.append((cX, cY))
        
    end_time = time.time()
    print(f"Processed {len(video_frames)} frames in {end_time - start_time:.4f} seconds.")
    return trajectory


def run_tests() -> None:
    """
    Rigorous test suite for the interview challenge and other utility functions.
    """
    print("--- 6. Running Test Cases ---")
    
    # Test Interview Challenge
    frames = []
    # Generate 5 frames with a moving square
    for i in range(5):
        frame = np.zeros((100, 100), dtype=np.uint8)
        # Square moves diagonally by 10 pixels each frame
        x, y = 10 + i * 10, 10 + i * 10
        cv2.rectangle(frame, (x, y), (x+10, y+10), 255, -1)
        frames.append(frame)
        
    trajectory = interview_challenge(frames)
    expected = [(15, 15), (25, 25), (35, 35), (45, 45), (55, 55)]
    
    try:
        assert trajectory == expected, f"Expected {expected}, got {trajectory}"
        print("Test Case 1 (Moving Object): PASSED")
        
        # Test Case 2: Empty frames
        empty_frames = [np.zeros((10, 10), dtype=np.uint8)] * 3
        traj2 = interview_challenge(empty_frames)
        assert traj2 == [(-1, -1)] * 3, f"Expected empty tracking, got {traj2}"
        print("Test Case 2 (Empty Frames): PASSED")
        
        print("All tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


if __name__ == "__main__":
    print("=================================================================")
    print("         PYTHON DSA MASTER - ADVANCED COMPUTER VISION            ")
    print("=================================================================\n")
    
    # 1. Feature Detection and Matching
    feature_detection_and_matching()
    
    # 2. Dense Optical Flow
    optical_flow_simulation()
    
    # 3. Image Segmentation (Watershed)
    image_segmentation_watershed()
    
    # 4. Contour Analysis
    contour_analysis()
    
    # 5. Interview Challenge & Tests
    run_tests()
    
    print("=================================================================")
    print("               END OF INTERACTIVE LESSON MODULE                  ")
    print("=================================================================\n")
