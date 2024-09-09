"""
Filename: engine.py

Description:
This Python file implements a simple Tic-Tac-Toe game.

The game logic revolves around managing the state of the board,
validating player moves, and determining the game outcome (win, lose, or tie).

The core classes and functions allow for game state transitions, generating legal moves,
and exploring all possible successor states for a given game configuration.

The file also includes a set of unit tests to ensure the correctness of the game mechanics and state management.
"""

import unittest
from copy import deepcopy
from dataclasses import dataclass

@dataclass
class Action:
    """Action performed by Controller."""
    agent: int
    pos: int


class GameState:
    """
    GameState represents the state of a game at a given point in time.
    It manages the current game board, tracks win/lose/tie conditions,
    and can generate successors for game tree exploration.
    """
    def __init__(self, prev_state: 'GameState | None' = None) -> None:
        """
        Initialize a new GameState.
        
        If a previous state is provided, the new state is a deep copy of the previous state,
        preserving the game's history. If no previous state is provided, a new game starts
        with an empty board.
        
        Parameters:
        - prev_state: The previous GameState to copy (optional).
        """
        if prev_state is not None:
            self.data: 'GameStateData' = deepcopy(prev_state.data)
        else:
            self.data = GameStateData()
    
    def is_game_over(self) -> bool:
        """
        Check if the game has ended (win/loss/draw)
        
        Returns:
        - bool: True if the state is a terminal state, False otherwise.
        """
        return self.is_win() or self.is_lose() or self.is_tie()
    
    def is_win(self) -> bool:
        """
        Check if the current state is a winning state.
        
        Returns:
        - bool: True if the current player has won the game, False otherwise.
        """
        return self.data._win
    
    def is_lose(self) -> bool:
        """
        Check if the current state is a losing state.
        
        Returns:
        - bool: True if the current player has lost the game, False otherwise.
        """
        return self.data._lose
    
    def is_tie(self) -> bool:
        """
        Check if the current state is a tie.
        
        Returns:
        - bool: True if the game is a tie, i.e., no more legal moves are available and no winner.
        """
        return self.data._tie
    
    def update(self) -> None:
        """
        Compute and update the outcome of the game based on the current state.
        
        This method checks all possible winning combinations to determine if the game
        has been won or lost. If the board is full and no winner is found, it sets the game
        as a tie.
        """
        for indices in self.data.winning_combinations:
            states = [self.data.squares[idx] for idx in indices]
            if states == [1, 1, 1]:
                self.data._win = True
            elif states == [2, 2, 2]:
                self.data._lose = True
        if self.data.squares.count(0) == 0:
            self.data._tie = True
    
    def get_legal_moves(self) -> list[int]:
        """
        Get a list of all legal moves available in the current state.
        
        Legal moves are positions on the board that are not yet occupied.
        
        Returns:
        - list[int]: A list of indices corresponding to empty positions on the board.
        """
        # Check that successors exist
        if self.is_win() or self.is_lose() or self.is_tie():
            return []
        return [i for i, mark in enumerate(self.data.squares) if mark == 0]
    
    def apply_action(self, move: Action) -> None:
        """Place a mark by the agent in the spot given.

        The following are required for a move to be valid:
        * The agent must be a known agent ID (either 0 or 1).
        * The spot must be be empty.
        * The spot must be in the board (integer: 0 <= spot <= 8)

        If any of those are not true, an assertion will fail.
        """
        assert move.pos >= 0 and move.pos <= 8, "Invalid insert location"
        assert move.agent in [0, 1], "Invalid agent"
        assert self.data.squares[move.pos] == 0, "Location is not empty"

        # agent is [0, 1]. board values are stored as [1, 2].
        self.data.squares[move.pos] = move.agent + 1
        self.update()
    
    def generate_successor(self, move: Action) -> 'GameState':
        """
        Generate a successor GameState by applying an action.

        This method creates a new GameState based on the current state and applies
        the action taken by the agent (placing a mark on the board). It then computes
        the outcome of the game after this move.
        
        Parameters:
        - agent_index: The index of the agent making the move (1 or 2).
        - pos: The position on the board where the agent wants to place their mark.
        
        Returns:
        - GameState: The new game state after the move has been applied.

        Raises:
        - Exception: If the current state is terminal (win/lose/tie), no successor can be generated.
        """
        # Check that successors exist
        if self.is_game_over():
            raise Exception('Can\'t generate a successor of a terminal state.')

        # Copy current state
        state = self.clone()
        # Apply action
        state.apply_action(move)
        return state

    def generate_successors(self, agent_index: int) -> list['GameState']:
        """
        Generate all possible successor states from the current state.

        For each legal move available, this method generates a new GameState
        representing the board after that move has been made.
        
        Parameters:
        - agent_index: The index of the agent making the move (1 or 2).
        
        Returns:
        - list[GameState]: A list of all possible successor game states.
        """
        return [self.generate_successor(Action(agent=agent_index, pos=pos)) for pos in self.get_legal_moves()]

    def clone(self) -> 'GameState':
        """
        Create a deepcopy of the current state.
        
        Returns:
        - GameState: a deepcopy of the state.
        """
        return deepcopy(self)


