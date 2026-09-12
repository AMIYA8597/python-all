"""
Module: 04-reinforce-learn
Description: Textbook-Grade Interactive Lesson on Reinforcement Learning (RL)

================================================================================
INTRODUCTION TO REINFORCEMENT LEARNING
================================================================================

Reinforcement Learning (RL) is a subfield of machine learning where an agent learns
to make decisions by performing actions in an environment to maximize a numerical
reward signal. Unlike supervised learning, the agent is not told which actions to
take, but instead must discover which actions yield the most reward by trying them.

This module provides a comprehensive, ground-up implementation of foundational RL
algorithms, specifically focusing on tabular Q-learning and Markov Decision Processes
(MDP).

--------------------------------------------------------------------------------
MATHEMATICAL BACKGROUND
--------------------------------------------------------------------------------

1. Markov Decision Process (MDP)
An MDP provides the mathematical framework for modeling decision making in situations
where outcomes are partly random and partly under the control of a decision maker.
It is defined by a 5-tuple (S, A, P, R, γ):
    - S: A finite set of states.
    - A: A finite set of actions.
    - P(s' | s, a): Transition probability of moving to state s' given action a in state s.
    - R(s, a, s'): Expected immediate reward received after transition.
    - γ (gamma): Discount factor, γ ∈ [0, 1]. Balances immediate and future rewards.

2. The Bellman Equation
The Bellman Equation is a fundamental recursive equation in RL that decomposes the
value function into the immediate reward plus the discounted expected value of
the next state.

    V(s) = max_a Σ_s' P(s' | s, a) [ R(s, a, s') + γ * V(s') ]

3. Q-Learning (Action-Value Function)
Q-learning is an off-policy, model-free RL algorithm. It aims to find the best
action to take given a current state.

Q-value Update Rule:
    Q(s, a) = Q(s, a) + α * [ R + γ * max_a' Q(s', a') - Q(s, a) ]

    Where:
    - α (alpha) is the learning rate (0 < α ≤ 1).
    - γ (gamma) is the discount factor (0 ≤ γ ≤ 1).
    - R is the reward obtained after taking action a in state s.
    - max_a' Q(s', a') is the maximum predicted reward for the next state s'.

--------------------------------------------------------------------------------
COMPLEXITY & BIG-O ANALYSIS
--------------------------------------------------------------------------------

Time Complexity:
- Q-Table Update: O(1) per step. Finding max Q value for next state takes O(|A|),
  where |A| is the number of possible actions.
- Total Training Time: O(E * T * |A|) where E is the number of episodes and T is
  the maximum steps per episode.

Space Complexity:
- Q-Table Storage: O(|S| * |A|), where |S| is the number of states and |A| is
  the number of actions. This makes tabular Q-learning impractical for continuous
  or large state spaces (which is where Deep Reinforcement Learning comes in).

--------------------------------------------------------------------------------
REAL-WORLD APPLICATIONS
--------------------------------------------------------------------------------
1. Autonomous Vehicles: Path planning, obstacle avoidance.
2. Robotics: Robotic arm manipulation, walking robots.
3. Game Playing: AlphaGo, DeepBlue, superhuman performance in video games.
4. Finance: Algorithmic trading and portfolio management.
5. Recommendation Systems: Maximizing long-term user engagement.

================================================================================
"""

import sys
import time
import math
import random
from typing import List, Dict, Any, Optional, Tuple

try:
    import numpy as np
except ImportError:
    print("WARNING: numpy is required for this module. Please install it using 'pip install numpy'.")
    sys.exit(1)


# ============================================================================
# 1. ENVIRONMENT: THE GRID WORLD
# ============================================================================

