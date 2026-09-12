"""
## A. Concept Name
Combinatorics (Permutations and Combinations)

## B. Why It Matters
Combinatorics forms the foundation for calculating probabilities, optimizing search spaces, and analyzing the complexity of algorithms.

## C. Prerequisites
Basic arithmetic, factorials, and an understanding of sets.

## D. Key Terminology
- Permutation: Arrangement where order matters.
- Combination: Selection where order does not matter.
- Factorial (n!): Product of an integer and all integers below it.

## E. Core Mechanism
Using formulas like nPr = n! / (n-r)! and nCr = n! / (r! * (n-r)!) to calculate arrangements and selections.

## F. Step-by-Step Breakdown
1. Identify if order matters (Permutation vs Combination).
2. Determine total items (n) and selected items (r).
3. Apply the appropriate formula or generate them using recursion.

## G. Visual/Mental Model
Think of a combination lock as a "permutation lock" because order matters. For combinations, think of a fruit salad; the order of fruits doesn't matter.

## H. Basic Implementation
Using Python's `math` or `itertools` to compute permutations and combinations.

## I. Edge Cases
Choosing 0 items (nC0 = 1), choosing all items (nCn = 1), negative inputs (invalid).

## J. Performance Characteristics
Time complexity for generation is typically O(n!) for permutations and O(nCr) for combinations. Space complexity matches. Calculating the count takes O(min(r, n-r)) if done iteratively, or O(1) if factorials are precomputed.

## K. Advanced Variations
Stars and bars theorem, combinations with repetition, derangements, Catalan numbers.

## L. Common Mistakes
Confusing permutations and combinations. Integer overflow in other languages (Python handles arbitrarily large integers, but performance may suffer).

## M. Debugging Tips
Print intermediate factorials. Test with very small inputs where you can manually verify the answer.

## N. Testing Strategies
Verify edge cases like r=0, r=n. Ensure large outputs complete within time limits by using modulo arithmetic if required.

## O. AI/ML Applications
Combinatorial optimization in hyperparameter tuning (Grid Search), permutations of input features for feature importance calculation, sampling spaces in Reinforcement Learning.

## P. Real-world Scenarios
Cryptography, network routing, combinatorial auctions, scheduling problems.

## Q. Interview Focus
Counting problems often appear in dynamic programming, backtracking, and probability questions.

## R. Related Concepts
Probability theory, graph theory, binomial theorem.

## S. Alternatives
Monte Carlo simulations for estimating combinations in extremely large search spaces where exact calculation is impossible.

## T. History/Origin
Originated from ancient Indian mathematics (Bhaskara II) and formalized in Europe by Pascal and Fermat in the 17th century.

## U. Best Practices
Precompute factorials if you need to calculate combinations multiple times. Use `itertools` for generating combinations/permutations rather than writing custom backtracking when applicable.

## V. Code Smells
Calculating n! / (n-r)! manually without simplifying the division first, leading to unnecessarily large intermediate values.

## W. Further Reading
"Concrete Mathematics" by Knuth et al., Introduction to Algorithms (CLRS).

## X. Project Connection
In AI models, combinatorics can be applied to generate all possible states in games (like Chess or Tic-Tac-Toe) for tree search algorithms (Minimax, MCTS).
"""

import math
import itertools
from typing import List, Tuple

def calculate_nCr(n: int, r: int) -> int:
    """
    Calculate the number of combinations nCr efficiently.
    """
    if r < 0 or r > n:
        return 0
    return math.comb(n, r)

def calculate_nPr(n: int, r: int) -> int:
    """
    Calculate the number of permutations nPr.
    """
    if r < 0 or r > n:
        return 0
    return math.perm(n, r)

def generate_combinations(items: List[int], r: int) -> List[Tuple[int, ...]]:
    """
    Generate all combinations of size r from a list of items.
    """
    return list(itertools.combinations(items, r))

def generate_permutations(items: List[int], r: int) -> List[Tuple[int, ...]]:
    """
    Generate all permutations of size r from a list of items.
    """
    return list(itertools.permutations(items, r))

if __name__ == "__main__":
    n, r = 5, 3
    print(f"{n}C{r} = {calculate_nCr(n, r)}")
    print(f"{n}P{r} = {calculate_nPr(n, r)}")
    
    items = [1, 2, 3]
    print(f"Combinations of {items} size 2: {generate_combinations(items, 2)}")
    print(f"Permutations of {items} size 2: {generate_permutations(items, 2)}")
