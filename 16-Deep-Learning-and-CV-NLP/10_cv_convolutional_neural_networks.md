# Convolutional Neural Networks (CNN) and Pooling

## Prerequisites
- Deep Learning fundamentals (Feedforward NNs, Activation functions).
- Image Tensors and Convolutions.

## Objectives
- Understand the architecture of a CNN (Conv Layer -> Activation -> Pooling).
- Learn how CNNs automatically learn filters (kernels) during training via backpropagation.
- Understand hyper-parameters: Padding and Stride.
- Understand the role of Pooling (Max, Average) in reducing dimensionality and providing translation invariance.

## Intuition
Instead of manually designing filters (like the Sobel edge detector), **Convolutional Neural Networks (CNNs)** *learn* the optimal filters from the data. 
In a standard CNN architecture, early layers learn low-level features (edges, corners, colors). Deeper layers combine these low-level features to recognize complex shapes (wheels, eyes), and final layers recognize entire objects (cars, faces).
Because an image can be huge, applying many filters results in massive data structures. To combat this, we use **Pooling Layers** (usually Max Pooling). Pooling slides a window over the feature map and takes the maximum value, effectively downsampling the image. This reduces computation and makes the network robust to slight shifts (translation invariance) — a face is still a face if it shifts a few pixels to the left.

## Mathematics
### Output Size Formula
Given an input of size $W$, a kernel of size $K$, padding $P$, and stride $S$, the spatial dimension of the output feature map is:
$$ O = \lfloor \frac{W - K + 2P}{S} \rfloor + 1 $$

### Max Pooling
For a $2 \times 2$ pooling window with stride 2:
$$ y = \max(x_{11}, x_{12}, x_{21}, x_{22}) $$

## Code Reference
Refer to `10_cv_convolutional_neural_networks.py` for a PyTorch implementation of a simple CNN.

## Interview Questions
1. **Why are CNNs preferred over standard Feedforward Networks for images?**
   *Answer:* Standard networks require flattening the image into a 1D vector, destroying spatial structure, and require massive amounts of parameters (dense connections to every pixel). CNNs preserve spatial structure and share parameters (the same filter slides over the whole image), making them vastly more efficient and effective.
2. **Explain Stride and Padding.**
   *Answer:* **Stride** is the number of pixels the filter shifts horizontally and vertically. A stride > 1 downsamples the image. **Padding** involves adding a border of zeros around the image to prevent the spatial dimensions from shrinking rapidly and to ensure border pixels are processed fairly.
3. **What is the purpose of Max Pooling?**
   *Answer:* Max pooling reduces the spatial dimensions (height and width) of the feature maps, which reduces computational load and the number of parameters. More importantly, it provides local translation invariance—the exact location of a feature becomes less important than its rough position relative to other features.
