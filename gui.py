import pygame
import os
from engine import GameState
from utils import get_image, get_board_matrix
from settings import *


class View:
    """Abstract class for View, which defines a display method."""
    def display(self, state: GameState) -> None:
        """Display the game state, this method must be implemented by subclasses."""
        raise NotImplementedError("Abstract class")


class NoView(View):
    """No View: A placeholder view that performs no rendering."""
    def display(self, state: GameState) -> None:
        """No rendering is performed in this method."""
        pass
    

class TextView(View):
    """CLI View: A text-based view for rendering the game state."""
    def display(self, state: GameState) -> None:
        """
        Display the game state in a text-based format.
        
        Parameters:
        - state(GameState): the state to render.
        """
        to_print: str = ""
        for i in range(3):
            to_print += "|"  # Begin each row with a vertical bar
            for j in range(3):
                mark: str
                # Determine which mark to display in each cell
                if state.data.squares[i + 3 * j] == 1:
                    mark = "X" 
                elif state.data.squares[i + 3 * j] == 2:
                    mark = "O"
                else:
                    mark = " "
                to_print += " " + mark + " " + "|"  # Add the mark and another vertical bar
            to_print += "\n"  # Move to the next line after each row
        
        print(to_print)  # Print the entire board to the terminal

        if state.is_game_over():
            print("Game over!")
        if state.is_win():
            print("Agent 'X' wins the game!")
        elif state.is_lose():
            print("Agent 'O' wins the game!")
        elif state.is_tie():
            print("It's a tie! No one wins.")



class GUIView(View):
    """GUI View: A graphical view for rendering the game state using Pygame."""
    def __init__(self) -> None:
        # Pygame Init
        pygame.init()

        # Screen
        self.GAME_W: int = GAME_W
        self.GAME_H: int = GAME_H
        self.SCREEN_W: int = self.GAME_W
        self.SCREEN_H: int = self.GAME_H
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pygame.display.set_caption(GAME_TITLE)
        self.FPS: int = FPS
        self.clock = pygame.time.Clock()

    def display(self, state: GameState) -> None:
        """
        Display the game state graphically using Pygame.
        
        Parameters:
        - state(GameState): the state to render.
        """
        screen_height = self.GAME_H
        screen_width = self.GAME_W

        # Setup dimensions for 'x' and 'o' marks
        tile_size = int(screen_height / 4)

        # Load and blit the board image for the game
        board_img = get_image(os.path.join("img", "board.png"))
        board_img = pygame.transform.scale(
            board_img, (int(screen_width), int(screen_height))
        )

        self.game_canvas.blit(board_img, (0, 0))

        # Load and blit actions for the game
        def getSymbol(input):
            if input == 0:
                return None
            elif input == 1:
                return "cross"
            else:
                return "circle"

        board_state = list(map(getSymbol, state.data.squares))

        mark_pos = 0
        for x in range(3):
            for y in range(3):
                mark = board_state[mark_pos]
                mark_pos += 1

                if mark is None:
                    continue

                mark_img = get_image(os.path.join("img", mark + ".png"))
                mark_img = pygame.transform.scale(mark_img, (tile_size, tile_size))

                self.game_canvas.blit(
                    mark_img,
                    (
                        (screen_width / 3.1) * x + (screen_width / 17),
                        (screen_width / 3.145) * y + (screen_height / 19),
                    ),
                )

        self.screen.blit(pygame.transform.scale(self.game_canvas,
                                                (self.SCREEN_W, self.SCREEN_H)),
                                                (0, 0))
        pygame.display.update()
        if state.is_game_over():
            print("Game over!")
        if state.is_win():
            print("Agent 'X' wins the game!")
        elif state.is_lose():
            print("Agent 'O' wins the game!")
        elif state.is_tie():
            print("It's a tie! No one wins.")
        self.clock.tick(self.FPS)


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    matrix = get_board_matrix(os.path.join("img", "board.png"))
    print(matrix.shape)
    print(np.unique(matrix))
    plt.imshow(matrix)
    plt.show()
