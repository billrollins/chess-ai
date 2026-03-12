import asyncio
import uuid
from chess import Board, Move, parse_square, QUEEN, ROOK, BISHOP, KNIGHT
from typing import Optional

from ..players import get_ai_player

PROMO_MAP = {"q": QUEEN, "r": ROOK, "b": BISHOP, "n": KNIGHT}


def _players_for_mode(mode: str, ai_id: str) -> tuple[str, str]:
    """Return (white_player, black_player) strings for mode."""
    if mode == "2player":
        return "human", "human"
    if mode == "1vai":
        return "human", ai_id
    if mode == "2ai":
        return ai_id, ai_id
    return "human", "human"


class GameManager:
    """Manages in-memory game state for 2-player, 1vAI, and 2AI modes."""

    def __init__(self):
        self._games: dict[str, dict] = {}

    def create_game(self, mode: str = "2player", ai_id: str = "random") -> dict:
        """Create a new game. Returns game state dict."""
        game_id = str(uuid.uuid4())
        white_player, black_player = _players_for_mode(mode, ai_id)
        board = Board()
        self._games[game_id] = {
            "id": game_id,
            "mode": mode,
            "ai_id": ai_id,
            "board": board,
            "moves": [],
            "result": None,
            "white_player": white_player,
            "black_player": black_player,
        }
        return self._to_response(game_id)

    def get_game(self, game_id: str) -> Optional[dict]:
        """Get game state by ID."""
        if game_id not in self._games:
            return None
        return self._to_response(game_id)

    def make_move(
        self, game_id: str, from_square: str, to_square: str, promotion: Optional[str] = None
    ) -> tuple[Optional[dict], Optional[str]]:
        """
        Attempt to make a move. Returns (game_state, error_message).
        If error_message is set, game_state is None.
        """
        if game_id not in self._games:
            return None, "Game not found"

        data = self._games[game_id]
        board: Board = data["board"]
        is_white = board.turn
        current = data["white_player"] if is_white else data["black_player"]
        if current != "human":
            return None, "Not your turn (AI is thinking)"

        try:
            from_idx = parse_square(from_square.lower())
            to_idx = parse_square(to_square.lower())
        except (ValueError, IndexError) as e:
            return None, str(e)

        promotion_piece = PROMO_MAP.get(promotion.lower()) if promotion else None
        if promotion and not promotion_piece:
            return None, "Invalid promotion piece"

        try:
            move = board.find_move(from_idx, to_idx, promotion_piece)
        except Exception as e:
            return None, "Illegal move"

        board.push(move)
        data["moves"].append(move.uci())

        if board.is_game_over():
            data["result"] = self._result_from_board(board)

        return self._to_response(game_id), None

    async def make_ai_move(
        self, game_id: str, auto: bool = False, delay_ms: int = 500
    ) -> tuple[Optional[dict], Optional[str]]:
        """
        Make one AI move (or all AI moves until human turn / game over if auto=True).
        Returns (game_state, error_message). 1vAI/2AI games save to PGN+SQLite on game end.
        """
        if game_id not in self._games:
            return None, "Game not found"

        data = self._games[game_id]
        board: Board = data["board"]
        white_player = data["white_player"]
        black_player = data["black_player"]

        while True:
            is_white_turn = board.turn
            current_player = white_player if is_white_turn else black_player

            if current_player == "human":
                if not auto:
                    return None, "Not AI's turn"
                break

            player = get_ai_player(current_player)
            move = await player.get_move(board)
            if move is None or move not in board.legal_moves:
                return None, "AI returned invalid move"

            board.push(move)
            data["moves"].append(move.uci())

            if board.is_game_over():
                data["result"] = self._result_from_board(board)
                return self._to_response(game_id), None

            if not auto:
                return self._to_response(game_id), None

            await asyncio.sleep(delay_ms / 1000.0)

        return self._to_response(game_id), None

    def _result_from_board(self, board: Board) -> str:
        if board.is_checkmate():
            return "0-1" if board.turn else "1-0"
        if board.is_stalemate() or board.is_insufficient_material() or board.can_claim_fifty_moves():
            return "1/2-1/2"
        if board.is_repetition():
            return "1/2-1/2"
        return "*"

    def _to_response(self, game_id: str) -> dict:
        data = self._games[game_id]
        board: Board = data["board"]
        return {
            "id": game_id,
            "mode": data["mode"],
            "fen": board.fen(),
            "turn": "white" if board.turn else "black",
            "result": data["result"],
            "moves": data["moves"].copy(),
            "white_player": data["white_player"],
            "black_player": data["black_player"],
        }

    def get_board_for_pgn(self, game_id: str) -> Optional[Board]:
        """Get the chess Board for PGN export."""
        if game_id not in self._games:
            return None
        return self._games[game_id]["board"]

    def get_game_data(self, game_id: str) -> Optional[dict]:
        """Get raw game data for storage."""
        return self._games.get(game_id)
