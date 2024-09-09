import pygame
import numpy as np
from os import path as os_path
from settings import GAME_H, GAME_W

def get_image(path: str) -> pygame.Surface:
    """Return a pygame image loaded from the given path."""
    cwd = os_path.dirname(__file__)
    image = pygame.image.load(cwd + "/" + path)
    return image

def get_board_matrix(path: str) -> np.ndarray:
    surface: pygame.Surface = get_image(path)
    return pygame.surfarray.array2d(surface)

def inside_case(pos: tuple[int, int], board: np.ndarray) -> int:
    """
    Check if the mouse is inside a case and return the position.

    Returns:
    - pos(int): the pos of the case.
    """
    size_board = board.shape
    value_case: int = 5
    lower_bounds: tuple[int, int] = (3, 3)
    upper_bounds: tuple[int, int] = (95, 95)

    board[0:lower_bounds[0], :] = 0
    board[upper_bounds[1]:, :] = 0
    board[:, 0:lower_bounds[1]] = 0
    board[:, upper_bounds[1]:] = 0
    board[board != value_case] = 0

    x = int(pos[0]*size_board[0]/GAME_W)
    y = int(pos[1]*size_board[1]/GAME_H)

    b1: int = 5
    b2: int = 37
    b3: int = 69
    space: int = 25
    if board[x, y] == value_case:
        if x >= b1 and x <= b1 + space:
            if y >= b1 and y <= b1 + space:
                return 0
            elif y >= b2 and y <= b2 + space:
                return 1
            elif y >= b3 and y <= b3 + space:
                return 2
            else:
                return -1
        elif x >= b2 and x <= b2 + space:
            if y >= b1 and y <= b1 + space:
                return 3
            elif y >= b2 and y <= b2 + space:
                return 4
            elif y >= b3 and y <= b3 + space:
                return 5
            else:
                return -1
        elif x >= b3 and x <= b3 + space:
            if y >= b1 and y <= b1 + space:
                return 6
            elif y >= b2 and y <= b2 + space:
                return 7
            elif y >= b3 and y <= b3 + space:
                return 8
            else:
                return -1
        else:
            return -1
    else:
        return -1

