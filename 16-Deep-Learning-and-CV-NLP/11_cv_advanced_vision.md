# Advanced Vision: Transfer Learning and Object Detection

## Prerequisites
- Convolutional Neural Networks (CNNs).
- Backpropagation and Fine-Tuning.

## Objectives
- Understand Transfer Learning and why it is essential in deep learning.
- Explore popular CNN architectures (ResNet, VGG, MobileNet).
- Understand the difference between Image Classification, Object Detection, and Image Segmentation.
- High-level overview of Object Detection architectures (YOLO, Faster R-CNN).

## Intuition
### Transfer Learning
Training a deep CNN from scratch requires massive datasets (millions of images) and vast computing power (weeks on GPUs). 
**Transfer Learning** allows us to take a model trained on a massive generic dataset (like ImageNet, with 1000 categories) and repurpose it for our specific task (e.g., distinguishing between hotdogs and not-hotdogs) using very little data. We freeze the early layers (which learned generic features like edges and textures) and only retrain the final classification layers for our specific problem.

### Object Detection
Image classification outputs a single label for the entire image. What if there are multiple objects?
**Object Detection** involves identifying multiple objects in an image AND drawing bounding boxes around them.
- **Two-Stage Detectors (Faster R-CNN):** First propose regions where objects *might* be, then classify those regions. Highly accurate but slower.
- **One-Stage Detectors (YOLO - You Only Look Once):** Frame object detection as a single regression problem, predicting bounding boxes and class probabilities directly from the full image in one pass. Extremely fast (real-time) but sometimes slightly less accurate on tiny objects.

## Mathematics (Bounding Box IoU)
### Intersection over Union (IoU)
To evaluate how accurate a predicted bounding box is compared to the ground truth box, we compute IoU:
$$ \text{IoU} = \frac{\text{Area of Overlap}}{\text{Area of Union}} $$
IoU > 0.5 is typically considered a "good" prediction.

## Code Reference
Refer to `11_cv_advanced_vision.py` for an example of loading a pre-trained ResNet model using `torchvision` and modifying it for Transfer Learning.

## Interview Questions
1. **Explain the concept of "Freezing" layers in Transfer Learning.**
   *Answer:* Freezing a layer means we set its `requires_grad` property to `False`. During backpropagation, the gradients are not computed for these layers, and their weights remain unchanged. This preserves the pre-learned feature extraction capabilities and speeds up training on the new dataset.
2. **What problem does ResNet (Residual Networks) solve?**
   *Answer:* As neural networks get extremely deep, they suffer from the vanishing gradient problem, making them hard to train (adding layers actually degrades performance). ResNets introduce "Skip Connections" (or shortcuts) that allow gradients to flow directly through the network, bypassing certain layers. This enables the training of networks with hundreds of layers.
3. **What is the difference between Object Detection and Image Segmentation?**
   *Answer:* Object Detection draws rectangular bounding boxes around objects. Image Segmentation (like Mask R-CNN or U-Net) classifies every single pixel in the image, providing an exact outline/mask of the object.
