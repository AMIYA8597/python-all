# Compiler Lexer Project Specification

## 1. Introduction: What is a Lexer and Why Does it Exist?
A Lexical Analyzer, or "Lexer" (also called a tokenizer), is the first phase of a compiler or interpreter. It takes raw source code as a string of characters and converts it into a sequence of meaningful chunks called "Tokens". 

**Why does it exist?** 
Imagine trying to read a book by looking at each individual letter rather than grouping letters into words. A lexer groups characters into "words" (tokens) that the parser can then understand to form "sentences" (syntax trees). 
**Industry Use Cases:**
- **Compilers & Interpreters:** GCC, Clang, CPython, Node.js V8 all start with lexical analysis.
- **Syntax Highlighting:** IDEs (VSCode, PyCharm) use lexers to colorize code.
- **Data Parsing:** JSON parsers, configuration file parsers (YAML, TOML).
- **Search Engines:** Tokenizing text for indexing.

---

## 2. Explanations

### Beginner Explanation
Think of a lexer like a person reading a continuous stream of letters without spaces and breaking them down into recognizable words, numbers, and punctuation marks. 
If you have `x = 5 + 10`, the lexer reads it character by character and outputs:
- Identifier (`x`)
- Operator (`=`)
- Number (`5`)
- Operator (`+`)
- Number (`10`)

### Deep Technical Explanation
Under the hood, lexers are often implemented using **Finite State Machines (FSMs)** or **Regular Expressions (Regex)**. 
- A state machine reads a character, transitions to a new state based on that character, and continues until it hits an accepting state for a token (e.g., encountering a space after reading digits means the number is complete).
- Tokens are typically represented as objects or tuples containing a `type` (e.g., `TOKEN_NUMBER`) and a `value` (e.g., `5`).
- The lexer must also keep track of line numbers and column numbers for error reporting (e.g., "Unexpected character '$' at line 2, col 5").

---

## 3. Practical Real-World Example
In a real-world scenario, you might write a lexer to parse a custom configuration language. 
Consider a file like:
```
server_port = 8080
enable_logging = true
```
The lexer would convert this to:
`[ID(server_port), ASSIGN, INT(8080), NEWLINE, ID(enable_logging), ASSIGN, BOOL(true)]`

---

## 4. Internal Details and Advanced Concepts
- **Lookahead:** Sometimes a lexer needs to look at the next character to determine the token. For example, to distinguish between `=` (assignment) and `==` (equality).
- **Maximal Munch Rule:** A lexer generally matches the longest possible string for a token. Given `>=` it matches the single operator `>=` rather than `>` followed by `=`.
- **Lexical Error Handling:** When encountering an invalid character, a robust lexer will report an error, skip the character, and continue lexing to find further errors.

---

## 5. Considerations

### Common Mistakes
- **Ignoring Whitespace incorrectly:** Depending on the language, whitespace might be ignored (C++) or significant (Python indentation).
- **String Parsing:** Not handling escape characters (like `\n` or `\"`) properly within string literals.

### Performance Considerations
- **String Slicing:** Avoid excessive string slicing in Python, which creates copies. Instead, maintain a `pos` index and use regex matching at that index.
- **Regex Compilation:** If using regex, compile them ahead of time (`re.compile`) to improve performance.

### Security Concerns
- **ReDoS (Regular Expression Denial of Service):** If using regex, poorly written expressions can take exponential time on certain inputs, leading to DoS attacks.
- **Buffer Overflows:** More common in C/C++, but in Python, generating massive tokens (e.g., parsing a 10MB string literal) could cause MemoryErrors.

---

## 6. Interview Questions
1. What is the difference between a lexer and a parser?
   *Answer: A lexer breaks characters into tokens. A parser takes tokens and builds an abstract syntax tree (AST), checking grammar.*
2. How does the "maximal munch" principle work?
   *Answer: It dictates that the lexer should match the longest possible prefix of the remaining input that forms a valid token.*
3. How would you handle string literals with escape sequences in a lexer?
   *Answer: By defining a state or regex that allows `\"` or `\\` inside quotes without terminating the token early.*

---

## 7. Practical Exercises
1. **Basic Extension:** Modify the lexer to support floating-point numbers (e.g., `3.14`).
2. **String Support:** Add support for double-quoted string literals `"like this"`.
3. **Comments:** Make the lexer ignore single-line comments starting with `//` or `#`.
