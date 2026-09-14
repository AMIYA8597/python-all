"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (REINFORCEMENT LEARNING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer tries to program a robot to navigate a maze using standard 
# `if/else` statements. They write 5,000 lines of complex rules. The robot hits 
# an edge case on line 4,302, crashes into a wall, and physically explodes.
#
# A senior AI engineer understands "Reinforcement Learning". They write zero 
# `if/else` logic. Instead, they mathematically define an "Environment", a 
# "Reward System" (+10 for the exit, -100 for a wall), and deploy a Q-Learning 
# Matrix. They let the algorithm randomly explore the maze 10,000 times. Through 
# the Calculus of the Bellman Equation, the algorithm mathematically teaches 
# *itself* the perfect, infallible path to the exit in 5 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the architecture of the Q-Learning Algorithm (The Q-Table).
# - Understand the Bellman Equation (Learning Rate, Discount Factor).
# - Execute the Explore vs Exploit (Epsilon-Greedy) mathematical strategy.
#
# ==============================================================================
"""

import random
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE MATHEMATICAL ENVIRONMENT
# ==============================================================================
# We define a simple 1D grid world: [ START, SAFE, SAFE, SAFE, TRAP, EXIT ]
# State 0: Start
# State 4: Trap (-100 Reward)
# State 5: Exit (+100 Reward)

NUM_STATES = 6
ACTIONS = [0, 1] # 0: Move Left, 1: Move Right

def get_reward_and_next_state(state: int, action: int):
    """The Mathematical Physics Engine of the Environment."""
    if action == 0: # Left
        next_state = max(0, state - 1)
    else:           # Right
        next_state = min(NUM_STATES - 1, state + 1)
        
    # The Reward Logic!
    if next_state == 5:
        return 100, next_state, True # Found the Exit! (Terminal State)
    elif next_state == 4:
        return -100, next_state, True # Hit the Trap! (Terminal State)
    else:
        return -1, next_state, False # Standard move penalty (encourages speed)


# ==============================================================================
# 4. THE Q-LEARNING ALGORITHM
# ==============================================================================
def demonstrate_q_learning():
    section_header("Reinforcement Learning: The Q-Table Algorithm")
    
    print("  [INIT] Initializing the Q-Table Matrix...")
    # The Q-Table is a mathematical matrix: Rows = States, Columns = Actions.
    # It stores the "Quality" (Q-Value) of taking a specific action in a specific state.
    # We initialize it with absolute ZERO knowledge!
    q_table = [[0.0 for _ in range(len(ACTIONS))] for _ in range(NUM_STATES)]
    
    # --- HYPERPARAMETERS ---
    # The mathematical dials that control the AI's learning behavior!
    ALPHA = 0.1       # Learning Rate (How much it trusts new information)
    GAMMA = 0.9       # Discount Factor (How much it cares about long-term future rewards)
    EPSILON = 1.0     # Exploration Rate (1.0 = 100% random exploration)
    EPSILON_DECAY = 0.99 # Slowly reduces random exploration over time!
    
    EPISODES = 200 # The AI will play the game 200 times!
    
    print(f"  [TRAINING] Commencing {EPISODES} Simulations...")
    
    for episode in range(EPISODES):
        state = 0 # Start at the beginning!
        done = False
        
        while not done:
            # --- 1. EXPLORE VS EXPLOIT (The Epsilon-Greedy Strategy) ---
            if random.uniform(0, 1) < EPSILON:
                # EXPLORE: The AI takes a completely random action!
                action = random.choice(ACTIONS)
            else:
                # EXPLOIT: The AI looks at the Q-Table and takes the BEST known action!
                # It mathematically finds the highest Q-Value for the current state.
                action = q_table[state].index(max(q_table[state]))
                
            # --- 2. TAKE ACTION (Interact with Environment) ---
            reward, next_state, done = get_reward_and_next_state(state, action)
            
            # --- 3. THE BELLMAN EQUATION (Update the Q-Table!) ---
            # This is the core Calculus of Reinforcement Learning!
            # New Q(s,a) = Old Q(s,a) + Alpha * [Reward + Gamma * Max Q(s',a') - Old Q(s,a)]
            
            old_value = q_table[state][action]
            next_max = max(q_table[next_state])
            
            # The AI mathematically adjusts its internal belief system based on the reward!
            new_value = old_value + ALPHA * (reward + GAMMA * next_max - old_value)
            q_table[state][action] = new_value
            
            # Move to the next state for the next loop iteration!
            state = next_state
            
        # At the end of every episode, the AI mathematically becomes slightly less random!
        EPSILON = max(0.01, EPSILON * EPSILON_DECAY)
        
    print("  [TRAINING COMPLETE] The AI has mastered the environment.")
    
    
    # --- 5. THE FINAL MATHEMATICAL MATRIX ---
    print("\n  [THE FINAL Q-TABLE (AI KNOWLEDGE MATRIX)]")
    for s in range(NUM_STATES):
        print(f"    State {s} -> Left: {q_table[s][0]:8.2f} | Right: {q_table[s][1]:8.2f}")
        
    # --- 6. EXECUTING THE LEARNED POLICY ---
    print("\n  [TESTING] Releasing the trained AI into the maze...")
    state = 0
    path = []
    
    while state != 5 and state != 4:
        path.append(state)
        # The AI EXPLOITS the table perfectly! No random exploration!
        best_action = q_table[state].index(max(q_table[state]))
        
        # Calculate the text direction for logging
        dir_text = "LEFT" if best_action == 0 else "RIGHT"
        print(f"    -> AI is currently at State {state}. It decides to move {dir_text}.")
        
        _, state, _ = get_reward_and_next_state(state, best_action)
        
    path.append(state)
    
    if state == 5:
        print(f"  [SUCCESS] The AI flawlessly reached the EXIT! Path: {path}")
    else:
        print(f"  [FAILURE] The AI hit the TRAP. Path: {path}")


def run_all_labs():
    demonstrate_q_learning()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the 'Explore vs Exploit' dilemma in Reinforcement Learning, and how does the Epsilon-Greedy strategy mathematically solve it?"
   Senior Answer: "If the AI only ever 'Exploits' its current knowledge, it will find a sub-optimal path (e.g., getting $+5$ points) and endlessly repeat it, never realizing that a $+100$ point path exists just around the corner. If the AI only ever 'Explores' randomly, it will never actually learn how to execute a sequence of good moves. The Epsilon-Greedy strategy mathematically bridges this. We initialize Epsilon ($\epsilon$) to $1.0$ ($100\\%$ random exploration). In the beginning, the AI randomly flails around the environment, mapping out the Traps and the Exits. After every simulation, we multiply Epsilon by a decay factor (e.g., $0.99$). Over thousands of episodes, the probability of taking a random move slowly collapses towards $0\\%$, forcing the AI to perfectly transition from random mapping to flawless exploitation of the optimal mathematical path."

2. Interviewer: "In the Bellman Equation, what is the architectural purpose of 'Gamma' (The Discount Factor)?"
   Senior Answer: "Gamma ($\gamma$) is the mathematical representation of 'Delayed Gratification'. It ranges from $0$ to $1$. If Gamma is $0$, the AI mathematically only cares about immediate, instant rewards (e.g., eating the cookie right now). If Gamma is $0.99$, the AI mathematically cares about the long-term future (e.g., saving money for retirement). When calculating the Q-Value of the current state, we add the maximum possible Q-Value of the *next* state, multiplied by Gamma. This mathematically allows the massive $+100$ Reward from State $5$ to 'bleed backwards' into State $4$, State $3$, and State $2$. It acts as a breadcrumb trail of mathematical gravity, slowly pulling the AI towards the distant goal."

3. Interviewer: "If a Q-Table solves mazes so flawlessly, why don't we use a Q-Table for training self-driving cars or playing modern video games?"
   Senior Answer: "Because of 'The Curse of Dimensionality'. A Q-Table requires a physical row for every single possible State in the environment. In a 6-tile grid, we have 6 rows. In chess, there are $10^{40}$ possible board states. A self-driving car processes millions of continuous pixel inputs per second, resulting in functionally infinite states. If you attempted to allocate a Q-Table Matrix for a self-driving car, it would mathematically require more physical RAM than there are atoms in the universe. To solve complex environments, we must abandon Q-Tables and upgrade to 'Deep Q-Networks' (DQN). Instead of storing exact answers in a massive RAM matrix, we use a Deep Neural Network to mathematically *approximate* the Q-Values, collapsing the infinite matrix down to a few Megabytes of neural weights."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: AI & ML (Reinforcement Learning) Completed.")
