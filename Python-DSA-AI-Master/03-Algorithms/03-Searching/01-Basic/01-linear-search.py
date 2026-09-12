"""
## A. Concept Name
Linear Search

## B. One-Sentence Definition
A straightforward search algorithm that sequentially checks each element in a collection one by one until it finds the target or exhausts the collection.

## C. Why Does This Exist?
To locate a specific element in an unsorted or small dataset where structured searches (like Binary Search) cannot be applied or their overhead isn't justified.

## D. Intuition
If you lost your keys in a messy room, you would simply look at every single object one after another until you find them.

## E. Real-Life Analogy
Looking for a specific book on a completely disorganized bookshelf by reading every single spine from left to right until you spot the title.

## F. Mental Model
Start at index 0 -> Check if element matches target -> If yes, return index -> If no, move to next index -> If end of list reached without match, return -1.

## G. Visual Explanation
Array: [10, 23, 45, 70, 11, 15]
Target: 70

Step 1 (Index 0): 10 == 70? No.
Step 2 (Index 1): 23 == 70? No.
Step 3 (Index 2): 45 == 70? No.
Step 4 (Index 3): 70 == 70? Yes! Return 3.

## H. Formal Explanation
Linear search is the simplest search algorithm. It traverses an array sequentially and compares each element against the target value. It does not require the data structure to be sorted, making it universally applicable to any iterable collection.

## I. Mathematical / Memory Foundation
- The algorithm compares up to `n` elements.
- Time Complexity: T(n) = O(n) in the worst and average cases. T(n) = O(1) in the best case.
- Space Complexity: S(n) = O(1) as it only needs a single loop counter/variable.

## J. Implementation & Examples
See the `linear_search` function implementation and tests below.

## L. Trace (Step-by-Step)
Trace of linear_search([10, 20, 30], 20):
1. `index` 0, `value` 10 -> `10 == 20` is False.
2. `index` 1, `value` 20 -> `20 == 20` is True. Return 1.

## M. Complexity / Memory
- Time: O(N) where N is the number of elements.
- Space: O(1) auxiliary space, memory required is constant.

## N. Common Mistakes
- Returning prematurely: returning `False` inside the loop on the first mismatch instead of continuing to check the rest of the array.
- Using it on very large sorted datasets where Binary Search (O(log N)) would be drastically faster.

## O. Common Confusions
"Should I sort the array first and then use binary search?"
Sorting takes O(N log N). If you only need to search once, linear search (O(N)) is faster than sorting and then searching.

## P. When To Use (Algorithm)
- When the collection is unsorted.
- When the array is very small (often faster due to memory locality and lack of overhead).
- When data is coming in as a stream and cannot be indexed/sorted beforehand.

## S. Debugging
- Symptom: Always returns -1 or first element.
- Diagnosis: You might have placed the `return -1` inside the `for` loop, causing the function to exit after the very first comparison.
- Fix: Ensure `return -1` is outside and after the loop.

## T. Memory Hook
"Line-ar" -> Moving in a straight line from start to finish checking everything.

## U. Active Recall
1. What is the time complexity of linear search if the element is not in the array?
2. Is linear search an in-place algorithm?
3. When is linear search better than binary search?

## V. Practice
Exercise: Modify linear search to return a list of ALL indices where the target is found, rather than just the first one.

## W. Interview Question
Q: Can linear search be optimized?
A: While the worst-case remains O(N), we can slightly optimize average search times using heuristics like "Move-to-Front" (if an element is found, move it to the front of the array assuming it will be searched for again soon).

## X. Project Connection
In Machine Learning and Data Science, when you use the `in` keyword on an unsorted Python list (e.g., checking if a specific feature name exists in a list of dynamically generated features), Python inherently performs a linear search under the hood.
"""

def linear_search(arr, target):
    """
    Search for a target value in an array using linear search.
    
    Args:
        arr (list): The list to search through.
        target: The value to search for.
        
    Returns:
        int: The index of the target if found, otherwise -1.
    """
    for index, value in enumerate(arr):
        if value == target:
            return index
    return -1

if __name__ == "__main__":
    # Test cases
    test_arr = [10, 23, 45, 70, 11, 15]
    test_target = 70
    
    result = linear_search(test_arr, test_target)
    if result != -1:
        print(f"Target {test_target} found at index {result}.")
    else:
        print(f"Target {test_target} not found in the list.")
