"""
Professional Tic-Tac-Toe Implementation
=======================================

This module contains a production-grade implementation of Tic-Tac-Toe,
featuring Object-Oriented design, type hinting, and an unbeatable AI 
using the Minimax algorithm.

Please see the README.md for architectural details and conceptual explanations.
"""

import math
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod


class Board:
    """
    Represents the Tic-Tac-Toe playing board.
    Handles board state, move validation, and win detection.
    """
    def __init__(self) -> None:
        # Initialize an empty 3x3 board with spaces
        self.state: List[str] = [' ' for _ in range(9)]

    def display(self) -> None:
        """Prints the current board state to the console."""
        print("\n")
        for row in range(3):
            print(f" {self.state[row*3]} | {self.state[row*3+1]} | {self.state[row*3+2]} ")
            if row < 2:
                print("---+---+---")
        print("\n")

    def make_move(self, position: int, symbol: str) -> bool:
        """
        Attempts to place a symbol on the board.
        Returns True if successful, False if the position is invalid/occupied.
        """
        if 0 <= position < 9 and self.state[position] == ' ':
            self.state[position] = symbol
            return True
        return False

    def get_available_moves(self) -> List[int]:
        """Returns a list of indices that are currently empty."""
        return [i for i, cell in enumerate(self.state) if cell == ' ']

    def has_winner(self, symbol: str) -> bool:
        """Checks if the given symbol has achieved a winning combination."""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        return any(all(self.state[pos] == symbol for pos in combo) for combo in winning_combinations)

    def is_full(self) -> bool:
        """Checks if the board is completely filled."""
        return ' ' not in self.state

    def copy(self) -> 'Board':
        """Returns a deep copy of the board (useful for AI simulations)."""
        new_board = Board()
        new_board.state = self.state.copy()
        return new_board


class Player(ABC):
    """Abstract base class representing a generic player."""
    def __init__(self, symbol: str):
        self.symbol = symbol

    @abstractmethod
    def get_move(self, board: Board) -> int:
        """Determine the next move based on the board state."""
        pass


class HumanPlayer(Player):
    """Represents a human player interacting via standard IO."""
    def get_move(self, board: Board) -> int:
        valid_move = False
        move = -1
        while not valid_move:
            try:
                user_input = input(f"Player {self.symbol}, enter your move (1-9): ")
                # Adjust for 0-indexed internal board representation
                move = int(user_input) - 1
                if move in board.get_available_moves():
                    valid_move = True
                else:
                    print("Invalid move. Cell is either occupied or out of range. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 9.")
        return move


class AIPlayer(Player):
    """Represents an AI opponent utilizing the Minimax algorithm."""
    
    def __init__(self, symbol: str):
        super().__init__(symbol)
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'

    def get_move(self, board: Board) -> int:
        print(f"AI ({self.symbol}) is thinking...")
        best_score = -math.inf
        best_move = -1
        
        for move in board.get_available_moves():
            board.make_move(move, self.symbol)
            score = self.minimax(board, 0, False)
            board.state[move] = ' '  # Undo move
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move

    def minimax(self, board: Board, depth: int, is_maximizing: bool) -> float:
        """
        The Minimax algorithm.
        Returns a score representing the desirability of the board state.
        """
        # Base cases: Terminal states
        if board.has_winner(self.symbol):
            return 10 - depth  # Prefer faster wins
        if board.has_winner(self.opponent_symbol):
            return depth - 10  # Penalize faster losses
        if board.is_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.symbol)
                score = self.minimax(board, depth + 1, False)
                board.state[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for move in board.get_available_moves():
                board.make_move(move, self.opponent_symbol)
                score = self.minimax(board, depth + 1, True)
                board.state[move] = ' '
                best_score = min(score, best_score)
            return best_score


class TicTacToeGame:
    """Orchestrates the game loop and state transitions."""
    def __init__(self, player1: Player, player2: Player):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_index = 0

    def play(self) -> None:
        print("Welcome to Professional Tic-Tac-Toe!")
        print("Positions are mapped 1-9 starting from top-left to bottom-right.")
        
        self.board.display()
        
        while True:
            current_player = self.players[self.current_player_index]
            
            # 1. Get and apply move
            move = current_player.get_move(self.board)
            self.board.make_move(move, current_player.symbol)
            self.board.display()
            
            # 2. Check for win
            if self.board.has_winner(current_player.symbol):
                print(f"🎉 Player {current_player.symbol} wins! 🎉")
                break
                
            # 3. Check for draw
            if self.board.is_full():
                print("It's a draw! 🤝")
                break
                
            # 4. Switch turns
            self.current_player_index = 1 - self.current_player_index


# -----------------------------------------------------------------------------
# Test Harness / Main Guard
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # You can change these to two HumanPlayers or two AIPlayers!
    p1 = HumanPlayer("X")
    p2 = AIPlayer("O")
    
    game = TicTacToeGame(p1, p2)
    game.play()
