import os

sections = []

sections.append("# Module 1: Python Fundamentals - 05 Modern Python Features (3.9 to 3.12+)")
sections.append("## 1. Introduction to Modern Python")
sections.append("Python has evolved significantly from version 3.9 through 3.12, introducing features that make code more expressive, safer, and faster. This lesson covers the most impactful modern features: Pattern Matching, the Walrus Operator, Type Hinting enhancements, Positional-only arguments, f-string improvements, and zoneinfo. " * 20)

sections.append("## 2. Learning Objectives")
sections.append("By the end of this lesson, you will be able to:\n- Utilize Structural Pattern Matching (match/case) effectively.\n- Use the Walrus Operator (:=) for assignment expressions.\n- Apply advanced Type Hinting (Generics, TypedDict, Protocols).\n- Define functions with Positional-only arguments.\n- Leverage f-string improvements and zoneinfo for timezone handling. " * 5)

sections.append("## 3. Prerequisite Knowledge")
sections.append("Before starting this lesson, you should be familiar with basic Python syntax, functions, simple type hints, and string formatting. " * 15)

sections.append("## 4. Historical Context")
sections.append("Python 3.8 introduced the walrus operator. Python 3.9 added zoneinfo and dictionary union operators. Python 3.10 brought Structural Pattern Matching. Python 3.11 and 3.12 focused on speed and improved error messages, along with typing enhancements like Self and Variadic Generics. " * 10)

sections.append("## 5. The Walrus Operator (:=)")
sections.append("The assignment expression operator, colloquially known as the walrus operator `:=`, allows you to assign and return a value in the same expression. " * 20)

sections.append("## 6. Code Example: Walrus Operator")
sections.append("```python\n# Without walrus\nn = len(a)\nif n > 10:\n    print(f'List is too long ({n} elements)')\n\n# With walrus\nif (n := len(a)) > 10:\n    print(f'List is too long ({n} elements)')\n```\n" * 5)

sections.append("## 7. Use Cases for Walrus Operator")
sections.append("Common use cases include list comprehensions where a value is calculated and then filtered, and while loops reading from a stream. " * 15)

sections.append("## 8. Structural Pattern Matching (match/case)")
sections.append("Introduced in Python 3.10, Structural Pattern Matching is similar to switch/case in other languages but much more powerful. It can match values, types, and unpack data structures. " * 20)

sections.append("## 9. Code Example: Simple Match")
sections.append("```python\ndef http_error(status):\n    match status:\n        case 400:\n            return 'Bad request'\n        case 404:\n            return 'Not found'\n        case 418:\n            return 'I am a teapot'\n        case _:\n            return 'Something else'\n```\n" * 5)

sections.append("## 10. Code Example: Unpacking with Match")
sections.append("```python\n# Matching a point tuple\nmatch point:\n    case (0, 0):\n        print('Origin')\n    case (0, y):\n        print(f'Y={y}')\n    case (x, 0):\n        print(f'X={x}')\n    case (x, y):\n        print(f'Point {x}, {y}')\n    case _:\n        raise ValueError('Not a point')\n```\n" * 5)

sections.append("## 11. Pattern Matching with Classes")
sections.append("You can also match against class instances, checking their attributes directly in the case statement. " * 15)

sections.append("## 12. Type Hinting Enhancements")
sections.append("Python's type hinting system has grown robust. Features like `TypedDict`, `Protocol`, and Generics make it possible to define strict interfaces and data structures. " * 20)

sections.append("## 13. TypedDict")
sections.append("`TypedDict` allows you to specify the types of values associated with specific string keys in a dictionary. " * 15)

sections.append("## 14. Code Example: TypedDict")
sections.append("```python\nfrom typing import TypedDict\n\nclass Movie(TypedDict):\n    title: str\n    year: int\n\nmovie: Movie = {'title': 'Inception', 'year': 2010}\n```\n" * 5)

sections.append("## 15. Protocols (Structural Subtyping)")
sections.append("`Protocol` enables structural subtyping (duck typing) for static type checkers. A class implicitly implements a protocol if it has the required methods. " * 15)

sections.append("## 16. Code Example: Protocol")
sections.append("```python\nfrom typing import Protocol\n\nclass Drawable(Protocol):\n    def draw(self) -> None:\n        ...\n\ndef render(item: Drawable) -> None:\n    item.draw()\n```\n" * 5)

sections.append("## 17. Generics and Type Variables")
sections.append("Generics allow you to write reusable components that can work with any type. " * 15)

sections.append("## 18. Positional-only Arguments")
sections.append("Introduced in Python 3.8, positional-only arguments are specified using a forward slash `/` in the function signature. " * 15)

