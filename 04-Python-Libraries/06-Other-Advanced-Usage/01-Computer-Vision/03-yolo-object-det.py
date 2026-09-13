"""
# ==============================================================================
# LABORATORY: REAL-TIME OBJECT DETECTION (YOLO)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A standard Convolutional Neural Network (like ResNet) is a Classifier. 
# If you feed it an image, it outputs a single word: "Dog". 
# 
# But what if the image is a dashcam feed containing 5 cars, 3 pedestrians, 
# and 1 bicycle? ResNet will fail completely. You need Object Detection.
#
# Object Detection models do not just classify; they output the exact [X, Y, W, H] 
# pixel coordinates (Bounding Boxes) of every single object in the image.
#
# In 2015, "You Only Look Once" (YOLO) revolutionized Computer Vision. Older 
# models (like R-CNN) chopped the image into 2,000 regions and ran the CNN 
# 2,000 times. It was incredibly slow (0.5 frames per second). YOLO passes the 
# entire image through the CNN exactly ONCE, predicting bounding boxes mathematically 
# across a rigid grid. It runs at 150 Frames Per Second (FPS), enabling true 
# real-time autonomous driving and drone navigation.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of YOLO (Grid Division).
# - Understand Non-Maximum Suppression (NMS) and Intersection over Union (IoU).
# - Execute a YOLO Object Detection pipeline using the `ultralytics` package.
#
# ==============================================================================
"""

import numpy as np

# In a real environment: pip install ultralytics opencv-python
try:
    from ultralytics import YOLO
    import cv2
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. YOLO ARCHITECTURE & BOUNDING BOXES
# ==============================================================================
def demonstrate_yolo():
    section_header("YOLO Inference (Ultralytics API)")
    
    if not HAS_YOLO:
        print("[WARNING] Ultralytics (YOLO) not installed.")
        print("Run: pip install ultralytics opencv-python")
        return
        
    print("We will load the YOLOv8-nano model (an ultra-fast, tiny variant).")
    print("In a real environment, this automatically downloads the `.pt` PyTorch weights!\n")
    
    try:
        # 1. LOAD THE MODEL
        # YOLOv8n is pretrained on the COCO dataset (80 common objects: person, car, dog, etc.)
        model = YOLO('yolov8n.pt') 
        
        # 2. CREATE SYNTHETIC IMAGE
        # We create a simple image (but in reality, YOLO expects real photos, 
        # so it will likely predict nothing here. This is purely to demonstrate the API).
        synthetic_image = np.zeros((640, 640, 3), dtype=np.uint8)
        
        # 3. RUN INFERENCE
        # YOLO executes a single massive forward pass.
        print("Executing YOLO Forward Pass...")
        results = model(synthetic_image, verbose=False)
        
        # 4. PARSE THE RESULTS
        result = results[0] # Results for the first image in the batch
        boxes = result.boxes
        
        print("\n--- YOLO Output Tensors ---")
        print(f"Total Objects Detected: {len(boxes)}")
        
        if len(boxes) > 0:
            for box in boxes:
                # Extract Bounding Box Coordinates [X1, Y1, X2, Y2]
                coords = box.xyxy[0].tolist()
                
                # Extract Class ID and Confidence Score
                class_id = int(box.cls[0].item())
                confidence = box.conf[0].item()
                
                # Look up the human-readable string name of the class
                class_name = model.names[class_id]
                
                print(f"Detected: {class_name} | Confidence: {confidence*100:.1f}%")
                print(f"Bounding Box: [X1: {coords[0]:.1f}, Y1: {coords[1]:.1f}, X2: {coords[2]:.1f}, Y2: {coords[3]:.1f}]")
        else:
            print("No objects detected in the pure black synthetic image (As expected!)")
            
        print("\nIn a real script, you would draw the boxes on the image using:")
        print("  annotated_image = result.plot()")
        print("  cv2.imshow('YOLO', annotated_image)")
            
    except Exception as e:
        print(f"Execution skipped: {e}")


# ==============================================================================
# 4. NON-MAXIMUM SUPPRESSION (NMS) & IoU
# ==============================================================================
def demonstrate_nms_concept():
    section_header("Non-Maximum Suppression (NMS)")
    
    print("YOLO divides the image into a grid (e.g., 20x20).")
    print("If a large dog takes up 4 grid cells, ALL 4 grid cells will mathematically ")
    print("predict a bounding box for the dog! You end up with 4 overlapping ")
    print("rectangles drawn around the exact same dog.\n")
    
    print("--- Intersection over Union (IoU) ---")
    print("How does the computer know two rectangles are predicting the same object?")
    print("It calculates IoU: (Area of Overlap) / (Area of Union).")
    print("If IoU > 0.5, the boxes are highly overlapping.\n")
    
    print("--- Non-Maximum Suppression (NMS) ---")
    print("1. Sort all predicted boxes by their Confidence Score (e.g., Box A is 98%, Box B is 91%).")
    print("2. Select the #1 highest confidence box (Box A, 98%).")
    print("3. Calculate the IoU between Box A and Box B.")
    print("4. If IoU > 0.5, mathematically DESTROY Box B! (It is a duplicate).")
    print("5. Repeat for all remaining boxes.")
    
    print("\nYOLO does this automatically in C++ natively on the GPU, returning ")
    print("only the clean, singular bounding boxes to the Python API.")


def run_all_labs():
    demonstrate_yolo()
    demonstrate_nms_concept()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is YOLO mathematically able to achieve 150 Frames Per Second, while older models like R-CNN achieved only 0.5 FPS?
   Answer: R-CNN uses "Region Proposals". A separate algorithmic step mathematically identifies 2,000 potential bounding box regions in the image. The model then physically crops out those 2,000 regions and runs the heavy Convolutional Neural Network forward pass 2,000 separate times for a single image! YOLO (You Only Look Once) reframes object detection as a single regression problem. It passes the raw image through the CNN exactly *one time*. The final output tensor is a massive grid (e.g., $20 \times 20 \times 85$) that simultaneously contains the class probabilities and the mathematical $[X, Y, Width, Height]$ bounding box coordinates for every section of the image.

2. Explain the concept of "Intersection over Union" (IoU).
   Answer: IoU is a metric used to evaluate how well two bounding boxes overlap. It is calculated by dividing the Area of Overlap (the geometric intersection of Box A and Box B) by the Area of Union (the total geometric footprint of both boxes combined). If the boxes do not touch, IoU is 0.0. If the boxes are perfectly identical, IoU is 1.0. It is heavily used in two places: evaluating the accuracy of the model against human-drawn ground truth boxes, and calculating Non-Maximum Suppression to delete duplicate predictions.

3. If you run YOLO on a video feed and the bounding boxes violently flicker on and off every frame, what hyperparameter should you adjust?
   Answer: You need to lower the Confidence Threshold (e.g., from `0.50` to `0.25`). In frame 1, the model might predict the car with 52% confidence (drawing the box). In frame 2, the lighting shifts slightly, and the confidence drops to 48%. If your threshold is set to 50%, the box is deleted, causing the flicker. By lowering the confidence threshold to 25%, the model is allowed to draw boxes even if it is slightly unsure, resulting in smooth, continuous tracking across frames. (You may also need to implement an Object Tracking algorithm like DeepSORT to stabilize the IDs across frames).
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Real-Time Object Detection (YOLO) Completed.")
