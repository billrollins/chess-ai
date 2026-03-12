from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GameCreate(BaseModel):
    mode: str = "2player"  # 2player | 1vai | 2ai
    ai_id: str = "random"  # random | greedy (for AI sides)


class MoveRequest(BaseModel):
    from_square: str  # e.g. "e2"
    to_square: str    # e.g. "e4"
    promotion: Optional[str] = None  # q|r|b|n for pawn promotion


class GameResponse(BaseModel):
    id: str
    mode: str
    fen: str
    turn: str  # "white" | "black"
    result: Optional[str] = None  # 1-0 | 0-1 | 1/2-1/2 | None if ongoing
    moves: list[str]
    white_player: str = "human"
    black_player: str = "human"
    created_at: Optional[datetime] = None


class GameListResponse(BaseModel):
    games: list[GameResponse]
    total: int
