# 03-rl-app.py
"""
Reinforcement Learning Basics

This script demonstrates a very simple Q-learning algorithm in a 1D grid world.
The agent starts at position 0 and must reach position N to get a reward.

Topics Covered:
1. Environment state and actions.
2. Q-table initialization and updating.
3. Exploration vs. Exploitation (epsilon-greedy).
"""

import numpy as np
import random

def run_q_learning():
    """Runs a 1D grid world Q-learning simulation."""
    # Environment Setup
    grid_size = 6
    goal_state = 5
    num_actions = 2  # 0: Left, 1: Right
    
    # Q-table: states x actions
    Q = np.zeros((grid_size, num_actions))
    
    # Hyperparameters
    alpha = 0.1      # Learning rate
    gamma = 0.9      # Discount factor
    epsilon = 0.1    # Exploration rate
    episodes = 100
    
    print("Training the RL Agent...")
    for episode in range(episodes):
        state = 0  # Start at the beginning
        
        while state != goal_state:
            # Choose action (epsilon-greedy)
            if random.uniform(0, 1) < epsilon:
                action = random.choice([0, 1])  # Explore
            else:
                action = np.argmax(Q[state])    # Exploit
            
            # Take action and observe new state
            next_state = state
            if action == 0 and state > 0:       # Left
                next_state -= 1
            elif action == 1 and state < grid_size - 1: # Right
                next_state += 1
                
            # Reward assignment
            reward = 1 if next_state == goal_state else 0
            
            # Q-learning update rule
            best_next_action = np.argmax(Q[next_state])
            td_target = reward + gamma * Q[next_state][best_next_action]
            td_error = td_target - Q[state][action]
            Q[state][action] += alpha * td_error
            
            state = next_state
            
    print("\nTraining Complete. Final Q-Table:")
    print("State | Left  | Right")
    print("----------------------")
    for i in range(grid_size):
        print(f"  {i}   | {Q[i][0]:.3f} | {Q[i][1]:.3f}")

if __name__ == "__main__":
    run_q_learning()
