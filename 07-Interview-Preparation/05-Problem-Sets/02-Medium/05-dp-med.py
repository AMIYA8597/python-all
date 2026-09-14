"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (PROBLEM SETS - DP MEDIUM)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Dynamic Programming (DP) is the most feared category in technical interviews.
# It tests your ability to break a massive, chaotic problem into overlapping 
# sub-problems, solve the smallest possible sub-problem first (Bottom-Up), and 
# mathematically build up to the final answer.
#
# A junior engineer uses raw Recursion to solve "Coin Change". The execution 
# branches out exponentially (O(2^N)), solving the exact same sub-problems 
# millions of times, instantly crashing with a Time Limit Exceeded (TLE).
#
# A senior engineer allocates a DP Array. They calculate the absolute optimal 
# solution for 1 cent. Then 2 cents. Then 3 cents. Because they permanently cache 
# the answers, calculating 100 cents takes exactly O(Amount * Coins) linear time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Bottom-Up Tabulation (Coin Change).
# - Master Double-Loop Historical Comparison (Longest Increasing Subsequence).
# - Master String Partitioning via DP (Word Break).
#
# ==============================================================================
"""

from typing import List

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. COIN CHANGE (THE KNAPSACK PARADIGM)
# ==============================================================================
def coin_change(coins: List[int], amount: int) -> int:
    """
    Time: O(Amount * Coins) | Space: O(Amount)
    Return the fewest number of coins that you need to make up that amount.
    """
    # Create the DP array!
    # dp[i] represents the absolute minimum coins needed to make exactly 'i' cents.
    # We initialize the array with (amount + 1), which acts as mathematical 'Infinity' 
    # because it is physically impossible to need more coins than the amount itself!
    dp = [(amount + 1)] * (amount + 1)
    
    # Base Case: It takes exactly 0 coins to make 0 cents!
    dp[0] = 0
    
    print(f"  Target: {amount} | Available Coins: {coins}")
    
    # We build the answer Bottom-Up, calculating 1 cent, then 2 cents... up to Amount.
    for i in range(1, amount + 1):
        for coin in coins:
            # If the current coin physically fits inside the current target amount!
            if i - coin >= 0:
                # The optimal choice is the MINIMUM between:
                # A: Whatever is currently sitting in dp[i]
                # B: 1 (the coin we are using) + dp[i - coin] (the optimally cached answer for the remainder!)
                dp[i] = min(dp[i], 1 + dp[i - coin])
                
    # If the final target amount is still holding 'Infinity', it means we could 
    # never mathematically reach it using any combination of coins!
    if dp[amount] != (amount + 1):
        print(f"    -> [SUCCESS] Minimum coins required: {dp[amount]}")
        return dp[amount]
    else:
        print("    -> [FAIL] Impossible to form amount with given coins.")
        return -1

def demonstrate_coin_change():
    section_header("Medium: Coin Change (Bottom-Up Tabulation)")
    
    coins = [1, 2, 5]
    amount = 11
    ans = coin_change(coins, amount)
    print(f"\nResult: {ans} (Expected: 3 [5, 5, 1])")


# ==============================================================================
# 4. LONGEST INCREASING SUBSEQUENCE (DOUBLE-LOOP DP)
# ==============================================================================
def length_of_LIS(nums: List[int]) -> int:
    """
    Time: O(N^2) | Space: O(N)
    Return the length of the longest strictly increasing subsequence.
    """
    if not nums: return 0
    
    # dp[i] represents the length of the Longest Increasing Subsequence that 
    # strictly ENDS at index i.
    # Every single number is a subsequence of length 1 by itself!
    dp = [1] * len(nums)
    
    print(f"  Array: {nums}")
    
    # We iterate through the array. For every single number...
    for i in range(1, len(nums)):
        # We look BACKWARDS at every single number that came before it!
        for j in range(i):
            # If the current number is strictly LARGER than the historical number, 
            # we can mathematically attach ourselves to its Subsequence!
            if nums[i] > nums[j]:
                # We update our own DP value to be the MAXIMUM between:
                # A: Our current DP value
                # B: 1 (ourselves) + the DP value of the historical number!
                dp[i] = max(dp[i], dp[j] + 1)
                
    # The absolute longest subsequence could end ANYWHERE in the array, not just 
    # at the final index! So we must return the global maximum of the entire DP array.
    max_len = max(dp)
    print(f"    -> Final DP Array State: {dp}")
    return max_len

def demonstrate_lis():
    section_header("Medium: Longest Increasing Subsequence (O(N^2) DP)")
    
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    ans = length_of_LIS(nums)
    print(f"\nResult: Length {ans} (Expected: 4 [2, 3, 7, 101])")


# ==============================================================================
# 5. WORD BREAK (STRING PARTITIONING DP)
# ==============================================================================
def word_break(s: str, wordDict: List[str]) -> bool:
    """
    Time: O(N^3) | Space: O(N) where N is length of string
    Given a string s and a dictionary of strings, return true if s can be 
    segmented into a space-separated sequence of dictionary words.
    """
    word_set = set(wordDict) # O(1) lookup!
    
    # dp[i] is True if the string up to index `i` can be perfectly segmented!
    dp = [False] * (len(s) + 1)
    
    # Base Case: An empty string is mathematically valid!
    dp[0] = True
    
    print(f"  String: '{s}' | Dictionary: {wordDict}")
    
    for i in range(1, len(s) + 1):
        # We look backwards to find a valid 'cut' point!
        for j in range(i):
            # If the string up to `j` is perfectly valid...
            # AND the substring from `j` to `i` is a valid Dictionary word!
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                print(f"    -> [MATCH] Valid cut found at index {i}! (Word: '{s[j:i]}')")
                break # We found a valid path to index `i`. Stop searching backwards!
                
    return dp[len(s)]

def demonstrate_word_break():
    section_header("Medium: Word Break (String DP)")
    
    s = "leetcode"
    wordDict = ["leet", "code"]
    ans = word_break(s, wordDict)
    print(f"\nResult: {ans} (Expected: True)")


def run_all_labs():
    demonstrate_coin_change()
    demonstrate_lis()
    demonstrate_word_break()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In 'Coin Change', why do we initialize the DP array with `amount + 1` instead of `-1` or `float('inf')`?"
   Senior Answer: "Initializing with `-1` is dangerous because we rely on the `min()` function inside the loop; `min(-1, X)` would always falsely select `-1`! We could use `float('inf')`, but floating-point objects in Python carry mathematical and memory overhead compared to raw Integers. By using `amount + 1`, we define a strict integer value that mathematically acts as Infinity, because it is physically impossible to construct a sum of $N$ cents using more than $N$ coins (even if the smallest coin is 1 cent). It provides the flawless logical behavior of Infinity with the native execution speed of an Integer."

2. Interviewer: "Could Longest Increasing Subsequence (LIS) be solved faster than $O(N^2)$?"
   Senior Answer: "Yes. It can be solved in $O(N \\log N)$ using a combination of Dynamic Programming and Binary Search. Instead of looking backwards at every single historical number, we maintain an active array representing the absolute best possible subsequence we can build. For every new number, we use Binary Search (`bisect_left`) to instantly find exactly where it physically belongs in the active array, overwriting a larger number if necessary to 'lower the floor' for future numbers. This entirely eliminates the inner $O(N)$ loop, reducing the time complexity to a perfectly scalable $O(N \\log N)$."

3. Interviewer: "In 'Word Break', why is the Time Complexity mathematically stated as $O(N^3)$?"
   Senior Answer: "There are three distinct layers of complexity. The outer loop (`i`) runs $N$ times. The inner loop (`j`) looks backwards and runs up to $N$ times. This creates the baseline $O(N^2)$ traversal. However, inside the inner loop, we execute `s[j:i]`. In Python, strings are immutable, meaning slicing physically allocates a brand new string in RAM and copies the characters one by one. String slicing is an $O(N)$ operation! Therefore, multiplying the $O(N^2)$ double-loop by the $O(N)$ string slicing yields a total theoretical worst-case bound of $O(N^3)$."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Problem Sets (DP Medium) Completed.")
