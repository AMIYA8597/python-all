import re
from typing import List, NamedTuple, Optional, Dict

class Token(NamedTuple):
    """
    Represents a lexical token.
    type: The category of the token (e.g., 'NUMBER', 'IDENTIFIER').
    value: The actual string value matched.
    line: The line number where the token was found.
    column: The column number where the token starts.
    """
    type: str
    value: str
    line: int
    column: int


class LexicalError(Exception):
    """Exception raised for errors in the lexical analysis phase."""
    pass


class Lexer:
    """
    A professional-grade lexical analyzer (lexer) for a simple programming language.
    Uses pre-compiled regular expressions for token specification to ensure performance.
    """
    
    # Token specification using Regex
    # Order matters: we match longest/most specific first (e.g. >= before >)
    TOKEN_SPECIFICATION = [
        ('NUMBER',       r'\d+(\.\d*)?'),      # Integer or decimal number
        ('ASSIGN_ADD',   r'\+='),              # Add and assign
        ('ASSIGN_SUB',   r'-='),               # Subtract and assign
        ('EQ',           r'=='),               # Equality
        ('NEQ',          r'!='),               # Inequality
        ('LEQ',          r'<='),               # Less than or equal
        ('GEQ',          r'>='),               # Greater than or equal
        ('ASSIGN',       r'='),                # Assignment
        ('LT',           r'<'),                # Less than
        ('GT',           r'>'),                # Greater than
        ('ID',           r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
        ('OP',           r'[+\-*/]'),          # Arithmetic operators
        ('LPAREN',       r'\('),               # Left parenthesis
        ('RPAREN',       r'\)'),               # Right parenthesis
        ('LBRACE',       r'\{'),               # Left brace
        ('RBRACE',       r'\}'),               # Right brace
        ('COMMA',        r','),                # Comma separator
        ('SEMI',         r';'),                # Statement terminator
        ('STRING',       r'"(?:[^"\\]|\\.)*"'),# String literals with escape support
        ('COMMENT',      r'#.*'),              # Single line comments
        ('NEWLINE',      r'\n'),               # Line endings
        ('SKIP',         r'[ \t]+'),           # Skip over spaces and tabs
        ('MISMATCH',     r'.'),                # Any other character (error)
    ]

    # Pre-compile the regex pattern for performance
    # Joins all specifications into a single named regex group pattern
    REGEX = re.compile('|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATION))

    # Reserved language keywords
    KEYWORDS: Dict[str, str] = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'return': 'RETURN',
        'def': 'DEF',
        'true': 'TRUE',
        'false': 'FALSE'
    }

    def __init__(self, code: str):
        """
        Initializes the Lexer with source code.
        """
        self.code = code
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """
        Analyzes the source code and returns a list of Tokens.
        Raises LexicalError on invalid characters.
        """
        line_num = 1
        line_start = 0
        
        # Iterate over all regex matches in the source code
        for mo in self.REGEX.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group(kind)
            column = mo.start() - line_start + 1
            
            if kind == 'NUMBER':
                # Convert to float if decimal, otherwise int (kept as string in token value for simplicity,
                # actual parsing might convert type).
                pass
            elif kind == 'ID':
                # Check if the identifier is a reserved keyword
                kind = self.KEYWORDS.get(value, 'ID')
            elif kind == 'STRING':
                # Strip quotes from the string literal
                value = value[1:-1]
            elif kind == 'COMMENT':
                # Ignore comments
                continue
            elif kind == 'NEWLINE':
                # Update line number and start position
                line_num += 1
                line_start = mo.end()
                continue
            elif kind == 'SKIP':
                # Ignore whitespace
                continue
            elif kind == 'MISMATCH':
                # Throw a lexical error for invalid characters
                raise LexicalError(
                    f"Unexpected character {value!r} at line {line_num}, column {column}"
                )
            
            # Append valid token
            self.tokens.append(Token(kind, value, line_num, column))
            
        # Optional: Add an EOF token to signify end of file
        self.tokens.append(Token('EOF', '', line_num, len(self.code) - line_start + 1))
        
        return self.tokens

# =====================================================================
# Test Execution Block
# =====================================================================
if __name__ == '__main__':
    sample_code = '''
    def calculate_sum(a, b) {
        # This is a comment
        result = a + b;
        if (result >= 10) {
            msg = "Large sum";
            return true;
        } else {
            return false;
        }
    }
    '''
    
    print(f"Tokenizing sample code:\n{sample_code}\n")
    
    try:
        lexer = Lexer(sample_code)
        tokens = lexer.tokenize()
        
        print(f"{'TYPE':<15} {'VALUE':<15} {'LINE':<6} {'COL':<6}")
        print("-" * 45)
        for token in tokens:
            print(f"{token.type:<15} {token.value:<15} {token.line:<6} {token.column:<6}")
            
    except LexicalError as e:
        print(f"Lexical Error: {e}")
