# Basic Game: Professional Tic-Tac-Toe with AI

## 📖 What is this?
This project is a comprehensive, production-grade implementation of the classic game **Tic-Tac-Toe** running in the terminal. It goes beyond a simple script by employing robust Object-Oriented Programming (OOP) principles, the Minimax algorithm for an unbeatable AI opponent, and extensive error handling.

## 🎯 Why does it exist?
Building a basic game like Tic-Tac-Toe is a rite of passage for software engineers. However, transitioning from a basic script to a professional-grade application requires understanding:
1. **Separation of Concerns**: Decoupling the game logic (Model) from the user interface (View).
2. **Artificial Intelligence**: Implementing decision-making algorithms like Minimax.
3. **State Management**: Handling game states (in-progress, draw, win).
4. **Defensive Programming**: Handling unexpected user input gracefully.

## 🏗️ Architecture
The system is built using an Object-Oriented approach:

1. **`Board` Class**: 
   - Manages the state of the 3x3 grid.
   - Responsible for placing moves, checking for wins, and determining available spaces.
2. **`Player` Abstract Base Class**:
   - Defines the interface for a player.
3. **`HumanPlayer` Class (Inherits `Player`)**:
   - Handles standard IO to get moves from a human user.
4. **`AIPlayer` Class (Inherits `Player`)**:
   - Uses the **Minimax Algorithm** to calculate the most optimal move.
5. **`TicTacToeGame` Class**:
   - Orchestrates the game loop, alternating turns, and checking win/draw conditions.

## 🧠 Advanced Concepts: The Minimax Algorithm
The AI uses the Minimax algorithm, a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst-case scenario. When dealing with gains, it is referred to as "maximin"—to maximize the minimum gain.

In our game:
- The AI plays out *every possible future move* on a simulated board.
- It scores a win as +1, a loss as -1, and a draw as 0.
- It chooses the branch that guarantees the highest possible score regardless of what the human does.
- This makes the AI **unbeatable**.

## 🚀 Extensions & Interview Variations
If you were asked to build this in an interview, you might face these follow-up requests:
1. **Dynamic Board Size**: Modify the `Board` to accept an `n x n` size instead of hardcoding 3x3.
2. **Alpha-Beta Pruning**: Optimize the Minimax algorithm to skip evaluating branches that are demonstrably worse than a previously evaluated branch.
3. **Multiplayer via Sockets**: Separate the application into a client-server model where two players connect over TCP.
4. **GUI Integration**: Replace the terminal UI with a PySide6 or Tkinter graphical interface without changing the core game logic.

## 🛠️ Execution
To run the game:
```bash
python main.py
```
