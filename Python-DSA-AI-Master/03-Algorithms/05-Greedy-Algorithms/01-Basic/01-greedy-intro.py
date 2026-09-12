"""
## A. Concept Name
Greedy Algorithms (Introduction)

## B. Core Idea
A greedy algorithm builds up a solution piece by piece, always choosing the next piece that offers the most obvious and immediate benefit. It makes a locally optimal choice in the hope that this choice will lead to a globally optimal solution.

## C. Use Cases
- Coin Change Problem (for canonical coin systems)
- Fractional Knapsack Problem
- Dijkstra's Shortest Path Algorithm
- Prim's and Kruskal's Minimum Spanning Tree Algorithms

## D. Key Advantages
- Easy to conceptualize and implement
- Usually highly efficient (often linear or log-linear time complexity)

## E. Limitations
- Does not always yield the globally optimal solution (e.g., Coin Change with non-canonical coin systems)
- Requires proving that a local optimum leads to a global optimum

## F. Implementation Strategy
1. Initialize an empty result or configuration.
2. Iterate through the available choices.
3. Apply a greedy choice property to pick the best current option.
4. Add the choice to the result and reduce the problem size.
5. Repeat until the target is reached or choices are exhausted.

## G. Common Pitfalls
- Assuming a greedy choice always works without mathematical proof
- Forgetting to sort the input data, which is often a prerequisite for greedy choices

## H. Mathematical Foundation
Relies on two properties:
1. Greedy Choice Property: A global optimum can be arrived at by selecting a local optimum.
2. Optimal Substructure: An optimal solution to the problem contains optimal solutions to sub-problems.

## I. Best Practices
- Sort the data first if the greedy choice depends on order (e.g., highest value first).
- Validate if the problem has the greedy choice property before implementation.

## J. Testing Strategies
- Test with standard cases.
- Test with edge cases (e.g., empty input, impossible targets).
- Test with known counter-examples to ensure the algorithm handles limitations gracefully (if applicable).

## K. Debugging Tips
- Trace the choices step-by-step to verify if the local optimum was selected.
- Print intermediate states of the result variable.

## L. Performance Metrics
- Time Complexity: O(N log N) if sorting is required, otherwise O(N).
- Space Complexity: O(1) or O(N) depending on result storage.

## M. Code Reusability
The basic structure of iterating and picking the best option can be abstracted into a generic template.

## N. Documentation Guidelines
- Clearly state the greedy choice being made in comments.
- Note any assumptions made about the input (e.g., input must be sorted).

## O. Error Handling
- Handle cases where no solution is possible (e.g., target cannot be reached with given choices).

## P. Edge Cases
- Target is 0.
- Available choices are empty.
- Target is smaller than the smallest available choice.

## Q. Refactoring Opportunities
- Extract the greedy selection logic into a separate function.

## R. Maintainability
- Keep the greedy choice logic simple and readable.

## S. Security Implications
- Generally low risk, but ensure input validation to prevent infinite loops.

## T. Deployment Considerations
- Minimal external dependencies, easy to deploy.

## U. Scalability
- Scales well for large datasets due to low time complexity.

## V. Cross-Platform Compatibility
- Standard Python implementation works across platforms.

## W. Future Enhancements
- Adapt the algorithm for more complex variations (e.g., bounded capacities).

## X. Project Connection
This serves as the foundational introduction for the Greedy Algorithms module in the DSA-AI curriculum, setting the stage for more advanced applications like Huffman Coding and Scheduling.
"""

def coin_change_greedy(coins: list[int], amount: int) -> list[int]:
    """
    Finds the minimum number of coins to make the given amount using a greedy approach.
    Note: This only works perfectly for canonical coin systems (e.g., US currency).
    """
    # Sort coins in descending order for the greedy choice
    coins.sort(reverse=True)
    result = []
    
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
            
    if amount != 0:
        return []  # Cannot make the exact amount
        
    return result

if __name__ == "__main__":
    # Example usage
    us_coins = [25, 10, 5, 1]
    target_amount = 67
    
    change = coin_change_greedy(us_coins, target_amount)
    print(f"Target amount: {target_amount}")
    print(f"Coins used: {change}")
    print(f"Total coins: {len(change)}")
