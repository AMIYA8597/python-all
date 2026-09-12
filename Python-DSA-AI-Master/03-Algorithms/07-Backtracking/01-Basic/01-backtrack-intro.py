"""
## A. Concept Name
Backtracking

## B. Core Concept
Backtracking is a general algorithmic technique that considers searching every possible combination in order to solve a computational problem. It incrementally builds candidates to the solutions, and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot possibly be completed to a valid solution.

## C. Why It Matters
Backtracking is essential for solving complex combinatorial problems like puzzle solving, scheduling, routing, and search problems where evaluating all possibilities is necessary but brute-forcing every single combination is inefficient.

## D. Real-World Analogy
Imagine navigating a maze. You walk down a path, and if it leads to a dead end, you retrace your steps (backtrack) to the last intersection and try a different path until you find the exit.

## E. Key Vocabulary
- **Candidate:** A potential partial solution.
- **State Space Tree:** A tree representing all possible states in the search space.
- **Pruning:** Discarding invalid candidates early to save computation.
- **Base Case:** The condition that indicates a candidate is a complete and valid solution.

## F. Common Pitfalls
- Failing to undo state changes when backtracking.
- Missing a base case, leading to infinite recursion.
- Not pruning the search space effectively, causing performance issues.

## G. Best Practices
- Always pass state variables by value or ensure they are explicitly reversed.
- Optimize the pruning condition to fail as early as possible.
- Use helper functions to keep the main logic clean.

## H. Code Walkthrough
The `generate_permutations` function builds permutations step-by-step. It iterates through available choices, adds a choice to the current path, recurses, and then removes the choice (backtracks) to try the next one.

## I. Time Complexity
O(N * N!) for generating all permutations of N items, since there are N! permutations and each takes O(N) to build.

## J. Space Complexity
O(N) for the recursion stack and the path array.

## K. Variations
- Finding combinations.
- Sudoku solver.
- N-Queens problem.

## L. Testing Strategies
- Test with an empty input.
- Test with small inputs (e.g., [1, 2, 3]).
- Check if all permutations are unique.

## M. Alternative Approaches
- Iterative approaches (like Heap's algorithm for permutations).
- Dynamic programming (if the problem has overlapping subproblems).

## N. Edge Cases
- Duplicate elements in the input array.
- Large input sizes causing recursion depth limits.

## O. Optimization Techniques
- Memoization (if applicable).
- Bit manipulation for tracking visited elements.

## P. Debugging Tips
- Print the current path and choices at each recursive step.
- Trace the recursion tree for small inputs on paper.

## Q. Historical Context
Backtracking algorithms have been formalized since the 1950s for solving games and mathematical puzzles.

## R. Related Patterns
- Depth-First Search (DFS)
- Recursion
- Branch and Bound

## S. Industry Standards
Used in compilers for parsing, in AI for game tree search, and in combinatorial optimization libraries.

## T. Security Implications
Backtracking can be vulnerable to Denial of Service (DoS) if the input causes catastrophic backtracking (e.g., in regex engines).

## U. Performance Metrics
Number of recursive calls, time taken to find the first solution vs. all solutions.

## V. Scalability
Not naturally scalable for large N due to exponential or factorial time complexities.

## W. Future Trends
Integration with heuristics and machine learning to guide the search and prune the state space faster.

## X. Project Connection
Understanding basic backtracking is the foundation for implementing complex AI solvers, routing engines, and constraint-based scheduling systems in larger projects.
"""

def generate_permutations(nums):
    """
    Generate all permutations of a given list of numbers using backtracking.
    """
    result = []
    
    def backtrack(path, choices):
        # Base case: if there are no more choices, the path is a complete permutation
        if not choices:
            result.append(path[:])
            return
        
        # Iterate through all available choices
        for i in range(len(choices)):
            # Choose: Pick one element
            choice = choices[i]
            path.append(choice)
            
            # Explore: Recurse with the remaining choices
            next_choices = choices[:i] + choices[i+1:]
            backtrack(path, next_choices)
            
            # Un-choose (Backtrack): Remove the element and try the next one
            path.pop()

    backtrack([], nums)
    return result

if __name__ == "__main__":
    nums = [1, 2, 3]
    print(f"Permutations of {nums}:")
    for p in generate_permutations(nums):
        print(p)
