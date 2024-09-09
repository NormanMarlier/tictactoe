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
    The Game class manages the control flow of a Tic-Tac-Toe game, coordinating actions between two agents.
    This class is responsible for running the game logic, determining the current player, processing their moves,
    and updating the game state. It handles the non-GUI aspects of the game but can print the board and game status 
    to the terminal if needed.
    """
    
    def __init__(self, model: GameState, view: View, player1: Controller, player2: Controller) -> None:
        """
        Initialize the Game with two agents and a display option.
        
        Parameters:
        - agent_x: The agent playing as 'X'.
        - agent_o: The agent playing as 'O'.
        - display: A boolean flag to determine whether to print the game board to the terminal.
        """
        self.model: GameState = model
        self.view: View = view
        self.player1_controller: Controller = player1
        self.player2_controller: Controller = player2
        
        self.current_turn: int = 1 # Store the current turn
        
        self.num_moves: int = 0
        self.move_history: list[Action] = []  # Store move history as a list of (agent index, position) tuples
    
    def game_loop(self) -> None:
        
        while not self.model.is_game_over():
            #print(f"Turn {self.num_moves}")
            # Get the current state
            prev_state: GameState = self.model.clone()
            if self.current_turn == 1:
                # Apply move
                self.player1_controller.process_inputs(self.model, self.move_history)
            else:
                # Apply move
                self.player2_controller.process_inputs(self.model, self.move_history)
            # Check if the game state changes
            if self.model.data != prev_state.data:
                self.current_turn = 2 if self.current_turn == 1 else 1
                self.num_moves += 1
            
            # Display
            self.view.display(self.model)
    

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

    game = GameController(model=model, view=view, player1=minimax_controller0, player2=bot_controller1)
    game.game_loop()