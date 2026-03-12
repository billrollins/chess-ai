"""AI registry: maps ai_id to AIPlayer class."""
from .base import AIPlayer
from .random_ai import RandomAI
from .greedy_ai import GreedyMaterialAI

AI_REGISTRY: dict[str, type] = {
    "random": RandomAI,
    "greedy": GreedyMaterialAI,
}


def get_ai_player(ai_id: str) -> AIPlayer:
    """Instantiate AI by id. Raises KeyError if unknown."""
    cls = AI_REGISTRY.get(ai_id.lower(), RandomAI)
    return cls()
