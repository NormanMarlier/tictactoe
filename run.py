import argparse
from engine import GameState
from agent import RandomAgent
from controller import Controller, HumanController, AgentController, MinimaxController
from gui import View, NoView, TextView, GUIView
from game import GameController


def get_controller_from_option(option: str, index: int) -> Controller:
    
    assert option in ["human", "agent", "minimax"]
    if option == "human":
        return HumanController(index=index)
    elif option == "agent":
        pass
    elif option == "minimax":
        return MinimaxController(index=index)
    else:
        return AgentController(index=index, agent=RandomAgent())


def get_view_from_option(option: str) -> View:
    if option == "gui":
        return GUIView()
    elif option == "text":
        return TextView()
    else:
        return NoView()


def main(args) -> None:

    # Model
    model: GameState = GameState()

    # View
    view: View = get_view_from_option(args.view)
    
    # Controllers
    player_1: Controller = get_controller_from_option(args.agent1, 0)
    player_2: Controller = get_controller_from_option(args.agent2, 1)

    # Game controller
    game: GameController = GameController(model=model,
                                          view=view,
                                          player1=player_1,
                                          player2=player_2)
    # Game loop
    game.game_loop()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tic-Tac-Toe game")
    parser.add_argument("--view", type=str, help="Rendering of the game", choices=["gui", "text", "no-view"], default="no-view")
    parser.add_argument("--player_1", type=str, help="Player 1", choices=["human", "minimax", "random"], default="random")
    parser.add_argument("--player_2", type=str, help="Player 2", choices=["human", "minimax", "random"], default="random")
    args = parser.parse_args()
    main(args)