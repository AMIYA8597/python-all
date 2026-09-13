"""
# ==============================================================================
# LABORATORY: REINFORCEMENT LEARNING (Q-LEARNING)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Supervised Learning trains models using static datasets with known answers.
# What if you want to teach an AI to play Super Mario, fly a drone, or 
# optimize a data center's cooling system in real-time? There is no "Dataset" 
# of perfect drone flights.
#
# You must use Reinforcement Learning (RL).
# In RL, an "Agent" interacts with an "Environment".
# 1. The Agent observes the State.
# 2. It takes an Action.
# 3. The Environment returns a new State and a Reward (positive or negative).
# 4. The Agent updates its internal mathematical policy to maximize long-term reward.
#
# This is how DeepMind built AlphaGo to defeat the world champion in Go!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Markov Decision Process (State, Action, Reward).
# - Understand the Bellman Equation and Q-Values.
# - Implement Tabular Q-Learning (Epsilon-Greedy).
#
# ==============================================================================
"""

import numpy as np

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE ENVIRONMENT (MARKOV DECISION PROCESS)
# ==============================================================================
class GridWorldEnv:
    """
    A simple 1D Grid Environment.
    [Start (0)] -> [Empty (1)] -> [Empty (2)] -> [Goal/Reward +10 (3)]
    If the agent goes out of bounds, it hits a Wall (Reward -1).
    Actions: 0 = Left, 1 = Right
    """
    def __init__(self):
        self.state = 0
        self.num_states = 4
        self.num_actions = 2
        
    def reset(self):
        self.state = 0
        return self.state
        
    def step(self, action):
        reward = 0
        done = False
        
        if action == 0: # Left
            self.state -= 1
        elif action == 1: # Right
            self.state += 1
            
        # Check boundaries and goal
        if self.state < 0:
            self.state = 0
            reward = -1 # Penalty for hitting wall
        elif self.state >= 3:
            self.state = 3
            reward = 10 # Massive reward for reaching the goal!
            done = True
        else:
            reward = 0 # No immediate reward for just moving
            
        return self.state, reward, done


def demonstrate_q_learning():
    section_header("Tabular Q-Learning (The Bellman Equation)")
    
    print("We will train an AI Agent to navigate a grid to find a reward.")
    print("The Agent uses a 'Q-Table' (a matrix) to store the expected future ")
    print("reward for every possible action in every possible state.\n")
    
    env = GridWorldEnv()
    
    # 1. INITIALIZE THE Q-TABLE
    # Rows = States (0 to 3). Columns = Actions (0=Left, 1=Right).
    # Initially, the AI knows absolutely nothing, so all values are 0.0!
    q_table = np.zeros((env.num_states, env.num_actions))
    
    # 2. HYPERPARAMETERS
    alpha = 0.1       # Learning Rate (How much old knowledge to overwrite)
    gamma = 0.9       # Discount Factor (How much it cares about FUTURE rewards vs immediate)
    epsilon = 1.0     # Exploration Rate (1.0 = 100% random actions initially)
    epsilon_decay = 0.95
    min_epsilon = 0.01
    
    episodes = 50
    rng = np.random.default_rng(42)
    
    print("Starting Training Loop (50 Episodes)...\n")
    
    # 3. THE TRAINING LOOP
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            # EPSILON-GREEDY POLICY (Exploration vs Exploitation)
            # Do we take a random action to discover new things, or use our Q-Table 
            # to exploit what we already know?
            if rng.random() < epsilon:
                action = rng.integers(0, env.num_actions) # Explore (Random)
            else:
                action = np.argmax(q_table[state]) # Exploit (Best known action)
                
            # Take the action in the Environment
            next_state, reward, done = env.step(action)
            total_reward += reward
            
            # THE BELLMAN EQUATION (The Core of Reinforcement Learning)
            # Update the Q-Table based on the reward received AND the maximum 
            # possible future reward available in the NEXT state!
            
            old_q = q_table[state, action]
            max_future_q = np.max(q_table[next_state])
            
            # Q_new = Q_old + alpha * (Reward + gamma * MaxFutureQ - Q_old)
            new_q = old_q + alpha * (reward + gamma * max_future_q - old_q)
            
            q_table[state, action] = new_q
            state = next_state
            
        # Decay Epsilon (Become less random as we learn)
        epsilon = max(min_epsilon, epsilon * epsilon_decay)
        
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode+1:2d} | Total Reward: {total_reward:3d} | Epsilon: {epsilon:.2f}")

    print("\nTraining Complete! The Agent has mapped the environment.")
    print("Final Learned Q-Table:")
    print("           Left    Right")
    for i in range(3): # We don't print state 3, as it's the terminal goal
        print(f"State {i}: {q_table[i, 0]:7.2f} {q_table[i, 1]:7.2f}")
        
    print("\nNotice the Q-Values! The 'Right' action mathematically carries a ")
    print("higher expected reward propagating backwards from State 2 to State 0.")
    print("If you drop the Agent in State 0, it will look at the table, ")
    print("see Right > Left, and perfectly march toward the goal!")


def run_all_labs():
    demonstrate_q_learning()


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the "Exploration vs. Exploitation" dilemma in Reinforcement Learning?
   Answer: If an AI finds a path that gives a +5 reward, it might want to "Exploit" that path forever to guarantee points. However, if it stops exploring, it will never discover the secret path that yields a +100 reward! We solve this using the Epsilon-Greedy policy. Epsilon starts at $1.0$ (100% random exploration). As the AI trains, we decay Epsilon down to $0.01$ (1% random, 99% exploitation), allowing it to discover the world early on, and then ruthlessly optimize its path later.

2. What is the fundamental limitation of Tabular Q-Learning?
   Answer: Tabular Q-Learning creates a physical Matrix (Rows = States, Cols = Actions). In a simple GridWorld (100 squares, 4 directions), the table is $100 \times 4$. But what if the AI is playing chess ($10^{40}$ states) or navigating a Self-Driving Car using HD Camera pixels (infinite continuous states)? The Q-Table would require more RAM than atoms in the universe.

3. How do Deep Q-Networks (DQN) solve the limitation of Tabular Q-Learning?
   Answer: A DQN deletes the physical Q-Table matrix entirely and replaces it with a Deep Neural Network (usually a CNN). You feed the current State (e.g., the raw pixels of the video game) into the Input layer of the Neural Network. The Network's Output layer emits the estimated Q-Values for the 4 possible joystick actions! The neural network mathematically *approximates* the Q-Table, allowing the AI to calculate actions for novel states (new camera angles) it has never explicitly seen before.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Reinforcement Learning (Q-Learning) Completed.")
