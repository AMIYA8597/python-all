"""
Sorting Visualizer - Main Application and Algorithms

This module contains a graphical Sorting Visualizer using Tkinter, along with
the underlying sorting algorithms implemented as generators to facilitate animation.

Usage:
    python main.py          # Runs the GUI
    python main.py --test   # Runs the unit tests for the sorting algorithms
"""

import tkinter as tk
from tkinter import ttk
import random
import sys
import unittest

# -------------------------------------------------------------------------
# Sorting Algorithms (Generators for Animation)
# -------------------------------------------------------------------------
# Each algorithm yields a tuple: (array_state, color_array)
# color_array maps indices to colors (e.g., 'red' for comparison, 'green' for sorted)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            yield arr, {j: 'red', j+1: 'red'}
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, {j: 'green', j+1: 'green'}
    yield arr, {i: 'blue' for i in range(len(arr))}


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        yield arr, {i: 'red', j: 'yellow'}
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, {j + 1: 'red', j: 'yellow'}
        arr[j + 1] = key
        yield arr, {j + 1: 'green'}
    yield arr, {i: 'blue' for i in range(len(arr))}


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr, {min_idx: 'red', j: 'yellow'}
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, {i: 'green', min_idx: 'green'}
    yield arr, {i: 'blue' for i in range(len(arr))}


def quick_sort(arr, low, high):
    if low < high:
        # Partition
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            yield arr, {j: 'red', high: 'yellow'}
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr, {i: 'green', j: 'green'}
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield arr, {i + 1: 'green', high: 'green'}
        pi = i + 1

        # Recursive calls
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)
    
    if low == 0 and high == len(arr) - 1:
        yield arr, {i: 'blue' for i in range(len(arr))}


def quick_sort_wrapper(arr):
    yield from quick_sort(arr, 0, len(arr) - 1)


# -------------------------------------------------------------------------
# GUI Application
# -------------------------------------------------------------------------

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("900x600")
        self.root.config(bg="white")
        
        # Variables
        self.data = []
        self.generator = None
        self.sorting = False
        self.algorithm_name = tk.StringVar(value="Bubble Sort")
        
        self.setup_ui()
        self.generate_data()

    def setup_ui(self):
        # Control Frame
        control_frame = tk.Frame(self.root, bg="lightgrey", padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Algorithm Selection
        tk.Label(control_frame, text="Algorithm:", bg="lightgrey").grid(row=0, column=0, padx=5, pady=5)
        algo_menu = ttk.Combobox(
            control_frame, 
            textvariable=self.algorithm_name,
            values=["Bubble Sort", "Insertion Sort", "Selection Sort", "Quick Sort"]
        )
        algo_menu.grid(row=0, column=1, padx=5, pady=5)
        
        # Speed Scale
        tk.Label(control_frame, text="Speed (ms):", bg="lightgrey").grid(row=0, column=2, padx=5, pady=5)
        self.speed_scale = tk.Scale(control_frame, from_=5, to=500, resolution=5, orient=tk.HORIZONTAL, bg="lightgrey")
        self.speed_scale.set(50)
        self.speed_scale.grid(row=0, column=3, padx=5, pady=5)

        # Array Size
        tk.Label(control_frame, text="Array Size:", bg="lightgrey").grid(row=0, column=4, padx=5, pady=5)
        self.size_scale = tk.Scale(control_frame, from_=10, to=150, resolution=1, orient=tk.HORIZONTAL, bg="lightgrey")
        self.size_scale.set(50)
        self.size_scale.grid(row=0, column=5, padx=5, pady=5)

        # Buttons
        tk.Button(control_frame, text="Generate Array", command=self.generate_data, bg="white").grid(row=0, column=6, padx=5, pady=5)
        self.start_button = tk.Button(control_frame, text="Start Sorting", command=self.start_sorting, bg="lightgreen")
        self.start_button.grid(row=0, column=7, padx=5, pady=5)

        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def generate_data(self):
        if self.sorting:
            return
        size = self.size_scale.get()
        self.data = [random.randint(10, 500) for _ in range(size)]
        self.draw_data(self.data, {})

    def draw_data(self, data, color_map):
        self.canvas.delete("all")
        c_height = self.canvas.winfo_height()
        c_width = self.canvas.winfo_width()
        
        # Avoid zero division before canvas is fully rendered
        if c_height == 1 or c_width == 1:
            c_height, c_width = 500, 860

        x_width = c_width / (len(data) + 1)
        offset = 5
        spacing = 2
        
        normalized_data = [i / max(data) for i in data] if data else []

        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = c_height - (height * (c_height - 20))
            x1 = (i + 1) * x_width + offset
            y1 = c_height
            
            color = color_map.get(i, "blue")
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        
        self.root.update_idletasks()

    def start_sorting(self):
        if self.sorting:
            return
        self.sorting = True
        self.start_button.config(state=tk.DISABLED)

        algo = self.algorithm_name.get()
        if algo == "Bubble Sort":
            self.generator = bubble_sort(self.data)
        elif algo == "Insertion Sort":
            self.generator = insertion_sort(self.data)
        elif algo == "Selection Sort":
            self.generator = selection_sort(self.data)
        elif algo == "Quick Sort":
            self.generator = quick_sort_wrapper(self.data)
        
        self.animate()

    def animate(self):
        try:
            arr, color_map = next(self.generator)
            self.draw_data(arr, color_map)
            # Schedule next frame
            self.root.after(self.speed_scale.get(), self.animate)
        except StopIteration:
            self.sorting = False
            self.start_button.config(state=tk.NORMAL)
            self.draw_data(self.data, {i: 'green' for i in range(len(self.data))})


# -------------------------------------------------------------------------
# Unit Tests for Sorting Algorithms
# -------------------------------------------------------------------------
class TestSortingAlgorithms(unittest.TestCase):
    
    def setUp(self):
        self.arrays = [
            [],
            [1],
            [3, 1, 2],
            [9, 8, 7, 6, 5, 4, 3, 2, 1],
            [1, 2, 3, 4, 5],
            [random.randint(-100, 100) for _ in range(50)]
        ]
        
    def _run_generator(self, gen, arr):
        """Helper to exhaust the generator and return the final array."""
        try:
            for state, _ in gen(arr):
                pass
        except StopIteration:
            pass
        return arr

    def test_bubble_sort(self):
        for arr in self.arrays:
            with self.subTest(arr=arr):
                copy_arr = list(arr)
                expected = sorted(copy_arr)
                self.assertEqual(self._run_generator(bubble_sort, copy_arr), expected)

    def test_insertion_sort(self):
        for arr in self.arrays:
            with self.subTest(arr=arr):
                copy_arr = list(arr)
                expected = sorted(copy_arr)
                self.assertEqual(self._run_generator(insertion_sort, copy_arr), expected)
                
    def test_selection_sort(self):
        for arr in self.arrays:
            with self.subTest(arr=arr):
                copy_arr = list(arr)
                expected = sorted(copy_arr)
                self.assertEqual(self._run_generator(selection_sort, copy_arr), expected)

    def test_quick_sort(self):
        for arr in self.arrays:
            if len(arr) <= 1:
                continue
            with self.subTest(arr=arr):
                copy_arr = list(arr)
                expected = sorted(copy_arr)
                self._run_generator(quick_sort_wrapper, copy_arr)
                self.assertEqual(copy_arr, expected)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        sys.argv.pop()
        unittest.main()
    else:
        root = tk.Tk()
        app = SortingVisualizer(root)
        root.mainloop()
