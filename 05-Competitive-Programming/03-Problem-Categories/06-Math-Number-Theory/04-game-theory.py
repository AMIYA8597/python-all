"""
# ==============================================================================
# LABORATORY: COMPETITIVE PROGRAMMING (GAME THEORY)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You and a friend are playing a game. There are 3 piles of stones:
# Pile A has 3 stones. Pile B has 4 stones. Pile C has 5 stones.
# 
# Rules: 
# 1. You take turns.
# 2. On your turn, you can remove any number of stones (1 or more), but they 
#    MUST all come from the same single pile.
# 3. The person who takes the last stone wins.
#
# You go first. Assuming both you and your friend play flawlessly like 
# supercomputers, who will mathematically win?
#
# This is the "Game of Nim". You could try to write a recursive Minimax DFS 
# with Memoization to test all $3 \times 4 \times 5 = 60$ states. But what if 
# the piles have $10^9$ stones? Minimax will instantly crash.
#
# You must use Nim-Sum (XOR). Charles Bouton mathematically proved in 1901 
# that you can determine the exact winner of ANY Nim game in exactly $O(N)$ 
# time by simply applying the Bitwise XOR operator to the pile sizes!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Game of Nim and the XOR-Sum mathematical proof.
# - Master the Sprague-Grundy Theorem using the MEX function for complex games.
#
# ==============================================================================
"""

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE GAME OF NIM (XOR SUM)
# ==============================================================================
def can_first_player_win_nim(piles: list[int]) -> bool:
    """
    Determines if the first player will win the Game of Nim, assuming perfect play.
    Time Complexity: O(N) where N is the number of piles.
    Space Complexity: O(1)
    """
    # Calculate the Nim-Sum (The XOR of all pile sizes)
    nim_sum = 0
    for stones in piles:
        nim_sum ^= stones
        
    # THE MATHEMATICAL LAW OF NIM:
    # If the Nim-Sum is NON-ZERO before you make a move, you have a guaranteed 
    # mathematical path to victory. (You can force the Nim-Sum to 0 for the opponent).
    #
    # If the Nim-Sum is ZERO before you make a move, you are mathematically doomed. 
    # No matter what you do, you will create a NON-ZERO state for your opponent, 
    # handing them the victory.
    return nim_sum != 0

def demonstrate_nim():
    section_header("The Game of Nim (XOR Sum)")
    
    # 3, 4, 5
    # 3 in binary: 011
    # 4 in binary: 100
    # 5 in binary: 101
    # XOR Sum:     010 (Decimal 2)
    piles = [3, 4, 5]
    
    print(f"Pile Sizes: {piles}")
    print(f"Nim-Sum (3 ^ 4 ^ 5) = {3 ^ 4 ^ 5}")
    
    if can_first_player_win_nim(piles):
        print("\nResult: The FIRST player is mathematically guaranteed to WIN.")
        print("Winning Strategy: Remove exactly 2 stones from Pile A.")
        print("This forces Pile A to 1 stone. The new piles are [1, 4, 5].")
        print("The new Nim-Sum is (1 ^ 4 ^ 5) = 0. The opponent is now doomed!")
    else:
        print("\nResult: The FIRST player is mathematically DOOMED to LOSE.")


# ==============================================================================
# 4. SPRAGUE-GRUNDY THEOREM (MEX FUNCTION)
# ==============================================================================
def calculate_mex(state_set: set[int]) -> int:
    """
    MEX (Minimum Excluded Value).
    Returns the smallest non-negative integer that is NOT present in the set.
    """
    mex = 0
    while mex in state_set:
        mex += 1
    return mex

