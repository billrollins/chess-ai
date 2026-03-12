"""GreedyMaterialAI: piece values + piece-square table, ~1200 Elo feel."""
import random
from chess import Board, Move, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING

from .base import AIPlayer

PIECE_VALUES = {PAWN: 1, KNIGHT: 3, BISHOP: 3, ROOK: 5, QUEEN: 9, KING: 0}

# Simple center bonus (a1=0, h8=63). Encourages central control.
# Format: 64 values per piece, indexed by square. Positive = good for that square.
def _center_bonus(sq: int) -> int:
    file_idx = sq & 7
    rank_idx = sq >> 3
    # Center files/ranks get bonus
    file_center = abs(file_idx - 3.5)  # 0 at center
    rank_center = abs(rank_idx - 3.5)
    return int(4 - file_center - rank_center)  # max 4 at e4/e5/d4/d5

PST = {}
for pt in [PAWN, KNIGHT, BISHOP, ROOK, QUEEN]:
    PST[pt] = [_center_bonus(sq) for sq in range(64)]
PST[KING] = [0] * 64  # No PST for king


def evaluate_move(board: Board, move: Move) -> float:
    """Score a move: capture value + piece-square bonus."""
    score = 0.0
    captured = board.piece_type_at(move.to_square)
    if captured:
        score += PIECE_VALUES.get(captured, 0)
    piece = board.piece_type_at(move.from_square)
    if piece:
        pst = PST.get(piece, [0] * 64)
        score += pst[move.to_square] - pst[move.from_square]
    return score


class GreedyMaterialAI(AIPlayer):
    @property
    def name(self) -> str:
        return "greedy"

    async def get_move(self, board: Board) -> Move | None:
        moves = list(board.legal_moves)
        if not moves:
            return None
        best_score = max(evaluate_move(board, m) for m in moves)
        best_moves = [m for m in moves if evaluate_move(board, m) == best_score]
        return random.choice(best_moves)
