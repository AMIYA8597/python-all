"""
## A. Concept Name
Modules and Packages in Python

## B. One-Sentence Definition
Modules are single Python files containing reusable code, while packages are directories containing multiple modules that structure large codebases.

## C. Why Does This Exist?
If all code were written in a single file, the file would quickly become millions of lines long, impossible to navigate, debug, or collaborate on. Modules and packages exist to break code down into logical, reusable, and isolated namespaces.

## D. Intuition
Think of writing code like organizing a household. Instead of putting all your belongings (variables, functions, classes) into a single giant pile in the middle of a room (one file), you put kitchen tools in the kitchen (a module) and bathroom supplies in the bathroom. The entire house with its categorized rooms is a package. 

## E. Real-Life Analogy
A **Module** is a single toolbox containing specific tools (e.g., a plumber's toolbox).
A **Package** is the entire hardware store containing many different toolboxes organized by aisles.
`import` is you going to the store to borrow a specific tool for your current task.

## F. Mental Model
File system == Code architecture.
- `something.py` -> Module `something`
- Folder `my_folder/` with `__init__.py` -> Package `my_folder`
- `sys.path` -> The list of addresses (directories) Python checks to find the module when you type `import`.

## G. Visual Explanation
Code Repository
├── main.py                (Imports from math_ops and data/loaders)
├── math_ops.py            <-- MODULE (Just a file)
└── data/                  <-- PACKAGE (Directory with __init__.py)
    ├── __init__.py        (Makes 'data' a package, can be empty)
    ├── loaders.py         <-- MODULE inside a package
    └── parsers.py         <-- MODULE inside a package

Memory space:
When `main.py` says `import math_ops`, Python:
1. Checks if `math_ops` is already in `sys.modules` (cache).
2. If not, searches directories in `sys.path` for `math_ops.py`.
3. Compiles it to bytecode (.pyc) if needed.
4. Executes the module's code top-to-bottom.
5. Puts the resulting module object in `sys.modules` and binds it to the local name `math_ops`.

## H. Formal Explanation
In Python, a module is an object of type `types.ModuleType` that serves as an organizational unit of code. It acts as an execution environment and a namespace. A package is a special kind of module that contains a `__path__` attribute, pointing to a directory. Python's import system uses `importlib` machinery, consisting of finders (to locate the module in `sys.path`) and loaders (to execute the module's code). To ensure performance and singleton behavior, all loaded modules are cached in the `sys.modules` dictionary. Subsequent imports of the same module simply return a reference from `sys.modules`.

## I. Mathematical Foundation (if applicable)
Not strictly applicable to imports, but consider a graph model: 
Modules form a Directed Acyclic Graph (DAG) of dependencies. 
Let G = (V, E) where V are modules and an edge (u, v) exists if u imports v.
If there is a cycle in this graph (u imports v, and v imports u), a "circular import" occurs, which can cause runtime errors if names are not fully initialized.

## J. From-Scratch Implementation (if applicable)
(See code below for the from-scratch implementation of MockSysModules).

## K. Library / Production Implementation (if applicable)
Python handles all this natively via the `importlib` standard library. Specifically, `importlib.import_module()` is the programmatic hook to dynamically load modules at runtime. The `sys` module also exposes `sys.modules` (the cache) and `sys.path` (the search paths).

## L. Trace (walk through example)
Step-by-step of `import math`:
1. `import math` is encountered.
2. Python checks `sys.modules['math']`.
3. If found, it binds the local variable `math` to that module object. DONE.
4. If not found, Python iterates through `sys.path` (list of directories).
5. It looks for `math.py`, `math` directory (package), or a built-in C-extension `math.so`/`math.dll`.
6. Once found, an empty module object is created and added to `sys.modules['math']`.
7. The code inside `math.py` is executed line by line. Everything defined (vars, funcs, classes) is added to the module's `__dict__`.
8. The local name `math` now points to this initialized module.

## M. Complexity
- **Time Complexity of Import:**
  - First import: O(N + K), where N is `sys.path` search time, K is the time to execute module-level code.
  - Subsequent imports: O(1) hash map lookup in `sys.modules`.
- **Space Complexity:** O(M) where M is the memory required for the module's attributes, loaded exactly once (Singleton).

## N. Common Mistakes
1. **Name Shadowing:** Naming your script `math.py` or `email.py`. When you `import math`, Python finds your local file first before the standard library, breaking standard tools.
2. **Circular Imports:** Module A imports Module B, but Module B imports Module A. If they depend on each other's uninitialized variables at the module level, Python raises an `ImportError` or `AttributeError`.
3. **`from module import *`**: Pollutes the current namespace. It makes it impossible to know where a function came from and can silently overwrite existing variables.

## O. Common Confusions
- **`import module` vs `from module import function`**:
  - Both execute the ENTIRE module file the first time!
  - `from X import Y` does NOT save memory or CPU time compared to `import X`. It just adds `Y` directly to your local namespace instead of making you type `X.Y`.
- **Module vs Script**:
  - A file run directly via `python file.py` has its `__name__` set to `"__main__"`.
  - The exact same file, if imported, has its `__name__` set to the filename (e.g., `"file"`).
  - This is why `if __name__ == "__main__":` is used: to run code only when executed as a script, not when imported.

## P. When To Use
- Break down files when they exceed ~500-1000 lines.
- Group related functionality (e.g., all database models in `models.py`).
- Use packages (directories) to group related modules (e.g., an `api/` package containing `routes.py`, `auth.py`, `responses.py`).

## Q. When NOT To Use
- Don't split code into too many tiny 10-line modules. Over-fragmentation makes the codebase exhausting to navigate.
- Avoid deeply nested packages (e.g., `pkg.subpkg.subsub.module`) unless writing a massive library.

## R. Trade-offs
- **Modularity vs. Cognitive Load:** While modules separate concerns effectively, having too many requires developers to frequently switch contexts and track cross-file dependencies.
- **Granularity vs. Performance:** Extremely deep package structures might slow down the initial application startup time slightly as Python traverses directories and checks `__init__.py` files.

## S. Debugging
- **ModuleNotFoundError**: The module doesn't exist, OR the directory containing it is not in `sys.path`.
  - *Fix*: Check spelling, verify your virtual environment is active, or append the directory to `sys.path`.
- **ImportError / Circular Import**: Usually happens when two files import each other.
  - *Fix*: Refactor shared code into a third module, or move the `import` statement inside a function (so it only runs when the function is called, not at load time).

## T. Memory Hook (a short memorable principle)
"Imports are Singleton Scripts."
Importing a file just runs the script top-to-bottom once, saves the result in a dictionary (`sys.modules`), and gives you a reference to it.

## U. Active Recall (questions before answers)
1. Does `from math import pi` use less memory than `import math`?
2. Why is `import *` considered bad practice?
3. How does Python prevent a module from being executed twice if imported in multiple files?
4. What is `sys.path`?

## V. Practice (exercises)
Exercise: Write a dynamic plugin loader. Given a list of strings representing module names, import them dynamically. If they don't exist, handle the error gracefully without crashing. (See `load_plugins` implementation below).

## W. Interview Question
Question: "Explain how you would temporarily modify the import path to load a module from a specific isolated directory, ensuring the path is cleaned up even if the import fails."
Solution: Use a context manager to modify `sys.path`. (See `isolated_import_path` implementation below).

## X. Project Connection
In real AI/ML systems like PyTorch or HuggingFace Transformers, `__init__.py` is used heavily for "API Flattening" and "Lazy Loading".

For example, a massive library might have a deep structure:
`transformers/models/bert/modeling_bert.py`

But users just want to type:
`from transformers import BertModel`

In HuggingFace, the `transformers/__init__.py` file imports `BertModel` from the deep sub-package and exposes it at the top level. Furthermore, they use custom lazy-loading logic in `__init__.py` (overriding `__getattr__`) so that heavy dependencies (like torch or tensorflow) are only imported when a specific class is actually accessed, drastically reducing the startup time of the package!
"""

