"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (COMPILER LEXICAL ANALYSIS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer tries to write a custom scripting language for their game engine. 
# They use `string.split(" ")` to separate the code into words, and then run a 
# massive `if/else` block on every word. When a user types `print("Hello World")`, 
# the script mathematically explodes because there are no spaces separating the 
# function name from the parentheses.
#
# A senior compiler engineer understands "Lexical Analysis". Before the computer 
# attempts to understand what the code *means* (Parsing), it must mathematically 
# classify what the text *is* (Lexing). They build a Regex-powered "Lexer". The 
# Lexer scans `print("Hello")` and instantly shatters it into a stream of absolute 
# mathematical Tokens: `[IDENTIFIER:print]`, `[PUNCTUATION:(]`, `[STRING:"Hello"]`, 
# `[PUNCTUATION:)]`. The Parser can now execute this stream flawlessly.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architecture of a Compiler Frontend (Lexical Analysis).
# - Execute Regular Expressions (Regex) for algorithmic pattern matching.
# - Generate a strict stream of immutable Token objects.
#
# ==============================================================================
"""

import re
from typing import List, NamedTuple, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE TOKEN ARCHITECTURE
# ==============================================================================
# A Token is a mathematical abstraction of raw text.
# The string "=" is just a character. The Token [ASSIGN_OP, "="] is a compiler directive!
class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


# ==============================================================================
# 4. THE LEXER (THE SCANNER)
# ==============================================================================
class Lexer:
    """
    The Lexer mathematically scans raw source code from left to right.
    It uses a dictionary of Regular Expressions to identify mathematical boundaries.
    """
    def __init__(self):
        # The exact mathematical order of these rules is hyper-critical!
        # If we put IDENTIFIER before KEYWORD, the word "if" will be misclassified 
        # as a variable name instead of a reserved keyword!
        self.rules = [
            ('COMMENT',    r'#.*'),                    # # followed by anything
            ('STRING',     r'"[^"]*"'),                # " followed by anything but ", ending with "
            ('FLOAT',      r'\d+\.\d+'),               # 10.5
            ('INTEGER',    r'\d+'),                    # 10
            ('KEYWORD',    r'\b(?:if|else|while|def|return)\b'), # Exact word matches
            ('IDENTIFIER', r'[a-zA-Z_]\w*'),           # Variable names (e.g., my_var_1)
            ('OPERATOR',   r'[+\-*/=<>!]+'),           # Math and Comparison ops
            ('PUNCTUATION',r'[(),:{}\[\]]'),           # Parentheses, brackets, colons
            ('NEWLINE',    r'\n'),                     # Line breaks (for tracking line numbers)
            ('WHITESPACE', r'[ \t]+'),                 # Spaces and Tabs
            ('MISMATCH',   r'.')                       # Anything else is a fatal syntax error!
        ]
        
        # We mathematically fuse all the Regex patterns into ONE giant OR statement!
        # Syntax: (?P<NAME>PATTERN) creates a named capture group in Python.
        regex_parts = []
        for name, pattern in self.rules:
            regex_parts.append(f'(?P<{name}>{pattern})')
            
        self.master_regex = re.compile('|'.join(regex_parts))

    def tokenize(self, source_code: str) -> List[Token]:
        """Executes the mathematical scan."""
        tokens = []
        line_num = 1
        line_start_idx = 0
        
        # We ask the Regex Engine to find ALL matches in the source code sequentially!
        for match in self.master_regex.finditer(source_code):
            # `lastgroup` mathematically tells us WHICH of the rules was triggered!
            token_type = match.lastgroup
            token_value = match.group()
            
            # We calculate the exact Column Number for Error Reporting!
            column_num = match.start() - line_start_idx
            
            if token_type == 'NEWLINE':
                line_num += 1
                line_start_idx = match.end()
                continue
                
            elif token_type == 'WHITESPACE' or token_type == 'COMMENT':
                # We mathematically discard spaces and comments! The Parser doesn't care about them!
                continue
                
            elif token_type == 'MISMATCH':
                # We encountered an illegal character (e.g., a random @ symbol)
                raise SyntaxError(f"Lexical Error on Line {line_num}, Col {column_num}: Unexpected character '{token_value}'")
                
            # If it's a valid token, we lock it into the Stream!
            token = Token(token_type, token_value, line_num, column_num)
            tokens.append(token)
            
        return tokens


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_lexer():
    section_header("Project: Compiler Lexical Analysis")
    
    lexer = Lexer()
    
    # We write a snippet of custom programming language code!
    raw_source_code = """
    # Calculate the speed of light
    def calculate_speed(distance, time):
        if time == 0:
            return "ERROR"
        speed = distance / time
        return speed
    """
    
    print("  [PHASE 1: THE RAW SOURCE CODE]")
    print(raw_source_code)
    
    print("  [PHASE 2: THE TOKEN STREAM]")
    print("  Executing Mathematical Lexical Analysis...")
    
    token_stream = lexer.tokenize(raw_source_code)
    
    for t in token_stream:
        # We visually align the output for easy reading
        print(f"    Line {t.line:02d} | Col {t.column:02d} | {t.type:<12} | {t.value}")
        
    print("\n  [SUCCESS] The chaotic string was successfully shattered into 23 immutable Tokens.")
    print("  The Parser can now execute this stream mathematically.")


def run_all_labs():
    demonstrate_lexer()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why do we mathematically discard `WHITESPACE` and `COMMENT` tokens in the Lexer? Why not pass them to the Parser?"
   Senior Answer: "Abstract Syntax Tree (AST) Optimization. The Parser's job is to mathematically prove that the grammar of the code is valid (e.g., making sure an `if` statement has a condition). If the Lexer passes Spaces and Comments to the Parser, the Parser would have to mathematically account for them in every single grammar rule (`IF_TOKEN + SPACE + CONDITION + SPACE + COLON`). This would cause a catastrophic explosion in compiler complexity. By discarding non-executable text at the Lexical Phase, the Parser receives a mathematically pure stream of executable logic, drastically reducing CPU cycles during compilation."

2. Interviewer: "In our Regex Rules, why must the `KEYWORD` rule mathematically appear BEFORE the `IDENTIFIER` rule?"
   Senior Answer: "Regex Priority Resolution. The word 'def' mathematically satisfies the condition for an Identifier (`[a-zA-Z_]\\w*`). If the `IDENTIFIER` rule was evaluated first, the Lexer would incorrectly classify 'def' as a variable name. The Parser would then crash because it was expecting a Function Declaration, but received a random variable instead. By strictly enforcing rule order, the Regex engine checks if the word is a reserved `KEYWORD` first. If it is, it locks in the Token and stops checking. Only if the word fails the Keyword check does it mathematically fall through and become classified as a standard Identifier."

3. Interviewer: "If the Lexer only cares about classifying characters, what mathematically happens in the next phase (The Parser)?"
   Senior Answer: "Context and Grammar Validation. The Lexer is mathematically 'Context-Free'. It knows that `=` is an Operator and `5` is an Integer, but it has absolutely no idea if the code is actually valid. A user could type `5 = = = if`. The Lexer will happily generate $4$ perfect Tokens for that garbage string without throwing an error. The Parser receives those Tokens and runs them through a 'Context-Free Grammar' (CFG). It realizes that three consecutive assignment operators followed by an 'if' keyword is mathematically impossible in the language's grammar, and *that* is when the fatal Syntax Error is thrown."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Compiler Lexer) Completed.")
