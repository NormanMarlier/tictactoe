import argparse
from engine import GameState
from agent import RandomAgent
from controller import Controller, HumanController, AgentController, MinimaxController
from gui import View, NoView, TextView, GUIView
from game import GameController


def get_controller_from_option(option: str, index: int) -> Controller:
    """
    Get a Controller for a player based on the selected option.

    Parameters:
    - option (str): The type of controller ("human", "agent", "minimax", "random").
    - index (int): The index of the player (used to identify the player).

    Returns:
    - Controller: A controller object for the player based on the selected option.
    """
    # List of valid options for the controller types
    available_options: list[str] = ["human", "agent", "minimax", "random"]

    # Ensure that the option provided is one of the available options
    assert option in available_options, f"Invalid option: {option}. Expected one of {available_options}"

    # Return the appropriate controller based on the selected option
    if option == "human":
        # Return a HumanController, used for player-controlled input
        return HumanController(index=index)
    
    elif option == "agent":
        # Placeholder for an agent-based controller (likely to be implemented later)
        pass  # No agent controller defined yet
    
    elif option == "minimax":
        # Return a MinimaxController, used for an AI that uses the minimax algorithm
        return MinimaxController(index=index)
    
    elif option == "random":
        # Return an AgentController with a RandomAgent, which makes random moves
        return AgentController(index=index, agent=RandomAgent())
    
    else:
        # Raise an error if an invalid option is provided (this should never happen due to the earlier assert)
        raise ValueError(f"option: {option} not in available options: {available_options}")



def get_view_from_option(option: str) -> View:
    """
    Get the appropriate renderer (view) for the game based on the selected option.

    Parameters:
    - option (str): The type of rendering. Can be "gui", "text", or other.

    Returns:
    - View: The renderer object that handles how the game state is displayed.
    """
    # If the option is "gui", return the GUI-based view for graphical rendering
    if option == "gui":
        return GUIView()
    
    # If the option is "text", return the text-based view for CLI rendering
    elif option == "text":
        return TextView()
    
    # For any other option (or default), return a NoView, which performs no rendering
    else:
        return NoView()


def play_game(view: View, player1: Controller, player2: Controller) -> int:
    """
    Play a game and return the outcome.
    
    Parameters:
    - view (View): the renderer.
    - player1 (Controller): player 1 (X)
    - player2 (Controller): player 2 (O).
    
    Returns:
    - outcome (int): the outcome of the game.
    """
    # Initial state
    model: GameState = GameState()

    # Game Controller
    game: GameController = GameController(model=model,
                                          view=view,
                                          player1=player1,
                                          player2=player2)
    # Game loop
    game.game_loop()

    return game.result()


def main(args) -> None:

    # View
    view: View = get_view_from_option(args.view)
    
    # Controllers
    player_1: Controller = get_controller_from_option(args.player1, 0)
    player_2: Controller = get_controller_from_option(args.player2, 1)

    play_game(view=view, player1=player_1, player2=player_2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe game")
    parser.add_argument("--view", type=str, help="Rendering of the game", choices=["gui", "text", "no-view"], default="no-view")
    parser.add_argument("--player1", type=str, help="Player 1", choices=["human", "minimax", "random"], default="random")
    parser.add_argument("--player2", type=str, help="Player 2", choices=["human", "minimax", "random"], default="random")
    args = parser.parse_args()
    main(args)