# Advanced Calculator - Project Specification

## 1. Project Overview
This project involves building a robust, extensible, and production-ready "Advanced Calculator" in Python. It goes beyond simple arithmetic, introducing concepts like expression parsing, plugin architectures for extensibility, error handling, logging, and comprehensive unit testing.

**Why does this project exist?**
To transition learners from writing basic procedural scripts to building structured, object-oriented applications that mimic real-world software engineering practices. It demonstrates how to handle complex string parsing (a very common task in compilers and data ingestion pipelines) and how to design software that can be easily updated in the future.

**Industry Use Cases:**
- **Expression Evaluation:** Parsing engines used in data analysis tools (like pandas `eval()`), spreadsheet software (Excel formulas), and rule engines in fintech.
- **Plugin Architectures:** Used extensively in IDEs (VSCode), web browsers, and media players to allow third-party developers to add functionality without modifying the core codebase.

---

## 2. Architecture & Design

### Core Components
1.  **Lexer/Tokenizer:** Takes a raw string input (e.g., `"3 + 4 * (2 - 1)"`) and breaks it down into meaningful tokens (Numbers, Operators, Parentheses).
2.  **Parser (Abstract Syntax Tree - AST):** Takes the sequence of tokens and builds a tree structure representing the mathematical hierarchy, enforcing order of operations (PEMDAS/BODMAS).
3.  **Evaluator:** Traverses the AST to compute the final result.
4.  **Plugin Manager:** Dynamically loads external modules to add new mathematical functions (e.g., `sin`, `cos`, `log`) without hardcoding them into the evaluator.
5.  **REPL (Read-Eval-Print Loop) CLI:** The user interface that continuously accepts user input, processes it, and prints the result.

### System Diagram (Mental Model)
```text
[User Input] -> (REPL) -> [String] -> (Lexer) -> [Tokens] -> (Parser) -> [AST] -> (Evaluator) -> [Result] -> (REPL)
                                                                                     ^
                                                                                     |
                                                                              (Plugin Manager)
```

---

## 3. Requirements Specification

### Functional Requirements
- **Basic Arithmetic:** Support addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), and exponentiation (`^`).
- **Precedence & Grouping:** Correctly evaluate expressions using standard mathematical order of operations and parentheses.
- **Variables:** Allow the user to store results in memory variables (e.g., `x = 10`, then `x * 2`).
- **Extensibility:** Support a plugin system where new functions can be dropped into a `plugins/` directory and immediately used (e.g., `sin(90)`).
- **History:** Keep track of the last 10 calculations and allow the user to view them with a `history` command.

### Non-Functional Requirements
- **Error Handling:** Must gracefully handle division by zero, malformed expressions, and unknown variables. The application must *never* crash abruptly.
- **Logging:** Log all user inputs, calculated results, and errors to a file (`calc.log`) for auditing and debugging.
- **Testing:** Must achieve at least 90% test coverage using `pytest`.
- **Typing:** Code must be fully type-hinted and pass `mypy` static analysis.

---

## 4. Implementation Details & Beginner to Advanced Concepts

### Beginner Concepts Applied
- **Variables & Data Types:** Storing numbers and strings.
- **Control Flow:** `while` loops for the REPL, `if/else` for routing commands.
- **Functions:** Breaking down operations into small, testable units.

### Advanced Concepts Applied
- **Recursive Descent Parsing:** A classic computer science algorithm for parsing context-free grammars. You will implement mutually recursive functions (e.g., `parse_expression()`, `parse_term()`, `parse_factor()`).
- **The Strategy / Command Pattern:** Encapsulating operations into classes to easily swap out implementations.
- **Dynamic Imports:** Using Python's `importlib` to load Python files from a directory at runtime for the plugin system.
- **Logging Configuration:** Setting up Python's built-in `logging` module with formatters and file handlers.

---

## 5. Security & Performance Considerations

### Security Concerns
- **Eval() Vulnerability:** Beginners often try to build calculators using Python's built-in `eval()` function (e.g., `eval("2 + 2")`). **This is a massive security risk.** If a user inputs `eval("__import__('os').system('rm -rf /')")`, it will execute system commands.
- **Mitigation:** We will *strictly* parse the string ourselves and build an AST, making code injection impossible. Our evaluator only knows how to process mathematical nodes, not arbitrary Python code.

### Performance Considerations
- The parsing phase creates many small objects (Tokens, AST Nodes). For extreme performance, one might use a Pratt Parser or a shunting-yard algorithm, but Recursive Descent is preferred here for its readability and educational value.
- Caching/Memoization can be added to the evaluator for repetitive function calls (e.g., if a plugin calculates a heavy Fibonacci sequence).

---

## 6. Deployment & Packaging

To make this project professional, it should be installable via pip.

1.  **Directory Structure:**
    ```text
    advanced_calc/
    ├── src/
    │   └── adv_calc/
    │       ├── __init__.py
    │       ├── lexer.py
    │       ├── parser.py
    │       ├── evaluator.py
    │       ├── cli.py
    │       └── plugins/
    ├── tests/
    │   ├── test_lexer.py
    │   └── test_parser.py
    ├── pyproject.toml
    └── README.md
    ```
2.  **pyproject.toml:** Define the build system and entry points so that installing the package gives the user a `calc` command in their terminal.

---

## 7. Interview Questions & Exercises

### Interview Questions
1.  **"Why didn't you just use Python's built-in `eval()` for this project?"**
    *Answer: Security and control. `eval()` executes arbitrary Python code, making it vulnerable to injection attacks. Building a custom lexer/parser ensures only mathematical expressions are evaluated, and it allows us to easily add custom syntax or variables that `eval()` wouldn't understand natively.*
2.  **"How does your plugin system work, and what are the advantages of this architecture?"**
    *Answer: It uses dynamic importing (`importlib`) to scan a directory for Python files, looking for classes that implement a specific interface (e.g., a `BasePlugin` class). The advantage is the Open-Closed Principle: the core calculator is closed for modification, but open for extension. We can add new features without risking breaking the core parser.*

### Practical Exercises to Extend the Project
1.  **Boolean Logic:** Add support for operators like `>`, `<`, `==`, `AND`, and `OR`.
2.  **Complex Numbers:** Modify the lexer and evaluator to handle inputs like `3 + 4i`.
3.  **GUI:** Build a `tkinter` or `PyQt` graphical interface that utilizes your core calculator engine backend.
