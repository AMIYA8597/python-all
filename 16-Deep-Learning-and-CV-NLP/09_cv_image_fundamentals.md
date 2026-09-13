# Computer Vision Fundamentals: Image Tensors and Convolutions

## Prerequisites
- Linear Algebra (Matrices).
- NumPy arrays.

## Objectives
- Understand how images are represented in memory (Tensors).
- Differentiate between Grayscale and RGB color channels.
- Learn the mechanics of convolution operations on 2D grids.
- Understand how image filters (kernels) extract features (e.g., edges).

## Intuition
To a computer, an image is simply a multi-dimensional array (tensor) of numbers representing pixel intensities.
- A **grayscale image** is a 2D matrix (Height x Width) where values range from 0 (black) to 255 (white).
- A **color image** (RGB) is a 3D tensor (Height x Width x Channels), having 3 matrices stacked, one for Red, Green, and Blue.

**Convolutions** are mathematical operations used to extract local spatial features from these images. We slide a small grid of numbers (called a **kernel** or **filter**) over the image. At every position, we multiply the overlapping values and sum them up to produce a new value.
Different kernels produce different effects. For example, a kernel can be designed to detect vertical edges, horizontal edges, blur the image, or sharpen it. This local processing is the foundation of how computers "see".

## Mathematics
### 2D Convolution Operation
Let $I$ be an image and $K$ be a kernel of size $m \times n$. The discrete convolution operation $S(i, j) = (I * K)(i, j)$ is defined as:
$$ S(i, j) = \sum_{m} \sum_{n} I(i-m, j-n) K(m, n) $$
In deep learning frameworks, we often implement **cross-correlation** (which doesn't flip the kernel), but loosely call it convolution:
$$ S(i, j) = \sum_{m} \sum_{n} I(i+m, j+n) K(m, n) $$

### Sobel Filter (Edge Detection)
An example of a vertical edge detection filter (Sobel X):
$$
G_x = \begin{bmatrix}
-1 & 0 & 1 \\
-2 & 0 & 2 \\
-1 & 0 & 1
\end{bmatrix}
$$

## Code Reference
Refer to `09_cv_image_fundamentals.py` for applying standard image filters using NumPy and OpenCV/SciPy.

## Interview Questions
1. **How is a colored RGB image represented as a Tensor?**
   *Answer:* It is a 3-dimensional array. Common formats are [Height, Width, Channels] (HWC, used in OpenCV/Matplotlib) or [Channels, Height, Width] (CHW, used in PyTorch).
2. **What does a convolution operation actually achieve?**
   *Answer:* It extracts local spatial features by combining neighboring pixels. By using different kernels, it can highlight edges, textures, or other patterns, reducing the image to its most important structural components.
3. **What happens at the boundaries of an image during convolution?**
   *Answer:* The kernel "falls off" the edge. We handle this using **Padding** (adding zeros around the border) to maintain the original spatial dimensions, or we allow the output to shrink (Valid convolution).