# Generate with ChatGPT
class TestGameState(unittest.TestCase):

    def test_initial_state(self):
        """Test that a new GameState initializes with no win, lose, or tie condition."""
        state = GameState()
        self.assertFalse(state.is_win())
        self.assertFalse(state.is_lose())
        self.assertFalse(state.is_tie())
        self.assertEqual(state.get_legal_moves(), list(range(9)))

    def test_win_detection(self):
        """Test that the game correctly identifies a win."""
        state = GameState()
        state.data.squares = [1, 1, 1, 0, 0, 0, 0, 0, 0]  # Player 1 wins on top row
        state.update()
        self.assertTrue(state.is_win())
        self.assertFalse(state.is_lose())
        self.assertFalse(state.is_tie())

    def test_lose_detection(self):
        """Test that the game correctly identifies a loss."""
        state = GameState()
        state.data.squares = [2, 2, 2, 0, 0, 0, 0, 0, 0]  # Player 2 wins on top row
        state.update()
        self.assertFalse(state.is_win())
        self.assertTrue(state.is_lose())
        self.assertFalse(state.is_tie())

    def test_tie_detection(self):
        """Test that the game correctly identifies a tie."""
        state = GameState()
        state.data.squares = [1, 2, 1, 1, 1, 2, 2, 1, 2]  # Board is full, no winner
        state.update()
        self.assertFalse(state.is_win())
        self.assertFalse(state.is_lose())
        self.assertTrue(state.is_tie())

    def test_get_legal_moves(self):
        """Test that the game returns the correct legal moves."""
        state = GameState()
        state.data.squares = [1, 2, 0, 1, 2, 0, 1, 2, 0]  # Some positions filled
        legal_moves = state.get_legal_moves()
        self.assertEqual(legal_moves, [2, 5, 8])

    def test_generate_successor(self):
        """Test generating a successor state after a move."""
        state = GameState()
        new_state = state.generate_successor(Action(agent=0, pos=0))  # Player 1 marks position 0
        self.assertEqual(new_state.data.squares[0], 1)
        self.assertNotEqual(state.data.squares, new_state.data.squares)  # Ensure original state is unchanged

    def test_generate_successors(self):
        """Test generating all possible successor states."""
        state = GameState()
        successors = state.generate_successors(0) # Player 1 tests all legal actions
        self.assertEqual(len(successors), 9)
        for i, successor in enumerate(successors):
            self.assertEqual(successor.data.squares[i], 1)

    def test_generate_successor_on_terminal_state(self):
        """Test that generating a successor from a terminal state raises an exception."""
        state = GameState()
        state.data.squares = [1, 1, 1, 0, 0, 0, 0, 0, 0]  # Player 1 wins
        state.update()
        with self.assertRaises(Exception):
            state.generate_successor(Action(agent=0, pos=3))
        

class GameStateData:
    """
    GameStateData stores the data associated with a particular state of the game.
    It includes the state of the board, the status of the game (win/lose/tie), and
    the winning combinations that can determine the outcome of the game.
    """

    # A list of all possible winning combinations on a 3x3 board.
    winning_combinations: list[tuple[int, int, int]] = [
        (0, 1, 2),  # Top row
        (3, 4, 5),  # Middle row
        (6, 7, 8),  # Bottom row
        (0, 3, 6),  # Left column
        (1, 4, 7),  # Middle column
        (2, 5, 8),  # Right column
        (0, 4, 8),  # Diagonal from top-left to bottom-right
        (2, 4, 6),  # Diagonal from top-right to bottom-left
    ]

    def __init__(self, prev_state: 'GameStateData | None' = None) -> None:
        """
        Initialize the GameStateData.
        
        If a previous state is provided, this instance is a deep copy of that state,
        preserving the game history. Otherwise, it initializes a new game with an empty
        board and default win/lose/tie conditions.
        
        Parameters:
        - prev_state: The previous GameStateData to copy (optional).
        """
        self.squares: list[int]
        self._win: bool
        self._lose: bool
        self._tie: bool
        if prev_state is not None:
            # Deep copy the previous state's data to maintain independent state history
            self.squares = deepcopy(prev_state.squares)
            self._win = deepcopy(prev_state._win)
            self._lose = deepcopy(prev_state._lose)
            self._tie = deepcopy(prev_state._tie)
        else:
            # Initialize a new game with an empty 3x3 board
            self.squares = [0] * 9
            self._win = False
            self._lose = False
            self._tie = False
    
    def __eq__(self, other):
        """
        Compare this GameStateData with another for equality.
        
        Two GameStateData instances are considered equal if their board states (squares)
        are identical.
        
        Parameters:
        - other: The other GameStateData instance to compare against.
        
        Returns:
        - bool: True if the board states are identical, False otherwise.
        """
        if other is None:
            return False
        return self.squares == other.squares


# Generate with ChatGPT
class TestGameStateData(unittest.TestCase):

    def test_initial_state(self):
        """Test that a new GameStateData instance initializes with an empty board and no win/lose/tie."""
        state = GameStateData()
        self.assertEqual(state.squares, [0] * 9)
        self.assertFalse(state._win)
        self.assertFalse(state._lose)
        self.assertFalse(state._tie)

    def test_copy_state(self):
        """Test that copying a GameStateData instance creates a deep copy."""
        state1 = GameStateData()
        state1.squares[0] = 1
        state1._win = True
        state1._lose = False
        state1._tie = False

        state2 = GameStateData(state1)

        self.assertEqual(state2.squares, state1.squares)
        self.assertEqual(state2._win, state1._win)
        self.assertEqual(state2._lose, state1._lose)
        self.assertEqual(state2._tie, state1._tie)

        # Modify original state and ensure copy does not change
        state1.squares[1] = 2
        self.assertNotEqual(state2.squares, state1.squares)

    def test_equality(self):
        """Test that two GameStateData instances with the same state are considered equal."""
        state1 = GameStateData()
        state2 = GameStateData()

        self.assertEqual(state1, state2)

        state1.squares[0] = 1
        self.assertNotEqual(state1, state2)

        state2.squares[0] = 1
        self.assertEqual(state1, state2)

    def test_equality_with_none(self):
        """Test that comparing a GameStateData instance with None returns False."""
        state = GameStateData()
        self.assertNotEqual(state, None)


if __name__ == '__main__':
    unittest.main()