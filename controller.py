import pygame
import sys
import os
import numpy as np
from engine import GameState, Action
from agent import Agent
from settings import GAME_H, GAME_W
from utils import get_board_matrix, inside_case
from minimax import alpha_beta_search
from mcts import Node, monte_carlo_tree_search


class Controller:
    """
    Abstract base class for game controllers, representing a player (human or AI).
    This class defines the interface that all specific controller types (e.g., HumanController, AIController) must implement.
    It is responsible for processing player inputs and updating the game state accordingly.
    """
    
    def __init__(self, index: int) -> None:
        """
        Initialize the Controller with a player index (0 for player 1, 1 for player 2).

        Parameters:
        - index (int): The player's index, where 0 represents player 1 and 1 represents player 2.
        
        Raises:
        - AssertionError: If the index is not 0 or 1, as there are only two players allowed.
        """
        # Ensure the index is either 0 or 1 (for two-player games like Tic-Tac-Toe)
        assert index in [0, 1], f"Only two players, got player number {index}"
        self.index: int = index  # Store the player's index (0 for X, 1 for O)
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        """
        Process player inputs and modify the game state. Must be implemented by subclasses.
        
        Parameters:
        - state (GameState): The current state of the game.
        - move_history (list[Action] | None): Optional history of previous moves (useful for AI decision-making).
        
        Raises:
        - NotImplementedError: This method must be overridden in subclasses to provide specific behavior for each controller type.
        """
        raise NotImplementedError("Abstract class - process_inputs must be implemented in subclasses")


class HumanController(Controller):
    """
    HumanController handles input from a human player, such as mouse clicks in a graphical interface (GUI).
    It extends the base Controller class and provides functionality to gather and process human inputs during the game.
    """
    
    def __init__(self, index: int) -> None:
        """
        Initialize the HumanController for a specific player (X or O).

        Parameters:
        - index (int): The player's index, where 0 represents player 1 and 1 represents player 2.
        """
        # Call the parent Controller class to initialize the player's index
        super().__init__(index)

    def get_inputs(self) -> Action:
        """
        Capture input from a human player and translate it into a game action.
        This method listens for mouse clicks to determine the player's move.

        Returns:
        - Action: The action object containing the player's index and the selected position on the board.
        """
        computed_pos: int = -1  # Initialize the position as -1 (invalid by default)

        # Loop through the events captured by pygame
        for event in pygame.event.get():
            # If the user tries to close the game window, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()  # Close the pygame window
                sys.exit()  # Exit the program

            # Check if the player has clicked the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # Get the position of the mouse click

                # Convert the mouse position to a board position
                computed_pos = inside_case(mouse_pos, get_board_matrix(os.path.join("img", "board.png")))

        # Return an Action object with the player's index and the computed board position
        return Action(agent=self.index, pos=computed_pos)

    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        """
        Process the human player's input and apply their move to the game state.
        
        Parameters:
        - state (GameState): The current state of the game.
        - move_history (list[Action] | None): A list storing previous moves (optional).
        """
        # Get the player's action (input) by calling get_inputs
        action: Action = self.get_inputs()

        # Check if the chosen position is a legal move
        if action.pos in state.get_legal_moves():
            # If move history tracking is enabled, add this move to the history
            if move_history:
                move_history.append(action)

            # Apply the action to the game state (update the board)
            state.apply_action(action)
        else:
            # If the move is illegal, do nothing (can add feedback or error handling here if needed)
            pass


