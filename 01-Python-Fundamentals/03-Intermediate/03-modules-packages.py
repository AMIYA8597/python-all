"""
# ==============================================================================
# LABORATORY: MODULES, PACKAGES, AND IMPORT MECHANICS
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Python's import system is notoriously confusing for beginners. Understanding 
# `sys.modules`, the `PYTHONPATH`, circular dependencies, and how `__init__.py` 
# works is mandatory for structuring large-scale AI applications, publishing 
# PyPI packages, and debugging "ModuleNotFoundError" in Docker containers.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the difference between a Module and a Package.
# - Understand how the `sys.path` determines import resolution.
# - Master the `sys.modules` cache (and why imports only run once).
# - Understand Circular Imports and how to fix them.
# - Master `__all__` for controlling public APIs.
# - Understand Absolute vs Relative Imports.
#
# ==============================================================================
"""

import sys
import importlib
from pathlib import Path

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MODULES VS PACKAGES
# ==============================================================================
def demonstrate_definitions():
    """
    A MODULE is just a single `.py` file.
    A PACKAGE is a directory containing an `__init__.py` file (Python < 3.3) 
    or just a directory of modules (Namespace Packages in Python 3.3+).
    """
    section_header("Modules vs Packages")
    
    # We are currently in a module!
    print(f"Current module name: {__name__}")
    
    if __name__ == "__main__":
        print("Because we ran this file directly, Python named it '__main__'.")
        print("If we imported this file from elsewhere, its name would be '03-modules-packages'.")


# ==============================================================================
# 4. SYS.PATH (WHERE PYTHON LOOKS)
# ==============================================================================
def demonstrate_sys_path():
    """
    When you do `import foo`, Python searches for `foo.py` or a folder `foo`
    in the directories listed in `sys.path`.
    """
    section_header("sys.path (Import Resolution)")
    
    print("Python searches these directories in order:")
    for i, path in enumerate(sys.path[:5]):
        # The first entry (sys.path[0]) is ALWAYS the directory containing the running script!
        print(f" {i}: {path if path else 'Current Directory'}")
        
    print("...")
    
    # HACKING SYS.PATH (Common in legacy ML projects)
    # If you want to import a module from a completely different folder,
    # you can dynamically append to sys.path at runtime.
    # WARNING: This is an anti-pattern. Use proper packaging (setup.py/pyproject.toml) instead.
    
    fake_path = "/path/to/secret/ml_models"
    if fake_path not in sys.path:
        sys.path.append(fake_path)
    print(f"\nAdded {fake_path} to sys.path.")
    print("Python will now look there for imports!")


# ==============================================================================
# 5. THE IMPORT CACHE (SYS.MODULES)
# ==============================================================================
def demonstrate_sys_modules():
    """
    When you import a module, Python executes its top-level code EXACTLY ONCE.
    It then caches the resulting module object in a dictionary called `sys.modules`.
    Any subsequent imports of the same module just fetch it from this dictionary.
    """
    section_header("The Import Cache (sys.modules)")
    
    # Let's check if 'math' is cached
    print(f"Is 'math' in sys.modules? {'math' in sys.modules}")
    
    import math
    print(f"After importing, is 'math' in sys.modules? {'math' in sys.modules}")
    
    # If we modify a module, we can FORCE Python to reload it and re-execute 
    # its top-level code using importlib.reload(). This is useful in Jupyter Notebooks.
    print("\nForce reloading the math module...")
    importlib.reload(math)
    print("Reload successful.")


# ==============================================================================
# 6. CIRCULAR IMPORTS
# ==============================================================================
def demonstrate_circular_imports():
    """
    A circular import occurs when Module A imports Module B, and Module B 
    imports Module A at the top level.
    
    Because Python executes top-level code sequentially, Module A is only partially 
    initialized when it triggers Module B, which then tries to import from Module A, 
    resulting in an ImportError (or AttributeError).
    """
    section_header("Circular Imports")
    
    print("""
HOW TO FIX CIRCULAR IMPORTS:
1. Architectural Fix (Best): Extract the shared code into a new Module C, 
   and have both A and B import C.
   
2. Deferred Import (Hack): Move the `import B` statement INSIDE the function 
   that needs it, rather than at the top of the file.
   
   def process_data():
       import B  # Deferred import
       B.do_something()
       
3. Type Checking Import (typing.TYPE_CHECKING): If the import is only needed 
   for type hints, wrap it:
   
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from B import ComplexModelType
    """)


# ==============================================================================
# 7. __ALL__ AND PUBLIC APIS
# ==============================================================================

# If someone does `from module import *`, they get everything defined here.
# To restrict what is exported, we define `__all__`.
__all__ = ["public_function", "PublicClass"]

def public_function():
    pass

class PublicClass:
    pass

def _private_function():
    # The leading underscore signals it is internal.
    # It will NOT be exported when using `import *` if __all__ is not defined.
    pass

def demonstrate_all():
    section_header("__all__ and Public APIs")
    print(f"This module explicitly exports: {__all__}")
    print("Use __all__ in __init__.py files to define the public API of a package.")


# ==============================================================================
# 8. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What does `if __name__ == "__main__":` do?
   Answer: It checks if the script is being executed directly by the user (via `python script.py`). If the file is being imported by another module, `__name__` will be the module's name instead, so the block won't execute.

2. Why does top-level print() output only show up the FIRST time you import a module?
   Answer: Python executes the module code only once. It caches the module object in `sys.modules`. Future imports just pull a reference from `sys.modules`.

3. What is the first entry in `sys.path`?
   Answer: `sys.path[0]` is always the directory containing the script that was used to invoke the Python interpreter. This allows relative scripts in the same folder to be imported easily.

4. How do you resolve a Circular Import without changing the architecture?
   Answer: Move the import statement from the top of the file to INSIDE the function or method that actually uses it (Deferred Import).
"""

if __name__ == "__main__":
    demonstrate_definitions()
    demonstrate_sys_path()
    demonstrate_sys_modules()
    demonstrate_circular_imports()
    demonstrate_all()
    print("\n[SUCCESS] Laboratory: Modules and Packages Completed.")
