# Sorting Visualizer Project Specification

## 1. Project Overview
The **Sorting Visualizer** is a Python-based graphical application designed to help students, developers, and educators understand how various sorting algorithms work under the hood. By animating the process of sorting an array of numbers, this project demystifies the mechanics of algorithms such as Bubble Sort, Merge Sort, Quick Sort, and more.

## 2. Purpose and Learning Outcomes
- **Algorithm Comprehension**: Visualize the step-by-step execution of sorting algorithms to understand comparisons, swaps, and recursive divisions.
- **Time Complexity Intuition**: Gain a visual intuition for Big-O time complexity (e.g., observing the quadratic nature of Bubble Sort vs. the logarithmic efficiency of Quick Sort).
- **GUI Programming**: Learn how to build interactive desktop applications using Python's built-in `tkinter` library.
- **Concurrency & Animation**: Understand how to manage UI updates and background tasks (or generator-based stepping) to animate processes without freezing the main application thread.

## 3. Features
- **Multiple Algorithms**: Supports Bubble Sort, Insertion Sort, Selection Sort, Merge Sort, and Quick Sort.
- **Dynamic Array Generation**: Generate random arrays of varying sizes and ranges.
- **Speed Control**: Adjust the speed of the animation to see operations in slow motion or fast forward.
- **Color Coding**: Visual cues indicating which elements are currently being compared (e.g., Red for comparisons, Green for sorted elements, Blue for default).
- **Real-time Statistics**: Displays the number of comparisons and array accesses during the sorting process (optional extension).

## 4. Technical Requirements
- **Language**: Python 3.8+
- **Libraries**:
  - `tkinter`: Standard GUI library for Python (No external dependencies).
  - `random`: For generating random arrays.
  - `time`: For introducing delays in the animation loop.
  - `unittest`: For validating the correctness of the sorting logic.

## 5. Architecture and Design
The application is built using an Object-Oriented approach with a Model-View-Controller (MVC) mindset:
- **Model**: The data representation (the array) and the sorting algorithms. The algorithms are implemented as Python generator functions (`yield`) to pause execution and allow the UI to update at each step.
- **View**: The `tkinter` Canvas where data points are drawn as vertical bars. The height of the bar represents the value.
- **Controller**: The UI components (Buttons, Sliders, Dropdowns) that handle user input, update the data model, and trigger the visualization loop.

### 5.1 Generator-based Animation
To prevent the sorting algorithms from blocking the Tkinter main loop, algorithms `yield` their current state (or the specific indices being compared/swapped). The main application periodically calls `next()` on the generator using Tkinter's `.after()` method to advance the algorithm by one step and redraw the canvas.

## 6. Setup and Usage

### Running the Application
To run the visualizer GUI:
```bash
python main.py
```

### Running Tests
To verify that the underlying sorting algorithms are mathematically correct:
```bash
python main.py --test
```

## 7. Advanced Concepts to Explore
- **Sound Generation**: Map the value of the array elements to audio frequencies and play a sound when they are accessed, creating an auditory representation of the sort (similar to famous YouTube sorting videos).
- **Additional Algorithms**: Implement Heap Sort, Radix Sort, or Bogo Sort.
- **Custom Input**: Allow users to enter a specific comma-separated list of numbers to sort.

## 8. Common Mistakes & Troubleshooting
- **Freezing the GUI**: Using `time.sleep()` in a standard loop will block the `tkinter` main thread, making the app unresponsive. Always use `.after()` or generator patterns to yield control back to the event loop.
- **Recursion Limits**: For Quick Sort or Merge Sort on very large arrays, Python's default recursion limit might be reached. It's essential to manage array sizes or increase the recursion limit via `sys.setrecursionlimit()`.
