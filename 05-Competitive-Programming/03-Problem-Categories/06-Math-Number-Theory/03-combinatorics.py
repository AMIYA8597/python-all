"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (ADVANCED COMBINATORICS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are given 10 identical cookies. You have 3 distinct children. 
# How many different ways can you distribute the cookies? 
# A child might get 0 cookies.
#
# Standard Permutations and Combinations fail here because the cookies are 
# IDENTICAL, but the children are DISTINCT. You must use the "Stars and Bars" 
# theorem, which beautifully reduces this physics problem into a simple string 
# permutation of Stars (cookies) and Bars (dividers).
#
# Second Scenario: 100 people arrive at a party and throw their hats in a pile. 
# When they leave, they randomly grab a hat. What is the probability that 
# NOBODY gets their own hat back?
# 
# This is a "Derangement" (a permutation where no element is in its original 
# position). The mathematical formula involves an elegant Dynamic Programming 
# recurrence relation: D(N) = (N-1) * (D(N-1) + D(N-2)).
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Stars and Bars (Balls and Urns).
# - Master Derangements (Subfactorials).
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

MOD = 10**9 + 7

# ==============================================================================
# 3. STARS AND BARS (BALLS AND URNS)
# ==============================================================================
def nCr_mod(n: int, r: int, mod: int = MOD) -> int:
    """Helper function to calculate nCr modulo P"""
    if r < 0 or r > n: return 0
    num, den = 1, 1
    for i in range(r):
        num = (num * (n - i)) % mod
        den = (den * (i + 1)) % mod
    return (num * pow(den, mod - 2, mod)) % mod

def stars_and_bars_zero_allowed(cookies: int, children: int) -> int:
    """
    Theorem 1: Distributing N identical items into K distinct bins, 
    where a bin can be EMPTY (0 items).
    Formula: (N + K - 1) Choose (K - 1)
    """
    # N stars, and (K-1) bars needed to split them into K sections!
    return nCr_mod(cookies + children - 1, children - 1)

def stars_and_bars_at_least_one(cookies: int, children: int) -> int:
    """
    Theorem 2: Distributing N identical items into K distinct bins, 
    where every bin MUST have AT LEAST ONE item.
    Formula: (N - 1) Choose (K - 1)
    """
    if cookies < children: return 0
    # Pre-distribute 1 cookie to every child. Then use Theorem 1 on the rest!
    # Mathematically simplifies to (N-1) C (K-1)
    return nCr_mod(cookies - 1, children - 1)

def demonstrate_stars_and_bars():
    section_header("Stars and Bars (Distributing Identical Items)")
    
    cookies = 5
    children = 3
    
    ans_zero = stars_and_bars_zero_allowed(cookies, children)
    ans_one = stars_and_bars_at_least_one(cookies, children)
    
    print(f"Distributing {cookies} Identical Cookies to {children} Distinct Children.")
    print(f"\nIf children can receive 0 cookies: {ans_zero} ways.")
    print("Example: (5,0,0), (0,5,0), (2,1,2), etc.")
    
    print(f"\nIf every child MUST receive at least 1: {ans_one} ways.")
    print("Example: (3,1,1), (1,3,1), (1,1,3), (2,2,1), (2,1,2), (1,2,2). (Exactly 6 ways!)")


# ==============================================================================
# 4. DERANGEMENTS (NOBODY GETS THEIR OWN HAT)
# ==============================================================================
def count_derangements(n: int) -> int:
    """
    Calculates the number of permutations where NO element is in its original position.
    Also known as Subfactorial, denoted as !N.
    Time Complexity: O(N) using Dynamic Programming.
    Space Complexity: O(1) with space optimization!
    """
    if n == 1: return 0 # 1 person gets their own hat (impossible to derange)
    if n == 2: return 1 # 2 people swap hats (1 derangement)
    
    prev2 = 0 # D(1)
    prev1 = 1 # D(2)
    
    for i in range(3, n + 1):
        # The Recurrence Relation:
        # Person `i` swaps with Person `j` (there are i-1 choices for j).
        # Two universes spawn from this swap:
        # Universe A: Person `j` got Person `i`'s hat. They cleanly swapped! 
        #             The remaining (i-2) people must be deranged.
        # Universe B: Person `j` did NOT get `i`'s hat. Person `j` basically 
        #             inherited `i`'s restriction. 
        #             The remaining (i-1) people must be deranged.
        
        current = (i - 1) * (prev1 + prev2) % MOD
        
        # Roll the array for O(1) Space!
        prev2 = prev1
        prev1 = current
        
    return prev1

def demonstrate_derangements():
    section_header("Derangements (!N)")
    
    people = 4
    total_permutations = 24 # 4!
    
    derangements = count_derangements(people)
    
    print(f"People: {people}")
    print(f"Total possible hat assignments: {total_permutations}")
    print(f"\nWays where NOBODY gets their own hat: {derangements}")
    
    print(f"\nProbability of this happening: {(derangements / total_permutations) * 100:.2f}%")
    print("Fun fact: As N approaches infinity, the probability converges perfectly to 1/e (36.78%)!")


def run_all_labs():
    demonstrate_stars_and_bars()
    demonstrate_derangements()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the visual string logic behind the "Stars and Bars" Theorem `(N+K-1) Choose (K-1)`.
   Answer: Imagine you have 5 identical cookies (Stars: *****). You want to split them among 3 children. To mathematically divide a sequence of items into 3 sections, you need exactly 2 Dividers (Bars: ||). If you place the items in a line `**|*|**`, Child A gets 2, Child B gets 1, Child C gets 2. The entire problem reduces to arranging a String containing exactly 5 Stars and 2 Bars! The total length of the string is $N + K - 1$. Out of those positions, you must choose exactly $K - 1$ positions to place the Bars. This perfectly maps to the combinatorial formula $(N+K-1) \text{ Choose } (K-1)$.

2. In the Stars and Bars theorem where every child MUST receive at least one cookie, why does the formula simplify to `(N-1) Choose (K-1)`?
   Answer: If a child must receive at least 1 cookie, it is identical to saying "No bin can be empty". In the Stars and Bars string representation `* * * * *`, there are exactly 4 "gaps" between the stars. To ensure no bin is empty, we are mathematically forced to place our 2 Dividers (Bars) strictly *inside* these gaps. We cannot place a Divider at the very end of the string, and we cannot place two Dividers in the exact same gap (which would create an empty bin). There are $N-1$ valid gaps. We must choose exactly $K-1$ gaps to place our Bars. This maps perfectly to $(N-1) \text{ Choose } (K-1)$.

3. Explain the Dynamic Programming recurrence relation for Derangements: `D(N) = (N-1) * [D(N-1) + D(N-2)]`.
   Answer: Imagine 10 people grabbing hats. You are Person 10. You must grab someone else's hat. You have exactly $(N-1) = 9$ choices. Let's say you grab Person 4's hat. Now, what does Person 4 do?
   Universe A (Clean Swap): Person 4 grabs *your* hat! You two perfectly resolved each other. The 8 remaining people must now derange amongst themselves. This is exactly `D(N-2)`.
   Universe B (Chain Reaction): Person 4 grabs *someone else's* hat. Person 4 acts as if they are the new "Person 10" (they are forbidden from taking your hat). The remaining 9 people (including Person 4) must derange amongst themselves. This is exactly `D(N-1)`.
   Because you had 9 choices initially, we multiply the sum of these two universes by $(N-1)$.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Advanced Combinatorics Completed.")
