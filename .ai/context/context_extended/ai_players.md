# AI Players

## Location

`backend/app/players/`

## Base (base.py)

- **Player** ABC: `is_human`, `name`, `async get_move(board) -> Move | None`
- **HumanPlayer:** get_move returns None (move from API)
- **AIPlayer:** subclasses implement get_move, return legal Move

## Registry (registry.py)

- `AI_REGISTRY`: { "random": RandomAI, "greedy": GreedyMaterialAI }
- `get_ai_player(ai_id)` → instance

## Implementations

- **RandomAI:** random.choice(list(board.legal_moves))
- **GreedyMaterialAI:** piece values + piece-square table; picks best-scoring move, random among ties

## Invocation

GameManager.make_ai_move → get_ai_player(current_player) → await player.get_move(board) → board.push(move)
