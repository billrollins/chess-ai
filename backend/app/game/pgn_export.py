from chess import Board, Move
from chess.pgn import Game, StringExporter
from datetime import datetime


def board_to_pgn(
    board: Board,
    moves: list[str],
    mode: str = "2player",
    white_player: str = "human",
    black_player: str = "human",
    result: str | None = None,
) -> str:
    """Export a game to PGN string."""
    game = Game()
    game.headers["Event"] = "Chess Game"
    game.headers["Site"] = "chess-ai"
    game.headers["Date"] = datetime.utcnow().strftime("%Y.%m.%d")
    game.headers["White"] = white_player
    game.headers["Black"] = black_player
    game.headers["Result"] = result or "*"

    node = game
    temp_board = Board()
    for uci in moves:
        move = Move.from_uci(uci)
        node = node.add_variation(move)
        temp_board.push(move)

    exporter = StringExporter(headers=True, variations=False, comments=False)
    return game.accept(exporter)