class GridWorldEnv:
    """
    A simple 2D Grid World Environment for Reinforcement Learning.
    
    The agent starts at a designated start state and must navigate to a goal state.
    The environment may contain obstacles (pits) which terminate the episode with
    a negative reward. Reaching the goal yields a positive reward.
    """
    
    def __init__(self, grid_size: Tuple[int, int] = (4, 4)):
        """
        Initializes the Grid World Environment.
        
        Args:
            grid_size: A tuple (rows, cols) defining the size of the grid.
        """
        self.rows, self.cols = grid_size
        self.start_state = (0, 0)
        self.goal_state = (self.rows - 1, self.cols - 1)
        self.pit_states = [(1, 1), (1, 2), (2, 2)] # Some static pits
        
        # State space representation: Tuple (r, c)
        self.state = self.start_state
        
        # Actions: 0: Up, 1: Right, 2: Down, 3: Left
        self.action_space = [0, 1, 2, 3]
        self.action_meanings = {0: "UP", 1: "RIGHT", 2: "DOWN", 3: "LEFT"}
        
    def reset(self) -> Tuple[int, int]:
        """
        Resets the environment to the starting state.
        
        Returns:
            The initial state.
        """
        self.state = self.start_state
        return self.state
    
    def step(self, action: int) -> Tuple[Tuple[int, int], float, bool, Dict[str, Any]]:
        """
        Executes an action in the environment.
        
        Args:
            action: An integer representing the action to take.
            
        Returns:
            A tuple (next_state, reward, done, info).
        """
        if action not in self.action_space:
            raise ValueError(f"Invalid action. Choose from {self.action_space}")
        
        r, c = self.state
        
        # Determine next state based on action
        if action == 0:   # UP
            r = max(0, r - 1)
        elif action == 1: # RIGHT
            c = min(self.cols - 1, c + 1)
        elif action == 2: # DOWN
            r = min(self.rows - 1, r + 1)
        elif action == 3: # LEFT
            c = max(0, c - 1)
            
        self.state = (r, c)
        
        # Determine reward and if episode is done
        done = False
        reward = -0.1 # Small negative reward to encourage faster paths
        
        if self.state == self.goal_state:
            reward = 10.0
            done = True
        elif self.state in self.pit_states:
            reward = -10.0
            done = True
            
        info = {"action_taken": self.action_meanings[action]}
        return self.state, reward, done, info
    
    def render(self) -> None:
        """Prints a simple text representation of the environment."""
        print("-" * (self.cols * 4 + 1))
        for r in range(self.rows):
            row_str = "|"
            for c in range(self.cols):
                cell = (r, c)
                if cell == self.state:
                    row_str += " A |" # Agent
                elif cell == self.goal_state:
                    row_str += " G |" # Goal
                elif cell in self.pit_states:
                    row_str += " X |" # Pit
                else:
                    row_str += "   |" # Empty space
            print(row_str)
            print("-" * (self.cols * 4 + 1))
        print()


# ============================================================================
# 2. THE AGENT: Q-LEARNING IMPLEMENTATION
# ============================================================================

class QLearningAgent:
    """
    A reinforcement learning agent that uses tabular Q-learning.
    
    The agent maintains a Q-table (a mapping of state-action pairs to values)
    and updates it based on the rewards received from the environment.
    """
    
    def __init__(self, action_space: List[int], alpha: float = 0.1, 
                 gamma: float = 0.99, epsilon: float = 1.0, 
                 epsilon_decay: float = 0.995, min_epsilon: float = 0.01):
        """
        Initializes the Q-Learning Agent.
        
        Args:
            action_space: A list of possible actions.
            alpha: Learning rate.
            gamma: Discount factor.
            epsilon: Initial exploration rate (epsilon-greedy policy).
            epsilon_decay: Rate at which epsilon decays after each episode.
            min_epsilon: Minimum value for exploration rate.
        """
        self.action_space = action_space
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        
        # Q-table: Maps state to a numpy array of Q-values for each action
        # Using a dictionary where keys are string representations of states
        self.q_table: Dict[str, np.ndarray] = {}
        
    def _get_q_values(self, state: Tuple[int, int]) -> np.ndarray:
        """
        Retrieves Q-values for a given state. Initializes to zeros if state is new.
        """
        state_key = str(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(len(self.action_space))
        return self.q_table[state_key]
        
    def choose_action(self, state: Tuple[int, int]) -> int:
        """
        Selects an action using the epsilon-greedy policy.
        
        With probability epsilon, chooses a random action (exploration).
        With probability 1 - epsilon, chooses the action with max Q-value (exploitation).
        """
        if random.uniform(0, 1) < self.epsilon:
            # Exploration
            return random.choice(self.action_space)
        else:
            # Exploitation
            q_values = self._get_q_values(state)
            # Break ties randomly by using np.random.choice on indices of max values
            max_val = np.max(q_values)
            best_actions = np.where(q_values == max_val)[0]
            return int(np.random.choice(best_actions))
            
    def update_q_value(self, state: Tuple[int, int], action: int, 
                       reward: float, next_state: Tuple[int, int]) -> None:
        """
        Updates the Q-value for a state-action pair using the Q-learning update rule.
        
        Q(s, a) <- Q(s, a) + α * [ R + γ * max_a' Q(s', a') - Q(s, a) ]
        """
        state_key = str(state)
        next_state_key = str(next_state)
        
        # Ensure states exist in Q-table
        self._get_q_values(state)
        self._get_q_values(next_state)
        
        current_q = self.q_table[state_key][action]
        max_next_q = np.max(self.q_table[next_state_key])
        
        # Bellman equation update
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state_key][action] = new_q
        
    def decay_epsilon(self) -> None:
        """Decays the exploration rate epsilon."""
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.min_epsilon, self.epsilon)


