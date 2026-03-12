"""RandomAI: picks a random legal move."""
import random
from chess import Board, Move

from .base import AIPlayer


class RandomAI(AIPlayer):
    @property
    def name(self) -> str:
        return "random"

    async def get_move(self, board: Board) -> Move | None:
        moves = list(board.legal_moves)
        if not moves:
            return None
        return random.choice(moves)
