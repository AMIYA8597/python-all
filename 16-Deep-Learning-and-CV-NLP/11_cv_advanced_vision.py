"""
# ==============================================================================
# LABORATORY: COMPUTER VISION (ADVANCED: OBJECT DETECTION & ViT)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer builds a self-driving car using a standard CNN Image 
# Classifier. The camera looks at a street and the model outputs "Pedestrian: 99%". 
# The car knows a pedestrian exists, but it has absolutely no idea *where* the 
# pedestrian is in the 1920x1080 frame. The car crashes.
#
# A senior AI engineer understands "Object Detection" (YOLO, Faster R-CNN). The 
# network is architecturally modified to output not just a Class, but 4 exact 
# Regression coordinates: [X_min, Y_min, X_max, Y_max] (a Bounding Box). They 
# mathematically evaluate the model's accuracy using IoU (Intersection over Union). 
# The car knows exactly where the pedestrian is and successfully stops.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Bounding Box Mathematics [x1, y1, x2, y2].
# - Execute Intersection over Union (IoU) calculations.
# - Architect Vision Transformer (ViT) Image Patching logic.
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (INTERSECTION OVER UNION)
# ==============================================================================
class ObjectDetectionSimulator:
    
    @staticmethod
    def calculate_iou(boxA, boxB):
        """
        [SECURE] Intersection over Union (IoU).
        Box format: [x_min, y_min, x_max, y_max]
        """
        # 1. Calculate the intersection rectangle (Where do they overlap?)
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # If they don't overlap, intersection area is 0
        interArea = max(0, xB - xA) * max(0, yB - yA)

        # 2. Calculate the area of both individual bounding boxes
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

        # 3. Calculate the Union (Total combined area minus the overlapping part)
        unionArea = float(boxAArea + boxBArea - interArea)

        # 4. Divide Intersection by Union
        iou = interArea / unionArea if unionArea > 0 else 0.0
        return iou

    def evaluate_model_prediction(self):
        print("  [INIT] Evaluating Object Detection Bounding Boxes...")
        
        # Ground Truth: A pedestrian is exactly at these coordinates
        # [x_min, y_min, x_max, y_max]
        ground_truth_box = [50, 50, 150, 200]
        
        # Model Prediction: The YOLO model predicted these coordinates
        predicted_box = [60, 60, 160, 190]
        
        # Totally Wrong Prediction
        wrong_box = [300, 300, 400, 500]
        
        print(f"\n  [BOXES]")
        print(f"  -> Ground Truth: {ground_truth_box}")
        print(f"  -> Predicted:    {predicted_box}")
        print(f"  -> Bad Guess:    {wrong_box}")
        
        print("\n  [EXECUTION] Calculating Intersection over Union (IoU)...")
        iou_score = self.calculate_iou(ground_truth_box, predicted_box)
        iou_wrong = self.calculate_iou(ground_truth_box, wrong_box)
        
        print(f"  -> Good Prediction IoU: {iou_score:.4f} (Threshold typically > 0.5 is a 'Hit')")
        print(f"  -> Bad Prediction IoU:  {iou_wrong:.4f}")
        print("  -> [FLAWLESS] The algorithm mathematically verified the physical ")
        print("     spatial accuracy of the prediction box.")


# ==============================================================================
# 4. THE ARCHITECTURAL PATTERN: VISION TRANSFORMERS (ViT)
# ==============================================================================
class VisionTransformerSimulator:
    
    @staticmethod
    def simulate_image_patching():
        """
        [SECURE] Simulates the critical first step of a Vision Transformer.
        Transformers process 'Tokens' (Words), not 2D Grids. We must hack the Image 
        by cutting it into a sequence of flat patches!
        """
        print("\n  [INIT] Architecting Vision Transformer (ViT) Patching...")
        
        # A 4x4 Grayscale Image
        image = np.array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]
        ])
        
        print("\n  [IMAGE TENSOR (4x4)]")
        print(image)
        
        # We define a patch size of 2x2.
        # This will slice the 4x4 image into 4 distinct 2x2 blocks.
        patch_size = 2
        
        print("\n  [EXECUTION] Slicing Image into 2x2 Patches...")
        patches = []
        
        for i in range(0, 4, patch_size):
            for j in range(0, 4, patch_size):
                # Extract the 2x2 patch
                patch = image[i:i+patch_size, j:j+patch_size]
                
                # Flatten the 2x2 matrix into a 1D vector (length 4)
                # This acts exactly like a 'Word Embedding' in NLP!
                flat_patch = patch.flatten()
                patches.append(flat_patch)
                
        print("  -> The image has been sliced into 4 discrete patches.")
        for idx, p in enumerate(patches):
            print(f"     - Patch Token {idx+1}: {p}")
            
        print("\n  [FLAWLESS] The 2D image has been mathematically converted into a 1D ")
        print("  sequence of 'Tokens'. This sequence can now be fed directly into ")
        print("  a standard NLP Self-Attention matrix (ChatGPT architecture) to ")
        print("  perform Computer Vision, completely bypassing Convolutional layers!")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE BENCHMARK)
# ==============================================================================
def demonstrate_advanced_vision():
    section_header("Computer Vision: Advanced Architectures (YOLO & ViT)")
    
    sim1 = ObjectDetectionSimulator()
    sim1.evaluate_model_prediction()
    
    sim2 = VisionTransformerSimulator()
    sim2.simulate_image_patching()


def run_all_labs():
    demonstrate_advanced_vision()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In Object Detection architectures like YOLO, why do we use Non-Maximum Suppression (NMS) during inference?"
   Senior Answer: "Duplicate Elimination. When YOLO looks at an image of a dog, its dense grid architecture might mathematically trigger $5$ slightly different overlapping Bounding Boxes, all claiming to contain the dog with varying confidences (e.g., $99\\%$, $95\\%$, $85\\%$). NMS is a post-processing algorithm that mathematically resolves this. It first selects the box with the absolute highest confidence ($99\\%$). It then calculates the IoU between that winner and the remaining $4$ boxes. If the IoU is highly overlapping (e.g., $>0.5$), NMS brutally deletes the lower-confidence boxes, assuming they are redundant detections of the exact same physical object."

2. Interviewer: "What is the architectural difference between 'Semantic Segmentation' (like U-Net) and 'Instance Segmentation' (like Mask R-CNN)?"
   Senior Answer: "Pixel Labeling vs Object Identification. Semantic Segmentation classifies every single pixel in an image into a category. If there are $5$ sheep in a field, a U-Net will color all the sheep pixels 'White'. It mathematically does not know there are $5$ distinct sheep; it just knows a massive blob of 'Sheep-Class' pixels exists. Instance Segmentation first runs Object Detection to draw $5$ distinct Bounding Boxes (identifying $5$ individual entities), and *then* runs a pixel-level mask inside each box. It can physically distinguish 'Sheep 1' from 'Sheep 2' even if their pixels are touching."

3. Interviewer: "Why did Vision Transformers (ViT) require massive datasets (JFT-300M) to beat ResNet, whereas ResNet trains effectively on smaller datasets?"
   Senior Answer: "The Lack of Inductive Bias. A Convolutional Neural Network (ResNet) contains a strict architectural 'Inductive Bias'. The sliding 3x3 kernel forces the network to assume that adjacent pixels are physically related, and that patterns are translationally invariant. The network doesn't have to learn this; it is hardcoded into the mathematics of Convolution. A Vision Transformer (ViT) treats an image as a randomized sequence of flattened patches. It has zero Inductive Bias. It literally has to learn the concept of '2D spatial geometry' from scratch using pure Self-Attention. To mathematically learn geometry from zero, it requires an astronomically larger dataset than a CNN."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: CV (Advanced Vision) Completed.")
