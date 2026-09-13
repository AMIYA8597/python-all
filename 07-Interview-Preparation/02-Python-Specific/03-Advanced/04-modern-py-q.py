"""
Modern Python Features

Learning Objectives:
1. Utilize the Walrus Operator (:=) for concise assignment expressions (Python 3.8+).
2. Master Structural Pattern Matching (match/case) for complex control flow (Python 3.10+).
3. Understand positional-only (/) and keyword-only (*) arguments.
4. Use modern dataclasses for boilerplate-free class definitions.

Concept Explanation:
- The Walrus Operator allows assignment and evaluation in the same expression.
- Pattern Matching is akin to switch/case but much more powerful, allowing data extraction and structural validation.
- Dataclasses automatically generate `__init__`, `__repr__`, `__eq__`, etc., based on type hints.

Interview Focus:
- How does pattern matching differ from a standard switch statement?
- Provide an example where the walrus operator reduces code duplication.
- Explain keyword-only arguments.
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional

# ==========================================
# 1. The Walrus Operator (:=)
# ==========================================

def get_valid_emails(texts: List[str]) -> List[str]:
    """Extracts valid emails using the walrus operator to avoid double evaluation."""
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    valid = []
    for text in texts:
        # Assign and evaluate in one step
        if (match := pattern.match(text)) is not None:
            valid.append(match.group(0))
    return valid

# ==========================================
# 2. Structural Pattern Matching
# ==========================================

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Circle:
    center: Point
    radius: float

def describe_shape(shape: any) -> str:
    """Uses pattern matching to handle different structures."""
    match shape:
        case Point(x=0, y=0):
            return "Origin point"
        case Point(x=x, y=y) if x == y:
            return f"Point on the diagonal line (x={x})"
        case Point(x, y):
            return f"Point at ({x}, {y})"
        case Circle(center=Point(0, 0), radius=r):
            return f"Circle centered at origin with radius {r}"
        case _:
            return "Unknown shape"

# ==========================================
# 3. Argument Specifiers (/, *)
# ==========================================

# positional_only_arg must be passed by position
# keyword_only_arg must be passed by keyword
def complex_func(positional_only, /, standard, *, keyword_only):
    return (positional_only, standard, keyword_only)

# ==========================================
# 4. Dataclasses
# ==========================================

@dataclass(order=True)
class Task:
    priority: int
    description: str
    completed: bool = False
    tags: List[str] = field(default_factory=list)

def test_modern_features():
    # Test Walrus
    emails = ["invalid", "test@example.com", "bad email", "admin@site.org"]
    assert get_valid_emails(emails) == ["test@example.com", "admin@site.org"]
    
    # Test Pattern Matching
    p1 = Point(0, 0)
    p2 = Point(5, 5)
    p3 = Point(3, 4)
    c1 = Circle(Point(0, 0), 10.5)
    
    assert describe_shape(p1) == "Origin point"
    assert describe_shape(p2) == "Point on the diagonal line (x=5)"
    assert describe_shape(p3) == "Point at (3, 4)"
    assert describe_shape(c1) == "Circle centered at origin with radius 10.5"
    assert describe_shape("Not a shape") == "Unknown shape"
    
    # Test Arguments
    # Valid:
    res = complex_func(1, standard=2, keyword_only=3)
    assert res == (1, 2, 3)
    # Invalid: complex_func(positional_only=1, standard=2, keyword_only=3)
    
    # Test Dataclass
    t1 = Task(priority=2, description="Write tests")
    t2 = Task(priority=1, description="Fix bugs")
    assert repr(t1) == "Task(priority=2, description='Write tests', completed=False, tags=[])"
    # Testing ordering
    assert t2 < t1 # Because priority 1 < priority 2
    
    print("All modern feature tests passed!")

if __name__ == "__main__":
    test_modern_features()