# ============================================================================
# 3. TRAINING LOOP
# ============================================================================

def train_agent(episodes: int = 500) -> Tuple[QLearningAgent, List[float]]:
    """
    Trains the Q-Learning agent in the Grid World environment.
    
    Args:
        episodes: Number of episodes to train.
        
    Returns:
        The trained agent and a list of total rewards per episode.
    """
    print(f"--- Training Q-Learning Agent for {episodes} Episodes ---")
    env = GridWorldEnv()
    agent = QLearningAgent(action_space=env.action_space)
    
    rewards_history = []
    
    start_time = time.time()
    
    for episode in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0.0
        done = False
        steps = 0
        
        # Prevent infinite loops in case agent gets stuck
        max_steps = 100 
        
        while not done and steps < max_steps:
            # 1. Choose action
            action = agent.choose_action(state)
            
            # 2. Take action in environment
            next_state, reward, done, _ = env.step(action)
            
            # 3. Update Q-values
            agent.update_q_value(state, action, reward, next_state)
            
            # 4. Move to next state
            state = next_state
            total_reward += reward
            steps += 1
            
        # Decay epsilon at the end of each episode
        agent.decay_epsilon()
        rewards_history.append(total_reward)
        
        if episode % 100 == 0:
            avg_reward = np.mean(rewards_history[-100:])
            print(f"Episode: {episode:4d} | Epsilon: {agent.epsilon:.4f} | Avg Reward (last 100): {avg_reward:.2f}")
            
    end_time = time.time()
    print(f"Training completed in {end_time - start_time:.4f} seconds.\n")
    return agent, rewards_history


# ============================================================================
# 4. EVALUATION & VISUALIZATION
# ============================================================================

def evaluate_agent(agent: QLearningAgent) -> None:
    """
    Evaluates the trained agent greedily (no exploration) and visualizes the path.
    """
    print("--- Evaluating Trained Agent ---")
    env = GridWorldEnv()
    state = env.reset()
    done = False
    
    # Temporarily set epsilon to 0 for pure exploitation
    original_epsilon = agent.epsilon
    agent.epsilon = 0.0
    
    total_reward = 0.0
    steps = 0
    
    print("Initial State:")
    env.render()
    
    while not done and steps < 20:
        action = agent.choose_action(state)
        action_name = env.action_meanings[action]
        print(f"Step {steps+1}: Agent chooses to move {action_name}")
        
        state, reward, done, info = env.step(action)
        total_reward += reward
        steps += 1
        
        env.render()
        
        if done:
            if reward > 0:
                print("Agent successfully reached the goal! 🎉")
            else:
                print("Agent fell into a pit! 💥")
                
    print(f"Total Reward Gained: {total_reward:.2f}\n")
    
    # Restore epsilon
    agent.epsilon = original_epsilon


# ============================================================================
# 5. ADVANCED TOPIC: MARKOV DECISION PROCESS VALUE ITERATION
# ============================================================================

def value_iteration_demo():
    """
    Demonstrates Value Iteration, a dynamic programming algorithm to solve known MDPs.
    Unlike Q-Learning which is model-free, Value Iteration assumes we know the transition
    probabilities and rewards (the model).
    """
    print("--- Advanced: Value Iteration ---")
    print("Value Iteration computes the optimal value function for every state iteratively.")
    
    # Simplified 1D grid world of 5 states: S0 - S1 - S2 - S3 - S4
    # Goal is at S4 (reward +10), Pit at S0 (reward -10)
    num_states = 5
    gamma = 0.9
    threshold = 1e-4
    
    # V stores the value of each state
    V = np.zeros(num_states)
    
    # Rewards for entering states
    rewards = np.array([-10, -1, -1, -1, 10])
    
    iterations = 0
    while True:
        delta = 0
        V_new = np.copy(V)
        
        # Update values for non-terminal states (S1, S2, S3)
        for s in range(1, num_states - 1):
            # Two actions: Left (-1), Right (+1)
            # Assuming deterministic transitions (P=1.0)
            
            # Action: Left
            next_s_left = s - 1
            v_left = rewards[next_s_left] + gamma * V[next_s_left]
            
            # Action: Right
            next_s_right = s + 1
            v_right = rewards[next_s_right] + gamma * V[next_s_right]
            
            # Bellman optimality update
            V_new[s] = max(v_left, v_right)
            
            delta = max(delta, abs(V_new[s] - V[s]))
            
        V = V_new
        iterations += 1
        
        if delta < threshold:
            break
            
    print(f"Value Iteration converged in {iterations} iterations.")
    print("Optimal State Values:")
    for i, v in enumerate(V):
        print(f"State {i}: {v:.2f}")
    print()


