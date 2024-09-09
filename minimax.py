import numpy as np

def alpha_beta_search(state, max_p: bool) -> float:
    v = minimax(state, alpha=-np.inf, beta=np.inf, max_p=max_p)
    return v


def minimax(state, alpha: float, beta: float, max_p: bool) -> float:
    """"""
    if state.is_win():
        return 1.
    elif state.is_lose():
        return -1.
    elif state.is_tie():
        return 0.
    if max_p:
        v: float = -np.inf
        for successor in state.generate_successors(0):
            v = max(v, minimax(successor, alpha, beta, False))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    else:
        v: float = np.inf
        for successor in state.generate_successors(1):
            v = min(v, minimax(successor, alpha, beta, True))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
