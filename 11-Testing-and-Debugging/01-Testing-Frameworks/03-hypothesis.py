"""
# ==============================================================================
# LABORATORY: TESTING AND DEBUGGING (PROPERTY-BASED TESTING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer writes a string sorting function. To test it, they write 
# three Unit Tests: sorting "cba" to "abc", sorting an empty string, and sorting 
# a pre-sorted string. The tests pass. In Production, a user inputs a string 
# containing a zero-width Arabic Unicode character (`\\u200B`), and the server 
# mathematically explodes, causing an outage. The junior developer failed because 
# humans are mathematically incapable of imagining every possible edge case.
#
# A senior software engineer uses Property-Based Testing (via the `hypothesis` library). 
# Instead of hardcoding 3 examples, they mathematically declare the "Properties" of 
# a sorted string (e.g., "The output length must equal the input length"). They 
# command the `hypothesis` engine to violently bombard the function with thousands 
# of randomly generated, mathematically hostile inputs (Unicode, Null bytes, massive 
# integers). If the code has a flaw, `hypothesis` will find the exact string that 
# breaks it, automatically shrink it to the smallest possible failing example, and 
# hand it to the engineer for fixing.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Property-Based Testing concepts.
# - Execute algorithmic bombardment using `hypothesis` strategies.
# - Architect mathematical invariants (Properties) for validation.
#
# ==============================================================================
"""

import unittest

# Gracefully handle Hypothesis dependency
try:
    from hypothesis import given, settings, strategies as st
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE BUSINESS LOGIC (THE CODE WE ARE TESTING)
# ==============================================================================
class StringAlgorithms:
    """A collection of string manipulation logic."""
    
    @staticmethod
    def reverse_string(text: str) -> str:
        """Mathematically reverses a string."""
        return text[::-1]
        
    @staticmethod
    def run-length-encode(text: str) -> str:
        """
        Compresses a string: "AABBB" -> "2A3B"
        (Intentionally buggy to demonstrate Hypothesis finding the flaw!)
        """
        if not text:
            return ""
            
        encoded = ""
        current_char = text[0]
        count = 0
        
        for char in text:
            # THE BUG: If the user inputs a literal integer like "5A", 
            # our encoding output will be "151A".
            # The decompressor won't know if it's "15" of "1A" or "1" of "5" and "1" of "A"!
            if char == current_char:
                count += 1
            else:
                encoded += f"{count}{current_char}"
                current_char = char
                count = 1
                
        encoded += f"{count}{current_char}"
        return encoded


# ==============================================================================
# 4. THE HYPOTHESIS ARCHITECTURE (PROPERTY-BASED TESTS)
# ==============================================================================
# We define "Mathematical Properties" that must ALWAYS be true, no matter the input!

if HAS_LIBS:
    class TestStringAlgorithms(unittest.TestCase):
        
        # --- TEST 1: REVERSE STRING INVARIANTS ---
        # The `@given` decorator injects algorithmic hostility!
        # `st.text()` tells Hypothesis to generate completely random text strings,
        # including Chinese characters, Emojis, RTL Arabic, Null Bytes, and whitespace.
        
        @given(st.text())
        @settings(max_examples=100) # Bombard it 100 times!
        def test_reverse_string_properties(self, random_text: str):
            """
            Property 1: Reversing a string twice MUST equal the original string.
            Property 2: The length MUST remain identical.
            """
            reversed_text = StringAlgorithms.reverse_string(random_text)
            double_reversed = StringAlgorithms.reverse_string(reversed_text)
            
            self.assertEqual(random_text, double_reversed)
            self.assertEqual(len(random_text), len(reversed_text))
            
            
        # --- TEST 2: INTEGER MATH INVARIANTS ---
        # Hypothesis can generate mathematical boundaries (MAX_INT, Negative Infinity)
        @given(st.integers(), st.integers())
        def test_addition_commutativity(self, x: int, y: int):
            """
            Property: x + y MUST mathematically equal y + x.
            """
            self.assertEqual(x + y, y + x)


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE TEST RUNNER)
# ==============================================================================
def demonstrate_hypothesis():
    section_header("Unit Testing: Hypothesis Bombardment")
    
    if not HAS_LIBS:
        print("  [ERROR] Hypothesis not installed. Run `pip install hypothesis`.")
        return
        
    print("  [EXECUTION] Booting Hypothesis Fuzzer...")
    print("  Hypothesis will now algorithmically generate hundreds of hostile edge cases")
    print("  and hurl them at our functions to prove they are mathematically sound.\n")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringAlgorithms)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n  [ARCHITECTURE PROOF]")
    print(f"  Tests Run: {test_result.testsRun}")
    if test_result.wasSuccessful():
        print("  -> [FLAWLESS] The functions survived hundreds of hostile algorithmic mutations!")


def run_all_labs():
    demonstrate_hypothesis()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the philosophical difference between standard 'Example-Based Testing' (like standard `pytest`) and 'Property-Based Testing' (`hypothesis`)?"
   Senior Answer: "Human limitations versus Mathematical Exhaustion. In Example-Based Testing, the developer manually hardcodes specific inputs ($x=5, y=10$). The test proves the function works *for those two numbers only*. The developer is mathematically blind to the infinite space of edge cases (e.g., $x=-0.0, y=NaN$). In Property-Based Testing, the developer does not write inputs. They write 'Invariants' (mathematical truths that must always hold, like `len(input) == len(output)`). The framework then algorithmically searches the parameter space, generating thousands of hostile inputs (Max Int, Null Bytes, Emojis) to actively try and break the invariant. It shifts the paradigm from 'proving it works once' to 'mathematically failing to prove it breaks'."

2. Interviewer: "When `hypothesis` finds a massive, complex input that breaks your code (like a $500$-character string of random Unicode), how do you debug it? It seems impossible to read."
   Senior Answer: "Test Case Shrinking (Algorithmic Minimization). This is the most powerful feature of the Hypothesis engine. When it finds a failure (e.g., a $500$-character string containing Chinese characters, Emojis, and numbers), it does NOT immediately show you that string. It mathematically pauses and executes a 'Shrinking Phase'. It algorithmically removes characters, swaps Emojis for standard letters, and reduces the length, re-running the test on every mutation. It actively hunts for the absolute minimal, simplest possible input that still triggers the exact same Exception. By the time it reports the error to you, the $500$-character chaotic string has been shrunk down to `input='0'`, immediately pinpointing the exact mathematical edge case that broke the logic."

3. Interviewer: "How do you test a complex function, like a Database Sorting Algorithm, where calculating the 'correct' answer to assert against is just as hard as writing the sorting algorithm itself?"
   Senior Answer: "The Test Oracle (or Invariant Assertions). If testing a sorting algorithm, you do not need to calculate the exact sorted output. You only need to mathematically assert the *Properties* of a sorted list. You assert Property 1: `len(output) == len(input)`. You assert Property 2: `The elements in the output have the exact same frequencies as the input` (using `collections.Counter`). You assert Property 3: `output[i] <= output[i+1]` for the entire array. If Hypothesis feeds it $1,000$ chaotic arrays and all $3$ mathematical properties hold true, you have conclusively proven the sorting algorithm works without ever needing to know the 'correct' answer."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Testing and Debugging (Hypothesis) Completed.")