import sys
import types
import importlib
import timeit
import os
from contextlib import contextmanager

# ==========================================
# J. From-Scratch Implementation
# ==========================================
# Let's simulate Python's internal import caching mechanism from scratch.

class MockSysModules:
    """Simulates sys.modules cache."""
    def __init__(self):
        self.cache = {}

    def get_or_load(self, name: str, code_str: str) -> types.ModuleType:
        # Step 1: Check cache (Singleton pattern)
        if name in self.cache:
            print(f"[Import] Cache hit for '{name}'. Returning existing module.")
            return self.cache[name]

        print(f"[Import] Cache miss for '{name}'. Loading module...")
        
        # Step 2: Create a new empty Module object
        mod = types.ModuleType(name)
        
        # Step 3: Put in cache BEFORE execution to handle circular imports!
        # (Real Python does this too)
        self.cache[name] = mod
        
        # Step 4: Execute the code within the module's namespace (its __dict__)
        try:
            exec(code_str, mod.__dict__)
        except Exception as e:
            # If execution fails, remove from cache and re-raise
            del self.cache[name]
            raise e
            
        print(f"[Import] Successfully loaded '{name}'.")
        return mod

# Let's see it in action
mock_sys = MockSysModules()

# We simulate the source code of a module 'math_helpers'
math_helpers_source = """
PI = 3.14159
def square(x):
    return x * x
print("  => math_helpers module is executing!")
"""

def demonstrate_import_system():
    print("\n--- Simulating First Import ---")
    math_mod1 = mock_sys.get_or_load("math_helpers", math_helpers_source)
    print("PI:", math_mod1.PI)
    
    print("\n--- Simulating Second Import ---")
    math_mod2 = mock_sys.get_or_load("math_helpers", math_helpers_source)
    
    print("\n--- Identity Check ---")
    print(f"Are they the exact same object in memory? {math_mod1 is math_mod2}")


# ==========================================
# V. Practice (exercises)
# ==========================================
def load_plugins(plugin_names: list) -> dict:
    """
    Dynamically loads a list of modules by their string names.
    Returns a dictionary mapping module name to the module object.
    """
    loaded_plugins = {}
    for name in plugin_names:
        try:
            # importlib.import_module is the programmatic equivalent of 'import name'
            module = importlib.import_module(name)
            loaded_plugins[name] = module
            print(f"Successfully loaded: {name}")
        except ModuleNotFoundError:
            print(f"Warning: Plugin '{name}' not found. Skipping.")
    return loaded_plugins


# ==========================================
# W. Interview Question Implementation
# ==========================================
@contextmanager
def isolated_import_path(path: str):
    """Context manager to safely prepend and remove a directory from sys.path."""
    sys.path.insert(0, path)
    try:
        yield
    finally:
        # Guarantee cleanup even if an exception occurs
        if path in sys.path:
            sys.path.remove(path)


if __name__ == "__main__":
    demonstrate_import_system()
    
    print("\n--- Practice Exercise ---")
    plugins = load_plugins(["math", "json", "fake_nonexistent_plugin"])
    print(f"Loaded {len(plugins)} plugins.")

    print("\n--- Interview Question Context Manager ---")
    dummy_path = "/path/to/secret/modules"
    print("sys.path length before:", len(sys.path))
    with isolated_import_path(dummy_path):
        print(f"Is dummy_path at sys.path[0]? {sys.path[0] == dummy_path}")
    print(f"Is dummy_path in sys.path after? {dummy_path in sys.path}")
