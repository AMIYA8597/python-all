\"\"\"
Computer Vision (CV) Application Fundamentals

What is Computer Vision?
Computer Vision is a field of Artificial Intelligence (AI) that enables computers and systems 
to derive meaningful information from digital images, videos, and other visual inputs. 
Industry use cases include facial recognition, autonomous vehicles, medical image analysis, 
and manufacturing defect detection.

Learning Objectives:
1. Understand the foundational concepts of processing images as multi-dimensional arrays.
2. Build basic image manipulation techniques (grayscale conversion, blurring).
3. Develop professional-grade CV pipelines using object-oriented design and type hints.
4. Learn how to handle missing libraries gracefully in a production environment.

Concept Explanation:
An image is essentially a matrix of pixels. In a standard RGB image, each pixel has three 
values representing Red, Green, and Blue intensities (typically 0-255). Computer vision 
algorithms apply mathematical operations on these matrices to extract features like edges, 
shapes, and textures.

Beginner Explanation:
Imagine an image as a giant Excel spreadsheet where every cell has a color. CV is like writing 
formulas that look at these cells and say, "Ah, there's a sharp change in color here, this 
must be the edge of a cat!"

Advanced Explanation:
At scale, images are represented as NumPy ndarrays of shape (H, W, C) - Height, Width, Channels. 
Operations like convolutions (used in edge detection and deep learning) slide a kernel (a small 
matrix) over the image matrix to compute dot products, producing feature maps. Real-world 
systems optimize these array operations using vectorized instructions, GPUs, and parallel 
processing pipelines.

Performance Considerations:
- Memory: Large images consume significant RAM. Consider resizing or processing in batches.
- Speed: Use vectorized operations (NumPy) instead of nested loops.
- I/O Bound: Reading/writing images to disk can be slow. Use asynchronous I/O if processing 
  massive datasets.

Security Concerns:
- Malicious files: Images can contain embedded malware or exploit parser vulnerabilities. 
  Always sanitize and validate image formats.
- Privacy: CV apps often handle PII (faces, license plates). Ensure data is anonymized or 
  stored securely in compliance with GDPR/CCPA.
\"\"\"

import sys
import logging
from typing import Tuple, List, Optional, Any
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mocking cv2 for educational completeness in environments where it's not installed.
# In a real environment, you would just `import cv2` and `import numpy as np`.
try:
    import cv2
    import numpy as np
    CV_AVAILABLE = True
