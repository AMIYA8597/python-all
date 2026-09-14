"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (DOCUMENTATION & SPHINX)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a massive 5,000-line math library. They don't write 
# a single comment or docstring because they believe their code is "self-documenting". 
# When another developer tries to use the `process()` function, they don't know 
# if it expects a String, an Integer, or a Dictionary. They execute the function 
# incorrectly, breaking the production pipeline.
#
# A senior software architect understands that "Documentation is Code". They 
# execute strict Google-Style or NumPy-Style Docstrings on every single class 
# and method. Furthermore, they automate the pipeline using `Sphinx` or `MkDocs`. 
# Every time code is pushed, the CI/CD pipeline mathematically extracts the 
# Docstrings from the Python files and compiles a gorgeous, searchable, HTML 
# website documenting the entire API.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Google-Style and NumPy-Style Docstring Architectures.
# - Execute algorithmic Documentation Generation (Sphinx/MkDocs).
# - Architect self-documenting APIs with `typing` integration.
#
# ==============================================================================
"""

from typing import List, Dict, Union

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE "BAD" DOCUMENTATION)
# ==============================================================================
# ANTI-PATTERN: The "Useless Comment" and the "Missing Docstring"

class data_parser:
    # initialize it
    def __init__(self, data):
        self.d = data
        
    def run(self, mod):
        # run the mod on the data and return it
        res = []
        for x in self.d:
            res.append(x * mod)
        return res


# ==============================================================================
# 4. THE ARCHITECTURAL SOLUTION (GOOGLE-STYLE DOCSTRINGS)
# ==============================================================================
# This is how senior engineers write Python. 
# It is mathematically parsable by Sphinx/MkDocs!

class DataParser:
    """
    An algorithmic engine for parsing and mutating large datasets.
    
    This class loads a raw dataset into memory and applies mathematical 
    transformations to it in a highly optimized loop.
    
    Attributes:
        dataset (List[float]): The numerical dataset stored in RAM.
    """
    
    def __init__(self, dataset: List[float]):
        """
        Initializes the DataParser with a target dataset.
        
        Args:
            dataset (List[float]): A list of floats to be processed.
        """
        self.dataset = dataset
        
    def apply_modifier(self, modifier: float) -> List[float]:
        """
        Applies a mathematical multiplier to every element in the dataset.
        
        This method executes a linear O(N) scan across the array, multiplying 
        each element by the requested `modifier`. It does not mutate the 
        original array in place; it returns a new array.
        
        Args:
            modifier (float): The mathematical scalar to apply.
            
        Returns:
            List[float]: A new array containing the mutated values.
            
        Raises:
            ValueError: If the dataset is empty.
            TypeError: If the modifier is not a numerical type.
            
        Example:
            >>> parser = DataParser([1.0, 2.0, 3.0])
            >>> parser.apply_modifier(2.0)
            [2.0, 4.0, 6.0]
        """
        if not self.dataset:
            raise ValueError("Cannot process an empty dataset.")
        if not isinstance(modifier, (int, float)):
            raise TypeError("Modifier must be a number.")
            
        return [val * modifier for val in self.dataset]


# ==============================================================================
# 5. THE SPHINX / MKDOCS SIMULATOR
# ==============================================================================
class DocumentationGenerator:
    """Simulates what Sphinx does mathematically under the hood."""
    
    @staticmethod
    def generate_html_docs():
        print("  [INIT] Booting Sphinx/MkDocs documentation engine...")
        print("  [SCAN] Scanning abstract syntax trees for Docstrings...")
        
        # We programmatically extract the docstring using the `__doc__` dunder method!
        target_doc = DataParser.apply_modifier.__doc__
        
        print("\n  [RENDER] Successfully parsed the following Docstring into HTML:\n")
        print("="*50)
        print(target_doc)
        print("="*50)
        print("\n  [DEPLOY] HTML website automatically deployed to GitHub Pages.")


# ==============================================================================
# 6. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_documentation():
    section_header("Code Quality: Docstrings & Sphinx")
    
    DocumentationGenerator.generate_html_docs()
    
    print("\n  [ARCHITECTURE PROOF]")
    print("  By writing rigidly structured Docstrings, the codebase acts as its own ")
    print("  Source of Truth. The IDE auto-completes the parameter requirements, ")
    print("  and the CI/CD pipeline guarantees the API website is never out of date.")


def run_all_labs():
    demonstrate_documentation()


# ==============================================================================
# 7. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why are inline comments (e.g., `# loops through the array`) considered an anti-pattern compared to Docstrings and descriptive variable names?"
   Senior Answer: "Code Rot and Redundancy. If you write a variable named `x` and put a comment next to it saying `# x is the user's age`, you have created redundancy. Six months later, a developer renames `x` to `account_balance` but forgets to update the comment. The comment now mathematically lies to the next developer, causing a catastrophic logic bug. 'Code never lies; comments do.' By deleting the comment and naming the variable `user_age_years`, the code becomes mathematically self-documenting. Inline comments should *never* explain WHAT the code is doing (the code itself explains that); they should only ever explain WHY a non-obvious business decision was made."

2. Interviewer: "What is the architectural purpose of writing an `Example:` block inside a Google-style docstring, and what tool can leverage it?"
   Senior Answer: "Doctest Execution. When you write `>>> parser.apply_modifier(2.0)` inside the docstring, it serves as a visual example for humans reading the HTML documentation. However, Python has a built-in module called `doctest`. When executed, `doctest` mathematically scans the raw text of the docstrings, extracts the code following the `>>>` arrows, physically executes it in RAM, and asserts that the actual output matches the text on the next line. If they don't match, the CI/CD pipeline fails, mathematically guaranteeing that the examples in your API documentation are never out of sync with the underlying codebase."

3. Interviewer: "Explain how tools like Sphinx and MkDocs turn Python files into HTML websites."
   Senior Answer: "Introspection and Markdown Rendering. Tools like Sphinx (using the `autodoc` extension) do not just blindly read text files. They physically import the Python module into RAM during the CI/CD build process. They use Python's `inspect` module to mathematically crawl the object tree, extracting classes, methods, Type Hints, and the `__doc__` dunder attributes. They then pass this raw text through a Parser (like reStructuredText or Markdown), convert the structural tags into HTML/CSS components, and generate a static website. This ensures that the generated API Reference is mathematically identical to the actual executing Python code."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Code Quality (Documentation) Completed.")