# ============================================================================
# 6. INTERVIEW CHALLENGE
# ============================================================================

def interview_challenge() -> None:
    """
    Common Reinforcement Learning Interview Question:
    "Explain the Exploration vs Exploitation tradeoff and how Epsilon-Greedy handles it."
    
    Code Challenge:
    Implement a Multi-Armed Bandit using Epsilon-Greedy strategy.
    """
    print("--- Interview Challenge: Multi-Armed Bandit ---")
    
    # Scenario: 5 slot machines (bandits) with different hidden win probabilities
    true_probabilities = [0.1, 0.5, 0.8, 0.3, 0.2]
    num_bandits = len(true_probabilities)
    
    # Agent's knowledge
    q_values = np.zeros(num_bandits)
    action_counts = np.zeros(num_bandits)
    
    epsilon = 0.1 # 10% exploration
    total_pulls = 1000
    
    total_reward = 0
    
    for _ in range(total_pulls):
        # Epsilon-Greedy Action Selection
        if random.random() < epsilon:
            # Explore: random bandit
            action = random.randint(0, num_bandits - 1)
        else:
            # Exploit: best known bandit
            action = np.argmax(q_values)
            
        # Simulate environment response
        # Win (reward 1) with true_probability, else 0
        reward = 1 if random.random() < true_probabilities[action] else 0
        total_reward += reward
        
        # Update Agent's Q-values iteratively
        # New Q = Old Q + 1/N * (Reward - Old Q)
        action_counts[action] += 1
        q_values[action] += (1 / action_counts[action]) * (reward - q_values[action])
        
    print(f"True Probabilities: {true_probabilities}")
    print(f"Agent's Estimated Probabilities (Q-values): {np.round(q_values, 2)}")
    print(f"Number of times each bandit was pulled: {action_counts}")
    print(f"Total Reward (Wins) over {total_pulls} pulls: {total_reward}")
    best_bandit_found = np.argmax(q_values)
    print(f"Agent determined Bandit {best_bandit_found} is the best. Correct? {best_bandit_found == np.argmax(true_probabilities)}\n")


# ============================================================================
# 7. UNIT TESTS
# ============================================================================

def run_tests() -> None:
    """
    Basic unit testing for the environment and agent components.
    """
    print("--- Running Unit Tests ---")
    try:
        # Test 1: Grid World Bounds
        env = GridWorldEnv((3, 3))
        state = env.reset()
        assert state == (0, 0), "Initial state should be (0,0)"
        
        next_state, _, _, _ = env.step(3) # Move Left against wall
        assert next_state == (0, 0), "Agent should not move out of bounds (Left)"
        
        next_state, _, _, _ = env.step(0) # Move Up against wall
        assert next_state == (0, 0), "Agent should not move out of bounds (Up)"
        
        # Test 2: Q-Value Update Logic
        agent = QLearningAgent(action_space=[0, 1])
        agent.alpha = 1.0 # Force replace
        agent.gamma = 0.5
        
        # Mock transition: s=(0,0), a=1, r=10, s'=(0,1). max Q(s') = 0
        agent.update_q_value((0,0), 1, 10.0, (0,1))
        assert agent.q_table["(0, 0)"][1] == 10.0, "Q-value not updated correctly for alpha=1.0"
        
        print("All internal tests passed successfully!\n")
    except AssertionError as e:
        print(f"Test Failed: {e}\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print(" PYTHON DSA & AI MASTER: REINFORCEMENT LEARNING")
    print("=" * 60 + "\n")
    
    # 1. Train the Agent
    trained_agent, _ = train_agent(episodes=600)
    
    # 2. Evaluate the Agent
    evaluate_agent(trained_agent)
    
    # 3. Advanced: Value Iteration
    value_iteration_demo()
    
    # 4. Interview Challenge (Multi-Armed Bandit)
    interview_challenge()
    
    # 5. Run internal tests
    run_tests()
    
    print("=" * 60)
    print(" END OF LESSON")
    print("=" * 60)