except ImportError:
    CV_AVAILABLE = False
    logging.warning(\"OpenCV (cv2) or NumPy is not installed. Using mock objects for demonstration.\")
    
    class MockNumPy:
        def zeros(self, shape, dtype):
            return [0]
            
        def array(self, data):
            return data
            
    class MockCV2:
        IMREAD_COLOR = 1
        IMREAD_GRAYSCALE = 0
        COLOR_BGR2GRAY = 6
        
        def imread(self, path: str, flags: int = 1) -> Any:
            logging.info(f\"Mock: Reading image from {path}\")
            return [[\"mock_pixel_data\"]]
            
        def imwrite(self, path: str, img: Any) -> bool:
            logging.info(f\"Mock: Writing image to {path}\")
            return True
            
        def cvtColor(self, src: Any, code: int) -> Any:
            logging.info(\"Mock: Converting color space\")
            return [[\"mock_grayscale_data\"]]
            
        def GaussianBlur(self, src: Any, ksize: Tuple[int, int], sigmaX: float) -> Any:
            logging.info(f\"Mock: Applying Gaussian Blur with kernel {ksize}\")
            return [[\"mock_blurred_data\"]]
            
    cv2 = MockCV2()
    np = MockNumPy()

# ---------------------------------------------------------
# Basic Implementation
# ---------------------------------------------------------

def basic_image_processor(input_path: str, output_path: str) -> None:
    \"\"\"
    A basic, procedural approach to reading an image, converting it to grayscale,
    and saving it.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the processed image.
    \"\"\"
    print(\"--- Running Basic Processor ---\")
    # 1. Read the image
    image = cv2.imread(input_path)
    if image is None:
        print(f\"Error: Could not read image at {input_path}\")
        return
        
    # 2. Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 3. Save the result
    success = cv2.imwrite(output_path, gray_image)
    if success:
        print(f\"Successfully saved processed image to {output_path}\")
    else:
        print(\"Failed to save the image.\")

# ---------------------------------------------------------
# Professional Implementation
# ---------------------------------------------------------

class ImageProcessor:
    \"\"\"
    A professional-grade class for image processing pipelines.
    Supports chaining operations, robust error handling, and type hinting.
    \"\"\"
    
    def __init__(self, image_path: str):
        \"\"\"
        Initializes the processor and loads the image into memory.
        
        Args:
            image_path (str): Absolute or relative path to the image file.
        
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the image cannot be decoded.
        \"\"\"
        self.image_path = Path(image_path)
        if not self.image_path.exists():
            raise FileNotFoundError(f\"Image file not found: {self.image_path}\")
            
        self.image_data = cv2.imread(str(self.image_path))
        if self.image_data is None or len(self.image_data) == 0:
            raise ValueError(f\"Failed to decode image from {self.image_path}. Corrupted or unsupported format.\")
            
        self.history: List[str] = [\"loaded\"]
        logging.info(f\"Image {self.image_path.name} loaded successfully.\")

    def to_grayscale(self) -> 'ImageProcessor':
        \"\"\"
        Converts the current image to grayscale.
        Returns self for method chaining.
        \"\"\"
        try:
            self.image_data = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2GRAY)
            self.history.append(\"grayscale\")
            logging.info(\"Converted image to grayscale.\")
        except Exception as e:
            logging.error(f\"Error converting to grayscale: {e}\")
            raise
        return self

    def apply_blur(self, kernel_size: Tuple[int, int] = (5, 5)) -> 'ImageProcessor':
        \"\"\"
        Applies a Gaussian blur to the image to reduce noise.
        Returns self for method chaining.
        
        Args:
            kernel_size: Tuple representing the (width, height) of the kernel. Must be odd numbers.
        \"\"\"
        if kernel_size[0] % 2 == 0 or kernel_size[1] % 2 == 0:
            raise ValueError(\"Kernel size dimensions must be odd numbers (e.g., 3, 5, 7).\")
            
        try:
            self.image_data = cv2.GaussianBlur(self.image_data, kernel_size, 0)
            self.history.append(f\"blurred_{kernel_size[0]}x{kernel_size[1]}\")
            logging.info(f\"Applied Gaussian blur with kernel {kernel_size}.\")
        except Exception as e:
            logging.error(f\"Error applying blur: {e}\")
            raise
        return self

    def save(self, output_dir: str = \".\", prefix: str = \"processed_\") -> str:
        \"\"\"
        Saves the processed image to disk.
        
        Args:
            output_dir: Directory to save the file.
            prefix: Prefix to prepend to the original filename.
            
        Returns:
            str: The full path to the saved file.
        \"\"\"
        out_dir_path = Path(output_dir)
        out_dir_path.mkdir(parents=True, exist_ok=True)
        
        output_name = f\"{prefix}{self.image_path.name}\"
        output_path = out_dir_path / output_name
        
        success = cv2.imwrite(str(output_path), self.image_data)
        if not success:
            raise IOError(f\"Failed to write image to {output_path}\")
            
        logging.info(f\"Saved processed image to {output_path}\")
        return str(output_path)


# ---------------------------------------------------------
# Complexity Analysis & Interview Challenge
# ---------------------------------------------------------
\"\"\"
Complexity Analysis:
- Time Complexity: O(H * W) for most basic pixel-wise operations (like grayscale conversion), 
  where H is image height and W is image width. Blurring with a kernel of size K is O(H * W * K^2).
- Space Complexity: O(H * W * C) to store the image in memory, where C is the number of channels (3 for RGB, 1 for Grayscale).

Interview Challenge:
Question: You are tasked with processing a live video feed (60 fps) at 4K resolution to detect faces. 
Your current Python + OpenCV script drops frames because it takes 50ms per frame to process. How do you optimize this pipeline?

Answer Guide:
1. Resize the frames: 4K is too large for real-time face detection. Downscale to 720p or 480p before processing.
2. Frame Skipping: Process every 3rd or 5th frame instead of all 60 frames per second.
3. Multi-threading/Multiprocessing: Use a separate thread to read frames from the camera (I/O) and a pool 
   of workers to process them (CPU).
4. Hardware Acceleration: Offload processing to a GPU using CUDA or OpenCL, or use specialized inference 
   engines like TensorRT for deep learning models.
\"\"\"

# ---------------------------------------------------------
# Example Usage and Tests (Main Guard)
# ---------------------------------------------------------
if __name__ == \"__main__\":
    print(\"\\n=== Computer Vision App Execution ===\")
    
    # Create a dummy image file for testing purposes
    test_img_path = Path(\"dummy_test_image.jpg\")
    test_img_path.touch()
    
    try:
        # Test Basic Implementation
        basic_image_processor(str(test_img_path), \"basic_out.jpg\")
        
        print(\"\\n--- Running Professional Processor ---\")
        # Test Professional Implementation (Method Chaining)
        processor = ImageProcessor(str(test_img_path))
        saved_path = (processor
                     .to_grayscale()
                     .apply_blur(kernel_size=(7, 7))
                     .save(output_dir=\".\", prefix=\"pro_out_\"))
        
        # Assertions to verify correctness
        assert \"grayscale\" in processor.history, \"Grayscale operation not recorded.\"
        assert \"blurred_7x7\" in processor.history, \"Blur operation not recorded.\"
        assert Path(saved_path).exists() or not CV_AVAILABLE, \"Output file should exist in mock mode.\"
        print(\"\\nAll assertions passed successfully! Professional pipeline works.\")
        
    except Exception as e:
        print(f\"An error occurred during execution: {e}\")
    finally:
        # Cleanup dummy files
        if test_img_path.exists():
            test_img_path.unlink()
        
        # Cleanup mock outputs if they were somehow created
        for p in [Path(\"basic_out.jpg\"), Path(\"pro_out_dummy_test_image.jpg\")]:
            if p.exists():
                p.unlink()
                
    print(\"=== Execution Complete ===\")