class MinimaxController(Controller):
    """
    MinimaxController is responsible for selecting moves using the Minimax algorithm with Alpha-Beta pruning.
    It extends the base Controller class and implements the logic for an AI player that optimizes its move selection.
    """

    def __init__(self, index: int) -> None:
        """
        Initialize the MinimaxController for a specific player (X or O).

        Parameters:
        - index (int): The player's index, where 0 represents player 1 (X) and 1 represents player 2 (O).
        """
        # Call the parent Controller class to initialize the player's index
        super().__init__(index)
    
    def select_move(self, state: GameState) -> Action:
        """
        Select the best move for the AI player using the Minimax algorithm with Alpha-Beta pruning.

        Parameters:
        - state (GameState): The current state of the game.

        Returns:
        - Action: The optimal action selected based on the Minimax evaluation.
        """
        # Initialize best_value based on the player's index:
        # Player 0 (X) is maximizing, so best_value starts at negative infinity.
        # Player 1 (O) is minimizing, so best_value starts at positive infinity.
        if self.index == 0:
            best_value = -np.inf  # Maximizing player
        else:
            best_value = np.inf  # Minimizing player

        # Initialize the best action with a default invalid move (-1).
        best_action = Action(agent=self.index, pos=-1)

        # Loop through all legal moves available in the current game state
        for pos in state.get_legal_moves():
            action = Action(agent=self.index, pos=pos)  # Create an action for each move
            successor = state.generate_successor(action)  # Generate the resulting state after the action
            
            # Use Alpha-Beta search to evaluate the value of the successor state
            value = alpha_beta_search(successor, self.index)

            # Maximizing player 0 (X): update if a higher value is found
            if self.index == 0:
                if value > best_value:
                    best_value = value
                    best_action = action
            # Minimizing player 1 (O): update if a lower value is found
            else:
                if value < best_value:
                    best_value = value
                    best_action = action

        # Return the best action determined by the Minimax algorithm
        return best_action
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        """
        Process the inputs by selecting and applying the best move using the Minimax algorithm.
        
        Parameters:
        - state (GameState): The current state of the game.
        - move_history (list[Action] | None): A list storing previous moves (optional).
        """
        # Select the best move using the Minimax algorithm
        action: Action = self.select_move(state=state)

        # Check if the selected move is a legal move
        if action.pos in state.get_legal_moves():
            # If move history tracking is enabled, add this move to the history
            if move_history:
                move_history.append(action)

            # Apply the selected action to the game state (update the board)
            state.apply_action(action)
        else:
            # If the move is illegal, do nothing (can add feedback or error handling here if needed)
            pass


class MCTSController(Controller):
    """
    """
    def __init__(self, index: int, simulations: int = 1000) -> None:
        super().__init__(index)
        self.simulations: int = simulations
        self.exploration_value: float = 2.
    
    def select_move(self, state: GameState) -> Action:

        root: Node = Node(state=state)

        best_node: Node = monte_carlo_tree_search(root=root,
                                                  iterations=self.simulations,
                                                  index=self.index,
                                                  c=self.exploration_value)

        return Action(agent=self.index, pos=best_node.pos)
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        """
        Process the inputs by selecting and applying the agent's move based on the current game state.
        
        Parameters:
        - state (GameState): The current state of the game.
        - move_history (list[Action] | None): A list storing previous moves (optional).
        """
        # Select the agent's move using the select_move method
        action: Action = self.select_move(state=state)

        # Check if the selected move is a legal move
        if action.pos in state.get_legal_moves():
            # If move history tracking is enabled, add this move to the history
            if move_history:
                move_history.append(action)

            # Apply the selected action to the game state (update the board)
            state.apply_action(action)
        else:
            # If the move is illegal, do nothing (can add feedback or error handling here if needed)
            pass


class AgentController(Controller):
    """
    AgentController manages the actions of an AI agent (e.g., RandomAgent or a more complex RL agent).
    It extends the base Controller class and is responsible for making decisions based on the AI agent's policy.
    This controller interacts with the game state by selecting moves from the agent and applying them.
    """
    
    def __init__(self, index: int, agent: Agent) -> None:
        """
        Initialize the AgentController with a player index and the associated AI agent.
        
        Parameters:
        - index (int): The player's index, where 0 represents player 1 (X) and 1 represents player 2 (O).
        - agent (Agent): The AI agent responsible for selecting moves, which could be a simple agent (like RandomAgent) or a more advanced one (like a reinforcement learning agent).
        """
        # Call the parent Controller class to initialize the player's index
        super().__init__(index)
        self.agent: Agent = agent  # Store the agent responsible for move selection
    
    def select_move(self, state: GameState) -> Action:
        """
        Select the next move for the AI agent based on the current game state.
        
        Parameters:
        - state (GameState): The current state of the game.
        
        Returns:
        - Action: The action selected by the agent, consisting of the player's index and the position on the board.
        """
        # Use the agent's policy to determine the position of the next move
        pos: int = self.agent.get_action(state)
        
        # Return an Action object with the player's index and selected position
        return Action(agent=self.index, pos=pos)
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        """
        Process the inputs by selecting and applying the agent's move based on the current game state.
        
        Parameters:
        - state (GameState): The current state of the game.
        - move_history (list[Action] | None): A list storing previous moves (optional).
        """
        # Select the agent's move using the select_move method
        action: Action = self.select_move(state=state)

        # Check if the selected move is a legal move
        if action.pos in state.get_legal_moves():
            # If move history tracking is enabled, add this move to the history
            if move_history:
                move_history.append(action)

            # Apply the selected action to the game state (update the board)
            state.apply_action(action)
        else:
            # If the move is illegal, do nothing (can add feedback or error handling here if needed)
            pass