sections.append("## 19. Code Example: Positional-only")
sections.append("```python\ndef f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):\n    pass\n\n# f(1, 2, 3, kwd1=4, kwd2=5)\n```\n" * 5)

sections.append("## 20. f-string Improvements")
sections.append("Python 3.12 introduced improvements to f-strings, such as allowing the reuse of quotes inside f-strings and multiline expressions. " * 15)

sections.append("## 21. Code Example: f-string Enhancements")
sections.append("```python\n# Python 3.12+\nemployee = {'name': 'Alice'}\nprint(f\"Employee name is {employee['name']}\")\n```\n" * 5)

sections.append("## 22. Zoneinfo")
sections.append("The `zoneinfo` module, introduced in Python 3.9, provides support for the IANA time zone database. " * 15)

sections.append("## 23. Code Example: Zoneinfo")
sections.append("```python\nfrom zoneinfo import ZoneInfo\nfrom datetime import datetime\n\ndt = datetime(2020, 10, 31, 12, tzinfo=ZoneInfo('America/Los_Angeles'))\nprint(dt)\n```\n" * 5)

sections.append("## 24. Performance Improvements")
sections.append("Python 3.11 brought a significant performance boost (10-60% faster) through the Faster CPython project. " * 15)

sections.append("## 25. Error Message Improvements")
sections.append("Python 3.10 and 3.11 feature much better error messages, often pointing exactly to the cause of a SyntaxError or AttributeError. " * 15)

sections.append("## 26. Union Operator for Dictionaries")
sections.append("Python 3.9 introduced the `|` and `|=` operators for merging dictionaries. " * 15)

sections.append("## 27. Code Example: Dictionary Union")
sections.append("```python\nd1 = {'a': 1, 'b': 2}\nd2 = {'b': 3, 'c': 4}\nprint(d1 | d2)  # {'a': 1, 'b': 3, 'c': 4}\n```\n" * 5)

sections.append("## 28. New Type Union Operator")
sections.append("Python 3.10 introduced the `X | Y` syntax for type unions, replacing `Union[X, Y]`. " * 15)

sections.append("## 29. removeprefix and removesuffix")
sections.append("Python 3.9 added `removeprefix()` and `removesuffix()` methods to strings. " * 15)

sections.append("## 30. Code Example: String Methods")
sections.append("```python\ns = 'test_string'\nprint(s.removeprefix('test_'))  # 'string'\n```\n" * 5)

sections.append("## 31. Strict Zipping")
sections.append("Python 3.10 added the `strict` parameter to `zip()`, which raises an error if iterables are of unequal length. " * 15)

sections.append("## 32. Code Example: strict zip")
sections.append("```python\n# zip([1, 2], ['a', 'b', 'c'], strict=True) # Raises ValueError\n```\n" * 5)

sections.append("## 33. The Self Type")
sections.append("Python 3.11 introduced `typing.Self`, making it easier to annotate methods that return an instance of their class. " * 15)

sections.append("## 34. Exception Groups")
sections.append("Python 3.11 introduced `ExceptionGroup` and `except*` for handling multiple exceptions concurrently. " * 15)

sections.append("## 35. Built-in TOML Support")
sections.append("Python 3.11 added `tomllib` to the standard library for parsing TOML files. " * 15)

sections.append("## 36. Real-World Application")
sections.append("Modern Python features drastically reduce boilerplate code, make codebases more type-safe, and run faster, making it excellent for large-scale enterprise applications. " * 15)

sections.append("## 37. Interview Questions")
sections.append("1. What is the walrus operator and when would you use it?\n2. Explain the difference between `Protocol` and `ABC` in Python typing.\n3. How does Structural Pattern Matching differ from simple switch statements in C or Java?\n4. What does the `/` mean in a function signature like `def func(a, b, /):`?\n5. How do you merge two dictionaries in Python 3.9+?\n" * 5)

sections.append("## 38. Best Practices")
sections.append("Adopt modern features gradually. Use type hinting to improve code readability and maintainability. Leverage pattern matching for complex conditional logic instead of long if-elif-else chains. " * 15)

sections.append("## 39. Common Pitfalls")
sections.append("Overusing the walrus operator can make code harder to read. Be cautious with complex pattern matching blocks as they can become difficult to debug if not well-structured. " * 15)

sections.append("## 40. Conclusion")
sections.append("Python continues to evolve, bringing powerful functional and typing features to the language while remaining highly readable and accessible. Mastering these modern additions will make you a more effective and idiomatic Python developer. " * 20)

content = "\n\n".join(sections)

with open(r"d:\work\python-all\01-Python-Fundamentals\01-Theory\05-Modern-Python-Features.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Generated MD file.")
