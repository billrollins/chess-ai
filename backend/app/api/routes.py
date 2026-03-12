from pathlib import Path

from fastapi import APIRouter, HTTPException

from ..models import GameCreate, GameResponse, MoveRequest
from ..game import GameManager
from ..game.pgn_export import board_to_pgn
from ..storage import GameStorage

router = APIRouter()
game_manager = GameManager()
_project_root = Path(__file__).resolve().parent.parent.parent.parent
storage = GameStorage(
    games_dir=str(_project_root / "games"),
    db_path=str(_project_root / "chess.db"),
)


@router.post("/games", response_model=GameResponse)
def create_game(body: GameCreate):
    """Create a new game. Mode: 2player | 1vai | 2ai. ai_id: random | greedy."""
    state = game_manager.create_game(mode=body.mode, ai_id=body.ai_id)
    return state


@router.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str):
    """Get current game state."""
    state = game_manager.get_game(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")
    return state


@router.post("/games/{game_id}/move", response_model=GameResponse)
def make_move(game_id: str, body: MoveRequest):
    """Make a move. Returns updated game state or error."""
    state, error = game_manager.make_move(
        game_id,
        body.from_square,
        body.to_square,
        body.promotion,
    )
    if error:
        raise HTTPException(status_code=400, detail=error)

    if state["result"] and state["result"] != "*":
        _save_game_to_storage(game_id)

    return state


@router.post("/games/{game_id}/ai-move", response_model=GameResponse)
async def ai_move(game_id: str, auto: bool = False, delay_ms: int = 500):
    """
    Make AI move(s). If auto=True, run all AI moves until human turn or game over (delay_ms between moves).
    1vAI/2AI games save to PGN+SQLite on game end, same as 2-player.
    """
    state, error = await game_manager.make_ai_move(game_id, auto=auto, delay_ms=delay_ms)
    if error:
        raise HTTPException(status_code=400, detail=error)

    if state["result"] and state["result"] != "*":
        _save_game_to_storage(game_id)

    return state


def _save_game_to_storage(game_id: str):
    """Persist finished game to PGN + SQLite."""
    data = game_manager.get_game_data(game_id)
    if not data:
        return
    board = data["board"]
    pgn = board_to_pgn(
        board,
        data["moves"],
        mode=data["mode"],
        white_player=data["white_player"],
        black_player=data["black_player"],
        result=data["result"],
    )
    storage.save_game(
        game_id=game_id,
        mode=data["mode"],
        white_player=data["white_player"],
        black_player=data["black_player"],
        result=data["result"],
        pgn_content=pgn,
    )


@router.get("/games")
def list_games(limit: int = 50, offset: int = 0):
    """List saved games (finished games only)."""
    games = storage.list_games(limit=limit, offset=offset)
    total = storage.count_games()
    return {"games": games, "total": total}


@router.get("/games/{game_id}/replay")
def get_replay(game_id: str):
    """Get game for replay (PGN + move list). For saved games."""
    meta = storage.get_game_metadata(game_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Game not found")
    pgn = storage.get_pgn_content(game_id)
    if not pgn:
        raise HTTPException(status_code=404, detail="PGN not found")
    return {"metadata": meta, "pgn": pgn}
