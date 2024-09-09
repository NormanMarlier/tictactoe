import random
import pygame

from engine import GameState, Action

class Agent:
    """
    An agent must define a get_action method, but may also define the
    following methods which will be called if they exist:

    def register_initial_state(self, state): # inspects the starting state
    """
    def get_action(self, state: GameState) -> int:
        """
        The Agent will receive a GameState and
        must return an action.
        """
        raise NotImplementedError()

    def register_initial_state(self, state: GameState):
        """
        The Agent will receive a GameState and
        must return an action.
        """
        raise NotImplementedError()


class RandomAgent(Agent):

    def get_action(self, state: GameState) -> int:
        return random.choice(state.get_legal_moves())