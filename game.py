"""
Filename: game.py
This module defines the core functionality for a Tic-Tac-Toe game.

It includes the `Game` class, which orchestrates the game flow,
 manages the interaction between two agents, and maintains the game state.
 
The game can be run in a non-GUI mode,
 with optional terminal-based output to display the game board and status updates.

This module is intended for games that are fully autonomous, with agents providing all game input.
"""
from engine import GameState, Action
from controller import Controller
from gui import View


class GameController:
    """
    The GameController class manages the control flow of a Tic-Tac-Toe game, coordinating actions between two players (agents).
    It is responsible for running the game logic, determining the current player, processing their moves, and updating the game state.
    This class handles the non-GUI aspects of the game but can interact with the view to display the game state.
    """
    
    def __init__(self, model: GameState, view: View, player1: Controller, player2: Controller) -> None:
        """
        Initialize the GameController with two players (agents) and a view for rendering.

        Parameters:
        - model (GameState): The current game state object that holds the board and related information.
        - view (View): The view object responsible for rendering the game (CLI or GUI).
        - player1 (Controller): The controller for player 1 (e.g., human or AI).
        - player2 (Controller): The controller for player 2 (e.g., human or AI).
        """
        self.model: GameState = model  # The game state model (board and game logic)
        self.view: View = view  # The view responsible for rendering the game state
        self.player1_controller: Controller = player1  # Controller for player 1 (X)
        self.player2_controller: Controller = player2  # Controller for player 2 (O)
        
        self.current_turn: int = 1  # Track whose turn it is (1 for player 1, 2 for player 2)
        
        self.num_moves: int = 0  # Track the total number of moves made in the game
        self.move_history: list[Action] = []  # A list storing the history of moves, useful for tracking and debugging
    
    def game_loop(self) -> None:
        """
        The main game loop that runs until the game is over.
        It handles turn-taking, move processing, and view rendering.
        """
        # Continue looping until the game reaches a terminal state (win, draw)
        while not self.model.is_game_over():
            # Optionally, you can print the current move number for debugging
            print(f"Turn {self.num_moves}")
            
            # Clone the previous game state to check if it changes after a move
            prev_state: GameState = self.model.clone()

            if self.current_turn == 1:
                # If it's player 1's turn, process their input
                self.player1_controller.process_inputs(self.model, self.move_history)
            else:
                # If it's player 2's turn, process their input
                self.player2_controller.process_inputs(self.model, self.move_history)
            
            # If the game state has changed, switch turns and increment the move count
            if self.model.data != prev_state.data:
                # Toggle the turn: if it was player 1's turn, switch to player 2, and vice versa
                self.current_turn = 2 if self.current_turn == 1 else 1
                self.num_moves += 1  # Increment the move counter
            
            # Render the current game state using the view
            self.view.display(self.model)

    def result(self) -> int:
        """
        Return the outcome of a game.
        
        Returns:
        - outcome (int): the outcome of the game (-1 = lose, 0 = tie, 1 = win) for the player 1.
        """
        if self.model.is_game_over():
            if self.model.is_win():
                return 1
            elif self.model.is_lose():
                return -1
            elif self.model.is_tie():
                return 0
            else:
                raise ValueError(f"This state {self.model.data.squares} is not a terminal state")
        else:
            raise ValueError(f"This state {self.model.data.squares} is not a terminal state")
    

if __name__ == "__main__":
    from agent import RandomAgent
    from controller import HumanController, AgentController, MinimaxController
    from gui import NoView, TextView, GUIView

    model = GameState()
    view = GUIView()

    human_controller = HumanController(index=0)
    bot_controller0 = AgentController(index=0, agent=RandomAgent())
    bot_controller1 = AgentController(index=1, agent=RandomAgent())
    minimax_controller0 = MinimaxController(index=0)
    minimax_controller1 = MinimaxController(index=1)

    game = GameController(model=model, view=view, player1=bot_controller0, player2=minimax_controller1)
    game.game_loop()
    print(game.result())