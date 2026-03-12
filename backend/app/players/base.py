"""Player abstraction: HumanPlayer and AIPlayer subclasses with async get_move."""
from abc import ABC, abstractmethod
from chess import Board, Move
from typing import Optional


class Player(ABC):
    """Base for all players. Async get_move for future PyTorch model support."""

    @property
    @abstractmethod
    def is_human(self) -> bool:
        """True if move comes from UI/API; False if computed."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name: 'human', 'random', 'greedy', etc."""
        ...

    @abstractmethod
    async def get_move(self, board: Board) -> Optional[Move]:
        """
        Get the next move. Human returns None (move comes from API).
        AI returns a legal Move.
        """
        ...


class HumanPlayer(Player):
    """Move comes from API; get_move is never called for move input."""

    @property
    def is_human(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return "human"

    async def get_move(self, board: Board) -> Optional[Move]:
        return None


class AIPlayer(Player):
    """Base for AI players. Subclasses implement get_move."""

    @property
    def is_human(self) -> bool:
        return False

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def get_move(self, board: Board) -> Optional[Move]:
        """Return a legal move. Must not return None for AI."""
        ...
