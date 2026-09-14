"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (COMPUTER VISION / OPENCV)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer is asked to write a program that detects human faces in 
# a video stream. They attempt to write a complex Python loop, iterating over 
# every pixel in the 1920x1080 matrix, manually analyzing RGB values. The 
# laptop melts, executing at 0.001 frames per second.
#
# A senior Computer Vision engineer installs `OpenCV`. They mathematically 
# understand that an image is simply a multi-dimensional NumPy C-array. They 
# convert the 3-channel RGB image to a 1-channel Grayscale array to collapse 
# the mathematical complexity by 66%. They deploy a pre-trained Haar Cascade 
# Classifier (a machine learning model) that utilizes C++ SIMD instructions to 
# mathematically scan the matrix in microseconds, achieving 60 frames per second.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Image Representation (The NumPy Matrix).
# - Master the mathematical necessity of Grayscale conversion.
# - Execute algorithmic object detection (Haar Cascades).
#
# ==============================================================================
"""

import urllib.request
import os

# Gracefully handle missing OpenCV dependency
try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. PREPARING THE ENVIRONMENT
# ==============================================================================
# We must download a mathematical model (Haar Cascade) and a test image!
CASCADE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
IMAGE_URL = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg"

CASCADE_FILE = "haarcascade_frontalface.xml"
IMAGE_FILE = "test_face.jpg"

def download_assets():
    if not os.path.exists(CASCADE_FILE):
        print("  [INIT] Downloading Haar Cascade Mathematical Model...")
        urllib.request.urlretrieve(CASCADE_URL, CASCADE_FILE)
    if not os.path.exists(IMAGE_FILE):
        print("  [INIT] Downloading Test Image...")
        urllib.request.urlretrieve(IMAGE_URL, IMAGE_FILE)


# ==============================================================================
# 4. COMPUTER VISION ALGORITHM
# ==============================================================================
def demonstrate_opencv_pipeline():
    section_header("The Mathematical Matrix: OpenCV Face Detection")
    
    if not HAS_CV2:
        print("  [ERROR] OpenCV is not installed.")
        print("  Run `pip install opencv-python numpy` to execute this lab.")
        return
        
    download_assets()
    
    # --- 1. MATRIX LOAD (The Extraction) ---
    print("\n  [PHASE 1: THE NUMPY MATRIX]")
    # OpenCV loads the image directly into C-memory as a NumPy array!
    image = cv2.imread(IMAGE_FILE)
    
    if image is None:
        print("  [ERROR] Failed to load image.")
        return
        
    height, width, channels = image.shape
    print(f"    -> Image loaded!")
    print(f"    -> Mathematical Dimensions: {width}x{height} pixels.")
    print(f"    -> Channels: {channels} (Blue, Green, Red).")
    print(f"    -> Memory Footprint: {image.nbytes:,} bytes.")


    # --- 2. GRAYSCALE OPTIMIZATION (The Transformation) ---
    print("\n  [PHASE 2: MATHEMATICAL OPTIMIZATION (GRAYSCALE)]")
    # A standard RGB image has 3 layers of mathematical complexity.
    # To find a face, the algorithm mathematically searches for contrasting edges 
    # (dark eyes vs light skin). Color is mathematically irrelevant and destroys CPU efficiency!
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    print(f"    -> Converted to Grayscale.")
    print(f"    -> New Dimensions: {gray_image.shape} (The 3 channels collapsed to 1).")
    print(f"    -> New Memory Footprint: {gray_image.nbytes:,} bytes (66% reduction!).")


    # --- 3. THE MACHINE LEARNING ALGORITHM (The Detection) ---
    print("\n  [PHASE 3: HAAR CASCADE ALGORITHM]")
    # We load the pre-trained C++ mathematical model!
    face_cascade = cv2.CascadeClassifier(CASCADE_FILE)
    
    # The algorithm rapidly scans the Grayscale matrix!
    # scaleFactor: Downscales the image mathematically by 10% each pass to find faces of different sizes.
    # minNeighbors: A mathematical threshold to prevent false positives.
    faces = face_cascade.detectMultiScale(
        gray_image, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )
    
    print(f"    -> The Algorithm detected {len(faces)} face(s) in the matrix!")


    # --- 4. DRAWING THE BOUNDING BOXES (The Visualization) ---
    print("\n  [PHASE 4: BOUNDING BOX INJECTION]")
    # `faces` is a mathematical array of coordinates: (x, y, width, height)
    for (x, y, w, h) in faces:
        print(f"    -> Drawing Rectangle at X:{x} Y:{y} (Width:{w} Height:{h})")
        # We mathematically alter the original RGB matrix, turning specific pixels Green!
        # (Image, Start Coordinate, End Coordinate, BGR Color, Thickness)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    print("\n  [SUCCESS] Mathematical Pipeline Complete.")
    
    # We save the altered matrix back to the hard drive!
    output_file = "detected_faces.jpg"
    cv2.imwrite(output_file, image)
    print(f"  -> Check your directory for '{output_file}' to see the result!")


def run_all_labs():
    demonstrate_opencv_pipeline()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why does OpenCV load images in BGR format instead of the industry-standard RGB format?"
   Senior Answer: "Historical legacy. When OpenCV was initially architected in $1999$ by Intel, the dominant camera manufacturers and hardware graphic interfaces (like Windows GDI) mathematically stored uncompressed pixel data in Memory as Blue-Green-Red (BGR). OpenCV adopted this C-level memory alignment to prevent the CPU from executing an expensive matrix-swapping operation on every single frame captured from a live webcam. While modern web browsers and Deep Learning models (like PyTorch) strictly enforce RGB, OpenCV has retained BGR to preserve backwards compatibility across its billions of deployed C++ library functions."

2. Interviewer: "Why is converting a video stream to Grayscale mathematically mandatory before feeding it into a Haar Cascade or Edge Detection algorithm?"
   Senior Answer: "Computational bandwidth. An RGB $1920 \\times 1080$ frame contains exactly $6,220,800$ individual bytes of mathematical data per frame. At $60$ frames per second, the CPU must process $373$ Megabytes of data every second. Algorithms like Haar Cascades or Canny Edge Detection do not care if a car is red or blue; they mathematically search for rapid changes in pixel intensity (Luminance) to detect boundaries. By converting the matrix to Grayscale, we mathematically average the RGB channels (`0.299*R + 0.587*G + 0.114*B`), collapsing the 3-channel matrix into a single 1-channel matrix. This instantly destroys $66\\%$ of the data payload, dropping the CPU load from $373$ MB/s down to $124$ MB/s, allowing the C++ engine to achieve real-time $60$ FPS."

3. Interviewer: "What is a 'Haar Cascade', and how does it fundamentally differ from a modern Deep Learning Neural Network (like YOLO or ResNet)?"
   Senior Answer: "A Haar Cascade is an old-school (2001) Machine Learning algorithm based on 'Feature Rectangles'. It is incredibly lightweight. It subtracts the sum of pixels under a white rectangle from the sum of pixels under a black rectangle to detect generic features (like the bridge of a nose being lighter than the eye sockets). It executes extremely fast on weak CPUs. Modern Deep Learning architectures (like YOLO - You Only Look Once) are Convolutional Neural Networks (CNNs). They use massive, complex Tensor math to learn deep contextual representations of objects. While YOLO is exponentially more accurate and handles lighting variations flawlessly, it requires a dedicated GPU to mathematically calculate the millions of Tensor operations required for real-time video."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AI & ML (OpenCV) Completed.")
