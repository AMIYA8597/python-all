"""
# ==============================================================================
# LABORATORY: ADVANCED COMPUTER VISION (SEGMENTATION & TRACKING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Object Detection (YOLO) draws a rigid rectangular Bounding Box around a car.
# But cars are not rectangles. If a self-driving car algorithm uses a bounding 
# box to determine the "drivable area" of a road, it will crash, because the 
# road is a complex, curved polygon.
#
# We must use Image Segmentation.
# Segmentation algorithms do not draw boxes. They classify every single pixel 
# in the image! If the image is 1920x1080 (2 Million pixels), the model outputs 
# 2 Million predictions, creating a perfect, pixel-accurate silhouette mask 
# of the car, the road, and the pedestrians.
#
# Furthermore, if you detect a car in a video, how do you know it is the SAME 
# car in the next frame? You must use Object Tracking algorithms (like DeepSORT) 
# to maintain identity persistence across time.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand Semantic vs Instance Segmentation.
# - Understand Object Tracking (Kalman Filters & DeepSORT).
# - Understand Facial Landmark Detection.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. IMAGE SEGMENTATION
# ==============================================================================
def demonstrate_segmentation():
    section_header("Image Segmentation (Pixel-Perfect Masks)")
    
    print("There are two main types of Segmentation:\n")
    
    print("--- 1. Semantic Segmentation ---")
    print("Classifies every pixel into a category, but DOES NOT differentiate ")
    print("between objects of the same category.")
    print("If there are 5 people in the photo, Semantic Segmentation outputs ")
    print("one giant 'Person' mask that covers all 5 of them combined.")
    print("Use Case: Medical Imaging (Is this pixel a tumor or healthy tissue?).\n")
    
    print("--- 2. Instance Segmentation (Mask R-CNN / YOLOv8-Seg) ---")
    print("Classifies every pixel AND separates distinct objects!")
    print("If there are 5 people, it outputs 5 completely separate masks: ")
    print("Person 1, Person 2, etc.")
    print("Use Case: Self-Driving Cars (Isolating exactly where Car A ends and Car B begins).")
    
    print("\n--- The Mathematical Output ---")
    print("Instead of outputting [X, Y, W, H], a segmentation model outputs ")
    print("a binary Matrix the exact same size as the image (e.g. 1920x1080).")
    print("If a pixel belongs to the object, the matrix value is 1. Else, 0.")
    print("You can mathematically multiply this Binary Mask against the original ")
    print("image to 'cut out' the object perfectly like Photoshop!")


# ==============================================================================
# 4. OBJECT TRACKING (DeepSORT)
# ==============================================================================
def demonstrate_object_tracking():
    section_header("Object Tracking (Identity Persistence across Frames)")
    
    print("If YOLO detects a Person in Frame 1, and a Person in Frame 2, YOLO ")
    print("has NO IDEA they are the same person. YOLO is stateless.")
    print("To count foot traffic in a store, you must Track the objects.\n")
    
    print("--- The DeepSORT Algorithm ---")
    print("DeepSORT (Deep Simple Online and Realtime Tracking) has two components:\n")
    
    print("1. THE KALMAN FILTER (Physics)")
    print("   If a car is moving at 60 MPH in Frame 1, Physics dictates exactly ")
    print("   where it *should* be in Frame 2. The Kalman Filter uses velocity ")
    print("   and trajectory math to predict the car's future location.")
    print("   If YOLO finds a car near that predicted location, it mathematically ")
    print("   links them together as ID #1!")
    
    print("\n2. THE DEEP APPEARANCE DESCRIPTOR (Neural Network)")
    print("   What if two people walk past each other and overlap? The Kalman ")
    print("   Filter's physics math will fail and swap their IDs!")
    print("   DeepSORT uses a tiny CNN to extract a 128-dimensional 'Appearance Vector' ")
    print("   (the color of their shirt, their height) for every bounding box.")
    print("   It calculates the Cosine Similarity between the people in Frame 1 ")
    print("   and Frame 2 to guarantee the IDs are assigned correctly even during occlusions!")


# ==============================================================================
# 5. FACIAL LANDMARK DETECTION
# ==============================================================================
def demonstrate_landmarks():
    section_header("Facial Landmarks & Pose Estimation")
    
    print("Basic face detection (like Haar Cascades) just draws a box around a face.")
    print("Advanced algorithms (like MediaPipe or Dlib) predict the exact X,Y ")
    print("pixel coordinates of 468 microscopic points on the human face!\n")
    
    print("--- How it works ---")
    print("The Neural Network is trained as a Regression model. Instead of outputting ")
    print("probabilities (0.0 to 1.0), the final Dense layer directly outputs ")
    print("936 floating-point numbers (468 X-coordinates and 468 Y-coordinates).")
    
    print("\n--- Applications ---")
    print("1. Drowsiness Detection: Calculate the geometric Euclidean Distance ")
    print("   between the Top Eyelid point and the Bottom Eyelid point. If the ")
    print("   distance approaches 0 for more than 2 seconds, sound a car alarm!")
    
    print("2. Snapchat Filters: You have the exact X,Y coordinate of the tip of ")
    print("   the nose. You can simply render a 3D dog nose graphic at that exact ")
    print("   coordinate, updating 60 times a second.")


def run_all_labs():
    demonstrate_segmentation()
    demonstrate_object_tracking()
    demonstrate_landmarks()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Instance Segmentation computationally much heavier than Object Detection (Bounding Boxes)?
   Answer: Object detection outputs a tiny tensor (e.g., $1 \times 85$) containing the $[X, Y, W, H]$ coordinates for a box. Instance segmentation must output an enormous mathematical Matrix (a Binary Mask) that has the exact same Height and Width as the original image (e.g., $1080 \times 1920$). For a self-driving car operating at 60 FPS, the GPU must calculate and output over 2 million precise pixel classifications every 16 milliseconds, requiring vastly more VRAM and memory bandwidth.

2. In Object Tracking, what is the specific role of the Kalman Filter?
   Answer: The Kalman Filter is a classical recursive mathematical algorithm that predicts the future state of a dynamic system. In Object Tracking, YOLO provides the "Measurement" (the car's current bounding box). The Kalman Filter uses that measurement to update its internal physics model (velocity and trajectory). In the next frame, before YOLO even runs, the Kalman Filter outputs a "Prediction" of exactly where the bounding box should geometrically be. By calculating the IoU (Intersection over Union) between YOLO's new measurement and the Kalman Filter's prediction, the tracking algorithm can confidently assign the same ID across frames.

3. How does DeepSORT recover an object's ID if the object walks behind a wall for 3 seconds?
   Answer: When an object is occluded by a wall, YOLO fails to detect it, and the Kalman Filter's trajectory predictions eventually expire. To prevent the object from being assigned a brand new ID when it emerges from the wall, DeepSORT relies on its "Deep Appearance Descriptor". The system caches the 128-dimensional visual feature vector (shirt color, texture) of the object *before* it disappeared. When a "new" unassigned bounding box appears 3 seconds later, DeepSORT calculates the Cosine Similarity between the new box's visual vector and the cached vectors of recently lost IDs. If the geometric match is close, it re-assigns the old ID, perfectly bridging the 3-second occlusion!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Computer Vision Completed.")