def calculate_grundy_numbers(max_stones: int) -> list[int]:
    """
    Solves a complex game: "You can only remove 1, 3, or 4 stones."
    This is NOT standard Nim, so we cannot just XOR the raw pile sizes!
    We must use the Sprague-Grundy theorem to map this custom game into 
    equivalent "Nim-values" (Grundy Numbers) using the MEX function.
    """
    # valid_moves = [1, 3, 4]
    
    # grundy[i] stores the equivalent Nim-value for a pile of size i
    grundy = [0] * (max_stones + 1)
    
    # Base case: 0 stones left. The player whose turn it is loses. 
    # In Game Theory, losing states ALWAYS have a Grundy value of 0.
    grundy[0] = 0
    
    for current_stones in range(1, max_stones + 1):
        reachable_states = set()
        
        # From the current pile size, simulate all possible legal moves!
        for move in [1, 3, 4]:
            if current_stones - move >= 0:
                # Add the Grundy value of the resulting state
                reachable_states.add(grundy[current_stones - move])
                
        # The Grundy value of THIS state is the MEX of all reachable states!
        grundy[current_stones] = calculate_mex(reachable_states)
        
    return grundy

def demonstrate_sprague_grundy():
    section_header("Sprague-Grundy Theorem (Custom Games)")
    
    print("Custom Game Rules: You can ONLY remove 1, 3, or 4 stones at a time.")
    print("Let's calculate the equivalent Nim-values (Grundy Numbers) up to 10 stones.\n")
    
    grundy = calculate_grundy_numbers(10)
    
    for i in range(11):
        print(f"A pile of {i} stones is mathematically equivalent to a standard Nim pile of {grundy[i]}")
        
    print("\nIf you had piles of [7, 9, 10] playing this custom game:")
    print("Instead of XORing 7 ^ 9 ^ 10 (Which is wrong!)...")
    print("You XOR their Grundy Equivalents: grundy[7] ^ grundy[9] ^ grundy[10]")
    
    custom_xor = grundy[7] ^ grundy[9] ^ grundy[10]
    print(f"({grundy[7]} ^ {grundy[9]} ^ {grundy[10]}) = {custom_xor}")
    print(f"Since {custom_xor} != 0, the First Player WINS!")


def run_all_labs():
    demonstrate_nim()
    demonstrate_sprague_grundy()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Explain the mathematical logic behind the Nim-Sum (XOR). Why does an XOR sum of 0 mean the current player is doomed?
   Answer: XOR mathematically acts as a binary balancing scale without carryover. If the XOR sum is 0, it means that for every single bit column (1s, 2s, 4s, 8s), there is an exactly EVEN number of 1s across all the piles. The game is perfectly balanced. If you remove any stones from any single pile, you are mathematically forced to flip at least one bit. Because you only touched one pile, you can only flip one instance of that bit, turning the even count into an ODD count. Therefore, making *any* move from a balanced (0) state mathematically guarantees the state becomes unbalanced ($\neq 0$) for your opponent. Your opponent will then strategically remove stones to restore the balance back to 0. You will continuously be handed 0, until you are handed exactly 0 stones and lose!

2. What is the fundamental principle of the Sprague-Grundy Theorem?
   Answer: The Sprague-Grundy Theorem states that *every single* impartial game under normal play convention (where the last player to move wins) is mathematically isomorphic to a standard Game of Nim. Even if the game rules are incredibly complex ("You can only split a pile into two unequal halves, or remove a prime number of stones"), you can map every single state of that game to a single integer called a Grundy Number (or Nim-value). Once you calculate the Grundy Numbers for your custom piles, you simply XOR them together exactly as if they were standard Nim piles!

3. In the Sprague-Grundy Theorem, why is the MEX (Minimum Excluded Value) function used to determine the Grundy Number?
   Answer: The Grundy Number represents the power of choice. If you are in a state that can transition to states with Grundy values of `{0, 1, 2}`, you possess the power to hand your opponent a 0, a 1, or a 2. In a standard Game of Nim, if you have a pile of size 3, you can remove stones to leave a pile of size 0, 1, or 2! Notice the exact mathematical equivalence! If your custom game state can transition to `{0, 1, 2}`, it behaves exactly like a Nim pile of size 3! What is the MEX of `{0, 1, 2}`? It is 3! The MEX function perfectly calculates the "equivalent Nim pile size" by finding the smallest power of choice you *don't* have.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Game Theory Completed.")
