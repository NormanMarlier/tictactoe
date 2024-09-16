import numpy as np
import random
from engine import GameState, Action


class Node:
    def __init__(self, state: GameState, parent: 'Node | None' = None, pos: int | None = None) -> None:
        self.state: GameState = state
        self.parent = parent
        self.children: list['Node'] = []
        self.visits: int = 0
        self.wins: int = 0
        self.pos = pos
    
    def add_child(self, child_state: GameState, pos: int) -> 'Node':
        child: Node = Node(child_state, self, pos)
        self.children.append(child)
        return child
    
    def update(self, result: int) -> None:
        self.visits += 1
        self.wins += result
    
    def is_fully_expanded(self) -> bool:
        return self.state.is_game_over()
    
    def best_child(self, c: float = 1.414) -> 'Node':
        best_score: float = -np.inf
        best_child = self
        for child in self.children:
            score: float = float(child.wins)/float(child.visits) + c * np.sqrt(np.log(self.visits)/child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        
        return best_child


def mcts_simulate(state: GameState, start_index: int) -> float:
    current_state: GameState = state.clone()
    index: int = start_index
    while not current_state.is_game_over():
        possibles_moves = current_state.get_legal_moves()
        move = random.choice(possibles_moves)
        action = Action(agent=index, pos=move)
        current_state = current_state.generate_successor(action)
        index = 1 if index == 0 else 1

    return current_state.evaluate()


def mcts_expand(node: Node, index: int) -> Node:
    """
    Expand the node by creating a new child node for one of the unvisited legal moves.
    
    Returns:
    - Node: The newly added child node.
    """
    legal_moves = node.state.get_legal_moves()
    
    # Generate successors for unexpanded moves
    for move in legal_moves:
        new_state = node.state.generate_successor(Action(agent=index, pos=move))
        child_node = node.add_child(child_state=new_state, pos=move)
        return child_node
    
    raise Exception('No legal moves left to expand.')
    

def mcts_backpropagate(node: Node, result: int) -> None:
    """
    Backpropagate the result of a simulation up the tree, updating the visits and wins.
    
    Parameters:
    - result (int): The outcome of the simulation. 1 for a win, -1 for a loss, 0 for a tie.
    """
    while node is not None:
        node.visits += 1
        if result == 1:
            node.wins += 1
        elif result == -1:
            node.wins -= 1  # You may need to adjust this based on how you're handling wins/losses
        # Move up to the parent node
        node = node.parent


def monte_carlo_tree_search(root: Node, iterations: int, index: int, c: float) -> Node:
    for i in range(iterations):
        node = root
        # Selection: Traverse the tree to the best child
        while not node.state.is_game_over():
            if not node.is_fully_expanded():
                node = mcts_expand(node=node, index=index)
            else:
                node = node.best_child(c=c)        
        # Simulation: Simulate the game starting from this node's state
        result = mcts_simulate(node.state, start_index=index)
        # Backpropagation: Update the nodes along the path
        if index == 1: result *= -1
        mcts_backpropagate(node=node, result=int(result))
        
    
    # Return the best move (child) after the iterations
    return root.best_child(c=0)  # c=0 to select the most visited child (exploit)



