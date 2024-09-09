import pygame
import sys
import os
import numpy as np
from engine import GameState, Action
from agent import Agent
from settings import GAME_H, GAME_W
from utils import get_board_matrix, inside_case
from minimax import alpha_beta_search


class Controller:
    """Abstract class"""
    def __init__(self, index: int) -> None:
        assert index in [0, 1], f"Only two players, got player number {index}"
        self.index: int = index
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        raise NotImplementedError("Abstract class")


class HumanController(Controller):
    """
    This controller is responsible for collecting human input
    (e.g., a mouse click in the GUI or keyboard input in CLI).
    """
    def __init__(self, index: int) -> None:
        super().__init__(index)

    def get_inputs(self) -> Action:
        """
        Get inputs from a human player
        
        Returns:
        - Action: the action performed by the human player.
        """
        computed_pos: int = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                computed_pos = inside_case(mouse_pos, get_board_matrix(os.path.join("img", "board.png")))

        return Action(agent=self.index, pos=computed_pos)

    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        action: Action = self.get_inputs()
        if action.pos in state.get_legal_moves():
            if move_history:
                move_history.append(action)
            state.apply_action(action)
        else:
            # Do nothing
            pass


class MinimaxController(Controller):
    """"""
    def __init__(self, index: int) -> None:
        super().__init__(index)
    
    def select_move(self, state: GameState) -> Action:
        if self.index == 0:
            best_value = -np.inf
        else:
            best_value = np.inf
        best_action = Action(agent=self.index, pos=-1)
        for pos in state.get_legal_moves():
            action = Action(agent=self.index, pos=pos)
            successor = state.generate_successor(action)
            value = alpha_beta_search(successor, self.index)
            print(f"value {value} - action {action}")
            if self.index == 0:
                if value > best_value:
                    best_value = value
                    best_action = action
            else:
                if value < best_value:
                    best_value = value
                    best_action = action

        
        return best_action
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        action: Action = self.select_move(state=state)
        if action.pos in state.get_legal_moves():
            if move_history:
                move_history.append(action)
            state.apply_action(action)
        else:
            # Do nothing
            pass



class AgentController(Controller):
    """
    This controller is responsible for collecting actions
    from an agent. It can be a trivial angent (RandomAgent) or
    a more sophisticated one such as a rl agent.
    """
    def __init__(self, index: int, agent: Agent) -> None:
        super().__init__(index)
        self.agent: Agent = agent
    
    def select_move(self, state: GameState) -> Action:
        pos: int = self.agent.get_action(state)
        return Action(agent=self.index, pos=pos)
    
    def process_inputs(self, state: GameState, move_history: list[Action] | None) -> None:
        action: Action = self.select_move(state=state)
        if action.pos in state.get_legal_moves():
            if move_history:
                move_history.append(action)
            state.apply_action(action)
        else:
            # Do nothing
            pass
